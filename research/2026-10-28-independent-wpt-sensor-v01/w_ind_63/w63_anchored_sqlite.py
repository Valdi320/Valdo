"""W63: experimental SQLite epoch journal with an EXTERNAL trusted anchor.

NOT a standalone anti-rollback store. An independently qualified, atomic,
power-fail-safe TrustedAnchor must be supplied. Do not enable robot hardware.
"""
from __future__ import annotations

import hashlib
import os
import sqlite3
from pathlib import Path
from typing import Protocol
from urllib.parse import quote

GENESIS = hashlib.sha256(b"VALDO-W63-EPOCH-JOURNAL-GENESIS-v1\0").digest()
DOMAIN = b"VALDO-W63-EPOCH-JOURNAL-ENTRY-v1\0"


class JournalBlocked(RuntimeError):
    """Missing/corrupt/rolled-back/untrusted state. No credential issued."""


class TrustedAnchor(Protocol):
    """External NON-SOFTWARE security prerequisite, not implemented here.

    read_checkpoint: trusted durable (counter, 32-byte digest).
    advance_from: atomic durable compare-and-swap, never decreases counter.
    Must survive power loss and reject rollback/replacement; arbitrary files,
    test fakes or an ordinary SQLite database do NOT implement this guarantee.
    """
    def read_checkpoint(self) -> tuple[int, bytes]: ...
    def advance_from(self, old: tuple[int, bytes], new: tuple[int, bytes]) -> bool: ...


def _entry_hash(previous: bytes, number: int, token: bytes) -> bytes:
    return hashlib.sha256(DOMAIN + previous + number.to_bytes(8, "big") + token).digest()


def _valid_checkpoint(value: object) -> bool:
    return (type(value) is tuple and len(value) == 2
            and type(value[0]) is int and 0 <= value[0] <= 2**63 - 2
            and type(value[1]) is bytes and len(value[1]) == 32)


class AnchoredSqliteJournal:
    """A SQLite side of W62 DurableOnceStore, *conditional* on real anchor.

    `checkpoint_trusted()` cannot validate the physical trustworthiness of an
    injected anchor. Tests use an untrusted fake: synthetic evidence only.
    """

    def __init__(self, path: str | Path, anchor: TrustedAnchor):
        self.path = Path(path).absolute()
        if anchor is None or not callable(getattr(anchor, "read_checkpoint", None)) \
                or not callable(getattr(anchor, "advance_from", None)):
            raise ValueError("an independently qualified anchor is required")
        self.anchor = anchor

    @classmethod
    def initialize_new(cls, path: str | Path, anchor: TrustedAnchor) -> "AnchoredSqliteJournal":
        """One-time explicit genesis, only when anchor reports fresh genesis.

        DOES NOT provision the anchor. Never auto-initialize an erased database.
        Incomplete initialization must be inspected, not silently retried.
        """
        j = cls(path, anchor)
        if j.path.is_symlink() or j.path.exists():
            raise JournalBlocked("journal already exists; refuse overwrite")
        try:
            if anchor.read_checkpoint() != (0, GENESIS):
                raise JournalBlocked("trusted virgin anchor not established")
            # Exclusive create refuses overwrite even if another initializer races.
            fd = os.open(j.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            os.close(fd)
            c = j._connect()
            try:
                c.execute("BEGIN IMMEDIATE")
                c.execute("CREATE TABLE checkpoint (id INTEGER PRIMARY KEY CHECK(id=1), number INTEGER NOT NULL, digest BLOB NOT NULL)")
                c.execute("CREATE TABLE tokens (number INTEGER PRIMARY KEY CHECK(number>0), token BLOB NOT NULL UNIQUE)")
                c.execute("INSERT INTO checkpoint VALUES (1, 0, ?)", (GENESIS,))
                c.commit()
            finally:
                c.close()
            # Directory durability matters on Linux; still requires real FS proof.
            dfd = os.open(j.path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
            try:
                os.fsync(dfd)
            finally:
                os.close(dfd)
            if not j.checkpoint_trusted():
                raise JournalBlocked("genesis checkpoint did not verify")
            return j
        except JournalBlocked:
            raise
        except Exception as e:
            raise JournalBlocked("genesis failed; no implicit recovery") from e

    def _connect(self) -> sqlite3.Connection:
        if self.path.is_symlink() or not self.path.is_file():
            raise JournalBlocked("missing or symlinked journal")
        uri = "file:" + quote(str(self.path), safe="/") + "?mode=rw"
        c = sqlite3.connect(uri, uri=True, timeout=3, isolation_level=None)
        try:
            mode = c.execute("PRAGMA journal_mode").fetchone()[0]
            c.execute("PRAGMA synchronous=EXTRA")  # stronger than FULL in DELETE mode
            c.execute("PRAGMA trusted_schema=OFF")
            if mode.lower() != "delete" or c.execute("PRAGMA synchronous").fetchone()[0] != 3:
                raise JournalBlocked("required SQLite durability pragmas unsupported")
            return c
        except Exception:
            c.close()
            raise

    def _check(self, c: sqlite3.Connection) -> tuple[int, bytes]:
        if c.execute("PRAGMA quick_check(1)").fetchone() != ("ok",):
            raise JournalBlocked("database integrity check failed")
        rows = c.execute("SELECT number,digest FROM checkpoint WHERE id=1").fetchall()
        if len(rows) != 1:
            raise JournalBlocked("checkpoint missing")
        number, stored_root = rows[0]
        if type(number) is not int or type(stored_root) is not bytes or len(stored_root) != 32:
            raise JournalBlocked("invalid checkpoint")
        root, seen, count = GENESIS, set(), 0
        for n, token in c.execute("SELECT number,token FROM tokens ORDER BY number"):
            if type(n) is not int or n != count + 1 or type(token) is not bytes or len(token) != 32 or token in seen:
                raise JournalBlocked("invalid or duplicate journal entry")
            seen.add(token)
            root = _entry_hash(root, n, token)
            count += 1
        if (count, root) != (number, stored_root):
            raise JournalBlocked("journal chain inconsistent")
        trusted = self.anchor.read_checkpoint()
        if not _valid_checkpoint(trusted) or trusted != (count, root):
            raise JournalBlocked("external anchor differs: rollback/crash/erasure")
        return count, root

    def checkpoint_trusted(self) -> bool:
        c = None
        try:
            c = self._connect()
            c.execute("BEGIN IMMEDIATE")
            self._check(c)
            c.rollback()
            return True
        except Exception:
            return False
        finally:
            if c is not None:
                c.close()

    def _after_anchor_advanced(self) -> None:
        """Fault-injection seam; override ONLY in isolated tests."""
        return None

    def reserve_once(self, token: bytes) -> bool:
        if type(token) is not bytes or len(token) != 32:
            return False
        c = None
        try:
            c = self._connect()
            c.execute("BEGIN IMMEDIATE")
            number, root = self._check(c)  # re-check under write lock
            if c.execute("SELECT 1 FROM tokens WHERE token=?", (token,)).fetchone():
                c.rollback()
                return False
            if number >= 2**63 - 2:
                raise JournalBlocked("counter overflow")
            newer = (number + 1, _entry_hash(root, number + 1, token))
            c.execute("INSERT INTO tokens VALUES (?, ?)", (newer[0], token))
            c.execute("UPDATE checkpoint SET number=?, digest=? WHERE id=1", newer)
            # Anchor advances FIRST. If DB later fails, mismatch locks out future
            # issues, rather than allowing a reused epoch. Availability is lost.
            if self.anchor.advance_from((number, root), newer) is not True:
                raise JournalBlocked("anchor refused durable atomic CAS")
            self._after_anchor_advanced()
            c.commit()
            return True
        except Exception:
            if c is not None:
                try:
                    c.rollback()
                except Exception:
                    pass
            return False
        finally:
            if c is not None:
                c.close()
