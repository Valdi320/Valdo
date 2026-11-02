import copy
import json
import math
import unittest
from pathlib import Path
from w80_threshold_window import audit

BASE = json.loads((Path(__file__).parent / "SCENARIO_SYNTHETIC.json").read_text(encoding="utf-8"))


def scenario():
    return copy.deepcopy(BASE)


def candidate(result, nominal):
    return next(x for x in result["illustrative_candidates"] if x["nominal_v"] == nominal)


class W80ThresholdTests(unittest.TestCase):
    def test_family_has_34_grid_points(self):
        self.assertEqual(audit(BASE)["family_grid_count"], 34)

    def test_nominal_rail_minimum(self):
        self.assertEqual(audit(BASE)["normal_rail_min_v"], "3.135000")

    def test_lower_threshold_boundary(self):
        self.assertEqual(audit(BASE)["nominal_threshold_static_window_v"]["lower"], "3.045685")

    def test_upper_threshold_boundary(self):
        self.assertEqual(audit(BASE)["nominal_threshold_static_window_v"]["upper"], "3.088670")

    def test_no_grid_member_in_feasible_window(self):
        r = audit(BASE)
        self.assertEqual(r["feasible_catalog_grid_nominal_v"], [])
        self.assertTrue(r["no_grid_member_satisfies_both_static_constraints"])

    def test_28_min_trip_too_low(self):
        x = candidate(audit(BASE), "2.800000")
        self.assertEqual(x["fall_min_v"], "2.758000")
        self.assertFalse(x["static_floor_protected"])

    def test_30_min_trip_too_low(self):
        x = candidate(audit(BASE), "3.000000")
        self.assertEqual(x["fall_min_v"], "2.955000")
        self.assertFalse(x["static_floor_protected"])

    def test_31_trip_floor_passes(self):
        x = candidate(audit(BASE), "3.100000")
        self.assertEqual(x["fall_min_v"], "3.053500")
        self.assertTrue(x["static_floor_protected"])

    def test_31_can_trip_at_normal_rail_min(self):
        x = candidate(audit(BASE), "3.100000")
        self.assertEqual(x["fall_max_v"], "3.146500")
        self.assertFalse(x["static_no_false_trip_at_normal_min"])

    def test_non_catalog_305_meets_only_static_window(self):
        x = candidate(audit(BASE), "3.050000")
        self.assertTrue(x["static_conditions_met"])
        self.assertFalse(x["catalog_grid_member"])
        self.assertFalse(x["approved_for_hardware"])

    def test_good_family_at_higher_rail_still_unapproved(self):
        x = scenario()
        x["normal_rail_nominal_v"] = "3.50"
        r = audit(x)
        self.assertIn("3.100000", r["feasible_catalog_grid_nominal_v"])
        self.assertFalse(r["hardware_approved"])

    def test_lower_floor_changes_static_window_only(self):
        x = scenario()
        x["sensor_floor_v"] = "2.70"
        r = audit(x)
        self.assertIn("2.800000", r["feasible_catalog_grid_nominal_v"])
        self.assertFalse(r["critical_stop_authorized"])

    def test_rail_below_sensor_floor_never_authorizes(self):
        x = scenario()
        x["normal_rail_nominal_v"] = "2.90"
        r = audit(x)
        self.assertEqual(r["feasible_catalog_grid_nominal_v"], [])
        self.assertFalse(r["hardware_approved"])

    def test_no_false_hysteresis_or_delay_qualification(self):
        r = audit(BASE)
        self.assertFalse(r["hysteresis_release_qualified"])
        self.assertFalse(r["timing_and_voltage_slew_qualified"])

    def test_independent_supply_not_proven(self):
        self.assertFalse(audit(BASE)["independent_monitor_supply_and_cut_qualified"])

    def test_dock_battery_never_approved(self):
        r = audit(BASE)
        self.assertFalse(r["battery_bms_and_dock_approved"])

    def test_reject_bool_numeric(self):
        x = scenario()
        x["sensor_floor_v"] = True
        with self.assertRaises(ValueError):
            audit(x)

    def test_reject_nan_and_infinity(self):
        for bad in (float("nan"), float("inf"), "-Infinity"):
            x = scenario()
            x["normal_rail_nominal_v"] = bad
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                audit(x)

    def test_reject_negative_values(self):
        for key in ("sensor_floor_v", "normal_rail_nominal_v", "supervisor_nominal_threshold_step_v"):
            x = scenario()
            x[key] = "-1"
            with self.subTest(key=key), self.assertRaises(ValueError):
                audit(x)

    def test_reject_fractional_tolerance_out_of_range(self):
        for key in ("normal_rail_fractional_tolerance", "supervisor_fractional_threshold_tolerance"):
            for bad in ("1", "-0.1"):
                x = scenario()
                x[key] = bad
                with self.subTest(key=key, bad=bad), self.assertRaises(ValueError):
                    audit(x)

    def test_reject_non_divisible_grid(self):
        x = scenario()
        x["supervisor_nominal_threshold_step_v"] = "0.07"
        with self.assertRaises(ValueError):
            audit(x)

    def test_reject_duplicate_candidate(self):
        x = scenario()
        x["illustrative_thresholds_v"].append("3.10")
        with self.assertRaises(ValueError):
            audit(x)

    def test_reject_candidate_outside_grid(self):
        x = scenario()
        x["illustrative_thresholds_v"].append("5.00")
        with self.assertRaises(ValueError):
            audit(x)

    def test_reject_absurdly_many_grid_values(self):
        x = scenario()
        x["supervisor_nominal_threshold_step_v"] = "0.0001"
        with self.assertRaises(ValueError):
            audit(x)

    def test_reject_missing_keys(self):
        x = scenario()
        del x["sensor_floor_v"]
        with self.assertRaises(KeyError):
            audit(x)

    def test_deterministic_report(self):
        self.assertEqual(audit(scenario()), audit(scenario()))


if __name__ == "__main__":
    unittest.main()
