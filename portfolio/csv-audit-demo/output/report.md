# Synthetic-safe, review-only CSV audit

Source file: sample_input.csv
Original SHA-256: bc01998406782a74f960918ec02cac4301bd2f69e3ea0a620afdf1bc3363643b
Input records: 5
Output records: 5
Review records: 5
Candidate pairs: 2 (capped: False)

## Issues
- duplicate_id_review: 2
- invalid_decimal: 1
- missing_required: 1
- possible_same_name_review: 4

## Limitations
- No automatic deletion or merging; every original record was preserved.
- Repeated identifiers and matching names may be legitimate; flagged for review.
- Identical names never prove real-world identity.
- Numeric checks use dot-decimal values, with no auto conversion.
- All checks are limited to the authorized input, not external facts.
