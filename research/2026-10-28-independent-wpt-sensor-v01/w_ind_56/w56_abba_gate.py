"""W-IND-56: synthetic-only AB/BA/BA/AB consistency gate for two power meters.

Original VALDO W-sector implementation. No I2C, RF, hardware or lithium charging.
All numeric tolerances are arbitrary screening hypotheses, not safety limits.
"""
from __future__ import annotations
import argparse
import json
from decimal import Decimal, InvalidOperation

ROLES = (("A", "B"), ("B", "A"), ("B", "A"), ("A", "B"))
D1 = Decimal(1)


def num(value):
    if isinstance(value, bool):
        raise ValueError("boolean supplied as measurement")
    try:
        v = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError("invalid numeric evidence") from exc
    if not v.is_finite():
        raise ValueError("non-finite evidence")
    return v


def _range_ratio(row):
    pin, pout = num(row["pin_mw"]), num(row["pout_mw"])
    ui, uo = num(row["u_pin_mw"]), num(row["u_pout_mw"])
    if min(pin, pout) <= 0 or min(ui, uo) < 0 or pin <= ui or pout <= uo:
        raise ValueError("non-positive power or uncertain power interval")
    low, high = (pout - uo) / (pin + ui), (pout + uo) / (pin - ui)
    if high >= 1:
        raise ValueError("apparent energy efficiency impossible or unresolved")
    return pout / pin, low, high


def evaluate(rows):
    """Cancel fixed relative meter gain, then screen a one-passage interior anomaly.

    With equally spaced t=0,1,2,3 and log-linear true efficiency:
        R0=k*eta0, R1=eta1/k, R2=eta2/k, R3=k*eta3
    Estimator=(R0*R1*R2*R3)^0.25; rho=(R2/R1)^3/(R3/R0)=1.
    The latter comparison detects a transient on just ONE middle passage,
    which 3-pass ABA cannot distinguish from an unobserved central anomaly.
    Two equal center anomalies, correlated meter changes and non-log-linear
    fluctuations can still evade this gate.
    """
    if type(rows) not in (list, tuple) or len(rows) != 4 or any(type(r) is not dict for r in rows):
        raise ValueError("four independent dictionaries required")
    if any((r.get("in_meter"), r.get("out_meter")) != role for r, role in zip(rows, ROLES)):
        raise ValueError("expected AB-BA-BA-AB meter positions")
    for field in ("run_id", "trace_id"):
        vals = [r.get(field) for r in rows]
        if any(type(v) is not str or not v.strip() for v in vals) or len(set(vals)) != 4:
            raise ValueError("missing or reused sample/trace identity")
    fixture = rows[0].get("fixture_id")
    if type(fixture) is not str or not fixture or any(r.get("fixture_id") != fixture for r in rows):
        raise ValueError("fixture must be common and identified")
    source = rows[0].get("source_kind")
    if source not in ("SYNTHETIC", "BENCH_MEASURED") or any(r.get("source_kind") != source for r in rows):
        raise ValueError("mixed or unknown provenance")
    centers = []
    previous_end = -1
    for r in rows:
        start, end = r.get("start_ms"), r.get("end_ms")
        if type(start) is not int or type(end) is not int or start < 0 or end <= start or start < previous_end:
            raise ValueError("non-monotonic, overlapping or malformed acquisition")
        centers.append(Decimal(start + end) / 2)
        previous_end = end
    ratios = [_range_ratio(r) for r in rows]
    r0, r1, r2, r3 = [x[0] for x in ratios]
    low = [x[1] for x in ratios]
    high = [x[2] for x in ratios]
    eta = (r0 * r1 * r2 * r3).sqrt().sqrt()
    eta_lo = (low[0] * low[1] * low[2] * low[3]).sqrt().sqrt()
    eta_hi = (high[0] * high[1] * high[2] * high[3]).sqrt().sqrt()
    rho = r2**3 * r0 / (r1**3 * r3)
    rho_lo = low[2]**3 * low[0] / (high[1]**3 * high[3])
    rho_hi = high[2]**3 * high[0] / (low[1]**3 * low[3])
    residual_worst = max(abs(rho_lo - D1), abs(rho_hi - D1)) * 100
    end_lo = low[3] / high[0]
    end_hi = high[3] / low[0]
    endpoint_worst = max(abs(end_lo - D1), abs(end_hi - D1)) * 100
    blockers = []
    dt = [centers[i + 1] - centers[i] for i in range(3)]
    mean = sum(dt) / 3
    if any(abs(x / mean - 1) > Decimal("0.05") for x in dt):
        blockers.append("unequally_spaced_acquisitions")
    for key, maxspread in (("temperature_c", Decimal(1)), ("gap_mm", Decimal("0.1")),
                           ("offset_mm", Decimal("0.1"))):
        vals = [num(r[key]) for r in rows]
        if key != "temperature_c" and min(vals) < 0:
            raise ValueError("negative physical distance")
        if max(vals) - min(vals) > maxspread:
            blockers.append("unstable_" + key)
    loads = [num(r["load_ohm"]) for r in rows]
    if min(loads) <= 0:
        raise ValueError("non-positive test load")
    if (max(loads) - min(loads)) / min(loads) * 100 > Decimal("0.5"):
        blockers.append("unstable_load")
    if residual_worst > Decimal(3):
        blockers.append("center_ABBA_curvature_or_transient")
    if endpoint_worst > Decimal(2):
        blockers.append("endpoint_drift")
    flags = ("independently_verified_conditions", "gain_stability_verified",
             "offsets_traceable", "instrument_and_clock_verified")
    if any(any(type(r.get(f)) is not bool for f in flags) for r in rows):
        raise ValueError("traceability flags must be genuine booleans")
    if source == "BENCH_MEASURED" and not all(all(r[f] for f in flags) for r in rows):
        blockers.append("missing_independent_calibration_or_conditions")
    return {
        "milestone": "W-IND-56",
        "source_kind": source,
        "passage_count": 4,
        "meter_switches": 2,
        "eta_abba_percent": str(eta * 100),
        "conditional_eta_interval_percent": [str(eta_lo * 100), str(eta_hi * 100)],
        "center_residual_rho": str(rho),
        "center_residual_worst_percent": str(residual_worst),
        "endpoint_drift_worst_percent": str(endpoint_worst),
        "blockers": blockers,
        "candidate_for_external_metrology_review": source == "BENCH_MEASURED" and not blockers,
        "remaining_blind_spots": ["same_anomaly_in_both_middle_passages", "gain_or_offset_changes",
                                  "non_loglinear_or_correlated_drift", "self_reported_calibration_flags"],
        "physical_measurements": 0 if source == "SYNTHETIC" else "self_reported_not_validated",
        "added_robots_parts_eur": "0",
        "hardware_approved": False,
        "energization_approved": False,
        "lithium_dock_approved": False,
        "local_cutoff_qualified": False,
    }


def example():
    # Fiction: true Pin=1000mW, Pout=800mW, meters A=1.1 and B=0.9 gains.
    common = dict(fixture_id="synthetic-fixture", u_pin_mw="0.1", u_pout_mw="0.1",
                  temperature_c="25", gap_mm="2", offset_mm="0", load_ohm="20",
                  source_kind="SYNTHETIC", independently_verified_conditions=False,
                  gain_stability_verified=False, offsets_traceable=False,
                  instrument_and_clock_verified=False)
    return [dict(common, run_id=f"r{i}", trace_id=f"t{i}", in_meter=role[0],
                 out_meter=role[1], start_ms=i * 200, end_ms=i * 200 + 100,
                 pin_mw=pin, pout_mw=pout)
            for i, (role, pin, pout) in enumerate(zip(ROLES,
                ("1100", "900", "900", "1100"), ("720", "880", "880", "720")))]


def main():
    parser = argparse.ArgumentParser(description="Synthetic ABBA meter screening: never authorizes hardware")
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--out")
    args = parser.parse_args()
    if not args.demo:
        parser.error("only --demo supported; no direct hardware interface")
    data = evaluate(example())
    output = json.dumps(data, indent=2, sort_keys=True) + "\n"
    if args.out:
        from pathlib import Path
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
