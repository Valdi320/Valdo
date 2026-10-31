"""W64: optional application-layer AES-256-GCM confidentiality for bench telemetry.

No radio, provisioning, secure antirollback anchor or power hardware is included.
The epoch MUST be unique per key across reboots; W62/W63 do not prove hardware.
DO NOT use to control motors, charge, safety cutoffs or lithium.
"""
from __future__ import annotations

import threading
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
from w_link import ACK, DATA, FRAME_LEN, Frame, AckTracker, ModuleReceiver
from w_ind_61.w61_auth import hkdf32

MAGIC = b"WE"
VERSION = 1
PREFIX_LEN = 4
NONCE_LEN = 12
TAG_LEN = 16
WIRE_LEN = PREFIX_LEN + NONCE_LEN + FRAME_LEN + TAG_LEN  # 54 bytes
DOMAIN = b"VALDO-W64-AEAD-TELEMETRY-v1\x00"


class AeadCodec:
    """Bench reference only; production requires trusted W62 epoch issuance.

    A unique 16-byte epoch per master key is required for every commissioning.
    Nonce is deterministic from (direction, seq) and unique IF sequence never
    repeats under the same epoch/key. This object enforces nonce monotonicity
    only during its lifetime; persistence across reboot requires an external,
    qualified, atomic antirollback store and secure entropy for epochs.
    """

    def __init__(self, master_key: bytes, epoch: bytes, node_id: int, session: int):
        if type(master_key) is not bytes or len(master_key) < 32 or not any(master_key):
            raise ValueError("requires a nonzero >=256-bit secret")
        if type(epoch) is not bytes or len(epoch) != 16 or not any(epoch):
            raise ValueError("requires a nonzero 128-bit unique epoch")
        if type(node_id) is not int or not 0 <= node_id <= 65535:
            raise ValueError("invalid node")
        if type(session) is not int or not 0 < session <= 0xFFFFFFFF:
            raise ValueError("invalid session")
        self.node_id, self.session = node_id, session
        self._context = node_id.to_bytes(2, 'big') + session.to_bytes(4, 'big')
        self._keys = {kind: AESGCM(hkdf32(master_key, epoch, DOMAIN + self._context + bytes([kind])))
                      for kind in (DATA, ACK)}
        self._last = {}  # kind -> (seq, plaintext, wire), per-process only
        self._lock = threading.Lock()
        self._tx_blocked = False

    def _check(self, plain: bytes, kind: int) -> Frame:
        if type(plain) is not bytes or type(kind) is not int or kind not in (DATA, ACK):
            raise ValueError("invalid frame or direction")
        frame = Frame.decode(plain)  # CRC + canonical field validation
        if frame.kind != kind or frame.node_id != self.node_id or frame.session != self.session:
            raise ValueError("incorrect kind, peer or session")
        return frame

    @staticmethod
    def _nonce(kind: int, seq: int) -> bytes:
        return b"W64\x00" + bytes([kind]) + b"\x00\x00\x00" + seq.to_bytes(4, 'big')

    def seal(self, plain: bytes, kind: int) -> bytes:
        frame = self._check(plain, kind)
        with self._lock:
            if self._tx_blocked:
                raise ValueError("session transmit latched off")
            prev = self._last.get(kind)
            if prev is not None and frame.seq <= prev[0]:
                if frame.seq == prev[0] and plain == prev[1]:
                    return prev[2]  # retransmit IDENTICAL ciphertext, no reuse with new plaintext
                self._tx_blocked = True
                raise ValueError("unsafe nonce/sequence reuse or rollback; recommission")
            header = MAGIC + bytes((VERSION, kind))
            nonce = self._nonce(kind, frame.seq)
            try:
                wire = header + nonce + self._keys[kind].encrypt(nonce, plain, DOMAIN + self._context + header)
            except Exception:
                self._tx_blocked = True
                raise
            self._last[kind] = (frame.seq, plain, wire)
            return wire

    def open(self, wire: bytes, kind: int) -> bytes | None:
        if type(wire) is not bytes or len(wire) != WIRE_LEN or type(kind) is not int or kind not in (DATA, ACK):
            return None
        header, nonce, encrypted = wire[:PREFIX_LEN], wire[PREFIX_LEN:PREFIX_LEN + NONCE_LEN], wire[PREFIX_LEN + NONCE_LEN:]
        if header != MAGIC + bytes((VERSION, kind)):
            return None
        try:
            plain = self._keys[kind].decrypt(nonce, encrypted, DOMAIN + self._context + header)
            frame = self._check(plain, kind)
            if nonce != self._nonce(kind, frame.seq):
                return None
            return plain
        except (InvalidTag, ValueError, TypeError):
            return None


class EncryptedSender:
    """Application ACK still required; AEAD has NO functional safety authority."""

    def __init__(self, codec: AeadCodec, retry_ms: int = 60, expiry_ms: int = 240):
        self.codec = codec
        self.tx = AckTracker(codec.node_id, codec.session, retry_ms, expiry_ms)

    def start(self, value_milli: int, now_ms: int) -> bytes:
        return self.codec.seal(self.tx.start(value_milli, now_ms), DATA)

    def retry(self, now_ms: int) -> bytes | None:
        plain = self.tx.retry(now_ms)
        return self.codec.seal(plain, DATA) if plain is not None else None

    def accept_ack(self, wire: bytes, now_ms: int) -> bool:
        plain = self.codec.open(wire, ACK)
        return self.tx.accept_ack(plain, now_ms, authenticated_transport=True) if plain is not None else False


class EncryptedReceiver:
    """Never treats RF delivery, even authenticated, as a safety signal."""

    def __init__(self, codec: AeadCodec, commissioned_ms: int = 0, timeout_ms: int = 250):
        self.codec = codec
        self.rx = ModuleReceiver(codec.node_id, timeout_ms)
        self.rx.commission_local(codec.session, commissioned_ms)

    def receive(self, wire: bytes, now_ms: int) -> bytes | None:
        self.rx.tick(now_ms)  # faults can latch BEFORE decrypt; invalid input cannot refresh
        plain = self.codec.open(wire, DATA)
        if plain is None:
            return None
        ack = self.rx.receive(plain, now_ms, authenticated_transport=True)
        return self.codec.seal(ack, ACK) if ack is not None else None

    def tick(self, now_ms: int) -> bool:
        return self.rx.tick(now_ms)
