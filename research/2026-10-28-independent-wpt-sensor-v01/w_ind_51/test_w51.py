"""Deterministic tests, no electronics or network access."""
import unittest
from dataclasses import replace
from w51_cost_metrology_gate import D, Offer, price_gate, shunt_screen, compare_qualified_prices, demo


class PriceTests(unittest.TestCase):
    def setUp(self):
        self.good = Offer("X", "Seller", "4.00", "3.00", "0", vat_verified=True,
                          seller_stock_verified=True, shunt_traceable=True, calibrated_pair=True,
                          min_order_qty=1, fixture_gross_eur="2", calibration_gross_eur="5",
                          delivery_to_zaragoza_verified=True)

    def test_landed_pair(self):
        self.assertEqual(price_gate(self.good)["pair_delivered_gross_eur"], "18.00")

    def test_no_hardware_approval_even_if_qualified(self):
        self.assertFalse(price_gate(self.good)["hardware_approved"])

    def test_shipment_unknown_blocks(self):
        p = price_gate(replace(self.good, shipping_gross_eur=None))
        self.assertFalse(p["ready_for_cost_comparison"])
        self.assertIsNone(p["pair_delivered_gross_eur"])
        self.assertEqual(p["pair_gross_floor_eur"], "8.00")

    def test_minimum_order_quantity_changes_cost(self):
        p = price_gate(replace(self.good, min_order_qty=5))
        self.assertEqual(p["pair_gross_floor_eur"], "20.00")
        self.assertEqual(p["pair_delivered_gross_eur"], "30.00")

    def test_moq_unknown_blocks(self):
        self.assertFalse(price_gate(replace(self.good, min_order_qty=None))["ready_for_cost_comparison"])

    def test_zaragoza_delivery_unknown_blocks(self):
        self.assertFalse(price_gate(replace(self.good, delivery_to_zaragoza_verified=False))["ready_for_cost_comparison"])

    def test_fixture_or_calibration_cost_unknown_blocks(self):
        for name in ("fixture_gross_eur", "calibration_gross_eur"):
            with self.subTest(name=name):
                self.assertFalse(price_gate(replace(self.good, **{name: None}))["ready_for_cost_comparison"])

    def test_vat_unknown_blocks_floor(self):
        p = price_gate(replace(self.good, vat_verified=False))
        self.assertIsNone(p["pair_gross_floor_eur"])
        self.assertFalse(p["ready_for_cost_comparison"])

    def test_stock_unknown_blocks(self):
        self.assertFalse(price_gate(replace(self.good, seller_stock_verified=False))["ready_for_cost_comparison"])

    def test_shunt_unqualified_blocks(self):
        self.assertFalse(price_gate(replace(self.good, shunt_traceable=False))["ready_for_cost_comparison"])

    def test_calibration_missing_blocks(self):
        self.assertFalse(price_gate(replace(self.good, calibrated_pair=False))["ready_for_cost_comparison"])

    def test_bare_mounting_unknown_blocks(self):
        self.assertFalse(price_gate(replace(self.good, mounting_gross_eur=None))["ready_for_cost_comparison"])

    def test_minimum_two_meters(self):
        for n in (0, 1, -1, True):
            with self.subTest(n=n), self.assertRaises(ValueError):
                price_gate(replace(self.good, quantity=n))

    def test_price_guards(self):
        for field, bad in (("unit_price_gross_eur", "NaN"),
                           ("shipping_gross_eur", "-1"),
                           ("mounting_gross_eur", "Infinity")):
            with self.subTest(field=field), self.assertRaises(ValueError):
                price_gate(replace(self.good, **{field: bad}))

    def test_identifiable_product(self):
        with self.assertRaises(ValueError):
            price_gate(replace(self.good, sku=" "))

    def test_unconfirmed_zaragoza_separate_from_global_stock(self):
        p = price_gate(self.good)
        self.assertTrue(p["ready_for_cost_comparison"])
        self.assertFalse(p["stock_in_zaragoza_confirmed"])

    def test_price_comparison_known(self):
        b = replace(self.good, sku="Y", unit_price_gross_eur="5")
        self.assertEqual(compare_qualified_prices(self.good, b)["winner"], "X")
        self.assertEqual(compare_qualified_prices(self.good, b)["difference_eur"], "2.00")

    def test_price_tie(self):
        self.assertEqual(compare_qualified_prices(self.good, replace(self.good, sku="Y"))["winner"], "tie")

    def test_price_comparison_unknown(self):
        p = compare_qualified_prices(self.good, replace(self.good, shipping_gross_eur=None))
        self.assertIsNone(p["winner"])


class ShuntTests(unittest.TestCase):
    def f(self, **kwargs):
        params = dict(current_min_a="0.08", current_peak_a="0.30", shunt_ohm="0.1",
                      shunt_fsr_v="0.04", offset_uv="50", quantization_half_lsb_uv="5",
                      shunt_tolerance_pct="1", gain_error_pct="0.5", max_current_error_pct="3")
        params.update(kwargs)
        return shunt_screen(**params)

    def test_80ma_drop(self):
        self.assertEqual(self.f()["shunt_v_at_min"], "0.008")

    def test_peak_drop_fits_40mv(self):
        self.assertEqual(self.f()["shunt_v_at_peak"], "0.030")
        self.assertTrue(self.f()["peak_fits_selected_pga"])

    def test_min_power(self):
        self.assertEqual(self.f()["shunt_loss_w_at_min"], "0.00064")

    def test_peak_power(self):
        self.assertEqual(self.f()["shunt_loss_w_at_peak"], "0.00900")

    def test_bound_100mohm(self):
        self.assertEqual(self.f()["hypothetical_current_error_bound_pct"], "2.187500")
        self.assertTrue(self.f()["passes_hypothetical_budget"])

    def test_10mohm_fails(self):
        self.assertFalse(self.f(shunt_ohm="0.01")["passes_hypothetical_budget"])

    def test_peak_saturation_fails(self):
        self.assertFalse(self.f(current_peak_a="1")["peak_fits_selected_pga"])

    def test_fractional_budget_fails(self):
        self.assertFalse(self.f(max_current_error_pct="2")["passes_hypothetical_budget"])

    def test_nonpositive_ranges(self):
        for key, value in (("current_min_a", "0"), ("current_peak_a", "0.01"),
                           ("shunt_ohm", "0"), ("shunt_fsr_v", "-1")):
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.f(**{key: value})

    def test_negative_uncertainties(self):
        for key in ("offset_uv", "quantization_half_lsb_uv", "shunt_tolerance_pct", "gain_error_pct"):
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.f(**{key: "-1"})

    def test_nonfinite(self):
        with self.assertRaises(ValueError):
            self.f(current_min_a="NaN")

    def test_never_measurement(self):
        v = self.f()
        self.assertIsNone(v["actual_calibrated_accuracy"])
        self.assertFalse(v["safety_protection_proved"])

    def test_synthetic_label(self):
        d = demo()
        self.assertEqual(d["evidence_kind"], "SYNTHETIC-CATALOG-NOT-HARDWARE")
        self.assertFalse(d["hardware_approved"])
        self.assertTrue(all(p["pair_delivered_gross_eur"] is None for p in d["offers"]))
        self.assertEqual(d["offers"][0]["pair_gross_floor_eur"], "7.26")


if __name__ == "__main__":
    unittest.main()
