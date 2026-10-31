#!/usr/bin/env python3
"""W-IND-47: cost/idle-energy screening for an independently powered LOW-power sensor.

Original code, standard library only. ALL results are either dated catalog
snapshots or explicitly synthetic assumptions, NEVER hardware measurements.
The WPT option is power only; it needs separate RF/data and autonomous safety.
"""
import argparse
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

EUR = Decimal("0.01")
WPT_PAIR_EUR = Decimal("9.92")   # DFR0362 BricoGeek, VAT included, 2026-10-30
WPT_SHIP_FLOOR_EUR = Decimal("3.95")   # "desde", not final
WIRED_5PIN_PAIR_EUR = Decimal("4.50")  # Adafruit 5089 Opencircuit, VAT included
WIRED_SHIP_FLOOR_EUR = Decimal("12.50")  # "desde", not final
VOLT = Decimal("5")
NO_LOAD_CURRENT_MA = (30, 50)  # DFR0362 documented range; unmeasured here

def money(x):
    return str(x.quantize(EUR, rounding=ROUND_HALF_UP))

def evaluate(n_modules, absent_hours_per_day, tx_idle_ma):
    """One kit per module, no sharing of unproven transmitter electronics.

    This is a paired-product cost comparison, NOT an equivalent installed system:
    the wired product carries FIVE lines, WPT carries POWER ONLY.
    """
    if not isinstance(n_modules, int) or n_modules <= 0:
        raise ValueError("n_modules must be positive integer")
    hours = Decimal(str(absent_hours_per_day))
    ma = Decimal(str(tx_idle_ma))
    if not (Decimal("0") <= hours <= Decimal("24")):
        raise ValueError("absent_hours_per_day outside 0-24")
    if ma < 0:
        raise ValueError("negative current")
    wpt_items = WPT_PAIR_EUR * n_modules
    wired_items = WIRED_5PIN_PAIR_EUR * n_modules
    # Compare shipping floors separately. A "desde" quote is NEVER a final quote.
    wpt_floor = wpt_items + WPT_SHIP_FLOOR_EUR
    wired_floor = wired_items + WIRED_SHIP_FLOOR_EUR
    standby_wh = VOLT * ma / Decimal("1000") * hours * n_modules
    return {
        "modules_hypothetical": n_modules,
        "absent_hours_per_day_assumed": str(hours),
        "tx_idle_mA_assumed": str(ma),
        "wpt_pair_items_vat_eur": money(wpt_items),
        "wired_5pin_pair_items_vat_eur": money(wired_items),
        "wpt_items_minus_wired_items_eur": money(wpt_items - wired_items),
        "wpt_plus_min_shipping_eur": money(wpt_floor),
        "wired_plus_min_shipping_eur": money(wired_floor),
        "difference_with_shipping_floors_eur": money(wpt_floor - wired_floor),
        "idle_energy_wh_per_day_hypothetical": str(standby_wh.normalize()),
        "equivalent_functionality": False,
        "radio_esp_now_or_openthread_included": False,
        "safety_fod_thermal_independent_cut_included": False,
        "battery_dock_included": False,
        "cost_complete": False,
        "physical_measurement": False,
        "wpt_production_authorized": False,
        "decision": "WIRED_BASELINE; WPT_ONLY_EXPERIMENTAL_NONCRITICAL_PENDING_SAFETY_AND_PRICE",
    }

def report():
    cases = [evaluate(n, h, ma)
             for n in (1, 2, 4, 8)
             for h in (0, 2, 24)
             for ma in NO_LOAD_CURRENT_MA]
    return {
        "milestone": "W-IND-47",
        "date": "2026-10-30",
        "title": "Lowest-cost repairable low-power modules: unit BOM + idle-energy gate",
        "evidence_type": "CATALOG_PRICE_SNAPSHOTS_PLUS_SYNTHETIC_ARITHMETIC_NOT_HARDWARE",
        "source_urls": {
            "wpt_kit": "https://tienda.bricogeek.com/fuentes-de-alimentacion/899-cargador-inalambrico-5v-1a.html",
            "wpt_manufacturer": "https://wiki.dfrobot.com/dfr0362",
            "wired_5pin": "https://opencircuit.es/producto/2.0mm-pitch-5-pin-cable-matching-pair-jst-ph",
            "diotronic_ph_housing": "https://diotronic.com/serie-ph/13930-conector-hembra-ph-p-2-00-2v",
            "diotronic_ph_header": "https://diotronic.com/1290-serie-ph",
        },
        "unit_price_snapshot_eur_incl_vat": {
            "wpt_pair": money(WPT_PAIR_EUR),
            "wpt_shipping_from": money(WPT_SHIP_FLOOR_EUR),
            "wired_5pin_pair": money(WIRED_5PIN_PAIR_EUR),
            "wired_shipping_from": money(WIRED_SHIP_FLOOR_EUR),
            "diotronic_ph_2_housing_only": "0.18",
            "diotronic_ph_2_pcb_header_only": "0.36",
            "diotronic_2pin_partial_without_contacts_wires": "0.54",
        },
        "noncomparable_notice": "WPT kit supplies only power, not data or physical safety. Wired reference supplies 5 conductors. Shipping is a floor and local inventory is NOT verified.",
        "preconditions": ["independent hard cutoff and POR", "thermal trip independent of MCU",
                          "physical FOD qualification", "offset and EMI evaluation",
                          "fault recovery and safe reset", "complete supplier BOM with landed cost",
                          "noncritical module functional test and cable lifetime"],
        "cases": cases,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    body = json.dumps(report(), sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(body, encoding="utf-8")
    else:
        print(body, end="")

if __name__ == "__main__":
    main()
