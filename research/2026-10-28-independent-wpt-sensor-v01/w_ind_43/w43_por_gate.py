"""VALDO W-IND-43: TPS3700 OUTB -> P-MOS positive-health prequalification.

Original analytic/fault-injection code. No manufacturer's transistor SPICE model,
no native KiCad netlist, no electrical safety qualification, no hardware.
W43 does not connect this signal to real eFuse EN inputs.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from itertools import product
from pathlib import Path
import json

TOP_OHM = 63_400.0  # candidate E96 1%, supersedes W41 62k after falling-hysteresis check
BOT_OHM = 10_000.0
GATE_PULLUP_OHM = 22_000.0
RECEIVER_PULLDOWN_OHM = 47_000.0
VIT_RISE_MIN, VIT_RISE_MAX = 0.396, 0.404  # TI TPS3700 at VDD=1.8 and 18 V
VIT_FALL_MIN, VIT_FALL_MAX = 0.387, 0.400  # Guaranteed, not typical
TOP_BOT_TOL = 0.01                          # Engineering candidate 1% resistors
INB_LEAKAGE_SWEEP_A = 1e-6                  # HYPOTHETICAL, not TI INB specification


def threshold_bounds(i_error_a: float = INB_LEAKAGE_SWEEP_A,
                     rtop: float = TOP_OHM, rbot: float = BOT_OHM,
                     falling: bool = False) -> tuple[float, float]:
    """3V3 rail trip envelope at guaranteed TPS3700 rising/falling thresholds.

    Worst-case negative-going threshold is *falling*, not rising; assuming
    the rising boundary for a brownout falsely certifies legacy 62k/10k.
    KCL with input current +/-i_error and a 1% resistor each:
    Vrail = Vref*(1 + Rtop/Rbot) + Iin*Rtop.
    This is a static screening equation, not a dynamic comparator model.
    """
    if min(rtop, rbot) <= 0 or i_error_a < 0:
        raise ValueError("invalid divider parameters")
    low, high = (VIT_FALL_MIN, VIT_FALL_MAX) if falling else (VIT_RISE_MIN, VIT_RISE_MAX)
    corners = [vref * (1 + rt / rb) + current * rt
               for vref, rt, rb, current in product(
                   (low, high),
                   (rtop * 0.99, rtop * 1.01),
                   (rbot * 0.99, rbot * 1.01),
                   (-i_error_a, i_error_a))]
    return min(corners), max(corners)


def gate_bias(source_5v: float = 5.0,
              gate_pullup_ohm: float = GATE_PULLUP_OHM,
              receiver_pulldown_ohm: float = RECEIVER_PULLDOWN_OHM,
              hypothetical_hiz_leak_a: float = 0.3e-6) -> dict:
    """Ohmic limits; MOSFET threshold/RDS(on) and input VOH deliberately not assumed."""
    if source_5v < 0 or gate_pullup_ohm <= 0 or receiver_pulldown_ohm <= 0 or hypothetical_hiz_leak_a < 0:
        raise ValueError("invalid DC parameters")
    return {
        "gate_sinking_current_upper_ma_at_gate_zero": round(source_5v / gate_pullup_ohm * 1000, 6),
        "gate_pullup_dissipation_upper_mw": round(source_5v ** 2 / gate_pullup_ohm * 1000, 6),
        "health_receiver_current_if_high_ma": round(source_5v / receiver_pulldown_ohm * 1000, 6),
        "health_receiver_dissipation_if_high_mw": round(source_5v ** 2 / receiver_pulldown_ohm * 1000, 6),
        "gate_to_source_bias_from_hypothetical_hiz_leak_mv": round(hypothetical_hiz_leak_a * gate_pullup_ohm * 1000, 6),
        "pmos_turnon_and_receiver_voltage_qualified": False,
    }


@dataclass(frozen=True)
class Inputs:
    receiver_supply_5v: bool
    monitor_vdd: float
    sensed_3v3: float
    outb_open: bool = False
    health_wire_open: bool = False
    gate_stuck_ground: bool = False
    health_short_to_5v: bool = False
    locally_armed: bool = True
    independent_interlocks_ok: bool = True

    def __post_init__(self) -> None:
        for f in ('receiver_supply_5v','outb_open','health_wire_open',
                  'gate_stuck_ground','health_short_to_5v','locally_armed',
                  'independent_interlocks_ok'):
            if type(getattr(self, f)) is not bool:
                raise TypeError(f'{f} must be bool')
        if not (0 <= self.monitor_vdd <= 18 and 0 <= self.sensed_3v3 <= 5.5):
            raise ValueError('voltage outside modeled range')


def outb_possible_states(vdd: float, sensed_3v3: float,
                         rtop: float = TOP_OHM) -> tuple[str, ...]:
    """TI verified polarity, but conservatively ambiguous below operating VDD.

    Minimum guaranteed VDD for functional operation: 1.8V. Below POR 0.8V
    max, TI says the output is INDETERMINATE, not definitely high-impedance.
    0.8..1.3V lies beneath minimum UVLO (1.3V); OUTB is HiZ.
    1.3..1.8V covers device threshold spread, hence adversarial outcomes.
    Disqualification on brownout requires the *minimum falling* boundary.
    Qualification on ramp up requires *maximum rising* boundary.
    The envelope between retains both states due to possible prior history.
    """
    if vdd < 0.8:
        return ('hiz', 'sink')  # UNDEFINED POR: possible unsafe sink
    if vdd < 1.3:
        return ('hiz',)
    if vdd < 1.8:
        return ('hiz', 'sink')
    falling_lo = threshold_bounds(rtop=rtop, falling=True)[0]
    rising_hi = threshold_bounds(rtop=rtop, falling=False)[1]
    if sensed_3v3 <= falling_lo:
        return ('hiz',)
    if sensed_3v3 >= rising_hi:
        return ('sink',)
    return ('hiz', 'sink')  # uncertain near threshold


def evaluate(x: Inputs) -> dict:
    """Ideal P-MOS topology: source to pre-cut 5V, gate pulled to source,
    TPS3700 OUTB sinks gate only when INB- > threshold, drain drives HEALTH,
    input on receptor has *local* pull-down. Ideal switching asserted only.
    """
    sink_options = outb_possible_states(x.monitor_vdd, x.sensed_3v3)
    states = []
    for state in sink_options:
        gate_low = x.gate_stuck_ground or (state == 'sink' and not x.outb_open)
        driver_on_ideal = x.receiver_supply_5v and gate_low
        health_high_ideal = x.receiver_supply_5v and not x.health_wire_open and (
            driver_on_ideal or x.health_short_to_5v)
        permission = bool(health_high_ideal and x.locally_armed and x.independent_interlocks_ok)
        states.append({
            'outb': state,
            'pmos_drives_health_ideal': driver_on_ideal,
            'health_high_ideal': bool(health_high_ideal),
            'request_on_ideal': permission,
            'unsafe_on_with_3v3_bad': permission and x.sensed_3v3 <= 2.7,
        })
    return {
        'possible_states': states,
        'could_request_on': any(s['request_on_ideal'] for s in states),
        'guaranteed_off': all(not s['request_on_ideal'] for s in states),
        'unsafe_possible': any(s['unsafe_on_with_3v3_bad'] for s in states),
        'uncertainty': len(states) > 1,
    }


def evidence() -> dict:
    cases = 0
    unsafe_cases = 0
    ambiguous = 0
    examples = []
    for sensed, vdd, vsupply, outopen, healthopen, gatefault, short, armed, others in product(
        (0.0, 2.7, 3.3), (0.4, 1.0, 1.5, 5.0),
        (False, True), repeat_bool(), repeat_bool(), repeat_bool(),
        repeat_bool(), repeat_bool(), repeat_bool()):
        x = Inputs(vsupply, vdd, sensed, outopen, healthopen, gatefault, short, armed, others)
        y = evaluate(x)
        cases += 1
        unsafe_cases += int(y['unsafe_possible'])
        ambiguous += int(y['uncertainty'])
        if y['unsafe_possible'] and len(examples) < 12:
            examples.append({**asdict(x), **y})
    rising_lo, rising_hi = threshold_bounds()
    falling_lo, falling_hi = threshold_bounds(falling=True)
    legacy_falling_lo, legacy_falling_hi = threshold_bounds(rtop=62_000, falling=True)
    return {
        'schema': 'VALDO_W_IND_43_POR_AWARE_OUTB_PMOS_V1',
        'date': '2026-10-30',
        'classification': 'ORIGINAL_PYTHON_FINITE_ADVERSARIAL_MODEL_NOT_SPICE_NOT_HARDWARE',
        'cases': cases,
        'unsafe_possible_cases': unsafe_cases,
        'ambiguity_cases': ambiguous,
        'unsafe_examples': examples,
        'candidate': 'TPS3700 INB- overvoltage output OUTB sinks when rail healthy; OUTB gates high-side P-MOS; receiver pull-down',
        'critical_finding': 'TPS3700 OUTB below POR is indeterminate; legacy W41 62k/10k fails a guaranteed falling hysteresis corner at 2.7V',
        'candidate_divider_top_ohm': TOP_OHM,
        'candidate_divider_bottom_ohm': BOT_OHM,
        'rising_trip_3v3_range_1pct_and_hypothetical_1uA': [round(rising_lo, 6), round(rising_hi, 6)],
        'falling_trip_3v3_range_1pct_and_hypothetical_1uA': [round(falling_lo, 6), round(falling_hi, 6)],
        'legacy_w41_62k_falling_3v3_range_1pct_and_hypothetical_1uA': [round(legacy_falling_lo, 6), round(legacy_falling_hi, 6)],
        'legacy_w41_failing_bad_rail_margin_v': round(legacy_falling_lo - 2.7, 6),
        'candidate_min_bad_rail_margin_v': round(falling_lo - 2.7, 6),
        'candidate_min_good_rail_margin_v': round(3.135 - rising_hi, 6),
        'source_hypothesis': '1% resistors; +/-1uA input perturbation fictional, NOT TI leakage spec; rail normal>=3.135V/bad<=2.70V hypothetical',
        'sensitivity_sweep_hypothetical': [
            {
                'input_perturbation_ua': i_ua,
                'bad_margin_v': round(threshold_bounds(i_error_a=i_ua * 1e-6, falling=True)[0] - 2.7, 6),
                'good_margin_v': round(3.135 - threshold_bounds(i_error_a=i_ua * 1e-6)[1], 6),
            } for i_ua in (0, .5, 1, 1.25, 1.5, 2)
        ],
        'gate_22k': gate_bias(),
        'verified_source_facts': {
            'TPS3700_OUTB_low_when_INB_above_400mV': 'https://www.ti.com/product/TPS3700',
            'TPS3700_PWR_POR_unknown_under_0v8_and_OUTB_HIZ_below_UVLO': 'https://www.ti.com/document-viewer/TPS3700/datasheet/electrical-characteristics-slvsci76498',
            'TI_OUTB_VOL_max250mV_at_sink5mA_and_VDD5': True,
            'TI_OUTB_OD_leakage_max300nA_with_valid_VDD_only': True,
        },
        'missing_guarantees': [
            'Independent hardware 5V POR-qualified enable, no EN power before both local latches off',
            'Validate P-MOS exact manufacturer part pinout, VGS, leakage, RDS(on) at 5V and temperature',
            'Receiver voltage domain / unpowered input injection / capacitive backfeed',
            'W37 local release then rearm implemented in electrical hardware',
            'No broken shunt, false-low OUTB, stuck gate or health short-high diagnosis yet',
            '63.4k/10k 1% margin only with fictional +/-1uA: actual temperature, parasitics, RF, hysteresis timing not qualified',
            'Native KiCad + ERC/netlist plus analog timing and cold-start testing not done',
            'Dock charger FOD, thermal, offset, EMI, wetness, lithium battery/BMS not tested or connected',
        ],
        'release_for_bench_or_hardware': False,
        'lithium_or_real_power_energized': False,
        'third_party_designs_copied': False,
    }


def repeat_bool() -> tuple[bool, bool]:
    return (False, True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.write_text(json.dumps(evidence(), sort_keys=True, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
