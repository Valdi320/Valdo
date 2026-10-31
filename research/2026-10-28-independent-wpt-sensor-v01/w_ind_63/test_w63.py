"""W63 tests of a REAL SQLite FILE plus an UNTRUSTED fake anchor.

Not a hardware NVM/antirollback/EMI/charging/radio test.
"""
from __future__ import annotations
import hashlib
import shutil
import sqlite3
import sys
import tempfile
import threading
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from w_ind_63.w63_anchored_sqlite import AnchoredSqliteJournal, GENESIS, JournalBlocked

T1 = hashlib.sha256(b"public epoch token 1").digest()
T2 = hashlib.sha256(b"public epoch token 2").digest()


class FakeAnchor:
    """SYNTHETIC ONLY: mutable RAM, not antirollback or power-fail-safe."""
    def __init__(self):
        self.state = (0, GENESIS)
        self.lock = threading.Lock()
        self.deny = False

    def read_checkpoint(self):
        with self.lock:
            return self.state

    def advance_from(self, old, new):
        with self.lock:
            if self.deny or old != self.state or new[0] != old[0] + 1:
                return False
            self.state = new
            return True


class BreakAfterAnchor(AnchoredSqliteJournal):
    def _after_anchor_advanced(self):
        raise OSError("injected crash before SQLite COMMIT")


class JournalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "epoch.db"
        self.anchor = FakeAnchor()

    def new(self):
        return AnchoredSqliteJournal.initialize_new(self.path, self.anchor)

    def test_no_implicit_creation(self):
        j = AnchoredSqliteJournal(self.path, self.anchor)
        self.assertFalse(j.checkpoint_trusted())
        self.assertFalse(j.reserve_once(T1))
        self.assertFalse(self.path.exists())

    def test_initial_genesis_and_checkpoint(self):
        j = self.new()
        self.assertTrue(j.checkpoint_trusted())
        self.assertEqual(self.anchor.state, (0, GENESIS))

    def test_created_with_restricted_permissions(self):
        self.new()
        self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)

    def test_persisted_token_after_reopening_database(self):
        self.assertTrue(self.new().reserve_once(T1))
        j2 = AnchoredSqliteJournal(self.path, self.anchor)
        self.assertTrue(j2.checkpoint_trusted())
        self.assertFalse(j2.reserve_once(T1))
        self.assertTrue(j2.reserve_once(T2))
        self.assertEqual(self.anchor.state[0], 2)

    def test_duplicate_refused(self):
        j = self.new()
        self.assertTrue(j.reserve_once(T1))
        self.assertFalse(j.reserve_once(T1))
        self.assertEqual(self.anchor.state[0], 1)

    def test_old_snapshot_restore_is_blocked_by_anchor(self):
        j = self.new()
        self.assertTrue(j.reserve_once(T1))
        snapshot = Path(self.temp.name) / "snapshot.db"
        shutil.copyfile(self.path, snapshot)
        self.assertTrue(j.reserve_once(T2))
        shutil.copyfile(snapshot, self.path)  # attacks only our TEMP test file
        self.assertFalse(j.checkpoint_trusted())
        self.assertFalse(j.reserve_once(T2))

    def test_truncated_database_fails_closed(self):
        j = self.new()
        self.path.write_bytes(b"not SQLite")
        self.assertFalse(j.checkpoint_trusted())
        self.assertFalse(j.reserve_once(T1))

    def test_erased_database_fails_closed(self):
        j = self.new()
        self.path.unlink()
        self.assertFalse(j.checkpoint_trusted())
        self.assertFalse(j.reserve_once(T1))

    def test_reinitialization_rejected(self):
        self.new()
        with self.assertRaises(JournalBlocked): self.new()

    def test_anchor_not_at_genesis_rejects_initialization(self):
        self.anchor.state = (1, GENESIS)
        with self.assertRaises(JournalBlocked): self.new()
        self.assertFalse(self.path.exists())

    def test_anchor_forgery_mismatch_fails_closed(self):
        j = self.new()
        self.anchor.state = (1, b"x" * 32)
        self.assertFalse(j.checkpoint_trusted())
        self.assertFalse(j.reserve_once(T1))

    def test_anchor_type_confusion_is_denied(self):
        j = self.new()
        self.anchor.state = (True, GENESIS)
        self.assertFalse(j.checkpoint_trusted())

    def test_anchor_cas_refusal_does_not_commit(self):
        j = self.new()
        self.anchor.deny = True
        self.assertFalse(j.reserve_once(T1))
        self.anchor.deny = False
        self.assertTrue(j.checkpoint_trusted())
        self.assertTrue(j.reserve_once(T1))

    def test_crash_after_external_advance_locks_out(self):
        self.new()
        crashed = BreakAfterAnchor(self.path, self.anchor)
        self.assertFalse(crashed.reserve_once(T1))
        j = AnchoredSqliteJournal(self.path, self.anchor)
        self.assertFalse(j.checkpoint_trusted())
        self.assertFalse(j.reserve_once(T1))
        self.assertEqual(self.anchor.state[0], 1)

    def test_corrupt_token_row_detected_even_if_anchor_unchanged(self):
        j = self.new()
        self.assertTrue(j.reserve_once(T1))
        with sqlite3.connect(self.path) as c:
            c.execute("UPDATE tokens SET token=? WHERE number=1", (T2,))
        self.assertFalse(j.checkpoint_trusted())

    def test_malformed_token_rejected(self):
        j = self.new()
        for bad in (None, b"abc", "a" * 32, bytearray(T1), True):
            self.assertFalse(j.reserve_once(bad))
        self.assertEqual(self.anchor.state[0], 0)

    def test_two_threads_only_one_can_claim_token(self):
        j = self.new()
        results = []
        def worker():
            results.append(j.reserve_once(T1))
        threads = [threading.Thread(target=worker) for _ in range(6)]
        for t in threads: t.start()
        for t in threads: t.join()
        self.assertEqual(results.count(True), 1)
        self.assertEqual(results.count(False), 5)
        self.assertEqual(self.anchor.state[0], 1)

    def test_ledger_rejects_symlink(self):
        target = Path(self.temp.name) / "target.db"
        target.write_text("file not trusted")
        self.path.symlink_to(target)
        self.assertFalse(AnchoredSqliteJournal(self.path, self.anchor).checkpoint_trusted())
        self.assertFalse(AnchoredSqliteJournal(self.path, self.anchor).reserve_once(T1))

    def test_protocol_supports_w62_epoch_issuer_when_checkout_present(self):
        try:
            from w_ind_62.w62_epoch_lease import EpochIssuer, LeaseBlocked
        except ImportError:
            self.skipTest("full repository required for W62 integration")
        j = self.new()
        key = bytes(range(1,33))
        epoch = bytes(range(101,117))
        codec = EpochIssuer(j).issue(key, epoch, 7, 123)
        self.assertEqual(codec.node_id, 7)
        with self.assertRaises(LeaseBlocked): EpochIssuer(AnchoredSqliteJournal(self.path, self.anchor)).issue(key, epoch, 7, 123)


if __name__ == "__main__": unittest.main()
