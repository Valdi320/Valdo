"""W-IND-104 analytical energy-gate regression tests; no hardware."""
import json
import unittest

from w_ind_102.w_ind_102 import load_rows
from w_ind_104.w_ind_104 import (
    SCENARIO, build_report, exact_point, simulate_point, validate_scenario
)

class TestWInd104(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_rows()
        cls.row = exact_point(cls.rows, 10, 1.0)

    def test_uses_exact_manufacturer_point_without_interpolation(self):
        self.assertEqual(self.row["p_eh_mw"], 1.035)
        with self.assertRaises(ValueError):
            exact_point(self.rows, 10, 1.1)

    def test_average_sensor_profile_is_0_248mw(self):
        result = simulate_point(self.row)
        self.assertAlmostEqual(result["average_sensor_load_mw"], 0.248, places=9)

    def test_tolerance_and_retention_raise_nominal_cap_requirement(self):
        result = simulate_point(self.row)
        self.assertAlmostEqual(result["nominal_capacitance_required_uf"], 45.3555878, places=6)

    def test_47uf_has_only_about_3_6_percent_energy_margin(self):
        result = simulate_point(self.row)
        self.assertAlmostEqual(result["cap_effective_uf"], 18.8, places=9)
        self.assertAlmostEqual(result["cap_energy_margin_ratio"], 1.036256, places=6)
        self.assertEqual(result["status"], "CONDITIONAL_PASS")

    def test_field_duty_50_percent_passes_but_40_percent_fails(self):
        s50 = dict(SCENARIO, field_duty_off=0.50)
        s40 = dict(SCENARIO, field_duty_off=0.40)
        self.assertEqual(simulate_point(self.row, s50)["status"], "CONDITIONAL_PASS")
        self.assertEqual(simulate_point(self.row, s40)["status"], "NO_GO_UNDER_ASSUMPTIONS")
        self.assertAlmostEqual(simulate_point(self.row, s50)["required_field_duty_during_off_time"], 0.4156541258, places=8)

    def test_field_duty_25_percent_cannot_recharge(self):
        result = simulate_point(self.row, dict(SCENARIO, field_duty_off=0.25))
        self.assertEqual(result["status"], "NO_GO_UNDER_ASSUMPTIONS")
        self.assertIsNone(result["recharge_time_s"])

    def test_retention_40_percent_fails_cap_energy(self):
        result = simulate_point(self.row, dict(SCENARIO, cap_retention=0.40))
        self.assertFalse(result["checks"]["capacitor_energy"])
        self.assertEqual(result["status"], "NO_GO_UNDER_ASSUMPTIONS")

    def test_retention_60_percent_passes_cap_energy(self):
        result = simulate_point(self.row, dict(SCENARIO, cap_retention=0.60))
        self.assertTrue(result["checks"]["capacitor_energy"])

    def test_esr_10_ohm_passes_and_25_ohm_fails_voltage(self):
        r10 = simulate_point(self.row, dict(SCENARIO, cap_esr_ohm=10.0))
        r25 = simulate_point(self.row, dict(SCENARIO, cap_esr_ohm=25.0))
        self.assertTrue(r10["checks"]["terminal_voltage_after_esr"])
        self.assertFalse(r25["checks"]["terminal_voltage_after_esr"])

    def test_leakage_20ua_passes_narrowly_and_30ua_fails(self):
        r20 = simulate_point(self.row, dict(SCENARIO, cap_leakage_ua=20.0))
        r30 = simulate_point(self.row, dict(SCENARIO, cap_leakage_ua=30.0))
        self.assertEqual(r20["status"], "CONDITIONAL_PASS")
        self.assertEqual(r30["status"], "NO_GO_UNDER_ASSUMPTIONS")

    def test_0_5a_per_m_am10_is_below_design_gate(self):
        row = exact_point(self.rows, 10, 0.5)
        result = simulate_point(row)
        self.assertGreater(result["required_field_duty_during_off_time"], 1.0)

    def test_all_20_points_at_or_above_1a_per_m_pass_at_assumed_50pct_duty(self):
        report = build_report(self.rows)
        sweep = report["sweep_h_ge_1a_per_m"]
        self.assertEqual(sweep["point_count"], 20)
        self.assertEqual(sweep["conditional_pass_at_assumptions"], 20)

    def test_report_excludes_reader_power_and_hardware_approval(self):
        report = build_report(self.rows)
        self.assertFalse(report["assumptions"]["reader_power_included"])
        self.assertFalse(report["limits"]["hardware_approved"])
        self.assertFalse(report["limits"]["battery_bms_connected"])
        self.assertFalse(report["limits"]["dock_modified"])

    def test_scenario_rejects_bool_nan_inf_and_invalid_ranges(self):
        cases = (
            ("idle_mw", True), ("burst_mw", float("nan")),
            ("cap_esr_ohm", float("inf")), ("field_duty_off", 1.1),
            ("cap_retention", 0.0), ("burst_ms", 1000.0),
        )
        for field, bad in cases:
            scenario = dict(SCENARIO)
            scenario[field] = bad
            with self.subTest(field=field, bad=bad):
                with self.assertRaises(ValueError):
                    validate_scenario(scenario)

    def test_report_is_strict_json_and_deterministic(self):
        first = build_report(self.rows)
        second = build_report(self.rows)
        encoded = json.dumps(first, sort_keys=True, allow_nan=False)
        self.assertEqual(encoded, json.dumps(second, sort_keys=True, allow_nan=False))
        self.assertIn('"milestone": "W-IND-104"', encoded)

    def test_constant_power_esr_solver_rejects_no_real_solution(self):
        result = simulate_point(self.row, dict(SCENARIO, cap_esr_ohm=1000.0))
        self.assertFalse(result["checks"]["terminal_voltage_after_esr"])

if __name__ == "__main__":
    unittest.main()
