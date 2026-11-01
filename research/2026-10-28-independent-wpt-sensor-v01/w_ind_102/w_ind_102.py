#!/usr/bin/env python3
"""W-IND-102: ST25DVxxKC energy-harvesting feasibility gate.

Manufacturer-data analysis only. It is not a physical WPT measurement.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA_PATH = HERE / "AN4913_REV2_EH.csv"

PILOT_AVG_MW = 400.0
PILOT_PEAK_MW = 1500.0
MICRO_AVG_TARGET_MW = 0.25
MIN_FIELD_A_PER_M = 1.0
MICRO_PEAK_MW = 5.0
MICRO_PEAK_MS = 10.0
BUFFER_V_HI = 3.3
BUFFER_V_LO = 2.0
BUFFER_EFFICIENCY = 0.80
CAPACITANCE_RETENTION = 0.50


def validate_rows(rows: list[dict]) -> None:
    if len(rows) != 22:
        raise ValueError("expected 22 AN4913 points")
    for am in (10, 100):
        group = [r for r in rows if r["am_percent"] == am]
        if len(group) != 11:
            raise ValueError("expected 11 points for each AM setting")
        if sorted(r["h_a_per_m_rms"] for r in group) != [x / 2 for x in range(1, 12)]:
            raise ValueError("unexpected H-field sweep")
    keys = [(r["am_percent"], r["h_a_per_m_rms"]) for r in rows]
    if len(set(keys)) != len(keys):
        raise ValueError("duplicate AM/H point")


def load_rows(path: Path = DATA_PATH) -> list[dict]:
    expected = ["am_percent", "h_a_per_m_rms", "v_eh_v", "i_eh_ma", "p_eh_mw"]
    rows = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != expected:
            raise ValueError("unexpected AN4913 CSV columns")
        for raw in reader:
            row = {
                "am_percent": int(raw["am_percent"]),
                "h_a_per_m_rms": float(raw["h_a_per_m_rms"]),
                "v_eh_v": float(raw["v_eh_v"]),
                "i_eh_ma": float(raw["i_eh_ma"]),
                "p_eh_mw": float(raw["p_eh_mw"]),
            }
            if row["am_percent"] not in (10, 100):
                raise ValueError("AM must be 10 or 100 percent")
            if min(row["h_a_per_m_rms"], row["v_eh_v"], row["i_eh_ma"], row["p_eh_mw"]) <= 0:
                raise ValueError("manufacturer values must be positive")
            if abs(row["v_eh_v"] * row["i_eh_ma"] - row["p_eh_mw"]) > 0.0051:
                raise ValueError("P_EH does not match V_EH * I_EH")
            rows.append(row)
    validate_rows(rows)
    return rows


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_report(rows: list[dict]) -> dict:
    validate_rows(rows)
    am100 = [r for r in rows if r["am_percent"] == 100]
    am10 = [r for r in rows if r["am_percent"] == 10]
    best = max(rows, key=lambda r: r["p_eh_mw"])
    reference = [r for r in rows if r["h_a_per_m_rms"] >= MIN_FIELD_A_PER_M]
    min_reference = min(reference, key=lambda r: r["p_eh_mw"])

    pulse_energy_j = MICRO_PEAK_MW / 1000.0 * MICRO_PEAK_MS / 1000.0
    delta_v_squared = BUFFER_V_HI ** 2 - BUFFER_V_LO ** 2
    c_effective_f = 2.0 * pulse_energy_j / delta_v_squared / BUFFER_EFFICIENCY
    c_nominal_f = c_effective_f / CAPACITANCE_RETENTION

    return {
        "schema": "valdo.w_ind_102.eh-envelope.v1",
        "classification": "MANUFACTURER_DATA_ANALYSIS_NOT_PHYSICAL_MEASUREMENT",
        "source": {
            "document": "STMicroelectronics AN4913 Rev 2",
            "revision_date": "2021-06-01",
            "applicable_parts_table_1": [
                "ST25DV04K", "ST25DV16K", "ST25DV64K",
                "ST25DV04KC", "ST25DV16KC", "ST25DV64KC"
            ],
            "measurement_setup": "ST25DV-I2C on ISO/IEC Class 1 antenna, 13.6 MHz tuning, 10 nF V_EH capacitor, controlled RF field",
            "tables": [4, 5],
            "board_transfer_limit": "The data applies to ST25DV64KC silicon, but does not qualify the 54 mm X-NUCLEO-NFC07A1 antenna/board."
        },
        "manufacturer_points": {
            "count": len(rows),
            "am100_count": len(am100),
            "am10_count": len(am10),
            "max_am100_mw": max(r["p_eh_mw"] for r in am100),
            "max_am10_mw": max(r["p_eh_mw"] for r in am10),
            "max_all_mw": best["p_eh_mw"],
            "max_all_point": best,
            "min_h_ge_1a_m_point": min_reference,
            "min_h_ge_1a_mw": min_reference["p_eh_mw"],
            "h_ge_1a_points": len(reference)
        },
        "pilot_400mw_avg_1500mw_peak": {
            "avg_mw": PILOT_AVG_MW,
            "peak_mw": PILOT_PEAK_MW,
            "avg_ratio_of_best_reference_pct": round(100.0 * best["p_eh_mw"] / PILOT_AVG_MW, 6),
            "avg_shortfall_factor": round(PILOT_AVG_MW / best["p_eh_mw"], 6),
            "peak_ratio_of_best_reference_pct": round(100.0 * best["p_eh_mw"] / PILOT_PEAK_MW, 6),
            "peak_shortfall_factor": round(PILOT_PEAK_MW / best["p_eh_mw"], 6),
            "nfc_eh_for_continuous_pilot": "NO_GO"
        },
        "proposed_microsensor_gate": {
            "average_power_max_mw": MICRO_AVG_TARGET_MW,
            "field_min_a_per_m_rms": MIN_FIELD_A_PER_M,
            "manufacturer_points_meeting_reference_gate": len(reference),
            "minimum_reference_power_mw": min_reference["p_eh_mw"],
            "minimum_reference_margin_factor": round(min_reference["p_eh_mw"] / MICRO_AVG_TARGET_MW, 6),
            "status": "CONDITIONAL_REFERENCE_ONLY_NOT_BOARD_QUALIFIED"
        },
        "illustrative_peak_buffer": {
            "peak_mw": MICRO_PEAK_MW,
            "duration_ms": MICRO_PEAK_MS,
            "energy_uj": round(pulse_energy_j * 1e6, 6),
            "voltage_window_v": [BUFFER_V_HI, BUFFER_V_LO],
            "buffer_efficiency_assumption": BUFFER_EFFICIENCY,
            "capacitance_retention_assumption": CAPACITANCE_RETENTION,
            "effective_capacitance_uf_min": round(c_effective_f * 1e6, 3),
            "nominal_capacitance_uf_min": round(c_nominal_f * 1e6, 3),
            "standard_value_candidate_uf": 47,
            "status": "CALCULATION_ONLY_NOT_SELECTED_ESR_LEAKAGE_COLD_START_UNTESTED"
        },
        "electrical_and_rf_constraints": {
            "v_eh_regulated": False,
            "v_eh_high_z_when_field_insufficient_or_eh_disabled": True,
            "rf_communication_guaranteed_across_full_eh_domain": False,
            "rf_communication_can_work_inside_an4913_measured_green_domain": True,
            "high_load_can_break_rf_communication": True,
            "battery_bms_dock_connected": False,
            "physical_measurements_performed": 0,
            "hardware_approved": False
        },
        "architecture_decision": {
            "module_400mw_average": "REJECT_ST25DV64KC_EH; use dedicated regulated WPT only after FOD/thermal/offset/EMI/independent-cut qualification, otherwise locking wired connector",
            "first_microsensor": "PROVISIONAL_TARGET <=0.25mW average, <=5mW for <=10ms buffered pulse, field >=1A/m RMS at the actual tag; board-specific RF/energy measurements still required",
            "dock_charging": "SEPARATE_SYSTEM; no battery/BMS/dock work in this milestone",
            "data": "ESP-NOW for a small one-hop Espressif network; OpenThread only if IPv6 mesh/multi-hop is required; both need application ACK, CRC, sequence, timeout, authenticated privacy and recovery; no radio critical stop",
            "wisp5": "Only consider for passive microsensors; no firmware or CAD reused"
        },
        "input_sha256": sha256(DATA_PATH),
        "model_sha256": sha256(Path(__file__).resolve())
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    payload = json.dumps(build_report(load_rows()), indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
