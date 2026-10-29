"""W-IND-25. Independent sub-500 mA analog trip *feasibility* envelope.

This is ORIGINAL deterministic arithmetic/logic. No comparator circuit/threshold
resistor is designed, powered or calibrated. All results are CONDITIONAL.
No real electrical tests, certification, permission to switch on, or FOD proof.
"""
from __future__ import annotations
from dataclasses import dataclass
import itertools
import json
import math

TI_INA301_A1 = "https://www.ti.com/product/INA301"
TI_TPS2521 = "https://www.ti.com/product/TPS2521"


@dataclass(frozen=True)
class Assumptions:
    normal_peak_a: float = 0.300
    fault_min_a: float = 0.400
    nominal_shunt_ohm: float = 0.100
    shunt_fraction: float = 0.01  # hypothetical selected 1% resistor
    gain_nominal: float = 20.0  # TI INA301A1 manufacturer nominal
    gain_error_fraction: float = 0.001 + 10e-6*60  # TI gain + 60C drift bound (illustrative)
    offset_input_v: float = 35e-6 + 0.5e-6*60  # TI offset max + 60C drift bound
    threshold_nominal_v: float = 0.700  # hypothetical comparator effective output threshold
    threshold_fraction: float = 0.01  # UNKNOWN effective tolerance, assumed only
    comparator_uncertainty_v: float = 0.010  # UNKNOWN, deliberately hypothetical


def validate(c: Assumptions) -> None:
    vals = tuple(vars(c).values())
    if any(not math.isfinite(v) for v in vals):
        raise ValueError("finite numeric values required")
    if (not 0 < c.normal_peak_a < c.fault_min_a or c.nominal_shunt_ohm <= 0
            or not 0 <= c.shunt_fraction < 1 or c.gain_nominal <= 0
            or not 0 <= c.gain_error_fraction < 1 or c.offset_input_v < 0
            or c.threshold_nominal_v <= 0 or not 0 <= c.threshold_fraction < 1
            or c.comparator_uncertainty_v < 0):
        raise ValueError("invalid unqualified envelope")


def signal_v(i_a: float, r_ohm: float, gain: float, offset_v: float) -> float:
    return (i_a * r_ohm + offset_v) * gain


def corner_screen(c: Assumptions = Assumptions()) -> dict:
    """Exhaustive 2^3 signed input corners at 300mA and 400mA.

    This is exact FOR THE ASSUMED BOX, not a statement about real IC
    comparator threshold error, thermal response, electrical isolation or PCB.
    """
    validate(c)
    def corners(i_a: float):
        return [signal_v(i_a,
                         c.nominal_shunt_ohm*(1+sr*c.shunt_fraction),
                         c.gain_nominal*(1+sg*c.gain_error_fraction),
                         so*c.offset_input_v)
                for sr, sg, so in itertools.product((-1, 1), repeat=3)]
    high_ok = max(corners(c.normal_peak_a))
    low_bad = min(corners(c.fault_min_a))
    threshold_min = c.threshold_nominal_v*(1-c.threshold_fraction)-c.comparator_uncertainty_v
    threshold_max = c.threshold_nominal_v*(1+c.threshold_fraction)+c.comparator_uncertainty_v
    is_separable = high_ok < threshold_min and low_bad > threshold_max
    return {
        "schema": "W-IND-25-v1", "candidate": "TI INA301A1 + resistor shunt + true reverse blocking eFuse",
        "assumed_normal_peak_a": c.normal_peak_a, "assumed_fault_min_a": c.fault_min_a,
        "expected_nominal_shunt_loss_mw_at_peak": round(c.normal_peak_a**2*c.nominal_shunt_ohm*1000, 6),
        "expected_nominal_shunt_loss_mw_at_fault": round(c.fault_min_a**2*c.nominal_shunt_ohm*1000, 6),
        "nominal_300ma_signal_v": round(signal_v(c.normal_peak_a,c.nominal_shunt_ohm,c.gain_nominal,0),6),
        "nominal_400ma_signal_v": round(signal_v(c.fault_min_a,c.nominal_shunt_ohm,c.gain_nominal,0),6),
        "max_healthy_signal_v_assumed": round(high_ok, 9),
        "min_fault_signal_v_assumed": round(low_bad, 9),
        "min_trip_threshold_v_assumed": round(threshold_min, 9),
        "max_trip_threshold_v_assumed": round(threshold_max, 9),
        "no_false_trip_margin_mv_assumed": round((threshold_min-high_ok)*1000, 6),
        "fault_detect_margin_mv_assumed": round((low_bad-threshold_max)*1000, 6),
        "threshold_window_exists_in_hypothetical_box": is_separable,
        "manufacturer_ina301_gain_cited": TI_INA301_A1,
        "manufacturer_efuse_ilim_min_0p5a_cited": TI_TPS2521,
        "effective_threshold_tolerance_verified": False,
        "limit_resistor_value_qualified": False,
        "comparator_power_rail_qualified": False,
        "shunt_part_verified": False,
        "cutoff_path_schematic_verified": False,
        "autonomous_fod_hardware_verified": False,
        "thermal_cut_hardware_verified": False,
        "coil_temperature_offset_emi_measured": False,
        "dock_battery_bms_connected": False,
        "physical_tests": 0,
        "hardware_approved": False, "power_on_allowed": False,
        "result": "CONDITIONAL_FEASIBILITY_ONLY_NOT_BUILT" if is_separable else "REJECT_ASSUMPTIONS_NOT_SEPARABLE",
    }


def independent_permission(*, source_healthy: bool, comparator_power_good: bool,
                           current_below_trip: bool, thermal_healthy: bool,
                           fod_healthy: bool, local_watchdog_healthy: bool) -> bool:
    """Fail-closed Boolean contract only; radio is deliberately not an input."""
    return all((source_healthy, comparator_power_good, current_below_trip,
                thermal_healthy, fod_healthy, local_watchdog_healthy))


def single_weld_interruptible(cut_a_welded: bool, cut_b_welded: bool) -> bool:
    """Ideal switch fault model: one good open can interrupt; common faults unmodeled."""
    return not (cut_a_welded and cut_b_welded)


def summary() -> dict:
    a=corner_screen()
    return {"assumed_box":vars(Assumptions()),"screen":a,
            "source_caveat":"TI INA301A1 gain/offset/drift facts; threshold tolerance & Rlimit unqualified",
            "independent_fault_cases":"powered-off monitor inhibits; both welded cuts cannot isolate",
            "hardware_approved":False,"power_on_allowed":False}

if __name__ == "__main__":
    print(json.dumps(summary(), sort_keys=True, indent=2))
