"""W39 self-tests: netlist fault mutations and idealised single-point failures."""
import unittest
import xml.etree.ElementTree as ET
from dataclasses import replace
import generate_w39 as d
import netlist_gate_w39 as gate
import fault_model_w39 as model

class W39(unittest.TestCase):
    def test_dual_drains_separate_reset_paths(self):
        self.assertEqual(set(d.NETS["ALERT_N_FORCE_LOCAL_RESET"]),
                         {("U1","6"),("R2","2"),("U4","4")})
        self.assertEqual(set(d.NETS["ALERT_B_FORCE_RX_RESET"]),
                         {("U12","6"),("R3","2"),("U9","4")})
        self.assertNotIn(("U9","4"), d.NC)
    def test_different_pullup_supply_domains(self):
        self.assertIn(("R2","1"),d.NETS["MON_3V3_EXTERNAL"])
        self.assertIn(("R3","1"),d.NETS["RX5_SOURCE"])
        self.assertNotIn(("R3","1"),d.NETS["MON_3V3_EXTERNAL"])
    def test_own_decoupling_and_limit(self):
        self.assertEqual(set(d.NETS["LIMIT_B"]),{("U12","3"),("R4","1")})
        self.assertIn(("C7","1"),d.NETS["MON_3V3_EXTERNAL"])
        self.assertIn(("C7","2"),d.NETS["GND"])
        self.assertIn(("U12","8"),d.NETS["KELVIN_PLUS"])
        self.assertIn(("U12","7"),d.NETS["KELVIN_MINUS"])
        self.assertIn(("U12","5"),d.NETS["MON_3V3_EXTERNAL"])
    def test_variants_and_no_radio(self):
        variants={ref:val for ref,_,_,_,val in d.INSTANCES}
        self.assertEqual(variants["U1"],variants["U12"])
        self.assertEqual(variants["U12"],"INA301A1IDGKR")
        self.assertEqual(variants["U9"],"TPS3840PL42DBVR")
        self.assertTrue(all("RADIO" not in n for n in d.NETS))
    def test_every_pin_once(self):
        pins=[(r,p) for v in d.NETS.values() for r,p in v] + d.NC
        self.assertEqual(len(pins),len(set(pins)))
    def test_deterministic_generator(self):
        a=d.files()
        self.assertEqual(a,d.files())
        self.assertIn(d.PROJECT+".kicad_sch",a)
        self.assertIn("W39.kicad_sym",a)
        self.assertIn("W39",a["sym-lib-table"])
    def test_ideal_gate_pass_no_safety_claim(self):
        report=gate.evaluate(gate.fixture())
        self.assertTrue(report["passed"],report["problems"])
        for flag in ("safe_to_energize","physical_current_trip_tested",
                     "fod_thermal_emi_qualified", "common_shunt_failure_covered"):
            self.assertFalse(report[flag])
    def test_native_net_mutants_rejected(self):
        edits=("remove_alert_b","move_mr_b_to_a","remove_u12_vs","remove_u12_kelvin",
               "remove_r3_source","short_domains","wrong_u12","duplicate_pin")
        for case in edits:
            root=ET.fromstring(gate.fixture())
            nets={x.get("name"):x for x in root.find("nets").findall("net")}
            def remove(name,ref,pin):
                net=nets["/"+name]
                for node in net.findall("node"):
                    if node.get("ref")==ref and node.get("pin")==pin:
                        net.remove(node)
                        return
                raise AssertionError("fixture missing")
            if case=="remove_alert_b":
                remove("ALERT_B_FORCE_RX_RESET","U12","6")
            elif case=="move_mr_b_to_a":
                remove("ALERT_B_FORCE_RX_RESET","U9","4")
                ET.SubElement(nets["/ALERT_N_FORCE_LOCAL_RESET"],"node",ref="U9",pin="4")
            elif case=="remove_u12_vs":
                remove("MON_3V3_EXTERNAL","U12","1")
            elif case=="remove_u12_kelvin":
                remove("KELVIN_PLUS","U12","8")
            elif case=="remove_r3_source":
                remove("RX5_SOURCE","R3","1")
            elif case=="short_domains":
                ET.SubElement(nets["/MON_3V3_EXTERNAL"],"node",ref="R3",pin="1")
            elif case=="wrong_u12":
                for comp in root.find("components").findall("comp"):
                    if comp.get("ref")=="U12":
                        comp.find("value").text="INA301A2IDGKR"
            elif case=="duplicate_pin":
                ET.SubElement(nets["/ALERT_B_FORCE_RX_RESET"],"node",ref="U12",pin="6")
            with self.subTest(case=case):
                self.assertFalse(gate.evaluate(ET.tostring(root))["passed"])
    def test_one_silent_ina_still_cuts(self):
        self.assertFalse(model.observe(replace(model.Case(),mon_a_alive=False))["requested_en_a"])
        self.assertFalse(model.observe(replace(model.Case(),mon_b_alive=False))["requested_en_b"])
    def test_one_broken_alert_still_cuts(self):
        self.assertFalse(model.observe(replace(model.Case(),alert_a_connected=False))["unsafe_overcurrent_permission"])
        self.assertFalse(model.observe(replace(model.Case(),alert_b_connected=False))["unsafe_overcurrent_permission"])
    def test_one_reset_chain_stuck_high_still_cuts(self):
        self.assertFalse(model.observe(replace(model.Case(),reset_a_path=False))["unsafe_overcurrent_permission"])
        self.assertFalse(model.observe(replace(model.Case(),reset_b_path=False))["unsafe_overcurrent_permission"])
    def test_common_shunt_and_dual_faults_remain_unsafe(self):
        for c in (replace(model.Case(),shunt_valid=False),
                  replace(model.Case(),mon_a_alive=False,mon_b_alive=False),
                  replace(model.Case(),alert_a_connected=False,alert_b_connected=False)):
            self.assertTrue(model.observe(c)["unsafe_overcurrent_permission"])
    def test_rail_loss_boolean_only(self):
        for k in ("pg_3v3","pg_5v"):
            self.assertFalse(model.observe(replace(model.Case(),**{k:False}))["requested_en_a"])
    def test_study_all_64_combinations(self):
        report=model.study()
        self.assertEqual(report["six_input_fault_combinations"],64)
        self.assertTrue(all(report["shared_failure_counterexamples"].values()))
        self.assertFalse(report["safe_to_energize"])

if __name__=="__main__":
    unittest.main()
