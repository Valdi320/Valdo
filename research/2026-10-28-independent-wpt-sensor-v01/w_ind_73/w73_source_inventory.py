#!/usr/bin/env python3
"""Read-only, source-pinned TX capacitor inventory. No upstream code is bundled."""
import argparse
import csv
import hashlib
import io
import json
import re
import urllib.request
from pathlib import Path

OWNER = "mark-belbin"
REPO = "simple-wireless-power"
REF = "7c7858c0dd7040801b6f191df1396115560218f0"
ROOT = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{REF}/hardware/WPT_TX/"
NET_NAME = "WPT_TX.net"
BOM_NAME = "WPT_TX_bom_001.csv"
# Immutable Git blob IDs, independently checked via the author's GitHub content API.
NET_BLOB = "d4ef7e2c2c9588abcc2f28c6a775715108f2e523"
BOM_BLOB = "04f274dfa46810d655ae2d9783cb96ad1f17bc27"
COMPONENT = re.compile(r"\(comp \(ref ([A-Za-z]+\d+)\)\s+\(value ([^)]+)\)")
NET_HEADER = re.compile(r'^    \(net \(code \d+\) \(name (?:"([^"]+)"|([^)]*))\)', re.M)
NODE = re.compile(r'\(node \(ref ([A-Za-z]+\d+)\) \(pin ([^)]*)\)\)')
CAP_VALUE = re.compile(r'^(\d+(?:\.\d+)?)(p|n|u|m)$')
EXPECTED_BULK = ("C35", "C36", "C37", "C38")
EXPECTED_RF = ("C26", "C27", "C28", "C29")


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def validate_source(data: bytes, expected: str) -> None:
    if git_blob_sha(data) != expected:
        raise ValueError("upstream source blob SHA mismatch: FAIL CLOSED")


def parse_netlist(net_text: str):
    if "  (nets\n" not in net_text:
        raise ValueError("KiCad legacy nets section missing")
    section = net_text.split("  (nets\n", 1)[1]
    components = {}
    for ref, value in COMPONENT.findall(net_text.split("  (nets\n", 1)[0]):
        if ref in components:
            raise ValueError("duplicate component " + ref)
        components[ref] = value
    caps = {r: v for r, v in components.items() if r.startswith("C")}
    if not caps:
        raise ValueError("no capacitor records")
    matches = list(NET_HEADER.finditer(section))
    if not matches:
        raise ValueError("no net headers")
    pins = {ref: {} for ref in caps}
    for index, match in enumerate(matches):
        name = match.group(1) or match.group(2)
        body = section[match.end(): matches[index+1].start() if index+1 < len(matches) else len(section)]
        for ref, pin in NODE.findall(body):
            if ref in pins:
                if pin in pins[ref]:
                    raise ValueError("duplicate capacitor pin mapping")
                pins[ref][pin] = name
    for ref in caps:
        if sorted(pins[ref]) != ["1", "2"]:
            raise ValueError(f"incomplete or ambiguous pin mapping: {ref}")
    return {ref: {"value": caps[ref], "pins": pins[ref]} for ref in sorted(caps, key=lambda x: int(x[1:]))}


def bom_cap_refs(bom_text: str):
    listed = set()
    reader = csv.DictReader(io.StringIO(bom_text))
    if not reader.fieldnames or "References" not in reader.fieldnames:
        raise ValueError("BOM References column missing")
    for row in reader:
        for ref in (row.get("References") or "").split():
            if re.fullmatch(r"C\d+", ref):
                if ref in listed:
                    raise ValueError("duplicate BOM capacitor reference")
                listed.add(ref)
    if not listed:
        raise ValueError("BOM capacitor references missing")
    return listed


def farads(value: str) -> float:
    m = CAP_VALUE.fullmatch(value)
    if not m:
        raise ValueError("unknown capacitor value unit: " + value)
    return float(m[1]) * {"p": 1e-12, "n": 1e-9, "u": 1e-6, "m": 1e-3}[m[2]]


def is_between(comp, rail_a: str, rail_b: str) -> bool:
    return set(comp["pins"].values()) == {rail_a, rail_b}


def audit(net_bytes: bytes, bom_bytes: bytes) -> dict:
    validate_source(net_bytes, NET_BLOB)
    validate_source(bom_bytes, BOM_BLOB)
    net = parse_netlist(net_bytes.decode("utf-8-sig"))
    bom = bom_cap_refs(bom_bytes.decode("utf-8-sig"))
    missing = sorted(set(net) - bom, key=lambda x: int(x[1:]))
    extra = sorted(bom - set(net), key=lambda x: int(x[1:]))
    bulk_ok = all(ref in net and net[ref]["value"] == "330u" and is_between(net[ref], "/HD", "GND") for ref in EXPECTED_BULK)
    rf_ok = all(ref in net and net[ref]["value"] == "100n" and is_between(net[ref], "/HS_1", "Net-(C26-Pad1)") for ref in EXPECTED_RF)
    if not bulk_ok or not rf_ok or set(missing) != set(EXPECTED_BULK) or extra or len(net) != 37 or len(bom) != 33:
        raise ValueError("source topology differs from reviewed provenance: FAIL CLOSED")
    c_hd = sum(farads(net[ref]["value"]) for ref in EXPECTED_BULK)
    c_rf = sum(farads(net[ref]["value"]) for ref in EXPECTED_RF)
    return {
        "provenance": "AUTHOR_NETLIST_AND_2020_BOM_NOT_OWN_HARDWARE",
        "author": f"{OWNER}/{REPO}",
        "license": "GPL-3.0 (external only; no CAD/code redistributed)",
        "source_commit": REF,
        "netlist_git_blob_sha1": NET_BLOB,
        "bom_git_blob_sha1": BOM_BLOB,
        "netlist_capacitors": len(net),
        "legacy_bom_capacitors": len(bom),
        "missing_from_legacy_bom": missing,
        "unlisted_bus_capacitors": [{"ref": ref, "value": net[ref]["value"], "nets": ["/HD", "GND"]} for ref in EXPECTED_BULK],
        "bus_capacitance_nominal_uF": round(c_hd * 1e6, 6),
        "rf_series_bank": {"refs": list(EXPECTED_RF), "nominal_parallel_nF": round(c_rf * 1e9, 6), "net": "/HS_1 <-> Net-(C26-Pad1)", "not_dc_bleed_capacitance": True},
        "conditional_energy_at_HD": [
            {"voltage_V_assumed": voltage, "joule_nominal_if_all_at_that_voltage": round(0.5 * c_hd * voltage**2, 6)}
            for voltage in (5.5, 12.0, 24.0)
        ],
        "topology_status": "SOURCE_VERIFIED_NOT_HARDWARE_APPROVED",
        "blockers": [
            "Historical 2020 BOM omits four 330uF caps listed in 2021 netlist",
            "No verified populated PCB/voltage across /HD/tolerance/leakage/discharge network",
            "The 24V author design cannot be equated to our 5V W21 circuit",
            "RF series compensation bank is not the DC-bus discharge capacitor",
            "FOD, temperatures, coil offset, EMI, independent cutoff and physical discharge unqualified",
        ],
        "hardware_approved": False,
        "battery_connected": False,
        "measurement_performed": False,
    }


def fetch(name):
    url = ROOT + name
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Valdo-W73-source-audit"}), timeout=30) as response:
        return response.read()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--netlist", type=Path)
    p.add_argument("--bom", type=Path)
    p.add_argument("--fetch-pinned", action="store_true", help="read from immutable author URLs; no local clone modification")
    p.add_argument("--out", type=Path)
    args = p.parse_args()
    if args.fetch_pinned and (args.netlist or args.bom):
        p.error("select remote pinned or BOTH local source inputs")
    if args.fetch_pinned:
        net, bom = fetch(NET_NAME), fetch(BOM_NAME)
    elif args.netlist and args.bom:
        net, bom = args.netlist.read_bytes(), args.bom.read_bytes()
    else:
        p.error("--fetch-pinned or both --netlist and --bom required")
    result = audit(net, bom)
    data = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.out:
        args.out.write_text(data, encoding="utf-8")
    else:
        print(data, end="")


if __name__ == "__main__":
    main()
