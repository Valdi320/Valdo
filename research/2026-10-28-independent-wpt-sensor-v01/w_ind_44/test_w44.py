"""W-IND-44 original Python checks. Synthetic/static only; no simulator/hardware."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"w_ind_43"))
from w43_por_gate import Inputs, evaluate as eval_w43
import generate_w44 as draft
from netlist_gate_w44 import EXPECTED,NC,PARTS,fixture,evaluate as verify_xml

class TopologyTests(unittest.TestCase):
    def test_parts(self):
        self.assertEqual(set(PARTS),{"J1","J2","J3","U1","Q1","R1","R2","R3","R4","C1"})
    def test_six_separate_nets(self):
        self.assertEqual(len(EXPECTED),6)
    def test_all_25_pins_accounted(self):
        all_pins=set().union(*EXPECTED.values(),NC)
        self.assertEqual(len(all_pins),25)
        self.assertEqual(len(NC),2)
    def test_no_duplicate_net_membership(self):
        pins=[v for group in EXPECTED.values() for v in group]
        self.assertEqual(len(pins),len(set(pins)))
    def test_ti_tps3700_ddc_pin_map(self):
        actual={n:name for n,name,*_ in draft.SPECS["TPS3700_DDC6"][2]}
        self.assertEqual(actual,{"1":"OUTA","2":"GND","3":"INA+","4":"INB-","5":"VDD","6":"OUTB"})
    def test_onsemi_pmos_gate_source_drain(self):
        actual={n:name for n,name,*_ in draft.SPECS["PMOS_BSS84"][2]}
        self.assertEqual(actual,{"1":"GATE","2":"SOURCE","3":"DRAIN"})
    def test_pmos_diode_orientation_not_reversed(self):
        self.assertIn("Q1.2",EXPECTED["VIN_5V_PRE_CUT"])
        self.assertIn("Q1.3",EXPECTED["HEALTH_DIAGNOSTIC"])
    def test_gate_pullup_and_outb_connection(self):
        self.assertEqual(EXPECTED["OUTB_GATE"],{"U1.6","Q1.1","R3.2"})
        self.assertEqual({"R3.1","Q1.2","U1.5"},EXPECTED["VIN_5V_PRE_CUT"] & {"R3.1","Q1.2","U1.5"})
    def test_divider_independent_of_health(self):
        self.assertEqual(EXPECTED["INB_DIVIDED"],{"R1.2","R2.1","U1.4"})
        self.assertNotIn("U1.4",EXPECTED["HEALTH_DIAGNOSTIC"])
    def test_health_has_local_pulldown(self):
        self.assertEqual(EXPECTED["HEALTH_DIAGNOSTIC"],{"Q1.3","J3.1","R4.1"})
        self.assertIn("R4.2",EXPECTED["GND"])
    def test_no_hardwired_efuse_en_or_rf(self):
        self.assertNotIn("U2",PARTS)
        self.assertNotIn("U3",PARTS)
        self.assertFalse(any("EN" in n or "MOTOR" in n or "BAT" in n for n in EXPECTED))
    def test_nc_explicit(self):
        self.assertEqual(NC,{"U1.1","U1.3"})
    def test_repeatable_generator(self):
        self.assertEqual(draft.files(),draft.files())
    def test_symbols_and_warning_present(self):
        files=draft.files()
        schematic=files[draft.PROJECT+".kicad_sch"]
        self.assertIn("OUTB-PMOS PIN-MAPPED DIAGNOSTIC ONLY",schematic)
        self.assertIn("NO EFUSE CONNECTION",schematic)
        self.assertIn('lib_id "W44:TPS3700_DDC6"',schematic)
        self.assertIn('lib_id "W44:PMOS_BSS84"',schematic)
    def test_base_W32_provenance_not_modified(self):
        self.assertEqual(draft.base.PREFIX,"W44")
        self.assertIn("W44",draft.files()["sym-lib-table"])
    def test_fixture_passes(self):
        self.assertTrue(verify_xml(fixture())["passed"])
    def test_bad_xml_fails(self):
        self.assertFalse(verify_xml(b"<oops>")["passed"])
    def test_pin_swap_detected(self):
        mutant=fixture().replace(b'pin="2"',b'pin="999"',1)
        self.assertFalse(verify_xml(mutant)["passed"])
    def test_missing_component_detected(self):
        mutant=fixture().replace(b'ref="Q1"',b'ref="Q2"',1)
        self.assertFalse(verify_xml(mutant)["passed"])

class FaultLimitTests(unittest.TestCase):
    def test_broken_health_wire_fails_ideal_off(self):
        self.assertTrue(eval_w43(Inputs(True,5,3.3,health_wire_open=True))["guaranteed_off"])
    def test_low_3v3_normal_vdd_off(self):
        self.assertTrue(eval_w43(Inputs(True,5,2.7))["guaranteed_off"])
    def test_unknown_outb_below_por_may_enable(self):
        self.assertTrue(eval_w43(Inputs(True,0.4,0))["unsafe_possible"])
    def test_stuck_gate_may_enable(self):
        self.assertTrue(eval_w43(Inputs(True,5,0,gate_stuck_ground=True))["unsafe_possible"])
    def test_health_short_high_may_enable(self):
        self.assertTrue(eval_w43(Inputs(True,5,0,health_short_to_5v=True))["unsafe_possible"])
    def test_electrically_unqualified_even_if_xml_passes(self):
        self.assertFalse(verify_xml(fixture())["hardware_allowed"])

if __name__=="__main__":
    unittest.main()
