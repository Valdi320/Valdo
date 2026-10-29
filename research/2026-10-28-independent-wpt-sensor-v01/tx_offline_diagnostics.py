"""W-IND-14 — two-phase DC diagnostic of two OFF series TX cuts.

Original bench-only model for the *new independent robot*. This is a
conductance-matrix calculation, not SPICE, KiCad ERC, a device model,
validated sensor logic, or permission to energize a WPT transmitter.

Circuit *hypothesis* (all grounds common, no lithium or dock):

  V_IN -- R_A -- MID -- R_B -- TX -- R_TX_BLEED -- GND
                  |             |
               R_MID           R_LOAD(optional)
                  |             |
                 GND           GND

  V_PROBE -- R_PROBE -- MID only in SECOND diagnostic phase.

R_A/R_B are equivalent idealized resistor states; a MOSFET may have
parasitic diode/ESD paths which this model DOES NOT simulate.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from math import isfinite


class Verdict(str, Enum):
    MODEL_CONSISTENT = "MODEL_CONSISTENT_NOT_HARDWARE_APPROVAL"
    DENY = "DENY_OBSERVED_FAULT"
    HOLD = "HOLD_UNQUALIFIED_OR_AMBIGUOUS"


@dataclass(frozen=True)
class BenchHypothesis:
    vin_v: float = 5.0
    probe_v: float = 5.0
    r_a_ohm: float = 100_000_000.0    # idealized OFF state, not a datasheet guarantee
    r_b_ohm: float = 100_000_000.0
    r_mid_bleed_ohm: float = 22_000.0
    r_tx_bleed_ohm: float = 1_000.0
    r_probe_ohm: float = 10_000.0
    r_load_ohm: float | None = None
    r_aux_to_tx_ohm: float | None = None
    aux_v: float = 0.0
    sensor_error_v: float = 0.08
    mid_sensor_present: bool = True
    tx_sensor_present: bool = True
    supply_qualified: bool = True
    probe_available: bool = True

    def __post_init__(self):
        positive = ("r_a_ohm", "r_b_ohm", "r_mid_bleed_ohm",
                    "r_tx_bleed_ohm", "r_probe_ohm")
        for n in positive:
            v = getattr(self, n)
            if type(v) not in (float, int) or not isfinite(v) or v <= 0:
                raise ValueError(f"{n} must be positive and finite")
        for n in ("r_load_ohm", "r_aux_to_tx_ohm"):
            v = getattr(self, n)
            if v is not None and (type(v) not in (float, int) or not isfinite(v) or v <= 0):
                raise ValueError(f"{n} must be positive, finite or None")
        for n in ("vin_v", "probe_v", "aux_v", "sensor_error_v"):
            v = getattr(self, n)
            if type(v) not in (int, float) or not isfinite(v) or v < 0:
                raise ValueError(f"{n} must be finite and nonnegative")
        for n in ("mid_sensor_present", "tx_sensor_present", "supply_qualified", "probe_available"):
            if type(getattr(self, n)) is not bool:
                raise ValueError(f"{n} must be boolean")


@dataclass(frozen=True)
class Reading:
    vmid_v: float
    vtx_v: float
    source_current_a: float
    probe_current_a: float
    probe_active: bool


def dc_solve(h: BenchHypothesis, *, probe_active: bool) -> Reading:
    """Nodal DC solution for two nodes; no reactive components or timing."""
    if type(probe_active) is not bool:
        raise ValueError("probe_active must be boolean")
    ga, gb = 1 / h.r_a_ohm, 1 / h.r_b_ohm
    gm, gt = 1 / h.r_mid_bleed_ohm, 1 / h.r_tx_bleed_ohm
    gp = 1 / h.r_probe_ohm if probe_active else 0.0
    gl = 0.0 if h.r_load_ohm is None else 1 / h.r_load_ohm
    gx = 0.0 if h.r_aux_to_tx_ohm is None else 1 / h.r_aux_to_tx_ohm
    a11, a22 = ga + gb + gm + gp, gb + gt + gl + gx
    rhs1, rhs2 = ga * h.vin_v + gp * h.probe_v, gx * h.aux_v
    determinant = a11 * a22 - gb * gb
    if determinant <= 0 or not isfinite(determinant):
        raise ValueError("singular or ill-conditioned DC topology")
    mid = (rhs1 * a22 + gb * rhs2) / determinant
    tx = (a11 * rhs2 + gb * rhs1) / determinant
    return Reading(mid, tx, (h.vin_v - mid) * ga,
                   (h.probe_v - mid) * gp, probe_active)


@dataclass(frozen=True)
class DiagnosticResult:
    verdict: Verdict
    reason: str
    passive: Reading | None
    probe: Reading | None
    hardware_approved: bool = False
    covers_esd_body_diodes: bool = False
    proves_real_fod: bool = False


def diagnose(h: BenchHypothesis) -> DiagnosticResult:
    """No output can enable a real TX. Use a hard HOLD on any unknown evidence."""
    if not h.supply_qualified or not (4.5 <= h.vin_v <= 5.5):
        return DiagnosticResult(Verdict.HOLD, "unqualified VIN", None, None)
    if not (4.5 <= h.probe_v <= 5.5):
        return DiagnosticResult(Verdict.HOLD, "unqualified probe supply", None, None)
    if not h.mid_sensor_present or not h.tx_sensor_present:
        return DiagnosticResult(Verdict.HOLD, "missing node monitor", None, None)
    if h.sensor_error_v > 0.1 or not h.probe_available:
        return DiagnosticResult(Verdict.HOLD, "unknown monitor tolerance or probe", None, None)
    if not (9_000 <= h.r_probe_ohm <= 11_000):
        return DiagnosticResult(Verdict.HOLD, "probe current limit unqualified", None, None)
    if not (17_600 <= h.r_mid_bleed_ohm <= 26_400):
        return DiagnosticResult(Verdict.HOLD, "MID bleed unqualified", None, None)
    if not (900 <= h.r_tx_bleed_ohm <= 1100):
        return DiagnosticResult(Verdict.HOLD, "TX bleed unqualified", None, None)
    # Physical remote proof-of-off is still impossible from this model.
    p = dc_solve(h, probe_active=False)
    e = h.sensor_error_v
    if p.vmid_v - e > 0.25 or p.vtx_v - e > 0.25:
        return DiagnosticResult(Verdict.DENY, "passive node unexpectedly high", p, None)
    if p.vmid_v + e >= 0.25 or p.vtx_v + e >= 0.25:
        return DiagnosticResult(Verdict.HOLD, "passive node ambiguous", p, None)
    a = dc_solve(h, probe_active=True)
    if a.vmid_v + e < 2.5 or a.vtx_v - e > 0.25:
        return DiagnosticResult(Verdict.DENY, "active diagnostic incompatible with dual OFF cuts", p, a)
    if a.vmid_v - e <= 2.5 or a.vtx_v + e >= 0.25:
        return DiagnosticResult(Verdict.HOLD, "active diagnostic ambiguous", p, a)
    return DiagnosticResult(Verdict.MODEL_CONSISTENT,
                            "idealized DC nodes only; installation not approved", p, a)


def demonstration() -> str:
    from dataclasses import replace
    h = BenchHypothesis()
    for name, case in (("both modeled OFF", h),
                       ("CUT A welded", replace(h, r_a_ohm=0.1)),
                       ("CUT B welded", replace(h, r_b_ohm=0.1)),
                       ("both welded", replace(h, r_a_ohm=0.1, r_b_ohm=0.1))):
        r = diagnose(case)
        p = r.passive
        a = r.probe
        yield (f"{name:18s}: {r.verdict.value:40s} "
               f"passiveMID={p.vmid_v:.3f}V " if p else f"{name}: {r.verdict.value}") + \
              (f"probeMID={a.vmid_v:.3f}V probeTX={a.vtx_v:.3f}V" if a else "")


if __name__ == "__main__":
    print("\n".join(demonstration()))
