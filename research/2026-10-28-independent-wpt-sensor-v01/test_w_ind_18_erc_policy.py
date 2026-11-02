"""Deterministic adversarial tests; real ERC remains KiCad CLI in CI."""
import hashlib
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from w_ind_17_erc_gate import evaluate
from w_ind_18_erc_policy import check_evidence, main

SOURCE = "research/2026-10-28-independent-wpt-sensor-v01/W_IND_15_TX_DUAL_CUT_UNQUALIFIED.kicad_sch"
BYTES = b"example-source-schematic"
SHA = "fixture-head"

def fixtures(n=9):
    violations = ([{"type":"label_dangling","severity":"error"},
                   {"type":"power_pin_not_driven","severity":"error"},
                   {"type":"power_pin_not_driven","severity":"error"}]
                  + [{"type":"lib_symbol_issues","severity":"warning"} for _ in range(6)]) if n else []
    report = {"$schema":"https://schemas.kicad.org/erc.v1.json", "kicad_version":"9.0.2",
              "source":Path(SOURCE).name, "sheets":[{"path":"/","violations":violations}]}
    att = evaluate(5 if n else 0, report)
    att.update(source_sha256=hashlib.sha256(BYTES).hexdigest(),source_schematic=SOURCE,
               kicad_version="9.0.2",test_kind="real_KiCad_ERC_ephemeral_CI",
               hardware_energized=False,physical_tests=0,github_sha=SHA)
    return report,att

class TestBlockingCI(unittest.TestCase):
    def test_known_nine_erc_defects_are_blocking(self):
        self.assertEqual(check_evidence(*fixtures(), BYTES, SOURCE, SHA),(False,9))
    def test_clean_erc_passes_only_erc_stage(self):
        self.assertEqual(check_evidence(*fixtures(0), BYTES, SOURCE, SHA),(True,0))
    def test_fake_clean_attestation_rejected(self):
        r,a=fixtures();a["erc_count"]=0
        with self.assertRaisesRegex(ValueError,"mismatch"):check_evidence(r,a,BYTES,SOURCE,SHA)
    def test_false_hardware_approval_rejected(self):
        r,a=fixtures(0);a["hardware_approved"]=True
        with self.assertRaisesRegex(ValueError,"hardware_approved"):check_evidence(r,a,BYTES,SOURCE,SHA)
    def test_changed_source_rejected(self):
        with self.assertRaisesRegex(ValueError,"altered"):check_evidence(*fixtures(),b"changed",SOURCE,SHA)
    def test_wrong_source_path_rejected(self):
        with self.assertRaisesRegex(ValueError,"path"):check_evidence(*fixtures(),BYTES,"other.kicad_sch",SHA)
    def test_wrong_version_rejected(self):
        r,a=fixtures();a["kicad_version"]="8.0.0"
        with self.assertRaisesRegex(ValueError,"version"):check_evidence(r,a,BYTES,SOURCE,SHA)
    def test_other_commit_evidence_rejected(self):
        with self.assertRaisesRegex(ValueError,"revision"):check_evidence(*fixtures(),BYTES,SOURCE,"other-sha")
    def test_unknown_erc_exit_rejected(self):
        r,a=fixtures();a["erc_rc"]=127
        with self.assertRaises(ValueError):check_evidence(r,a,BYTES,SOURCE,SHA)
    def test_erased_violations_rejected(self):
        r,a=fixtures();r["sheets"][0]["violations"]=[]
        with self.assertRaises(ValueError):check_evidence(r,a,BYTES,SOURCE,SHA)
    def test_invalid_schema_rejected(self):
        r,a=fixtures();r["$schema"]="wrong"
        with self.assertRaises(ValueError):check_evidence(r,a,BYTES,SOURCE,SHA)
    def test_missing_provenance_rejected(self):
        r,a=fixtures();del a["test_kind"]
        with self.assertRaisesRegex(ValueError,"test path"):check_evidence(r,a,BYTES,SOURCE,SHA)
    def test_physical_test_claim_rejected(self):
        r,a=fixtures();a["physical_tests"]=1
        with self.assertRaisesRegex(ValueError,"physical"):check_evidence(r,a,BYTES,SOURCE,SHA)
    def test_main_returns_failure_and_success(self):
        with TemporaryDirectory() as tmp:
            d=Path(tmp);sch=d/Path(SOURCE).name;sch.write_bytes(BYTES)
            for n,expected in [(9,1),(0,0)]:
                report,att=fixtures(n);att["source_schematic"]=str(sch)
                (d/"erc.json").write_text(json.dumps(report))
                (d/"att.json").write_text(json.dumps(att))
                with patch.dict("os.environ", {"GITHUB_SHA": SHA}):
                    self.assertEqual(main(["--erc",str(d/"erc.json"),"--attestation",str(d/"att.json"),"--schematic",str(sch)]),expected)
    def test_missing_files_fail_closed(self):
        self.assertEqual(main(["--erc","/unavailable/erc.json","--attestation","/unavailable/att.json",
                               "--schematic","/unavailable/sch.kicad_sch"]),2)

if __name__ == "__main__": unittest.main()
