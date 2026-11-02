"""W46 focused regression. Synthetic only, no electrical safety validation."""
from __future__ import annotations
import unittest
from w46_diagnostic_model import (PARTS,NETS,NO_CONNECT,audit_contract,evidence,
    sink_current_ma,sink_resistor_mw,line_state)

class W46Tests(unittest.TestCase):
    def test_8_parts_and_5_nets(self):
        self.assertEqual((len(PARTS),len(NETS)),(8,5))
    def test_20_pins_unique(self):
        pins=[p for group in NETS.values() for p in group]+NO_CONNECT
        self.assertEqual(len(pins),len(set(pins)))
        self.assertEqual(len(pins),20)
    def test_no_5v_on_health(self):
        self.assertNotIn("J3.1",NETS["5V_SUPERVISOR_ONLY"])
        self.assertNotIn("R5.1",NETS["5V_SUPERVISOR_ONLY"])
        self.assertIn("R5.1",NETS["3V3_LOCAL"])
    def test_health_pin_exact(self):
        self.assertEqual(set(NETS["HEALTH_N_LOCAL_DIAGNOSTIC"]),
                         {"J3.1","R5.2","U1.6"})
    def test_no_mosfet_and_cut_en(self):
        self.assertNotIn("Q1",PARTS)
        self.assertFalse(any("EN" in n for n in NETS))
    def test_native_erc_not_claimed(self):
        x=audit_contract()
        self.assertTrue(x["structural_pass"])
        self.assertFalse(x["native_kicad_erc"])
        self.assertFalse(x["hardware_approved"])
    def test_healthy_ideal_low(self):
        self.assertEqual(line_state(vdd=5,pullup=3.3,threshold_good=True),
                         "LOW_SINK_IDEAL")
    def test_bad_supply_ideal_high(self):
        self.assertEqual(line_state(vdd=5,pullup=3.3,threshold_good=False),
                         "HIGH_IF_RECEIVER_VIH_SUPPORTS_IT")
    def test_open_signal_local_pullup_high(self):
        self.assertEqual(line_state(vdd=5,pullup=3.3,threshold_good=True,wire_open=True),
                         "HIGH_IF_RECEIVER_VIH_SUPPORTS_IT")
    def test_vdd_lost_unresolved(self):
        self.assertEqual(line_state(vdd=0,pullup=3.3,threshold_good=False),
                         "UNKNOWN_SUPERVISOR_POR")
    def test_local_3v3_lost_unresolved(self):
        self.assertEqual(line_state(vdd=5,pullup=0,threshold_good=False),
                         "UNKNOWN_RECEIVER_SUPPLY")
    def test_stuck_low_false_health(self):
        self.assertEqual(line_state(vdd=5,pullup=3.3,threshold_good=False,stuck_low=True),
                         "LOW_FALSE_HEALTH_POSSIBLE")
    def test_short_high(self):
        self.assertEqual(line_state(vdd=5,pullup=3.3,threshold_good=True,short_high=True),
                         "HIGH_IF_RECEIVER_VIH_SUPPORTS_IT")
    def test_ideal_load_values(self):
        self.assertAlmostEqual(sink_current_ma(3.3),0.33)
        self.assertAlmostEqual(sink_resistor_mw(3.3),1.089)
        self.assertGreater(sink_current_ma(3.3,0.01),0.33)
    def test_invalid_inputs_rejected(self):
        for call in (lambda:sink_current_ma(0),
                     lambda:line_state(vdd=-1,pullup=3.3,threshold_good=True),
                     lambda:line_state(vdd=5,pullup=3.3,threshold_good=1)):
            with self.assertRaises(ValueError):
                call()
    def test_evidence_not_hardware(self):
        x=evidence()
        self.assertEqual(len(x["cases"]),8)
        self.assertEqual(x["parts_saved_in_unbuilt_concept"],2)
        self.assertFalse(x["hardware_approved"])
        self.assertTrue(x["no_hardware_tests"])
        self.assertFalse(x["connected_to_safety_en"])

if __name__=="__main__":
    unittest.main()
