"""Original adversarial and boundary tests, all digital."""
import unittest
from decimal import Decimal
from w87_nfc_duty_gate import duty_gate, report


BASE = dict(am="AM100", field="0.5", efficiency="0.8", baseline_mw="0.1",
            leakage_mw="0", event_mj="1", period_s="1",
            capacitance_effective_uf="1200", v_storage_high="3.3",
            v_storage_low="3.0", vin_min="3.0", startup_mj="5")


class DutyGateTests(unittest.TestCase):
    def go(self, **changes):
        return duty_gate(**{**BASE, **changes})

    def test_author_st_point_not_our_measurement(self):
        x = self.go()
        self.assertFalse(x["author_data_guaranteed_minimum"])
        self.assertFalse(x["bench_measurements_by_us"])
        self.assertEqual(x["hardware_release"], "BLOCKED")

    def test_weak_field_modulation_reverses_sustainability(self):
        a = self.go(am="AM100")
        b = self.go(am="AM10")
        self.assertTrue(a["average_energy_conditionally_sustained"])
        self.assertFalse(b["average_energy_conditionally_sustained"])
        self.assertEqual(a["hypothetical_net_before_events_mW"], "1.748")
        self.assertEqual(b["hypothetical_net_before_events_mW"], "0.188")

    def test_weak_field_am10_recharge_is_over_five_seconds(self):
        x = self.go(am="AM10")
        self.assertGreater(Decimal(x["ideal_min_recharge_seconds"]), Decimal("5"))
        self.assertLess(Decimal(x["ideal_min_recharge_seconds"]), Decimal("6"))

    def test_weak_field_ten_second_screen_passes_energy_only(self):
        x = self.go(am="AM10", period_s="10")
        self.assertTrue(x["average_energy_conditionally_sustained"])
        self.assertEqual(x["hardware_release"], "BLOCKED")
        self.assertIn("CONDITIONAL_MATH_ONLY", x["screen_reasons"][0])

    def test_high_power_point_can_fail_voltage(self):
        x = self.go(am="AM10", field="3", vin_min="3.3")
        self.assertTrue(x["average_energy_conditionally_sustained"])
        self.assertFalse(x["author_point_voltage_passes_assumed_vin"])
        self.assertIn("AUTHOR_POINT_BELOW_HYPOTHETICAL_CONVERTER_VIN", x["screen_reasons"])

    def test_too_small_buffer_fails_despite_average(self):
        x = self.go(capacitance_effective_uf="100")
        self.assertFalse(x["single_event_ideal_buffer_sufficient"])
        self.assertIn("INSUFFICIENT_IDEAL_EFFECTIVE_STORAGE", x["screen_reasons"])

    def test_cap_threshold_equality_passes(self):
        x = self.go(capacitance_effective_uf="2000", event_mj="1.89")
        self.assertTrue(x["single_event_ideal_buffer_sufficient"])
        self.assertEqual(x["ideal_reservoir_event_energy_mJ"], "1.89")

    def test_exact_energy_break_even(self):
        x = self.go(event_mj="1.748")
        self.assertEqual(x["hypothetical_energy_margin_mW"], "0.000")
        self.assertTrue(x["average_energy_conditionally_sustained"])

    def test_overload_break_even(self):
        self.assertFalse(self.go(event_mj="1.749")["average_energy_conditionally_sustained"])

    def test_leakage_can_eliminate_all_net(self):
        x = self.go(leakage_mw="2")
        self.assertIsNone(x["ideal_min_recharge_seconds"])
        self.assertIsNone(x["ideal_cold_start_seconds_for_assumed_startup_energy"])
        self.assertFalse(x["average_energy_conditionally_sustained"])

    def test_no_events_without_net_even_with_huge_buffer(self):
        x = self.go(leakage_mw="2", capacitance_effective_uf="1000000")
        self.assertFalse(x["average_energy_conditionally_sustained"])

    def test_startup_energy_zero_is_valid(self):
        self.assertEqual(self.go(startup_mj="0")["ideal_cold_start_seconds_for_assumed_startup_energy"], "0E+3")

    def test_negative_idle_rejected(self):
        with self.assertRaises(ValueError): self.go(baseline_mw="-0.1")

    def test_negative_leakage_rejected(self):
        with self.assertRaises(ValueError): self.go(leakage_mw="-0.001")

    def test_negative_start_rejected(self):
        with self.assertRaises(ValueError): self.go(startup_mj="-1")

    def test_bad_efficiency_zero_rejected(self):
        with self.assertRaises(ValueError): self.go(efficiency="0")

    def test_bad_efficiency_above_one_rejected(self):
        with self.assertRaises(ValueError): self.go(efficiency="1.01")

    def test_bad_event_zero_rejected(self):
        with self.assertRaises(ValueError): self.go(event_mj="0")

    def test_bad_period_zero_rejected(self):
        with self.assertRaises(ValueError): self.go(period_s="0")

    def test_bad_cap_zero_rejected(self):
        with self.assertRaises(ValueError): self.go(capacitance_effective_uf="0")

    def test_storage_reversed_rejected(self):
        with self.assertRaises(ValueError): self.go(v_storage_high="2", v_storage_low="3")

    def test_zero_storage_low_rejected(self):
        with self.assertRaises(ValueError): self.go(v_storage_low="0")

    def test_bad_vin_zero_rejected(self):
        with self.assertRaises(ValueError): self.go(vin_min="0")

    def test_nan_rejected(self):
        with self.assertRaises(ValueError): self.go(event_mj="NaN")

    def test_infinity_rejected(self):
        with self.assertRaises(ValueError): self.go(leakage_mw="Infinity")

    def test_bool_rejected(self):
        with self.assertRaises(ValueError): self.go(efficiency=True)

    def test_float_rejected(self):
        with self.assertRaises(ValueError): self.go(efficiency=0.8)

    def test_unsampled_field_rejected(self):
        with self.assertRaises(ValueError): self.go(field="0.75")

    def test_invalid_modulation_rejected(self):
        with self.assertRaises(ValueError): self.go(am="AM50")

    def test_dock_and_radio_unqualified(self):
        x = report()
        self.assertIn("not dock", x["scope"])
        self.assertTrue(x["not_applicable_to_ST_radio_reliability"])
        self.assertEqual(x["hardware_release"], "BLOCKED")

    def test_no_pretend_dynamic_or_safety_measurements(self):
        x = self.go()
        for key in ["converter_ESR_dynamic_and_offset_verified", "FOD_thermal_EMI_independent_cut_verified",
                    "rf_application_ACK_privacy_recovery_verified", "reader_input_power_known"]:
            self.assertFalse(x[key])


if __name__ == "__main__": unittest.main()
