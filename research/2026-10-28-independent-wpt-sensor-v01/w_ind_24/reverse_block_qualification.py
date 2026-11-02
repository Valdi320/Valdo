"""W-IND-24: conservative datasheet screen, not an electrical safety approval.
Original independent analysis; no third-party firmware, PCB or code copied.
"""
from __future__ import annotations
from dataclasses import dataclass
import json
import math
from typing import Optional

@dataclass(frozen=True)
class Candidate:
    name: str
    source: str
    vin_min_v: float
    vin_max_v: float
    ron_typ_ohm: float
    iq_typ_a: float
    ilim_min_a: Optional[float]
    current_monitor_accuracy_min_a: Optional[float]
    true_reverse_block: bool
    revision: str

# Manufacturer TYPICAL values only; no guaranteed tolerance / temperature bound.
CANDIDATES = {
    "TPS22918DBVR": Candidate("TPS22918DBVR", "https://www.ti.com/product/TPS22918", 1, 5.5, .052, 8.7e-6, None, None, False, "Rev. C"),
    "TPS25210ARPWR": Candidate("TPS25210ARPWR", "https://www.ti.com/product/TPS2521", 2.7, 5.7, .031, 411e-6, .5, 1.0, True, "Rev. A"),
    "TPS259474ARPWR": Candidate("TPS259474ARPWR", "https://www.ti.com/product/TPS25947", 2.7, 23, .0283, 426e-6, .5, 1.0, True, "Rev. C"),
}

def screen(part: str, *, supply_v: float = 5.0, average_w: float = .4,
           peak_w: float = 1.5, detectable_fault_a: float = .4,
           internal_pass_fet_short: bool = False) -> dict:
    """Illustrative single-device DC screen. Fault current is an ASSUMPTION,
    not a real hardware trip threshold or a power-on permission."""
    if part not in CANDIDATES:
        raise ValueError("unreviewed part")
    vals = (supply_v, average_w, peak_w, detectable_fault_a)
    if not all(math.isfinite(v) for v in vals):
        raise ValueError("non-finite input")
    if supply_v <= 0 or average_w < 0 or peak_w < average_w or detectable_fault_a <= 0:
        raise ValueError("invalid illustrative envelope")
    c = CANDIDATES[part]
    ia, ip = average_w / supply_v, peak_w / supply_v
    vin_ok = c.vin_min_v <= supply_v <= c.vin_max_v
    healthy = c.true_reverse_block and vin_ok
    floor_above_fault = c.ilim_min_a is None or detectable_fault_a < c.ilim_min_a
    monitor_qualified = (c.current_monitor_accuracy_min_a is not None
                         and ia >= c.current_monitor_accuracy_min_a)
    return {
        "part": part, "manufacturer_spec_revision": c.revision,
        "source": c.source, "datasheet_operating_vin_ok": vin_ok,
        "average_current_a_assumed": round(ia, 9),
        "peak_current_a_assumed": round(ip, 9),
        "manufacturer_claims_healthy_reverse_block": healthy,
        "reverse_block_with_injected_internal_short": healthy and not internal_pass_fet_short,
        "current_limit_floor_a": c.ilim_min_a,
        "assumed_fault_below_configurable_limit_floor": floor_above_fault,
        "assumed_peak_below_limit_floor": c.ilim_min_a is not None and ip < c.ilim_min_a,
        "current_monitor_accuracy_qualified_at_assumed_average": monitor_qualified,
        "typical_avg_device_overhead_mw": round((ia**2 * c.ron_typ_ohm + supply_v*c.iq_typ_a)*1000, 6),
        "typical_peak_device_overhead_mw": round((ip**2 * c.ron_typ_ohm + supply_v*c.iq_typ_a)*1000, 6),
        "autonomous_fod_proven": False, "independent_thermal_cut_proven": False,
        "independent_overcurrent_cut_proven": False, "reverse_block_hardware_measured": False,
        "hardware_approved": False, "power_on_allowed": False,
        "decision": "DATASHEET_CANDIDATE_ONLY_NO_POWER",
        "scope": "isolated 5V sensor module; dock/battery/RF separate",
    }

def summary() -> dict:
    return {"schema": "W-IND-24-v1",
            "method": "manufacturer datasheet and arithmetic; no measured sample",
            "assumptions": {"supply_v": 5, "avg_w": .4, "peak_w": 1.5, "desired_fault_a": .4},
            "candidates": [screen(p) for p in sorted(CANDIDATES)], "hardware_approved": False}

if __name__ == "__main__":
    print(json.dumps(summary(), indent=2, sort_keys=True))
