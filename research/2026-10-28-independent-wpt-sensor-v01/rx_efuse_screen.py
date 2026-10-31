"""W-IND-06: pure-Python *screening*, never an eFuse, WPT safety controller or FOD.
All library numbers are transcribed from cited manufacturer sheets in README_W_IND_06.md.
No dependency, register writes, battery, GPIO, or power control.
"""
from dataclasses import dataclass, asdict
import json
from math import isfinite, isclose


@dataclass(frozen=True)
class EFuse:
    name: str
    limit_min_a: float
    limit_max_a: float
    tolerance_fraction: float | None
    evidence: str


TPS2663 = EFuse("TPS2663x", 0.60, 6.0, None, "https://www.ti.com/product/TPS2663")
TPS25947 = EFuse("TPS25947xx", 0.50, 6.0, None, "https://www.ti.com/product/TPS25947")
TPS259630 = EFuse("TPS259630", 0.125, 2.0, 0.104, "https://www.ti.com/product/TPS2596")
# W-IND-05 sensor-only *assumptions*; 5V interface is not a measured fact.
DEFAULT_PEAK_W = 1.5
DEFAULT_AVG_W = 0.4


def _valid_pos(x: float, field: str) -> float:
    x = float(x)
    if not isfinite(x) or x <= 0:
        raise ValueError(f"{field} must be finite and positive")
    return x


def thresholds(nominal_a: float, tolerance: float) -> tuple[float, float]:
    nominal_a = _valid_pos(nominal_a, "nominal_a")
    if not isfinite(float(tolerance)) or not 0 <= tolerance < 1:
        raise ValueError("invalid tolerance")
    return nominal_a * (1 - tolerance), nominal_a * (1 + tolerance)


def screen_rx(device: EFuse, *, nominal_limit_a: float, peak_w: float = DEFAULT_PEAK_W,
              v_rx_min: float = 4.5, fault_current_a: float = 0.5) -> dict:
    """Worst-case tolerance screening for the *receiver DC rail*, not transmitter FOD.

    A limit must exceed maximum assumed load current even at its low-tolerance edge;
    a hypothetical fault must exceed the high-tolerance edge for guaranteed
    *threshold crossing*, not guaranteed disconnect or FOD. Timing, real IC behavior,
    transients and device temperature are not modelled.
    """
    p = _valid_pos(peak_w, "peak_w")
    v = _valid_pos(v_rx_min, "v_rx_min")
    lim = _valid_pos(nominal_limit_a, "nominal_limit_a")
    fault = _valid_pos(fault_current_a, "fault_current_a")
    in_range = device.limit_min_a <= lim <= device.limit_max_a
    if device.tolerance_fraction is None:
        # Not an assumed zero tolerance: no manufacturer bound was extracted.
        return {"device": device.name, "range_supported": in_range,
                "manufacturer_tolerance_available": False,
                "steady_load_below_low_threshold": False, "fault_above_high_threshold": False,
                "paper_feasible": False, "installation_approved": False,
                "reason": "tolerance/response not qualified for this comparison"}
    lo, hi = thresholds(lim, device.tolerance_fraction)
    need = p / v
    pass_load = in_range and lo > need
    fault_beyond_threshold = in_range and fault > hi and not isclose(fault, hi, rel_tol=1e-12)
    return {"device": device.name, "range_supported": in_range,
            "manufacturer_tolerance_available": True,
            "nominal_limit_a": lim, "low_limit_a": lo, "high_limit_a": hi,
            "max_assumed_load_a": need, "assumed_fault_a": fault,
            "steady_load_below_low_threshold": pass_load,
            "fault_above_high_threshold": fault_beyond_threshold,
            "paper_feasible": pass_load and fault_beyond_threshold,
            "installation_approved": False,
            "reason": "DC threshold crossing only; IC may current-limit without disconnecting. TX FOD, coil temperature, startup, EMC and cut-off unverified"}


def input_budget(*, rx_peak_w: float, tx_supply_v: float,
                 efficiency: float, tx_controls_w: float = 0) -> dict:
    """Power conservation for *transmitter* input, not measured efficiency."""
    load = _valid_pos(rx_peak_w, "rx_peak_w")
    supply = _valid_pos(tx_supply_v, "tx_supply_v")
    extra = float(tx_controls_w)
    eta = float(efficiency)
    if not isfinite(extra) or extra < 0 or not isfinite(eta) or not 0 < eta <= 1:
        raise ValueError("invalid efficiency or auxiliary load")
    pin = load / eta + extra
    return {"tx_input_w": pin, "tx_input_a": pin / supply,
            "total_losses_w": pin - load, "efficiency_assumed": eta,
            "measured": False, "tx_fod_verified": False}


def data() -> dict:
    return {"revision": "W-IND-06", "scope": "new robot low-power sensor, RX DC only",
            "device_choice": "TPS259630 candidate, NOT approved",
            "rx_5v_0_4a": screen_rx(TPS259630, nominal_limit_a=.4),
            "other_min_ranges": {x.name: x.limit_min_a for x in (TPS2663, TPS25947)},
            "tx_example_eta55_percent": input_budget(rx_peak_w=1.5,
                                                        tx_supply_v=5, efficiency=.55, tx_controls_w=.05),
            "dock_charge_validated": False, "distributed_motor_power_validated": False,
            "physical_evidence": False}


if __name__ == "__main__":
    print(json.dumps(data(), indent=2, sort_keys=True))
