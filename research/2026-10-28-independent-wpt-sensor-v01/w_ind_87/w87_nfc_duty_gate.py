"""W-IND-87: conditional NFC energy-harvesting duty-cycle and storage gate.

Inputs other than the ST author sample are explicit hypothetical assumptions.
No third-party code, no hardware qualification, no battery/BMS/dock/motor.
For ST measurements, reuse the original numerical transcription in W-IND-86.
"""
from __future__ import annotations

from decimal import Decimal
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "w_ind_86"))
from w86_field_sweep import at, number, SOURCE, PROVENANCE  # original W code, ST data attributed

D = Decimal


def duty_gate(*, am: str, field: str, efficiency: str, baseline_mw: str,
              leakage_mw: str, event_mj: str, period_s: str,
              capacitance_effective_uf: str, v_storage_high: str,
              v_storage_low: str, vin_min: str, startup_mj: str) -> dict:
    """Screen ideal steady-state energy and one buffered event at one ST sample.

    p(mW) * t(s) = E(mJ). Ecap(mJ) = C(uF)*(Vhi^2 - Vlo^2)/2000.
    P_ST is an author *point*, not a guaranteed continuously available value.
    The model does NOT cover field transients, startup current, ESR, converter
    efficiencies versus current, RF coexistence, FOD, heat, or switching time.
    """
    p = at(am, field)
    raw = (efficiency, baseline_mw, leakage_mw, event_mj, period_s,
           capacitance_effective_uf, v_storage_high, v_storage_low,
           vin_min, startup_mj)
    eta, idle, leak, event, period, cap, high, low, vin, startup = map(number, raw)
    if not (D("0") < eta <= D("1")):
        raise ValueError("0 < conversion efficiency <= 1 required")
    if idle < 0 or leak < 0 or event <= 0 or period <= 0 or cap <= 0 or startup < 0:
        raise ValueError("invalid nonnegative costs or positive period/event/cap")
    if low <= 0 or high <= low or vin <= 0:
        raise ValueError("invalid storage voltage range or converter VIN min")
    usable = p.p * eta
    net = usable - idle - leak
    radio_ave = event / period
    margin = net - radio_ave
    reservoir_mj = cap * (high * high - low * low) / D("2000")
    cap_min = D("2000") * event / (high * high - low * low)
    recharge_s = event / net if net > 0 else None
    cold_start_s = startup / net if net > 0 else None
    voltage_ok = p.v >= vin
    average_ok = margin >= 0
    buffer_ok = reservoir_mj >= event
    reasons = []
    if not voltage_ok:
        reasons.append("AUTHOR_POINT_BELOW_HYPOTHETICAL_CONVERTER_VIN")
    if not average_ok:
        reasons.append("STEADY_STATE_ENERGY_DEFICIT")
    if not buffer_ok:
        reasons.append("INSUFFICIENT_IDEAL_EFFECTIVE_STORAGE")
    if not reasons:
        reasons.append("CONDITIONAL_MATH_ONLY_NOT_HARDWARE_APPROVAL")
    def s(x: Decimal | None) -> str | None:
        return str(x) if x is not None else None
    return {
        "modulation": am,
        "field_A_per_m_rms_author_sample": str(p.h),
        "author_EH_mW_not_guaranteed": str(p.p),
        "author_EH_voltage_V_not_guaranteed": str(p.v),
        "hypothetical_conversion_efficiency": str(eta),
        "hypothetical_available_after_conversion_mW": s(usable),
        "hypothetical_baseline_plus_leakage_mW": s(idle + leak),
        "hypothetical_net_before_events_mW": s(net),
        "hypothetical_event_energy_mJ": s(event),
        "hypothetical_interval_s": s(period),
        "hypothetical_event_average_mW": s(radio_ave),
        "hypothetical_energy_margin_mW": s(margin),
        "hypothetical_effective_capacitance_uF": s(cap),
        "ideal_reservoir_event_energy_mJ": s(reservoir_mj),
        "ideal_min_effective_capacitance_uF": s(cap_min),
        "ideal_min_recharge_seconds": s(recharge_s),
        "ideal_cold_start_seconds_for_assumed_startup_energy": s(cold_start_s),
        "author_point_voltage_passes_assumed_vin": voltage_ok,
        "average_energy_conditionally_sustained": average_ok,
        "single_event_ideal_buffer_sufficient": buffer_ok,
        "screen_reasons": reasons,
        "datasheet_provenance": PROVENANCE,
        "author_source": SOURCE,
        "reader_input_power_known": False,
        "rf_application_ACK_privacy_recovery_verified": False,
        "converter_ESR_dynamic_and_offset_verified": False,
        "FOD_thermal_EMI_independent_cut_verified": False,
        "author_data_guaranteed_minimum": False,
        "bench_measurements_by_us": False,
        "hardware_release": "BLOCKED",
    }


def report() -> dict:
    common = dict(efficiency="0.8", baseline_mw="0.1", leakage_mw="0",
                  event_mj="1", period_s="1", capacitance_effective_uf="1200",
                  v_storage_high="3.3", v_storage_low="3.0",
                  vin_min="3.0", startup_mj="5")
    return {
        "milestone": "W-IND-87",
        "scope": "optional intermittent microsensor, not dock, lithium, motors or critical sensors",
        "AM100_weak_field_one_second": duty_gate(am="AM100", field="0.5", **common),
        "AM10_weak_field_one_second": duty_gate(am="AM10", field="0.5", **common),
        "AM10_weak_field_ten_seconds": duty_gate(am="AM10", field="0.5", **{**common, "period_s": "10"}),
        "AM10_three_A_per_m_vin_3v3": duty_gate(am="AM10", field="3", **{**common, "vin_min": "3.3"}),
        "field_offset_temperature_and_reader_load_unmeasured": True,
        "no_interpolation_or_extrapolation": True,
        "not_applicable_to_ST_radio_reliability": True,
        "hardware_release": "BLOCKED",
    }


if __name__ == "__main__":
    print(json.dumps(report(), sort_keys=True, ensure_ascii=False, indent=2))
