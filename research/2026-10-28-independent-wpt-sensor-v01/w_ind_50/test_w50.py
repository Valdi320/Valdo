import json
import unittest
from dataclasses import replace
from decimal import Decimal
from w50_ina219_freshness import PairedGate, RawSample, DataRejected, decode, demo, example_samples

class W50Test(unittest.TestCase):
    def setUp(self):
        self.tx, self.rx = example_samples()
        self.g = PairedGate('demo-w50')

    def reject(self, tx=None, rx=None, now='20', source_kind='synthetic'):
        with self.assertRaises(DataRejected):
            self.g.accept(self.tx if tx is None else tx,
                          self.rx if rx is None else rx, now, source_kind)

    def test_nominal_pass(self): self.assertEqual(self.g.accept(self.tx, self.rx, '20')['link_efficiency_percent_nominal'], '79.872')
    def test_raw_bus_decode(self): self.assertEqual(decode(self.tx)['bus_v'], 5)
    def test_current_80mA(self): self.assertEqual(decode(self.tx)['current_a'], Decimal('0.08'))
    def test_highside_shunt_loss(self): self.assertEqual(decode(self.tx)['shunt_loss_w'], Decimal('0.00064'))
    def test_highside_input_40064(self): self.assertEqual(decode(self.tx)['power_before_shunt_w'], Decimal('0.40064'))
    def test_uncalibrated_power_register_not_needed(self): self.assertEqual(decode(self.tx)['power_bus_w'], Decimal('0.4'))
    def test_no_ready(self): self.reject(tx=replace(self.tx,bus_reg_16=self.tx.bus_reg_16 & ~2))
    def test_overflow(self): self.reject(tx=replace(self.tx,bus_reg_16=self.tx.bus_reg_16 | 1))
    def test_no_post_trigger_low(self): self.reject(rx=replace(self.rx,cnvr_low_after_trigger=False))
    def test_no_power_read(self): self.reject(rx=replace(self.rx,power_reg_read_after=False))
    def test_wrong_mode(self): self.reject(tx=replace(self.tx,single_shot_shunt_bus_mode=False))
    def test_fast_ready(self): self.reject(tx=replace(self.tx,ready_ms='5',read_ms='18'))
    def test_future_ready(self): self.reject(tx=replace(self.tx,ready_ms='25'))
    def test_stale_read(self): self.reject(rx=replace(self.rx,read_ms='30'),now='40')
    def test_stale_collection(self): self.reject(now='31')
    def test_wrong_order(self): self.reject(tx=replace(self.tx,read_ms='16'))
    def test_different_clock(self): self.reject(rx=replace(self.rx,clock_id='independent-esp32-clock'))
    def test_trigger_skew(self): self.reject(rx=replace(self.rx,trigger_ms='10',ready_ms='27.05',read_ms='28'),now='29')
    def test_read_skew(self): self.reject(rx=replace(self.rx,ready_ms='22.05',read_ms='24'),now='25')
    def test_overshoot_efficiency(self): self.reject(rx=replace(self.rx,bus_reg_16=(1500<<3)|2))
    def test_reverse_current(self): self.reject(tx=replace(self.tx,shunt_reg_16=65536-800))
    def test_zero_current(self): self.reject(tx=replace(self.tx,shunt_reg_16=0))
    def test_nan_shunt(self): self.reject(tx=replace(self.tx,shunt_milliohm='NaN'))
    def test_infinite_time(self): self.reject(tx=replace(self.tx,trigger_ms='Infinity'))
    def test_invalid_register(self): self.reject(tx=replace(self.tx,bus_reg_16=65536))
    def test_negative_sequence(self): self.reject(tx=replace(self.tx,sequence=-1))
    def test_invalid_run(self): self.reject(tx=replace(self.tx,run_id='other-run'))
    def test_bench_mode_forbidden(self): self.reject(source_kind='bench')
    def test_no_physical_claim(self):
        result = self.g.accept(self.tx,self.rx,'20')
        self.assertFalse(result['hardware_approved'])
        self.assertFalse(result['lithium_dock_approved'])
        self.assertFalse(result['uncertainty_calibrated'])
    def test_duplicate_after_success(self):
        self.g.accept(self.tx,self.rx,'20'); self.reject()
    def test_gap_sequence(self):
        self.g.accept(self.tx,self.rx,'20')
        self.reject(replace(self.tx,sequence=2,trigger_ms='100',ready_ms='117.05',read_ms='118'),
                    replace(self.rx,sequence=2,trigger_ms='101',ready_ms='118.05',read_ms='119'), '120')
    def test_next_sequence_ok(self):
        self.g.accept(self.tx,self.rx,'20')
        tx=replace(self.tx,sequence=1,trigger_ms='100',ready_ms='117.05',read_ms='118')
        rx=replace(self.rx,sequence=1,trigger_ms='101',ready_ms='118.05',read_ms='119')
        self.assertEqual(self.g.accept(tx,rx,'120')['seq'],1)
    def test_failed_attempt_keeps_seq(self):
        self.reject(tx=replace(self.tx,bus_reg_16=self.tx.bus_reg_16&~2))
        self.assertEqual(self.g.last_sequences,{'TX':-1,'RX':-1})
        self.g.accept(self.tx,self.rx,'20')
        self.assertEqual(self.g.last_sequences,{'TX':0,'RX':0})
    def test_no_cross_run(self): self.reject(tx=replace(self.tx,run_id='other'))
    def test_wrong_role(self): self.reject(tx=replace(self.tx,node='RX'))
    def test_non_integer_shunt_reg(self): self.reject(tx=replace(self.tx,shunt_reg_16='800'))
    def test_boolean_shunt_reg(self): self.reject(tx=replace(self.tx,shunt_reg_16=True))
    def test_low_shunt_not_qualified(self): self.reject(tx=replace(self.tx,shunt_milliohm='1'))
    def test_data_source_no_calibration_gate(self):
        self.assertNotIn('calibration_approved',self.g.accept(self.tx,self.rx,'20'))
    def test_demo_six_failures(self): self.assertEqual(len(demo()['rejections']),6)
    def test_demo_no_bad_accepted(self): self.assertNotIn('BUG_ACCEPTED',demo()['rejections'].values())
    def test_demo_json_deterministic(self):self.assertEqual(json.dumps(demo(),sort_keys=True),json.dumps(demo(),sort_keys=True))

if __name__=='__main__':unittest.main()
