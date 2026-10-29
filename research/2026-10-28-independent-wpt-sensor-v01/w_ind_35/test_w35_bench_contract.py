"""W-IND-35: tests of analyzer only, with SYNTHETIC inputs, no energized hardware."""
import copy
import unittest
from w35_bench_contract import demo_rows, format_csv, parse_csv, evaluate

class BenchGateTests(unittest.TestCase):
    def setUp(self):
        self.rows = demo_rows()

    def analyze(self, rows=None):
        return evaluate(parse_csv(format_csv(self.rows if rows is None else rows)))

    def corrupt(self, scenario, key, value):
        rows = copy.deepcopy(self.rows)
        for r in rows:
            if r["scenario"] == scenario and r["t_ms"] >= 100:
                r[key] = value
        return rows

    def test_demo_synthetic_never_approves_hardware(self):
        e = self.analyze()
        self.assertTrue(e["contract_pass"])
        self.assertFalse(e["hardware_validated"])
        self.assertFalse(e["energization_authorized"])
        self.assertEqual(e["sample_count"], 32)

    def test_reported_measured_also_requires_external_review(self):
        e = evaluate(self.rows, evidence_kind="measured_unverified")
        self.assertTrue(e["contract_pass"])
        self.assertFalse(e["hardware_validated"])
        self.assertIn("REVIEW_REQUIRED", e["status"])

    def test_monitor_unpowered_looks_healthy_by_passive_eol(self):
        rows = [r for r in self.rows if r["scenario"] == "monitor_vdd_lost"]
        self.assertTrue(all(r["v_alert"] / r["v_logic"] == .5 for r in rows))
        self.assertTrue(all(r["v_monitor"] == 0 for r in rows))
        self.assertTrue(self.analyze()["contract_pass"])

    def test_single_enable_stuck_high_is_rejected(self):
        self.assertFalse(self.analyze(self.corrupt("monitor_vdd_lost", "v_enable_a", 3.3))["contract_pass"])

    def test_second_enable_stuck_high_is_rejected(self):
        self.assertFalse(self.analyze(self.corrupt("monitor_pg_lost", "v_enable_b", 3.3))["contract_pass"])

    def test_residual_output_is_rejected_even_with_both_en_low(self):
        self.assertFalse(self.analyze(self.corrupt("alert_open", "v_load", 2.4))["contract_pass"])

    def test_unpowered_monitor_requires_valid_low_pg(self):
        self.assertFalse(self.analyze(self.corrupt("monitor_vdd_lost", "v_pg", 5.0))["contract_pass"])

    def test_unpowered_monitor_requires_genuinely_low_supply(self):
        self.assertFalse(self.analyze(self.corrupt("monitor_vdd_lost", "v_monitor", 5.0))["contract_pass"])

    def test_unpowered_monitor_requires_ambiguous_alert(self):
        self.assertFalse(self.analyze(self.corrupt("monitor_vdd_lost", "v_alert", 5.0))["contract_pass"])

    def test_missing_scenario_is_not_accepted(self):
        self.assertFalse(self.analyze([r for r in self.rows if r["scenario"] != "alert_short"])["contract_pass"])

    def test_missing_confirmation_samples_rejected(self):
        rows = [r for r in self.rows if r["scenario"] != "idle" or r["t_ms"] < 100]
        self.assertFalse(self.analyze(rows)["contract_pass"])

    def test_duplicate_timestamp_rejected(self):
        rows = copy.deepcopy(self.rows); rows.append(copy.deepcopy(rows[0]))
        self.assertFalse(self.analyze(rows)["contract_pass"])

    def test_nan_input_is_invalid(self):
        text = format_csv(self.rows).replace(',5.0,', ',nan,', 1)
        with self.assertRaisesRegex(ValueError, "nonfinite"):
            parse_csv(text)

    def test_negative_input_is_invalid(self):
        rows = self.corrupt("alert_short", "v_load", -1.0)
        with self.assertRaisesRegex(ValueError, "nonfinite/negative"):
            parse_csv(format_csv(rows))

    def test_invalid_origin_is_invalid(self):
        rows = self.corrupt("rf_rearm_attempt", "rearm_origin", "remote_untrusted")
        with self.assertRaisesRegex(ValueError, "invalid rearm"):
            parse_csv(format_csv(rows))

    def test_rf_cannot_claim_local_rearm(self):
        self.assertFalse(self.analyze(self.corrupt("local_rearm", "rearm_origin", "rf"))["contract_pass"])

    def test_rf_attempt_does_not_authorize_power(self):
        self.assertFalse(self.analyze(self.corrupt("rf_rearm_attempt", "v_load", 5.0))["contract_pass"])

    def test_brownout_of_control_is_rejected(self):
        self.assertFalse(self.analyze(self.corrupt("alert_short", "v_logic", 3.0))["contract_pass"])

    def test_local_rearm_must_really_turn_on_in_fixture(self):
        self.assertFalse(self.analyze(self.corrupt("local_rearm", "v_load", 0.0))["contract_pass"])

    def test_alert_open_must_be_exercised(self):
        self.assertFalse(self.analyze(self.corrupt("alert_open", "v_alert", 2.5))["contract_pass"])

    def test_alert_short_must_be_exercised(self):
        self.assertFalse(self.analyze(self.corrupt("alert_short", "v_alert", 2.5))["contract_pass"])

    def test_csv_column_omission_rejected(self):
        text = format_csv(self.rows).replace("v_pg,", "", 1)
        with self.assertRaisesRegex(ValueError, "fields"):
            parse_csv(text)

if __name__ == "__main__":
    unittest.main()
