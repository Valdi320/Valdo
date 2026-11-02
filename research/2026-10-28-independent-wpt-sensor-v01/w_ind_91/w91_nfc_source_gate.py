"""W-IND-91: prevent falsely attributing external Nucleo power to harvested NFC energy.

Original digital evidence gate, NOT a circuit simulator, firmware, or physical approval.
Source: ST UM2960 Rev.2 pp. 2,4,7: ST1 selects 3V3 versus EH for ST25DV64KC VCC,
I2C/GPO go to Nucleo, V_EH is not a documented Nucleo MCU supply.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import json

SOURCE_DATE = "2026-11-01"
TX_BOARD = "X-NUCLEO-NFC08A1"
RX_BOARD = "X-NUCLEO-NFC07A1"
RX_IC = "ST25DV64KC"
ST1_VALUES = frozenset({"EH", "3V3", "REMOVED", "UNKNOWN"})
EH_VALUES = frozenset({"STATIC", "DYNAMIC", "DISABLED", "UNKNOWN"})
FIELD_VALUES = frozenset({"ON_PLANNED", "WAKEUP_NO_FIELD", "UNKNOWN"})


@dataclass(frozen=True)
class Topology:
    tx_board: str
    rx_board: str
    rx_ic: str
    st1_position: str
    eh_configuration: str
    reader_field_mode: str
    nucleo_attached: bool
    nucleo_usb_powered: bool
    external_3v3_present: bool
    absence_of_other_sources_verified: bool
    i2c_gpo_physically_isolated: bool
    veh_to_sensor_path_documented: bool
    request_mcu_supply_from_eh: bool
    eh_load_iv_measured: bool

    def __post_init__(self) -> None:
        if self.st1_position not in ST1_VALUES:
            raise ValueError("Unknown ST1 selector")
        if self.eh_configuration not in EH_VALUES:
            raise ValueError("Unknown EH register configuration")
        if self.reader_field_mode not in FIELD_VALUES:
            raise ValueError("Unknown reader field mode")
        for field in ("nucleo_attached", "nucleo_usb_powered", "external_3v3_present",
                      "absence_of_other_sources_verified", "i2c_gpo_physically_isolated",
                      "veh_to_sensor_path_documented", "request_mcu_supply_from_eh",
                      "eh_load_iv_measured"):
            if type(getattr(self, field)) is not bool:
                raise ValueError(f"{field} must be explicit boolean")


def assess(t: Topology) -> dict:
    """Fail closed: topology candidate is NOT proof of WPT or sensor power.

    An RF field 'ON_PLANNED' is a requirement for the future bench, not a
    measured duty cycle. GPIO source/backfeed is a *risk*, not a proven fault.
    """
    reasons: list[str] = []
    if (t.tx_board, t.rx_board, t.rx_ic) != (TX_BOARD, RX_BOARD, RX_IC):
        reasons.append("MISMATCH_BOARD_OR_TAG_IC")
    if t.st1_position == "3V3":
        reasons.append("ST1_SELECTS_EXTERNAL_3V3")
    elif t.st1_position == "REMOVED":
        reasons.append("ST1_DOES_NOT_CONNECT_EH_TO_TAG_VCC")
    elif t.st1_position == "UNKNOWN":
        reasons.append("ST1_UNKNOWN")
    if t.eh_configuration == "DISABLED":
        reasons.append("EH_NOT_ENABLED_FOR_EXTERNAL_LOAD")
    elif t.eh_configuration == "UNKNOWN":
        reasons.append("EH_ENABLE_STATE_UNKNOWN")
    if t.reader_field_mode == "WAKEUP_NO_FIELD":
        reasons.append("READER_WAKEUP_WITHOUT_FIELD_CANNOT_SUPPLY_EH")
    elif t.reader_field_mode == "UNKNOWN":
        reasons.append("RF_FIELD_CONTINUITY_UNVERIFIED")
    if t.nucleo_attached:
        # No external MCU may be used as evidence of an RF-only powered sensor.
        reasons.append("NUCLEO_ATTACHED_SENSOR_POWER_PROVENANCE_NOT_ISOLATED")
        if not t.i2c_gpo_physically_isolated:
            reasons.append("I2C_GPO_BACKFEED_NOT_EXCLUDED")
        if t.nucleo_usb_powered:
            reasons.append("USB_POWERED_NUCLEO_PRESENT")
    if t.external_3v3_present:
        reasons.append("EXTERNAL_3V3_PRESENT")
    if not t.absence_of_other_sources_verified:
        reasons.append("ABSENCE_OF_EXTERNAL_POWER_NOT_VERIFIED")
    if not t.veh_to_sensor_path_documented:
        reasons.append("VEH_SENSOR_PATH_NOT_DOCUMENTED")
    if t.request_mcu_supply_from_eh:
        reasons.append("ST1_EH_DOES_NOT_POWER_NUCLEO_MCU")
    # Even a structurally isolated candidate cannot claim measured output.
    topology_candidate = not reasons
    if not t.eh_load_iv_measured:
        reasons.append("EH_LOAD_IV_NOT_MEASURED")
    # Manufacturer says EH analog output may be high-Z for insufficient field.
    reasons.append("ST25DV64KC_VEH_HIGH_Z_AT_INSUFFICIENT_FIELD_UNTESTED")
    reasons.append("FOD_TEMP_EMI_OFFSET_AND_INDEPENDENT_CUT_UNVERIFIED")
    return {
        "topology_candidate_only": topology_candidate,
        "claim_RF_only_powered_sensor_validated": False,
        "claim_Nucleo_MCU_powered_by_EH": False,
        "hardware_release": "BLOCKED",
        "reasons": reasons,
    }


def base_case() -> Topology:
    # Synthetic clean *topology* proposal, not proof of physical wiring or RF.
    return Topology(TX_BOARD, RX_BOARD, RX_IC, "EH", "STATIC", "ON_PLANNED",
                    False, False, False, True, True, True, False, False)


def report() -> dict:
    clean = base_case()
    examples = {
        "isolated_proposal_no_measurements": clean,
        "ST_default_usb_external_power": replace(clean, st1_position="3V3", nucleo_attached=True,
                                                 nucleo_usb_powered=True,
                                                 i2c_gpo_physically_isolated=False,
                                                 external_3v3_present=True),
        "EH_selected_but_USB_MCU_attached": replace(clean, nucleo_attached=True,
                                                     nucleo_usb_powered=True,
                                                     i2c_gpo_physically_isolated=False),
        "EH_selected_RF_reader_wakeup": replace(clean, reader_field_mode="WAKEUP_NO_FIELD"),
        "EH_disabled": replace(clean, eh_configuration="DISABLED"),
        "unsupported_claim_EH_powers_Nucleo": replace(clean, request_mcu_supply_from_eh=True),
    }
    return {
        "milestone": "W-IND-91",
        "source_date": SOURCE_DATE,
        "evidence_kind": "synthetic_topology_and_manufacturer_schematic_review",
        "source": "ST UM2960 Rev2 pp2,4,6-7; ST DB4607 Rev1 p2; ST X-NUCLEO-NFC08A1 product page",
        "board_configuration_fact": "ST1 selects the ST25DV64KC VCC source (3V3 or EH), not a Nucleo MCU power feed",
        "no_external_sensor_power_proven": True,
        "examples": {k: assess(v) for k, v in examples.items()},
        "buyer_decision": "DO_NOT_ORDER_TWO_NUCLEOS_TO_PROVE_BATTERYLESS_SENSOR",
        "battery_BMS_dock_status": "DISCONNECTED_OUT_OF_SCOPE",
        "motors_pumps_WPT": "NOT_PROPOSED",
        "ESP_NOW_OpenThread": "DATA_ONLY_ACK_CRC_SEQ_TIMEOUT_PRIVACY_REQUIRED",
        "physical_tests_conducted": 0,
        "hardware_release": "BLOCKED",
    }


if __name__ == "__main__":
    print(json.dumps(report(), sort_keys=True, indent=2, ensure_ascii=False))
