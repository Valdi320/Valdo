"""Synthetic adversarial W-IND-28 checks; no hardware tests."""
from dataclasses import replace
import json
import unittest
from stage_current_envelope import Pilot, input_current, evaluate, report

class Tests(unittest.TestCase):
    def setUp(self):
        self.p=Pilot()
        self.a=evaluate()

    def test_power_rx(self):
        self.assertAlmostEqual(self.a["rx_healthy_output_power_w"],1.5)
        self.assertAlmostEqual(self.a["rx_fault_output_power_w"],2.0)

    def test_good_input_min(self):
        self.assertAlmostEqual(self.a["tx_healthy_input_current_a"]["minimum"],1.5/(5*.9))

    def test_good_input_max(self):
        self.assertAlmostEqual(self.a["tx_healthy_input_current_a"]["maximum"],1.5/(5*.55))

    def test_fault_input_min(self):
        self.assertAlmostEqual(self.a["tx_fault_input_current_a"]["minimum"],2/(5*.9))

    def test_fault_input_max(self):
        self.assertAlmostEqual(self.a["tx_fault_input_current_a"]["maximum"],2/(5*.55))

    def test_disjoint_window_impossible_at_55(self):
        self.assertFalse(self.a["tx_can_separate_rx_current_states_with_one_trip"])
        self.assertLess(self.a["tx_trip_window_width_a"],0)

    def test_rx_nominal_candidate_separates(self):
        self.assertEqual(self.a["receiver_nominal_candidate_window_a"],
                         {"must_be_greater_than":.3,"must_be_at_most":.4})

    def test_old_threshold_causes_false_tx_trip(self):
        self.assertTrue(self.a["former_346p4ma_trip_inevitably_falsely_blocks_some_good_TX_cases"])
        self.assertAlmostEqual(self.a["good_TX_current_at_75_percent_efficiency_a"],.4)

    def test_needed_efficiency_0p675(self):
        self.assertAlmostEqual(self.a["ideal_required_min_eta_to_separate_without_aux"],.675)

    def test_positive_control_at_eta_80(self):
        self.assertTrue(evaluate(replace(self.p,eta_min=.8))
                        ["tx_can_separate_rx_current_states_with_one_trip"])

    def test_boundary_below(self):
        self.assertFalse(evaluate(replace(self.p,eta_min=.674))
                         ["tx_can_separate_rx_current_states_with_one_trip"])

    def test_boundary_above(self):
        self.assertTrue(evaluate(replace(self.p,eta_min=.676))
                        ["tx_can_separate_rx_current_states_with_one_trip"])

    def test_more_aux_uncertainty_worsens(self):
        other=evaluate(replace(self.p,auxiliary_max_w=.05))
        self.assertLess(other["tx_trip_window_width_a"],self.a["tx_trip_window_width_a"])

    def test_fixed_aux_does_not_change_width(self):
        other=evaluate(replace(self.p,auxiliary_min_w=.05,auxiliary_max_w=.05))
        self.assertAlmostEqual(other["tx_trip_window_width_a"],self.a["tx_trip_window_width_a"])

    def test_energy_conservation(self):
        for eta in (.55,.65,.75,.9,1.):
            i=input_current(self.p,.3,eta)
            self.assertAlmostEqual(i*5*eta,1.5)

    def test_efficiency_monotonic(self):
        values=[input_current(self.p,.3,x) for x in (.55,.70,.80,.90)]
        self.assertTrue(all(a>b for a,b in zip(values,values[1:])))

    def test_load_monotonic(self):
        self.assertLess(input_current(self.p,.3,.75),input_current(self.p,.4,.75))

    def test_aux_increases_tx_current(self):
        self.assertAlmostEqual(input_current(self.p,.3,.75,.05)-
                               input_current(self.p,.3,.75),.01)

    def test_tx_is_not_rx(self):
        self.assertNotAlmostEqual(input_current(self.p,.3,.75),.3)

    def test_100_percent_efficiency_has_window(self):
        self.assertTrue(evaluate(Pilot(eta_min=1,eta_max=1))
                        ["tx_can_separate_rx_current_states_with_one_trip"])

    def test_reject_invalid_eta(self):
        for kwargs in ({"eta_min":0},{"eta_min":-.5},{"eta_max":1.1},
                       {"eta_min":.95},{"eta_max":.1}):
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):
                evaluate(replace(self.p,**kwargs))

    def test_reject_invalid_current(self):
        for kwargs in ({"rx_good_peak_a":0},{"rx_fault_min_a":.2},
                       {"rx_fault_min_a":-1}):
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):
                evaluate(replace(self.p,**kwargs))

    def test_reject_invalid_voltage_aux(self):
        for kwargs in ({"tx_input_v":0},{"rx_output_v":-5},
                       {"auxiliary_min_w":-1},{"auxiliary_min_w":.1}):
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):
                evaluate(replace(self.p,**kwargs))

    def test_nan_inf(self):
        for value in (float("nan"),float("inf"),float("-inf")):
            with self.subTest(value=value),self.assertRaises(ValueError):
                evaluate(replace(self.p,eta_min=value))

    def test_invalid_call_inputs(self):
        for r,eta,aux in [(-1,.5,0),(.3,0,0),(.3,1.1,0),
                          (.3,.8,-1),(.3,float("nan"),0),(True,.8,0)]:
            with self.subTest(r=r,eta=eta,aux=aux),self.assertRaises(ValueError):
                input_current(self.p,r,eta,aux)

    def test_broad_grid(self):
        for low in (.50,.60,.70,.80,.90):
            for high in (.90,.95,1):
                s=evaluate(replace(self.p,eta_min=low,eta_max=high))
                self.assertAlmostEqual(s["tx_trip_window_width_a"],
                                       (2/high-1.5/low)/5)

    def test_no_hardware_claim(self):
        for k in ("location_of_shunt_selected",
                  "independent_primary_fod_thermal_trip_qualified",
                  "receiver_brownout_failure_qualified","radio_used_for_safety_stop",
                  "lithium_or_dock_connected","power_on_approved"):
            self.assertFalse(self.a[k])
        self.assertEqual(self.a["real_tests"],0)

    def test_json_roundtrip(self):
        self.assertEqual(json.loads(json.dumps(report())),report())

if __name__=="__main__":
    unittest.main()
