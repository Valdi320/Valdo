"""W-IND-57: INA219 two-address single-shot acquisition contract (NO hardware backend).

Only an injected transport/clock can operate the recorder. Included simulation is
synthetic; this module contains no SMBus, GPIO, RF or power-control operations.
"""
from __future__ import annotations
import argparse
import json

CONFIG, SHUNT, BUS, POWER = 0, 1, 2, 3
# INA219: BRNG=16V, PGA=40mV, bus/shunt 12-bit 16 averages, shunt+bus TRIGGERED.
CFG_16AVG_TRIGGER = (12 << 7) | (12 << 3) | 3  # 0x0663
CONVERSION_NS = 17_020_000  # 2 * 8.51ms, TYPICAL datasheet, NOT guaranteed max
TIMEOUT_NS = 50_000_000     # W bench screening policy, NOT datasheet maximum
MAX_SKEW_NS = 2_000_000    # W screening policy, not physical synchronization


class CaptureFault(ValueError):
    """Reject the entire capture; never manufacture missing measurements."""


def word(value):
    if type(value) is not int or not (0 <= value <= 65535):
        raise CaptureFault("invalid_unsigned_16bit_register")
    return value


def _read(bus, addr, register):
    return word(bus.read16(addr, register))


def _time(clock):
    t = clock.monotonic_ns()
    if type(t) is not int or t < 0:
        raise CaptureFault("invalid_monotonic_clock")
    return t


def capture_pair(port, clock, tx_address=0x40, rx_address=0x41):
    """Acquire overlapping INA219 triggered conversion *windows*.

    Port exposes write16(addr,reg,word) / read16(addr,reg).
    Clock exposes monotonic_ns() / sleep_ns(delay). These are injected;
    no physical adapter is implemented. All failures are fail-closed.
    The data never authorizes any energization, lithium charging or cutoff.
    """
    addresses = (tx_address, rx_address)
    if any(type(a) is not int or not 0x40 <= a <= 0x4F for a in addresses) or addresses[0] == addresses[1]:
        raise CaptureFault("ina219_addresses_not_distinct_or_invalid")
    first = _time(clock)
    starts = {}
    try:
        for addr in addresses:
            starts[addr] = _time(clock)
            port.write16(addr, CONFIG, CFG_16AVG_TRIGGER)
            if _read(port, addr, CONFIG) != CFG_16AVG_TRIGGER:
                raise CaptureFault("config_write_not_read_back")
            status = _read(port, addr, BUS)
            if status & 0b11:  # CNVR bit 1; OVF bit 0
                raise CaptureFault("cnvr_or_overflow_not_cleared_by_trigger")
        if max(starts.values()) - min(starts.values()) > MAX_SKEW_NS:
            raise CaptureFault("trigger_skew_exceeds_screening_policy")
        samples = {}
        last = _time(clock)
        # Finite loop even if a fake clock remains frozen.
        for _ in range(60):
            for addr in addresses:
                if addr in samples:
                    continue
                status = _read(port, addr, BUS)
                if status & 1:
                    raise CaptureFault("ina219_math_overflow")
                if not (status & 2):
                    continue
                when = _time(clock)
                if when < starts[addr] or when - starts[addr] > TIMEOUT_NS:
                    raise CaptureFault("conversion_outside_capture_window")
                signed = _read(port, addr, SHUNT)
                signed = signed - 65536 if signed >= 32768 else signed
                if _read(port, addr, CONFIG) != CFG_16AVG_TRIGGER:
                    raise CaptureFault("configuration_changed_during_capture")
                if _read(port, addr, BUS) != status:
                    raise CaptureFault("bus_sample_changed_during_single_shot")
                # Reading POWER clears CNVR per TI. This is NOT a power reading.
                _read(port, addr, POWER)
                if _read(port, addr, BUS) & 3:
                    raise CaptureFault("cnvr_not_cleared_by_power_read")
                bus_mv = (status >> 3) * 4
                shunt_uv = signed * 10  # TI: 10 microvolt per signed LSB
                current_ma_tenths = signed  # with *ASSUMED* 0.1 ohm shunt: 0.1mA/LSB
                if not (0 < bus_mv <= 6000) or not (0 <= current_ma_tenths <= 3000):
                    raise CaptureFault("outside_hypothetical_sensor_voltage_current_envelope")
                samples[addr] = dict(address_hex=hex(addr), trigger_ns=starts[addr], ready_ns=when,
                                     raw_shunt_u16=(signed & 65535), raw_bus_u16=status,
                                     shunt_uv=shunt_uv, bus_mv=bus_mv,
                                     current_ma_tenths_assuming_100mohm=current_ma_tenths)
            if len(samples) == 2:
                tx, rx = (samples[a] for a in addresses)
                return {"milestone":"W-IND-57", "source_kind":"SYNTHETIC_OR_UNTRUSTED_ADAPTER",
                        "config_word_hex":hex(CFG_16AVG_TRIGGER),"addresses":list(map(hex, addresses)),
                        "start_ns":first,"trigger_skew_ns":abs(starts[addresses[1]]-starts[addresses[0]]),
                        "tx":tx,"rx":rx,"conversion_windows_overlap":(
                            max(starts.values()) <= min(tx["ready_ns"],rx["ready_ns"])),
                        "simulated_only":True,"physical_measurements":0,
                        "meter_shunt_calibrated":False,"physical_clock_proven":False,
                        "efficiency_qualified":False,"hardware_approved":False,
                        "energization_approved":False,"lithium_dock_approved":False}
            now = _time(clock)
            if now < last:
                raise CaptureFault("clock_moved_backwards")
            if now - first > TIMEOUT_NS:
                raise CaptureFault("ina219_conversion_timeout")
            last = now
            clock.sleep_ns(1_000_000)
        raise CaptureFault("ina219_no_progress")
    except CaptureFault:
        raise
    except Exception as ex:
        raise CaptureFault("transport_or_clock_failure") from ex


class FakeClock:
    def __init__(self): self.now = 0
    def monotonic_ns(self): return self.now
    def sleep_ns(self, delay): self.now += delay


class FakePort:
    """Synthetic INA219 registers, not actual I2C hardware."""
    def __init__(self, clock, faults=None):
        self.clock, self.faults = clock, set(faults or ())
        self.started, self.ready_cleared = {}, {}
        self.words = {0x40: (1250 << 3, 800), 0x41: (1000 << 3, 800)}
    def write16(self, address, register, value):
        if register != CONFIG or value != CFG_16AVG_TRIGGER: raise ValueError("fake unexpected write")
        self.started[address] = self.clock.now
        self.ready_cleared[address] = False
    def read16(self, address, register):
        if "i2c_fault" in self.faults: raise OSError("synthetic bus fault")
        if "short_read" in self.faults: return None
        if register == CONFIG:
            return 0x399F if "reset" in self.faults else CFG_16AVG_TRIGGER
        if register == BUS:
            v, _ = self.words[address]
            if "stale_cnvr" in self.faults: return v | 2
            if "overflow" in self.faults: return v | 1
            if "high_bus" in self.faults: v = 1750 << 3
            if "no_ready" in self.faults: return v
            ready = self.clock.now - self.started[address] >= CONVERSION_NS
            if ready and not self.ready_cleared[address]: return v | 2
            if ready and "stuck_cnvr" in self.faults: return v | 2
            return v
        if register == SHUNT:
            s = self.words[address][1]
            if "reverse_current" in self.faults: s = 65536 - 800
            if "overcurrent" in self.faults: s = 4000
            return s
        if register == POWER:
            if "stuck_cnvr" not in self.faults: self.ready_cleared[address] = True
            return 0  # no calibration programmed in this simulation
        raise ValueError("fake invalid register")


def demo():
    c = FakeClock()
    return capture_pair(FakePort(c), c)


def main():
    p = argparse.ArgumentParser(description="INA219 I2C contract; synthetic only")
    p.add_argument("--demo", action="store_true", required=True)
    p.add_argument("--out")
    args = p.parse_args()
    s = json.dumps(demo(),sort_keys=True,indent=2)+"\n"
    if args.out:
        from pathlib import Path
        Path(args.out).write_text(s,encoding="utf-8")
    else: print(s,end="")

if __name__ == "__main__": main()
