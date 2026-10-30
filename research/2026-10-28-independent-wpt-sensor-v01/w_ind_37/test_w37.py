"""Deterministic original tests for W37; digital assumptions only."""
import importlib.util
from pathlib import Path
import unittest
from w37_rearm_guard import Frame, GuardedRearm, sample_trace, evaluate

PG = (True, True)
HOLD = Frame(*PG, True, True)
IDLE = Frame(*PG, False, False)

def ready(m):
    for _ in range(3): m.tick(IDLE)
    for _ in range(2): m.tick(IDLE)
    return m

class W37(unittest.TestCase):
    def test_reset_start_off(self):
        self.assertEqual(m:=GuardedRearm().stage, "WAIT_PG")
    def test_cold_boot_held_does_not_arm(self):
        m=GuardedRearm()
        for _ in range(50):
            o=m.tick(HOLD)
            self.assertFalse(o.en_a or o.en_b)
        self.assertEqual(o.stage, "WAIT_BOTH_RELEASED")
    def test_release_both_then_press(self):
        m=GuardedRearm()
        for _ in range(4):m.tick(HOLD)
        m.tick(IDLE)
        self.assertEqual(m.tick(IDLE).stage, "WAIT_FRESH_PRESSES")
        self.assertFalse(m.tick(HOLD).en_a)
        o=m.tick(HOLD)
        self.assertTrue(o.en_a and o.en_b)
    def test_initial_buttons_released_requires_two_press_ticks(self):
        m=ready(GuardedRearm())
        self.assertFalse(m.tick(HOLD).en_a)
        self.assertTrue(m.tick(HOLD).en_a)
    def test_no_one_sided_power_stage(self):
        m=ready(GuardedRearm())
        for _ in range(3):
            o=m.tick(Frame(*PG,True,False))
            self.assertFalse(o.en_a or o.en_b)
        self.assertFalse(m.tick(Frame(*PG,False,True)).en_a)
        self.assertTrue(m.tick(Frame(*PG,False,True)).en_a)
    def test_single_sample_button_noise_does_not_arm(self):
        m=ready(GuardedRearm())
        for _ in range(20):
            self.assertFalse(m.tick(HOLD).en_a)
            m.tick(IDLE)
    def test_split_rail_brownout_loses_all_state(self):
        for fault in [Frame(False,True,True,True),Frame(True,False,True,True),Frame(False,False,True,True)]:
            with self.subTest(fault=fault):
                m=ready(GuardedRearm());m.tick(HOLD);m.tick(HOLD)
                self.assertTrue(m.tick(IDLE).en_a)
                self.assertFalse(m.tick(fault).en_a)
                for _ in range(7):self.assertFalse(m.tick(HOLD).en_a)
                self.assertFalse(m.tick(IDLE).en_a)
                m.tick(IDLE); m.tick(HOLD)
                self.assertTrue(m.tick(HOLD).en_a)
    def test_short_power_glitch_clears_without_rearm(self):
        m=ready(GuardedRearm());m.tick(HOLD);m.tick(HOLD)
        self.assertFalse(m.tick(Frame(False,True,False,False)).en_a)
        for _ in range(3):self.assertFalse(m.tick(HOLD).en_a)
    def test_wait_release_restarts_on_mixed_buttons(self):
        m=GuardedRearm()
        for _ in range(3):m.tick(HOLD)
        m.tick(IDLE)
        m.tick(Frame(*PG,True,False))
        self.assertEqual(m.tick(IDLE).stage,"WAIT_BOTH_RELEASED")
        self.assertEqual(m.tick(IDLE).stage,"WAIT_FRESH_PRESSES")
    def test_pressed_never_disarmed_until_fault(self):
        m=ready(GuardedRearm());m.tick(HOLD);self.assertTrue(m.tick(HOLD).en_a)
        self.assertTrue(m.tick(IDLE).en_a)
        self.assertFalse(m.tick(Frame(False,True,False,False)).en_a)
    def test_no_radio_channel_input(self):
        self.assertEqual(set(Frame.__dataclass_fields__),{"pg_mon","pg_rx","btn_a","btn_b"})
    def test_threshold_validation(self):
        for name in ["good_samples","release_samples","press_samples"]:
            with self.subTest(name=name):
                with self.assertRaises(ValueError): GuardedRearm(**{name:1})
    def test_deterministic_trace(self):
        rows=[(True,True,False,False)]*5+[(True,True,True,True)]*2
        self.assertTrue(sample_trace(rows)[-1].en_b)
        self.assertEqual(sample_trace(rows),sample_trace(rows))
    def test_real_w36_model_regression_counterexample_if_available(self):
        path=Path(__file__).resolve().parents[1]/"w_ind_36"/"digital_model_w36.py"
        if not path.exists(): self.skipTest("W36 repo source unavailable in isolated scratch")
        spec=importlib.util.spec_from_file_location("existing_w36_reference",path)
        mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        self.assertEqual(mod.Rearm().step(True,True,True,True),(True,True),
                         "If W36 is repaired, update the W37 known-counterexample regression")
        self.assertFalse(GuardedRearm().tick(HOLD).en_a)
    def test_report_explicit_no_approval(self):
        r=evaluate()
        self.assertEqual(r["short_trace_exhaustive_checked"],65536)
        self.assertFalse(r["hardware_tested"])
        self.assertFalse(r["safe_to_energize"])
        self.assertTrue(r["w37_release_then_press"]["enabled_after_fresh_sequence"])

if __name__ == "__main__":unittest.main()
