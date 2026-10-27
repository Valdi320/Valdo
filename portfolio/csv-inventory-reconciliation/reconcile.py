#!/usr/bin/env python3
"""AI-produced, stdlib-only, review-first reconciliation of two small CSV exports."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path


class ReconciliationError(ValueError):
    """Reject inputs for which a truthful comparison cannot be made."""


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path, key: str, fields: list[str], max_rows: int) -> tuple[list[str], list[tuple[int, dict[str, str]]]]:
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle, strict=True)
            columns = next(reader, None)
            if not columns or not all(columns) or len(columns) > 40 or len(set(columns)) != len(columns):
                raise ReconciliationError(f"{path.name}: invalid, repeated or excessive headers")
            missing = set([key, *fields]) - set(columns)
            if missing:
                raise ReconciliationError(f"{path.name}: missing columns {sorted(missing)}")
            rows: list[tuple[int, dict[str, str]]] = []
            for index, raw in enumerate(reader, 1):
                if index > max_rows:
                    raise ReconciliationError(f"{path.name}: row limit exceeded")
                if len(raw) != len(columns):
                    raise ReconciliationError(f"{path.name}: row {index} has {len(raw)} cells; expected {len(columns)}")
                rows.append((index, dict(zip(columns, raw))))
            return columns, rows
    except (UnicodeError, csv.Error) as exc:
        raise ReconciliationError(f"{path.name}: invalid UTF-8 or CSV syntax: {exc}") from exc


def write_csv(dest: Path, columns: list[str], rows: list[list[str]]) -> None:
    with dest.open("w", encoding="utf-8", newline="") as out:
        writer = csv.writer(out, lineterminator="\n")
        writer.writerow(columns)
        writer.writerows(rows)


def compare(old_path: Path, new_path: Path, output: Path, *, key: str,
            fields: list[str], numeric: list[str] | None = None, max_rows: int = 20000) -> dict:
    numeric = numeric or []
    if not key or not fields or len(fields) != len(set(fields)) or key in fields:
        raise ReconciliationError("Supply a key and distinct comparison fields")
    if not set(numeric).issubset(fields):
        raise ReconciliationError("Numeric fields must be in compared fields")
    if max_rows < 1:
        raise ReconciliationError("Row limit must be positive")
    old_path, new_path, output = old_path.resolve(), new_path.resolve(), output.resolve()
    if old_path == new_path or old_path in output.parents or new_path in output.parents:
        raise ReconciliationError("Use two distinct CSVs; output must not be an ancestor of either")
    if output == old_path.parent or output == new_path.parent:
        raise ReconciliationError("Output directory must differ from both source directories")
    old_cols, old_rows = read_csv(old_path, key, fields, max_rows)
    new_cols, new_rows = read_csv(new_path, key, fields, max_rows)
    if old_cols != new_cols:
        raise ReconciliationError("Column layout differs; explicit mapping not supported")
    old_ids = Counter(row[key] for _, row in old_rows if row[key].strip())
    new_ids = Counter(row[key] for _, row in new_rows if row[key].strip())
    old_unique = {row[key]: (index, row) for index, row in old_rows if old_ids[row[key]] == 1}
    new_unique = {row[key]: (index, row) for index, row in new_rows if new_ids[row[key]] == 1}
    exceptions = []
    for side, rows, ids, other_ids in (("old", old_rows, old_ids, new_ids), ("new", new_rows, new_ids, old_ids)):
        for index, row in rows:
            identifier = row[key]
            if not identifier.strip():
                reason = "missing_key"
            elif ids[identifier] > 1:
                reason = "duplicate_key"
            elif other_ids[identifier] > 1:
                reason = "ambiguous_counterpart"
            else:
                continue
            exceptions.append([side, str(index), identifier, reason])
    old_only = sorted((key_value for key_value in old_unique if key_value not in new_ids))
    new_only = sorted((key_value for key_value in new_unique if key_value not in old_ids))
    common = sorted(old_unique.keys() & new_unique.keys())
    changes = []
    unchanged = 0
    for identifier in common:
        _, before = old_unique[identifier]
        _, after = new_unique[identifier]
        changed = False
        for field in fields:
            a, b = before[field], after[field]
            kind = "value_changed"
            if field in numeric:
                try:
                    x, y = Decimal(a), Decimal(b)
                    if not x.is_finite() or not y.is_finite():
                        raise InvalidOperation
                except (InvalidOperation, ValueError):
                    kind = "invalid_numeric"
                    changed = True
                else:
                    if x == y:
                        continue
            elif a == b:
                continue
            changes.append([identifier, field, a, b, kind])
            changed = True
        if not changed:
            unchanged += 1
    # Strict fail-closed: no output is written before both inputs are validated.
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / "only_old.csv", ["source_row", *old_cols],
              [[str(old_unique[k][0]), *[old_unique[k][1][col] for col in old_cols]] for k in old_only])
    write_csv(output / "only_new.csv", ["source_row", *new_cols],
              [[str(new_unique[k][0]), *[new_unique[k][1][col] for col in new_cols]] for k in new_only])
    write_csv(output / "changes.csv", [key, "field", "old_value", "new_value", "flag"], changes)
    write_csv(output / "exceptions.csv", ["side", "source_row", key, "flag"], exceptions)
    result = {
        "description": "Synthetic, review-only comparison. No data cleaned, merged or deleted.",
        "old_rows": len(old_rows), "new_rows": len(new_rows),
        "unambiguous_pairs": len(common), "unchanged_pairs": unchanged,
        "changed_fields_or_invalid_numeric": len(changes),
        "only_old": len(old_only), "only_new": len(new_only),
        "exception_rows": len(exceptions),
        "numeric_fields": numeric, "compared_fields": fields, "key": key,
        "old_sha256": digest(old_path), "new_sha256": digest(new_path),
        "output_sha256": {name: digest(output / name) for name in
                          ("only_old.csv", "only_new.csv", "changes.csv", "exceptions.csv")},
    }
    (output / "receipt.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old", type=Path)
    parser.add_argument("new", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--key", required=True)
    parser.add_argument("--fields", required=True, help="Comma-separated columns")
    parser.add_argument("--numeric", default="", help="Comma-separated numeric columns")
    args = parser.parse_args()
    try:
        receipt = compare(args.old, args.new, args.out, key=args.key,
                          fields=[f.strip() for f in args.fields.split(",") if f.strip()],
                          numeric=[f.strip() for f in args.numeric.split(",") if f.strip()])
    except (ReconciliationError, OSError) as error:
        parser.exit(2, f"AUDIT REJECTED: {error}\n")
    print(json.dumps({k: receipt[k] for k in
                      ("old_rows", "new_rows", "unambiguous_pairs", "changed_fields_or_invalid_numeric", "only_old", "only_new", "exception_rows")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
