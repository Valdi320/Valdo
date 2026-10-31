"""W-IND-71: passive TX bleeder Pareto gate, strictly digital and fail-closed.

One ideal RC model with worst-case assumed tolerances, *not* measured WPT
hardware. Inspect actual W21 native KiCad XML via W70/W22 before calculations.
No permission to construct, energize, charge a battery or call this FOD.
Copyright 2026 VALDO W contributors. Original Python standard-library code.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
from w_ind_70.w70_native_storage_gate import review_native_xml


def number(name, x, lo, hi):
    if type(x) not in (float, int) or not math.isfinite(x) or not lo <= x <= hi:
        raise ValueError(f"{name}: finite non-boolean number in [{lo}, {hi}] required")
    return float(x)


def assess(
    xml_bytes: bytes, *,
    max_assumed_v: float = 5.5,
    cap_nominal_f: float = 100e-6,
    cap_tolerance: float = 0.20,
    resistor_tolerance: float = 0.05,
    threshold_assumed_v: float = 0.5,
    max_assumed_decay_s: float = 0.250,
    max_assumed_standby_bleed_w: float = 0.005,
) -> dict:
    """Derive an allowed R_nom interval, or prove it is empty for given assumptions.

    In an ideal, *unpowered* RC: t=R*C*ln(V0/Vthreshold).
    If source stays at V0, P_bleed=V0**2/R.
    For R_nom tolerances +/- dR and C_nom tolerances +/- dC:
      Rnom >= Vmax**2 / (Pbudget * (1-dR))
      Rnom <= tbudget / ((1+dR)*Cnom*(1+dC)*ln(Vmax/Vthreshold))
    Both inequalities are only conditional on the assumptions.
    """
    if type(xml_bytes) is not bytes:
        raise TypeError("native KiCad XML must be bytes")
    v = number("max_assumed_v", max_assumed_v, 0.01, 5.5)
    c = number("cap_nominal_f", cap_nominal_f, 1e-10, 0.1)
    dc = number("cap_tolerance", cap_tolerance, 0, 0.999999)
    dr = number("resistor_tolerance", resistor_tolerance, 0, 0.999999)
    vt = number("threshold_assumed_v", threshold_assumed_v, 1e-8, 5.5)
    deadline = number("max_assumed_decay_s", max_assumed_decay_s, 1e-6, 3600)
    budget = number("max_assumed_standby_bleed_w", max_assumed_standby_bleed_w, 1e-8, 10)
    if vt >= v:
        raise ValueError("threshold_assumed_v must be below max_assumed_v")

    w70 = review_native_xml(xml_bytes)
    result = {
        "milestone": "W-IND-71",
        "source_xml_sha256": hashlib.sha256(xml_bytes).hexdigest(),
        "source": "W21 native KiCad XML through W22/W70; tolerances and targets are hypothetical",
        "status": "BLOCKED_UNREVIEWED_NETLIST",
        "w70_status": w70["status"],
        "w22_exact_netlist": w70["topology_exact_w22"],
        "hardware_approved": False,
        "power_on_allowed": False,
        "battery_bms_dock_connected": False,
        "physical_tests": 0,
        "actual_external_tx_storage": "UNKNOWN_NOT_ZERO",
        "independent_fod_thermal_cut_qualified": False,
        "resistor_open_failure_auto_detected": False,
        "no_radio_dependent_critical_stop": True,
        "data_kind": "MODEL_NOT_MEASURED",
    }
    if w70["status"] != "BLOCKED_EXTERNAL_TX_STORAGE_UNCHARACTERIZED":
        return result

    r2 = w70["nominal_resistive_branches"]["R2"]
    if r2["terminals"] != ["/GND", "/TX_5V_CUT"]:
        return result
    r = r2["nominal_ohms"]
    logratio = math.log(v / vt)
    min_nom_r = v*v / (budget * (1-dr))
    max_nom_r = deadline / ((1+dr) * c * (1+dc) * logratio)
    worst_power_existing = v*v / (r * (1-dr))
    worst_decay_existing = r * (1+dr) * c * (1+dc) * logratio
    # Largest nominal capacitor compatible with the *two* hypothetical
    # conditions if R_nom is optimized and both tolerance bounds hold.
    max_nom_c_feasible_f = deadline / (
        (1+dr) * (1+dc) * min_nom_r * logratio)
    feasible = min_nom_r <= max_nom_r
    result.update({
        "status": ("BLOCKED_PASSIVE_CONSTRAINTS_INCOMPATIBLE"
                   if not feasible else "BLOCKED_FEASIBLE_ONLY_UNDER_ASSUMPTIONS"),
        "hypotheses": {
            "max_assumed_v": v,
            "cap_nominal_f": c,
            "cap_tolerance_fraction": dc,
            "resistor_tolerance_fraction": dr,
            "threshold_assumed_v": vt,
            "max_assumed_decay_s": deadline,
            "max_assumed_standby_bleed_w": budget,
            "ideal_single_RC_only": True,
        },
        "nominal_resistor_interval_ohm": {
            "minimum_from_standby": min_nom_r,
            "maximum_from_decay": max_nom_r,
        },
        "any_fixed_passive_resistor_meets_both_assumptions": feasible,
        "largest_feasible_nominal_capacitance_f": max_nom_c_feasible_f,
        "existing_W21_R2_nominal_ohm": r,
        "existing_R2_worst_case_screen": {
            "max_continuous_bleed_w": worst_power_existing,
            "max_ideal_decay_s": worst_decay_existing,
            "passes_power_budget": worst_power_existing <= budget,
            "passes_decay_target": worst_decay_existing <= deadline,
        },
        "power_safety_limit": (
            "Ideal RC does not cover external TX inductors, capacitors, "
            "resonance, reverse feed, failed-open R2, metal FOD, thermal/EMI, "
            "power source regulation, independent switch failures or real values"),
        "design_conclusion": (
            "Passive-only R cannot satisfy both *assumed* goals; inspect "
            "real storage and study independently controlled discharge, "
            "but do not select or energize hardware"
            if not feasible else
            "A resistor interval exists mathematically; no physical or "
            "thermal qualification follows"),
    })
    return result


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("native_xml", type=Path)
    p.add_argument("--report", type=Path, required=True)
    a = p.parse_args(argv)
    try:
        result = assess(a.native_xml.read_bytes())
        result["source_file"] = a.native_xml.as_posix()
        exit_code = (0 if result["status"] in (
            "BLOCKED_PASSIVE_CONSTRAINTS_INCOMPATIBLE",
            "BLOCKED_FEASIBLE_ONLY_UNDER_ASSUMPTIONS",
        ) else 1)
    except (OSError, TypeError, ValueError, OverflowError) as exc:
        result = {
            "milestone": "W-IND-71", "status": "BLOCKED_INVALID_INPUT",
            "error": str(exc), "hardware_approved": False,
            "power_on_allowed": False, "physical_tests": 0,
        }
        exit_code = 1
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    print(result["status"])
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
