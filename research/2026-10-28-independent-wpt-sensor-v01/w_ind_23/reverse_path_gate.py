"""W-IND-23: native-netlist-linked TPS22918 reverse-body-diode review.

Copyright 2026 VALDO contributors. Original Python standard-library code.
This identifies a CONDITIONALLY conductive device-internal path. It neither
predicts current nor qualifies any powered circuit or battery charger.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import deque
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

# Locked W-IND-21 native KiCad 9.0.2 topology; independent of ERC and W-IND-22.
# A circuit revision must explicitly requalify this review, never auto-allow it.
NETS = {
    "/VIN_5V": {"J1.1", "U1.1"},
    "/MID": {"U1.6", "U2.1", "R1.1"},
    "/TX_5V_CUT": {"U2.6", "R2.1"},
    "/EN_A": {"U1.3", "R3.1"},
    "/EN_B": {"U2.3", "R4.1"},
    "/GND": {"J1.2", "U1.2", "U2.2", "R1.2", "R2.2", "R3.2", "R4.2"},
    "unconnected-(U1-CT-Pad4)": {"U1.4"},
    "unconnected-(U1-QOD-Pad5)": {"U1.5"},
    "unconnected-(U2-CT-Pad4)": {"U2.4"},
    "unconnected-(U2-QOD-Pad5)": {"U2.5"},
}
PARTS = {
    "J1": "BENCH_SOURCE_DECLARATION_ONLY",
    "U1": "TPS22918DBVR", "U2": "TPS22918DBVR",
    "R1": "22k", "R2": "1k", "R3": "100k", "R4": "100k",
}
# TI TPS22918 Rev C, section 9.2.2.2: body diode can conduct VOUT -> VIN.
# VIN=pad1 and VOUT=pad6 for the locked DBV part. Not reverse-blocking!
DIODE_PINS = (("U1", "6", "1"), ("U2", "6", "1"))
DATASHEET = "https://www.ti.com/product/TPS22918"


def path(edges: list[tuple[str, str, str]], start: str, stop: str) -> list[str]:
    """Find a directed component-internal path (NO voltage/current model)."""
    queue = deque([(start, [])])
    seen = {start}
    while queue:
        current, route = queue.popleft()
        if current == stop:
            return route
        for source, target, label in edges:
            if source == current and target not in seen:
                seen.add(target)
                queue.append((target, route + [label]))
    return []


def audit_native(xml_bytes: bytes) -> dict:
    """Require the exact KiCad netlist and model *only* internal body diodes.

    A detected reverse path means potential backfeed *if* TX voltage is high
    enough relative to VIN. An absent path in this toy graph never means safe.
    """
    errors = []
    pin_net: dict[str, str] = {}
    try:
        root = ET.fromstring(xml_bytes)
        if root.tag != "export":
            raise ValueError("not a KiCad XML export")
        parts = root.find("components")
        nets = root.find("nets")
        if parts is None or nets is None:
            raise ValueError("missing components or nets")
        observed_parts = {}
        for component in parts.findall("comp"):
            ref, val = component.get("ref"), component.findtext("value")
            if not ref or val is None or ref in observed_parts:
                errors.append("invalid/duplicate component")
            else:
                observed_parts[ref] = val
        if observed_parts != PARTS:
            errors.append("parts/values differ from unqualified W-IND-21 baseline")
        observed_nets = {}
        for net in nets.findall("net"):
            name = net.get("name")
            if not name or name in observed_nets:
                errors.append("invalid/duplicate net")
                continue
            members = set()
            for node in net.findall("node"):
                ref, pin = node.get("ref"), node.get("pin")
                if not ref or not pin:
                    errors.append("invalid node")
                    continue
                item = ref + "." + pin
                if item in pin_net or item in members:
                    errors.append("duplicate pin membership: " + item)
                pin_net[item] = name
                members.add(item)
            observed_nets[name] = members
        if observed_nets != NETS:
            errors.append("native pin-to-net topology differs from locked baseline")
    except (ET.ParseError, ValueError, TypeError) as exc:
        errors.append("invalid netlist: " + str(exc))

    route = []
    if not errors:
        diodes = [(pin_net[f"{ref}.{out_pin}"], pin_net[f"{ref}.{in_pin}"],
                   ref + ":VOUT6->VIN1_body_diode")
                  for ref, out_pin, in_pin in DIODE_PINS]
        route = path(diodes, "/TX_5V_CUT", "/VIN_5V")
        if route != ["U2:VOUT6->VIN1_body_diode", "U1:VOUT6->VIN1_body_diode"]:
            errors.append("reviewer expected reverse path not reproduced")
        if path(diodes, "/VIN_5V", "/TX_5V_CUT"):
            errors.append("internal diode orientation contradiction")

    return {
        "status": ("REVIEW_BLOCKED_UNKNOWN_TOPOLOGY" if errors
                   else "REVIEW_BLOCKED_TPS22918_REVERSE_DIODE_PATH"),
        "known_hazard_detected": bool(route) and not errors,
        "reverse_path": route if not errors else [],
        "condition": "TX-side stored/external energy raises VOUT over VIN enough to forward-bias both body diodes",
        "evidence": "TI TPS22918 datasheet Rev C section 9.2.2.2; graph evaluated on locked native KiCad XML",
        "datasheet": DATASHEET,
        "errors": errors,
        "hardware_approved": False,
        "power_on_allowed": False,
        "battery_charging_allowed": False,
        "current_or_temperature_predicted": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xml", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--expect-known-blocker", action="store_true",
                        help="CI passes only if the KNOWN REVERSE-PATH BLOCKER is detected; NOT safety approval")
    args = parser.parse_args(argv)
    try:
        raw = args.xml.read_bytes()
        result = audit_native(raw)
        result["netlist_sha256"] = hashlib.sha256(raw).hexdigest()
    except OSError as exc:
        result = {"status": "REVIEW_BLOCKED_NO_NETLIST", "errors": [str(exc)],
                  "known_hazard_detected": False, "hardware_approved": False,
                  "power_on_allowed": False, "battery_charging_allowed": False}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(result["status"], file=sys.stderr)
    if args.expect_known_blocker:
        return 0 if result["known_hazard_detected"] else 1
    return 2 if result["known_hazard_detected"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
