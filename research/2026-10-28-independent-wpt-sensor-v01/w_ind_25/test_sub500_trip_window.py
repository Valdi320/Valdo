"""Original software-only W-IND-25 corner/fault regressions."""
from dataclasses import replace
import itertools
import json
import unittest
from sub500_trip_window import Assumptions, corner_screen, independent_permission, single_weld_interruptible, summary


class W25AnalogCornerTests(unittest.TestCase):
    def setUp(self): self.v=corner_screen()
    def test_nominal_sensor(self): self.assertEqual(self.v['nominal_300ma_signal_v'], .6)
    def test_nominal_fault(self): self.assertEqual(self.v['nominal_400ma_signal_v'], .8)
    def test_default_separable(self): self.assertTrue(self.v['threshold_window_exists_in_hypothetical_box'])
    def test_peak_margin_positive(self): self.assertGreater(self.v['no_false_trip_margin_mv_assumed'], 0)
    def test_fault_margin_positive(self): self.assertGreater(self.v['fault_detect_margin_mv_assumed'], 0)
    def test_order(self): self.assertLess(self.v['max_healthy_signal_v_assumed'],self.v['min_fault_signal_v_assumed'])
    def test_loss_peak_mw(self): self.assertEqual(self.v['expected_nominal_shunt_loss_mw_at_peak'], 9)
    def test_loss_fault_mw(self): self.assertEqual(self.v['expected_nominal_shunt_loss_mw_at_fault'],16)
    def test_threshold_min_max(self): self.assertLess(self.v['min_trip_threshold_v_assumed'],self.v['max_trip_threshold_v_assumed'])
    def test_threshold_low_fails(self):
        x=corner_screen(replace(Assumptions(), threshold_nominal_v=.60))
        self.assertFalse(x['threshold_window_exists_in_hypothetical_box'])
    def test_threshold_high_fails(self):
        x=corner_screen(replace(Assumptions(), threshold_nominal_v=.85))
        self.assertFalse(x['threshold_window_exists_in_hypothetical_box'])
    def test_wide_comparator_uncertainty_fails(self):
        x=corner_screen(replace(Assumptions(), comparator_uncertainty_v=.125))
        self.assertFalse(x['threshold_window_exists_in_hypothetical_box'])
    def test_wide_shunt_tolerance_fails(self):
        x=corner_screen(replace(Assumptions(), shunt_fraction=.30))
        self.assertFalse(x['threshold_window_exists_in_hypothetical_box'])
    def test_fault_too_close_fails(self):
        x=corner_screen(replace(Assumptions(),fault_min_a=.31))
        self.assertFalse(x['threshold_window_exists_in_hypothetical_box'])
    def test_increased_fault_helps(self):
        x=corner_screen(replace(Assumptions(),fault_min_a=.8))
        self.assertGreater(x['fault_detect_margin_mv_assumed'],self.v['fault_detect_margin_mv_assumed'])
    def test_increased_peak_hurts(self):
        x=corner_screen(replace(Assumptions(),normal_peak_a=.35))
        self.assertLess(x['no_false_trip_margin_mv_assumed'],self.v['no_false_trip_margin_mv_assumed'])
    def test_invalid_params(self):
        cases=[{'normal_peak_a':0},{'fault_min_a':.2},{'gain_nominal':0},
               {'nominal_shunt_ohm':0},{'shunt_fraction':1},
               {'gain_error_fraction':1},{'offset_input_v':-1},
               {'threshold_nominal_v':-1},{'threshold_fraction':1},
               {'comparator_uncertainty_v':-1},{'normal_peak_a':float('nan')},
               {'fault_min_a':float('inf')}]
        for case in cases:
            with self.subTest(case=case),self.assertRaises(ValueError):
                corner_screen(replace(Assumptions(),**case))
    def test_no_fake_datasheet_claim(self):
        self.assertFalse(self.v['effective_threshold_tolerance_verified'])
        self.assertFalse(self.v['limit_resistor_value_qualified'])
    def test_separate_safety_blocks(self):
        for k in ('comparator_power_rail_qualified','shunt_part_verified','cutoff_path_schematic_verified',
                  'autonomous_fod_hardware_verified','thermal_cut_hardware_verified','coil_temperature_offset_emi_measured'):
            with self.subTest(key=k): self.assertFalse(self.v[k])
    def test_no_lithium(self): self.assertFalse(self.v['dock_battery_bms_connected'])
    def test_never_enabled(self):
        for v in (self.v,summary()):
            self.assertFalse(v['hardware_approved']);self.assertFalse(v['power_on_allowed'])
    def test_json_serializable(self): json.loads(json.dumps(summary()))
    def test_no_measured_runs(self): self.assertEqual(self.v['physical_tests'], 0)

class W25IndependentInterlockTests(unittest.TestCase):
    def test_all_healthy_only(self):
        self.assertTrue(independent_permission(source_healthy=True,comparator_power_good=True,
            current_below_trip=True,thermal_healthy=True,fod_healthy=True,local_watchdog_healthy=True))
    def test_exhaustive_one_of_64_healthy(self):
        enabled=0
        for bits in itertools.product((False,True),repeat=6):
            enabled+=independent_permission(**dict(zip(('source_healthy','comparator_power_good',
                'current_below_trip','thermal_healthy','fod_healthy','local_watchdog_healthy'),bits)))
        self.assertEqual(enabled,1)
    def test_power_loss_stops(self):
        self.assertFalse(independent_permission(source_healthy=True,comparator_power_good=False,
            current_below_trip=True,thermal_healthy=True,fod_healthy=True,local_watchdog_healthy=True))
    def test_fod_stops(self):
        self.assertFalse(independent_permission(source_healthy=True,comparator_power_good=True,
            current_below_trip=True,thermal_healthy=True,fod_healthy=False,local_watchdog_healthy=True))
    def test_thermal_stops(self):
        self.assertFalse(independent_permission(source_healthy=True,comparator_power_good=True,
            current_below_trip=True,thermal_healthy=False,fod_healthy=True,local_watchdog_healthy=True))
    def test_radio_not_dependency(self):
        self.assertNotIn('radio', independent_permission.__code__.co_varnames)
    def test_no_welds_interruptible(self): self.assertTrue(single_weld_interruptible(False,False))
    def test_a_weld_interruptible(self): self.assertTrue(single_weld_interruptible(True,False))
    def test_b_weld_interruptible(self): self.assertTrue(single_weld_interruptible(False,True))
    def test_double_weld_unsafe(self): self.assertFalse(single_weld_interruptible(True,True))

if __name__=='__main__':unittest.main()
