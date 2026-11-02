"""Adversarial, purely digital tests of W-IND-91; no hardware connected."""
import dataclasses
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from w91_nfc_source_gate import Topology, assess, base_case, report


class SourceIsolationTests(unittest.TestCase):
    def test_clean_topology_only_not_power_proof(self):
        r = assess(base_case())
        self.assertTrue(r["topology_candidate_only"])
        self.assertFalse(r["claim_RF_only_powered_sensor_validated"])
        self.assertEqual(r["hardware_release"], "BLOCKED")
        self.assertIn("EH_LOAD_IV_NOT_MEASURED", r["reasons"])

    def assert_rejected(self, key, value, code):
        r = assess(dataclasses.replace(base_case(), **{key: value}))
        self.assertFalse(r["topology_candidate_only"])
        self.assertIn(code, r["reasons"])
        self.assertEqual(r["hardware_release"], "BLOCKED")

    def test_wrong_board(self): self.assert_rejected("rx_board", "NFC04A1", "MISMATCH_BOARD_OR_TAG_IC")
    def test_wrong_ic(self): self.assert_rejected("rx_ic", "ST25DV04KC", "MISMATCH_BOARD_OR_TAG_IC")
    def test_wrong_reader(self): self.assert_rejected("tx_board", "NFC06A1", "MISMATCH_BOARD_OR_TAG_IC")
    def test_st1_3v3(self): self.assert_rejected("st1_position", "3V3", "ST1_SELECTS_EXTERNAL_3V3")
    def test_st1_removed(self): self.assert_rejected("st1_position", "REMOVED", "ST1_DOES_NOT_CONNECT_EH_TO_TAG_VCC")
    def test_st1_unknown(self): self.assert_rejected("st1_position", "UNKNOWN", "ST1_UNKNOWN")
    def test_eh_off(self): self.assert_rejected("eh_configuration", "DISABLED", "EH_NOT_ENABLED_FOR_EXTERNAL_LOAD")
    def test_eh_unknown(self): self.assert_rejected("eh_configuration", "UNKNOWN", "EH_ENABLE_STATE_UNKNOWN")
    def test_reader_low_power_mode(self): self.assert_rejected("reader_field_mode", "WAKEUP_NO_FIELD", "READER_WAKEUP_WITHOUT_FIELD_CANNOT_SUPPLY_EH")
    def test_reader_mode_unknown(self): self.assert_rejected("reader_field_mode", "UNKNOWN", "RF_FIELD_CONTINUITY_UNVERIFIED")
    def test_host_attached_without_usb(self): self.assert_rejected("nucleo_attached", True, "NUCLEO_ATTACHED_SENSOR_POWER_PROVENANCE_NOT_ISOLATED")
    def test_external_3v3(self): self.assert_rejected("external_3v3_present", True, "EXTERNAL_3V3_PRESENT")
    def test_no_external_source_evidence(self): self.assert_rejected("absence_of_other_sources_verified", False, "ABSENCE_OF_EXTERNAL_POWER_NOT_VERIFIED")
    def test_veh_path_missing(self): self.assert_rejected("veh_to_sensor_path_documented", False, "VEH_SENSOR_PATH_NOT_DOCUMENTED")
    def test_mcu_from_eh_unsupported(self): self.assert_rejected("request_mcu_supply_from_eh", True, "ST1_EH_DOES_NOT_POWER_NUCLEO_MCU")

    def test_host_usb_backfeed_risk(self):
        t = dataclasses.replace(base_case(), nucleo_attached=True,
                                nucleo_usb_powered=True, i2c_gpo_physically_isolated=False)
        rs = assess(t)["reasons"]
        self.assertIn("USB_POWERED_NUCLEO_PRESENT", rs)
        self.assertIn("I2C_GPO_BACKFEED_NOT_EXCLUDED", rs)

    def test_even_reported_eh_measurement_not_hardware_release(self):
        r = assess(dataclasses.replace(base_case(), eh_load_iv_measured=True))
        self.assertTrue(r["topology_candidate_only"])
        self.assertEqual(r["hardware_release"], "BLOCKED")
        self.assertFalse(r["claim_RF_only_powered_sensor_validated"])

    def test_missing_iv_never_accepted_as_measurement(self):
        self.assertIn("EH_LOAD_IV_NOT_MEASURED", assess(base_case())["reasons"])

    def test_contradictory_external_power_does_not_pass(self):
        t = dataclasses.replace(base_case(), st1_position="EH", external_3v3_present=True,
                                absence_of_other_sources_verified=True)
        self.assertFalse(assess(t)["topology_candidate_only"])

    def test_bool_must_not_be_int(self):
        with self.assertRaises(ValueError): dataclasses.replace(base_case(), nucleo_attached=1)

    def test_bool_must_not_be_string(self):
        with self.assertRaises(ValueError): dataclasses.replace(base_case(), nucleo_attached="false")

    def test_unknown_st1_rejected(self):
        with self.assertRaises(ValueError): dataclasses.replace(base_case(), st1_position="JUMPER_TO_BOTH")

    def test_unknown_eh_rejected(self):
        with self.assertRaises(ValueError): dataclasses.replace(base_case(), eh_configuration="MAGIC")

    def test_unknown_field_rejected(self):
        with self.assertRaises(ValueError): dataclasses.replace(base_case(), reader_field_mode="ALWAYS_MEASURED")

    def test_no_scenario_claims_hardware_release(self):
        for x in report()["examples"].values():
            self.assertEqual(x["hardware_release"], "BLOCKED")
            self.assertFalse(x["claim_RF_only_powered_sensor_validated"])

    def test_no_hardware_measured(self):
        self.assertEqual(report()["physical_tests_conducted"], 0)


if __name__ == "__main__":
    unittest.main()
