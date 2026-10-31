"""W69 worst-case post-cut energy screen (original, purely hypothetical).

No circuit safety certification. Nodes must be electrically independent; no
charging, cross-coupling, foreign-object heating or transient faults modelled.
"""
from dataclasses import dataclass
from math import exp, isfinite


@dataclass(frozen=True)
class Node:
    name: str
    c_max_f: float
    v_max_v: float
    r_bleed_max_ohm: float | None
    bleeder_open_fault: bool = False


@dataclass(frozen=True)
class Case:
    nodes: tuple[Node, ...]
    elapsed_s: float
    source_cut_verified: bool
    backfeed_excluded: bool
    nodes_independent_verified: bool
    screening_v: float = 0.5
    screening_j: float = 0.001


def _numeric(name: str, value, low: float, high: float):
    if type(value) not in (int, float) or not isfinite(value) or not low <= value <= high:
        raise ValueError(f"{name} outside hypothetical model envelope")


def screen(case: Case) -> dict:
    """Return conservative upper bounds; NEVER approve construction or operation."""
    if type(case) is not Case or type(case.nodes) is not tuple or not 1 <= len(case.nodes) <= 32:
        raise ValueError("Case with 1..32 tuple nodes required")
    for field in ("source_cut_verified", "backfeed_excluded", "nodes_independent_verified"):
        if type(getattr(case, field)) is not bool:
            raise ValueError(f"{field} must be an exact bool")
    _numeric("elapsed_s", case.elapsed_s, 0, 86400)
    _numeric("screening_v", case.screening_v, 1e-6, 5.5)
    _numeric("screening_j", case.screening_j, 1e-12, 100)
    seen = set()
    for n in case.nodes:
        if type(n) is not Node or not isinstance(n.name, str) or not n.name or len(n.name) > 64 or n.name in seen:
            raise ValueError("Node type, unique name and length required")
        seen.add(n.name)
        if type(n.bleeder_open_fault) is not bool:
            raise ValueError("bleeder_open_fault must be an exact bool")
        _numeric("c_max_f", n.c_max_f, 1e-9, 0.1)
        _numeric("v_max_v", n.v_max_v, 0, 5.5)
        if n.r_bleed_max_ohm is not None:
            _numeric("r_bleed_max_ohm", n.r_bleed_max_ohm, 1, 1e7)

    result = {
        "evidence_type": "SYNTHETIC_INDEPENDENT_RC_UPPER_BOUND",
        "hardware_approved": False,
        "physical_tests": 0,
        "lithium_connected": False,
        "classification": None,
        "nodes": [],
        "total_energy_upper_j": None,
    }
    # These fields are assertions only, never inferred from RF or a simulated cutoff.
    if not case.source_cut_verified:
        result["classification"] = "SOURCE_CUT_UNVERIFIED"
        return result
    if not case.backfeed_excluded:
        result["classification"] = "BACKFEED_NOT_EXCLUDED"
        return result
    if not case.nodes_independent_verified:
        result["classification"] = "NODE_COUPLING_UNKNOWN"
        return result
    if any(n.r_bleed_max_ohm is None and not n.bleeder_open_fault for n in case.nodes):
        result["classification"] = "BLEED_PATH_UNKNOWN"
        return result

    total = 0.0
    above = False
    any_open = False
    for n in case.nodes:
        if n.bleeder_open_fault:
            any_open = True
            v = float(n.v_max_v)  # open resistor: no ideal discharge at all
        else:
            v = float(n.v_max_v) * exp(-case.elapsed_s / (n.c_max_f * n.r_bleed_max_ohm))
        e = 0.5 * n.c_max_f * v * v
        total += e
        above |= v >= case.screening_v or e >= case.screening_j
        result["nodes"].append({"name": n.name, "upper_voltage_v": v,
                                "upper_energy_j": e, "bleeder_open": n.bleeder_open_fault})
    result["total_energy_upper_j"] = total
    above |= total >= case.screening_j
    result["classification"] = ("OPEN_BLEEDER_FAULT" if any_open else
                                "RESIDUAL_ABOVE_HYPOTHETICAL_SCREEN" if above else
                                "BELOW_HYPOTHETICAL_SCREEN_NOT_SAFE")
    return result
