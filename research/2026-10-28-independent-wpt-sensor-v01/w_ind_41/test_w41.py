"""W-IND-41 logic and resistor-corner regression. Synthetic, NOT hardware."""
import unittest
import json
import w41_independent_pg as w


class SupervisorTests(unittest.TestCase):
    def test_ti_reference_nominal_tripping(self):
        self.assertAlmostEqual(w.LOW_Z.record()['nominal_trip_v'],2.88)
    def test_same_nominal_ratio_but_different_leakage(self):
        self.assertAlmostEqual(w.LOW_Z.record()['nominal_trip_v'],w.HIGH_Z.record()['nominal_trip_v'])
        self.assertGreater(w.HIGH_Z.record()['maximum_trip_v'],w.LOW_Z.record()['maximum_trip_v'])
    def test_low_z_corner_pass(self):
        self.assertTrue(w.LOW_Z.record()['stress_pass'])
    def test_high_z_corner_fails(self):
        self.assertFalse(w.HIGH_Z.record()['stress_pass'])
    def test_68k_corner_fails(self):
        self.assertFalse(w.TOO_HIGH.record()['stress_pass'])
    def test_normal_supply_has_positive_margin(self):
        self.assertGreater(w.LOW_Z.record()['no_false_trip_margin_v'],0.10)
    def test_dead_rail_below_min_trip(self):
        self.assertGreater(w.LOW_Z.record()['minimum_trip_v'],2.70)
    def test_leakage_sign_matters(self):
        self.assertGreater(w.LOW_Z.crossing_v(.4,62000,10000,1e-6),
                           w.LOW_Z.crossing_v(.4,62000,10000,-1e-6))
    def test_stress_rejected_if_negative(self):
        with self.assertRaises(ValueError):w.LOW_Z.corners(-1)
    def test_ideal_power_domain_trip(self):
        self.assertFalse(w.idealized_permission(5.,0.,True)['request_on'])
    def test_open_wire_is_unsafe(self):
        self.assertTrue(w.idealized_permission(5.,0.,True,wire_open=True)['unsafe_if_3v3_dead'])
    def test_stuck_output_is_unsafe(self):
        self.assertTrue(w.idealized_permission(5.,0.,True,comparator_stuck_released=True)['unsafe_if_3v3_dead'])
    def test_bad_5v_rail_is_blocked_ideally(self):
        self.assertFalse(w.idealized_permission(2.2,0.,True)['request_on'])
    def test_good_rail_without_local_rearm_blocked(self):
        self.assertFalse(w.idealized_permission(5.,3.3,False)['request_on'])
    def test_normal_assumed_armed(self):
        self.assertTrue(w.idealized_permission(5.,3.3,True)['request_on'])
    def test_5v_external_pg_reject(self):
        self.assertFalse(w.idealized_permission(5.,3.3,True,external_5v_good=False)['request_on'])
    def test_low_z_consumption_is_small_but_not_free(self):
        extra=w.LOW_Z.record()['divider_power_at_3v3_mw']-w.HIGH_Z.record()['divider_power_at_3v3_mw']
        self.assertGreater(extra,.13);self.assertLess(extra,.14)
    def test_unpowered_qualifications_frozen(self):
        d=w.evidence()
        self.assertIs(d['safe_to_energize'],False)
        self.assertIs(d['hardware_tested'],False)
        self.assertIs(d['input_leakage_stress_is_TEXAS_INSTRUMENTS_SPEC'],False)
    def test_deterministic_serialization(self):
        self.assertEqual(json.dumps(w.evidence(),sort_keys=True),json.dumps(w.evidence(),sort_keys=True))


if __name__=='__main__':unittest.main()
