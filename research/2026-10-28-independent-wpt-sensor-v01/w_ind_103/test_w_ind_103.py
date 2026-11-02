"""W-IND-103 regressions for finite, typed ST25DV manufacturer data."""
import copy
import csv
import json
import tempfile
import unittest
from pathlib import Path

from w_ind_102.w_ind_102 import DATA_PATH, build_report, load_rows, validate_rows


NUMERIC_FIELDS = ("h_a_per_m_rms", "v_eh_v", "i_eh_ma", "p_eh_mw")


class TestWInd103(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_rows(DATA_PATH)

    @staticmethod
    def _legacy_guard(row):
        # Exact pre-W103 numeric guard, retained only to reproduce the defect.
        return not (
            min(row["h_a_per_m_rms"], row["v_eh_v"], row["i_eh_ma"], row["p_eh_mw"]) <= 0
        ) and not (
            abs(row["v_eh_v"] * row["i_eh_ma"] - row["p_eh_mw"]) > 0.0051
        )

    @staticmethod
    def _write_raw_csv(raw_rows, directory):
        path = Path(directory) / "malformed_an4913.csv"
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(raw_rows[0]))
            writer.writeheader()
            writer.writerows(raw_rows)
        return path

    def _raw_rows(self):
        with DATA_PATH.open("r", encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))

    def test_nan_inf_and_negative_inf_rejected_in_every_numeric_field(self):
        for field in NUMERIC_FIELDS:
            for bad in (float("nan"), float("inf"), float("-inf")):
                damaged = [dict(row) for row in self.rows]
                damaged[0][field] = bad
                with self.subTest(field=field, bad=bad):
                    with self.assertRaises(ValueError):
                        validate_rows(damaged)

    def test_boolean_string_and_none_rejected_in_every_numeric_field(self):
        for field in NUMERIC_FIELDS:
            for bad in (True, False, "3.3", None):
                damaged = [dict(row) for row in self.rows]
                damaged[0][field] = bad
                with self.subTest(field=field, bad=bad):
                    with self.assertRaises(ValueError):
                        validate_rows(damaged)

    def test_am_percent_requires_exact_integer(self):
        for bad in (100.0, True, "100", None):
            damaged = [dict(row) for row in self.rows]
            damaged[0]["am_percent"] = bad
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    validate_rows(damaged)

    def test_missing_numeric_column_rejected(self):
        damaged = [dict(row) for row in self.rows]
        damaged[0].pop("p_eh_mw")
        with self.assertRaises(ValueError):
            validate_rows(damaged)

    def test_product_overflow_rejected(self):
        damaged = [dict(row) for row in self.rows]
        damaged[0]["v_eh_v"] = 1e308
        damaged[0]["i_eh_ma"] = 1e308
        with self.assertRaises(ValueError):
            validate_rows(damaged)

    def test_legacy_guard_false_acceptance_is_reproduced_and_fixed(self):
        nan_case = dict(self.rows[0])
        nan_case["p_eh_mw"] = float("nan")
        inf_case = dict(self.rows[0])
        inf_case["v_eh_v"] = float("inf")
        inf_case["p_eh_mw"] = float("inf")
        self.assertTrue(self._legacy_guard(nan_case))
        self.assertTrue(self._legacy_guard(inf_case))
        for damaged in (nan_case, inf_case):
            bad_rows = [dict(row) for row in self.rows]
            bad_rows[0] = damaged
            with self.assertRaises(ValueError):
                validate_rows(bad_rows)

    def test_csv_nan_power_rejected_at_ingress(self):
        raw = self._raw_rows()
        raw[0]["p_eh_mw"] = "nan"
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_raw_csv(raw, directory)
            with self.assertRaises(ValueError):
                load_rows(path)

    def test_csv_infinite_voltage_and_power_pair_rejected_at_ingress(self):
        raw = self._raw_rows()
        raw[0]["v_eh_v"] = "inf"
        raw[0]["p_eh_mw"] = "inf"
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_raw_csv(raw, directory)
            with self.assertRaises(ValueError):
                load_rows(path)

    def test_csv_negative_infinite_current_rejected_at_ingress(self):
        raw = self._raw_rows()
        raw[0]["i_eh_ma"] = "-inf"
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_raw_csv(raw, directory)
            with self.assertRaises(ValueError):
                load_rows(path)

    def test_valid_22_point_dataset_remains_unchanged_and_strict_json(self):
        report = build_report(self.rows)
        encoded = json.dumps(report, sort_keys=True, allow_nan=False)
        self.assertEqual(report["manufacturer_points"]["count"], 22)
        self.assertAlmostEqual(report["manufacturer_points"]["max_am10_mw"], 12.593, places=3)
        self.assertAlmostEqual(report["manufacturer_points"]["max_am100_mw"], 8.640, places=3)
        self.assertIn('"count": 22', encoded)

    def test_wrong_point_count_still_rejected(self):
        with self.assertRaises(ValueError):
            validate_rows(self.rows[:-1])


if __name__ == "__main__":
    unittest.main()
