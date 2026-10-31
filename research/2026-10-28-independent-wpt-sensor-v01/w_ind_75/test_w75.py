import copy
import json
import unittest
from pathlib import Path
from w75_vendor_state_gate import screen

BASE = json.loads((Path(__file__).parent / "SCENARIO_VENDOR_DOCUMENT_ONLY.json").read_text())


def synthetic_measured():
    v = copy.deepcopy(BASE)
    v["vendor"] = "EXPERIMENTAL SYNTHETIC ONLY"
    v["lifecycle"] = "active"
    v["loaded"].update(tx_input_mw=20, rx_output_mw=2.9, source_kind="bench_measured", gap_mm=2, offset_mm=0, coil_temp_c=25)
    for k in v["safety"]:
        v["safety"][k] = "bench_measured"
    for k in v["radio"]:
        v["radio"][k] = True
    return v


class VendorGate(unittest.TestCase):
    def test_vendor_standby_calculated_but_never_promoted_to_load(self):
        v = screen(BASE)
        self.assertEqual(v["standby_no_receiver_mw"], 5)
        self.assertIsNone(v["loaded_input_wh_day"])
        self.assertFalse(v["standby_is_loaded_evidence"])
        self.assertIn("LOADED_POWER_UNKNOWN", v["blockers"])

    def test_obsolete_blocks(self):
        self.assertIn("LIFECYCLE_NOT_ACTIVE", screen(BASE)["blockers"])

    def test_unverified_protections_block(self):
        self.assertIn("SAFETY_GATES_UNVERIFIED", screen(BASE)["blockers"])

    def test_unverified_radio_blocks(self):
        self.assertIn("RADIO_APP_GATES_UNVERIFIED", screen(BASE)["blockers"])

    def test_hypothetical_digital_pass_not_hardware_approval(self):
        v = screen(synthetic_measured())
        self.assertEqual(v["status"], "DIGITAL_SCREEN_PASS_NOT_HARDWARE_APPROVAL")
        self.assertFalse(v["hardware_approved"])
        self.assertAlmostEqual(v["excess_wh_day"], 0.4104)
        self.assertAlmostEqual(v["maximum_loaded_tx_mw_for_budget"], 23.733333333, places=8)

    def test_high_tx_consumption_fail(self):
        v = synthetic_measured()
        v["loaded"]["tx_input_mw"] = 100
        self.assertIn("EXCESS_DAILY_ENERGY", screen(v)["blockers"])

    def test_nonrepresentative_rx_fail(self):
        v = synthetic_measured()
        v["loaded"]["rx_output_mw"] = 3.2
        self.assertIn("MEASURED_LOAD_NOT_REPRESENTATIVE", screen(v)["blockers"])

    def test_vendor_figure_as_loaded_is_not_a_measurement(self):
        v = synthetic_measured()
        v["loaded"]["source_kind"] = "manufacturer_claim"
        self.assertIn("LOADED_POWER_NOT_BENCH_MEASURED", screen(v)["blockers"])

    def test_missing_alignment_blocks(self):
        v = synthetic_measured()
        v["loaded"]["offset_mm"] = None
        self.assertIn("OPERATING_GEOMETRY_TEMP_UNKNOWN", screen(v)["blockers"])

    def test_more_output_than_input_rejected(self):
        v = synthetic_measured()
        v["loaded"]["tx_input_mw"] = 1
        with self.assertRaises(ValueError):
            screen(v)

    def test_nan_inf_bool_values_rejected(self):
        for value in (float('nan'), float('inf'), float('-inf'), True, -1, "2.9"):
            v = synthetic_measured()
            v["sensor_mean_mw"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                screen(v)

    def test_absent_or_improperly_claimed_standby_rejected(self):
        for cond in (None, "loaded", "receiver_present"):
            v = synthetic_measured()
            v["standby"]["condition"] = cond
            with self.subTest(cond=cond), self.assertRaises(ValueError):
                screen(v)

    def test_no_manufacturer_source_rejected(self):
        v = synthetic_measured()
        v["standby"]["source_url"] = ""
        with self.assertRaises(ValueError):
            screen(v)

    def test_risky_actuator_or_battery_case_blocks(self):
        for k in ("motor_or_pump", "battery_or_bms_connected", "critical_radio_stop"):
            v = synthetic_measured()
            v[k] = True
            with self.subTest(k=k):
                self.assertEqual(screen(v)["status"], "BLOCKED")

    def test_missing_explicit_false_blocks(self):
        v = synthetic_measured()
        del v["battery_or_bms_connected"]
        self.assertIn("FORBIDDEN_BATTERY_OR_BMS_CONNECTED", screen(v)["blockers"])

    def test_noncritical_module_only(self):
        v = synthetic_measured()
        v["module_kind"] = "cliff_sensor"
        self.assertIn("NOT_A_NONCRITICAL_SENSOR", screen(v)["blockers"])

    def test_radio_requires_all_guards(self):
        for k in synthetic_measured()["radio"]:
            v = synthetic_measured()
            v["radio"][k] = False
            with self.subTest(k=k):
                self.assertIn("RADIO_APP_GATES_UNVERIFIED", screen(v)["blockers"])

    def test_safety_requires_all_guards(self):
        for k in synthetic_measured()["safety"]:
            v = synthetic_measured()
            v["safety"][k] = "unknown"
            with self.subTest(k=k):
                self.assertIn("SAFETY_GATES_UNVERIFIED", screen(v)["blockers"])

    def test_deterministic_output(self):
        self.assertEqual(screen(BASE), screen(copy.deepcopy(BASE)))

    def test_fixed_threshold_comparison(self):
        v = synthetic_measured()
        v["loaded"]["tx_input_mw"] = 2.9 + 500 / 24
        self.assertEqual(screen(v)["status"], "DIGITAL_SCREEN_PASS_NOT_HARDWARE_APPROVAL")
        v["loaded"]["tx_input_mw"] += 0.001
        self.assertIn("EXCESS_DAILY_ENERGY", screen(v)["blockers"])

if __name__ == "__main__":
    unittest.main()
