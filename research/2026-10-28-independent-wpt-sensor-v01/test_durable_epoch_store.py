"""W-IND-04: all tests synthetic/local filesystem, never physical power."""
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from durable_epoch_store import (EpochJournalError, MAX_EPOCH,
                                 SQLiteEpochStore, provision_epoch_database)

class DurableEpochTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="w_ind04_")
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "epoch.db"

    def provision(self, ids=(7, 8)):
        provision_epoch_database(self.path, ids, physically_authorized=True)

    @staticmethod
    def stable(g, start=0):
        for t in range(start, start + 101, 10):
            g.observe(t, power_good=True, temperature_ok=True, fod_clear=True)

    def test_absent_refused_and_not_created(self):
        with self.assertRaises(EpochJournalError): SQLiteEpochStore(self.path)
        self.assertFalse(self.path.exists())

    def test_unauthorized_provision_refused(self):
        with self.assertRaises(PermissionError):
            provision_epoch_database(self.path, [7], physically_authorized=False)
        self.assertFalse(self.path.exists())

    def test_preexisting_database_cannot_reset_epochs(self):
        self.provision()
        with SQLiteEpochStore(self.path) as s: self.assertTrue(s.claim(7, 51))
        with self.assertRaises(FileExistsError):
            provision_epoch_database(self.path, [7], physically_authorized=True)
        with SQLiteEpochStore(self.path) as s: self.assertFalse(s.claim(7, 51))

    def test_invalid_provision_nodes(self):
        for nodes in ([], [7, 7], [0], [True], [65536], ["7"]):
            with self.subTest(nodes=nodes):
                with self.assertRaises(ValueError):
                    provision_epoch_database(self.path, nodes, physically_authorized=True)
                self.assertFalse(self.path.exists())

    def test_monotonic_reopen(self):
        self.provision()
        with SQLiteEpochStore(self.path) as s:
            self.assertTrue(s.claim(7, 42))
            self.assertFalse(s.claim(7, 41))
        with SQLiteEpochStore(self.path) as s:
            self.assertFalse(s.claim(7, 42))
            self.assertTrue(s.claim(7, 43))
            self.assertEqual(s.observed_epoch_for_test(7), 43)

    def test_unknown_node_is_denied(self):
        self.provision([7])
        with SQLiteEpochStore(self.path) as s:
            self.assertFalse(s.claim(8, 1))
            self.assertIsNone(s.observed_epoch_for_test(8))

    def test_independent_node_epochs(self):
        self.provision()
        with SQLiteEpochStore(self.path) as s:
            self.assertTrue(s.claim(7, 99))
            self.assertTrue(s.claim(8, 1))
            self.assertFalse(s.claim(7, 1))
            self.assertTrue(s.claim(8, 2))

    def test_invalid_claim_values_rejected(self):
        self.provision()
        with SQLiteEpochStore(self.path) as s:
            for node, epoch in ((0, 1), (True, 1), (7, 0), (7, True),
                                (7, MAX_EPOCH + 1), (7, 2.3), (-1, 1)):
                with self.subTest(node=node, epoch=epoch):
                    with self.assertRaises(ValueError): s.claim(node, epoch)

    def test_epoch_exhaustion_has_no_wrap(self):
        self.provision()
        with SQLiteEpochStore(self.path) as s:
            self.assertTrue(s.claim(7, MAX_EPOCH))
            self.assertFalse(s.claim(7, MAX_EPOCH))
            with self.assertRaises(ValueError): s.claim(7, MAX_EPOCH + 1)

    def test_unprovisioned_empty_sqlite_failclosed(self):
        sqlite3.connect(self.path).close()
        with self.assertRaises(EpochJournalError): SQLiteEpochStore(self.path)

    def test_garbled_file_failclosed(self):
        self.path.write_bytes(b"not a sqlite database or original valid epoch")
        with self.assertRaises(EpochJournalError): SQLiteEpochStore(self.path)

    def test_truncated_file_failclosed(self):
        self.provision()
        with SQLiteEpochStore(self.path) as s: self.assertTrue(s.claim(7, 5))
        self.path.write_bytes(self.path.read_bytes()[:36])
        with self.assertRaises(EpochJournalError): SQLiteEpochStore(self.path)

    def test_symlink_to_previously_valid_db_denied(self):
        self.provision()
        self.path.rename(self.path.with_name("old.db"))
        self.path.symlink_to("old.db")
        with self.assertRaises(EpochJournalError): SQLiteEpochStore(self.path)

    def test_rollback_on_before_commit_exception(self):
        self.provision()
        def inject(stage):
            if stage == "before_commit": raise IOError("injected disk error")
        with SQLiteEpochStore(self.path, checkpoint=inject) as s:
            with self.assertRaises(EpochJournalError): s.claim(7, 12)
        with SQLiteEpochStore(self.path) as s:
            self.assertEqual(s.observed_epoch_for_test(7), 0)
            self.assertTrue(s.claim(7, 12))

    def test_exception_after_commit_is_ambiguous_safe_failure(self):
        self.provision()
        def inject(stage):
            if stage == "after_commit": raise IOError("lost acknowledgement")
        with SQLiteEpochStore(self.path, checkpoint=inject) as s:
            with self.assertRaises(EpochJournalError): s.claim(7, 7)
        with SQLiteEpochStore(self.path) as s:
            self.assertEqual(s.observed_epoch_for_test(7), 7)
            self.assertFalse(s.claim(7, 7))
            self.assertTrue(s.claim(7, 8))

    def test_two_writers_same_session_only_one_wins(self):
        self.provision()
        results, errors = [], []
        barrier = threading.Barrier(2)
        def run():
            try:
                with SQLiteEpochStore(self.path) as s:
                    barrier.wait(timeout=2)
                    results.append(s.claim(7, 987))
            except BaseException as exc:
                errors.append(str(exc))
        threads = [threading.Thread(target=run) for _ in range(2)]
        for t in threads: t.start()
        for t in threads: t.join(timeout=3)
        self.assertEqual(errors, [])
        self.assertEqual(sorted(results), [False, True])

    def test_write_lock_fails_closed(self):
        self.provision()
        with sqlite3.connect(self.path, isolation_level=None) as db:
            db.execute("BEGIN IMMEDIATE")
            with SQLiteEpochStore(self.path) as s:
                with self.assertRaises(EpochJournalError): s.claim(7, 99)
            db.execute("ROLLBACK")
        with SQLiteEpochStore(self.path) as s: self.assertTrue(s.claim(7, 99))

    def test_pragma_extra_sync_delete_journal(self):
        self.provision()
        with SQLiteEpochStore(self.path) as s:
            self.assertEqual(s.db.execute("PRAGMA synchronous").fetchone()[0], 3)
            self.assertEqual(s.db.execute("PRAGMA journal_mode").fetchone()[0], "delete")

    def test_software_crash_between_update_and_commit(self):
        self.provision()
        source = ('import os,sqlite3,sys; db=sqlite3.connect(sys.argv[1]);'
                  'db.execute("BEGIN IMMEDIATE");'
                  'db.execute("UPDATE epoch SET last_epoch=91 WHERE node_id=7");'
                  'os._exit(77)')
        proc = subprocess.run([sys.executable, "-c", source, str(self.path)],
                              timeout=5, check=False)
        self.assertEqual(proc.returncode, 77)
        with SQLiteEpochStore(self.path) as s:
            self.assertEqual(s.observed_epoch_for_test(7), 0)
            self.assertTrue(s.claim(7, 91))

    def test_w_ind_03_gate_reboot_rejects_old_epoch(self):
        from power_restart_gate import PowerFencedTelemetry
        from w_link import Frame, DATA
        self.provision([7])
        with SQLiteEpochStore(self.path) as s:
            g = PowerFencedTelemetry(7, s)
            self.stable(g)
            self.assertTrue(g.commission(100, 100, locally_authorized=True))
            self.assertIsNotNone(g.receive(Frame(DATA, 7, 100, 1, value_milli=400).encode(),
                                           100, authenticated_transport=True))
        with SQLiteEpochStore(self.path) as s:
            h = PowerFencedTelemetry(7, s)
            self.stable(h, start=200)
            self.assertFalse(h.commission(100, 300, locally_authorized=True))
            self.assertTrue(h.commission(101, 300, locally_authorized=True))
            self.assertIsNone(h.receive(Frame(DATA, 7, 100, 2, value_milli=400).encode(),
                                        300, authenticated_transport=True))
            self.assertIsNotNone(h.receive(Frame(DATA, 7, 101, 1, value_milli=400).encode(),
                                           300, authenticated_transport=True))

    def test_gate_persistence_failure_never_arms(self):
        from power_restart_gate import PowerFencedTelemetry
        self.provision()
        def inject(stage):
            if stage == "before_commit": raise IOError("synthetic commit fault")
        with SQLiteEpochStore(self.path, checkpoint=inject) as s:
            g = PowerFencedTelemetry(7, s)
            self.stable(g)
            self.assertFalse(g.commission(100, 100, locally_authorized=True))
            self.assertFalse(g.armed)
            self.assertEqual(g.fault_reason, "journal_commit_failed")

    def test_closed_db_fails_claim(self):
        self.provision()
        s = SQLiteEpochStore(self.path)
        s.close()
        with self.assertRaises(EpochJournalError): s.claim(7, 1)

if __name__ == "__main__":
    unittest.main()
