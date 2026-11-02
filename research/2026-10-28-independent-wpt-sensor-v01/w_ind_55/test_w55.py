"""Adversarial synthetic tests for W55. No I2C/hardware measurements."""
import unittest
from dataclasses import replace
from decimal import Decimal
from w55_aba_drift_gate import Passage, dec, evaluate, demo


def good():
    common = dict(fixture_id="F", u_pin_mw="2", u_pout_mw="2",
                  temperature_c="25", gap_mm="2", offset_mm="0", load_ohm="20")
    return (
        Passage("a", "ta", in_meter="A", out_meter="B", start_ms=0, end_ms=100,
                pin_mw="1100", pout_mw="720", **common),
        Passage("b", "tb", in_meter="B", out_meter="A", start_ms=200, end_ms=300,
                pin_mw="900", pout_mw="880", **common),
        Passage("c", "tc", in_meter="A", out_meter="B", start_ms=400, end_ms=500,
                pin_mw="1100", pout_mw="720", **common),
    )


class ABATests(unittest.TestCase):
    def test_gain_ratio_exact_cancel(self):
        r = evaluate(good())
        self.assertEqual(Decimal(r["eta_aba_percent"]), Decimal("80"))
        self.assertFalse(r["hardware_approved"])

    def test_interval_contains_nominal(self):
        r = evaluate(good())
        lo, hi = map(Decimal, r["conditional_interval_percent"])
        self.assertLess(lo, 80)
        self.assertGreater(hi, 80)

    def test_zero_error_exact_interval(self):
        z = tuple(replace(x, u_pin_mw="0", u_pout_mw="0") for x in good())
        r = evaluate(z)
        self.assertEqual([Decimal(v) for v in r["conditional_interval_percent"]], [Decimal(80), Decimal(80)])

    def test_gross_endpoint_drift_blocked(self):
        a, b, c = good()
        # An 8% increase in the true later efficiency is visible in the repeated AB assignment.
        c = replace(c, pout_mw="777.6")
        r = evaluate((a, b, c))
        self.assertGreater(Decimal(r["endpoint_drift_worst_percent"]), 2)
        self.assertTrue(any("endpoint_drift" in x for x in r["blockers"]))

    def test_time_asymmetry_rejected(self):
        a, b, c = good()
        c = replace(c, start_ms=1000, end_ms=1100)
        r = evaluate((a, b, c))
        self.assertTrue(any("time_center" in x for x in r["blockers"]))

    def test_linear_log_efficiency_drift_midpoint_estimate(self):
        a, b, c = good()
        # Eta0 = 0.75 and Eta1 = 0.80; log-linear Eta2 = 0.80^2 / 0.75.
        a = replace(a, pout_mw="675")
        c = replace(c, pout_mw="768")
        r = evaluate((a, b, c))
        self.assertAlmostEqual(float(r["eta_aba_percent"]), 80.0, places=10)
        self.assertGreater(Decimal(r["endpoint_drift_worst_percent"]), 2)

    def test_midpoint_only_transient_not_detectable(self):
        a, b, c = good()
        # BA midpoint has different true efficiency, AB endpoints remain identical.
        b = replace(b, pout_mw="770")
        r = evaluate((a, b, c))
        self.assertEqual(Decimal(r["endpoint_drift_nominal_percent"]), Decimal(0))
        self.assertNotEqual(Decimal(r["eta_aba_percent"]), Decimal(80))
        self.assertTrue(any("midpoint-only" in x for x in r["unobservable_risks"]))
        self.assertFalse(r["hardware_approved"])

    def test_instrument_position_drift_not_proven(self):
        a, b, c = good()
        b = replace(b, pout_mw="870")
        r = evaluate((a, b, c))
        self.assertFalse(r["candidate_for_external_metrology_review"])
        self.assertTrue(any("gain_stability_verified" in x for x in r["blockers"]))

    def test_repeated_ids_fail(self):
        a, b, c = good()
        for change in (replace(c, run_id="a"), replace(c, trace_id="tb"), replace(c, fixture_id="other")):
            with self.subTest(change=change):
                with self.assertRaises(ValueError):
                    evaluate((a, b, change))

    def test_instrument_order_fail(self):
        a, b, c = good()
        invalid = (
            (a, b, replace(c, in_meter="B")),
            (a, replace(b, out_meter="B"), c),
            (replace(a, out_meter="A"), b, c),
        )
        for triplet in invalid:
            with self.subTest(triplet=triplet):
                with self.assertRaises(ValueError):
                    evaluate(triplet)

    def test_timestamp_bad(self):
        a, b, c = good()
        for change in (replace(b, start_ms=80), replace(b, end_ms=80), replace(b, start_ms=-5),
                       replace(b, start_ms=True), replace(b, end_ms=500)):
            with self.subTest(change=change):
                with self.assertRaises(ValueError):
                    evaluate((a, change, c))

    def test_non_numeric_rejected(self):
        a, b, c = good()
        for val in ("nan", "inf", "-Infinity", "bad", None):
            with self.subTest(val=val):
                with self.assertRaises(ValueError):
                    evaluate((replace(a, pin_mw=val), b, c))

    def test_power_bounds_rejected(self):
        a, b, c = good()
        for key, val in (("pin_mw", "0"), ("pout_mw", "-1"), ("u_pin_mw", "10000"),
                         ("u_pout_mw", "-1"), ("pout_mw", "1200"), ("u_pin_mw", "500")):
            with self.subTest(key=key, val=val):
                with self.assertRaises(ValueError):
                    evaluate((replace(a, **{key: val}), b, c))

    def test_conditions_spread_and_negative(self):
        a, b, c = good()
        for key, val in (("temperature_c", "27"), ("gap_mm", "2.2"),
                         ("offset_mm", "0.2"), ("load_ohm", "21")):
            with self.subTest(key=key):
                r = evaluate((a, b, replace(c, **{key: val})))
                self.assertFalse(r["candidate_for_external_metrology_review"])
                self.assertTrue(any(key.split("_")[0] in x for x in r["blockers"]))
        for key, val in (("temperature_c", "200"), ("gap_mm", "-1"),
                         ("offset_mm", "-1"), ("load_ohm", "0")):
            with self.subTest(key=key):
                with self.assertRaises(ValueError):
                    evaluate((a, b, replace(c, **{key: val})))

    def test_evidence_type(self):
        a, b, c = good()
        with self.assertRaises(ValueError):
            evaluate((a, replace(b, source_kind="BENCH_MEASURED"), c))
        with self.assertRaises(ValueError):
            evaluate((a, replace(b, source_kind="UNVERIFIED"), c))

    def test_self_declared_evidence_not_safety_approval(self):
        flags = dict(source_kind="BENCH_MEASURED", independently_verified_conditions=True,
                     gain_stability_verified=True, offsets_traceable=True, instrument_and_clock_verified=True)
        runs = tuple(replace(x, **flags) for x in good())
        r = evaluate(runs)
        self.assertTrue(r["candidate_for_external_metrology_review"])
        self.assertFalse(r["hardware_approved"])
        self.assertFalse(r["energization_approved"])
        self.assertFalse(r["lithium_dock_approved"])
        self.assertTrue(any("self-declared" in s for s in r["unobservable_risks"]))

    def test_flags_are_exact_bool(self):
        flags = dict(source_kind="BENCH_MEASURED", independently_verified_conditions=True,
                     gain_stability_verified=True, offsets_traceable=True, instrument_and_clock_verified=True)
        r = tuple(replace(x, **flags) for x in good())
        for v in (1, "true", None, False):
            with self.subTest(v=v):
                modified = (r[0], replace(r[1], gain_stability_verified=v), r[2])
                self.assertFalse(evaluate(modified)["candidate_for_external_metrology_review"])

    def test_no_hardware_or_price_claim_in_demo(self):
        r = demo()
        self.assertEqual(r["physical_measurements"], 0)
        self.assertEqual(r["added_robots_parts_eur"], "0")
        for key in ("hardware_approved", "energization_approved", "lithium_dock_approved", "local_cutoff_qualified"):
            self.assertFalse(r[key])

    def test_invalid_container(self):
        a, b, c = good()
        with self.assertRaises(ValueError):
            evaluate([a, b, c])
        with self.assertRaises(ValueError):
            evaluate((a, b))
        with self.assertRaises(ValueError):
            evaluate((a, b, object()))

    def test_consistent_source_and_seed(self):
        self.assertEqual(dec("0.8"), Decimal("0.8"))
        self.assertEqual(demo(), demo())


if __name__ == "__main__":
    unittest.main()
