"""W45 original BSS84 HEALTH leakage stress, software-only (NOT hardware safety)."""
from __future__ import annotations
import argparse
import csv
import io
import json
from pathlib import Path

# Hypotheses, not any receiver's verified input thresholds.
OFF_CEILING_V = 0.4
RESISTORS_OHM = (2200, 4700, 10000, 47000)
SUPPLIES_V = (4.5, 5.0, 5.5)
# IDSS figures from onsemi BSS84LT1 Apr 2024 Rev14 p2, but at VDS=-25/-50V.
# These are deliberately injected STRESSES, NOT guaranteed leakages at W44 5V.
STRESS_UA = (0.1, 15.0, 60.0)
RESISTOR_TOL = 0.01

def off_node_v(r_ohm, supply_v, injected_ua, tol=RESISTOR_TOL):
    if r_ohm <= 0 or supply_v <= 0 or injected_ua < 0 or not 0 <= tol < 1:
        raise ValueError("invalid hypothetical input")
    return min(supply_v, (injected_ua * 1e-6) * r_ohm * (1 + tol))

def on_resistor_mw(r_ohm, supply_v=5.0, tol=RESISTOR_TOL):
    """Resistor upper bound for IDEAL ON P-MOS (not a device dissipation claim)."""
    if r_ohm <= 0 or supply_v <= 0 or not 0 <= tol < 1:
        raise ValueError("invalid hypothetical input")
    return supply_v**2 / (r_ohm * (1 - tol)) * 1000

def results():
    records = []
    for r in RESISTORS_OHM:
        fails = 0
        worst = 0.0
        for v in SUPPLIES_V:
            for ua in STRESS_UA:
                x = off_node_v(r,v,ua)
                fails += x > OFF_CEILING_V
                worst = max(x,worst)
        records.append({
            "r_ohm":r,
            "cases":len(SUPPLIES_V)*len(STRESS_UA),
            "failing_synthetic_cases":fails,
            "off_v_at_60ua_and_5v":off_node_v(r,5,60),
            "worst_stress_v":worst,
            "off_margin_v_at_60ua":OFF_CEILING_V-off_node_v(r,5,60),
            "on_resistor_mw_5v_ideal":on_resistor_mw(r),
            "conditional_pass":fails==0,
        })
    eligible = [row for row in records if row["conditional_pass"]]
    preferred = min(eligible,key=lambda d:d["on_resistor_mw_5v_ideal"])["r_ohm"] if eligible else None
    return {
        "schema":"W45_SYNTHETIC_IDSS_NOT_HARDWARE_V1",
        "datasheet":"https://www.onsemi.com/download/data-sheet/pdf/bss84lt1-d.pdf",
        "source_conditions":"0.1uA at VDS=-25V TJ=25C; 15uA at -50V 25C; 60uA at -50V 125C",
        "IMPORTANT":"None of these figures guarantees IDSS at W44 5V. No receiver VIL or VIH is specified.",
        "assumed_off_ceiling_v":OFF_CEILING_V,
        "assumed_resistor_tolerance":RESISTOR_TOL,
        "assumed_supplies_v":SUPPLIES_V,
        "stress_injections_ua_not_5v_spec":STRESS_UA,
        "total_synthetic_cases":len(SUPPLIES_V)*len(STRESS_UA)*len(RESISTORS_OHM),
        "records":records,
        "preferred_only_if_assumptions_hold_ohm":preferred,
        "w44_kicad_modified":False,
        "battery_dock_energized":False,
        "hardware_safety_proven":False,
        "hardware_power_authorized":False,
        "unresolved":["HEALTH short to +5V","TPS3700 undervoltage and POR","P-MOS stuck or open","receiver VIH/VIL and backfeed","TX FOD and thermal","dual cutoff and local rearm"]
    }

def to_csv(data):
    out=io.StringIO(newline="")
    w=csv.DictWriter(out,fieldnames=list(data["records"][0].keys()))
    w.writeheader()
    w.writerows(data["records"])
    return out.getvalue()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path)
    p.add_argument("--csv",type=Path)
    a=p.parse_args()
    data=results()
    if a.out:
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    if a.csv:
        a.csv.parent.mkdir(parents=True,exist_ok=True)
        a.csv.write_text(to_csv(data),encoding="utf-8")
    print(json.dumps({"synthetic_cases":data["total_synthetic_cases"],"conditional_ohm":data["preferred_only_if_assumptions_hold_ohm"],"hardware_power_authorized":False}))

if __name__=="__main__":
    main()
