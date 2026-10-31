"""Reproducible deterministic synthetic tests; no hardware or radio required."""
import random
import unittest

from w_link import ACK, DATA, FRAME_LEN, MAX_SEQ, AckTracker, Frame, ModuleReceiver, crc16_ccitt
from power_screen import hold_up_farads, screen


class TestFraming(unittest.TestCase):
    def setUp(self):
        self.frame = Frame(DATA, 7, 0x12345678, 1, value_milli=250)
        self.raw = self.frame.encode()

    def test_roundtrip(self):
        self.assertEqual(Frame.decode(self.raw), self.frame)
        self.assertEqual(len(self.raw), FRAME_LEN)

    def test_crc_known_vector(self):
        self.assertEqual(crc16_ccitt(b"123456789"), 0x29B1)

    def test_every_single_bit_flip_detected(self):
        for i in range(len(self.raw)):
            for bit in range(8):
                damaged = bytearray(self.raw)
                damaged[i] ^= 1 << bit
                with self.assertRaises(ValueError):
                    Frame.decode(bytes(damaged))

    def test_noncanonical_data_ack(self):
        with self.assertRaises(ValueError):
            Frame(DATA, 7, 5, 1, ack_seq=1).encode()
        with self.assertRaises(ValueError):
            Frame(ACK, 7, 5, 1, ack_seq=1, value_milli=1).encode()

    def test_range(self):
        for f in (Frame(DATA, -1, 3, 1), Frame(DATA, 1, 0, 1),
                  Frame(DATA, 1, 3, 0), Frame(DATA, 1, 3, 1, value_milli=65536),
                  Frame(DATA, 1, 3, MAX_SEQ + 1), Frame(5, 1, 3, 1)):
            with self.assertRaises(ValueError):
                f.encode()

    def test_truncation_and_random_corruption(self):
        for length in range(FRAME_LEN):
            with self.assertRaises(ValueError):
                Frame.decode(self.raw[:length])
        rng = random.Random(20261028)
        for _ in range(1000):
            raw = bytearray(self.raw)
            byte_idx = rng.randrange(len(raw))
            raw[byte_idx] ^= 1 << rng.randrange(8)
            with self.assertRaises(ValueError):
                Frame.decode(raw)


class TestReceiver(unittest.TestCase):
    def setUp(self):
        self.rx = ModuleReceiver(7, timeout_ms=250)
        self.rx.commission_local(123, 0)

    def msg(self, seq=1, node_id=7, session=123):
        return Frame(DATA, node_id, session, seq, value_milli=1234).encode()

    def test_no_data_no_health(self):
        self.assertFalse(self.rx.tick(0))

    def test_ack_and_freshness(self):
        ack = self.rx.receive(self.msg(), 10, authenticated_transport=True)
        self.assertEqual(Frame.decode(ack), Frame(ACK, 7, 123, 1, ack_seq=1))
        self.assertTrue(self.rx.tick(260))
        self.assertFalse(self.rx.tick(261))
        self.assertTrue(self.rx.latched_fault)

    def test_unauthenticated_never_refreshes(self):
        self.assertIsNone(self.rx.receive(self.msg(), 10, authenticated_transport=False))
        self.assertFalse(self.rx.fresh(10))

    def test_replayed_and_reordered(self):
        packet = self.msg(2)
        ack = self.rx.receive(packet, 10, authenticated_transport=True)
        # Same authenticated bytes may be re-ACKed after a lost ACK; never re-delivered.
        self.assertEqual(self.rx.receive(packet, 11, authenticated_transport=True), ack)
        self.assertIsNone(self.rx.receive(self.msg(1), 12, authenticated_transport=True))
        self.assertEqual(self.rx.last_ms, 10)

    def test_different_session_or_node(self):
        self.assertIsNone(self.rx.receive(self.msg(node_id=8), 2, authenticated_transport=True))
        self.assertIsNone(self.rx.receive(self.msg(session=999), 3, authenticated_transport=True))
        self.assertFalse(self.rx.fresh(3))

    def test_invalid_message_no_refresh(self):
        self.assertIsNone(self.rx.receive(b"hi", 10, authenticated_transport=True))
        self.assertFalse(self.rx.fresh(10))

    def test_timeout_latched_even_after_new_frame(self):
        self.rx.receive(self.msg(), 10, authenticated_transport=True)
        self.assertIsNone(self.rx.receive(self.msg(2), 400, authenticated_transport=True))
        self.assertFalse(self.rx.fresh(401))
        self.assertIsNone(self.rx.receive(self.msg(3), 410, authenticated_transport=True))

    def test_clock_rollback_latches(self):
        self.rx.receive(self.msg(), 10, authenticated_transport=True)
        self.assertIsNone(self.rx.receive(self.msg(2), 9, authenticated_transport=True))
        self.assertTrue(self.rx.latched_fault)

    def test_local_fault_requires_local_recommission(self):
        self.rx.receive(self.msg(), 10, authenticated_transport=True)
        self.rx.fault()
        self.assertIsNone(self.rx.receive(self.msg(2), 12, authenticated_transport=True))
        self.rx.commission_local(124, 20)
        self.assertIsNone(self.rx.receive(self.msg(3, session=123), 21, authenticated_transport=True))
        self.assertIsNotNone(self.rx.receive(self.msg(1, session=124), 22, authenticated_transport=True))

    def test_ack_message_does_not_count_as_data(self):
        self.assertIsNone(self.rx.receive(Frame(ACK, 7, 123, 1, ack_seq=1).encode(), 1,
                                          authenticated_transport=True))
        self.assertFalse(self.rx.fresh(1))


class TestReliableTelemetry(unittest.TestCase):
    def setUp(self):
        self.tx = AckTracker(7, 123)
        self.rx = ModuleReceiver(7)
        self.rx.commission_local(123, 0)

    def test_real_ack_after_application(self):
        p = self.tx.start(55, 10)
        ack = self.rx.receive(p, 10, authenticated_transport=True)
        self.assertTrue(self.tx.accept_ack(ack, 10, authenticated_transport=True))
        self.assertIsNone(self.tx.pending)
        self.assertEqual(self.tx.acked, 1)

    def test_esp_now_send_callback_is_not_ack(self):
        self.tx.start(55, 10)
        self.assertFalse(self.tx.accept_ack(b"SEND_OK", 10, authenticated_transport=True))
        self.assertIsNotNone(self.tx.pending)

    def test_wrong_or_unencrypted_ack(self):
        self.tx.start(55, 10)
        bad = Frame(ACK, 7, 123, 2, ack_seq=2).encode()
        self.assertFalse(self.tx.accept_ack(bad, 10, authenticated_transport=True))
        ok = Frame(ACK, 7, 123, 1, ack_seq=1).encode()
        self.assertFalse(self.tx.accept_ack(ok, 10, authenticated_transport=False))
        self.assertTrue(self.tx.accept_ack(ok, 10, authenticated_transport=True))

    def test_stale_ack_never_completes(self):
        self.tx.start(55, 0)
        valid = Frame(ACK, 7, 123, 1, ack_seq=1).encode()
        self.assertFalse(self.tx.accept_ack(valid, 240, authenticated_transport=True))
        self.assertIsNone(self.tx.pending)
        self.assertEqual(self.tx.failed, 1)

    def test_retries_bounded_expire(self):
        packet = self.tx.start(55, 0)
        self.assertIsNone(self.tx.retry(59))
        self.assertEqual(self.tx.retry(60), packet)
        self.assertEqual(self.tx.retry(120), packet)
        self.assertIsNone(self.tx.retry(180))
        self.assertIsNone(self.tx.retry(240))
        self.assertEqual(self.tx.failed, 1)

    def test_retry_on_backwards_clock_fails(self):
        self.tx.start(55, 10)
        self.assertIsNone(self.tx.retry(9))
        self.assertEqual(self.tx.failed, 1)

    def test_pending_and_sequence_no_wrap(self):
        self.tx.start(1, 0)
        with self.assertRaises(RuntimeError):
            self.tx.start(1, 1)
        self.tx.pending = None
        self.tx.next_seq = MAX_SEQ + 1
        with self.assertRaises(ValueError):
            self.tx.start(1, 1)


class TestPowerScreen(unittest.TestCase):
    def test_nominal_and_offset(self):
        a = screen(5, 0.3, 0.75, 1.0)
        b = screen(5, 0.3, 0.75, 0.5)
        self.assertEqual(a.output_w, 1.5)
        self.assertEqual(a.input_w, 2.0)
        self.assertEqual(a.loss_w, 0.5)
        self.assertEqual(b.input_w, 4.0)
        self.assertEqual(b.loss_w, 2.5)

    def test_energy_conservation_on_grid(self):
        for eta in (0.3, 0.45, 0.6, 0.75):
            for offset in (0.5, 0.75, 1.0):
                r = screen(5, 0.3, eta, offset)
                self.assertAlmostEqual(r.input_w, r.output_w + r.loss_w, places=5)

    def test_ideal_hold_up_only(self):
        self.assertAlmostEqual(hold_up_farads(1.5, 0.15, 5, 3.5),
                               0.03529411764705882)

    def test_invalid_values(self):
        for args in [(5, .3, 0, 1), (5, .3, .5, 0), (5, -1, .5, 1),
                     (5, 2, .5, 1), (0, .3, .5, 1)]:
            with self.assertRaises(ValueError):
                screen(*args)
        with self.assertRaises(ValueError):
            hold_up_farads(1, 1, 3, 4)


if __name__ == "__main__":
    unittest.main()
