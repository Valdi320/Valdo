"""Deterministic paper-only negative tests. No hardware, external network or GPL code."""
import copy
from decimal import Decimal
import json
import tempfile
from pathlib import Path
import unittest
from wpt_pair_screen import (load_catalog,cost_bounds_eur,screen_pair,report,InvalidCatalog,MANDATORY_PHYSICAL_GATES)

PATH=Path(__file__).with_name('WPT_PAIR_CATALOG_W_IND_05.json')

class QualificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cat=load_catalog(PATH)
        cls.dfr,cls.qi=cls.cat['candidates']

    def test_two_different_pairs(self): self.assertNotEqual(self.dfr['id'],self.qi['id'])
    def test_fixture_paper_power_fits_both(self):
        self.assertTrue(all(screen_pair(self.cat,p)['paper_fit_at_nominal_only'] for p in (self.dfr,self.qi)))
    def test_low_power_pilot_not_motor(self): self.assertEqual(self.cat['pilot']['peak_power_w'],1.5)
    def test_dfr_price_floor(self): self.assertEqual(cost_bounds_eur(self.cat,self.dfr), (Decimal('22.00'),Decimal('22.00')))
    def test_qi_price_conflict_preserved(self): self.assertEqual(cost_bounds_eur(self.cat,self.qi),(Decimal('64.50'),Decimal('75.00')))
    def test_five_pair_minimum_spend(self):
        self.assertEqual(cost_bounds_eur(self.cat,self.dfr,5),(Decimal('60.00'),Decimal('60.00')))
        self.assertEqual(cost_bounds_eur(self.cat,self.qi,5),(Decimal('260.00'),Decimal('312.50')))
    def test_qty_zero_rejected(self):
        with self.assertRaises(ValueError): cost_bounds_eur(self.cat,self.dfr,0)
    def test_qty_boolean_rejected(self):
        with self.assertRaises(ValueError): cost_bounds_eur(self.cat,self.dfr,True)
    def test_qty_negative_rejected(self):
        with self.assertRaises(ValueError): cost_bounds_eur(self.cat,self.dfr,-2)
    def test_bad_peak_load_rejected(self):
        for val in (0,-1,float('nan'),float('inf'),True):
            with self.subTest(val=val),self.assertRaises(ValueError): screen_pair(self.cat,self.dfr,load_w=val)
    def test_bad_gap_rejected(self):
        for val in (0,-1,float('nan'),True):
            with self.subTest(val=val),self.assertRaises(ValueError): screen_pair(self.cat,self.qi,required_gap_mm=val)
    def test_nominal_limit_at_gap_not_physical_proof(self):
        obj=screen_pair(self.cat,self.dfr,required_gap_mm=11.0)
        self.assertFalse(obj['paper_fit_at_nominal_only'])
        self.assertFalse(obj['installation_approved'])
    def test_overpower_not_approved(self):
        obj=screen_pair(self.cat,self.qi,load_w=3.0)
        self.assertFalse(obj['paper_fit_at_nominal_only'])
    def test_no_installation_even_paper_fit(self):
        for pair in (self.dfr,self.qi):
            x=screen_pair(self.cat,pair)
            self.assertFalse(x['installation_approved'])
            self.assertFalse(x['physical_bench_approved'])
    def test_full_independent_gates_unmet(self):
        for p in (self.dfr,self.qi):
            self.assertEqual(tuple(screen_pair(self.cat,p)['safety_gates_missing']),MANDATORY_PHYSICAL_GATES)
    def test_qi_rx_chip_fod_not_tx_proof(self):
        self.assertFalse(self.qi['tx_fod_physical_verified'])
        self.assertTrue(any('NOT demonstrate' in x for x in self.qi['limitations']))
    def test_false_thermal_approval_prevented(self):
        p=copy.deepcopy(self.qi)
        p['tx_thermal_cut_physical_verified']=True
        self.assertFalse(screen_pair(self.cat,p)['installation_approved'])
    def test_positive_claims_not_accepted_as_real_measurements(self):
        x=screen_pair(self.cat,self.dfr)
        self.assertTrue(x['warn_no_output_voltage_tolerance_guarantee'])
        self.assertIn('not_measured',str(x))
    def test_bad_price_nan_rejected(self):
        p=copy.deepcopy(self.dfr);p['prices_eur_vat_incl']=['NaN']
        with self.assertRaises(InvalidCatalog): cost_bounds_eur(self.cat,p)
    def test_bad_price_more_than_2_decimals_rejected(self):
        p=copy.deepcopy(self.dfr);p['prices_eur_vat_incl']=['1.005']
        with self.assertRaises(InvalidCatalog): cost_bounds_eur(self.cat,p)
    def test_bad_negative_price_rejected(self):
        p=copy.deepcopy(self.dfr);p['prices_eur_vat_incl']=['-1']
        with self.assertRaises(InvalidCatalog): cost_bounds_eur(self.cat,p)
    def test_bad_quote_number_not_string_rejected(self):
        p=copy.deepcopy(self.dfr);p['prices_eur_vat_incl']=[9.5]
        with self.assertRaises(InvalidCatalog): cost_bounds_eur(self.cat,p)
    def test_invalid_flag_rejected(self):
        obj=copy.deepcopy(self.cat);obj['candidates'][1].pop('tx_fod_physical_verified')
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/'test.json';f.write_text(json.dumps(obj))
            with self.assertRaises(InvalidCatalog):load_catalog(f)
    def test_duplicate_id_rejected(self):
        obj=copy.deepcopy(self.cat);obj['candidates'][1]['id']=obj['candidates'][0]['id']
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/'test.json';f.write_text(json.dumps(obj))
            with self.assertRaises(InvalidCatalog):load_catalog(f)
    def test_report_never_grants_installation(self):
        r=report(PATH)
        self.assertEqual(r['selection_for_installation'],'NONE')
        self.assertEqual(r['physical_tests'],0)
        self.assertTrue(all(x['installation_approved'] is False for x in r['screened']))
        self.assertIn('deferred',r['domains']['dock_battery'])
    def test_actual_shipping_not_falsely_claimed(self): self.assertFalse(report(PATH)['vendor_price_is_order_quote'])

if __name__=='__main__': unittest.main()
