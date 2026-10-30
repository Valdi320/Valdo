"""Synthetic fault injection for a two-INA219 triggered capture; NO I2C device."""
import unittest
from w57_i2c_capture import (capture_pair, FakeClock, FakePort, CaptureFault,
                             CFG_16AVG_TRIGGER, CONVERSION_NS, demo)

class CaptureTests(unittest.TestCase):
    def setUp(self):
        self.clock=FakeClock()
    def run_fault(self, flag):
        with self.assertRaises(CaptureFault): capture_pair(FakePort(self.clock, {flag}),self.clock)
    def test_synthetic_two_channel_capture(self):
        result=demo()
        self.assertEqual(result["config_word_hex"],"0x663")
        self.assertEqual(result["tx"]["bus_mv"],5000)
        self.assertEqual(result["rx"]["bus_mv"],4000)
        self.assertEqual(result["tx"]["shunt_uv"],8000)
        self.assertEqual(result["rx"]["current_ma_tenths_assuming_100mohm"],800)
        self.assertTrue(result["conversion_windows_overlap"])
        self.assertEqual(result["trigger_skew_ns"],0)
        self.assertGreaterEqual(result["tx"]["ready_ns"],CONVERSION_NS)
        for field in ("hardware_approved","energization_approved","lithium_dock_approved",
                      "efficiency_qualified","meter_shunt_calibrated","physical_clock_proven"):
            self.assertFalse(result[field],field)
        self.assertEqual(result["physical_measurements"],0)
    def test_cnvr_stale_rejected(self): self.run_fault("stale_cnvr")
    def test_overflow_rejected(self): self.run_fault("overflow")
    def test_no_ready_rejected(self): self.run_fault("no_ready")
    def test_reset_detected(self): self.run_fault("reset")
    def test_i2c_error_rejected(self): self.run_fault("i2c_fault")
    def test_short_register_rejected(self): self.run_fault("short_read")
    def test_cnvr_did_not_clear_rejected(self): self.run_fault("stuck_cnvr")
    def test_voltage_limit_rejected(self): self.run_fault("high_bus")
    def test_reverse_current_rejected(self): self.run_fault("reverse_current")
    def test_overcurrent_rejected(self): self.run_fault("overcurrent")
    def test_address_same_rejected(self):
        with self.assertRaises(CaptureFault): capture_pair(FakePort(self.clock),self.clock,0x40,0x40)
    def test_bad_addresses_and_types_rejected(self):
        for a in (True,0x30,0x50,"0x40",None):
            with self.subTest(a=a),self.assertRaises(CaptureFault):
                capture_pair(FakePort(self.clock),self.clock,a,0x41)
    def test_trigger_skew_rejected(self):
        class SlowPort(FakePort):
            def write16(self,address,reg,value):
                super().write16(address,reg,value)
                self.clock.sleep_ns(3_000_000)
        with self.assertRaises(CaptureFault): capture_pair(SlowPort(self.clock),self.clock)
    def test_backwards_clock_rejected(self):
        class EvilClock(FakeClock):
            def sleep_ns(self, delay): self.now -= delay
        c=EvilClock()
        with self.assertRaises(CaptureFault): capture_pair(FakePort(c),c)
    def test_stuck_clock_finite(self):
        class FrozenClock(FakeClock):
            def sleep_ns(self,delay): pass
        c=FrozenClock()
        with self.assertRaises(CaptureFault): capture_pair(FakePort(c),c)
    def test_serial_2_byte_register_required(self):
        self.assertEqual(CFG_16AVG_TRIGGER,0x663)
    def test_no_untrusted_efficiency_claim(self):
        r=demo()
        self.assertNotIn("eta_percent",r)
        self.assertEqual(r["source_kind"],"SYNTHETIC_OR_UNTRUSTED_ADAPTER")
    def test_malformed_word_rejected(self):
        class BadPort(FakePort):
            def read16(self,a,r):
                if r==2: return 70000
                return super().read16(a,r)
        with self.assertRaises(CaptureFault): capture_pair(BadPort(self.clock),self.clock)

if __name__ == "__main__": unittest.main()
