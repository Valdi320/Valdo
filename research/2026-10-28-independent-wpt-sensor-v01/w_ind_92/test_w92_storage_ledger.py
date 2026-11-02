"""Digital adversarial tests; no hardware has been energized or measured."""
import unittest
from copy import deepcopy
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from w92_storage_ledger import energy_bounds, demo, REQUIRED_FLAGS


def base():
    return {
        "case_id": "synthetic_test", "provenance": "synthetic",
        "tx_input_uj": "100", "load_uj": "120", "tx_abs_error_uj": "2",
        "load_abs_error_uj": "2", "cap_effective_uf": "1000",
        "cap_tolerance_pct": "5", "cap_start_mv": "3200", "cap_end_mv": "3190",
        "voltage_abs_error_mv": "1", "cap_rated_mv": "6300",
        **{k: True for k in REQUIRED_FLAGS},
    }


class LedgerTests(unittest.TestCase):
    def test_buffered_burst_reconciled(self):
        r = energy_bounds(base())
        self.assertEqual(r["naive_load_to_TX_ratio_pct"], "120.000")
        self.assertEqual(r["consistency"], "CONSISTENT_WITH_IDEAL_SINGLE_BUFFER_MODEL")
        self.assertEqual(r["hardware_release"], "BLOCKED")
        self.assertFalse(r["candidate_for_manual_evidence_review"])

    def test_real_source_not_proved_by_synthetic(self):
        self.assertEqual(demo()["source"], "invented_synthetic_values_not_ST_measurements")

    def test_energy_creation_flagged_when_cap_stable(self):
        c=base(); c.update(cap_end_mv="3200", load_uj="150")
        self.assertEqual(energy_bounds(c)["consistency"], "INCOMPATIBLE_WITH_SINGLE_SOURCE_MODEL")

    def test_charging_reservoir_increases_accounted_energy(self):
        c=base(); c.update(tx_input_uj="110", load_uj="50", cap_start_mv="3190", cap_end_mv="3200")
        r=energy_bounds(c)
        self.assertGreater(float(r["inferred_rail_source_uj_interval"][0]),50)

    def test_measurement_uncertainty_can_be_ambiguous(self):
        c=base(); c.update(voltage_abs_error_mv="10")
        self.assertEqual(energy_bounds(c)["consistency"], "UNCERTAIN_REQUIRES_REVIEW")

    def test_no_field_energy_may_come_from_buffer(self):
        c=base(); c.update(tx_input_uj="0",tx_abs_error_uj="0", load_uj="25",load_abs_error_uj="0")
        self.assertEqual(energy_bounds(c)["consistency"], "NO_TX_INPUT_OBSERVED")
        self.assertIsNone(energy_bounds(c)["conditional_rail_to_TX_energy_ratio_pct_interval"])

    def test_negative_inferred_energy_indicates_hidden_load(self):
        c=base(); c.update(load_uj="1", load_abs_error_uj="0", cap_end_mv="3100")
        self.assertEqual(energy_bounds(c)["consistency"], "UNACCOUNTED_RAIL_SINK_OR_BAD_MODEL")

    def test_provenance_not_recognized(self):
        c=base(); c["provenance"]="lab certified"
        with self.assertRaises(ValueError): energy_bounds(c)

    def test_no_bench_claim_from_unproven_metadata(self):
        c=base(); c["provenance"]="bench_measured"
        with self.assertRaisesRegex(ValueError,"metadata"): energy_bounds(c)

    def test_bench_metadata_claim_never_hardware_release(self):
        c=base(); c["provenance"]="bench_measured"
        c.update(instrument_id="declared",calibration_reference="declared",fixture_id="declared",operator_record="declared",raw_trace_sha256="a"*64)
        r=energy_bounds(c)
        self.assertEqual(r["hardware_release"],"BLOCKED")
        self.assertIn("metadata_not_authentication",r["limitations"])

    def test_bad_hash_rejected(self):
        c=base(); c["provenance"]="bench_measured"
        c.update(instrument_id="x",calibration_reference="x",fixture_id="x",operator_record="x",raw_trace_sha256="xyz")
        with self.assertRaisesRegex(ValueError,"SHA256"):energy_bounds(c)

    def test_unverified_external_source_blocks_review(self):
        c=base(); c["external_sources_excluded"]=False
        self.assertIn("not_verified_external_sources_excluded",energy_bounds(c)["reject_reasons"])

    def test_missing_buffer_location_blocks_review(self):
        c=base(); c["buffer_on_measured_rx_rail"]=False
        self.assertIn("not_verified_buffer_on_measured_rx_rail",energy_bounds(c)["reject_reasons"])

    def test_bool_is_not_int(self):
        c=base(); c["all_other_stores_accounted"]=1
        with self.assertRaises(ValueError):energy_bounds(c)

    def test_bool_is_not_string(self):
        c=base(); c["same_measurement_window"]="true"
        with self.assertRaises(ValueError):energy_bounds(c)

    def test_cap_rating_checked_with_uncertainty(self):
        c=base(); c["cap_rated_mv"]="3200"
        with self.assertRaisesRegex(ValueError,"rating"):energy_bounds(c)

    def test_zero_cap_invalid(self):
        c=base(); c["cap_effective_uf"]="0"
        with self.assertRaises(ValueError):energy_bounds(c)

    def test_over_100_pct_cap_tolerance_invalid(self):
        c=base(); c["cap_tolerance_pct"]="100"
        with self.assertRaises(ValueError):energy_bounds(c)

    def test_nonfinite_and_negative_rejected(self):
        for field,value in (("tx_input_uj","NaN"),("load_uj","Infinity"),("cap_start_mv","-2")):
            c=base(); c[field]=value
            with self.subTest(field=field), self.assertRaises(ValueError):energy_bounds(c)

    def test_error_larger_than_energy_rejected(self):
        c=base(); c["tx_abs_error_uj"]="120"
        with self.assertRaises(ValueError):energy_bounds(c)

    def test_error_larger_than_voltage_rejected(self):
        c=base(); c["voltage_abs_error_mv"]="3201"
        with self.assertRaises(ValueError):energy_bounds(c)

    def test_missing_field_rejected(self):
        c=base();del c["load_uj"]
        with self.assertRaises(KeyError):energy_bounds(c)

    def test_deterministic_pure_function(self):
        c=base();self.assertEqual(energy_bounds(c),energy_bounds(deepcopy(c)))

    def test_no_radio_safety_claim(self):
        self.assertIn("FOD_heat_offset_EMI_cut_and_humidity_unverified", energy_bounds(base())["limitations"])

    def test_no_battery_approval(self):
        self.assertIn("battery_BMS_dock_disconnected", energy_bounds(base())["limitations"])


if __name__ == "__main__": unittest.main()
