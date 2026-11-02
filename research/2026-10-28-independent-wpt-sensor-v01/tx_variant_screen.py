"""W-IND-09: manufacturer-variant selection gate, NOT an electrical simulator.

Original VALDO educational code. No external source code/CAD incorporated.
Never interpret a matching silicon feature as permission to energize WPT.
"""
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class Variant:
    sku: str
    vin_min: float
    vin_max: float
    ilim_min_typ: float | None
    ilim_max_typ: float | None
    overcurrent_response: str
    rcb: bool
    reverse_trip_typ: float | None
    qod_ohm_typ: float | None
    qod_is_optional: bool
    ron_ohm_typ_at_5v: float
    source: str


TI_22950_DATASHEET = "https://www.ti.com/document-viewer/TPS22950/datasheet"
TI_22918 = "https://www.ti.com/product/TPS22918"
VARIANTS = {
    "TPS22950": Variant("TPS22950", 1.8, 5.5, .05, 3.5, "auto_retry", True,
                        .9, 150., False, .034, TI_22950_DATASHEET),
    "TPS22950L": Variant("TPS22950L", 1.8, 5.5, .5, 3.5, "latch_off", False,
                         None, 150., False, .034, TI_22950_DATASHEET),
    "TPS22950C": Variant("TPS22950C", 1.8, 5.5, .5, 3.5, "auto_retry", True,
                         .9, 150., False, .034, TI_22950_DATASHEET),
    "TPS22918": Variant("TPS22918", 1.0, 5.5, None, None, "none", False,
                        None, None, True, .052, TI_22918),
}


def validate_variant(v: Variant) -> None:
    numbers = [v.vin_min, v.vin_max, v.ron_ohm_typ_at_5v]
    numbers += [x for x in (v.ilim_min_typ, v.ilim_max_typ,
                            v.reverse_trip_typ, v.qod_ohm_typ) if x is not None]
    if (not all(isfinite(x) for x in numbers)
            or not 0 < v.vin_min < v.vin_max
            or v.ron_ohm_typ_at_5v < 0
            or (v.ilim_min_typ is None) != (v.ilim_max_typ is None)
            or (v.ilim_min_typ is not None and not 0 < v.ilim_min_typ <= v.ilim_max_typ)
            or (v.reverse_trip_typ is not None and v.reverse_trip_typ <= 0)
            or (v.qod_ohm_typ is not None and v.qod_ohm_typ <= 0)
            or v.overcurrent_response not in {"none", "auto_retry", "latch_off"}
            or not v.sku or not v.source.startswith("https://")):
        raise ValueError("invalid or incomplete component evidence")


def screen_sensor_rail(v: Variant, supply_v: float = 5.0,
                       nominal_limit_a: float = .4) -> dict:
    """Conservative feature audit; never an installation pass/fail certificate.

    ilim ranges and reverse-current thresholds are **typical** only; neither
    establishes worst-case current, thermal safety or physical FOD.
    """
    validate_variant(v)
    if (not all(isfinite(x) for x in (supply_v, nominal_limit_a))
            or supply_v <= 0 or nominal_limit_a <= 0):
        raise ValueError("invalid screen target")
    blockers = []
    if not v.vin_min <= supply_v <= v.vin_max:
        blockers.append("supply_outside_rated_range")
    if v.ilim_min_typ is None or v.ilim_max_typ is None:
        blockers.append("adjustable_current_limit_absent")
    elif not v.ilim_min_typ <= nominal_limit_a <= v.ilim_max_typ:
        blockers.append("target_below_or_above_typical_limit_range")
    if v.overcurrent_response == "auto_retry":
        blockers.append("fault_retries_without_independent_latch")
    elif v.overcurrent_response != "latch_off":
        blockers.append("no_overcurrent_latch")
    if not v.rcb:
        blockers.append("no_reverse_current_blocking")
    elif v.reverse_trip_typ is not None and v.reverse_trip_typ > nominal_limit_a:
        blockers.append("reverse_trip_typically_above_sensor_limit")
    if v.qod_ohm_typ is not None and not v.qod_is_optional:
        blockers.append("fixed_qod_short_fault_path_unresolved")
    return {
        "sku": v.sku,
        "blockers": tuple(blockers),
        "partial_evaluation_only": True,
        "hardware_approved": False,
        "real_fod_verified": False,
        "independent_cutoff_verified": False,
        "reverse_trip_value_is_typical_not_guaranteed": v.reverse_trip_typ is not None,
    }


def hypothetical_qod_weld(v: Variant, source_v: float,
                          pass_element_short: bool, on_command: bool) -> dict:
    """Only DC I=V/R under an *assumed* welded pass-FET and QOD-on failure.

    If QOD resistor is absent or intentionally unconnected, this MODEL has no
    QOD shunt. It makes no claims about other return paths or IC pin physics.
    """
    validate_variant(v)
    if not isfinite(source_v) or source_v < 0:
        raise ValueError("invalid voltage")
    active = pass_element_short and not on_command and v.qod_ohm_typ is not None
    if not active:
        return {"potential_shunt_a": 0., "potential_shunt_w": 0., "fault_scenario": False}
    return {"potential_shunt_a": source_v / v.qod_ohm_typ,
            "potential_shunt_w": source_v * source_v / v.qod_ohm_typ,
            "fault_scenario": True}


def typical_on_loss(v: Variant, current_a: float) -> float:
    """One-chip I^2 R at 5 V; not max loss/temperature qualification."""
    validate_variant(v)
    if not isfinite(current_a) or not 0 <= current_a <= 2.0:
        raise ValueError("unsupported illustrative current")
    return current_a * current_a * v.ron_ohm_typ_at_5v


if __name__ == "__main__":
    for part in VARIANTS.values():
        report = screen_sensor_rail(part)
        print(part.sku, "blockers=", ",".join(report["blockers"]))
    print("HARDWARE_APPROVED=False; no live TX, dock, lithium or FOD tests")
