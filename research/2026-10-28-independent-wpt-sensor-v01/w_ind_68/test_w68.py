"""W68: original synthetic regression and injected failures; NOT physical tests."""
from dataclasses import replace
from math import exp
import unittest
from tx_cut_power_screen import Interlocks, Switch, Fault, evaluate
from w_ind_68.w68_residual import ResidualCase, screen


def sample(**kw):
    return replace(ResidualCase(Interlocks(), Switch(), Switch(),
        physical_source_present=False, reverse_feed_excluded=True,
        initial_downstream_v=5.0, downstream_c_f=100e-6,
        independent_bleeder_ohm=1000.0), **kw)


class ResidualEnergyGate(unittest.TestCase):
    def test_w67_false_no_forward_is_not_safe_when_cap_is_charged(self):
        old = evaluate(Interlocks(), Switch(Fault.CLOSED), Switch(Fault.CLOSED),
                       supply_present=False)
        self.assertFalse(old.supply_to_tx)
        v = screen(sample(switch_a=Switch(Fault.CLOSED), switch_b=Switch(Fault.CLOSED)))
        self.assertEqual(v.classification, "RESIDUAL_ABOVE_HYPOTHETICAL_SCREEN")
        self.assertFalse(v.possible_forward_dc)
        self.assertFalse(v.hardware_approved)

    def test_forward_supply_overrides_declared_empty_cap(self):
        v = screen(sample(physical_source_present=True,
            switch_a=Switch(Fault.CLOSED), switch_b=Switch(Fault.CLOSED),
            initial_downstream_v=0.0))
        self.assertTrue(v.possible_forward_dc)
        self.assertEqual(v.classification, "FORWARD_SUPPLY_POSSIBLE")

    def test_monitor_permission_cannot_erase_double_weld(self):
        v = screen(sample(physical_source_present=True,
            switch_a=Switch(Fault.CLOSED), switch_b=Switch(Fault.CLOSED)))
        self.assertEqual(v.classification, "FORWARD_SUPPLY_POSSIBLE")

    def test_backfeed_unknown_dominates_rc_prediction(self):
        for proof in (None, False):
            with self.subTest(proof=proof):
                v = screen(sample(reverse_feed_excluded=proof, elapsed_s=100))
                self.assertEqual(v.classification, "BACKFEED_NOT_EXCLUDED")
                self.assertIsNone(v.voltage_at_t_v)

    def test_missing_cap_bleeder_or_initial_voltage_cannot_prove_empty(self):
        for key in ("initial_downstream_v", "downstream_c_f",
                    "independent_bleeder_ohm"):
            with self.subTest(key=key):
                v = screen(sample(**{key: None}))
                self.assertEqual(v.classification, "STORAGE_OR_BLEED_UNKNOWN")

    def test_exact_rc_decay_and_energy(self):
        v = screen(sample(elapsed_s=0.1))
        self.assertAlmostEqual(v.voltage_at_t_v, 5.0 * exp(-1), 12)
        self.assertAlmostEqual(v.initial_j, 0.00125, 12)
        self.assertAlmostEqual(v.residual_j, 0.00125 * exp(-2), 12)
        self.assertAlmostEqual(v.initial_bleeder_w, 0.025, 12)

    def test_late_rc_below_hypothetical_is_not_physical_safety(self):
        v = screen(sample(elapsed_s=0.5))
        self.assertEqual(v.classification, "BELOW_HYPOTHETICAL_SCREEN_NOT_SAFE")
        self.assertFalse(v.hardware_approved)

    def test_stricter_screen_does_not_qualify_hardware(self):
        for thr in (0.001, 0.05, 0.5, 5.0):
            with self.subTest(threshold=thr):
                v = screen(sample(screening_voltage_v=thr))
                self.assertFalse(v.hardware_approved)

    def test_ideal_bleeder_assumption_cannot_be_inferred(self):
        self.assertEqual(screen(sample(independent_bleeder_ohm=None)).classification,
                         "STORAGE_OR_BLEED_UNKNOWN")

    def test_energy_is_monotone_and_nonnegative_in_hypothetical_rc(self):
        for c in (1e-6, 100e-6, 1e-3, 0.01):
            previous = float("inf")
            for t in (0, 0.001, 0.01, 0.1, 1, 10):
                v = screen(sample(downstream_c_f=c, elapsed_s=t))
                self.assertGreaterEqual(v.residual_j, 0)
                self.assertLessEqual(v.residual_j, previous + 1e-15)
                previous = v.residual_j

    def test_zero_initial_voltage_still_no_approval(self):
        v = screen(sample(initial_downstream_v=0))
        self.assertEqual(v.voltage_at_t_v, 0)
        self.assertFalse(v.hardware_approved)

    def test_stored_energy_does_not_falsify_forward_sourcing(self):
        out = screen(sample(physical_source_present=True,
            switch_a=Switch(), switch_b=Switch()))
        self.assertFalse(out.possible_forward_dc)
        self.assertEqual(out.classification, "RESIDUAL_ABOVE_HYPOTHETICAL_SCREEN")

    def test_non_boolean_safety_inputs_rejected(self):
        for val in (0, 1, "false", None, []):
            with self.subTest(value=val):
                with self.assertRaises(ValueError):
                    screen(sample(physical_source_present=val))
        for val in (0, 1, "true", []):
            with self.subTest(reverse=val):
                with self.assertRaises(ValueError):
                    screen(sample(reverse_feed_excluded=val))

    def test_nonfinite_and_out_of_envelope_rejected(self):
        for field, values in {
            "elapsed_s": (-1, 86401, float("nan"), True),
            "initial_downstream_v": (-1, 6, float("inf"), "5"),
            "downstream_c_f": (0, 0.11, float("nan"), False),
            "independent_bleeder_ohm": (0, 1e8, float("inf"), "1000"),
            "screening_voltage_v": (0, 6, float("nan")),
            "screening_energy_j": (0, float("inf"), -1),
        }.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    with self.assertRaises(ValueError):
                        screen(sample(**{field: value}))

    def test_missing_wrong_dataclass_and_switch_are_rejected(self):
        with self.assertRaises(TypeError): screen({})
        with self.assertRaises(TypeError): screen(sample(switch_a=None))

    def test_all_scenarios_have_synthetic_provenance(self):
        scenarios = (sample(), sample(elapsed_s=20),
                     sample(reverse_feed_excluded=None),
                     sample(physical_source_present=True,
                        switch_a=Switch(Fault.CLOSED), switch_b=Switch(Fault.CLOSED)))
        for s in scenarios:
            v = screen(s)
            self.assertEqual(v.evidence_type, "SYNTHETIC_RC_TOPOLOGY_ONLY")
            self.assertFalse(v.hardware_approved)


if __name__ == "__main__":
    unittest.main()
