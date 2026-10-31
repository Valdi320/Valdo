"""Offline, deterministic adversarial tests; absolutely no hardware or radio."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from w_link import ACK, DATA, FRAME_LEN, Frame
from w_ind_61.w61_auth import (hkdf32, AuthCodec, AuthenticatedSender,
                               AuthenticatedReceiver, TAG_LEN, WIRE_LEN)

SECRET = bytes(range(1, 33))  # Test vector only! NEVER put in live hardware.
EPOCH = bytes(range(101, 117))  # Nonrandom test vector; NOT provisionable.


def codec(secret=SECRET, epoch=EPOCH, node=7, session=123):
    return AuthCodec(secret, epoch, node, session)


def raw(value=55, seq=1, node=7, session=123):
    return Frame(DATA, node, session, seq, value_milli=value).encode()


class AuthEnvelopeTests(unittest.TestCase):
    def test_rfc5869_vector_case1(self):
        # RFC 5869 Appendix A.1, independent authoritative HKDF test vector.
        ikm = bytes([0x0b] * 22)
        salt = bytes(range(0x00, 0x0d))
        info = bytes(range(0xf0, 0xfa))
        expected = bytes.fromhex("3cb25f25faacd57a90434f64d0362f2a"
                                 "2d2d0a90cf1a5a4c5db02d56ecc4c5bf")
        self.assertEqual(hkdf32(ikm, salt, info), expected)

    def test_no_confidentiality_claim(self):
        # Signed packet remains readable; this is NOT encryption.
        wire = codec().seal(raw(value=531), DATA)
        self.assertEqual(wire[:FRAME_LEN], raw(value=531))

    def test_dimensions(self):
        self.assertEqual(FRAME_LEN, 22)
        self.assertEqual(TAG_LEN, 16)
        self.assertEqual(WIRE_LEN, 38)

    def test_data_round_trip(self):
        c = codec()
        self.assertEqual(c.open(c.seal(raw(), DATA), DATA), raw())

    def test_ack_round_trip(self):
        c = codec()
        x = Frame(ACK, 7, 123, 1, ack_seq=1).encode()
        self.assertEqual(c.open(c.seal(x, ACK), ACK), x)

    def test_deterministic_mac(self):
        c = codec()
        self.assertEqual(c.seal(raw(), DATA), c.seal(raw(), DATA))

    def test_modified_payload_with_recalculated_crc_rejected(self):
        c = codec()
        original = c.seal(raw(), DATA)
        altered = raw(value=56)  # Fully valid FRAME and CRC; no valid MAC.
        self.assertIsNone(c.open(altered + original[-TAG_LEN:], DATA))

    def test_modified_mac_rejected(self):
        c = codec()
        v = bytearray(c.seal(raw(), DATA))
        v[-1] ^= 1
        self.assertIsNone(c.open(bytes(v), DATA))

    def test_peer_key_mismatch(self):
        self.assertIsNone(codec(bytes(range(33, 65))).open(codec().seal(raw(), DATA), DATA))

    def test_epoch_mismatch(self):
        self.assertIsNone(codec(epoch=bytes(range(1, 17))).open(codec().seal(raw(), DATA), DATA))

    def test_node_mismatch(self):
        self.assertIsNone(codec(node=8).open(codec().seal(raw(), DATA), DATA))

    def test_session_mismatch(self):
        self.assertIsNone(codec(session=124).open(codec().seal(raw(), DATA), DATA))

    def test_direction_reflection(self):
        self.assertIsNone(codec().open(codec().seal(raw(), DATA), ACK))

    def test_data_cannot_be_sealed_as_ack(self):
        with self.assertRaises(ValueError):
            codec().seal(raw(), ACK)

    def test_invalid_length_and_type(self):
        c = codec()
        self.assertIsNone(c.open(raw(), DATA))
        self.assertIsNone(c.open(c.seal(raw(), DATA)[:-1], DATA))
        self.assertIsNone(c.open(bytearray(c.seal(raw(), DATA)), DATA))
        self.assertIsNone(c.open(None, DATA))

    def test_wrong_direction_type(self):
        c = codec()
        self.assertIsNone(c.open(c.seal(raw(), DATA), 13))
        self.assertIsNone(c.open(c.seal(raw(), DATA), True))
        with self.assertRaises(ValueError):
            c.seal(raw(), 13)

    def test_invalid_secret(self):
        for key in (b"A" * 31, b"", b"\0" * 32, "X" * 32, bytearray(b"X" * 32)):
            with self.subTest(key=type(key)):
                with self.assertRaises(ValueError):
                    AuthCodec(key, EPOCH, 7, 123)

    def test_invalid_epoch(self):
        for epoch in (b"", b"\0" * 16, b"A" * 15, b"A" * 17, bytearray(EPOCH)):
            with self.subTest(epoch=type(epoch)):
                with self.assertRaises(ValueError):
                    AuthCodec(SECRET, epoch, 7, 123)

    def test_bad_node_or_session(self):
        for node, sess in ((True, 123), (-1, 123), (65536, 123), (7, 0), (7, False), (7, 2**32)):
            with self.subTest(node=node,session=sess):
                with self.assertRaises(ValueError):
                    AuthCodec(SECRET, EPOCH, node, sess)

    def test_corrupted_crc_cannot_be_signed(self):
        data = bytearray(raw()); data[-1] ^= 1
        with self.assertRaises(ValueError):
            codec().seal(bytes(data), DATA)


class IntegrationTests(unittest.TestCase):
    def test_send_receive_ack(self):
        c = codec(); tx = AuthenticatedSender(c); rx = AuthenticatedReceiver(c)
        ack = rx.receive(tx.start(55, 0), 1)
        self.assertIsNotNone(ack)
        self.assertTrue(tx.accept_ack(ack, 2))
        self.assertEqual(tx.acked, 1)
        self.assertEqual(rx.last_seq, 1)

    def test_lost_ack_two_retries_without_reprocessing(self):
        c = codec(); tx = AuthenticatedSender(c); rx = AuthenticatedReceiver(c)
        initial = tx.start(55, 0); a1 = rx.receive(initial, 1)
        self.assertIsNotNone(a1)
        retry = tx.retry(60)
        self.assertEqual(retry, initial)
        a2 = rx.receive(retry, 60)
        self.assertEqual(a2, a1)
        self.assertTrue(tx.accept_ack(a2, 61))
        self.assertEqual(rx.last_ms, 1)
        self.assertEqual(rx.last_seq, 1)

    def test_forged_ack_crc_valid_cannot_confirm(self):
        c = codec(); tx = AuthenticatedSender(c)
        tx.start(55, 0)
        forged_raw_ack = Frame(ACK, 7, 123, 1, ack_seq=1).encode()
        self.assertFalse(tx.accept_ack(forged_raw_ack + b"\x00" * TAG_LEN, 1))
        self.assertEqual(tx.acked, 0)

    def test_raw_data_rejected_by_receiver(self):
        rx = AuthenticatedReceiver(codec())
        self.assertIsNone(rx.receive(raw(), 1))
        self.assertIsNone(rx.last_ms)

    def test_old_epoch_replay_after_new_commission(self):
        tx = AuthenticatedSender(codec())
        pkt = tx.start(55, 0)
        rx_new = AuthenticatedReceiver(codec(epoch=bytes(range(1,17))))
        self.assertIsNone(rx_new.receive(pkt, 1))
        self.assertEqual(rx_new.last_seq, 0)

    def test_stale_packet_does_not_refresh_link(self):
        c = codec(); tx = AuthenticatedSender(c); rx = AuthenticatedReceiver(c)
        packet = tx.start(55, 0); self.assertIsNotNone(rx.receive(packet, 1))
        self.assertIsNone(rx.receive(packet, 260))
        self.assertTrue(rx.latched_fault)
        self.assertIsNone(rx.receive(packet, 261))

    def test_malformed_wire_does_not_refresh_link(self):
        c = codec(); tx = AuthenticatedSender(c); rx = AuthenticatedReceiver(c)
        self.assertIsNotNone(rx.receive(tx.start(55, 0), 1))
        self.assertIsNone(rx.receive(b"X" * WIRE_LEN, 200))
        self.assertEqual(rx.last_ms, 1)
        self.assertFalse(rx.tick(252))
        self.assertTrue(rx.latched_fault)

    def test_time_rollback_latches(self):
        c = codec(); tx = AuthenticatedSender(c); rx = AuthenticatedReceiver(c)
        packet = tx.start(55, 10)
        self.assertIsNotNone(rx.receive(packet, 11))
        self.assertIsNone(rx.receive(packet, 10))
        self.assertTrue(rx.latched_fault)

    def test_mismatched_peer_node(self):
        tx = AuthenticatedSender(codec())
        rx = AuthenticatedReceiver(codec(node=9))
        self.assertIsNone(rx.receive(tx.start(55, 0), 1))


if __name__ == "__main__":
    unittest.main()
