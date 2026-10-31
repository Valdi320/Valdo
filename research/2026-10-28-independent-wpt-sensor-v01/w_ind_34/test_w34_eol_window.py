"""Deterministic pure-Python tests of the hypothetical W-IND-34 envelope."""
import unittest
from dataclasses import replace
from w34_eol_window import Corner, corner_grid, probe, evidence

class WindowContract(unittest.TestCase):
    def test_01_nominal_half_rail(self):
        self.assertAlmostEqual(probe(Corner())['observed_ratio'], 0.5)
    def test_02_no_automatic_hardware_approval(self):
        self.assertFalse(probe(Corner())['hardware_power_authorized'])
    def test_03_nominal_open_rejected(self):
        self.assertFalse(probe(Corner(), signal_open=True)['permit_request'])
    def test_04_nominal_return_open_rejected(self):
        self.assertFalse(probe(Corner(), return_open=True)['permit_request'])
    def test_05_nominal_short_rejected(self):
        self.assertFalse(probe(Corner(), signal_short=True)['permit_request'])
    def test_06_nominal_eol_open_rejected(self):
        self.assertFalse(probe(Corner(), eol_open=True)['permit_request'])
    def test_07_nominal_eol_short_rejected(self):
        self.assertFalse(probe(Corner(), eol_short=True)['permit_request'])
    def test_08_nominal_alert_assertion_rejected(self):
        self.assertFalse(probe(Corner(), alarm=True)['permit_request'])
    def test_09_duplicate_w32_w33_pullups_not_silent(self):
        x=probe(Corner(extra_pullup_ohm=10000.0))
        self.assertAlmostEqual(x['observed_ratio'], 2/3)
        self.assertFalse(x['permit_request'])
    def test_10_monitor_unpowered_needs_separate_pg(self):
        self.assertTrue(probe(Corner())['in_window'])
        self.assertFalse(probe(Corner(), monitor_power_good=False)['permit_request'])
    def test_11_rail_supervision_required(self):
        self.assertFalse(probe(Corner(), rail_supervised=False)['permit_request'])
    def test_12_local_rearm_required(self):
        self.assertFalse(probe(Corner(), local_armed=False)['permit_request'])
    def test_13_drift_14k_can_look_healthy(self):
        self.assertTrue(probe(Corner(eol_ohm=14000.0))['in_window'])
    def test_14_negative_rail_rejected(self):
        with self.assertRaises(ValueError):probe(Corner(rail_v=-1))
    def test_15_zero_eol_rejected_as_invalid_component(self):
        with self.assertRaises(ValueError):probe(Corner(eol_ohm=0))
    def test_16_bad_window_rejected(self):
        with self.assertRaises(ValueError):probe(Corner(lower_ratio=.8,upper_ratio=.2))
    def test_17_bad_extra_pullup_rejected(self):
        with self.assertRaises(ValueError):probe(Corner(extra_pullup_ohm=0))
    def test_18_healthy_all_corners(self):
        self.assertEqual(sum(probe(c)['permit_request'] for c in corner_grid()),128)
    def test_19_open_all_corners_rejected(self):
        self.assertEqual(sum(probe(c,signal_open=True)['permit_request'] for c in corner_grid()),0)
    def test_20_ground_return_all_corners_rejected(self):
        self.assertEqual(sum(probe(c,return_open=True)['permit_request'] for c in corner_grid()),0)
    def test_21_alarm_all_corners_rejected(self):
        self.assertEqual(sum(probe(c,alarm=True)['permit_request'] for c in corner_grid()),0)
    def test_22_duplicate_pullup_all_corners_rejected(self):
        self.assertEqual(sum(probe(replace(c,extra_pullup_ohm=c.pullup_ohm))['permit_request'] for c in corner_grid()),0)
    def test_23_worst_case_margin_positive(self):
        self.assertGreater(evidence()['minimum_window_margin_ratio'],.04)
    def test_24_scenarios_and_dead_monitor_counterexample(self):
        e=evidence()
        self.assertEqual(e['corners'],128)
        self.assertEqual(e['total_scenario_checks'],1152)
        self.assertEqual(e['monitor_off_without_pg_misses'],128)
        self.assertFalse(e['safety_verified'])

if __name__=='__main__':unittest.main()
