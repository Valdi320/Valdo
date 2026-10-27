"""Synthetic-only verification of the public AI-produced CSV demonstration."""
import csv
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from reconcile import compare, ReconciliationError


OLD = "sku,label,stock,price\n0001,Hinge,12,2.50\n0002,Screw,60,0.10\n0003,Brush,3,7.20\n0004,Glue,8,3.00\n0004,Glue,9,3.00\n0005,Hex,2,8.50\n"
NEW = "sku,label,stock,price\n0001,Hinge,10,2.50\n0002,Screw,60,0.100\n0003,Brush,3,bad\n0006,Glasses,4,12.00\n0007,Glue,5,3.00\n0007,Glue,6,3.00\n"


def csvrows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class ReconcileTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root = Path(self.t.name)
        self.old = self.root / "old.csv"
        self.new = self.root / "new.csv"
        self.out = self.root / "output"
        self.old.write_text(OLD, encoding="utf-8")
        self.new.write_text(NEW, encoding="utf-8")

    def run_comparison(self):
        return compare(self.old, self.new, self.out, key="sku", fields=["label", "stock", "price"], numeric=["stock", "price"])

    def test_counts_and_limited_comparison(self):
        r = self.run_comparison()
        self.assertEqual((r["old_rows"], r["new_rows"], r["unambiguous_pairs"]), (6, 6, 3))
        self.assertEqual((r["only_old"], r["only_new"], r["exception_rows"]), (1, 1, 4))
        self.assertEqual(r["changed_fields_or_invalid_numeric"], 2)
        self.assertEqual(r["unchanged_pairs"], 1)
        self.assertEqual([row["sku"] for row in csvrows(self.out / "only_old.csv")], ["0005"])
        self.assertEqual([row["sku"] for row in csvrows(self.out / "only_new.csv")], ["0006"])

    def test_duplicate_keys_excluded_not_merged(self):
        self.run_comparison()
        exceptions = csvrows(self.out / "exceptions.csv")
        self.assertEqual(len(exceptions), 4)
        self.assertEqual({(r["side"], r["sku"], r["flag"]) for r in exceptions},
                         {("old", "0004", "duplicate_key"), ("new", "0007", "duplicate_key")})

    def test_invalid_numeric_and_decimal_semantics(self):
        self.run_comparison()
        changes = csvrows(self.out / "changes.csv")
        self.assertEqual({(r["sku"], r["field"], r["flag"]) for r in changes},
                         {("0001", "stock", "value_changed"), ("0003", "price", "invalid_numeric")})

    def test_reproducible_hashes_and_unmodified_sources(self):
        old_before = hashlib.sha256(self.old.read_bytes()).hexdigest()
        new_before = hashlib.sha256(self.new.read_bytes()).hexdigest()
        first = self.run_comparison()
        self.assertEqual(first["old_sha256"], old_before)
        self.assertEqual(first["new_sha256"], new_before)
        self.assertEqual(self.run_comparison(), first)
        self.assertEqual(json.loads((self.out / "receipt.json").read_text()), first)
        for name, hashed in first["output_sha256"].items():
            self.assertEqual(hashlib.sha256((self.out / name).read_bytes()).hexdigest(), hashed)

    def test_reject_duplicate_headers_without_writing_outputs(self):
        self.old.write_text("sku,sku,stock,price\n1,1,2,3\n", encoding="utf-8")
        with self.assertRaisesRegex(ReconciliationError, "headers"):
            self.run_comparison()
        self.assertFalse(self.out.exists())

    def test_reject_ragged_rows_without_writing_outputs(self):
        self.new.write_text("sku,label,stock,price\n1,X,2,3,EXTRA\n", encoding="utf-8")
        with self.assertRaisesRegex(ReconciliationError, "cells"):
            self.run_comparison()
        self.assertFalse(self.out.exists())

    def test_reject_mismatched_columns(self):
        self.new.write_text("sku,stock,label,price\n1,2,X,3\n", encoding="utf-8")
        with self.assertRaisesRegex(ReconciliationError, "layout"):
            self.run_comparison()
        self.assertFalse(self.out.exists())

    def test_reject_excessive_rows(self):
        with self.assertRaisesRegex(ReconciliationError, "limit"):
            compare(self.old, self.new, self.out, key="sku", fields=["label"], max_rows=2)
        self.assertFalse(self.out.exists())

    def test_blank_key_reported_not_added_or_removed(self):
        self.old.write_text(OLD + ",Unknown,1,2.00\n", encoding="utf-8")
        r = self.run_comparison()
        self.assertEqual(r["exception_rows"], 5)
        self.assertTrue(any(x["flag"] == "missing_key" for x in csvrows(self.out / "exceptions.csv")))

    def test_ambiguous_counterpart_reported(self):
        self.old.write_text(OLD + "0007,Glue,3,3.00\n", encoding="utf-8")
        r = self.run_comparison()
        self.assertEqual(r["exception_rows"], 5)
        self.assertTrue(any(x["flag"] == "ambiguous_counterpart" for x in csvrows(self.out / "exceptions.csv")))

    def test_ids_not_numeric_or_normalized(self):
        self.old.write_text("sku,label,stock,price\n001,A,2,1.0\n", encoding="utf-8")
        self.new.write_text("sku,label,stock,price\n1,A,2,1.0\n", encoding="utf-8")
        r = self.run_comparison()
        self.assertEqual((r["only_old"], r["only_new"], r["unambiguous_pairs"]), (1, 1, 0))


if __name__ == "__main__":
    unittest.main()
