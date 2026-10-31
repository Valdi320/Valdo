"""Original fault-injection suite. All inputs fictitious; no hardware access."""
from decimal import Decimal
import unittest
from w56_abba_gate import evaluate, example


def changed(index, **fields):
    rows = example()
    rows[index].update(fields)
    return rows


class ABBATests(unittest.TestCase):
    def test_perfect_gain_cancellation(self):
        r = evaluate(example())
        self.assertEqual(Decimal(r["eta_abba_percent"]), Decimal(80))
        self.assertEqual(r["center_residual_rho"], "1")
        self.assertEqual(r["passage_count"], 4)
        self.assertEqual(r["meter_switches"], 2)

    def test_uncertainty_contains_true_result(self):
        r = evaluate(example())
        low, high = map(Decimal, r["conditional_eta_interval_percent"])
        self.assertLess(low, 80)
        self.assertGreater(high, 80)
        self.assertLess(Decimal(r["center_residual_worst_percent"]), 3)

    def test_zero_error_interval_exact(self):
        rows = example()
        for x in rows:
            x["u_pin_mw"] = x["u_pout_mw"] = "0"
        a = evaluate(rows)
        self.assertEqual([Decimal(v) for v in a["conditional_eta_interval_percent"]], [Decimal(80), Decimal(80)])
        self.assertEqual(Decimal(a["center_residual_worst_percent"]), 0)

    def test_single_middle_transient_first_is_detected(self):
        r = evaluate(changed(1, pout_mw="770"))
        self.assertIn("center_ABBA_curvature_or_transient", r["blockers"])
        self.assertLess(Decimal(r["endpoint_drift_worst_percent"]), 2)

    def test_single_middle_transient_second_is_detected(self):
        r = evaluate(changed(2, pout_mw="770"))
        self.assertIn("center_ABBA_curvature_or_transient", r["blockers"])

    def test_endpoint_drift_is_detected(self):
        r = evaluate(changed(3, pout_mw="780"))
        self.assertIn("endpoint_drift", r["blockers"])

    def test_loglinear_drift_has_zero_curvature(self):
        rows = example()
        rows[1]["pout_mw"] = "883.52"
        rows[2]["pout_mw"] = "887.05408"
        rows[3]["pout_mw"] = "728.6746048"
        r = evaluate(rows)
        self.assertLess(abs(Decimal(r["center_residual_rho"]) - 1), Decimal("0.00001"))
        self.assertNotIn("endpoint_drift", r["blockers"])

    def test_same_middle_anomaly_stays_unobservable(self):
        rows = example()
        rows[1]["pout_mw"] = rows[2]["pout_mw"] = "770"
        r = evaluate(rows)
        self.assertNotIn("center_ABBA_curvature_or_transient", r["blockers"])
        self.assertIn("same_anomaly_in_both_middle_passages", r["remaining_blind_spots"])
        self.assertFalse(r["hardware_approved"])

    def test_variability_of_conditions_blocks(self):
        for k, value, name in (("temperature_c", "27", "unstable_temperature_c"),
                               ("gap_mm", "2.2", "unstable_gap_mm"),
                               ("offset_mm", "0.2", "unstable_offset_mm"),
                               ("load_ohm", "20.3", "unstable_load")):
            with self.subTest(k=k):
                self.assertIn(name, evaluate(changed(3, **{k: value}))["blockers"])

    def test_time_asymmetry_is_blocked(self):
        self.assertIn("unequally_spaced_acquisitions", evaluate(changed(3, start_ms=1300, end_ms=1400))["blockers"])

    def test_overlapping_or_bad_timestamps_raise(self):
        for kwargs in (dict(start_ms=80), dict(end_ms=200), dict(start_ms=-1),
                       dict(start_ms=True), dict(end_ms=200)):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    evaluate(changed(1, **kwargs))

    def test_wrong_order_roles_raise(self):
        with self.assertRaises(ValueError):
            evaluate(changed(2, in_meter="A"))

    def test_reused_sample_or_trace_ids_raise(self):
        for key, v in (("run_id", "r0"), ("trace_id", "t1"), ("fixture_id", "wrong")):
            with self.subTest(key=key), self.assertRaises(ValueError):
                evaluate(changed(3, **{key: v}))

    def test_corrupt_measurements_raise(self):
        for field, bad in (("pin_mw", 0), ("pout_mw", "-1"), ("pout_mw", "8000"),
                           ("u_pin_mw", "9999"), ("u_pout_mw", "-1"),
                           ("pin_mw", "NaN"), ("pin_mw", True)):
            with self.subTest(field=field, bad=bad), self.assertRaises(ValueError):
                evaluate(changed(1, **{field: bad}))

    def test_unknown_or_mixed_provenance_raise(self):
        for source in ("RF", "BENCH_MEASURED"):
            with self.subTest(source=source), self.assertRaises(ValueError):
                evaluate(changed(2, source_kind=source))

    def test_malformed_container_raise(self):
        for rows in ([], tuple(example()[:3]), [1, 2, 3, 4], "example"):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                evaluate(rows)

    def test_bench_self_assertion_cannot_approve_hardware(self):
        rows = example()
        for x in rows:
            x.update(source_kind="BENCH_MEASURED", independently_verified_conditions=True,
                     gain_stability_verified=True, offsets_traceable=True,
                     instrument_and_clock_verified=True)
        r = evaluate(rows)
        self.assertTrue(r["candidate_for_external_metrology_review"])
        self.assertFalse(r["hardware_approved"])
        self.assertFalse(r["energization_approved"])
        self.assertFalse(r["local_cutoff_qualified"])
        self.assertFalse(r["lithium_dock_approved"])

    def test_missing_calibration_flag_blocks_review(self):
        rows = example()
        for x in rows:
            x.update(source_kind="BENCH_MEASURED", independently_verified_conditions=True,
                     gain_stability_verified=True, offsets_traceable=True,
                     instrument_and_clock_verified=True)
        rows[2]["offsets_traceable"] = False
        self.assertIn("missing_independent_calibration_or_conditions", evaluate(rows)["blockers"])

    def test_nonboolean_flags_raise(self):
        for bad in (1, "true", None):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                evaluate(changed(3, gain_stability_verified=bad))

    def test_no_hardware_claims_or_purchase(self):
        r = evaluate(example())
        self.assertEqual(r["physical_measurements"], 0)
        self.assertEqual(r["added_robots_parts_eur"], "0")
        for k in ("hardware_approved", "energization_approved", "lithium_dock_approved", "local_cutoff_qualified"):
            self.assertFalse(r[k])

    def test_false_uncertainty_widens_residual_and_blocks(self):
        rows = example()
        for x in rows:
            x["u_pin_mw"] = x["u_pout_mw"] = "5"
        r = evaluate(rows)
        self.assertIn("center_ABBA_curvature_or_transient", r["blockers"])


if __name__ == "__main__":
    unittest.main()
