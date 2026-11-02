"""W-IND-19: reject unsafe open-drain thermal interlocks (simulation only).

Independent robot, isolated low-power transmitter concept, 5 V nominal.
Nothing here is a physical sensor, power switch, charging controller, or
certified safety function. Fault inputs are synthetic and hardware unverified.
"""
from dataclasses import dataclass
from enum import Enum
from math import isfinite


class Level(Enum):
    SINK_LOW = "sink_low"
    RELEASED = "released"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Challenge:
    """Proof of witnessed LOW then RELEASED during a disarmed test.

    Inputs are synthetic; no TMP390 trip-test wiring or actual response tested.
    """
    low_observed: bool
    release_observed: bool
    completed_ms: int


@dataclass(frozen=True)
class ThermalChannel:
    """Model of *external* rail-health monitor + active-low thermal output.

    'rail_good' must come from a separately qualified hardwired monitor.
    It is not a software GPIO or a measurement made by the thermal IC itself.
    """
    rail_good: bool | None
    outa: Level
    challenge: Challenge | None


# Candidate only: TMP390A3 ±2 C maximum trip error between 0 and 70 C.
# Hysteresis, thermal path, temperature gradients, startup and latency are
# omitted, so trip_band() is NOT a guarantee of coil hotspot temperature.
HOT_SETPOINT_C = 50.0  # design assumption, no resistor selected
TRIP_ERROR_C = 2.0  # manufacturer A3 accuracy range 0 to 70 C
PROOF_MAX_AGE_MS = 1000  # arbitrary simulation requirement, NOT HW rated


def trip_band(temperature_c: float) -> str:
    """Compare sensor temperature against a *proposed* 50 C nominal trip.

    'certain_trip' means nominal + datasheet trip tolerance exceeded in a
    static, powered nominal scenario; it excludes dynamics and sensor placement.
    """
    if isinstance(temperature_c, bool):
        raise ValueError("temperature must be finite numeric")
    try:
        t = float(temperature_c)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("invalid temperature") from exc
    if not isfinite(t):
        raise ValueError("invalid temperature")
    if t < HOT_SETPOINT_C - TRIP_ERROR_C:
        return "clear_if_not_latched"
    if t >= HOT_SETPOINT_C + TRIP_ERROR_C:
        return "trip_if_powered"
    return "uncertain"


def direct_pullup_may_enable(outa: Level) -> bool:
    """Legacy candidate: pull-up directly driving active-high EN.

    Low inhibits; released is high. UNKNOWN (unpowered/open wire) can also be
    pulled high, i.e. a *possible unsafe enable*, not a guaranteed voltage.
    """
    if not isinstance(outa, Level):
        raise TypeError("invalid open-drain state")
    return outa is not Level.SINK_LOW


def channel_qualified(line: ThermalChannel, now_ms: int,
                      max_age_ms: int = PROOF_MAX_AGE_MS) -> bool:
    """Require independently indicated live rail and fresh low/high proof.

    The proof must be collected with transmitter hardware positively disabled;
    tests do NOT demonstrate that the real TMP390 test cycle is achievable.
    """
    if type(now_ms) is not int or now_ms < 0:
        raise ValueError("invalid monotonic clock")
    if type(max_age_ms) is not int or max_age_ms <= 0:
        raise ValueError("invalid proof lifetime")
    if not isinstance(line, ThermalChannel) or line.rail_good is not True:
        return False
    if line.outa is not Level.RELEASED or not isinstance(line.challenge, Challenge):
        return False
    p = line.challenge
    if p.low_observed is not True or p.release_observed is not True:
        return False
    if type(p.completed_ms) is not int or p.completed_ms < 0:
        return False
    age = now_ms - p.completed_ms
    return 0 <= age <= max_age_ms


def dual_hardwired_permission(a: ThermalChannel, b: ThermalChannel, *,
                              now_ms: int, local_request: bool = False,
                              fod_clear: bool | None = None,
                              overcurrent_clear: bool | None = None,
                              dry_clear: bool | None = None) -> bool:
    """Illustrative logic only: requires two *separately instrumented* cuts.

    No radio/ACK parameter can override local interlocks. 'True' fixture
    inputs are hypotheses, NOT evidence of FOD/current/wetness protection.
    There is no automatic rearm state machine or physical driver here.
    """
    return (local_request is True and fod_clear is True
            and overcurrent_clear is True and dry_clear is True
            and channel_qualified(a, now_ms)
            and channel_qualified(b, now_ms))


def proof_fixture(now_ms: int = 0) -> ThermalChannel:
    """Synthetic GOOD test stimulus only. Never interpret as real proof."""
    return ThermalChannel(True, Level.RELEASED, Challenge(True, True, now_ms))


if __name__ == "__main__":
    print("W-IND-19: direct pull-up with UNKNOWN line could enable:",
          direct_pullup_may_enable(Level.UNKNOWN))
    print("W-IND-19: hardwired model without any actual proofs remains OFF:",
          dual_hardwired_permission(ThermalChannel(None, Level.UNKNOWN, None),
              ThermalChannel(None, Level.UNKNOWN, None), now_ms=0))
