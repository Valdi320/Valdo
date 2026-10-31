"""W61: authenticated telemetry envelopes for VALDO W (software bench only).

HMAC-SHA256-128 authenticates 22-byte application frames in both directions.
No encryption, physical radio, secure key storage, or safety authority.
"""
from __future__ import annotations
import hashlib
import hmac
from w_link import ACK, DATA, FRAME_LEN, AckTracker, Frame, ModuleReceiver

TAG_LEN = 16
WIRE_LEN = FRAME_LEN + TAG_LEN
DOMAIN = b"VALDO-W61-APP-AUTH-v1\x00"


def hkdf32(ikm: bytes, salt: bytes, info: bytes) -> bytes:
    """RFC 5869 HKDF-SHA256, 32-byte extract + single-block expand."""
    prk = hmac.new(salt, ikm, hashlib.sha256).digest()
    return hmac.new(prk, info + b"\x01", hashlib.sha256).digest()


class AuthCodec:
    """A single, OFFLINE-provisioned peer/session; epoch uniqueness is external.

    16-byte epoch MUST be freshly and securely random for EVERY commissioning,
    not merely the existing 32-bit session counter. Keys need secure storage;
    no internal nonvolatile uniqueness/secure provisioning is implemented.
    """

    def __init__(self, master_key: bytes, epoch: bytes, node_id: int, session: int):
        if type(master_key) is not bytes or len(master_key) < 32 or not any(master_key):
            raise ValueError("requires a nonzero 256-bit-or-longer secret")
        if type(epoch) is not bytes or len(epoch) != 16 or not any(epoch):
            raise ValueError("requires a nonzero 128-bit epoch")
        if type(node_id) is not int or not 0 <= node_id <= 0xFFFF:
            raise ValueError("invalid node")
        if type(session) is not int or not 0 < session <= 0xFFFFFFFF:
            raise ValueError("invalid session")
        self.node_id, self.session = node_id, session
        context = DOMAIN + node_id.to_bytes(2, "big") + session.to_bytes(4, "big")
        self._keys = {
            DATA: hkdf32(master_key, epoch, context + b"/DATA"),
            ACK: hkdf32(master_key, epoch, context + b"/ACK"),
        }

    def _check(self, frame_bytes: bytes, kind: int) -> None:
        if type(frame_bytes) is not bytes or type(kind) is not int or kind not in (DATA, ACK):
            raise ValueError("wrong input or frame direction")
        frame = Frame.decode(frame_bytes)  # Also validates the legacy CRC.
        if frame.kind != kind or frame.node_id != self.node_id or frame.session != self.session:
            raise ValueError("wrong kind, node, or session")

    def seal(self, frame_bytes: bytes, kind: int) -> bytes:
        self._check(frame_bytes, kind)
        tag = hmac.new(self._keys[kind], DOMAIN + bytes([kind]) + frame_bytes,
                       hashlib.sha256).digest()[:TAG_LEN]
        return frame_bytes + tag

    def open(self, wire_bytes: bytes, kind: int) -> bytes | None:
        if type(wire_bytes) is not bytes or len(wire_bytes) != WIRE_LEN or type(kind) is not int or kind not in (DATA, ACK):
            return None
        payload, presented_tag = wire_bytes[:-TAG_LEN], wire_bytes[-TAG_LEN:]
        expected_tag = hmac.new(self._keys[kind], DOMAIN + bytes([kind]) + payload,
                                hashlib.sha256).digest()[:TAG_LEN]
        if not hmac.compare_digest(expected_tag, presented_tag):
            return None
        try:
            self._check(payload, kind)
        except (ValueError, TypeError):
            return None
        return payload


class AuthenticatedSender:
    """Reject unauthenticated ACKs BEFORE passing them to AckTracker."""

    def __init__(self, codec: AuthCodec, retry_ms: int = 60, expiry_ms: int = 240):
        self._codec = codec
        self._tx = AckTracker(codec.node_id, codec.session, retry_ms, expiry_ms)

    def start(self, value_milli: int, now_ms: int) -> bytes:
        return self._codec.seal(self._tx.start(value_milli, now_ms), DATA)

    def retry(self, now_ms: int) -> bytes | None:
        payload = self._tx.retry(now_ms)
        return self._codec.seal(payload, DATA) if payload is not None else None

    def accept_ack(self, envelope: bytes, now_ms: int) -> bool:
        payload = self._codec.open(envelope, ACK)
        return (self._tx.accept_ack(payload, now_ms, authenticated_transport=True)
                if payload is not None else False)

    @property
    def acked(self) -> int:
        return self._tx.acked

    @property
    def failed(self) -> int:
        return self._tx.failed


class AuthenticatedReceiver:
    """Auth-gated, telemetry-only receiver. No motor, dock, or safety permissions."""

    def __init__(self, codec: AuthCodec, commissioned_ms: int = 0, timeout_ms: int = 250):
        self._codec = codec
        self._rx = ModuleReceiver(codec.node_id, timeout_ms)
        self._rx.commission_local(codec.session, commissioned_ms)

    def receive(self, envelope: bytes, now_ms: int) -> bytes | None:
        self._rx.tick(now_ms)  # Timeout/clock latch independently of MAC validity.
        payload = self._codec.open(envelope, DATA)
        if payload is None:
            return None
        ack = self._rx.receive(payload, now_ms, authenticated_transport=True)
        return self._codec.seal(ack, ACK) if ack is not None else None

    def tick(self, now_ms: int) -> bool:
        return self._rx.tick(now_ms)

    @property
    def last_ms(self) -> int | None:
        return self._rx.last_ms

    @property
    def last_seq(self) -> int:
        return self._rx.last_seq

    @property
    def latched_fault(self) -> bool:
        return self._rx.latched_fault
