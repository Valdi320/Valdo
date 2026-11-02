"""W-IND-13: synthetic common-cause fault-tree for an OFF-state WPT TX.

Original, dependency-free Python model. NOT a circuit model, KiCad ERC, SPICE,
certification, or permission to power hardware. Every connectivity assumption
remains a hypothesis until checked in a real schematic and isolated bench.
"""
from dataclasses import dataclass
from enum import Enum
from itertools import combinations


class Wiring(str, Enum):
    SHARED_ENABLE = "shared_enable"
    SEPARATE_ENABLE = "separate_enable"
    SEPARATE_WITH_COMMON_LATCH = "separate_with_common_latch"


class Failure(str, Enum):
    WELD_A = "weld_a"
    WELD_B = "weld_b"
    SHARED_DRIVER_HIGH = "shared_driver_high"
    A_ENABLE_HIGH = "a_enable_high"
    B_ENABLE_HIGH = "b_enable_high"
    COMMON_LATCH_HIGH = "common_latch_high"
    BOARD_VIN_TX_BRIDGE = "board_vin_tx_bridge"
    AUX_TX_BRIDGE = "aux_tx_bridge"


@dataclass(frozen=True)
class Hypothesis:
    wiring: Wiring
    vin_present: bool = True
    aux_present: bool = False
    model_board_bridge: bool = True
    model_aux_bridge: bool = True

    def __post_init__(self):
        if not isinstance(self.wiring, Wiring):
            raise ValueError("wiring must be a Wiring enum")
        for field in ("vin_present", "aux_present", "model_board_bridge", "model_aux_bridge"):
            if type(getattr(self, field)) is not bool:
                raise ValueError(f"{field} must be bool")


def available_failures(h: Hypothesis) -> tuple[Failure, ...]:
    faults = [Failure.WELD_A, Failure.WELD_B]
    if h.wiring is Wiring.SHARED_ENABLE:
        faults.append(Failure.SHARED_DRIVER_HIGH)
    else:
        faults.extend([Failure.A_ENABLE_HIGH, Failure.B_ENABLE_HIGH])
        if h.wiring is Wiring.SEPARATE_WITH_COMMON_LATCH:
            faults.append(Failure.COMMON_LATCH_HIGH)
    if h.model_board_bridge:
        faults.append(Failure.BOARD_VIN_TX_BRIDGE)
    if h.model_aux_bridge and h.aux_present:
        faults.append(Failure.AUX_TX_BRIDGE)
    return tuple(sorted(faults, key=lambda x: x.value))


def off_state_tx_paths(h: Hypothesis, failures: frozenset[Failure]) -> tuple[str, ...]:
    """Return modeled source-to-TX path labels; do not equate empty with safe."""
    if type(failures) is not frozenset or any(not isinstance(f, Failure) for f in failures):
        raise ValueError("failures must be a frozenset[Failure]")
    if not failures.issubset(available_failures(h)):
        raise ValueError("failure set has events outside this hypothesis")
    common_on = ((h.wiring is Wiring.SHARED_ENABLE and Failure.SHARED_DRIVER_HIGH in failures)
                 or (h.wiring is Wiring.SEPARATE_WITH_COMMON_LATCH
                     and Failure.COMMON_LATCH_HIGH in failures))
    a_on = (Failure.WELD_A in failures or common_on
            or Failure.A_ENABLE_HIGH in failures)
    b_on = (Failure.WELD_B in failures or common_on
            or Failure.B_ENABLE_HIGH in failures)
    paths = []
    if h.vin_present and a_on and b_on:
        paths.append("VIN->CUT_A->MID->CUT_B->TX")
    if h.vin_present and Failure.BOARD_VIN_TX_BRIDGE in failures:
        paths.append("VIN->BOARD_BRIDGE->TX")
    if h.aux_present and Failure.AUX_TX_BRIDGE in failures:
        paths.append("AUX->BYPASS->TX")
    return tuple(paths)


def minimal_energizing_fault_sets(h: Hypothesis, max_faults: int = 3) -> tuple[frozenset[Failure], ...]:
    """Exhaustively enumerate inclusion-minimal energizing sets up to cap."""
    if type(max_faults) is not int or max_faults < 0 or max_faults > 5:
        raise ValueError("max_faults must be integer 0..5")
    available = available_failures(h)
    found: list[frozenset[Failure]] = []
    for n in range(1, min(max_faults, len(available)) + 1):
        for subset in combinations(available, n):
            s = frozenset(subset)
            if any(prev.issubset(s) for prev in found):
                continue
            if off_state_tx_paths(h, s):
                found.append(s)
    return tuple(found)


@dataclass(frozen=True)
class Screening:
    minimal_sets: tuple[frozenset[Failure], ...]
    single_fault_paths: tuple[frozenset[Failure], ...]
    model_covers_all_real_paths: bool = False
    hardware_approved: bool = False


def screen(h: Hypothesis) -> Screening:
    found = minimal_energizing_fault_sets(h)
    return Screening(found, tuple(x for x in found if len(x) == 1))


def demonstration() -> str:
    rows = []
    for wiring in Wiring:
        h = Hypothesis(wiring=wiring, aux_present=False, model_board_bridge=False)
        sets = minimal_energizing_fault_sets(h)
        names = ["+".join(sorted(x.value for x in fs)) for fs in sets]
        rows.append(f"{wiring.value}: {', '.join(names)}")
    rows.append("HARDWARE_APPROVED=False; board/aux paths excluded only for comparison")
    return "\n".join(rows)


if __name__ == "__main__":
    print(demonstration())
