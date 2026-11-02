"""Deterministic synthetic tests for W-IND-52. They are NOT physical tests."""
from dataclasses import replace
import importlib.util
import pathlib
import unittest

path = pathlib.Path(__file__).with_name('w52_calibration_gate.py')
spec = importlib.util.spec_from_file_location('w52', path)
w = importlib.util.module_from_spec(spec)
import sys
sys.modules['w52'] = w
spec.loader.exec_module(w)


class TestW52(unittest.TestCase):
    def setUp(self):
        b = w.demo()
        self.tx = w.Channel(position='TX',meter_id='T',shunt_id='S-T',reference_id='REF',
            calibration_valid_from='2026-10-29',calibration_valid_until='2026-11-29',
            as_of='2026-10-30',source_kind='SYNTHETIC',zero_uv=20,check_uv=8020,span_uv=30020,
            check_reference_ma='80',span_reference_ma='300',check_reference_uncertainty_ma='0.2',
            span_reference_uncertainty_ma='0.2',cal_temperature_c='25',use_temperature_c='27',
            shunt_tcr_ppm_per_c='100',chip_gain_drift_ppm_per_c='167',
            chip_offset_drift_uv_per_c='0.5')
        self.rx = replace(self.tx,position='RX',meter_id='R',shunt_id='S-R')

    def test_nominal_holdout(self):
        r=w.screen_channel(self.tx)
        self.assertEqual(r['nominal_check_ma'],'80')
        self.assertTrue(r['pass_conditional_model'])
        self.assertLess(float(r['conditional_worst_case_error_percent']),3)
    def test_synthetic_never_bench_qualified(self):
        self.assertFalse(w.screen_channel(self.tx)['bench_metrology_candidate'])
    def test_bad_holdout_detected(self):
        r=w.screen_channel(replace(self.tx,check_uv=6420))
        self.assertFalse(r['pass_conditional_model'])
        self.assertIn('holdout current mismatch exceeds error budget',r['blockers'])
    def test_zero_over_limit_blocks(self):
        r=w.screen_channel(replace(self.tx,zero_uv=70,check_uv=8070,span_uv=30070))
        self.assertIn('zero reading exceeds conditional device offset bound',r['blockers'])
    def test_negative_polarity(self):
        with self.assertRaises(ValueError): w.screen_channel(replace(self.tx,check_uv=-8000))
    def test_saturated_pga(self):
        with self.assertRaises(ValueError): w.screen_channel(replace(self.tx,span_uv=40010))
    def test_non_quantized_raw(self):
        with self.assertRaises(ValueError): w.screen_channel(replace(self.tx,check_uv=8021))
    def test_unsorted_raw(self):
        with self.assertRaises(ValueError): w.screen_channel(replace(self.tx,check_uv=30020))
    def test_missing_reference(self):
        with self.assertRaises(ValueError): w.screen_channel(replace(self.tx,reference_id=''))
    def test_bad_channel(self):
        with self.assertRaises(ValueError): w.screen_channel(replace(self.tx,position='MOTOR'))
    def test_negative_ref_error(self):
        with self.assertRaises(ValueError): w.screen_channel(replace(self.tx,span_reference_uncertainty_ma='-0.2'))
    def test_uncertainty_over_current(self):
        with self.assertRaises(ValueError): w.screen_channel(replace(self.tx,check_reference_uncertainty_ma='81'))
    def test_nan_rejected(self):
        with self.assertRaises(ValueError): w.screen_channel(replace(self.tx,check_reference_ma='NaN'))
    def test_gain_temperature_drift_missing(self):
        r=w.screen_channel(replace(self.tx,chip_gain_drift_ppm_per_c=None))
        self.assertIsNone(r['conditional_worst_case_error_percent'])
        self.assertIn('temperature drift parameters missing',r['blockers'])
    def test_shunt_temperature_drift_missing(self):
        r=w.screen_channel(replace(self.tx,shunt_tcr_ppm_per_c=None))
        self.assertIn('temperature drift parameters missing',r['blockers'])
    def test_negative_tcr(self):
        with self.assertRaises(ValueError): w.screen_channel(replace(self.tx,shunt_tcr_ppm_per_c='-1'))
    def test_temperature_outside_window(self):
        r=w.screen_channel(replace(self.tx,use_temperature_c='50'))
        self.assertIn('measurement temperature outside calibration window',r['blockers'])
    def test_temperature_increases_uncertainty(self):
        a=w.screen_channel(replace(self.tx,use_temperature_c='25'))
        b=w.screen_channel(replace(self.tx,use_temperature_c='27'))
        self.assertLess(float(a['conditional_worst_case_error_percent']),float(b['conditional_worst_case_error_percent']))
    def test_expired_reference(self):
        r=w.screen_channel(replace(self.tx,as_of='2026-12-01'))
        self.assertIn('reference calibration not valid on as_of date',r['blockers'])
    def test_future_reference(self):
        r=w.screen_channel(replace(self.tx,as_of='2026-10-01'))
        self.assertIn('reference calibration not valid on as_of date',r['blockers'])
    def test_reversed_dates(self):
        with self.assertRaises(ValueError): w.screen_channel(replace(self.tx,calibration_valid_until='2026-10-01'))
    def test_unknown_source(self):
        with self.assertRaises(ValueError): w.screen_channel(replace(self.tx,source_kind='AUTHOR_MEASURED'))
    def test_unqualified_reference_burden(self):
        r=w.screen_channel(self.tx)
        self.assertIn('reference burden not qualified',r['blockers'])
    def test_no_zero_current_evidence(self):
        r=w.screen_channel(self.tx)
        self.assertIn('zero-current state not independently verified',r['blockers'])
    def test_no_temperature_measurement(self):
        r=w.screen_channel(self.tx)
        self.assertIn('temperature is not measured',r['blockers'])
    def test_missing_shunt_identity(self):
        r=w.screen_channel(self.tx)
        self.assertIn('shunt identity/TCR unverified',r['blockers'])
    def test_bench_measured_metadata_conditional(self):
        # Synthetic data with BENCH_MEASURED label is NOT evidence: this test
        # exercises only software logic. No measurement is claimed.
        r=w.screen_channel(replace(self.tx,source_kind='BENCH_MEASURED',reference_traceable=True,
            reference_burden_qualified=True,chip_grade_verified=True,shunt_identity_verified=True,
            zero_current_verified=True,temperature_measured=True))
        self.assertTrue(r['bench_metrology_candidate'])
        self.assertFalse(r['hardware_approved'])
    def test_wrong_meter_pair(self):
        with self.assertRaises(ValueError): w.screen_pair(self.tx,replace(self.tx,position='RX'))
    def test_same_shunt_pair(self):
        with self.assertRaises(ValueError): w.screen_pair(self.tx,replace(self.rx,shunt_id='S-T'))
    def test_swapped_roles_pair(self):
        with self.assertRaises(ValueError): w.screen_pair(self.rx,self.tx)
    def test_dual_is_not_efficiency_approval(self):
        r=w.screen_pair(self.tx,self.rx)
        self.assertFalse(r['both_current_channels_bench_candidates'])
        self.assertFalse(r['efficiency_metrology_approved'])
        self.assertTrue(r['battery_BMS_dock_disconnected'])
    def test_demo_rejects_bad_rx(self):
        d=w.demo()
        self.assertFalse(d['bad_rx_holdout_example']['pass_conditional_model'])
        self.assertFalse(d['hardware_approved'])

if __name__ == '__main__': unittest.main()
