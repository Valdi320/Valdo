"""W-IND-14 tests. All pass/fail labels are MODEL ONLY, never hardware safety."""
from dataclasses import replace
from itertools import product
import unittest
from tx_offline_diagnostics import BenchHypothesis as H, Verdict, dc_solve, diagnose


class TestTwoPhaseBench(unittest.TestCase):
    def test_healthy_equivalent_resistances_are_only_model_consistent(self):
        r = diagnose(H())
        self.assertEqual(r.verdict, Verdict.MODEL_CONSISTENT)
        self.assertFalse(r.hardware_approved)
        self.assertFalse(r.covers_esd_body_diodes)
        self.assertFalse(r.proves_real_fod)
        self.assertGreater(r.probe.vmid_v, 3.0)
        self.assertLess(r.passive.vmid_v, 0.01)

    def test_a_weld_is_seen_before_probe(self):
        r = diagnose(H(r_a_ohm=0.1))
        self.assertEqual(r.verdict, Verdict.DENY)
        self.assertIsNone(r.probe)
        self.assertGreater(r.passive.vmid_v, 4)

    def test_b_weld_is_detected_by_second_phase(self):
        r = diagnose(H(r_b_ohm=0.1))
        self.assertEqual(r.verdict, Verdict.DENY)
        self.assertIsNotNone(r.probe)
        self.assertLess(r.probe.vmid_v, 1)

    def test_both_welded_never_probed(self):
        r = diagnose(H(r_a_ohm=0.1, r_b_ohm=0.1))
        self.assertEqual(r.verdict, Verdict.DENY)
        self.assertIsNone(r.probe)
        self.assertGreater(r.passive.vtx_v, 4)

    def test_wide_resistance_corner_sweep(self):
        cases = 0
        for vin, probe, mid_bleed, tx_bleed, rprobe, roff, err in product(
                [4.5, 5.0, 5.5], [4.5, 5.5], [17600., 26400.],
                [900., 1100.], [9000., 11000.], [1e6, 1e8], [0., .08]):
            h = H(vin_v=vin, probe_v=probe, r_mid_bleed_ohm=mid_bleed,
                  r_tx_bleed_ohm=tx_bleed, r_probe_ohm=rprobe,
                  r_a_ohm=roff, r_b_ohm=roff, sensor_error_v=err)
            self.assertEqual(diagnose(h).verdict, Verdict.MODEL_CONSISTENT)
            self.assertEqual(diagnose(replace(h, r_a_ohm=0.1)).verdict, Verdict.DENY)
            self.assertEqual(diagnose(replace(h, r_b_ohm=0.1)).verdict, Verdict.DENY)
            self.assertEqual(diagnose(replace(h, r_a_ohm=0.1, r_b_ohm=0.1)).verdict, Verdict.DENY)
            cases += 1
        self.assertEqual(cases, 3*2*2*2*2*2*2)

    def test_old_47k_bleed_would_be_ambiguous_at_1megaohm_leak(self):
        h = H(vin_v=4.5, probe_v=4.5, r_mid_bleed_ohm=47000.,
              r_a_ohm=1e6, r_b_ohm=1e6)
        self.assertEqual(diagnose(h).verdict, Verdict.HOLD)
        self.assertGreater(dc_solve(h, probe_active=False).vmid_v, .17)

    def test_leaky_a_rejected_without_probe(self):
        self.assertEqual(diagnose(H(r_a_ohm=100000.)).verdict, Verdict.DENY)

    def test_open_mid_bleed_is_held_not_approved(self):
        self.assertEqual(diagnose(H(r_mid_bleed_ohm=1e9)).verdict, Verdict.HOLD)

    def test_probe_current_max_at_lowest_resistance(self):
        h = H(probe_v=5.5, r_probe_ohm=9000., r_b_ohm=0.1)
        r = dc_solve(h, probe_active=True)
        self.assertGreaterEqual(r.probe_current_a, 0)
        self.assertLessEqual(r.probe_current_a, 5.5/9000)

    def test_auxiliary_bridge_to_tx_cannot_claim_safe_model(self):
        r = diagnose(H(r_aux_to_tx_ohm=0.1, aux_v=5))
        self.assertEqual(r.verdict, Verdict.DENY)
        self.assertGreater(r.passive.vtx_v, 4)

    def test_no_sensor_or_probe_holds(self):
        for f in ('mid_sensor_present','tx_sensor_present','probe_available','supply_qualified'):
            self.assertEqual(diagnose(replace(H(), **{f: False})).verdict, Verdict.HOLD)

    def test_brownout_is_hold(self):
        for x in (0, 4.0, 5.6):
            self.assertEqual(diagnose(H(vin_v=x)).verdict, Verdict.HOLD)

    def test_probe_invalid_voltage_is_hold(self):
        self.assertEqual(diagnose(H(probe_v=3.3)).verdict, Verdict.HOLD)

    def test_unknown_resistor_is_hold(self):
        for f,v in [('r_probe_ohm',100.), ('r_probe_ohm',1e6),
                    ('r_mid_bleed_ohm',100.), ('r_tx_bleed_ohm',1e9),
                    ('sensor_error_v',.3)]:
            self.assertEqual(diagnose(replace(H(),**{f:v})).verdict, Verdict.HOLD)

    def test_invalid_types_and_values(self):
        for f,v in [('r_a_ohm',0), ('r_b_ohm',-1), ('r_probe_ohm',float('inf')),
                    ('vin_v',float('nan')), ('r_load_ohm',0),
                    ('probe_available',1), ('sensor_error_v',-1)]:
            with self.subTest(f=f,v=v), self.assertRaises(ValueError):
                H(**{f:v})
        with self.assertRaises(ValueError):
            dc_solve(H(),probe_active=1)

    def test_dc_kcl_at_both_nodes(self):
        h=H(r_a_ohm=3e6,r_b_ohm=30000.,r_load_ohm=4700.,
            r_aux_to_tx_ohm=2000.,aux_v=3.3)
        for probe in (False,True):
            r=dc_solve(h,probe_active=probe)
            mid=((r.vmid_v-h.vin_v)/h.r_a_ohm +
                 (r.vmid_v-r.vtx_v)/h.r_b_ohm +
                 r.vmid_v/h.r_mid_bleed_ohm +
                 (r.vmid_v-h.probe_v)/h.r_probe_ohm * int(probe))
            tx=((r.vtx_v-r.vmid_v)/h.r_b_ohm +
                r.vtx_v/h.r_tx_bleed_ohm +
                r.vtx_v/h.r_load_ohm +
                (r.vtx_v-h.aux_v)/h.r_aux_to_tx_ohm)
            self.assertAlmostEqual(mid,0,places=12)
            self.assertAlmostEqual(tx,0,places=12)

    def test_safety_flags_never_granted(self):
        for ra,rb in product((.1,1e8),(0.1,1e8)):
            r=diagnose(H(r_a_ohm=ra,r_b_ohm=rb))
            self.assertFalse(r.hardware_approved)
            self.assertFalse(r.covers_esd_body_diodes)
            self.assertFalse(r.proves_real_fod)

    def test_stuck_probe_low_is_deny(self):
        self.assertEqual(diagnose(H(probe_v=0)).verdict,Verdict.HOLD)


if __name__=='__main__':
    unittest.main()
