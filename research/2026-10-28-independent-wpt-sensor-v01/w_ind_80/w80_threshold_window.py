#!/usr/bin/env python3
"""W80: static worst-case threshold-window audit, NOT physical safety validation.

All requirements in the input scenario are hypothetical. TI TPS3840 family
0.1-V increments and 1.5% maximum threshold accuracy are manufacturer data.
No hardware, dynamic response, latch, energy or operating approval is inferred.
"""
import argparse
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

SIX = Decimal("0.000001")


def number(value, label):
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise ValueError(label + ": not a number")
    try:
        n = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(label + ": invalid decimal") from exc
    if not n.is_finite():
        raise ValueError(label + ": nonfinite")
    return n


def fmt(n):
    return format(n.quantize(SIX), "f")


def audit(scenario):
    if not isinstance(scenario, dict):
        raise ValueError("scenario must be object")
    fields = {
        key: number(scenario[key], key)
        for key in (
            "normal_rail_nominal_v",
            "normal_rail_fractional_tolerance",
            "sensor_floor_v",
            "supervisor_nominal_threshold_min_v",
            "supervisor_nominal_threshold_max_v",
            "supervisor_nominal_threshold_step_v",
            "supervisor_fractional_threshold_tolerance",
        )
    }
    rail = fields["normal_rail_nominal_v"]
    rail_tol = fields["normal_rail_fractional_tolerance"]
    floor = fields["sensor_floor_v"]
    tmin = fields["supervisor_nominal_threshold_min_v"]
    tmax = fields["supervisor_nominal_threshold_max_v"]
    step = fields["supervisor_nominal_threshold_step_v"]
    err = fields["supervisor_fractional_threshold_tolerance"]
    if rail <= 0 or floor <= 0 or tmin <= 0 or tmax < tmin or step <= 0:
        raise ValueError("nonpositive or inverted voltage/grid")
    if not (0 <= rail_tol < 1 and 0 <= err < 1):
        raise ValueError("tolerances outside [0,1)")
    ticks = (tmax - tmin) / step
    if ticks != ticks.to_integral_value() or ticks > 1000:
        raise ValueError("grid must terminate exactly and have <=1001 entries")
    candidates = scenario["illustrative_thresholds_v"]
    if not isinstance(candidates, list) or not candidates or len(candidates) > 100:
        raise ValueError("illustrative_thresholds_v must be nonempty bounded list")
    names = [number(x, "candidate") for x in candidates]
    if any(x <= 0 or x < tmin or x > tmax for x in names) or len(names) != len(set(names)):
        raise ValueError("candidates must be distinct and within range")

    normal_min = rail * (1 - rail_tol)
    # A static trip must be >= the required floor at the LOW threshold corner,
    # but must not be asserted at the minimum normal rail at the HIGH corner.
    nominal_lower = floor / (1 - err)
    nominal_upper = normal_min / (1 + err)

    def evaluate(nominal):
        fall_min = nominal * (1 - err)
        fall_max = nominal * (1 + err)
        member_tick = (nominal - tmin) / step
        member = member_tick == member_tick.to_integral_value()
        protects = fall_min >= floor
        normal = fall_max <= normal_min
        return {
            "nominal_v": fmt(nominal),
            "fall_min_v": fmt(fall_min),
            "fall_max_v": fmt(fall_max),
            "catalog_grid_member": member,
            "static_floor_protected": protects,
            "static_no_false_trip_at_normal_min": normal,
            "static_conditions_met": protects and normal,
            "approved_for_hardware": False,
        }

    grid = [tmin + step * i for i in range(int(ticks) + 1)]
    feasible = [fmt(v) for v in grid if v * (1 - err) >= floor and v * (1 + err) <= normal_min]
    result = {
        "analysis_class": "STATIC_BOUNDS_ONLY_SYNTHETIC_REQUIREMENTS",
        "normal_rail_min_v": fmt(normal_min),
        "sensor_floor_v": fmt(floor),
        "nominal_threshold_static_window_v": {
            "lower": fmt(nominal_lower),
            "upper": fmt(nominal_upper),
        },
        "family_grid_count": len(grid),
        "feasible_catalog_grid_nominal_v": feasible,
        "no_grid_member_satisfies_both_static_constraints": len(feasible) == 0,
        "illustrative_candidates": [evaluate(v) for v in names],
        "hysteresis_release_qualified": False,
        "timing_and_voltage_slew_qualified": False,
        "independent_monitor_supply_and_cut_qualified": False,
        "physical_measurements_authenticated": False,
        "hardware_approved": False,
        "critical_stop_authorized": False,
        "battery_bms_and_dock_approved": False,
        "decision": "NO_HARDWARE_SELECTION; retain serviceable wired sensor baseline",
        "blockers": [
            "STATIC_CATALOG_GRID_EMPTY" if not feasible else "STATIC_ONLY_NOT_DYNAMIC",
            "HYSTERESIS_RELEASE_WORST_CASE_NOT_QUALIFIED",
            "FALL_SLEW_AND_DELAY_NOT_QUALIFIED",
            "MONITOR_SUPPLY_LATCH_CUT_BACKFEED_NOT_QUALIFIED",
            "WPT_FOD_THERMAL_EMI_OFFSET_NOT_MEASURED",
            "DOCK_BATTERY_BMS_OUT_OF_SCOPE",
        ],
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    a = parser.parse_args()
    report = audit(json.loads(Path(a.input).read_text(encoding="utf-8")))
    Path(a.output).write_text(
        json.dumps(report, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
