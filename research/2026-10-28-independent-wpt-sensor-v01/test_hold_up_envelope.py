"""Deterministic software-only regression of a synthetic WPT-receiver supply outage."""
import unittest
from dataclasses import replace
from hold_up_envelope import Envelope, ideal_f, needed_nominal_f, operating_point, simulate

class HoldUpTests(unittest.TestCase):
    def setUp(self):
        self.env=Envelope()

    def test_ideal_analytic_limit(self):
        e=Envelope(efficiency=1,esr_ohm=0,retained_capacity_fraction=1,step_ms=.025)
        expected=ideal_f(e.load_w,e.outage_ms,e.initial_v,e.min_regulator_input_v)
        self.assertAlmostEqual(expected,.03529411764705882,places=10)
        self.assertLess(abs(needed_nominal_f(e)/expected-1),.001)

    def test_realistic_assumptions_increase_capacitance(self):
        ideal=needed_nominal_f(Envelope(efficiency=1,esr_ohm=0,retained_capacity_fraction=1))
        self.assertGreater(needed_nominal_f(self.env),ideal*1.5)

    def test_threshold_bracket(self):
        threshold=needed_nominal_f(self.env)
        self.assertTrue(simulate(1.01*threshold,self.env).ok)
        self.assertFalse(simulate(.99*threshold,self.env).ok)

    def test_high_esr_cannot_be_fixed_with_capacitance(self):
        e=replace(self.env,esr_ohm=4)
        self.assertIsNone(needed_nominal_f(e))
        self.assertFalse(simulate(100,e).ok)

    def test_more_capacitance_never_shortens_ride_through(self):
        grid=[.005,.01,.02,.05,.1,.2]
        durations=[simulate(c,self.env).delivered_ms for c in grid]
        self.assertEqual(durations,sorted(durations))
        self.assertTrue(simulate(.2,self.env).ok)

    def test_esr_cost(self):
        a=needed_nominal_f(replace(self.env,esr_ohm=0))
        b=needed_nominal_f(replace(self.env,esr_ohm=.5))
        self.assertGreater(b,a)

    def test_conversion_efficiency_cost(self):
        low=needed_nominal_f(replace(self.env,efficiency=.75))
        high=needed_nominal_f(replace(self.env,efficiency=.95))
        self.assertGreater(low,high)

    def test_idle(self):
        e=replace(self.env,load_w=0)
        r=simulate(.001,e)
        self.assertTrue(r.ok)
        self.assertEqual(r.final_cap_v,e.initial_v)
        self.assertEqual(needed_nominal_f(e),0)

    def test_zero_outage(self):
        e=replace(self.env,outage_ms=0)
        self.assertTrue(simulate(.001,e).ok)
        self.assertEqual(needed_nominal_f(e),0)

    def test_eaton_kw_0p22f_50ohm_candidate_is_electrically_infeasible(self):
        # Farnell ES official listing for Eaton KW-5R5C224-R: 0.22F, 5.5V, ESR=50 ohms.
        # Manufacturer-related product data, not measured by us; not WPT hardware proof.
        for load in (.4, 1.5):
            e=replace(self.env,esr_ohm=50,load_w=load,
                      retained_capacity_fraction=.8)
            self.assertIsNone(needed_nominal_f(e))
            self.assertEqual(simulate(.22,e).delivered_ms,0)

    def test_step_convergence_nominal(self):
        slow=needed_nominal_f(replace(self.env,step_ms=1))
        fine=needed_nominal_f(replace(self.env,step_ms=.05))
        self.assertLess(abs(slow/fine-1),.002)

    def test_bad_parameters(self):
        for params in (dict(initial_v=3),dict(min_regulator_input_v=5),
                       dict(efficiency=0),dict(esr_ohm=-1),dict(step_ms=0),
                       dict(load_w=float('nan')),dict(retained_capacity_fraction=1.1)):
            with self.assertRaises(ValueError):
                replace(self.env,**params)
        for cap in (0,-1,float('nan'),float('inf')):
            with self.assertRaises(ValueError):
                simulate(cap,self.env)

    def test_operating_point_power_conservation(self):
        for esr in (0,.02,.2,.5):
            i,v=operating_point(5,1.5,.85,esr)
            self.assertAlmostEqual(.85*i*v,1.5,places=9)

    def test_radio_cannot_authorize_supply(self):
        self.assertNotIn('radio',Envelope.__dataclass_fields__)
        self.assertNotIn('ack',Envelope.__dataclass_fields__)

if __name__ == '__main__':
    unittest.main()
