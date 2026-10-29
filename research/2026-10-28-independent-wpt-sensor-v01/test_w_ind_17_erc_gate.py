"""W-IND-17: adversarial result attestation fixtures, not simulated KiCad ERC."""
import unittest
from w_ind_17_erc_gate import evaluate

class TestERCVerdicts(unittest.TestCase):
    def v(self,kind="pin_not_driven",sev="error"):
        return {"type":kind,"severity":sev}
    def test_real_violations_block(self):
        self.assertEqual(evaluate(5,{"violations":[self.v()]})["status"],"ERC_HAS_VIOLATIONS_DO_NOT_BUILD")
    def test_zero_violations_still_unqualified(self):
        self.assertEqual(evaluate(0,{"violations":[]})["status"],"ERC_ZERO_REPORTED_STILL_DO_NOT_BUILD")
    def test_counts(self):
        x=evaluate(5,{"violations":[self.v(),self.v(),self.v("label_dangling","warning")]})
        self.assertEqual(x["erc_count"],3)
        self.assertEqual(x["by_type"]["pin_not_driven"],2)
        self.assertEqual(x["by_severity"]["warning"],1)
    def test_rc5_without_errors_rejected(self):
        with self.assertRaises(ValueError):evaluate(5,{"violations":[]})
    def test_rc0_with_errors_rejected(self):
        with self.assertRaises(ValueError):evaluate(0,{"violations":[self.v()]})
    def test_binary_missing_rejected(self):
        with self.assertRaises(ValueError):evaluate(127,{"violations":[]})
    def test_parser_failure_rejected(self):
        with self.assertRaises(ValueError):evaluate(3,{"violations":[self.v()]})
    def test_wrong_shape_rejected(self):
        with self.assertRaises(ValueError):evaluate(0,[])
    def test_missing_violations_rejected(self):
        with self.assertRaises(ValueError):evaluate(0,{"other":[]})
    def test_bad_violation_rejected(self):
        with self.assertRaises(ValueError):evaluate(5,{"violations":["bad"]})
    def test_no_safety_approval_for_both_results(self):
        for code,report in [(0,{"violations":[]}), (5,{"violations":[self.v()]})]:
            with self.subTest(code=code):
                x=evaluate(code,report)
                for key in ("hardware_approved","autonomous_fod_proven",
                            "thermal_trip_proven","overcurrent_proven",
                            "reverse_blocking_proven","independent_cuts_proven",
                            "lithium_charging_approved"):
                    self.assertIs(x[key],False)
    def test_erc_was_executed_field(self):
        self.assertIs(evaluate(5,{"violations":[self.v()]})["erc_executed"],True)

if __name__=="__main__":
    unittest.main()
