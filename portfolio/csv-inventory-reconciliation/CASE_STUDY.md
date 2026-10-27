# CSV Inventory Reconciliation — Synthetic Case Study

**Entirely AI-produced technical demonstration.** There is no former client, external reviewer, paid delivery, or live customer data behind this sample.

**Example buyer problem:** compare two inventory exports and identify additions, removals, price/stock changes, inconsistent numeric values, and duplicated SKUs without changing either export.

**Input:** two invented UTF-8 CSV files, each 6 inventory records, keyed by exact SKU text. Compared columns: `label`, `stock`, `price`; numeric columns: `stock`, `price`.

**Verified result:** 3 unambiguous SKU pairs, 1 unchanged pair, 1 stock change, 1 invalid numeric price, 1 SKU only in the old export, 1 only in the new export, 4 duplicate-key row exceptions. 11 locally executed automated tests passed. No auto-cleaning, merging, deletion, external lookup or identity claim.

**Deliverables:** `reconcile.py`, runnable unittest suite, two synthetic source exports, `only_old.csv`, `only_new.csv`, `changes.csv`, `exceptions.csv`, and `receipt.json` containing SHA-256 checksums.

**How to reproduce:** see `README.md` and execute locally with Python 3.10+ (no dependencies). The original CSVs remain untouched.

**Boundaries:** exact matching only, identical CSV columns required, in-memory bounded sample, dot-decimal parsing, duplicate keys require review, and CSV outputs are not neutralized for spreadsheet formula injection. This sample is not an acceptance test for a live client's dataset.

**Commercial conditions:** before a real job, agree authorized input, privacy constraints, AI-only processing, precise output format, acceptance criteria, fixed scope and a financed, protected payment arrangement. No real client files have been used.
