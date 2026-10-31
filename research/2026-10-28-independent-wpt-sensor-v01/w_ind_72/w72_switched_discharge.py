"""W-IND-72: switched bleeder mathematical screen, independent robot W sector.

Original VALDO W code (2026). Digital hypothesis only: no measured WPT,
component qualification, real cutoff, or physical approval is implemented.
No third-party firmware, schematics, CAD or code incorporated.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def finite(name: str, value: object, low: float, high: float) -> float:
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError(f"{name}: numeric finite non-boolean input required")
    value = float(value)
    if not low <= value <= high:
        raise ValueError(f"{name}: outside [{low}, {high}]")
    return value


def strictly_bool(name: str, value: object) -> bool:
    if type(value) is not bool:
        raise ValueError(f"{name}: boolean required")
    return value


def screen(
    *,
    max_v: float = 5.5,
    cap_nominal_f: float = 100e-6,
    cap_tolerance_fraction: float = 0.20,
    resistor_nominal_ohm: float = 750.0,
    resistor_tolerance_fraction: float = 0.05,
    max_switch_on_resistance_ohm: float = 10.0,
    max_off_leakage_a: float | None = 1e-6,
    max_driver_on_quiescent_a: float | None = 100e-6,
    target_v: float = 0.5,
    deadline_s: float = 0.250,
    standby_budget_w: float = 0.005,
    existing_always_on_bleeder_ohm: float | None = 1000.0,
    source_cut_physically_verified: bool = False,
    reverse_feed_physically_excluded: bool = False,
    external_tx_storage_physically_characterized: bool = False,
    monitor_independently_powered_verified: bool = False,
) -> dict:
    """Bound an *idealized single-node* switched discharge under assumptions.

    The existing W21 R2 is still permanently connected on the schematic.
    A proposed switched branch in parallel does NOT remove its standby loss.
    If R2 is absent in a future, *unbuilt* revision, pass None explicitly.
    """
    v = finite('max_v', max_v, 0.01, 5.5)
    c = finite('cap_nominal_f', cap_nominal_f, 1e-10, 0.1)
    dc = finite('cap_tolerance_fraction', cap_tolerance_fraction, 0.0, 0.99)
    r = finite('resistor_nominal_ohm', resistor_nominal_ohm, 1.0, 1e9)
    dr = finite('resistor_tolerance_fraction', resistor_tolerance_fraction, 0.0, 0.99)
    r_switch = finite('max_switch_on_resistance_ohm', max_switch_on_resistance_ohm, 0.0, 1e6)
    vt = finite('target_v', target_v, 1e-8, 5.5)
    deadline = finite('deadline_s', deadline_s, 1e-6, 3600)
    budget = finite('standby_budget_w', standby_budget_w, 1e-9, 10)
    if vt >= v:
        raise ValueError('target_v must be strictly below max_v')
    if (max_off_leakage_a is None) != (max_driver_on_quiescent_a is None):
        raise ValueError('leakage and driver quiescent must both be known or both unknown')
    if max_off_leakage_a is not None:
        leak = finite('max_off_leakage_a', max_off_leakage_a, 0.0, 1.0)
        iq = finite('max_driver_on_quiescent_a', max_driver_on_quiescent_a, 0.0, 1.0)
        on_branch_w = v * (leak + iq)
    else:
        leak = iq = on_branch_w = None
    if existing_always_on_bleeder_ohm is None:
        existing_ohm = None
        existing_worst_w = 0.0
        existing_max_r_ohm = math.inf
    else:
        existing_ohm = finite('existing_always_on_bleeder_ohm', existing_always_on_bleeder_ohm, 1.0, 1e12)
        # Existing W21 R2 tolerance isn't documented: conservative 5% hypothetical.
        existing_worst_w = v*v/(existing_ohm*(1-dr))
        existing_max_r_ohm = existing_ohm * (1+dr)
    physical_flags = {
        'source_cut_physically_verified': strictly_bool('source_cut_physically_verified',source_cut_physically_verified),
        'reverse_feed_physically_excluded': strictly_bool('reverse_feed_physically_excluded',reverse_feed_physically_excluded),
        'external_tx_storage_physically_characterized': strictly_bool('external_tx_storage_physically_characterized',external_tx_storage_physically_characterized),
        'monitor_independently_powered_verified': strictly_bool('monitor_independently_powered_verified',monitor_independently_powered_verified),
    }
    cap_hi = c*(1+dc)
    r_active_hi = r*(1+dr) + r_switch
    # Parallel existing R2 can only SPEED discharge under the ideal assumptions.
    effective_r_hi = (r_active_hi*existing_max_r_ohm/(r_active_hi+existing_max_r_ohm)
                      if existing_ohm is not None else r_active_hi)
    decay_worst_s = effective_r_hi * cap_hi * math.log(v/vt)
    active_peak_resistor_w = v*v/(r*(1-dr))
    peak_switch_path_a = v/(r*(1-dr))
    initial_storage_max_j = 0.5*cap_hi*v*v
    on_total_w = None if on_branch_w is None else on_branch_w + existing_worst_w
    on_within_budget = None if on_total_w is None else on_total_w <= budget
    decay_within_target = decay_worst_s <= deadline
    faults = {
        'active_switch_stuck_open': ('passive R2 may still discharge in ideal model' if existing_ohm is not None
                                      else 'NO IDEAL DC DISCHARGE PATH; unlimited retention possible'),
        'active_switch_stuck_closed': 'constant shunt during TX ON; peak branch estimate applies, may overload source',
        'both_upstream_switches_welded': 'discharge switch can shunt live power; no independent safe isolation demonstrated',
        'monitor_loses_supply': 'last voltage reading is stale; cannot infer residual energy safe',
        'external_tx_resonance_or_backfeed': 'no modeled bound; do not energize',
    }
    # Even when theoretical targets pass, this is never physical clearance.
    if not all(physical_flags.values()):
        status = 'BLOCKED_PHYSICAL_POWER_PATH_UNVERIFIED'
    elif on_total_w is None:
        status = 'BLOCKED_STANDBY_PARAMETERS_UNKNOWN'
    elif not (decay_within_target and on_within_budget):
        status = 'BLOCKED_SYNTHETIC_TARGETS_NOT_MET'
    else:
        status = 'SCREEN_ONLY_SYNTHETIC_TARGETS_MET_NOT_HARDWARE_APPROVAL'
    return {
        'milestone': 'W-IND-72',
        'status': status,
        'data_kind': 'SYNTHETIC_IDEAL_RC_NOT_MEASURED',
        'hardware_approved': False,
        'may_energize': False,
        'physical_tests': 0,
        'battery_bms_dock_connected': False,
        'qualified_fod_thermal_emi_offset': False,
        'critical_cut_depends_on_radio': False,
        'prior_w21_r2_ohm_if_retained': existing_ohm,
        'assumptions': {
            'max_v': v, 'cap_nominal_f': c, 'cap_tolerance_fraction': dc,
            'resistor_nominal_ohm': r, 'resistor_tolerance_fraction': dr,
            'max_switch_on_resistance_ohm': r_switch,
            'max_off_leakage_a': leak, 'max_driver_on_quiescent_a': iq,
            'existing_r2_tolerance_fraction_assumed': dr,
            'target_v': vt, 'deadline_s': deadline, 'standby_budget_w': budget,
            'single_ideal_unfed_RC': True, 'physical_flags': physical_flags,
        },
        'bounded_ideal_metrics': {
            'max_stored_j': initial_storage_max_j,
            'max_decay_s': decay_worst_s,
            'max_initial_active_resistor_w': active_peak_resistor_w,
            'max_initial_switch_path_a': peak_switch_path_a,
            'max_known_steady_on_w': on_total_w,
            'existing_r2_steady_w': existing_worst_w,
            'new_active_branch_steady_on_w': on_branch_w,
            'decay_within_assumed_target': decay_within_target,
            'standby_within_assumed_budget': on_within_budget,
        },
        'fault_screen': faults,
        'decision': ('Do not add an active discharge in parallel with W21 R2 claiming standby savings; '
                     'change of R2 topology needs separate schematic and independent safety review. '
                     'Real TX C/L/voltage, isolation, cutoff, FOD, heat and EMI unknown. No real proof.'),
        'next_discriminating_evidence': ('Full independent TX netlist/datasheets and actual capacitor inventory; '
                                          'then approved isolated, current-limited resistive bench measurements.'),
    }


def main(argv=None) -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--no-w21-r2', action='store_true', help='Hypothetical future topology; does not alter W21')
    p.add_argument('--report', type=Path, required=True)
    args=p.parse_args(argv)
    result=screen(existing_always_on_bleeder_ohm=None if args.no_w21_r2 else 1000.0)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print(result['status'])
    return 0 # This exit code attests successful analysis, NOT approved power.


if __name__=='__main__':
    raise SystemExit(main())
