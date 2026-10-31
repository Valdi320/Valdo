"""W-IND-16: deterministic original-schematic mutation regression."""
import unittest
import json
from copy import deepcopy
from pathlib import Path
from sch_graph_audit import audit,parse
HERE=Path(__file__).resolve().parent
class GeometryRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sch=(HERE/"W_IND_15_TX_DUAL_CUT_UNQUALIFIED.kicad_sch").read_text()
        cls.c=json.loads((HERE/"W_IND_15_PIN_CONTRACT.json").read_text())
    def changed(self,old,new):
        self.assertIn(old,self.sch)
        self.assertTrue(audit(self.sch.replace(old,new,1),self.c))
    def test_pass_real_schematic(self):
        self.assertEqual(audit(self.sch,self.c),[])
    def test_valid_parse(self):
        self.assertEqual(parse(self.sch)[0],"kicad_sch")
    def test_unbalanced(self):
        self.assertTrue(audit(self.sch[:-2],self.c))
    def test_duplicate_ref(self):
        self.changed('(property "Reference" "U2"','(property "Reference" "U1"')
    def test_move_u2(self):
        self.changed('(at 137.16 63.5 0)','(at 139.7 63.5 0)')
    def test_move_u1(self):
        self.changed('(at 76.2 63.5 0)','(at 76.2 66.04 0)')
    def test_rotate_u2(self):
        self.changed('(at 137.16 63.5 0)','(at 137.16 63.5 90)')
    def test_move_r1(self):
        self.changed('(at 104.14 86.36 0)','(at 106.68 86.36 0)')
    def test_change_library_pin_number(self):
        self.changed('(number "6" (effects','(number "5" (effects')
    def test_change_library_pin_name(self):
        self.changed('(name "VOUT"','(name "QOD"')
    def test_change_pin_type(self):
        self.changed('(pin power_out line','(pin passive line')
    def test_unknown_label(self):
        self.changed('(label "MID" (at 127 58.42 0)','(label "WRONG" (at 127 58.42 0)')
    def test_floating_label(self):
        self.changed('(label "MID" (at 127 58.42 0)','(label "MID" (at 129.54 58.42 0)')
    def test_shared_enable_label(self):
        self.changed('(label "EN_B" (at 127 68.58 0)','(label "EN_A" (at 127 68.58 0)')
    def test_missing_nc(self):
        self.changed('(no_connect (at 142.24 73.66)','(no_connect (at 145 73.66)')
    def test_new_power_bypass_wire(self):
        self.changed('(sheet_instances ','(wire (pts (xy 66.04 58.42) (xy 147.32 58.42)))\n (sheet_instances ')
    def test_new_global_label(self):
        self.changed('(sheet_instances ','(global_label "VIN_5V" (at 10 10 0))\n (sheet_instances ')
    def test_changed_resistor(self):
        self.changed('(property "Value" "22k"','(property "Value" "47k"')
    def test_changed_mpn(self):
        self.changed('(property "Value" "TPS22918DBVR" (at 86.36','(property "Value" "TPS22950" (at 86.36')
    def test_repeated_uuid(self):
        self.changed('00000000-0000-4000-8000-000000000048','00000000-0000-4000-8000-000000000001')
    def test_false_erc_claim(self):
        c=deepcopy(self.c);c["KiCad_ERC_run"]=True
        self.assertTrue(audit(self.sch,c))
    def test_false_hardware_claim(self):
        c=deepcopy(self.c);c["hardware_approved"]=True
        self.assertTrue(audit(self.sch,c))
    def test_modified_contract_pin_position(self):
        c=deepcopy(self.c);c["switch_pin_endpoints_mm"]["U2"]["6"][1]=150
        self.assertTrue(audit(self.sch,c))
    def test_modified_contract_net_membership(self):
        c=deepcopy(self.c);c["expected_nets"]["EN_B"].append("U1.1")
        self.assertTrue(audit(self.sch,c))
if __name__=="__main__":
    unittest.main()
