"""W70 digital adversarial tests. All constructed XML samples are SYNTHETIC."""
from __future__ import annotations
import math
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET
from w_ind_22.w_ind_22_netlist_guard import EXPECTED_NATIVE_NETS, EXPECTED_VALUES
from w_ind_70.w70_native_storage_gate import review_native_xml, main


def sample_xml(*, mutate=None):
    root = ET.Element("export")
    components = ET.SubElement(root, "components")
    for ref, value in EXPECTED_VALUES.items():
        item = ET.SubElement(components, "comp", ref=ref)
        ET.SubElement(item, "value").text = value
    nets = ET.SubElement(root, "nets")
    for name, pins in EXPECTED_NATIVE_NETS.items():
        entry = ET.SubElement(nets, "net", name=name)
        for pin in sorted(pins):
            ref, number = pin.split(".", 1)
            ET.SubElement(entry, "node", ref=ref, pin=number)
    if mutate is not None:
        mutate(root)
    return ET.tostring(root, encoding="utf-8")


class TestW70(unittest.TestCase):
    def assert_blocked(self, raw, *, matching=False):
        out = review_native_xml(raw)
        self.assertFalse(out["hardware_approved"])
        self.assertFalse(out["power_on_allowed"])
        self.assertFalse(out["residual_discharge_qualified"])
        self.assertFalse(out["battery_or_dock_allowed"])
        self.assertEqual(out["topology_exact_w22"], matching)
        return out

    def test_exact_w21_maps_post_second_cut_r2_only(self):
        out = self.assert_blocked(sample_xml(), matching=True)
        self.assertEqual(out["status"], "BLOCKED_EXTERNAL_TX_STORAGE_UNCHARACTERIZED")
        self.assertEqual(out["nominal_resistive_branches"]["R2"]["terminals"], ["/GND", "/TX_5V_CUT"])
        self.assertEqual(out["nominal_resistive_branches"]["R1"]["terminals"], ["/GND", "/MID"])
        self.assertIn("NOT a direct", out["between_cuts_bleeder"])

    def test_absence_of_declared_capacitors_is_not_zero_storage(self):
        out = self.assert_blocked(sample_xml(), matching=True)
        self.assertEqual(out["explicit_storage_items"], 0)
        self.assertEqual(out["off_board_tx_load_and_parasitics"], "UNKNOWN_NOT_ZERO")
        self.assertFalse(out["post_cut_storage_complete"])

    def test_nominal_bleed_power_and_threshold_screen(self):
        a = self.assert_blocked(sample_xml(), matching=True)["nominal_screen_only"]
        self.assertAlmostEqual(a["tx_r2_power_if_continuously_at_assumed_v_w"], 0.025)
        self.assertAlmostEqual(a["mid_r1_power_if_continuously_at_assumed_v_w"], 25/22000)
        self.assertAlmostEqual(a["tx_r2_energy_24h_if_continuously_at_assumed_v_wh"], 0.6)
        self.assertAlmostEqual(a["tx_r2_hypothetical_time_to_threshold_s"], math.log(10)*0.1)
        self.assertAlmostEqual(a["alternative_hypothetical_time_to_threshold_s"], math.log(10))
        self.assertAlmostEqual(a["alternative_loss_if_continuously_at_assumed_v_w"], 0.0025)

    def test_custom_screen_values_remain_hypothetical(self):
        out = review_native_xml(sample_xml(), hypothetical_supply_v=3.3,
                                hypothetical_cap_f=470e-6,
                                hypothetical_threshold_v=0.1,
                                alternative_bleeder_ohm=4700)
        self.assertEqual(out["status"], "BLOCKED_EXTERNAL_TX_STORAGE_UNCHARACTERIZED")
        self.assertAlmostEqual(out["nominal_screen_only"]["tx_r2_power_if_continuously_at_assumed_v_w"], 3.3**2/1000)
        self.assertFalse(out["local_safety_cuts_proven"])

    def test_added_capacitor_triggers_review_not_new_inferred_rc(self):
        def mutation(root):
            e = ET.SubElement(root.find("components"), "comp", ref="C1")
            ET.SubElement(e, "value").text = "100u"
        out = self.assert_blocked(sample_xml(mutate=mutation))
        self.assertEqual(out["status"], "BLOCKED_UNREVIEWED_NETLIST")

    def test_remove_tx_bleeder_triggers_review(self):
        def mutation(root):
            root.find("components").remove(next(c for c in root.find("components") if c.attrib.get("ref") == "R2"))
        self.assert_blocked(sample_xml(mutate=mutation))

    def test_bleeder_value_mutation_triggers_review(self):
        def mutation(root):
            next(c for c in root.find("components") if c.get("ref") == "R2").find("value").text = "10k"
        self.assert_blocked(sample_xml(mutate=mutation))

    def test_r1_does_not_become_postcut_on_swap(self):
        def mutation(root):
            mid = next(n for n in root.find("nets") if n.get("name") == "/MID")
            tx = next(n for n in root.find("nets") if n.get("name") == "/TX_5V_CUT")
            r1 = next(n for n in mid if n.get("ref") == "R1")
            r2 = next(n for n in tx if n.get("ref") == "R2")
            mid.remove(r1); tx.remove(r2); mid.append(r2); tx.append(r1)
        self.assert_blocked(sample_xml(mutate=mutation))

    def test_bypass_u2_output_to_source_invalid(self):
        def mutation(root):
            n = next(n for n in root.find("nets") if n.get("name") == "/VIN_5V")
            ET.SubElement(n, "node", ref="U2", pin="6")
        self.assert_blocked(sample_xml(mutate=mutation))

    def test_unknown_external_load_invalidates_netlist(self):
        def mutation(root):
            n = next(n for n in root.find("nets") if n.get("name") == "/TX_5V_CUT")
            ET.SubElement(n, "node", ref="J2", pin="1")
        self.assert_blocked(sample_xml(mutate=mutation))

    def test_duplicate_ledger_pin_rejected(self):
        def mutation(root):
            n = next(n for n in root.find("nets") if n.get("name") == "/GND")
            ET.SubElement(n, "node", ref="R2", pin="2")
        self.assert_blocked(sample_xml(mutate=mutation))

    def test_unknown_supply_value_rejected(self):
        def mutation(root):
            next(c for c in root.find("components") if c.get("ref") == "J1").find("value").text = "REAL_CHARGER_12V"
        self.assert_blocked(sample_xml(mutate=mutation))

    def test_empty_malformed_xml_rejected(self):
        for data in (b"", b"not xml", b"<export/>", b"<unknown/>"):
            with self.subTest(data=data):
                self.assert_blocked(data)

    def test_no_measurement_pretended(self):
        out = self.assert_blocked(sample_xml(), matching=True)
        self.assertEqual(out["physical_tests"], 0)
        self.assertEqual(out["data_origin"], "INPUT_XML_DIGITAL_NOT_A_PHYSICAL_MEASUREMENT")
        self.assertFalse(out["backfeed_excluded_by_physical_test"])

    def test_bad_hypothetical_arguments_fail_closed(self):
        variants = [dict(hypothetical_supply_v=float("nan")),
                    dict(hypothetical_supply_v=True),
                    dict(hypothetical_supply_v=12),
                    dict(hypothetical_cap_f=0),
                    dict(hypothetical_cap_f=float("inf")),
                    dict(hypothetical_threshold_v=5),
                    dict(alternative_bleeder_ohm=-1),
                    dict(alternative_bleeder_ohm="1000")]
        for kw in variants:
            with self.subTest(kw=kw), self.assertRaises(ValueError):
                review_native_xml(sample_xml(), **kw)

    def test_nonbytes_rejected(self):
        with self.assertRaises(TypeError):
            review_native_xml("<export/>")

    def test_cli_known_blocked_is_review_pass(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"native.xml"; p.write_bytes(sample_xml())
            report = Path(d)/"report.json"
            self.assertEqual(main([str(p), "--report", str(report)]), 0)
            import json
            self.assertEqual(json.loads(report.read_text())["status"], "BLOCKED_EXTERNAL_TX_STORAGE_UNCHARACTERIZED")

    def test_cli_changed_topology_exits_failure(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"native.xml"; p.write_bytes(b"<export/>")
            report = Path(d)/"report.json"
            self.assertEqual(main([str(p), "--report", str(report)]), 1)
            import json
            self.assertFalse(json.loads(report.read_text())["power_on_allowed"])

    def test_cli_absent_export_exits_failure(self):
        with tempfile.TemporaryDirectory() as d:
            report = Path(d)/"report.json"
            self.assertEqual(main([str(Path(d)/'no.xml'), "--report", str(report)]), 1)
            self.assertTrue(report.exists())


if __name__ == "__main__":
    unittest.main()
