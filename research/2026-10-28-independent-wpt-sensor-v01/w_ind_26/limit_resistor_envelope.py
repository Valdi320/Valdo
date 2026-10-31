"""W-IND-26: INA301A1 LIMIT resistor worst-case *arithmetic*, not safety approval.

Own original code. Based on TI INA301 SBOS713A Rev A (2016), pp 5, 6, 16.
No sourced shunt MPN, powered circuitry, independent cutoff or FOD detection.
No radio can issue an emergency-power permission. No battery/BMS/dock.
"""
from dataclasses import dataclass
from itertools import product
import json
import math

TI_DATASHEET = "https://www.ti.com/lit/ds/symlink/ina301.pdf"
RLIMIT_CANDIDATE = "Vishay CRCW06038K66FKEA"  # not purchased

@dataclass(frozen=True)
class Envelope:
    normal_peak_a: float = 0.300  # prospective pilot load, NOT measured
    fault_min_a: float = 0.400  # hypothetical hazardous current, NOT measured
    rshunt_ohm: float = 0.100  # unselected 4-terminal MPN
    rshunt_initial_fraction: float = 0.01  # ASSUMPTION, unqualified over temperature
    rshunt_tcr_ppm_c: float = 200.0  # ASSUMPTION until exact shunt selected
    rlimit_ohm: float = 8660.0  # manufacturer resistor candidate; not fitted
    rlimit_initial_fraction: float = 0.01  # Vishay part catalog
    rlimit_tcr_ppm_c: float = 100.0  # Vishay part catalog, see BOM
    ilimit_nominal_a: float = 80e-6  # TI typical
    ilimit_min_a: float = 79.2e-6  # TI over full device operating temperature
    ilimit_max_a: float = 80.8e-6
    gain: float = 20.0  # TI INA301A1
    gain_fraction_25c: float = 0.001  # TI max at specified test conditions
    gain_drift_ppm_c: float = 10.0  # TI max
    offset_a1_input_25c_v: float = 125e-6  # CORRECT A1 max; 35uV is A3
    offset_drift_v_c: float = 0.5e-6  # TI max
    comparator_offset_25c_v: float = 3.5e-3  # TI INA301A1 at 25C
    unqualified_extra_threshold_v: float = 0.010  # ASSUMED 10mV, not vendor guarantee
    temperature_excursion_c: float = 100.0  # e.g. 25C -> 125C, not a measurement

def _validate(c: Envelope) -> None:
    values = vars(c).values()
    if any(not isinstance(x, (int,float)) or not math.isfinite(x) for x in values):
        raise ValueError("all inputs must be finite numeric values")
    if not (0 < c.normal_peak_a < c.fault_min_a and c.rshunt_ohm > 0
            and c.rlimit_ohm > 0 and c.gain > 0
            and 0 < c.ilimit_min_a <= c.ilimit_nominal_a <= c.ilimit_max_a
            and 0 <= c.temperature_excursion_c <= 100):
        raise ValueError("invalid current, resistor, gain, temperature or ILIMIT")
    for name in ("rshunt_initial_fraction", "rlimit_initial_fraction",
                 "gain_fraction_25c", "rshunt_tcr_ppm_c", "rlimit_tcr_ppm_c",
                 "gain_drift_ppm_c", "offset_a1_input_25c_v",
                 "offset_drift_v_c", "comparator_offset_25c_v",
                 "unqualified_extra_threshold_v"):
        if getattr(c, name) < 0:
            raise ValueError("negative tolerance/uncertainty")
    if (c.rshunt_initial_fraction + c.rshunt_tcr_ppm_c*1e-6*c.temperature_excursion_c >= 1
        or c.rlimit_initial_fraction + c.rlimit_tcr_ppm_c*1e-6*c.temperature_excursion_c >= 1
        or c.gain_fraction_25c + c.gain_drift_ppm_c*1e-6*c.temperature_excursion_c >= 1):
        raise ValueError("unphysical tolerance exceeds 100%")

def evaluate(c: Envelope = Envelope()) -> dict:
    """Exhaustive sign corners of a simplified monotonic static uncertainty box.

    Comparator temperature drift and EMI remain UNKNOWN: the extra 10mV is
    hypothetical and cannot convert this envelope into a rated specification.
    """
    _validate(c)
    dt = c.temperature_excursion_c
    rs_fraction = c.rshunt_initial_fraction + c.rshunt_tcr_ppm_c*1e-6*dt
    rl_fraction = c.rlimit_initial_fraction + c.rlimit_tcr_ppm_c*1e-6*dt
    gain_fraction = c.gain_fraction_25c + c.gain_drift_ppm_c*1e-6*dt
    vin_offset = c.offset_a1_input_25c_v + c.offset_drift_v_c*dt
    cmp_offset = c.comparator_offset_25c_v + c.unqualified_extra_threshold_v
    def signal_corners(current):
        return [(current*c.rshunt_ohm*(1+s*rs_fraction) + o*vin_offset)
                * c.gain*(1+g*gain_fraction)
                for s,g,o in product((-1,1), repeat=3)]
    def threshold_corners():
        return [c.rlimit_ohm*(1+r*rl_fraction)*ilim + o*cmp_offset
                for r,ilim,o in product((-1,1),
                                         (c.ilimit_min_a,c.ilimit_max_a),
                                         (-1,1))]
    good = signal_corners(c.normal_peak_a)
    bad = signal_corners(c.fault_min_a)
    thresholds = threshold_corners()
    tlo, thi, goodhi, badlo = min(thresholds),max(thresholds),max(good),min(bad)
    gain_max = c.gain*(1+gain_fraction)
    gain_min = c.gain*(1-gain_fraction)
    rshunt_max = c.rshunt_ohm*(1+rs_fraction)
    rshunt_min = c.rshunt_ohm*(1-rs_fraction)
    no_false_a = (tlo/gain_max-vin_offset)/rshunt_max
    certain_trip_a = (thi/gain_min+vin_offset)/rshunt_min
    margin_no_false_mv = 1000*(tlo-goodhi)
    margin_trip_mv = 1000*(badlo-thi)
    return {
        "schema":"W-IND-26-v1",
        "sources":{"ina301":TI_DATASHEET,
                   "resistor":"https://www.digikey.fr/en/products/detail/vishay-dale/CRCW06038K66FKEA/1174775"},
        "model_kind":"deterministic_static_corner_math_NOT_measured",
        "product":"INA301A1 only (not A3)",
        "max_a1_input_offset_25c_uv":c.offset_a1_input_25c_v*1e6,
        "rlimit_candidate":RLIMIT_CANDIDATE,
        "rlimit_ohm":c.rlimit_ohm,
        "nominal_limit_v":c.rlimit_ohm*c.ilimit_nominal_a,
        "nominal_trip_a":(c.rlimit_ohm*c.ilimit_nominal_a)/(c.gain*c.rshunt_ohm),
        "min_effective_threshold_v_assumed":tlo,
        "max_effective_threshold_v_assumed":thi,
        "max_healthy_output_v_assumed":goodhi,
        "min_fault_output_v_assumed":badlo,
        "no_false_trip_margin_mv_assumed":margin_no_false_mv,
        "fault_detect_margin_mv_assumed":margin_trip_mv,
        "certain_no_false_trip_below_a_assumed":no_false_a,
        "certain_trip_above_a_assumed":certain_trip_a,
        "all_static_corners":len(good)*len(thresholds)+len(bad)*len(thresholds),
        "hypothetical_window_positive":margin_no_false_mv>0 and margin_trip_mv>0,
        "shunt_mpn_qualified":False,
        "comparator_overtemperature_offset_qualified":False,
        "emi_transients_qualified":False,
        "alert_open_drain_to_cutoff_qualified":False,
        "autonomous_fod_and_thermal_qualified":False,
        "single_fault_and_rail_loss_safe":False,
        "radio_critical_cutoff_dependency":False,
        "dock_battery_bms_connected":False,
        "physical_measurements":0,
        "hardware_approved":False,
        "power_on_allowed":False
    }

if __name__ == "__main__":
    print(json.dumps({"configuration":vars(Envelope()),"result":evaluate()},
                     sort_keys=True,indent=2))
