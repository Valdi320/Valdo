import copy
import json
import math
import unittest
from pathlib import Path
from w78_inter_sample_gate import screen

BASE = json.loads((Path(__file__).parent / "TRACE_SYNTHETIC.json").read_text(encoding="utf-8"))


def sample():
    return copy.deepcopy(BASE)


class W78Tests(unittest.TestCase):
    def test_aliasing_detected_despite_good_samples(self):
        r = screen(BASE)
        self.assertEqual(r["lowest_observed_v"], 3.3)
        self.assertAlmostEqual(r["conditional_inter_sample_lower_v"], 2.95)
        self.assertIn("INTER_SAMPLE_VOLTAGE_MAY_FALL_BELOW_MIN", r["blockers"])

    def test_shorter_sampling_passes_conditional_bound(self):
        x = sample(); x["capture_duration_s"] = 0.01
        x["samples"] = [{"t_s": 0.0, "v_rx_v": 3.3}, {"t_s": 0.005, "v_rx_v": 3.3}, {"t_s": 0.01, "v_rx_v": 3.3}]
        r = screen(x)
        self.assertAlmostEqual(r["conditional_inter_sample_lower_v"], 3.10)
        self.assertNotIn("INTER_SAMPLE_VOLTAGE_MAY_FALL_BELOW_MIN", r["blockers"])

    def test_bound_is_conditional_even_with_claims(self):
        x = sample(); x["slew_bound_v_per_s"] = 20
        x["source_kind"] = "bench_measured_claim"; x["slew_bound_evidence"] = "independent_characterization_claim"
        r = screen(x)
        self.assertEqual(r["status"], "CONDITIONAL_DIGITAL_SCREEN_ONLY")
        self.assertFalse(r["hardware_approved"])
        self.assertFalse(r["instantaneous_voltage_proven"])

    def test_no_finite_samples_prove_slew(self):
        x = sample(); x["slew_bound_v_per_s"] = 0
        self.assertIn("SLEW_BOUND_NOT_INDEPENDENTLY_CHARACTERIZED", screen(x)["blockers"])

    def test_uncertainty_weakens_bound(self):
        x = sample(); x["voltage_uncertainty_v"] = 0.10
        self.assertAlmostEqual(screen(x)["conditional_inter_sample_lower_v"], 2.90)

    def test_clock_jitter_weakens_bound(self):
        x = sample(); x["timestamp_uncertainty_s"] = 0.001
        self.assertAlmostEqual(screen(x)["conditional_inter_sample_lower_v"], 2.89)

    def test_timestamp_jitter_warning(self):
        x = sample(); x["timestamp_uncertainty_s"] = 0.006
        self.assertIn("TIMESTAMP_UNCERTAINTY_TOO_LARGE_FOR_GAP", screen(x)["blockers"])

    def test_sampling_gap_flag(self):
        x = sample(); x["max_nominal_sample_gap_s"] = 0.009
        self.assertIn("NOMINAL_SAMPLING_GAP_EXCEEDED", screen(x)["blockers"])

    def test_exact_threshold(self):
        x = sample(); x["slew_bound_v_per_s"] = 50
        self.assertNotIn("INTER_SAMPLE_VOLTAGE_MAY_FALL_BELOW_MIN", screen(x)["blockers"])

    def test_asymmetric_endpoints(self):
        x = sample(); x["samples"][1]["v_rx_v"] = 3.1
        self.assertAlmostEqual(screen(x)["conditional_inter_sample_lower_v"], 2.85)

    def test_inconsistent_slew_raises(self):
        x = sample(); x["slew_bound_v_per_s"] = 1
        x["samples"][1]["v_rx_v"] = 3.0
        with self.assertRaises(ValueError): screen(x)

    def test_zero_slew_equal_endpoints(self):
        x = sample(); x["slew_bound_v_per_s"] = 0
        self.assertAlmostEqual(screen(x)["conditional_inter_sample_lower_v"], 3.25)

    def test_missing_coverage_start(self):
        x = sample(); x["samples"][0]["t_s"] = 0.001
        with self.assertRaises(ValueError): screen(x)

    def test_missing_coverage_end(self):
        x = sample(); x["capture_duration_s"] = 0.03
        with self.assertRaises(ValueError): screen(x)

    def test_duplicate_time(self):
        x = sample(); x["samples"][1]["t_s"] = 0
        with self.assertRaises(ValueError): screen(x)

    def test_unsorted_time(self):
        x = sample(); x["samples"] = list(reversed(x["samples"]))
        with self.assertRaises(ValueError): screen(x)

    def test_invalid_samples(self):
        for bad in (None, [], {}, False, "samples"):
            x = sample(); x["samples"] = bad
            with self.subTest(bad=bad), self.assertRaises(ValueError): screen(x)

    def test_invalid_voltage_and_slew(self):
        for bad in (True, float("nan"), float("inf"), -1, None, "60"):
            for key in ("slew_bound_v_per_s", "voltage_uncertainty_v", "rx_required_min_v"):
                x = sample(); x[key] = bad
                with self.subTest(bad=bad, key=key), self.assertRaises(ValueError): screen(x)

    def test_invalid_source(self):
        for key, bad in (("source_kind", "author_claim"), ("slew_bound_evidence", "verified")):
            x = sample(); x[key] = bad
            with self.assertRaises(ValueError): screen(x)

    def test_overflow_rejected(self):
        x = sample(); x["slew_bound_v_per_s"] = 1e308
        x["timestamp_uncertainty_s"] = 1e308
        with self.assertRaises(ValueError): screen(x)

    def test_stable_replay(self):
        self.assertEqual(screen(BASE), screen(sample()))

    def test_always_never_hardware_or_critical_stop(self):
        r = screen(sample())
        for k in ("hardware_approved", "physical_measures_authenticated", "instantaneous_voltage_proven", "critical_stop_authorized"):
            self.assertIs(r[k], False)


if __name__ == "__main__":
    unittest.main()
