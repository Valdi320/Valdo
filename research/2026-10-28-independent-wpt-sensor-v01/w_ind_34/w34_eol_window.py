"""W-IND-34: original, unpowered end-of-line ALERT continuity screening.

This is a DC resistor/window arithmetic model, not a validated comparator,
KiCad schematic, normally-off physical shutdown, FOD or safety certification.
All analog limits and supply ranges below are DESIGN ASSUMPTIONS, not
manufacturer limits. No third-party source code is included.
"""
from dataclasses import dataclass, asdict
from itertools import product
import json

@dataclass(frozen=True)
class Corner:
    rail_v: float = 5.0
    pullup_ohm: float = 10000.0
    eol_ohm: float = 10000.0
    wire_ohm: float = 0.0
    lower_ratio: float = 0.40
    upper_ratio: float = 0.60
    comparator_offset_v: float = 0.0
    extra_pullup_ohm: float | None = None


def probe(c: Corner, *, alarm=False, signal_open=False, return_open=False,
          signal_short=False, eol_open=False, eol_short=False,
          monitor_power_good=True, rail_supervised=True, local_armed=True):
    """Near-end ratiometric window, ideal switches; not real analogue timing.

    The EOL resistor is at the remote INA301 end. A broken signal wire or
    remote ground return looks like high-Z, and an asserted ALERT like low.
    An unpowered open-drain monitor ALSO looks healthy unless separately PG.
    """
    if c.rail_v <= 0 or min(c.pullup_ohm, c.eol_ohm) <= 0:
        raise ValueError('positive rail and resistances required')
    if not 0 <= c.lower_ratio < c.upper_ratio <= 1 or c.wire_ohm < 0:
        raise ValueError('invalid window or wire resistance')
    if c.extra_pullup_ohm is not None and c.extra_pullup_ohm <= 0:
        raise ValueError('invalid second pullup')
    rp = c.pullup_ohm
    if c.extra_pullup_ohm is not None:
        rp = 1.0 / (1.0 / rp + 1.0 / c.extra_pullup_ohm)
    if signal_short or eol_short or alarm:
        sensed_v = 0.0  # ideal low; VOL and burden not qualified
    elif signal_open or return_open or eol_open:
        sensed_v = c.rail_v
    else:
        rg = c.eol_ohm + c.wire_ohm
        sensed_v = c.rail_v * rg / (rp + rg)
    observed_ratio = (sensed_v + c.comparator_offset_v) / c.rail_v
    in_window = c.lower_ratio <= observed_ratio <= c.upper_ratio
    # Desired logical contract only: no demonstrated enforcement hardware.
    permit_request = bool(in_window and monitor_power_good and
                          rail_supervised and local_armed)
    return dict(observed_ratio=observed_ratio, in_window=in_window,
                permit_request=permit_request,
                monitor_power_good_required=True,
                hardware_power_authorized=False,
                physical_comparator_verified=False)


def corner_grid():
    for rail, rp, re, rw, low, high, offset in product(
            (4.5, 5.5), (9500.0, 10500.0), (9500.0, 10500.0),
            (0.0, 100.0), (0.38, 0.42), (0.58, 0.62), (-0.025, 0.025)):
        yield Corner(rail, rp, re, rw, low, high, offset)


def evidence():
    cases = list(corner_grid())
    scenarios = {
        'intact': lambda c: probe(c),
        'alert_asserted_ideal': lambda c: probe(c, alarm=True),
        'signal_open': lambda c: probe(c, signal_open=True),
        'return_open': lambda c: probe(c, return_open=True),
        'signal_short': lambda c: probe(c, signal_short=True),
        'eol_open': lambda c: probe(c, eol_open=True),
        'eol_short': lambda c: probe(c, eol_short=True),
        'duplicate_10k_pullup': lambda c: probe(Corner(**{
            **asdict(c), 'extra_pullup_ohm': c.pullup_ohm})),
        'monitor_unpowered_pg_absent': lambda c: probe(c, monitor_power_good=False),
    }
    passing = {name: sum(bool(run(c)['permit_request']) for c in cases)
               for name, run in scenarios.items()}
    vdd_dead_undetected_by_passives = sum(
        probe(c, monitor_power_good=False)['in_window'] for c in cases)
    ratios = [probe(c)['observed_ratio'] for c in cases]
    margin = min(min(probe(c)['observed_ratio'] - c.lower_ratio,
                     c.upper_ratio - probe(c)['observed_ratio']) for c in cases)
    return dict(corners=len(cases), scenario_pass_counts=passing,
                total_scenario_checks=len(cases)*len(scenarios),
                healthy_ratio_min=min(ratios), healthy_ratio_max=max(ratios),
                minimum_window_margin_ratio=margin,
                monitor_off_without_pg_misses=vdd_dead_undetected_by_passives,
                drift_14k_nominal_is_undetected=probe(Corner(eol_ohm=14000))['in_window'],
                hardware_power_authorized=False,
                safety_verified=False,
                source_category='DESIGN ASSUMPTIONS / CPU ARITHMETIC')

if __name__ == '__main__':
    print(json.dumps(evidence(), indent=2, sort_keys=True))
