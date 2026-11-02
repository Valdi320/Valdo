"""W62: fail-closed epoch issuance gate for the VALDO W61 telemetry codec.

Digital-only interface. A trustworthy, atomic, anti-rollback durable store and
local provisioning are EXTERNAL dependencies, neither is implemented here.
This must never be used to authorize charging, motors or a safety cutoff.
"""
from __future__ import annotations

import hashlib
import hmac
from typing import Protocol

LEASE_DOMAIN = b"VALDO-W62-epoch-lease-v1\x00"


class LeaseBlocked(RuntimeError):
    """No credential may be issued for a rejected or unverified reservation."""


class DurableOnceStore(Protocol):
    """Hardware/OS-dependent contract, NOT implemented by W62.

    checkpoint_trusted must reject erased, corrupt, rolled-back or uninitialized
    state. reserve_once MUST atomically commit the token to nonvolatile storage
    before returning exactly True; False means duplicate/refused. The backend
    must be power-loss safe, cross-process safe, and independently audited.
    A normal file or bare flash by itself does not prove anti-rollback.
    """

    def checkpoint_trusted(self) -> bool: ...
    def reserve_once(self, token: bytes) -> bool: ...


class EpochIssuer:
    """One attempt per local commissioning object, never on a radio callback.

    Safely denies reuse only *if* the injected store satisfies DurableOnceStore.
    Epoch entropy, PSK provisioning, secure MCU storage and hardware NVM gates
    are outside W62. Do not use test vectors as deployed secrets.
    """

    def __init__(self, store: DurableOnceStore):
        if store is None or not callable(getattr(store, "checkpoint_trusted", None)) or not callable(getattr(store, "reserve_once", None)):
            raise ValueError("requires an independently qualified durable store")
        self._store = store
        self._attempted = False

    def issue(self, master_key: bytes, epoch: bytes, node_id: int, session: int):
        if self._attempted:
            raise LeaseBlocked("a new local commissioning instance is required")
        self._attempted = True  # Even a failed attempt cannot silently retry.

        # Importing AuthCodec alone doesn't enable RF, charging or other hardware.
        from w_ind_61.w61_auth import AuthCodec
        codec = AuthCodec(master_key, epoch, node_id, session)
        token = hmac.new(master_key, LEASE_DOMAIN + epoch, hashlib.sha256).digest()
        # Deliberately independent of session and node: under a single master
        # key the 128-bit epoch must never be reused for ANY commissioning.
        try:
            if self._store.checkpoint_trusted() is not True:
                raise LeaseBlocked("durable trust checkpoint unavailable")
            accepted = self._store.reserve_once(token)
            if accepted is not True:
                raise LeaseBlocked("epoch already used or reservation not committed")
        except LeaseBlocked:
            raise
        except Exception as exc:
            raise LeaseBlocked("durable reservation failed; no credential issued") from exc
        # Crash after the commit but before this return burns the epoch: safe loss.
        return codec
