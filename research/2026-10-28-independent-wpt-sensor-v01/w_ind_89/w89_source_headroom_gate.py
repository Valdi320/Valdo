"""W-IND-89: reject an optimistic NFC capacitor precharge before a RF energy ledger.

This is an original digital screen of *manufacturer samples*, not an electrical
model, component certification, or permission to energize hardware.
"""
from __future__ import annotations

from decimal import Decimal
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "w_ind_86"))
from w86_field_sweep import points, number, SOURCE, PROVENANCE

D = Decimal


def evaluate_point(point, *, topology: str, assumed_drop_v: str,
                   charge_target_v: str, operating_floor_v: str,
                   effective_cap_uf: str, eta: str, idle_mw: str,
                   event_mj: str, period_s: str, blackout_s: str,
                   burst_attempts: int) -> dict:
    """Single manufacturer point, fixed-load sample, constant-source hypothesis.

    A buck/linear assumed voltage drop is NOT a sourced part specification. It
    can change with current/temperature and the unregulated EH I-V curve. No
    boost path is assessed without a qualified real converter and measurements.
    """
    fields = [assumed_drop_v, charge_target_v, operating_floor_v,
              effective_cap_uf, eta, idle_mw, event_mj, period_s, blackout_s]
    drop, high, low, cap, eff, idle, event, period, gap = map(number, fields)
    if topology not in ("linear_or_buck", "boost_unqualified"):
        raise ValueError("topology must be explicit")
    if drop < 0 or high <= 0 or low <= 0 or low >= high or cap <= 0:
        raise ValueError("invalid source drop, voltage window or capacitance")
    if not (D("0") < eff <= 1) or idle < 0 or event <= 0 or period <= 0 or gap < 0 or gap > period:
        raise ValueError("invalid power, event or time")
    if type(burst_attempts) is not int or not (1 <= burst_attempts <= 32):
        raise ValueError("burst_attempts must be 1..32 integer")
    if point.v <= 0 or point.p <= 0 or not point.v.is_finite() or not point.p.is_finite():
        raise ValueError("invalid manufacturer sample")

    required_burst = event * burst_attempts + idle * gap
    ideal_w88_reserve = cap * (high * high - low * low) / D("2000")
    average_margin = point.p * eff * (period-gap) / period - idle - event * burst_attempts / period
    if topology == "boost_unqualified":
        conditional_voltage = None
        reaches_target = False
        reachable_reserve = None
        shortfall = None
        reasons = ["BOOST_OUTPUT_AND_INPUT_CURVES_UNQUALIFIED"]
    else:
        # At EXACT manufacturer loaded V_EH, not a guaranteed source ceiling.
        conditional_voltage = max(D("0"), point.v - drop)
        reaches_target = conditional_voltage > high  # require nonzero margin
        reached = min(high, conditional_voltage)
        reachable_reserve = cap * max(D("0"), reached * reached - low * low) / D("2000")
        shortfall = max(D("0"), required_burst - reachable_reserve)
        reasons = [] if reaches_target else ["CHARGE_TARGET_NOT_SUPPORTED_AT_THIS_SAMPLED_VOLTAGE"]
        if shortfall > 0:
            reasons.append("INITIAL_BURST_EXCEEDS_CONDITIONAL_REACHABLE_RESERVE")
    if average_margin <= 0:
        reasons.append("AVERAGE_ENERGY_NOT_SUSTAINABLE_AT_THIS_SAMPLE")
    # A pass here is an ideal algebraic conjunction, NOT a real WPT qualification.
    conditional_preflight = bool(reaches_target and shortfall == 0 and average_margin > 0)
    return {
        "field_A_per_m_rms": str(point.h),
        "sample_V_EH_V_not_minimum": str(point.v),
        "sample_P_EH_mW_not_minimum": str(point.p),
        "conditional_at_sample_after_drop_v": str(conditional_voltage) if conditional_voltage is not None else None,
        "charge_target_reachable_with_positive_margin_in_assumed_model": reaches_target,
        "hypothetical_average_margin_mW": str(average_margin),
        "ideal_W88_fully_precharged_reserve_mJ": str(ideal_w88_reserve),
        "conditional_at_sample_reachable_reserve_mJ": str(reachable_reserve) if reachable_reserve is not None else None,
        "hypothetical_burst_demand_mJ": str(required_burst),
        "conditional_at_sample_burst_shortfall_mJ": str(shortfall) if shortfall is not None else None,
        "conditional_preflight_pass_not_hardware": conditional_preflight,
        "reasons": reasons,
        "provenance": PROVENANCE,
        "source_voltage_is_guaranteed_minimum": False,
        "regulated_conductor_and_boot_measured": False,
        "hardware_release": "BLOCKED",
    }


def report() -> dict:
    assumptions = dict(topology="linear_or_buck", assumed_drop_v="0.20",
                       charge_target_v="3.30", operating_floor_v="3.00",
                       effective_cap_uf="1200", eta="0.8", idle_mw="0.1",
                       event_mj="1", period_s="1", blackout_s="0.1",
                       burst_attempts=1)
    bands = {am: [evaluate_point(p, **assumptions) for p in points(am)]
             for am in ("AM100", "AM10")}
    ideal_no_drop = {**assumptions, "assumed_drop_v": "0"}
    counterfactual = evaluate_point(points("AM100")[1], **ideal_no_drop)
    return {
        "milestone": "W-IND-89",
        "purpose": "precharge/headroom preflight before trusting W88 precharged RF ledger",
        "source": SOURCE,
        "source_revision": "ST AN4913 Rev2 June 2021 tables 4-5 p7; 22 manufacturer points",
        "assumptions_hypothetical": assumptions,
        "sampled_points_total": sum(map(len, bands.values())),
        "voltage_possible_points": {k: sum(x["charge_target_reachable_with_positive_margin_in_assumed_model"] for x in v)
                                    for k, v in bands.items()},
        "full_conditional_preflight_points": {k: sum(x["conditional_preflight_pass_not_hardware"] for x in v)
                                               for k, v in bands.items()},
        "W88_optimistic_start_0_5A_AM100": bands["AM100"][0],
        "AM10_0_5A_voltage_but_power": bands["AM10"][0],
        "zero_drop_counterfactual_AM100_1A": counterfactual,
        "headroom_and_power_sample_winners": [{"AM": k, "field_A_per_m_rms": x["field_A_per_m_rms"]}
                                               for k, v in bands.items() for x in v if x["conditional_preflight_pass_not_hardware"]],
        "important_limit": "Loaded V_EH samples are NOT source min/max or an I-V curve; dropout 0.20V is hypothetical. No path-level proof, cold-start, current-dependent dropout or physical validation.",
        "data_transport": "ESP-NOW/OpenThread distinct; ACK CRC epoch timeout encryption; RF cannot safety-stop",
        "charging_and_BMS": "out of scope, physically isolated",
        "next_discriminating_evidence": "measured loaded V_EH/I curve versus charge state, reader input, alignment and RF phases; regulator max dropout/boost efficiency/cold-start",
        "FOD_heat_EMI_independent_cut": "UNQUALIFIED",
        "hardware_release": "BLOCKED",
    }


if __name__ == "__main__":
    print(json.dumps(report(), sort_keys=True, indent=2, ensure_ascii=False))
