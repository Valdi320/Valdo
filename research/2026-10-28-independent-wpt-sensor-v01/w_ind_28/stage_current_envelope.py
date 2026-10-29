"""W-IND-28: conservation-of-power check before placing a current-sense shunt.
All efficiencies and loads are invented pilot scenarios, NOT measured.
No circuit, RF simulation, hardware approval, or lithium charging.
"""
from dataclasses import dataclass, asdict
import math
import json

@dataclass(frozen=True)
class Pilot:
    tx_input_v: float = 5.0
    rx_output_v: float = 5.0
    rx_good_peak_a: float = 0.300
    rx_fault_min_a: float = 0.400
    eta_min: float = 0.55
    eta_max: float = 0.90
    auxiliary_min_w: float = 0.0
    auxiliary_max_w: float = 0.0
    previous_rx_nominal_limit_a: float = 0.3464

def validate(p: Pilot) -> None:
    vals = asdict(p)
    if any(isinstance(v,bool) or not isinstance(v,(int,float)) or
           not math.isfinite(v) for v in vals.values()):
        raise ValueError("finite real numbers required")
    if not (p.tx_input_v>0 and p.rx_output_v>0 and
            0<p.rx_good_peak_a<p.rx_fault_min_a and
            0<p.eta_min<=p.eta_max<=1 and
            0<=p.auxiliary_min_w<=p.auxiliary_max_w and
            p.previous_rx_nominal_limit_a>0):
        raise ValueError("invalid pilot")

def input_current(p: Pilot, rx_current_a: float, eta: float, auxiliary_w: float=0) -> float:
    validate(p)
    for value in (rx_current_a,eta,auxiliary_w):
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
            raise ValueError("invalid operating point")
    if rx_current_a<0 or not 0<eta<=1 or auxiliary_w<0:
        raise ValueError("out of domain")
    return (p.rx_output_v*rx_current_a/eta+auxiliary_w)/p.tx_input_v

def evaluate(p: Pilot=Pilot()) -> dict:
    validate(p)
    good_low=input_current(p,p.rx_good_peak_a,p.eta_max,p.auxiliary_min_w)
    good_high=input_current(p,p.rx_good_peak_a,p.eta_min,p.auxiliary_max_w)
    fault_low=input_current(p,p.rx_fault_min_a,p.eta_max,p.auxiliary_min_w)
    fault_high=input_current(p,p.rx_fault_min_a,p.eta_min,p.auxiliary_max_w)
    return {
        "schema":"W-IND-28-stage-current-v1",
        "evidence":"HYPOTHETICAL_STEADY_STATE_POWER_ARITHMETIC_NOT_MEASURED",
        "parameters":asdict(p),
        "rx_healthy_output_power_w":p.rx_output_v*p.rx_good_peak_a,
        "rx_fault_output_power_w":p.rx_output_v*p.rx_fault_min_a,
        "tx_healthy_input_current_a":{"minimum":good_low,"maximum":good_high},
        "tx_fault_input_current_a":{"minimum":fault_low,"maximum":fault_high},
        "tx_fixed_trip_window_a":{"must_be_greater_than":good_high,
                                  "must_be_at_most":fault_low},
        "tx_trip_window_width_a":fault_low-good_high,
        "tx_can_separate_rx_current_states_with_one_trip":good_high<fault_low,
        "receiver_nominal_candidate_window_a":{"must_be_greater_than":p.rx_good_peak_a,
                                               "must_be_at_most":p.rx_fault_min_a},
        "former_346p4ma_trip_inevitably_falsely_blocks_some_good_TX_cases":
            p.previous_rx_nominal_limit_a<=good_high,
        "good_TX_current_at_75_percent_efficiency_a":
            input_current(p,p.rx_good_peak_a,.75),
        "ideal_required_min_eta_to_separate_without_aux":
            p.rx_good_peak_a/p.rx_fault_min_a*p.eta_max,
        "location_of_shunt_selected":False,
        "independent_primary_fod_thermal_trip_qualified":False,
        "receiver_brownout_failure_qualified":False,
        "radio_used_for_safety_stop":False,
        "real_tests":0,
        "lithium_or_dock_connected":False,
        "power_on_approved":False,
    }

def report() -> dict:
    return {
        "hypothetical_55_to_90_percent":evaluate(),
        "hypothetical_80_to_90_percent":evaluate(Pilot(eta_min=.80)),
        "added_uncertain_tx_auxiliary_watts":evaluate(Pilot(auxiliary_max_w=.05)),
        "sources":{"prior_W27":"../w_ind_27/README_W_IND_27.md",
                   "INA301":"https://www.ti.com/lit/ds/symlink/ina301.pdf",
                   "author_WPT_not_transferred_to_our_robot":
                       "https://github.com/mark-belbin/simple-wireless-power"}
    }

if __name__=="__main__":
    print(json.dumps(report(),indent=2,sort_keys=True))
