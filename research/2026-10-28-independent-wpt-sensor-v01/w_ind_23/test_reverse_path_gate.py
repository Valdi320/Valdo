"""W-IND-23 synthetic netlists. Native KiCad export is separately exercised in CI."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

from reverse_path_gate import NETS, PARTS, audit_native, main, path


def fixture():
    root = ET.Element("export")
    components = ET.SubElement(root, "components")
    for ref, value in PARTS.items():
        c = ET.SubElement(components, "comp", ref=ref)
        ET.SubElement(c, "value").text = value
    nets = ET.SubElement(root, "nets")
    for name, members in NETS.items():
        n = ET.SubElement(nets, "net", name=name)
        for member in sorted(members):
            ref, pad = member.rsplit(".", 1)
            ET.SubElement(n, "node", ref=ref, pin=pad)
    return root


def encoded(root):
    return ET.tostring(root, encoding="utf-8")


def net(root, name):
    return next(n for n in root.find("nets") if n.get("name") == name)


class ReversePathEvidence(unittest.TestCase):
    def setUp(self):
        self.root = fixture()

    def blocked_unknown(self):
        report = audit_native(encoded(self.root))
        self.assertEqual(report["status"], "REVIEW_BLOCKED_UNKNOWN_TOPOLOGY")
        self.assertFalse(report["known_hazard_detected"])
        self.assertFalse(report["hardware_approved"])
        self.assertFalse(report["power_on_allowed"])
        return report

    def test_known_native_topology_reports_two_diodes_in_reverse(self):
        result = audit_native(encoded(self.root))
        self.assertTrue(result["known_hazard_detected"])
        self.assertEqual(result["reverse_path"], [
            "U2:VOUT6->VIN1_body_diode", "U1:VOUT6->VIN1_body_diode"])
        self.assertFalse(result["hardware_approved"])
        self.assertFalse(result["current_or_temperature_predicted"])

    def test_graph_is_directional(self):
        edges = [("TX", "MID", "U2"), ("MID", "VIN", "U1")]
        self.assertEqual(path(edges, "TX", "VIN"), ["U2", "U1"])
        self.assertEqual(path(edges, "VIN", "TX"), [])

    def test_single_reverse_isolator_blocks_abstract_path_only(self):
        for remaining in [[("TX", "MID", "U2")], [("MID", "VIN", "U1")]]:
            self.assertEqual(path(remaining, "TX", "VIN"), [])

    def test_transistor_value_changed_blocks_review(self):
        c = next(c for c in self.root.find("components") if c.get("ref") == "U2")
        c.find("value").text = "UNQUALIFIED_SWITCH"
        self.blocked_unknown()

    def test_wrong_pin_on_mid_blocks(self):
        n = net(self.root, "/MID")
        next(x for x in n if x.get("ref") == "U2" and x.get("pin") == "1").set("pin", "3")
        self.blocked_unknown()

    def test_diode_output_disconnected_blocks(self):
        n = net(self.root, "/TX_5V_CUT")
        n.remove(next(x for x in n if x.get("ref") == "U2"))
        self.blocked_unknown()

    def test_input_short_to_tx_blocks(self):
        for x in list(net(self.root, "/TX_5V_CUT")):
            net(self.root, "/VIN_5V").append(copy.deepcopy(x))
        self.root.find("nets").remove(net(self.root, "/TX_5V_CUT"))
        self.blocked_unknown()

    def test_enables_tied_blocks(self):
        for x in list(net(self.root, "/EN_B")):
            net(self.root, "/EN_A").append(copy.deepcopy(x))
        self.root.find("nets").remove(net(self.root, "/EN_B"))
        self.blocked_unknown()

    def test_additional_component_blocks(self):
        c = ET.SubElement(self.root.find("components"), "comp", ref="U3")
        ET.SubElement(c, "value").text = "TPS22918DBVR"
        self.blocked_unknown()

    def test_component_duplicate_blocks(self):
        self.root.find("components").append(copy.deepcopy(self.root.find("components")[1]))
        self.blocked_unknown()

    def test_duplicate_node_membership_blocks(self):
        ET.SubElement(net(self.root, "/MID"), "node", ref="U2", pin="6")
        self.blocked_unknown()

    def test_missing_ground_blocks(self):
        n = net(self.root, "/GND")
        n.remove(next(x for x in n if x.get("ref") == "J1"))
        self.blocked_unknown()

    def test_unknown_extra_net_blocks(self):
        ET.SubElement(self.root.find("nets"), "net", name="/NEW")
        self.blocked_unknown()

    def test_missing_nc_stub_blocks(self):
        self.root.find("nets").remove(net(self.root, "unconnected-(U1-CT-Pad4)"))
        self.blocked_unknown()

    def test_malformed_xml_blocks(self):
        for raw in (b"", b"<export>", b"<wrong/>", b"<export/>"):
            self.assertFalse(audit_native(raw)["hardware_approved"])
            self.assertFalse(audit_native(raw)["known_hazard_detected"])

    def test_cli_expect_known_blocker_is_not_approval(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder/"synthetic.xml").write_bytes(encoded(self.root))
            self.assertEqual(main([str(folder/"synthetic.xml"), "--report", str(folder/"result.json"),
                                   "--expect-known-blocker"]), 0)
            report = json.loads((folder/"result.json").read_text())
            self.assertFalse(report["power_on_allowed"])
            self.assertIn("sha256", " ".join(report.keys()))
            self.assertEqual(main([str(folder/"synthetic.xml"), "--report", str(folder/"result.json")]), 2)

    def test_cli_missing_native_xml_never_succeeds(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            self.assertEqual(main([str(folder/"missing.xml"), "--report", str(folder/"result.json"),
                                   "--expect-known-blocker"]), 1)
            report = json.loads((folder/"result.json").read_text())
            self.assertFalse(report["hardware_approved"])


if __name__ == "__main__":
    unittest.main()
