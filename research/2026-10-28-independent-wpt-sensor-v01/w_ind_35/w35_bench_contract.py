"""W-IND-35: safe-by-default CSV evidence gate for future, authorized, isolated bench.

Original VALDO W work. No I/O to hardware; this parser does not authorize energizing.
All voltage/time acceptance thresholds are provisional engineering assumptions.
"""
from __future__ import annotations
import csv
import io
import json
import math
import sys
from collections import defaultdict

FIELDS = ("scenario", "t_ms", "v_logic", "v_monitor", "v_alert", "v_pg",
          "v_enable_a", "v_enable_b", "v_load", "rearm_origin")
SCENARIOS = ("idle", "local_rearm", "monitor_vdd_lost", "alert_open",
             "alert_short", "monitor_pg_lost", "restore_no_rearm", "rf_rearm_attempt")
NUMERIC = set(FIELDS) - {"scenario", "rearm_origin"}
# All of these are DESIGN HYPOTHESES, not component limits or safety certifications.
LOGIC_MIN, LOGIC_MAX = 4.5, 5.5
OFF_MAX = 0.4
LOAD_OFF_MAX = 0.5
ON_MIN = 2.5
LOAD_ON_MIN = 4.0
DECISION_FROM_MS = 100.0


def parse_csv(text: str):
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None or tuple(reader.fieldnames) != FIELDS:
        raise ValueError(f"CSV fields must be exactly: {','.join(FIELDS)}")
    rows = []
    for lineno, raw in enumerate(reader, 2):
        if raw["scenario"] not in SCENARIOS:
            raise ValueError(f"line {lineno}: unknown scenario")
        if raw["rearm_origin"] not in ("none", "local", "rf"):
            raise ValueError(f"line {lineno}: invalid rearm_origin")
        r = dict(raw)
        for key in NUMERIC:
            try:
                r[key] = float(raw[key])
            except (ValueError, TypeError):
                raise ValueError(f"line {lineno}: invalid {key}") from None
            if not math.isfinite(r[key]) or r[key] < 0:
                raise ValueError(f"line {lineno}: nonfinite/negative {key}")
        if r["t_ms"] > 10000 or any(r[k] > 6.0 for k in NUMERIC if k != "t_ms"):
            raise ValueError(f"line {lineno}: outside provisional 0..6 V/10s fixture envelope")
        rows.append(r)
    return rows


def evaluate(rows, *, evidence_kind="synthetic"):
    """Checks ONLY observable voltage/path behavior, never approves power hardware.

    Source labels are self-asserted: even a 'measured' CSV requires external
    calibration, schematic review and an authorized safety process.
    """
    if evidence_kind not in ("synthetic", "measured_unverified"):
        raise ValueError("evidence_kind must be synthetic or measured_unverified")
    groups = defaultdict(list)
    for r in rows:
        groups[r["scenario"]].append(r)
    problems = []
    if set(groups) != set(SCENARIOS):
        problems.append("coverage: missing=" + repr(sorted(set(SCENARIOS) - set(groups))))
    observations = {}
    for scenario in SCENARIOS:
        seq = groups[scenario]
        if not seq:
            continue
        times = [r["t_ms"] for r in seq]
        if times != sorted(set(times)):
            problems.append(f"{scenario}: nonmonotonic or repeated timestamps")
        if not times or times[0] != 0:
            problems.append(f"{scenario}: missing t=0 baseline")
        # Ensures we cannot certify a 100-ms event from only a final late sample.
        samples = [r for r in seq if DECISION_FROM_MS <= r["t_ms"] <= 200]
        if len(samples) < 2 or (samples[-1]["t_ms"] - samples[0]["t_ms"] > 50):
            problems.append(f"{scenario}: require >=2 samples in 100..200 ms, span <=50 ms")
            continue
        observations[scenario] = len(samples)
        for r in samples:
            if not LOGIC_MIN <= r["v_logic"] <= LOGIC_MAX:
                problems.append(f"{scenario}: control rail not valid at {r['t_ms']} ms")
            if scenario == "local_rearm":
                if r["rearm_origin"] != "local":
                    problems.append("local_rearm: missing positive local-action provenance")
                if not (r["v_enable_a"] >= ON_MIN and r["v_enable_b"] >= ON_MIN
                        and r["v_load"] >= LOAD_ON_MIN and r["v_pg"] >= ON_MIN):
                    problems.append("local_rearm: fixture did not show requested live state")
            else:
                if not (r["v_enable_a"] <= OFF_MAX and r["v_enable_b"] <= OFF_MAX
                        and r["v_load"] <= LOAD_OFF_MAX):
                    problems.append(f"{scenario}: physical OFF not observed at {r['t_ms']} ms")
                if scenario == "rf_rearm_attempt" and r["rearm_origin"] != "rf":
                    problems.append("rf_rearm_attempt: RF attempt was not actually represented")
                if scenario in ("idle", "restore_no_rearm") and r["rearm_origin"] != "none":
                    problems.append(f"{scenario}: must not have a local rearm")
                if scenario == "monitor_vdd_lost":
                    if not (r["v_monitor"] <= 0.5 and r["v_pg"] <= OFF_MAX):
                        problems.append("monitor_vdd_lost: monitor-off/PG-low stimulus not proven")
                    # The special discriminatory case: passive EOL stays plausible.
                    if not 0.40 <= r["v_alert"] / r["v_logic"] <= 0.60:
                        problems.append("monitor_vdd_lost: ALERT was not in false-healthy window")
                if scenario == "monitor_pg_lost" and r["v_pg"] > OFF_MAX:
                    problems.append("monitor_pg_lost: missing low-PG stimulus")
                if scenario == "alert_open" and r["v_alert"] / r["v_logic"] < 0.8:
                    problems.append("alert_open: no high ALERT stimulus")
                if scenario == "alert_short" and r["v_alert"] / r["v_logic"] > 0.2:
                    problems.append("alert_short: no low ALERT stimulus")
    return {
        "case_count": len(groups), "expected_cases": len(SCENARIOS),
        "sample_count": len(rows), "decision_window_ms": [100, 200],
        "discriminatory_condition": "monitor unpowered; ALERT in healthy EOL window; independent PG low",
        "case_decision_samples": observations,
        "contract_pass": not problems,
        "problems": sorted(set(problems)),
        "origin": evidence_kind,
        "hardware_validated": False,
        "energization_authorized": False,
        "status": "DIGITAL_FIXTURE_DEMONSTRATION_ONLY" if evidence_kind == "synthetic"
                  else "HUMAN_INSTRUMENT_AND_SAFETY_REVIEW_REQUIRED",
    }


def demo_rows():
    """Strictly synthetic fixture to test the EVIDENCE ANALYZER, not the circuit."""
    rows = []
    for name in SCENARIOS:
        for t in (0, 100, 120, 140):
            live = name == "local_rearm"
            rows.append(dict(scenario=name, t_ms=float(t), v_logic=5.,
                v_monitor=0.0 if name == "monitor_vdd_lost" else 5.,
                v_alert=5.0 if name == "alert_open" else 0.0 if name == "alert_short" else 2.5,
                v_pg=0.0 if name in ("monitor_vdd_lost", "monitor_pg_lost") else 5.0,
                v_enable_a=3.3 if live else 0.0,
                v_enable_b=3.3 if live else 0.0,
                v_load=5.0 if live else 0.0,
                rearm_origin="local" if live else "rf" if name == "rf_rearm_attempt" else "none"))
    return rows


def format_csv(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=FIELDS, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow(r)
    return buf.getvalue()


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--demo":
        rows = parse_csv(format_csv(demo_rows()))
        print(json.dumps(evaluate(rows), indent=2, ensure_ascii=False, sort_keys=True))
    elif len(sys.argv) == 3 and sys.argv[1] == "--csv":
        with open(sys.argv[2], encoding="utf-8", newline="") as f:
            rows = parse_csv(f.read())
        print(json.dumps(evaluate(rows, evidence_kind="measured_unverified"),
                         indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print("Usage: python3 w35_bench_contract.py --demo | --csv <file>", file=sys.stderr)
        sys.exit(2)
