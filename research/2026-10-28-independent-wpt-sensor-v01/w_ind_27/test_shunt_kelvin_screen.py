"""W-IND-27 adversarial arithmetic regression; synthetic, never hardware."""
from dataclasses import replace
import json
import unittest
from shunt_kelvin_screen import CHEAP,KELVIN,Pilot,calculate,report

class ShuntTests(unittest.TestCase):
    def setUp(self):
        self.a=calculate(CHEAP)
        self.b=calculate(KELVIN)

    def test_parts_and_terminations(self):
        self.assertEqual(CHEAP.terminals,2)
        self.assertEqual(KELVIN.terminals,4)
        self.assertEqual(CHEAP.mpn,'Vishay WSL2512R1000FEA')
        self.assertEqual(KELVIN.mpn,'VPG Y44880R10000F9R')

    def test_vendor_tcr_differ(self):
        self.assertEqual((CHEAP.tempco_ppm_per_c,KELVIN.tempco_ppm_per_c),(75,5))

    def test_nominal_current_loss(self):
        self.assertAlmostEqual(self.a['rshunt_power_at_300ma_w_nominal'],.009)
        self.assertAlmostEqual(self.a['rshunt_power_at_400ma_w_nominal'],.016)
        self.assertAlmostEqual(self.a['shunt_drop_at_400ma_v_nominal'],.04)

    def test_static_two_terminal_five_milliohm(self):
        self.assertTrue(self.a['static_envelope_separates_300ma_and_400ma'])
        self.assertAlmostEqual(self.a['no_false_margin_mv'],13.36656,5)
        self.assertAlmostEqual(self.a['fault_detection_margin_mv'],53.71244,5)

    def test_8milliohm_parasitic_breaks_window(self):
        bad=calculate(replace(CHEAP,sense_extra_max_ohm=.008))
        self.assertFalse(bad['static_envelope_separates_300ma_and_400ma'])
        self.assertLess(bad['no_false_margin_mv'],0)

    def test_critical_parasitic_threshold(self):
        self.assertAlmostEqual(self.a['max_parasitic_to_avoid_false_300ma_ohm_in_model'],.007223313373253493)
        below=calculate(replace(CHEAP,sense_extra_max_ohm=.00722))
        above=calculate(replace(CHEAP,sense_extra_max_ohm=.00723))
        self.assertGreater(below['no_false_margin_mv'],0)
        self.assertLess(above['no_false_margin_mv'],0)

    def test_four_terminal_assumption_not_manufacturer_guarantee(self):
        self.assertTrue(self.b['static_envelope_separates_300ma_and_400ma'])
        self.assertEqual(self.b['parasitic_sense_max_ohm_assumed'],.00005)
        self.assertFalse(self.b['pad_parasitic_measured'])
        self.assertFalse(self.b['pcb_kelvin_layout_verified'])

    def test_four_terminal_cannot_ignore_bad_layout(self):
        bad=calculate(replace(KELVIN,sense_extra_max_ohm=.01))
        self.assertFalse(bad['static_envelope_separates_300ma_and_400ma'])

    def test_gain_and_limit_voltages_reproduce_w26(self):
        self.assertAlmostEqual(self.a['threshold_low_v'],.65865456)
        self.assertAlmostEqual(self.a['threshold_high_v'],.72722256)

    def test_parasitic_increases_false_trip_risk(self):
        m=[calculate(replace(CHEAP,sense_extra_max_ohm=x))['no_false_margin_mv']
           for x in (0,.001,.002,.005,.008,.01)]
        self.assertTrue(all(x>y for x,y in zip(m,m[1:])))

    def test_cannot_assume_zero_pad_error(self):
        zero=calculate(replace(CHEAP,sense_extra_max_ohm=0))
        self.assertGreater(zero['no_false_margin_mv'],self.a['no_false_margin_mv'])
        self.assertFalse(zero['pad_parasitic_measured'])

    def test_cost_ratio(self):
        self.assertGreater(report()['cost_ratio_ex_vat'],30)
        self.assertAlmostEqual(self.a['price_with_es_21pct_vat_eur_calculated'],.6413)
        self.assertAlmostEqual(self.b['price_with_es_21pct_vat_eur_calculated'],19.5052)

    def test_bom_not_local_stock(self):
        self.assertFalse(self.a['diotronic_local_stock_verified'])
        self.assertFalse(self.b['diotronic_local_stock_verified'])

    def test_no_hardware_security_guarantees(self):
        for item in (self.a,self.b):
            self.assertFalse(item['power_on_approved'])
            self.assertFalse(item['independent_cutoff_fod_thermal_verified'])
            self.assertFalse(item['real_comparator_temperature_emi_verified'])
            self.assertFalse(item['lithium_bms_dock_connected'])
            self.assertEqual(item['physical_tests'],0)

    def test_nan_or_inf_rejected(self):
        for v in (float('nan'),float('inf'),float('-inf')):
            with self.subTest(v=v),self.assertRaises(ValueError):
                calculate(replace(CHEAP,sense_extra_max_ohm=v))

    def test_negative_or_wrong_input_rejected(self):
        for opt in (replace(CHEAP,sense_extra_min_ohm=-1),
                    replace(CHEAP,sense_extra_max_ohm=-1),
                    replace(CHEAP,terminals=3),
                    replace(CHEAP,tolerance_fraction=1),
                    replace(CHEAP,unit_price_ex_vat_eur=0),
                    replace(CHEAP,tempco_ppm_per_c=-1)):
            with self.subTest(opt=opt),self.assertRaises(ValueError):calculate(opt)

    def test_invalid_current_order_rejected(self):
        with self.assertRaises(ValueError):calculate(CHEAP,replace(Pilot(),i_fault_min_a=.2))

    def test_nonphysical_temperature_rejected(self):
        with self.assertRaises(ValueError):calculate(CHEAP,replace(Pilot(),temp_excursion_c=120))

    def test_no_claim_about_30_w_dock_or_motors(self):
        for item in (self.a,self.b):
            self.assertNotIn('dock_approved',item)
            self.assertFalse(item['lithium_bms_dock_connected'])

    def test_reproducible_json(self):
        self.assertEqual(json.loads(json.dumps(report())),report())

if __name__=='__main__':unittest.main()
