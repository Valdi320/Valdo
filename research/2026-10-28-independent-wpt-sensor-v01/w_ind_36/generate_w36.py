"""W-IND-36: original candidate RX dual-supply supervisory/local-rearm KiCad overlay.
INCOMPLETE: not a safety circuit or permission to apply power. No battery.
Derives ONLY our own reviewed W32 generator; external project code is not copied.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from uuid import uuid5, NAMESPACE_URL

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "w_ind_32"))
import generate_w32 as base

PROJECT = "W36_RX_DUAL_PG_LOCAL_REARM_INCOMPLETE"
PREFIX = "W36"
p = base.p

# TI datasheet pin maps are tied to the exact DBV, DCU and RPW variants.
SUP_PINS = [
    p(1, "RESET_N", "output", 12.7, 10.16, 180),
    p(2, "VDD", "power_in", -12.7, 5.08, 0),
    p(3, "GND", "power_in", -12.7, -10.16, 0),
    p(4, "MR_N", "input", 12.7, 5.08, 180),
    p(5, "CT", "passive", 12.7, 0, 180),
]
AND_PINS = [
    p(1, "A", "input", -12.7, 5.08, 0),
    p(2, "B", "input", -12.7, 0, 0),
    p(3, "GND", "power_in", -12.7, -10.16, 0),
    p(4, "Y", "output", 12.7, 0, 180),
    p(5, "VCC", "power_in", -12.7, 10.16, 0),
]
DFF_PINS = [
    p(1, "CLK", "input", -12.7, 15.24, 0),
    p(2, "D", "input", -12.7, 10.16, 0),
    p(3, "Q_N", "output", 12.7, 10.16, 180),
    p(4, "GND", "power_in", -12.7, -15.24, 0),
    p(5, "Q", "output", 12.7, 5.08, 180),
    p(6, "CLR_N", "input", -12.7, 0, 0),
    p(7, "PRE_N", "input", -12.7, -5.08, 0),
    p(8, "VCC", "power_in", -12.7, -10.16, 0),
]

# The only modification of prior work is IN-MEMORY in this Python process.
base.PROJECT = PROJECT
base.PREFIX = PREFIX
base.uid = lambda key: str(uuid5(NAMESPACE_URL, "valdo-original-w36/" + key))
base.SPECS = dict(base.SPECS)
base.SPECS.update({
    "SUP_MON": ("U", "TPS3840PL28DBVR", SUP_PINS, 9, 13, True),
    "SUP_RX": ("U", "TPS3840PL42DBVR", SUP_PINS, 9, 13, True),
    "AND": ("U", "SN74LVC1G08DBVR", AND_PINS, 9, 13, True),
    "DFF": ("U", "SN74LVC1G74DCUR", DFF_PINS, 9, 18, True),
    "SW": ("SW", "LOCAL_BUTTON_TBD_NOT_DEBOUNCED", [
        p(1, "A", "passive", -10.16, 0, 0),
        p(2, "B", "passive", 10.16, 0, 180),
    ], 8, 5, False),
    "MON_SOURCE": ("J", "EXT_3V3_RAIL_NOT_QUALIFIED", [
        p(1, "3V3", "power_out", 10.16, 2.54, 180),
        p(2, "RETURN", "passive", 10.16, -2.54, 180),
    ], 8, 7, False),
})
base.INSTANCES = [x for x in base.INSTANCES if x[0] not in ("J3", "J4")]
base.INSTANCES += [
    ("J5", "MON_SOURCE", 22.86, 238.76, "EXT_3V3_RAIL_NOT_QUALIFIED"),
    ("U4", "SUP_MON", 223.52, 53.34, "TPS3840PL28DBVR"),
    ("U9", "SUP_RX", 271.78, 53.34, "TPS3840PL42DBVR"),
    ("U5", "AND", 223.52, 137.16, "SN74LVC1G08DBVR"),
    ("U6", "AND", 271.78, 137.16, "SN74LVC1G08DBVR"),
    ("U10", "AND", 223.52, 95.25, "SN74LVC1G08DBVR"),
    ("U11", "AND", 271.78, 95.25, "SN74LVC1G08DBVR"),
    ("U7", "DFF", 223.52, 184.15, "SN74LVC1G74DCUR"),
    ("U8", "DFF", 271.78, 184.15, "SN74LVC1G74DCUR"),
    ("SW1", "SW", 22.86, 218.44, "LOCAL_ARM_A_NO_DEBOUNCE"),
    ("SW2", "SW", 71.12, 218.44, "LOCAL_ARM_B_NO_DEBOUNCE"),
    ("RCLK1", "R", 114.3, 218.44, "100k_CLOCK_A_TBD"),
    ("RCLK2", "R", 139.7, 218.44, "100k_CLOCK_B_TBD"),
    ("RPG1", "R", 322.58, 95.25, "100k_PG_MON_TBD"),
    ("RPG2", "R", 350.52, 95.25, "100k_PG_RX_TBD"),
    ("RCLR1", "R", 322.58, 137.16, "100k_CLR_A_TBD"),
    ("RCLR2", "R", 350.52, 137.16, "100k_CLR_B_TBD"),
    ("C3", "C", 322.58, 187.96, "100nF_MON_TBD"),
    ("C4", "C", 350.52, 187.96, "100nF_RX_TBD"),
    ("C5", "C", 322.58, 222.25, "100nF_LATCH_A_TBD"),
    ("C6", "C", 350.52, 222.25, "100nF_LATCH_B_TBD"),
]
base.NETS = {k:list(v) for k,v in base.NETS.items()}
base.NETS["RX5_SOURCE"] = [x for x in base.NETS["RX5_SOURCE"]
                             if x not in (("U1","1"), ("U1","5"), ("C1","1"))] + [
    ("U9","2"), ("C4","1")
]
base.NETS["GND"] = [x for x in base.NETS["GND"] if x[0] not in ("J3","J4")] + [
    ("J5","2"),("U4","3"),("U9","3"),
    ("U5","3"),("U6","3"),("U10","3"),("U11","3"),
    ("U7","4"),("U8","4"),
    ("RCLK1","2"),("RCLK2","2"),("RPG1","2"),("RPG2","2"),
    ("RCLR1","2"),("RCLR2","2"),
    ("C3","2"),("C4","2"),("C5","2"),("C6","2")
]
del base.NETS["PERMIT_A_UNQUALIFIED"]
del base.NETS["PERMIT_B_UNQUALIFIED"]
base.NETS.update({
    "MON_3V3_EXTERNAL": [
        ("J5","1"),("U1","1"),("U1","5"),("C1","1"),("U4","2"),
        ("U5","5"),("U6","5"),("U10","5"),("U11","5"),
        ("U7","2"),("U7","7"),("U7","8"),("U8","2"),("U8","7"),("U8","8"),
        ("SW1","1"),("SW2","1"),("C3","1"),("C5","1"),("C6","1")
    ],
    "PG_MON_3V3": [("U4","1"),("U10","1"),("U11","1"),("U5","2"),("RPG1","1")],
    "PG_RX5": [("U9","1"),("U10","2"),("U11","2"),("U6","2"),("RPG2","1")],
    "CLR_A_POSITIVE": [("U10","4"),("U7","6"),("RCLR1","1")],
    "CLR_B_POSITIVE": [("U11","4"),("U8","6"),("RCLR2","1")],
    "CLOCK_A_LOCAL": [("SW1","2"),("RCLK1","1"),("U7","1")],
    "CLOCK_B_LOCAL": [("SW2","2"),("RCLK2","1"),("U8","1")],
    "Q_A_ARMED": [("U7","5"),("U5","1")],
    "Q_B_ARMED": [("U8","5"),("U6","1")],
    "PERMIT_A_LOCAL_PG": [("U5","4"),("U2","1"),("RPD1","1")],
    "PERMIT_B_LOCAL_PG": [("U6","4"),("U3","1"),("RPD2","1")],
})
base.NC = list(base.NC) + [
    ("U4","4"), ("U4","5"), ("U9","4"), ("U9","5"),
    ("U7","3"), ("U8","3")
]
INSTANCES, SPECS, NETS, NC = base.INSTANCES, base.SPECS, base.NETS, base.NC

def files():
    r = base.render_files()
    # Remap W32's hardcoded library basename only in the new W36 output.
    r['W36.kicad_sym'] = r.pop('W32.kicad_sym')
    r['sym-lib-table'] = r['sym-lib-table'].replace('W32', 'W36')
    old = "INCOMPLETE RX CUT TOPOLOGY - DO NOT FABRICATE / ENERGIZE."
    replacements = {
        old: "W36 DUAL SUPERVISORS + LOCAL LATCH - INCOMPLETE. DO NOT ENERGIZE.",
        "TWO TPS259470L STAGES; EXTERNAL PERMITS NOT QUALIFIED; PULL-DOWNS ONLY.":
            "EN A/B: independent PG-gated DFF + LOCAL switches; NO RADIO REARM.",
        "INA301 ALERT IS READ-ONLY, NOT CONNECTED TO EN. NO FOD/THERMAL/POR/REARM HARDWARE.":
            "INA301 ALERT READ ONLY; NO CURRENT TRIP, FOD OR THERMAL CUT BUILT.",
        "ILM / ITIMER ARE TBD; OVLO IS GROUNDED AND THUS NO OVP; DVDT OPEN (INRUSH UNSIZED).":
            "ILIM ITIMER OVP INRUSH UNQUALIFIED; SEQUENCING BOUNCE FAULTS OPEN.",
        "NO TX, NO DOCK, NO BATTERY/BMS, NO EMI OR PHYSICAL DATA.":
            "EXT 3V3 SUPPLY UNQUALIFIED; NO TX/DOCK/BATTERY/EMI OR PHYSICAL QA."
    }
    schematic_name = PROJECT + ".kicad_sch"
    sch = r[schematic_name]
    for prev, nxt in replacements.items():
        assert prev in sch, "base generator notes changed: " + prev
        sch = sch.replace(prev,nxt)
    sch = sch.replace("valdo-w32-original", "valdo-w36-original")
    r[schematic_name] = sch
    r[PROJECT + ".kicad_pro"] = '{"meta": {"filename": "' + PROJECT + '.kicad_pro", "version": 3}}\n'
    return r

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()
    dest = Path(__file__).parent
    expected = files()
    if args.verify:
        missing = [n for n,c in expected.items() if not (dest/n).exists() or (dest/n).read_text() != c]
        if missing: raise SystemExit("BLOCKED: generated files missing/modified " + repr(missing))
        print("PASS deterministic KiCad W36 generators (NOT safety approval)")
    else:
        for name,content in expected.items(): (dest/name).write_text(content)
        print("GENERATED " + ",".join(expected))
if __name__ == "__main__":
    main()
