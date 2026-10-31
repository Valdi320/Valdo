"""W-IND-10 deterministic Python tests; offline, no device or external libs."""
import unittest
from dataclasses import replace
from itertools import product
from fod_uncertainty_gate import Observation, Verdict, compare, example

def pair():
    p=dict(fixture="fixture",coils="pair",load="dummy",
           provenance="synthetic",uin_w=.04,uout_w=.03,
           xy_x_mm=0.,xy_y_mm=0.,gap_mm=4.,ambient_c=25.)
    return (Observation("reference",pin_w=2.,pout_w=1.,**p),
            Observation("candidate",pin_w=2.12,pout_w=1.,**p))

def run(base=None,evt=None,**kw):
    b,c=pair()
    return compare(base or b,evt or c,drift_w=.05,**kw)

class FodTests(unittest.TestCase):
    def test_three_outcomes(self):
        a=example()
        self.assertEqual(a["no_extra_loss"].verdict,Verdict.BELOW_THRESHOLD)
        self.assertEqual(a["small_loss"].verdict,Verdict.INDETERMINATE)
        self.assertEqual(a["large_loss"].verdict,Verdict.SUSPECTED_EXCESS)
    def test_uncertainty_calculation(self):
        r=run()
        self.assertAlmostEqual(r.extra_loss_w,.12)
        self.assertAlmostEqual(r.uncertainty_bound_w,.19)
        self.assertAlmostEqual(r.lower_w,-.07)
        self.assertAlmostEqual(r.upper_w,.31)
    def test_all_never_approve_energization(self):
        for r in example().values():
            self.assertFalse(r.installation_approved)
            self.assertFalse(r.physical_tx_enable_allowed)
            self.assertFalse(r.demonstrated_fod_clear)
    def test_fixture_identity_matters(self):
        b,c=pair()
        for field in ("fixture","coils","load","provenance"):
            v="bench_measured" if field=="provenance" else "other"
            with self.subTest(field=field):
                self.assertEqual(run(b,replace(c,**{field:v})).verdict,
                                 Verdict.NOT_COMPARABLE)
    def test_geometry_ambient_mismatch(self):
        b,c=pair()
        for field,value in (("xy_x_mm",.51),("xy_y_mm",-.51),
                            ("gap_mm",4.21),("ambient_c",27.01)):
            with self.subTest(field=field):
                self.assertEqual(run(b,replace(c,**{field:value})).verdict,
                                 Verdict.NOT_COMPARABLE)
    def test_borderline_float_tolerance(self):
        b,c=pair()
        c=replace(c,xy_x_mm=.5,xy_y_mm=-.5,gap_mm=4.2,ambient_c=27.)
        self.assertNotEqual(run(b,c).verdict,Verdict.NOT_COMPARABLE)
    def test_radio_rx_report_not_proven_meter(self):
        b,c=pair()
        for bad in ("radio_report","",None,"datasheet_claim"):
            with self.subTest(bad=repr(bad)):
                with self.assertRaises(ValueError):
                    run(b,replace(c,provenance=bad))
    def test_nonfinite_and_mistyped_power(self):
        b,c=pair()
        for field in ("pin_w","pout_w","uin_w","uout_w"):
            for bad in (float("nan"),float("inf"),-1,True,"1"):
                with self.subTest(field=field,bad=repr(bad)):
                    with self.assertRaises(ValueError):
                        run(b,replace(c,**{field:bad}))
    def test_output_greater_than_input_invalid(self):
        b,c=pair()
        with self.assertRaises(ValueError):
            run(b,replace(c,pout_w=5.))
    def test_nonfinite_and_mistyped_geometry(self):
        b,c=pair()
        for field in ("xy_x_mm","xy_y_mm","gap_mm","ambient_c"):
            for bad in (float("nan"),float("inf"),True,"0"):
                with self.subTest(field=field,bad=repr(bad)):
                    with self.assertRaises(ValueError):
                        run(b,replace(c,**{field:bad}))
    def test_invalid_gap_temperature(self):
        b,c=pair()
        for field,value in (("gap_mm",0),("gap_mm",-1),
                            ("ambient_c",-41),("ambient_c",101)):
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    run(b,replace(c,**{field:value}))
    def test_provenance_and_labels_required(self):
        b,c=pair()
        for field in ("scenario","fixture","coils","load"):
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    run(b,replace(c,**{field:" "}))
    def test_invalid_configuration(self):
        b,c=pair()
        for field in ("drift_w","diagnostic_threshold_w","max_xy_mm",
                      "max_gap_mm","max_ambient_c"):
            for bad in (-1,float("nan"),float("inf"),True,None):
                with self.subTest(field=field,bad=repr(bad)):
                    kwargs={"drift_w":.05}
                    kwargs[field]=bad
                    with self.assertRaises(ValueError):
                        compare(b,c,**kwargs)
    def test_zero_threshold_is_not_safety_norm(self):
        b,c=pair()
        with self.assertRaises(ValueError):
            compare(b,c,drift_w=.05,diagnostic_threshold_w=0)
    def test_exact_threshold_border_is_indeterminate(self):
        self.assertEqual(run(diagnostic_threshold_w=.31).verdict,
                         Verdict.INDETERMINATE)
    def test_common_loss_rejected_as_metal_claim(self):
        b,c=pair()
        b=replace(b,pin_w=4.,pout_w=3.)
        c=replace(c,pin_w=4.12,pout_w=3.)
        self.assertAlmostEqual(run(b,c).extra_loss_w,.12)
    def test_lost_output_same_extra_loss(self):
        b,c=pair()
        self.assertEqual(run(b,replace(c,pin_w=2.,pout_w=.88)).verdict,
                         Verdict.INDETERMINATE)
    def test_negative_loss_delta_not_clean(self):
        b,c=pair()
        r=run(b,replace(c,pin_w=1.9))
        self.assertEqual(r.verdict,Verdict.BELOW_THRESHOLD)
        self.assertFalse(r.demonstrated_fod_clear)
    def test_labels_not_hardware(self):
        b,c=pair()
        self.assertEqual(run(b,c).extra_loss_w,
                         run(replace(b,scenario="no_metal"),
                             replace(c,scenario="metal")).extra_loss_w)
    def test_thermometry_not_in_model_means_no_enable(self):
        self.assertFalse(run().physical_tx_enable_allowed)
    def test_error_grid_never_enables(self):
        b,c=pair()
        for err,drift,delta in product((0.,.01,.05,.1),
                                       (0.,.05,.1),
                                       (0.,.1,.5,1.)):
            b1=replace(b,uin_w=err,uout_w=err)
            c1=replace(c,uin_w=err,uout_w=err,pin_w=2.+delta)
            r=compare(b1,c1,drift_w=drift)
            self.assertFalse(r.physical_tx_enable_allowed)

if __name__=="__main__":
    unittest.main()
