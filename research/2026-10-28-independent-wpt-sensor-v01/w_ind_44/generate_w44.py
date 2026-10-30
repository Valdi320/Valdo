"""W-IND-44: original, pin-mapped KiCad draft for W43 TPS3700 OUTB -> P-MOS.
Only a DIAGNOSTIC signal: NOT connected to eFuse EN, dock, motor or battery.
The circuit is NOT qualified: TPS3700 below POR and stuck-high faults remain.
Uses our pre-existing W32 KiCad text renderer IN MEMORY; never edits W32.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from uuid import uuid5, NAMESPACE_URL

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "w_ind_32"))
import generate_w32 as base

PROJECT = "W44_TPS3700_OUTB_PMOS_DIAGNOSTIC_NOT_SAFETY"
base.PROJECT = PROJECT
base.PREFIX = "W44"
base.uid = lambda key: str(uuid5(NAMESPACE_URL, "valdo-w44-original/" + key))
p = base.p
old = base.SPECS

# TI TPS3700 DDC6: 1 OUTA, 2 GND, 3 INA+, 4 INB-, 5 VDD, 6 OUTB.
# onsemi BSS84LT1G SOT23: 1 gate, 2 source, 3 drain. No PCB footprint is selected.
base.SPECS = {
    "SOURCE": old["SOURCE"],
    "MON_SOURCE": ("J", "EXTERNAL_3V3_TEST_ONLY", [
        p(1, "3V3", "power_out", 10.16, 2.54, 180),
        p(2, "RTN", "passive", 10.16, -2.54, 180),
    ], 8, 7, False),
    "HEALTH_OUTPUT": ("J", "DIAGNOSTIC_NOT_EN", [
        p(1, "HEALTH", "passive", -10.16, 2.54, 0),
        p(2, "RTN", "passive", -10.16, -2.54, 0),
    ], 8, 7, False),
    "TPS3700_DDC6": ("U", "TPS3700DDCR_CANDIDATE", [
        p(1, "OUTA", "open_collector", 12.7, 10.16, 180),
        p(2, "GND", "power_in", -12.7, -10.16, 0),
        p(3, "INA+", "input", -12.7, 0, 0),
        p(4, "INB-", "input", -12.7, 5.08, 0),
        p(5, "VDD", "power_in", -12.7, 10.16, 0),
        p(6, "OUTB", "open_collector", 12.7, 5.08, 180),
    ], 9, 13, True),
    "PMOS_BSS84": ("Q", "BSS84LT1G_PROVISIONAL", [
        p(1, "GATE", "passive", -12.7, 0, 0),
        p(2, "SOURCE", "passive", -12.7, 5.08, 0),
        p(3, "DRAIN", "passive", 12.7, 0, 180),
    ], 9, 10, True),
    "R": old["R"],
    "C": old["C"],
}
base.INSTANCES = [
    ("J1", "SOURCE", 22.86, 66.04, "DECLARED_5V_PRE_CUT_NOT_REAL"),
    ("J2", "MON_SOURCE", 22.86, 99.06, "DECLARED_3V3_NOT_REAL"),
    ("J3", "HEALTH_OUTPUT", 243.84, 66.04, "DIAGNOSTIC_ONLY_NOT_EFUSE_EN"),
    ("U1", "TPS3700_DDC6", 116.84, 66.04, "TPS3700DDCR_CANDIDATE"),
    ("Q1", "PMOS_BSS84", 180.34, 66.04, "BSS84LT1G_PROVISIONAL"),
    ("R1", "R", 76.2, 111.76, "63k4_1PCT_CANDIDATE"),
    ("R2", "R", 76.2, 137.16, "10k_1PCT_CANDIDATE"),
    ("R3", "R", 147.32, 111.76, "22k_GATE_PULLUP"),
    ("R4", "R", 220.98, 111.76, "47k_RECEIVER_PULLDOWN"),
    ("C1", "C", 116.84, 111.76, "100nF_DECOUPLE_CANDIDATE"),
]
base.NETS = {
    "VIN_5V_PRE_CUT": [("J1","1"), ("U1","5"), ("Q1","2"), ("R3","1"), ("C1","1")],
    "GND": [("J1","2"), ("J2","2"), ("J3","2"), ("U1","2"), ("R2","2"), ("R4","2"), ("C1","2")],
    "RAIL_3V3_OBSERVED": [("J2","1"), ("R1","1")],
    "INB_DIVIDED": [("R1","2"), ("R2","1"), ("U1","4")],
    "OUTB_GATE": [("U1","6"), ("Q1","1"), ("R3","2")],
    "HEALTH_DIAGNOSTIC": [("Q1","3"), ("J3","1"), ("R4","1")],
}
base.NC = [("U1","1"), ("U1","3")]

NETS, INSTANCES, SPECS, NC = base.NETS, base.INSTANCES, base.SPECS, base.NC

def files() -> dict[str, str]:
    result = base.render_files()
    result["W44.kicad_sym"] = result.pop("W32.kicad_sym")
    result["sym-lib-table"] = result["sym-lib-table"].replace("W32", "W44")
    filename = PROJECT + ".kicad_sch"
    diagram = result[filename]
    messages = [
        ("INCOMPLETE RX CUT TOPOLOGY - DO NOT FABRICATE / ENERGIZE.",
         "W44 OUTB-PMOS PIN-MAPPED DIAGNOSTIC ONLY. DO NOT ENERGIZE."),
        ("TWO TPS259470L STAGES; EXTERNAL PERMITS NOT QUALIFIED; PULL-DOWNS ONLY.",
         "NO EFUSE CONNECTION; HEALTH IS NOT A POWER OR SAFETY ENABLE."),
        ("INA301 ALERT IS READ-ONLY, NOT CONNECTED TO EN. NO FOD/THERMAL/POR/REARM HARDWARE.",
         "TPS3700 OUTB UNDEFINED BELOW POR; STUCK HIGH AND GATE FAULTS REMAIN."),
        ("ILM / ITIMER ARE TBD; OVLO IS GROUNDED AND THUS NO OVP; DVDT OPEN (INRUSH UNSIZED).",
         "BSS84 PIN MAP REQUIRES FOOTPRINT AND BODY-DIODE REVIEW; NO SPICE."),
        ("NO TX, NO DOCK, NO BATTERY/BMS, NO EMI OR PHYSICAL DATA.",
         "NO COIL OR RF OR TX; NO BATTERY/BMS/DOCK/MOTOR/EXPERIMENT."),
    ]
    for src, dst in messages:
        if src not in diagram:
            raise RuntimeError("W32 renderer warning changed; stop instead of dropping notice")
        diagram = diagram.replace(src, dst)
    result[filename] = diagram
    result[PROJECT + ".kicad_pro"] = '{"meta":{"filename":"' + PROJECT + '.kicad_pro","version":3}}\n'
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    target = Path(__file__).parent
    generated = files()
    if args.verify:
        differences = [name for name, body in generated.items()
                       if not (target / name).exists() or (target / name).read_text(encoding="utf-8") != body]
        if differences:
            raise SystemExit("BLOCKED reproducibility: " + ", ".join(differences))
        print("PASS W44 deterministic KiCad source: electrical safety NOT validated")
    else:
        for name, body in generated.items():
            (target / name).write_text(body, encoding="utf-8")
        print("GENERATED " + ", ".join(sorted(generated)))

if __name__ == "__main__":
    main()
