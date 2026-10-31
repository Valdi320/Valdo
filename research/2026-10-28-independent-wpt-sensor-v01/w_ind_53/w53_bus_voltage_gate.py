"""W-IND-53: fail-closed, offline dual INA219 bus-voltage calibration.

Original VALDO W-only source; never operates I2C, a WPT transmitter or lithium.
An offline pass is only a conditional arithmetic result, not hardware approval.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
import argparse
import json


def dec(value: object) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as error:
        raise ValueError('invalid decimal evidence') from error
    if not result.is_finite():
        raise ValueError('nonfinite decimal evidence')
    return result


@dataclass(frozen=True)
class Channel:
    role: str
    meter_id: str
    reference_id: str
    source_kind: str
    valid_from: str
    valid_until: str
    as_of: str
    low_raw_mv: int
    high_raw_mv: int
    check_raw_mv: int
    low_ref_mv: str
    high_ref_mv: str
    check_ref_mv: str
    low_uncertainty_mv: str
    high_uncertainty_mv: str
    check_uncertainty_mv: str
    calibration_temperature_c: str
    operating_temperature_c: str
    gain_drift_ppm_per_c: str | None
    offset_drift_mv_per_c: str | None
    reference_traceable: bool = False
    correct_board_and_chip_verified: bool = False
    independent_holdout_recorded: bool = False
    temperature_measured: bool = False
    acquisition_and_clock_verified: bool = False
    max_temperature_delta_c: str = '5'
    max_conditional_error_percent: str = '2'
    bus_lsb_mv: int = 4
    max_bus_mv: int = 26000


def screen_channel(c: Channel) -> dict:
    if c.role not in ('TX', 'RX'):
        raise ValueError('only TX and RX rails')
    if not (c.meter_id.strip() and c.reference_id.strip()):
        raise ValueError('meter/reference identification required')
    if c.source_kind not in ('SYNTHETIC', 'BENCH_MEASURED'):
        raise ValueError('unknown source kind')
    raw_values = (c.low_raw_mv, c.check_raw_mv, c.high_raw_mv)
    if any(type(x) is not int for x in (*raw_values, c.bus_lsb_mv, c.max_bus_mv)):
        raise ValueError('raw units must be integer millivolts')
    if c.bus_lsb_mv != 4 or c.max_bus_mv != 26000:
        raise ValueError('INA219 bus LSB/range contract unqualified')
    if any(x % c.bus_lsb_mv for x in raw_values):
        raise ValueError('INA219 bus register quantization is 4mV')
    if not (0 < c.low_raw_mv < c.check_raw_mv < c.high_raw_mv < c.max_bus_mv):
        raise ValueError('invalid, reversed or saturated bus points')

    vlo, vhi, vcheck, ulo, uhi, ucheck, tcal, tuse, max_dt, max_err = map(dec, (
        c.low_ref_mv, c.high_ref_mv, c.check_ref_mv,
        c.low_uncertainty_mv, c.high_uncertainty_mv, c.check_uncertainty_mv,
        c.calibration_temperature_c, c.operating_temperature_c,
        c.max_temperature_delta_c, c.max_conditional_error_percent))
    if not (0 < ulo < vlo < vcheck < vhi < dec(c.max_bus_mv)):
        raise ValueError('invalid reference bracket')
    if not (0 < uhi < vhi and 0 < ucheck < vcheck and max_dt >= 0 and max_err > 0):
        raise ValueError('invalid reference uncertainty or acceptance limit')
    if not (vlo + ulo < vcheck - ucheck < vcheck + ucheck < vhi - uhi):
        raise ValueError('reference ranges overlap; no independent holdout')
    try:
        start, end, when = (date.fromisoformat(s) for s in (c.valid_from, c.valid_until, c.as_of))
    except (TypeError, ValueError) as error:
        raise ValueError('invalid calibration date') from error
    if start > end:
        raise ValueError('reversed calibration validity')

    reasons: list[str] = []
    if not start <= when <= end:
        reasons.append('reference expired or not yet valid')
    if c.source_kind != 'BENCH_MEASURED':
        reasons.append('synthetic inputs do not qualify a meter')
    for flag, label in (
        ('reference_traceable', 'traceable reference missing'),
        ('correct_board_and_chip_verified', 'INA219 board/grade not verified'),
        ('independent_holdout_recorded', 'independent operating-point holdout missing'),
        ('temperature_measured', 'real temperatures not measured'),
        ('acquisition_and_clock_verified', 'I2C clock and freshness not verified'),
    ):
        if not getattr(c, flag):
            reasons.append(label)
    delta_temp = abs(tuse - tcal)
    if delta_temp > max_dt:
        reasons.append('outside calibrated temperature window')
    if c.gain_drift_ppm_per_c is None or c.offset_drift_mv_per_c is None:
        gain = offset = None
        reasons.append('temperature drift bounds missing')
    else:
        gain, offset = dec(c.gain_drift_ppm_per_c), dec(c.offset_drift_mv_per_c)
        if gain < 0 or offset < 0:
            raise ValueError('negative drift bound')

    raw_lo, raw_ck, raw_hi = map(dec, raw_values)
    half_lsb = dec(c.bus_lsb_mv) / dec(2)
    # Exact monotonic extrema of the interpolation weight given independently
    # bounded ±half-LSB readings. NOT a statistical confidence interval.
    span = raw_hi - raw_lo
    weight = (raw_ck - raw_lo) / span
    weight_min = (raw_ck - raw_lo - 2 * half_lsb) / span
    weight_max = (raw_ck - raw_lo + 2 * half_lsb) / span
    if not dec(0) < weight_min <= weight <= weight_max < dec(1):
        raise ValueError('insufficient independent interpolation margin')
    nominal = vlo + (vhi - vlo) * weight
    predicted_min = (dec(1) - weight_min) * (vlo - ulo) + weight_min * (vhi - uhi)
    predicted_max = (dec(1) - weight_max) * (vlo + ulo) + weight_max * (vhi + uhi)
    if gain is None:
        error_percent = None
    else:
        # Conservative thermal allowance; all coefficients in the example
        # are HYPOTHESES until the actual meter is characterized.
        drift_mv = delta_temp * (vhi * gain / dec(1000000) + offset)
        predicted_min -= drift_mv
        predicted_max += drift_mv
        ref_min, ref_max = vcheck - ucheck, vcheck + ucheck
        worst = max(abs(predicted_max - ref_min), abs(ref_max - predicted_min))
        error_percent = worst / ref_min * dec(100)
        if error_percent > max_err:
            reasons.append('independent voltage holdout exceeds error budget')

    return {
        'role': c.role, 'meter_id': c.meter_id, 'reference_id': c.reference_id,
        'source_kind': c.source_kind, 'raw_holdout_mv': c.check_raw_mv,
        'nominal_predicted_holdout_mv': str(nominal),
        'independent_reference_holdout_mv': str(vcheck),
        'conditional_worst_case_error_percent': str(error_percent) if error_percent is not None else None,
        'limit_percent': str(max_err), 'temperature_delta_c': str(delta_temp),
        'pass_conditional_model': error_percent is not None and error_percent <= max_err,
        'voltage_bench_candidate': not reasons, 'blockers': reasons,
        'hardware_approved': False, 'lithium_charge_approved': False,
    }


def screen_pair(tx: Channel, rx: Channel) -> dict:
    if (tx.role, rx.role) != ('TX', 'RX') or tx.meter_id == rx.meter_id:
        raise ValueError('different physical TX/RX meters required')
    out_tx, out_rx = screen_channel(tx), screen_channel(rx)
    return {
        'evidence_kind': 'SYNTHETIC-BUS-VOLTAGE-CALIBRATION-NOT-HARDWARE',
        'tx': out_tx, 'rx': out_rx,
        'voltage_pair_bench_candidate': out_tx['voltage_bench_candidate'] and out_rx['voltage_bench_candidate'],
        'efficiency_metrology_approved': False,
        'reason': 'W52 real current calibration, W50 acquisition and simultaneous TX/RX tests still missing',
        'independent_FOD_overtemp_cutoff_approved': False,
        'hardware_approved': False, 'battery_BMS_dock_disconnected': True,
    }


def demo() -> dict:
    b = Channel(role='TX', meter_id='TX-SYNTH-1', reference_id='VOLTMETER-SYNTH',
        source_kind='SYNTHETIC', valid_from='2026-10-29', valid_until='2026-11-29',
        as_of='2026-10-30', low_raw_mv=3000, high_raw_mv=6000, check_raw_mv=5000,
        low_ref_mv='3000', high_ref_mv='6000', check_ref_mv='5000',
        low_uncertainty_mv='3', high_uncertainty_mv='3', check_uncertainty_mv='3',
        calibration_temperature_c='25', operating_temperature_c='27',
        gain_drift_ppm_per_c='200', offset_drift_mv_per_c='0.5')
    rx = replace(b, role='RX', meter_id='RX-SYNTH-2', check_raw_mv=4000, check_ref_mv='4000')
    result = screen_pair(b, rx)
    result['bad_rx_holdout_example'] = screen_channel(replace(rx, check_raw_mv=3840))
    result['model_inputs_are_fictitious'] = True
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--demo', action='store_true')
    parser.add_argument('--out', default='-')
    args = parser.parse_args()
    if not args.demo:
        parser.error('only synthetic demonstration is supported; NO hardware I2C')
    content = json.dumps(demo(), sort_keys=True, ensure_ascii=False, indent=2) + '\n'
    if args.out == '-':
        print(content, end='')
    else:
        Path(args.out).write_text(content, encoding='utf-8')


if __name__ == '__main__':
    main()
