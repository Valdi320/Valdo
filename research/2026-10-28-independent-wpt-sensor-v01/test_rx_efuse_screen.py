"""Deterministic negative tests; no real WPT or electrical measurements."""
import math
import unittest
from rx_efuse_screen import (TPS2663, TPS25947, TPS259630, EFuse,
                              thresholds, screen_rx, input_budget, data)


class PaperEnvelope(unittest.TestCase):
    def test_5v_scenario_guaranteed(self):
        r = screen_rx(TPS259630, nominal_limit_a=.4)
        self.assertTrue(r["paper_feasible"])
        self.assertAlmostEqual(r["max_assumed_load_a"], 1.5/4.5)
        self.assertAlmostEqual(r["low_limit_a"], .3584)
        self.assertAlmostEqual(r["high_limit_a"], .4416)
        self.assertFalse(r["installation_approved"])

    def test_lower_bound_4v_fails(self):
        self.assertFalse(screen_rx(TPS259630, nominal_limit_a=.4,v_rx_min=4)["paper_feasible"])

    def test_half_amp_fault_caught(self):
        self.assertTrue(screen_rx(TPS259630, nominal_limit_a=.4, fault_current_a=.5)["fault_above_high_threshold"])

    def test_42a_not_guaranteed(self):
        self.assertFalse(screen_rx(TPS259630, nominal_limit_a=.4, fault_current_a=.42)["fault_above_high_threshold"])

    def test_35a_peak_overcurrent(self):
        self.assertFalse(screen_rx(TPS259630, nominal_limit_a=.4,peak_w=1.75)["paper_feasible"])

    def test_tps2663_cannot_set_0p4(self):
        self.assertFalse(screen_rx(TPS2663, nominal_limit_a=.4)["range_supported"])

    def test_tps25947_cannot_set_0p4(self):
        self.assertFalse(screen_rx(TPS25947, nominal_limit_a=.4)["range_supported"])

    def test_unknown_tolerance_never_approved(self):
        self.assertFalse(screen_rx(TPS2663, nominal_limit_a=.6)["paper_feasible"])

    def test_lower_bound_device(self):
        self.assertTrue(screen_rx(TPS259630,nominal_limit_a=.125)["range_supported"])

    def test_out_of_range_device(self):
        self.assertFalse(screen_rx(TPS259630,nominal_limit_a=2.1)["range_supported"])

    def test_tolerance_edges(self):
        lo, hi = thresholds(.4,.104)
        self.assertAlmostEqual(lo,.3584)
        self.assertAlmostEqual(hi,.4416)

    def test_threshold_equality_is_not_guaranteed(self):
        self.assertFalse(screen_rx(TPS259630,nominal_limit_a=.4,fault_current_a=.4416)["fault_above_high_threshold"])

    def test_current_fod_false(self):
        self.assertFalse(input_budget(rx_peak_w=1.5,tx_supply_v=5,efficiency=.7)["tx_fod_verified"])

    def test_input_loss_budget(self):
        r=input_budget(rx_peak_w=1.5,tx_supply_v=5,efficiency=.5,tx_controls_w=.05)
        self.assertAlmostEqual(r["tx_input_a"],.61)
        self.assertAlmostEqual(r["total_losses_w"],1.55)

    def test_worse_eta_more_input(self):
        self.assertGreater(input_budget(rx_peak_w=1.5,tx_supply_v=5,efficiency=.45)["tx_input_a"],
                           input_budget(rx_peak_w=1.5,tx_supply_v=5,efficiency=.85)["tx_input_a"])

    def test_no_tx_automatic_fod(self):
        self.assertFalse(data()["tx_example_eta55_percent"]["tx_fod_verified"])

    def test_no_lithium_approval(self):
        self.assertFalse(data()["dock_charge_validated"])

    def test_no_motor_approval(self):
        self.assertFalse(data()["distributed_motor_power_validated"])

    def test_invalid_zero(self):
        with self.assertRaises(ValueError):screen_rx(TPS259630,nominal_limit_a=0)

    def test_nan(self):
        with self.assertRaises(ValueError):screen_rx(TPS259630,nominal_limit_a=float('nan'))

    def test_inf(self):
        with self.assertRaises(ValueError):screen_rx(TPS259630,nominal_limit_a=float('inf'))

    def test_negative_power(self):
        with self.assertRaises(ValueError):input_budget(rx_peak_w=-1,tx_supply_v=5,efficiency=.5)

    def test_eta_zero(self):
        with self.assertRaises(ValueError):input_budget(rx_peak_w=1,tx_supply_v=5,efficiency=0)

    def test_eta_above_one(self):
        with self.assertRaises(ValueError):input_budget(rx_peak_w=1,tx_supply_v=5,efficiency=1.01)

    def test_negative_controls(self):
        with self.assertRaises(ValueError):input_budget(rx_peak_w=1,tx_supply_v=5,efficiency=.7,tx_controls_w=-.1)

    def test_5v_nominal_0p3_a(self):
        self.assertAlmostEqual(1.5/5,.3)

    def test_5v_mean_0p08_a(self):
        self.assertAlmostEqual(.4/5,.08)

    def test_0p4limit_lower_below_peak_4p5(self):
        self.assertGreater(.4*(1-.104),1.5/4.5)

    def test_boundary_fault_at_trip_is_not_strict(self):
        self.assertFalse(screen_rx(TPS259630,nominal_limit_a=.4,fault_current_a=.4416)["paper_feasible"])

    def test_all_limits_finite(self):
        for x in (.125,.2,.4,1.,2.):
            self.assertTrue(math.isfinite(screen_rx(TPS259630,nominal_limit_a=x)["high_limit_a"]))


if __name__ == '__main__': unittest.main()
