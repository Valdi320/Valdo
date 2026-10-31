#!/usr/bin/env python3
"""W-IND-50: fail-closed, unenergised model for paired INA219 single-shot readings.

Original work, Python stdlib only. Not a driver and not safety control.
Register layout follows TI INA219 datasheet Rev.G.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from decimal import Decimal, InvalidOperation
from hashlib import sha256
import argparse
import json

CONVERSION_BOTH_MS = Decimal('17.02')
MAX_TRIGGER_SKEW_MS = Decimal('5')
MAX_READ_SKEW_MS = Decimal('5')
MAX_READY_READ_MS = Decimal('8')
MAX_READ_AGE_MS = Decimal('10')
MIN_CONVERSION_FUZZ_MS = Decimal('0.20')


class DataRejected(ValueError):
    """Rejected metrology record; NOT a physical cutoff."""


def decimal(value: object, label: str) -> Decimal:
    if isinstance(value, bool):
        raise DataRejected(label + ': bool is not a measurement')
    try:
        d = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise DataRejected(label + ': not numeric') from None
    if not d.is_finite():
        raise DataRejected(label + ': nonfinite')
    return d


@dataclass(frozen=True)
class RawSample:
    node: str
    sequence: int
    run_id: str
    clock_id: str
    trigger_ms: object
    ready_ms: object
    read_ms: object
    cnvr_low_after_trigger: bool
    shunt_reg_16: int
    bus_reg_16: int
    power_reg_read_after: bool
    shunt_milliohm: object
    single_shot_shunt_bus_mode: bool = True


def decode(sample: RawSample):
    """Decode raw registers, never trust uncalibrated CURRENT/POWER registers."""
    if sample.node not in ('TX', 'RX'):
        raise DataRejected('unknown node')
    if not sample.run_id or not sample.clock_id:
        raise DataRejected('missing provenance/clock')
    if type(sample.sequence) is not int or sample.sequence < 0:
        raise DataRejected('invalid sequence')
    for n, v in [('trigger mode', sample.single_shot_shunt_bus_mode),
                 ('CNVR low post trigger', sample.cnvr_low_after_trigger),
                 ('POWER register read', sample.power_reg_read_after)]:
        if v is not True:
            raise DataRejected(n + ' unverified')
    for n, v in [('shunt', sample.shunt_reg_16), ('bus', sample.bus_reg_16)]:
        if type(v) is not int or not 0 <= v <= 65535:
            raise DataRejected(n + ' register not uint16')
    if not (sample.bus_reg_16 & 2):
        raise DataRejected('CNVR not ready; old conversion possible')
    if sample.bus_reg_16 & 1:
        raise DataRejected('OVF; current/power may be meaningless')
    trigger = decimal(sample.trigger_ms, 'trigger_ms')
    ready = decimal(sample.ready_ms, 'ready_ms')
    read = decimal(sample.read_ms, 'read_ms')
    if not trigger <= ready <= read:
        raise DataRejected('noncausal timestamps')
    if ready - trigger < CONVERSION_BOTH_MS - MIN_CONVERSION_FUZZ_MS:
        raise DataRejected('ready earlier than configured two ADC conversions')
    if read - ready > MAX_READY_READ_MS:
        raise DataRejected('stale ready-to-read interval')
    shunt_mohm = decimal(sample.shunt_milliohm, 'shunt_milliohm')
    if not Decimal('10') <= shunt_mohm <= Decimal('200'):
        raise DataRejected('shunt not qualified by W50 design range')
    signed_shunt = sample.shunt_reg_16 if sample.shunt_reg_16 < 32768 else sample.shunt_reg_16 - 65536
    shunt_v = Decimal(signed_shunt) * Decimal('0.00001')
    current_a = shunt_v / (shunt_mohm / Decimal('1000'))
    bus_v = Decimal(sample.bus_reg_16 >> 3) * Decimal('0.004')
    if bus_v <= 0 or current_a <= 0:
        raise DataRejected('not a forward, positive-power resistive load')
    power_bus_w = bus_v * current_a
    power_before_shunt_w = (bus_v + shunt_v) * current_a
    if power_before_shunt_w <= 0:
        raise DataRejected('unphysical source power')
    return {
        'node': sample.node, 'sequence': sample.sequence,
        'trigger_ms': trigger, 'ready_ms': ready, 'read_ms': read,
        'current_a': current_a, 'bus_v': bus_v,
        'power_bus_w': power_bus_w,
        'power_before_shunt_w': power_before_shunt_w,
        'shunt_loss_w': power_before_shunt_w - power_bus_w,
    }


class PairedGate:
    """Atomic validation: rejection never advances either sequence."""
    def __init__(self, run_id: str):
        self.run_id = run_id
        self.last_sequences = {'TX': -1, 'RX': -1}
        self.last_triggers = {'TX': Decimal('-1'), 'RX': Decimal('-1')}

    def accept(self, tx: RawSample, rx: RawSample, collection_ms: object,
               source_kind: str = 'synthetic') -> dict:
        if source_kind != 'synthetic':
            raise DataRejected('no measured-data accreditation in W50')
        if tx.node != 'TX' or rx.node != 'RX':
            raise DataRejected('TX/RX roles missing')
        if tx.run_id != self.run_id or rx.run_id != self.run_id:
            raise DataRejected('mixed or unknown run')
        if tx.clock_id != rx.clock_id:
            raise DataRejected('independent clocks without synchronisation')
        a, b = decode(tx), decode(rx)
        for obj in (a, b):
            node = obj['node']
            if obj['sequence'] != self.last_sequences[node] + 1:
                raise DataRejected('duplicate, missing, or reordered conversion sequence')
            if obj['trigger_ms'] <= self.last_triggers[node]:
                raise DataRejected('nonmonotonic trigger')
        now = decimal(collection_ms, 'collection_ms')
        if max(a['read_ms'], b['read_ms']) > now:
            raise DataRejected('collection before read completion')
        for obj in (a, b):
            if now - obj['read_ms'] > MAX_READ_AGE_MS:
                raise DataRejected('stale sample at collection')
        if abs(a['trigger_ms'] - b['trigger_ms']) > MAX_TRIGGER_SKEW_MS:
            raise DataRejected('TX/RX triggers not aligned')
        if abs(a['read_ms'] - b['read_ms']) > MAX_READ_SKEW_MS:
            raise DataRejected('TX/RX reads too far apart')
        eta = b['power_bus_w'] / a['power_before_shunt_w']
        if eta > 1:
            raise DataRejected('apparent >100% efficiency: measurement error/phase/calibration')
        self.last_sequences = {'TX': tx.sequence, 'RX': rx.sequence}
        self.last_triggers = {'TX': a['trigger_ms'], 'RX': b['trigger_ms']}
        return {
            'run_id': self.run_id, 'seq': tx.sequence,
            'tx_source_w': str(a['power_before_shunt_w']),
            'tx_shunt_loss_w': str(a['shunt_loss_w']),
            'rx_load_w': str(b['power_bus_w']),
            'link_efficiency_percent_nominal': str((eta * 100).quantize(Decimal('0.001'))),
            'measurement_kind': 'SYNTHETIC_ONLY',
            'shunt_actual_resistance_measured': False,
            'clock_alignment_measured': False,
            'uncertainty_calibrated': False,
            'fod_verified': False, 'emi_verified': False,
            'hardware_approved': False, 'lithium_dock_approved': False,
        }


def example_samples():
    tx = RawSample('TX', 0, 'demo-w50', 'host-monotonic-assumed',
                   '0', '17.05', '18.00', True, 800, (1250 << 3) | 2, True, '100')
    rx = RawSample('RX', 0, 'demo-w50', 'host-monotonic-assumed',
                   '1', '18.05', '19.00', True, 800, (1000 << 3) | 2, True, '100')
    return tx, rx


def demo():
    tx, rx = example_samples()
    positive = PairedGate('demo-w50').accept(tx, rx, '20')
    cases = {
        'no_cnvr_low': (replace(tx, cnvr_low_after_trigger=False), rx),
        'no_ready': (replace(tx, bus_reg_16=tx.bus_reg_16 & ~2), rx),
        'overflow': (replace(tx, bus_reg_16=tx.bus_reg_16 | 1), rx),
        'stale': (tx, rx),
        'clock_mismatch': (replace(tx, clock_id='clock-A'), replace(rx, clock_id='clock-B')),
        'impossible_efficiency': (tx, replace(rx, bus_reg_16=(1500 << 3) | 2)),
    }
    rejected = {}
    for name, (a, b) in cases.items():
        try:
            PairedGate('demo-w50').accept(a, b, '40' if name == 'stale' else '20')
            rejected[name] = 'BUG_ACCEPTED'
        except DataRejected as exc:
            rejected[name] = str(exc)
    source = json.dumps({'positive': positive, 'rejected': rejected}, sort_keys=True)
    return {'title': 'W50-SYNTHETIC-NOT-HARDWARE', 'positive': positive,
            'rejections': rejected, 'payload_sha256': sha256(source.encode()).hexdigest(),
            'sources': ['https://www.ti.com/product/INA219',
                        'https://github.com/Valdi320/Valdo/pull/9'],
            'physical_tests': 0, 'purchase_eur': 0}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--demo', action='store_true')
    parser.add_argument('--out')
    args = parser.parse_args()
    if args.demo:
        output = json.dumps(demo(), indent=2, sort_keys=True) + '\n'
        if args.out:
            with open(args.out, 'w', encoding='utf-8') as file:
                file.write(output)
        else:
            print(output)
