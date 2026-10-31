"""VALDO W-IND-04: durable monotonic telemetry epoch journal (host-only).
Original code, stdlib sqlite3. NEVER handles WPT power, lithium or motors.
Assumptions: trusted local POSIX filesystem honoring sync, no malicious NVM
rollback, externally authenticated radio, explicitly authorized provisioning.
This is NOT a flash/FRAM implementation for ESP32.
"""
from __future__ import annotations
from pathlib import Path
from contextlib import closing
from typing import Callable, Iterable
import os
import sqlite3

SCHEMA_VERSION = 1
APP_ID = 0x56415731  # Format marker, NOT authentication.
MAX_EPOCH = 0xFFFFFFFF

class EpochJournalError(RuntimeError):
    """Fail closed on missing, corrupt or uncertain durable storage."""


def _node(value: int) -> int:
    if type(value) is not int or not 1 <= value <= 65535:
        raise ValueError("invalid node ID")
    return value


def _session(value: int) -> int:
    if type(value) is not int or not 1 <= value <= MAX_EPOCH:
        raise ValueError("invalid session counter")
    return value


def provision_epoch_database(path: str | os.PathLike[str],
                             node_ids: Iterable[int],
                             *, physically_authorized: bool) -> None:
    """One-time operator provisioning. Missing DB is NEVER auto-restored at boot.

    physically_authorized is a test/API CONTRACT boolean, NOT physical auth.
    O_EXCL refuses overwrite; interrupted setup leaves a suspect file to inspect.
    """
    if physically_authorized is not True:
        raise PermissionError("operator authorization required")
    path = Path(path).absolute()
    nodes = list(node_ids)
    for item in nodes:
        _node(item)
    if not nodes or len(set(nodes)) != len(nodes):
        raise ValueError("nonempty unique node IDs required")
    if not path.parent.is_dir():
        raise ValueError("parent must exist")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    os.close(fd)
    try:
        with closing(sqlite3.connect(path, isolation_level=None, timeout=1.0)) as db:
            db.execute("PRAGMA journal_mode=DELETE")
            db.execute("PRAGMA synchronous=EXTRA")
            db.execute("BEGIN IMMEDIATE")
            db.execute(f"PRAGMA application_id={APP_ID}")
            db.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
            db.execute("CREATE TABLE epoch ("
                       "node_id INTEGER PRIMARY KEY CHECK(node_id BETWEEN 1 AND 65535),"
                       "last_epoch INTEGER NOT NULL CHECK(last_epoch BETWEEN 0 AND 4294967295)"
                       ") WITHOUT ROWID")
            db.executemany("INSERT INTO epoch(node_id,last_epoch) VALUES(?,0)",
                           [(n,) for n in nodes])
            db.execute("COMMIT")
        if hasattr(os, "O_DIRECTORY"):
            dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(dfd)
            finally:
                os.close(dfd)
    except BaseException:
        # Intentional: auto-deleting it would allow untrusted zero reset.
        raise


class SQLiteEpochStore:
    """W-IND-03 EpochStore protocol, designed for a Linux host only.

    BEGIN IMMEDIATE serializes independent writers; UPDATE is conditional.
    claim=True means SQLite COMMIT returned without error.
    """
    def __init__(self, path: str | os.PathLike[str], *,
                 checkpoint: Callable[[str], None] | None = None):
        path = Path(path).absolute()
        if not path.is_file() or path.is_symlink():
            raise EpochJournalError("journal missing or symlink")
        self.path = path
        self._checkpoint = checkpoint  # Software-only fault injection hook.
        self.db: sqlite3.Connection | None = None
        try:
            self.db = sqlite3.connect(path.as_uri() + "?mode=rw",
                                      uri=True, isolation_level=None, timeout=0.15)
            if self.db.execute("PRAGMA journal_mode=DELETE").fetchone()[0].lower() != "delete":
                raise EpochJournalError("unexpected journal mode")
            self.db.execute("PRAGMA synchronous=EXTRA")
            if self.db.execute("PRAGMA synchronous").fetchone()[0] != 3:
                raise EpochJournalError("synchronous=EXTRA unavailable")
            if self.db.execute("PRAGMA application_id").fetchone()[0] != APP_ID:
                raise EpochJournalError("unprovisioned journal")
            if self.db.execute("PRAGMA user_version").fetchone()[0] != SCHEMA_VERSION:
                raise EpochJournalError("unknown schema version")
            if self.db.execute("PRAGMA quick_check").fetchone()[0] != "ok":
                raise EpochJournalError("corrupt journal")
            self.db.execute("SELECT node_id,last_epoch FROM epoch LIMIT 1").fetchone()
        except (sqlite3.Error, OSError, EpochJournalError) as exc:
            self.close()
            if isinstance(exc, EpochJournalError):
                raise
            raise EpochJournalError("untrusted journal") from exc

    def close(self) -> None:
        if self.db is not None:
            self.db.close()
            self.db = None

    def __enter__(self) -> SQLiteEpochStore:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def claim(self, node_id: int, session: int) -> bool:
        """Reserve an epoch DURABLY before W-IND-03 can arm telemetry.

        False means non-increasing epoch or unprovisioned node.
        Exceptions always mean deny; after ambiguous commit, use NEW epoch.
        """
        _node(node_id)
        _session(session)
        if self.db is None:
            raise EpochJournalError("closed journal")
        began = False
        try:
            self.db.execute("BEGIN IMMEDIATE")
            began = True
            cur = self.db.execute(
                "UPDATE epoch SET last_epoch=? WHERE node_id=? AND last_epoch<?",
                (session, node_id, session))
            if cur.rowcount != 1:
                self.db.execute("ROLLBACK")
                return False
            if self._checkpoint is not None:
                self._checkpoint("before_commit")
            self.db.execute("COMMIT")
            began = False
            if self._checkpoint is not None:
                self._checkpoint("after_commit")
            return True
        except BaseException as exc:
            if began:
                try:
                    self.db.execute("ROLLBACK")
                except sqlite3.Error:
                    pass
            if isinstance(exc, (KeyboardInterrupt, SystemExit)):
                raise
            raise EpochJournalError("commit failed or uncertain: deny telemetry") from exc

    def observed_epoch_for_test(self, node_id: int) -> int | None:
        """Read-only laboratory helper, never external commissioning API."""
        _node(node_id)
        if self.db is None:
            raise EpochJournalError("closed journal")
        try:
            row = self.db.execute(
                "SELECT last_epoch FROM epoch WHERE node_id=?", (node_id,)
            ).fetchone()
            return None if row is None else int(row[0])
        except sqlite3.Error as exc:
            raise EpochJournalError("journal read failed") from exc
