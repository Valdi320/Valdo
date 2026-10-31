#!/usr/bin/env python3
"""W76: integrate synthetic or reported TX/RX cycle energy; NEVER approve hardware.

Original research tool. No batteries, motors, electronics, or RF are controlled.
"""
import argparse
import json
import math
from pathlib import Path


def finite_number(v, key, *, zero_ok=False):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError(f"{key} must be finite numeric, not bool")
    if v < 0 or (v == 0 and not zero_ok):
        raise ValueError(f"{key} must be {'nonnegative' if zero_ok else 'positive'}")
    return float(v)


def evaluate(payload):
    if not isinstance(payload, dict):
        raise ValueError("expected a JSON object")
    min_rx = finite_number(payload.get("sensor_continuous_mw"), "sensor_continuous_mw")
    allowance = finite_number(payload.get("max_extra_wh_day"), "max_extra_wh_day", zero_ok=True)
    duration = finite_number(payload.get("cycle_seconds"), "cycle_seconds")
    phases = payload.get("phases")
    if not isinstance(phases, list) or not phases:
        raise ValueError("phases must be a nonempty list")
    times, inputs, upper_inputs, outputs, lower_outputs, origins = [], [], [], [], [], []
    names = set()
    for index, phase in enumerate(phases):
        if not isinstance(phase, dict):
            raise ValueError(f"phase {index} must be an object")
        name = phase.get("name")
        if not isinstance(name, str) or not name.strip() or name in names:
            raise ValueError("phase names must be nonempty and unique")
        names.add(name)
        t = finite_number(phase.get("seconds"), f"{name}.seconds")
        pin = finite_number(phase.get("tx_input_mw"), f"{name}.tx_input_mw", zero_ok=True)
        pout = finite_number(phase.get("rx_output_mw"), f"{name}.rx_output_mw", zero_ok=True)
        uncertainty = finite_number(phase.get("relative_error_pct"), f"{name}.relative_error_pct", zero_ok=True)
        if uncertainty >= 100:
            raise ValueError("measurement relative error must be less than 100 percent")
        if pout > pin:
            raise ValueError("RX output cannot exceed TX input in this simplified model")
        kind = phase.get("source_kind")
        if kind not in ("synthetic", "bench_measured"):
            raise ValueError("phase source_kind must be synthetic or bench_measured")
        times.append(t)
        inputs.append(pin)
        upper_inputs.append(pin * (1 + uncertainty / 100))
        outputs.append(pout)
        lower_outputs.append(pout * (1 - uncertainty / 100))
        origins.append(kind)
    if not math.isclose(math.fsum(times), duration, rel_tol=1e-12, abs_tol=1e-9):
        raise ValueError("phase durations do not cover modeled cycle: do not extrapolate")
    mean_tx = math.fsum(t * p for t, p in zip(times, inputs)) / duration
    mean_upper = math.fsum(t * p for t, p in zip(times, upper_inputs)) / duration
    mean_rx = math.fsum(t * p for t, p in zip(times, outputs)) / duration
    min_guaranteed_rx = min(lower_outputs)
    excess = (mean_tx - min_rx) * 24 / 1000
    worst_excess = (mean_upper - min_rx) * 24 / 1000
    budget_tx = min_rx + allowance * 1000 / 24
    if not all(math.isfinite(x) for x in (mean_tx, mean_upper, mean_rx, min_guaranteed_rx, excess, worst_excess, budget_tx)):
        raise ValueError("cycle arithmetic overflow")
    blockers = []
    if min_guaranteed_rx + 1e-12 < min_rx:
        blockers.append("RX_PHASE_MEAN_BELOW_TARGET")
    if worst_excess > allowance + 1e-12:
        blockers.append("ENERGY_BUDGET_EXCEEDED")
    if any(k != "bench_measured" for k in origins):
        blockers.append("NO_COMPLETE_BENCH_MEASURED_CYCLE")
    if payload.get("cycle_representative") is not True:
        blockers.append("CYCLE_REPRESENTATIVENESS_UNVERIFIED")
    return {
        "status": "BLOCKED" if blockers else "DIGITAL_BUDGET_SCREEN_ONLY",
        "blockers": sorted(blockers),
        "tx_mean_mw": round(mean_tx, 9),
        "tx_conservative_upper_mean_mw": round(mean_upper, 9),
        "rx_mean_mw": round(mean_rx, 9),
        "rx_min_phase_mean_lower_bound_mw": round(min_guaranteed_rx, 9),
        "max_tx_mean_mw_for_budget": round(budget_tx, 9),
        "extra_wh_day_nominal": round(excess, 9),
        "extra_wh_day_conservative": round(worst_excess, 9),
        "assumed_cycle_seconds": duration,
        "all_phases_labeled_bench_measured": all(k == "bench_measured" for k in origins),
        "hardware_approved": False,
        "safety_tests_completed_by_model": False,
        "evidence_scope": "cycle-energy mathematical screen only; phase means do not prove instantaneous sensor continuity",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    a = parser.parse_args()
    bad_constant = lambda x: (_ for _ in ()).throw(ValueError(f"invalid JSON number {x}"))
    doc = json.loads(Path(a.input).read_text(encoding="utf-8"), parse_constant=bad_constant)
    out = evaluate(doc)
    Path(a.output).write_text(json.dumps(out, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
