"""W-IND-55: three-pass A/B -> B/A -> A/B meter drift screening.

Original VALDO W-only synthetic metrology model; NO hardware interfaces.
Provides an estimate *conditional* on stable gains and physical test state.
Does not replace calibration, FOD, thermal protection, local cutoffs or EMI tests.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import argparse
import json


def dec(value: object) -> Decimal:
    try:
        d = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError("non-numeric evidence") from exc
    if not d.is_finite():
        raise ValueError("non-finite evidence")
    return d


@dataclass(frozen=True)
class Passage:
    run_id: str
    trace_id: str
    fixture_id: str
    in_meter: str
    out_meter: str
    start_ms: int
    end_ms: int
    pin_mw: str
    pout_mw: str
    u_pin_mw: str
    u_pout_mw: str
    temperature_c: str
    gap_mm: str
    offset_mm: str
    load_ohm: str
    source_kind: str = "SYNTHETIC"
    independently_verified_conditions: bool = False
    gain_stability_verified: bool = False
    offsets_traceable: bool = False
    instrument_and_clock_verified: bool = False


LIMITS = {
    "temperature_spread_c": dec("1.0"),
    "gap_spread_mm": dec("0.1"),
    "offset_spread_mm": dec("0.1"),
    "load_spread_percent": dec("0.5"),
    "endpoint_drift_worst_percent": dec("2.0"),
    "time_center_skew_fraction": dec("0.05"),
}


def evaluate(runs: tuple[Passage, Passage, Passage]) -> dict:
    """A-B-A estimator: (R_AB0 * R_AB2)**(1/4) * R_BA1**(1/2).

    For fixed per-instrument multiplicative gains and true efficiency eta,
    this cancels relative gain. Linear drift in log(eta) with equally-spaced
    run centers yields the true *midpoint* efficiency, NOT any guarantee of
    stable load/temperature. Endpoint comparison catches large drift but NOT
    interior-only transients or correlated gain changes.
    """
    if type(runs) is not tuple or len(runs) != 3 or any(not isinstance(r, Passage) for r in runs):
        raise ValueError("exactly three Passage items required")
    a, b, c = runs
    if any(not r.run_id or not r.trace_id or not r.fixture_id for r in runs):
        raise ValueError("nonempty identifiers required")
    if len({r.run_id for r in runs}) != 3 or len({r.trace_id for r in runs}) != 3:
        raise ValueError("run and trace IDs must be unique; no replay")
    if len({r.fixture_id for r in runs}) != 1:
        raise ValueError("test fixture must remain identical")
    if not a.in_meter or not a.out_meter or a.in_meter == a.out_meter:
        raise ValueError("two distinct instruments required")
    if (b.in_meter, b.out_meter) != (a.out_meter, a.in_meter) or (c.in_meter, c.out_meter) != (a.in_meter, a.out_meter):
        raise ValueError("exact A-B-A meter assignment required")
    if any(type(getattr(r, x)) is not int or getattr(r, x) < 0 for r in runs for x in ("start_ms", "end_ms")):
        raise ValueError("integer nonnegative monotonic timestamp required")
    if not (a.start_ms < a.end_ms <= b.start_ms < b.end_ms <= c.start_ms < c.end_ms):
        raise ValueError("strict temporal order without overlapping readings")
    if len({r.source_kind for r in runs}) != 1 or a.source_kind not in ("SYNTHETIC", "BENCH_MEASURED"):
        raise ValueError("evidence type must be consistent and supported")

    mids2 = [r.start_ms + r.end_ms for r in runs]  # twice the midpoint, exactly
    d01 = mids2[1] - mids2[0]
    d12 = mids2[2] - mids2[1]
    if not (d01 > 0 and d12 > 0):
        raise ValueError("run centers out of order")
    center_skew_fraction = dec(abs(d01 - d12)) / dec(min(d01, d12))

    ratios = []
    intervals = []
    for r in runs:
        pin, pout, uin, uout = (dec(v) for v in (r.pin_mw, r.pout_mw, r.u_pin_mw, r.u_pout_mw))
        if not (pin > uin >= 0 and pout > uout >= 0):
            raise ValueError("invalid power or uncertainty")
        ratio = pout / pin
        lo = (pout - uout) / (pin + uin)
        hi = (pout + uout) / (pin - uin)
        if not (0 < lo <= ratio <= hi < 1):
            raise ValueError("apparent energy gain or unbounded ratio: quarantine")
        ratios.append(ratio)
        intervals.append((lo, hi))

    # 4th root via two Decimal.sqrt operations; conservative interval products.
    estimate = ((ratios[0] * ratios[2]).sqrt() * ratios[1]).sqrt()
    low = ((intervals[0][0] * intervals[2][0]).sqrt() * intervals[1][0]).sqrt()
    high = ((intervals[0][1] * intervals[2][1]).sqrt() * intervals[1][1]).sqrt()

    # Same orientation at endpoints -> its instrument ratio cancels.
    endpoint_ratio = ratios[2] / ratios[0]
    end_lo = intervals[2][0] / intervals[0][1]
    end_hi = intervals[2][1] / intervals[0][0]
    drift_nominal = abs(endpoint_ratio - 1) * 100
    drift_worst = max(abs(end_lo - 1), abs(end_hi - 1)) * 100

    numeric = {}
    for col, label in (("temperature_c", "temperature_spread_c"),
                       ("gap_mm", "gap_spread_mm"),
                       ("offset_mm", "offset_spread_mm"),
                       ("load_ohm", "load_spread_percent")):
        values = [dec(getattr(r, col)) for r in runs]
        if col == "temperature_c":
            if not all(dec("-10") <= v <= dec("80") for v in values):
                raise ValueError("unqualified temperature range")
        elif col == "load_ohm":
            if not all(v > 0 for v in values):
                raise ValueError("nonpositive load")
        elif not all(v >= 0 for v in values):
            raise ValueError("negative physical displacement")
        numeric[label] = ((max(values) - min(values)) / min(values) * 100
                          if col == "load_ohm" else max(values) - min(values))
    numeric["endpoint_drift_worst_percent"] = drift_worst
    numeric["time_center_skew_fraction"] = center_skew_fraction

    blockers = [f"{name}: exceeds synthetic screening threshold"
                for name, value in numeric.items() if value > LIMITS[name]]
    if a.source_kind == "SYNTHETIC":
        blockers.append("synthetic data: no physical measurement")
    for key in ("independently_verified_conditions", "gain_stability_verified",
                "offsets_traceable", "instrument_and_clock_verified"):
        if not all(getattr(r, key) is True for r in runs):
            blockers.append(f"{key} not established externally")

    return {
        "method": "aba_three_pass_gain_ratio_cancellation_and_endpoint_drift_screen",
        "source_kind": a.source_kind,
        "passage_count": 3,
        "eta_aba_percent": str(100 * estimate),
        "conditional_interval_percent": [str(100 * low), str(100 * high)],
        "apparent_passage_percent": [str(x * 100) for x in ratios],
        "endpoint_drift_nominal_percent": str(drift_nominal),
        "endpoint_drift_worst_percent": str(drift_worst),
        "center_skew_fraction": str(center_skew_fraction),
        "observed_spread": {k: str(v) for k, v in numeric.items()},
        "hypothetical_limits": {k: str(v) for k, v in LIMITS.items()},
        "candidate_for_external_metrology_review": not blockers,
        "blockers": blockers,
        "unobservable_risks": [
            "midpoint-only power/efficiency transient can escape endpoint check",
            "meter gain may drift with position, current, temperature or reconnection",
            "self-declared source and flags do not authenticate measurements",
            "measurement of power does not establish foreign-object detection",
        ],
        "hardware_approved": False,
        "energization_approved": False,
        "lithium_dock_approved": False,
        "local_cutoff_qualified": False,
        "added_robots_parts_eur": "0",
        "physical_measurements": 0,
    }


def demo() -> dict:
    common = dict(fixture_id="SYNTHETIC-FIXTURE", u_pin_mw="2", u_pout_mw="2",
                  temperature_c="25", gap_mm="2", offset_mm="0", load_ohm="20")
    runs = (
        Passage("AB-1", "trace-1", in_meter="A", out_meter="B", start_ms=0, end_ms=100,
                pin_mw="1100", pout_mw="720", **common),
        Passage("BA-2", "trace-2", in_meter="B", out_meter="A", start_ms=200, end_ms=300,
                pin_mw="900", pout_mw="880", **common),
        Passage("AB-3", "trace-3", in_meter="A", out_meter="B", start_ms=400, end_ms=500,
                pin_mw="1100", pout_mw="720", **common),
    )
    return evaluate(runs)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", required=True)
    parser.add_argument("--out", default="-")
    args = parser.parse_args()
    output = json.dumps(demo(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out == "-":
        print(output, end="")
    else:
        from pathlib import Path
        Path(args.out).write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
