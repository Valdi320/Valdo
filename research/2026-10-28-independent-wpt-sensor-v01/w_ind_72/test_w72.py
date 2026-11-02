"""Synthetic adversarial test suite for W72, no hardware, power or radio."""
from __future__ import annotations
import json
import math
import tempfile
import unittest
from pathlib import Path
from w_ind_72.w72_switched_discharge import screen, main


class ScreenTests(unittest.TestCase):
    def test_existing_r2_remains_lossy(self):
        x=screen()
        m=x['bounded_ideal_metrics']
        self.assertGreater(m['existing_r2_steady_w'],0.030)
        self.assertFalse(m['standby_within_assumed_budget'])
        self.assertFalse(x['hardware_approved'])

    def test_switch_branch_does_not_erase_w21_resistor(self):
        x=screen(); y=screen(existing_always_on_bleeder_ohm=None)
        self.assertGreater(x['bounded_ideal_metrics']['max_known_steady_on_w'],y['bounded_ideal_metrics']['max_known_steady_on_w'])
        self.assertTrue(y['bounded_ideal_metrics']['standby_within_assumed_budget'])
        self.assertTrue(y['bounded_ideal_metrics']['decay_within_assumed_target'])
        self.assertFalse(y['may_energize'])

    def test_unknown_driver_leakage(self):
        x=screen(max_off_leakage_a=None,max_driver_on_quiescent_a=None)
        self.assertIsNone(x['bounded_ideal_metrics']['standby_within_assumed_budget'])
        self.assertIsNone(x['bounded_ideal_metrics']['max_known_steady_on_w'])

    def test_incomplete_leakage_rejected(self):
        for a,b in [(None,0.0),(0.0,None)]:
            with self.assertRaises(ValueError): screen(max_off_leakage_a=a,max_driver_on_quiescent_a=b)

    def test_without_r2_switch_open_no_path(self):
        x=screen(existing_always_on_bleeder_ohm=None)
        self.assertIn('NO IDEAL DC DISCHARGE PATH',x['fault_screen']['active_switch_stuck_open'])

    def test_double_weld_not_safe(self):
        self.assertIn('shunt live power',screen()['fault_screen']['both_upstream_switches_welded'])

    def test_sensor_power_loss_fails(self):
        self.assertIn('stale',screen()['fault_screen']['monitor_loses_supply'])

    def test_physical_flags_default_fail_closed(self):
        self.assertEqual(screen(existing_always_on_bleeder_ohm=None)['status'],'BLOCKED_PHYSICAL_POWER_PATH_UNVERIFIED')

    def test_all_declared_flags_do_not_approve_hardware(self):
        y=screen(existing_always_on_bleeder_ohm=None,
                 source_cut_physically_verified=True, reverse_feed_physically_excluded=True,
                 external_tx_storage_physically_characterized=True,
                 monitor_independently_powered_verified=True)
        self.assertTrue(y['status'].startswith('SCREEN_ONLY'))
        self.assertFalse(y['hardware_approved'])
        self.assertFalse(y['may_energize'])
        self.assertEqual(y['physical_tests'],0)

    def test_all_flags_and_real_r2_still_budget_fail(self):
        x=screen(source_cut_physically_verified=True,reverse_feed_physically_excluded=True,
                 external_tx_storage_physically_characterized=True,monitor_independently_powered_verified=True)
        self.assertEqual(x['status'],'BLOCKED_SYNTHETIC_TARGETS_NOT_MET')

    def test_too_slow_branch_fails(self):
        x=screen(resistor_nominal_ohm=10000,existing_always_on_bleeder_ohm=None)
        self.assertFalse(x['bounded_ideal_metrics']['decay_within_assumed_target'])

    def test_total_energy_upper(self):
        x=screen(existing_always_on_bleeder_ohm=None)
        self.assertAlmostEqual(x['bounded_ideal_metrics']['max_stored_j'],0.5*120e-6*5.5**2)

    def test_faster_with_existing_r2(self):
        x=screen();y=screen(existing_always_on_bleeder_ohm=None)
        self.assertLess(x['bounded_ideal_metrics']['max_decay_s'],y['bounded_ideal_metrics']['max_decay_s'])

    def test_tolerance_stretches_decay(self):
        x=screen(resistor_tolerance_fraction=0.0,cap_tolerance_fraction=0.0,
                 existing_always_on_bleeder_ohm=None)
        y=screen(existing_always_on_bleeder_ohm=None)
        self.assertGreater(y['bounded_ideal_metrics']['max_decay_s'],x['bounded_ideal_metrics']['max_decay_s'])

    def test_r_on_stretches_decay(self):
        a=screen(max_switch_on_resistance_ohm=0,existing_always_on_bleeder_ohm=None)
        b=screen(max_switch_on_resistance_ohm=100,existing_always_on_bleeder_ohm=None)
        self.assertGreater(b['bounded_ideal_metrics']['max_decay_s'],a['bounded_ideal_metrics']['max_decay_s'])

    def test_leakage_over_budget(self):
        x=screen(max_off_leakage_a=0.003,max_driver_on_quiescent_a=0,
                 existing_always_on_bleeder_ohm=None)
        self.assertFalse(x['bounded_ideal_metrics']['standby_within_assumed_budget'])

    def test_incorrect_v_threshold(self):
        with self.assertRaises(ValueError): screen(target_v=5.5)

    def test_all_critical_flags_strict_boolean(self):
        for k in ('source_cut_physically_verified','reverse_feed_physically_excluded',
                  'external_tx_storage_physically_characterized','monitor_independently_powered_verified'):
            for bad in (0,1,'false',None):
                with self.subTest(k=k,bad=bad),self.assertRaises(ValueError): screen(**{k:bad})

    def test_nan_inf_boolean_numeric_rejected(self):
        fields=('max_v','cap_nominal_f','cap_tolerance_fraction','resistor_nominal_ohm',
                'resistor_tolerance_fraction','max_switch_on_resistance_ohm','target_v',
                'deadline_s','standby_budget_w','existing_always_on_bleeder_ohm',
                'max_off_leakage_a','max_driver_on_quiescent_a')
        for k in fields:
            for bad in (math.nan,math.inf,False,'0.01'):
                with self.subTest(k=k,bad=bad),self.assertRaises(ValueError):screen(**{k:bad})

    def test_outputs_serializable(self):
        self.assertEqual(json.loads(json.dumps(screen()))['milestone'],'W-IND-72')

    def test_cli_retained_and_absent(self):
        with tempfile.TemporaryDirectory() as td:
            a=Path(td)/'a.json';b=Path(td)/'b.json'
            self.assertEqual(main(['--report',str(a)]),0)
            self.assertEqual(main(['--no-w21-r2','--report',str(b)]),0)
            self.assertFalse(json.loads(a.read_text())['bounded_ideal_metrics']['standby_within_assumed_budget'])
            self.assertTrue(json.loads(b.read_text())['bounded_ideal_metrics']['standby_within_assumed_budget'])


if __name__=='__main__': unittest.main()
