"""W-IND-84: fail-closed digital audit of measured/synthetic WPT/RF traces.

No hardware control; standard library only; not a safety certificate.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

COLUMNS = ("t_us", "tx_mv", "tx_ua", "rx_mv", "rx_ua", "rail_mv", "phase")
PHASES = frozenset(("sleep", "wake", "tx", "rx", "ack", "retry", "idle"))
RF_REQUIRED = frozenset(("sleep", "wake", "tx", "rx", "ack"))
MAX_RECORDS = 2_000_000


def _number(x: str) -> Decimal:
    try:
        d = Decimal(str(x))
    except InvalidOperation as exc:
        raise ValueError("invalid_numeric_value") from exc
    if not d.is_finite() or d < 0:
        raise ValueError("negative_or_nonfinite_value")
    return d


def parse_csv(raw: bytes) -> list[dict]:
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("trace_not_utf8") from exc
    rd = csv.DictReader(io.StringIO(text), strict=True)
    if tuple(rd.fieldnames or ()) != COLUMNS:
        raise ValueError("unexpected_csv_columns")
    rows = []
    last = None
    for row in rd:
        if len(rows) >= MAX_RECORDS:
            raise ValueError("too_many_samples")
        if None in row or any(row[k] is None for k in COLUMNS):
            raise ValueError("incomplete_csv_row")
        rec = {k: _number(row[k]) for k in COLUMNS[:-1]}
        rec["phase"] = row["phase"]
        if rec["phase"] not in PHASES:
            raise ValueError("unknown_radio_phase")
        if rec["t_us"] != rec["t_us"].to_integral_value():
            raise ValueError("fractional_timestamp_us")
        if last is None and rec["t_us"] != 0:
            raise ValueError("trace_must_start_at_zero")
        if last is not None and rec["t_us"] <= last:
            raise ValueError("nonmonotonic_timestamp")
        last = rec["t_us"]
        rows.append(rec)
    if len(rows) < 2:
        raise ValueError("insufficient_samples")
    return rows


def evaluate(manifest: dict, raw: bytes) -> dict:
    """Integrate time-aligned WPT TX input and regulated RX output; never approve hardware."""
    rows = parse_csv(raw)
    expected_hash = manifest.get("trace_sha256", "")
    if not isinstance(expected_hash, str) or len(expected_hash) != 64:
        raise ValueError("sha256_required")
    if hashlib.sha256(raw).hexdigest() != expected_hash:
        raise ValueError("trace_sha256_mismatch")
    provenance = manifest.get("provenance")
    if provenance not in ("synthetic", "manufacturer_data", "bench_measured"):
        raise ValueError("invalid_provenance")
    max_gap = _number(manifest["max_gap_us"])
    floor = _number(manifest["required_rail_min_mv"])
    uncertainty = _number(manifest["rail_uncertainty_mv"])
    if max_gap == 0:
        raise ValueError("zero_gap_limit")
    tx_uj = Decimal(0)
    rx_uj = Decimal(0)
    max_seen_gap = Decimal(0)
    phase_us = {p: Decimal(0) for p in sorted(PHASES)}
    reasons = []
    for a, b in zip(rows, rows[1:]):
        dt = b["t_us"] - a["t_us"]
        max_seen_gap = max(max_seen_gap, dt)
        phase_us[a["phase"]] += dt
        for prefix in ("tx", "rx"):
            p0 = a[f"{prefix}_mv"] * a[f"{prefix}_ua"]
            p1 = b[f"{prefix}_mv"] * b[f"{prefix}_ua"]
            energy_uj = (p0 + p1) * dt / Decimal(2_000_000_000)
            if prefix == "tx":
                tx_uj += energy_uj
            else:
                rx_uj += energy_uj
    if max_seen_gap > max_gap:
        reasons.append("sample_gap_exceeded")
    minimum_rail = min(x["rail_mv"] for x in rows)
    if minimum_rail - uncertainty < floor:
        reasons.append("sampled_rail_below_guarded_floor")
    if tx_uj == 0:
        reasons.append("zero_tx_input_energy")
    if rx_uj > tx_uj:
        reasons.append("rx_energy_exceeds_tx_input_check_storage_or_channels")
    total_us = rows[-1]["t_us"]
    radio_complete = RF_REQUIRED.issubset({p for p, t in phase_us.items() if t > 0})
    if not radio_complete:
        reasons.append("rf_cycle_incomplete")
    if provenance == "bench_measured":
        if not all(isinstance(manifest.get(k), str) and manifest[k].strip() for k in
                   ("instrument_id", "calibration_reference", "fixture_id", "operator_record")):
            reasons.append("bench_trace_missing_provenance_metadata")
        if total_us < 2_500_000:
            reasons.append("bench_trace_shorter_than_ten_250ms_leases")
        if max_gap > 1_000:
            reasons.append("bench_sampling_requirement_over_1ms")
        if manifest.get("steady_state_cycle") is not True:
            reasons.append("storage_end_state_not_declared_equal")
    if provenance != "bench_measured":
        reasons.append("not_own_bench_measurement")
    out = {
        "case_id": str(manifest.get("case_id", "unnamed")),
        "provenance": provenance,
        "sample_count": len(rows),
        "duration_us": int(total_us),
        "max_observed_gap_us": int(max_seen_gap),
        "tx_input_energy_uj": f"{tx_uj:.3f}",
        "rx_output_energy_uj": f"{rx_uj:.3f}",
        "apparent_cycle_efficiency_pct": f"{rx_uj * 100 / tx_uj:.3f}" if tx_uj else None,
        "minimum_sampled_rail_mv": f"{minimum_rail:.3f}",
        "guarded_sampled_rail_mv": f"{minimum_rail - uncertainty:.3f}",
        "rf_observation_phases": sorted(p for p, t in phase_us.items() if t > 0),
        "evidence_eligible": not reasons,
        "reject_reasons": sorted(reasons),
        "hardware_release": "BLOCKED",
        "unverified": ["subsample_brownouts", "FOD_real", "thermal_real", "EMI_real",
                       "offset_real", "independent_cutoff", "water_ingress",
                       "battery_BMS_dock", "radio_privacy_and_application_ACK"],
    }
    return out


def demo() -> tuple[dict, bytes]:
    """Invented numbers explicitly labelled synthetic, never a physical measurement."""
    phases = ("sleep", "wake", "tx", "rx", "ack", "idle")
    rows = [COLUMNS]
    for i, phase in enumerate(phases):
        rows.append((str(i * 1000), "5000", "4000", "3300", "1000", "3300", phase))
    raw = ("\n".join(",".join(row) for row in rows) + "\n").encode()
    manifest = {"case_id": "SYNTHETIC_W84_DEMO", "provenance": "synthetic",
                "trace_sha256": hashlib.sha256(raw).hexdigest(),
                "max_gap_us": 1000, "required_rail_min_mv": 3000,
                "rail_uncertainty_mv": 20}
    return manifest, raw


def main() -> None:
    parser = argparse.ArgumentParser(description="W84 digital-only WPT measurement gate")
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--trace", type=Path)
    args = parser.parse_args()
    if bool(args.manifest) != bool(args.trace):
        parser.error("pass BOTH --manifest and --trace, or neither for synthetic demo")
    if args.manifest:
        meta = json.loads(args.manifest.read_text(encoding="utf-8"))
        raw = args.trace.read_bytes()
    else:
        meta, raw = demo()
    print(json.dumps(evaluate(meta, raw), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
