"""W65: fail-closed, synthetic-only ESP-NOW/OpenThread policy screening.

Original VALDO W software. This DOES NOT provision, encrypt or transmit on
a physical device, nor approve any motor, WPT, dock, BMS or battery use.
"""
from __future__ import annotations
from dataclasses import dataclass, fields
from typing import Mapping, Any

RAW_FRAME_BYTES = 22          # w_link.FRAME_LEN; cross-check in CI
W64_AESGCM_BYTES = 54         # w_ind_64.w64_aead.WIRE_LEN; cross-check in CI
ESP_NOW_V1_MTU = 250          # application payload only, per Espressif IDF 5.5
MAX_EXPIRY_MS = 250
MAX_RETRIES = 2

@dataclass(frozen=True)
class RFProfile:
    version: int
    transport: str
    privacy: str
    role: str
    peer_unicast: bool
    peer_bound: bool
    peer_lmk_bytes: int
    custom_pmk: bool
    application_aead: bool
    application_ack: bool
    crc16: bool
    sequence_numbers: bool
    expiry_ms: int
    max_retries: int
    cutoff_independent_of_rf: bool
    mac_callback_as_app_ack: bool
    persistent_epoch_anchor_qualified: bool
    app_payload_limit_bytes: int
    evidence_type: str

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "RFProfile":
        if not isinstance(data, Mapping):
            raise ValueError("configuration must be a mapping")
        names = {f.name for f in fields(cls)}
        if set(data) != names:
            raise ValueError("unknown or missing fields")
        flags = {"peer_unicast", "peer_bound", "custom_pmk",
                 "application_aead", "application_ack", "crc16",
                 "sequence_numbers", "cutoff_independent_of_rf",
                 "mac_callback_as_app_ack", "persistent_epoch_anchor_qualified"}
        ints = {"version", "peer_lmk_bytes", "expiry_ms", "max_retries",
                "app_payload_limit_bytes"}
        for k in names:
            expected = bool if k in flags else int if k in ints else str
            if type(data[k]) is not expected:
                raise ValueError(k + " wrong type")
        return cls(**data)

@dataclass(frozen=True)
class Verdict:
    bench_candidate: bool
    production_approved: bool
    reasons: tuple[str, ...]
    notes: tuple[str, ...]
    frame_bytes: int | None

    def as_dict(self):
        return dict(bench_candidate=self.bench_candidate,
                    production_approved=self.production_approved,
                    reasons=list(self.reasons), notes=list(self.notes),
                    frame_bytes=self.frame_bytes)

def assess(p: RFProfile) -> Verdict:
    """Checks declared configuration only. No actual PMK/LMK, radio or safety proof."""
    if type(p) is not RFProfile:
        raise ValueError("parse exact RFProfile")
    # Direct dataclass construction MUST NOT bypass strict JSON schema types.
    try:
        RFProfile.from_mapping({f.name: getattr(p, f.name) for f in fields(RFProfile)})
    except ValueError:
        return Verdict(False, False, ("SCHEMA_INVALID",),
                       ("No RF configuration was validated",), None)
    bad, notes = [], []
    if p.version != 1: bad.append("UNKNOWN_VERSION")
    if p.evidence_type != "SYNTHETIC_CONFIGURATION_ONLY": bad.append("UNPROVEN_EVIDENCE")
    if p.role != "sensor_telemetry": bad.append("CRITICAL_ROLE_FORBIDDEN")
    if not p.peer_unicast: bad.append("UNICAST_ONLY")
    if not p.peer_bound: bad.append("PEER_UNBOUND")
    if not p.application_ack: bad.append("APP_ACK_REQUIRED")
    if not p.crc16: bad.append("CRC_REQUIRED")
    if not p.sequence_numbers: bad.append("SEQUENCE_REQUIRED")
    if type(p.expiry_ms) is not int or not 0 < p.expiry_ms <= MAX_EXPIRY_MS:
        bad.append("TIMEOUT_INVALID")
    if type(p.max_retries) is not int or not 0 <= p.max_retries <= MAX_RETRIES:
        bad.append("RETRIES_INVALID")
    if not p.cutoff_independent_of_rf: bad.append("RF_SAFETY_FORBIDDEN")
    if p.mac_callback_as_app_ack: bad.append("MAC_ACK_NOT_APP_ACK")
    lengths = {"native_ccmp": RAW_FRAME_BYTES,
               "dual_aead": W64_AESGCM_BYTES,
               "app_aead": W64_AESGCM_BYTES}
    size = lengths.get(p.privacy)
    if size is None: bad.append("UNKNOWN_PRIVACY")
    if p.transport == "esp_now":
        if p.privacy not in ("native_ccmp", "dual_aead"):
            bad.append("ESP_NOW_CCMP_REQUIRED")
        if type(p.peer_lmk_bytes) is not int or p.peer_lmk_bytes != 16:
            bad.append("LMK_16_BYTES_REQUIRED")
        if p.custom_pmk is not True: bad.append("DEFAULT_PMK_FORBIDDEN")
        if p.privacy == "dual_aead" and p.application_aead is not True:
            bad.append("APP_AEAD_REQUIRED")
        if p.privacy == "native_ccmp" and p.application_aead is not False:
            bad.append("CCMP_ONLY_MODE_MISMATCH")
        if type(p.app_payload_limit_bytes) is not int or p.app_payload_limit_bytes != ESP_NOW_V1_MTU:
            bad.append("ESP_NOW_MTU_UNQUALIFIED")
        elif size is not None and size > p.app_payload_limit_bytes:
            bad.append("PAYLOAD_TOO_LONG")
        notes.append("Native CCMP only authenticates/encrypts a Wi-Fi hop; provisioning declarations not verified")
    elif p.transport == "openthread":
        if p.privacy != "app_aead" or p.application_aead is not True:
            bad.append("THREAD_APP_AEAD_REQUIRED")
        if p.peer_lmk_bytes != 0 or p.custom_pmk is not False:
            bad.append("ESP_NOW_KEYS_INVALID_FOR_THREAD")
        if type(p.app_payload_limit_bytes) is not int or p.app_payload_limit_bytes != 0:
            bad.append("THREAD_MTU_NOT_QUALIFIED")
        notes.append("Thread commissioning, fragmenting and radio hardware untested")
    else:
        bad.append("UNKNOWN_TRANSPORT")
    if p.privacy in ("dual_aead", "app_aead") and not p.persistent_epoch_anchor_qualified:
        notes.append("W64 application AEAD has no qualified physical antirollback anchor")
    if p.privacy == "native_ccmp":
        notes.append("CCMP key security, replay resistance and peer binding need physical verification")
    notes.append("No RF energy, latency, packet loss, EMI or physical independent cutoff measured")
    return Verdict(not bad, False, tuple(sorted(set(bad))), tuple(notes), size)

def app_byte_budget(frame_bytes: int, *, data_attempts: int = 3,
                    ack_emissions: int = 3) -> dict[str, int]:
    """Only application payload bytes; excludes MAC/CCMP airtime and energy."""
    if (type(frame_bytes) is not int or frame_bytes not in
        (RAW_FRAME_BYTES, W64_AESGCM_BYTES) or
        type(data_attempts) is not int or not 1 <= data_attempts <= 3 or
        type(ack_emissions) is not int or not 0 <= ack_emissions <= 3):
        raise ValueError("unbounded/invalid scenario")
    return {"frame_bytes": frame_bytes,
            "data_plus_ack_bytes_nominal": frame_bytes * 2,
            "scenario_max_payload_bytes": (data_attempts + ack_emissions) * frame_bytes,
            "data_attempts_upper": data_attempts,
            "ack_emissions_upper": ack_emissions}
