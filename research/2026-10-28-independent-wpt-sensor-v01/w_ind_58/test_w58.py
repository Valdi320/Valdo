"""W58 injected raw-byte tests and W57 full-capture integration, CPU only."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "w_ind_57"))
from w57_i2c_capture import CaptureFault, FakeClock, FakePort, capture_pair
from w58_ina219_wire import INA219WirePort, SyntheticRawBus, WireFault, synthetic_demo


class WireContractTests(unittest.TestCase):
    def setUp(self):
        self.clock = FakeClock()
        self.raw = SyntheticRawBus(FakePort(self.clock))
        self.port = INA219WirePort(self.raw)

    def test_complete_two_channel_w57_capture(self):
        sample = capture_pair(self.port, self.clock)
        self.assertEqual((sample["tx"]["bus_mv"], sample["rx"]["bus_mv"]), (5000, 4000))
        self.assertEqual((sample["tx"]["shunt_uv"], sample["rx"]["shunt_uv"]), (8000, 8000))
        self.assertFalse(sample["hardware_approved"])
        self.assertGreater(self.port.transactions, 10)

    def test_exact_big_endian_configuration_write(self):
        self.port.write16(0x40, 0, 0x0663)
        self.assertEqual(self.raw.write_log, [(0x40, "000663")])

    def test_read_wire_bytes_decode_big_endian(self):
        class FixedRaw:
            def write_read(self, address, command, count):
                assert (address, command, count) == (0x40, b"\x02", 2)
                return b"\x27\x12"
        self.assertEqual(INA219WirePort(FixedRaw()).read16(0x40, 2), 0x2712)

    def test_swapped_config_bytes_rejected_by_w57(self):
        with self.assertRaises(CaptureFault):
            capture_pair(INA219WirePort(SyntheticRawBus(FakePort(self.clock), reverse_read_bytes=True)), self.clock)

    def test_missing_or_extra_bytes_rejected(self):
        for bad in (b"", b"\x01", b"\x01\x02\x03", None, [1, 2], bytearray(b"\x01\x02")):
            class BadRaw:
                def write_read(self, *args): return bad
            with self.subTest(bad=bad), self.assertRaises(WireFault):
                INA219WirePort(BadRaw()).read16(0x40, 1)

    def test_invalid_addresses_fail_closed(self):
        for bad in (0x3F, 0x50, True, 64.0, "0x40", None):
            with self.subTest(bad=bad), self.assertRaises(WireFault):
                self.port.read16(bad, 1)

    def test_invalid_registers_fail_closed(self):
        for bad in (4, True, "1", -1):
            with self.subTest(bad=bad), self.assertRaises(WireFault):
                self.port.read16(0x40, bad)

    def test_write_only_configuration(self):
        with self.assertRaises(WireFault): self.port.write16(0x40, 1, 3)

    def test_invalid_write_word(self):
        for bad in (True, None, -1, 65536, 4.0):
            with self.subTest(bad=bad), self.assertRaises(WireFault):
                self.port.write16(0x40, 0, bad)

    def test_transport_read_failure(self):
        class Crash:
            def write_read(self, *args): raise OSError("no adapter")
        with self.assertRaises(WireFault): INA219WirePort(Crash()).read16(0x40, 2)

    def test_transport_write_failure(self):
        class Crash:
            def write(self, *args): raise OSError("NACK")
        with self.assertRaises(WireFault): INA219WirePort(Crash()).write16(0x40, 0, 0x0663)

    def test_write_receipt_contract(self):
        class Impostor:
            def write(self, *args): return 1
        with self.assertRaises(WireFault): INA219WirePort(Impostor()).write16(0x40, 0, 0x0663)

    def test_big_endian_byte_order_and_no_physical_claims(self):
        d = synthetic_demo()
        self.assertEqual(d["first_config_write_hex"], "000663")
        self.assertEqual(d["second_config_write_hex"], "000663")
        self.assertEqual(d["physical_measurements"], 0)
        for field in ("hardware_approved", "energization_approved", "lithium_dock_approved",
                      "physical_i2c_implemented", "meter_identity_proven", "calibration_proven",
                      "thermal_fod_emi_proven"):
            self.assertFalse(d[field], field)

    def test_failures_do_not_count_successful_transactions(self):
        class Short:
            def write_read(self, *args): return b"\x01"
        port = INA219WirePort(Short())
        with self.assertRaises(WireFault): port.read16(0x40, 2)
        self.assertEqual(port.transactions, 0)


if __name__ == "__main__":
    unittest.main()
