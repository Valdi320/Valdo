"""W-IND-33: source-owned, unpowered RX permit specifications and logic.

NOT a physical cutoff, KiCad netlist, SPICE or hardware safety approval.
TI SN74LVC1G74 DCU8, TPS3839 DBZ3, INA301 manufacturer PDFs consulted.
No external source code was copied.
"""
from dataclasses import dataclass
from itertools import product
import json

DFF_DCU8 = {"CLK":1,"D":2,"Q_N":3,"GND":4,"Q":5,"CLR_N":6,"PRE_N":7,"VCC":8}
SUPERVISOR_DBZ3 = {"GND":1,"RESET_N":2,"VDD":3}
PARTS = {"supervisors":{"part":"TPS3839K50DBZR","quantity":2},
         "latches":{"part":"SN74LVC1G74DCUR","quantity":2},
         "alarm_diodes":{"part":"BAT54 (package UNQUALIFIED)","quantity":2}}
# A symbolic wiring contract; NOT verified real KiCad or an installed assembly.
INTERFACE = {
  "RAIL_5V":("SUP_A.VDD3","SUP_B.VDD3","FF_A.VCC8","FF_B.VCC8",
             "FF_A.D2","FF_B.D2","FF_A.PRE_N7","FF_B.PRE_N7"),
  "LOCAL_BUTTON_ONLY":("FF_A.CLK1","FF_B.CLK1","CLK_PULLDOWN_100K"),
  "SUP_A_RESET_N":("SUP_A.RESET_N2","R_SER_A_10K"),
  "SUP_B_RESET_N":("SUP_B.RESET_N2","R_SER_B_10K"),
  "CLEAR_A_N":("R_SER_A_10K","FF_A.CLR_N6","DIODE_A.ANODE","R_PD_A_100K"),
  "CLEAR_B_N":("R_SER_B_10K","FF_B.CLR_N6","DIODE_B.ANODE","R_PD_B_100K"),
  "INA301_ALERT_N":("DIODE_A.CATHODE","DIODE_B.CATHODE","PULLUP_10K"),
  "EN_A_PROPOSED":("FF_A.Q5","EN_PULLDOWN_A_10K","W32.U2.EN1_NOT_CONNECTED"),
  "EN_B_PROPOSED":("FF_B.Q5","EN_PULLDOWN_B_10K","W32.U3.EN1_NOT_CONNECTED"),
}
MANUFACTURER = {
 "TPS3839": "https://www.ti.com/lit/ds/symlink/tps3839.pdf",
 "SN74LVC1G74": "https://www.ti.com/lit/ds/symlink/sn74lvc1g74.pdf",
 "INA301": "https://www.ti.com/lit/ds/symlink/ina301.pdf",
 "TPS25947": "https://www.ti.com/product/TPS25947"
}
def nominal_budget(volts=5.0, series_ohm=10000.0, pulldown_ohm=100000.0):
    """ARITHMETIC only; no worst-case diode VF/IR or PCB fault qualification."""
    high = volts * pulldown_ohm / (pulldown_ohm + series_ohm)
    # 2 CLR series feeds + W33 ALERT pullup + W32 already-existing ALERT pullup.
    sink_ideal_amps = 4.0 * volts / series_ohm
    return dict(clear_high_v=round(high,6),
                lvc_vih_v=round(.7*volts,6),
                alert_sink_ideal_ma=round(sink_ideal_amps*1000,6),
                ina301_datasheet_test_ma=3.0,
                reset_nominal_threshold_v=4.38,
                reset_delay_min_ms=120,
                reset_delay_max_ms=350,
                reset_valid_only_above_v=.6,
                possible_unpowered_monitor_fault=True,
                analog_trip_levels_qualified=False,
                physical_cut_qualified=False)
@dataclass(frozen=True)
class Signals:
    voltage_ok:bool=True
    alert_not_asserted:bool=True
    supervisor_a_ok:bool=True
    supervisor_b_ok:bool=True
    button:bool=False
    ff_a_stuck_high:bool=False
    ff_b_stuck_high:bool=False

class PositivePermits:
    """Ideal async CLR/reset and edge CLK, no power/noise/temperature dynamics."""
    def __init__(self):
        self.q_a=False;self.q_b=False;self.prev_button=False
    def step(self, s:Signals, *, radio_rearm=False):
        rising=s.button and not self.prev_button
        self.prev_button=s.button
        good_a=s.voltage_ok and s.alert_not_asserted and s.supervisor_a_ok
        good_b=s.voltage_ok and s.alert_not_asserted and s.supervisor_b_ok
        if not good_a:self.q_a=False
        elif rising:self.q_a=True
        if not good_b:self.q_b=False
        elif rising:self.q_b=True
        en_a=s.voltage_ok and (self.q_a or s.ff_a_stuck_high)
        en_b=s.voltage_ok and (self.q_b or s.ff_b_stuck_high)
        return dict(en_a=en_a,en_b=en_b,both_en=en_a and en_b,
                    safety_rearm_via_radio=False,needs_local_edge=not(self.q_a and self.q_b))

def enumerate_faults():
    fields=("voltage_ok","alert_not_asserted","supervisor_a_ok",
            "supervisor_b_ok","ff_a_stuck_high","ff_b_stuck_high")
    unsafe=[]
    for bits in product((False,True),repeat=len(fields)):
        s=Signals(**dict(zip(fields,bits)))
        model=PositivePermits()
        model.step(Signals(button=True))
        out=model.step(s)
        required=s.voltage_ok and s.alert_not_asserted and s.supervisor_a_ok and s.supervisor_b_ok
        if out["both_en"] and not required:
            unsafe.append({name:getattr(s,name) for name in fields})
    return dict(cases=64,unsafe_logic_counterexamples=len(unsafe),
                examples=unsafe,hardware_power_authorized=False,
                no_radio_critical_control=True)
if __name__ == "__main__":
    print(json.dumps({"model":enumerate_faults(),"nominal":nominal_budget(),
                      "interface_is_not_connected_to_w32":True},indent=2,sort_keys=True))
