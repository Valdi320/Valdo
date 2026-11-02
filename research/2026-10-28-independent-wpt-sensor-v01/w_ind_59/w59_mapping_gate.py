"""W-IND-59: offline anti-alias check for two INA219 channel labels.

This has NO I2C backend and NEVER enables power. A patterned trace cannot prove
silicon identity, calibration, safe WPT power, or physical measurement provenance.
The independent stimulus is a future, separately authorised *resistive* bench.
"""
from __future__ import annotations
import copy
import json


class MappingFault(ValueError):
    """Fail closed; no result is an authorisation for electrical operation."""


PHASES = ("baseline", "tx_step", "rx_step")
CHANNELS = ("tx", "rx")
ADDRESSES = {"tx": 0x40, "rx": 0x41}
# SCREENING assumptions, not product acceptance or guaranteed sensor accuracy.
MAX_ABSOLUTE_ERROR_MV = 60
MIN_TARGET_STEP_MV = 1000
MAX_REFERENCE_OFFTARGET_MV = 40
MIN_ON_TARGET_GAIN = 0.90
MAX_ON_TARGET_GAIN = 1.10
MAX_CROSS_GAIN = 0.05
MIN_DETERMINANT = 0.80
MAX_DURATION_MS = 30000


def _exact_int(value, name, low, high):
    if type(value) is not int or not low <= value <= high:
        raise MappingFault("invalid_" + name)
    return value


def _phase_record(record, phase):
    if type(record) is not dict or record.get("phase") != phase:
        raise MappingFault("invalid_or_out_of_order_phase")
    if set(record) != {"phase", "timestamp_ms", "reference_mv", "observed_mv", "addresses"}:
        raise MappingFault("unexpected_or_missing_trace_field")
    timestamp = _exact_int(record["timestamp_ms"], "timestamp", 0, 2**53 - 1)
    for key in ("reference_mv", "observed_mv", "addresses"):
        if type(record[key]) is not dict or set(record[key]) != set(CHANNELS):
            raise MappingFault("invalid_" + key)
    for channel in CHANNELS:
        _exact_int(record["addresses"][channel], "address", 0, 127)
        if record["addresses"][channel] != ADDRESSES[channel]:
            raise MappingFault("address_role_changed")
        _exact_int(record["reference_mv"][channel], "reference_mv", 1, 6000)
        _exact_int(record["observed_mv"][channel], "observed_mv", 1, 6000)
    return timestamp


def check_mapping(records):
    """Assess a 3-phase, independently challenged 2x2 measurement response.

    Inputs are ALWAYS untrusted offline records. The caller must use separate
    evidence of instrument/source identity before any hardware qualification.
    This function intentionally never returns hardware_approved=True.
    """
    if type(records) is not list or len(records) != len(PHASES):
        raise MappingFault("exactly_three_ordered_phases_required")
    times = [_phase_record(record, phase) for phase, record in zip(PHASES, records)]
    if not (times[0] < times[1] < times[2]):
        raise MappingFault("timestamps_not_strictly_increasing")
    if times[2] - times[0] > MAX_DURATION_MS:
        raise MappingFault("challenge_duration_too_long")

    r0, rtx, rrx = (r["reference_mv"] for r in records)
    m0, mtx, mrx = (r["observed_mv"] for r in records)
    dtx = rtx["tx"] - r0["tx"]
    drx = rrx["rx"] - r0["rx"]
    if dtx < MIN_TARGET_STEP_MV or drx < MIN_TARGET_STEP_MV:
        raise MappingFault("independent_reference_step_missing")
    if abs(rtx["rx"] - r0["rx"]) > MAX_REFERENCE_OFFTARGET_MV:
        raise MappingFault("tx_step_reference_not_independent")
    if abs(rrx["tx"] - r0["tx"]) > MAX_REFERENCE_OFFTARGET_MV:
        raise MappingFault("rx_step_reference_not_independent")

    matrix = {
        "tx_from_tx": (mtx["tx"] - m0["tx"]) / dtx,
        "rx_from_tx": (mtx["rx"] - m0["rx"]) / dtx,
        "tx_from_rx": (mrx["tx"] - m0["tx"]) / drx,
        "rx_from_rx": (mrx["rx"] - m0["rx"]) / drx,
    }
    determinant = (matrix["tx_from_tx"] * matrix["rx_from_rx"]
                   - matrix["tx_from_rx"] * matrix["rx_from_tx"])
    # Error budget is independent of mapping: correctly-labelled but biased
    # channels must not appear fit for efficiency calculations.
    errors = {p: {ch: abs(r["observed_mv"][ch] - r["reference_mv"][ch])
                  for ch in CHANNELS} for p, r in zip(PHASES, records)}
    good_gain = all(MIN_ON_TARGET_GAIN <= matrix[k] <= MAX_ON_TARGET_GAIN
                    for k in ("tx_from_tx", "rx_from_rx"))
    good_cross = all(abs(matrix[k]) <= MAX_CROSS_GAIN
                     for k in ("rx_from_tx", "tx_from_rx"))
    good_abs = all(e <= MAX_ABSOLUTE_ERROR_MV
                   for by_channel in errors.values() for e in by_channel.values())
    pattern_pass = good_gain and good_cross and good_abs and determinant >= MIN_DETERMINANT
    return {
        "milestone": "W-IND-59",
        "source_kind": "UNTRUSTED_OFFLINE_RECORDS",
        "screening_result": "PASS_PATTERN_ONLY" if pattern_pass else "REJECT_PATTERN",
        "pattern_pass": pattern_pass,
        "response_matrix": {k: round(v, 6) for k, v in matrix.items()},
        "determinant": round(determinant, 6),
        "absolute_errors_mv": errors,
        "gate_diagnostics": {
            "gain": good_gain, "cross_coupling": good_cross,
            "absolute_reference_error": good_abs,
            "positive_determinant": determinant >= MIN_DETERMINANT,
        },
        "physical_measurements_performed_by_this_software": 0,
        "meter_identity_proven": False,
        "independent_reference_proven": False,
        "calibration_proven": False,
        "efficiency_qualified": False,
        "hardware_approved": False,
        "energization_approved": False,
        "lithium_dock_approved": False,
        "thermal_fod_emi_and_independent_cutoff_proven": False,
    }


def capture_to_record(capture, phase, timestamp_ms, reference_mv):
    """Convert *one* W57 capture into a W59 offline role challenge record.

    The W57/W58 capture data has no independently trusted identity metadata.
    In particular W57 currently marks simulated_only=True even if a future
    injected raw bus reads hardware: never infer physical evidence here.
    """
    if type(capture) is not dict or capture.get("milestone") != "W-IND-57":
        raise MappingFault("unsupported_capture_format")
    if capture.get("addresses") != ["0x40", "0x41"]:
        raise MappingFault("unexpected_capture_address_map")
    if (capture.get("hardware_approved") is not False
            or capture.get("physical_measurements") != 0):
        raise MappingFault("untrusted_capture_claims")
    measured = {}
    for ch, address in ADDRESSES.items():
        sample = capture.get(ch)
        if type(sample) is not dict or sample.get("address_hex") != hex(address):
            raise MappingFault("capture_role_mismatch")
        measured[ch] = _exact_int(sample.get("bus_mv"), "capture_bus_mv", 1, 6000)
    record = {"phase": phase, "timestamp_ms": timestamp_ms,
              "reference_mv": copy.deepcopy(reference_mv),
              "observed_mv": measured, "addresses": dict(ADDRESSES)}
    _phase_record(record, phase)
    return record


def synthetic_records():
    """Generated offline fixtures, NOT a suggested live supply sequence."""
    return [
        {"phase": "baseline", "timestamp_ms": 100, "reference_mv": {"tx": 2000, "rx": 2000},
         "observed_mv": {"tx": 2000, "rx": 2000}, "addresses": dict(ADDRESSES)},
        {"phase": "tx_step", "timestamp_ms": 200, "reference_mv": {"tx": 5000, "rx": 2000},
         "observed_mv": {"tx": 5000, "rx": 2000}, "addresses": dict(ADDRESSES)},
        {"phase": "rx_step", "timestamp_ms": 300, "reference_mv": {"tx": 2000, "rx": 4000},
         "observed_mv": {"tx": 2000, "rx": 4000}, "addresses": dict(ADDRESSES)},
    ]


def synthetic_demo():
    good = synthetic_records()
    alias = copy.deepcopy(good)
    for r in alias:
        r["observed_mv"]["rx"] = r["observed_mv"]["tx"]
    swapped = copy.deepcopy(good)
    for r in swapped:
        r["observed_mv"]["tx"], r["observed_mv"]["rx"] = (
            r["observed_mv"]["rx"], r["observed_mv"]["tx"])
    return {"synthetic_valid": check_mapping(good),
            "synthetic_alias": check_mapping(alias),
            "synthetic_swapped": check_mapping(swapped)}


if __name__ == "__main__":
    print(json.dumps(synthetic_demo(), indent=2, sort_keys=True))
