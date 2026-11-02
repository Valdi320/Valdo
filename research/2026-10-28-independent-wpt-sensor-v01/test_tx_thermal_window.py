"""W-IND-07 synthetic tests, NOT energized bench or safety qualification."""
from dataclasses import replace
import math
import unittest
from tx_thermal_window import (LOW_RATIO, HIGH_RATIO, Channel, TxInterlock,
    ntc_ratio, window_clear, corner_sweep, all_corners_clear, all_corners_trip,
    assumed_channel)


class ThermistorWindowTests(unittest.TestCase):
    def test_25c_ratio_is_half(self):
        self.assertAlmostEqual(ntc_ratio(25), .5)

    def test_45c_is_normal_at_all_assumed_corners(self):
        self.assertTrue(all_corners_clear(45))

    def test_55c_trips_all_assumed_corners(self):
        self.assertTrue(all_corners_trip(55))

    def test_minus_10c_is_normal_at_assumed_corners(self):
        self.assertTrue(all_corners_clear(-10))

    def test_minus_20c_fails_closed(self):
        self.assertTrue(all_corners_trip(-20))

    def test_50c_boundary_not_universally_classified(self):
        self.assertFalse(all_corners_clear(50))
        self.assertFalse(all_corners_trip(50))

    def test_open_wire_detected(self):
        self.assertFalse(window_clear(1.0))

    def test_short_wire_detected(self):
        self.assertFalse(window_clear(0.0))

    def test_single_low_threshold_would_miss_open(self):
        self.assertGreater(1.0, LOW_RATIO)
        self.assertFalse(window_clear(1.0))

    def test_short_boundary_strict(self):
        self.assertFalse(window_clear(LOW_RATIO))
        self.assertFalse(window_clear(HIGH_RATIO))

    def test_window_midpoint(self):
        self.assertTrue(window_clear(.5))

    def test_nan_inf_missing_are_inhibit(self):
        for value in (None, float('nan'), float('inf'), -float('inf')):
            self.assertFalse(window_clear(value))

    def test_out_of_range_values_inhibit(self):
        for value in (-1.0, 1.2, 'absent', object(), True):
            self.assertFalse(window_clear(value))

    def test_invalid_temperatures_raise(self):
        for value in (-273.15, float('nan'), float('inf')):
            with self.assertRaises(ValueError):
                ntc_ratio(value)

    def test_invalid_resistor_values_raise(self):
        for kw in ({'r25_ohm': 0}, {'beta_k': -5}, {'pullup_ohm': math.nan}):
            with self.assertRaises(ValueError):
                ntc_ratio(25, **kw)

    def test_all_corner_ratios_physical(self):
        for value in corner_sweep(45):
            self.assertTrue(0 < value < 1)


class InterlockTests(unittest.TestCase):
    def setUp(self):
        self.a = assumed_channel()
        self.b = assumed_channel()
        self.g = TxInterlock()

    def _on(self):
        return self.g.step(self.a, self.b, local_request=True, local_reset=True)

    def test_power_on_default_off(self):
        self.assertFalse(self.g.step(self.a, self.b, local_request=True)['energized'])

    def test_manual_rising_edge_allows_assumed_good(self):
        self.assertTrue(self._on()['energized'])

    def test_no_local_request_even_with_reset(self):
        self.assertFalse(self.g.step(self.a, self.b, local_request=False, local_reset=True)['energized'])

    def test_absent_fod_blocks(self):
        self.assertFalse(self.g.step(self.a, replace(self.b, fod_clear=None),
                          local_request=True, local_reset=True)['energized'])

    def test_fod_trigger_blocks_after_on(self):
        self._on()
        self.assertFalse(self.g.step(replace(self.a, fod_clear=False), self.b,
                         local_request=True)['energized'])

    def test_one_thermistor_open_blocks_after_on(self):
        self._on()
        self.assertFalse(self.g.step(replace(self.a, ntc_ratio_read=1.0), self.b,
                         local_request=True)['energized'])

    def test_one_thermistor_short_blocks(self):
        self._on()
        self.assertFalse(self.g.step(self.a, replace(self.b, ntc_ratio_read=0),
                         local_request=True)['energized'])

    def test_one_sensor_stuck_normal_other_hot_blocks(self):
        self._on()
        self.assertFalse(self.g.step(self.a, assumed_channel(60),
                         local_request=True)['energized'])

    def test_single_weld_a_with_b_hot_blocks(self):
        self._on()
        self.assertFalse(self.g.step(assumed_channel(60), assumed_channel(60),
                         local_request=True, cut_a_fault='welded_closed')['energized'])

    def test_single_weld_b_with_a_hot_blocks(self):
        self._on()
        self.assertFalse(self.g.step(assumed_channel(60), assumed_channel(60),
                         local_request=True, cut_b_fault='welded_closed')['energized'])

    def test_both_welded_remains_dangerous(self):
        result = self.g.step(assumed_channel(60), assumed_channel(60),
                   local_request=True, cut_a_fault='welded_closed', cut_b_fault='welded_closed')
        self.assertTrue(result['energized'])
        self.assertFalse(result['installation_approved'])

    def test_common_mode_two_stuck_thermistors_undetected(self):
        # Real hot TX but both analogue inputs are stuck at nominal: cannot detect.
        nominal = assumed_channel(25)
        self.assertTrue(self.g.step(nominal, nominal, local_request=True,
                                    local_reset=True)['energized'])

    def test_current_fault_blocks(self):
        self.assertFalse(self.g.step(self.a, replace(self.b, current_ok=False),
                         local_request=True, local_reset=True)['energized'])

    def test_moisture_fault_blocks(self):
        self.assertFalse(self.g.step(replace(self.a, dry_ok=False), self.b,
                         local_request=True, local_reset=True)['energized'])

    def test_alignment_fault_blocks(self):
        self.assertFalse(self.g.step(self.a, replace(self.b, alignment_ok=False),
                         local_request=True, local_reset=True)['energized'])

    def test_watchdog_fault_blocks(self):
        self.assertFalse(self.g.step(replace(self.a, supervisor_ok=False), self.b,
                         local_request=True, local_reset=True)['energized'])

    def test_unqualified_bool_value_blocks(self):
        self.assertFalse(self.g.step(replace(self.a, fod_clear=1), self.b,
                         local_request=True, local_reset=True)['energized'])

    def test_fault_latch_survives_sensor_recovery(self):
        self._on()
        self.g.step(replace(self.a, fod_clear=False), self.b, local_request=True)
        self.assertFalse(self.g.step(self.a, self.b, local_request=True)['energized'])

    def test_held_reset_cannot_auto_rearm(self):
        self._on()  # reset goes high
        self.g.step(replace(self.a, fod_clear=False), self.b,
                    local_request=True, local_reset=True)  # still high
        self.assertFalse(self.g.step(self.a, self.b, local_request=True,
                                     local_reset=True)['energized'])

    def test_release_then_reset_rearms(self):
        self._on()
        self.g.step(replace(self.a, fod_clear=False), self.b, local_request=True)
        self.g.step(self.a, self.b, local_request=True, local_reset=False)
        self.assertTrue(self.g.step(self.a, self.b, local_request=True,
                                    local_reset=True)['energized'])

    def test_supply_loss_latches_off(self):
        self._on()
        self.assertFalse(self.g.step(self.a, self.b, local_request=True,
                                    supply_present=False)['energized'])
        self.assertFalse(self.g.step(self.a, self.b, local_request=True,
                                     supply_present=True)['energized'])

    def test_local_request_drop_requires_rearm(self):
        self._on()
        self.g.step(self.a, self.b, local_request=False)
        self.assertFalse(self.g.step(self.a, self.b, local_request=True)['energized'])

    def test_stuck_open_is_safe(self):
        self.assertFalse(self.g.step(self.a, self.b, local_request=True,
                       local_reset=True, cut_b_fault='stuck_open')['energized'])

    def test_invalid_switch_fault_rejected(self):
        with self.assertRaises(ValueError):
            self.g.step(self.a, self.b, local_request=True,
                        cut_a_fault='laser')

    def test_non_boolean_request_rejected(self):
        with self.assertRaises(ValueError):
            self.g.step(self.a, self.b, local_request=1)

    def test_no_physical_approval_even_if_assumptions_good(self):
        self.assertFalse(self._on()['installation_approved'])

    def test_exhaustive_single_stuck_cut_at_hot(self):
        for a_fault in ('normal', 'welded_closed', 'stuck_open'):
            for b_fault in ('normal', 'welded_closed', 'stuck_open'):
                if a_fault == b_fault == 'welded_closed':
                    continue
                g = TxInterlock()
                g.step(self.a, self.b, local_request=True, local_reset=True)
                got = g.step(assumed_channel(60), assumed_channel(60),
                             local_request=True, cut_a_fault=a_fault, cut_b_fault=b_fault)
                self.assertFalse(got['energized'], (a_fault, b_fault))


if __name__ == '__main__':
    unittest.main()
