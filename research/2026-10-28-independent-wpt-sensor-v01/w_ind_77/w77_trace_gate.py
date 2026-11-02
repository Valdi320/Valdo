#!/usr/bin/env python3
"""W77: fail-closed mathematical screen of integrated TX energy and observed RX minima.

Does NOT acquire measurements, select hardware, or control safety-critical outputs.
Data provenance and acquisition quality are claims from the caller, NOT verified.
"""
import argparse
import json
import math
from pathlib import Path


def numeric(v, name, *, allow_zero=False):
    if type(v) not in (float, int) or not math.isfinite(v):
        raise ValueError(f"{name}: finite numeric required; booleans forbidden")
    if v < 0 or (v == 0 and not allow_zero):
        raise ValueError(f"{name}: {'nonnegative' if allow_zero else 'positive'} required")
    return float(v)


def positive_integer(v, name):
    if type(v) is not int or v < 1:
        raise ValueError(f"{name}: positive integer required")
    return v


def evaluate(record):
    if not isinstance(record, dict):
        raise ValueError("document must be object")
    cycle = numeric(record.get("cycle_seconds"), "cycle_seconds")
    sensor_mw = numeric(record.get("sensor_reference_mw"), "sensor_reference_mw")
    rx_min_v = numeric(record.get("rx_required_min_v"), "rx_required_min_v")
    allowed = numeric(record.get("max_extra_wh_day"), "max_extra_wh_day", allow_zero=True)
    allowed_gap = numeric(record.get("max_observation_gap_ms"), "max_observation_gap_ms")
    min_cycles = positive_integer(record.get("minimum_cycles_required"), "minimum_cycles_required")
    cycles = positive_integer(record.get("cycles_observed"), "cycles_observed")
    controls = record.get("acquisition_claims")
    required_controls = (
        "monotonic_clock", "simultaneous_tx_rx", "tx_meter_calibrated",
        "rx_meter_calibrated", "cycle_representative",
    )
    if not isinstance(controls, dict) or any(type(controls.get(k)) is not bool for k in required_controls):
        raise ValueError("acquisition_claims must contain exact booleans for all required flags")
    windows = record.get("windows")
    if not isinstance(windows, list) or not windows:
        raise ValueError("windows: nonempty list required")
    prev_end, energy, energy_upper = 0.0, [], []
    gaps, volts, classes, modes = [], [], [], []
    for idx, w in enumerate(windows):
        if not isinstance(w, dict):
            raise ValueError(f"window {idx}: object required")
        start = numeric(w.get("start_s"), f"window {idx}.start_s", allow_zero=True)
        end = numeric(w.get("end_s"), f"window {idx}.end_s")
        if end <= start or not math.isclose(start, prev_end, rel_tol=0, abs_tol=1e-9):
            raise ValueError(f"window {idx}: overlap, gap, reversed or unordered timestamps")
        if end > cycle + 1e-9:
            raise ValueError(f"window {idx}: outside declared cycle")
        e = numeric(w.get("tx_integrated_mj"), f"window {idx}.tx_integrated_mj", allow_zero=True)
        eu = numeric(w.get("tx_relative_uncertainty_pct"), f"window {idx}.tx_relative_uncertainty_pct", allow_zero=True)
        if eu >= 100:
            raise ValueError(f"window {idx}: uncertainty must be <100%")
        v = numeric(w.get("rx_observed_min_v"), f"window {idx}.rx_observed_min_v", allow_zero=True)
        vu = numeric(w.get("rx_voltage_uncertainty_v"), f"window {idx}.rx_voltage_uncertainty_v", allow_zero=True)
        gap = numeric(w.get("rx_max_sample_gap_ms"), f"window {idx}.rx_max_sample_gap_ms")
        if gap > (end - start) * 1000 + 1e-6:
            raise ValueError(f"window {idx}: RX sampling gap exceeds its window duration")
        src = w.get("source_kind")
        if src not in ("synthetic", "bench_measured"):
            raise ValueError(f"window {idx}: unsupported provenance")
        mode = w.get("tx_capture_mode")
        if mode not in ("energy_integrator", "point_samples"):
            raise ValueError(f"window {idx}: unsupported TX capture mode")
        energy.append(e)
        energy_upper.append(e * (1 + eu / 100))
        volts.append(v - vu)
        gaps.append(gap)
        classes.append(src)
        modes.append(mode)
        prev_end = end
    if not math.isclose(prev_end, cycle, rel_tol=0, abs_tol=1e-9):
        raise ValueError("time coverage incomplete; no extrapolation")
    try:
        tx_mw = math.fsum(energy) / cycle
        upper_mw = math.fsum(energy_upper) / cycle
        extra = (tx_mw - sensor_mw) * 24 / 1000
        extra_upper = (upper_mw - sensor_mw) * 24 / 1000
    except OverflowError as exc:
        raise ValueError("arithmetic overflow") from exc
    values = (tx_mw, upper_mw, extra, extra_upper, min(volts), max(gaps))
    if not all(math.isfinite(v) for v in values):
        raise ValueError("arithmetic overflow")
    blockers = []
    if min(volts) + 1e-12 < rx_min_v:
        blockers.append("OBSERVED_RX_VOLTAGE_BELOW_ILLUSTRATIVE_MIN")
    if max(gaps) > allowed_gap + 1e-12:
        blockers.append("RX_SAMPLING_GAP_EXCEEDS_SCREEN")
    if extra_upper > allowed + 1e-12:
        blockers.append("CONSERVATIVE_TX_ENERGY_BUDGET_EXCEEDED")
    if upper_mw + 1e-12 < sensor_mw:
        blockers.append("TX_INPUT_BELOW_SENSOR_BASELINE")
    if any(x != "energy_integrator" for x in modes):
        blockers.append("TX_POINT_SAMPLING_CAN_MISS_SPIKES")
    if any(x != "bench_measured" for x in classes):
        blockers.append("NOT_ALL_WINDOWS_BENCH_MEASURED")
    if cycles < min_cycles:
        blockers.append("TOO_FEW_CYCLES")
    for key in required_controls:
        if not controls[key]:
            blockers.append("UNVERIFIED_" + key.upper())
    return {
        "status": "BLOCKED" if blockers else "DIGITAL_ENERGY_AND_OBSERVED_VOLTAGE_SCREEN_ONLY",
        "blockers": sorted(blockers),
        "windows": len(windows),
        "coverage_seconds": round(prev_end, 9),
        "tx_mean_mw": round(tx_mw, 9),
        "tx_conservative_upper_mean_mw": round(upper_mw, 9),
        "extra_wh_day_nominal": round(extra, 9),
        "extra_wh_day_conservative": round(extra_upper, 9),
        "rx_observed_lower_voltage_v": round(min(volts), 9),
        "rx_max_observed_sample_gap_ms": round(max(gaps), 9),
        "hardware_approved": False,
        "safety_cuts_proven": False,
        "physical_measurements_verified_by_software": False,
        "instantaneous_continuity_proven": False,
        "scope": "reported integrated TX energy and observed RX minima only; intervals between observations remain unproven",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    def reject_constant(x):
        raise ValueError(f"nonfinite JSON constant {x}")
    data = json.loads(Path(args.input).read_text(encoding="utf-8"), parse_constant=reject_constant)
    result = evaluate(data)
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
