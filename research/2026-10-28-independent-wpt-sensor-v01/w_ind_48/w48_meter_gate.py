#!/usr/bin/env python3
"""W-IND-48: conservative, bench-only paired power/energy screening; stdlib only.

Not protection, FOD, safety interlock, oscilloscope or Li-ion charging qualification.
"""
import argparse
import csv
import hashlib
import io
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQ = ("t_ms", "v_volts", "i_amps")
BLOCKERS = ("independent normally-OFF cutoff", "hardware overcurrent/thermal", "physical metal FOD", "offset/wetness", "EMI", "bench instrumentation calibration and clock check", "lithium charger/BMS review is out of scope")


def number(s, name):
    try:
        value = Decimal(str(s))
    except (InvalidOperation, TypeError) as exc:
        raise ValueError(f"invalid {name}") from exc
    if not value.is_finite():
        raise ValueError(f"nonfinite {name}")
    return value


def read_stream(raw):
    reader = csv.DictReader(io.StringIO(raw))
    if tuple(reader.fieldnames or ()) != REQ:
        raise ValueError("expected exact header t_ms,v_volts,i_amps")
    samples = []
    for item in reader:
        if None in item or any(x is None for x in item.values()):
            raise ValueError("malformed CSV row")
        t, v, i = (number(item[k], k) for k in REQ)
        if t < 0 or v <= 0 or i < 0:
            raise ValueError("negative time/current or nonpositive bus voltage")
        if samples and t <= samples[-1][0]:
            raise ValueError("nonmonotonic or duplicate timestamp")
        samples.append((t, v, i))
    if len(samples) < 3:
        raise ValueError("at least three samples per stream required")
    return samples


def integrate(samples):
    return sum((((a[1] * a[2]) + (b[1] * b[2])) / 2) * ((b[0] - a[0]) / 1000)
               for a, b in zip(samples, samples[1:]))


def screen(tx_csv, rx_csv, config):
    if not isinstance(config, dict):
        raise ValueError("config must be an object")
    mode = config.get("mode")
    if mode not in ("synthetic", "measured"):
        raise ValueError("mode must be synthetic or measured")
    if mode == "measured" and (not config.get("battery_disconnected") or
                               config.get("source_kind") != "isolated_current_limited" or
                               config.get("load_kind") != "resistive" or
                               not config.get("calibration_ref")):
        raise ValueError("measured mode needs bench declarations and calibration reference")
    u_tx = number(config.get("tx_relative_power_uncertainty"), "tx uncertainty")
    u_rx = number(config.get("rx_relative_power_uncertainty"), "rx uncertainty")
    skew_limit = number(config.get("max_skew_ms", "25"), "max skew")
    gap_limit = number(config.get("max_gap_ms", "250"), "max gap")
    min_eff = number(config.get("min_efficiency", "0.70"), "min efficiency")
    if any(u < 0 or u >= Decimal("0.5") for u in (u_tx, u_rx)) or min_eff <= 0 or min_eff > 1 or skew_limit < 0 or gap_limit <= 0:
        raise ValueError("invalid limits or uncertainty")
    if mode == "measured" and (u_tx == 0 or u_rx == 0):
        raise ValueError("real measurement cannot declare zero uncertainty")
    tx, rx = read_stream(tx_csv), read_stream(rx_csv)
    if len(tx) != len(rx):
        raise ValueError("missing samples; do not interpolate silently")
    if any(abs(a[0]-b[0]) > skew_limit for a,b in zip(tx,rx)):
        raise ValueError("TX and RX sample clocks are not aligned")
    if any(y[0]-x[0] > gap_limit for series in (tx,rx) for x,y in zip(series,series[1:])):
        raise ValueError("unobserved sampling gap")
    e_in, e_out = integrate(tx), integrate(rx)
    if e_in <= 0:
        raise ValueError("no input energy")
    eta = e_out / e_in
    lower = eta * (1-u_rx)/(1+u_tx)
    upper = eta * (1+u_rx)/(1-u_tx)
    plausible = eta <= 1 and lower <= 1
    payload = {
        "evidence_class": mode,
        "samples_per_side": len(tx),
        "window_ms": str(tx[-1][0]-tx[0][0]),
        "energy_input_j": str(e_in),
        "energy_output_j": str(e_out),
        "efficiency_nominal": str(eta),
        "efficiency_conservative_lower": str(lower),
        "efficiency_upper": str(upper),
        "screening_threshold": str(min_eff),
        "energetic_screen_pass": bool(plausible and lower >= min_eff),
        "anomalous_energy_gain": not plausible,
        "hardware_approved": False,
        "battery_or_dock_approved": False,
        "blockers": BLOCKERS,
        "input_sha256": {"tx": hashlib.sha256(tx_csv.encode()).hexdigest(),
                         "rx": hashlib.sha256(rx_csv.encode()).hexdigest(),
                         "config": hashlib.sha256(json.dumps(config,sort_keys=True,ensure_ascii=False).encode()).hexdigest()},
        "uncertainty_note": "User-supplied assumptions; not inferred from INA219 chip accuracy. Includes shunt, gain, offset, temperature and clock only if explicitly budgeted.",
    }
    return payload


def demo():
    # 21 points x 50 ms; TX 0.50 W, RX 0.40 W for 1.0 s: 80% synthetic.
    header = "t_ms,v_volts,i_amps\n"
    tx = header+"".join(f"{t},5,0.1\n" for t in range(0,1001,50))
    rx = header+"".join(f"{t},5,0.08\n" for t in range(0,1001,50))
    cfg = {"mode":"synthetic","tx_relative_power_uncertainty":"0.03","rx_relative_power_uncertainty":"0.03", "max_skew_ms":"25","max_gap_ms":"250","min_efficiency":"0.70"}
    return screen(tx,rx,cfg)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tx",type=Path)
    p.add_argument("--rx",type=Path)
    p.add_argument("--config",type=Path)
    p.add_argument("--demo",action="store_true")
    p.add_argument("--out",type=Path)
    a = p.parse_args()
    if a.demo:
        result=demo()
    else:
        if not all((a.tx,a.rx,a.config)):
            p.error("supply --tx --rx --config or --demo")
        result=screen(a.tx.read_text(encoding="utf-8"),a.rx.read_text(encoding="utf-8"),json.loads(a.config.read_text(encoding="utf-8")))
    text=json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n"
    if a.out:
        a.out.write_text(text,encoding="utf-8")
    else:
        print(text,end="")

if __name__ == "__main__":
    main()
