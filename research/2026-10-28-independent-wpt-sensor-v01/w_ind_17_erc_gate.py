"""W-IND-17: read actual KiCad CLI ERC JSON. NOT physical safety proof."""
import argparse
import hashlib
import json
import os
from collections import Counter
from pathlib import Path

def evaluate(code, report):
    if code not in (0, 5):
        raise ValueError("KiCad invocation error, not an ERC verdict")
    # Real KiCad 9.0.2 writes ERC findings PER SHEET, not at report root.
    if not isinstance(report, dict) or report.get("$schema") != "https://schemas.kicad.org/erc.v1.json":
        raise ValueError("unrecognized KiCad ERC JSON schema")
    sheets = report.get("sheets")
    if not isinstance(sheets, list) or not sheets:
        raise ValueError("invalid or missing KiCad sheets array")
    violations = []
    for sheet in sheets:
        if not isinstance(sheet, dict) or not isinstance(sheet.get("violations"), list):
            raise ValueError("invalid KiCad sheet violations")
        if not isinstance(sheet.get("path"), str) or not sheet["path"]:
            raise ValueError("invalid KiCad sheet path")
        violations.extend(sheet["violations"])
    if any(not isinstance(v, dict) for v in violations):
        raise ValueError("invalid violation entry")
    if (code == 0) != (len(violations) == 0):
        raise ValueError("CLI return and report disagree")
    by_type=Counter(str(v.get("type", "unspecified")) for v in violations)
    by_severity=Counter(str(v.get("severity", "unspecified")) for v in violations)
    return {
        "status": ("ERC_HAS_VIOLATIONS_DO_NOT_BUILD" if violations
                   else "ERC_ZERO_REPORTED_STILL_DO_NOT_BUILD"),
        "erc_rc": code, "erc_count": len(violations),
        "by_type": dict(sorted(by_type.items())),
        "by_severity": dict(sorted(by_severity.items())),
        "erc_executed": True, "hardware_approved": False,
        "autonomous_fod_proven": False, "thermal_trip_proven": False,
        "overcurrent_proven": False, "reverse_blocking_proven": False,
        "independent_cuts_proven": False, "lithium_charging_approved": False}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--rc",type=int,required=True)
    p.add_argument("--report",type=Path,required=True)
    p.add_argument("--schematic",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--version",required=True)
    a=p.parse_args()
    verdict=evaluate(a.rc,json.loads(a.report.read_text(encoding="utf-8")))
    verdict.update(milestone="W-IND-17", kicad_version=a.version,
        source_schematic=a.schematic.as_posix(),
        source_sha256=hashlib.sha256(a.schematic.read_bytes()).hexdigest(),
        github_sha=os.environ.get("GITHUB_SHA","local"),
        test_kind="real_KiCad_ERC_ephemeral_CI",
        physical_tests=0, hardware_energized=False)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(verdict,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(verdict,indent=2,sort_keys=True))
if __name__=="__main__":
    main()
