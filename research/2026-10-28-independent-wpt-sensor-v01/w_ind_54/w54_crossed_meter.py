"""W-IND-54: synthetic crossed-meter WPT efficiency de-bias (NO I/O).

Original VALDO W-only educational metrology code. Neither validates hardware
nor replaces reference calibration, isolation, FOD, overtemperature, or cutoff.
"""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import argparse
import json


def d(x):
    try:
        z = Decimal(str(x))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError("invalid finite numeric evidence") from exc
    if not z.is_finite():
        raise ValueError("invalid finite numeric evidence")
    return z


@dataclass(frozen=True)
class Run:
    run_id: str
    meter_in: str
    meter_out: str
    pin_mw: str
    pout_mw: str
    bound_in_mw: str
    bound_out_mw: str
    temperature_c: str
    gap_mm: str
    lateral_offset_mm: str
    load_ohm: str
    start_ms: int
    end_ms: int
    trace_id: str
    fixture_id: str
    source_kind: str = "SYNTHETIC"
    independently_verified_conditions: bool = False
    gain_stability_verified: bool = False
    offsets_traceable: bool = False
    instrument_and_clock_verified: bool = False


def evaluate(ab: Run, ba: Run) -> dict:
    """A on input/B on output then B on input/A on output.

    With *constant multiplicative* instrument gains and identical true
    efficiencies: sqrt(eta_AB * eta_BA) cancels their gain ratio.
    Additive errors are bounded separately. Different true efficiencies
    yield their geometric mean, NOT either run's true efficiency.
    """
    if not (ab.run_id and ba.run_id and ab.run_id != ba.run_id):
        raise ValueError("two distinct run IDs required")
    if not (ab.trace_id and ba.trace_id and ab.trace_id != ba.trace_id):
        raise ValueError("two distinct raw traces required")
    if not (ab.fixture_id and ab.fixture_id == ba.fixture_id):
        raise ValueError("same identified test fixture required")
    if not (ab.meter_in and ab.meter_out and ab.meter_in != ab.meter_out
            and ba.meter_in == ab.meter_out and ba.meter_out == ab.meter_in):
        raise ValueError("two independent meters must exchange places")
    if not all(type(v) is int and v >= 0 for v in
               (ab.start_ms, ab.end_ms, ba.start_ms, ba.end_ms)):
        raise ValueError("timestamps must be integer monotonic milliseconds")
    if not (ab.start_ms < ab.end_ms <= ba.start_ms < ba.end_ms):
        raise ValueError("ordered nonoverlapping runs required")
    if ab.source_kind not in ("SYNTHETIC", "BENCH_MEASURED") or ba.source_kind != ab.source_kind:
        raise ValueError("evidence source types must match")

    p = []
    for r in (ab, ba):
        pin, pout, uin, uout = map(d, (r.pin_mw, r.pout_mw, r.bound_in_mw, r.bound_out_mw))
        if not (pin > uin >= 0 and pout > uout >= 0):
            raise ValueError("power/sign/offset uncertainty invalid")
        if (pout + uout) / (pin - uin) >= 1:
            raise ValueError("individual ratio at or above unity: unqualified")
        lo = (pout - uout) / (pin + uin)
        hi = (pout + uout) / (pin - uin)
        p.append((pout / pin, lo, hi))

    temp = [d(r.temperature_c) for r in (ab, ba)]
    gap = [d(r.gap_mm) for r in (ab, ba)]
    offset = [d(r.lateral_offset_mm) for r in (ab, ba)]
    load = [d(r.load_ohm) for r in (ab, ba)]
    if not all(d(-10) <= x <= d(80) for x in temp):
        raise ValueError("unqualified ambient temperature")
    if not all(x >= 0 for x in gap + offset) or not all(x > 0 for x in load):
        raise ValueError("invalid geometry or load")

    # These are screening ASSUMPTIONS, not qualified tolerances.
    limits = {
        "temperature_delta_c": d("1.0"),
        "gap_delta_mm": d("0.1"),
        "lateral_offset_delta_mm": d("0.1"),
        "load_difference_percent": d("0.5"),
    }
    variation = {
        "temperature_delta_c": abs(temp[0] - temp[1]),
        "gap_delta_mm": abs(gap[0] - gap[1]),
        "lateral_offset_delta_mm": abs(offset[0] - offset[1]),
        "load_difference_percent": abs(load[0] - load[1]) / min(load) * 100,
    }
    reasons = [k + " above hypothetical repeatability threshold"
               for k, v in variation.items() if v > limits[k]]
    if ab.source_kind != "BENCH_MEASURED":
        reasons.append("synthetic fixture is not measurement")
    for flag in ("independently_verified_conditions", "gain_stability_verified",
                 "offsets_traceable", "instrument_and_clock_verified"):
        if not (getattr(ab, flag) and getattr(ba, flag)):
            reasons.append(flag + " missing")
    eta = (p[0][0] * p[1][0]).sqrt()
    eta_lo = (p[0][1] * p[1][1]).sqrt()
    eta_hi = (p[0][2] * p[1][2]).sqrt()
    return {
        "method": "crossed_meter_geometric_mean_conditional",
        "source_kind": ab.source_kind,
        "eta_ab_percent": str(p[0][0] * 100),
        "eta_ba_percent": str(p[1][0] * 100),
        "eta_cross_percent": str(eta * 100),
        "conditional_interval_percent": [str(eta_lo * 100), str(eta_hi * 100)],
        "hypothetical_repeatability_limits": {k: str(v) for k, v in limits.items()},
        "observed_deltas": {k: str(v) for k, v in variation.items()},
        "candidate_for_metrology_review": not reasons,
        "blockers": reasons,
        "hardware_approved": False,
        "wpt_energization_approved": False,
        "lithium_dock_approved": False,
        "safety_cutoff_or_fod_proven": False,
        "claim": ("gain-ratio cancellation only if gains remain constant; "
                  "different true efficiencies produce geometric mean; "
                  "offsets and condition stability still need external proof"),
    }


def demo():
    # True Pin=1000 mW, true Pout=800 mW, gains A=1.10 and B=0.90.
    # Naive readings differ sharply, crossed result is exactly 80%.
    common = dict(bound_in_mw="2", bound_out_mw="2",
                  temperature_c="25", gap_mm="2", lateral_offset_mm="0",
                  load_ohm="20", fixture_id="FICTITIOUS-1",
                  source_kind="SYNTHETIC")
    ab = Run("AB", "METER-A", "METER-B", "1100", "720",
             start_ms=0, end_ms=1000, trace_id="SYNTH-A", **common)
    ba = Run("BA", "METER-B", "METER-A", "900", "880",
             start_ms=2000, end_ms=3000, trace_id="SYNTH-B", **common)
    result = evaluate(ab, ba)
    result.update({
        "physical_bench_measurements": 0,
        "cost_per_finished_robot_eur": "0",
        "added_meter_count": 0,
        "purchase_authorized": False,
        "battery_bms_dock_disconnected": True,
    })
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--out", default="-")
    args = parser.parse_args()
    if not args.demo:
        parser.error("NO hardware/real-data mode; --demo only")
    s = json.dumps(demo(), indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.out == "-":
        print(s, end="")
    else:
        from pathlib import Path
        Path(args.out).write_text(s, encoding="utf-8")


if __name__ == "__main__":
    main()
