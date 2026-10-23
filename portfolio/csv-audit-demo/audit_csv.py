#!/usr/bin/env python3
"""Traceable, review-only CSV QA. Python 3.10+ stdlib; no external services."""
from __future__ import annotations
import argparse
import collections
import csv
import hashlib
import itertools
import json
import re
import sys
import unicodedata
from decimal import Decimal, InvalidOperation
from pathlib import Path


class AuditError(ValueError):
    pass


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for part in iter(lambda: f.read(1048576), b""):
            h.update(part)
    return h.hexdigest()


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.casefold())
    value = "".join(c for c in value if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^\w]+", " ", value).split())


def fields(arg: str) -> list[str]:
    return [s.strip() for s in arg.split(",") if s.strip()]


def write_rows(path: Path, headings: list[str], records: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(headings)
        w.writerows(records)


def analyze(source: Path, dest: Path, id_col: str = "", name_col: str = "",
            city_col: str = "", required: list[str] | None = None,
            numeric: list[str] | None = None, limit: int = 5000,
            column_limit: int = 30, pair_limit: int = 2500) -> dict:
    source, dest = source.resolve(), dest.resolve()
    if not source.is_file():
        raise AuditError("Source CSV not found")
    if source.parent == dest or source == dest:
        raise AuditError("Output must be a separate directory")
    if min(limit, column_limit, pair_limit) < 1:
        raise AuditError("Safety limits must be positive")
    required, numeric = required or [], numeric or []
    try:
        with source.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f, strict=True)
            header = next(reader, None)
            if not header or any(not h.strip() for h in header):
                raise AuditError("Missing or empty CSV headings")
            if len(header) > column_limit:
                raise AuditError("Too many columns for agreed tier")
            if len(header) != len({h.strip() for h in header}):
                raise AuditError("Duplicate headings; review source manually")
            if {"__audit_record", "__audit_status", "__audit_issues"} & set(header):
                raise AuditError("Reserved audit column present in source")
            missing_cols = [x for x in [id_col, name_col, city_col, *required, *numeric]
                            if x and x not in header]
            if missing_cols:
                raise AuditError("Unknown columns: " + ", ".join(sorted(set(missing_cols))))
            records = []
            for record_num, row in enumerate(reader, 1):
                if record_num > limit:
                    raise AuditError("Input exceeds agreed row limit")
                if len(row) != len(header):
                    raise AuditError(f"Record {record_num} has {len(row)} fields; "
                                     f"expected {len(header)}. No fields dropped.")
                records.append(row)
    except (UnicodeError, csv.Error) as e:
        raise AuditError("Invalid UTF-8 CSV: " + str(e)) from e

    loc = {name: i for i, name in enumerate(header)}
    ids = collections.Counter(r[loc[id_col]].strip() for r in records
                              if id_col and r[loc[id_col]].strip())
    groups = collections.defaultdict(list)
    if name_col:
        for i, row in enumerate(records, 1):
            n = normalize(row[loc[name_col]])
            c = normalize(row[loc[city_col]]) if city_col else ""
            if n:
                groups[(n, c)].append(i)
    matching = set()
    pairs = []
    capped = False
    for (n, c), indices in sorted(groups.items()):
        for a, b in itertools.combinations(indices, 2):
            matching.update([a, b])
            if len(pairs) < pair_limit:
                pairs.append([str(a), str(b), n, c, "REVIEW ONLY; not proven to be identical"])
            else:
                capped = True

    annotated, exceptions = [], []
    counts = collections.Counter()
    for idx, row in enumerate(records, 1):
        issues = []
        for field in required:
            if not row[loc[field]].strip():
                issues.append(("missing_required", field))
        if id_col and row[loc[id_col]].strip() and ids[row[loc[id_col]].strip()] > 1:
            issues.append(("duplicate_id_review", id_col))
        for field in numeric:
            value = row[loc[field]].strip()
            if value:
                try:
                    if not Decimal(value).is_finite():
                        raise InvalidOperation()
                except (InvalidOperation, ValueError):
                    issues.append(("invalid_decimal", field))
        if idx in matching:
            issues.append(("possible_same_name_review", name_col))
        for code, field in issues:
            counts[code] += 1
            exceptions.append([str(idx), code, field])
        annotated.append([*row, str(idx), "REVIEW" if issues else "OK",
                          ";".join(f"{code}:{field}" for code, field in issues)])

    dest.mkdir(parents=True, exist_ok=True)
    outputs = {
        "annotated_rows.csv": ([*header, "__audit_record", "__audit_status", "__audit_issues"], annotated),
        "exceptions.csv": (["source_record", "issue_type", "field"], exceptions),
        "candidate_duplicates.csv": (["record_a", "record_b", "normalized_name", "normalized_city", "warning"], pairs),
    }
    digest = {}
    for filename, (head, body) in outputs.items():
        p = dest / filename
        write_rows(p, head, body)
        digest[filename] = sha256(p)
    with (dest / "annotated_rows.csv").open(encoding="utf-8", newline="") as f:
        check = sum(1 for _ in csv.reader(f)) - 1
    if check != len(records):
        raise AuditError("FAIL: output record count mismatch")

    receipt = {
        "version": 1,
        "source_filename": source.name,
        "source_sha256": sha256(source),
        "original_unmodified": True,
        "automatically_merged_or_deleted": False,
        "source_records": len(records),
        "annotated_records": check,
        "source_columns": header,
        "rules": {"id": id_col, "name": name_col, "city": city_col,
                  "required": required, "numeric_decimal_dot": numeric},
        "issues": dict(sorted(counts.items())),
        "candidate_pairs": len(pairs),
        "candidate_pairs_capped": capped,
        "output_sha256": digest,
    }
    (dest / "receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8")
    report = [
        "# Synthetic-safe, review-only CSV audit", "",
        f"Source file: {source.name}", f"Original SHA-256: {receipt['source_sha256']}",
        f"Input records: {len(records)}", f"Output records: {check}",
        f"Review records: {sum(row[-2] == 'REVIEW' for row in annotated)}",
        f"Candidate pairs: {len(pairs)} (capped: {capped})", "",
        "## Issues", *[f"- {k}: {v}" for k, v in sorted(counts.items())], "",
        "## Limitations",
        "- No automatic deletion or merging; every original record was preserved.",
        "- Repeated identifiers and matching names may be legitimate; flagged for review.",
        "- Identical names never prove real-world identity.",
        "- Numeric checks use dot-decimal values, with no auto conversion.",
        "- All checks are limited to the authorized input, not external facts.",
    ]
    (dest / "report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return receipt


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source", type=Path)
    p.add_argument("--outdir", type=Path, required=True)
    p.add_argument("--id", default="")
    p.add_argument("--name", default="")
    p.add_argument("--city", default="")
    p.add_argument("--required", default="")
    p.add_argument("--numeric", default="")
    p.add_argument("--limit", type=int, default=5000)
    args = p.parse_args()
    try:
        result = analyze(args.source, args.outdir, args.id, args.name,
                         args.city, fields(args.required), fields(args.numeric), args.limit)
        print(json.dumps({"status": "PASS", "records": result["source_records"],
                          "issues": result["issues"], "candidate_pairs": result["candidate_pairs"]},
                         ensure_ascii=False))
        return 0
    except (AuditError, OSError) as exc:
        print("AUDIT FAILED: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
