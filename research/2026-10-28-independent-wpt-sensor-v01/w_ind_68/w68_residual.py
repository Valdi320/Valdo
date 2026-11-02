"""W68: post-cut residual TX-node energy screen. SYNTHETIC ONLY.

The existing W67 ideal DC graph deliberately excludes downstream capacitor
charge. A missing forward DC path is NOT a proof of de-energization.
No circuit, component value, thermal behavior or safe voltage is qualified.
Copyright 2026 VALDO contributors. No external source code copied.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import exp, isfinite
from tx_cut_power_screen import Interlocks, Switch, evaluate


@dataclass(frozen=True)
class ResidualCase:
    interlocks: Interlocks
    switch_a: Switch
    switch_b: Switch
    physical_source_present: bool = False
    reverse_feed_excluded: bool | None = None
    initial_downstream_v: float | None = None
    downstream_c_f: float | None = None
    independent_bleeder_ohm: float | None = None
    elapsed_s: float = 0.0
    screening_voltage_v: float = 0.5
    screening_energy_j: float = 0.001


@dataclass(frozen=True)
class Verdict:
    classification: str
    possible_forward_dc: bool
    voltage_at_t_v: float | None
    residual_j: float | None
    initial_j: float | None
    initial_bleeder_w: float | None
    hardware_approved: bool = False
    evidence_type: str = "SYNTHETIC_RC_TOPOLOGY_ONLY"

    def as_dict(self):
        return vars(self).copy()


def _finite_real(name: str, value, minimum: float, maximum: float):
    if type(value) not in (int, float) or not isfinite(value):
        raise ValueError(f"{name}: not finite real (bool forbidden)")
    if not minimum <= value <= maximum:
        raise ValueError(f"{name}: outside SCREENING model envelope")


def screen(case: ResidualCase) -> Verdict:
    """Conservative classification; never a physical no-energy or safety certificate.

    Model assumes one lumped capacitor ON THE TX SIDE OF BOTH series cuts,
    an ideal permanently connected independent bleeder, no other paths.
    These assumptions must be measured/checked separately before use.
    """
    if type(case) is not ResidualCase:
        raise TypeError("ResidualCase required")
    if type(case.physical_source_present) is not bool:
        raise ValueError("physical_source_present must be an exact bool")
    if case.reverse_feed_excluded is not None and type(case.reverse_feed_excluded) is not bool:
        raise ValueError("reverse-feed proof flag invalid")
    _finite_real("elapsed_s", case.elapsed_s, 0, 86400)
    _finite_real("screening_voltage_v", case.screening_voltage_v, 1e-6, 5.5)
    _finite_real("screening_energy_j", case.screening_energy_j, 1e-12, 100)
    fields = (
        ("initial_downstream_v", case.initial_downstream_v, 0, 5.5),
        ("downstream_c_f", case.downstream_c_f, 1e-9, 0.1),
        ("independent_bleeder_ohm", case.independent_bleeder_ohm, 1, 1e7),
    )
    for name, value, lo, hi in fields:
        if value is not None:
            _finite_real(name, value, lo, hi)
    electrical = evaluate(case.interlocks, case.switch_a, case.switch_b,
                          supply_present=case.physical_source_present)
    if electrical.supply_to_tx:
        return Verdict("FORWARD_SUPPLY_POSSIBLE", True, None, None, None, None)
    if case.reverse_feed_excluded is not True:
        return Verdict("BACKFEED_NOT_EXCLUDED", False, None, None, None, None)
    if any(value is None for _, value, _, _ in fields):
        return Verdict("STORAGE_OR_BLEED_UNKNOWN", False, None, None, None, None)

    v0 = float(case.initial_downstream_v)
    c = float(case.downstream_c_f)
    r = float(case.independent_bleeder_ohm)
    vt = v0 * exp(-float(case.elapsed_s) / (r * c))
    initial_j = 0.5 * c * v0 * v0
    residual_j = 0.5 * c * vt * vt
    initial_w = v0 * v0 / r
    above = vt >= float(case.screening_voltage_v) or residual_j >= float(case.screening_energy_j)
    return Verdict("RESIDUAL_ABOVE_HYPOTHETICAL_SCREEN" if above
                   else "BELOW_HYPOTHETICAL_SCREEN_NOT_SAFE",
                   False, vt, residual_j, initial_j, initial_w)
