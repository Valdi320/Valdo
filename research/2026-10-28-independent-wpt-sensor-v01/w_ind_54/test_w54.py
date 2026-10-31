"""Original synthetic W54 adversarial cases; no measurement/hardware."""
import unittest
from dataclasses import replace
from decimal import Decimal
from w54_crossed_meter import Run, evaluate, demo


def pair():
    base = dict(bound_in_mw="2", bound_out_mw="2",
                temperature_c="25", gap_mm="2", lateral_offset_mm="0",
                load_ohm="20", fixture_id="FICTITIOUS-1")
    a = Run("a", "A", "B", "1100", "720", start_ms=0, end_ms=100,
            trace_id="trace-a", **base)
    b = Run("b", "B", "A", "900", "880", start_ms=200, end_ms=300,
            trace_id="trace-b", **base)
    return a, b


class CrossedMeterTests(unittest.TestCase):
    def test_ideal_gain_cancels(self):
        r = evaluate(*pair())
        self.assertEqual(Decimal(r["eta_cross_percent"]), Decimal("80"))
        self.assertLess(Decimal(r["eta_ab_percent"]), Decimal("70"))
        self.assertGreater(Decimal(r["eta_ba_percent"]), Decimal("90"))
        self.assertFalse(r["candidate_for_metrology_review"])
        self.assertFalse(r["hardware_approved"])

    def test_uncertainty_interval_contains_nominal(self):
        r = evaluate(*pair())
        lo, hi = map(Decimal, r["conditional_interval_percent"])
        self.assertLess(lo, 80)
        self.assertGreater(hi, 80)

    def test_zero_offset_interval_exact(self):
        a, b = pair()
        a = replace(a, bound_in_mw="0", bound_out_mw="0")
        b = replace(b, bound_in_mw="0", bound_out_mw="0")
        r = evaluate(a, b)
        self.assertEqual([Decimal(x) for x in r["conditional_interval_percent"]], [Decimal(80), Decimal(80)])

    def test_mismatch_gain_breaks_invariance(self):
        a, b = pair()
        b = replace(b, pin_mw="920")
        r = evaluate(a, b)
        self.assertNotEqual(Decimal(r["eta_cross_percent"]), 80)
        self.assertFalse(r["hardware_approved"])

    def test_different_true_efficiencies_geometric_not_one_run(self):
        a, b = pair()
        b = replace(b, pout_mw="792")
        r = evaluate(a, b)
        self.assertAlmostEqual(float(r["eta_cross_percent"]), (0.8 * 0.72) ** 0.5 * 100)
        self.assertFalse(r["hardware_approved"])

    def test_invalid_identity_roles(self):
        a, b = pair()
        bad = (replace(b, meter_in="A"),
               replace(a, meter_out="A"),
               replace(b, trace_id=a.trace_id),
               replace(b, run_id=a.run_id),
               replace(b, fixture_id="other"))
        for x in bad:
            with self.subTest(bad=x):
                with self.assertRaises(ValueError):
                    evaluate(a, x)

    def test_replayed_time(self):
        a, b = pair()
        for x in (replace(b, start_ms=90), replace(b, end_ms=90),
                  replace(b, start_ms=-1), replace(b, start_ms=100, end_ms=100)):
            with self.subTest(x=x):
                with self.assertRaises(ValueError):
                    evaluate(a, x)

    def test_bad_power_and_uncertainty(self):
        a, b = pair()
        for x in (replace(a, pin_mw="0"), replace(a, pout_mw="-5"),
                  replace(a, bound_in_mw="-1"), replace(a, bound_in_mw="9999"),
                  replace(a, pout_mw="1100"), replace(a, pin_mw="nan"),
                  replace(a, pin_mw="inf"), replace(a, pin_mw="not_a_number")):
            with self.subTest(x=x):
                with self.assertRaises(ValueError):
                    evaluate(x, b)

    def test_conditions_fail_closed(self):
        a, b = pair()
        flags = dict(source_kind="BENCH_MEASURED",
                     independently_verified_conditions=True,
                     gain_stability_verified=True,
                     offsets_traceable=True,
                     instrument_and_clock_verified=True)
        a, b = replace(a, **flags), replace(b, **flags)
        self.assertTrue(evaluate(a, b)["candidate_for_metrology_review"])
        changes = (("temperature_c", "27", "temperature_delta_c"),
                   ("gap_mm", "2.2", "gap_delta_mm"),
                   ("lateral_offset_mm", "0.3", "lateral_offset_delta_mm"),
                   ("load_ohm", "20.2", "load_difference_percent"))
        for name, value, key in changes:
            with self.subTest(name=name):
                r = evaluate(a, replace(b, **{name: value}))
                self.assertFalse(r["candidate_for_metrology_review"])
                self.assertTrue(any(key in x for x in r["blockers"]))

    def test_source_and_flags_required(self):
        a, b = pair()
        flags = dict(source_kind="BENCH_MEASURED",
                     independently_verified_conditions=True,
                     gain_stability_verified=True,
                     offsets_traceable=True,
                     instrument_and_clock_verified=True)
        r = evaluate(replace(a, **flags), replace(b, **flags))
        self.assertTrue(r["candidate_for_metrology_review"])
        self.assertFalse(r["hardware_approved"])
        for key in list(flags)[1:]:
            with self.subTest(flag=key):
                x = replace(b, **{**flags, key: False})
                self.assertFalse(evaluate(replace(a, **flags), x)["candidate_for_metrology_review"])
        with self.assertRaises(ValueError):
            evaluate(a, replace(b, source_kind="BENCH_MEASURED"))

    def test_unqualified_geometry(self):
        a, b = pair()
        for key, val in (("gap_mm", "-1"), ("temperature_c", "100"),
                         ("load_ohm", "0"), ("lateral_offset_mm", "-2")):
            with self.subTest(key=key):
                with self.assertRaises(ValueError):
                    evaluate(replace(a, **{key: val}), b)

    def test_no_synthetic_claim_as_hardware(self):
        r = demo()
        for flag in ("hardware_approved", "wpt_energization_approved",
                     "lithium_dock_approved", "safety_cutoff_or_fod_proven",
                     "purchase_authorized"):
            self.assertFalse(r[flag])
        self.assertEqual(r["physical_bench_measurements"], 0)
        self.assertTrue(r["battery_bms_dock_disconnected"])


if __name__ == "__main__":
    unittest.main()
