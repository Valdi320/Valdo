# Traceable CSV Audit — Public Portfolio Demonstration

**A fully AI-produced, synthetic Python demonstration.** This is not paid client work, not a claim of prior freelance experience, and contains no real customer or private project data. Technical production and verification were carried out by AI with Python 3.

## Reproducible results (verified 23 October 2026)

- **5 records in; 5 annotated records out** — no automatic deletion or merging.
- **8 flags:** 2 repeated-ID record flags, 1 invalid decimal, 1 missing required ID, 4 possible matching-name flags.
- **2 candidate duplicate pairs**, requiring human review; no identity claims.
- **6 automated tests passed**, none failed.
- Source SHA-256: `bc01998406782a74f960918ec02cac4301bd2f69e3ea0a620afdf1bc3363643b`.
- Three output hashes match the included receipt.

### Verify on any machine (Python 3.10+, no external dependencies)

```bash
python3 -m unittest test_audit_csv.py -v
python3 audit_csv.py sample_input.csv --outdir output --id id --name name --city city --required id,name,city --numeric amount
```

You can review [the Python source](audit_csv.py), [tests](test_audit_csv.py), [synthetic fixture](sample_input.csv), [case study](CASE_STUDY.md), and the five files in [output](output/).

## Limitations and safe use

The script is a **review-only quality audit**, not automatic cleaning. It checks named fields in UTF-8 CSV files with dot-decimal numeric values and bounded input sizes. Duplicate candidates do not prove real-world identities. It does not send data to external APIs or paid services. These six tests are not a claim of exhaustive QA.

**Spreadsheet security:** Output CSV fields are not neutralized against spreadsheet formula injection. Do not open unknown or untrusted output in Excel/Google Sheets without applying an appropriate spreadsheet-safe import process first.

Commercial work would require approved scope, data permissions, explicit disclosure that AI performs the production, agreed deliverables, and verified funded payment protection **before any real client data is processed**. Do not send secrets, private records or sensitive personal data.

*English case study and Spanish instructions are included; all sample data is invented.*
