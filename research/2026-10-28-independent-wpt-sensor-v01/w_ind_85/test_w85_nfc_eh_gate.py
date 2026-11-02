import unittest
from decimal import Decimal

from w85_nfc_eh_gate import POINTS, cap_min_uf, evaluate, positive, screen_point


class HarvestingGateTest(unittest.TestCase):
    def test_author_points_are_internally_consistent(self):
        self.assertEqual(len(POINTS), 2)
        for p in POINTS:
            self.assertEqual(Decimal(p["v_eh_v"]) * Decimal(p["i_eh_ma"]), Decimal(p["p_eh_mw"]))

    def test_100_percent_am_is_just_below_illustrative_power(self):
        case = evaluate()["manufacturer_fixture_cases"][0]
        self.assertEqual(case["assumed_regulated_output_mw"], "2.3256")
        self.assertEqual(case["assumed_output_margin_mw"], "-0.5744")
        self.assertFalse(case["conditional_static_budget_pass"])

    def test_10_percent_am_appears_budget_capable_only_hypothetically(self):
        case = evaluate()["manufacturer_fixture_cases"][1]
        self.assertEqual(case["assumed_regulated_output_mw"], "3.2552")
        self.assertEqual(case["assumed_output_margin_mw"], "+0.3552")
        self.assertTrue(case["conditional_static_budget_pass"])
        self.assertFalse(case["guaranteed_power_or_rf_data"])

    def test_both_author_rails_below_hypothetical_3v3(self):
        self.assertTrue(all(x["direct_rail_voltage_inadequate"] for x in evaluate()["manufacturer_fixture_cases"]))

    def test_efficiency_needed_100_percent_am(self):
        self.assertEqual(evaluate()["manufacturer_fixture_cases"][0]["ideal_efficiency_needed_pct"], "99.759")

    def test_efficiency_needed_10_percent_am(self):
        self.assertEqual(evaluate()["manufacturer_fixture_cases"][1]["ideal_efficiency_needed_pct"], "71.271")

    def test_100ms_cap(self):
        r = evaluate()
        self.assertEqual(r["ideal_cap_min_uf"], "306.878")
        self.assertTrue(r["conditional_ideal_cap_pass"])

    def test_250ms_cap_fails(self):
        r = evaluate(outage_ms="250")
        self.assertEqual(r["ideal_cap_min_uf"], "767.196")
        self.assertFalse(r["conditional_ideal_cap_pass"])

    def test_zero_cap_not_a_real_buffer(self):
        self.assertFalse(evaluate(effective_cap_uf="0")["conditional_ideal_cap_pass"])

    def test_large_cap_does_not_approve_hardware(self):
        self.assertEqual(evaluate(effective_cap_uf="1000000")["hardware_release"], "BLOCKED")

    def test_proven_flags_do_not_override_hardware_stop(self):
        r = evaluate(field_and_alignment_proven=True, continuous_rf_data_proven=True, thermal_fod_cutout_proven=True)
        self.assertEqual(r["hardware_release"], "BLOCKED")
        self.assertIn("no_own_energized_hardware_or_bench_measurement", r["missing_evidence"])

    def test_evidence_false_by_default(self):
        self.assertIn("reader_field_coupling_in_robot_unverified", evaluate()["missing_evidence"])
        self.assertIn("rf_data_during_energy_harvesting_unverified", evaluate()["missing_evidence"])

    def test_data_not_power_for_esp_now(self):
        self.assertTrue(evaluate()["requires_active_NFC_reader_not_an_ESP_NOW_radio"])

    def test_no_critical_domain(self):
        self.assertEqual(evaluate()["dock_BMS_motors_safety"], "NOT_IN_SCOPE")

    def test_unregulated_is_not_3v3_supply(self):
        self.assertTrue(evaluate()["EH_voltage_is_unregulated_and_absent_if_field_insufficient"])

    def test_insufficient_power_even_at_perfect_efficiency(self):
        self.assertFalse(evaluate(load_mw="4.5", illustrative_efficiency="1")["manufacturer_fixture_cases"][1]["conditional_static_budget_pass"])

    def test_low_load_ideal_conditional_not_approval(self):
        r = evaluate(load_mw="0.1", illustrative_efficiency="1")
        self.assertTrue(all(x["conditional_static_budget_pass"] for x in r["manufacturer_fixture_cases"]))
        self.assertEqual(r["hardware_release"], "BLOCKED")

    def test_low_rail_flags_no_direct_conversion_requirement_but_no_regulation_approval(self):
        r = evaluate(rail_v="2.9", floor_v="2.5")
        self.assertFalse(r["manufacturer_fixture_cases"][1]["direct_rail_voltage_inadequate"])
        self.assertEqual(r["hardware_release"], "BLOCKED")

    def test_improper_voltage_window(self):
        with self.assertRaisesRegex(ValueError, "hold_up_voltage_window_invalid"):
            cap_min_uf("2.9", "100", "3.0", "3.0")

    def test_inverted_voltage_window(self):
        with self.assertRaisesRegex(ValueError, "hold_up_voltage_window_invalid"):
            evaluate(rail_v="2.9", floor_v="3.0")

    def test_load_infinite_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(load_mw="Infinity")

    def test_nan_efficiency_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(illustrative_efficiency="NaN")

    def test_superunity_efficiency_rejected(self):
        with self.assertRaisesRegex(ValueError, "illustrative_efficiency_exceeds_unity"):
            evaluate(illustrative_efficiency="1.001")

    def test_zero_efficiency_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(illustrative_efficiency="0")

    def test_negative_outage_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(outage_ms="-1")

    def test_negative_effective_cap_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(effective_cap_uf="-0.1")

    def test_wrong_flag_type_rejected(self):
        with self.assertRaisesRegex(ValueError, "evidence_flags_must_be_boolean"):
            evaluate(continuous_rf_data_proven="false")

    def test_mismatch_author_point_rejected(self):
        p = dict(POINTS[0], p_eh_mw="99")
        with self.assertRaisesRegex(ValueError, "manufacturer_point_power_mismatch"):
            screen_point(p, power_mw="2.9", rail_v="3.3", illustrative_efficiency="0.8")

    def test_unknown_am_rejected(self):
        p = dict(POINTS[0], am_pct=42)
        with self.assertRaisesRegex(ValueError, "unrecognized_modulation"):
            screen_point(p, power_mw="2.9", rail_v="3.3", illustrative_efficiency="0.8")

    def test_bad_field_rejected(self):
        p = dict(POINTS[0], h_arms="0")
        with self.assertRaises(ValueError):
            screen_point(p, power_mw="2.9", rail_v="3.3", illustrative_efficiency="0.8")

    def test_physical_power_points_are_not_wpt_efficiency_readings(self):
        for row in evaluate()["manufacturer_fixture_cases"]:
            self.assertEqual(row["origin"], "manufacturer_test_fixture_not_our_own_measurement")
            self.assertNotIn("tx_input_energy", row)


if __name__ == "__main__":
    unittest.main()
