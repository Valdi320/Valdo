"""W-IND-16: geometry-based KiCad net-label audit (NOT ERC or safety proof).
Current draft uses pin-attached labels with NO wires; unknown topology fails shut.
"""
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path
import json
import re

TOKEN = re.compile(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+')
ALLOWED_COMPONENTS = {"U1": "VALDO:TPS22918_DBV", "U2": "VALDO:TPS22918_DBV",
                      **{f"R{i}": "VALDO:R" for i in range(1, 5)}}
EXPECTED_PIN_TYPES = {"1": "power_in", "2": "power_in", "3": "input",
                      "4": "passive", "5": "passive", "6": "power_out"}
FORBIDDEN_TOPOLOGY = {"wire", "junction", "bus", "bus_entry", "global_label",
                      "hierarchical_label", "sheet", "image", "polyline"}

def parse(text):
    """Simple rigorous S-expression reader for this one reviewed schematic."""
    roots, stack, end = [], [], 0
    for match in TOKEN.finditer(text):
        if text[end:match.start()].strip():
            raise ValueError("invalid token")
        word = match.group()
        if word == "(":
            group = []
            (stack[-1] if stack else roots).append(group)
            stack.append(group)
        elif word == ")":
            if not stack:
                raise ValueError("unexpected )")
            stack.pop()
        else:
            if not stack:
                raise ValueError("bare atom")
            try:
                stack[-1].append(json.loads(word) if word.startswith('"') else word)
            except json.JSONDecodeError as exc:
                raise ValueError("invalid string") from exc
        end = match.end()
    if text[end:].strip() or stack or len(roots) != 1 or roots[0][0] != "kicad_sch":
        raise ValueError("invalid/incomplete schematic")
    return roots[0]

def children(node, key):
    return [v for v in node if isinstance(v, list) and v and v[0] == key]

def one(node, key):
    v = children(node, key)
    if len(v) != 1:
        raise ValueError(f"expected exactly one {key}; found {len(v)}")
    return v[0]

def loc(node):
    v = one(node, "at")
    try:
        return Decimal(str(v[1])), Decimal(str(v[2])), Decimal(str(v[3] if len(v)>3 else 0))
    except (InvalidOperation, IndexError) as exc:
        raise ValueError("invalid coordinates") from exc

def spot(x, y):
    return Decimal(str(x)), Decimal(str(y))

def prop(node, key):
    v = [x for x in children(node, "property") if len(x)>2 and x[1]==key]
    if len(v)!=1:
        raise ValueError(f"property {key} missing or duplicate")
    return v[0][2]

def audit(schematic, contract):
    errors = []
    try:
        root = parse(schematic)
        if any(children(root, kind) for kind in FORBIDDEN_TOPOLOGY):
            errors.append("unreviewed wire, bus, hierarchical or graphic topology")
        defs = one(root, "lib_symbols")
        libraries = {s[1]:s for s in children(defs, "symbol")}
        if set(libraries)!=set(ALLOWED_COMPONENTS.values()):
            errors.append("unreviewed symbol library")
        placed={}
        for s in children(root,"symbol"):
            ref=prop(s,"Reference")
            if ref in placed:
                errors.append("duplicate component reference")
            placed[ref]=s
        if set(placed)!=set(ALLOWED_COMPONENTS):
            errors.append("unreviewed or missing component")
        actual={}
        for ref,sym in placed.items():
            libid=one(sym,"lib_id")[1]
            if libid!=ALLOWED_COMPONENTS.get(ref) or libid not in libraries:
                errors.append(f"{ref}: unknown symbol")
                continue
            ox,oy,angle=loc(sym)
            if angle!=0:
                errors.append(f"{ref}: unreviewed rotation")
                continue
            pins=[]
            for unit in children(libraries[libid],"symbol"):
                pins.extend(children(unit,"pin"))
            declared={pin[1] for pin in children(sym,"pin")}
            seen=set()
            for pin in pins:
                number=one(pin,"number")[1]
                if number in seen:
                    errors.append(f"{libid}: repeated physical pin number")
                seen.add(number)
                dx,dy,_=loc(pin)
                if ref.startswith("U") and pin[1]!=EXPECTED_PIN_TYPES.get(number):
                    errors.append(f"{ref}.{number}: pin type altered")
                if ref.startswith("U") and contract["pinmap"].get(number)!=one(pin,"name")[1]:
                    errors.append(f"{ref}.{number}: pin name differs from TI contract")
                actual[f"{ref}.{number}"]=(ox+dx,oy-dy)
            if seen!=declared:
                errors.append(f"{ref}: pin declaration mismatch")
            if ref.startswith("U"):
                if prop(sym,"Value")!="TPS22918DBVR":
                    errors.append(f"{ref}: component value changed")
                if prop(libraries[libid],"Footprint")!="Package_TO_SOT_SMD:SOT-23-6":
                    errors.append(f"{ref}: footprint changed")
            if ref.startswith("R") and prop(sym,"Value")!=contract["resistors"][ref]["value"]:
                errors.append(f"{ref}: resistor altered")
        expected={}
        for ref,pins in contract["switch_pin_endpoints_mm"].items():
            for number,(net,x,y) in pins.items():
                expected[f"{ref}.{number}"]=(net,spot(x,y))
        for ref,res in contract["resistors"].items():
            for number,(net,x,y) in res["pins"].items():
                expected[f"{ref}.{number}"]=(net,spot(x,y))
        if set(actual)!=set(expected) or any(actual.get(k)!=v[1] for k,v in expected.items()):
            errors.append("actual pins differ from JSON coordinates")
        labels=[(v[1],loc(v)[:2]) for v in children(root,"label")]
        ncs=[loc(v)[:2] for v in children(root,"no_connect")]
        label_expected=Counter((net,pos) for net,pos in expected.values() if net!="NC")
        nc_expected=Counter(pos for net,pos in expected.values() if net=="NC")
        if Counter(labels)!=label_expected:
            errors.append("missing/loose/misnamed labels")
        if Counter(ncs)!=nc_expected:
            errors.append("missing/incorrect no-connect markers")
        nets={}
        for pin,(net,_) in expected.items():
            if net!="NC":
                nets.setdefault(net,[]).append(pin)
        if {k:set(v) for k,v in nets.items()}!={k:set(v) for k,v in contract["expected_nets"].items()}:
            errors.append("pin-to-net map differs")
        uuids=[]
        def visit(n):
            if isinstance(n,list):
                if n and n[0]=="uuid":
                    uuids.append(n[1])
                for item in n:
                    visit(item)
        visit(root)
        if len(uuids)!=len(set(uuids)):
            errors.append("duplicated UUID")
        if any(contract.get(k) for k in ("hardware_approved","KiCad_ERC_run","SPICE_run")):
            errors.append("unsupported physical safety / KiCad ERC / SPICE claim")
    except (ValueError,KeyError,TypeError,IndexError,AttributeError) as exc:
        errors.append(f"invalid schematic or contract: {exc}")
    return errors

def main():
    folder=Path(__file__).resolve().parent
    src=(folder/"W_IND_15_TX_DUAL_CUT_UNQUALIFIED.kicad_sch").read_text()
    spec=json.loads((folder/"W_IND_15_PIN_CONTRACT.json").read_text())
    errors=audit(src,spec)
    print(json.dumps({"milestone":"W-IND-16","static_geometry_pass":not errors,"errors":errors,
                      "kicad_erc_run":False,"hardware_approved":False},indent=2))
    return bool(errors)

if __name__=="__main__":
    raise SystemExit(main())
