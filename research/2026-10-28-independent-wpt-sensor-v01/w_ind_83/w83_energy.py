"""W83: synthetic RF burst energy screen for optional low-consumption sensor.
Not a physical RF, electrical, EMI or WPT safety qualification.
"""
from dataclasses import dataclass
from decimal import Decimal, getcontext
import json
getcontext().prec = 32

def D(x):
    return Decimal(str(x))

@dataclass(frozen=True)
class Envelope:
    v_hi: Decimal
    v_floor: Decimal
    c_effective_f: Decimal
    rx_mw: Decimal
    idle_mw: Decimal
    pulse_total_mw: Decimal
    pulse_ms: Decimal
    period_ms: Decimal
    pulses: int

    def validate(self):
        nums = (self.v_hi, self.v_floor, self.c_effective_f, self.rx_mw, self.idle_mw,
                self.pulse_total_mw, self.pulse_ms, self.period_ms)
        if not all(isinstance(x, Decimal) and x.is_finite() for x in nums):
            raise ValueError("finite Decimal required")
        if self.v_hi <= self.v_floor or self.v_floor <= 0:
            raise ValueError("voltage order invalid")
        if min(self.c_effective_f, self.rx_mw, self.idle_mw, self.pulse_total_mw) < 0:
            raise ValueError("negative energy/power")
        if not 0 < self.pulse_ms <= self.period_ms:
            raise ValueError("invalid pulse timing")
        if type(self.pulses) is not int or self.pulses < 1:
            raise ValueError("invalid count")

def event_energy_j(power_mw, duration_ms):
    return power_mw * duration_ms / D(1000000)

def simulate(e: Envelope):
    e.validate()
    usable_j = e.c_effective_f * (e.v_hi ** 2 - e.v_floor ** 2) / 2
    one_pulse_deficit = max(D(0), event_energy_j(e.pulse_total_mw-e.rx_mw,e.pulse_ms))
    min_c = 2*one_pulse_deficit/(e.v_hi**2-e.v_floor**2)
    rest_ms = e.period_ms - e.pulse_ms
    need = event_energy_j(e.pulse_total_mw,e.pulse_ms)+event_energy_j(e.idle_mw,rest_ms)
    provided = event_energy_j(e.rx_mw,e.period_ms)
    average = need*D(1000000)/e.period_ms
    stored = usable_j
    first_brownout = None
    events = []
    for i in range(e.pulses):
        if i:
            stored = min(usable_j,stored+event_energy_j(e.rx_mw-e.idle_mw,rest_ms))
        before = stored
        stored = min(usable_j,stored+event_energy_j(e.rx_mw-e.pulse_total_mw,e.pulse_ms))
        safe_in_ideal_model = stored >= 0
        events.append({"pulse":i+1,"before_j":str(before),"after_j":str(stored),
                       "above_floor":safe_in_ideal_model})
        if not safe_in_ideal_model:
            first_brownout = i+1
            break
    return {"evidence_class":"synthetic_ideal_envelope_only",
            "max_capacitor_energy_j":str(usable_j),
            "min_effective_cap_for_one_pulse_f":str(min_c),
            "average_required_mw":str(average),
            "assumed_delivered_rx_mw":str(e.rx_mw),
            "cycle_net_energy_j":str(provided-need),
            "cycle_unsustainable_indefinitely":need>provided,
            "first_brownout_pulse":first_brownout,
            "pulse_history":events,
            "approved_for_hardware":False}

def demo():
    # Espressif ESP32-C3 datasheet v2.4 Table 5-7: 335mA peak, 3.3V, 802.11b
    # 1Mbps/21dBm TX mode @25C. NOT ESP-NOW TX duration or assured peak.
    mode_mw = D("3.3")*D("335")
    e = Envelope(D("3.3"),D("3.0"),D("0.015"),D("20"),D("2.9"),
                 mode_mw,D("10"),D("250"),6)
    return {"model":"W-IND-83",
            "reference_radio":"ESP32-C3 Table 5-7 335mA RF mode",
            "hypothetical_tx_ms":"10","hypothetical_rx_output_mw":"20",
            "baseline_idling_mw":"2.9",
            "source":"https://documentation.espressif.com/esp32-c3_datasheet_en.html",
            "result":simulate(e)}

if __name__ == "__main__":
    print(json.dumps(demo(),indent=2,sort_keys=True))
