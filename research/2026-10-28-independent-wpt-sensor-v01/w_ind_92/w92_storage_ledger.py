"""W-IND-92: interval energy ledger for a single isolated NFC/WPT sensor rail.

Original arithmetic/checking only. It cannot authenticate bench data or control hardware.
Model: E_rail = E_load + 0.5*C*(V_end**2-V_start**2), with buffer ON measured load rail.
No claims of WPT coil efficiency, RF-only sourcing, or battery safety are permitted.
"""
from __future__ import annotations
import json
import re
from decimal import Decimal, InvalidOperation

ONE_MILLION = Decimal(1_000_000)
REQUIRED_FLAGS = ("buffer_on_measured_rx_rail", "same_measurement_window",
                  "external_sources_excluded", "all_other_stores_accounted",
                  "capacitance_characterized")
PROVENANCES = {"synthetic", "manufacturer_data", "bench_measured"}


def decimal_field(d: dict, name: str, *, positive: bool = False) -> Decimal:
    value = d[name]
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise ValueError(f"{name}: not a scalar number")
    try:
        n = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{name}: invalid number") from exc
    if not n.is_finite() or n < 0 or (positive and n == 0):
        raise ValueError(f"{name}: nonfinite/negative/zero")
    return n


def energy_bounds(record: dict) -> dict:
    """Conservative intervals; neither field claims nor arithmetic prove measurements."""
    if record.get("provenance") not in PROVENANCES:
        raise ValueError("unknown provenance")
    for k in REQUIRED_FLAGS:
        if type(record.get(k)) is not bool:
            raise ValueError(f"{k}: explicit bool required")
    tx = decimal_field(record, "tx_input_uj")
    load = decimal_field(record, "load_uj")
    tx_err = decimal_field(record, "tx_abs_error_uj")
    load_err = decimal_field(record, "load_abs_error_uj")
    cap = decimal_field(record, "cap_effective_uf", positive=True)
    tol = decimal_field(record, "cap_tolerance_pct")
    vs = decimal_field(record, "cap_start_mv")
    ve = decimal_field(record, "cap_end_mv")
    ve_err = decimal_field(record, "voltage_abs_error_mv")
    vrated = decimal_field(record, "cap_rated_mv", positive=True)
    if tx_err > tx or load_err > load:
        raise ValueError("energy error larger than reading")
    if tol >= 100:
        raise ValueError("cap tolerance >=100%")
    if ve_err > min(vs, ve):
        raise ValueError("voltage uncertainty includes negative voltage")
    if max(vs, ve) + ve_err > vrated:
        raise ValueError("cap endpoint could exceed specified rating")
    if not isinstance(record.get("case_id"), str) or not record["case_id"].strip():
        raise ValueError("case_id required")
    if record["provenance"] == "bench_measured":
        for f in ("instrument_id", "calibration_reference", "fixture_id", "operator_record"):
            if not isinstance(record.get(f), str) or not record[f].strip():
                raise ValueError(f"bench metadata missing: {f}")
        if not re.fullmatch(r"[0-9a-f]{64}", str(record.get("raw_trace_sha256", ""))):
            raise ValueError("raw trace SHA256 required for bench provenance")
    c_lo, c_hi = cap * (1 - tol / 100), cap * (1 + tol / 100)
    # V in mV, C in uF; energy output in uJ.
    d_min = (ve-ve_err)**2 - (vs+ve_err)**2
    d_max = (ve+ve_err)**2 - (vs-ve_err)**2
    possibilities = [c*d/(2*ONE_MILLION) for c in (c_lo, c_hi) for d in (d_min,d_max)]
    delta_lo, delta_hi = min(possibilities), max(possibilities)
    in_lo, in_hi = tx-tx_err, tx+tx_err
    load_lo, load_hi = load-load_err, load+load_err
    rail_lo, rail_hi = load_lo+delta_lo, load_hi+delta_hi
    reasons = []
    for flag in REQUIRED_FLAGS:
        if not record[flag]:
            reasons.append("not_verified_" + flag)
    if record["provenance"] != "bench_measured":
        reasons.append("no_own_bench_measurement")
    if in_hi == 0:
        status = "NO_TX_INPUT_OBSERVED"
        reasons.append("cannot_infer_RF_power_from_reservoir")
    elif rail_lo > in_hi:
        status = "INCOMPATIBLE_WITH_SINGLE_SOURCE_MODEL"
        reasons.append("lower_rail_energy_exceeds_upper_TX_energy")
    elif rail_hi < 0:
        status = "UNACCOUNTED_RAIL_SINK_OR_BAD_MODEL"
        reasons.append("negative_inferred_rail_energy")
    elif rail_lo < 0 or rail_hi > in_lo:
        status = "UNCERTAIN_REQUIRES_REVIEW"
        reasons.append("energy_bound_crosses_physical_limit")
    else:
        status = "CONSISTENT_WITH_IDEAL_SINGLE_BUFFER_MODEL"
    ratio = None if in_lo == 0 or rail_lo < 0 else [f"{100*rail_lo/in_hi:.3f}", f"{100*rail_hi/in_lo:.3f}"]
    out = {
        "milestone": "W-IND-92", "case_id": record["case_id"],
        "provenance": record["provenance"],
        "delta_buffer_energy_uj_interval": [f"{delta_lo:.3f}", f"{delta_hi:.3f}"],
        "tx_input_uj_interval": [f"{in_lo:.3f}", f"{in_hi:.3f}"],
        "load_uj_interval": [f"{load_lo:.3f}", f"{load_hi:.3f}"],
        "inferred_rail_source_uj_interval": [f"{rail_lo:.3f}", f"{rail_hi:.3f}"],
        "conditional_rail_to_TX_energy_ratio_pct_interval": ratio,
        "naive_load_to_TX_ratio_pct": None if tx == 0 else f"{100*load/tx:.3f}",
        "consistency": status,
        "candidate_for_manual_evidence_review": record["provenance"] == "bench_measured" and not reasons,
        "reject_reasons": sorted(reasons),
        "hardware_release": "BLOCKED",
        "limitations": ["assumed_one_ideal_effective_capacitor", "ESR_leakage_unmeasured",
                        "RF_magnetic_and_converter_losses_not_recovered", "metadata_not_authentication",
                        "W91_USB_I2C_backfeed_exclusion_requires_independent_inspection",
                        "FOD_heat_offset_EMI_cut_and_humidity_unverified", "battery_BMS_dock_disconnected"],
    }
    return out


def demo() -> dict:
    # Invented arithmetic ONLY: one buffered burst can draw > TX input in a short window.
    case = {
        "case_id": "SYNTHETIC_W92_BUFFERED_BURST", "provenance": "synthetic",
        "tx_input_uj": "100", "load_uj": "120", "tx_abs_error_uj": "2",
        "load_abs_error_uj": "2", "cap_effective_uf": "1000",
        "cap_tolerance_pct": "5", "cap_start_mv": "3200", "cap_end_mv": "3190",
        "voltage_abs_error_mv": "1", "cap_rated_mv": "6300",
        **{k: True for k in REQUIRED_FLAGS},
    }
    return {"source": "invented_synthetic_values_not_ST_measurements", "audit": energy_bounds(case)}


if __name__ == "__main__":
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser(description="W92 energy storage ledger (never hardware approval)")
    parser.add_argument("--case", type=Path)
    args = parser.parse_args()
    result = {"audit": energy_bounds(json.loads(args.case.read_text(encoding="utf8")))} if args.case else demo()
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
