#!/usr/bin/env python3
"""W-IND-49: cheap INA219 bench-meter timing + shunt screening (NOT a safety gate).

Only compares stated engineering assumptions to datasheet conversion times. It
cannot validate physical synchronization, radio, metal/FOD, lithium charging,
or protection. No third-party code is included. Python standard library only.
"""
import argparse
import hashlib
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

# TI INA219 SBOS448G, Table 5: conversion time per ADC (shunt or bus), 12-bit.
# With both shunt and bus sampled, continuous conversions can take about 2x.
CONVERSION_MS = {
    1: '0.532', 2: '1.06', 4: '2.13', 8: '4.26',
    16: '8.51', 32: '17.02', 64: '34.05', 128: '68.10',
}
SOURCE = 'https://www.ti.com/lit/ds/symlink/ina219.pdf'
BLOCKERS = [
    'No physical TX/RX synchronized capture or shunt calibration',
    'Conversion-ready/I2C timestamp accuracy and ADC noise unmeasured',
    'Manufacturer internal conversion times are not RF ripple/EMI measurements',
    'Independent normally-OFF cuts, thermal/FOD/offset/wetness remain unverified',
    'Lithium battery, BMS and charging dock excluded from bench',
]

def decimal(value, name):
    if isinstance(value, bool):
        raise ValueError('invalid '+name)
    try:
        out = Decimal(str(value))
    except (TypeError, InvalidOperation, ValueError) as exc:
        raise ValueError('invalid '+name) from exc
    if not out.is_finite():
        raise ValueError('nonfinite '+name)
    return out


def evaluate(cfg):
    if not isinstance(cfg, dict):
        raise ValueError('configuration must be a dict')
    mode = cfg.get('mode')
    if mode not in ('synthetic', 'measured'):
        raise ValueError('mode must be synthetic or measured')
    if mode == 'measured':
        for k in ('calibration_ref','shunt_resistance_measurement_ref',
                  'physical_clock_capture_ref','hardware_revision'):
            if not isinstance(cfg.get(k),str) or not cfg[k].strip():
                raise ValueError('measured requires '+k)
        if cfg.get('battery_disconnected') is not True or cfg.get('source_kind') != 'isolated_current_limited' or cfg.get('load_kind') != 'resistive':
            raise ValueError('measured mode requires isolated current-limited resistive bench declarations')
    n = cfg.get('samples_averaged')
    if type(n) is not int or n not in CONVERSION_MS:
        raise ValueError('invalid INA219 samples_averaged')
    names = ('shunt_ohm','probe_current_min_a','peak_current_a',
             'bus_voltage_v','sampling_period_ms','max_host_pair_skew_ms',
             'max_effective_skew_ms','max_offset_uv','max_offset_fraction')
    v = {k:decimal(cfg.get(k),k) for k in names}
    if any(v[k] <= 0 for k in ('shunt_ohm','probe_current_min_a','peak_current_a','bus_voltage_v','sampling_period_ms','max_effective_skew_ms','max_offset_uv','max_offset_fraction')):
        raise ValueError('nonpositive physical parameter')
    if v['max_host_pair_skew_ms'] < 0 or v['max_offset_fraction'] >= 1:
        raise ValueError('negative skew or unrealistic offset fraction')
    if v['peak_current_a'] < v['probe_current_min_a'] or v['bus_voltage_v'] > 26:
        raise ValueError('inconsistent current or out-of-range INA219 bus')
    conversion = Decimal(CONVERSION_MS[n])
    # Deliberately conservative *candidate* allowance, NOT a proof of physical
    # capture phase: shunt and bus ADCs convert at different times. Without
    # conversion-ready capture and independent timestamp verification, reject
    # any assertion of measured physical synchronization.
    two_conversions = conversion*2
    phase_budget = v['max_host_pair_skew_ms'] + two_conversions
    time_pass = (v['sampling_period_ms'] >= two_conversions and
                 phase_budget <= v['max_effective_skew_ms'])
    drop_mv = v['probe_current_min_a']*v['shunt_ohm']*1000
    peak_drop_mv = v['peak_current_a']*v['shunt_ohm']*1000
    # Input offset max: 50uV *only if actual B-grade INA219 and its specific
    # conditions are verified*. The offset fraction is a single contribution;
    # it EXCLUDES voltage gain, shunt tolerance, temperature, noise and clocks.
    offset_fraction = v['max_offset_uv']/(v['probe_current_min_a']*v['shunt_ohm']*1000000)
    shunt_pass = offset_fraction <= v['max_offset_fraction'] and peak_drop_mv <= 40
    screen_pass = bool(time_pass and shunt_pass)
    return {
        'evidence_class':mode,
        'chosen_adc_averaging':n,
        'per_adc_conversion_ms':str(conversion),
        'both_adc_conversion_ms':str(two_conversions),
        'sample_period_ms':str(v['sampling_period_ms']),
        'host_pair_skew_allowance_ms':str(v['max_host_pair_skew_ms']),
        'candidate_time_envelope_ms':str(phase_budget),
        'screen_time_budget_ms':str(v['max_effective_skew_ms']),
        'time_screen_pass':bool(time_pass),
        'probe_shunt_drop_mv':str(drop_mv),
        'peak_shunt_drop_mv':str(peak_drop_mv),
        'offset_error_contribution_fraction':str(offset_fraction),
        'offset_error_limit_fraction':str(v['max_offset_fraction']),
        'shunt_screen_pass':bool(shunt_pass),
        'candidate_screen_pass':screen_pass,
        'decision':'DIGITAL_CANDIDATE_ONLY' if screen_pass else 'REJECT_OR_REMEASURE',
        'hardware_approved':False,
        'lithium_dock_approved':False,
        'source_timing':SOURCE,
        'blockers':BLOCKERS,
        'assumptions_note': ('Envelope presumes an assigned host-skew upper bound and covers two sequential ADC times; not a calibrated synchronization guarantee. Input offset alone is never total accuracy; this does NOT establish FOD.'),
        'config_sha256':hashlib.sha256(json.dumps(cfg,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),
    }


def demo():
    shared = {
        'mode':'synthetic', 'probe_current_min_a':'0.08',
        'peak_current_a':'0.30', 'bus_voltage_v':'5',
        'sampling_period_ms':'50', 'max_host_pair_skew_ms':'5',
        'max_effective_skew_ms':'25','max_offset_uv':'50',
        'max_offset_fraction':'0.02',
    }
    return {
        'zero_hardware_trials':True,
        'examples':{
            'assembled_100mohm_16avg':evaluate({**shared,'shunt_ohm':'0.1','samples_averaged':16}),
            'high_current_10mohm_16avg':evaluate({**shared,'shunt_ohm':'0.01','samples_averaged':16}),
            'slow_100mohm_128avg':evaluate({**shared,'shunt_ohm':'0.1','samples_averaged':128}),
            'fast_100mohm_1avg':evaluate({**shared,'shunt_ohm':'0.1','samples_averaged':1}),
        }
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--demo',action='store_true')
    parser.add_argument('--config',type=Path)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    if args.demo == bool(args.config):
        parser.error('choose exactly one of --demo or --config')
    payload=demo() if args.demo else evaluate(json.loads(args.config.read_text(encoding='utf-8')))
    body=json.dumps(payload,indent=2,sort_keys=True,ensure_ascii=False)+'\n'
    if args.out: args.out.write_text(body,encoding='utf-8')
    else: print(body,end='')

if __name__=='__main__':main()
