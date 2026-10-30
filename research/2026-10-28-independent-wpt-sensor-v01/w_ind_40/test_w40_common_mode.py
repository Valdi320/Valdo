"""Pure-software adversarial tests: NOT a physical safety validation."""
import json
import unittest
from itertools import combinations
import w40_common_mode as w


class CommonModeSafetyTests(unittest.TestCase):
    def test_nofault_overcurrent_always_asks_off(self):
        for arch in w.ARCHITECTURES:
            with self.subTest(arch=arch.name):
                x = w.evaluate(arch)
                self.assertFalse(x["requested_on"])
                self.assertFalse(x["unsafe_overcurrent_path"])

    def test_shared_shunt_is_single_cutset_in_all_designs(self):
        for arch in w.ARCHITECTURES:
            self.assertTrue(w.evaluate(arch, {"shared_shunt_bypassed"})["unsafe_overcurrent_path"])

    def test_existing_w39_shared_rail_is_single_critical_fault(self):
        self.assertTrue(w.evaluate(w.W39, {"shared_3v3_lost"})["unsafe_overcurrent_path"])

    def test_third_shared_ina_does_not_rescue_rail(self):
        self.assertTrue(w.evaluate(w.THIRD, {"shared_3v3_lost"})["unsafe_overcurrent_path"])
        self.assertTrue(w.evaluate(w.THIRD, {"shared_shunt_bypassed"})["unsafe_overcurrent_path"])

    def test_independent_pg_rejects_3v3_loss_in_ideal_model(self):
        x = w.evaluate(w.PG_INDEPENDENT, {"shared_3v3_lost"})
        self.assertTrue(x["separate_pg_trip_assumed"])
        self.assertFalse(x["unsafe_overcurrent_path"])

    def test_pg_on_same_lost_rail_does_not_get_credit(self):
        x = w.evaluate(w.PG_SHARED, {"shared_3v3_lost"})
        self.assertFalse(x["separate_pg_trip_assumed"])
        self.assertTrue(x["unsafe_overcurrent_path"])

    def test_independent_pg_stuck_needs_rail_fault(self):
        self.assertFalse(w.evaluate(w.PG_INDEPENDENT, {"rail_pg_stuck_healthy"})["unsafe_overcurrent_path"])
        self.assertTrue(w.evaluate(w.PG_INDEPENDENT,
            {"shared_3v3_lost", "rail_pg_stuck_healthy"})["unsafe_overcurrent_path"])

    def test_single_monitor_or_wire_fault_is_not_single_cutset(self):
        for f in ("ina_a_silent", "ina_b_silent", "alert_a_open", "alert_b_open",
                  "reset_a_open", "reset_b_open"):
            with self.subTest(fault=f):
                self.assertFalse(w.evaluate(w.W39, {f})["unsafe_overcurrent_path"])

    def test_two_independent_path_faults_defeat_w39(self):
        for a in ("ina_a_silent", "alert_a_open", "reset_a_open"):
            for b in ("ina_b_silent", "alert_b_open", "reset_b_open"):
                with self.subTest(faults=(a,b)):
                    self.assertTrue(w.evaluate(w.W39, {a,b})["unsafe_overcurrent_path"])

    def test_single_weld_is_contained_but_both_welds_are_not(self):
        for a in w.ARCHITECTURES:
            self.assertFalse(w.evaluate(a, {"cut_a_welded"})["unsafe_overcurrent_path"])
            self.assertFalse(w.evaluate(a, {"cut_b_welded"})["unsafe_overcurrent_path"])
            self.assertTrue(w.evaluate(a, {"cut_a_welded", "cut_b_welded"})["unsafe_overcurrent_path"])

    def test_minimality_and_bounded_exhaustiveness(self):
        for a in w.ARCHITECTURES:
            cuts = w.minimal_cutsets(a, 2)
            for cs in cuts:
                self.assertTrue(w.evaluate(a, cs)["unsafe_overcurrent_path"])
                for x in cs:
                    self.assertFalse(w.evaluate(a, cs-{x})["unsafe_overcurrent_path"])
            for order in (1,2):
                for bits in combinations(w.FAULTS,order):
                    fs=frozenset(bits)
                    # PG can make the hazard NONMONOTONE: adding a rail-loss
                    # fault can actively trip an independently powered PG.
                    # A safe superset of an unsafe cutset is thus possible.
                    if w.evaluate(a,fs)["unsafe_overcurrent_path"]:
                        self.assertTrue(any(c <= fs for c in cuts))

    def test_nonmonotone_pg_is_not_mislabeled_as_fault_probability(self):
        baseline = w.evaluate(w.PG_INDEPENDENT, {"shared_shunt_bypassed"})
        both = w.evaluate(w.PG_INDEPENDENT, {"shared_shunt_bypassed", "shared_3v3_lost"})
        self.assertTrue(baseline["unsafe_overcurrent_path"])
        self.assertFalse(both["unsafe_overcurrent_path"])
        self.assertTrue(both["separate_pg_trip_assumed"])

    def test_model_expected_single_cutsets(self):
        self.assertEqual({next(iter(s)) for s in w.minimal_cutsets(w.W39) if len(s)==1},
                         {"shared_shunt_bypassed", "shared_3v3_lost"})
        self.assertEqual({next(iter(s)) for s in w.minimal_cutsets(w.PG_INDEPENDENT) if len(s)==1},
                         {"shared_shunt_bypassed"})

    def test_input_rejects_unknown_faults_and_invalid_orders(self):
        with self.assertRaises(ValueError):
            w.evaluate(w.W39,{"alien_fault"})
        for order in (0, len(w.FAULTS)+1):
            with self.assertRaises(ValueError):
                w.minimal_cutsets(w.W39,order)

    def test_report_is_deterministic_and_not_hardware_pass(self):
        r1,r2=w.report(),w.report()
        self.assertEqual(json.dumps(r1, sort_keys=True), json.dumps(r2, sort_keys=True))
        self.assertFalse(r1["safe_to_energize"])
        self.assertFalse(r1["hardware_qualified"])
        self.assertEqual(r1["physical_measurements"],0)
        self.assertFalse(r1["existing_W39_independent_3v3_pg_proven"])

    def test_exhaustive_fault_space_within_order_2_is_stable(self):
        self.assertEqual(len(w.FAULTS),14)
        self.assertEqual(1+len(w.FAULTS)+len(tuple(combinations(w.FAULTS,2))),106)
        self.assertGreater(len(w.minimal_cutsets(w.W39)),len(w.minimal_cutsets(w.THIRD)))

    def test_no_radio_or_lithium_or_motor_dependency(self):
        for a in w.ARCHITECTURES:
            self.assertFalse(any("radio" in s or "battery" in s for s in w.FAULTS))
            self.assertFalse(w.evaluate(a)["unsafe_overcurrent_path"])


if __name__ == "__main__":
    unittest.main()
