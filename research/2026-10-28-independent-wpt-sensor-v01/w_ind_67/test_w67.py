"""W67 synthetic DC-topology regression. Original W code; Codex A02 diagnosed the defect."""
import itertools
import unittest
from dataclasses import replace
from tx_cut_power_screen import Fault, Interlocks, Switch, evaluate


def all_permitted():
    return Interlocks(**{name: True for name in Interlocks.__dataclass_fields__})


class PhysicalSupplyVsPermission(unittest.TestCase):
    def test_denied_monitor_does_not_invent_absent_voltage(self):
        model = evaluate(Interlocks(), Switch(Fault.CLOSED), Switch(Fault.CLOSED))
        self.assertFalse(model.command_on)
        self.assertTrue(model.supply_to_tx)

    def test_source_ok_denied_still_energized_if_both_welded(self):
        i = replace(all_permitted(), source_ok=False)
        out = evaluate(i, Switch(Fault.CLOSED), Switch(Fault.CLOSED), supply_present=True)
        self.assertFalse(out.command_on)
        self.assertTrue(out.supply_to_tx)

    def test_only_explicit_absent_source_zeroes_forward_supply(self):
        a, b = Switch(Fault.CLOSED, True), Switch(Fault.CLOSED, True)
        present = evaluate(Interlocks(), a, b, supply_present=True)
        absent = evaluate(Interlocks(), a, b, supply_present=False)
        self.assertTrue(present.supply_to_tx)
        self.assertTrue(present.any_sustained_qod_shunt)
        self.assertFalse(absent.supply_to_tx)
        self.assertFalse(absent.any_sustained_qod_shunt)

    def test_all_nine_denied_permissions_cannot_hide_double_weld(self):
        for name in Interlocks.__dataclass_fields__:
            with self.subTest(permission=name):
                i = replace(all_permitted(), **{name: False})
                out = evaluate(i, Switch(Fault.CLOSED), Switch(Fault.CLOSED))
                self.assertFalse(out.command_on)
                self.assertTrue(out.supply_to_tx)

    def test_welded_a_with_qod_produces_shunt_despite_source_monitor(self):
        out = evaluate(Interlocks(), Switch(Fault.CLOSED, True), Switch())
        self.assertFalse(out.supply_to_tx)
        self.assertTrue(out.supply_to_qod_a)

    def test_no_source_does_not_assert_output_capacitance_safe(self):
        out = evaluate(Interlocks(), Switch(Fault.CLOSED), Switch(Fault.CLOSED),
                       supply_present=False)
        self.assertFalse(out.supply_to_tx)
        self.assertFalse(out.command_on)

    def test_single_weld_is_isolated_by_healthy_off_other_switch(self):
        for side in ("A", "B"):
            with self.subTest(side=side):
                a, b = ((Switch(Fault.CLOSED), Switch()) if side == "A"
                        else (Switch(), Switch(Fault.CLOSED)))
                self.assertFalse(evaluate(Interlocks(), a, b).supply_to_tx)

    def test_both_enable_pins_stuck_high_still_unsafe(self):
        out = evaluate(Interlocks(), Switch(Fault.ENABLE_HIGH),
                       Switch(Fault.ENABLE_HIGH))
        self.assertTrue(out.supply_to_tx)

    def test_full_sixteen_fault_grid_with_monitor_denied(self):
        for a, b in itertools.product(Fault, repeat=2):
            with self.subTest(a=a, b=b):
                result = evaluate(Interlocks(), Switch(a), Switch(b))
                should_conduct = a in (Fault.CLOSED, Fault.ENABLE_HIGH) and b in (
                    Fault.CLOSED, Fault.ENABLE_HIGH)
                self.assertEqual(result.supply_to_tx, should_conduct)
                self.assertFalse(result.command_on)

    def test_all_valid_bool_combinations_pass_exact_types(self):
        for source_ok, supply_present in itertools.product((False, True), repeat=2):
            with self.subTest(source_ok=source_ok, supply=supply_present):
                i = replace(all_permitted(), source_ok=source_ok)
                out = evaluate(i, Switch(), Switch(), supply_present=supply_present)
                self.assertEqual(out.supply_to_tx, source_ok and supply_present)

    def test_all_nine_permissions_reject_truthy_nonbool_values(self):
        for name in Interlocks.__dataclass_fields__:
            for bad in (1, "false", None, 0):
                with self.subTest(name=name, bad=bad):
                    i = replace(all_permitted(), **{name: bad})
                    with self.assertRaises(ValueError):
                        evaluate(i, Switch(), Switch())

    def test_no_hidden_truthiness_in_supply_present(self):
        for bad in (0, 1, None, "false", "true", 0.0, []):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    evaluate(all_permitted(), Switch(), Switch(), supply_present=bad)

    def test_malformed_switch_inputs_fail(self):
        for sw in (Switch("pass_element_short"), Switch(Fault.CLOSED, 1),
                   Switch(Fault.HEALTHY, "false")):
            with self.subTest(sw=sw):
                with self.assertRaises(ValueError):
                    evaluate(all_permitted(), sw, Switch())

    def test_missing_or_wrong_model_objects_fail(self):
        for i, a, b in (({}, Switch(), Switch()),
                        (Interlocks(), None, Switch()),
                        (Interlocks(), Switch(), "closed")):
            with self.subTest(i=i, a=a, b=b):
                with self.assertRaises(TypeError):
                    evaluate(i, a, b)

    def test_valid_no_fault_keeps_both_off_on_denied_permission(self):
        out = evaluate(Interlocks(), Switch(), Switch())
        self.assertFalse(out.command_on)
        self.assertFalse(out.supply_to_tx)
        self.assertFalse(out.any_sustained_qod_shunt)

    def test_qod_unconnected_does_not_make_modelled_shunt(self):
        out = evaluate(Interlocks(), Switch(Fault.CLOSED, False),
                       Switch(Fault.CLOSED, False))
        self.assertTrue(out.supply_to_tx)
        self.assertFalse(out.any_sustained_qod_shunt)

    def test_fod_true_only_fixture_not_proof(self):
        i = replace(all_permitted(), fod_proven_clear=True)
        out = evaluate(i, Switch(), Switch())
        self.assertTrue(out.command_on)
        self.assertTrue(out.supply_to_tx)


if __name__ == "__main__":
    unittest.main()
