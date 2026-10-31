"""Reproducible SYNTHETIC auth / forged-ACK rejection, NO RADIO."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from w_link import ACK, Frame
from w_ind_61.w61_auth import AuthCodec, AuthenticatedSender, AuthenticatedReceiver, TAG_LEN, WIRE_LEN


def demo():
    # Public hard-coded test constants. NEVER use them on a real device.
    codec = AuthCodec(bytes(range(1, 33)), bytes(range(101, 117)), 7, 123)
    sender, receiver = AuthenticatedSender(codec), AuthenticatedReceiver(codec)
    data = sender.start(55, 0)
    forged_ack = Frame(ACK, 7, 123, 1, ack_seq=1).encode() + b"\x00" * TAG_LEN
    forgery_rejected = not sender.accept_ack(forged_ack, 1)
    first_ack = receiver.receive(data, 2)
    retry = sender.retry(60)
    replacement_ack = receiver.receive(retry, 60)
    accepted = sender.accept_ack(replacement_ack, 61)
    return {
        "milestone": "W-IND-61", "evidence_type": "SYNTHETIC_ONLY",
        "real_radio_used": False, "hardware_approved": False,
        "physical_measurements": 0, "battery_or_dock_tested": False,
        "encryption_implemented": False, "key_storage_provisioned": False,
        "mac_algorithm": "HKDF-SHA256+HMAC-SHA256-truncated-128",
        "legacy_frame_bytes": 22, "envelope_bytes": WIRE_LEN,
        "tampered_or_forged_ack_rejected": forgery_rejected,
        "lost_ack_recovered_authentic": bool(accepted and first_ack == replacement_ack),
        "duplicate_did_not_refresh_freshness": receiver.last_ms == 2,
        "accepted_sequence": receiver.last_seq,
    }


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2, sort_keys=True))
