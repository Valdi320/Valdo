"""W-IND-93: fail-closed application ACK proof-type boundary, software only."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from w_link import ACK, DATA, AckTracker, Frame, ModuleReceiver


def pair(*, node=17, session=93, when=100):
    tracker = AckTracker(node, session)
    packet = tracker.start(1234, when)
    data = Frame.decode(packet)
    ack = Frame(ACK, node, session, data.seq, ack_seq=data.seq).encode()
    return tracker, ack, packet


class TruthinessExplosion:
    def __bool__(self):
        raise AssertionError("auth flag must never be coerced")


class TypeBoundaryTests(unittest.TestCase):
    def test_only_literal_boolean_true_allows_well_formed_ack(self):
        sender, ack, _ = pair()
        self.assertTrue(sender.accept_ack(ack, 105, authenticated_transport=True))
        self.assertEqual(sender.acked, 1)
        self.assertIsNone(sender.pending)

    def test_truthy_string_false_cannot_count_ack(self):
        sender, ack, _ = pair()
        self.assertFalse(sender.accept_ack(ack, 105, authenticated_transport="false"))
        self.assertEqual(sender.acked, 0)
        self.assertIsNotNone(sender.pending)

    def test_truthy_nonboolean_values_rejected(self):
        for value in ("true", "1", 1, [True], {"authenticated": True}, object()):
            with self.subTest(value=repr(value)):
                sender, ack, _ = pair()
                self.assertFalse(sender.accept_ack(ack, 105, authenticated_transport=value))
                self.assertEqual(sender.acked, 0)

    def test_falsy_non_boolean_values_rejected(self):
        for value in (0, "", [], None):
            with self.subTest(value=repr(value)):
                sender, ack, _ = pair()
                self.assertFalse(sender.accept_ack(ack, 105, authenticated_transport=value))

    def test_false_boolean_rejected(self):
        sender, ack, _ = pair()
        self.assertFalse(sender.accept_ack(ack, 105, authenticated_transport=False))

    def test_dangerous_truthiness_not_evaluated(self):
        sender, ack, _ = pair()
        self.assertFalse(sender.accept_ack(ack, 105, authenticated_transport=TruthinessExplosion()))

    def test_bad_auth_then_valid_mac_verified_by_external_caller(self):
        sender, ack, _ = pair()
        self.assertFalse(sender.accept_ack(ack, 105, authenticated_transport="false"))
        self.assertTrue(sender.accept_ack(ack, 106, authenticated_transport=True))
        self.assertEqual(sender.acked, 1)

    def test_correctly_framed_crc_does_not_authenticate(self):
        sender, ack, _ = pair()
        self.assertEqual(Frame.decode(ack).kind, ACK)
        self.assertFalse(sender.accept_ack(ack, 105, authenticated_transport="authenticated"))
        self.assertEqual(sender.acked, 0)

    def test_true_flag_does_not_bypass_crc(self):
        sender, ack, _ = pair()
        damaged = ack[:-1] + bytes([ack[-1] ^ 0x01])
        self.assertFalse(sender.accept_ack(damaged, 105, authenticated_transport=True))

    def test_true_flag_does_not_bypass_session(self):
        sender, _, _ = pair()
        other = Frame(ACK, 17, 94, 1, ack_seq=1).encode()
        self.assertFalse(sender.accept_ack(other, 105, authenticated_transport=True))

    def test_true_flag_does_not_bypass_expiry(self):
        sender, ack, _ = pair()
        self.assertFalse(sender.accept_ack(ack, 340, authenticated_transport=True))
        self.assertEqual(sender.failed, 1)

    def test_true_flag_does_not_allow_duplicate_receipt(self):
        sender, ack, _ = pair()
        self.assertTrue(sender.accept_ack(ack, 105, authenticated_transport=True))
        self.assertFalse(sender.accept_ack(ack, 106, authenticated_transport=True))

    def test_receiver_has_same_strict_boolean_contract(self):
        receiver = ModuleReceiver(17)
        receiver.commission_local(93, 100)
        data = Frame(DATA, 17, 93, 1, value_milli=1).encode()
        self.assertIsNone(receiver.receive(data, 101, authenticated_transport=1))
        self.assertEqual(receiver.last_seq, 0)
        self.assertIsNotNone(receiver.receive(data, 102, authenticated_transport=True))
        self.assertEqual(receiver.last_seq, 1)

    def test_true_is_not_radio_or_cryptographic_evidence(self):
        sender, ack, _ = pair()
        self.assertTrue(sender.accept_ack(ack, 105, authenticated_transport=True))
        # This is a test-stub. Real call sites MUST verify the HMAC/AEAD.
        self.assertEqual(sender.acked, 1)


if __name__ == "__main__":
    unittest.main()
