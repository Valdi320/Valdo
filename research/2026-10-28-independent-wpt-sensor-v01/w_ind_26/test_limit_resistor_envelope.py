"""W-IND-26: original regression and adversarial tests; NO physical tests."""
from dataclasses import replace
import json
import math
import unittest
from limit_resistor_envelope import Envelope, evaluate

class LimitResistorEnvelopeTests(unittest.TestCase):
    def setUp(self):
        self.c=Envelope()
        self.r=evaluate(self.c)

    def test_a1_offset_not_a3(self):
        self.assertEqual(self.c.offset_a1_input_25c_v,125e-6)
        self.assertNotEqual(self.c.offset_a1_input_25c_v,35e-6)

    def test_ina301_vendor_limit_current_bounds(self):
        self.assertEqual((self.c.ilimit_min_a,self.c.ilimit_max_a),(79.2e-6,80.8e-6))

    def test_limit_resistor_value(self):
        self.assertEqual(self.c.rlimit_ohm,8660)
        self.assertAlmostEqual(self.r["nominal_limit_v"],.6928,9)

    def test_nominal_trip(self):
        self.assertAlmostEqual(self.r["nominal_trip_a"],.3464,9)

    def test_resistor_temperature_derating(self):
        self.assertAlmostEqual(self.c.rlimit_initial_fraction+
            self.c.rlimit_tcr_ppm_c*1e-6*self.c.temperature_excursion_c,.02,9)

    def test_shunt_temperature_derating_explicit_unqualified(self):
        self.assertAlmostEqual(self.c.rshunt_initial_fraction+
            self.c.rshunt_tcr_ppm_c*1e-6*self.c.temperature_excursion_c,.03,9)
        self.assertFalse(self.r["shunt_mpn_qualified"])

    def test_gain_and_input_offset(self):
        self.assertEqual(self.c.gain,20)
        self.assertAlmostEqual((self.c.offset_a1_input_25c_v +
            self.c.offset_drift_v_c*self.c.temperature_excursion_c),175e-6,12)

    def test_threshold_bounds_include_10mv_unknown(self):
        self.assertAlmostEqual(self.r["min_effective_threshold_v_assumed"],.65865456,8)
        self.assertAlmostEqual(self.r["max_effective_threshold_v_assumed"],.72722256,8)

    def test_healthy_fault_bounds(self):
        self.assertAlmostEqual(self.r["max_healthy_output_v_assumed"],.622743,8)
        self.assertAlmostEqual(self.r["min_fault_output_v_assumed"],.770955,8)

    def test_static_window(self):
        self.assertTrue(self.r["hypothetical_window_positive"])
        self.assertAlmostEqual(self.r["no_false_trip_margin_mv_assumed"],35.91156,4)
        self.assertAlmostEqual(self.r["fault_detect_margin_mv_assumed"],43.73244,4)

    def test_guaranteed_intervals_only_in_model(self):
        self.assertLess(self.c.normal_peak_a,self.r["certain_no_false_trip_below_a_assumed"])
        self.assertGreater(self.c.fault_min_a,self.r["certain_trip_above_a_assumed"])
        self.assertAlmostEqual(self.r["certain_no_false_trip_below_a_assumed"],.317398,5)
        self.assertAlmostEqual(self.r["certain_trip_above_a_assumed"],.37741233,5)

    def test_corner_count(self):
        self.assertEqual(self.r["all_static_corners"],128)

    def test_350ma_healthy_is_not_guaranteed(self):
        self.assertFalse(evaluate(replace(self.c,normal_peak_a=.350))["hypothetical_window_positive"])

    def test_360ma_fault_is_not_guaranteed(self):
        self.assertFalse(evaluate(replace(self.c,fault_min_a=.360))["hypothetical_window_positive"])

    def test_low_resistor_not_qualified(self):
        self.assertFalse(evaluate(replace(self.c,rlimit_ohm=6600))["hypothetical_window_positive"])

    def test_high_resistor_not_qualified(self):
        self.assertFalse(evaluate(replace(self.c,rlimit_ohm=12000))["hypothetical_window_positive"])

    def test_bigger_unknown_comparator_drift_fails(self):
        self.assertFalse(evaluate(replace(self.c,unqualified_extra_threshold_v=.075))["hypothetical_window_positive"])

    def test_bigger_shunt_tcr_fails(self):
        self.assertFalse(evaluate(replace(self.c,rshunt_tcr_ppm_c=2000))["hypothetical_window_positive"])

    def test_low_current_gap_not_inferred(self):
        self.assertLess(self.r["certain_no_false_trip_below_a_assumed"],
                        self.r["certain_trip_above_a_assumed"])

    def test_invalid_nan_and_inf(self):
        for value in (float("nan"),float("inf"),-float("inf")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                evaluate(replace(self.c,rlimit_ohm=value))

    def test_invalid_orders_and_limits(self):
        for changes in ({"normal_peak_a":0},{"fault_min_a":.2},
                        {"ilimit_min_a":0},{"ilimit_max_a":70e-6},
                        {"rlimit_ohm":0},{"temperature_excursion_c":110},
                        {"rshunt_initial_fraction":1},
                        {"rlimit_tcr_ppm_c":-1}):
            with self.subTest(changes=changes),self.assertRaises(ValueError):
                evaluate(replace(self.c,**changes))

    def test_no_certification_or_direct_cut(self):
        for k in ("hardware_approved","power_on_allowed","shunt_mpn_qualified",
                  "comparator_overtemperature_offset_qualified",
                  "emi_transients_qualified","alert_open_drain_to_cutoff_qualified",
                  "autonomous_fod_and_thermal_qualified",
                  "single_fault_and_rail_loss_safe","dock_battery_bms_connected",
                  "radio_critical_cutoff_dependency"):
            with self.subTest(key=k):
                self.assertFalse(self.r[k])
        self.assertEqual(self.r["physical_measurements"],0)

    def test_json_reproducible(self):
        self.assertEqual(json.loads(json.dumps(evaluate())),self.r)

if __name__=="__main__":
    unittest.main()
