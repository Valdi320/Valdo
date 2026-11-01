"""W-IND-104: burst, capacitor tolerance/derating, ESR, leakage and recharge gate.

Analytical sensor-side energy model only. It does not model the NFC reader,
RF field geometry, antenna, regulator dynamics, electromagnetic coupling or
whole-system reader input power. No hardware control is implemented.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from w_ind_102.w_ind_102 import DATA_PATH, load_rows, validate_rows

SCENARIO = {
    "idle_mw": 0.20,
    "burst_mw": 5.0,
    "burst_ms": 10.0,
    "period_s": 1.0,
    "cap_nominal_uf": 47.0,
    "cap_tolerance_min": 0.80,
    "cap_retention": 0.50,
    "cap_esr_ohm": 2.0,
    "cap_leakage_ua": 5.0,
    "v_start_v": 3.3,
    "v_min_v": 2.0,
    "harvest_efficiency": 0.65,
    "cap_discharge_efficiency": 0.80,
    "field_duty_off": 0.50,
}

def _number(name: str, value: object, *, allow_zero: bool = False) -> float:
    if type(value) not in (int, float):
        raise ValueError(f"{name} must be a literal number")
    value = float(value)
    if not math.isfinite(value) or value < 0 or (not allow_zero and value == 0):
        raise ValueError(f"{name} must be finite and {'nonnegative' if allow_zero else 'positive'}")
    return value

def validate_scenario(scenario: dict) -> None:
    if not isinstance(scenario, dict) or set(scenario) != set(SCENARIO):
        raise ValueError("scenario keys do not match W-IND-104 schema")
    values = {k: _number(k, v, allow_zero=k in ("cap_esr_ohm", "cap_leakage_ua"))
              for k, v in scenario.items()}
    if values["burst_mw"] < values["idle_mw"]:
        raise ValueError("burst_mw must be >= idle_mw")
    if values["burst_ms"] / 1000.0 >= values["period_s"]:
        raise ValueError("burst must fit inside one period")
    if values["v_start_v"] <= values["v_min_v"]:
        raise ValueError("capacitor voltage window must be positive")
    for key in ("cap_tolerance_min", "cap_retention", "harvest_efficiency",
                "cap_discharge_efficiency", "field_duty_off"):
        if not 0 < values[key] <= 1:
            raise ValueError(f"{key} must be in (0, 1]")

def exact_point(rows: list[dict], am_percent: int, h_a_per_m_rms: float) -> dict:
    validate_rows(rows)
    if type(am_percent) is not int or am_percent not in (10, 100):
        raise ValueError("AM must be exact integer 10 or 100")
    h = _number("h_a_per_m_rms", h_a_per_m_rms)
    matches = [r for r in rows
               if r["am_percent"] == am_percent and r["h_a_per_m_rms"] == h]
    if len(matches) != 1:
        raise ValueError("requested point is not present exactly; interpolation is forbidden")
    return dict(matches[0])

def _validate_point(row: dict) -> None:
    if type(row) is not dict:
        raise ValueError("manufacturer point must be a mapping")
    if type(row.get("am_percent")) is not int or row["am_percent"] not in (10, 100):
        raise ValueError("manufacturer point AM must be exact integer 10 or 100")
    for field in ("h_a_per_m_rms", "v_eh_v", "i_eh_ma", "p_eh_mw"):
        _number(field, row.get(field))
    product = row["v_eh_v"] * row["i_eh_ma"]
    if not math.isfinite(product) or abs(product - row["p_eh_mw"]) > 0.0051:
        raise ValueError("manufacturer point power does not match V_EH * I_EH")

def _constant_power_current(power_w: float, capacitor_v: float, esr_ohm: float) -> tuple[float | None, float]:
    if capacitor_v <= 0:
        return None, 0.0
    if esr_ohm == 0:
        current = power_w / capacitor_v
        return current, capacitor_v
    discriminant = capacitor_v * capacitor_v - 4.0 * esr_ohm * power_w
    if discriminant < 0:
        return None, 0.0
    current = (capacitor_v - math.sqrt(discriminant)) / (2.0 * esr_ohm)
    terminal_v = capacitor_v - current * esr_ohm
    return current, terminal_v

def simulate_point(row: dict, scenario: dict | None = None) -> dict:
    scenario = dict(SCENARIO if scenario is None else scenario)
    validate_scenario(scenario)
    _validate_point(row)
    p_eh_mw = _number("p_eh_mw", row["p_eh_mw"])
    t_burst_s = scenario["burst_ms"] / 1000.0
    t_off_s = scenario["period_s"] - t_burst_s

    # Apply both the candidate's ±20% tolerance and a separate 50% retention
    # stress factor. Neither is a measurement of a selected capacitor.
    c_effective_f = (scenario["cap_nominal_uf"] * 1e-6
                     * scenario["cap_tolerance_min"] * scenario["cap_retention"])
    e_burst_load_j = scenario["burst_mw"] * 1e-3 * t_burst_s
    e_burst_cap_j = e_burst_load_j / scenario["cap_discharge_efficiency"]
    e_cap_available_j = 0.5 * c_effective_f * (
        scenario["v_start_v"] ** 2 - scenario["v_min_v"] ** 2
    )
    cap_energy_pass = e_cap_available_j + 1e-15 >= e_burst_cap_j

    v2_after = scenario["v_start_v"] ** 2 - 2.0 * e_burst_cap_j / c_effective_f
    v_cap_after = math.sqrt(max(0.0, v2_after))
    current_a, v_terminal_after = _constant_power_current(
        scenario["burst_mw"] * 1e-3, v_cap_after, scenario["cap_esr_ohm"]
    )
    terminal_voltage_pass = current_a is not None and v_terminal_after >= scenario["v_min_v"]

    # Conservative timing assumption: no harvest during the burst; the reader
    # field is available only during a fraction of the off-time.
    p_harvest_off_w = (p_eh_mw * 1e-3 * scenario["harvest_efficiency"]
                       * scenario["field_duty_off"])
    p_idle_w = scenario["idle_mw"] * 1e-3
    p_leak_w = scenario["v_start_v"] * scenario["cap_leakage_ua"] * 1e-6
    p_net_recharge_w = p_harvest_off_w - p_idle_w - p_leak_w
    recharge_time_s = e_burst_cap_j / p_net_recharge_w if p_net_recharge_w > 0 else math.inf
    recharge_pass = recharge_time_s <= t_off_s

    e_harvest_per_period_j = p_harvest_off_w * t_off_s
    e_idle_per_period_j = p_idle_w * t_off_s
    e_leak_per_period_j = p_leak_w * scenario["period_s"]
    e_required_per_period_j = e_idle_per_period_j + e_leak_per_period_j + e_burst_cap_j
    energy_balance_pass = e_harvest_per_period_j + 1e-15 >= e_required_per_period_j

    p_eh_w = p_eh_mw * 1e-3
    required_field_duty = (
        p_idle_w + p_leak_w + e_burst_cap_j / t_off_s
    ) / (p_eh_w * scenario["harvest_efficiency"])
    nominal_capacitance_required_uf = (
        2.0 * e_burst_cap_j
        / (scenario["v_start_v"] ** 2 - scenario["v_min_v"] ** 2)
        / (scenario["cap_tolerance_min"] * scenario["cap_retention"])
        * 1e6
    )
    max_esr_ohm = (
        max(0.0, (v_cap_after - scenario["v_min_v"])
            * scenario["v_min_v"] / (scenario["burst_mw"] * 1e-3))
        if v_cap_after >= scenario["v_min_v"] else 0.0
    )
    max_leakage_ua = max(
        0.0,
        (p_harvest_off_w - p_idle_w - e_burst_cap_j / t_off_s)
        / scenario["v_start_v"] * 1e6,
    )
    checks = {
        "capacitor_energy": cap_energy_pass,
        "terminal_voltage_after_esr": terminal_voltage_pass,
        "recharge_before_next_burst": recharge_pass,
        "period_energy_balance": energy_balance_pass,
    }
    return {
        "am_percent": row["am_percent"],
        "h_a_per_m_rms": row["h_a_per_m_rms"],
        "p_eh_mw_manufacturer": p_eh_mw,
        "average_sensor_load_mw": (
            scenario["idle_mw"] * t_off_s
            + scenario["burst_mw"] * t_burst_s
        ) / scenario["period_s"],
        "cap_effective_uf": c_effective_f * 1e6,
        "cap_energy_available_uj": e_cap_available_j * 1e6,
        "burst_load_energy_uj": e_burst_load_j * 1e6,
        "burst_cap_energy_required_uj": e_burst_cap_j * 1e6,
        "cap_energy_margin_ratio": e_cap_available_j / e_burst_cap_j,
        "cap_voltage_after_burst_v": v_cap_after,
        "terminal_voltage_after_esr_v": v_terminal_after,
        "burst_current_at_end_ma": current_a * 1e3 if current_a is not None else None,
        "required_field_duty_during_off_time": required_field_duty,
        "assumed_field_duty_during_off_time": scenario["field_duty_off"],
        "harvest_power_during_off_time_mw": p_harvest_off_w * 1e3,
        "idle_power_mw": scenario["idle_mw"],
        "capacitor_leakage_power_mw": p_leak_w * 1e3,
        "net_recharge_power_mw": p_net_recharge_w * 1e3,
        "recharge_time_s": recharge_time_s if math.isfinite(recharge_time_s) else None,
        "off_time_s": t_off_s,
        "harvest_energy_per_period_uj": e_harvest_per_period_j * 1e6,
        "required_energy_per_period_uj": e_required_per_period_j * 1e6,
        "energy_margin_per_period_uj": (e_harvest_per_period_j - e_required_per_period_j) * 1e6,
        "nominal_capacitance_required_uf": nominal_capacitance_required_uf,
        "max_esr_at_minimum_terminal_voltage_ohm": max_esr_ohm,
        "max_leakage_at_assumed_field_duty_ua": max_leakage_ua,
        "checks": checks,
        "status": "CONDITIONAL_PASS" if all(checks.values()) else "NO_GO_UNDER_ASSUMPTIONS",
    }

def build_report(rows: list[dict]) -> dict:
    validate_rows(rows)
    baseline_row = exact_point(rows, 10, 1.0)
    baseline = simulate_point(baseline_row, SCENARIO)
    gated_rows = [r for r in rows if r["h_a_per_m_rms"] >= 1.0]
    sweep = [simulate_point(r, SCENARIO) for r in gated_rows]
    worst = max(sweep, key=lambda r: r["required_field_duty_during_off_time"])
    field_sensitivity = []
    for duty in (0.25, 0.40, 0.50, 1.00):
        s = dict(SCENARIO)
        s["field_duty_off"] = duty
        result = simulate_point(baseline_row, s)
        field_sensitivity.append({
            "field_duty_off": duty,
            "status": result["status"],
            "recharge_time_s": result["recharge_time_s"],
            "energy_margin_per_period_uj": result["energy_margin_per_period_uj"],
        })
    cap_sensitivity = []
    for retention in (0.40, 0.50, 0.60):
        s = dict(SCENARIO)
        s["cap_retention"] = retention
        result = simulate_point(baseline_row, s)
        cap_sensitivity.append({
            "cap_retention": retention,
            "status": result["status"],
            "cap_energy_margin_ratio": result["cap_energy_margin_ratio"],
            "terminal_voltage_after_esr_v": result["terminal_voltage_after_esr_v"],
        })
    esr_sensitivity = []
    for esr in (2.0, 10.0, 25.0):
        s = dict(SCENARIO)
        s["cap_esr_ohm"] = esr
        result = simulate_point(baseline_row, s)
        esr_sensitivity.append({
            "cap_esr_ohm": esr,
            "status": result["status"],
            "terminal_voltage_after_esr_v": result["terminal_voltage_after_esr_v"],
        })
    leakage_sensitivity = []
    for leakage in (5.0, 20.0, 30.0):
        s = dict(SCENARIO)
        s["cap_leakage_ua"] = leakage
        result = simulate_point(baseline_row, s)
        leakage_sensitivity.append({
            "cap_leakage_ua": leakage,
            "status": result["status"],
            "recharge_time_s": result["recharge_time_s"],
            "energy_margin_per_period_uj": result["energy_margin_per_period_uj"],
        })
    return {
        "schema": "valdo.w_ind_104.capacitor_recharge_gate.v1",
        "milestone": "W-IND-104",
        "classification": "ANALYTICAL_SENSOR_SIDE_ENERGY_MODEL_NOT_PHYSICAL_MEASUREMENT",
        "source": {
            "document": "STMicroelectronics AN4913 Rev. 2",
            "tables": [4, 5],
            "manufacturer_points": 22,
            "exact_point_used": {
                "am_percent": 10,
                "h_a_per_m_rms": 1.0,
                "p_eh_mw": baseline_row["p_eh_mw"],
            },
            "antenna_limit": "Class 1 antenna, 13.6 MHz, 10 nF V_EH setup; does not qualify X-NUCLEO-NFC07A1 or robot geometry.",
        },
        "load_profile": {
            "idle_mw": SCENARIO["idle_mw"],
            "burst_mw": SCENARIO["burst_mw"],
            "burst_ms": SCENARIO["burst_ms"],
            "period_s": SCENARIO["period_s"],
            "average_sensor_load_mw": baseline["average_sensor_load_mw"],
            "status": "HYPOTHETICAL_NONCRITICAL_SENSOR_PROFILE",
        },
        "baseline_scenario": baseline,
        "sweep_h_ge_1a_per_m": {
            "point_count": len(gated_rows),
            "conditional_pass_at_assumptions": sum(x["status"] == "CONDITIONAL_PASS" for x in sweep),
            "worst_required_field_duty_point": worst,
        },
        "sensitivity": {
            "field_duty": field_sensitivity,
            "capacitance_retention": cap_sensitivity,
            "esr": esr_sensitivity,
            "leakage": leakage_sensitivity,
        },
        "decision": {
            "47uf_candidate": "NOT_APPROVED: only 3.6% energy margin after 20% tolerance and 50% retention assumptions; exact ESR/leakage/DC-bias/temperature behavior unqualified.",
            "microsensor": "CONDITIONAL_ONLY: at 1 A/m RMS, AM=10%, 65% assumed conversion efficiency, requires at least 41.6% reader-field duty during off-time under this load profile.",
            "active_module_400mw": "NO_GO_FOR_ST25DV_EH: manufacturer reference maximum is 12.593 mW; use regulated WPT only after FOD/thermal/offset/EMI/independent-cut qualification, otherwise keyed locking connector.",
            "dock_charging": "SEPARATE: OOMWOO official dock remains contact-based; no battery/BMS/dock modification in this milestone.",
            "reader_energy": "EXCLUDED: reader input power and RF field generation overhead are unknown; this is not whole-system efficiency.",
            "data": "ESP-NOW is provisional for a small one-hop Espressif network; OpenThread only if IPv6 mesh/multi-hop is needed. Both require application ACK, sequence, timeout, authenticated privacy and recovery.",
            "critical_stop": "LOCAL_HARDWIRED_FAIL_SAFE_ONLY; never radio-dependent.",
        },
        "assumptions": {
            **SCENARIO,
            "field_duty_off_definition": "fraction of the off-time during which the manufacturer-point harvest power is assumed available",
            "no_harvest_during_burst": True,
            "reader_power_included": False,
            "field_interpolation": False,
            "antenna_transfer_qualified": False,
            "cap_esr_and_leakage_are_stress_assumptions_not_part_data": True,
            "cap_retention_is_assumption_not_datasheet": True,
            "cap_tolerance_min_from_rejected_47uf_candidate": 0.80,
        },
        "limits": {
            "physical_measurements": 0,
            "electromagnetic_simulations": 0,
            "battery_bms_connected": False,
            "dock_modified": False,
            "hardware_approved": False,
            "third_party_code_or_cad_copied": False,
            "third_party_repositories_modified": False,
            "oomwoo_or_pr79_modified": False,
        },
        "input_sha256": hashlib.sha256(DATA_PATH.read_bytes()).hexdigest(),
        "model_sha256": hashlib.sha256(Path(__file__).resolve().read_bytes()).hexdigest(),
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    report = build_report(load_rows())
    payload = json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
