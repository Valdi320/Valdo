"""W-IND-15 static connection audit; NOT KiCad ERC, SPICE or physical verification."""
from copy import deepcopy
from pathlib import Path
import json
import re
import unittest

HERE = Path(__file__).resolve().parent
SCHEMATIC = HERE / "W_IND_15_TX_DUAL_CUT_UNQUALIFIED.kicad_sch"
CONTRACT = HERE / "W_IND_15_PIN_CONTRACT.json"

def validate(c):
    errors=[]
    nets=c["expected_nets"]
    expected={
        "VIN_5V":{"U1.1"},
        "MID":{"U1.6","U2.1","R1.1"},
        "TX_5V_CUT":{"U2.6","R2.1"},
        "GND":{"U1.2","U2.2","R1.2","R2.2","R3.2","R4.2"},
        "EN_A":{"U1.3","R3.1"},
        "EN_B":{"U2.3","R4.1"}
    }
    if set(nets)!=set(expected): errors.append("unexpected net name/bypass")
    if any(set(nets.get(k,[]))!=v for k,v in expected.items()):
        errors.append("pin/net mismatch or shared control")
    seen=[p for pins in nets.values() for p in pins]
    nc=c["intentional_no_connect"]
    all_pins={f"U{i}.{j}" for i in (1,2) for j in range(1,7)}
    all_pins|={f"R{i}.{j}" for i in range(1,5) for j in (1,2)}
    if len(seen)!=len(set(seen)) or len(nc)!=len(set(nc)):
        errors.append("repeated pin")
    if set(seen)|set(nc)!=all_pins or set(seen)&set(nc):
        errors.append("uncovered or shorted pin")
    if set(nc)!={"U1.4","U1.5","U2.4","U2.5"}:
        errors.append("CT/QOD incorrectly connected")
    if c["pinmap"]!={"1":"VIN","2":"GND","3":"ON","4":"CT","5":"QOD","6":"VOUT"}:
        errors.append("TI DBV pin mapping modified")
    if {k:v["value"] for k,v in c["resistors"].items()}!={"R1":"22k","R2":"1k","R3":"100k","R4":"100k"}:
        errors.append("resistors altered without review")
    if c.get("hardware_approved") or c.get("KiCad_ERC_run") or c.get("SPICE_run"):
        errors.append("unperformed qualification claimed")
    return errors

def balanced(text):
    n=0; quote=False; esc=False
    for ch in text:
        if esc: esc=False; continue
        if ch=="\\" and quote: esc=True; continue
        if ch=='"': quote=not quote; continue
        if not quote:
            if ch=="(": n+=1
            elif ch==")": n-=1
            if n<0: return False
    return n==0 and not quote

class TestPinLevelReference(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=json.loads(CONTRACT.read_text(encoding="utf-8"))
        cls.sch=SCHEMATIC.read_text(encoding="utf-8")

    def test_contract_pin_map_and_coverage(self):
        self.assertEqual(validate(self.c),[])
    def test_schematic_sexpr_lexical_balance_only(self):
        self.assertTrue(balanced(self.sch))
        self.assertIn('(kicad_sch (version 20230121)',self.sch)
    def test_each_pin_label_matches_contract_coordinate(self):
        pairs={}
        for pins in self.c["switch_pin_endpoints_mm"].values():
            for net,x,y in pins.values():
                if net!="NC":
                    k=(net,str(x),str(y));pairs[k]=pairs.get(k,0)+1
        for r in self.c["resistors"].values():
            for net,x,y in r["pins"].values():
                k=(net,str(x),str(y));pairs[k]=pairs.get(k,0)+1
        for (net,x,y),quantity in pairs.items():
            self.assertEqual(self.sch.count(f'(label "{net}" (at {x} {y} 0)'),quantity)
    def test_no_connects_at_both_qod_ct_pins(self):
        nc=[]
        for pins in self.c["switch_pin_endpoints_mm"].values():
            for net,x,y in pins.values():
                if net=="NC": nc.append((x,y))
        self.assertEqual(len(nc),4)
        for x,y in nc:self.assertIn(f'(no_connect (at {x} {y})',self.sch)
        self.assertEqual(self.sch.count("(no_connect "),4)
    def test_six_placed_symbols_without_footprint_assumption(self):
        self.assertEqual(self.sch.count("(instances (project "),6)
        self.assertEqual(self.sch.count('(lib_id "VALDO:TPS22918_DBV")'),2)
        self.assertEqual(self.sch.count('(lib_id "VALDO:R")'),4)
    def test_no_hardware_ready_claim(self):
        self.assertFalse(self.c["hardware_approved"])
        self.assertIn("DO NOT BUILD/ENERGIZE",self.sch)
        self.assertEqual(self.c["real_metal_fod"],"MISSING")
    def test_shared_enable_fault_rejected(self):
        x=deepcopy(self.c);x["expected_nets"]["EN_A"].append("U2.3")
        self.assertTrue(validate(x))
    def test_power_bypass_fault_rejected(self):
        x=deepcopy(self.c);x["expected_nets"]["VIN_5V"].append("U2.6")
        self.assertTrue(validate(x))
    def test_qod_short_fault_rejected(self):
        x=deepcopy(self.c);x["intentional_no_connect"].remove("U1.5")
        x["expected_nets"]["MID"].append("U1.5")
        self.assertTrue(validate(x))
    def test_missing_essential_bleeder_rejected(self):
        x=deepcopy(self.c);x["expected_nets"]["GND"].remove("R2.2")
        self.assertTrue(validate(x))
    def test_miswired_sot_pin_rejected(self):
        x=deepcopy(self.c);x["pinmap"]["6"]="QOD"
        self.assertTrue(validate(x))
    def test_unqualified_erc_claim_rejected(self):
        x=deepcopy(self.c);x["KiCad_ERC_run"]=True
        self.assertTrue(validate(x))
    def test_missing_independent_on_pull_down_rejected(self):
        x=deepcopy(self.c);x["expected_nets"]["EN_B"].remove("R4.1")
        self.assertTrue(validate(x))

if __name__=="__main__":
    unittest.main()
