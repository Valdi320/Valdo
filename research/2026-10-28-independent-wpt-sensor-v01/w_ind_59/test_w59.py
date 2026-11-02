"""W59 deterministic offline tests: no physical I2C, radio or power."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from w59_mapping_gate import MappingFault, capture_to_record, check_mapping, synthetic_demo, synthetic_records


class MappingGateTests(unittest.TestCase):
    def setUp(self):
        self.r = synthetic_records()

    def rejects(self, modified):
        self.assertFalse(check_mapping(modified)["pattern_pass"])

    def test_valid_is_only_pattern_not_hardware(self):
        r = check_mapping(self.r)
        self.assertTrue(r["pattern_pass"])
        self.assertEqual(r["determinant"], 1)
        self.assertEqual(r["screening_result"], "PASS_PATTERN_ONLY")
        for key in ("meter_identity_proven", "independent_reference_proven", "calibration_proven",
                    "hardware_approved", "energization_approved", "lithium_dock_approved",
                    "efficiency_qualified", "thermal_fod_emi_and_independent_cutoff_proven"):
            self.assertFalse(r[key], key)
        self.assertEqual(r["physical_measurements_performed_by_this_software"], 0)

    def test_both_logical_addresses_alias_same_tx_sensor(self):
        for p in self.r:
            p["observed_mv"]["rx"] = p["observed_mv"]["tx"]
        self.rejects(self.r)

    def test_both_logical_addresses_alias_same_rx_sensor(self):
        for p in self.r:
            p["observed_mv"]["tx"] = p["observed_mv"]["rx"]
        self.rejects(self.r)

    def test_swapped_meters(self):
        for p in self.r:
            p["observed_mv"]["tx"], p["observed_mv"]["rx"] = p["observed_mv"]["rx"], p["observed_mv"]["tx"]
        v = check_mapping(self.r)
        self.assertFalse(v["pattern_pass"])
        self.assertLess(v["determinant"], 0)

    def test_tx_frozen(self):
        self.r[1]["observed_mv"]["tx"] = 2000
        self.rejects(self.r)

    def test_rx_frozen(self):
        self.r[2]["observed_mv"]["rx"] = 2000
        self.rejects(self.r)

    def test_cross_coupling_only(self):
        self.r[1]["observed_mv"]["rx"] += 200
        self.rejects(self.r)

    def test_bias_without_mapping_error(self):
        for p in self.r:
            p["observed_mv"]["tx"] += 100
        v = check_mapping(self.r)
        self.assertTrue(v["gate_diagnostics"]["gain"])
        self.assertFalse(v["gate_diagnostics"]["absolute_reference_error"])
        self.assertFalse(v["pattern_pass"])

    def test_small_independent_error_tolerated(self):
        self.r[1]["observed_mv"]["tx"] -= 30
        self.r[2]["observed_mv"]["rx"] += 25
        self.assertTrue(check_mapping(self.r)["pattern_pass"])

    def test_reference_tx_step_required(self):
        self.r[1]["reference_mv"]["tx"] = 2500
        with self.assertRaises(MappingFault): check_mapping(self.r)

    def test_reference_rx_step_required(self):
        self.r[2]["reference_mv"]["rx"] = 2500
        with self.assertRaises(MappingFault): check_mapping(self.r)

    def test_reference_not_independent_tx(self):
        self.r[1]["reference_mv"]["rx"] += 100
        with self.assertRaises(MappingFault): check_mapping(self.r)

    def test_reference_not_independent_rx(self):
        self.r[2]["reference_mv"]["tx"] += 100
        with self.assertRaises(MappingFault): check_mapping(self.r)

    def test_timestamps_equal(self):
        self.r[1]["timestamp_ms"] = 100
        with self.assertRaises(MappingFault): check_mapping(self.r)

    def test_timestamps_reversed(self):
        self.r[2]["timestamp_ms"] = 50
        with self.assertRaises(MappingFault): check_mapping(self.r)

    def test_timestamps_far_apart(self):
        self.r[2]["timestamp_ms"] = 30101
        with self.assertRaises(MappingFault): check_mapping(self.r)

    def test_wrong_phase_order(self):
        self.r[1], self.r[2] = self.r[2], self.r[1]
        with self.assertRaises(MappingFault): check_mapping(self.r)

    def test_wrong_address_role(self):
        self.r[1]["addresses"] = {"tx": 0x41, "rx": 0x40}
        with self.assertRaises(MappingFault): check_mapping(self.r)

    def test_reject_bools_floats_negative_overlimit(self):
        for bad in (True, 2000.0, -1, 6001, None, "2000", float("nan")):
            a = copy.deepcopy(self.r)
            a[0]["observed_mv"]["tx"] = bad
            with self.subTest(bad=bad), self.assertRaises(MappingFault): check_mapping(a)

    def test_malformed_untrusted_trace(self):
        for bad in (None, {}, [1, 2], [self.r[0], self.r[1]], tuple(self.r)):
            with self.subTest(bad=str(bad)[:30]), self.assertRaises(MappingFault): check_mapping(bad)

    def test_no_extra_fields_or_missing_channel(self):
        self.r[0]["arbitrary_hardware_ok"] = True
        with self.assertRaises(MappingFault): check_mapping(self.r)
        self.r[0].pop("arbitrary_hardware_ok")
        self.r[0]["reference_mv"].pop("rx")
        with self.assertRaises(MappingFault): check_mapping(self.r)

    def test_w57_w58_full_synthetic_capture_pipeline(self):
        """Checks real code boundary over three fake, distinct challenges."""
        root = Path(__file__).resolve().parent
        sys.path.insert(0, str(root.parent / "w_ind_57"))
        sys.path.insert(0, str(root.parent / "w_ind_58"))
        from w57_i2c_capture import FakeClock, FakePort, capture_pair
        from w58_ina219_wire import INA219WirePort, SyntheticRawBus

        records = []
        for fixture in synthetic_records():
            clock = FakeClock()
            fake = FakePort(clock)
            fake.words = {address: (fixture["observed_mv"][ch] // 4 << 3, 800)
                          for ch, address in (("tx", 0x40), ("rx", 0x41))}
            capture = capture_pair(INA219WirePort(SyntheticRawBus(fake)), clock)
            record = capture_to_record(capture, fixture["phase"],
                                       fixture["timestamp_ms"], fixture["reference_mv"])
            records.append(record)
        self.assertTrue(check_mapping(records)["pattern_pass"])
        self.assertFalse(check_mapping(records)["hardware_approved"])

    def test_capture_rejects_hardware_claims_and_swapped_role(self):
        d = {"milestone": "W-IND-57", "addresses": ["0x40", "0x41"],
             "hardware_approved": False, "physical_measurements": 0,
             "tx": {"address_hex": "0x40", "bus_mv": 2000},
             "rx": {"address_hex": "0x41", "bus_mv": 2000}}
        r = self.r[0]
        self.assertEqual(capture_to_record(d, r["phase"], r["timestamp_ms"], r["reference_mv"]), r)
        for mutation in (lambda x: x.update(hardware_approved=True),
                         lambda x: x.update(physical_measurements=1),
                         lambda x: x["rx"].update(address_hex="0x40"),
                         lambda x: x["tx"].update(bus_mv=True)):
            altered = copy.deepcopy(d)
            mutation(altered)
            with self.assertRaises(MappingFault):
                capture_to_record(altered, r["phase"], r["timestamp_ms"], r["reference_mv"])

    def test_synthetic_demo_rejects_attacks(self):
        d = synthetic_demo()
        self.assertTrue(d["synthetic_valid"]["pattern_pass"])
        self.assertFalse(d["synthetic_alias"]["pattern_pass"])
        self.assertFalse(d["synthetic_swapped"]["pattern_pass"])
        for v in d.values():
            self.assertFalse(v["hardware_approved"])


if __name__ == "__main__":
    unittest.main()
