"""Adversarial offline tests: zero physical tests and no external dependencies."""
from decimal import Decimal as D
import json
import subprocess
import sys
import unittest
from pathlib import Path

import w86_field_sweep as m


class ManufacturerIntegrity(unittest.TestCase):
    def test_valid_points(self):
        self.assertTrue(m.validate_points())

    def test_22_points(self):
        self.assertEqual(sum(len(m.points(x)) for x in ('AM10', 'AM100')), 22)

    def test_all_exact_products(self):
        for name in ('AM10', 'AM100'):
            for p in m.points(name):
                self.assertEqual(p.v*p.i, p.p)

    def test_field_grid_spacing(self):
        for name in ('AM10', 'AM100'):
            self.assertEqual([p.h for p in m.points(name)], [D(i)/2 for i in range(1, 12)])

    def test_author_am100_h3(self):
        self.assertEqual(m.at('AM100', '3').p, D('2.907'))

    def test_author_am10_h3(self):
        self.assertEqual(m.at('AM10', '3').p, D('4.069'))

    def test_author_weak_h05(self):
        self.assertEqual((m.at('AM10', '0.5').p, m.at('AM100', '0.5').p), (D('0.36'), D('2.31')))

    def test_author_high_h55(self):
        self.assertEqual(m.at('AM10', '5.5').v, D('2.57'))

    def test_no_field_interpolation(self):
        with self.assertRaises(ValueError): m.at('AM10', '0.75')

    def test_no_negative_field(self):
        with self.assertRaises(ValueError): m.at('AM10', '-1')

    def test_no_outside_field(self):
        with self.assertRaises(ValueError): m.at('AM10', '6')

    def test_no_unknown_am(self):
        with self.assertRaises(ValueError): m.points('AM30')

    def test_unknown_malformed(self):
        with self.assertRaises(ValueError): m.at('AM10', 'wat')

    def test_no_float(self):
        with self.assertRaises(ValueError): m.at('AM10', 3.0)

    def test_no_nonfinite(self):
        for bad in ('NaN', 'Infinity', '-Infinity'):
            with self.subTest(bad=bad), self.assertRaises(ValueError): m.at('AM10', bad)

    def test_no_boolean(self):
        with self.assertRaises(ValueError): m.at('AM10', True)


class ConditionalScreen(unittest.TestCase):
    PARAM = dict(sensor_mw='2.9', efficiency='0.8', converter_vin_min_v='3.3')

    def test_am10_weak_power_failure(self):
        o = m.screen('AM10', '0.5', **self.PARAM)
        self.assertEqual(o['hypothetical_useful_mW'], '0.288')
        self.assertFalse(o['power_meets_assumption'])
        self.assertTrue(o['voltage_meets_assumption'])

    def test_am10_3_power_appears_good_but_voltage_fails(self):
        o = m.screen('AM10', '3', **self.PARAM)
        self.assertTrue(o['power_meets_assumption'])
        self.assertFalse(o['voltage_meets_assumption'])
        self.assertEqual(o['hardware_release'], 'BLOCKED')

    def test_am100_3_fails_power_and_voltage(self):
        o = m.screen('AM100', '3', **self.PARAM)
        self.assertFalse(o['power_meets_assumption'])
        self.assertFalse(o['voltage_meets_assumption'])

    def test_am10_0_5_to_3_no_author_point_satisfies_both(self):
        o = m.window('AM10', '0.5', '3', **self.PARAM)
        self.assertEqual(o['sampled_points'], 6)
        self.assertEqual(o['sampled_points_meeting_both'], 0)
        self.assertFalse(o['continuum_certified'])

    def test_am100_0_5_to_3_no_author_point_satisfies_both(self):
        o = m.window('AM100', '0.5', '3', **self.PARAM)
        self.assertEqual(o['sampled_points_meeting_both'], 0)

    def test_reversal_in_modulation(self):
        self.assertEqual(m.compare_modulations('0.5')['higher_power_at_this_author_point'], 'AM100')
        self.assertEqual(m.compare_modulations('3')['higher_power_at_this_author_point'], 'AM10')

    def test_equal_power_sample(self):
        self.assertEqual(m.compare_modulations('1.5')['higher_power_at_this_author_point'], 'EQUAL')

    def test_observed_ranking(self):
        self.assertEqual(m.report()['observed_power_ranking'], {'AM100': 2, 'AM10': 8, 'EQUAL': 1})

    def test_zero_load_invalid(self):
        with self.assertRaises(ValueError): m.screen('AM10','3',sensor_mw='0',efficiency='0.8',converter_vin_min_v='3.3')

    def test_eff_above_one(self):
        with self.assertRaises(ValueError): m.screen('AM10','3',sensor_mw='1',efficiency='1.001',converter_vin_min_v='3.3')

    def test_eff_zero(self):
        with self.assertRaises(ValueError): m.screen('AM10','3',sensor_mw='1',efficiency='0',converter_vin_min_v='3.3')

    def test_bad_vin(self):
        with self.assertRaises(ValueError): m.screen('AM10','3',sensor_mw='1',efficiency='1',converter_vin_min_v='-1')

    def test_window_unsupported_boundary(self):
        with self.assertRaises(ValueError): m.window('AM10','0.75','3', **self.PARAM)

    def test_window_reversed(self):
        with self.assertRaises(ValueError): m.window('AM10','3','2', **self.PARAM)

    def test_no_false_hardware_release_any_point(self):
        for am in ('AM100', 'AM10'):
            for p in m.points(am):
                self.assertEqual(m.screen(am,p.h,**self.PARAM)['hardware_release'], 'BLOCKED')

    def test_manufacturer_not_minimum(self):
        self.assertIn('not_guaranteed', m.PROVENANCE)
        self.assertFalse(m.report()['measured_by_us'])

    def test_weak_finds_lower_than_3a(self):
        self.assertLess(m.at('AM10','0.5').p, m.at('AM10','3').p)

    def test_deterministic_cli_json(self):
        proc = subprocess.run([sys.executable, str(Path(__file__).with_name('w86_field_sweep.py'))], capture_output=True, check=True, text=True)
        self.assertEqual(json.loads(proc.stdout), m.report())
        self.assertEqual(proc.stdout, Path(__file__).with_name('expected.json').read_text())


if __name__ == '__main__':
    unittest.main()
