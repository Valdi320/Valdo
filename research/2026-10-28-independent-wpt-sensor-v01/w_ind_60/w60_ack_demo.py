"""W-IND-60 reproducible simulated ACK-loss example; no hardware or RF."""
from __future__ import annotations
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from w_link import AckTracker, ModuleReceiver

def demo():
    tx = AckTracker(7, 123)
    rx = ModuleReceiver(7, timeout_ms=250)
    rx.commission_local(123, 0)
    packet = tx.start(55, 0)
    original_ack = rx.receive(packet, 1, authenticated_transport=True)
    initial_accept_ms = rx.last_ms
    # Deliberately discard the first valid application ACK.
    duplicate_data = tx.retry(60)
    recovered_ack = rx.receive(duplicate_data, 60, authenticated_transport=True)
    acknowledged = tx.accept_ack(recovered_ack, 60, authenticated_transport=True)
    # Additional unsolicited retries are bounded by the remaining allowance.
    duplicate_ack_2 = rx.receive(packet, 120, authenticated_transport=True)
    duplicate_ack_3 = rx.receive(packet, 180, authenticated_transport=True)
    return {
        "milestone": "W-IND-60",
        "source_kind": "SYNTHETIC_ONLY",
        "radio_tested": False,
        "hardware_approved": False,
        "physical_measurements": 0,
        "battery_or_dock_tested": False,
        "local_safety_cutoff_implemented": False,
        "transport_crypto_implemented": False,
        "lost_ack_recovered": bool(acknowledged and original_ack == recovered_ack),
        "freshness_unchanged_after_retransmission": rx.last_ms == initial_accept_ms == 1,
        "accepted_data_sequence": rx.last_seq,
        "max_duplicate_app_acks": 2,
        "duplicate_ack_limit_enforced": duplicate_ack_2 is not None and duplicate_ack_3 is None,
        "tx_confirmed": tx.acked,
        "simulation_time_ms_first_accept": initial_accept_ms,
    }

if __name__ == "__main__":
    print(json.dumps(demo(), indent=2, sort_keys=True))
