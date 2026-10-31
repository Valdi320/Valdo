#!/usr/bin/env python3
"""W79: synthetic asynchronous UVLO capture/latched reset contract.

No actual comparator, clock, latch, monitoring rail, or safety certification.
The input trace is an intentionally ideal piecewise-constant voltage.
"""
import argparse
import json
import math
from pathlib import Path


def number(value, name, *, allow_zero=False):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError(f"{name}: finite numeric (not bool) required")
    if value < 0 or (not allow_zero and value == 0):
        raise ValueError(f"{name}: positive required")
    return float(value)


def time_us(value, name, *, allow_zero=False):
    n = number(value, name, allow_zero=allow_zero)
    if type(value) is not int or value > 10_000_000:
        raise ValueError(f"{name}: bounded integer microseconds required")
    return int(n)


def analyze(doc):
    if not isinstance(doc, dict):
        raise ValueError("root object required")
    threshold = number(doc.get("rx_min_v"), "rx_min_v")
    latency = time_us(doc.get("assumed_response_max_us"), "assumed_response_max_us")
    evidence = doc.get("response_evidence")
    if evidence not in ("hypothesis", "datasheet_max_claim", "bench_claim"):
        raise ValueError("response_evidence must be explicitly classified")
    source = doc.get("source_kind")
    if source not in ("synthetic", "bench_claim"):
        raise ValueError("source_kind invalid")
    claims = doc.get("monitor_claims")
    if not isinstance(claims, dict) or any(type(claims.get(k)) is not bool for k in
            ("independent_supply", "sticky_fault_memory", "hardware_cut_independent_of_radio")):
        raise ValueError("three explicit boolean monitor claims required")
    pieces = doc.get("trace")
    times = doc.get("sample_times_us")
    if not isinstance(pieces, list) or not 1 <= len(pieces) <= 10000:
        raise ValueError("trace length invalid")
    if not isinstance(times, list) or not 2 <= len(times) <= 10000:
        raise ValueError("sample times invalid")
    end = 0
    clean = []
    for i, seg in enumerate(pieces):
        if not isinstance(seg, dict) or type(seg.get("monitor_supply_ok")) is not bool:
            raise ValueError(f"trace[{i}] supply status invalid")
        start = time_us(seg.get("start_us"), "start_us", allow_zero=True)
        stop = time_us(seg.get("end_us"), "end_us")
        v = number(seg.get("rx_v"), "rx_v", allow_zero=True)
        if start != end or stop <= start:
            raise ValueError("trace must cover time contiguously without gaps/overlap")
        clean.append((start, stop, v, seg["monitor_supply_ok"]))
        end = stop
    sample_ts = [time_us(t, "sample_time", allow_zero=True) for t in times]
    if sample_ts[0] != 0 or sample_ts[-1] != end or any(
            b <= a for a, b in zip(sample_ts, sample_ts[1:])):
        raise ValueError("samples must be ordered and span trace endpoints")
    # Synthetic point observations: choose the segment starting at each timestamp.
    samples = []
    j = 0
    for t in sample_ts:
        while j + 1 < len(clean) and t >= clean[j][1]:
            j += 1
        samples.append(clean[j][2])
    faults = []
    active = None
    for start, stop, v, monitor_ok in clean:
        if v < threshold:
            if active is None:
                active = {"start_us": start, "end_us": stop, "monitor_survived": monitor_ok}
            else:
                active["end_us"] = stop
                active["monitor_survived"] &= monitor_ok
        elif active is not None:
            faults.append(active)
            active = None
    if active is not None:
        faults.append(active)
    for fault in faults:
        fault["duration_us"] = fault["end_us"] - fault["start_us"]
        fault["captured_in_ideal_model"] = (
            fault["duration_us"] >= latency and fault["monitor_survived"])
    blockers = []
    if any(not seg[3] for seg in clean):
        blockers.append("MONITOR_SUPPLY_LOST_OR_UNCERTAIN")
    if any(not f["captured_in_ideal_model"] for f in faults):
        blockers.append("UNDERVOLTAGE_PULSE_NOT_CAPTURED_IN_MODEL")
    if response_missing := evidence == "hypothesis":
        blockers.append("RESPONSE_TIME_NOT_QUALIFIED")
    if not all(claims.values()):
        blockers.append("INDEPENDENT_POWER_LATCH_OR_CUT_UNQUALIFIED")
    if source != "bench_claim":
        blockers.append("NO_BENCH_TRACE")
    hidden = [f for f in faults if not any(
        f["start_us"] <= t < f["end_us"] for t in sample_ts)]
    return {
        "status": "BLOCKED" if blockers else "CONDITIONAL_MODEL_ONLY",
        "blockers": sorted(blockers),
        "assumed_response_max_us": latency,
        "response_evidence": evidence,
        "source_kind": source,
        "samples_v": samples,
        "observed_samples_all_above_threshold": all(v >= threshold for v in samples),
        "undervoltage_events": faults,
        "hidden_events_between_samples": len(hidden),
        "ideal_model_capture_count": sum(f["captured_in_ideal_model"] for f in faults),
        "monitor_claims": claims,
        "hardware_approved": False,
        "physical_evidence_authenticated": False,
        "real_pulse_capture_proven": False,
        "critical_stop_authorized": False,
        "note": "idealized event source and latency; physical comparator maximum delay, rail survival and sticky latch remain unproven",
    }


class StickyPermit:
    """Logic model only. An RF packet can neither clear nor replace a hardware trip."""
    def __init__(self, stable_required_us=100000):
        self.stable_required_us = time_us(stable_required_us, "stable_required_us")
        self.fault_latched = True  # safe at power-on

    def fault(self, *, undervoltage=False, monitor_alive=True):
        if type(undervoltage) is not bool or type(monitor_alive) is not bool:
            raise ValueError("boolean hardware event required")
        if undervoltage or not monitor_alive:
            self.fault_latched = True

    def arm(self, *, stable_us, local_reset, monitor_alive, temperature_ok, fod_clear):
        stable = time_us(stable_us, "stable_us", allow_zero=True)
        signals = (local_reset, monitor_alive, temperature_ok, fod_clear)
        if any(type(x) is not bool for x in signals):
            raise ValueError("boolean conditions required")
        if stable >= self.stable_required_us and all(signals):
            self.fault_latched = False
        return not self.fault_latched

    def radio_ack(self):
        return not self.fault_latched


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    def reject(token):
        raise ValueError("nonfinite JSON: " + token)
    doc = json.loads(Path(a.input).read_text(encoding="utf-8"), parse_constant=reject)
    Path(a.output).write_text(json.dumps(analyze(doc), indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
