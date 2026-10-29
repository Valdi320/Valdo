"""W-IND-27: shunt 0.1 ohm/INA301A1 layout and price tradeoff.

Deterministic STATIC sensitivity study, not a circuit emulator or safety rating.
Vendor values: WSL2512R1000FEA 1%, 75ppm/C, 1W, 2 terminals;
VPG Y44880R10000F9R 1%, 5ppm/C, 1W, 4 terminals.
Extra sensed pad resistance, error budget and 100C excursion are assumptions.
No battery, BMS, motors, docking charger or powered RF.
"""
from dataclasses import dataclass
import json
import math

TI = 'https://www.ti.com/lit/ds/symlink/ina301.pdf'
TME = 'https://www.tme.eu/es/details/wsl2512r1000fea/resistencias-smd/vishay/'
FARNELL = 'https://es.farnell.com/vpg-foil-resistors/y44880r10000f9r/current-sense-res-0r1-1-1w-2512/dp/4266769'

@dataclass(frozen=True)
class Option:
    mpn: str
    terminals: int
    tempco_ppm_per_c: float
    tolerance_fraction: float
    unit_price_ex_vat_eur: float
    moq: int
    url: str
    sense_extra_min_ohm: float
    sense_extra_max_ohm: float

CHEAP = Option('Vishay WSL2512R1000FEA', 2, 75, .01, .53, 1, TME, 0, .005)
KELVIN = Option('VPG Y44880R10000F9R', 4, 5, .01, 16.12, 1, FARNELL, 0, .00005)

@dataclass(frozen=True)
class Pilot:
    r_shunt_nom_ohm: float = .1
    i_good_peak_a: float = .3
    i_fault_min_a: float = .4
    temp_excursion_c: float = 100.0
    gain_nominal: float = 20.0
    gain_initial_error: float = .001
    gain_drift_ppm_per_c: float = 10
    input_offset_max_v: float = 125e-6
    input_offset_drift_v_per_c: float = .5e-6
    r_limit_ohm: float = 8660
    r_limit_tolerance_fraction: float = .01
    r_limit_tcr_ppm_per_c: float = 100
    i_limit_min_a: float = 79.2e-6
    i_limit_nom_a: float = 80e-6
    i_limit_max_a: float = 80.8e-6
    comparator_offset_25c_max_v: float = .0035
    unqualified_extra_threshold_v: float = .010

def calculate(option: Option = CHEAP, pilot: Pilot = Pilot()) -> dict:
    """Corner envelope over stated assumptions; not a qualification result."""
    vals = [v for v in vars(option).values() if isinstance(v, (int, float))]
    vals += list(vars(pilot).values())
    if not all(math.isfinite(v) for v in vals):
        raise ValueError('all numeric inputs must be finite')
    if (option.terminals not in (2, 4) or option.tempco_ppm_per_c < 0
            or not 0 <= option.tolerance_fraction < 1
            or option.unit_price_ex_vat_eur <= 0 or option.moq < 1
            or option.sense_extra_min_ohm < 0
            or option.sense_extra_max_ohm < option.sense_extra_min_ohm
            or not 0 < pilot.i_good_peak_a < pilot.i_fault_min_a
            or pilot.r_shunt_nom_ohm <= 0 or pilot.gain_nominal <= 0
            or not 0 <= pilot.temp_excursion_c <= 100
            or pilot.r_limit_ohm <= 0
            or not 0 < pilot.i_limit_min_a <= pilot.i_limit_nom_a <= pilot.i_limit_max_a):
        raise ValueError('invalid option or pilot')
    for n in ('gain_initial_error', 'gain_drift_ppm_per_c', 'input_offset_max_v',
              'input_offset_drift_v_per_c', 'r_limit_tolerance_fraction',
              'r_limit_tcr_ppm_per_c', 'comparator_offset_25c_max_v',
              'unqualified_extra_threshold_v'):
        if getattr(pilot, n) < 0:
            raise ValueError('negative tolerance or uncertainty')
    dt = pilot.temp_excursion_c
    rerr = option.tolerance_fraction + option.tempco_ppm_per_c * 1e-6 * dt
    gerr = pilot.gain_initial_error + pilot.gain_drift_ppm_per_c * 1e-6 * dt
    lerr = pilot.r_limit_tolerance_fraction + pilot.r_limit_tcr_ppm_per_c * 1e-6 * dt
    if max(rerr, gerr, lerr) >= 1:
        raise ValueError('unphysical tolerance')
    vin_off = pilot.input_offset_max_v + pilot.input_offset_drift_v_per_c * dt
    cmp_off = pilot.comparator_offset_25c_max_v + pilot.unqualified_extra_threshold_v
    tlo = pilot.r_limit_ohm * (1-lerr) * pilot.i_limit_min_a - cmp_off
    thi = pilot.r_limit_ohm * (1+lerr) * pilot.i_limit_max_a + cmp_off
    gmin, gmax = pilot.gain_nominal*(1-gerr), pilot.gain_nominal*(1+gerr)
    rmin = pilot.r_shunt_nom_ohm*(1-rerr)+option.sense_extra_min_ohm
    rmax = pilot.r_shunt_nom_ohm*(1+rerr)+option.sense_extra_max_ohm
    healthy_hi = (pilot.i_good_peak_a*rmax + vin_off)*gmax
    fault_lo = (pilot.i_fault_min_a*rmin - vin_off)*gmin
    allowable_extra = (tlo/gmax-vin_off)/pilot.i_good_peak_a - pilot.r_shunt_nom_ohm*(1+rerr)
    return {
        'schema': 'W-IND-27-shunt-v1',
        'model_kind': 'STATIC_ASSUMPTION_ONLY_NOT_MEASURED',
        'part': option.mpn, 'terminals': option.terminals,
        'part_datasheet_claims': {'resistance_ohm': pilot.r_shunt_nom_ohm,
                                  'initial_tolerance_fraction': option.tolerance_fraction,
                                  'tempco_ppm_per_c': option.tempco_ppm_per_c,
                                  'nominal_power_w': 1.0},
        'parasitic_sense_min_ohm_assumed': option.sense_extra_min_ohm,
        'parasitic_sense_max_ohm_assumed': option.sense_extra_max_ohm,
        'max_parasitic_to_avoid_false_300ma_ohm_in_model': allowable_extra,
        'threshold_low_v': tlo, 'threshold_high_v': thi,
        'healthy_output_max_v': healthy_hi, 'fault_output_min_v': fault_lo,
        'no_false_margin_mv': 1000*(tlo-healthy_hi),
        'fault_detection_margin_mv': 1000*(fault_lo-thi),
        'static_envelope_separates_300ma_and_400ma': healthy_hi < tlo and fault_lo > thi,
        'rshunt_power_at_300ma_w_nominal': pilot.i_good_peak_a**2*pilot.r_shunt_nom_ohm,
        'rshunt_power_at_400ma_w_nominal': pilot.i_fault_min_a**2*pilot.r_shunt_nom_ohm,
        'shunt_drop_at_400ma_v_nominal': pilot.i_fault_min_a*pilot.r_shunt_nom_ohm,
        'price_ex_vat_eur_snapshot': option.unit_price_ex_vat_eur,
        'price_with_es_21pct_vat_eur_calculated': round(option.unit_price_ex_vat_eur*1.21,4),
        'catalog_min_order': option.moq, 'price_source': option.url,
        'diotronic_local_stock_verified': False,
        'pad_parasitic_measured': False,
        'pcb_kelvin_layout_verified': False,
        'real_comparator_temperature_emi_verified': False,
        'independent_cutoff_fod_thermal_verified': False,
        'physical_tests': 0,
        'power_on_approved': False,
        'lithium_bms_dock_connected': False,
    }

def report() -> dict:
    return {'cheap_2_terminal_assumed_5milliohm':calculate(CHEAP),
            'true_4_terminal_assumed_0p05milliohm':calculate(KELVIN),
            'cost_ratio_ex_vat': KELVIN.unit_price_ex_vat_eur/CHEAP.unit_price_ex_vat_eur,
            'sources':{'ina301':TI,'two_terminal':TME,'four_terminal':FARNELL}}

if __name__ == '__main__':
    print(json.dumps(report(),sort_keys=True,indent=2))
