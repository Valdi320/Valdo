"""W-IND-43: synthetic/datasheet-derived tests; NOT a hardware safety test."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from w43_por_gate import (Inputs, outb_possible_states, threshold_bounds,
                         gate_bias, evaluate, evidence, main)


class W43ThresholdTests(unittest.TestCase):
    def test_nominal_divider(self):
        self.assertAlmostEqual(.4 * (1 + 63400/10000), 2.936)

    def test_worst_case_threshold_bounds(self):
        lo, hi = threshold_bounds()
        self.assertAlmostEqual(lo, 2.7941583564356436, places=8)
        self.assertAlmostEqual(hi, 3.0811389898989897, places=6)

    def test_below_2p7_disqualified(self):
        self.assertGreater(threshold_bounds(falling=True)[0], 2.7)

    def test_legacy_w41_hysteresis_counterexample(self):
        # W41 assessed only rising 396-404mV. A brownout can persist
        # in healthy OUTB SINK until *falling* 387mV min, below 2.70V.
        self.assertGreater(threshold_bounds(rtop=62000)[0], 2.7)
        self.assertLess(threshold_bounds(rtop=62000, falling=True)[0], 2.7)
        self.assertEqual(outb_possible_states(5, 2.7, rtop=62000), ('hiz','sink'))

    def test_candidate_63400_falling_clears_at_2p7(self):
        self.assertGreater(threshold_bounds(rtop=63400, falling=True)[0], 2.7)
        self.assertEqual(outb_possible_states(5,2.7), ('hiz',))
        self.assertGreater(3.135 - threshold_bounds(rtop=63400)[1], 0)

    def test_midrange_64900_can_miss_normal_at_3p135(self):
        self.assertGreater(threshold_bounds(rtop=64900)[1], 3.135)

    def test_sensitivity_fails_if_input_perturbation_exceeds_1p5ua(self):
        self.assertLess(threshold_bounds(i_error_a=1.5e-6,falling=True)[0], 2.7)
        self.assertGreater(threshold_bounds(i_error_a=1e-6,falling=True)[0], 2.7)

    def test_above_3p135_qualified_only_when_powered(self):
        self.assertLess(threshold_bounds()[1], 3.135)

    def test_bad_divider_rejected(self):
        for args in [(-1, 10), (10, 0)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                threshold_bounds(rtop=args[0], rbot=args[1])

    def test_negative_injection_rejected(self):
        with self.assertRaises(ValueError):
            threshold_bounds(i_error_a=-1)


class W43GateTests(unittest.TestCase):
    def x(self, vdd=5, sensed=3.3, **kwargs):
        return Inputs(receiver_supply_5v=True, monitor_vdd=vdd, sensed_3v3=sensed, **kwargs)

    def test_healthy_rail_sinks_outb_and_enables_ideal_health(self):
        self.assertTrue(evaluate(self.x())['could_request_on'])

    def test_undervoltage_tristate_and_off(self):
        self.assertTrue(evaluate(self.x(sensed=2.7))['guaranteed_off'])

    def test_broken_outb_gate_pullup_off(self):
        self.assertTrue(evaluate(self.x(outb_open=True))['guaranteed_off'])

    def test_broken_health_wire_receiver_pulldown_off(self):
        self.assertTrue(evaluate(self.x(health_wire_open=True))['guaranteed_off'])

    def test_no_receiver_source_off(self):
        self.assertTrue(evaluate(Inputs(False, 5.0, 3.3))['guaranteed_off'])

    def test_no_local_arm_off(self):
        self.assertTrue(evaluate(self.x(locally_armed=False))['guaranteed_off'])

    def test_independent_interlock_off(self):
        self.assertTrue(evaluate(self.x(independent_interlocks_ok=False))['guaranteed_off'])

    def test_undervoltage_bad_stuck_gate_to_ground_unsafe(self):
        self.assertTrue(evaluate(self.x(sensed=0, gate_stuck_ground=True))['unsafe_possible'])

    def test_health_wire_hard_short_to_5v_unsafe(self):
        self.assertTrue(evaluate(self.x(sensed=0, health_short_to_5v=True))['unsafe_possible'])

    def test_monitor_vdd_below_por_indeterminate_and_unsafe_possible(self):
        y = evaluate(self.x(vdd=0.4, sensed=0))
        self.assertTrue(y['uncertainty'])
        self.assertTrue(y['unsafe_possible'])

    def test_monitor_vdd_in_guaranteed_uvlo_hiz_off(self):
        y = evaluate(self.x(vdd=1.0, sensed=0))
        self.assertTrue(y['guaranteed_off'])
        self.assertFalse(y['uncertainty'])

    def test_monitor_vdd_1p5_not_qualified(self):
        self.assertTrue(evaluate(self.x(vdd=1.5, sensed=0))['unsafe_possible'])

    def test_permanent_vdd0_is_not_safely_assumed_off(self):
        self.assertFalse(evaluate(self.x(vdd=0, sensed=0))['guaranteed_off'])

    def test_outb_open_defeats_uncertain_sink_if_no_other_fault(self):
        self.assertTrue(evaluate(self.x(vdd=0.4, sensed=0, outb_open=True))['guaranteed_off'])

    def test_receiver_open_can_not_be_bypassed_by_gate_short(self):
        self.assertTrue(evaluate(self.x(health_wire_open=True, gate_stuck_ground=True))['guaranteed_off'])

    def test_source_not_present_remains_off_even_stuck_output(self):
        x=Inputs(False, 0.4, 0, health_short_to_5v=True)
        self.assertTrue(evaluate(x)['guaranteed_off'])

    def test_unknown_near_threshold(self):
        self.assertTrue(evaluate(self.x(sensed=2.88))['uncertainty'])

    def test_rail_3p3_lost_even_with_vdd5_safely_off_ideal(self):
        self.assertTrue(evaluate(self.x(vdd=5, sensed=0))['guaranteed_off'])

    def test_two_permissions_enforced_at_receiver(self):
        self.assertTrue(evaluate(self.x(locally_armed=False, independent_interlocks_ok=False))['guaranteed_off'])

    def test_bool_inputs_strict(self):
        with self.assertRaises(TypeError):
            Inputs(1, 5, 3.3)

    def test_invalid_vdd_and_3v3(self):
        for vdd, rail in [(-1, 3.3), (19, 3.3), (5, 5.6)]:
            with self.subTest(vdd=vdd, rail=rail), self.assertRaises(ValueError):
                Inputs(True, vdd, rail)

    def test_gate_sink_current_screen_below_5ma_datasheet(self):
        z=gate_bias()
        self.assertLess(z['gate_sinking_current_upper_ma_at_gate_zero'],5.0)
        self.assertAlmostEqual(z['gate_sinking_current_upper_ma_at_gate_zero'],5/22,places=6)

    def test_gate_sink_and_receiver_load_power(self):
        z=gate_bias()
        self.assertAlmostEqual(z['gate_pullup_dissipation_upper_mw'],25/22,places=6)
        self.assertAlmostEqual(z['health_receiver_dissipation_if_high_mw'],25/47,places=6)

    def test_gate_leakage_is_not_por_guarantee(self):
        z=gate_bias()
        self.assertAlmostEqual(z['gate_to_source_bias_from_hypothetical_hiz_leak_mv'],6.6)
        self.assertFalse(z['pmos_turnon_and_receiver_voltage_qualified'])

    def test_gate_invalid_inputs(self):
        for kw in ({'source_5v':-1},{'gate_pullup_ohm':0},{'receiver_pulldown_ohm':0},{'hypothetical_hiz_leak_a':-1}):
            with self.subTest(kw=kw), self.assertRaises(ValueError):
                gate_bias(**kw)

    def test_datasheet_outb_states(self):
        self.assertEqual(outb_possible_states(5,3.3), ('sink',))
        self.assertEqual(outb_possible_states(5,2.7), ('hiz',))
        self.assertEqual(outb_possible_states(1.,0), ('hiz',))
        self.assertEqual(outb_possible_states(.4,0), ('hiz','sink'))

    def test_evidence_is_reproducible(self):
        self.assertEqual(evidence(),evidence())

    def test_evidence_hardware_blocked(self):
        z=evidence()
        self.assertFalse(z['release_for_bench_or_hardware'])
        self.assertFalse(z['lithium_or_real_power_energized'])
        self.assertGreater(z['unsafe_possible_cases'],0)
        self.assertEqual(z['cases'], 1536)
        self.assertLess(z['legacy_w41_failing_bad_rail_margin_v'], 0)
        self.assertGreater(z['candidate_min_bad_rail_margin_v'], 0)
        self.assertGreater(z['candidate_min_good_rail_margin_v'], 0)

    def test_evidence_includes_counterexamples(self):
        z=evidence()
        self.assertTrue(any(t['monitor_vdd']<0.8 and t['sensed_3v3']<=2.7 for t in z['unsafe_examples']))

    def test_cli_json(self):
        with tempfile.TemporaryDirectory() as td:
            fn=Path(td)/'evidence.json'
            with patch('sys.argv',['w43_por_gate.py','--out',str(fn)]):
                main()
            self.assertEqual(json.loads(fn.read_text())['schema'],'VALDO_W_IND_43_POR_AWARE_OUTB_PMOS_V1')


if __name__ == '__main__':
    unittest.main()
