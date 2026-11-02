"""W38 KiCad experimental candidate. Builds exclusively on our W36/W32 generators.
Edits their Python objects IN MEMORY, never any upstream, historical or coworker files.
NOT safety qualified. DO NOT ENERGIZE.
"""
from pathlib import Path
from uuid import uuid5, NAMESPACE_URL
import argparse
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "w_ind_36"))
import generate_w36 as previous

b = previous.base
PROJECT = "W38_RX_INA301_TO_DUAL_CUT_INCOMPLETE"
assert ("U1", "6") in b.NETS["ALERT_N_READ_ONLY"]
assert ("R2", "1") in b.NETS["RX5_SOURCE"]
assert ("U4", "4") in b.NC
assert ("U4", "1") in b.NETS["PG_MON_3V3"]
assert ("U7", "6") in b.NETS["CLR_A_POSITIVE"]
assert ("U8", "6") in b.NETS["CLR_B_POSITIVE"]
assert ("U9", "4") in b.NC # never short output domains

# Repair domain-level pull-up mismatch, and permit local autonomous alarm reset.
b.NETS["RX5_SOURCE"].remove(("R2", "1"))
b.NETS["MON_3V3_EXTERNAL"].append(("R2", "1"))
b.NETS["ALERT_N_FORCE_LOCAL_RESET"] = b.NETS.pop("ALERT_N_READ_ONLY") + [("U4", "4")]
b.NC.remove(("U4", "4"))
previous.PROJECT = b.PROJECT = PROJECT
previous.PREFIX = b.PREFIX = "W38"
b.uid = lambda key: str(uuid5(NAMESPACE_URL, "valdo-original-w38/" + key))
NETS, NC, INSTANCES, SPECS = b.NETS, b.NC, b.INSTANCES, b.SPECS

def files():
    results = previous.files()
    results["W38.kicad_sym"] = results.pop("W36.kicad_sym")
    results["sym-lib-table"] = results["sym-lib-table"].replace("W36", "W38")
    name = PROJECT + ".kicad_sch"
    schematic = results[name]
    replacements = {
        "W36 DUAL SUPERVISORS + LOCAL LATCH - INCOMPLETE. DO NOT ENERGIZE.":
            "W38 INA301 ALARM TO DUAL LOCAL CUT CANDIDATE. DO NOT ENERGIZE.",
        "INA301 ALERT READ ONLY; NO CURRENT TRIP, FOD OR THERMAL CUT BUILT.":
            "INA301 ALERT_N LOW -> U4 MR_N -> U7/U8 CLR -> both EN OFF; NO PHYSICAL QA.",
        "EXT 3V3 SUPPLY UNQUALIFIED; NO TX/DOCK/BATTERY/EMI OR PHYSICAL QA.":
            "ALERT 10k pullup now 3V3; lost INA301 VDD can still look healthy; NO POWER."
    }
    for old, new in replacements.items():
        assert old in schematic, "W36 notes changed: " + old
        schematic = schematic.replace(old, new)
    results[name] = schematic
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    destination = Path(__file__).parent
    expected = files()
    if args.verify:
        bad = [name for name, value in expected.items()
               if not (destination / name).exists() or
               (destination / name).read_text(encoding="utf-8") != value]
        if bad: raise SystemExit("BLOCKED generated output differs: " + str(bad))
        print("PASS generated W38 assets match sources (UNPOWERED ONLY)")
    else:
        for name, value in expected.items():
            (destination / name).write_text(value, encoding="utf-8")
        print("Generated", ", ".join(expected))
