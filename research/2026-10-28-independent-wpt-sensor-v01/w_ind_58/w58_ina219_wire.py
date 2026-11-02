"""W-IND-58: INA219 big-endian register wire adapter (injected bus only).

NO physical I2C implementation. A raw bus must supply write(addr, bytes) and
write_read(addr, command_bytes, count) with an atomic repeated-start transfer.
This wrapper NEVER operates a battery, charger, GPIO, motor, or WPT stage.
"""
from __future__ import annotations

import json


class WireFault(ValueError):
    """No measurement may be accepted after malformed raw I2C traffic."""


class INA219WirePort:
    """Implement W57's read16/write16 through explicit MSB-first bytes.

    SMBus read_word_data uses the opposite byte ordering on many adapters;
    passing its integer straight to W57 is NOT this contract.
    """

    def __init__(self, raw_bus):
        self.raw_bus = raw_bus
        self.transactions = 0

    @staticmethod
    def _address(address):
        if type(address) is not int or not 0x40 <= address <= 0x4F:
            raise WireFault("invalid_ina219_i2c_address")

    @staticmethod
    def _register(register):
        if type(register) is not int or register not in (0, 1, 2, 3):
            raise WireFault("invalid_ina219_register")

    def write16(self, address, register, value):
        self._address(address)
        self._register(register)
        if register != 0:
            raise WireFault("configuration_only_write_policy")
        if type(value) is not int or not 0 <= value <= 0xFFFF:
            raise WireFault("invalid_write_word")
        payload = bytes((register, value >> 8, value & 0xFF))
        try:
            receipt = self.raw_bus.write(address, payload)
        except Exception as exc:
            raise WireFault("raw_i2c_write_failure") from exc
        if receipt is not None:
            raise WireFault("raw_write_contract_violation")
        self.transactions += 1

    def read16(self, address, register):
        self._address(address)
        self._register(register)
        try:
            data = self.raw_bus.write_read(address, bytes((register,)), 2)
        except Exception as exc:
            raise WireFault("raw_i2c_read_failure") from exc
        if type(data) is not bytes or len(data) != 2:
            raise WireFault("raw_i2c_exact_two_bytes_required")
        self.transactions += 1
        return int.from_bytes(data, byteorder="big", signed=False)


class SyntheticRawBus:
    """Test bridge to a fake register model. Never accesses /dev/i2c*."""

    def __init__(self, fake_register_port, *, reverse_read_bytes=False):
        self.fake = fake_register_port
        self.reverse_read_bytes = reverse_read_bytes
        self.write_log = []
        self.read_log = []

    def write(self, address, payload):
        if type(payload) is not bytes or len(payload) != 3:
            raise WireFault("raw_write_requires_register_and_two_bytes")
        self.write_log.append((address, payload.hex()))
        self.fake.write16(address, payload[0], int.from_bytes(payload[1:], "big"))
        return None

    def write_read(self, address, command, count):
        if type(command) is not bytes or len(command) != 1 or count != 2:
            raise WireFault("raw_read_requires_one_register_two_bytes")
        word = self.fake.read16(address, command[0])
        if type(word) is not int or not 0 <= word <= 0xFFFF:
            raise WireFault("fake_bad_register_word")
        value = word.to_bytes(2, "big")
        self.read_log.append((address, command.hex(), value.hex()))
        return value[::-1] if self.reverse_read_bytes else value


def synthetic_demo():
    from pathlib import Path
    import sys
    # Explicitly reuse the original W57 test double, not a hardware driver.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "w_ind_57"))
    from w57_i2c_capture import FakeClock, FakePort, capture_pair

    clock = FakeClock()
    raw = SyntheticRawBus(FakePort(clock))
    port = INA219WirePort(raw)
    result = capture_pair(port, clock)
    return {
        "milestone": "W-IND-58", "source_kind": "SYNTHETIC", "transactions": port.transactions,
        "first_config_write_hex": raw.write_log[0][1],
        "second_config_write_hex": raw.write_log[1][1],
        "first_read_command_hex": raw.read_log[0][1],
        "first_read_response_hex": raw.read_log[0][2],
        "tx_bus_mv_synthetic": result["tx"]["bus_mv"],
        "rx_bus_mv_synthetic": result["rx"]["bus_mv"],
        "physical_measurements": 0, "hardware_approved": False,
        "energization_approved": False, "lithium_dock_approved": False,
        "physical_i2c_implemented": False, "meter_identity_proven": False,
        "calibration_proven": False, "thermal_fod_emi_proven": False,
    }


if __name__ == "__main__":
    print(json.dumps(synthetic_demo(), indent=2, sort_keys=True))
