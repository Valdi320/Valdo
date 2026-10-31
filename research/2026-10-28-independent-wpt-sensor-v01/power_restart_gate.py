"""W-IND-03: brownout-fenced, NON-SAFETY telemetry state machine (original VALDO code).

NOT a hardware cutoff, firmware authenticator, battery charger, or persistence backend.
The external power_good input is a test/driver signal; radio must never operate the
real power cutoff. Persistent EpochStore.claim MUST atomically commit to durable NVM
before returning True in a product. This module provides only an in-memory TEST fake.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol
from w_link import ModuleReceiver, MAX_SEQ

class EpochStore(Protocol):
    def claim(self, node_id: int, session: int) -> bool:
        """Return True only AFTER durable monotonic commit (contract, not implemented)."""

class VolatileEpochStore:
    """TEST ONLY. Survives simulated object replacement, NOT actual reset/power loss."""
    def __init__(self):
        self.last: dict[int, int] = {}
        self.fail_writes = False

    def claim(self, node_id: int, session: int) -> bool:
        if self.fail_writes:
            raise IOError('simulated journal failure')
        prev = self.last.get(node_id, 0)
        if not 0 < session <= MAX_SEQ or session <= prev:
            return False
        self.last[node_id] = session
        return True

@dataclass(frozen=True)
class GatePolicy:
    settle_ms: int = 100  # TARGET ONLY, not an electrical measurement
    sample_max_gap_ms: int = 20  # TARGET ONLY; driver must provide periodic readings
    telemetry_timeout_ms: int = 250

    def __post_init__(self):
        for field in ('settle_ms', 'sample_max_gap_ms', 'telemetry_timeout_ms'):
            value = getattr(self, field)
            if type(value) is not int or value <= 0 or value > 60000:
                raise ValueError('invalid policy '+field)

class PowerFencedTelemetry:
    """Require stabilized supply AND local re-commissioning after every fault.

    Power-good, thermal and foreign-object signals are externally supervised INPUTS.
    The class only masks telemetry. The TX must be cut OFF physically by dedicated
    current/thermal/FOD circuitry independent of CPU/radio and this Python code.
    """
    def __init__(self, node_id: int, journal: EpochStore, policy: GatePolicy | None = None):
        if type(node_id) is not int or not 0 < node_id <= 0xFFFF:
            raise ValueError('invalid node ID')
        self.node_id = node_id
        self.journal = journal
        self.policy = policy if policy is not None else GatePolicy()
        self.rx = ModuleReceiver(node_id, timeout_ms=self.policy.telemetry_timeout_ms)
        self.last_now: int | None = None
        self.last_sample: int | None = None
        self.good_since: int | None = None
        self.supply_good = False
        self.health_ok = False
        self.armed = False
        self.fault_reason = 'uncommissioned'

    def _clock(self, now_ms: int) -> bool:
        if type(now_ms) is not int or now_ms < 0 or (self.last_now is not None and now_ms < self.last_now):
            self._trip('invalid_or_reversed_time')
            self.good_since = None
            self.last_sample = None
            self.supply_good = False
            self.health_ok = False
            return False
        self.last_now = now_ms
        return True

    def _trip(self, reason: str) -> None:
        self.armed = False
        self.fault_reason = reason
        self.rx.fault()

    def observe(self, now_ms: int, *, power_good: bool, temperature_ok: bool, fod_clear: bool) -> None:
        """Sample external health; all unknown signals fail closed. No hardware actions."""
        if not self._clock(now_ms):
            return
        if not all(type(x) is bool for x in (power_good, temperature_ok, fod_clear)):
            self.supply_good = False
            self.health_ok = False
            self.good_since = None
            self._trip('unknown_health_signal')
            return
        sample_gap = None if self.last_sample is None else now_ms-self.last_sample
        self.last_sample = now_ms
        self.supply_good = power_good
        self.health_ok = temperature_ok and fod_clear
        if not power_good or not self.health_ok:
            self.good_since = None
            self._trip('power_loss' if not power_good else 'thermal_or_fod')
            return
        if sample_gap is None or sample_gap > self.policy.sample_max_gap_ms:
            if sample_gap is not None:
                self._trip('missed_power_monitor_samples')
            self.good_since = now_ms
            return
        if self.good_since is None:
            self.good_since = now_ms

    def ready(self, now_ms: int) -> bool:
        if not self._clock(now_ms):
            return False
        if (self.last_sample is None or now_ms-self.last_sample > self.policy.sample_max_gap_ms):
            self.good_since = None
            self._trip('stale_power_monitor')
            return False
        return (self.supply_good and self.health_ok and self.good_since is not None
                and now_ms - self.good_since >= self.policy.settle_ms)

    def commission(self, session: int, now_ms: int, *, locally_authorized: bool) -> bool:
        """True only after external local approval, supply settle and journal commit.

        locally_authorized is a TEST HOOK, NOT an authenticated physical operator.
        The node must coordinate this counter with a crypto-protected host protocol.
        """
        if type(locally_authorized) is not bool or not locally_authorized:
            return False
        if type(session) is not int or not 0 < session <= MAX_SEQ:
            return False
        if not self.ready(now_ms):
            return False
        try:
            if not self.journal.claim(self.node_id, session):
                self._trip('reused_epoch')
                return False
        except Exception:
            self._trip('journal_commit_failed')
            return False
        self.rx = ModuleReceiver(self.node_id, timeout_ms=self.policy.telemetry_timeout_ms)
        self.rx.commission_local(session, now_ms)
        self.armed = True
        self.fault_reason = ''
        return True

    def receive(self, packet: bytes, now_ms: int, *, authenticated_transport: bool) -> bytes | None:
        if not self.ready(now_ms) or not self.armed:
            return None
        if type(authenticated_transport) is not bool or not authenticated_transport:
            return None
        reply = self.rx.receive(packet, now_ms, authenticated_transport=True)
        if self.rx.latched_fault:
            self._trip('radio_telemetry_timeout')
        return reply

    def fresh(self, now_ms: int) -> bool:
        if not self.ready(now_ms) or not self.armed:
            return False
        good = self.rx.tick(now_ms)
        if self.rx.latched_fault:
            self._trip('radio_telemetry_timeout')
        return good
