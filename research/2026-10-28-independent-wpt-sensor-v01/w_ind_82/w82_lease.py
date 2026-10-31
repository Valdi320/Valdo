"""W82: synthetic, transport-agnostic *noncritical* sensor telemetry lease.

Pure-Python reference model; neither a certified safety cutoff nor RF stack.
Privacy must be established by the actual encrypted unicast radio link.
"""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import hmac
import secrets
import struct
import zlib

MAGIC = b"W82!"
VERSION = 1
CHALLENGE, HELLO, DATA, ACK = 1, 2, 3, 4
ZERO = bytes(16)
HEADER = struct.Struct("!4sBBH16s16sIH")
CRC = struct.Struct("!I")
TAG_BYTES = 16
FRAME_BYTES = HEADER.size + CRC.size + TAG_BYTES  # 66 B, unicast only
MAX_SEQ = (1 << 32) - 1


@dataclass(frozen=True)
class Frame:
    kind: int
    module: int
    epoch: bytes
    challenge: bytes
    seq: int = 0
    value: int = 0


def _key(key: bytes) -> None:
    if not isinstance(key, bytes) or len(key) < 32:
        raise ValueError("A distinct provisioned key of at least 32 bytes is required")


def _nonce(b: bytes, *, allow_zero: bool = False) -> bool:
    return isinstance(b, bytes) and len(b) == 16 and (allow_zero or b != ZERO)


def pack(f: Frame, key: bytes) -> bytes:
    _key(key)
    if not (0 <= f.module <= 65535 and 0 <= f.seq <= MAX_SEQ and 0 <= f.value <= 65535):
        raise ValueError("field out of range")
    if f.kind not in (CHALLENGE, HELLO, DATA, ACK):
        raise ValueError("unrecognized frame")
    if not _nonce(f.challenge):
        raise ValueError("empty or invalid challenge")
    if not _nonce(f.epoch, allow_zero=f.kind == CHALLENGE):
        raise ValueError("invalid boot epoch")
    if f.kind != DATA and f.value != 0:
        raise ValueError("unexpected value in control frame")
    if f.kind in (CHALLENGE, HELLO) and f.seq != 0:
        raise ValueError("nonzero control sequence")
    if f.kind == CHALLENGE and f.epoch != ZERO:
        raise ValueError("challenge must not claim a sensor epoch")
    header = HEADER.pack(MAGIC, VERSION, f.kind, f.module, f.epoch,
                         f.challenge, f.seq, f.value)
    body = header + CRC.pack(zlib.crc32(header) & 0xFFFFFFFF)
    return body + hmac.new(key, body, hashlib.sha256).digest()[:TAG_BYTES]


def unpack(raw: bytes, key: bytes) -> Frame:
    _key(key)
    if not isinstance(raw, bytes) or len(raw) != FRAME_BYTES:
        raise ValueError("invalid packet size")
    body = raw[:-TAG_BYTES]
    tag = hmac.new(key, body, hashlib.sha256).digest()[:TAG_BYTES]
    if not hmac.compare_digest(raw[-TAG_BYTES:], tag):
        raise ValueError("authentication failure")
    header = body[:HEADER.size]
    if CRC.unpack(body[HEADER.size:])[0] != zlib.crc32(header) & 0xFFFFFFFF:
        raise ValueError("CRC failure")
    magic, ver, kind, module, epoch, challenge, seq, value = HEADER.unpack(header)
    if magic != MAGIC or ver != VERSION:
        raise ValueError("unknown protocol/version")
    f = Frame(kind, module, epoch, challenge, seq, value)
    # Canonical framing rules are the same on encode and decode.
    pack(f, key)
    return f


@dataclass(frozen=True)
class Outcome:
    event: str
    ack: bytes | None = None


class Receiver:
    """Controller-side read-only diagnostic data. No actuator or stop API."""
    def __init__(self, module: int, key: bytes, *, encrypted_unicast: bool = False,
                 lease_ms: int = 250, hello_ms: int = 500):
        _key(key)
        if not (0 <= module <= 65535 and lease_ms > 0 and hello_ms > 0):
            raise ValueError("invalid configuration")
        self.module, self.key = module, key
        self.encrypted_unicast = encrypted_unicast
        self.lease_ms, self.hello_ms = lease_ms, hello_ms
        self.last_clock = -1
        self.pending_challenge: bytes | None = None
        self.handshake_start: int | None = None
        self.last_issued_challenge: bytes | None = None
        self.session_ready_at: int | None = None
        self.epoch: bytes | None = None
        self.session_challenge: bytes | None = None
        self.seq: int | None = None
        self.value: int | None = None
        self.accepted_at: int | None = None

    def _time(self, now: int) -> None:
        if not isinstance(now, int) or now < 0 or now < self.last_clock:
            raise ValueError("controller's monotonic clock required")
        self.last_clock = now

    def _invalidate(self) -> None:
        self.epoch = self.session_challenge = self.session_ready_at = None
        self.seq = self.value = self.accepted_at = None

    def poll(self, now: int) -> bool:
        self._time(now)
        if ((self.accepted_at is not None and now - self.accepted_at > self.lease_ms)
                or (self.accepted_at is None and self.session_ready_at is not None
                    and now - self.session_ready_at > self.lease_ms)):
            self._invalidate()  # require fresh HELLO if no recent accepted data
        if self.pending_challenge is not None and now - self.handshake_start > self.hello_ms:
            self.pending_challenge = self.handshake_start = None
        return self.encrypted_unicast and self.accepted_at is not None

    def begin(self, now: int, challenge: bytes | None = None) -> bytes:
        self.poll(now)
        if not self.encrypted_unicast:
            raise PermissionError("verified encrypted unicast is a required deployment gate")
        challenge = secrets.token_bytes(16) if challenge is None else challenge
        if not _nonce(challenge) or challenge == self.last_issued_challenge:
            raise ValueError("fresh unpredictable challenge required")
        self._invalidate()  # fail closed during every re-handshake
        self.pending_challenge, self.handshake_start = challenge, now
        self.last_issued_challenge = challenge
        return pack(Frame(CHALLENGE, self.module, ZERO, challenge), self.key)

    def receive(self, raw: bytes, now: int) -> Outcome:
        self.poll(now)
        if not self.encrypted_unicast:
            return Outcome("BLOCK_PRIVACY")
        try:
            f = unpack(raw, self.key)
        except (ValueError, TypeError):
            return Outcome("BLOCK_INTEGRITY")
        if f.module != self.module:
            return Outcome("BLOCK_MODULE")
        if f.kind == HELLO:
            if self.pending_challenge is None or f.challenge != self.pending_challenge:
                return Outcome("BLOCK_HANDSHAKE_REPLAY")
            self._invalidate()
            self.epoch, self.session_challenge, self.session_ready_at = f.epoch, f.challenge, now
            self.pending_challenge = self.handshake_start = None
            return Outcome("SESSION_READY")
        if f.kind != DATA or self.epoch is None or f.epoch != self.epoch or f.challenge != self.session_challenge:
            return Outcome("BLOCK_SESSION")
        if self.seq is None and f.seq != 1:
            return Outcome("BLOCK_SEQUENCE")
        if self.seq is not None and f.seq == self.seq and f.value == self.value:
            # ACK a retry, but NEVER extend the lease with a duplicate.
            return Outcome("DUPLICATE_ACK_ONLY", pack(Frame(ACK, self.module, f.epoch, f.challenge, f.seq), self.key))
        if self.seq is not None and (self.seq == MAX_SEQ or f.seq != self.seq + 1):
            return Outcome("BLOCK_SEQUENCE")
        self.seq, self.value, self.accepted_at = f.seq, f.value, now
        return Outcome("FRESH_DATA", pack(Frame(ACK, self.module, f.epoch, f.challenge, f.seq), self.key))


class Sensor:
    """Reference sender: one outstanding sample, application ACK, bounded retries."""
    def __init__(self, module: int, key: bytes, epoch: bytes | None = None):
        _key(key)
        self.module, self.key = module, key
        self.epoch = secrets.token_bytes(16) if epoch is None else epoch
        if not _nonce(self.epoch):
            raise ValueError("fresh unpredictable boot epoch required")
        self.challenge: bytes | None = None
        self.seq = 1
        self.pending: bytes | None = None
        self.sent_at: int | None = None
        self.retries = 0

    def reboot(self, epoch: bytes | None = None) -> None:
        e = secrets.token_bytes(16) if epoch is None else epoch
        if not _nonce(e) or e == self.epoch:
            raise ValueError("boot epoch must change")
        self.epoch, self.challenge, self.seq = e, None, 1
        self.pending = self.sent_at = None
        self.retries = 0

    def hello(self, raw: bytes) -> bytes:
        f = unpack(raw, self.key)
        if f.kind != CHALLENGE or f.module != self.module:
            raise ValueError("authenticated challenge required")
        self.challenge, self.seq = f.challenge, 1
        self.pending = self.sent_at = None
        self.retries = 0
        return pack(Frame(HELLO, self.module, self.epoch, self.challenge), self.key)

    def send(self, value: int, now: int) -> bytes:
        if self.challenge is None or self.pending is not None or self.seq > MAX_SEQ or now < 0:
            raise ValueError("not paired, sequence exhausted, or awaiting application ACK")
        self.pending = pack(Frame(DATA, self.module, self.epoch, self.challenge, self.seq, value), self.key)
        self.sent_at, self.retries = now, 0
        return self.pending

    def ack(self, raw: bytes) -> bool:
        try:
            f = unpack(raw, self.key)
        except (ValueError, TypeError):
            return False
        if (self.pending is None or f.kind != ACK or f.module != self.module
                or f.epoch != self.epoch or f.challenge != self.challenge or f.seq != self.seq):
            return False
        self.pending = self.sent_at = None
        self.seq += 1
        return True

    def retry(self, now: int, *, timeout_ms: int = 60, max_retries: int = 2) -> bytes | None:
        if (self.pending is None or self.sent_at is None or timeout_ms <= 0
                or max_retries < 0 or now < self.sent_at):
            return None
        if now - self.sent_at < timeout_ms or self.retries >= max_retries:
            return None
        self.sent_at = now
        self.retries += 1
        return self.pending
