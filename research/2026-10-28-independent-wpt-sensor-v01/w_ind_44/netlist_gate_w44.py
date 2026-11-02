"""W44 native KiCad 9 XML checker: exact pin-identity topology, NOT electrical approval."""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import generate_w44 as design

EXPECTED = {label: {f"{ref}.{number}" for ref,number in pins} for label,pins in design.NETS.items()}
NC = {f"{ref}.{num}" for ref,num in design.NC}
PARTS = {ref:value for ref,typ,x,y,value in design.INSTANCES}

def fixture():
    doc = ET.Element("export")
    components = ET.SubElement(doc, "components")
    nets = ET.SubElement(doc, "nets")
    for ref,value in PARTS.items():
        ET.SubElement(ET.SubElement(components,"comp",ref=ref),"value").text=value
    for index,(name,nodes) in enumerate(EXPECTED.items(),1):
        net=ET.SubElement(nets,"net",name="/"+name,code=str(index))
        for key in sorted(nodes):
            ref,num=key.split(".",1)
            ET.SubElement(net,"node",ref=ref,pin=num)
    for index,key in enumerate(sorted(NC),100):
        ref,num=key.split(".",1)
        net=ET.SubElement(nets,"net",name=f"unconnected-{index}",code=str(index))
        ET.SubElement(net,"node",ref=ref,pin=num)
    return ET.tostring(doc,encoding="utf-8")

def evaluate(blob:bytes) -> dict:
    errors=[]
    components={}
    nets={}
    nc=set()
    allpins=set()
    try:
        doc=ET.fromstring(blob)
        if doc.tag!="export":
            raise ValueError("not native KiCad XML export")
        croot,nroot=doc.find("components"),doc.find("nets")
        if croot is None or nroot is None:
            raise ValueError("missing components/nets")
        for component in croot.findall("comp"):
            ref=component.get("ref")
            value=component.findtext("value")
            if not ref or value is None or ref in components:
                raise ValueError("duplicate or invalid component")
            components[ref]=value
        for net in nroot.findall("net"):
            label=net.get("name")
            if not label:
                raise ValueError("unnamed net")
            pins=set()
            for node in net.findall("node"):
                ref,num=node.get("ref"),node.get("pin")
                if not ref or not num:
                    raise ValueError("invalid node")
                key=f"{ref}.{num}"
                if key in allpins:
                    raise ValueError("repeated pin " + key)
                allpins.add(key)
                pins.add(key)
            if label.startswith("unconnected-"):
                if len(pins)!=1:
                    raise ValueError("bad NC net")
                nc.update(pins)
            else:
                name=label.lstrip("/")
                if name in nets:
                    raise ValueError("duplicate label " + name)
                nets[name]=pins
        if components!=PARTS:
            errors.append("component identity mismatch")
        if nets!=EXPECTED:
            errors.append("pin topology mismatch")
            errors.extend("DIFF "+name for name in sorted(set(nets)|set(EXPECTED)) if nets.get(name)!=EXPECTED.get(name))
        if nc!=NC:
            errors.append("no-connect mismatch")
        if allpins!=set().union(*EXPECTED.values(),NC):
            errors.append("total pins mismatch")
    except (ET.ParseError,ValueError) as err:
        errors.append("invalid XML: "+str(err))
    return {
        "schema":"W44_NATIVE_EXACT_PIN_NET_AUDIT_ONLY",
        "passed":not errors,
        "errors":errors,
        "parts":len(components),
        "named_nets":len(nets),
        "verified_electrical_performance":False,
        "qualified_por":False,
        "qualified_pmos":False,
        "cut_en_connected":False,
        "hardware_allowed":False
    }

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("xml",type=Path)
    parser.add_argument("--out",required=True,type=Path)
    args=parser.parse_args()
    try:
        data=args.xml.read_bytes()
        output=evaluate(data)
        output["xml_sha256"]=hashlib.sha256(data).hexdigest()
    except OSError as exc:
        output=evaluate(b"")
        output["errors"].append(str(exc))
        output["passed"]=False
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(output,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(output,sort_keys=True))
    raise SystemExit(0 if output["passed"] else 1)
