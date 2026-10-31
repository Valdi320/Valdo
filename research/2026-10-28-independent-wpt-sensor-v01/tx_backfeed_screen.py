"""W-IND-12: directed DC-path screening for a NEW, independent WPT sensor.

Original VALDO study (2026). Standard library only. This is a deliberately
coarse *connectivity model*, not SPICE, PCB, firmware or a safety-rated FOD.

Proven absent physical paths must be established by actual component
characterization, not by setting a flag in this model. Unknown == possible.
There is no hardware-approval output.
"""
from collections import deque
from dataclasses import dataclass
from enum import Enum


class Fault(Enum):
    NORMAL = "normal"
    STUCK_CONDUCTING = "stuck_conducting"
    STUCK_OPEN = "stuck_open"


class PathState(Enum):
    NO_PATH_IN_MODEL = "no_path_in_model"
    POSSIBLE_UNVERIFIED = "possible_unverified"
    CONFIRMED_IN_MODEL = "confirmed_in_model"


@dataclass(frozen=True)
class Case:
    """Assumed switches A (VIN->MID), B (MID->TX), default commanded OFF.

    *_blocked true* means independently characterized as blocking DC reverse
    current while OFF. False means a conductive reverse path; None = unknown.
    The other tri-state fields represent possible *parallel* supply paths.
    Presence of an external TX energy source is an injected fault scenario,
    NOT an assertion that an inductive receiver galvanically connects to TX.
    """
    commanded_on: bool = False
    primary_present: bool = True
    aux_present: bool = False
    external_tx_present: bool = False
    cut_a: Fault = Fault.NORMAL
    cut_b: Fault = Fault.NORMAL
    a_reverse_blocked: bool | None = None
    b_reverse_blocked: bool | None = None
    aux_to_tx_conducts: bool | None = None
    tx_to_logic_conducts: bool | None = None

    def __post_init__(self) -> None:
        for name in ("commanded_on", "primary_present", "aux_present", "external_tx_present"):
            if type(getattr(self, name)) is not bool:
                raise ValueError(f"{name} must be a literal bool")
        for name in ("a_reverse_blocked", "b_reverse_blocked", "aux_to_tx_conducts", "tx_to_logic_conducts"):
            if getattr(self, name) is not None and type(getattr(self, name)) is not bool:
                raise ValueError(f"{name} must be bool or unknown None")
        if not isinstance(self.cut_a, Fault) or not isinstance(self.cut_b, Fault):
            raise ValueError("switch fault must be a Fault member")


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    conducts: bool | None
    label: str


@dataclass(frozen=True)
class Finding:
    state: PathState
    path: tuple[str, ...] = ()


@dataclass(frozen=True)
class Review:
    primary_to_tx: Finding
    aux_to_tx: Finding
    external_tx_to_primary: Finding
    external_tx_to_logic: Finding
    primary_to_mid: Finding
    off_path_requires_investigation: bool
    hardware_approved: bool = False


def _forward(fault: Fault, command: bool) -> bool:
    if fault is Fault.STUCK_CONDUCTING:
        return True
    if fault is Fault.STUCK_OPEN:
        return False
    return command


def _reverse(fault: Fault, proven_blocked: bool | None, command: bool) -> bool | None:
    if fault is Fault.STUCK_CONDUCTING:
        return True
    if fault is Fault.STUCK_OPEN:
        return False
    if command:
        return True  # conducting devices may conduct in either direction
    if proven_blocked is None:
        return None
    return not proven_blocked


def _edges(c: Case) -> tuple[Edge, ...]:
    return (
        Edge("VIN", "MID", _forward(c.cut_a, c.commanded_on), "cut_A_forward"),
        Edge("MID", "TX", _forward(c.cut_b, c.commanded_on), "cut_B_forward"),
        Edge("MID", "VIN", _reverse(c.cut_a, c.a_reverse_blocked, c.commanded_on), "cut_A_reverse"),
        Edge("TX", "MID", _reverse(c.cut_b, c.b_reverse_blocked, c.commanded_on), "cut_B_reverse"),
        Edge("AUX", "TX", c.aux_to_tx_conducts, "auxiliary_bypass"),
        Edge("EXT_TX", "TX", True, "external_injection"),
        Edge("TX", "LOGIC", c.tx_to_logic_conducts, "GPIO_ESD_or_aux_backfeed"),
    )


def _route(edges: tuple[Edge, ...], origin: str, target: str, unknown_as_conducting: bool) -> tuple[str, ...]:
    queue = deque([(origin, ())])
    seen = {origin}
    while queue:
        at, path = queue.popleft()
        if at == target:
            return path
        for edge in edges:
            if edge.source != at or edge.conducts is False:
                continue
            if edge.conducts is None and not unknown_as_conducting:
                continue
            if edge.target not in seen:
                seen.add(edge.target)
                queue.append((edge.target, path + (edge.label,)))
    return ()


def _finding(edges: tuple[Edge, ...], present: bool, origin: str, target: str) -> Finding:
    if not present:
        return Finding(PathState.NO_PATH_IN_MODEL)
    definite = _route(edges, origin, target, False)
    if definite:
        return Finding(PathState.CONFIRMED_IN_MODEL, definite)
    possible = _route(edges, origin, target, True)
    if possible:
        return Finding(PathState.POSSIBLE_UNVERIFIED, possible)
    return Finding(PathState.NO_PATH_IN_MODEL)


def review(c: Case) -> Review:
    """Fault-inject conceptual paths, never declare a circuit safe to energize.

    No-path means no connectivity under the ASSUMED edge states, NOT zero
    current/leakage, certified separation, sufficient FOD or validated PCB.
    """
    edges = _edges(c)
    primary = _finding(edges, c.primary_present, "VIN", "TX")
    aux = _finding(edges, c.aux_present, "AUX", "TX")
    reverse = _finding(edges, c.external_tx_present, "EXT_TX", "VIN")
    logic = _finding(edges, c.external_tx_present, "EXT_TX", "LOGIC")
    mid = _finding(edges, c.primary_present, "VIN", "MID")
    paths = (primary, aux, reverse, logic)
    needs_review = not c.commanded_on and any(f.state is not PathState.NO_PATH_IN_MODEL for f in paths)
    return Review(primary, aux, reverse, logic, mid, needs_review, False)


def demo() -> dict[str, str]:
    scenarios = {
        "both_off_no_aux": Case(a_reverse_blocked=True, b_reverse_blocked=True),
        "one_welded": Case(cut_a=Fault.STUCK_CONDUCTING, a_reverse_blocked=True, b_reverse_blocked=True),
        "both_welded": Case(cut_a=Fault.STUCK_CONDUCTING, cut_b=Fault.STUCK_CONDUCTING),
        "unknown_debug_bypass": Case(aux_present=True),
        "external_reverse_unknown": Case(external_tx_present=True),
        "external_reverse_blocked": Case(external_tx_present=True, a_reverse_blocked=True, b_reverse_blocked=True, tx_to_logic_conducts=False),
    }
    return {name: "HALT_REVIEW" if review(s).off_path_requires_investigation else "NO_PATH_ASSUMED_NOT_APPROVED"
            for name, s in scenarios.items()}


if __name__ == "__main__":
    for key, status in demo().items():
        print(f"{key}: {status}")
    print("HARDWARE_APPROVAL=False; tests prove only a graph algorithm")
