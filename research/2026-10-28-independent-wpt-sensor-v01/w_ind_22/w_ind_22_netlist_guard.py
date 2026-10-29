"""Native KiCad XML netlist topology gate for VALDO W-IND-21.

Copyright 2026 VALDO contributors. Original code; Python standard library only.
This is a REVIEW CHECK, not a WPT power-system safety evaluation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

# Positive allowlist of a single, UNQUALIFIED, 5-V isolated-bench drawing.
# Any architectural edit MUST be reviewed and versioned, not silently accepted.
EXPECTED_NETS = {
    "VIN_5V": {"J1.1", "U1.1"},
    "MID": {"U1.6", "U2.1", "R1.1"},
    "TX_5V_CUT": {"U2.6", "R2.1"},
    "EN_A": {"U1.3", "R3.1"},
    "EN_B": {"U2.3", "R4.1"},
    "GND": {"J1.2", "U1.2", "U2.2", "R1.2", "R2.2", "R3.2", "R4.2"},
}
EXPECTED_REFS = {"J1", "U1", "U2", "R1", "R2", "R3", "R4"}
EXPECTED_VALUES = {
    "J1": "BENCH_SOURCE_DECLARATION_ONLY",
    "U1": "TPS22918DBVR", "U2": "TPS22918DBVR",
    "R1": "22k", "R2": "1k", "R3": "100k", "R4": "100k",
}


def audit_netlist(xml_bytes: bytes) -> dict:
    """Strict audit of native-exported components and electrical connectivity.

    Fail closed on malformed export, extra/absent components, renamed/merged
    nets, any unauthorized node, or duplicate pin memberships. Does not
    reason about transistor parasitics, solder shorts, EMC, or hardware.
    """
    errors: list[str] = []
    parts: dict[str, str] = {}
    nets: dict[str, set[str]] = {}
    duplicate_pin_occurrences: list[str] = []
    try:
        root = ET.fromstring(xml_bytes)
        if root.tag != "export":
            raise ValueError("root is not a KiCad <export>")
        comps = root.find("components")
        net_list = root.find("nets")
        if comps is None or net_list is None:
            raise ValueError("missing components/nets section")
        for comp in comps.findall("comp"):
            ref = comp.get("ref")
            value = comp.findtext("value")
            if not ref or value is None:
                errors.append("component missing reference/value")
                continue
            if ref in parts:
                errors.append(f"duplicate component: {ref}")
            parts[ref] = value
        seen_nodes: dict[str, str] = {}
        for net in net_list.findall("net"):
            name = net.get("name")
            if not name:
                errors.append("unnamed net")
                continue
            if name in nets:
                errors.append(f"duplicate net: {name}")
            pins: set[str] = set()
            for node in net.findall("node"):
                ref, pin = node.get("ref"), node.get("pin")
                if not ref or not pin:
                    errors.append(f"malformed node on net {name}")
                    continue
                item = f"{ref}.{pin}"
                if item in pins or item in seen_nodes:
                    duplicate_pin_occurrences.append(item)
                pins.add(item)
                seen_nodes[item] = name
            nets[name] = pins
        missing_parts = sorted(EXPECTED_REFS - parts.keys())
        extra_parts = sorted(parts.keys() - EXPECTED_REFS)
        if missing_parts:
            errors.append("missing components: " + ", ".join(missing_parts))
        if extra_parts:
            errors.append("unreviewed components: " + ", ".join(extra_parts))
        for ref, value in EXPECTED_VALUES.items():
            if ref in parts and parts[ref] != value:
                errors.append(f"{ref} value changed from locked W-IND-21 contract")
        for name in sorted(EXPECTED_NETS.keys() | nets.keys()):
            if name not in EXPECTED_NETS:
                errors.append(f"unreviewed electrical net: {name}")
            elif name not in nets:
                errors.append(f"missing reviewed net: {name}")
            elif nets[name] != EXPECTED_NETS[name]:
                missing = sorted(EXPECTED_NETS[name] - nets[name])
                extra = sorted(nets[name] - EXPECTED_NETS[name])
                errors.append(f"{name} pins changed: missing={missing}, extra={extra}")
        if duplicate_pin_occurrences:
            errors.append("duplicate pin memberships: " + ", ".join(sorted(set(duplicate_pin_occurrences))))
    except (ET.ParseError, ValueError, TypeError) as exc:
        errors.append(f"unreadable native KiCad XML: {exc}")
    return {
        "status": "NETLIST_EXACT_MATCH_NO_HARDWARE_APPROVAL" if not errors else "REVIEW_BLOCKED_NETLIST_MISMATCH",
        "passed": not errors,
        "errors": errors,
        "components": parts,
        "nets": {name: sorted(pins) for name, pins in sorted(nets.items())},
        "expected_net_count": len(EXPECTED_NETS),
        "data_origin": "KiCad-exported XML or explicitly labeled synthetic test input",
        "physical_approval": False,
        "battery_charging_allowed": False,
        "power_on_allowed": False,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("native_netlist_xml", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        xml_bytes = args.native_netlist_xml.read_bytes()
        result = audit_netlist(xml_bytes)
        result["netlist_sha256"] = hashlib.sha256(xml_bytes).hexdigest()
    except OSError as exc:
        result = {
            "status": "REVIEW_BLOCKED_NETLIST_UNAVAILABLE", "passed": False,
            "errors": [str(exc)], "physical_approval": False,
            "battery_charging_allowed": False, "power_on_allowed": False,
        }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(result["status"], *result["errors"], sep="\n", file=sys.stderr)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
