"""W-IND-40: finite fault-tree screening, not a circuit or safety certificate.

Copyright 2026 VALDO contributors. Original Python (no upstream code copied).
All paths and faults are HYPOTHETICAL, including the proposed 3V3 PG.
The existing W39 PG assumption is *not* proof of an independent 3V3 PG.
"""
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
import argparse
import json

FAULTS = (
    "shared_shunt_bypassed", "shared_3v3_lost",
    "ina_a_silent", "ina_b_silent", "ina_c_silent",
    "alert_a_open", "alert_b_open", "alert_c_open",
    "reset_a_open", "reset_b_open", "reset_c_open",
    "cut_a_welded", "cut_b_welded", "rail_pg_stuck_healthy",
)


@dataclass(frozen=True)
class Architecture:
    name: str
    monitors: tuple = ("a", "b")
    independent_3v3_pg: bool = False
    # An incorrectly supplied PG from the failing 3V3 rail has NO credit.
    pg_power_independent: bool = False


W39 = Architecture("W39_two_INA_same_shunt_rail")
THIRD = Architecture("third_INA_same_shunt_rail", ("a", "b", "c"))
PG_SHARED = Architecture("PG_3v3_derived_from_3v3_INVALID", independent_3v3_pg=True)
PG_INDEPENDENT = Architecture("PG_3v3_supplied_independently_HYPOTHETICAL",
                              independent_3v3_pg=True, pg_power_independent=True)
ARCHITECTURES = (W39, THIRD, PG_SHARED, PG_INDEPENDENT)


def evaluate(architecture: Architecture, failed=frozenset()):
    """Logical output during a postulated overcurrent while source is present.

    WORST-CASE ASSUMPTION: missing 3V3 leaves the existing W39 permit
    apparently healthy unless a SEPARATELY POWERED supervisor forces OFF.
    This is a deliberate fault-injection bound, NOT a measurement of W39.
    Immediate tripping, perfect thresholds, and zero residual energy are
    simplifying assumptions; therefore even a 'safe' row is NOT qualification.
    """
    failed = frozenset(failed)
    if not failed <= set(FAULTS):
        raise ValueError("Unknown fault: " + repr(sorted(failed - set(FAULTS))))
    evidence = {}
    for node in architecture.monitors:
        evidence[node] = not any(x in failed for x in (
            "shared_shunt_bypassed", "shared_3v3_lost",
            f"ina_{node}_silent", f"alert_{node}_open", f"reset_{node}_open"
        ))
    local_trip_from_ina = any(evidence.values())
    independent_pg_trip = bool(
        architecture.independent_3v3_pg and architecture.pg_power_independent
        and "shared_3v3_lost" in failed
        and "rail_pg_stuck_healthy" not in failed
    )
    request_on = not (local_trip_from_ina or independent_pg_trip)
    # Two series cuts only stop current if at least one opens physically.
    physical_path_on = (
        (request_on or "cut_a_welded" in failed) and
        (request_on or "cut_b_welded" in failed)
    )
    return {
        "ina_alarm_paths": evidence,
        "separate_pg_trip_assumed": independent_pg_trip,
        "requested_on": request_on,
        "physical_path_on_in_ideal_series_model": physical_path_on,
        "unsafe_overcurrent_path": physical_path_on,
    }


def minimal_cutsets(architecture: Architecture, max_order=2):
    """Find minimal unsafe fault SETS (no probabilities or timing)."""
    if not 1 <= max_order <= len(FAULTS):
        raise ValueError("max_order out of range")
    cutsets = []
    for order in range(1, max_order + 1):
        for items in combinations(FAULTS, order):
            faultset = frozenset(items)
            if any(s <= faultset for s in cutsets):
                continue
            if evaluate(architecture, faultset)["unsafe_overcurrent_path"]:
                cutsets.append(faultset)
    return tuple(cutsets)


def report():
    results = {}
    for a in ARCHITECTURES:
        cuts = minimal_cutsets(a)
        exact_by_order = {str(k): sum(
            evaluate(a, items)["unsafe_overcurrent_path"]
            for items in combinations(FAULTS, k)
        ) for k in (0, 1, 2)}
        results[a.name] = {
            "exact_unsafe_states_by_fault_order": exact_by_order,
            "single_fault_cutsets": [sorted(s) for s in cuts if len(s) == 1],
            "double_fault_cutsets": [sorted(s) for s in cuts if len(s) == 2],
            "single_count": sum(len(s) == 1 for s in cuts),
            "double_count": sum(len(s) == 2 for s in cuts),
            "rail_failure_unsafe": evaluate(a, {"shared_3v3_lost"})["unsafe_overcurrent_path"],
            "shunt_bypass_unsafe": evaluate(a, {"shared_shunt_bypassed"})["unsafe_overcurrent_path"],
            "both_cuts_welded_unsafe": evaluate(a, {"cut_a_welded", "cut_b_welded"})["unsafe_overcurrent_path"],
        }
    return {
        "schema": "VALDO_W40_FAULT_TREE_V1",
        "input_origin": "SYNTHETIC_BOOLEAN_ASSUMPTIONS_ONLY",
        "faults_enumerated": len(FAULTS),
        "maximum_fault_order": 2,
        "nonmonotone_risk_note": "PG power-loss trip can make an unsafe 1-fault case safe when an additional rail-loss fault occurs; cutset counts do NOT imply a probability, likelihood or monotonic fault model.",
        "designs": results,
        "selected_change": "DO_NOT_ADD_THIRD_INA; REVIEW_INDEPENDENT_RAIL_PG_FIRST",
        "single_shunt_fault_uncovered": True,
        "existing_W39_independent_3v3_pg_proven": False,
        "hardware_qualified": False,
        "safe_to_energize": False,
        "physical_measurements": 0,
        "no_battery_or_motor_or_dock": True,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = report()
    payload = json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    print(payload, end="")
