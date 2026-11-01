"""W-IND-85: reproducible source-attributed NFC harvesting feasibility screen.

Analysis only: no RF transmission, motor, charging, WPT control or hardware approval.
Author test points are short factual excerpts from ST AN4913 Rev 2 Table 4/5.
"""
from __future__ import annotations

import argparse
import json
from decimal import Decimal, InvalidOperation

SOURCE = (
    "STMicroelectronics AN4913 Rev2 June 2021, p7, Table 4/5; "
    "ISO class 1 antenna, 13.6MHz tuning, RF inventory response test"
)
DATASHEET = "STMicroelectronics DS13519 Rev8 July 2024 p49 section 5.5.2"
# Two manufacturer-fixture observations, not robot measurements or guaranteed bounds.
POINTS = (
    {"case": "ST_AM100_H3", "am_pct": 100, "h_arms": "3", "v_eh_v": "3.23",
     "i_eh_ma": "0.9", "p_eh_mw": "2.907"},
    {"case": "ST_AM10_H3", "am_pct": 10, "h_arms": "3", "v_eh_v": "3.13",
     "i_eh_ma": "1.3", "p_eh_mw": "4.069"},
)


def positive(value, label: str, allow_zero: bool = False) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError(f"{label}: invalid decimal") from exc
    if not result.is_finite() or (result < 0 if allow_zero else result <= 0):
        raise ValueError(f"{label}: out of range")
    return result


def cap_min_uf(power_mw, outage_ms, v_high, v_floor) -> Decimal:
    """Ideal, lossless hold-up at constant power, no ESR, derating or backfeed."""
    p, t = positive(power_mw, "power_mw"), positive(outage_ms, "outage_ms")
    hi, lo = positive(v_high, "v_high"), positive(v_floor, "v_floor")
    if hi <= lo:
        raise ValueError("hold_up_voltage_window_invalid")
    # P[mW]*t[ms] = microjoules; C[uF] = 2E[uJ] / (Vhi^2-Vlo^2).
    return Decimal(2) * p * t / (hi * hi - lo * lo)


def screen_point(point: dict, *, power_mw, rail_v, illustrative_efficiency) -> dict:
    load = positive(power_mw, "power_mw")
    rail = positive(rail_v, "rail_v")
    efficiency = positive(illustrative_efficiency, "illustrative_efficiency")
    if efficiency > 1:
        raise ValueError("illustrative_efficiency_exceeds_unity")
    v = positive(point["v_eh_v"], "v_eh_v")
    i = positive(point["i_eh_ma"], "i_eh_ma")
    p = positive(point["p_eh_mw"], "p_eh_mw")
    h = positive(point["h_arms"], "h_arms")
    if point["am_pct"] not in (10, 100):
        raise ValueError("unrecognized_modulation")
    if v * i != p:
        raise ValueError("manufacturer_point_power_mismatch")
    theoretical = p * efficiency
    return {
        "point_id": point["case"],
        "origin": "manufacturer_test_fixture_not_our_own_measurement",
        "field_arms": str(h),
        "reader_am_pct": point["am_pct"],
        "author_v_eh_v": str(v),
        "author_p_eh_mw": str(p),
        "ideal_efficiency_needed_pct": f"{load * 100 / p:.3f}",
        "assumed_regulated_output_mw": f"{theoretical:.4f}",
        "assumed_output_margin_mw": f"{theoretical - load:+.4f}",
        "direct_rail_voltage_inadequate": bool(v < rail),
        "conditional_static_budget_pass": bool(theoretical >= load),
        "guaranteed_power_or_rf_data": False,
    }


def evaluate(*, load_mw="2.9", rail_v="3.3", floor_v="3.0",
             outage_ms="100", effective_cap_uf="330", illustrative_efficiency="0.8",
             field_and_alignment_proven=False, continuous_rf_data_proven=False,
             thermal_fod_cutout_proven=False) -> dict:
    # Explicit booleans do not turn supplier data into our own measurements.
    for flag in (field_and_alignment_proven, continuous_rf_data_proven, thermal_fod_cutout_proven):
        if type(flag) is not bool:
            raise ValueError("evidence_flags_must_be_boolean")
    load, rail, floor, outage, cap, eta = (
        positive(load_mw, "load_mw"), positive(rail_v, "rail_v"),
        positive(floor_v, "floor_v"), positive(outage_ms, "outage_ms"),
        positive(effective_cap_uf, "effective_cap_uf", allow_zero=True),
        positive(illustrative_efficiency, "illustrative_efficiency"),
    )
    if eta > 1:
        raise ValueError("illustrative_efficiency_exceeds_unity")
    minimum = cap_min_uf(load, outage, rail, floor)
    cases = [screen_point(p, power_mw=load, rail_v=rail, illustrative_efficiency=eta) for p in POINTS]
    missing = []
    if not field_and_alignment_proven:
        missing.append("reader_field_coupling_in_robot_unverified")
    if not continuous_rf_data_proven:
        missing.append("rf_data_during_energy_harvesting_unverified")
    if not thermal_fod_cutout_proven:
        missing.append("FOD_temperature_and_independent_cutout_unverified")
    missing.extend(("actual_5V_or_3V3_regulator_curve_unverified",
                    "capacitor_ESR_leakage_aging_unverified",
                    "full_reader_antenna_cost_and_consumption_unverified",
                    "no_own_energized_hardware_or_bench_measurement"))
    return {
        "scope": "optional_noncritical_low_power_service_sensor_only",
        "source_power": SOURCE,
        "source_unregulated_and_rf_caution": DATASHEET,
        "input_provenance": "two_observed_author_fixture_points_plus_explicit_hypotheses",
        "assumed_load_mw": f"{load:.3f}",
        "assumed_rail_v": f"{rail:.3f}",
        "assumed_floor_v": f"{floor:.3f}",
        "assumed_outage_ms": f"{outage:.3f}",
        "assumed_efficiency_pct": f"{eta * 100:.2f}",
        "ideal_cap_min_uf": f"{minimum:.3f}",
        "assumed_effective_cap_uf": f"{cap:.3f}",
        "conditional_ideal_cap_pass": cap >= minimum,
        "manufacturer_fixture_cases": cases,
        "requires_active_NFC_reader_not_an_ESP_NOW_radio": True,
        "EH_voltage_is_unregulated_and_absent_if_field_insufficient": True,
        "RF_communication_guaranteed_while_EH": False,
        "hardware_release": "BLOCKED",
        "dock_BMS_motors_safety": "NOT_IN_SCOPE",
        "missing_evidence": missing,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="W85 digital-only NFC/EH field/energy viability gate")
    parser.add_argument("--load-mw", default="2.9")
    parser.add_argument("--rail-v", default="3.3")
    parser.add_argument("--floor-v", default="3.0")
    parser.add_argument("--outage-ms", default="100")
    parser.add_argument("--effective-cap-uf", default="330")
    parser.add_argument("--illustrative-efficiency", default="0.8")
    args = parser.parse_args()
    out = evaluate(load_mw=args.load_mw, rail_v=args.rail_v, floor_v=args.floor_v,
                   outage_ms=args.outage_ms, effective_cap_uf=args.effective_cap_uf,
                   illustrative_efficiency=args.illustrative_efficiency)
    print(json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
