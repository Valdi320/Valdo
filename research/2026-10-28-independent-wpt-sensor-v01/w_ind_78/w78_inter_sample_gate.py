#!/usr/bin/env python3
"""W78: bounded-slew inter-sample RX voltage screen (digital only).

All bounds/provenance are caller assertions, NOT externally authenticated.
Never grants hardware approval, motor/battery control, or safe-stop authority.
"""
import argparse
import json
import math
from pathlib import Path


def finite(value, name, *, zero=False):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError(f"{name}: finite numeric, not boolean, required")
    if value < 0 or (not zero and value == 0):
        raise ValueError(f"{name}: {'nonnegative' if zero else 'positive'} required")
    return float(value)


def screen(doc):
    if not isinstance(doc, dict):
        raise ValueError("input must be a JSON object")
    threshold = finite(doc.get("rx_required_min_v"), "rx_required_min_v")
    uncertainty = finite(doc.get("voltage_uncertainty_v"), "voltage_uncertainty_v", zero=True)
    jitter = finite(doc.get("timestamp_uncertainty_s"), "timestamp_uncertainty_s", zero=True)
    slew = finite(doc.get("slew_bound_v_per_s"), "slew_bound_v_per_s", zero=True)
    max_gap = finite(doc.get("max_nominal_sample_gap_s"), "max_nominal_sample_gap_s")
    duration = finite(doc.get("capture_duration_s"), "capture_duration_s")
    source = doc.get("source_kind")
    if source not in ("synthetic", "bench_measured_claim"):
        raise ValueError("source_kind: unknown")
    evidence = doc.get("slew_bound_evidence")
    if evidence not in ("hypothesis", "independent_characterization_claim"):
        raise ValueError("slew_bound_evidence: unknown")
    samples = doc.get("samples")
    if not isinstance(samples, list) or len(samples) < 2:
        raise ValueError("samples: at least two required")
    if len(samples) > 100000:
        raise ValueError("samples: explicit size cap exceeded")
    values = []
    times = []
    for i, sample in enumerate(samples):
        if not isinstance(sample, dict):
            raise ValueError(f"sample {i}: object required")
        t = finite(sample.get("t_s"), f"sample {i}.t_s", zero=True)
        v = finite(sample.get("v_rx_v"), f"sample {i}.v_rx_v", zero=True)
        if t > duration:
            raise ValueError("sample outside capture")
        if times and t <= times[-1]:
            raise ValueError("sample times must strictly increase")
        values.append(v)
        times.append(t)
    # Exactly observed endpoints: no hidden pre/post sample interval may be inferred.
    if times[0] != 0.0 or times[-1] != duration:
        raise ValueError("unobserved capture boundary")
    conservative_intervals = []
    nominal_gaps = []
    effective_gaps = []
    for i in range(len(times) - 1):
        dt = times[i + 1] - times[i]
        nominal_gaps.append(dt)
        dt_upper = dt + 2 * jitter
        effective_gaps.append(dt_upper)
        a = values[i] - uncertainty
        b = values[i + 1] - uncertainty
        if not all(math.isfinite(x) for x in (dt_upper, a, b)):
            raise ValueError("numeric overflow")
        if abs(a - b) > slew * dt_upper + 1e-12:
            raise ValueError("claimed slew bound inconsistent with samples")
        # Tight lower bound for an S-Lipschitz signal between endpoints:
        # v(t) >= max(a - S*t, b - S*(dt_upper-t)).
        # Minimum of envelope: (a+b-S*dt_upper)/2.
        floor = (a + b - slew * dt_upper) / 2
        if not math.isfinite(floor):
            raise ValueError("numeric overflow")
        conservative_intervals.append(floor)
    floor = min(conservative_intervals)
    if not all(math.isfinite(x) for x in (floor, max(effective_gaps))):
        raise ValueError("numeric overflow")
    blockers = []
    if max(nominal_gaps) > max_gap + 1e-12:
        blockers.append("NOMINAL_SAMPLING_GAP_EXCEEDED")
    if floor < threshold - 1e-12:
        blockers.append("INTER_SAMPLE_VOLTAGE_MAY_FALL_BELOW_MIN")
    if evidence != "independent_characterization_claim":
        blockers.append("SLEW_BOUND_NOT_INDEPENDENTLY_CHARACTERIZED")
    if source != "bench_measured_claim":
        blockers.append("TRACE_NOT_BENCH_MEASURED")
    if jitter > max_gap / 2:
        blockers.append("TIMESTAMP_UNCERTAINTY_TOO_LARGE_FOR_GAP")
    return {
        "status": "BLOCKED" if blockers else "CONDITIONAL_DIGITAL_SCREEN_ONLY",
        "blockers": sorted(blockers),
        "samples": len(samples),
        "nominal_max_gap_s": round(max(nominal_gaps), 9),
        "conservative_max_gap_s": round(max(effective_gaps), 9),
        "lowest_observed_v": round(min(values), 9),
        "conditional_inter_sample_lower_v": round(floor, 9),
        "voltage_threshold_v": round(threshold, 9),
        "derivation": "Lipschitz bound, with endpoint voltage error and interval timestamp uncertainty; contingent on independently proven global slew bound",
        "source_kind": source,
        "slew_bound_evidence": evidence,
        "hardware_approved": False,
        "physical_measures_authenticated": False,
        "instantaneous_voltage_proven": False,
        "critical_stop_authorized": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    def reject_constant(token):
        raise ValueError(f"invalid non-finite JSON constant: {token}")
    doc = json.loads(Path(args.input).read_text(encoding="utf-8"), parse_constant=reject_constant)
    result = screen(doc)
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
