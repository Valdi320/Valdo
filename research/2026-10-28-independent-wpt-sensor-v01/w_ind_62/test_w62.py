"""W62 adversarial digital tests; no radio, durable hardware or batteries."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from w_link import DATA, Frame
from w_ind_61.w61_auth import AuthenticatedSender, AuthenticatedReceiver
from w_ind_62.w62_epoch_lease import EpochIssuer, LeaseBlocked, LEASE_DOMAIN

# Deliberately PUBLIC and predictable synthetic test values; NOT for deployment.
KEY = bytes(range(1, 33))
EPOCH1 = bytes(range(101, 117))
EPOCH2 = bytes(range(117, 133))


class FakeLedger:
    """Non-durable testing substitute. Do NOT deploy, does not resist rollback."""
    def __init__(self):
        self.seen = set()
        self.trusted = True
        self.fail = False
        self.bad_result = None
        self.commits = 0

    def checkpoint_trusted(self):
        return self.trusted

    def reserve_once(self, token):
        if self.fail:
            raise OSError("injected write failure")
        if self.bad_result is not None:
            return self.bad_result
        if token in self.seen:
            return False
        self.seen.add(token)
        self.commits += 1
        return True


def issue(ledger, epoch=EPOCH1, key=KEY, node=7, session=123):
    return EpochIssuer(ledger).issue(key, epoch, node, session)


class EpochLeaseTests(unittest.TestCase):
    def test_fresh_lease_creates_real_w61_codec(self):
        l = FakeLedger(); c = issue(l)
        self.assertEqual((c.node_id, c.session), (7, 123))
        self.assertEqual(l.commits, 1)

    def test_restart_rejects_old_epoch_and_old_session(self):
        l = FakeLedger(); issue(l)
        with self.assertRaises(LeaseBlocked): issue(l)
        self.assertEqual(l.commits, 1)

    def test_epoch_reuse_denied_after_session_number_change(self):
        l = FakeLedger(); issue(l)
        with self.assertRaises(LeaseBlocked): issue(l, session=456)

    def test_epoch_reuse_denied_after_node_change(self):
        l = FakeLedger(); issue(l)
        with self.assertRaises(LeaseBlocked): issue(l, node=8)

    def test_new_epoch_new_keys_accepted(self):
        l = FakeLedger(); old = issue(l)
        new = issue(l, epoch=EPOCH2)
        pkt = Frame(DATA, 7, 123, 1, value_milli=55).encode()
        self.assertIsNone(new.open(old.seal(pkt, DATA), DATA))
        self.assertEqual(l.commits, 2)

    def test_end_to_end_old_data_replay_rejected_after_restart(self):
        sender_store, receiver_store = FakeLedger(), FakeLedger()
        c_tx_old = issue(sender_store); c_rx_old = issue(receiver_store)
        tx_old, rx_old = AuthenticatedSender(c_tx_old), AuthenticatedReceiver(c_rx_old)
        wire = tx_old.start(55, 0)
        self.assertIsNotNone(rx_old.receive(wire, 1))
        c_tx_new = issue(sender_store, epoch=EPOCH2)
        c_rx_new = issue(receiver_store, epoch=EPOCH2)
        self.assertIsNone(AuthenticatedReceiver(c_rx_new).receive(wire, 1))
        tx_new, rx_new = AuthenticatedSender(c_tx_new), AuthenticatedReceiver(c_rx_new)
        self.assertTrue(tx_new.accept_ack(rx_new.receive(tx_new.start(56, 2), 3), 4))

    def test_no_store_refused(self):
        with self.assertRaises(ValueError): EpochIssuer(None)
        with self.assertRaises(ValueError): EpochIssuer(object())

    def test_untrusted_checkpoint_denies_and_burns_attempt(self):
        l = FakeLedger(); l.trusted = False
        issuer = EpochIssuer(l)
        with self.assertRaises(LeaseBlocked): issuer.issue(KEY, EPOCH1, 7, 123)
        l.trusted = True
        with self.assertRaises(LeaseBlocked): issuer.issue(KEY, EPOCH2, 7, 123)
        self.assertEqual(l.commits, 0)

    def test_erased_checkpoint_denies(self):
        l = FakeLedger(); issue(l); l.seen.clear(); l.trusted = False
        with self.assertRaises(LeaseBlocked): issue(l)

    def test_reservation_write_failure_denies(self):
        l = FakeLedger(); l.fail = True
        with self.assertRaises(LeaseBlocked): issue(l)
        self.assertEqual(l.commits, 0)

    def test_reservation_false_rejected(self):
        l = FakeLedger(); l.bad_result = False
        with self.assertRaises(LeaseBlocked): issue(l)

    def test_nonboolean_success_is_not_a_commit(self):
        l = FakeLedger(); l.bad_result = 1
        with self.assertRaises(LeaseBlocked): issue(l)

    def test_nonboolean_trust_is_not_trusted(self):
        l = FakeLedger(); l.trusted = 1
        with self.assertRaises(LeaseBlocked): issue(l)

    def test_no_retry_even_if_different_epoch(self):
        l = FakeLedger(); issuer = EpochIssuer(l)
        issuer.issue(KEY, EPOCH1, 7, 123)
        with self.assertRaises(LeaseBlocked): issuer.issue(KEY, EPOCH2, 7, 123)

    def test_invalid_secret_cannot_commit(self):
        l = FakeLedger()
        with self.assertRaises(ValueError): issue(l, key=b"x" * 8)
        self.assertEqual(l.commits, 0)

    def test_invalid_epoch_cannot_commit(self):
        l = FakeLedger()
        with self.assertRaises(ValueError): issue(l, epoch=b"\x00" * 16)
        self.assertEqual(l.commits, 0)

    def test_bad_node_cannot_commit(self):
        l = FakeLedger()
        with self.assertRaises(ValueError): issue(l, node=2**16)
        self.assertEqual(l.commits, 0)

    def test_bad_session_cannot_commit(self):
        l = FakeLedger()
        with self.assertRaises(ValueError): issue(l, session=0)
        self.assertEqual(l.commits, 0)

    def test_key_rotation_changes_reservation_namespace(self):
        l = FakeLedger(); issue(l)
        self.assertEqual(issue(l, key=bytes(range(33, 65))).node_id, 7)

    def test_ledger_exposes_no_master_or_raw_epoch(self):
        l = FakeLedger(); issue(l)
        token = next(iter(l.seen))
        self.assertEqual(len(token), 32)
        self.assertNotIn(KEY, token)
        self.assertNotIn(EPOCH1, token)
        self.assertTrue(LEASE_DOMAIN.startswith(b"VALDO"))

    def test_checkpoint_exception_denies(self):
        class DeadLedger(FakeLedger):
            def checkpoint_trusted(self):
                raise OSError("NVM unreadable")
        with self.assertRaises(LeaseBlocked): issue(DeadLedger())

    def test_simulated_crash_after_commit_burns_epoch(self):
        l = FakeLedger()
        from hashlib import sha256
        from hmac import new
        token = new(KEY, LEASE_DOMAIN + EPOCH1, sha256).digest()
        self.assertTrue(l.reserve_once(token))
        with self.assertRaises(LeaseBlocked): issue(l)

    def test_no_motor_charger_or_radio_apis(self):
        c = issue(FakeLedger())
        self.assertFalse(hasattr(c, "enable_motor"))
        self.assertFalse(hasattr(c, "enable_charge"))
        self.assertFalse(hasattr(c, "radio_send"))


if __name__ == "__main__":
    unittest.main()
