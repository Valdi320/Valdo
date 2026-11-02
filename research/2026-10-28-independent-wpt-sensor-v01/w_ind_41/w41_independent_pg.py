"""W-IND-41: analytical 3V3 supervision screen; NO safety validation.

Own engineering equations, not semiconductor simulation. The +/-1uA input
bias is an intentionally hypothetical stress, NOT a TPS3700 datasheet limit.
"""
from dataclasses import dataclass
from itertools import product
import argparse
import json
from pathlib import Path

REF_NOMINAL_V = 0.400
REF_CORNER_FRACTION = 0.01
RESISTOR_CORNER_FRACTION = 0.01
LEAK_STRESS_A = 1e-6  # adversarial assumption; NOT TI-characterized leakage
NORMAL_RAIL_MIN_V = 3.3 * 0.95  # hypothetical requirement
DEAD_RAIL_MAX_V = 2.70  # test target; not real INA301 characterization


@dataclass(frozen=True)
class Divider:
    name: str
    top_ohm: float
    bottom_ohm: float

    def crossing_v(self, reference_v, top_ohm, bottom_ohm, sink_from_sense_a=0.):
        if min(top_ohm, bottom_ohm, reference_v) <= 0:
            raise ValueError('positive parameters required')
        # KCL: pin sink current increases source-rail crossing voltage.
        return reference_v * (1.0 + top_ohm/bottom_ohm) + sink_from_sense_a * top_ohm

    def corners(self, sink_stress_a=LEAK_STRESS_A):
        if sink_stress_a < 0:
            raise ValueError('stress must not be negative')
        cases = [self.crossing_v(ref, self.top_ohm*tr, self.bottom_ohm*br, leak)
                 for ref,tr,br,leak in product(
                     (REF_NOMINAL_V*(1-REF_CORNER_FRACTION),
                      REF_NOMINAL_V*(1+REF_CORNER_FRACTION)),
                     (1-RESISTOR_CORNER_FRACTION,1+RESISTOR_CORNER_FRACTION),
                     (1-RESISTOR_CORNER_FRACTION,1+RESISTOR_CORNER_FRACTION),
                     (-sink_stress_a,+sink_stress_a))]
        return min(cases),max(cases)

    def record(self):
        lo,hi = self.corners()
        return dict(nominal_trip_v=self.crossing_v(REF_NOMINAL_V,self.top_ohm,self.bottom_ohm),
                    minimum_trip_v=lo, maximum_trip_v=hi,
                    no_false_trip_margin_v=NORMAL_RAIL_MIN_V-hi,
                    guaranteed_trip_for_rail_at_or_below_v=lo,
                    divider_current_at_3v3_ua=1e6*3.3/(self.top_ohm+self.bottom_ohm),
                    divider_power_at_3v3_mw=1000*3.3**2/(self.top_ohm+self.bottom_ohm),
                    stress_pass=lo>DEAD_RAIL_MAX_V and hi<NORMAL_RAIL_MIN_V)


LOW_Z = Divider('62k_10k_1pct',62000.,10000.)
HIGH_Z = Divider('620k_100k_1pct',620000.,100000.)
TOO_HIGH = Divider('68k_10k_1pct',68000.,10000.)
CANDIDATES=(LOW_Z,HIGH_Z,TOO_HIGH)


def idealized_permission(supply_5v, rail_3v3, local_rearmed,
                         comparator_stuck_released=False, wire_open=False,
                         external_5v_good=True):
    """Ideal NOT hardware: upstream 5V-qualified pull-up and pull-down.

    Broken OUTA or high-Z-stuck is a dangerous negative control. The output
    needs physical latching/interlock before any power application.
    """
    v5_ok = 4.5 <= supply_5v <= 5.5 and external_5v_good
    output_sinking = rail_3v3 <= LOW_Z.corners()[0] and not (
        comparator_stuck_released or wire_open)
    permission = bool(v5_ok and local_rearmed and not output_sinking)
    return {'v5_ok_assumed':v5_ok,'outa_sink_assumed':output_sinking,
            'request_on':permission,'unsafe_if_3v3_dead':permission and rail_3v3<=DEAD_RAIL_MAX_V}


def evidence():
    records={d.name:d.record() for d in CANDIDATES}
    fault_cases={
      'rail_3v3_lost_5v_alive':idealized_permission(5.,0.,True),
      'rail_3v3_lost_relay_wire_open':idealized_permission(5.,0.,True,wire_open=True),
      'rail_3v3_lost_comparator_stuck_released':idealized_permission(5.,0.,True,comparator_stuck_released=True),
      'rail_5v_lost_3v3_leak':idealized_permission(0.,3.3,True),
      'rail_5v_partial_uncertain':idealized_permission(2.2,0.,True),
      'local_not_rearmed':idealized_permission(5.,3.3,False),
      'normal_armed':idealized_permission(5.,3.3,True),
      '5v_supervisor_rejects':idealized_permission(5.,3.3,True,external_5v_good=False),
    }
    return {'schema':'VALDO_W41_DIVERSE_SUPPLY_PG_SCREEN_V1',
            'classification':'ANALYTICAL_CORNERS_AND_SYNTHETIC_FAULTS',
            'source_power':'RX5_SOURCE_BEFORE_CUT; NOT INA301_3V3',
            'candidate':'TPS3700DDCR_OUTA_OPEN_DRAIN_NOT_SELF_POWERED',
            'input_leakage_stress_a':LEAK_STRESS_A,
            'input_leakage_stress_is_TEXAS_INSTRUMENTS_SPEC':False,
            'resistor_nominal_tolerance':RESISTOR_CORNER_FRACTION,
            'reference_tolerance':REF_CORNER_FRACTION,
            'target_healthy_min_v':NORMAL_RAIL_MIN_V,
            'target_dead_max_v':DEAD_RAIL_MAX_V,
            'dividers':records,'fault_cases':fault_cases,
            'recommended_for_further_electrical_design':'62k_10k_1pct',
            'qualified_physical_interlock':False,'hardware_tested':False,
            'battery_bms_dock_connected':False,'safe_to_energize':False,
            'missing_electrical_evidence':['INA301 selective loss and leakage',
                'TPS3700 hysteresis and pin current at temperature','5V PG POR/hold-up',
                'OUTA wire open and backfeed','EN loading and two cuts response',
                'FOD thermal EMI offset','rearm W37 in KiCad']}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path)
    args=parser.parse_args();payload=json.dumps(evidence(),indent=2,sort_keys=True)+'\n'
    if args.out:args.out.write_text(payload,encoding='utf-8')
    print(payload,end='')


if __name__=='__main__':main()
