"""Experimental transport-neutral telemetry; NOT a safety controller or authentication implementation.
Original VALDO W code, Python 3.10+, standard library only.
"""
from __future__ import annotations
from dataclasses import dataclass
import struct

MAGIC = b"VW"
VERSION = 1
DATA = 1
ACK = 2
BODY = struct.Struct("!2sBBHIIIH")
FRAME_LEN = BODY.size + 2
MAX_SEQ = 0xFFFFFFFF


def crc16_ccitt(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


@dataclass(frozen=True)
class Frame:
    kind: int
    node_id: int
    session: int
    seq: int
    ack_seq: int = 0
    value_milli: int = 0

    def encode(self) -> bytes:
        if self.kind not in (DATA, ACK):
            raise ValueError("invalid kind")
        for value, limit in ((self.node_id, 0xFFFF), (self.session, MAX_SEQ),
                             (self.seq, MAX_SEQ), (self.ack_seq, MAX_SEQ),
                             (self.value_milli, 0xFFFF)):
            if not isinstance(value, int) or not 0 <= value <= limit:
                raise ValueError("invalid numeric field")
        if self.session == 0 or self.seq == 0:
            raise ValueError("session and sequence must be nonzero")
        if (self.kind == DATA and self.ack_seq != 0) or (self.kind == ACK and self.value_milli != 0):
            raise ValueError("reserved field is nonzero")
        body = BODY.pack(MAGIC, VERSION, self.kind, self.node_id,
                         self.session, self.seq, self.ack_seq, self.value_milli)
        return body + struct.pack("!H", crc16_ccitt(body))

    @classmethod
    def decode(cls, packet: bytes) -> Frame:
        if len(packet) != FRAME_LEN:
            raise ValueError("wrong frame length")
        body, crc_bytes = packet[:-2], packet[-2:]
        if crc16_ccitt(body) != struct.unpack("!H", crc_bytes)[0]:
            raise ValueError("bad CRC")
        magic, version, kind, node, session, seq, ack_seq, value = BODY.unpack(body)
        if magic != MAGIC or version != VERSION:
            raise ValueError("wrong protocol")
        frame = cls(kind, node, session, seq, ack_seq, value)
        frame.encode()  # Canonical fields and reserved bits.
        return frame


class ModuleReceiver:
    """Telemetry only; never permits motors or power.

    Sessions are commissioned locally. Encrypted authenticated radio transport
    is REQUIRED externally. authenticated_transport is a TEST STUB, not crypto.
    A timeout/reversed clock latches fault until local recommissioning.
    """

    def __init__(self, node_id: int, timeout_ms: int = 250):
        if not 0 <= node_id <= 0xFFFF or timeout_ms <= 0:
            raise ValueError("invalid receiver configuration")
        self.node_id = node_id
        self.timeout_ms = timeout_ms
        self.session = None
        self.last_seq = 0
        self.last_ms = None
        self.last_clock_ms = None
        self.latched_fault = True

    def commission_local(self, session: int, now_ms: int) -> None:
        if not isinstance(session, int) or not 0 < session <= MAX_SEQ or now_ms < 0:
            raise ValueError("invalid commissioning")
        self.session = session
        self.last_seq = 0
        self.last_ms = None
        self.last_clock_ms = now_ms
        self.latched_fault = False

    def fault(self) -> None:
        self.latched_fault = True

    def _clock(self, now_ms: int) -> bool:
        if not isinstance(now_ms, int) or now_ms < 0:
            self.fault()
            return False
        if self.last_clock_ms is not None and now_ms < self.last_clock_ms:
            self.fault()
            return False
        self.last_clock_ms = now_ms
        return True

    def tick(self, now_ms: int) -> bool:
        if not self._clock(now_ms):
            return False
        if self.last_ms is not None and now_ms - self.last_ms > self.timeout_ms:
            self.fault()
        return self.fresh(now_ms)

    def fresh(self, now_ms: int) -> bool:
        return (not self.latched_fault and self.session is not None
                and self.last_ms is not None and isinstance(now_ms, int)
                and now_ms >= self.last_ms and now_ms - self.last_ms <= self.timeout_ms)

    def receive(self, packet: bytes, now_ms: int, *, authenticated_transport: bool) -> bytes | None:
        if not self._clock(now_ms):
            return None
        if self.last_ms is not None and now_ms - self.last_ms > self.timeout_ms:
            self.fault()
        if self.latched_fault or not authenticated_transport or self.session is None:
            return None
        try:
            frame = Frame.decode(packet)
        except (ValueError, TypeError, struct.error):
            return None
        if (frame.kind != DATA or frame.node_id != self.node_id
                or frame.session != self.session or frame.seq <= self.last_seq):
            return None
        self.last_seq = frame.seq
        self.last_ms = now_ms
        return Frame(ACK, self.node_id, self.session, frame.seq, ack_seq=frame.seq).encode()


class AckTracker:
    """Bounded application-ACK retries; never gates safety or charge power."""

    def __init__(self, node_id: int, session: int, retry_ms: int = 60,
                 expiry_ms: int = 240, max_attempts: int = 3):
        if not 0 <= node_id <= 0xFFFF or not 0 < session <= MAX_SEQ:
            raise ValueError("invalid peer")
        if not 0 < retry_ms < expiry_ms or max_attempts < 1:
            raise ValueError("invalid timing")
        self.node_id, self.session = node_id, session
        self.retry_ms, self.expiry_ms, self.max_attempts = retry_ms, expiry_ms, max_attempts
        self.next_seq = 1
        self.pending = None
        self.acked = 0
        self.failed = 0

    def start(self, value_milli: int, now_ms: int) -> bytes:
        if self.pending is not None:
            raise RuntimeError("one outstanding frame maximum")
        if self.next_seq > MAX_SEQ or not isinstance(now_ms, int) or now_ms < 0:
            raise ValueError("sequence exhausted or invalid time")
        frame = Frame(DATA, self.node_id, self.session, self.next_seq, value_milli=value_milli)
        packet = frame.encode()
        self.pending = {"frame": packet, "seq": self.next_seq,
                        "start": now_ms, "last": now_ms, "attempts": 1}
        self.next_seq += 1
        return packet

    def retry(self, now_ms: int) -> bytes | None:
        p = self.pending
        if p is None:
            return None
        if now_ms < p["last"] or now_ms - p["start"] >= self.expiry_ms:
            self.failed += 1
            self.pending = None
            return None
        if now_ms - p["last"] < self.retry_ms or p["attempts"] >= self.max_attempts:
            return None
        p["attempts"] += 1
        p["last"] = now_ms
        return p["frame"]

    def accept_ack(self, packet: bytes, now_ms: int, *, authenticated_transport: bool) -> bool:
        p = self.pending
        if p is None:
            return False
        if (not isinstance(now_ms, int) or now_ms < p["last"] or
                now_ms - p["start"] >= self.expiry_ms):
            self.failed += 1
            self.pending = None
            return False
        if not authenticated_transport:
            return False
        try:
            frame = Frame.decode(packet)
        except (TypeError, ValueError, struct.error):
            return False
        if (frame.kind != ACK or frame.node_id != self.node_id
                or frame.session != self.session or frame.seq != p["seq"]
                or frame.ack_seq != p["seq"]):
            return False
        self.acked += 1
        self.pending = None
        return True
