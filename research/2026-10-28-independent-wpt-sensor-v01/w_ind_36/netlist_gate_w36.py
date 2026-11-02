"""W-IND-36 exact native KiCad XML netlist audit. Tests connectivity, NOT safety."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import generate_w36 as d

EXPECTED = {name:{f"{ref}.{pin}" for ref,pin in nodes} for name,nodes in d.NETS.items()}
PARTS = {ref:val for ref,_,_,_,val in d.INSTANCES}
NC = {f"{r}.{n}" for r,n in d.NC}

def evaluate(xml_bytes):
    problems = []
    components, nets, nc, all_seen = {}, {}, set(), set()
    try:
        root = ET.fromstring(xml_bytes)
        if root.tag != "export": raise ValueError("not KiCad XML export")
        comp_root, net_root = root.find("components"), root.find("nets")
        if comp_root is None or net_root is None: raise ValueError("missing components or nets")
        for item in comp_root.findall("comp"):
            ref, val = item.get("ref"), item.findtext("value")
            if not ref or ref in components or val is None: raise ValueError("duplicated/incomplete component")
            components[ref] = val
        for item in net_root.findall("net"):
            name = item.get("name")
            if not name: raise ValueError("unnamed net")
            nodes = set()
            for node in item.findall("node"):
                pin = f"{node.get('ref')}.{node.get('pin')}"
                if "None" in pin or pin in all_seen: raise ValueError("missing/reused pin")
                all_seen.add(pin)
                nodes.add(pin)
            if name.startswith("unconnected-"):
                if len(nodes) != 1: raise ValueError("malformed NC net")
                nc.update(nodes)
            else:
                label = name[1:] if name.startswith("/") else name
                if label in nets: raise ValueError("duplicate named net")
                nets[label] = nodes
        if components != PARTS: problems.append("component variants/values changed")
        if nets != EXPECTED:
            problems.append("native net topology differs from reviewed permit/PG graph")
            problems.extend("net:"+n for n in sorted(set(nets)^set(EXPECTED)))
            problems.extend("changed:"+n for n in sorted(set(nets)&set(EXPECTED)) if nets[n]!=EXPECTED[n])
        if nc != NC: problems.append("NC pins differ")
        known = set().union(*EXPECTED.values()) | NC
        if all_seen != known: problems.append("missing or extra pins")
    except (ET.ParseError, ValueError) as exc:
        problems.append("XML invalid: " + str(exc))
    return {
        "schema": "VALDO-W36-KICAD-EXACT-NETS-V1",
        "passed": not problems, "problems": problems,
        "component_count": len(components),
        "net_count": len(nets),
        "hardware_tested": False,
        "supervisors_physically_qualified": False,
        "overcurrent_autonomous_trip_built": False,
        "fod_thermal_emi_qualified": False,
        "battery_or_dock_connected": False,
        "power_authorized": False,
    }

def fixture_xml():
    # Synthetic XML useful to unit-test this auditor; NOT a native KiCad result.
    root = ET.Element("export")
    parts = ET.SubElement(root, "components")
    nets = ET.SubElement(root, "nets")
    for ref,val in PARTS.items():
        comp = ET.SubElement(parts, "comp", ref=ref)
        ET.SubElement(comp,"value").text = val
    for idx,(name,pins) in enumerate(EXPECTED.items()):
        net = ET.SubElement(nets,"net",name="/"+name,code=str(idx+1))
        for node in sorted(pins):
            ref,pin = node.split(".",1)
            ET.SubElement(net,"node",ref=ref,pin=pin)
    for idx,node in enumerate(sorted(NC)):
        net = ET.SubElement(nets,"net",name="unconnected-"+str(idx),code=str(1000+idx))
        ref,pin = node.split(".",1)
        ET.SubElement(net,"node",ref=ref,pin=pin)
    return ET.tostring(root)

def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument("xml",type=Path)
    ap.add_argument("--out",required=True,type=Path)
    args=ap.parse_args(argv)
    try:
        data=args.xml.read_bytes()
        report=evaluate(data)
        report["native_xml_sha256"]=hashlib.sha256(data).hexdigest()
    except OSError as exc:
        report=evaluate(b"")
        report["passed"]=False
        report["problems"].append("read failure: "+str(exc))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print("PASS netlist topology only" if report["passed"] else "BLOCKED",report["problems"])
    return 0 if report["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
