"""W-IND-03 deterministic tests; all power/FOD/temperature signals simulated."""
import unittest
from w_link import Frame, DATA
from power_restart_gate import PowerFencedTelemetry, GatePolicy, VolatileEpochStore

class GateTests(unittest.TestCase):
    def setUp(self):
        self.journal=VolatileEpochStore()
        self.g=PowerFencedTelemetry(7,self.journal)

    def sample(self,t,good=True,temp=True,fod=True,gate=None):
        (gate or self.g).observe(t,power_good=good,temperature_ok=temp,fod_clear=fod)

    def stable(self,gate=None,start=0):
        for t in range(start,start+101,10):self.sample(t,gate=gate)

    def arm(self,session=100,gate=None,t=100):
        return (gate or self.g).commission(session,t,locally_authorized=True)

    def pkt(self,session=100,seq=1):
        return Frame(DATA,7,session,seq,value_milli=400).encode()

    def test_boot_is_locked(self):
        self.assertFalse(self.g.armed)
        self.assertFalse(self.g.fresh(0))
        self.assertIsNone(self.g.receive(self.pkt(),0,authenticated_transport=True))

    def test_cross_node_epoch_independence(self):
        self.stable();self.arm(101)
        node8=PowerFencedTelemetry(8,self.journal)
        self.stable(node8)
        self.assertTrue(node8.commission(99,100,locally_authorized=True))
        self.assertEqual(self.journal.last,{7:101,8:99})

    def test_foreign_object_alarm(self):
        self.stable();self.arm();self.sample(110,fod=False)
        self.assertFalse(self.g.armed)
        self.assertEqual(self.g.fault_reason,'thermal_or_fod')

    def test_invalid_clock_never_raises(self):
        self.stable();self.arm()
        self.assertFalse(self.g.fresh(-1));self.assertFalse(self.g.armed)

    def test_journal_never_decreases(self):
        self.stable();self.arm(101)
        self.assertEqual(self.journal.last[7],101)
        self.assertFalse(self.arm(100))
        self.assertEqual(self.journal.last[7],101)

    def test_journal_power_loss_not_persisted_warning_by_contract(self):
        fresh=PowerFencedTelemetry(7,VolatileEpochStore())
        self.stable(fresh)
        self.assertTrue(fresh.commission(100,100,locally_authorized=True))
        # Deliberately demonstrate UNSAFE volatile storage after real reboot.
        another=PowerFencedTelemetry(7,VolatileEpochStore())
        self.stable(another)
        self.assertTrue(another.commission(100,100,locally_authorized=True))

    def test_large_session_never_allowed(self):
        self.stable()
        self.assertFalse(self.arm(2**32))

    def test_missed_power_samples_reset_settle(self):
        self.sample(0);self.sample(30)
        self.assertFalse(self.arm(t=30))
        for t in range(40,131,10):self.sample(t)
        self.assertTrue(self.arm(t=130))

    def test_monitor_staleness_faults(self):
        self.stable();self.arm()
        self.assertFalse(self.g.fresh(121))
        self.assertEqual(self.g.fault_reason,'stale_power_monitor')

    def test_no_rf_authentication_no_ack(self):
        self.stable();self.arm()
        self.assertIsNone(self.g.receive(self.pkt(),100,authenticated_transport=False))
        self.assertFalse(self.g.fresh(100))

    def test_packet_from_old_epoch_rejected_after_new_commission(self):
        self.stable();self.arm();self.sample(110,good=False);self.stable(start=120)
        self.assertTrue(self.arm(session=101,t=220))
        self.assertIsNone(self.g.receive(self.pkt(100),220,authenticated_transport=True))
        self.assertIsNotNone(self.g.receive(self.pkt(101),220,authenticated_transport=True))

    def test_policy_rejects_invalid(self):
        for p in (dict(settle_ms=0),dict(sample_max_gap_ms=-1),dict(telemetry_timeout_ms=True)):
            with self.assertRaises(ValueError):GatePolicy(**p)

    def test_power_loss_immediately_masks_telemetry(self):
        self.stable();self.arm()
        self.g.receive(self.pkt(),100,authenticated_transport=True)
        self.sample(110,good=False)
        self.assertFalse(self.g.fresh(110));self.assertFalse(self.g.armed)
        self.assertEqual(self.g.fault_reason,'power_loss')

    def test_power_return_does_not_rearm(self):
        self.stable();self.arm();self.sample(110,good=False)
        self.stable(start=120)
        self.assertFalse(self.g.armed)
        self.assertIsNone(self.g.receive(self.pkt(),220,authenticated_transport=True))
        self.assertTrue(self.arm(session=101,t=220))

    def test_radio_timeout_requires_new_commission(self):
        self.stable();self.arm()
        self.g.receive(self.pkt(),100,authenticated_transport=True)
        for t in range(110,361,10):self.sample(t)
        self.assertFalse(self.g.fresh(360))
        self.assertFalse(self.g.armed)
        self.assertTrue(self.g.commission(101,360,locally_authorized=True))

    def test_requires_local_physical_pretend_authorization(self):
        self.stable()
        self.assertFalse(self.g.commission(100,100,locally_authorized=False))
        self.assertFalse(self.g.commission(100,100,locally_authorized='yes'))
        self.assertTrue(self.arm())

    def test_reusing_session_after_power_cycle_denied(self):
        self.stable();self.arm();self.sample(110,good=False);self.stable(start=120)
        self.assertFalse(self.arm(session=100,t=220))
        self.assertEqual(self.g.fault_reason,'reused_epoch')

    def test_same_volatile_journal_across_object_restart(self):
        self.stable();self.arm()
        b=PowerFencedTelemetry(7,self.journal)
        self.stable(b,start=200)
        self.assertFalse(b.commission(100,300,locally_authorized=True))
        self.assertTrue(b.commission(101,300,locally_authorized=True))
        self.assertIsNone(b.receive(self.pkt(100),300,authenticated_transport=True))

    def test_seq_duplicate_on_same_epoch(self):
        self.stable();self.arm()
        self.assertIsNotNone(self.g.receive(self.pkt(seq=1),100,authenticated_transport=True))
        self.assertIsNone(self.g.receive(self.pkt(seq=1),100,authenticated_transport=True))

    def test_settle_ms_not_optional(self):
        self.sample(0);self.assertFalse(self.arm(t=0))
        for t in range(10,100,10):self.sample(t)
        self.assertFalse(self.arm(t=90))
        self.sample(100);self.assertTrue(self.arm())

    def test_thermal_alarm(self):
        self.stable();self.arm();self.sample(110,temp=False)
        self.assertFalse(self.g.armed)
        self.stable(start=120)
        self.assertIsNone(self.g.receive(self.pkt(),220,authenticated_transport=True))
        self.assertTrue(self.arm(101,t=220))

    def test_time_rollback_latches(self):
        self.stable();self.arm();self.g.fresh(99)
        self.assertEqual(self.g.fault_reason,'invalid_or_reversed_time')
        self.assertFalse(self.g.armed)

    def test_time_rollback_requires_new_power_settle(self):
        self.stable();self.arm()
        self.assertFalse(self.g.fresh(99))
        self.assertFalse(self.g.commission(101,100,locally_authorized=True))
        self.stable(start=200)
        self.assertTrue(self.g.commission(101,300,locally_authorized=True))

    def test_unauthorized_source_cannot_switch_power(self):
        self.assertFalse(hasattr(self.g,'power_cutoff'))
        self.assertFalse(hasattr(self.g,'set_power'))

    def test_unknown_signal_faults(self):
        self.stable();self.arm()
        self.g.observe(110,power_good=True,temperature_ok=None,fod_clear=True)
        self.assertFalse(self.g.armed)
        self.assertEqual(self.g.fault_reason,'unknown_health_signal')

    def test_valid_message_and_fresh(self):
        self.stable();self.assertTrue(self.arm())
        self.assertIsNotNone(self.g.receive(self.pkt(),100,authenticated_transport=True))
        self.assertTrue(self.g.fresh(100))

    def test_write_failure_blocks_commission(self):
        self.stable();self.journal.fail_writes=True
        self.assertFalse(self.arm());self.assertFalse(self.g.armed)
        self.assertEqual(self.g.fault_reason,'journal_commit_failed')

    def test_zero_session_never_allowed(self):
        self.stable();self.assertFalse(self.arm(0))

if __name__=='__main__':unittest.main()
