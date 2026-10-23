#!/usr/bin/env python3
"""Synthetic-only regression suite for csv audit commercial sample."""
import csv
import hashlib
import tempfile
import unittest
from pathlib import Path

from audit_csv import AuditError, analyze, normalize


FIXTURE = """id,name,city,amount
001,Alpha Bikes,Madrid,12.50
002,Beta Supplies,Barcelona,seven
002,Beta Supplies,Barcelona,7.00
,Missing Id,Zaragoza,8.00
005,Alpha Bikes,Madrid,15.00
"""


class AuditTests(unittest.TestCase):
    def test_normalization(self):
        self.assertEqual(normalize("  Café  de  la Plaza "), "cafe de la plaza")
        self.assertEqual(normalize("ALPHA - Bikes"), "alpha bikes")

    def test_preserves_source_and_reconciles_records(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "synthetic.csv"
            source.write_text(FIXTURE, encoding="utf-8")
            original_sha = hashlib.sha256(source.read_bytes()).hexdigest()
            out = root / "out"
            receipt = analyze(source, out, "id", "name", "city",
                              ["id", "name", "city"], ["amount"])
            self.assertEqual(receipt["source_sha256"], original_sha)
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), original_sha)
            self.assertEqual(receipt["source_records"], 5)
            self.assertEqual(receipt["annotated_records"], 5)
            self.assertEqual(receipt["candidate_pairs"], 2)
            self.assertEqual(receipt["issues"]["duplicate_id_review"], 2)
            self.assertEqual(receipt["issues"]["missing_required"], 1)
            self.assertEqual(receipt["issues"]["invalid_decimal"], 1)
            self.assertEqual(receipt["issues"]["possible_same_name_review"], 4)
            self.assertFalse(receipt["automatically_merged_or_deleted"])
            with (out / "annotated_rows.csv").open(encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), 5)
            self.assertEqual(rows[0]["id"], "001")
            self.assertEqual(rows[1]["id"], "002")
            self.assertEqual(rows[2]["id"], "002")
            self.assertEqual(rows[3]["id"], "")
            self.assertEqual(rows[4]["id"], "005")
            for i, row in enumerate(rows, 1):
                self.assertEqual(row["__audit_record"], str(i))
            # Re-running the same audit must produce identical receipt and output digests.
            repeated = analyze(source, out, "id", "name", "city",
                               ["id", "name", "city"], ["amount"])
            self.assertEqual(receipt, repeated)

    def test_ragged_rows_rejected_without_silently_dropping_fields(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "ragged.csv"
            source.write_text("id,name\n1,A,extra\n", encoding="utf-8")
            with self.assertRaisesRegex(AuditError, "No fields dropped"):
                analyze(source, root / "out", "id")

    def test_duplicate_headers_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "duplicate.csv"
            source.write_text("id,name,name\n001,A,B\n", encoding="utf-8")
            with self.assertRaisesRegex(AuditError, "Duplicate headings"):
                analyze(source, root / "out", "id")

    def test_max_rows_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "sample.csv"
            source.write_text(FIXTURE, encoding="utf-8")
            with self.assertRaisesRegex(AuditError, "row limit"):
                analyze(source, root / "out", "id", limit=4)

    def test_reserved_column_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "reserved.csv"
            source.write_text("id,__audit_status\n1,OK\n", encoding="utf-8")
            with self.assertRaisesRegex(AuditError, "Reserved audit"):
                analyze(source, root / "out", "id")


if __name__ == "__main__":
    unittest.main()
