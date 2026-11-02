"""W38 digital/structural regression; never physical safety testing."""
import copy
import unittest
import xml.etree.ElementTree as ET
import generate_w38 as d
import netlist_gate_w38 as gate
from local_trip_model_w38 import Local

class W38(unittest.TestCase):
    def test_alert_route_pins(self):
        self.assertEqual(set(d.NETS["ALERT_N_FORCE_LOCAL_RESET"]),
                         {("U1","6"),("R2","2"),("U4","4")})
        self.assertNotIn(("U4","4"), d.NC)
        self.assertIn(("U9","4"), d.NC)
    def test_3v3_pullup_not_5v(self):
        self.assertIn(("R2","1"),d.NETS["MON_3V3_EXTERNAL"])
        self.assertNotIn(("R2","1"),d.NETS["RX5_SOURCE"])
    def test_hardwire_chain(self):
        self.assertIn(("U4","1"),d.NETS["PG_MON_3V3"])
        self.assertIn(("U7","6"),d.NETS["CLR_A_POSITIVE"])
        self.assertIn(("U8","6"),d.NETS["CLR_B_POSITIVE"])
        self.assertIn(("U2","1"),d.NETS["PERMIT_A_LOCAL_PG"])
        self.assertIn(("U3","1"),d.NETS["PERMIT_B_LOCAL_PG"])
        self.assertFalse(any("RADIO" in name or "WIFI" in name for name in d.NETS))
    def test_part_variant(self):
        by_ref={ref:val for ref,_,_,_,val in d.INSTANCES}
        self.assertEqual(by_ref["U1"],"INA301A1IDGKR")
        self.assertEqual(by_ref["U4"],"TPS3840PL28DBVR")
        self.assertEqual(by_ref["U2"],"TPS259470LRPWR")
    def test_no_duplicate_connected_pins(self):
        pins=[f"{r}.{n}" for v in d.NETS.values() for r,n in v]
        pins += [f"{r}.{n}" for r,n in d.NC]
        self.assertEqual(len(pins),len(set(pins)))
    def test_generated_files_same_on_repeat(self):
        a=d.files()
        self.assertEqual(a,d.files())
        self.assertIn("W38.kicad_sym",a)
        self.assertIn("W38",a["sym-lib-table"])
        self.assertIn("INA301 ALERT_N LOW -> U4 MR_N",a[d.PROJECT+".kicad_sch"])
    def test_fixture_and_not_power_authorized(self):
        out=gate.evaluate(gate.fixture())
        self.assertTrue(out["passed"],out["problems"])
        self.assertFalse(out["power_on_authorized"])
        self.assertFalse(out["ina301_internal_health_proven"])
    def test_mutated_netlist_fail_closed(self):
        for bad in ("no_mr","back_to_5v","cut_bypass","wrong_part","double_pin","radio"):
            xml=ET.fromstring(gate.fixture())
            nets={n.get("name"):n for n in xml.find("nets").findall("net")}
            if bad=="no_mr":
                n=nets["/ALERT_N_FORCE_LOCAL_RESET"]
                for p in n.findall("node"):
                    if p.get("ref")=="U4":n.remove(p)
            elif bad=="back_to_5v":
                n=nets["/MON_3V3_EXTERNAL"]
                for p in n.findall("node"):
                    if p.get("ref")=="R2":n.remove(p)
                ET.SubElement(nets["/RX5_SOURCE"],"node",ref="R2",pin="1")
            elif bad=="cut_bypass":
                ET.SubElement(nets["/RX5_LOAD"],"node",ref="U2",pin="5")
            elif bad=="wrong_part":
                xml.find("components").find("comp").find("value").text="WRONG"
            elif bad=="double_pin":
                ET.SubElement(nets["/ALERT_N_FORCE_LOCAL_RESET"],"node",ref="U4",pin="4")
            elif bad=="radio":
                n=ET.SubElement(xml.find("nets"),"net",name="/RADIO_REARM")
                ET.SubElement(n,"node",ref="WIFI",pin="1")
            with self.subTest(bad=bad):
                self.assertFalse(gate.evaluate(ET.tostring(xml))["passed"])
    def test_overcurrent_disarms_both(self):
        s=Local()
        self.assertEqual(s.tick(True,True,True,True,True),(True,True))
        self.assertEqual(s.tick(True,True,False,True,True),(False,False))
        self.assertEqual(s.tick(True,True,True,True,True),(False,False))
        s.tick(True,True,True,False,False)
        self.assertEqual(s.tick(True,True,True,True,True),(True,True))
    def test_either_rail_down_cuts(self):
        for a,b in ((False,True),(True,False),(False,False)):
            s=Local()
            s.tick(True,True,True,True,True)
            self.assertEqual(s.tick(a,b,True),(False,False))
    def test_32_boolean_fault_states(self):
        n=0
        for p33 in (False,True):
            for p5 in (False,True):
                for alarm in (False,True):
                    for prev_a in (False,True):
                        for prev_b in (False,True):
                            m=Local(a=prev_a,b=prev_b,prev_a=True,prev_b=True)
                            ea,eb=m.tick(p33,p5,alarm,True,True)
                            if not (p33 and p5 and alarm):
                                self.assertFalse(ea or eb)
                            n+=1
        self.assertEqual(n,32)
    def test_supply_loss_of_ina301_still_unprotected(self):
        m=Local()
        self.assertEqual(m.tick(True,True,True,True,True),(True,True))
        self.assertFalse(gate.evaluate(gate.fixture())["ina301_internal_health_proven"])
    def test_w37_rearm_not_implemented(self):
        self.assertFalse(gate.evaluate(gate.fixture())["W37_release_gate_hardware_built"])
    def test_safe_flags_remain_false(self):
        out=gate.evaluate(gate.fixture())
        for flag in ("physically_measured","power_on_authorized",
                     "fod_thermal_emi_qualified","battery_bms_dock_connected"):
            self.assertFalse(out[flag])
if __name__=="__main__": unittest.main()
