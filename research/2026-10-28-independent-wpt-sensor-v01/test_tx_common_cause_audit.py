"""Deterministic tests of one synthetic fault-tree, not electrical safety."""
import itertools
import unittest
from tx_common_cause_audit import (Failure as F, Hypothesis, Wiring,
                                   available_failures, off_state_tx_paths,
                                   minimal_energizing_fault_sets, screen,
                                   demonstration)


def sets(h):
    return set(minimal_energizing_fault_sets(h))


class TestTxCommonCause(unittest.TestCase):
    def test_normal_off_no_path_in_model(self):
        for wiring in Wiring:
            self.assertEqual(off_state_tx_paths(Hypothesis(wiring), frozenset()), ())

    def test_shared_enable_has_single_fault(self):
        h = Hypothesis(Wiring.SHARED_ENABLE, model_board_bridge=False)
        self.assertEqual(sets(h), {frozenset([F.SHARED_DRIVER_HIGH]),
                                   frozenset([F.WELD_A, F.WELD_B])})

    def test_independent_enables_need_two_control_or_weld_faults(self):
        h = Hypothesis(Wiring.SEPARATE_ENABLE, model_board_bridge=False)
        self.assertEqual(sets(h), {frozenset([a, b]) for a in (F.WELD_A, F.A_ENABLE_HIGH)
                                   for b in (F.WELD_B, F.B_ENABLE_HIGH)})

    def test_common_latch_defeats_separate_pins(self):
        h = Hypothesis(Wiring.SEPARATE_WITH_COMMON_LATCH, model_board_bridge=False)
        self.assertIn(frozenset([F.COMMON_LATCH_HIGH]), sets(h))
        self.assertEqual(len(sets(h)), 5)

    def test_board_bridge_defeats_both_open_cuts(self):
        for wiring in Wiring:
            h = Hypothesis(wiring)
            self.assertIn(frozenset([F.BOARD_VIN_TX_BRIDGE]), sets(h))
            self.assertIn("VIN->BOARD_BRIDGE->TX", off_state_tx_paths(h, frozenset([F.BOARD_VIN_TX_BRIDGE])))

    def test_aux_present_adds_single_fault_bypass(self):
        h = Hypothesis(Wiring.SEPARATE_ENABLE, aux_present=True)
        self.assertIn(frozenset([F.AUX_TX_BRIDGE]), sets(h))

    def test_aux_absent_cannot_energize(self):
        h = Hypothesis(Wiring.SEPARATE_ENABLE, aux_present=False)
        self.assertNotIn(F.AUX_TX_BRIDGE, available_failures(h))

    def test_disabled_bridge_is_restricted_model_only(self):
        h = Hypothesis(Wiring.SEPARATE_ENABLE, model_board_bridge=False)
        self.assertNotIn(F.BOARD_VIN_TX_BRIDGE, available_failures(h))
        self.assertFalse(screen(h).hardware_approved)
        self.assertFalse(screen(h).model_covers_all_real_paths)

    def test_vin_absent_and_aux_absent_no_source(self):
        h = Hypothesis(Wiring.SHARED_ENABLE, vin_present=False, aux_present=False)
        self.assertEqual(sets(h), set())

    def test_vin_absent_aux_may_still_supply(self):
        h = Hypothesis(Wiring.SEPARATE_ENABLE, vin_present=False, aux_present=True)
        self.assertEqual(sets(h), {frozenset([F.AUX_TX_BRIDGE])})

    def test_unknown_fault_is_rejected(self):
        h = Hypothesis(Wiring.SHARED_ENABLE)
        with self.assertRaises(ValueError):
            off_state_tx_paths(h, frozenset([F.A_ENABLE_HIGH]))

    def test_non_enum_and_non_frozenset_rejected(self):
        h = Hypothesis(Wiring.SHARED_ENABLE)
        for faults in (set(), frozenset(["weld_a"]), frozenset([1])):
            with self.subTest(faults=faults), self.assertRaises(ValueError):
                off_state_tx_paths(h, faults)

    def test_invalid_hypotheses_rejected(self):
        for field, bad in (("wiring", "shared_enable"), ("vin_present", 1),
                           ("aux_present", None), ("model_board_bridge", "no"),
                           ("model_aux_bridge", 0)):
            with self.subTest(field=field), self.assertRaises(ValueError):
                Hypothesis(**{**{"wiring": Wiring.SHARED_ENABLE}, field: bad})

    def test_invalid_fault_bound_rejected(self):
        h = Hypothesis(Wiring.SHARED_ENABLE)
        for n in (-1, 6, True, 1.5):
            with self.subTest(n=n), self.assertRaises(ValueError):
                minimal_energizing_fault_sets(h, n)

    def test_limiting_depth_does_not_fabricate_faults(self):
        h = Hypothesis(Wiring.SEPARATE_ENABLE, model_board_bridge=False)
        self.assertEqual(minimal_energizing_fault_sets(h, 1), ())
        self.assertEqual(len(minimal_energizing_fault_sets(h, 2)), 4)

    def test_minimal_sets_are_not_supersets(self):
        for wiring, aux in itertools.product(Wiring, (False, True)):
            ss = minimal_energizing_fault_sets(Hypothesis(wiring, aux_present=aux))
            for a, b in itertools.permutations(ss, 2):
                self.assertFalse(a.issubset(b))

    def test_monotone_energization_for_added_faults(self):
        for wiring, aux in itertools.product(Wiring, (False, True)):
            h = Hypothesis(wiring, aux_present=aux)
            catalog = available_failures(h)
            all_sets = [frozenset(f for i, f in enumerate(catalog) if mask & (1 << i))
                        for mask in range(1 << len(catalog))]
            for fs in all_sets:
                if off_state_tx_paths(h, fs):
                    for f in catalog:
                        if f not in fs:
                            self.assertTrue(off_state_tx_paths(h, fs | frozenset([f])))

    def test_screen_never_approves_hardware(self):
        for wiring, aux, board in itertools.product(Wiring, (False, True), (False, True)):
            r = screen(Hypothesis(wiring, aux_present=aux, model_board_bridge=board))
            self.assertFalse(r.hardware_approved)
            self.assertFalse(r.model_covers_all_real_paths)
            self.assertEqual(r.single_fault_paths, tuple(fs for fs in r.minimal_sets if len(fs) == 1))

    def test_stable_demo_no_claim_of_safety(self):
        s = demonstration()
        self.assertIn("shared_driver_high", s)
        self.assertIn("common_latch_high", s)
        self.assertIn("HARDWARE_APPROVED=False", s)


if __name__ == "__main__":
    unittest.main()
