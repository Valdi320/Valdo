import csv
import io
import json
import unittest
from w48_meter_gate import screen, demo


def stream(current="0.1", n=21, dt=50, offset=0, v="5"):
    result="t_ms,v_volts,i_amps\n"
    return result+"".join(f"{i*dt+offset},{v},{current}\n" for i in range(n))

CFG={"mode":"synthetic", "tx_relative_power_uncertainty":"0.03", "rx_relative_power_uncertainty":"0.03", "max_gap_ms":"250", "max_skew_ms":"25", "min_efficiency":"0.70"}

class W48Tests(unittest.TestCase):
    def run_gate(self, tx=None,rx=None,cfg=None):
        return screen(tx if tx is not None else stream(),rx if rx is not None else stream("0.08"),cfg if cfg is not None else CFG)
    def invalid(self,*args,**kw):
        with self.assertRaises(ValueError): self.run_gate(*args,**kw)

    def test_nominal_80(self): self.assertEqual(self.run_gate()["efficiency_nominal"],"0.8")
    def test_pass_uncertainty(self): self.assertTrue(self.run_gate()["energetic_screen_pass"])
    def test_lower_bound(self): self.assertAlmostEqual(float(self.run_gate()["efficiency_conservative_lower"]),0.8*0.97/1.03)
    def test_lower_65_not_pass(self): self.assertFalse(self.run_gate(rx=stream("0.065"))["energetic_screen_pass"])
    def test_app_not_safety(self): self.assertFalse(self.run_gate()["hardware_approved"])
    def test_dock_not_approved(self): self.assertFalse(self.run_gate()["battery_or_dock_approved"])
    def test_duplicate_ts(self): self.invalid(tx=stream().replace("50,5,0.1","0,5,0.1"))
    def test_nonmonotonic(self): self.invalid(tx=stream().replace("100,5,0.1","49,5,0.1"))
    def test_skew(self): self.invalid(rx=stream("0.08",offset=30))
    def test_skew_at_edge(self): self.assertTrue(self.run_gate(rx=stream("0.08",offset=25))["energetic_screen_pass"])
    def test_gap(self): self.invalid(tx=stream(dt=300),rx=stream("0.08",dt=300))
    def test_missing(self): self.invalid(rx=stream("0.08",n=20))
    def test_zero_input(self): self.invalid(tx=stream("0"))
    def test_zero_output(self): self.assertEqual(float(self.run_gate(rx=stream("0"))["efficiency_nominal"]),0.0)
    def test_negative_current(self): self.invalid(rx=stream("-0.01"))
    def test_negative_voltage(self): self.invalid(rx=stream(v="-5"))
    def test_zero_voltage(self): self.invalid(tx=stream(v="0"))
    def test_nonfinite(self): self.invalid(tx=stream(current="NaN"))
    def test_invalid_header(self): self.invalid(tx=stream().replace("t_ms,v_volts,i_amps","timestamp,volt,amp"))
    def test_extra_col(self): self.invalid(tx=stream().replace("t_ms,v_volts,i_amps","t_ms,v_volts,i_amps,extra"))
    def test_few_samples(self): self.invalid(tx=stream(n=2),rx=stream("0.08",n=2))
    def test_false_gain(self):
        r=self.run_gate(rx=stream("0.12"))
        self.assertTrue(r["anomalous_energy_gain"])
        self.assertFalse(r["energetic_screen_pass"])
    def test_invalid_uncertainty(self): self.invalid(cfg={**CFG,"tx_relative_power_uncertainty":"0.6"})
    def test_missing_uncertainty(self): self.invalid(cfg={k:v for k,v in CFG.items() if k!="tx_relative_power_uncertainty"})
    def test_bad_threshold(self): self.invalid(cfg={**CFG,"min_efficiency":"1.01"})
    def test_measured_requires_bench(self): self.invalid(cfg={**CFG,"mode":"measured"})
    def test_measured_zero_uncertainty(self):
        cfg={**CFG,"mode":"measured","battery_disconnected":True,"source_kind":"isolated_current_limited","load_kind":"resistive","calibration_ref":"cal-1","tx_relative_power_uncertainty":"0"}
        self.invalid(cfg=cfg)
    def test_measured_metadata_allows_analysis_not_approval(self):
        cfg={**CFG,"mode":"measured","battery_disconnected":True,"source_kind":"isolated_current_limited","load_kind":"resistive","calibration_ref":"cal-1"}
        r=self.run_gate(cfg=cfg)
        self.assertEqual(r["evidence_class"],"measured")
        self.assertFalse(r["hardware_approved"])
    def test_sha_determinism(self): self.assertEqual(self.run_gate()["input_sha256"],self.run_gate()["input_sha256"])
    def test_demo_energy(self):
        r=demo()
        self.assertEqual(r["energy_input_j"],"0.500")
        self.assertEqual(float(r["energy_output_j"]),0.4)
    def test_json_safe(self): json.loads(json.dumps(demo()))

if __name__ == "__main__": unittest.main()
