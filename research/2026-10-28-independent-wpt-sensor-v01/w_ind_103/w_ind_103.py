"""W-IND-103: deterministic evidence for the finite manufacturer-data gate."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from w_ind_102.w_ind_102 import DATA_PATH, build_report, load_rows, validate_rows


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def legacy_guard(row: dict) -> bool:
    return not (
        min(row["h_a_per_m_rms"], row["v_eh_v"], row["i_eh_ma"], row["p_eh_mw"]) <= 0
    ) and not (
        abs(row["v_eh_v"] * row["i_eh_ma"] - row["p_eh_mw"]) > 0.0051
    )


def strict_rejects(rows: list[dict]) -> bool:
    try:
        validate_rows(rows)
    except ValueError:
        return True
    return False


def build_evidence() -> dict:
    rows = load_rows(DATA_PATH)
    nan_case = [dict(row) for row in rows]
    nan_case[0]["p_eh_mw"] = float("nan")
    inf_case = [dict(row) for row in rows]
    inf_case[0]["v_eh_v"] = float("inf")
    inf_case[0]["p_eh_mw"] = float("inf")

    cases = [
        {
            "case": "p_eh_mw=NaN",
            "legacy_guard_accepts": legacy_guard(nan_case[0]),
            "strict_validator_rejects": strict_rejects(nan_case),
        },
        {
            "case": "v_eh_v=+Inf and p_eh_mw=+Inf",
            "legacy_guard_accepts": legacy_guard(inf_case[0]),
            "strict_validator_rejects": strict_rejects(inf_case),
        },
    ]
    if not all(c["legacy_guard_accepts"] and c["strict_validator_rejects"] for c in cases):
        raise AssertionError("legacy defect reproduction or strict rejection changed")

    valid_report = build_report(rows)
    json.dumps(valid_report, sort_keys=True, allow_nan=False)

    return {
        "schema": "valdo.w_ind_103.evidence.v1",
        "milestone": "W-IND-103",
        "classification": "SOFTWARE_DATA_VALIDATION_ONLY",
        "baseline_head": "be2dbbbcdd3d6f8f00e49065c222ed737c7d5b31",
        "status": "REPRODUCED_LOCALLY_CI_REQUIRED",
        "baseline_false_acceptance_cases": cases,
        "valid_manufacturer_points": valid_report["manufacturer_points"]["count"],
        "max_am10_mw": valid_report["manufacturer_points"]["max_am10_mw"],
        "max_am100_mw": valid_report["manufacturer_points"]["max_am100_mw"],
        "valid_report_strict_json": True,
        "physical_measurements": 0,
        "electromagnetic_simulations": 0,
        "battery_bms_dock_connected": False,
        "hardware_approved": False,
        "third_party_code_or_cad_copied": False,
        "third_party_repositories_modified": False,
        "oomwoo_or_pr79_modified": False,
        "input_sha256": sha256(DATA_PATH),
        "model_sha256": sha256(Path(__file__).resolve()),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    payload = json.dumps(build_evidence(), indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
