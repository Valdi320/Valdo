"""W81 deterministic adverse-input tests; no device or WPT physics simulation."""
import copy
import json
import unittest
from pathlib import Path

from w81_timing_provenance import audit, number_string

SCENARIO = json.loads((Path(__file__).parent / 'SCENARIO_SYNTHETIC.json').read_text())


class TimingGate(unittest.TestCase):
    def model(self, **changes):
        x = copy.deepcopy(SCENARIO)
        x.update(changes)
        return audit(x)

    def test_real_datasheet_typical_never_qualifies(self):
        r = self.model()
        self.assertEqual('manufacturer_typical', r['fall_delay_evidence_class'])
        self.assertIn('NO_QUALIFIED_FALLING_PROPAGATION_MAX', r['blockers'])
        self.assertIn('NO_QUALIFIED_CUT_PROPAGATION_MAX', r['blockers'])
        self.assertFalse(r['hardware_approved'])

    def test_energy_exact(self):
        self.assertEqual('121.600000', self.model()['hold_up_us_conditional_on_hypotheses'])

    def test_counterfactual_false_pass(self):
        r = self.model()
        self.assertEqual('58.000000', r['naive_delay_sum_us_NOT_A_GUARANTEED_MAX'])
        self.assertTrue(r['naive_typical_based_timing_seems_to_fit'])
        self.assertFalse(r['documented_delay_pair'])
        self.assertIsNone(r['manufacturer_bounded_delay_fits_ideal_reserve'])

    def test_200_plus_40_us_cap_requirement(self):
        self.assertEqual('19.736842', self.model()['conditional_min_effective_cap_uf_IF_200us_detector_AND_40us_cut_MAX'])

    def test_47uf_ideal_reserve(self):
        self.assertEqual('571.520000', self.model(effective_cap_min_uf='47')['hold_up_us_conditional_on_hypotheses'])

    def test_very_low_effective_cap_does_not_hide_risk(self):
        self.assertFalse(self.model(effective_cap_min_uf='1')['naive_typical_based_timing_seems_to_fit'])

    def test_high_load_shrinks_hold(self):
        a = self.model()['hold_up_us_conditional_on_hypotheses']
        b = self.model(sensor_peak_power_mw='40')['hold_up_us_conditional_on_hypotheses']
        self.assertGreater(float(a), float(b))

    def test_higher_sensor_floor_shorter_hold(self):
        a = self.model()['hold_up_us_conditional_on_hypotheses']
        b = self.model(sensor_floor_v='3.05')['hold_up_us_conditional_on_hypotheses']
        self.assertGreater(float(a), float(b))

    def test_documented_max_hypothetical_counterfactual_never_authorizes(self):
        x = copy.deepcopy(SCENARIO)
        for field in ('fall_delay', 'cut_delay'):
            x[field]['evidence_class'] = 'manufacturer_max'
            x[field]['source'] = 'https://example.org/NOT-A-REAL-COMPONENT-CLAIM'
        r = audit(x)
        self.assertTrue(r['documented_delay_pair'])
        self.assertTrue(r['manufacturer_bounded_delay_fits_ideal_reserve'])
        self.assertFalse(r['hardware_approved'])

    def test_long_qualified_max_fails_hold(self):
        x = copy.deepcopy(SCENARIO)
        for field in ('fall_delay', 'cut_delay'):
            x[field]['evidence_class'] = 'manufacturer_max'
            x[field]['source'] = 'https://example.org/NOT-A-REAL-COMPONENT-CLAIM'
        x['fall_delay']['value_us'] = '200'
        self.assertIn('DOCUMENTED_DELAY_EXCEEDS_IDEAL_HOLDUP', audit(x)['blockers'])

    def test_equality_fails_to_reserve_margin(self):
        x = copy.deepcopy(SCENARIO)
        x['fall_delay']['evidence_class'] = 'manufacturer_max'
        x['cut_delay']['evidence_class'] = 'manufacturer_max'
        x['cut_delay']['source'] = 'https://example.org/not-valid-real-spec'
        x['fall_delay']['value_us'] = '81.6'
        self.assertFalse(audit(x)['manufacturer_bounded_delay_fits_ideal_reserve'])

    def test_all_switch_flags_true_still_not_hardware(self):
        r = self.model(**{n: True for n in (
            'independent_monitor_supply_verified', 'normally_off_cut_verified',
            'reverse_isolation_verified', 'latch_retention_verified')})
        self.assertFalse(r['hardware_approved'])

    def test_battery_forbidden(self):
        with self.assertRaises(ValueError):
            self.model(battery_connected=True)

    def test_critical_sensor_forbidden(self):
        with self.assertRaises(ValueError):
            self.model(sensor_kind='cliff_motor_stop')

    def test_trip_cannot_equal_floor(self):
        with self.assertRaises(ValueError):
            self.model(trip_lower_bound_v='3.0')

    def test_trip_cannot_below_floor(self):
        with self.assertRaises(ValueError):
            self.model(trip_lower_bound_v='2.8')

    def test_boolean_voltage_rejected(self):
        with self.assertRaises(ValueError):
            self.model(sensor_floor_v=True)

    def test_nonfinite_voltage_rejected(self):
        with self.assertRaises(ValueError):
            self.model(sensor_floor_v='NaN')

    def test_inf_power_rejected(self):
        with self.assertRaises(ValueError):
            self.model(sensor_peak_power_mw='Infinity')

    def test_negative_cap_rejected(self):
        with self.assertRaises(ValueError):
            self.model(effective_cap_min_uf='-1')

    def test_zero_power_rejected(self):
        with self.assertRaises(ValueError):
            self.model(sensor_peak_power_mw='0')

    def test_unbounded_cap_rejected(self):
        with self.assertRaises(ValueError):
            self.model(effective_cap_min_uf='99999999999')

    def test_true_string_for_boolean_rejected(self):
        with self.assertRaises(ValueError):
            self.model(independent_monitor_supply_verified='true')

    def test_unknown_provenance_rejected(self):
        x = copy.deepcopy(SCENARIO)
        x['fall_delay']['evidence_class'] = 'guaranteed_by_ai'
        with self.assertRaises(ValueError):
            audit(x)

    def test_empty_manufacturer_url_rejected(self):
        x = copy.deepcopy(SCENARIO)
        x['fall_delay']['source'] = ''
        with self.assertRaises(ValueError):
            audit(x)

    def test_missing_condition_rejected(self):
        x = copy.deepcopy(SCENARIO)
        del x['fall_delay']['conditions']
        with self.assertRaises(ValueError):
            audit(x)

    def test_bogus_extra_field_rejected(self):
        with self.assertRaises(ValueError):
            self.model(approved=True)

    def test_naive_fake_max_no_autoselection(self):
        x = copy.deepcopy(SCENARIO)
        x['fall_delay']['evidence_class'] = 'manufacturer_max'
        r = audit(x)
        self.assertFalse(r['design_selected'])
        self.assertFalse(r['physical_trials_authorized'])

    def test_unknown_cap_source_rejected(self):
        with self.assertRaises(ValueError):
            self.model(cap_bound_source_class='magic')

    def test_max_historical_200_not_mfr(self):
        x = copy.deepcopy(SCENARIO)
        x['fall_delay']['evidence_class'] = 'hypothesis'
        x['fall_delay']['value_us'] = '200'
        r = audit(x)
        self.assertFalse(r['documented_delay_pair'])
        self.assertIn('NO_QUALIFIED_FALLING_PROPAGATION_MAX', r['blockers'])

    def test_decimal_render_stable(self):
        self.assertEqual('1.230000', number_string(__import__('decimal').Decimal('1.23')))


if __name__ == '__main__':
    unittest.main()
