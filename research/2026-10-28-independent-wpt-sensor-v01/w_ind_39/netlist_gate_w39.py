"""Native KiCad XML pin-identity audit for W39. Topology != functional safety."""
from pathlib import Path
import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
import generate_w39 as design

EXPECTED = {name: {f"{ref}.{pin}" for ref, pin in pins}
            for name, pins in design.NETS.items()}
PARTS = {ref: value for ref, _, _, _, value in design.INSTANCES}
NC = {f"{ref}.{pin}" for ref, pin in design.NC}

def evaluate(xml):
    errors = []
    parts, nets, unused, seen = {}, {}, set(), set()
    try:
        root = ET.fromstring(xml)
        if root.tag != "export":
            raise ValueError("not native KiCad XML")
        comps, wires = root.find("components"), root.find("nets")
        if comps is None or wires is None:
            raise ValueError("missing components or nets")
        for part in comps.findall("comp"):
            ref, value = part.get("ref"), part.findtext("value")
            if not ref or value is None or ref in parts:
                raise ValueError("invalid/duplicate part")
            parts[ref] = value
        for net in wires.findall("net"):
            label = net.get("name")
            if not label:
                raise ValueError("net missing name")
            nodes = set()
            for item in net.findall("node"):
                ref, pin = item.get("ref"), item.get("pin")
                if not ref or not pin:
                    raise ValueError("invalid node")
                identifier = f"{ref}.{pin}"
                if identifier in seen:
                    raise ValueError("pin assigned twice: " + identifier)
                seen.add(identifier)
                nodes.add(identifier)
            if label.startswith("unconnected-"):
                if len(nodes) != 1:
                    raise ValueError("invalid no-connect")
                unused.update(nodes)
            else:
                key = label[1:] if label.startswith("/") else label
                if key in nets:
                    raise ValueError("duplicate net: " + key)
                nets[key] = nodes
        if parts != PARTS:
            errors.append("part references/variants changed")
        if nets != EXPECTED:
            errors.append("pin topology changed")
            errors += ["changed:" + key for key in sorted(set(nets)&set(EXPECTED))
                       if nets[key] != EXPECTED[key]]
            errors += ["missing-or-added:" + key
                       for key in sorted(set(nets)^set(EXPECTED))]
        if unused != NC:
            errors.append("no-connect pins changed")
        target = set().union(*EXPECTED.values(), NC)
        if seen != target:
            errors.append("missing/extra pin")
    except (ET.ParseError, ValueError) as exc:
        errors.append("invalid native netlist: " + str(exc))
    return {
        "schema": "VALDO-W39-KICAD9-TOPOLOGY",
        "passed": not errors, "problems": errors,
        "component_count": len(parts), "net_count": len(nets),
        "single_monitor_silent_failure_theoretical_coverage": True,
        "common_shunt_failure_covered": False,
        "common_3v3_failure_covered": False,
        "w37_physical_rearm_implemented": False,
        "physical_current_trip_tested": False,
        "fod_thermal_emi_qualified": False,
        "safe_to_energize": False,
        "battery_bms_dock_connected": False,
    }

def fixture():
    root = ET.Element("export")
    comps = ET.SubElement(root, "components")
    nets = ET.SubElement(root, "nets")
    for ref, val in PARTS.items():
        ET.SubElement(ET.SubElement(comps, "comp", ref=ref), "value").text = val
    for i, (name, members) in enumerate(EXPECTED.items(), 1):
        node = ET.SubElement(nets, "net", name="/"+name, code=str(i))
        for key in sorted(members):
            ref, pin = key.split(".", 1)
            ET.SubElement(node, "node", ref=ref, pin=pin)
    for i, key in enumerate(sorted(NC), 1000):
        net = ET.SubElement(nets, "net", name="unconnected-"+str(i),
                            code=str(i))
        ref, pin = key.split(".", 1)
        ET.SubElement(net, "node", ref=ref, pin=pin)
    return ET.tostring(root)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xml", type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    try:
        raw = args.xml.read_bytes()
        result = evaluate(raw)
        result["xml_sha256"] = hashlib.sha256(raw).hexdigest()
    except OSError as exc:
        result = evaluate(b"")
        result["problems"].append(str(exc))
        result["passed"] = False
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(result)
    raise SystemExit(0 if result["passed"] else 1)

if __name__ == "__main__":
    main()
