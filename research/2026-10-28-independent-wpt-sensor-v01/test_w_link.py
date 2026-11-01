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



class TestClockBoundary(unittest.TestCase):
    """W95: malformed timestamps never retransmit, ACK, or certify freshness."""

    def test_start_rejects_noninteger_time_without_sequence_consumption(self):
        for t in (True, False, 0.0, 10.0, float("nan"), float("inf"),
                  float("-inf"), "100", None, object()):
            with self.subTest(clock=repr(t)):
                tx = AckTracker(7, 123)
                with self.assertRaises(ValueError):
                    tx.start(55, t)
                self.assertEqual(tx.next_seq, 1)
                self.assertIsNone(tx.pending)
                self.assertEqual(tx.failed, 0)

    def test_retry_invalid_time_fails_closed_without_emitting_packet(self):
        for t in (True, False, 0.0, 60.0, float("nan"), float("inf"),
                  float("-inf"), "60", None, object()):
            with self.subTest(clock=repr(t)):
                tx = AckTracker(7, 123)
                tx.start(55, 0)
                self.assertIsNone(tx.retry(t))
                self.assertIsNone(tx.pending)
                self.assertEqual(tx.failed, 1)
                self.assertEqual(tx.acked, 0)

    def test_rejected_nan_retry_cannot_later_be_acknowledged(self):
        tx = AckTracker(7, 123)
        tx.start(55, 0)
        ack = Frame(ACK, 7, 123, 1, ack_seq=1).encode()
        self.assertIsNone(tx.retry(float("nan")))
        self.assertFalse(tx.accept_ack(ack, 60, authenticated_transport=True))
        self.assertEqual((tx.failed, tx.acked), (1, 0))

    def test_ack_boolean_timestamp_cannot_confirm_pending_message(self):
        for t in (True, False):
            with self.subTest(clock=t):
                tx = AckTracker(7, 123)
                tx.start(55, 0)
                ack = Frame(ACK, 7, 123, 1, ack_seq=1).encode()
                self.assertFalse(tx.accept_ack(ack, t, authenticated_transport=True))
                self.assertEqual((tx.failed, tx.acked), (1, 0))
                self.assertIsNone(tx.pending)

    def test_ack_nonfinite_or_nonnumeric_timestamp_never_confirms(self):
        for t in (float("nan"), float("inf"), None, "60", object()):
            with self.subTest(clock=repr(t)):
                tx = AckTracker(7, 123)
                tx.start(55, 0)
                ack = Frame(ACK, 7, 123, 1, ack_seq=1).encode()
                self.assertFalse(tx.accept_ack(ack, t, authenticated_transport=True))
                self.assertEqual((tx.failed, tx.acked), (1, 0))
                self.assertIsNone(tx.pending)

    def test_commission_bad_time_rejected_before_receiver_mutation(self):
        for t in (True, False, 0.0, float("nan"), float("inf"), None, "0"):
            with self.subTest(clock=repr(t)):
                rx = ModuleReceiver(7)
                with self.assertRaises(ValueError):
                    rx.commission_local(123, t)
                self.assertIsNone(rx.session)
                self.assertTrue(rx.latched_fault)

    def test_receiver_freshness_rejects_boolean_timestamp(self):
        rx = ModuleReceiver(7)
        rx.commission_local(123, 0)
        packet = Frame(DATA, 7, 123, 1, value_milli=55).encode()
        self.assertIsNotNone(rx.receive(packet, 0, authenticated_transport=True))
        self.assertFalse(rx.fresh(True))
        self.assertFalse(rx.fresh(False))
        self.assertTrue(rx.fresh(1))
        self.assertEqual(rx.last_ms, 0)

    def test_valid_integer_clock_keeps_lost_ack_recovery(self):
        tx = AckTracker(7, 123)
        rx = ModuleReceiver(7)
        rx.commission_local(123, 0)
        packet = tx.start(55, 0)
        original = rx.receive(packet, 1, authenticated_transport=True)
        resent = tx.retry(60)
        self.assertEqual(resent, packet)
        recovered = rx.receive(resent, 60, authenticated_transport=True)
        self.assertEqual(original, recovered)
        self.assertTrue(tx.accept_ack(recovered, 60, authenticated_transport=True))
        self.assertEqual((tx.failed, tx.acked), (0, 1))
        self.assertEqual(rx.last_ms, 1)

    def test_sender_restarts_new_sequence_after_rejected_bad_time(self):
        tx = AckTracker(7, 123)
        tx.start(55, 0)
        self.assertIsNone(tx.retry(float("nan")))
        packet = tx.start(56, 100)
        self.assertEqual(Frame.decode(packet).seq, 2)
        ack = Frame(ACK, 7, 123, 2, ack_seq=2).encode()
        self.assertTrue(tx.accept_ack(ack, 101, authenticated_transport=True))
        self.assertEqual((tx.failed, tx.acked), (1, 1))


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



class TestW96StrictProtocolNumbers(unittest.TestCase):
    """W96: no boolean/float identities or non-finite watchdog policy."""

    def test_frame_boolean_message_kind_rejected(self):
        with self.assertRaises(ValueError):
            Frame(True, 7, 123, 1, value_milli=55).encode()

    def test_frame_boolean_node_session_and_sequence_rejected(self):
        frames = (Frame(DATA, True, 123, 1),
                  Frame(DATA, 7, True, 1),
                  Frame(DATA, 7, 123, True))
        for frame in frames:
            with self.subTest(frame=repr(frame)):
                with self.assertRaises(ValueError):
                    frame.encode()

    def test_frame_ack_sequence_and_value_bool_rejected(self):
        for frame in (Frame(ACK, 7, 123, 1, ack_seq=True),
                      Frame(DATA, 7, 123, 1, value_milli=True)):
            with self.subTest(frame=repr(frame)):
                with self.assertRaises(ValueError):
                    frame.encode()

    def test_frame_node_fraction_is_rejected_without_packing_exception(self):
        for node in (7.0, float("nan"), float("inf"), "7", None):
            with self.subTest(node=repr(node)):
                with self.assertRaises(ValueError):
                    Frame(DATA, node, 123, 1).encode()

    def test_receiver_refuses_noninteger_ids_and_watchdog(self):
        for node, timeout in ((True, 250), (7.0, 250), (7, True),
                              (7, False), (7, 250.0), (7, float("inf")),
                              (7, float("nan")), (7, "250"), (7, None)):
            with self.subTest(node=repr(node), timeout=repr(timeout)):
                with self.assertRaises(ValueError):
                    ModuleReceiver(node, timeout)

    def test_receiver_commission_bool_session_does_not_mutate(self):
        rx = ModuleReceiver(7)
        with self.assertRaises(ValueError):
            rx.commission_local(True, 0)
        self.assertIsNone(rx.session)
        self.assertTrue(rx.latched_fault)
        self.assertIsNone(rx.last_ms)

    def test_sender_refuses_boolean_and_float_peer_identifiers(self):
        for node, session in ((True, 123), (7, True), (7.0, 123),
                              (7, 123.0), (7, float("nan"))):
            with self.subTest(node=repr(node), session=repr(session)):
                with self.assertRaises(ValueError):
                    AckTracker(node, session)

    def test_sender_refuses_noninteger_retry_expiry_and_attempts(self):
        for kwargs in ({"retry_ms": True}, {"retry_ms": 60.0},
                       {"expiry_ms": True}, {"expiry_ms": 240.0},
                       {"max_attempts": True}, {"max_attempts": 3.0},
                       {"max_attempts": float("nan")},
                       {"max_attempts": float("inf")}):
            with self.subTest(policy=repr(kwargs)):
                with self.assertRaises(ValueError):
                    AckTracker(7, 123, **kwargs)

    def test_invalid_value_does_not_consume_sender_sequence(self):
        tx = AckTracker(7, 123)
        with self.assertRaises(ValueError):
            tx.start(True, 0)
        self.assertEqual(tx.next_seq, 1)
        self.assertIsNone(tx.pending)

    def test_valid_integer_wire_and_lost_ack_recovery_unchanged(self):
        tx = AckTracker(7, 123)
        rx = ModuleReceiver(7, timeout_ms=250)
        rx.commission_local(123, 0)
        data = tx.start(55, 0)
        self.assertEqual(Frame.decode(data), Frame(DATA, 7, 123, 1, value_milli=55))
        first = rx.receive(data, 1, authenticated_transport=True)
        self.assertEqual(tx.retry(60), data)
        second = rx.receive(data, 60, authenticated_transport=True)
        self.assertEqual(first, second)
        self.assertTrue(tx.accept_ack(second, 60, authenticated_transport=True))
        self.assertEqual(rx.last_ms, 1)
        self.assertEqual((tx.acked, tx.failed), (1, 0))


# W-IND-97: local epoch/clock rollback cannot reopen stale telemetry.
def w97_packet(session, seq=1, value=400):
    return Frame(DATA, 7, session, seq, value_milli=value).encode()

class TestW97RecommissionBoundary(unittest.TestCase):
    def new_receiver(self):
        rx = ModuleReceiver(7)
        rx.commission_local(123, 0)
        return rx

    def test_same_epoch_rejected_before_first_data(self):
        rx = self.new_receiver()
        with self.assertRaises(ValueError):
            rx.commission_local(123, 1)
        self.assertEqual(rx.session, 123)
        self.assertEqual(rx.last_clock_ms, 0)
        self.assertFalse(rx.latched_fault)

    def test_same_epoch_cannot_clear_fault_and_reaccept_old_data(self):
        rx = self.new_receiver()
        self.assertIsNotNone(rx.receive(w97_packet(123), 10, authenticated_transport=True))
        rx.fault()
        with self.assertRaises(ValueError):
            rx.commission_local(123, 20)
        self.assertTrue(rx.latched_fault)
        self.assertEqual((rx.session, rx.last_seq, rx.last_ms), (123, 1, 10))
        self.assertIsNone(rx.receive(w97_packet(123), 21, authenticated_transport=True))

    def test_older_epoch_cannot_roll_back_or_replay(self):
        rx = self.new_receiver()
        rx.commission_local(124, 10)
        rx.fault()
        with self.assertRaises(ValueError):
            rx.commission_local(123, 11)
        self.assertEqual(rx.session, 124)
        self.assertTrue(rx.latched_fault)
        self.assertIsNone(rx.receive(w97_packet(123), 12, authenticated_transport=True))

    def test_clock_rollback_recommission_rejected_without_mutation(self):
        rx = self.new_receiver()
        rx.tick(30)
        rx.fault()
        with self.assertRaises(ValueError):
            rx.commission_local(124, 29)
        self.assertEqual(rx.session, 123)
        self.assertEqual(rx.last_clock_ms, 30)
        self.assertTrue(rx.latched_fault)

    def test_clock_rollback_cannot_reopen_telemetry_lease(self):
        rx = self.new_receiver()
        rx.receive(w97_packet(123), 10, authenticated_transport=True)
        rx.tick(200)
        rx.fault()
        with self.assertRaises(ValueError):
            rx.commission_local(124, 50)
        self.assertFalse(rx.fresh(50))
        self.assertEqual(rx.last_ms, 10)
        self.assertEqual(rx.last_clock_ms, 200)

    def test_forward_epoch_and_time_still_recover_locally(self):
        rx = self.new_receiver()
        rx.receive(w97_packet(123), 10, authenticated_transport=True)
        rx.fault()
        rx.commission_local(124, 20)
        self.assertFalse(rx.latched_fault)
        self.assertIsNone(rx.receive(w97_packet(123), 21, authenticated_transport=True))
        self.assertIsNotNone(rx.receive(w97_packet(124), 22, authenticated_transport=True))
        self.assertTrue(rx.fresh(22))

    def test_equal_time_allows_new_epoch_not_old_one(self):
        rx = self.new_receiver()
        rx.tick(20)
        rx.fault()
        rx.commission_local(124, 20)
        self.assertEqual((rx.session, rx.last_clock_ms), (124, 20))
        with self.assertRaises(ValueError):
            rx.commission_local(124, 20)

    def test_max_epoch_exhaustion_fails_closed(self):
        rx = ModuleReceiver(7)
        rx.commission_local(MAX_SEQ, 0)
        rx.fault()
        with self.assertRaises(ValueError):
            rx.commission_local(MAX_SEQ, 1)
        with self.assertRaises(ValueError):
            rx.commission_local(MAX_SEQ + 1, 1)
        self.assertTrue(rx.latched_fault)

    def test_invalid_recommission_preserves_ack_budget_and_clock(self):
        rx = self.new_receiver()
        data = w97_packet(123)
        self.assertIsNotNone(rx.receive(data, 10, authenticated_transport=True))
        budget = rx._duplicate_acks_remaining
        with self.assertRaises(ValueError):
            rx.commission_local(123, 11)
        self.assertEqual(rx._duplicate_acks_remaining, budget)
        self.assertEqual(rx.last_ms, 10)
        self.assertEqual(rx.last_clock_ms, 10)

    def test_new_object_still_needs_durable_journal(self):
        # Counterexample by design: a new object has no trusted persistent epoch.
        first = self.new_receiver()
        restarted = ModuleReceiver(7)
        restarted.commission_local(123, 0)
        self.assertEqual(first.session, restarted.session)
        # Not a protection result: use durable_epoch_store with PowerFencedTelemetry.



if __name__ == "__main__":
    unittest.main()
