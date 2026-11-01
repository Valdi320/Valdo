"""Digital only; points from existing original W86 table; no hardware assertions."""
import unittest
from decimal import Decimal
from w89_source_headroom_gate import evaluate_point, report
from w86_field_sweep import at

B = dict(topology="linear_or_buck", assumed_drop_v="0.20", charge_target_v="3.30",
         operating_floor_v="3.00", effective_cap_uf="1200", eta="0.8",
         idle_mw="0.1", event_mj="1", period_s="1", blackout_s="0.1",
         burst_attempts=1)


class HeadroomTests(unittest.TestCase):
    def check(self, am="AM100", field="0.5", **kw):
        return evaluate_point(at(am, field), **{**B, **kw})

    def test_original_w88_assumed_precharge_ideal_can_pass_one_burst(self):
        x = self.check()
        self.assertEqual(Decimal(x["ideal_W88_fully_precharged_reserve_mJ"]), Decimal("1.134"))
        self.assertGreater(Decimal(x["ideal_W88_fully_precharged_reserve_mJ"]), Decimal("1.01"))

    def test_fixed_0_2v_drop_reduces_initial_reserve_and_blocks_burst(self):
        x = self.check()
        self.assertEqual(x["conditional_at_sample_after_drop_v"], "3.10")
        self.assertEqual(Decimal(x["conditional_at_sample_reachable_reserve_mJ"]), Decimal("0.366"))
        self.assertEqual(Decimal(x["conditional_at_sample_burst_shortfall_mJ"]), Decimal("0.644"))
        self.assertFalse(x["conditional_preflight_pass_not_hardware"])

    def test_weak_field_modulation_opposite_voltage_energy_risks(self):
        x = self.check(am="AM10")
        self.assertTrue(x["charge_target_reachable_with_positive_margin_in_assumed_model"])
        self.assertEqual(Decimal(x["hypothetical_average_margin_mW"]), Decimal("-0.8408"))
        self.assertFalse(x["conditional_preflight_pass_not_hardware"])

    def test_22_samples_none_pass_with_hypothetical_0_2v_drop(self):
        x = report()
        self.assertEqual(x["sampled_points_total"], 22)
        self.assertEqual(x["full_conditional_preflight_points"], {"AM100": 0, "AM10": 0})
        self.assertEqual(x["voltage_possible_points"], {"AM100": 0, "AM10": 1})

    def test_zero_drop_counterfactual_not_hardware_evidence(self):
        x = self.check(field="1", assumed_drop_v="0")
        self.assertTrue(x["conditional_preflight_pass_not_hardware"])
        self.assertEqual(x["hardware_release"], "BLOCKED")
        self.assertFalse(x["source_voltage_is_guaranteed_minimum"])

    def test_equal_input_and_charge_target_is_not_positive_headroom(self):
        x = self.check(assumed_drop_v="0")
        self.assertFalse(x["charge_target_reachable_with_positive_margin_in_assumed_model"])

    def test_more_cap_does_not_create_missing_voltage_headroom(self):
        x = self.check(effective_cap_uf="1000000")
        self.assertFalse(x["conditional_preflight_pass_not_hardware"])
        self.assertFalse(x["charge_target_reachable_with_positive_margin_in_assumed_model"])

    def test_boost_needs_a_real_qualified_converter(self):
        x = self.check(topology="boost_unqualified")
        self.assertIsNone(x["conditional_at_sample_reachable_reserve_mJ"])
        self.assertIn("BOOST_OUTPUT_AND_INPUT_CURVES_UNQUALIFIED", x["reasons"])
        self.assertFalse(x["conditional_preflight_pass_not_hardware"])

    def test_blackout_and_retransmissions_both_cost_energy(self):
        x = self.check(burst_attempts=2, idle_mw="0.2", blackout_s="0.25")
        self.assertEqual(Decimal(x["hypothetical_burst_demand_mJ"]), Decimal("2.050"))
        self.assertGreater(Decimal(x["conditional_at_sample_burst_shortfall_mJ"]), Decimal("1.6"))

    def test_bad_inputs_fail_closed(self):
        bad = [("topology", "magic"), ("assumed_drop_v", "-0.01"),
               ("effective_cap_uf", "0"), ("charge_target_v", "3.00"),
               ("operating_floor_v", "3.30"), ("eta", "1.01"),
               ("eta", "NaN"), ("period_s", "0"), ("blackout_s", "2"),
               ("burst_attempts", 0), ("burst_attempts", 33),
               ("burst_attempts", True), ("event_mj", 1.0)]
        for k, v in bad:
            with self.subTest(k=k, v=v), self.assertRaises(ValueError):
                self.check(**{k: v})

    def test_never_qualifies_physical_conditions(self):
        x = report()
        self.assertEqual(x["hardware_release"], "BLOCKED")
        self.assertEqual(x["FOD_heat_EMI_independent_cut"], "UNQUALIFIED")
        self.assertFalse(x["W88_optimistic_start_0_5A_AM100"]["regulated_conductor_and_boot_measured"])

    def test_determinism(self):
        self.assertEqual(report(), report())


if __name__ == "__main__":
    unittest.main()
