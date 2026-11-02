"""Hypothetical screening only. No coil model, FOD certification or safety approval."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Budget:
    output_w: float
    input_w: float
    loss_w: float
    effective_efficiency: float


def screen(v_rx: float, i_rx: float, nominal_eta: float, offset_factor: float) -> Budget:
    if not (0 < v_rx <= 24 and 0 <= i_rx <= 1 and
            0 < nominal_eta <= 1 and 0 < offset_factor <= 1):
        raise ValueError("invalid hypothetical parameters")
    efficiency = nominal_eta * offset_factor
    output = v_rx * i_rx
    incoming = output / efficiency
    return Budget(round(output, 6), round(incoming, 6),
                  round(incoming - output, 6), round(efficiency, 6))


def hold_up_farads(power_w: float, dropout_s: float, v_high: float, v_low: float) -> float:
    """Ideal capacitor ONLY: ignores ESR, regulator efficiency, cell chemistry and ageing."""
    if not (power_w >= 0 and dropout_s >= 0 and v_high > v_low >= 0):
        raise ValueError("invalid hold-up")
    return 2 * power_w * dropout_s / (v_high**2 - v_low**2)
