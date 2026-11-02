"""W-IND-70: fail-closed inventory of actual W21 KiCad netlist storage.

Digital audit ONLY. Parsing an exported XML netlist cannot establish the energy
of off-board resonant loads, parasitic capacitance, reverse feed or safety.
Original VALDO W-sector code; no third-party code or CAD incorporated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from w_ind_22.w_ind_22_netlist_guard import audit_netlist


# Named hypothetical screening conditions, NOT hardware ratings.
V_SCREEN = 5.0
C_SCREEN_F = 100e-6
V_STOP_SCREEN = 0.5
ALTERNATE_R_OHM = 10000.0


def _strict_positive_number(label: str, value: object, minimum: float, maximum: float) -> float:
    if type(value) not in (int, float) or not math.isfinite(value) or not minimum <= value <= maximum:
        raise ValueError(f"{label}: finite non-boolean number in [{minimum}, {maximum}] required")
    return float(value)


def _resistance(value: str) -> float:
    """Small explicit unit syntax for W21 labels, never a general SPICE parser."""
    if not isinstance(value, str):
        raise ValueError("resistor value must be string")
    import re
    if not re.fullmatch(r"[1-9][0-9]{0,6}(?:\.[0-9]{1,4})?[kM]?", value):
        raise ValueError("unreviewed resistance notation")
    multiplier = {"k": 1_000.0, "M": 1_000_000.0}.get(value[-1], 1.0)
    base = value[:-1] if multiplier != 1.0 else value
    return float(base) * multiplier


def review_native_xml(
    xml_bytes: bytes,
    *,
    hypothetical_supply_v: float = V_SCREEN,
    hypothetical_cap_f: float = C_SCREEN_F,
    hypothetical_threshold_v: float = V_STOP_SCREEN,
    alternative_bleeder_ohm: float = ALTERNATE_R_OHM,
) -> dict:
    """Inspect actual named KiCad pin nets and *refuse* storage qualification.

    The W22 exact-netlist gate is deliberately mandatory. An added capacitor,
    altered source, short, or a new external load must trigger a new engineering
    review rather than be silently treated as zero capacitance.
    """
    if type(xml_bytes) is not bytes:
        raise TypeError("xml_bytes must be exact bytes")
    v = _strict_positive_number("hypothetical_supply_v", hypothetical_supply_v, 0.01, 5.5)
    c = _strict_positive_number("hypothetical_cap_f", hypothetical_cap_f, 1e-9, 0.1)
    threshold = _strict_positive_number("hypothetical_threshold_v", hypothetical_threshold_v, 1e-6, 5.5)
    alternative = _strict_positive_number("alternative_bleeder_ohm", alternative_bleeder_ohm, 1, 1e7)
    if threshold >= v:
        raise ValueError("hypothetical threshold must be below hypothetical initial voltage")

    topology = audit_netlist(xml_bytes)  # independent W22 strict native-netlist allowlist
    result = {
        "hito": "W-IND-70",
        "status": "BLOCKED_UNREVIEWED_NETLIST",
        "data_origin": "INPUT_XML_DIGITAL_NOT_A_PHYSICAL_MEASUREMENT",
        "xml_sha256": hashlib.sha256(xml_bytes).hexdigest(),
        "topology_exact_w22": bool(topology["passed"]),
        "topology_errors": topology["errors"],
        "physical_tests": 0,
        "hardware_approved": False,
        "power_on_allowed": False,
        "battery_or_dock_allowed": False,
        "local_safety_cuts_proven": False,
        "post_cut_storage_complete": False,
        "backfeed_excluded_by_physical_test": False,
        "residual_discharge_qualified": False,
        "unqualified_reasons": [
            "no measured downstream and off-board capacitance/inductance inventory",
            "no qualified reverse-feed cut, independent safety switches or physical bleed test",
            "FOD, metal, offset, wetness, thermal, EMI and lithium charging unverified",
        ],
    }
    if not topology["passed"]:
        return result

    # Use actual pin membership, not layout or a verbal assumption that all
    # resistors bleed the transmitter. W22 rejects extra nets, pins, parts.
    memberships = {pin: name for name, nodes in topology["nets"].items() for pin in nodes}
    expected = {
        "R1": frozenset(("/MID", "/GND")),
        "R2": frozenset(("/TX_5V_CUT", "/GND")),
        "R3": frozenset(("/EN_A", "/GND")),
        "R4": frozenset(("/EN_B", "/GND")),
    }
    branches = {}
    for ref, required in expected.items():
        actual = frozenset((memberships.get(ref + ".1"), memberships.get(ref + ".2")))
        if actual != required:
            result["topology_errors"] = [f"unexpected endpoints for {ref}: {sorted(str(x) for x in actual)}"]
            return result
        branches[ref] = {"terminals": sorted(actual),
                         "nominal_ohms": _resistance(topology["components"][ref])}

    # W21 has no capacitor OR inductor in its design, not a proof that the
    # external TX has zero storage. J1 is a source *declaration*, not hardware.
    explicitly_listed_storage = [ref for ref in topology["components"] if ref.startswith(("C", "L"))]
    r_tx = branches["R2"]["nominal_ohms"]
    r_mid = branches["R1"]["nominal_ohms"]
    nominal_tx_w = v * v / r_tx
    nominal_mid_w = v * v / r_mid
    def hypothetical_time(r: float) -> float:
        return r * c * math.log(v / threshold)

    result.update({
        "status": "BLOCKED_EXTERNAL_TX_STORAGE_UNCHARACTERIZED",
        "schematic": "W_IND_21_TX_BENCH_DECLARED.kicad_sch",
        "source_is_declaration_only": True,
        "nominal_resistive_branches": branches,
        "post_second_cut_bleeder": "R2: /TX_5V_CUT -> /GND",
        "between_cuts_bleeder": "R1: /MID -> /GND; NOT a direct discharge resistor for TX_5V_CUT",
        "enable_pull_downs": ["R3", "R4"],
        "schematic_capacitors_and_inductors": explicitly_listed_storage,
        "explicit_storage_items": len(explicitly_listed_storage),
        "off_board_tx_load_and_parasitics": "UNKNOWN_NOT_ZERO",
        "nominal_screen_only": {
            "assumed_v": v,
            "assumed_capacitance_f": c,
            "assumed_voltage_threshold_v": threshold,
            "tx_r2_power_if_continuously_at_assumed_v_w": nominal_tx_w,
            "mid_r1_power_if_continuously_at_assumed_v_w": nominal_mid_w,
            "tx_r2_energy_24h_if_continuously_at_assumed_v_wh": nominal_tx_w * 24,
            "tx_r2_hypothetical_time_to_threshold_s": hypothetical_time(r_tx),
            "alternative_r_ohm_not_installed": alternative,
            "alternative_loss_if_continuously_at_assumed_v_w": v * v / alternative,
            "alternative_hypothetical_time_to_threshold_s": hypothetical_time(alternative),
        },
    })
    return result


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("native_xml", type=Path)
    ap.add_argument("--report", type=Path, required=True)
    args = ap.parse_args(argv)
    try:
        data = args.native_xml.read_bytes()
        result = review_native_xml(data)
        result["source_netlist_path"] = str(args.native_xml)
    except (OSError, ValueError, TypeError) as exc:
        result = {"status": "BLOCKED_INVALID_INPUT", "error": str(exc),
                  "hardware_approved": False, "power_on_allowed": False,
                  "residual_discharge_qualified": False}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(result["status"])
    # Recognized and correctly BLOCKED W21 is a PASS for this *review gate*,
    # not permission to energize. A mutated/unknown netlist returns an error.
    return 0 if result["status"] == "BLOCKED_EXTERNAL_TX_STORAGE_UNCHARACTERIZED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
