"""Synthetic XML mutation tests. Native KiCad export is independently checked in CI."""
import copy
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

from w_ind_22_netlist_guard import EXPECTED_NETS, EXPECTED_VALUES, audit_netlist, main


def fixture() -> ET.Element:
    root = ET.Element("export", version="E")
    comps = ET.SubElement(root, "components")
    for ref, value in EXPECTED_VALUES.items():
        comp = ET.SubElement(comps, "comp", ref=ref)
        ET.SubElement(comp, "value").text = value
    nets = ET.SubElement(root, "nets")
    for i, (name, pins) in enumerate(EXPECTED_NETS.items(), 1):
        net = ET.SubElement(nets, "net", code=str(i), name=name)
        for item in sorted(pins):
            ref, pin = item.rsplit(".", 1)
            ET.SubElement(net, "node", ref=ref, pin=pin)
    return root


def xml(root):
    return ET.tostring(root, encoding="utf-8")


def net(root, name):
    return next(n for n in root.find("nets") if n.get("name") == name)


def mutate_node(root, name, ref, pin, replacement=None):
    n = net(root, name)
    target = next(x for x in n if x.get("ref") == ref and x.get("pin") == pin)
    if replacement is None:
        n.remove(target)
    else:
        target.attrib.update(replacement)


class NativeNetlistGuard(unittest.TestCase):
    def setUp(self):
        self.root = fixture()

    def fails(self):
        result = audit_netlist(xml(self.root))
        self.assertFalse(result["passed"], result)
        self.assertEqual(result["status"], "REVIEW_BLOCKED_NETLIST_MISMATCH")
        self.assertFalse(result["physical_approval"])
        return result

    def test_baseline_synthetic_contract(self):
        result = audit_netlist(xml(self.root))
        self.assertTrue(result["passed"], result)
        self.assertFalse(result["physical_approval"])
        self.assertFalse(result["power_on_allowed"])
        self.assertEqual(result["expected_net_count"], 6)

    def test_bypass_merges_input_and_output(self):
        source = net(self.root, "VIN_5V")
        output = net(self.root, "TX_5V_CUT")
        for x in list(output):
            source.append(copy.deepcopy(x))
        self.root.find("nets").remove(output)
        self.assertIn("TX_5V_CUT", str(self.fails()["errors"]))

    def test_bridge_input_and_mid(self):
        x=net(self.root, "MID")
        for child in list(x): net(self.root,"VIN_5V").append(copy.deepcopy(child))
        self.root.find("nets").remove(x)
        self.fails()

    def test_bridge_mid_and_output(self):
        x=net(self.root,"MID")
        for child in list(x): net(self.root,"TX_5V_CUT").append(copy.deepcopy(child))
        self.root.find("nets").remove(x)
        self.fails()

    def test_critical_en_a_b_short(self):
        n = net(self.root,"EN_B")
        for x in list(n): net(self.root,"EN_A").append(copy.deepcopy(x))
        self.root.find("nets").remove(n)
        self.fails()

    def test_short_en_to_power(self):
        x=net(self.root,"EN_A")
        for n in list(x): net(self.root,"VIN_5V").append(copy.deepcopy(n))
        self.root.find("nets").remove(x)
        self.fails()

    def test_source_return_connected_to_vin(self):
        mutate_node(self.root,"GND","J1","2")
        ET.SubElement(net(self.root,"VIN_5V"),"node",ref="J1",pin="2")
        self.fails()

    def test_unqualified_added_bypass_component(self):
        c=ET.SubElement(self.root.find("components"),"comp",ref="R5")
        ET.SubElement(c,"value").text="0R"
        self.assertIn("R5",str(self.fails()["errors"]))

    def test_gnd_resistor_omitted(self):
        mutate_node(self.root,"GND","R1","2")
        self.fails()

    def test_mid_critical_pin_omitted(self):
        mutate_node(self.root,"MID","U2","1")
        self.fails()

    def test_output_critical_pin_omitted(self):
        mutate_node(self.root,"TX_5V_CUT","U2","6")
        self.fails()

    def test_power_input_pin_omitted(self):
        mutate_node(self.root,"VIN_5V","J1","1")
        self.fails()

    def test_unaudited_extra_net(self):
        ET.SubElement(self.root.find("nets"),"net",name="BYPASS")
        self.fails()

    def test_renamed_mid_not_accepted(self):
        net(self.root,"MID").set("name","MID2")
        self.fails()

    def test_duplicate_pin_membership(self):
        ET.SubElement(net(self.root,"EN_A"),"node",ref="U2",pin="3")
        self.assertIn("duplicate",str(self.fails()["errors"]))

    def test_duplicate_named_net(self):
        self.root.find("nets").append(copy.deepcopy(net(self.root,"MID")))
        self.fails()

    def test_switched_component_relabeling(self):
        for c in self.root.find("components"):
            if c.get("ref") == "U2": c.find("value").text="TPS22950"
        self.fails()

    def test_unknown_third_component(self):
        for c in self.root.find("components"):
            if c.get("ref") == "U2": c.set("ref","U3")
        self.fails()

    def test_empty_xml_rejected(self):
        self.assertFalse(audit_netlist(b"")["passed"])

    def test_non_export_root_rejected(self):
        self.assertFalse(audit_netlist(b"<schematic/>")["passed"])

    def test_incomplete_export_rejected(self):
        self.assertFalse(audit_netlist(b"<export/>")["passed"])

    def test_missing_nodes_rejected(self):
        self.root.find("nets").clear()
        self.fails()

    def test_command_writes_blocked_attestation(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/"net.xml").write_bytes(b"<export/>")
            self.assertEqual(main([str(root/"net.xml"),"--report",str(root/"out.json")]),1)
            output=(root/"out.json").read_text()
            self.assertIn('"power_on_allowed": false',output)
            self.assertIn('"netlist_sha256":',output)

    def test_command_returns_zero_only_for_synthetic_fixture(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/"net.xml").write_bytes(xml(self.root))
            self.assertEqual(main([str(root/"net.xml"),"--report",str(root/"out.json")]),0)
            self.assertIn("NETLIST_EXACT_MATCH_NO_HARDWARE_APPROVAL",(root/"out.json").read_text())

    def test_missing_file_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            self.assertEqual(main([str(root/"missing.xml"),"--report",str(root/"out.json")]),1)
            self.assertIn("NETLIST_UNAVAILABLE",(root/"out.json").read_text())


if __name__ == "__main__":
    unittest.main()
