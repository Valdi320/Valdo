"""Deterministic, synthetic-only W93 ACK type-boundary demonstration."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from w_link import ACK, AckTracker, Frame


def receive(flag):
    tx = AckTracker(17, 93)
    data = Frame.decode(tx.start(1234, 100))
    forged_but_crc_valid_ack = Frame(ACK, 17, 93, data.seq, ack_seq=data.seq).encode()
    return tx.accept_ack(forged_but_crc_valid_ack, 105, authenticated_transport=flag)


def main():
    cases = ["false", "true", "1", 1, [1], {"true": True}, object()]
    # This tests the *type contract*, not the authenticity of a real peer.
    rejected = [type(x).__name__ + ":" + repr(x) if type(x) is not object else "object" for x in cases if not receive(x)]
    evidence = {
        "milestone": "W-IND-93",
        "evidence_type": "SYNTHETIC_ONLY",
        "accepted_string_false_flag": receive("false"),
        "accepted_explicit_true_flag": receive(True),
        "rejected_truthy_non_boolean_cases": rejected,
        "wire_crc_authentication": False,
        "cryptography_performed": False,
        "real_radio_used": False,
        "hardware_release": "BLOCKED",
        "battery_BMS_dock_connected": False,
        "notes": "Caller must cryptographically verify HMAC/AEAD before passing literal True; no radio, power or safety authority"
    }
    print(json.dumps(evidence, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
