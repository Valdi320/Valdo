"""W-IND-86: manufacturer point-screen for one OPTIONAL NFC-powered microsensor.

No third-party code. Source *numbers* transcribed from ST AN4913 Rev 2 p.7,
Tables 4-5. Never equate manufacturer setup points with guaranteed minima.
No battery, dock, motor or safety-critical control is modeled.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import json

SOURCE = "https://www.st.com/resource/en/application_note/an4913-energy-harvesting-delivery-impact-on-st25dvi2c-series-behaviour-during-rf-communication-stmicroelectronics.pdf#page=7"
PROVENANCE = "manufacturer_characterization_point_not_guaranteed"

# (H_EH A/m rms, V_EH V, I_EH mA, P_EH mW); all 22 samples belong to ST.
_RAW = {
    "AM100": [
        ("0.5", "3.3", "0.7", "2.31"),
        ("1", "3.35", "0.7", "2.345"),
        ("1.5", "3.29", "0.7", "2.303"),
        ("2", "3.29", "0.7", "2.303"),
        ("2.5", "3.23", "0.9", "2.907"),
        ("3", "3.23", "0.9", "2.907"),
        ("3.5", "3.13", "1.3", "4.069"),
        ("4", "3.05", "1.7", "5.185"),
        ("4.5", "3.03", "1.9", "5.757"),
        ("5", "3.08", "2.3", "7.084"),
        ("5.5", "3.2", "2.7", "8.64"),
    ],
    "AM10": [
        ("0.5", "3.6", "0.1", "0.36"),
        ("1", "3.45", "0.3", "1.035"),
        ("1.5", "3.29", "0.7", "2.303"),
        ("2", "3.23", "0.9", "2.907"),
        ("2.5", "3.15", "1.1", "3.465"),
        ("3", "3.13", "1.3", "4.069"),
        ("3.5", "3.09", "1.5", "4.635"),
        ("4", "2.97", "2.1", "6.237"),
        ("4.5", "2.78", "3.3", "9.174"),
        ("5", "2.57", "4.5", "11.565"),
        ("5.5", "2.57", "4.9", "12.593"),
    ],
}
D = Decimal


def number(x: object) -> Decimal:
    """Reject bools, nonfinite, and malformed values; no silent float precision."""
    if isinstance(x, bool) or isinstance(x, float):
        raise ValueError("use decimal string or integer, not bool/float")
    try:
        n = D(str(x))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("not a decimal") from exc
    if not n.is_finite():
        raise ValueError("nonfinite")
    return n


@dataclass(frozen=True)
class Point:
    h: Decimal
    v: Decimal
    i: Decimal
    p: Decimal


def points(am: str) -> tuple[Point, ...]:
    if am not in _RAW:
        raise ValueError("AM only 100% or 10%, no interpolation")
    return tuple(Point(*(number(x) for x in row)) for row in _RAW[am])


def validate_points() -> bool:
    expected = tuple(D("0.5") * (k + 1) for k in range(11))
    for am in _RAW:
        data = points(am)
        if tuple(p.h for p in data) != expected:
            raise ValueError("missing, reordered or repeated sampled field")
        for p in data:
            if min(p.v, p.i, p.p) <= 0 or p.v * p.i != p.p:
                raise ValueError("point V*I/P mismatch or nonpositive")
    return True


def at(am: str, field: object) -> Point:
    h = number(field)
    for p in points(am):
        if p.h == h:
            return p
    raise ValueError("no author sample at this exact field; do not interpolate")


def screen(am: str, field: object, *, sensor_mw: object,
           efficiency: object, converter_vin_min_v: object) -> dict:
    """Conditional *point screen* of one hypothetical converter/sensor.

    Never a guarantee: the ST points are from one reader+ISO class 1 antenna.
    The converter's min VIN / efficiency here are INJECTED HYPOTHESES.
    """
    p = at(am, field)
    load, eff, vin = map(number, (sensor_mw, efficiency, converter_vin_min_v))
    if load <= 0 or eff <= 0 or eff > 1 or vin <= 0:
        raise ValueError("invalid positive load/efficiency/required VIN")
    useful = p.p * eff
    return {
        "am": am,
        "field_A_per_m_rms": str(p.h),
        "author_power_mW": str(p.p),
        "author_voltage_V": str(p.v),
        "hypothetical_useful_mW": str(useful),
        "power_meets_assumption": useful >= load,
        "voltage_meets_assumption": p.v >= vin,
        "point_meets_both_assumptions": useful >= load and p.v >= vin,
        "provenance": PROVENANCE,
        "hardware_release": "BLOCKED",
    }


def window(am: str, first_field: object, last_field: object, **assumptions: object) -> dict:
    """Evaluate *sampled points only* within a field window, not continuum."""
    a, b = number(first_field), number(last_field)
    if a > b:
        raise ValueError("reversed field window")
    # Endpoints must be in source table; unknown intermediate values are NEVER qualified.
    at(am, a)
    at(am, b)
    selected = [p for p in points(am) if a <= p.h <= b]
    found = [screen(am, p.h, **assumptions) for p in selected]
    return {
        "am": am,
        "field_window_sampled_endpoints": [str(a), str(b)],
        "sampled_points": len(found),
        "worst_observed_power_mW": str(min(p.p for p in selected)),
        "lowest_observed_voltage_V": str(min(p.v for p in selected)),
        "sampled_points_meeting_both": sum(p["point_meets_both_assumptions"] for p in found),
        "continuum_certified": False,
        "hardware_release": "BLOCKED",
    }


def compare_modulations(field: object) -> dict:
    a, b = at("AM100", field), at("AM10", field)
    return {
        "field_A_per_m_rms": str(a.h),
        "AM100_power_mW": str(a.p),
        "AM10_power_mW": str(b.p),
        "AM10_vs_AM100_power_ratio": str(b.p / a.p),
        "higher_power_at_this_author_point": ("AM100" if a.p > b.p else "AM10" if b.p > a.p else "EQUAL"),
        "both_rf_inventory_guaranteed_in_robot": False,
    }


def report() -> dict:
    validate_points()
    assumptions = {"sensor_mw": "2.9", "efficiency": "0.8", "converter_vin_min_v": "3.3"}
    winners = [compare_modulations(p.h) for p in points("AM100")]
    return {
        "milestone": "W-IND-86",
        "source": SOURCE,
        "manufacturer_revision": "AN4913 Rev 2, June 2021, Tables 4 and 5, p.7",
        "sampled_author_points_count": sum(len(points(am)) for am in _RAW),
        "measured_by_us": False,
        "hypothetical_case": assumptions,
        "observed_power_ranking": {"AM100": sum(r["higher_power_at_this_author_point"] == "AM100" for r in winners),
                                   "AM10": sum(r["higher_power_at_this_author_point"] == "AM10" for r in winners),
                                   "EQUAL": sum(r["higher_power_at_this_author_point"] == "EQUAL" for r in winners)},
        "critical_weak_field": compare_modulations("0.5"),
        "contrast_3A": compare_modulations("3"),
        "conditional_point_AM10_0_5": screen("AM10", "0.5", **assumptions),
        "conditional_point_AM10_3": screen("AM10", "3", **assumptions),
        "window_AM10_0_5_to_3": window("AM10", "0.5", "3", **assumptions),
        "window_AM100_0_5_to_3": window("AM100", "0.5", "3", **assumptions),
        "nonuniform_modulation_benefit": True,
        "no_guaranteed_field_or_converter_characterization": True,
        "radio_app_ack_privacy_and_recovery_qualified": False,
        "reader_input_watts_known": False,
        "temperature_FOD_EMI_moisture_offset_cutoff_qualified": False,
        "hardware_release": "BLOCKED",
    }


if __name__ == "__main__":
    print(json.dumps(report(), ensure_ascii=False, sort_keys=True, indent=2))
