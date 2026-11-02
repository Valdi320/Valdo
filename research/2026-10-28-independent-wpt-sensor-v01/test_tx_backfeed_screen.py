"""W-IND-12 deterministic fault-injection tests. No external dependencies."""
import itertools
import unittest

from tx_backfeed_screen import Case, Fault, PathState, demo, review


class TestPowerPathTopology(unittest.TestCase):
    def test_default_forward_off(self):
        r = review(Case())
        self.assertEqual(r.primary_to_tx.state, PathState.NO_PATH_IN_MODEL)
        self.assertFalse(r.off_path_requires_investigation)
        self.assertFalse(r.hardware_approved)

    def test_all_one_faults_isolated_from_primary(self):
        for a, b in [(Fault.STUCK_CONDUCTING, Fault.NORMAL),
                     (Fault.NORMAL, Fault.STUCK_CONDUCTING),
                     (Fault.STUCK_OPEN, Fault.NORMAL),
                     (Fault.NORMAL, Fault.STUCK_OPEN)]:
            with self.subTest(a=a, b=b):
                self.assertEqual(review(Case(cut_a=a, cut_b=b)).primary_to_tx.state,
                                 PathState.NO_PATH_IN_MODEL)

    def test_double_weld_defeats_forward_cutoff(self):
        r = review(Case(cut_a=Fault.STUCK_CONDUCTING, cut_b=Fault.STUCK_CONDUCTING))
        self.assertEqual(r.primary_to_tx.state, PathState.CONFIRMED_IN_MODEL)
        self.assertEqual(r.primary_to_tx.path, ("cut_A_forward", "cut_B_forward"))
        self.assertTrue(r.off_path_requires_investigation)

    def test_one_weld_energizes_intermediate_node_only(self):
        r = review(Case(cut_a=Fault.STUCK_CONDUCTING))
        self.assertEqual(r.primary_to_mid.state, PathState.CONFIRMED_IN_MODEL)
        self.assertEqual(r.primary_to_tx.state, PathState.NO_PATH_IN_MODEL)

    def test_secondary_weld_neither_mid_nor_tx_from_vin(self):
        r = review(Case(cut_b=Fault.STUCK_CONDUCTING))
        self.assertEqual(r.primary_to_mid.state, PathState.NO_PATH_IN_MODEL)
        self.assertEqual(r.primary_to_tx.state, PathState.NO_PATH_IN_MODEL)

    def test_requested_on_is_expected_path_but_not_approved(self):
        r = review(Case(commanded_on=True))
        self.assertEqual(r.primary_to_tx.state, PathState.CONFIRMED_IN_MODEL)
        self.assertFalse(r.hardware_approved)
        self.assertFalse(r.off_path_requires_investigation)

    def test_failed_open_cut_stops_forward_even_if_on(self):
        for f in (Fault.STUCK_OPEN,):
            for position in ("cut_a", "cut_b"):
                with self.subTest(position=position):
                    kwargs = {position: f}
                    r = review(Case(commanded_on=True, **kwargs))
                    self.assertEqual(r.primary_to_tx.state, PathState.NO_PATH_IN_MODEL)

    def test_auxiliary_verified_conducting_bypass_defeats_both_off(self):
        r = review(Case(aux_present=True, aux_to_tx_conducts=True))
        self.assertEqual(r.aux_to_tx.state, PathState.CONFIRMED_IN_MODEL)
        self.assertEqual(r.aux_to_tx.path, ("auxiliary_bypass",))
        self.assertTrue(r.off_path_requires_investigation)

    def test_aux_unknown_must_not_be_assumed_blocked(self):
        r = review(Case(aux_present=True))
        self.assertEqual(r.aux_to_tx.state, PathState.POSSIBLE_UNVERIFIED)
        self.assertTrue(r.off_path_requires_investigation)

    def test_aux_proven_isolated_is_no_path_in_model(self):
        r = review(Case(aux_present=True, aux_to_tx_conducts=False))
        self.assertEqual(r.aux_to_tx.state, PathState.NO_PATH_IN_MODEL)
        self.assertFalse(r.off_path_requires_investigation)

    def test_aux_with_no_source_has_no_path(self):
        r = review(Case(aux_present=False, aux_to_tx_conducts=True))
        self.assertEqual(r.aux_to_tx.state, PathState.NO_PATH_IN_MODEL)

    def test_unknown_reverse_blocking_flags_external_backfeed(self):
        r = review(Case(external_tx_present=True, tx_to_logic_conducts=False))
        self.assertEqual(r.external_tx_to_primary.state, PathState.POSSIBLE_UNVERIFIED)
        self.assertEqual(r.external_tx_to_primary.path,
                         ("external_injection", "cut_B_reverse", "cut_A_reverse"))
        self.assertTrue(r.off_path_requires_investigation)

    def test_both_reverse_conducting_definite_backfeed(self):
        r = review(Case(external_tx_present=True, a_reverse_blocked=False,
                        b_reverse_blocked=False, tx_to_logic_conducts=False))
        self.assertEqual(r.external_tx_to_primary.state, PathState.CONFIRMED_IN_MODEL)

    def test_either_proven_reverse_block_breaks_return(self):
        for a, b in ((True, None), (None, True), (True, False), (False, True)):
            with self.subTest(a=a, b=b):
                r = review(Case(external_tx_present=True, a_reverse_blocked=a,
                                b_reverse_blocked=b, tx_to_logic_conducts=False))
                self.assertEqual(r.external_tx_to_primary.state, PathState.NO_PATH_IN_MODEL)

    def test_gpio_esd_backfeed_has_independent_path(self):
        r = review(Case(external_tx_present=True, a_reverse_blocked=True,
                        b_reverse_blocked=True, tx_to_logic_conducts=True))
        self.assertEqual(r.external_tx_to_primary.state, PathState.NO_PATH_IN_MODEL)
        self.assertEqual(r.external_tx_to_logic.state, PathState.CONFIRMED_IN_MODEL)
        self.assertTrue(r.off_path_requires_investigation)

    def test_unknown_gpio_path_is_not_assumed_safe(self):
        r = review(Case(external_tx_present=True, a_reverse_blocked=True,
                        b_reverse_blocked=True))
        self.assertEqual(r.external_tx_to_logic.state, PathState.POSSIBLE_UNVERIFIED)

    def test_external_supply_absent_makes_reverse_hazard_inactive(self):
        r = review(Case(external_tx_present=False, a_reverse_blocked=False,
                        b_reverse_blocked=False, tx_to_logic_conducts=True))
        self.assertEqual(r.external_tx_to_primary.state, PathState.NO_PATH_IN_MODEL)
        self.assertEqual(r.external_tx_to_logic.state, PathState.NO_PATH_IN_MODEL)

    def test_double_weld_allows_backfeed_even_if_nominally_reverse_blocked(self):
        r = review(Case(external_tx_present=True, cut_a=Fault.STUCK_CONDUCTING,
                        cut_b=Fault.STUCK_CONDUCTING, a_reverse_blocked=True,
                        b_reverse_blocked=True, tx_to_logic_conducts=False))
        self.assertEqual(r.external_tx_to_primary.state, PathState.CONFIRMED_IN_MODEL)

    def test_failed_open_suppresses_reverse_even_if_not_reverse_blocking(self):
        r = review(Case(external_tx_present=True, cut_b=Fault.STUCK_OPEN,
                        a_reverse_blocked=False, b_reverse_blocked=False,
                        tx_to_logic_conducts=False))
        self.assertEqual(r.external_tx_to_primary.state, PathState.NO_PATH_IN_MODEL)

    def test_primary_absent_prevents_primary_injection(self):
        r = review(Case(primary_present=False, commanded_on=True))
        self.assertEqual(r.primary_to_tx.state, PathState.NO_PATH_IN_MODEL)

    def test_every_fault_combination_never_approves_hardware(self):
        for a, b in itertools.product(Fault, repeat=2):
            for aux in (False, True):
                for external in (False, True):
                    r = review(Case(cut_a=a, cut_b=b, aux_present=aux,
                                    external_tx_present=external))
                    self.assertFalse(r.hardware_approved)

    def test_no_boolean_integer_coercion(self):
        for kwargs in ({"commanded_on": 1}, {"primary_present": 0},
                       {"aux_present": "no"}, {"a_reverse_blocked": 1},
                       {"b_reverse_blocked": "true"},
                       {"aux_to_tx_conducts": 0}, {"tx_to_logic_conducts": "maybe"},
                       {"cut_a": "normal"}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    Case(**kwargs)

    def test_demo_determinism(self):
        out = demo()
        self.assertEqual(out["both_off_no_aux"], "NO_PATH_ASSUMED_NOT_APPROVED")
        self.assertEqual(out["one_welded"], "NO_PATH_ASSUMED_NOT_APPROVED")
        self.assertEqual(out["both_welded"], "HALT_REVIEW")
        self.assertEqual(out["unknown_debug_bypass"], "HALT_REVIEW")
        self.assertEqual(out["external_reverse_unknown"], "HALT_REVIEW")


if __name__ == "__main__":
    unittest.main()
