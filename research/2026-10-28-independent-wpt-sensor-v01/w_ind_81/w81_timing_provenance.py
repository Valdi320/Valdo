#!/usr/bin/env python3
"""W81: reject typical-as-maximum supervisory timing; ideal capacitor bound.

Pure mathematical/synthetic gate; NEVER qualifies actual WPT electronics or safety.
"""
import argparse
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

Q = Decimal('0.000001')
GRADES = frozenset(('manufacturer_typical', 'manufacturer_max', 'hypothesis', 'measurement'))


def numeric(v, key, positive=True):
    if type(v) not in (str, int, float, Decimal):
        raise ValueError(f'{key}: exact numeric type required')
    try:
        result = Decimal(str(v))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f'{key}: invalid numeric value') from exc
    if not result.is_finite() or (positive and result <= 0):
        raise ValueError(f'{key}: finite positive required')
    return result


def number_string(v):
    return format(v.quantize(Q), 'f')


def timing(t, key):
    if type(t) is not dict or set(t) != {'value_us', 'evidence_class', 'source', 'conditions'}:
        raise ValueError(f'{key}: exact provenance fields required')
    value = numeric(t['value_us'], key + '.value_us')
    grade = t['evidence_class']
    if type(grade) is not str or grade not in GRADES:
        raise ValueError(f'{key}: invalid evidence_class')
    if type(t['source']) is not str or type(t['conditions']) is not str:
        raise ValueError(f'{key}: invalid provenance strings')
    if grade.startswith('manufacturer_') and not t['source'].startswith('https://'):
        raise ValueError(f'{key}: manufacturer traceability URL required')
    return value, grade


def audit(data):
    if type(data) is not dict:
        raise ValueError('scenario must be an object')
    required = {'sensor_floor_v', 'trip_lower_bound_v', 'effective_cap_min_uf',
                'sensor_peak_power_mw', 'fall_delay', 'cut_delay',
                'independent_monitor_supply_verified', 'normally_off_cut_verified',
                'reverse_isolation_verified', 'latch_retention_verified',
                'trip_bound_source_class', 'cap_bound_source_class',
                'peak_power_source_class', 'battery_connected', 'sensor_kind'}
    if set(data) != required:
        raise ValueError(f'expected fields {sorted(required)}, got {sorted(data)}')
    for name in ('independent_monitor_supply_verified', 'normally_off_cut_verified',
                 'reverse_isolation_verified', 'latch_retention_verified', 'battery_connected'):
        if type(data[name]) is not bool:
            raise ValueError(name + ': boolean required')
    if data['battery_connected']:
        raise ValueError('battery connection is forbidden in W81 simulation')
    if data['sensor_kind'] != 'synthetic_noncritical':
        raise ValueError('only synthetic noncritical sensor is in scope')
    for name in ('trip_bound_source_class', 'cap_bound_source_class', 'peak_power_source_class'):
        if type(data[name]) is not str or data[name] not in ('hypothesis', 'manufacturer_minimum', 'measured'):
            raise ValueError(name + ': unknown provenance')
    floor = numeric(data['sensor_floor_v'], 'sensor_floor_v')
    trip = numeric(data['trip_lower_bound_v'], 'trip_lower_bound_v')
    capacitance = numeric(data['effective_cap_min_uf'], 'effective_cap_min_uf')
    peak_power = numeric(data['sensor_peak_power_mw'], 'sensor_peak_power_mw')
    if trip <= floor:
        raise ValueError('trip lower bound must be greater than sensor floor')
    if trip > 5.5 or floor > 5.5 or capacitance > Decimal('1000000') or peak_power > Decimal('1000000'):
        raise ValueError('out of range for limited mathematical screening')
    fall, fall_grade = timing(data['fall_delay'], 'fall_delay')
    cut, cut_grade = timing(data['cut_delay'], 'cut_delay')
    if fall > Decimal('1000000000') or cut > Decimal('1000000000'):
        raise ValueError('unbounded time input')
    # Exact capacitor-energy envelope, conditional on a minimum effective capacitance,
    # no other source/load and constant-power draw at or below P_peak:
    # t = C_eff*(V_trip^2 - V_floor^2)/(2*P_peak).
    hold_us = capacitance * (trip*trip - floor*floor) * Decimal('500') / peak_power
    illustrative_sum = fall + cut
    hypothetical_cap_200_40 = (Decimal('200') + Decimal('40')) * peak_power / (
        (trip*trip - floor*floor) * Decimal('500'))
    documented_pair = fall_grade == 'manufacturer_max' and cut_grade == 'manufacturer_max'
    bound_sources = all(data[k] != 'hypothesis' for k in (
        'trip_bound_source_class', 'cap_bound_source_class', 'peak_power_source_class'))
    physical_cut = all(data[k] for k in ('independent_monitor_supply_verified',
        'normally_off_cut_verified', 'reverse_isolation_verified', 'latch_retention_verified'))
    blocks = []
    if fall_grade != 'manufacturer_max':
        blocks.append('NO_QUALIFIED_FALLING_PROPAGATION_MAX')
    if cut_grade != 'manufacturer_max':
        blocks.append('NO_QUALIFIED_CUT_PROPAGATION_MAX')
    if not bound_sources:
        blocks.append('RAIL_CAP_AND_POWER_BOUNDS_HYPOTHETICAL')
    if not physical_cut:
        blocks.append('MONITOR_LATCH_CUT_AND_REVERSE_NOT_VERIFIED')
    if documented_pair and illustrative_sum >= hold_us:
        blocks.append('DOCUMENTED_DELAY_EXCEEDS_IDEAL_HOLDUP')
    blocks.append('WPT_FOD_TEMP_EMI_OFFSET_WETNESS_NOT_MEASURED')
    blocks.append('ACTUAL_POWER_TO_RX_AND_DOCK_BMS_NOT_QUALIFIED')
    return {
        'model': 'W81_IDEAL_CAPACITOR_ENERGY_AND_PROVENANCE_ONLY',
        'hold_up_us_conditional_on_hypotheses': number_string(hold_us),
        'fall_delay_us': number_string(fall),
        'fall_delay_evidence_class': fall_grade,
        'cut_delay_us': number_string(cut),
        'cut_delay_evidence_class': cut_grade,
        'naive_delay_sum_us_NOT_A_GUARANTEED_MAX': number_string(illustrative_sum),
        'naive_typical_based_timing_seems_to_fit': illustrative_sum < hold_us,
        'documented_delay_pair': documented_pair,
        'manufacturer_bounded_delay_fits_ideal_reserve': (illustrative_sum < hold_us) if documented_pair else None,
        'conditional_min_effective_cap_uf_IF_200us_detector_AND_40us_cut_MAX': number_string(hypothetical_cap_200_40),
        'safe_acceptance_blocked': True,
        'design_selected': False,
        'hardware_approved': False,
        'physical_trials_authorized': False,
        'critical_stop_authorized': False,
        'battery_bms_dock_authorized': False,
        'decision': 'BLOCK: typical is not worst-case delay; keep repairable cable baseline',
        'blockers': blocks,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    result = audit(json.loads(Path(a.input).read_text(encoding='utf-8')))
    Path(a.output).write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
