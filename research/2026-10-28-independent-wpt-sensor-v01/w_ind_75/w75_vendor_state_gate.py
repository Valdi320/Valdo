#!/usr/bin/env python3
"""W75: reject standby-as-loaded assumptions for a removable low-power sensor.

Original, dependency-free digital screening only. Never approves hardware.
"""
import argparse
import json
import math
from pathlib import Path

SAFETY_GATES = (
    "fod", "thermal_cut", "independent_cut", "emi", "offset_scan",
    "reverse_current", "residual_discharge", "wetness",
)
RADIO_GATES = (
    "application_ack", "crc", "sequence", "timeout", "privacy", "local_fail_safe"
)


def positive(value, name, *, allow_zero=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}: expected numeric value")
    if not math.isfinite(value) or (value < 0 if allow_zero else value <= 0):
        raise ValueError(f"{name}: outside valid finite range")
    return float(value)


def screen(record):
    if not isinstance(record, dict):
        raise ValueError("record must be an object")
    for key in ("module_kind", "vendor", "lifecycle", "sensor_mean_mw", "max_extra_wh_day", "standby", "loaded", "safety", "radio"):
        if key not in record:
            raise ValueError(f"missing {key}")
    sensor = positive(record["sensor_mean_mw"], "sensor_mean_mw")
    allowance = positive(record["max_extra_wh_day"], "max_extra_wh_day", allow_zero=True)
    if not isinstance(record["vendor"], str) or not record["vendor"].strip():
        raise ValueError("vendor empty")
    s = record["standby"]
    if not isinstance(s, dict) or s.get("condition") != "no_receiver":
        raise ValueError("standby condition must explicitly be no_receiver")
    if s.get("source_kind") != "manufacturer_claim" or not isinstance(s.get("source_url"), str) or not s["source_url"].startswith("https://"):
        raise ValueError("standby claim requires identified original manufacturer source")
    p_standby = positive(s.get("voltage_v"), "standby.voltage_v") * positive(s.get("current_ma"), "standby.current_ma", allow_zero=True)
    if not isinstance(record["safety"], dict) or not isinstance(record["radio"], dict) or not isinstance(record["loaded"], dict):
        raise ValueError("loaded/safety/radio must be objects")
    blockers = []
    if record["module_kind"] != "noncritical_readonly_sensor":
        blockers.append("NOT_A_NONCRITICAL_SENSOR")
    for forbidden in ("battery_or_bms_connected", "motor_or_pump", "critical_radio_stop"):
        if record.get(forbidden) is not False:
            blockers.append("FORBIDDEN_" + forbidden.upper())
    if record["lifecycle"] != "active":
        blockers.append("LIFECYCLE_NOT_ACTIVE")
    if any(record["safety"].get(g) != "bench_measured" for g in SAFETY_GATES):
        blockers.append("SAFETY_GATES_UNVERIFIED")
    if any(record["radio"].get(g) is not True for g in RADIO_GATES):
        blockers.append("RADIO_APP_GATES_UNVERIFIED")
    loaded = record["loaded"]
    loaded_input = loaded.get("tx_input_mw")
    loaded_output = loaded.get("rx_output_mw")
    measured_extra = None
    efficiency = None
    energy_input_wh_day = None
    if loaded_input is None or loaded_output is None:
        blockers.append("LOADED_POWER_UNKNOWN")
    else:
        pin = positive(loaded_input, "loaded.tx_input_mw")
        pout = positive(loaded_output, "loaded.rx_output_mw")
        if pout > pin:
            raise ValueError("measured RX output exceeds TX input")
        if loaded.get("source_kind") != "bench_measured":
            blockers.append("LOADED_POWER_NOT_BENCH_MEASURED")
        if any(loaded.get(k) is None for k in ("gap_mm", "offset_mm", "coil_temp_c")):
            blockers.append("OPERATING_GEOMETRY_TEMP_UNKNOWN")
        else:
            positive(loaded["gap_mm"], "loaded.gap_mm", allow_zero=True)
            positive(loaded["offset_mm"], "loaded.offset_mm", allow_zero=True)
            positive(loaded["coil_temp_c"], "loaded.coil_temp_c", allow_zero=True)
        if abs(pout - sensor) > 0.05 * sensor:
            blockers.append("MEASURED_LOAD_NOT_REPRESENTATIVE")
        efficiency = pout / pin
        energy_input_wh_day = pin * 24.0 / 1000.0
        measured_extra = (pin - sensor) * 24.0 / 1000.0
        if measured_extra > allowance + 1e-12:
            blockers.append("EXCESS_DAILY_ENERGY")
    return {
        "candidate": record["vendor"],
        "status": "DIGITAL_SCREEN_PASS_NOT_HARDWARE_APPROVAL" if not blockers else "BLOCKED",
        "blockers": sorted(set(blockers)),
        "standby_no_receiver_mw": round(p_standby, 9),
        "standby_is_loaded_evidence": False,
        "wired_ideal_floor_wh_day": round(sensor * 24.0 / 1000.0, 9),
        "maximum_loaded_tx_mw_for_budget": round(sensor + allowance * 1000.0 / 24.0, 9),
        "loaded_input_wh_day": None if energy_input_wh_day is None else round(energy_input_wh_day, 9),
        "loaded_link_efficiency": None if efficiency is None else round(efficiency, 9),
        "excess_wh_day": None if measured_extra is None else round(measured_extra, 9),
        "hardware_approved": False,
        "physical_tests_performed_by_this_tool": False,
        "evidence_class": "SYNTHETIC_OR_DOCUMENT_SCREEN_ONLY",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    record = json.loads(Path(args.input).read_text(encoding="utf-8"), parse_constant=lambda x: (_ for _ in ()).throw(ValueError(f"nonfinite {x}")))
    result = screen(record)
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
