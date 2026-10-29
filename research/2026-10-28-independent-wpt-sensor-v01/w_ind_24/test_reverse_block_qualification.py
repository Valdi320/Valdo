"""20 deterministic checks; NO physical/electrical/thermal measurements."""
import unittest
from reverse_block_qualification import CANDIDATES, screen, summary

class W24Tests(unittest.TestCase):
    def test_three_parts(self): self.assertEqual(len(CANDIDATES), 3)
    def test_22918_no_rcb(self): self.assertFalse(screen("TPS22918DBVR")["manufacturer_claims_healthy_reverse_block"])
    def test_22918_no_limit(self): self.assertIsNone(screen("TPS22918DBVR")["current_limit_floor_a"])
    def test_2521_rcb_claim(self): self.assertTrue(screen("TPS25210ARPWR")["manufacturer_claims_healthy_reverse_block"])
    def test_25947_rcb_claim(self): self.assertTrue(screen("TPS259474ARPWR")["manufacturer_claims_healthy_reverse_block"])
    def test_2521_vin_out(self): self.assertFalse(screen("TPS25210ARPWR",supply_v=5.8)["datasheet_operating_vin_ok"])
    def test_25947_vin_in(self): self.assertTrue(screen("TPS259474ARPWR",supply_v=5.8)["datasheet_operating_vin_ok"])
    def test_fet_short_denies_reverse_proof(self):
        self.assertFalse(screen("TPS25210ARPWR",internal_pass_fet_short=True)["reverse_block_with_injected_internal_short"])
    def test_avg_current(self): self.assertAlmostEqual(screen("TPS25210ARPWR")["average_current_a_assumed"], .08)
    def test_peak_current(self): self.assertAlmostEqual(screen("TPS259474ARPWR")["peak_current_a_assumed"], .3)
    def test_fault_below_limit_floor(self): self.assertTrue(screen("TPS25210ARPWR")["assumed_fault_below_configurable_limit_floor"])
    def test_fault_above_floor(self):
        self.assertFalse(screen("TPS25210ARPWR",detectable_fault_a=.6)["assumed_fault_below_configurable_limit_floor"])
    def test_peak_below_floor(self): self.assertTrue(screen("TPS259474ARPWR")["assumed_peak_below_limit_floor"])
    def test_monitor_not_qualified_at_80ma(self):
        self.assertFalse(screen("TPS25210ARPWR")["current_monitor_accuracy_qualified_at_assumed_average"])
    def test_typical_2521_overhead(self):
        self.assertAlmostEqual(screen("TPS25210ARPWR")["typical_avg_device_overhead_mw"], 2.2534)
    def test_typical_25947_overhead(self):
        self.assertAlmostEqual(screen("TPS259474ARPWR")["typical_avg_device_overhead_mw"], 2.31112)
    def test_bad_values(self):
        for kw in ({"supply_v":0},{"peak_w":.1},{"average_w":-1},
                   {"detectable_fault_a":0},{"supply_v":float("nan")},{"peak_w":float("inf")}):
            with self.subTest(kw=kw),self.assertRaises(ValueError): screen("TPS25210ARPWR",**kw)
    def test_unknown_part(self):
        with self.assertRaises(ValueError): screen("unqualified-efuse")
    def test_all_parts_locked(self):
        for c in CANDIDATES:
            d=screen(c)
            self.assertFalse(d["power_on_allowed"])
            self.assertFalse(d["hardware_approved"])
            self.assertFalse(d["reverse_block_hardware_measured"])
    def test_summary_locked(self):
        d=summary();self.assertFalse(d["hardware_approved"]);self.assertEqual(len(d["candidates"]),3)

if __name__ == "__main__": unittest.main()
