"""W71 deterministic adversarial tests; all electrical values are hypothetical."""
import json
import math
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET
from w_ind_70.test_w70 import sample_xml
from w_ind_71.w71_bleed_feasibility import assess, main


class W71Tests(unittest.TestCase):
    def setUp(self):
        self.xml = sample_xml()

    def test_baseline_proves_nominal_passive_constraint_conflict(self):
        a = assess(self.xml)
        self.assertEqual(a["status"], "BLOCKED_PASSIVE_CONSTRAINTS_INCOMPATIBLE")
        self.assertFalse(a["any_fixed_passive_resistor_meets_both_assumptions"])
        self.assertGreater(a["nominal_resistor_interval_ohm"]["minimum_from_standby"], 6000)
        self.assertLess(a["nominal_resistor_interval_ohm"]["maximum_from_decay"], 850)

    def test_existing_r2_worst_power(self):
        a = assess(self.xml)["existing_R2_worst_case_screen"]
        self.assertAlmostEqual(a["max_continuous_bleed_w"], 5.5**2/950)
        self.assertFalse(a["passes_power_budget"])

    def test_existing_r2_worst_decay(self):
        a = assess(self.xml)["existing_R2_worst_case_screen"]
        self.assertAlmostEqual(a["max_ideal_decay_s"],
                               1050 * 120e-6 * math.log(11))
        self.assertFalse(a["passes_decay_target"])

    def test_nominal_r2_provenance(self):
        a = assess(self.xml)
        self.assertEqual(a["existing_W21_R2_nominal_ohm"], 1000)
        self.assertTrue(a["w22_exact_netlist"])

    def test_feasible_small_cap_is_not_hardware_approval(self):
        a = assess(self.xml, cap_nominal_f=1e-6)
        self.assertTrue(a["any_fixed_passive_resistor_meets_both_assumptions"])
        self.assertEqual(a["status"], "BLOCKED_FEASIBLE_ONLY_UNDER_ASSUMPTIONS")
        self.assertFalse(a["hardware_approved"])

    def test_larger_cap_makes_worst_case_worse(self):
        a = assess(self.xml, cap_nominal_f=100e-6)
        b = assess(self.xml, cap_nominal_f=200e-6)
        self.assertGreater(b["existing_R2_worst_case_screen"]["max_ideal_decay_s"],
                           a["existing_R2_worst_case_screen"]["max_ideal_decay_s"])
        self.assertLess(b["nominal_resistor_interval_ohm"]["maximum_from_decay"],
                        a["nominal_resistor_interval_ohm"]["maximum_from_decay"])

    def test_cap_limit_is_true_boundary(self):
        a = assess(self.xml)
        lim = a["largest_feasible_nominal_capacitance_f"]
        lo = assess(self.xml, cap_nominal_f=lim*0.999)
        hi = assess(self.xml, cap_nominal_f=lim*1.001)
        self.assertTrue(lo["any_fixed_passive_resistor_meets_both_assumptions"])
        self.assertFalse(hi["any_fixed_passive_resistor_meets_both_assumptions"])

    def test_tolerance_increases_worst_case(self):
        base = assess(self.xml, cap_tolerance=0, resistor_tolerance=0)
        tol = assess(self.xml)
        self.assertGreater(
            tol["existing_R2_worst_case_screen"]["max_ideal_decay_s"],
            base["existing_R2_worst_case_screen"]["max_ideal_decay_s"])
        self.assertGreater(
            tol["existing_R2_worst_case_screen"]["max_continuous_bleed_w"],
            base["existing_R2_worst_case_screen"]["max_continuous_bleed_w"])

    def test_no_wpt_approvals_even_when_constraints_feasible(self):
        for f in (1e-6, 10e-6, 100e-6):
            a = assess(self.xml, cap_nominal_f=f)
            self.assertFalse(a["hardware_approved"])
            self.assertFalse(a["power_on_allowed"])
            self.assertFalse(a["independent_fod_thermal_cut_qualified"])
            self.assertEqual(a["physical_tests"], 0)
            self.assertEqual(a["actual_external_tx_storage"], "UNKNOWN_NOT_ZERO")
            self.assertFalse(a["battery_bms_dock_connected"])

    def test_open_bleeder_not_detected_or_claimed(self):
        self.assertFalse(assess(self.xml)["resistor_open_failure_auto_detected"])

    def test_source_is_digital_only(self):
        a = assess(self.xml)
        self.assertEqual(a["data_kind"], "MODEL_NOT_MEASURED")
        self.assertIn("inductors", a["power_safety_limit"])

    def test_mutated_resistor_value_blocks_before_optimization(self):
        def bad(root):
            for x in root.find("components"):
                if x.get("ref") == "R2":
                    x.find("value").text = "10k"
        a = assess(sample_xml(mutate=bad))
        self.assertEqual(a["status"], "BLOCKED_UNREVIEWED_NETLIST")
        self.assertFalse(a["hardware_approved"])

    def test_added_external_cap_still_requires_new_review(self):
        def bad(root):
            c = ET.SubElement(root.find("components"), "comp", ref="C1")
            ET.SubElement(c, "value").text = "100u"
        self.assertEqual(assess(sample_xml(mutate=bad))["status"],
                         "BLOCKED_UNREVIEWED_NETLIST")

    def test_short_bypassing_switch_rejected_by_upstream_w22(self):
        def bad(root):
            net = next(n for n in root.find("nets") if n.get("name") == "/VIN_5V")
            ET.SubElement(net, "node", ref="U2", pin="6")
        self.assertEqual(assess(sample_xml(mutate=bad))["status"],
                         "BLOCKED_UNREVIEWED_NETLIST")

    def test_bad_or_missing_netlist_blocks(self):
        for data in (b"", b"<export/>", b"<other/>", b"hello"):
            self.assertEqual(assess(data)["status"], "BLOCKED_UNREVIEWED_NETLIST")

    def test_input_types_and_domains_reject(self):
        invalid = [
            {"max_assumed_v": True},
            {"max_assumed_v": float("nan")},
            {"max_assumed_v": 12.0},
            {"cap_nominal_f": 0},
            {"cap_tolerance": 1},
            {"resistor_tolerance": -0.01},
            {"resistor_tolerance": float("inf")},
            {"threshold_assumed_v": 5.5},
            {"max_assumed_standby_bleed_w": 0},
            {"max_assumed_decay_s": 0},
        ]
        for kw in invalid:
            with self.subTest(kw=kw), self.assertRaises(ValueError):
                assess(self.xml, **kw)

    def test_string_netlist_not_accepted(self):
        with self.assertRaises(TypeError):
            assess("not bytes")

    def test_r2_screen_remains_watt_not_joule(self):
        a = assess(self.xml)["existing_R2_worst_case_screen"]
        self.assertTrue(0.03 < a["max_continuous_bleed_w"] < 0.04)

    def test_C_different_from_real_W21_cap_inventory(self):
        a = assess(self.xml)
        self.assertIn("hypothetical", a["source"])
        self.assertEqual(a["actual_external_tx_storage"], "UNKNOWN_NOT_ZERO")

    def test_cli_report_known_blocked_is_review_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            xml = Path(tmp)/"sample.xml"; xml.write_bytes(self.xml)
            report = Path(tmp)/"review.json"
            self.assertEqual(main([str(xml), "--report", str(report)]), 0)
            data = json.loads(report.read_text())
            self.assertEqual(data["status"], "BLOCKED_PASSIVE_CONSTRAINTS_INCOMPATIBLE")
            self.assertFalse(data["power_on_allowed"])

    def test_cli_mutation_returns_error_and_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            xml = Path(tmp)/"sample.xml"; xml.write_bytes(b"<export/>")
            report = Path(tmp)/"review.json"
            self.assertEqual(main([str(xml), "--report", str(report)]), 1)
            self.assertEqual(json.loads(report.read_text())["status"],
                             "BLOCKED_UNREVIEWED_NETLIST")

    def test_cli_missing_source_returns_error_and_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp)/"review.json"
            self.assertEqual(main([str(Path(tmp)/'absent.xml'), "--report", str(report)]), 1)
            self.assertEqual(json.loads(report.read_text())["status"],
                             "BLOCKED_INVALID_INPUT")


if __name__ == "__main__":
    unittest.main()
