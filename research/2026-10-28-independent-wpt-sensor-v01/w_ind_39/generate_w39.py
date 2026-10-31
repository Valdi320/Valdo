"""W-IND-39: redundant overcurrent monitor candidate on ORIGINAL VALDO W38.
Generated KiCad concept only. No battery/dock, no permission to energize.
Never modifies W32/W36/W38 files: module objects altered in process memory.
"""
from pathlib import Path
from uuid import uuid5, NAMESPACE_URL
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "w_ind_38"))
import generate_w38 as upstream

b = upstream.b
PROJECT = "W39_RX_DUAL_INA301_INCOMPLETE"
assert ("U1", "6") in b.NETS["ALERT_N_FORCE_LOCAL_RESET"]
assert ("U4", "4") in b.NETS["ALERT_N_FORCE_LOCAL_RESET"]
assert ("U9", "4") in b.NC
assert ("U1", "8") in b.NETS["KELVIN_PLUS"]
assert ("U1", "7") in b.NETS["KELVIN_MINUS"]
assert ("R2", "1") in b.NETS["MON_3V3_EXTERNAL"]
assert all(ref not in {x[0] for x in b.INSTANCES}
           for ref in ("U12", "R3", "R4", "C7"))

# Both comparators share ONE shunt (known common-mode failure).
# Their own independent ALERT_N signals drive the TWO existing voltage
# supervisors' separate manual-reset pins. No wired-OR on different rails.
b.INSTANCES += [
    ("U12", "INA301A1_DGK", 393.70, 111.76, "INA301A1IDGKR"),
    ("R3", "R", 384.81, 180.34, "10k_ALERT_B_PULLUP_5V_TBD"),
    ("R4", "R", 407.67, 180.34, "8k66_LIMIT_B_TBD"),
    ("C7", "C", 384.81, 226.06, "100nF_U12_TBD"),
]
b.NETS["MON_3V3_EXTERNAL"] += [("U12", "1"), ("U12", "5"), ("C7", "1")]
b.NETS["RX5_SOURCE"] += [("R3", "1")]
b.NETS["GND"] += [("U12", "4"), ("R4", "2"), ("C7", "2")]
b.NETS["KELVIN_PLUS"] += [("U12", "8")]
b.NETS["KELVIN_MINUS"] += [("U12", "7")]
b.NETS["LIMIT_B"] = [("U12", "3"), ("R4", "1")]
b.NETS["ALERT_B_FORCE_RX_RESET"] = [
    ("U12", "6"), ("R3", "2"), ("U9", "4")
]
b.NC.remove(("U9", "4"))
b.NC.append(("U12", "2"))
upstream.PROJECT = upstream.previous.PROJECT = b.PROJECT = PROJECT
upstream.previous.PREFIX = b.PREFIX = "W39"
b.uid = lambda key: str(uuid5(NAMESPACE_URL, "valdo-original-w39/" + key))
NETS, NC, INSTANCES, SPECS = b.NETS, b.NC, b.INSTANCES, b.SPECS

def files():
    result = upstream.files()
    result["W39.kicad_sym"] = result.pop("W38.kicad_sym")
    result["sym-lib-table"] = result["sym-lib-table"].replace("W38", "W39")
    filename = PROJECT + ".kicad_sch"
    schematic = result[filename]
    edits = {
        "W38 INA301 ALARM TO DUAL LOCAL CUT CANDIDATE. DO NOT ENERGIZE.":
            "W39 TWO INA301 ALARMS, TWO TPS3840 MR INPUTS; NOT QUALIFIED.",
        "INA301 ALERT_N LOW -> U4 MR_N -> U7/U8 CLR -> both EN OFF; NO PHYSICAL QA.":
            "U1 ALERT -> U4 MR; U12 ALERT -> U9 MR; BOTH GATE DUAL EN.",
        "ALERT 10k pullup now 3V3; lost INA301 VDD can still look healthy; NO POWER.":
            "TWO ICs SHARE SHUNT AND 3V3: COMMON FAILURES REMAIN; NO POWER."
    }
    for before, after in edits.items():
        assert before in schematic, "W38 baseline changed: " + before
        schematic = schematic.replace(before, after)
    result[filename] = schematic
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    path = Path(__file__).parent
    output = files()
    if args.verify:
        diff = [name for name, value in output.items()
                if not (path / name).exists() or (path / name).read_text() != value]
        if diff:
            raise SystemExit("BLOCKED generated W39 differs: " + repr(diff))
        print("PASS W39 generator reproducibility; NOT hardware clearance")
    else:
        for name, value in output.items():
            (path / name).write_text(value, encoding="utf-8")
        print("Generated W39 draft: " + ", ".join(output))

if __name__ == "__main__":
    main()
