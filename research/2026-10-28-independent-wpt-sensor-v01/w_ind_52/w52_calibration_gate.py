"""W-IND-52: fail-closed, offline INA219 shunt calibration screening.

No hardware I/O. A digital PASS never authorizes energizing a circuit.
The explicit validation point at 80 mA is not reused to fit the zero/span model.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from datetime import date
from decimal import Decimal, InvalidOperation
import argparse
import json
from pathlib import Path


def D(value) -> Decimal:
    try:
        d = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError("invalid numeric input") from exc
    if not d.is_finite():
        raise ValueError("NaN/Infinity are not calibration evidence")
    return d


@dataclass(frozen=True)
class Channel:
    position: str
    meter_id: str
    shunt_id: str
    reference_id: str
    calibration_valid_from: str
    calibration_valid_until: str
    as_of: str
    source_kind: str
    zero_uv: int
    check_uv: int
    span_uv: int
    check_reference_ma: str
    span_reference_ma: str
    check_reference_uncertainty_ma: str
    span_reference_uncertainty_ma: str
    cal_temperature_c: str
    use_temperature_c: str
    shunt_tcr_ppm_per_c: str | None
    chip_gain_drift_ppm_per_c: str | None
    chip_offset_drift_uv_per_c: str | None
    reference_traceable: bool = False
    reference_burden_qualified: bool = False
    chip_grade_verified: bool = False
    shunt_identity_verified: bool = False
    zero_current_verified: bool = False
    temperature_measured: bool = False
    max_error_percent: str = "3"
    max_temperature_delta_c: str = "5"
    shunt_fsr_uv: int = 40000
    raw_half_lsb_uv: int = 5
    device_offset_limit_uv: int = 50


def screen_channel(c: Channel) -> dict:
    if c.position not in ("TX", "RX"):
        raise ValueError("must identify TX or RX")
    if not all((c.meter_id.strip(), c.shunt_id.strip(), c.reference_id.strip())):
        raise ValueError("meter, shunt and independent reference IDs required")
    if c.source_kind not in ("SYNTHETIC", "BENCH_MEASURED"):
        raise ValueError("unknown evidence kind")
    if not all(isinstance(x, int) and not isinstance(x, bool) for x in
               (c.zero_uv, c.check_uv, c.span_uv, c.shunt_fsr_uv, c.raw_half_lsb_uv, c.device_offset_limit_uv)):
        raise ValueError("raw INA219 units must be integral microvolts")
    if c.raw_half_lsb_uv != 5 or c.shunt_fsr_uv <= 0 or c.device_offset_limit_uv <= 0:
        raise ValueError("unqualified quantization/range")
    if any(v % 10 for v in (c.zero_uv, c.check_uv, c.span_uv)):
        raise ValueError("INA219 raw shunt LSB must be 10 uV")
    if not (c.zero_uv < c.check_uv < c.span_uv <= c.shunt_fsr_uv):
        raise ValueError("reversed, saturated or unordered calibration points")
    vals = [D(v) for v in (c.check_reference_ma, c.span_reference_ma,
            c.check_reference_uncertainty_ma, c.span_reference_uncertainty_ma,
            c.cal_temperature_c, c.use_temperature_c,
            c.max_error_percent, c.max_temperature_delta_c)]
    lo, hi, ue_lo, ue_hi, tcal, tuse, max_error, max_dt = vals
    if not (D(0) < ue_lo < lo < hi and D(0) < ue_hi < hi and max_error > 0 and max_dt >= 0):
        raise ValueError("invalid references, uncertainty, or limits")
    start, expiry, today = map(date.fromisoformat, (c.calibration_valid_from,
                                                     c.calibration_valid_until, c.as_of))
    if start > expiry:
        raise ValueError("reference validity dates are reversed")
    reasons = []
    if not (start <= today <= expiry):
        reasons.append("reference calibration not valid on as_of date")
    if c.source_kind != "BENCH_MEASURED":
        reasons.append("synthetic input cannot qualify a real meter")
    for prop, msg in (("reference_traceable", "reference uncertainty not traceable"),
                      ("reference_burden_qualified", "reference burden not qualified"),
                      ("chip_grade_verified", "physical INA219 grade unknown"),
                      ("shunt_identity_verified", "shunt identity/TCR unverified"),
                      ("zero_current_verified", "zero-current state not independently verified"),
                      ("temperature_measured", "temperature is not measured")):
        if not getattr(c, prop):
            reasons.append(msg)
    if abs(c.zero_uv) > c.device_offset_limit_uv + c.raw_half_lsb_uv:
        reasons.append("zero reading exceeds conditional device offset bound")
    dt = abs(tuse - tcal)
    if dt > max_dt:
        reasons.append("measurement temperature outside calibration window")
    drift_values = (c.shunt_tcr_ppm_per_c, c.chip_gain_drift_ppm_per_c,
                    c.chip_offset_drift_uv_per_c)
    if any(x is None for x in drift_values):
        reasons.append("temperature drift parameters missing")
        drift = None
    else:
        tcr, gain, offset_drift = map(D, drift_values)
        if min(tcr, gain, offset_drift) < 0:
            raise ValueError("negative drift bound")
        drift = (tcr, gain, offset_drift)

    z, v, h, q = map(D, (c.zero_uv, c.check_uv, c.span_uv, c.raw_half_lsb_uv))
    span_min = (h - q) - (z + q)
    span_max = (h + q) - (z - q)
    check_min = (v - q) - (z + q)
    check_max = (v + q) - (z - q)
    if span_min <= 0 or check_min <= 0:
        raise ValueError("resolution insufficient for positive calibration")
    nominal_check = hi * (v - z) / (h - z)
    # Interval arithmetic: a deterministic conservative bound, NOT a confidence interval.
    predicted_min = (hi - ue_hi) * check_min / span_max
    predicted_max = (hi + ue_hi) * check_max / span_min
    if drift is not None:
        tcr, gain, offset_drift = drift
        extra = predicted_max * dt * (tcr + gain) / D(1000000)
        extra += hi * offset_drift * dt / span_min
        predicted_min -= extra
        predicted_max += extra
    else:
        extra = None
    if extra is not None:
        reference_min = lo - ue_lo
        reference_max = lo + ue_lo
        error = max(abs(predicted_max - reference_min), abs(reference_max - predicted_min))
        worst_percent = error * 100 / reference_min
        if worst_percent > max_error:
            reasons.append("holdout current mismatch exceeds error budget")
    else:
        worst_percent = None
    return {
        "position": c.position,
        "meter_id": c.meter_id,
        "shunt_id": c.shunt_id,
        "source_kind": c.source_kind,
        "nominal_check_ma": str(nominal_check),
        "holdout_reference_ma": str(lo),
        "conditional_worst_case_error_percent": str(worst_percent) if worst_percent is not None else None,
        "max_error_percent": str(max_error),
        "temperature_delta_c": str(dt),
        "pass_conditional_model": worst_percent is not None and worst_percent <= max_error,
        "bench_metrology_candidate": not reasons,
        "blockers": reasons,
        "hardware_approved": False,
        "lithium_or_dock_approved": False,
    }


def screen_pair(tx: Channel, rx: Channel) -> dict:
    if (tx.position, rx.position) != ("TX", "RX"):
        raise ValueError("TX and RX must have separate physical positions")
    if tx.meter_id == rx.meter_id or tx.shunt_id == rx.shunt_id:
        raise ValueError("a single physical shunt/meter cannot represent both rails")
    a, b = screen_channel(tx), screen_channel(rx)
    return {
        "evidence_kind": "SYNTHETIC-CALIBRATION-CONTRACT-NOT-HARDWARE",
        "tx": a, "rx": b,
        "both_current_channels_bench_candidates": a["bench_metrology_candidate"] and b["bench_metrology_candidate"],
        "efficiency_metrology_approved": False,
        "reason": "bus-voltage calibration, real clock alignment, temperature and RF/EMI tests remain separate",
        "independent_FOD_thermal_cutoff_approved": False,
        "hardware_approved": False,
        "battery_BMS_dock_disconnected": True,
    }


def demo() -> dict:
    base = Channel(position="TX", meter_id="TX-SYNTHETIC-001", shunt_id="TX-R-SYNTHETIC",
          reference_id="REFERENCE-SYNTHETIC", calibration_valid_from="2026-10-29",
          calibration_valid_until="2026-11-29", as_of="2026-10-30", source_kind="SYNTHETIC",
          zero_uv=20, check_uv=8020, span_uv=30020,
          check_reference_ma="80", span_reference_ma="300",
          check_reference_uncertainty_ma="0.2", span_reference_uncertainty_ma="0.2",
          cal_temperature_c="25", use_temperature_c="27",
          shunt_tcr_ppm_per_c="100", chip_gain_drift_ppm_per_c="167",
          chip_offset_drift_uv_per_c="0.5")
    tx = base
    rx = replace(base, position="RX", meter_id="RX-SYNTHETIC-002", shunt_id="RX-R-SYNTHETIC")
    bad_rx = replace(rx, check_uv=6420)
    out = screen_pair(tx, rx)
    out["bad_rx_holdout_example"] = screen_channel(bad_rx)
    out["model_inputs_are_fictitious"] = True
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--demo", action="store_true")
    p.add_argument("--out", default="-")
    args = p.parse_args()
    if not args.demo:
        p.error("--demo only; no I2C and no real metrology")
    data = json.dumps(demo(), ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.out == "-":
        print(data, end="")
    else:
        Path(args.out).write_text(data, encoding="utf-8")


if __name__ == "__main__":
    main()
