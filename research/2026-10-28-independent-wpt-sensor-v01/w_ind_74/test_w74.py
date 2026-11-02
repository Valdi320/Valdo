"""Synthetic adversarial tests, NOT WPT safety validation or physical tests."""
import copy
import json
import math
import unittest
from pathlib import Path
from w74_energy_gate import audit, SCHEMA

SAMPLE = json.loads((Path(__file__).parent / "SCENARIO_HYPOTHETICAL.json").read_text())

class W74(unittest.TestCase):
    def test_calculated_model(self):
        z = audit(SAMPLE)
        self.assertEqual(z["schema"], SCHEMA)
        self.assertAlmostEqual(z["sensor_load_average_W"], 0.0029)
        self.assertAlmostEqual(z["wpt_transmitter_average_W"], 0.1058)
        self.assertAlmostEqual(z["wpt_transmitter_peak_W"], 0.3)
        self.assertAlmostEqual(z["wpt_average_dissipation_W"], 0.1029)
        self.assertAlmostEqual(z["wpt_peak_dissipation_W"], 0.2)
        self.assertAlmostEqual(z["wpt_daily_energy_Wh"], 2.5392)
        self.assertGreater(z["wpt_to_wired_energy_ratio"], 36)
        self.assertGreater(z["wpt_extra_energy_Wh_per_day"], 2.46)
        self.assertAlmostEqual(z["max_tx_fixed_overhead_W_for_daily_budget"], 0.5/24+z["wired_supply_average_W"]-0.0029/0.5)
        self.assertLess(z["max_tx_fixed_overhead_W_for_daily_budget"], 0.018)
        self.assertAlmostEqual(z["wired_peak_voltage_drop_percent"], 100 * 0.1 / 3.3 * 0.2 / 3.3)
        self.assertEqual(z["failed_hypothetical_gates"], ["WPT_EXCESS_DAILY_ENERGY"])
        self.assertEqual(z["decision"], "NO_GO_UNDER_HYPOTHESES")
        self.assertFalse(z["hardware_approved"])
        self.assertFalse(z["physical_tests_performed"])
        self.assertFalse(z["battery_or_bms_connected"])

    def check_bad(self, path, value):
        obj = copy.deepcopy(SAMPLE)
        d = obj
        for k in path[:-1]: d = d[k]
        d[path[-1]] = value
        with self.assertRaises(ValueError): audit(obj)

    def test_bad_schema(self): self.check_bad(["schema"], "X20Pro")
    def test_bad_module_type(self): self.check_bad(["sensor", "function"], "motor")
    def test_motor_is_not_pilot(self): self.check_bad(["sensor", "motor_or_pump"], True)
    def test_radio_cannot_be_safety_cut(self): self.check_bad(["sensor", "radio_for_critical_stop"], True)
    def test_battery_stays_disconnected(self): self.check_bad(["sensor", "battery_or_bms_connected"], True)
    def test_battery_field_missing(self):
        obj = copy.deepcopy(SAMPLE); del obj["sensor"]["battery_or_bms_connected"]
        with self.assertRaises(ValueError): audit(obj)
    def test_zero_efficiency(self): self.check_bad(["wpt", "dc_efficiency_fraction"], 0)
    def test_eta_gt_one(self): self.check_bad(["wpt", "dc_efficiency_fraction"], 1.1)
    def test_nan(self): self.check_bad(["wpt", "tx_fixed_overhead_W"], math.nan)
    def test_infinite(self): self.check_bad(["wpt", "tx_fixed_overhead_W"], math.inf)
    def test_boolean_as_number(self): self.check_bad(["wpt", "tx_fixed_overhead_W"], True)
    def test_negative_overhead(self): self.check_bad(["wpt", "tx_fixed_overhead_W"], -0.01)
    def test_missing_efficiency(self):
        obj=copy.deepcopy(SAMPLE); del obj["wpt"]["dc_efficiency_fraction"]
        with self.assertRaises(ValueError): audit(obj)
    def test_bad_duty(self): self.check_bad(["sensor", "active_fraction"], 1.1)
    def test_negative_duty(self): self.check_bad(["sensor", "active_fraction"], -0.1)
    def test_sleep_gt_active(self): self.check_bad(["sensor", "sleep_W"], 0.03)
    def test_peak_below_active(self): self.check_bad(["sensor", "peak_W"], 0.001)
    def test_zero_rail(self): self.check_bad(["sensor", "rail_V"], 0)
    def test_unknown_provenance(self): self.check_bad(["evidence", "source_kind"], "CERTIFIED_REAL")
    def test_bench_authorization_not_granted(self): self.check_bad(["evidence", "physical_bench_authorized"], True)
    def test_no_evidence_section(self):
        obj=copy.deepcopy(SAMPLE); del obj["evidence"]
        with self.assertRaises(ValueError): audit(obj)
    def test_rx_peak_insufficient(self):
        obj=copy.deepcopy(SAMPLE); obj["wpt"]["rx_peak_rating_W"]=0.09
        self.assertIn("RX_PEAK_RATING_INSUFFICIENT",audit(obj)["failed_hypothetical_gates"])
    def test_tx_peak_insufficient(self):
        obj=copy.deepcopy(SAMPLE); obj["wpt"]["tx_input_limit_W"]=0.29
        self.assertIn("TX_PEAK_INPUT_LIMIT_INSUFFICIENT",audit(obj)["failed_hypothetical_gates"])
    def test_heat_hypothesis_exceeded(self):
        obj=copy.deepcopy(SAMPLE); obj["criteria"]["max_peak_dissipation_W"]=0.1
        self.assertIn("WPT_PEAK_DISSIPATION_HYPOTHESIS_EXCEEDED",audit(obj)["failed_hypothetical_gates"])
    def test_wire_drop_hypothesis_exceeded(self):
        obj=copy.deepcopy(SAMPLE); obj["wire"]["loop_resistance_ohm"]=8.0
        self.assertIn("WIRED_PEAK_DROP_HYPOTHESIS_EXCEEDED",audit(obj)["failed_hypothetical_gates"])
    def test_conditional_not_hardware_approved(self):
        obj=copy.deepcopy(SAMPLE); obj["wpt"]["tx_fixed_overhead_W"]=0
        z=audit(obj); self.assertEqual(z["decision"], "MODEL_ONLY_CONDITIONAL")
        self.assertFalse(z["hardware_approved"])
    def test_fabricated_bench_metadata_never_approves(self):
        obj=copy.deepcopy(SAMPLE); obj["evidence"]["source_kind"]="BENCH_UNREVIEWED"
        self.assertFalse(audit(obj)["hardware_approved"])
    def test_eta_one_ideal_no_overhead(self):
        obj=copy.deepcopy(SAMPLE); obj["wpt"]["dc_efficiency_fraction"]=1
        obj["wpt"]["tx_fixed_overhead_W"]=0
        z=audit(obj); self.assertAlmostEqual(z["wpt_transmitter_average_W"],z["sensor_load_average_W"])
    def test_zero_duty_is_sleep(self):
        obj=copy.deepcopy(SAMPLE); obj["sensor"]["active_fraction"]=0
        self.assertAlmostEqual(audit(obj)["sensor_load_average_W"],0.001)
    def test_one_duty_is_active(self):
        obj=copy.deepcopy(SAMPLE); obj["sensor"]["active_fraction"]=1
        self.assertAlmostEqual(audit(obj)["sensor_load_average_W"],0.020)
    def test_efficiency_alone_makes_budget_impossible(self):
        obj=copy.deepcopy(SAMPLE); obj["wpt"]["dc_efficiency_fraction"]=0.1
        obj["wpt"]["tx_fixed_overhead_W"]=0
        obj["wpt"]["tx_input_limit_W"]=2
        self.assertIn("WPT_ZERO_OVERHEAD_STILL_EXCEEDS_ENERGY_BUDGET",audit(obj)["failed_hypothetical_gates"])
    def test_negative_budget_rejected(self): self.check_bad(["criteria", "max_extra_Wh_per_day"], -1)

if __name__ == "__main__": unittest.main()
