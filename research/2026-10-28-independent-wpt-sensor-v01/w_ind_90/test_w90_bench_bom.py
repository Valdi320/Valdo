"""W90 original deterministic arithmetic/decision tests; no physical work."""
from dataclasses import replace
import unittest
from decimal import Decimal
from w90_bench_bom import D, MCU, READER, TAG_BOARD, Part, evaluate, report

class BenchBOMTests(unittest.TestCase):
    def test_one_host_partial_board_cost_vat(self):
        x = evaluate((READER, TAG_BOARD, MCU))
        self.assertEqual(x['subtotal_ex_vat_eur'], '69.58')
        self.assertEqual(x['subtotal_inc_21pct_vat_eur'], '84.19')
        self.assertEqual(x['unrounded_vat_inclusive_eur'], '84.1918')
    def test_dual_host_cost_and_moq(self):
        x = report()['two_host_digital_telemetry_demonstrator']
        self.assertEqual(x['subtotal_ex_vat_eur'], '89.86')
        self.assertEqual(x['subtotal_inc_21pct_vat_eur'], '108.73')
        self.assertEqual(x['unrounded_vat_inclusive_eur'], '108.7306')
        self.assertEqual(x['parts'][2]['qty'], 2)
    def test_no_manufacturer_curve_transfer(self):
        x = report()['two_host_digital_telemetry_demonstrator']
        self.assertIn('TAG_BOARD_ST25DV64KC_NOT_W89_ST25DV04KC_DEVICE', x['reject_reasons'])
        self.assertEqual(x['rf_energy_performance'], 'UNMEASURED')
    def test_mcu_is_not_one_for_two_full_firmware_hosts(self):
        x = report()['baseline_one_host_for_reader_tag_board_unprogrammed']
        self.assertIn('TWO_SIDED_APP_FIRMWARE_HOSTS_NOT_COVERED', x['reject_reasons'])
    def test_no_price_claim_is_complete(self):
        for scenario in ('baseline_one_host_for_reader_tag_board_unprogrammed', 'two_host_digital_telemetry_demonstrator'):
            x = report()[scenario]
            self.assertEqual(x['bench_hardware_release'], 'BLOCKED')
            self.assertFalse(x['system_cost_complete'])
    def test_claim_ready_rejected_even_if_flags_supplied(self):
        x = evaluate((READER,TAG_BOARD,replace(MCU,qty=2)), claim_ready=True,
                     exact_w89_tag=True, instrumented=True, independent_cut_tested=True)
        self.assertIn('UNSUPPORTED_HARDWARE_READY_CLAIM', x['reject_reasons'])
        self.assertEqual(x['bench_hardware_release'],'BLOCKED')
    def test_missing_tag_antenna_board_rejected(self):
        x = evaluate((READER,replace(MCU,qty=2)))
        self.assertIn('MISSING_READER_OR_TAG_ANTENNA_EVAL_BOARD', x['reject_reasons'])
    def test_duplicate_sku_rejected(self):
        with self.assertRaises(ValueError): evaluate((MCU,MCU))
    def test_invalid_price_and_stock_provenance_rejected(self):
        for price in ('NaN','Infinity','0','-1','bad'):
            with self.subTest(price=price),self.assertRaises(ValueError):
                evaluate((replace(MCU,unit_eur_ex_vat=price),))
        with self.assertRaises(ValueError): evaluate((replace(MCU,unit_eur_ex_vat=0.5),))
        with self.assertRaises(ValueError): evaluate((replace(MCU,stock_kind='in_stock_zaragoza'),))
        with self.assertRaises(ValueError): evaluate((replace(MCU,url='https://example.com/'),))
    def test_invalid_quantity_rejected(self):
        for q in (0, -1, True, 1.5):
            with self.subTest(q=q), self.assertRaises(ValueError):
                evaluate((replace(MCU,qty=q),))
    def test_no_automatic_purchasing_or_oem_dependency(self):
        x=report()
        self.assertFalse(x['actual_procurement_authorized'])
        self.assertIn('DISCONNECTED',x['battery_BMS_dock'])
        self.assertEqual(x['diotronic_zaragoza_stock'],'NOT_VERIFIED')
    def test_determinism(self):
        self.assertEqual(report(),report())

if __name__=='__main__': unittest.main()
