"""W-IND-46 local open-drain diagnostic model. Original, synthetic, unpowered."""
from __future__ import annotations
from pathlib import Path
import json
import argparse

MIN_VDD = 1.8  # TPS3700 specified operating minimum; NOT dynamic POR certification
R_OHM = 10000.0  # candidate local 3V3 pullup; input VIH/VIL unknown

def sink_current_ma(local_v: float, tolerance: float = 0.0) -> float:
    """Ideal LOW resistor current, not a measurement of output VOL/IOH."""
    if not 0 < local_v <= 6 or not 0 <= tolerance < 1:
        raise ValueError("invalid hypothetical supply/tolerance")
    return 1000.0 * local_v / (R_OHM * (1 - tolerance))

def sink_resistor_mw(local_v: float, tolerance: float = 0.0) -> float:
    return sink_current_ma(local_v, tolerance) * local_v

def line_state(*, vdd: float, pullup: float, threshold_good: bool,
               wire_open: bool = False, stuck_low: bool = False,
               short_high: bool = False) -> str:
    """Expected ideal electrical level only. Never a hardware-safe permission."""
    if not 0 <= vdd <= 6 or not 0 <= pullup <= 6 or type(threshold_good) is not bool:
        raise ValueError("invalid simulated input")
    if pullup < MIN_VDD:
        return "UNKNOWN_RECEIVER_SUPPLY"
    if wire_open or short_high:
        return "HIGH_IF_RECEIVER_VIH_SUPPORTS_IT"
    if stuck_low:
        return "LOW_FALSE_HEALTH_POSSIBLE"
    if vdd < MIN_VDD:
        return "UNKNOWN_SUPERVISOR_POR"
    return "LOW_SINK_IDEAL" if threshold_good else "HIGH_IF_RECEIVER_VIH_SUPPORTS_IT"

# Pin-level contract, not a connected electrical schematic or KiCad ERC claim.
# OUTB is open drain: P-MOS and 5-V-driven HEALTH output are eliminated.
PARTS = {
    "J1": "5V_supervisor_declared", "J2": "3V3_local_declared",
    "J3": "HEALTH_N_local_diagnostic_only", "U1": "TPS3700DDCR",
    "R1": "63k4_1pct_tentative", "R2": "10k_1pct_tentative",
    "R5": "10k_1pct_local_pullup_tentative", "C1": "100nF_tentative",
}
NETS = {
    "5V_SUPERVISOR_ONLY": ["J1.1", "U1.5", "C1.1"],
    "GND_LOCAL": ["J1.2", "J2.2", "J3.2", "U1.2", "R2.2", "C1.2"],
    "3V3_LOCAL": ["J2.1", "R1.1", "R5.1"],
    "INB_MONITOR": ["R1.2", "R2.1", "U1.4"],
    "HEALTH_N_LOCAL_DIAGNOSTIC": ["U1.6", "R5.2", "J3.1"],
}
NO_CONNECT = ["U1.1", "U1.3"]

def audit_contract() -> dict:
    all_pins = [pin for pins in NETS.values() for pin in pins] + NO_CONNECT
    errors = []
    if len(PARTS) != 8 or len(NETS) != 5:
        errors.append("incorrect parts or net count")
    if len(all_pins) != 20 or len(set(all_pins)) != len(all_pins):
        errors.append("pin count or duplicate")
    for pin in all_pins:
        if pin.split(".")[0] not in PARTS:
            errors.append("undefined component")
    if set(NETS["HEALTH_N_LOCAL_DIAGNOSTIC"]) != {"U1.6", "R5.2", "J3.1"}:
        errors.append("unqualified health topology")
    if not {"R5.1", "J2.1"}.issubset(NETS["3V3_LOCAL"]):
        errors.append("pullup does not belong to local 3V3")
    if "R5.1" in NETS["5V_SUPERVISOR_ONLY"]:
        errors.append("5V to receiver input")
    if any("EN" in name or "MOTOR" in name or "BATTERY" in name for name in NETS):
        errors.append("critical power enable leaked into diagnostic")
    return {"structural_pass": not errors, "errors": errors, "parts":len(PARTS),
            "nets":len(NETS),"pins":len(all_pins),"native_kicad_erc":False,
            "hardware_approved":False}

def evidence() -> dict:
    cases = [
        ("healthy", dict(vdd=5,pullup=3.3,threshold_good=True)),
        ("observed_rail_bad",dict(vdd=5,pullup=3.3,threshold_good=False)),
        ("broken_wire",dict(vdd=5,pullup=3.3,threshold_good=True,wire_open=True)),
        ("supervisor_off",dict(vdd=0,pullup=3.3,threshold_good=False)),
        ("local_rail_off",dict(vdd=5,pullup=0,threshold_good=False)),
        ("output_stuck_low",dict(vdd=5,pullup=3.3,threshold_good=False,stuck_low=True)),
        ("short_to_high",dict(vdd=5,pullup=3.3,threshold_good=True,short_high=True)),
        ("brownout",dict(vdd=5,pullup=1.6,threshold_good=False)),
    ]
    return {
        "schema":"W46_SYNTHETIC_LOCAL_OD_NOT_HARDWARE",
        "source":"https://www.ti.com/product/TPS3700",
        "contract":audit_contract(),
        "old_concept_parts":10,"new_concept_parts":8,
        "parts_saved_in_unbuilt_concept":2,
        "nominal_3v3_10k_sink_ma_ideal":sink_current_ma(3.3),
        "nominal_3v3_10k_resistor_mw_ideal":sink_resistor_mw(3.3),
        "cases":[{"name":name,"level":line_state(**kw)} for name,kw in cases],
        "limits":["receiver VIH/VIL and input clamps unknown","supervisor POR unknown",
                  "OUTB VOL/leakage/temperature and stuck-low unresolved",
                  "local rail lost means no valid HIGH; local independent UVLO mandatory",
                  "no radio, no actual wireless power, no independent cutoff",
                  "FOD, offset, EMI, thermal, wetness and dock/lithium untested"],
        "no_battery":True,"no_hardware_tests":True,
        "connected_to_safety_en":False,"hardware_approved":False,
    }

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path)
    a=p.parse_args()
    data=evidence()
    if a.out:
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"structural_pass":data["contract"]["structural_pass"],
                      "synthetic_cases":len(data["cases"]),
                      "hardware_approved":False},sort_keys=True))
    raise SystemExit(0 if data["contract"]["structural_pass"] else 1)
