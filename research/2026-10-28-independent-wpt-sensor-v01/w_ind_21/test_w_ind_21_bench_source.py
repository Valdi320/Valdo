"""W-IND-21 independent source-boundary regression, not electrical qualification."""
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from sch_graph_audit import parse, children, one, loc, prop

SCH = HERE / "W_IND_21_TX_BENCH_DECLARED.kicad_sch"
ORIGINAL = HERE.parent / "W_IND_15_TX_DUAL_CUT_UNQUALIFIED.kicad_sch"


def audit(text):
    errors = []
    try:
        tree = parse(text)
        lib = one(tree, "lib_symbols")
        defs = {x[1]: x for x in children(lib, "symbol")}
        refs = {prop(x, "Reference"): x for x in children(tree, "symbol")}
        if set(refs) != {"J1", "U1", "U2", "R1", "R2", "R3", "R4"}:
            errors.append("unexpected or missing components")
        if set(defs) != {"VALDO:TPS22918_DBV", "VALDO:R", "VALDO:BENCH_ISO_5V_SOURCE"}:
            errors.append("unknown symbols")
        j = refs["J1"]
        if one(j, "lib_id")[1] != "VALDO:BENCH_ISO_5V_SOURCE":
            errors.append("wrong source symbol")
        if "no" not in [x[1] for x in children(j, "in_bom")] or "no" not in [x[1] for x in children(j, "on_board")]:
            errors.append("virtual source must never enter the build BOM")
        jpins = {}
        for unit in children(defs["VALDO:BENCH_ISO_5V_SOURCE"], "symbol"):
            for pin in children(unit, "pin"):
                pn = one(pin, "number")[1]
                xp, yp, angle = loc(pin)
                jpins[pn] = (pin[1], one(pin,"name")[1], xp, yp, angle)
        if {(n, str(p[2]), str(p[3]), str(p[4])) for n,p in jpins.items()} != {
            ("1","10.16","2.54","180"),("2","10.16","-2.54","180")}:
            errors.append("source pins moved")
        if any(p[0] != "power_out" for p in jpins.values()):
            errors.append("source is not ERC-declared power output")
        if [jpins.get("1",[])[1], jpins.get("2",[])[1]] != ["+5V_EXTERNAL", "RETURN_EXTERNAL"]:
            errors.append("source rail identity wrong")
        labels = [(x[1], str(loc(x)[0]), str(loc(x)[1])) for x in children(tree, "label")]
        for net,x,y in [("VIN_5V","45.72","58.42"),("GND","45.72","63.5")]:
            if labels.count((net,x,y))!=1:
                errors.append("source pin not directly attached to reviewed rail: "+net)
        if labels.count(("VIN_5V","66.04","58.42")) != 1:
            errors.append("original VIN pin lost")
        if labels.count(("TX_5V_CUT","147.32","58.42")) != 1:
            errors.append("output changed")
        if "PWR_FLAG" in text or "battery" in text.lower().split("(lib_symbols")[0]:
            errors.append("inappropriate workaround or OEM domain")
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        errors.append("invalid or incomplete candidate: "+str(exc))
    return errors


class BenchSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SCH.read_text(encoding="utf-8")
        cls.legacy = ORIGINAL.read_text(encoding="utf-8")
        cls.library = (HERE/"VALDO.kicad_sym").read_text(encoding="utf-8")
        cls.table = (HERE/"sym-lib-table").read_text(encoding="utf-8")

    def test_bench_candidate_passes_static_contract(self):
        self.assertEqual(audit(self.source), [])
    def test_no_source_in_legacy_schematic(self):
        self.assertNotIn("BENCH_ISO_5V_SOURCE", self.legacy)
    def test_original_six_component_placements_preserved(self):
        old=parse(self.legacy); new=parse(self.source)
        def placements(root):
            return {prop(s,"Reference"): (one(s,"lib_id")[1],loc(s))
                    for s in children(root,"symbol") if prop(s,"Reference")!="J1"}
        self.assertEqual(placements(old), placements(new))
    def test_attached_power_pins_mutation(self):
        self.assertTrue(audit(self.source.replace('(label "VIN_5V" (at 45.72 58.42 0)', '(label "VIN_5V" (at 48.26 58.42 0)', 1)))
    def test_return_rail_mutation(self):
        self.assertTrue(audit(self.source.replace('(label "GND" (at 45.72 63.5 0)', '(label "EN_A" (at 45.72 63.5 0)', 1)))
    def test_virtual_source_not_buildable(self):
        self.assertTrue(audit(self.source.replace('(unit 1) (in_bom no) (on_board no)', '(unit 1) (in_bom yes) (on_board yes)', 1)))
    def test_power_type_tamper(self):
        self.assertTrue(audit(self.source.replace('(pin power_out line (at 10.16 2.54 180)', '(pin passive line (at 10.16 2.54 180)', 1)))
    def test_output_bypass_tamper(self):
        self.assertTrue(audit(self.source.replace('(label "TX_5V_CUT" (at 147.32 58.42 0)', '(label "VIN_5V" (at 147.32 58.42 0)', 1)))
    def test_source_pin_number_tamper(self):
        marker = '(symbol "BENCH_ISO_5V_SOURCE_1_1"'
        first, second = self.source.split(marker, 1)
        tampered = first + marker + second.replace('(number "2"', '(number "9"', 1)
        self.assertTrue(audit(tampered))
    def test_pin_names_and_symbol_registration(self):
        self.assertIn('(symbol "BENCH_ISO_5V_SOURCE"', self.library)
        self.assertIn("KIPRJMOD",self.table)
        self.assertIn("VALDO.kicad_sym",self.table)
    def test_legacy_pins_present_in_new_library(self):
        for key in ['(symbol "TPS22918_DBV"', '(symbol "R"', '(symbol "BENCH_ISO_5V_SOURCE"']:
            self.assertEqual(self.library.count(key),1)
    def test_no_pwr_flag_and_no_hardware_claim(self):
        self.assertNotIn("PWR_FLAG",self.source)
        self.assertIn("DO NOT BUILD/ENERGIZE",self.source)
        self.assertNotIn("(footprint ",self.source.lower())

if __name__ == "__main__":
    unittest.main()
