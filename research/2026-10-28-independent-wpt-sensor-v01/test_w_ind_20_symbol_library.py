"""W-IND-20: regression of project-local original KiCad symbol library."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parent


def sexp(source, key):
    pos = source.index(key)
    depth = 0
    quote = False
    escaped = False
    for i in range(pos, len(source)):
        c = source[i]
        if quote:
            if escaped:
                escaped = False
            elif c == "\\":
                escaped = True
            elif c == '"':
                quote = False
        elif c == '"':
            quote = True
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return source[pos:i + 1]
    raise ValueError("truncated KiCad sexp")


def reconstruct(sch):
    return (sexp(sch, "(lib_symbols")
            .replace("(lib_symbols", '(kicad_symbol_lib (version 20231120) (generator "kicad_symbol_editor")', 1)
            .replace('(symbol "VALDO:TPS22918_DBV"', '(symbol "TPS22918_DBV"', 1)
            .replace('(symbol "VALDO:R"', '(symbol "R"', 1) + "\n")


class SymbolLibrary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sch = (ROOT / "W_IND_15_TX_DUAL_CUT_UNQUALIFIED.kicad_sch").read_text()
        cls.lib = (ROOT / "VALDO.kicad_sym").read_text()
        cls.tbl = (ROOT / "sym-lib-table").read_text()
        cls.contract = json.loads((ROOT / "W_IND_15_PIN_CONTRACT.json").read_text())

    def test_exact_match_to_original_cached_symbols(self):
        self.assertEqual(reconstruct(self.sch), self.lib)

    def test_two_original_symbols_only(self):
        self.assertEqual(self.lib.count('(symbol "TPS22918_DBV"'), 1)
        self.assertEqual(self.lib.count('(symbol "R"'), 1)

    def test_library_alias_is_project_local(self):
        self.assertIn('(lib (name "VALDO")', self.tbl)
        self.assertIn('KIPRJMOD', self.tbl)
        self.assertIn('/VALDO.kicad_sym', self.tbl)
        self.assertEqual(self.tbl.count('(lib (name "VALDO")'), 1)

    def test_ti_pin_contract_is_present(self):
        for pin, name in self.contract["pinmap"].items():
            self.assertIn('(name "' + name + '"', self.lib)
            self.assertIn('(number "' + pin + '"', self.lib)

    def test_six_original_instances(self):
        self.assertEqual(self.sch.count('(lib_id "VALDO:TPS22918_DBV")'), 2)
        self.assertEqual(self.sch.count('(lib_id "VALDO:R")'), 4)

    def test_no_pseudo_power_source(self):
        self.assertNotIn("PWR_FLAG", self.lib)
        self.assertNotIn("PWR_FLAG", self.sch)

    def test_unqualified_without_battery(self):
        self.assertIs(self.contract["hardware_approved"], False)
        self.assertEqual(self.contract["battery_BMS_dock"], "DISCONNECTED")

    def test_detect_changed_pin_type(self):
        self.assertNotEqual(self.lib.replace("(pin power_out line", "(pin passive line", 1), reconstruct(self.sch))

    def test_detect_changed_pin_number(self):
        self.assertNotEqual(self.lib.replace('(number "6"', '(number "9"', 1), reconstruct(self.sch))

    def test_detect_changed_footprint(self):
        self.assertNotEqual(self.lib.replace("SOT-23-6", "SOT-23-5", 1), reconstruct(self.sch))

    def test_detect_changed_symbol_cache(self):
        self.assertNotEqual(self.lib, reconstruct(self.sch.replace("TPS22918DBVR", "CHANGED", 1)))

    def test_detect_truncation(self):
        self.assertNotEqual(self.lib[:-2], reconstruct(self.sch))

    def test_unterminated_library_cannot_parse(self):
        with self.assertRaises(ValueError):
            sexp('(lib_symbols (symbol "R")', "(lib_symbols")


if __name__ == "__main__":
    unittest.main()
