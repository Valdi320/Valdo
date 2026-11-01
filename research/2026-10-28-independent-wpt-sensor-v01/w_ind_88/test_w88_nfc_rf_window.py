"""W88 distinct RF-communication-gap/retry energy tests; all synthetic."""
import unittest
from decimal import Decimal
from w88_nfc_rf_window import window_gate, report

B = dict(am="AM100", field="0.5", eta="0.8", baseline_mw="0.1",
         event_mj="1", period_s="1", blackout_s="0.1", effective_cap_uf="1200",
         storage_vhigh="3.3", storage_vstart="3.3", storage_vlow="3.0",
         attempts_by_cycle=[1, 1, 1])


class WindowTests(unittest.TestCase):
    def go(self, **kw):
        return window_gate(**{**B, **kw})

    def test_st_sample_attributed_and_physical_release_always_blocked(self):
        x = self.go()
        self.assertEqual(x["author_EH_mW_sample_not_guaranteed"], "2.31")
        self.assertEqual(x["hardware_release"], "BLOCKED")
        self.assertFalse(x["RF_simultaneous_energy_and_communication_validated"])

    def test_single_attempt_and_100ms_rf_blackout_pass_ideal(self):
        x = self.go()
        self.assertTrue(x["ideal_window_pass"])
        self.assertEqual(x["ideal_cycles_completed"], 3)
        self.assertEqual(Decimal(x["trace"][0]["after_blackout_mJ"]), Decimal("0.124"))

    def test_second_attempt_in_same_gap_fails_immediately(self):
        x = self.go(attempts_by_cycle=[2, 1])
        self.assertEqual(x["first_failure"]["cycle"], 1)
        self.assertEqual(x["first_failure"]["stage"], "BURST")
        self.assertEqual(x["ideal_max_attempts_in_one_blackout_from_full_storage"], 1)

    def test_two_attempts_require_over_2mF_effective(self):
        x = self.go(attempts_by_cycle=[2])
        c = Decimal(x["ideal_min_effective_cap_uF_for_worst_cluster"])
        self.assertGreater(c, Decimal("2126"))
        self.assertLess(c, Decimal("2128"))

    def test_weak_field_am10_fails_second_cycle_not_first(self):
        x = self.go(am="AM10", attempts_by_cycle=[1, 1, 1])
        self.assertEqual(x["first_failure"]["cycle"], 2)
        self.assertEqual(x["first_failure"]["stage"], "BURST")
        self.assertEqual(Decimal(x["trace"][0]["after_recharge_mJ"]), Decimal("0.2932"))

    def test_am10_with_ten_seconds_recovery_survives_in_model(self):
        x = self.go(am="AM10", period_s="10")
        self.assertTrue(x["ideal_window_pass"])
        self.assertEqual(x["hardware_release"], "BLOCKED")

    def test_retry_cluster_also_shrinks_energy_margin(self):
        one = self.go(attempts_by_cycle=[1, 1])
        two = self.go(attempts_by_cycle=[2, 2])
        self.assertGreater(Decimal(one["ideal_average_energy_margin_mW"]),
                           Decimal(two["ideal_average_energy_margin_mW"]))

    def test_small_outage_can_still_fail_instant_burst(self):
        x = self.go(blackout_s="0", attempts_by_cycle=[2])
        self.assertEqual(x["first_failure"]["stage"], "BURST")

    def test_long_rf_blackout_can_fail_after_events(self):
        x = self.go(blackout_s="0.5", baseline_mw="0.5", attempts_by_cycle=[1])
        self.assertEqual(x["first_failure"]["stage"], "RF_BLACKOUT")

    def test_hypothetical_precharged_initial_rail_is_important(self):
        x = self.go(storage_vstart="3.15")
        self.assertEqual(x["first_failure"]["stage"], "BURST")

    def test_cap_minimum_boundary_exact(self):
        x = self.go(effective_cap_uf="2000", event_mj="1.89", baseline_mw="0",
                    attempts_by_cycle=[1], blackout_s="0")
        self.assertTrue(x["ideal_window_pass"])
        self.assertEqual(Decimal(x["trace"][0]["after_events_mJ"]), Decimal("0"))

    def test_zero_event_cycle_can_recover(self):
        x = self.go(attempts_by_cycle=[1, 0, 1])
        self.assertTrue(x["ideal_window_pass"])

    def test_no_live_rf_period_must_deplete_from_baseline(self):
        x = self.go(blackout_s="1", baseline_mw="2", attempts_by_cycle=[0])
        self.assertEqual(x["first_failure"]["stage"], "RF_BLACKOUT")

    def test_negative_recharge_net_depletes_even_without_tx(self):
        x = self.go(baseline_mw="3", blackout_s="0", attempts_by_cycle=[0])
        self.assertEqual(x["first_failure"]["stage"], "RECHARGE_WINDOW")

    def test_reject_blackout_longer_than_period(self):
        with self.assertRaises(ValueError): self.go(blackout_s="1.01")

    def test_reject_negative_blackout(self):
        with self.assertRaises(ValueError): self.go(blackout_s="-0.01")

    def test_reject_nonfinite_and_float(self):
        for key, value in [("eta", "NaN"), ("baseline_mw", "Infinity"),
                           ("event_mj", 0.1), ("eta", True)]:
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                self.go(**{key: value})

    def test_reject_invalid_eta_and_cap(self):
        for key, value in [("eta", "0"), ("eta", "1.1"), ("effective_cap_uf", "0")]:
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                self.go(**{key: value})

    def test_reject_bad_voltages(self):
        for key, value in [("storage_vstart", "3.31"), ("storage_vlow", "3.3"),
                           ("storage_vhigh", "2.5")]:
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                self.go(**{key: value})

    def test_reject_bad_cycles_list(self):
        for value in [[], [True], [1.0], [-1], [33], [0] * 1025, (1, 1)]:
            with self.subTest(value=type(value).__name__), self.assertRaises(ValueError):
                self.go(attempts_by_cycle=value)

    def test_reject_unsampled_field(self):
        with self.assertRaises(ValueError): self.go(field="0.75")

    def test_fod_privacy_emergency_stop_all_unverified(self):
        x = self.go()
        self.assertFalse(x["FOD_temperature_EMI_and_independent_cut_verified"])
        self.assertFalse(x["RF_app_ACK_seq_timeout_privacy_recovery_validated"])
        self.assertFalse(x["dock_BMS_lithium_in_scope"])

    def test_deterministic_report_and_no_false_qualification(self):
        a = report()
        self.assertEqual(a, report())
        self.assertEqual(a["hardware_release"], "BLOCKED")
        self.assertFalse(a["AM100_one_retry_first_cycle"]["ideal_window_pass"])
        self.assertTrue(a["AM100_one_attempt_3_cycles"]["ideal_window_pass"])


if __name__ == "__main__":
    unittest.main()
