"""W-IND-31: INA301 open-drain ALERT / enable polarity hazard screen.

Original, digital-only abstraction. The INA301 ALERT pin is open-drain,
active LOW on an over-limit condition (TI INA301 product/datasheet).
An idle high-Z or conservatively modelled unpowered high-Z is NOT a
positive proof that the current monitor is alive. No hardware validated.
"""
from dataclasses import dataclass
from itertools import product
import json
import unittest


@dataclass(frozen=True)
class Sample:
    source: bool = True
    monitor_power: bool = True
    overcurrent: bool = False
    temp_ok: bool = True
    fod_ok: bool = True
    pg_a: bool = True
    pg_b: bool = True
    a_stuck_closed: bool = False
    b_stuck_closed: bool = False


def direct_alert_enable(s: Sample) -> bool:
    """ANTI-PATTERN: pull-up makes EN high unless ALERT actively sinks."""
    alert_sinks = s.monitor_power and s.overcurrent
    return s.source and not alert_sinks


class PositivePermissionModel:
    """IDEAL contract, not a hardware circuit: two positive enables.

    Each cut is normally open in this model. Both must close for load power.
    Each driver is assumed to fail off on loss of its qualification supply;
    real transistor, POR, delay, backfeed and comparator characteristics
    remain unqualified. State is initially tripped; RF cannot rearm.
    """
    def __init__(self):
        self.tripped = True
        self.previous_local = False

    def step(self, s: Sample, *, local_rearm=False, radio_rearm=False):
        qualified = (s.source and s.monitor_power and not s.overcurrent
                     and s.temp_ok and s.fod_ok and s.pg_a and s.pg_b)
        rising_local = local_rearm and not self.previous_local
        self.previous_local = local_rearm
        if not qualified:
            self.tripped = True
        elif rising_local:
            self.tripped = False
        # radio_rearm is deliberately ignored: no RF-controlled safety reset.
        en_a = qualified and not self.tripped
        en_b = qualified and not self.tripped
        closed_a = s.a_stuck_closed or en_a
        closed_b = s.b_stuck_closed or en_b
        return {
            'qualified': qualified, 'latched_trip': self.tripped,
            'en_a': en_a, 'en_b': en_b,
            'load_powered': s.source and closed_a and closed_b,
        }


class DigitalChecks(unittest.TestCase):
    def _armed(self):
        x = PositivePermissionModel()
        self.assertTrue(x.step(Sample(), local_rearm=True)['load_powered'])
        x.step(Sample(), local_rearm=False)
        return x

    def test_01_normal_idle_alert_is_not_a_health_proof(self):
        self.assertTrue(direct_alert_enable(Sample()))

    def test_02_unpowered_monitor_can_leave_pullup_high(self):
        self.assertTrue(direct_alert_enable(Sample(monitor_power=False)))

    def test_03_active_low_alert_catches_overcurrent_if_powered(self):
        self.assertFalse(direct_alert_enable(Sample(overcurrent=True)))

    def test_04_start_inhibited(self):
        self.assertFalse(PositivePermissionModel().step(Sample())['load_powered'])

    def test_05_monitor_brownout_latches_both_off(self):
        x = self._armed()
        out = x.step(Sample(monitor_power=False))
        self.assertFalse(out['en_a'] or out['en_b'])
        self.assertFalse(out['load_powered'])

    def test_06_restored_power_does_not_rearm(self):
        x = self._armed()
        x.step(Sample(monitor_power=False))
        self.assertFalse(x.step(Sample())['load_powered'])

    def test_07_rf_never_rearms(self):
        x = PositivePermissionModel()
        self.assertFalse(x.step(Sample(), radio_rearm=True)['load_powered'])

    def test_08_local_rearm_requires_new_edge(self):
        x = PositivePermissionModel()
        self.assertTrue(x.step(Sample(), local_rearm=True)['load_powered'])
        x.step(Sample(overcurrent=True), local_rearm=True)
        self.assertFalse(x.step(Sample(), local_rearm=True)['load_powered'])
        x.step(Sample(), local_rearm=False)
        self.assertTrue(x.step(Sample(), local_rearm=True)['load_powered'])

    def test_09_individual_trip_causes_dual_inhibit(self):
        for name in ('monitor_power', 'temp_ok', 'fod_ok', 'pg_a', 'pg_b'):
            x = self._armed()
            self.assertFalse(x.step(Sample(**{name: False}))['load_powered'], name)
        self.assertFalse(self._armed().step(Sample(overcurrent=True))['load_powered'])

    def test_10_one_closed_switch_cannot_bypass_trip_in_ideal_model(self):
        for side in ('a_stuck_closed', 'b_stuck_closed'):
            self.assertFalse(self._armed().step(Sample(overcurrent=True, **{side: True}))['load_powered'])

    def test_11_two_closed_switches_remain_unsafe(self):
        s = Sample(monitor_power=False, a_stuck_closed=True, b_stuck_closed=True)
        self.assertTrue(self._armed().step(s)['load_powered'])

    def test_12_256_fault_combinations_exhaustive(self):
        fields = ('monitor_power', 'overcurrent', 'temp_ok', 'fod_ok',
                  'pg_a', 'pg_b', 'a_stuck_closed', 'b_stuck_closed')
        for vals in product((False, True), repeat=len(fields)):
            data = dict(zip(fields, vals))
            x = self._armed()
            out = x.step(Sample(**data))
            bad = (not data['monitor_power'] or data['overcurrent'] or
                   not data['temp_ok'] or not data['fod_ok'] or
                   not data['pg_a'] or not data['pg_b'])
            if bad and not (data['a_stuck_closed'] and data['b_stuck_closed']):
                self.assertFalse(out['load_powered'], str(data))


def evidence():
    fields = ('monitor_power', 'overcurrent', 'temp_ok', 'fod_ok',
              'pg_a', 'pg_b', 'a_stuck_closed', 'b_stuck_closed')
    total = unsafe_double_stuck = allowed_single_fault = 0
    for vals in product((False, True), repeat=len(fields)):
        d = dict(zip(fields, vals))
        x = PositivePermissionModel()
        x.step(Sample(), local_rearm=True)
        x.step(Sample())
        out = x.step(Sample(**d))
        total += 1
        bad = not (d['monitor_power'] and not d['overcurrent'] and d['temp_ok']
                   and d['fod_ok'] and d['pg_a'] and d['pg_b'])
        if bad and out['load_powered']:
            if d['a_stuck_closed'] and d['b_stuck_closed']:
                unsafe_double_stuck += 1
            else:
                allowed_single_fault += 1
    return {'model': 'digital-only; no real circuits, no hardware safety proof',
            'cases': total,
            'unsafe_double_stuck_in_bad_state': unsafe_double_stuck,
            'unexpected_energized_with_at_most_one_stuck': allowed_single_fault,
            'naive_unpowered_monitor_en_high': direct_alert_enable(Sample(monitor_power=False))}


if __name__ == '__main__':
    print(json.dumps(evidence(), sort_keys=True, indent=2))
