"""W-IND-11 offline tests: analytic identities, bounds, and input rejection."""
import math
import unittest
from dataclasses import replace
from standby_energy_screen import Scenario, screen, standby_budget_pass, part_floor_eur


class StandbyScreenTests(unittest.TestCase):
    def setUp(self):
        self.s = Scenario(8, 5.0, .030, .050, 24.0, .005)

    def test_vendor_min_power(self): self.assertAlmostEqual(screen(self.s).all_on_no_load_w_min, 1.2)
    def test_vendor_max_power(self): self.assertAlmostEqual(screen(self.s).all_on_no_load_w_max, 2.0)
    def test_vendor_one_module_low(self): self.assertAlmostEqual(screen(replace(self.s, modules=1)).all_on_no_load_w_min, .15)
    def test_vendor_one_module_high(self): self.assertAlmostEqual(screen(replace(self.s, modules=1)).all_on_no_load_w_max, .25)
    def test_day_low(self): self.assertAlmostEqual(screen(self.s).always_on_absent_wh_day_min, 28.8)
    def test_day_high(self): self.assertAlmostEqual(screen(self.s).always_on_absent_wh_day_max, 48.0)
    def test_gated_off_power(self): self.assertAlmostEqual(screen(self.s).all_off_assumed_w, .04)
    def test_gated_off_energy(self): self.assertAlmostEqual(screen(self.s).gated_absent_wh_day, .96)
    def test_saved_low(self): self.assertAlmostEqual(screen(self.s).saved_absent_wh_day_min, 27.84)
    def test_saved_high(self): self.assertAlmostEqual(screen(self.s).saved_absent_wh_day_max, 47.04)
    def test_zero_absence(self): self.assertEqual(screen(replace(self.s, absent_hours_per_day=0)).saved_absent_wh_day_max, 0)
    def test_half_absence(self): self.assertAlmostEqual(screen(replace(self.s, absent_hours_per_day=12)).saved_absent_wh_day_max, 23.52)
    def test_more_off_power_can_negate_savings(self): self.assertLess(screen(replace(self.s, assumed_off_power_w_per_tx=.3)).saved_absent_wh_day_max, 0)
    def test_budget_fails(self): self.assertFalse(standby_budget_pass(self.s, 1))
    def test_budget_passes_at_2w(self): self.assertTrue(standby_budget_pass(self.s, 2))
    def test_budget_is_inclusive(self): self.assertTrue(standby_budget_pass(replace(self.s, modules=1), .25))
    def test_years_scaling(self): self.assertAlmostEqual(screen(replace(self.s, horizon_years=10)).saved_absent_kwh_horizon_max, 2 * screen(self.s).saved_absent_kwh_horizon_max)
    def test_price_scaling(self): self.assertAlmostEqual(screen(replace(self.s, electricity_eur_per_kwh=.5)).saved_absent_eur_horizon_min, 2 * screen(self.s).saved_absent_eur_horizon_min)
    def test_eur_zero(self): self.assertEqual(screen(replace(self.s, electricity_eur_per_kwh=0)).saved_absent_eur_horizon_max, 0)
    def test_floor_price_one(self): self.assertEqual(part_floor_eur(1, 9.92, 3.95), 13.87)
    def test_floor_price_eight(self): self.assertEqual(part_floor_eur(8, 9.92, 3.95), 83.31)
    def test_no_physical_approval(self): self.assertFalse(screen(self.s).hardware_safe_to_enable)
    def test_no_hardware_measurement(self): self.assertFalse(screen(self.s).real_power_tested)
    def test_zero_idle(self): self.assertEqual(screen(replace(self.s, no_load_current_min_a=0, no_load_current_max_a=0)).all_on_no_load_w_max, 0)
    def test_ordering_of_envelope(self): self.assertLessEqual(screen(self.s).saved_absent_wh_day_min, screen(self.s).saved_absent_wh_day_max)

    def test_invalid_current_order(self):
        with self.assertRaises(ValueError): replace(self.s, no_load_current_min_a=.06)
    def test_invalid_current_negative(self):
        with self.assertRaises(ValueError): replace(self.s, no_load_current_min_a=-.01)
    def test_invalid_current_over_one_amp(self):
        with self.assertRaises(ValueError): replace(self.s, no_load_current_max_a=1.1)
    def test_invalid_hours(self):
        with self.assertRaises(ValueError): replace(self.s, absent_hours_per_day=25)
    def test_invalid_voltage(self):
        with self.assertRaises(ValueError): replace(self.s, tx_voltage_v=0)
    def test_invalid_voltage_over_limit(self):
        with self.assertRaises(ValueError): replace(self.s, tx_voltage_v=25)
    def test_invalid_mod_count(self):
        with self.assertRaises(ValueError): replace(self.s, modules=0)
    def test_boolean_rejected(self):
        with self.assertRaises(ValueError): replace(self.s, modules=True)
    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError): replace(self.s, no_load_current_max_a=math.nan)
    def test_infinite_rejected(self):
        with self.assertRaises(ValueError): replace(self.s, tx_voltage_v=math.inf)
    def test_invalid_days(self):
        with self.assertRaises(ValueError): replace(self.s, days_per_year=367)
    def test_negative_cost(self):
        with self.assertRaises(ValueError): replace(self.s, electricity_eur_per_kwh=-1)
    def test_bad_off_power(self):
        with self.assertRaises(ValueError): replace(self.s, assumed_off_power_w_per_tx=-.001)
    def test_off_above_reference_envelope(self):
        with self.assertRaises(ValueError): replace(self.s, assumed_off_power_w_per_tx=6)
    def test_out_of_horizon(self):
        with self.assertRaises(ValueError): replace(self.s, horizon_years=31)
    def test_bad_floor_quantity(self):
        with self.assertRaises(ValueError): part_floor_eur(0, 9.92, 3.95)
    def test_bad_floor_price(self):
        with self.assertRaises(ValueError): part_floor_eur(1, -9.92, 3.95)
    def test_bad_budget(self):
        with self.assertRaises(ValueError): standby_budget_pass(self.s, math.inf)
    def test_zero_off_no_invented_load(self):
        z = screen(replace(self.s, assumed_off_power_w_per_tx=0))
        self.assertEqual(z.gated_absent_wh_day, 0)
        self.assertEqual(z.always_on_absent_wh_day_max, 48)


if __name__ == "__main__":
    unittest.main()
