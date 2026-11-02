"""Fault injections for W-IND-19; no electrical measurements."""
from dataclasses import replace
import unittest
from w_ind_19_thermal_rail_gate import (
    Challenge, Level, ThermalChannel, channel_qualified,
    direct_pullup_may_enable, dual_hardwired_permission,
    proof_fixture, trip_band,
)


class OpenDrainHazard(unittest.TestCase):
    def test_open_drain_low_inhibits_direct_en(self):
        self.assertFalse(direct_pullup_may_enable(Level.SINK_LOW))

    def test_normal_released_drives_direct_enable(self):
        self.assertTrue(direct_pullup_may_enable(Level.RELEASED))

    def test_unpowered_or_open_line_possible_dangerous_high(self):
        self.assertTrue(direct_pullup_may_enable(Level.UNKNOWN))

    def test_nonsense_level_cannot_be_accepted(self):
        with self.assertRaises(TypeError):
            direct_pullup_may_enable(None)

    def test_47c_below_error_band(self):
        self.assertEqual(trip_band(47), "clear_if_not_latched")

    def test_50c_is_uncertain(self):
        self.assertEqual(trip_band(50), "uncertain")

    def test_51c_is_uncertain(self):
        self.assertEqual(trip_band(51), "uncertain")

    def test_52c_upper_tolerance_trips(self):
        self.assertEqual(trip_band(52), "trip_if_powered")

    def test_invalid_temperature_rejected(self):
        for x in (None, True, float('inf'), float('nan'), "bad"):
            with self.subTest(value=str(x)), self.assertRaises(ValueError):
                trip_band(x)


class IndependentRailProof(unittest.TestCase):
    def setUp(self):
        self.a = proof_fixture(100)
        self.b = proof_fixture(100)
        self.good = dict(now_ms=300, local_request=True,
                         fod_clear=True, overcurrent_clear=True, dry_clear=True)

    def allow(self, a=None, b=None, **changes):
        k = {**self.good, **changes}
        return dual_hardwired_permission(self.a if a is None else a,
                                         self.b if b is None else b, **k)

    def test_unarmed_by_default(self):
        self.assertFalse(self.allow(local_request=False))

    def test_missing_fod_never_implies_safety(self):
        self.assertFalse(self.allow(fod_clear=None))

    def test_good_synthetic_stimuli_allow_only_in_model(self):
        self.assertTrue(self.allow())

    def test_primary_rail_lost_inhibits(self):
        self.assertFalse(self.allow(a=replace(self.a, rail_good=False)))

    def test_secondary_rail_lost_inhibits(self):
        self.assertFalse(self.allow(b=replace(self.b, rail_good=False)))

    def test_unknown_rail_inhibits(self):
        self.assertFalse(self.allow(a=replace(self.a, rail_good=None)))

    def test_unpowered_output_unknown_inhibits_even_monitor_fault(self):
        self.assertFalse(self.allow(a=replace(self.a, outa=Level.UNKNOWN)))

    def test_temperature_trip_sinking_inhibits(self):
        self.assertFalse(self.allow(b=replace(self.b, outa=Level.SINK_LOW)))

    def test_missing_challenge_inhibits(self):
        self.assertFalse(self.allow(a=replace(self.a, challenge=None)))

    def test_challenge_without_witnessed_low_inhibits(self):
        self.assertFalse(self.allow(a=replace(self.a,
            challenge=Challenge(False, True, 100))))

    def test_challenge_without_release_inhibits(self):
        self.assertFalse(self.allow(a=replace(self.a,
            challenge=Challenge(True, False, 100))))

    def test_expired_challenge_inhibits(self):
        self.assertFalse(self.allow(now_ms=1101))

    def test_proof_at_exact_age_boundary_allowed(self):
        self.assertTrue(self.allow(now_ms=1100))

    def test_future_proof_inhibits(self):
        self.assertFalse(self.allow(now_ms=50))

    def test_negative_or_float_clock_raises(self):
        for clk in (-1, 1.4, True):
            with self.subTest(clk=clk), self.assertRaises(ValueError):
                channel_qualified(self.a, clk)

    def test_non_positive_lifetime_raises(self):
        with self.assertRaises(ValueError):
            channel_qualified(self.a, 300, max_age_ms=0)

    def test_secondary_channel_fails_for_any_non_released_level(self):
        for level in (Level.SINK_LOW, Level.UNKNOWN):
            with self.subTest(level=level):
                self.assertFalse(self.allow(b=replace(self.b, outa=level)))

    def test_fault_inputs_must_be_exact_true(self):
        for kw in ("fod_clear", "overcurrent_clear", "dry_clear", "local_request"):
            for value in (False, None, 1, "yes"):
                with self.subTest(input=kw, value=value):
                    self.assertFalse(self.allow(**{kw: value}))

    def test_exhaustive_two_line_levels_only_both_released_allow(self):
        for a in Level:
            for b in Level:
                result = self.allow(a=replace(self.a, outa=a),
                                    b=replace(self.b, outa=b))
                self.assertEqual(result, a is Level.RELEASED and b is Level.RELEASED)

    def test_exhaustive_rail_monitor_combinations(self):
        for a in (False, None, True):
            for b in (False, None, True):
                result = self.allow(a=replace(self.a, rail_good=a),
                                    b=replace(self.b, rail_good=b))
                self.assertEqual(result, a is True and b is True)

    def test_stuck_released_sensor_can_still_hide_real_hotspot(self):
        # Residual hazard: both monitor healthy and proof fresh, a stuck-open
        # output after last test is indistinguishable from a cool sensor.
        # This deliberately demonstrates why THIS MODEL is not safety proof.
        self.assertTrue(self.allow(a=replace(self.a, outa=Level.RELEASED)))

    def test_no_radio_argument_or_remote_restart_override(self):
        with self.assertRaises(TypeError):
            self.allow(radio_ack=True)


if __name__ == "__main__":
    unittest.main()
