#!/usr/bin/env python3
"""Independent synthetic parser/adversarial tests; never a hardware test."""
import csv
import io
import unittest
from w73_source_inventory import (
    audit, bom_cap_refs, farads, git_blob_sha, is_between, parse_netlist, validate_source,
)


def fixture(nets=None, component_lines=None):
    if component_lines is None:
        component_lines = ['    (comp (ref C101)\n      (value 330u))', '    (comp (ref C102)\n      (value 100n))']
    if nets is None:
        nets = [("GND", [("C101", "2")]), ("/HD", [("C101", "1")]),
                ("/HS_1", [("C102", "2")]), ("RF_COMP", [("C102", "1")])]
    blocks = []
    for i, (name, nodes) in enumerate(nets, 1):
        b = f'    (net (code {i}) (name {name})\n'
        b += '\n'.join(f'      (node (ref {ref}) (pin {pin}))' for ref, pin in nodes) + ')'
        blocks.append(b)
    return '(export\n  (components\n' + '\n'.join(component_lines) + ')\n  (nets\n' + '\n'.join(blocks) + '))'


class TestW73(unittest.TestCase):
    def test_two_capacitors_recognized(self):
        m = parse_netlist(fixture())
        self.assertEqual(set(m), {'C101', 'C102'})
    def test_pin_to_net_mapping(self):
        self.assertTrue(is_between(parse_netlist(fixture())['C101'], 'GND', '/HD'))
    def test_rf_is_not_ground_bypass(self):
        self.assertFalse(is_between(parse_netlist(fixture())['C102'], 'GND', '/HS_1'))
    def test_duplicate_component_rejected(self):
        with self.assertRaises(ValueError):
            parse_netlist(fixture(component_lines=['(comp (ref C101)\n(value 330u))']*2))
    def test_duplicate_pin_rejected(self):
        with self.assertRaises(ValueError):
            parse_netlist(fixture(nets=[('GND', [('C101','2'),('C101','2')])]))
    def test_incomplete_mapping_rejected(self):
        with self.assertRaises(ValueError):
            parse_netlist(fixture(nets=[('GND', [('C101','2')])]))
    def test_no_nets_rejected(self):
        with self.assertRaises(ValueError):
            parse_netlist('(export (components (comp (ref C1) (value 1u))))')
    def test_empty_caps_rejected(self):
        with self.assertRaises(ValueError):
            parse_netlist('(export\n  (components (comp (ref R1) (value 1k)))\n  (nets\n    (net (code 1) (name GND) (node (ref R1) (pin 1)))))')
    def test_values(self):
        self.assertAlmostEqual(farads('330u'), 330e-6)
        self.assertAlmostEqual(farads('100n'), 1e-7)
    def test_unsupported_value_rejected(self):
        for x in ('4.7µF', '100', 'NaN', '-3u', 'inf', '10UF'):
            with self.subTest(x=x), self.assertRaises(ValueError): farads(x)
    def test_blob_sha_golden(self):
        self.assertEqual(git_blob_sha(b'hello\n'), 'ce013625030ba8dba906f756967f9e9ca394464a')
    def test_blob_mismatch_rejected(self):
        with self.assertRaises(ValueError): validate_source(b'bad', '0'*40)
    def test_bom_refs(self):
        s='Component,References,Value\n1,C1 C2,330u\n2,C10,1u\n'
        self.assertEqual(bom_cap_refs(s), {'C1','C2','C10'})
    def test_duplicate_bom_ref_rejected(self):
        with self.assertRaises(ValueError): bom_cap_refs('References\nC1 C1\n')
    def test_empty_bom_rejected(self):
        with self.assertRaises(ValueError): bom_cap_refs('References\nR5 R9\n')
    def test_missing_bom_column_rejected(self):
        with self.assertRaises(ValueError): bom_cap_refs('Parts\nC3\n')
    def test_fixture_not_mistaken_for_real_author_source(self):
        with self.assertRaises(ValueError): audit(fixture().encode(), b'References\nC101\n')
    def test_energy_is_conditional_not_test_result(self):
        # 4 * 330uF nominal, assuming all at 24V, no tolerance/ESR/leakage.
        self.assertAlmostEqual(.5 * 4 * farads('330u') * 24**2, .38016, places=8)
    def test_duplicate_net_name_does_not_hide_duplicate_pin(self):
        with self.assertRaises(ValueError):
            parse_netlist(fixture(nets=[('GND', [('C101','2')]), ('GND', [('C101','2')])]))

if __name__ == '__main__':
    unittest.main()
