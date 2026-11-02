"""W66 synthetic-only W07 cross-trip adversarial regression.
Diagnosis credit: Codex A01 handoff 2026-10-28. No physical evidence.
"""
from dataclasses import replace
from itertools import product
import unittest
from tx_thermal_window import TxInterlock, assumed_channel

GOOD = assumed_channel()
HOT = assumed_channel(60)
FAULTS = {
    "hot": HOT,
    "ntc_open": replace(GOOD, ntc_ratio_read=1.0),
    "ntc_short": replace(GOOD, ntc_ratio_read=0.0),
    "ntc_absent": replace(GOOD, ntc_ratio_read=None),
    "fod": replace(GOOD, fod_clear=False),
    "fod_unknown": replace(GOOD, fod_clear=None),
    "overcurrent": replace(GOOD, current_ok=False),
    "supervisor": replace(GOOD, supervisor_ok=False),
    "wet": replace(GOOD, dry_ok=False),
    "offset": replace(GOOD, alignment_ok=False),
}
def armed():
    gate=TxInterlock()
    assert gate.step(GOOD, GOOD, local_request=True, local_reset=True)["energized"]
    gate.step(GOOD, GOOD, local_request=True, local_reset=False)
    return gate

class CrossTrip(unittest.TestCase):
    def test_hot_a_welded_a_other_cut_opens(self):
        out=armed().step(HOT,GOOD,local_request=True,cut_a_fault="welded_closed")
        self.assertFalse(out["energized"])
        self.assertFalse(out["latched_a"] or out["latched_b"])
        self.assertFalse(out["command_b"])
    def test_hot_b_welded_b_other_cut_opens(self):
        out=armed().step(GOOD,HOT,local_request=True,cut_b_fault="welded_closed")
        self.assertFalse(out["energized"])
        self.assertFalse(out["latched_a"] or out["latched_b"])
        self.assertFalse(out["command_a"])
    def test_ten_faults_either_side_matching_welded_cut(self):
        for name,bad in FAULTS.items():
            for side in ("a","b"):
                with self.subTest(name=name,side=side):
                    a,b=(bad,GOOD) if side=="a" else (GOOD,bad)
                    out=armed().step(a,b,local_request=True,
                        **{f"cut_{side}_fault":"welded_closed"})
                    self.assertFalse(out["energized"])
                    self.assertFalse(out["latched_a"] or out["latched_b"])
                    self.assertFalse(out["command_a"] or out["command_b"])
    def test_single_fault_over_all_two_cut_states(self):
        for side,fa,fb in product(("a","b"),("normal","welded_closed","stuck_open"),
                                  ("normal","welded_closed","stuck_open")):
            with self.subTest(side=side,fa=fa,fb=fb):
                a,b=(HOT,GOOD) if side=="a" else (GOOD,HOT)
                out=armed().step(a,b,local_request=True,cut_a_fault=fa,cut_b_fault=fb)
                self.assertFalse(out["command_a"] or out["command_b"])
                self.assertFalse(out["latched_a"] or out["latched_b"])
                self.assertEqual(out["energized"],fa==fb=="welded_closed")
    def test_recovery_without_new_local_reset_stays_off(self):
        gate=armed()
        gate.step(HOT,GOOD,local_request=True,cut_a_fault="welded_closed")
        for _ in range(20):
            self.assertFalse(gate.step(GOOD,GOOD,local_request=True)["energized"])
        self.assertTrue(gate.step(GOOD,GOOD,local_request=True,
                                  local_reset=True)["energized"])
    def test_reset_pressed_during_fault_not_partial_arm(self):
        gate=TxInterlock()
        out=gate.step(HOT,GOOD,local_request=True,local_reset=True,
                      cut_a_fault="welded_closed")
        self.assertFalse(out["energized"])
        self.assertFalse(out["latched_a"] or out["latched_b"])
        self.assertFalse(gate.step(GOOD,GOOD,local_request=True,
                                   local_reset=True)["energized"])
    def test_held_reset_does_not_rearm(self):
        gate=TxInterlock()
        self.assertTrue(gate.step(GOOD,GOOD,local_request=True,
                                  local_reset=True)["energized"])
        self.assertFalse(gate.step(HOT,GOOD,local_request=True,
                                   local_reset=True,cut_a_fault="welded_closed")["energized"])
        self.assertFalse(gate.step(GOOD,GOOD,local_request=True,
                                   local_reset=True)["energized"])
        gate.step(GOOD,GOOD,local_request=True,local_reset=False)
        self.assertTrue(gate.step(GOOD,GOOD,local_request=True,
                                  local_reset=True)["energized"])
    def test_loss_of_power_latches_both_off(self):
        gate=armed()
        out=gate.step(GOOD,GOOD,local_request=True,supply_present=False)
        self.assertFalse(out["latched_a"] or out["latched_b"])
        self.assertFalse(gate.step(GOOD,GOOD,local_request=True)["energized"])
    def test_loss_of_request_latches_both_off(self):
        gate=armed()
        out=gate.step(GOOD,GOOD,local_request=False)
        self.assertFalse(out["latched_a"] or out["latched_b"])
        self.assertFalse(gate.step(GOOD,GOOD,local_request=True)["energized"])
    def test_double_weld_remains_dangerous(self):
        out=armed().step(HOT,GOOD,local_request=True,
                         cut_a_fault="welded_closed",cut_b_fault="welded_closed")
        self.assertTrue(out["energized"])
        self.assertFalse(out["installation_approved"])
    def test_both_sensors_falsely_good_unseen(self):
        self.assertTrue(armed().step(GOOD,GOOD,local_request=True)["energized"])
    def test_no_physical_approval_from_model(self):
        out=armed().step(HOT,GOOD,local_request=True,cut_a_fault="welded_closed")
        self.assertTrue(out["theoretical_only"])
        self.assertFalse(out["installation_approved"])

if __name__=="__main__": unittest.main()
