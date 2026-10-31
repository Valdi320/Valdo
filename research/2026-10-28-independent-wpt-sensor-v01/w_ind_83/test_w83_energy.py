"""Only synthetic model assertions: never energizes hardware."""
from dataclasses import replace
import unittest
from w83_energy import D,Envelope,event_energy_j,simulate,demo

class EnergyTests(unittest.TestCase):
    def setUp(self):
        self.e=Envelope(D("3.3"),D("3.0"),D("0.015"),D("20"),D("2.9"),
                        D("1105.5"),D("10"),D("250"),6)
    def test_mode_math(self): self.assertEqual(D("335")*D("3.3"),D("1105.5"))
    def test_mw_ms_j(self): self.assertEqual(event_energy_j(D("1000"),D("10")),D("0.01"))
    def test_stored_j(self): self.assertEqual(simulate(self.e)["max_capacitor_energy_j"],"0.014175")
    def test_average(self): self.assertEqual(simulate(self.e)["average_required_mw"],"47.004000")
    def test_net_deficit(self): self.assertEqual(simulate(self.e)["cycle_net_energy_j"],"-0.006751")
    def test_first_burst_pass(self): self.assertIsNone(simulate(replace(self.e,pulses=1))["first_brownout_pulse"])
    def test_second_burst_fails(self): self.assertEqual(simulate(self.e)["first_brownout_pulse"],2)
    def test_10mf_fails(self): self.assertEqual(simulate(replace(self.e,c_effective_f=D("0.01")))["first_brownout_pulse"],1)
    def test_zero_cap_fails(self): self.assertEqual(simulate(replace(self.e,c_effective_f=D(0)))["first_brownout_pulse"],1)
    def test_min_cap_over_11mf(self): self.assertGreater(D(simulate(self.e)["min_effective_cap_for_one_pulse_f"]),D("0.011"))
    def test_min_cap_under_12mf(self): self.assertLess(D(simulate(self.e)["min_effective_cap_for_one_pulse_f"]),D("0.012"))
    def test_infinite_cap_does_not_fix_average(self): self.assertTrue(simulate(replace(self.e,c_effective_f=D(100000)))["cycle_unsustainable_indefinitely"])
    def test_large_cap_delays_brownout(self): self.assertIsNone(simulate(replace(self.e,c_effective_f=D(100000)))["first_brownout_pulse"])
    def test_1ms_counterexample(self):
        r=simulate(replace(self.e,pulse_ms=D("1"),c_effective_f=D("0.002")))
        self.assertFalse(r["cycle_unsustainable_indefinitely"])
        self.assertIsNone(r["first_brownout_pulse"])
    def test_no_rx(self): self.assertTrue(simulate(replace(self.e,rx_mw=D(0)))["cycle_unsustainable_indefinitely"])
    def test_more_power(self): self.assertIsNone(simulate(replace(self.e,rx_mw=D(2000)))["first_brownout_pulse"])
    def test_zero_pulse(self):
        with self.assertRaises(ValueError):simulate(replace(self.e,pulse_ms=D(0)))
    def test_overlap(self):
        with self.assertRaises(ValueError):simulate(replace(self.e,pulse_ms=D(251)))
    def test_negative_period(self):
        with self.assertRaises(ValueError):simulate(replace(self.e,period_ms=D(-1)))
    def test_inverted_voltage(self):
        with self.assertRaises(ValueError):simulate(replace(self.e,v_hi=D("2.5")))
    def test_nan(self):
        with self.assertRaises(ValueError):simulate(replace(self.e,c_effective_f=D("NaN")))
    def test_infinity(self):
        with self.assertRaises(ValueError):simulate(replace(self.e,rx_mw=D("Infinity")))
    def test_negative_supply(self):
        with self.assertRaises(ValueError):simulate(replace(self.e,rx_mw=D("-1")))
    def test_bool_pulses(self):
        with self.assertRaises(ValueError):simulate(replace(self.e,pulses=True))
    def test_zero_pulses(self):
        with self.assertRaises(ValueError):simulate(replace(self.e,pulses=0))
    def test_all_not_approved(self):
        for p in (D(1),D(10),D(1000)):
            self.assertFalse(simulate(replace(self.e,rx_mw=p))["approved_for_hardware"])
    def test_provenance(self):
        d=demo()
        self.assertIn("espressif.com",d["source"])
        self.assertEqual(d["model"],"W-IND-83")

if __name__=="__main__":
    unittest.main()
