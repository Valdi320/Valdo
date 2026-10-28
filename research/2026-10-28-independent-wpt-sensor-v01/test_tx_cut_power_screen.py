"""Deterministic offline fault-injection tests of W-IND-08 only."""
import itertools
import math
import unittest

from tx_cut_power_screen import (
    Fault, Interlocks, Switch, evaluate, bleeder, prospective_shunt,
    series_switch_loss,
)


def ready() -> Interlocks:
    return Interlocks(True, True, True, True, True, True, True, True, True)


class PowerCutTests(unittest.TestCase):
    def test_default_fails_closed(self):
        self.assertFalse(evaluate(Interlocks(), Switch(), Switch()).supply_to_tx)

    def test_hypothetical_healthy_permit(self):
        self.assertTrue(evaluate(ready(), Switch(), Switch()).supply_to_tx)

    def test_any_missing_interlock_blocks_both(self):
        raw = vars(ready())
        for key in raw:
            with self.subTest(key=key):
                c = dict(raw)
                c[key] = False
                o = evaluate(Interlocks(**c), Switch(), Switch())
                self.assertFalse(o.command_on)
                self.assertFalse(o.supply_to_tx)

    def test_metal_unknown_never_permits(self):
        x = dict(vars(ready()))
        x['fod_proven_clear'] = False
        self.assertFalse(evaluate(Interlocks(**x), Switch(), Switch()).supply_to_tx)

    def test_single_closed_contact_cannot_override_inhibit(self):
        deny = Interlocks(source_ok=True)
        for state in (Fault.CLOSED, Fault.ENABLE_HIGH):
            self.assertFalse(evaluate(deny, Switch(state), Switch()).supply_to_tx)
            self.assertFalse(evaluate(deny, Switch(), Switch(state)).supply_to_tx)

    def test_one_fault_exhaustive(self):
        deny = Interlocks(source_ok=True)
        for fa, fb in itertools.product(Fault, repeat=2):
            if fa in (Fault.HEALTHY, Fault.OPEN) or fb in (Fault.HEALTHY, Fault.OPEN):
                self.assertFalse(evaluate(deny, Switch(fa), Switch(fb)).supply_to_tx)

    def test_two_welds_are_unsafe(self):
        self.assertTrue(evaluate(Interlocks(source_ok=True), Switch(Fault.CLOSED),
                                 Switch(Fault.CLOSED)).supply_to_tx)

    def test_two_enabled_pins_stuck_high_are_unsafe(self):
        self.assertTrue(evaluate(Interlocks(source_ok=True), Switch(Fault.ENABLE_HIGH),
                                 Switch(Fault.ENABLE_HIGH)).supply_to_tx)

    def test_one_weld_with_active_qod_makes_supply_shunt(self):
        o = evaluate(Interlocks(source_ok=True), Switch(Fault.CLOSED, True), Switch())
        self.assertFalse(o.supply_to_tx)
        self.assertTrue(o.supply_to_qod_a)

    def test_disabled_qod_prevents_modelled_self_shunt(self):
        o = evaluate(Interlocks(source_ok=True), Switch(Fault.CLOSED, False), Switch())
        self.assertFalse(o.any_sustained_qod_shunt)

    def test_healthy_disabled_qod_not_shunt(self):
        o = evaluate(Interlocks(source_ok=True), Switch(Fault.HEALTHY, True), Switch())
        self.assertFalse(o.any_sustained_qod_shunt)

    def test_single_enable_high_not_the_same_as_qod_short(self):
        o = evaluate(Interlocks(source_ok=True), Switch(Fault.ENABLE_HIGH, True), Switch())
        self.assertFalse(o.any_sustained_qod_shunt)

    def test_b_weld_and_a_weld_has_two_possible_shunts(self):
        o = evaluate(Interlocks(source_ok=True), Switch(Fault.CLOSED, True),
                     Switch(Fault.CLOSED, True))
        self.assertTrue(o.supply_to_qod_a)
        self.assertTrue(o.supply_to_qod_b)

    def test_source_absent_has_no_forward_supply(self):
        o = evaluate(Interlocks(), Switch(Fault.CLOSED, True), Switch(Fault.CLOSED, True))
        self.assertFalse(o.supply_to_tx)
        self.assertFalse(o.any_sustained_qod_shunt)

    def test_rc_100uF_to_half_volt(self):
        r = bleeder(5, .5, 1000, 100e-6)
        self.assertAlmostEqual(r['seconds_to_target'], .2302585092994046)
        self.assertLess(r['seconds_to_target'], .5)
        self.assertAlmostEqual(r['permanent_current_a'], .005)
        self.assertAlmostEqual(r['permanent_bleeder_w'], .025)

    def test_rc_470uF_does_not_meet_half_second(self):
        self.assertGreater(bleeder(5, .5, 1000, 470e-6)['seconds_to_target'], .5)

    def test_bleeder_preserves_finite_energy(self):
        self.assertAlmostEqual(bleeder(5, .5, 1000, 100e-6)['initial_stored_j'], .00125)

    def test_bleeder_rejects_invalid(self):
        for args in ((5, 5, 1000, 1e-4), (5, .5, 0, 1e-4),
                     (5, .5, 1000, -1), (float('nan'), .5, 1000, 1e-4)):
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    bleeder(*args)

    def test_illustrative_qod_power(self):
        self.assertEqual(prospective_shunt(5, 200), (.025, .125))

    def test_invalid_qod_values(self):
        for v, r in ((5, 0), (5, -1), (-5, 200), (math.inf, 200)):
            with self.assertRaises(ValueError):
                prospective_shunt(v, r)

    def test_nominal_switch_loss(self):
        data = series_switch_loss(5, 1)
        self.assertAlmostEqual(data['series_drop_v'], .104)
        self.assertAlmostEqual(data['series_loss_w'], .104)
        self.assertAlmostEqual(data['load_voltage_v_typical'], 4.896)

    def test_12v_dock_excluded(self):
        with self.assertRaises(ValueError):
            series_switch_loss(12, 1)

    def test_overcurrent_excluded(self):
        with self.assertRaises(ValueError):
            series_switch_loss(5, 2.5)

    def test_power_screen_extreme_invalid(self):
        for x in (-1, math.inf, math.nan):
            with self.assertRaises(ValueError):
                series_switch_loss(5, x)

    def test_enumerate_16_fault_pairs_no_qod_shunt(self):
        deny = Interlocks(source_ok=True)
        for fa, fb in itertools.product(Fault, repeat=2):
            self.assertFalse(evaluate(deny, Switch(fa), Switch(fb)).any_sustained_qod_shunt)


if __name__ == '__main__':
    unittest.main()
