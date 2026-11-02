"""W-IND-60: adversarial OFFLINE application-ACK loss/replay tests.
No hardware, radio, keys, WPT or battery. External authentication is injected.
"""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from w_link import (ACK, DATA, AckTracker, Frame, ModuleReceiver,
                    MAX_DUPLICATE_ACKS, MAX_DUPLICATE_AGE_MS)


class W60ApplicationAck(unittest.TestCase):
    def setUp(self):
        self.rx = ModuleReceiver(7, timeout_ms=250)
        self.rx.commission_local(123, 0)
        self.tx = AckTracker(7, 123)

    def packet(self, seq=1, value=33, session=123, node=7):
        return Frame(DATA, node, session, seq, value_milli=value).encode()

    def receive(self, packet, when, auth=True):
        return self.rx.receive(packet, when, authenticated_transport=auth)

    def test_lost_application_ack_rescued_by_one_retry(self):
        sent = self.tx.start(33, 0)
        lost_ack = self.receive(sent, 1)
        self.assertIsNotNone(lost_ack)
        self.assertFalse(self.tx.accept_ack(b"SEND_OK", 1, authenticated_transport=True))
        retransmit = self.tx.retry(60)
        self.assertEqual(retransmit, sent)
        rescued_ack = self.receive(retransmit, 60)
        self.assertEqual(rescued_ack, lost_ack)
        self.assertTrue(self.tx.accept_ack(rescued_ack, 60, authenticated_transport=True))
        self.assertEqual(self.tx.acked, 1)
        self.assertEqual(self.rx.last_seq, 1)
        self.assertEqual(self.rx.last_ms, 1)
        self.assertFalse(self.rx.latched_fault)

    def test_two_lost_application_acks_recovered_third_attempt(self):
        sent = self.tx.start(10, 0)
        self.assertIsNotNone(self.receive(sent, 1))
        self.assertIsNotNone(self.receive(self.tx.retry(60), 60))
        ack = self.receive(self.tx.retry(120), 120)
        self.assertIsNotNone(ack)
        self.assertTrue(self.tx.accept_ack(ack, 120, authenticated_transport=True))
        self.assertEqual(self.rx.last_ms, 1)
        self.assertEqual(self.rx._duplicate_acks_remaining, 0)

    def test_packet_loss_then_first_delivery_on_retry(self):
        sent = self.tx.start(10, 0)
        # Initial DATA packet is lost, no application callback.
        self.assertEqual(self.tx.retry(60), sent)
        ack = self.receive(sent, 61)
        self.assertTrue(self.tx.accept_ack(ack, 61, authenticated_transport=True))
        self.assertEqual(self.rx.last_ms, 61)

    def test_duplicate_ack_is_byte_identical(self):
        sent = self.packet()
        ack = self.receive(sent, 0)
        self.assertEqual(self.receive(sent, 60), ack)

    def test_duplicate_does_not_extend_freshness_or_watchdog(self):
        sent = self.packet()
        self.receive(sent, 10)
        self.receive(sent, 100)
        self.receive(sent, 200)
        self.assertEqual(self.rx.last_ms, 10)
        self.assertTrue(self.rx.tick(260))
        self.assertFalse(self.rx.tick(261))
        self.assertTrue(self.rx.latched_fault)

    def test_duplicate_does_not_change_sequence(self):
        sent = self.packet(seq=19)
        self.receive(sent, 3)
        self.receive(sent, 60)
        self.assertEqual(self.rx.last_seq, 19)

    def test_two_reack_limit(self):
        sent = self.packet()
        self.receive(sent, 0)
        for _ in range(MAX_DUPLICATE_ACKS):
            self.assertIsNotNone(self.receive(sent, 60))
        self.assertIsNone(self.receive(sent, 60))
        self.assertEqual(self.rx._duplicate_acks_remaining, 0)

    def test_exact_duplicate_time_boundary(self):
        sent = self.packet()
        self.receive(sent, 0)
        self.assertIsNotNone(self.receive(sent, MAX_DUPLICATE_AGE_MS))

    def test_reack_refused_after_window_even_if_fresh(self):
        sent = self.packet()
        self.receive(sent, 0)
        self.assertIsNone(self.receive(sent, MAX_DUPLICATE_AGE_MS + 1))
        self.assertTrue(self.rx.fresh(MAX_DUPLICATE_AGE_MS + 1))
        self.assertEqual(self.rx._duplicate_acks_remaining, MAX_DUPLICATE_ACKS)

    def test_timeout_latches_and_does_not_reack(self):
        sent = self.packet()
        self.receive(sent, 0)
        self.assertIsNone(self.receive(sent, 251))
        self.assertTrue(self.rx.latched_fault)

    def test_same_sequence_modified_payload_is_not_reacked(self):
        sent = self.packet(seq=1, value=33)
        self.receive(sent, 0)
        self.assertIsNone(self.receive(self.packet(seq=1, value=34), 60))
        self.assertEqual(self.rx._duplicate_acks_remaining, MAX_DUPLICATE_ACKS)
        self.assertIsNotNone(self.receive(sent, 61))

    def test_corrupted_crc_cannot_reack(self):
        sent = self.packet()
        self.receive(sent, 0)
        damaged = bytearray(sent)
        damaged[-1] ^= 0x01
        self.assertIsNone(self.receive(bytes(damaged), 60))
        self.assertIsNotNone(self.receive(sent, 61))

    def test_older_sequence_not_reacked(self):
        p1 = self.packet(seq=1)
        p2 = self.packet(seq=2)
        self.receive(p1, 0)
        self.receive(p2, 50)
        self.assertIsNone(self.receive(p1, 60))
        self.assertIsNotNone(self.receive(p2, 61))
        self.assertEqual(self.rx.last_ms, 50)

    def test_session_mismatch_never_reack(self):
        sent = self.packet()
        self.receive(sent, 0)
        self.assertIsNone(self.receive(self.packet(session=999), 60))
        self.assertEqual(self.rx._duplicate_acks_remaining, MAX_DUPLICATE_ACKS)

    def test_node_mismatch_never_reack(self):
        sent = self.packet()
        self.receive(sent, 0)
        self.assertIsNone(self.receive(self.packet(node=8), 60))

    def test_authentication_must_be_explicit_true(self):
        sent = self.packet()
        self.receive(sent, 0)
        for untrusted in (False, None, 1, "yes", True if False else 0):
            with self.subTest(untrusted=untrusted):
                self.assertIsNone(self.receive(sent, 60, untrusted))
        self.assertEqual(self.rx._duplicate_acks_remaining, MAX_DUPLICATE_ACKS)
        self.assertIsNotNone(self.receive(sent, 61, True))

    def test_new_session_invalidates_duplicate_cache(self):
        sent = self.packet()
        self.receive(sent, 0)
        self.rx.commission_local(124, 70)
        self.assertIsNone(self.receive(sent, 80))
        self.assertIsNone(self.rx._last_data_packet)
        self.assertIsNotNone(self.receive(self.packet(session=124), 81))

    def test_fault_latches_and_requires_local_recommission(self):
        sent = self.packet()
        self.receive(sent, 0)
        self.rx.fault()
        self.assertIsNone(self.receive(sent, 60))
        self.rx.commission_local(124, 70)
        self.assertIsNone(self.receive(sent, 80))
        self.assertIsNotNone(self.receive(self.packet(session=124), 81))

    def test_clock_rollback_latches_and_blocks_reack(self):
        sent = self.packet()
        self.receive(sent, 50)
        self.assertIsNone(self.receive(sent, 49))
        self.assertTrue(self.rx.latched_fault)

    def test_boolean_timestamp_is_not_valid_monotonic_time(self):
        sent = self.packet()
        self.assertIsNone(self.receive(sent, True))
        self.assertTrue(self.rx.latched_fault)

    def test_negative_clock_latches_and_blocks_reack(self):
        sent = self.packet()
        self.receive(sent, 2)
        self.assertIsNone(self.receive(sent, -1))
        self.assertTrue(self.rx.latched_fault)

    def test_ack_message_is_never_reaccepted_as_data(self):
        sent = self.packet()
        ack = self.receive(sent, 0)
        self.assertIsNone(self.receive(ack, 60))
        self.assertEqual(self.rx.last_ms, 0)

    def test_ack_tracker_rejects_outdated_ack_even_if_receiver_reacked(self):
        sent = self.tx.start(33, 0)
        self.receive(sent, 0)
        late_ack = self.receive(sent, 240)
        self.assertIsNotNone(late_ack)
        self.assertFalse(self.tx.accept_ack(late_ack, 240, authenticated_transport=True))
        self.assertEqual(self.tx.failed, 1)

    def test_max_attempts_still_enforced_by_transmitter(self):
        sent = self.tx.start(33, 0)
        self.assertEqual(self.tx.retry(60), sent)
        self.assertEqual(self.tx.retry(120), sent)
        self.assertIsNone(self.tx.retry(180))
        self.assertIsNone(self.tx.retry(240))
        self.assertEqual(self.tx.failed, 1)

    def test_new_payload_resets_reack_budget_only_when_new_sequence_accepted(self):
        p1, p2 = self.packet(seq=1), self.packet(seq=2)
        self.receive(p1, 0)
        self.receive(p1, 10)
        self.assertEqual(self.rx._duplicate_acks_remaining, 1)
        self.receive(p2, 30)
        self.assertEqual(self.rx._duplicate_acks_remaining, MAX_DUPLICATE_ACKS)
        self.assertIsNone(self.receive(p1, 40))
        self.assertIsNotNone(self.receive(p2, 41))

    def test_w60_reproducible_artifact_is_explicitly_synthetic(self):
        from w60_ack_demo import demo
        report = demo()
        self.assertTrue(report["lost_ack_recovered"])
        self.assertTrue(report["freshness_unchanged_after_retransmission"])
        self.assertTrue(report["duplicate_ack_limit_enforced"])
        self.assertEqual(report["source_kind"], "SYNTHETIC_ONLY")
        self.assertFalse(report["radio_tested"])
        self.assertFalse(report["hardware_approved"])
        self.assertFalse(report["battery_or_dock_tested"])


if __name__ == "__main__":
    unittest.main()
