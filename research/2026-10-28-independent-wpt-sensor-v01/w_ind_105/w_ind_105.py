#!/usr/bin/env python3
"""W-IND-105: reader-inclusive NFC energy gate.

Uses ST's published ST25DVxxKC EH table and ST25R3916B reader-current
conditions. This is a datasheet-based lower-bound screen, not a physical
measurement or a whole-system efficiency calculation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

from w_ind_102.w_ind_102 import DATA_PATH, load_rows, validate_rows

DOWNSTREAM_EFFICIENCY = 0.65  # inherited W-IND-104 assumption; not measured
SENSOR_SCENARIO = {
    "average_load_mw": 0.248,
    "period_s": 1.0,
    "burst_ms": 10.0,
    "field_duty_during_off_time": 0.50,
}
READER = {
    "vdd_v": 2.4,
    "power_down_typ_ua": 0.5,
    "power_down_max_ua": 2.2,
    "wake_typ_ua": 1.8,
    "wake_max_ua": 5.0,
    "ready_typ_ma": 3.4,
    "ready_max_ma": 7.5,
    "active_typ_ma": 14.0,
    "active_max_ma": 23.0,
    "active_rfo_segments_enabled": False,
}
ACTIVE_MODULE_REFERENCE_MW = 400.0


def _finite_number(name: str, value: Any, *, allow_zero: bool = False) -> float:
    if type(value) not in (int, float):
        raise ValueError(f"{name} must be an exact int or float")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    if value < 0 or (value == 0 and not allow_zero):
        qualifier = "nonnegative" if allow_zero else "positive"
        raise ValueError(f"{name} must be {qualifier}")
    return value


def _validate_efficiency(value: Any) -> float:
    efficiency = _finite_number("downstream_efficiency", value)
    if efficiency > 1.0:
        raise ValueError("downstream_efficiency must be <= 1")
    return efficiency


def _validate_reader(reader: dict[str, Any]) -> tuple[float, float, float]:
    if type(reader) is not dict:
        raise ValueError("reader must be a mapping")
    if reader.get("active_rfo_segments_enabled") is not False:
        raise ValueError("reader reference must explicitly keep RFO segments disabled")
    vdd = _finite_number("reader_vdd_v", reader.get("vdd_v"))
    active_typ_ma = _finite_number("reader_active_typ_ma", reader.get("active_typ_ma"))
    active_max_ma = _finite_number("reader_active_max_ma", reader.get("active_max_ma"))
    if active_max_ma < active_typ_ma:
        raise ValueError("reader active maximum current must be >= typical current")
    return vdd, active_typ_ma, active_max_ma


def _validate_sensor_scenario(scenario: dict[str, Any]) -> tuple[float, float, float, float]:
    if type(scenario) is not dict:
        raise ValueError("sensor scenario must be a mapping")
    average_load_mw = _finite_number("sensor_average_load_mw", scenario.get("average_load_mw"))
    period_s = _finite_number("sensor_period_s", scenario.get("period_s"))
    burst_ms = _finite_number("sensor_burst_ms", scenario.get("burst_ms"))
    field_duty = _finite_number(
        "field_duty_during_off_time", scenario.get("field_duty_during_off_time")
    )
    if burst_ms / 1000.0 >= period_s:
        raise ValueError("sensor burst must fit inside its period")
    if field_duty > 1.0:
        raise ValueError("field duty must be <= 1")
    return average_load_mw, period_s, burst_ms, field_duty


def screen_point(
    row: dict[str, Any],
    downstream_efficiency: float = DOWNSTREAM_EFFICIENCY,
    reader: dict[str, Any] = READER,
    scenario: dict[str, Any] = SENSOR_SCENARIO,
) -> dict[str, Any]:
    """Compare one ST AN4913 point with a reader chip reference.

    P_EH is already the tag's DC output. Downstream efficiency is applied once
    to estimate a regulated sensor rail. The field duty is the W-IND-104
    assumption: 50% of the non-burst interval. Reader active power is counted
    only during the same field-on interval, and its output segments are disabled.
    """
    efficiency = _validate_efficiency(downstream_efficiency)
    if type(row) is not dict:
        raise ValueError("manufacturer row must be a mapping")
    am = row.get("am_percent")
    if type(am) is not int or am not in (10, 100):
        raise ValueError("am_percent must be exact integer 10 or 100")
    h_field = _finite_number("h_a_per_m_rms", row.get("h_a_per_m_rms"))
    p_eh = _finite_number("p_eh_mw", row.get("p_eh_mw"))
    vdd, active_typ_ma, active_max_ma = _validate_reader(reader)
    average_load_mw, period_s, burst_ms, field_duty = _validate_sensor_scenario(scenario)

    reader_typ_mw = vdd * active_typ_ma
    reader_max_mw = vdd * active_max_ma
    sensor_rail_mw = p_eh * efficiency
    if sensor_rail_mw <= 0:
        raise ValueError("sensor rail power must be positive")

    off_time_s = period_s - burst_ms / 1000.0
    field_on_time_s = field_duty * off_time_s
    period_fraction_with_field = field_on_time_s / period_s
    average_tag_rail_mw = sensor_rail_mw * period_fraction_with_field
    average_reader_chip_reference_mw = reader_typ_mw * period_fraction_with_field

    return {
        "am_percent": am,
        "h_a_per_m_rms": h_field,
        "p_eh_mw_manufacturer": p_eh,
        "downstream_efficiency_assumed": efficiency,
        "p_sensor_rail_mw_while_field_on_assumed": sensor_rail_mw,
        "average_tag_rail_mw_assumed": average_tag_rail_mw,
        "average_reader_chip_reference_mw": average_reader_chip_reference_mw,
        "reader_active_chip_reference_typ_mw": reader_typ_mw,
        "reader_active_chip_reference_max_mw": reader_max_mw,
        "field_duty_during_off_time_assumed": field_duty,
        "field_on_time_per_period_s_assumed": field_on_time_s,
        "reader_to_sensor_ratio_typ": reader_typ_mw / sensor_rail_mw,
        "reader_to_sensor_ratio_max": reader_max_mw / sensor_rail_mw,
        "ideal_tag_count_lower_bound_typ": math.ceil(reader_typ_mw / sensor_rail_mw),
        "ideal_tag_count_lower_bound_max": math.ceil(reader_max_mw / sensor_rail_mw),
        "reader_minus_one_tag_typ_mw_while_field_on": reader_typ_mw - sensor_rail_mw,
        "reader_minus_one_tag_max_mw_while_field_on": reader_max_mw - sensor_rail_mw,
        "average_sensor_load_mw_from_w_ind_104": average_load_mw,
        "average_sensor_side_margin_ratio": average_tag_rail_mw / average_load_mw,
        "dedicated_harvesting_break_even_vs_chip_reference": (
            average_tag_rail_mw >= average_reader_chip_reference_mw
        ),
    }


def build_report(
    rows: list[dict[str, Any]] | None = None,
    downstream_efficiency: float = DOWNSTREAM_EFFICIENCY,
) -> dict[str, Any]:
    rows = load_rows() if rows is None else rows
    validate_rows(rows)
    efficiency = _validate_efficiency(downstream_efficiency)
    points = [screen_point(row, efficiency) for row in rows]
    baseline = next(
        point for point in points
        if point["am_percent"] == 10 and point["h_a_per_m_rms"] == 1.0
    )
    best = max(points, key=lambda point: point["p_eh_mw_manufacturer"])
    all_below = all(
        point["average_tag_rail_mw_assumed"]
        < point["average_reader_chip_reference_mw"]
        for point in points
    )
    vdd = READER["vdd_v"]
    reader_typ_mw = vdd * READER["active_typ_ma"]
    reader_max_mw = vdd * READER["active_max_ma"]
    best_sensor_rail_mw = best["p_sensor_rail_mw_while_field_on_assumed"]
    average_load_mw, period_s, burst_ms, field_duty = _validate_sensor_scenario(
        SENSOR_SCENARIO
    )
    off_time_s = period_s - burst_ms / 1000.0
    field_on_time_s = field_duty * off_time_s

    return {
        "schema": "valdo.w_ind_105.reader_inclusive_nfc_energy_gate.v1",
        "milestone": "W-IND-105",
        "classification": "DATASHEET_BASED_LOWER_BOUND_SCREEN_NOT_PHYSICAL_MEASUREMENT",
        "sources": {
            "tag": "ST AN4913 Rev.2, Tables 4 and 5; 22 exact points; ISO/IEC Class 1 antenna tuned at 13.6 MHz; V_EH output.",
            "reader": "ST25R3916B DS13541 Rev.11, Table 127, VDD=2.4 V.",
            "reader_active_condition": (
                "RX and TX enabled, RFO output segments disabled (datasheet footnote 7). "
                "This is a chip-only active reference, not field-on reader input power."
            ),
            "reader_wake_condition": (
                "Logic and RC oscillator wake-up mode. No reader-generated RF field "
                "or tag energy-harvesting credit is assumed in this mode."
            ),
        },
        "reader_modes": {
            "vdd_v": vdd,
            "power_down_typ_uw": vdd * READER["power_down_typ_ua"],
            "power_down_max_uw": vdd * READER["power_down_max_ua"],
            "wake_typ_uw": vdd * READER["wake_typ_ua"],
            "wake_max_uw": vdd * READER["wake_max_ua"],
            "ready_typ_mw": vdd * READER["ready_typ_ma"],
            "ready_max_mw": vdd * READER["ready_max_ma"],
            "active_chip_reference_typ_mw": reader_typ_mw,
            "active_chip_reference_max_mw": reader_max_mw,
            "rfo_segments_enabled": False,
            "field_generated_in_wake_mode": False,
            "field_generated_in_ready_mode": False,
            "field_generated_in_power_down_mode": False,
            "wake_mode_tag_eh_credit_mw": 0.0,
        },
        "sensor_scenario": {
            "average_load_mw_from_w_ind_104": average_load_mw,
            "period_s": period_s,
            "burst_ms": burst_ms,
            "off_time_s": off_time_s,
            "field_duty_during_off_time": field_duty,
            "field_on_time_per_period_s": field_on_time_s,
            "field_on_fraction_of_period": field_on_time_s / period_s,
        },
        "downstream_efficiency_assumption": efficiency,
        "sensor_reference": {
            "average_load_mw": average_load_mw,
            "baseline_1a_m_am10": baseline,
            "best_case_average_tag_rail_mw": best["average_tag_rail_mw_assumed"],
            "best_case_average_reader_chip_reference_mw": (
                best["average_reader_chip_reference_mw"]
            ),
            "active_module_reference_mw": ACTIVE_MODULE_REFERENCE_MW,
            "best_case_average_tag_rail_fraction_of_active_module": (
                best["average_tag_rail_mw_assumed"] / ACTIVE_MODULE_REFERENCE_MW
            ),
            "baseline_average_sensor_side_margin_ratio": (
                baseline["average_sensor_side_margin_ratio"]
            ),
            "baseline_reader_chip_energy_per_period_mj": (
                reader_typ_mw * field_on_time_s
            ),
            "baseline_tag_rail_energy_per_period_mj": (
                baseline["average_tag_rail_mw_assumed"] * period_s
            ),
        },
        "best_tag_point_in_an4913": best,
        "sweep": {
            "manufacturer_point_count": len(points),
            "all_22_average_tag_rail_outputs_below_reader_active_typ": all_below,
            "dedicated_harvesting_points_at_or_above_reader_reference": sum(
                point["dedicated_harvesting_break_even_vs_chip_reference"]
                for point in points
            ),
            "best_case_sensor_rail_to_reader_typ_ratio": (
                best_sensor_rail_mw / reader_typ_mw
            ),
            "best_case_reader_minus_one_tag_typ_mw_while_field_on": (
                reader_typ_mw - best_sensor_rail_mw
            ),
            "ideal_tag_count_lower_bound_typ_min": min(
                point["ideal_tag_count_lower_bound_typ"] for point in points
            ),
            "ideal_tag_count_lower_bound_typ_max": max(
                point["ideal_tag_count_lower_bound_typ"] for point in points
            ),
            "ideal_tag_count_lower_bound_max_min": min(
                point["ideal_tag_count_lower_bound_max"] for point in points
            ),
            "ideal_tag_count_lower_bound_max_max": max(
                point["ideal_tag_count_lower_bound_max"] for point in points
            ),
            "points": points,
        },
        "decision": {
            "dedicated_nfc_energy_harvesting": (
                "NO_GO_FOR_ST25R3916B_READER_CANDIDATE: all 22 AN4913 tag points, "
                "after 65% assumed downstream conversion and 50% field duty over "
                "the W-IND-104 off-time, remain below the 33.6 mW typical chip-only "
                "active reference with RFO segments disabled. Actual field-on input "
                "must additionally account for antenna drive, host MCU, board, "
                "regulator and RF losses; no positive whole-system energy balance is demonstrated."
            ),
            "opportunistic_nfc_harvesting": (
                "CONDITIONAL_ONLY_WHEN_THE_READER_FIELD_IS_ALREADY_REQUIRED_FOR_DATA_OR_ID: "
                "incremental field power, tag loading, communication margin and duty "
                "must be measured; no energy-saving claim is made."
            ),
            "wisp5": (
                "DEFER: use only if a passive UHF RFID sensor and a UHF reader are "
                "already justified; it is not an active module power rail."
            ),
            "active_modules": (
                "KEYED_LOCKING_CONNECTOR_DEFAULT; regulated WPT only after measured "
                "load and documented FOD, thermal, offset, EMI and independent hardware cut."
            ),
            "dock": (
                "KEEP_CONTACT_BASELINE; do not route battery/BMS charging through NFC EH "
                "or an unqualified WPT stage."
            ),
            "data": (
                "ESP-NOW provisional for a small one-hop Espressif network; OpenThread "
                "only if IPv6 mesh/multi-hop is required. Both need application ACK, "
                "CRC, sequence, timeout, bounded retry, authenticated privacy and recovery."
            ),
            "critical_stop": "LOCAL_HARDWIRED_FAIL_SAFE_ONLY; never radio-dependent.",
        },
        "assumptions": {
            "downstream_efficiency": efficiency,
            "reader_vdd_v": vdd,
            "reader_active_typ_ma": READER["active_typ_ma"],
            "reader_active_max_ma": READER["active_max_ma"],
            "reader_active_rfo_segments_enabled": False,
            "reader_antenna_drive_power_included": False,
            "host_mcu_and_board_power_included": False,
            "reader_regulator_loss_included": False,
            "tag_coupling_changes_with_multiple_tags_included": False,
            "field_geometry_and_antenna_transfer_qualified": False,
            "field_duty_during_off_time": field_duty,
            "ideal_tag_count_assumes_linear_sum_without_mutual_loading": True,
            "reader_wake_mode_harvest_credit_mw": 0.0,
        },
        "limits": {
            "physical_measurements": 0,
            "electromagnetic_simulations": 0,
            "reader_input_power_measured": False,
            "whole_system_efficiency_measured": False,
            "battery_bms_connected": False,
            "dock_modified": False,
            "hardware_approved": False,
            "third_party_code_or_cad_copied": False,
            "third_party_repositories_modified": False,
            "oomwoo_or_pr79_modified": False,
        },
        "provenance": {
            "manufacturer_data_file": str(DATA_PATH.name),
            "manufacturer_data_sha256": hashlib.sha256(DATA_PATH.read_bytes()).hexdigest(),
            "model_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="-", help="JSON output path, or '-' for stdout")
    args = parser.parse_args()
    report = build_report()
    payload = json.dumps(report, sort_keys=True, indent=2, allow_nan=False) + "\n"
    if args.out == "-":
        print(payload, end="")
    else:
        output = Path(args.out)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
