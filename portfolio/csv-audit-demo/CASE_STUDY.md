# CSV Quality Audit — Verified Portfolio Sample

**Portfolio demonstration • 23 October 2026 • synthetic data • entirely AI-operated with Python 3**

A small, reproducible example of how a buyer's **authorized, non-sensitive CSV** can be checked for required-field gaps, repeated identifiers, invalid decimal values, and candidate duplicate records **without deleting, merging, or modifying the input**. This is **not** a paid-client reference.

## Measured result (verified on 23 October 2026)

| Evidence | Verified value |
| --- | ---: |
| Input CSV records | 5 |
| Annotated output records | 5 |
| Recorded issue flags | 8 |
| Possible duplicate pairs — for review only | 2 |
| Local automated tests | **6 passed / 0 failed** |
| Input SHA-256 matching the report receipt | **YES** |
| Output file SHA-256 values matching the receipt | **3 of 3** |

**Issue categories:** repeated ID (2 record flags); decimal parsing (1); missing required value (1); matching name/city (4 record flags). Multiple flags can refer to the same record. A probable pair does **not** prove two real-world people or businesses are identical.

### Synthetic input sample

| Record | id | name | city | amount |
| ---: | --- | --- | --- | --- |
| 1 | 001 | Alpha Bikes | Madrid | 12.50 |
| 2 | 002 | Beta Supplies | Barcelona | seven |
| 3 | 002 | Beta Supplies | Barcelona | 7.00 |
| 4 | *(empty)* | Missing Id | Zaragoza | 8.00 |
| 5 | 005 | Alpha Bikes | Madrid | 15.00 |

**What happened:** records 2 and 3 are flagged for repeated identifier; record 2 has an invalid decimal; record 4 lacks a required ID; records (1,5) and (2,3) form review-only candidate pairs.

### Deliverable set

- `output/annotated_rows.csv` — every source row, preserved with review annotations.
- `output/exceptions.csv` — eight issue flags mapped to source record and field.
- `output/candidate_duplicates.csv` — two suggested pairs (not confirmed duplicates).
- `output/report.md` — human-readable findings and scope limitations.
- `output/receipt.json` — source checksum, output checksums, reconciliation counts and rule configuration.
- `audit_csv.py`, `test_audit_csv.py` — local Python implementation and automated checks.

Source checksum (SHA-256): `bc01998406782a74f960918ec02cac4301bd2f69e3ea0a620afdf1bc3363643b`. The five input rows are still present in the annotated output; no record was automatically merged or deleted.

### Scope and integrity

The sample is fabricated. No actual customer data was used. This is a **static, rules-based demonstration**, not a guarantee of complete data quality, verified business identity, human manual review, or an already-fulfilled customer order. Decimal checks use dot-decimal input and are not locale-aware automatic corrections. Candidate duplicate decisions are deferred for customer approval.

Production work starts only after the buyer confirms the authorized source file, matching rules, deliverables, acceptance criteria, AI-only processing permission, price, and payment protection. No sensitive personal data is requested for this demonstration.

**Suggested client-facing description:** "I can review your authorized CSV with Python and AI, flag missing values, duplicate IDs, invalid formats and probable duplicate candidates, and deliver a row-preserving annotated file plus exception report and reproducibility receipt. All findings that require a human identity decision remain marked for your review."

