import copy
import json
import math
import unittest
from pathlib import Path
from w79_async_uvlo_gate import analyze, StickyPermit

BASE = json.loads((Path(__file__).parent / "TRACE_SYNTHETIC.json").read_text())
def model(): return copy.deepcopy(BASE)

class W79Tests(unittest.TestCase):
    def test_hidden_drop_while_samples_good(self):
        r = analyze(BASE)
        self.assertEqual(r["samples_v"], [3.3, 3.3])
        self.assertEqual(r["hidden_events_between_samples"], 1)
        self.assertEqual(r["ideal_model_capture_count"], 1)
        self.assertFalse(r["hardware_approved"])
    def test_fast_pulse_can_escape_200us_detector(self):
        x = model(); x["trace"][1]["end_us"] = 4100
        x["trace"][2]["start_us"] = 4100
        r = analyze(x)
        self.assertEqual(r["ideal_model_capture_count"], 0)
        self.assertIn("UNDERVOLTAGE_PULSE_NOT_CAPTURED_IN_MODEL", r["blockers"])
    def test_equal_duration_boundary(self):
        x = model(); x["assumed_response_max_us"] = 1000
        self.assertEqual(analyze(x)["ideal_model_capture_count"], 1)
    def test_slow_detector_misses_event(self):
        x = model(); x["assumed_response_max_us"] = 1001
        self.assertEqual(analyze(x)["ideal_model_capture_count"], 0)
    def test_monitor_supply_loss_cannot_certify_capture(self):
        x = model(); x["trace"][1]["monitor_supply_ok"] = False
        r = analyze(x)
        self.assertEqual(r["ideal_model_capture_count"], 0)
        self.assertIn("MONITOR_SUPPLY_LOST_OR_UNCERTAIN", r["blockers"])
    def test_external_monitor_lost_when_rx_looks_normal(self):
        x = model(); x["trace"][0]["monitor_supply_ok"] = False
        self.assertIn("MONITOR_SUPPLY_LOST_OR_UNCERTAIN", analyze(x)["blockers"])
    def test_claimed_evidence_only_model_not_certification(self):
        x = model(); x["source_kind"] = "bench_claim"
        x["response_evidence"] = "datasheet_max_claim"
        x["monitor_claims"] = {k: True for k in x["monitor_claims"]}
        r = analyze(x)
        self.assertEqual(r["status"], "CONDITIONAL_MODEL_ONLY")
        self.assertFalse(r["real_pulse_capture_proven"])
        self.assertFalse(r["physical_evidence_authenticated"])
    def test_event_in_observed_sample(self):
        x = model(); x["sample_times_us"] = [0, 4500, 10000]
        r = analyze(x)
        self.assertEqual(r["hidden_events_between_samples"], 0)
        self.assertFalse(r["observed_samples_all_above_threshold"])
    def test_events_merged_over_low_boundaries(self):
        x = model(); x["trace"].insert(2,{"start_us":4500,"end_us":5000,"rx_v":2.0,"monitor_supply_ok":True})
        x["trace"][1]["end_us"] = 4500
        self.assertEqual(len(analyze(x)["undervoltage_events"]),1)
    def test_ends_below(self):
        x = model(); x["trace"] = x["trace"][:2]
        x["sample_times_us"]=[0,5000]
        r=analyze(x)
        self.assertEqual(len(r["undervoltage_events"]),1)
    def test_no_low_events_still_no_approval(self):
        x=model(); x["trace"]=[{"start_us":0,"end_us":10000,"rx_v":3.3,"monitor_supply_ok":True}]
        self.assertFalse(analyze(x)["hardware_approved"])
    def test_gaps_overlap_rejected(self):
        for wrong in (3999,4001):
            x=model(); x["trace"][1]["start_us"]=wrong
            with self.subTest(wrong=wrong), self.assertRaises(ValueError):analyze(x)
    def test_missing_boundaries_rejected(self):
        x=model(); x["sample_times_us"]=[10,10000]
        with self.assertRaises(ValueError):analyze(x)
    def test_duplicate_samples_rejected(self):
        x=model(); x["sample_times_us"]=[0,0,10000]
        with self.assertRaises(ValueError):analyze(x)
    def test_false_boolean_numeric_rejected(self):
        for key in ("rx_min_v","assumed_response_max_us"):
            x=model(); x[key]=True
            with self.subTest(key=key),self.assertRaises(ValueError): analyze(x)
    def test_bad_latency_rejected(self):
        for v in (0,-1,0.5,1e100,None,"100",float("nan")):
            x=model(); x["assumed_response_max_us"]=v
            with self.subTest(v=v),self.assertRaises(ValueError): analyze(x)
    def test_nonfinite_voltage_rejected(self):
        for v in (float("nan"),float("inf"),-1):
            x=model(); x["trace"][0]["rx_v"]=v
            with self.subTest(v=v),self.assertRaises(ValueError):analyze(x)
    def test_invalid_claim_rejected(self):
        for v in (1,None,"true"):
            x=model(); x["monitor_claims"]["independent_supply"]=v
            with self.subTest(v=v),self.assertRaises(ValueError):analyze(x)
    def test_bad_sources_rejected(self):
        for field,val in (("source_kind","fabricated"),("response_evidence","verified")):
            x=model(); x[field]=val
            with self.subTest(field=field),self.assertRaises(ValueError):analyze(x)
    def test_repeat_deterministic(self):
        self.assertEqual(analyze(BASE),analyze(model()))
    def test_latch_boot_off(self):
        p=StickyPermit();self.assertTrue(p.fault_latched);self.assertFalse(p.radio_ack())
    def test_explicit_local_rearm_after_stability(self):
        p=StickyPermit(); self.assertFalse(p.arm(stable_us=99999,local_reset=True,monitor_alive=True,temperature_ok=True,fod_clear=True))
        self.assertTrue(p.arm(stable_us=100000,local_reset=True,monitor_alive=True,temperature_ok=True,fod_clear=True))
    def test_radio_cannot_reset_trip(self):
        p=StickyPermit(); p.arm(stable_us=100000,local_reset=True,monitor_alive=True,temperature_ok=True,fod_clear=True)
        p.fault(undervoltage=True);self.assertFalse(p.radio_ack());self.assertTrue(p.fault_latched)
    def test_monitor_brownout_trips(self):
        p=StickyPermit();p.arm(stable_us=100000,local_reset=True,monitor_alive=True,temperature_ok=True,fod_clear=True)
        p.fault(monitor_alive=False);self.assertTrue(p.fault_latched)
    def test_rearm_requires_all_conditions(self):
        for k in ("local_reset","monitor_alive","temperature_ok","fod_clear"):
            args={x:True for x in ("local_reset","monitor_alive","temperature_ok","fod_clear")};args[k]=False
            self.assertFalse(StickyPermit().arm(stable_us=100000,**args))
    def test_latch_rejects_non_boolean(self):
        p=StickyPermit()
        with self.assertRaises(ValueError):p.fault(undervoltage=1)
        with self.assertRaises(ValueError):p.arm(stable_us=100000,local_reset=1,monitor_alive=True,temperature_ok=True,fod_clear=True)

if __name__ == "__main__":unittest.main()
