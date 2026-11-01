import hashlib
import unittest

from w84_trace_gate import demo, evaluate, parse_csv


class TraceGateTest(unittest.TestCase):
    def setUp(self):
        self.meta, self.raw = demo()

    def with_text(self, text):
        raw = text.encode("utf-8")
        m = dict(self.meta, trace_sha256=hashlib.sha256(raw).hexdigest())
        return evaluate(m, raw)

    def test_demo_numeric_result(self):
        r = evaluate(self.meta, self.raw)
        self.assertEqual(r["tx_input_energy_uj"], "100.000")
        self.assertEqual(r["rx_output_energy_uj"], "16.500")
        self.assertEqual(r["apparent_cycle_efficiency_pct"], "16.500")
        self.assertEqual(r["minimum_sampled_rail_mv"], "3300.000")
        self.assertEqual(r["guarded_sampled_rail_mv"], "3280.000")
        self.assertFalse(r["evidence_eligible"])
        self.assertEqual(r["hardware_release"], "BLOCKED")
        self.assertIn("not_own_bench_measurement", r["reject_reasons"])

    def test_sha_mismatch_rejected(self):
        with self.assertRaisesRegex(ValueError, "trace_sha256_mismatch"):
            evaluate(dict(self.meta, trace_sha256="0" * 64), self.raw)

    def test_missing_hash_rejected(self):
        with self.assertRaisesRegex(ValueError, "sha256_required"):
            evaluate(dict(self.meta, trace_sha256=""), self.raw)

    def test_unknown_provenance_rejected(self):
        with self.assertRaisesRegex(ValueError, "invalid_provenance"):
            evaluate(dict(self.meta, provenance="measurement"), self.raw)

    def test_csv_header_changed_rejected(self):
        with self.assertRaisesRegex(ValueError, "unexpected_csv_columns"):
            self.with_text(self.raw.decode().replace("tx_mv", "voltage_v"))

    def test_duplicate_timestamp_rejected(self):
        with self.assertRaisesRegex(ValueError, "nonmonotonic_timestamp"):
            self.with_text(self.raw.decode().replace("1000,5000", "0,5000"))

    def test_first_timestamp_not_zero(self):
        with self.assertRaisesRegex(ValueError, "trace_must_start_at_zero"):
            self.with_text(self.raw.decode().replace("0,5000", "7,5000", 1))

    def test_negative_current_rejected(self):
        with self.assertRaisesRegex(ValueError, "negative_or_nonfinite_value"):
            self.with_text(self.raw.decode().replace(",4000,", ",-4000,", 1))

    def test_nan_voltage_rejected(self):
        with self.assertRaisesRegex(ValueError, "negative_or_nonfinite_value"):
            self.with_text(self.raw.decode().replace(",3300,1000,", ",nan,1000,", 1))

    def test_unknown_phase_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown_radio_phase"):
            self.with_text(self.raw.decode().replace(",ack\n", ",unsafe\n"))

    def test_gap_exceeded(self):
        r = evaluate(dict(self.meta, max_gap_us=500), self.raw)
        self.assertIn("sample_gap_exceeded", r["reject_reasons"])

    def test_guarded_voltage_rejected(self):
        r = evaluate(dict(self.meta, rail_uncertainty_mv=310), self.raw)
        self.assertIn("sampled_rail_below_guarded_floor", r["reject_reasons"])

    def test_missing_radio_phase(self):
        r = self.with_text(self.raw.decode().replace(",ack\n", ",idle\n"))
        self.assertIn("rf_cycle_incomplete", r["reject_reasons"])

    def test_zero_tx_energy(self):
        r = self.with_text(self.raw.decode().replace(",4000,", ",0,"))
        self.assertIn("zero_tx_input_energy", r["reject_reasons"])
        self.assertIsNone(r["apparent_cycle_efficiency_pct"])

    def test_rx_exceeds_tx(self):
        r = self.with_text(self.raw.decode().replace(",1000,", ",9000,"))
        self.assertIn("rx_energy_exceeds_tx_input_check_storage_or_channels", r["reject_reasons"])

    def test_bench_claim_without_instrument_rejected(self):
        r = evaluate(dict(self.meta, provenance="bench_measured"), self.raw)
        self.assertIn("bench_trace_missing_provenance_metadata", r["reject_reasons"])
        self.assertIn("bench_trace_shorter_than_ten_250ms_leases", r["reject_reasons"])
        self.assertIn("storage_end_state_not_declared_equal", r["reject_reasons"])
        self.assertFalse(r["evidence_eligible"])

    def test_manufacturer_data_not_own_measurement(self):
        r = evaluate(dict(self.meta, provenance="manufacturer_data"), self.raw)
        self.assertIn("not_own_bench_measurement", r["reject_reasons"])

    def test_no_rail_guarantee_between_samples(self):
        r = evaluate(self.meta, self.raw)
        self.assertIn("subsample_brownouts", r["unverified"])

    def test_infinite_or_negative_manifest_limits(self):
        for value in ("nan", "Infinity", -1):
            with self.subTest(value=value), self.assertRaises(ValueError):
                evaluate(dict(self.meta, max_gap_us=value), self.raw)

    def test_zero_gap_limit(self):
        with self.assertRaisesRegex(ValueError, "zero_gap_limit"):
            evaluate(dict(self.meta, max_gap_us=0), self.raw)

    def test_fractional_time_rejected(self):
        with self.assertRaisesRegex(ValueError, "fractional_timestamp_us"):
            self.with_text(self.raw.decode().replace("1000,5000", "1000.1,5000"))

    def test_one_sample_rejected(self):
        with self.assertRaisesRegex(ValueError, "insufficient_samples"):
            self.with_text("t_us,tx_mv,tx_ua,rx_mv,rx_ua,rail_mv,phase\n0,5000,4000,3300,1000,3300,sleep\n")


if __name__ == "__main__":
    unittest.main()
