"""W-IND-88: analytic NFC harvesting blackout/retry screen. Original W code.

Author measurements come only from the attributed W86 transcription. This is
NOT a regulator, NFC reader, RF communication simulation or hardware approval.
"""
from __future__ import annotations

from decimal import Decimal
import json
from pathlib import Path
import sys

# Reference pre-existing own W86 data without duplicating the ST tables.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "w_ind_86"))
from w86_field_sweep import at, number, SOURCE, PROVENANCE

D = Decimal


def window_gate(*, am: str, field: str, eta: str, baseline_mw: str,
                event_mj: str, period_s: str, blackout_s: str,
                effective_cap_uf: str, storage_vhigh: str,
                storage_vstart: str, storage_vlow: str,
                attempts_by_cycle: list[int]) -> dict:
    """Ideal energy ledger; assume ZERO usable harvesting in a communication gap.

    One attempt debit occurs at the start of every period; events/retries are
    conservatively clustered. Time outside the blackout is assigned an ST
    single-point EH *sample* times a hypothetical efficiency, not guaranteed
    available power. The storage is lossless, zero-ESR and constant-effective-C.
    """
    p = at(am, field)
    eta, base, event, period, gap, cap, hi, initial, lo = map(
        number, (eta, baseline_mw, event_mj, period_s, blackout_s,
                 effective_cap_uf, storage_vhigh, storage_vstart,
                 storage_vlow))
    if not (D("0") < eta <= D("1")):
        raise ValueError("eta must lie in (0,1]")
    if base < 0 or event <= 0 or period <= 0 or gap < 0 or gap > period or cap <= 0:
        raise ValueError("invalid load, time or capacitance")
    if not (D("0") < lo < initial <= hi):
        raise ValueError("storage voltage ordering must be 0 < low < start <= high")
    if type(attempts_by_cycle) is not list or not (1 <= len(attempts_by_cycle) <= 1024):
        raise ValueError("cycles must be nonempty bounded list")
    if any(type(n) is not int or n < 0 or n > 32 for n in attempts_by_cycle):
        raise ValueError("attempt count must be an integer between 0 and 32")

    energy_per_uf_mj = (hi * hi - lo * lo) / D("2000")
    capacity = cap * energy_per_uf_mj
    stored = cap * (initial * initial - lo * lo) / D("2000")
    live_input = p.p * eta
    live_net = live_input - base
    start_energy = stored
    trace = []
    failure = None
    min_energy = stored

    for cycle, attempts in enumerate(attempts_by_cycle, start=1):
        before = stored
        debit_events = event * attempts
        after_events = before - debit_events
        after_gap = after_events - base * gap
        min_energy = min(min_energy, after_events, after_gap)
        if after_events < 0:
            failure = {"cycle": cycle, "stage": "BURST", "deficit_mJ": str(-after_events)}
            trace.append({"cycle": cycle, "attempts": attempts, "before_mJ": str(before),
                          "after_events_mJ": str(after_events), "after_blackout_mJ": str(after_gap),
                          "after_recharge_mJ": None})
            break
        if after_gap < 0:
            failure = {"cycle": cycle, "stage": "RF_BLACKOUT", "deficit_mJ": str(-after_gap)}
            trace.append({"cycle": cycle, "attempts": attempts, "before_mJ": str(before),
                          "after_events_mJ": str(after_events), "after_blackout_mJ": str(after_gap),
                          "after_recharge_mJ": None})
            break
        recharge = live_net * (period - gap)
        raw_after_recharge = after_gap + recharge
        min_energy = min(min_energy, raw_after_recharge)
        trace.append({"cycle": cycle, "attempts": attempts, "before_mJ": str(before),
                      "after_events_mJ": str(after_events), "after_blackout_mJ": str(after_gap),
                      "after_recharge_mJ": str(min(capacity, raw_after_recharge))})
        if raw_after_recharge < 0:
            failure = {"cycle": cycle, "stage": "RECHARGE_WINDOW", "deficit_mJ": str(-raw_after_recharge)}
            break
        stored = min(capacity, raw_after_recharge)

    total_attempts = sum(attempts_by_cycle)
    total_periods = len(attempts_by_cycle)
    total_harvest = live_input * (period - gap) * total_periods
    total_demand = base * period * total_periods + event * total_attempts
    average_margin_mw = (total_harvest - total_demand) / (period * total_periods)
    max_attempts_full = max(0, int((capacity - base * gap) // event))
    maximum_attempts = max(attempts_by_cycle)
    min_cap_to_survive_worst_gap = (event * maximum_attempts + base * gap) / energy_per_uf_mj

    return {
        "milestone": "W-IND-88",
        "modulation": am,
        "author_field_A_per_m_rms_sample": str(p.h),
        "author_EH_mW_sample_not_guaranteed": str(p.p),
        "author_EH_voltage_V_sample_not_guaranteed": str(p.v),
        "hypothetical_eta": str(eta),
        "hypothetical_baseline_mW": str(base),
        "hypothetical_one_attempt_energy_mJ": str(event),
        "hypothetical_rf_blackout_s_per_cycle": str(gap),
        "hypothetical_period_s": str(period),
        "hypothetical_precharged_start_v": str(initial),
        "hypothetical_effective_cap_uF": str(cap),
        "ideal_storage_capacity_mJ": str(capacity),
        "ideal_start_energy_mJ": str(start_energy),
        "ideal_live_net_mW": str(live_net),
        "ideal_average_energy_margin_mW": str(average_margin_mw),
        "ideal_max_attempts_in_one_blackout_from_full_storage": max_attempts_full,
        "ideal_min_effective_cap_uF_for_worst_cluster": str(min_cap_to_survive_worst_gap),
        "ideal_min_energy_mJ_seen": str(min_energy),
        "ideal_final_energy_mJ_if_survived": str(stored) if failure is None else None,
        "ideal_cycles_completed": len(trace) if failure is None else len(trace) - 1,
        "ideal_window_pass": failure is None,
        "first_failure": failure,
        "trace": trace,
        "author_source": SOURCE,
        "author_provenance": PROVENANCE,
        "rf_energy_during_communication_assumed_mW": "0",
        "RF_app_ACK_seq_timeout_privacy_recovery_validated": False,
        "RF_simultaneous_energy_and_communication_validated": False,
        "reader_input_and_alignment_measured_by_us": False,
        "real_effective_cap_ESR_startup_regulator_measured": False,
        "FOD_temperature_EMI_and_independent_cut_verified": False,
        "dock_BMS_lithium_in_scope": False,
        "hardware_release": "BLOCKED",
    }


def report() -> dict:
    base = dict(eta="0.8", baseline_mw="0.1", event_mj="1", period_s="1",
                blackout_s="0.1", effective_cap_uf="1200", storage_vhigh="3.3",
                storage_vstart="3.3", storage_vlow="3.0")
    return {
        "milestone": "W-IND-88",
        "scope": "OPTIONAL noncritical intermittent NFC microsensor; no batteries, BMS, motors or dock",
        "AM100_one_attempt_3_cycles": window_gate(am="AM100", field="0.5", attempts_by_cycle=[1, 1, 1], **base),
        "AM100_one_retry_first_cycle": window_gate(am="AM100", field="0.5", attempts_by_cycle=[2, 1, 1], **base),
        "AM10_one_attempt_3_cycles": window_gate(am="AM10", field="0.5", attempts_by_cycle=[1, 1, 1], **base),
        "AM10_one_attempt_each_10_seconds": window_gate(am="AM10", field="0.5", attempts_by_cycle=[1, 1, 1], **{**base, "period_s": "10"}),
        "data_source_limit": "ST AN4913 Rev2 June2021 table sample, NOT power during RF exchanges",
        "all_physical_gates": "BLOCKED",
        "hardware_release": "BLOCKED",
    }


if __name__ == "__main__":
    print(json.dumps(report(), sort_keys=True, ensure_ascii=False, indent=2))
