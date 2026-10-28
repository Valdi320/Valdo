"""W-IND-07: synthetic fail-closed TX thermistor window + dual cut contract.

DESIGN STUDY ONLY. No GPIO, PWM, power electronics, lithium charger, or WPT hardware.
Window and fault inputs are abstractions, not measured sensor behavior or certified safety.
"""
from dataclasses import dataclass
from itertools import product
from math import exp, isfinite

LOW_RATIO = 0.27                # purely proposed ratiometric trip threshold
HIGH_RATIO = 0.88               # proposed open-wire/cold trip threshold
LOW_UNCERTAINTY = (0.26, 0.28)  # hypothetical comparator/reference error
HIGH_UNCERTAINTY = (0.87, 0.89)


def ntc_ratio(temp_c: float, *, r25_ohm: float = 10000.0,
              beta_k: float = 3950.0, pullup_ohm: float = 10000.0) -> float:
    """Divider with NTC to ground and resistor to VREF; returns V_NTC/VREF.

    Beta approximation is hypothetical beyond calibration points and is not a
    safety-grade thermometry model. No thermal contact, delay, self-heating or
    comparator propagation time is included.
    """
    values = [float(v) for v in (temp_c, r25_ohm, beta_k, pullup_ohm)]
    if any(not isfinite(x) for x in values) or values[0] <= -273.15 or any(x <= 0 for x in values[1:]):
        raise ValueError('invalid temperature or divider parameter')
    t, r25, beta, pullup = values
    r_ntc = r25 * exp(beta * (1.0 / (t + 273.15) - 1.0 / 298.15))
    return r_ntc / (r_ntc + pullup)


def window_clear(ratio: float | None, low: float = LOW_RATIO,
                 high: float = HIGH_RATIO) -> bool:
    """Open (ratio 1), short (0), missing/invalid must fail OFF."""
    if ratio is None or isinstance(ratio, bool):
        return False
    try:
        x = float(ratio)
    except (ValueError, TypeError, OverflowError):
        return False
    return isfinite(x) and 0 <= x <= 1 and low < x < high


def corner_sweep(temp_c: float) -> tuple[float, ...]:
    """8 assumed component corners, not statistical distribution or tolerance certification."""
    return tuple(ntc_ratio(temp_c, r25_ohm=r, beta_k=b, pullup_ohm=p)
                 for r, b, p in product((9500.0, 10500.0),
                                        (3850.0, 4050.0), (9900.0, 10100.0)))


def all_corners_clear(temp_c: float) -> bool:
    """Conservative unknown threshold phase: all 8*4 combinations clear."""
    return all(window_clear(value, low, high)
               for value, low, high in product(corner_sweep(temp_c),
                                                LOW_UNCERTAINTY, HIGH_UNCERTAINTY))


def all_corners_trip(temp_c: float) -> bool:
    return all(not window_clear(value, low, high)
               for value, low, high in product(corner_sweep(temp_c),
                                                LOW_UNCERTAINTY, HIGH_UNCERTAINTY))


@dataclass(frozen=True)
class Channel:
    """One independent *abstract* analog monitor chain, not a wired schematic.

    `fod_clear` is unqualified: there is currently NO functional FOD detector.
    Other inputs require real hardware before any physical enable.
    """
    ntc_ratio_read: float | None
    fod_clear: bool | None = None
    supervisor_ok: bool | None = None
    current_ok: bool | None = None
    dry_ok: bool | None = None
    alignment_ok: bool | None = None

    def clear(self) -> bool:
        return (window_clear(self.ntc_ratio_read)
                and self.fod_clear is True
                and self.supervisor_ok is True
                and self.current_ok is True
                and self.dry_ok is True
                and self.alignment_ok is True)


def assumed_channel(temp_c: float = 25.0, **overrides: object) -> Channel:
    """TEST FIXTURE ONLY: every 'True' is a synthetic injected healthy signal."""
    d = dict(ntc_ratio_read=ntc_ratio(temp_c), fod_clear=True,
             supervisor_ok=True, current_ok=True, dry_ok=True,
             alignment_ok=True)
    d.update(overrides)
    return Channel(**d)


class TxInterlock:
    """Temporal simulation of two normally-open series cuts with local rising-edge reset.

    A real design needs two independently capable physical disconnect paths,
    separate sensing/drive, defined reset circuit and power-on defaults. No such
    parts or board have been validated. This model NEVER proves FOD or safety.
    """
    def __init__(self):
        self._latched_a = False
        self._latched_b = False
        self._previous_reset = False

    def step(self, a: Channel, b: Channel, *, local_request: bool,
             local_reset: bool = False, supply_present: bool = True,
             cut_a_fault: str = 'normal', cut_b_fault: str = 'normal') -> dict:
        for name, value in [('local_request', local_request),
                            ('local_reset', local_reset), ('supply_present', supply_present)]:
            if type(value) is not bool:
                raise ValueError(name + ' must be bool')
        for fault in (cut_a_fault, cut_b_fault):
            if fault not in ('normal', 'welded_closed', 'stuck_open'):
                raise ValueError('invalid cut fault')
        rising_reset = local_reset and not self._previous_reset
        self._previous_reset = local_reset
        ok_a, ok_b = a.clear(), b.clear()
        if not supply_present or not local_request:
            self._latched_a = self._latched_b = False
        else:
            if not ok_a:
                self._latched_a = False
            if not ok_b:
                self._latched_b = False
            if rising_reset:
                if ok_a:
                    self._latched_a = True
                if ok_b:
                    self._latched_b = True
        command_a = local_request and supply_present and ok_a and self._latched_a
        command_b = local_request and supply_present and ok_b and self._latched_b
        effective_a = (True if cut_a_fault == 'welded_closed' else
                       False if cut_a_fault == 'stuck_open' else command_a)
        effective_b = (True if cut_b_fault == 'welded_closed' else
                       False if cut_b_fault == 'stuck_open' else command_b)
        return dict(energized=supply_present and effective_a and effective_b,
                    command_a=command_a, command_b=command_b,
                    effective_a=effective_a, effective_b=effective_b,
                    latched_a=self._latched_a, latched_b=self._latched_b,
                    theoretical_only=True, installation_approved=False)


if __name__ == '__main__':
    for temp in (-20, -10, 25, 45, 50, 55, 60):
        x = corner_sweep(temp)
        print(f'{temp:4d} C  ratio=[{min(x):.5f}, {max(x):.5f}]'
              f' all_clear={all_corners_clear(temp)} all_trip={all_corners_trip(temp)}')
