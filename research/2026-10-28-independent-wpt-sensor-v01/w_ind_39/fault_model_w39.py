"""Hypothetical Boolean single-fault analysis of two INA301 -> two TPS3840.
Independent open-drain alerts. No analog timing, thresholds or real chips tested.
"""
from dataclasses import dataclass
from itertools import product
from pathlib import Path
import argparse
import json

@dataclass(frozen=True)
class Case:
    overcurrent: bool = True
    shunt_valid: bool = True
    mon_a_alive: bool = True
    mon_b_alive: bool = True
    alert_a_connected: bool = True
    alert_b_connected: bool = True
    reset_a_path: bool = True
    reset_b_path: bool = True
    pg_3v3: bool = True
    pg_5v: bool = True
    local_armed: bool = True

def observe(c: Case):
    # Only for explicitly postulated over-threshold current. Component
    # tolerances, ramp, comparators' dynamics and individual VDD continuity
    # are OUTSIDE this model. Rail loss is modeled as an immediate PG event.
    alarm_a = bool(c.overcurrent and c.shunt_valid and
                   c.mon_a_alive and c.alert_a_connected and c.reset_a_path)
    alarm_b = bool(c.overcurrent and c.shunt_valid and
                   c.mon_b_alive and c.alert_b_connected and c.reset_b_path)
    pg_a = bool(c.pg_3v3 and not alarm_a)
    pg_b = bool(c.pg_5v and not alarm_b)
    both_cuts_requested_on = bool(c.local_armed and pg_a and pg_b)
    unsafe = bool(c.overcurrent and both_cuts_requested_on)
    return {"alarm_a": alarm_a, "alarm_b": alarm_b,
            "requested_en_a": both_cuts_requested_on,
            "requested_en_b": both_cuts_requested_on,
            "unsafe_overcurrent_permission": unsafe}

def study():
    singles = {}
    for key in ("mon_a_alive", "mon_b_alive", "alert_a_connected",
                "alert_b_connected", "reset_a_path", "reset_b_path"):
        c = Case(**{key: False})
        singles[key] = observe(c)["unsafe_overcurrent_permission"]
        assert not singles[key], key
    shared = {
        "shunt_bypassed": observe(Case(shunt_valid=False))["unsafe_overcurrent_permission"],
        "both_monitors_silent": observe(Case(mon_a_alive=False, mon_b_alive=False))["unsafe_overcurrent_permission"],
        "both_alerts_open": observe(Case(alert_a_connected=False, alert_b_connected=False))["unsafe_overcurrent_permission"],
    }
    assert all(shared.values())
    states = 0
    for ma, mb, wa, wb, pa, pb in product((False, True), repeat=6):
        c = Case(mon_a_alive=ma, mon_b_alive=mb, alert_a_connected=wa,
                 alert_b_connected=wb, reset_a_path=pa, reset_b_path=pb)
        result = observe(c)
        expected_unsafe = not ((ma and wa and pa) or (mb and wb and pb))
        assert result["unsafe_overcurrent_permission"] == expected_unsafe
        states += 1
    return {
        "schema": "VALDO-W39-IDEALISED-SINGLE-FAULT",
        "single_faults_covered_in_boolean_model": singles,
        "shared_failure_counterexamples": shared,
        "six_input_fault_combinations": states,
        "source_category": "ORIGINAL SOFTWARE / HYPOTHETICAL BOOLEAN",
        "no_physical_measurements": True,
        "no_timing_guarantee": True,
        "safe_to_energize": False
    }

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path)
    args = p.parse_args()
    result = study()
    if args.out:
        args.out.parent.mkdir(exist_ok=True, parents=True)
        args.out.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps(result, indent=2, sort_keys=True))
