"""VALDO W-IND-02: regulator hold-up ESR/derating simulation. NOT hardware or safety firmware.
Written by VALDO; Python 3.10 standard library only.
"""
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Envelope:
    load_w: float = 1.5
    outage_ms: float = 150
    initial_v: float = 5.0
    min_regulator_input_v: float = 3.5
    efficiency: float = 0.85
    esr_ohm: float = 0.2
    retained_capacity_fraction: float = 0.6
    step_ms: float = 0.25

    def __post_init__(self):
        vals = (self.load_w, self.outage_ms, self.initial_v, self.min_regulator_input_v,
                self.efficiency, self.esr_ohm, self.retained_capacity_fraction, self.step_ms)
        if not all(isinstance(x, (int, float)) and math.isfinite(x) for x in vals):
            raise ValueError('inputs must be finite numbers')
        if (not 0 <= self.load_w <= 30 or not 0 <= self.outage_ms <= 1000
            or not 0 < self.min_regulator_input_v < self.initial_v <= 24
            or not 0 < self.efficiency <= 1 or not 0 <= self.esr_ohm <= 200
            or not 0 < self.retained_capacity_fraction <= 1 or not 0 < self.step_ms <= 5):
            raise ValueError('invalid envelope')

@dataclass(frozen=True)
class Result:
    ok: bool
    delivered_ms: float
    minimum_input_v: float
    final_cap_v: float
    peak_cap_current_a: float

def operating_point(v_cap: float, load_w: float, efficiency: float, esr_ohm: float):
    """(I, input_v) for ideal constant-power buck-boost, series capacitor ESR.
    The stable (lower current) branch solves eta*I*(Vcap-I*R)=P.
    """
    if load_w == 0:
        return (0.0, v_cap)
    disc = v_cap*v_cap - 4*esr_ohm*load_w/efficiency
    if disc < 0 or v_cap <= 0:
        return None
    current = (2*load_w/efficiency) / (v_cap + math.sqrt(disc))
    return current, v_cap-current*esr_ohm

def simulate(nominal_farads: float, env: Envelope) -> Result:
    """Finite-step discharge: Vcap change = -I*dt/Ceffective. Numerical, not measured."""
    if (not isinstance(nominal_farads, (int, float))
        or not math.isfinite(nominal_farads) or nominal_farads <= 0):
        raise ValueError('capacitance must be positive and finite')
    effective_cap = nominal_farads*env.retained_capacity_fraction
    voltage, t, max_current, min_input = env.initial_v, 0.0, 0.0, float('inf')
    while True:
        point=operating_point(voltage,env.load_w,env.efficiency,env.esr_ohm)
        if point is None:
            return Result(False,t,float('-inf'),voltage,max_current)
        current, vin=point
        min_input=min(min_input,vin)
        max_current=max(max_current,current)
        if vin < env.min_regulator_input_v-1e-12:
            return Result(False,t,min_input,voltage,max_current)
        if t >= env.outage_ms-1e-12:
            return Result(True,env.outage_ms,min_input,voltage,max_current)
        dt=min(env.step_ms,env.outage_ms-t)
        voltage -= current * dt/(1000*effective_cap)
        t += dt

def needed_nominal_f(env: Envelope, cap_ceiling_f: float = 10.0):
    """Minimum C under stated model or None if infeasible; bisection."""
    if env.load_w == 0 or env.outage_ms == 0:
        return 0.0
    initial=operating_point(env.initial_v,env.load_w,env.efficiency,env.esr_ohm)
    if initial is None or initial[1] < env.min_regulator_input_v:
        return None
    lo,hi=0.0,0.001
    while hi <= cap_ceiling_f and not simulate(hi,env).ok:
        hi *= 2
    if hi > cap_ceiling_f:
        return None
    for _ in range(34):
        mid=(hi+lo)/2
        if simulate(mid,env).ok:
            hi=mid
        else:
            lo=mid
    return hi

def ideal_f(power_w, duration_ms, v_high, v_low):
    return 2*power_w*(duration_ms/1000)/(v_high**2-v_low**2)

if __name__ == '__main__':
    import json
    from dataclasses import replace
    cases={
        'ideal':Envelope(efficiency=1,esr_ohm=0,retained_capacity_fraction=1),
        'hypothetical_typical':Envelope(),
        'conservative_scenario':Envelope(efficiency=.75,esr_ohm=.5,retained_capacity_fraction=.5),
        'infeasible_initial_esr':Envelope(efficiency=.75,esr_ohm=4,retained_capacity_fraction=.5),
    }
    print(json.dumps({k: {'required_nominal_F':needed_nominal_f(e),
                            'ride_through_at_0p1F':simulate(.1,e).__dict__}
                      for k,e in cases.items()},indent=2))
