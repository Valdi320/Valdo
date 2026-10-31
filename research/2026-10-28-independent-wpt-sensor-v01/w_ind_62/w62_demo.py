"""W62 deterministic fixture ONLY: no physical NVM, entropy, radio or charging."""
from __future__ import annotations
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from w_ind_61.w61_auth import AuthenticatedReceiver, AuthenticatedSender
from w_ind_62.w62_epoch_lease import EpochIssuer, LeaseBlocked

KEY = bytes(range(1, 33))  # PUBLIC test constant: never provision onto a robot
EPOCH_OLD = bytes(range(101, 117))
EPOCH_NEW = bytes(range(117, 133))


class FixtureStore:
    """Retains state across *objects*, not process/power loss. Test-only."""
    def __init__(self):
        self.seen = set()
        self.healthy = True

    def checkpoint_trusted(self):
        return self.healthy

    def reserve_once(self, token):
        if token in self.seen:
            return False
        self.seen.add(token)
        return True


def demo():
    local_tx, local_rx = FixtureStore(), FixtureStore()
    tx_old = AuthenticatedSender(EpochIssuer(local_tx).issue(KEY, EPOCH_OLD, 7, 123))
    rx_old = AuthenticatedReceiver(EpochIssuer(local_rx).issue(KEY, EPOCH_OLD, 7, 123))
    old_wire = tx_old.start(55, 0)
    old_ack = rx_old.receive(old_wire, 1)
    old_ok = tx_old.accept_ack(old_ack, 2)
    try:
        EpochIssuer(local_rx).issue(KEY, EPOCH_OLD, 7, 124)
        reused_epoch_refused = False
    except LeaseBlocked:
        reused_epoch_refused = True
    tx_new = AuthenticatedSender(EpochIssuer(local_tx).issue(KEY, EPOCH_NEW, 7, 123))
    rx_new = AuthenticatedReceiver(EpochIssuer(local_rx).issue(KEY, EPOCH_NEW, 7, 123))
    old_packet_refused = rx_new.receive(old_wire, 1) is None
    new_wire = tx_new.start(56, 2)
    new_ack = rx_new.receive(new_wire, 3)
    new_ok = tx_new.accept_ack(new_ack, 4)
    return {
        "milestone": "W-IND-62",
        "evidence_type": "SYNTHETIC_ONLY",
        "storage_type": "test_in_memory_only_not_nvm",
        "physical_measurements": 0, "radio_tested": False,
        "hardware_approved": False, "antirollback_hardware_validated": False,
        "entropy_source_qualified": False, "key_provisioning_implemented": False,
        "encryption_implemented": False, "battery_or_dock_tested": False,
        "old_session_operated_before_restart": bool(old_ok),
        "same_epoch_recommission_rejected": reused_epoch_refused,
        "captured_old_data_rejected_after_new_epoch": old_packet_refused,
        "new_epoch_authenticated_ack_accepted": bool(new_ok),
        "store_tokens_per_side": [len(local_tx.seen), len(local_rx.seen)],
    }


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2, sort_keys=True))
