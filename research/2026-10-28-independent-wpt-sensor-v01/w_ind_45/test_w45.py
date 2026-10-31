"""28 original deterministic software-only W45 regression tests."""
import unittest
import json
from w45_leakage_screen import off_node_v, on_resistor_mw, results, to_csv, RESISTORS_OHM, SUPPLIES_V, STRESS_UA

class LeakageTests(unittest.TestCase):
    def test_old_47k_fails(self):
        self.assertGreater(off_node_v(47000,5,60),0.4)
    def test_old_47k_2p8482(self):
        self.assertAlmostEqual(off_node_v(47000,5,60),2.8482)
    def test_10k_fails(self):
        self.assertGreater(off_node_v(10000,5,60),0.4)
    def test_10k_0p606(self):
        self.assertAlmostEqual(off_node_v(10000,5,60),0.606)
    def test_4k7_passes_assumed(self):
        self.assertLess(off_node_v(4700,5,60),0.4)
    def test_4k7_0p28482(self):
        self.assertAlmostEqual(off_node_v(4700,5,60),0.28482)
    def test_2k2_passes_assumed(self):
        self.assertLess(off_node_v(2200,5,60),0.4)
    def test_margin_4k7(self):
        self.assertAlmostEqual(0.4-off_node_v(4700,5,60),0.11518)
    def test_47k_synthetic_fail_count(self):
        self.assertEqual(next(x for x in results()["records"] if x["r_ohm"]==47000)["failing_synthetic_cases"],6)
    def test_10k_synthetic_fail_count(self):
        self.assertEqual(next(x for x in results()["records"] if x["r_ohm"]==10000)["failing_synthetic_cases"],3)
    def test_4k7_synthetic_no_fail(self):
        self.assertEqual(next(x for x in results()["records"] if x["r_ohm"]==4700)["failing_synthetic_cases"],0)
    def test_2k2_synthetic_no_fail(self):
        self.assertEqual(next(x for x in results()["records"] if x["r_ohm"]==2200)["failing_synthetic_cases"],0)
    def test_36_scenarios(self):
        self.assertEqual(results()["total_synthetic_cases"],36)
    def test_optimum_only_among_four_options(self):
        self.assertEqual(results()["preferred_only_if_assumptions_hold_ohm"],4700)
    def test_power_4k7_ideal(self):
        self.assertAlmostEqual(on_resistor_mw(4700),5.372877713303245)
    def test_power_47k_ideal(self):
        self.assertAlmostEqual(on_resistor_mw(47000),0.5372877713303246)
    def test_power_tradeoff(self):
        self.assertGreater(on_resistor_mw(2200),on_resistor_mw(4700))
    def test_increasing_resistance_increases_off(self):
        self.assertEqual(sorted([off_node_v(r,5,60) for r in RESISTORS_OHM]),[off_node_v(r,5,60) for r in RESISTORS_OHM])
    def test_increasing_current_increases_off(self):
        for r in RESISTORS_OHM:
            self.assertEqual(sorted([off_node_v(r,5,ua) for ua in STRESS_UA]),[off_node_v(r,5,ua) for ua in STRESS_UA])
    def test_increasing_supply_nondecreasing_off(self):
        for r in RESISTORS_OHM:
            self.assertEqual(sorted([off_node_v(r,v,60) for v in SUPPLIES_V]),[off_node_v(r,v,60) for v in SUPPLIES_V])
    def test_zero_injected_floats(self):
        self.assertEqual(off_node_v(4700,5,0),0)
    def test_capped_at_source(self):
        self.assertEqual(off_node_v(1000000,5,60),5)
    def test_tolerance_increases_leakage(self):
        self.assertGreater(off_node_v(4700,5,60,.01),off_node_v(4700,5,60,0))
    def test_tolerance_decreases_resistance_increases_on_power(self):
        self.assertGreater(on_resistor_mw(4700,5,.01),on_resistor_mw(4700,5,0))
    def test_negative_inputs_rejected(self):
        for args in [(0,5,60),(4700,-1,60),(4700,5,-1)]:
            with self.assertRaises(ValueError):off_node_v(*args)
    def test_invalid_tolerance_rejected(self):
        for t in [-.01,1]:
            with self.assertRaises(ValueError):off_node_v(4700,5,60,t)
    def test_evidence_does_not_claim_hardware(self):
        data=results()
        self.assertFalse(data["hardware_safety_proven"])
        self.assertFalse(data["hardware_power_authorized"])
        self.assertFalse(data["w44_kicad_modified"])
        self.assertIn("None of these figures guarantees",data["IMPORTANT"])
    def test_deterministic_csv_and_json(self):
        data=results()
        self.assertEqual(to_csv(data),to_csv(results()))
        self.assertEqual(json.dumps(data,sort_keys=True),json.dumps(results(),sort_keys=True))
        self.assertIn("No receiver VIL",data["IMPORTANT"])

if __name__=="__main__":
    unittest.main()
