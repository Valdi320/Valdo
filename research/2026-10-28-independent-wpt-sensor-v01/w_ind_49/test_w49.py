import json
import unittest
from w49_ina219_acquisition_gate import evaluate, demo, CONVERSION_MS

BASE = {'mode':'synthetic','samples_averaged':16,'shunt_ohm':'0.1',
        'probe_current_min_a':'0.08','peak_current_a':'0.30','bus_voltage_v':'5',
        'sampling_period_ms':'50','max_host_pair_skew_ms':'5',
        'max_effective_skew_ms':'25','max_offset_uv':'50',
        'max_offset_fraction':'0.02'}

class W49Tests(unittest.TestCase):
    def gate(self, **kw):return evaluate({**BASE,**kw})
    def invalid(self, **kw):
        with self.assertRaises(ValueError):self.gate(**kw)
    def test_good_16(self):self.assertTrue(self.gate()['candidate_screen_pass'])
    def test_100mohm_drop_80ma(self):self.assertEqual(self.gate()['probe_shunt_drop_mv'],'8.000')
    def test_100mohm_peak_drop(self):self.assertEqual(self.gate()['peak_shunt_drop_mv'],'30.000')
    def test_100mohm_offset_fraction(self):self.assertEqual(self.gate()['offset_error_contribution_fraction'],'0.00625')
    def test_10mohm_offset_bad(self):self.assertFalse(self.gate(shunt_ohm='0.01')['shunt_screen_pass'])
    def test_10mohm_offset_ratio(self):self.assertEqual(self.gate(shunt_ohm='0.01')['offset_error_contribution_fraction'],'0.0625')
    def test_128avg_internally_unsynced(self):self.assertFalse(self.gate(samples_averaged=128)['time_screen_pass'])
    def test_128avg_2adc(self):self.assertEqual(self.gate(samples_averaged=128)['both_adc_conversion_ms'],'136.20')
    def test_16avg_2adc(self):self.assertEqual(self.gate()['both_adc_conversion_ms'],'17.02')
    def test_32avg_skew_fail(self):self.assertFalse(self.gate(samples_averaged=32)['time_screen_pass'])
    def test_1avg_pass_time(self):self.assertTrue(self.gate(samples_averaged=1)['time_screen_pass'])
    def test_16avg_short_sample_period(self):self.assertFalse(self.gate(sampling_period_ms='15')['time_screen_pass'])
    def test_16avg_too_big_host_skew(self):self.assertFalse(self.gate(max_host_pair_skew_ms='10')['time_screen_pass'])
    def test_bigger_shunt_saturates(self):self.assertFalse(self.gate(shunt_ohm='0.2')['shunt_screen_pass'])
    def test_zero_current(self):self.invalid(probe_current_min_a='0')
    def test_negative_offset(self):self.invalid(max_offset_uv='-1')
    def test_invalid_averaging(self):self.invalid(samples_averaged=3)
    def test_bool_averaging(self):self.invalid(samples_averaged=True)
    def test_nan(self):self.invalid(shunt_ohm='NaN')
    def test_inf(self):self.invalid(bus_voltage_v='Infinity')
    def test_current_range(self):self.invalid(probe_current_min_a='0.40')
    def test_bus_overvoltage(self):self.invalid(bus_voltage_v='30')
    def test_bad_limit(self):self.invalid(max_offset_fraction='1')
    def test_no_silent_sync(self):self.invalid(max_host_pair_skew_ms=None)
    def test_unknown_physical_capture(self):self.invalid(mode='measured')
    def test_measured_requires_isolation(self):
        cfg={**BASE,'mode':'measured','calibration_ref':'c1',
            'shunt_resistance_measurement_ref':'s1','physical_clock_capture_ref':'clk',
            'hardware_revision':'rev1'}
        with self.assertRaises(ValueError):evaluate(cfg)
    def test_measured_metadata_not_approval(self):
        cfg={**BASE,'mode':'measured','calibration_ref':'c1',
            'shunt_resistance_measurement_ref':'s1','physical_clock_capture_ref':'clk',
            'hardware_revision':'rev1','battery_disconnected':True,
            'source_kind':'isolated_current_limited','load_kind':'resistive'}
        out=evaluate(cfg)
        self.assertTrue(out['candidate_screen_pass'])
        self.assertFalse(out['hardware_approved'])
    def test_no_hardware_approval(self):self.assertFalse(self.gate()['hardware_approved'])
    def test_no_dock_approval(self):self.assertFalse(self.gate()['lithium_dock_approved'])
    def test_deterministic_sha(self):self.assertEqual(self.gate()['config_sha256'],self.gate()['config_sha256'])
    def test_demo_count(self):self.assertEqual(len(demo()['examples']),4)
    def test_demo_rejects_two(self):self.assertEqual(sum(bool(x['candidate_screen_pass']) for x in demo()['examples'].values()),2)
    def test_json_serializable(self):json.dumps(demo())
    def test_no_unlisted_average(self):self.assertEqual(set(CONVERSION_MS),{1,2,4,8,16,32,64,128})

if __name__=='__main__':unittest.main()
