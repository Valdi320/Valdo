"""Reproducible W63 JSON evidence, SQLite disk file + FAKE RAM ANCHOR only."""
import json
import shutil
import tempfile
from pathlib import Path
from w63_anchored_sqlite import AnchoredSqliteJournal
from test_w63 import FakeAnchor, T1, T2, BreakAfterAnchor

with tempfile.TemporaryDirectory() as tmp:
    db = Path(tmp) / "journal.db"
    anchor = FakeAnchor()  # NOT antirollback: test only
    ledger = AnchoredSqliteJournal.initialize_new(db, anchor)
    first = ledger.reserve_once(T1)
    opened_again = AnchoredSqliteJournal(db, anchor)
    old_rejected = not opened_again.reserve_once(T1)
    snap = Path(tmp) / "old_snapshot.db"
    shutil.copyfile(db, snap)
    second = opened_again.reserve_once(T2)
    shutil.copyfile(snap, db)
    rollback_blocked = not opened_again.checkpoint_trusted() and not opened_again.reserve_once(T2)

with tempfile.TemporaryDirectory() as tmp:
    db = Path(tmp) / "journal.db"
    anchor = FakeAnchor()
    AnchoredSqliteJournal.initialize_new(db, anchor)
    simulated_commit_gap = not BreakAfterAnchor(db, anchor).reserve_once(T1)
    permanently_blocked = not AnchoredSqliteJournal(db, anchor).checkpoint_trusted()

d = {
    "hito": "W-IND-63",
    "evidence_type": "SYNTHETIC_ANCHOR_PLUS_REAL_TEMP_SQLITE_FILE",
    "sqlite_commit_tested": True,
    "first_epoch_written": first,
    "duplicate_denied_after_object_restart": old_rejected,
    "second_epoch_written": second,
    "rollback_snapshot_detected": rollback_blocked,
    "injected_anchor_db_commit_gap_detected": simulated_commit_gap and permanently_blocked,
    "hardware_approved": False,
    "real_antirollback_anchor_proven": False,
    "power_cut_measured": False,
    "radio_tested": False,
    "battery_or_BMS_connected": False,
    "real_wpt_tested": False,
}
assert all(d[k] for k in (
    "first_epoch_written", "duplicate_denied_after_object_restart", "second_epoch_written",
    "rollback_snapshot_detected", "injected_anchor_db_commit_gap_detected"))
print(json.dumps(d, indent=2, sort_keys=True))
