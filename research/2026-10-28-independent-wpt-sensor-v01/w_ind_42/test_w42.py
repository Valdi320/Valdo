"""Only idealized digital counterexample and DC calculation; no electronics tested."""
import json
import unittest

from w42_positive_health import (Topology as T, Fault as F, Inputs,
                                 evaluate, health_pin_high, resistor_screen, evidence)


def x(healthy=False, fault=F.NONE, v5=True, armed=True, others=True):
    return Inputs(healthy, v5, armed, others, fault)


class HealthLineTests(unittest.TestCase):
    def test_normal_both_allow(self):
        for t in T:
            with self.subTest(topology=t):
                self.assertTrue(evaluate(t, x(True))['request_on_ideal'])

    def test_dead_rail_both_normal_outputs_trip(self):
        for t in T:
            self.assertFalse(evaluate(t, x())['request_on_ideal'])

    def test_open_line_legacy_danger(self):
        self.assertTrue(evaluate(T.OD_FAULT_LOW_PULLUP, x(fault=F.LINE_OPEN))['unsafe_request_when_rail_bad'])

    def test_open_line_positive_drive_trips(self):
        self.assertFalse(evaluate(T.PP_HEALTH_HIGH_PULLDOWN, x(fault=F.LINE_OPEN))['request_on_ideal'])

    def test_dead_monitor_legacy_danger(self):
        self.assertTrue(evaluate(T.OD_FAULT_LOW_PULLUP, x(fault=F.MONITOR_UNPOWERED))['unobserved_monitor_death'])

    def test_dead_monitor_positive_drive_trips(self):
        self.assertFalse(evaluate(T.PP_HEALTH_HIGH_PULLDOWN, x(fault=F.MONITOR_UNPOWERED))['request_on_ideal'])

    def test_stuck_hiz_legacy_danger(self):
        self.assertTrue(health_pin_high(T.OD_FAULT_LOW_PULLUP, x(fault=F.DRIVER_STUCK_HIZ)))

    def test_stuck_hiz_positive_drive_trips(self):
        self.assertFalse(health_pin_high(T.PP_HEALTH_HIGH_PULLDOWN, x(fault=F.DRIVER_STUCK_HIZ)))

    def test_stuck_high_still_unsafe(self):
        for f in (F.SHORT_TO_HIGH, F.DRIVER_STUCK_HIGH, F.SUPERVISOR_FALSE_HEALTHY):
            self.assertTrue(evaluate(T.PP_HEALTH_HIGH_PULLDOWN, x(fault=f))['unsafe_request_when_rail_bad'])

    def test_short_to_ground_trips(self):
        for t in T:
            self.assertFalse(evaluate(t, x(True, F.SHORT_TO_GND))['request_on_ideal'])

    def test_bad_5v_ideal_gate_disables_even_short_high(self):
        for t in T:
            self.assertFalse(evaluate(t, x(fault=F.SHORT_TO_HIGH, v5=False))['request_on_ideal'])

    def test_disarmed_ideal_gate_disables(self):
        for t in T:
            self.assertFalse(evaluate(t, x(True, F.NONE, armed=False))['request_on_ideal'])

    def test_other_protectors_ideal_gate_disables(self):
        for t in T:
            self.assertFalse(evaluate(t, x(True, others=False))['request_on_ideal'])

    def test_no_coercion_of_string_or_int_permission(self):
        for arg in (dict(rail_3v3_healthy=1), dict(armed_by_local_action='false')):
            data=dict(rail_3v3_healthy=True,precut_5v_qualified=True,
                      armed_by_local_action=True,other_local_interlocks_ok=True)
            data.update(arg)
            with self.assertRaises(TypeError): Inputs(**data)

    def test_fault_type_checked(self):
        with self.assertRaises(TypeError): Inputs(True,True,True,True,'none')

    def test_topology_type_checked(self):
        with self.assertRaises(TypeError): health_pin_high('PP',x())

    def test_hypothetical_open_line_leak_screen(self):
        a=resistor_screen(47000,5.0)
        self.assertAlmostEqual(a['open_wire_high_due_to_leak_volts_hypothetical'], .047)
        self.assertTrue(a['below_hypothetical_low_threshold'])
        self.assertFalse(a['logic_input_and_leakage_characterized'])

    def test_pull_down_tradeoff(self):
        a=resistor_screen(4700,5.0)
        b=resistor_screen(47000,5.0)
        self.assertGreater(a['sourcing_power_mw_ideal'],b['sourcing_power_mw_ideal'])
        self.assertLess(a['open_wire_high_due_to_leak_volts_hypothetical'],b['open_wire_high_due_to_leak_volts_hypothetical'])

    def test_invalid_resistance_rejected(self):
        with self.assertRaises(ValueError):resistor_screen(0,5.)

    def test_all_128_states_per_topology(self):
        e=evidence()
        self.assertEqual([e['enumerated_topologies'][t.value]['enumerated_cases'] for t in T], [128,128])

    def test_reduction_but_not_zero_hazards(self):
        e=evidence()['enumerated_topologies']
        self.assertEqual(e[T.OD_FAULT_LOW_PULLUP.value]['unsafe_requests_3v3_bad'], 6)
        self.assertEqual(e[T.PP_HEALTH_HIGH_PULLDOWN.value]['unsafe_requests_3v3_bad'], 3)

    def test_fail_open_never_implies_approved_hardware(self):
        e=evidence()
        self.assertFalse(e['safe_to_energize'])
        self.assertFalse(e['actual_bench_tested'])
        self.assertTrue(e['not_compatible_with_unmodified_tps3700_outa'])

    def test_repeatable_json(self):
        self.assertEqual(json.dumps(evidence(), sort_keys=True),json.dumps(evidence(), sort_keys=True))


if __name__ == '__main__': unittest.main()
