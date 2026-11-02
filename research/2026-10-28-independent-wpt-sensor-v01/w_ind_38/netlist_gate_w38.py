"""Exact pin/net audit for native KiCad 9 XML; strict topology only, NOT analog safety."""
from pathlib import Path
import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
import generate_w38 as design

EXPECTED = {net: {f"{ref}.{pin}" for ref, pin in entries}
            for net, entries in design.NETS.items()}
PARTS = {ref: val for ref, _, _, _, val in design.INSTANCES}
NC = {f"{ref}.{pin}" for ref, pin in design.NC}

def evaluate(xml):
    errors, parts, nets, unused, seen = [], {}, {}, set(), set()
    try:
        document = ET.fromstring(xml)
        if document.tag != "export": raise ValueError("not native KiCad export")
        comps, netroot = document.find("components"), document.find("nets")
        if comps is None or netroot is None: raise ValueError("missing component/net table")
        for component in comps.findall("comp"):
            ref, val = component.get("ref"), component.findtext("value")
            if not ref or val is None or ref in parts: raise ValueError("missing/duplicated part")
            parts[ref] = val
        for net in netroot.findall("net"):
            label = net.get("name")
            if not label: raise ValueError("missing label")
            pins = set()
            for node in net.findall("node"):
                ref, pin = node.get("ref"), node.get("pin")
                if not ref or not pin: raise ValueError("invalid pin")
                key = f"{ref}.{pin}"
                if key in seen: raise ValueError("duplicate pin: " + key)
                seen.add(key)
                pins.add(key)
            if label.startswith("unconnected-"):
                if len(pins) != 1: raise ValueError("invalid no-connect")
                unused.update(pins)
            else:
                label = label[1:] if label.startswith("/") else label
                if label in nets: raise ValueError("duplicate named net")
                nets[label] = pins
        if parts != PARTS: errors.append("component variants changed")
        if nets != EXPECTED:
            errors.append("pin topology changed")
            errors += ["changed:" + k for k in sorted(set(nets) & set(EXPECTED))
                       if nets[k] != EXPECTED[k]]
            errors += ["added-or-missing:" + k for k in sorted(set(nets) ^ set(EXPECTED))]
        if unused != NC: errors.append("no-connect pins changed")
        if seen != set().union(*EXPECTED.values(), NC):
            errors.append("missing/extra pins")
    except (ET.ParseError, ValueError) as exc:
        errors.append("XML invalid: " + str(exc))
    return {
        "schema": "W38-NATIVE-NET-REVIEW-ONLY",
        "passed": not errors, "problems": errors,
        "components_count": len(parts), "nets_count": len(nets),
        "physically_measured": False, "power_on_authorized": False,
        "ina301_internal_health_proven": False,
        "W37_release_gate_hardware_built": False,
        "fod_thermal_emi_qualified": False,
        "battery_bms_dock_connected": False
    }

def fixture():
    document = ET.Element("export")
    comps = ET.SubElement(document, "components")
    nets = ET.SubElement(document, "nets")
    for ref, val in PARTS.items():
        ET.SubElement(ET.SubElement(comps, "comp", ref=ref), "value").text = val
    for i, (label, nodes) in enumerate(EXPECTED.items(), 1):
        net = ET.SubElement(nets, "net", name="/" + label, code=str(i))
        for key in sorted(nodes):
            ref, pin = key.split(".", 1)
            ET.SubElement(net, "node", ref=ref, pin=pin)
    for i, key in enumerate(sorted(NC), 1000):
        net = ET.SubElement(nets, "net", name="unconnected-" + str(i), code=str(i))
        ref, pin = key.split(".", 1)
        ET.SubElement(net, "node", ref=ref, pin=pin)
    return ET.tostring(document)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("xml", type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    try:
        data = args.xml.read_bytes()
        result = evaluate(data)
        result["xml_sha256"] = hashlib.sha256(data).hexdigest()
    except OSError as exc:
        result = evaluate(b"")
        result["passed"] = False
        result["problems"].append(str(exc))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(result)
    raise SystemExit(0 if result["passed"] else 1)
