"""W-IND-36 pure Python deterministic mutation and reset tests."""
import copy
import math
import unittest
import xml.etree.ElementTree as ET
import generate_w36 as d
import netlist_gate_w36 as gate
from digital_model_w36 import Rearm,threshold_window,low_rail_guard

class W36(unittest.TestCase):
    def test_parts(self):
        actual={ref:val for ref,_,_,_,val in d.INSTANCES}
        for ref, val in {"U4":"TPS3840PL28DBVR","U9":"TPS3840PL42DBVR",
                         "U7":"SN74LVC1G74DCUR","U8":"SN74LVC1G74DCUR",
                         "U2":"TPS259470LRPWR","U3":"TPS259470LRPWR"}.items():
            with self.subTest(ref=ref): self.assertEqual(actual[ref],val)
        self.assertNotIn("J3",actual)
        self.assertNotIn("J4",actual)

    def test_pinmaps_exact(self):
        self.assertEqual([(p[0],p[1]) for p in d.SPECS["SUP_MON"][2]],
                         [("1","RESET_N"),("2","VDD"),("3","GND"),("4","MR_N"),("5","CT")])
        self.assertEqual([(p[0],p[1]) for p in d.SPECS["AND"][2]],
                         [("1","A"),("2","B"),("3","GND"),("4","Y"),("5","VCC")])
        self.assertEqual([(p[0],p[1]) for p in d.SPECS["DFF"][2]],
                         [("1","CLK"),("2","D"),("3","Q_N"),("4","GND"),("5","Q"),
                          ("6","CLR_N"),("7","PRE_N"),("8","VCC")])

    def test_ground_return_is_not_second_power_source(self):
        self.assertEqual(d.SPECS["MON_SOURCE"][2][1][2], "passive")

    def test_dedicated_latches_and_supervisors(self):
        e=gate.EXPECTED
        for case,required in {
            "PG_MON_3V3":{"U4.1","U10.1","U11.1","U5.2"},
            "PG_RX5":{"U9.1","U10.2","U11.2","U6.2"},
            "CLR_A_POSITIVE":{"U10.4","U7.6"},
            "CLR_B_POSITIVE":{"U11.4","U8.6"},
            "PERMIT_A_LOCAL_PG":{"U5.4","U2.1","RPD1.1"},
            "PERMIT_B_LOCAL_PG":{"U6.4","U3.1","RPD2.1"},
            "CLOCK_A_LOCAL":{"SW1.2","U7.1"},
            "CLOCK_B_LOCAL":{"SW2.2","U8.1"}
        }.items():
            with self.subTest(case=case): self.assertTrue(required <= e[case])
        self.assertNotEqual(e["PERMIT_A_LOCAL_PG"],e["PERMIT_B_LOCAL_PG"])
        self.assertEqual(e["RX5_BETWEEN_CUTS"],{"U2.6","U3.5"})
        self.assertEqual(e["RX5_LOAD"],{"U3.6","J2.1"})
        self.assertNotIn("U1.6",e["PERMIT_A_LOCAL_PG"] | e["PERMIT_B_LOCAL_PG"])
        self.assertFalse(any("RF" in name or "ESP" in name for name in e))

    def test_no_duplicate_connected_pin(self):
        all_pins=[f"{ref}.{num}" for entries in d.NETS.values() for ref,num in entries]
        all_pins.extend(f"{ref}.{num}" for ref,num in d.NC)
        self.assertEqual(len(all_pins),len(set(all_pins)))

    def test_native_gate_synthetic_fixture(self):
        self.assertTrue(gate.evaluate(gate.fixture_xml())["passed"])
        self.assertFalse(gate.evaluate(b"garbage")["passed"])
        self.assertFalse(gate.evaluate(b"")["power_authorized"])

    def test_mutations_rejected(self):
        baseline=ET.fromstring(gate.fixture_xml())
        for index, kind in enumerate(("missing_component","swap_variant","cut_a_bypass",
                                      "tie_en","delete_pg","extra_source","duplicate_pin")):
            root=copy.deepcopy(baseline)
            components=root.find("components")
            nets=root.find("nets")
            named={node.get("name"):node for node in nets.findall("net")}
            if kind=="missing_component": components.remove(components[0])
            if kind=="swap_variant": components.findall("comp")[0].find("value").text="WRONG"
            if kind=="cut_a_bypass":
                net=named["/RX5_LOAD"]
                ET.SubElement(net,"node",ref="U2",pin="5")
            if kind=="tie_en":
                net=named["/PERMIT_B_LOCAL_PG"]
                ET.SubElement(net,"node",ref="U2",pin="1")
            if kind=="delete_pg": nets.remove(named["/PG_MON_3V3"])
            if kind=="extra_source":
                net=ET.SubElement(nets,"net",name="/UNAUTHORIZED_SOURCE")
                ET.SubElement(net,"node",ref="X1",pin="1")
            if kind=="duplicate_pin":
                net=named["/CLOCK_A_LOCAL"]
                ET.SubElement(net,"node",ref="SW1",pin="2")
            with self.subTest(mutation=kind):
                self.assertFalse(gate.evaluate(ET.tostring(root))["passed"])

    def test_rearm_requires_two_distinct_local_edges(self):
        m=Rearm()
        self.assertEqual(m.step(True,True),(False,False))
        self.assertEqual(m.step(True,True,True,False),(True,False))
        self.assertEqual(m.step(True,True,True,True),(True,True))
        self.assertEqual(m.step(True,True,False,False),(True,True))

    def test_brownout_disarms_both_on_either_rail(self):
        for lost_mon,lost_rx in ((True,False),(False,True),(True,True)):
            with self.subTest(mon=lost_mon,rx=lost_rx):
                m=Rearm()
                m.step(True,True,True,True)
                self.assertEqual(m.step(not lost_mon,not lost_rx),(False,False))
                self.assertEqual(m.step(True,True),(False,False))
                self.assertEqual(m.step(True,True,True,True),(True,True))

    def test_stuck_button_is_not_new_edge(self):
        m=Rearm()
        m.step(True,True,True,True)
        m.step(False,True,True,True)
        self.assertEqual(m.step(True,True,True,True),(False,False))
        m.step(True,True,False,False)
        self.assertEqual(m.step(True,True,True,True),(True,True))

    def test_threshold_guards(self):
        self.assertAlmostEqual(threshold_window(2.8)[0],2.758)
        self.assertAlmostEqual(threshold_window(2.8)[1],2.842)
        self.assertAlmostEqual(low_rail_guard(4.5,4.4),0.034)
        self.assertAlmostEqual(low_rail_guard(4.5,4.2),0.237)
        self.assertGreater(low_rail_guard(4.5,4.2),low_rail_guard(4.5,4.4))
        self.assertFalse(math.isnan(low_rail_guard(4.5,4.2)))

    def test_generation_is_reproducible(self):
        f=d.files()
        self.assertIn("W36_RX_DUAL_PG_LOCAL_REARM_INCOMPLETE.kicad_sch",f)
        self.assertIn("sym-lib-table",f)
        sch=f["W36_RX_DUAL_PG_LOCAL_REARM_INCOMPLETE.kicad_sch"]
        self.assertIn("U10",sch)
        self.assertIn("U11",sch)
        self.assertIn("NO RADIO REARM",sch)
        self.assertNotIn("EXTERNAL PERMITS NOT QUALIFIED",sch)
        self.assertEqual(d.files(),f)

if __name__=="__main__": unittest.main()
