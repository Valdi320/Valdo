"""Deterministic adversarial tests; all times and packets are SYNTHETIC."""
import unittest
import zlib
import struct
import hmac
import hashlib
from w82_lease import (
    ACK, DATA, HELLO, CHALLENGE, FRAME_BYTES, MAX_SEQ, ZERO,
    Frame, Receiver, Sensor, pack, unpack,
)

K = b"EXAMPLE-NOT-A-REAL-SECRET!!".ljust(32, b"_")
K2 = b"unrelated-key".ljust(32, b"!")
E1, E2 = b"A" * 16, b"B" * 16
C1, C2 = b"a" * 16, b"b" * 16


class LeaseTests(unittest.TestCase):
    def setUp(self):
        self.r = Receiver(7, K, encrypted_unicast=True)
        self.s = Sensor(7, K, E1)

    def handshake(self, now=0, challenge=C1):
        challenge_packet = self.r.begin(now, challenge)
        hello = self.s.hello(challenge_packet)
        self.assertEqual(self.r.receive(hello, now).event, "SESSION_READY")
        return challenge_packet, hello

    def data(self, at=5, value=1234):
        raw = self.s.send(value, at)
        outcome = self.r.receive(raw, at)
        self.assertEqual(outcome.event, "FRESH_DATA")
        return raw, outcome.ack

    def test_frame_size_small_enough_for_esp_now_v1(self):
        self.assertEqual(FRAME_BYTES, 66)
        self.assertLessEqual(FRAME_BYTES, 250)

    def test_no_default_privacy_claim(self):
        r = Receiver(7, K)
        with self.assertRaises(PermissionError):
            r.begin(0, C1)
        self.assertEqual(r.receive(pack(Frame(HELLO, 7, E1, C1), K), 1).event, "BLOCK_PRIVACY")

    def test_weak_secret_rejected(self):
        with self.assertRaises(ValueError):
            Receiver(7, b"short")
        with self.assertRaises(ValueError):
            unpack(b"", b"short")

    def test_valid_handshake_is_not_valid_data(self):
        self.handshake()
        self.assertFalse(self.r.poll(1))
        self.assertIsNone(self.r.value)

    def test_data_then_app_ack(self):
        self.handshake()
        _, ack = self.data()
        self.assertTrue(self.s.ack(ack))
        self.assertTrue(self.r.poll(200))
        self.assertEqual((self.r.value, self.r.seq), (1234, 1))

    def test_mac_layer_success_not_an_app_ack(self):
        self.handshake()
        self.data()
        self.assertIsNotNone(self.s.pending)
        self.assertFalse(self.s.ack(b"MAC_CALLBACK_SUCCESS"))

    def test_mac_tamper_rejected(self):
        self.handshake()
        raw = bytearray(self.s.send(55, 1))
        raw[25] ^= 0x01
        self.assertEqual(self.r.receive(bytes(raw), 1).event, "BLOCK_INTEGRITY")
        self.assertFalse(self.r.poll(1))

    def test_crc_corruption_even_with_valid_hmac_rejected(self):
        self.handshake()
        raw = bytearray(self.s.send(55, 1))
        raw[-20] ^= 1  # CRC field
        raw[-16:] = hmac.new(K, raw[:-16], hashlib.sha256).digest()[:16]
        self.assertEqual(self.r.receive(bytes(raw), 1).event, "BLOCK_INTEGRITY")

    def test_wrong_key_rejected(self):
        self.handshake()
        raw = pack(Frame(DATA, 7, E1, C1, 1, 23), K2)
        self.assertEqual(self.r.receive(raw, 1).event, "BLOCK_INTEGRITY")

    def test_short_and_extra_packets(self):
        self.handshake()
        good = self.s.send(12, 1)
        for raw in [b"", good[:-1], good + b"\0"]:
            self.assertEqual(self.r.receive(raw, 1).event, "BLOCK_INTEGRITY")

    def test_wrong_module_rejected(self):
        self.handshake()
        raw = pack(Frame(DATA, 8, E1, C1, 1, 99), K)
        self.assertEqual(self.r.receive(raw, 1).event, "BLOCK_MODULE")

    def test_no_data_before_handshake(self):
        raw = pack(Frame(DATA, 7, E1, C1, 1, 12), K)
        self.assertEqual(self.r.receive(raw, 1).event, "BLOCK_SESSION")

    def test_wrong_challenge_hello_rejected(self):
        self.r.begin(0, C1)
        raw = pack(Frame(HELLO, 7, E1, C2), K)
        self.assertEqual(self.r.receive(raw, 1).event, "BLOCK_HANDSHAKE_REPLAY")

    def test_expired_hello_rejected(self):
        self.r.begin(0, C1)
        raw = pack(Frame(HELLO, 7, E1, C1), K)
        self.assertEqual(self.r.receive(raw, 501).event, "BLOCK_HANDSHAKE_REPLAY")

    def test_replay_old_hello_after_new_challenge(self):
        _, old_hello = self.handshake()
        self.r.begin(10, C2)
        self.assertEqual(self.r.receive(old_hello, 11).event, "BLOCK_HANDSHAKE_REPLAY")
        self.assertFalse(self.r.poll(11))

    def test_receiver_restarts_handshake_and_invalidates_data(self):
        self.handshake()
        self.data()
        self.r.begin(10, C2)
        self.assertFalse(self.r.poll(10))
        self.assertIsNone(self.r.value)

    def test_duplicate_ack_without_lease_extension(self):
        self.handshake()
        raw, ack = self.data(5)
        result = self.r.receive(raw, 240)
        self.assertEqual(result.event, "DUPLICATE_ACK_ONLY")
        self.assertEqual(result.ack, ack)
        self.assertEqual(self.r.accepted_at, 5)
        self.assertFalse(self.r.poll(256))

    def test_lost_ack_retry_idempotent(self):
        self.handshake()
        raw, _ = self.data(2)
        self.assertIsNone(self.s.retry(40))
        self.assertEqual(self.s.retry(62), raw)
        retry_ack = self.r.receive(raw, 62)
        self.assertEqual(retry_ack.event, "DUPLICATE_ACK_ONLY")
        self.assertTrue(self.s.ack(retry_ack.ack))
        self.assertEqual(self.s.seq, 2)
        self.assertEqual(self.r.accepted_at, 2)

    def test_bounded_retries(self):
        self.handshake()
        raw, _ = self.data(0)
        self.assertEqual(self.s.retry(60), raw)
        self.assertEqual(self.s.retry(120), raw)
        self.assertIsNone(self.s.retry(180))
        with self.assertRaises(ValueError):
            self.s.send(44, 181)

    def test_different_value_same_seq_is_not_duplicate(self):
        self.handshake()
        self.data(1, 1)
        forged = pack(Frame(DATA, 7, E1, C1, 1, 2), K)
        self.assertEqual(self.r.receive(forged, 2).event, "BLOCK_SEQUENCE")

    def test_rollback_sequence_rejected(self):
        self.handshake()
        _, a = self.data(1)
        self.s.ack(a)
        _, a = self.data(2)
        self.s.ack(a)
        raw = pack(Frame(DATA, 7, E1, C1, 1, 1234), K)
        self.assertEqual(self.r.receive(raw, 3).event, "BLOCK_SEQUENCE")

    def test_sequence_gap_rejected(self):
        self.handshake()
        raw = pack(Frame(DATA, 7, E1, C1, 9, 15), K)
        self.assertEqual(self.r.receive(raw, 1).event, "BLOCK_SEQUENCE")

    def test_old_epoch_after_brownout_rejected(self):
        self.handshake()
        stale, _ = self.data(1)
        self.s.reboot(E2)
        self.r.begin(2, C2)
        self.assertEqual(self.r.receive(self.s.hello(pack(Frame(CHALLENGE, 7, ZERO, C2), K)), 3).event, "SESSION_READY")
        self.assertEqual(self.r.receive(stale, 4).event, "BLOCK_SESSION")

    def test_late_first_sample_requires_new_handshake(self):
        self.handshake()
        raw = self.s.send(12, 1000)
        self.assertEqual(self.r.receive(raw, 1000).event, "BLOCK_SESSION")

    def test_reusing_previous_challenge_locally_blocked(self):
        self.r.begin(0, C1)
        with self.assertRaises(ValueError):
            self.r.begin(1, C1)

    def test_data_after_loss_requires_new_challenge(self):
        self.handshake()
        stale, _ = self.data(1)
        self.assertFalse(self.r.poll(252))
        self.assertEqual(self.r.receive(stale, 253).event, "BLOCK_SESSION")
        fresh_request = self.r.begin(254, C2)
        self.assertEqual(self.r.receive(self.s.hello(fresh_request), 255).event, "SESSION_READY")
        self.assertEqual(self.r.receive(self.s.send(99, 256), 256).event, "FRESH_DATA")

    def test_wrong_ack_never_advances_sender(self):
        self.handshake()
        _, ack = self.data(1)
        wrong = pack(Frame(ACK, 7, E1, C1, 3), K)
        self.assertFalse(self.s.ack(wrong))
        self.assertEqual(self.s.seq, 1)
        self.assertTrue(self.s.ack(ack))
        self.assertFalse(self.s.ack(ack))

    def test_stale_ack_after_reboot_ignored(self):
        self.handshake()
        _, ack = self.data(1)
        self.s.reboot(E2)
        self.assertFalse(self.s.ack(ack))

    def test_unknown_version_rejected_with_correct_mac_crc(self):
        raw = bytearray(pack(Frame(CHALLENGE, 7, ZERO, C1), K))
        raw[4] = 2
        raw[-20:-16] = struct.pack("!I", zlib.crc32(raw[:-20]))
        raw[-16:] = hmac.new(K, raw[:-16], hashlib.sha256).digest()[:16]
        with self.assertRaises(ValueError):
            unpack(bytes(raw), K)

    def test_zero_epoch_rejected(self):
        with self.assertRaises(ValueError):
            pack(Frame(HELLO, 7, ZERO, C1), K)

    def test_nonzero_control_value_rejected(self):
        with self.assertRaises(ValueError):
            pack(Frame(ACK, 7, E1, C1, 1, 2), K)

    def test_seq_wrap_is_blocked(self):
        self.handshake()
        self.r.seq, self.r.value, self.r.accepted_at = MAX_SEQ, 2, 0
        raw = pack(Frame(DATA, 7, E1, C1, 1, 5), K)
        self.assertEqual(self.r.receive(raw, 1).event, "BLOCK_SEQUENCE")

    def test_clock_regression_rejected(self):
        self.r.begin(10, C1)
        with self.assertRaises(ValueError):
            self.r.poll(9)

    def test_reboot_epoch_cannot_be_reused_locally(self):
        with self.assertRaises(ValueError):
            self.s.reboot(E1)

    def test_forged_challenge_does_not_create_session(self):
        with self.assertRaises(ValueError):
            self.s.hello(pack(Frame(DATA, 7, E1, C1, 1, 3), K))

    def test_no_actuator_command_surface(self):
        self.assertFalse(any(hasattr(self.r, method) for method in ("motor", "stop", "drive", "charge", "cut_power")))


if __name__ == "__main__":
    unittest.main()
