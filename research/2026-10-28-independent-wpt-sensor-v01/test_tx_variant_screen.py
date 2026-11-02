"""Offline deterministic tests for W-IND-09's variant-specific safety gates."""
from dataclasses import replace
import math
import unittest
from tx_variant_screen import (
    VARIANTS, Variant, screen_sensor_rail, hypothetical_qod_weld,
    typical_on_loss, validate_variant,
)


class VariantScreenTests(unittest.TestCase):
    def test_variant_identity_not_family_name(self):
        self.assertEqual(set(VARIANTS), {"TPS22950", "TPS22950L", "TPS22950C", "TPS22918"})

    def test_22950_has_rcb_but_not_latch(self):
        v = VARIANTS["TPS22950"]
        self.assertTrue(v.rcb)
        self.assertEqual(v.overcurrent_response, "auto_retry")
        self.assertAlmostEqual(v.ilim_min_typ, .05)

    def test_22950l_latches_but_no_rcb(self):
        v = VARIANTS["TPS22950L"]
        self.assertFalse(v.rcb)
        self.assertEqual(v.overcurrent_response, "latch_off")
        self.assertAlmostEqual(v.ilim_min_typ, .5)

    def test_22950c_has_half_amp_min(self):
        self.assertAlmostEqual(VARIANTS["TPS22950C"].ilim_min_typ, .5)

    def test_all_unapproved(self):
        for name, v in VARIANTS.items():
            with self.subTest(name=name):
                r = screen_sensor_rail(v)
                self.assertFalse(r["hardware_approved"])
                self.assertFalse(r["real_fod_verified"])
                self.assertFalse(r["independent_cutoff_verified"])
                self.assertTrue(r["blockers"])

    def test_22950_retries_and_reverse_threshold_above_target(self):
        r = screen_sensor_rail(VARIANTS["TPS22950"])
        self.assertIn("fault_retries_without_independent_latch", r["blockers"])
        self.assertIn("reverse_trip_typically_above_sensor_limit", r["blockers"])

    def test_l_not_substitute_for_nominal_0_4_a(self):
        r = screen_sensor_rail(VARIANTS["TPS22950L"])
        self.assertIn("target_below_or_above_typical_limit_range", r["blockers"])
        self.assertIn("no_reverse_current_blocking", r["blockers"])
        self.assertNotIn("fault_retries_without_independent_latch", r["blockers"])

    def test_c_not_substitute_for_nominal_0_4_a(self):
        self.assertIn("target_below_or_above_typical_limit_range",
                      screen_sensor_rail(VARIANTS["TPS22950C"])["blockers"])

    def test_22918_not_current_limiter_or_rcb(self):
        blockers = screen_sensor_rail(VARIANTS["TPS22918"])["blockers"]
        self.assertIn("adjustable_current_limit_absent", blockers)
        self.assertIn("no_reverse_current_blocking", blockers)

    def test_fixed_qod_adds_unresolved_hazard(self):
        for name in ("TPS22950", "TPS22950L", "TPS22950C"):
            self.assertIn("fixed_qod_short_fault_path_unresolved",
                          screen_sensor_rail(VARIANTS[name])["blockers"])

    def test_configurable_qod_unconnected_model_does_not_claim_safety(self):
        self.assertFalse(hypothetical_qod_weld(VARIANTS["TPS22918"], 5, True, False)["fault_scenario"])
        self.assertFalse(screen_sensor_rail(VARIANTS["TPS22918"])["hardware_approved"])

    def test_qod_weld_150ohm_5v_hypothetical(self):
        out = hypothetical_qod_weld(VARIANTS["TPS22950"], 5, True, False)
        self.assertAlmostEqual(out["potential_shunt_a"], 1 / 30)
        self.assertAlmostEqual(out["potential_shunt_w"], 1 / 6)

    def test_no_weld_or_on_no_modelled_qod_shunt(self):
        v = VARIANTS["TPS22950"]
        self.assertEqual(hypothetical_qod_weld(v, 5, False, False)["potential_shunt_w"], 0)
        self.assertEqual(hypothetical_qod_weld(v, 5, True, True)["potential_shunt_w"], 0)

    def test_typical_on_loss(self):
        self.assertAlmostEqual(typical_on_loss(VARIANTS["TPS22950"], .4), .00544)
        self.assertAlmostEqual(typical_on_loss(VARIANTS["TPS22918"], .4), .00832)

    def test_voltage_bounds_rejected(self):
        for value in (.1, 12, 100):
            self.assertIn("supply_outside_rated_range",
                          screen_sensor_rail(VARIANTS["TPS22950"], value)["blockers"])

    def test_invalid_target_not_silently_accepted(self):
        for value in (0, -1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                screen_sensor_rail(VARIANTS["TPS22950"], nominal_limit_a=value)

    def test_invalid_voltage_not_silently_accepted(self):
        for value in (0, -1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                screen_sensor_rail(VARIANTS["TPS22950"], supply_v=value)

    def test_invalid_datasheet_entries_not_silently_accepted(self):
        source = VARIANTS["TPS22950"]
        edits = ({"ilim_min_typ": -1}, {"ilim_max_typ": .01}, {"reverse_trip_typ": math.nan},
                 {"qod_ohm_typ": 0}, {"vin_max": 1}, {"source": "nothttps"},
                 {"overcurrent_response": "magic"}, {"ron_ohm_typ_at_5v": float("inf")},
                 {"ilim_min_typ": None})
        for edit in edits:
            with self.subTest(edit=edit), self.assertRaises(ValueError):
                validate_variant(replace(source, **edit))

    def test_nonfinite_qod_test_rejected(self):
        for x in (-1, math.nan, math.inf):
            with self.assertRaises(ValueError):
                hypothetical_qod_weld(VARIANTS["TPS22950"], x, True, False)

    def test_nonfinite_current_rejected(self):
        for x in (-1, math.nan, math.inf, 2.1):
            with self.assertRaises(ValueError):
                typical_on_loss(VARIANTS["TPS22950"], x)

    def test_rcb_typical_is_not_guaranteed(self):
        r = screen_sensor_rail(VARIANTS["TPS22950"])
        self.assertTrue(r["reverse_trip_value_is_typical_not_guaranteed"])


if __name__ == "__main__":
    unittest.main()
