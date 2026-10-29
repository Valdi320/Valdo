"""W-IND-17: adversarial result attestation fixtures, not simulated KiCad ERC."""
import unittest
from w_ind_17_erc_gate import evaluate

class TestERCVerdicts(unittest.TestCase):
    def report(self,violations):
        return {"$schema":"https://schemas.kicad.org/erc.v1.json","sheets":[{"path":"/","violations":violations}]}
    def v(self,kind="pin_not_driven",sev="error"):
        return {"type":kind,"severity":sev}
    def test_real_violations_block(self):
        self.assertEqual(evaluate(5,self.report([self.v()]))["status"],"ERC_HAS_VIOLATIONS_DO_NOT_BUILD")
    def test_zero_violations_still_unqualified(self):
        self.assertEqual(evaluate(0,self.report([]))["status"],"ERC_ZERO_REPORTED_STILL_DO_NOT_BUILD")
    def test_counts(self):
        x=evaluate(5,self.report([self.v(),self.v(),self.v("label_dangling","warning")]))
        self.assertEqual(x["erc_count"],3)
        self.assertEqual(x["by_type"]["pin_not_driven"],2)
        self.assertEqual(x["by_severity"]["warning"],1)
    def test_rc5_without_errors_rejected(self):
        with self.assertRaises(ValueError):evaluate(5,self.report([]))
    def test_rc0_with_errors_rejected(self):
        with self.assertRaises(ValueError):evaluate(0,self.report([self.v()]))
    def test_binary_missing_rejected(self):
        with self.assertRaises(ValueError):evaluate(127,self.report([]))
    def test_parser_failure_rejected(self):
        with self.assertRaises(ValueError):evaluate(3,self.report([self.v()]))
    def test_wrong_shape_rejected(self):
        with self.assertRaises(ValueError):evaluate(0,[])
    def test_missing_violations_rejected(self):
        with self.assertRaises(ValueError):evaluate(0,{"other":[]})
    def test_bad_violation_rejected(self):
        with self.assertRaises(ValueError):evaluate(5,self.report(["bad"]))
    def test_no_safety_approval_for_both_results(self):
        for code,report in [(0,self.report([])), (5,self.report([self.v()]))]:
            with self.subTest(code=code):
                x=evaluate(code,report)
                for key in ("hardware_approved","autonomous_fod_proven",
                            "thermal_trip_proven","overcurrent_proven",
                            "reverse_blocking_proven","independent_cuts_proven",
                            "lithium_charging_approved"):
                    self.assertIs(x[key],False)
    def test_erc_was_executed_field(self):
        self.assertIs(evaluate(5,self.report([self.v()]))["erc_executed"],True)

    def test_real_kicad9_json_shape_multiple_sheets(self):
        a=self.report([self.v()])
        a["sheets"].append({"path":"/subsheet","violations":[self.v("label_dangling","warning")]})
        self.assertEqual(evaluate(5,a)["erc_count"],2)
    def test_reject_root_level_fake_kicad_json(self):
        with self.assertRaises(ValueError):evaluate(5,{"violations":[self.v()]})
    def test_reject_empty_sheet_list(self):
        with self.assertRaises(ValueError):evaluate(0,{"$schema":"https://schemas.kicad.org/erc.v1.json","sheets":[]})
    def test_reject_incorrect_schema(self):
        with self.assertRaises(ValueError):
            evaluate(5,{"$schema":"https://invalid.test/erc.v1.json","sheets":[{"path":"/","violations":[self.v()]}]})

if __name__=="__main__":
    unittest.main()
