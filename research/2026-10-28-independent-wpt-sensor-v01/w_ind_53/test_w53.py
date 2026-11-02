"""Adversarial SYNTHETIC tests for W53; not physical calibration."""
import importlib.util
from dataclasses import replace
from pathlib import Path
import sys
import unittest

spec=importlib.util.spec_from_file_location('w53', Path(__file__).with_name('w53_bus_voltage_gate.py'))
w=importlib.util.module_from_spec(spec)
sys.modules['w53']=w
spec.loader.exec_module(w)

class TestW53(unittest.TestCase):
    def setUp(self):
        self.tx=w.Channel(role='TX',meter_id='TX-1',reference_id='REF-SYNTH',source_kind='SYNTHETIC',
            valid_from='2026-10-29',valid_until='2026-11-29',as_of='2026-10-30',
            low_raw_mv=3000,high_raw_mv=6000,check_raw_mv=5000,
            low_ref_mv='3000',high_ref_mv='6000',check_ref_mv='5000',
            low_uncertainty_mv='3',high_uncertainty_mv='3',check_uncertainty_mv='3',
            calibration_temperature_c='25',operating_temperature_c='27',
            gain_drift_ppm_per_c='200',offset_drift_mv_per_c='0.5')
        self.rx=replace(self.tx,role='RX',meter_id='RX-2',check_raw_mv=4000,check_ref_mv='4000')
    def test_tx_nominal_5000(self):
        r=w.screen_channel(self.tx)
        self.assertEqual(float(r['nominal_predicted_holdout_mv']),5000.0)
        self.assertTrue(r['pass_conditional_model'])
    def test_rx_nominal_4000(self):
        self.assertTrue(w.screen_channel(self.rx)['pass_conditional_model'])
    def test_conditional_bound_reasonable(self):
        self.assertLess(float(w.screen_channel(self.rx)['conditional_worst_case_error_percent']),1)
    def test_known_deviation_rejected(self):
        self.assertIn('independent voltage holdout exceeds error budget',w.screen_channel(replace(self.rx,check_raw_mv=3840))['blockers'])
    def test_reference_holdout_shift_detected(self):
        self.assertFalse(w.screen_channel(replace(self.rx,check_ref_mv='4200'))['pass_conditional_model'])
    def test_synthetic_cannot_qualify(self):
        self.assertFalse(w.screen_channel(self.tx)['voltage_bench_candidate'])
    def test_model_never_hardware_approval(self):
        self.assertFalse(w.screen_pair(self.tx,self.rx)['hardware_approved'])
    def test_voltage_not_efficiency_approval(self):
        self.assertFalse(w.screen_pair(self.tx,self.rx)['efficiency_metrology_approved'])
    def test_pair_different_meters(self):
        with self.assertRaises(ValueError):w.screen_pair(self.tx,replace(self.rx,meter_id='TX-1'))
    def test_swap_pair_fails(self):
        with self.assertRaises(ValueError):w.screen_pair(self.rx,self.tx)
    def test_bad_role(self):
        with self.assertRaises(ValueError):w.screen_channel(replace(self.tx,role='MOTOR'))
    def test_missing_reference(self):
        with self.assertRaises(ValueError):w.screen_channel(replace(self.tx,reference_id=''))
    def test_fake_source_not_accepted(self):
        with self.assertRaises(ValueError):w.screen_channel(replace(self.tx,source_kind='AUTHOR'))
    def test_non_lsb_quantized_rejected(self):
        with self.assertRaises(ValueError):w.screen_channel(replace(self.tx,check_raw_mv=5001))
    def test_boolean_as_raw_rejected(self):
        with self.assertRaises(ValueError):w.screen_channel(replace(self.tx,check_raw_mv=True))
    def test_wrong_lsb_rejected(self):
        with self.assertRaises(ValueError):w.screen_channel(replace(self.tx,bus_lsb_mv=1))
    def test_saturated_bus_rejected(self):
        with self.assertRaises(ValueError):w.screen_channel(replace(self.tx,high_raw_mv=26000))
    def test_reversed_bus_rejected(self):
        with self.assertRaises(ValueError):w.screen_channel(replace(self.tx,low_raw_mv=5000))
    def test_reference_not_ordered_rejected(self):
        with self.assertRaises(ValueError):w.screen_channel(replace(self.tx,check_ref_mv='6200'))
    def test_ref_ranges_cannot_overlap(self):
        with self.assertRaises(ValueError):w.screen_channel(replace(self.tx,check_uncertainty_mv='1200'))
    def test_zero_uncertainty_rejected(self):
        with self.assertRaises(ValueError):w.screen_channel(replace(self.tx,low_uncertainty_mv='0'))
    def test_nan_rejected(self):
        with self.assertRaises(ValueError):w.screen_channel(replace(self.tx,low_ref_mv='NaN'))
    def test_infinity_rejected(self):
        with self.assertRaises(ValueError):w.screen_channel(replace(self.tx,low_ref_mv='Infinity'))
    def test_negative_drift_rejected(self):
        with self.assertRaises(ValueError):w.screen_channel(replace(self.tx,gain_drift_ppm_per_c='-1'))
    def test_missing_drift_blocks(self):
        self.assertIn('temperature drift bounds missing',w.screen_channel(replace(self.tx,gain_drift_ppm_per_c=None))['blockers'])
    def test_expired_reference_blocks(self):
        self.assertIn('reference expired or not yet valid',w.screen_channel(replace(self.tx,as_of='2026-12-01'))['blockers'])
    def test_reverse_date_rejected(self):
        with self.assertRaises(ValueError):w.screen_channel(replace(self.tx,valid_until='2026-10-01'))
    def test_temperature_outside_window_blocks(self):
        self.assertIn('outside calibrated temperature window',w.screen_channel(replace(self.tx,operating_temperature_c='41'))['blockers'])
    def test_increased_drift_increases_error(self):
        a=w.screen_channel(replace(self.tx,operating_temperature_c='25'))
        b=w.screen_channel(replace(self.tx,operating_temperature_c='27'))
        self.assertLess(float(a['conditional_worst_case_error_percent']),float(b['conditional_worst_case_error_percent']))
    def test_metadata_cannot_authorize_hardware(self):
        p=replace(self.tx,source_kind='BENCH_MEASURED',reference_traceable=True,
            correct_board_and_chip_verified=True, independent_holdout_recorded=True,
            temperature_measured=True,acquisition_and_clock_verified=True)
        r=w.screen_channel(p)
        self.assertTrue(r['voltage_bench_candidate'])
        self.assertFalse(r['hardware_approved'])
    def test_missing_clock_gate_blocks(self):
        p=replace(self.tx,source_kind='BENCH_MEASURED',reference_traceable=True,
            correct_board_and_chip_verified=True, independent_holdout_recorded=True,
            temperature_measured=True)
        self.assertIn('I2C clock and freshness not verified',w.screen_channel(p)['blockers'])
    def test_demo_separates_fault(self):
        d=w.demo()
        self.assertTrue(d['tx']['pass_conditional_model'])
        self.assertFalse(d['bad_rx_holdout_example']['pass_conditional_model'])
    def test_even_low_noise_not_real(self):
        self.assertTrue(w.demo()['battery_BMS_dock_disconnected'])

if __name__=='__main__':
    unittest.main()
