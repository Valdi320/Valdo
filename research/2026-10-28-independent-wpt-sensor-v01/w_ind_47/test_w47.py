"""Original deterministic tests for cost and no-load energy bounds."""
import unittest
from decimal import Decimal
from w47_cost_gate import evaluate, report

class TestW47(unittest.TestCase):
    def test_one_module_shipping_floor_can_reverse_ranking(self):
        x=evaluate(1,0,30)
        self.assertEqual(x["difference_with_shipping_floors_eur"], "-3.13")
        self.assertFalse(x["cost_complete"])
    def test_two_modules_shipping_floors(self):
        self.assertEqual(evaluate(2,0,30)["difference_with_shipping_floors_eur"], "2.29")
    def test_eight_modules_shipping_floors(self):
        self.assertEqual(evaluate(8,0,30)["difference_with_shipping_floors_eur"], "34.81")
    def test_unit_price_penalty(self):
        self.assertEqual(evaluate(1,0,30)["wpt_items_minus_wired_items_eur"], "5.42")
    def test_eight_unit_price_penalty(self):
        self.assertEqual(evaluate(8,0,30)["wpt_items_minus_wired_items_eur"], "43.36")
    def test_eight_idle_upper_wh(self):
        self.assertEqual(Decimal(evaluate(8,24,50)["idle_energy_wh_per_day_hypothetical"]),Decimal("48"))
    def test_eight_idle_lower_wh(self):
        self.assertEqual(Decimal(evaluate(8,24,30)["idle_energy_wh_per_day_hypothetical"]),Decimal("28.8"))
    def test_one_idle_upper_wh(self):
        self.assertEqual(Decimal(evaluate(1,24,50)["idle_energy_wh_per_day_hypothetical"]),Decimal("6"))
    def test_two_hours_idle(self):
        self.assertEqual(Decimal(evaluate(1,2,30)["idle_energy_wh_per_day_hypothetical"]),Decimal("0.3"))
    def test_no_receiver_absence_zero(self):
        self.assertEqual(Decimal(evaluate(8,0,50)["idle_energy_wh_per_day_hypothetical"]),Decimal("0"))
    def test_no_dock_or_radio_claim(self):
        x=evaluate(2,2,50)
        self.assertFalse(x["radio_esp_now_or_openthread_included"])
        self.assertFalse(x["battery_dock_included"])
    def test_no_safety_approval(self):
        for n in (1,2,4,8):
            x=evaluate(n,24,50)
            self.assertFalse(x["safety_fod_thermal_independent_cut_included"])
            self.assertFalse(x["wpt_production_authorized"])
    def test_functionality_not_comparable(self):
        self.assertFalse(evaluate(1,0,30)["equivalent_functionality"])
    def test_bad_modules(self):
        for n in (0,-1,1.5):
            with self.assertRaises(ValueError): evaluate(n,0,30)
    def test_bad_time(self):
        for h in (-0.001,24.01):
            with self.assertRaises(ValueError): evaluate(1,h,30)
    def test_bad_current(self):
        with self.assertRaises(ValueError): evaluate(1,1,-1)
    def test_complete_matrix(self):
        r=report()
        self.assertEqual(len(r["cases"]),24)
        self.assertEqual(r["evidence_type"],"CATALOG_PRICE_SNAPSHOTS_PLUS_SYNTHETIC_ARITHMETIC_NOT_HARDWARE")
    def test_all_results_blocked(self):
        self.assertTrue(all(not x["wpt_production_authorized"] for x in report()["cases"]))
    def test_prices_are_catalog_not_local_stock(self):
        self.assertIn("NOT verified",report()["noncomparable_notice"])
    def test_diotronic_partial_not_equivalent(self):
        r=report()["unit_price_snapshot_eur_incl_vat"]
        self.assertEqual(Decimal(r["diotronic_2pin_partial_without_contacts_wires"]),Decimal("0.54"))

if __name__=="__main__":
    unittest.main()
