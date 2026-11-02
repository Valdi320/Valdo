"""W-IND-33 original digital-only regressions; never power-approval tests."""
import unittest
from w33_positive_permit import (DFF_DCU8,SUPERVISOR_DBZ3,INTERFACE,
                                  Signals,PositivePermits,nominal_budget,enumerate_faults)

class PinoutAndEnvelope(unittest.TestCase):
    def test_01_exact_dcu8(self):
        self.assertEqual(DFF_DCU8,{"CLK":1,"D":2,"Q_N":3,"GND":4,"Q":5,"CLR_N":6,"PRE_N":7,"VCC":8})
    def test_02_supervisor_dbz3(self):
        self.assertEqual(SUPERVISOR_DBZ3,{"GND":1,"RESET_N":2,"VDD":3})
    def test_03_two_distinct_supplies(self):
        self.assertNotEqual(INTERFACE["SUP_A_RESET_N"],INTERFACE["SUP_B_RESET_N"])
    def test_04_no_radio_clock(self):
        self.assertEqual(INTERFACE["LOCAL_BUTTON_ONLY"],("FF_A.CLK1","FF_B.CLK1","CLK_PULLDOWN_100K"))
    def test_05_two_correct_diode_anodes(self):
        self.assertIn("DIODE_A.ANODE",INTERFACE["CLEAR_A_N"])
        self.assertIn("DIODE_B.ANODE",INTERFACE["CLEAR_B_N"])
    def test_06_separate_q_en(self):
        self.assertIn("FF_A.Q5",INTERFACE["EN_A_PROPOSED"])
        self.assertIn("FF_B.Q5",INTERFACE["EN_B_PROPOSED"])
    def test_07_ideal_high_clear_not_analog_proof(self):
        x=nominal_budget()
        self.assertAlmostEqual(x["clear_high_v"],4.545455,places=5)
        self.assertFalse(x["analog_trip_levels_qualified"])
    def test_08_ina301_sink_envelope_only(self):
        x=nominal_budget()
        self.assertEqual(x["alert_sink_ideal_ma"],2.0)
        self.assertLess(x["alert_sink_ideal_ma"],x["ina301_datasheet_test_ma"])
    def test_09_no_authorization(self):
        self.assertFalse(nominal_budget()["physical_cut_qualified"])
class LatchBehavior(unittest.TestCase):
    def test_10_initial_off(self):
        self.assertFalse(PositivePermits().step(Signals())["both_en"])
    def test_11_new_local_press(self):
        self.assertTrue(PositivePermits().step(Signals(button=True))["both_en"])
    def test_12_radio_ignored(self):
        self.assertFalse(PositivePermits().step(Signals(),radio_rearm=True)["both_en"])
    def test_13_brownout_no_auto_rearm(self):
        x=PositivePermits()
        x.step(Signals(button=True))
        x.step(Signals(voltage_ok=False))
        self.assertFalse(x.step(Signals())["both_en"])
    def test_14_button_held_on_brownout(self):
        x=PositivePermits()
        x.step(Signals(button=True))
        x.step(Signals(voltage_ok=False,button=True))
        self.assertFalse(x.step(Signals(button=True))["both_en"])
    def test_15_overcurrent_latches_off(self):
        x=PositivePermits()
        x.step(Signals(button=True))
        x.step(Signals(button=False))
        x.step(Signals(alert_not_asserted=False))
        self.assertFalse(x.step(Signals())["both_en"])
    def test_16_single_bad_supervisor(self):
        for field in ("supervisor_a_ok","supervisor_b_ok"):
            x=PositivePermits();x.step(Signals(button=True))
            self.assertFalse(x.step(Signals(**{field:False}))["both_en"])
    def test_17_single_stuck_ff_with_alert_off(self):
        for field in ("ff_a_stuck_high","ff_b_stuck_high"):
            x=PositivePermits()
            self.assertFalse(x.step(Signals(alert_not_asserted=False,**{field:True}))["both_en"])
    def test_18_double_stuck_ff_still_unsafe(self):
        x=PositivePermits()
        self.assertTrue(x.step(Signals(alert_not_asserted=False,ff_a_stuck_high=True,ff_b_stuck_high=True))["both_en"])
    def test_19_exhaustive_64_and_9_known_hazards(self):
        x=enumerate_faults()
        self.assertEqual(x["cases"],64)
        self.assertEqual(x["unsafe_logic_counterexamples"],9)
        self.assertFalse(x["hardware_power_authorized"])
    def test_20_single_stuck_plus_matching_supervisor_failure_unsafe(self):
        x=enumerate_faults()["examples"]
        self.assertTrue(any(not t["supervisor_a_ok"] and t["supervisor_b_ok"] and
                            t["ff_a_stuck_high"] and not t["ff_b_stuck_high"]
                            and t["alert_not_asserted"] for t in x))
if __name__ == "__main__":unittest.main()
