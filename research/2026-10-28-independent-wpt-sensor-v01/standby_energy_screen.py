"""W-IND-11: deterministic no-load TX standby screen for a NEW open robot.

Original VALDO engineering study; Python standard library only.
The numbers supplied by a vendor are NOT verified measurements or a FOD claim.
Does not control, enable, charge, or interact with any physical electronics.
"""
from dataclasses import dataclass
from math import isfinite


def _real(name: str, value: float, *, minimum: float = 0.0) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} requires a finite real value")
    number = float(value)
    if not isfinite(number) or number < minimum:
        raise ValueError(f"{name} outside allowed range")
    return number


@dataclass(frozen=True)
class Scenario:
    modules: int
    tx_voltage_v: float
    no_load_current_min_a: float
    no_load_current_max_a: float
    absent_hours_per_day: float
    assumed_off_power_w_per_tx: float
    days_per_year: int = 365
    horizon_years: float = 5.0
    electricity_eur_per_kwh: float = 0.25

    def __post_init__(self) -> None:
        if type(self.modules) is not int or not 1 <= self.modules <= 64:
            raise ValueError("modules must be an integer 1..64")
        if type(self.days_per_year) is not int or not 1 <= self.days_per_year <= 366:
            raise ValueError("days_per_year must be 1..366")
        for key in ("tx_voltage_v", "no_load_current_min_a", "no_load_current_max_a",
                    "absent_hours_per_day", "assumed_off_power_w_per_tx",
                    "horizon_years", "electricity_eur_per_kwh"):
            _real(key, getattr(self, key))
        if not 0 < self.tx_voltage_v <= 24:
            raise ValueError("invalid hypothetical voltage")
        if not 0 <= self.no_load_current_min_a <= self.no_load_current_max_a <= 1:
            raise ValueError("invalid no-load current envelope")
        if not 0 <= self.absent_hours_per_day <= 24:
            raise ValueError("hours_per_day must be <= 24")
        if self.assumed_off_power_w_per_tx > self.tx_voltage_v:
            raise ValueError("off power implausibly above 1-A reference envelope")
        if self.horizon_years > 30 or self.electricity_eur_per_kwh > 5:
            raise ValueError("outside bounded exploratory scenario")


@dataclass(frozen=True)
class Screen:
    all_on_no_load_w_min: float
    all_on_no_load_w_max: float
    all_off_assumed_w: float
    always_on_absent_wh_day_min: float
    always_on_absent_wh_day_max: float
    gated_absent_wh_day: float
    saved_absent_wh_day_min: float
    saved_absent_wh_day_max: float
    saved_absent_kwh_horizon_min: float
    saved_absent_kwh_horizon_max: float
    saved_absent_eur_horizon_min: float
    saved_absent_eur_horizon_max: float
    real_power_tested: bool = False
    hardware_safe_to_enable: bool = False


def screen(scenario: Scenario) -> Screen:
    """Compare ONLY time with NO receiver/load, never invent loaded efficiency.

    Assumes vendor no-load current applies whenever a TX is left enabled with
    no module. Off-state power is explicitly hypothetical until measured.
    Does NOT account for MCU/radio, switch losses under load, coil coupling,
    battery capacity, active module time, or thermals.
    """
    s = scenario
    pmin = s.modules * s.tx_voltage_v * s.no_load_current_min_a
    pmax = s.modules * s.tx_voltage_v * s.no_load_current_max_a
    poff = s.modules * s.assumed_off_power_w_per_tx
    idle_min = pmin * s.absent_hours_per_day
    idle_max = pmax * s.absent_hours_per_day
    off = poff * s.absent_hours_per_day
    saved_min = idle_min - off
    saved_max = idle_max - off
    years_factor = s.days_per_year * s.horizon_years / 1000.0
    return Screen(pmin, pmax, poff, idle_min, idle_max, off,
                  saved_min, saved_max,
                  saved_min * years_factor, saved_max * years_factor,
                  saved_min * years_factor * s.electricity_eur_per_kwh,
                  saved_max * years_factor * s.electricity_eur_per_kwh)


def standby_budget_pass(s: Scenario, ceiling_w: float) -> bool:
    """Pass/fail of a HYPOTHETICAL no-module standby wattage budget only."""
    ceiling = _real("ceiling_w", ceiling_w)
    return screen(s).all_on_no_load_w_max <= ceiling


def part_floor_eur(quantity: int, unit_inc_vat_eur: float,
                   shipping_floor_inc_vat_eur: float) -> float:
    """Advertised arithmetic floor; NOT a final delivered or qualified BOM."""
    if type(quantity) is not int or not 1 <= quantity <= 64:
        raise ValueError("invalid quantity")
    unit = _real("unit_price", unit_inc_vat_eur)
    shipping = _real("shipping_floor", shipping_floor_inc_vat_eur)
    return round(quantity * unit + shipping, 2)


def example() -> Screen:
    return screen(Scenario(8, 5.0, .030, .050, 24.0, .005))


if __name__ == "__main__":
    x = example()
    print(f"8 TX: vendor NO-LOAD envelope={x.all_on_no_load_w_min:.2f}..{x.all_on_no_load_w_max:.2f} W")
    print(f"24h without receivers={x.always_on_absent_wh_day_min:.2f}..{x.always_on_absent_wh_day_max:.2f} Wh")
    print(f"5mW/TX HYPOTHETICAL OFF savings={x.saved_absent_wh_day_min:.2f}..{x.saved_absent_wh_day_max:.2f} Wh/day")
    print("APPROVAL=False; no TX measured, no independent physical FOD or cutoff")
