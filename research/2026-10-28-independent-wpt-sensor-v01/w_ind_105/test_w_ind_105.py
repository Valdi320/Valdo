"""Adversarial and arithmetic tests for W-IND-105."""
from __future__ import annotations

import json
import math
import unittest

from w_ind_102.w_ind_102 import load_rows
from w_ind_105.w_ind_105 import (
    READER,
    SENSOR_SCENARIO,
    build_report,
    screen_point,
)


class ReaderInclusiveNfcEnergyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_rows()
        cls.report = build_report(cls.rows)

    def test_exactly_22_manufacturer_points(self):
        self.assertEqual(self.report["sweep"]["manufacturer_point_count"], 22)

    def test_reader_active_chip_reference_power(self):
        modes = self.report["reader_modes"]
        self.assertAlmostEqual(modes["active_chip_reference_typ_mw"], 33.6, places=9)
        self.assertAlmostEqual(modes["active_chip_reference_max_mw"], 55.2, places=9)

    def test_reader_active_table_disables_rfo_segments(self):
        self.assertIs(self.report["reader_modes"]["rfo_segments_enabled"], False)
        self.assertIs(self.report["assumptions"]["reader_antenna_drive_power_included"], False)

    def test_reader_wake_power_is_micro_watts(self):
        modes = self.report["reader_modes"]
        self.assertAlmostEqual(modes["wake_typ_uw"], 4.32, places=9)
        self.assertAlmostEqual(modes["wake_max_uw"], 12.0, places=9)

    def test_wake_mode_gets_no_energy_harvesting_credit(self):
        modes = self.report["reader_modes"]
        self.assertIs(modes["field_generated_in_wake_mode"], False)
        self.assertEqual(modes["wake_mode_tag_eh_credit_mw"], 0.0)

    def test_reader_power_down_and_ready_units(self):
        modes = self.report["reader_modes"]
        self.assertAlmostEqual(modes["power_down_typ_uw"], 1.2, places=9)
        self.assertAlmostEqual(modes["ready_typ_mw"], 8.16, places=9)
        self.assertAlmostEqual(modes["ready_max_mw"], 18.0, places=9)

    def test_baseline_1a_m_am10_is_exact(self):
        point = self.report["sensor_reference"]["baseline_1a_m_am10"]
        self.assertEqual(point["p_eh_mw_manufacturer"], 1.035)
        self.assertAlmostEqual(point["p_sensor_rail_mw_while_field_on_assumed"], 0.67275, places=9)

    def test_baseline_field_duty_average_is_consistent_with_w_ind_104(self):
        point = self.report["sensor_reference"]["baseline_1a_m_am10"]
        self.assertAlmostEqual(point["field_on_time_per_period_s_assumed"], 0.495, places=9)
        self.assertAlmostEqual(point["average_tag_rail_mw_assumed"], 0.33301125, places=9)
        self.assertAlmostEqual(point["average_sensor_side_margin_ratio"], 1.3427872984, places=8)

    def test_baseline_reader_to_sensor_ratio_and_tag_count(self):
        point = self.report["sensor_reference"]["baseline_1a_m_am10"]
        self.assertAlmostEqual(point["reader_to_sensor_ratio_typ"], 49.9442586399, places=8)
        self.assertEqual(point["ideal_tag_count_lower_bound_typ"], 50)
        self.assertEqual(point["ideal_tag_count_lower_bound_max"], 83)

    def test_baseline_reader_energy_per_period_is_lower_bound(self):
        sensor = self.report["sensor_reference"]
        self.assertAlmostEqual(sensor["baseline_reader_chip_energy_per_period_mj"], 16.632, places=9)
        self.assertAlmostEqual(sensor["baseline_tag_rail_energy_per_period_mj"], 0.33301125, places=9)

    def test_best_an4913_point_and_ideal_tag_count(self):
        point = self.report["best_tag_point_in_an4913"]
        self.assertEqual(point["am_percent"], 10)
        self.assertEqual(point["h_a_per_m_rms"], 5.5)
        self.assertEqual(point["p_eh_mw_manufacturer"], 12.593)
        self.assertAlmostEqual(point["p_sensor_rail_mw_while_field_on_assumed"], 8.18545, places=9)
        self.assertAlmostEqual(point["average_tag_rail_mw_assumed"], 4.05179775, places=9)
        self.assertEqual(point["ideal_tag_count_lower_bound_typ"], 5)
        self.assertEqual(point["ideal_tag_count_lower_bound_max"], 7)

    def test_all_22_points_fail_dedicated_reader_break_even(self):
        sweep = self.report["sweep"]
        self.assertIs(sweep["all_22_average_tag_rail_outputs_below_reader_active_typ"], True)
        self.assertEqual(sweep["dedicated_harvesting_points_at_or_above_reader_reference"], 0)

    def test_sensor_side_margin_is_not_reader_energy_margin(self):
        point = self.report["sensor_reference"]["baseline_1a_m_am10"]
        self.assertGreater(point["average_sensor_side_margin_ratio"], 1.0)
        self.assertGreater(point["average_reader_chip_reference_mw"], point["average_tag_rail_mw_assumed"])

    def test_400mw_active_module_remains_far_above_best_tag_rail(self):
        self.assertLess(
            self.report["best_tag_point_in_an4913"]["average_tag_rail_mw_assumed"],
            400.0,
        )

    def test_boolean_efficiency_rejected(self):
        with self.assertRaises(ValueError):
            screen_point(self.rows[0], downstream_efficiency=True)

    def test_efficiency_above_one_rejected(self):
        with self.assertRaises(ValueError):
            screen_point(self.rows[0], downstream_efficiency=1.01)

    def test_nonfinite_tag_power_rejected(self):
        bad = dict(self.rows[0])
        bad["p_eh_mw"] = math.nan
        with self.assertRaises(ValueError):
            screen_point(bad)

    def test_boolean_am_rejected(self):
        bad = dict(self.rows[0])
        bad["am_percent"] = True
        with self.assertRaises(ValueError):
            screen_point(bad)

    def test_reader_with_rfo_enabled_rejected_as_wrong_reference(self):
        reader = dict(READER)
        reader["active_rfo_segments_enabled"] = True
        with self.assertRaises(ValueError):
            screen_point(self.rows[0], reader=reader)

    def test_reader_max_below_typ_rejected(self):
        reader = dict(READER)
        reader["active_max_ma"] = 10.0
        with self.assertRaises(ValueError):
            screen_point(self.rows[0], reader=reader)

    def test_field_duty_above_one_rejected(self):
        scenario = dict(SENSOR_SCENARIO)
        scenario["field_duty_during_off_time"] = 1.01
        with self.assertRaises(ValueError):
            screen_point(self.rows[0], scenario=scenario)

    def test_burst_must_fit_period(self):
        scenario = dict(SENSOR_SCENARIO)
        scenario["burst_ms"] = 1000.0
        with self.assertRaises(ValueError):
            screen_point(self.rows[0], scenario=scenario)

    def test_no_hardware_approval_or_battery_connection(self):
        limits = self.report["limits"]
        self.assertIs(limits["hardware_approved"], False)
        self.assertIs(limits["battery_bms_connected"], False)
        self.assertEqual(limits["physical_measurements"], 0)
        self.assertIs(limits["oomwoo_or_pr79_modified"], False)

    def test_json_is_strict_and_deterministic(self):
        first = json.dumps(self.report, sort_keys=True, allow_nan=False)
        second = json.dumps(build_report(self.rows), sort_keys=True, allow_nan=False)
        self.assertEqual(first, second)

    def test_manufacturer_data_hash_is_present(self):
        digest = self.report["provenance"]["manufacturer_data_sha256"]
        self.assertEqual(len(digest), 64)
        self.assertTrue(all(ch in "0123456789abcdef" for ch in digest))


if __name__ == "__main__":
    unittest.main()
