"""W-IND-42: idealized positive-health line counterexample model (NO hardware).

Compare an active-low OPEN-DRAIN fault output with pull-up against a
positive-drive push-pull HEALTHY output with a downstream pull-down.
Only the PG wire's fault semantics are studied; no analog propagation,
FOD, charging, BMS, EMC or real hardware safety is implied.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from enum import Enum
from itertools import product
import json
from pathlib import Path


class Topology(str, Enum):
    OD_FAULT_LOW_PULLUP = 'od_fault_low_pullup'
    PP_HEALTH_HIGH_PULLDOWN = 'pp_health_high_pulldown'


class Fault(str, Enum):
    NONE = 'none'
    LINE_OPEN = 'line_open'
    MONITOR_UNPOWERED = 'monitor_unpowered'
    DRIVER_STUCK_HIZ = 'driver_stuck_hiz'
    DRIVER_STUCK_HIGH = 'driver_stuck_high'
    SHORT_TO_HIGH = 'short_to_high'
    SHORT_TO_GND = 'short_to_gnd'
    SUPERVISOR_FALSE_HEALTHY = 'supervisor_false_healthy'


@dataclass(frozen=True)
class Inputs:
    rail_3v3_healthy: bool
    precut_5v_qualified: bool
    armed_by_local_action: bool
    other_local_interlocks_ok: bool
    fault: Fault = Fault.NONE

    def __post_init__(self):
        # Exact booleans prevent accidental truthiness of strings or integers.
        for n in ('rail_3v3_healthy', 'precut_5v_qualified',
                  'armed_by_local_action', 'other_local_interlocks_ok'):
            if type(getattr(self, n)) is not bool:
                raise TypeError(n + ' must be a bool')
        if not isinstance(self.fault, Fault):
            raise TypeError('fault must be a Fault')


def health_pin_high(topology: Topology, x: Inputs) -> bool:
    """Receiver voltage reduced to HIGH/LOW under explicitly IDEAL pull network.

    - OD fault alert: HIGH means *released*, not actively proven good.
    - PP healthy: HIGH needs an active driver, otherwise pull-down yields LOW.
    - A hard short-to-high/stuck-high still defeats both topologies.
    - This model assumes no phantom supply, no leakage exceeding the pull
      network's input threshold, and valid logic-level translation.
    """
    if not isinstance(topology, Topology):
        raise TypeError('invalid topology')
    if x.fault in (Fault.SHORT_TO_HIGH, Fault.DRIVER_STUCK_HIGH,
                   Fault.SUPERVISOR_FALSE_HEALTHY):
        return True
    if x.fault is Fault.SHORT_TO_GND:
        return False
    if topology is Topology.OD_FAULT_LOW_PULLUP:
        if x.fault in (Fault.LINE_OPEN, Fault.MONITOR_UNPOWERED,
                       Fault.DRIVER_STUCK_HIZ):
            return True  # floating/released input pulled UP: dangerous
        return x.rail_3v3_healthy  # an alert sinks only on detected fault
    if x.fault in (Fault.LINE_OPEN, Fault.MONITOR_UNPOWERED,
                   Fault.DRIVER_STUCK_HIZ):
        return False  # floating/unpowered input pulled DOWN
    return x.rail_3v3_healthy


def evaluate(topology: Topology, x: Inputs) -> dict:
    signal_high = health_pin_high(topology, x)
    # Independent 5V qualification and existing manual latch are IDEAL
    # prerequisites, not new actual components validated by this model.
    permission = bool(signal_high and x.precut_5v_qualified
                      and x.armed_by_local_action and x.other_local_interlocks_ok)
    return {
        'health_high_ideal': signal_high,
        'request_on_ideal': permission,
        'unsafe_request_when_rail_bad': permission and not x.rail_3v3_healthy,
        'unobserved_monitor_death': (permission and x.fault is Fault.MONITOR_UNPOWERED),
    }


def resistor_screen(pulldown_ohms: int, source_high_volts: float,
                    hypothetical_max_leakage_ua: float = 1.0,
                    hypothetical_low_threshold_volts: float = 0.8) -> dict:
    """DC IDEAL calculation only. Neither bias nor logic threshold is qualified."""
    if pulldown_ohms <= 0 or source_high_volts <= 0 or hypothetical_max_leakage_ua < 0:
        raise ValueError('invalid electrical assumptions')
    i_ua = source_high_volts * 1e6 / pulldown_ohms
    v_leak = pulldown_ohms * hypothetical_max_leakage_ua * 1e-6
    return {
        'pulldown_ohms': pulldown_ohms,
        'source_high_volts_hypothetical': source_high_volts,
        'sourcing_current_microamps_ideal': round(i_ua, 6),
        'sourcing_power_mw_ideal': round(source_high_volts**2 / pulldown_ohms * 1e3, 6),
        'open_wire_high_due_to_leak_volts_hypothetical': round(v_leak, 6),
        'below_hypothetical_low_threshold': v_leak < hypothetical_low_threshold_volts,
        'logic_input_and_leakage_characterized': False,
    }


def evidence() -> dict:
    all_cases = []
    per_topology = {}
    for topology in Topology:
        hazardous = []
        all_count = 0
        for healthy, v5, armed, others, fault in product(
            (False, True), (False, True), (False, True), (False, True), Fault
        ):
            x = Inputs(healthy, v5, armed, others, fault)
            result = evaluate(topology, x)
            all_count += 1
            if result['unsafe_request_when_rail_bad']:
                hazardous.append({'fault': fault.value, '3v3_healthy': healthy,
                                  '5v_qualified': v5, 'armed': armed,
                                  'other_local_interlocks': others})
        per_topology[topology.value] = {
            'enumerated_cases': all_count,
            'unsafe_requests_3v3_bad': len(hazardous),
            'unsafe_faults_when_armed_5v_good': sorted(set(x['fault'] for x in hazardous)),
            'unsafe_cases': hazardous,
            'line_open_3v3_bad': evaluate(topology, Inputs(False, True, True, True, Fault.LINE_OPEN)),
            'monitor_unpowered_3v3_bad': evaluate(topology, Inputs(False, True, True, True, Fault.MONITOR_UNPOWERED)),
            'stuck_high_3v3_bad': evaluate(topology, Inputs(False, True, True, True, Fault.DRIVER_STUCK_HIGH)),
        }
    return {
        'schema': 'VALDO_W_IND_42_POSITIVE_HEALTH_DIAGNOSTIC_V1',
        'date': '2026-10-30',
        'classification': 'FINITE_IDEAL_DIGITAL_STATES_PLUS_HYPOTHETICAL_DC',
        'scenario': 'independent_robot_5V_0.4W_sensor_only_not_charger',
        'design_decision': 'candidate_positive_driven_healthy_wire_with_receiver_pulldown',
        'not_compatible_with_unmodified_tps3700_outa': True,
        'physical_cutoff_qualified': False,
        'fOD_thermal_emi_wetness_or_offset_qualified': False,
        'battery_or_bms_connected': False,
        'actual_bench_tested': False,
        'safe_to_energize': False,
        'enumerated_topologies': per_topology,
        'resistor_examples_hypothetical': [
            resistor_screen(r, v) for r in (4700, 47000, 100000) for v in (3.3, 5.0)
        ],
        'minimum_requirements_for_next_electrical_gate': [
            'Exact supervisor SKU with push-pull actively driven HEALTHY on output; verify POR, logic polarity and max ratings',
            'Receiver-side pull-down, voltage-domain translation and unpowered pin injection/backfeed characterization',
            'Two independent eFuse EN drivers with no back-power and local W37 release/rearm',
            'State/time-domain simulation with transients and stuck-high/short-to-high detection strategy',
            'Real hardware isolated resistive bench only after separate safety authorization',
            'Preserve independent FOD, thermal, overcurrent and wetness controls; never radio emergency stop',
        ],
        'known_uncovered_faults': [
            'stuck-high / short-to-high / supervisor falsely healthy',
            'shared shunt or other common faults',
            'logic threshold and leakage assumptions',
            '5V supervisor itself, POR, brownout, backfeed and energy after cutoff',
            'all analog propagation/EMI/thermal and real WPT measurements',
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    args.out.write_text(json.dumps(evidence(), indent=2, sort_keys=True) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
