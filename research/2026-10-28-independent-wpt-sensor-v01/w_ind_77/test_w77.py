import copy
import json
import math
import unittest
from pathlib import Path
from w77_trace_gate import evaluate

BASE = json.loads((Path(__file__).parent / "TRACE_SYNTHETIC.json").read_text())


def clone():
    return copy.deepcopy(BASE)


def fake_perfect():
    obj = clone()
    obj["cycles_observed"] = 3
    for key in obj["acquisition_claims"]:
        obj["acquisition_claims"][key] = True
    for w in obj["windows"]:
        w["source_kind"] = "bench_measured"  # TEST LABEL ONLY: not physical evidence
        w["rx_observed_min_v"] = 3.3
    return obj


class W77TraceTests(unittest.TestCase):
    def test_undervoltage_detected_when_total_energy_passes(self):
        r = evaluate(BASE)
        self.assertAlmostEqual(r["tx_mean_mw"], 20)
        self.assertAlmostEqual(r["extra_wh_day_nominal"], 0.4104)
        self.assertNotIn("CONSERVATIVE_TX_ENERGY_BUDGET_EXCEEDED", r["blockers"])
        self.assertIn("OBSERVED_RX_VOLTAGE_BELOW_ILLUSTRATIVE_MIN", r["blockers"])

    def test_undervoltage_even_if_fake_measurement_qualified(self):
        x = fake_perfect()
        x["windows"][1]["rx_observed_min_v"] = 2.5
        self.assertIn("OBSERVED_RX_VOLTAGE_BELOW_ILLUSTRATIVE_MIN", evaluate(x)["blockers"])

    def test_measured_labels_never_certify_hardware(self):
        r = evaluate(fake_perfect())
        self.assertEqual(r["status"], "DIGITAL_ENERGY_AND_OBSERVED_VOLTAGE_SCREEN_ONLY")
        for k in ("hardware_approved", "safety_cuts_proven", "physical_measurements_verified_by_software", "instantaneous_continuity_proven"):
            self.assertIs(r[k], False)

    def test_missing_physical_evidence(self):
        self.assertIn("NOT_ALL_WINDOWS_BENCH_MEASURED", evaluate(BASE)["blockers"])

    def test_too_few_cycles(self):
        self.assertIn("TOO_FEW_CYCLES", evaluate(BASE)["blockers"])

    def test_unverified_claims(self):
        r = evaluate(BASE)
        for key in BASE["acquisition_claims"]:
            self.assertIn("UNVERIFIED_" + key.upper(), r["blockers"])

    def test_point_samples_cannot_prove_integrated_energy(self):
        x = fake_perfect()
        x["windows"][0]["tx_capture_mode"] = "point_samples"
        self.assertIn("TX_POINT_SAMPLING_CAN_MISS_SPIKES", evaluate(x)["blockers"])

    def test_sampling_gap_limit(self):
        x = fake_perfect()
        x["windows"][1]["rx_max_sample_gap_ms"] = 15
        self.assertIn("RX_SAMPLING_GAP_EXCEEDS_SCREEN", evaluate(x)["blockers"])

    def test_sampling_gap_equal_boundary(self):
        x = fake_perfect()
        x["windows"][1]["rx_max_sample_gap_ms"] = 10
        self.assertNotIn("RX_SAMPLING_GAP_EXCEEDS_SCREEN", evaluate(x)["blockers"])

    def test_uncertain_voltage_trips_minimum(self):
        x = fake_perfect()
        x["windows"][0]["rx_observed_min_v"] = 3.1
        x["windows"][0]["rx_voltage_uncertainty_v"] = 0.2
        self.assertIn("OBSERVED_RX_VOLTAGE_BELOW_ILLUSTRATIVE_MIN", evaluate(x)["blockers"])

    def test_energy_uncertainty_raises_upper_bound(self):
        x = fake_perfect()
        for w in x["windows"]:
            w["tx_relative_uncertainty_pct"] = 50
        r = evaluate(x)
        self.assertAlmostEqual(r["tx_conservative_upper_mean_mw"], 30)
        self.assertIn("CONSERVATIVE_TX_ENERGY_BUDGET_EXCEEDED", r["blockers"])

    def test_energy_spike_in_small_window(self):
        x = fake_perfect()
        x["windows"][1]["tx_integrated_mj"] = 400
        self.assertIn("CONSERVATIVE_TX_ENERGY_BUDGET_EXCEEDED", evaluate(x)["blockers"])

    def test_rx_minimum_exact_limit_passes_digital_screen(self):
        x = fake_perfect()
        x["windows"][0]["rx_observed_min_v"] = 3.0
        self.assertNotIn("OBSERVED_RX_VOLTAGE_BELOW_ILLUSTRATIVE_MIN", evaluate(x)["blockers"])

    def test_insufficient_tx_input_cannot_pass(self):
        x = fake_perfect()
        for w in x["windows"]: w["tx_integrated_mj"] = 0
        self.assertIn("TX_INPUT_BELOW_SENSOR_BASELINE", evaluate(x)["blockers"])

    def test_reject_timestamp_gap(self):
        x = clone(); x["windows"][1]["start_s"] = 9.91
        with self.assertRaises(ValueError): evaluate(x)

    def test_reject_timestamp_overlap(self):
        x = clone(); x["windows"][1]["start_s"] = 9.8
        with self.assertRaises(ValueError): evaluate(x)

    def test_reject_incomplete_cycle(self):
        x = clone(); x["cycle_seconds"] = 31
        with self.assertRaises(ValueError): evaluate(x)

    def test_reject_out_of_order(self):
        x = clone(); x["windows"].reverse()
        with self.assertRaises(ValueError): evaluate(x)

    def test_reject_zero_window(self):
        x = clone(); x["windows"][1]["end_s"] = 9.9
        with self.assertRaises(ValueError): evaluate(x)

    def test_reject_gap_longer_than_window(self):
        x = clone(); x["windows"][1]["rx_max_sample_gap_ms"] = 200
        with self.assertRaises(ValueError): evaluate(x)

    def test_reject_unknown_source(self):
        x = clone(); x["windows"][0]["source_kind"] = "author_claim"
        with self.assertRaises(ValueError): evaluate(x)

    def test_reject_unknown_capture_mode(self):
        x = clone(); x["windows"][0]["tx_capture_mode"] = "calculated_from_standby"
        with self.assertRaises(ValueError): evaluate(x)

    def test_reject_bad_bool_acquisition_claims(self):
        x = clone(); x["acquisition_claims"]["monotonic_clock"] = 1
        with self.assertRaises(ValueError): evaluate(x)

    def test_reject_non_integer_cycles(self):
        for bad in (3.0, True, "3", 0):
            x = clone(); x["cycles_observed"] = bad
            with self.subTest(bad=bad), self.assertRaises(ValueError): evaluate(x)

    def test_reject_nonfinite_bad_powers(self):
        for bad in (float("nan"), float("inf"), -1, True, None, "2"):
            x = clone(); x["windows"][0]["tx_integrated_mj"] = bad
            with self.subTest(bad=bad), self.assertRaises(ValueError): evaluate(x)

    def test_reject_nonfinite_uncertainty(self):
        for bad in (float("nan"), float("inf"), -1, 100, True):
            x = clone(); x["windows"][0]["tx_relative_uncertainty_pct"] = bad
            with self.subTest(bad=bad), self.assertRaises(ValueError): evaluate(x)

    def test_reject_boolean_required_voltage(self):
        x = clone(); x["rx_required_min_v"] = False
        with self.assertRaises(ValueError): evaluate(x)

    def test_overflow_rejected(self):
        x = clone(); x["windows"][0]["tx_integrated_mj"] = 1e308
        x["windows"][1]["tx_integrated_mj"] = 1e308
        with self.assertRaises(ValueError): evaluate(x)

    def test_missing_or_unknown_windows(self):
        for bad in ([], None, False, {}):
            x = clone(); x["windows"] = bad
            with self.subTest(bad=bad), self.assertRaises(ValueError): evaluate(x)

    def test_repeatable(self):
        self.assertEqual(evaluate(BASE), evaluate(clone()))


if __name__ == "__main__":
    unittest.main()
