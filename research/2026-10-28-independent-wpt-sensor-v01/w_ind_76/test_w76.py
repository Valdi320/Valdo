import copy
import json
import unittest
from pathlib import Path
from w76_cycle_gate import evaluate

BASE = json.loads((Path(__file__).parent / "SCENARIO_SYNTHETIC.json").read_text())


class W76CycleTests(unittest.TestCase):
    def test_spike_exceeds_daily_allowance(self):
        result = evaluate(BASE)
        self.assertAlmostEqual(result["tx_mean_mw"], 33)
        self.assertAlmostEqual(result["extra_wh_day_nominal"], 0.7224)
        self.assertIn("ENERGY_BUDGET_EXCEEDED", result["blockers"])

    def test_steady_only_would_hide_spike(self):
        v = copy.deepcopy(BASE)
        v["phases"] = [dict(v["phases"][0], seconds=30)]
        r = evaluate(v)
        self.assertAlmostEqual(r["tx_mean_mw"], 20)
        self.assertAlmostEqual(r["extra_wh_day_nominal"], 0.4104)
        self.assertNotIn("ENERGY_BUDGET_EXCEEDED", r["blockers"])
        self.assertFalse(r["hardware_approved"])

    def test_cannot_replace_measurement_by_synthetic(self):
        r = evaluate(BASE)
        self.assertIn("NO_COMPLETE_BENCH_MEASURED_CYCLE", r["blockers"])
        self.assertFalse(r["all_phases_labeled_bench_measured"])

    def test_representative_cycle_not_proven(self):
        self.assertIn("CYCLE_REPRESENTATIVENESS_UNVERIFIED", evaluate(BASE)["blockers"])

    def test_missing_phase_duration_fails_closed(self):
        v = copy.deepcopy(BASE)
        v["phases"][1]["seconds"] = 0.1
        with self.assertRaises(ValueError): evaluate(v)

    def test_unreasonable_overlap_fails_closed(self):
        v = copy.deepcopy(BASE)
        v["phases"][1]["seconds"] = 1.0
        with self.assertRaises(ValueError): evaluate(v)

    def test_sensor_must_be_powered_every_phase(self):
        v = copy.deepcopy(BASE)
        v["phases"][1]["rx_output_mw"] = 0
        self.assertIn("RX_PHASE_MEAN_BELOW_TARGET", evaluate(v)["blockers"])

    def test_uncertainty_conservatively_raises_energy(self):
        v = copy.deepcopy(BASE)
        for p in v["phases"]: p["relative_error_pct"] = 10
        r = evaluate(v)
        self.assertAlmostEqual(r["tx_conservative_upper_mean_mw"], 36.3)
        self.assertAlmostEqual(r["extra_wh_day_conservative"], 0.8016)
        self.assertAlmostEqual(r["rx_min_phase_mean_lower_bound_mw"], 2.61)
        self.assertIn("RX_PHASE_MEAN_BELOW_TARGET", r["blockers"])

    def test_no_false_hardware_certification_even_all_claim_measured(self):
        v = copy.deepcopy(BASE)
        for p in v["phases"]: p["source_kind"] = "bench_measured"
        v["cycle_representative"] = True
        r = evaluate(v)
        self.assertFalse(r["hardware_approved"])
        self.assertFalse(r["safety_tests_completed_by_model"])
        self.assertIn("ENERGY_BUDGET_EXCEEDED", r["blockers"])

    def test_digital_pass_not_hardware(self):
        v = copy.deepcopy(BASE)
        v["phases"] = [dict(v["phases"][0], seconds=30, source_kind="bench_measured")]
        v["cycle_representative"] = True
        r = evaluate(v)
        self.assertEqual(r["status"], "DIGITAL_BUDGET_SCREEN_ONLY")
        self.assertFalse(r["hardware_approved"])

    def test_reject_nonfinite_bool_or_negative_values(self):
        for bad in [float("nan"), float("inf"), -1, True, None, "30"]:
            v = copy.deepcopy(BASE)
            v["cycle_seconds"] = bad
            with self.subTest(bad=bad), self.assertRaises(ValueError): evaluate(v)

    def test_reject_negative_or_nonfinite_power(self):
        for bad in [-2.0, float("nan"), float("inf"), True]:
            v = copy.deepcopy(BASE)
            v["phases"][0]["tx_input_mw"] = bad
            with self.subTest(bad=bad), self.assertRaises(ValueError): evaluate(v)

    def test_more_rx_than_tx_cannot_pass(self):
        v = copy.deepcopy(BASE)
        v["phases"][0]["rx_output_mw"] = 30
        with self.assertRaises(ValueError): evaluate(v)

    def test_duplicate_names_rejected(self):
        v = copy.deepcopy(BASE)
        v["phases"][1]["name"] = "steady"
        with self.assertRaises(ValueError): evaluate(v)

    def test_unknown_source_kind_rejected(self):
        v = copy.deepcopy(BASE)
        v["phases"][0]["source_kind"] = "manufacturer_claim"
        with self.assertRaises(ValueError): evaluate(v)

    def test_zero_phase_duration_rejected(self):
        v = copy.deepcopy(BASE)
        v["phases"][1]["seconds"] = 0
        with self.assertRaises(ValueError): evaluate(v)

    def test_100pct_uncertainty_rejected(self):
        v = copy.deepcopy(BASE)
        v["phases"][0]["relative_error_pct"] = 100
        with self.assertRaises(ValueError): evaluate(v)

    def test_threshold_exact_and_above(self):
        v = copy.deepcopy(BASE)
        power = 2.9 + 500 / 24
        v["phases"] = [dict(v["phases"][0], seconds=30, tx_input_mw=power)]
        self.assertNotIn("ENERGY_BUDGET_EXCEEDED", evaluate(v)["blockers"])
        v["phases"][0]["tx_input_mw"] += 0.001
        self.assertIn("ENERGY_BUDGET_EXCEEDED", evaluate(v)["blockers"])

    def test_extreme_float_overflow_fails(self):
        v = copy.deepcopy(BASE)
        v["phases"][0]["tx_input_mw"] = 1e308
        with self.assertRaises(ValueError): evaluate(v)

    def test_deterministic(self):
        self.assertEqual(evaluate(BASE), evaluate(copy.deepcopy(BASE)))


if __name__ == "__main__": unittest.main()
