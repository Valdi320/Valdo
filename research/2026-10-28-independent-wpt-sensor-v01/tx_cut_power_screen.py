"""W-IND-08: non-energized analytical screen, NOT an electrical safety proof.

Copyright 2026 VALDO contributors. Original educational engineering model.
No external project code or manufacturer's CAD is included.

An experimental 5-V TX supply is represented as two independent active-high
high-side load switches in series. Their output is NOT assumed to decay
immediately when both contacts open. In particular a load switch's quick
output discharge (QOD) can create a *continuous* supply-to-ground path if
its pass element welds closed while its ON input is commanded low.

No physical FOD, temperature interlock, MCU authentication, component
failure probability or EMI physics is modeled. No actual hardware approval.
"""
from dataclasses import dataclass
from enum import Enum
from math import isfinite, log


class Fault(Enum):
    HEALTHY = "healthy"
    CLOSED = "pass_element_short"
    OPEN = "pass_element_open"
    ENABLE_HIGH = "enable_pin_stuck_high"


@dataclass(frozen=True)
class Interlocks:
    local_enable: bool = False
    source_ok: bool = False
    fod_proven_clear: bool = False
    temperature_a_ok: bool = False
    temperature_b_ok: bool = False
    wetness_clear: bool = False
    offset_ok: bool = False
    watchdog_a_ok: bool = False
    watchdog_b_ok: bool = False

    def permitted(self) -> bool:
        """Synthetic analog permit. FOD proven_clear has NO real sensor yet."""
        return all(vars(self).values())


@dataclass(frozen=True)
class Switch:
    fault: Fault = Fault.HEALTHY
    qod_connected: bool = False

    def enable_pin_high(self, commanded: bool) -> bool:
        return commanded or self.fault is Fault.ENABLE_HIGH

    def pass_closed(self, commanded: bool) -> bool:
        if self.fault is Fault.CLOSED:
            return True
        if self.fault is Fault.OPEN:
            return False
        return self.enable_pin_high(commanded)

    def discharge_active(self, commanded: bool) -> bool:
        return self.qod_connected and not self.enable_pin_high(commanded)


@dataclass(frozen=True)
class Result:
    command_on: bool
    a_closed: bool
    b_closed: bool
    supply_to_tx: bool
    supply_to_qod_a: bool
    supply_to_qod_b: bool

    @property
    def any_sustained_qod_shunt(self) -> bool:
        return self.supply_to_qod_a or self.supply_to_qod_b


def evaluate(interlocks: Interlocks, a: Switch, b: Switch) -> Result:
    """Idealized DC topology; no switch resistance or parasitic leakage."""
    cmd = interlocks.permitted()
    a_closed, b_closed = a.pass_closed(cmd), b.pass_closed(cmd)
    source = interlocks.source_ok
    return Result(
        cmd, a_closed, b_closed,
        source and a_closed and b_closed,
        source and a_closed and a.discharge_active(cmd),
        source and a_closed and b_closed and b.discharge_active(cmd),
    )


def prospective_shunt(v: float, qod_ohm: float) -> tuple[float, float]:
    """Illustrative I/P only; QOD resistance is an INPUT, not a TI guarantee."""
    if not all(isfinite(x) for x in (v, qod_ohm)) or v < 0 or qod_ohm <= 0:
        raise ValueError("invalid hypothetical shunt parameters")
    return v / qod_ohm, v * v / qod_ohm


def bleeder(v_start: float, v_end: float, resistance: float,
            capacitance_f: float) -> dict[str, float]:
    """Passive RC discharge with source fully isolated, absent external load."""
    if (not all(isfinite(x) for x in (v_start, v_end, resistance, capacitance_f))
            or not 0 < v_end < v_start or resistance <= 0 or capacitance_f <= 0):
        raise ValueError("invalid RC assumptions")
    return {
        "seconds_to_target": resistance * capacitance_f * log(v_start / v_end),
        "permanent_current_a": v_start / resistance,
        "permanent_bleeder_w": v_start * v_start / resistance,
        "initial_stored_j": 0.5 * capacitance_f * v_start * v_start,
    }


def series_switch_loss(input_v: float, load_a: float,
                       ron_each_ohm: float = 0.052) -> dict[str, float]:
    """Typical 5-V R_ON from TI TPS22918; not derated worst-case loss."""
    if (not all(isfinite(x) for x in (input_v, load_a, ron_each_ohm))
            or not 1.0 <= input_v <= 5.5 or not 0 <= load_a <= 2
            or ron_each_ohm < 0):
        raise ValueError("outside candidate manufacturer's basic rating")
    return {"series_drop_v": 2 * load_a * ron_each_ohm,
            "series_loss_w": 2 * load_a * load_a * ron_each_ohm,
            "load_voltage_v_typical": input_v - 2 * load_a * ron_each_ohm}


if __name__ == "__main__":
    inputs = Interlocks(True, True, True, True, True, True, True, True, True)
    no_qod = (Switch(), Switch())
    rc = bleeder(5, 0.5, 1000, 100e-6)
    loss = series_switch_loss(5, 1)
    print("synthetic_on=", evaluate(inputs, *no_qod).supply_to_tx)
    print("100uF_1kV_5to0.5_seconds=", round(rc["seconds_to_target"], 6))
    print("bleeder_mW=", round(rc["permanent_bleeder_w"] * 1000, 3))
    print("two_series_typical_mW_at_1A=", round(loss["series_loss_w"] * 1000, 3))
    print("PHYSICAL_APPROVAL=False; real FOD not selected")
