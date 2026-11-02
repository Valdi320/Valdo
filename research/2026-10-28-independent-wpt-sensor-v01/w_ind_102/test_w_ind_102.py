import json
import tempfile
import unittest
from pathlib import Path

from .w_ind_102 import DATA_PATH, load_rows, validate_rows, build_report


class TestWInd102(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_rows(DATA_PATH)
        cls.report = build_report(cls.rows)

    def test_exactly_22_manufacturer_points(self):
        self.assertEqual(self.report["manufacturer_points"]["count"], 22)
        self.assertEqual(self.report["manufacturer_points"]["am100_count"], 11)
        self.assertEqual(self.report["manufacturer_points"]["am10_count"], 11)

    def test_an4913_applicability_includes_64kc(self):
        self.assertIn("ST25DV64KC", self.report["source"]["applicable_parts_table_1"])

    def test_iso_class1_setup_is_not_board_specific(self):
        source = self.report["source"]
        self.assertIn("ISO/IEC Class 1", source["measurement_setup"])
        self.assertIn("does not qualify", source["board_transfer_limit"])

    def test_reported_power_matches_v_times_i(self):
        for row in self.rows:
            self.assertAlmostEqual(row["v_eh_v"] * row["i_eh_ma"], row["p_eh_mw"], places=3)

    def test_am100_and_am10_maxima(self):
        points = self.report["manufacturer_points"]
        self.assertAlmostEqual(points["max_am100_mw"], 8.64, places=3)
        self.assertAlmostEqual(points["max_am10_mw"], 12.593, places=3)

    def test_400mw_continuous_pilot_is_no_go(self):
        pilot = self.report["pilot_400mw_avg_1500mw_peak"]
        self.assertEqual(pilot["nfc_eh_for_continuous_pilot"], "NO_GO")
        self.assertAlmostEqual(pilot["avg_shortfall_factor"], 31.763678, places=5)
        self.assertLess(pilot["avg_ratio_of_best_reference_pct"], 3.2)

    def test_1500mw_peak_is_outside_reference(self):
        pilot = self.report["pilot_400mw_avg_1500mw_peak"]
        self.assertGreater(pilot["peak_shortfall_factor"], 119.0)
        self.assertLess(pilot["peak_ratio_of_best_reference_pct"], 0.85)

    def test_microsensor_gate_is_conditional(self):
        micro = self.report["proposed_microsensor_gate"]
        self.assertEqual(micro["status"], "CONDITIONAL_REFERENCE_ONLY_NOT_BOARD_QUALIFIED")
        self.assertEqual(micro["manufacturer_points_meeting_reference_gate"], 20)
        self.assertAlmostEqual(micro["minimum_reference_power_mw"], 1.035, places=3)
        self.assertGreaterEqual(micro["minimum_reference_margin_factor"], 4.1)

    def test_buffer_is_only_an_energy_lower_bound(self):
        buf = self.report["illustrative_peak_buffer"]
        self.assertAlmostEqual(buf["energy_uj"], 50.0, places=3)
        self.assertAlmostEqual(buf["nominal_capacitance_uf_min"], 36.284, places=2)
        self.assertIn("NOT_SELECTED", buf["status"])

    def test_no_hardware_or_battery_approval(self):
        flags = self.report["electrical_and_rf_constraints"]
        self.assertFalse(flags["hardware_approved"])
        self.assertFalse(flags["battery_bms_dock_connected"])
        self.assertEqual(flags["physical_measurements_performed"], 0)

    def test_duplicate_point_rejected(self):
        with self.assertRaises(ValueError):
            validate_rows(self.rows + [dict(self.rows[0])])

    def test_missing_point_rejected(self):
        with self.assertRaises(ValueError):
            validate_rows(self.rows[:-1])

    def test_tampered_power_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            path.write_text(DATA_PATH.read_text(encoding="utf-8").replace(
                "100,0.5,3.3,0.7,2.31", "100,0.5,3.3,0.7,99.0", 1
            ), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_rows(path)

    def test_invalid_am_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            path.write_text(DATA_PATH.read_text(encoding="utf-8").replace(
                "100,0.5,3.3,0.7,2.31", "77,0.5,3.3,0.7,2.31", 1
            ), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_rows(path)

    def test_report_deterministic(self):
        self.assertEqual(json.dumps(self.report, sort_keys=True),
                         json.dumps(build_report(self.rows), sort_keys=True))


if __name__ == "__main__":
    unittest.main()
