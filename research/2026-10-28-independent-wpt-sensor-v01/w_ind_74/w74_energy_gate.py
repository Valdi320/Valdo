#!/usr/bin/env python3
"""W74: source-independent, fail-closed energy/maintenance gate for a removable low-power sensor.

Only computes a transparent idealized budget; never certifies WPT safety or hardware.
Copyright (c) 2026 VALDO contributors. Original work, no third-party code copied.
"""
import argparse
import json
import math
from pathlib import Path

SCHEMA = "VALDO_W74_SENSOR_ENERGY_V1"


def number(obj, key, *, lo=0.0, hi=None, strict_lo=False):
    if key not in obj:
        raise ValueError(f"missing field {key}: cannot claim feasibility")
    val = obj[key]
    if isinstance(val, bool) or not isinstance(val, (int, float)):
        raise ValueError(f"{key} must be numeric, not a bool/string")
    if not math.isfinite(val) or val < lo or (strict_lo and val == lo) or (hi is not None and val > hi):
        raise ValueError(f"{key} outside allowed finite bounds")
    return float(val)


def exact_false(obj, key):
    if obj.get(key) is not False:
        raise ValueError(f"{key} must be explicitly false")


def audit(s):
    if not isinstance(s, dict) or s.get("schema") != SCHEMA:
        raise ValueError("schema mismatch")
    for section in ("sensor", "wpt", "wire", "criteria", "evidence"):
        if not isinstance(s.get(section), dict):
            raise ValueError(f"missing or invalid {section}")
    x, w, c, g, evidence = (s[k] for k in ("sensor", "wpt", "wire", "criteria", "evidence"))
    if x.get("function") != "noncritical_removable_sensor":
        raise ValueError("pilot must be a noncritical removable sensor, not an actuator")
    exact_false(x, "motor_or_pump")
    exact_false(x, "radio_for_critical_stop")
    exact_false(x, "battery_or_bms_connected")
    rail = number(x, "rail_V", lo=0.0, strict_lo=True)
    active = number(x, "active_W", lo=0.0, strict_lo=True)
    sleep = number(x, "sleep_W")
    if sleep > active:
        raise ValueError("sleep power greater than active power")
    duty = number(x, "active_fraction", hi=1.0)
    peak = number(x, "peak_W", lo=0.0, strict_lo=True)
    if peak < active:
        raise ValueError("peak power below active power")
    eta = number(w, "dc_efficiency_fraction", hi=1.0, strict_lo=True)
    overhead = number(w, "tx_fixed_overhead_W")
    rated_rx_peak = number(w, "rx_peak_rating_W", strict_lo=True)
    rated_tx_input = number(w, "tx_input_limit_W", strict_lo=True)
    rloop = number(c, "loop_resistance_ohm")
    wired_overhead = number(c, "fixed_overhead_W")
    extra_limit = number(g, "max_extra_Wh_per_day")
    thermal_limit = number(g, "max_peak_dissipation_W")
    drop_limit = number(g, "max_wired_drop_percent", hi=100)
    if evidence.get("source_kind") not in ("SYNTHETIC_HYPOTHESIS", "DATASHEET_UNVERIFIED", "BENCH_UNREVIEWED"):
        raise ValueError("provenance is unknown; fail closed")
    if evidence.get("physical_bench_authorized") is not False:
        raise ValueError("this model must not authorize physical tests")

    # Source-side power of a permanently energized hypothetical WPT transmitter.
    # 'dc_efficiency_fraction' is total load-dependent TX-input -> regulated RX rail efficiency,
    # excluding 'tx_fixed_overhead_W' to avoid double counting. Both NEED measurement.
    p_load = duty * active + (1 - duty) * sleep
    p_input_active = overhead + active / eta
    p_input_sleep = overhead + sleep / eta
    p_input_peak = overhead + peak / eta
    p_input_avg = duty * p_input_active + (1 - duty) * p_input_sleep
    p_loss_avg = p_input_avg - p_load
    p_loss_peak = p_input_peak - peak

    # Ideal constant regulated 3.3 V load, copper loop modeled as I^2 R only.
    # This is NOT a complete wired regulator efficiency model.
    wire_loss_active = (active / rail) ** 2 * rloop
    wire_loss_sleep = (sleep / rail) ** 2 * rloop
    p_wire_avg = p_load + duty * wire_loss_active + (1 - duty) * wire_loss_sleep + wired_overhead
    p_drop_percent = 100 * (peak / rail) * rloop / rail
    extra_wh_day = 24 * (p_input_avg - p_wire_avg)
    fixed_overhead_ceiling_w = extra_limit / 24 + p_wire_avg - p_load / eta
    failures = []
    if rated_rx_peak < peak:
        failures.append("RX_PEAK_RATING_INSUFFICIENT")
    if rated_tx_input < p_input_peak:
        failures.append("TX_PEAK_INPUT_LIMIT_INSUFFICIENT")
    if extra_wh_day > extra_limit:
        failures.append("WPT_EXCESS_DAILY_ENERGY")
    if fixed_overhead_ceiling_w < 0:
        failures.append("WPT_ZERO_OVERHEAD_STILL_EXCEEDS_ENERGY_BUDGET")
    if p_loss_peak > thermal_limit:
        failures.append("WPT_PEAK_DISSIPATION_HYPOTHESIS_EXCEEDED")
    if p_drop_percent > drop_limit:
        failures.append("WIRED_PEAK_DROP_HYPOTHESIS_EXCEEDED")
    # Criterion limits are investigation hypotheses, not certified safety limits.
    out = {
        "schema": SCHEMA,
        "source_kind": evidence["source_kind"],
        "model": "CONTINUOUS_TX_IDEAL_DC_PLUS_FIXED_OVERHEAD; WIRE_IDEAL_3V3_AND_I2R",
        "sensor_load_average_W": p_load,
        "wpt_transmitter_average_W": p_input_avg,
        "wpt_transmitter_peak_W": p_input_peak,
        "wpt_average_dissipation_W": p_loss_avg,
        "wpt_peak_dissipation_W": p_loss_peak,
        "wired_supply_average_W": p_wire_avg,
        "wired_peak_voltage_drop_percent": p_drop_percent,
        "wpt_daily_energy_Wh": 24 * p_input_avg,
        "wired_daily_energy_Wh": 24 * p_wire_avg,
        "wpt_extra_energy_Wh_per_day": extra_wh_day,
        "max_tx_fixed_overhead_W_for_daily_budget": fixed_overhead_ceiling_w,
        "wpt_to_wired_energy_ratio": p_input_avg / p_wire_avg,
        "failed_hypothetical_gates": failures,
        "decision": "NO_GO_UNDER_HYPOTHESES" if failures else "MODEL_ONLY_CONDITIONAL",
        "hardware_approved": False,
        "physical_tests_performed": False,
        "battery_or_bms_connected": False,
        "independent_review_required": [
            "actual TX idle/fixed dissipation and DC efficiency measured across load and offset",
            "real maximum output/peak load with startup and brownout",
            "FOD including metal and wet dustbin; temperature rise and drift",
            "hardware autonomous cutoff, independent overcurrent and thermal trip",
            "capacitor/inductor residual energy and reverse-feed routes",
            "EMI and RF coexistence; local ACK CRC sequence timeout privacy and recovery",
            "TX/RX alignment, gap, dust/water tolerance and module replacement cycles",
            "battery/BMS/charger remain unconnected; independent safe test authorization",
            "verified itemized parts and local Diotronic/TME/Mouser/DigiKey pricing with VAT/MOQ/stock",
        ],
    }
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(json.loads(args.input.read_text(encoding="utf-8")))
    data = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(data, encoding="utf-8")
    else:
        print(data, end="")


if __name__ == "__main__":
    main()
