# Inventory CSV reconciliation — tested AI-produced portfolio example

**Public demonstration with fabricated inventory data. All technical production was carried out by AI using Python 3. No paid-client experience, manual expert review or production deployment is implied.** It uses Python's standard library; no external APIs, subscriptions or customer datasets.

## Buyer problem

A supplier sends a new inventory export. Which SKU records appeared, disappeared or changed since the previous file? What should **not** be matched automatically because its key is absent or duplicated?

## Verified synthetic run

| Metric | Reproduced result |
| --- | ---: |
| Older export | 6 rows |
| Newer export | 6 rows |
| Unambiguously matched SKU pairs | 3 |
| Unchanged matches | 1 |
| Changed fields / invalid-decimal flags | 2 |
| Only in old / only in new | 1 / 1 |
| Ambiguous duplicate-key rows held for review | 4 |
| Automated tests | **11 passed, 0 failed** |

The tool records a stock difference for SKU `0001`, flags invalid numeric text for SKU `0003`, reports SKU `0005` as missing from the new export and SKU `0006` as new. Repeated SKU `0004` in the older export and `0007` in the newer export are **not** automatically merged, matched or deleted. SKU identifiers remain text, including leading zeros. Decimal strings like `0.10` and `0.100` compare equal when designated numeric.

## Reproduce locally

Requires Python **3.10+**, no package installation. Run from this folder:

```bash
python3 -m unittest discover -s tests -v
python3 reconcile.py examples/old.csv examples/new.csv \
  --out examples/output --key sku --fields label,stock,price --numeric stock,price
```

The CLI produces `only_old.csv`, `only_new.csv`, `changes.csv`, `exceptions.csv` and `receipt.json` under `examples/output`. The receipt records the source SHA-256 hashes and hashes of each CSV deliverable. Compare these with the checked-in sample outputs. Neither input file is modified.

## Known limits and safety

- UTF-8 CSV only; both exports need identical column order and names. Key values are compared **exactly**, with no fuzzy matching or inferred equivalences.
- Default maximum 20,000 data rows per input, 40 columns, fully in memory. No large-dataset performance guarantee.
- Duplicate keys, missing keys and non-numeric values are for review, not silent fixing. Only records with uniquely matching keys on both sides enter the change comparison.
- Numeric fields must use dot-decimal format. This is **not** a locale-aware currency reconciliation or accounting tool.
- **Spreadsheet warning:** CSV outputs are not escaped against formula injection. Do not open untrusted outputs in spreadsheet software without safe import/neutralization.
- A buyer's authorization, acceptance rules, AI-only processing consent, agreed payment and payment protection are required before any real customer work. Do not send private or sensitive data to demonstrate this tool.

**Result:** a narrowly scoped technical proof of concept, not an offer to start an order automatically. Suitable for a platform portfolio attachment subject to its rules.
