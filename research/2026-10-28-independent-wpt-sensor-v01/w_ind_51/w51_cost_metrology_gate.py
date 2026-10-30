"""W-IND-51: bench-only dual-meter cost and shunt screen, no hardware I/O.

Original implementation, standard library Python 3.10+. Neither approval of
energizing hardware nor proof of vendor availability or calibration.
"""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import argparse
import json
from pathlib import Path


def D(value):
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError("invalid decimal") from exc
    if not result.is_finite():
        raise ValueError("non-finite input")
    return result


@dataclass(frozen=True)
class Offer:
    sku: str
    seller: str
    unit_price_gross_eur: str | None
    shipping_gross_eur: str | None
    mounting_gross_eur: str | None
    quantity: int = 2
    vat_verified: bool = False
    seller_stock_verified: bool = False
    shunt_traceable: bool = False
    calibrated_pair: bool = False
    min_order_qty: int | None = None
    fixture_gross_eur: str | None = None
    calibration_gross_eur: str | None = None
    delivery_to_zaragoza_verified: bool = False
    # Verified store stock is not verified stock at the Zaragoza shop.
    diotronic_zaragoza_stock_verified: bool = False


def price_gate(offer: Offer) -> dict:
    if not isinstance(offer.quantity, int) or isinstance(offer.quantity, bool) or offer.quantity < 2:
        raise ValueError("two separately placed TX/RX meters are mandatory")
    missing = []
    for name in ("unit_price_gross_eur", "shipping_gross_eur", "mounting_gross_eur", "fixture_gross_eur", "calibration_gross_eur"):
        if getattr(offer, name) is None:
            missing.append(name)
    if offer.min_order_qty is None:
        missing.append("min_order_qty")
    elif not isinstance(offer.min_order_qty, int) or isinstance(offer.min_order_qty, bool) or offer.min_order_qty < 1:
        raise ValueError("invalid minimum order quantity")
    if not offer.delivery_to_zaragoza_verified:
        missing.append("delivery_to_zaragoza_verified")
    if not offer.vat_verified:
        missing.append("vat_verified")
    if not offer.seller_stock_verified:
        missing.append("seller_stock_verified")
    if not offer.shunt_traceable:
        missing.append("shunt_traceable")
    if not offer.calibrated_pair:
        missing.append("calibrated_pair")
    if not offer.sku.strip() or not offer.seller.strip():
        raise ValueError("identifiable seller and SKU required")
    if offer.unit_price_gross_eur is not None:
        unit = D(offer.unit_price_gross_eur)
        if unit < 0:
            raise ValueError("negative price")
        floor = unit * max(offer.quantity, offer.min_order_qty or offer.quantity) if offer.vat_verified else None
    else:
        floor = None
    if offer.shipping_gross_eur is not None and D(offer.shipping_gross_eur) < 0:
        raise ValueError("negative shipping")
    for field in ("mounting_gross_eur", "fixture_gross_eur", "calibration_gross_eur"):
        if getattr(offer, field) is not None and D(getattr(offer, field)) < 0:
            raise ValueError("negative added expense")
    complete = len(missing) == 0
    total = (floor + sum((D(getattr(offer, f)) for f in ("shipping_gross_eur", "mounting_gross_eur", "fixture_gross_eur", "calibration_gross_eur")), D(0))) if complete else None
    return {
        "sku": offer.sku, "seller": offer.seller,
        "pair_gross_floor_eur": str(floor) if floor is not None else None,
        "pair_delivered_gross_eur": str(total) if total is not None else None,
        "missing": missing, "ready_for_cost_comparison": complete,
        "stock_in_zaragoza_confirmed": offer.diotronic_zaragoza_stock_verified,
        "hardware_approved": False,
    }


def shunt_screen(current_min_a, current_peak_a, shunt_ohm, shunt_fsr_v,
                 offset_uv, quantization_half_lsb_uv,
                 shunt_tolerance_pct, gain_error_pct, max_current_error_pct):
    vals = [D(v) for v in (current_min_a, current_peak_a, shunt_ohm, shunt_fsr_v,
                             offset_uv, quantization_half_lsb_uv,
                             shunt_tolerance_pct, gain_error_pct, max_current_error_pct)]
    imin, ipeak, r, fsr, offset, quant, tol, gain, budget = vals
    if imin <= 0 or ipeak < imin or r <= 0 or fsr <= 0 or budget <= 0:
        raise ValueError("invalid electrical ranges")
    if min(offset, quant, tol, gain) < 0:
        raise ValueError("negative uncertainty")
    vmin = imin * r
    vpeak = ipeak * r
    # Linear worst-case bound by triangle inequality, not a confidence interval.
    relative_bound_pct = tol + gain + ((offset + quant) * D(1e-6) / vmin * D(100))
    return {
        "shunt_v_at_min": str(vmin),
        "shunt_v_at_peak": str(vpeak),
        "shunt_loss_w_at_min": str(imin * imin * r),
        "shunt_loss_w_at_peak": str(ipeak * ipeak * r),
        "hypothetical_current_error_bound_pct": str(relative_bound_pct),
        "peak_fits_selected_pga": vpeak <= fsr,
        "passes_hypothetical_budget": vpeak <= fsr and relative_bound_pct <= budget,
        "actual_calibrated_accuracy": None,
        "safety_protection_proved": False,
    }


def compare_qualified_prices(a: Offer, b: Offer) -> dict:
    x, y = price_gate(a), price_gate(b)
    if not (x["ready_for_cost_comparison"] and y["ready_for_cost_comparison"]):
        return {"difference_eur": None, "winner": None, "reason": "unknown landed/calibrated cost"}
    dx = D(x["pair_delivered_gross_eur"])
    dy = D(y["pair_delivered_gross_eur"])
    return {"difference_eur": str(abs(dx - dy)),
            "winner": a.sku if dx < dy else b.sku if dy < dx else "tie",
            "reason": "two qualified full-cost hypothetical offers; no hardware approval"}


def demo():
    satkit = Offer("MCU-219", "Satkit Spain", "3.63", None, "0", vat_verified=True,
                   seller_stock_verified=True, shunt_traceable=False, min_order_qty=1)
    berry = Offer("SOL-333066", "BerryBase EU", "7.20", None, "0", vat_verified=True,
                  seller_stock_verified=True, shunt_traceable=False, min_order_qty=1)
    ina260 = Offer("ADA4226", "BerryBase EU", "10.95", None, "0", vat_verified=True,
                   seller_stock_verified=True, shunt_traceable=False, min_order_qty=1)
    bare = Offer("INA219BIDCNR", "DigiKey Spain", "2.15380", None, None,
                 vat_verified=True, seller_stock_verified=True, shunt_traceable=False, min_order_qty=1)
    diode = Offer("PENDING-INA219", "Diotronic Zaragoza", None, None, None)
    return {
        "date": "2026-10-30", "evidence_kind": "SYNTHETIC-CATALOG-NOT-HARDWARE",
        "requirements": "2 reusable DC input/output meters, 80mA minimum, 300mA peak hypothetical, 5V",
        "offers": [price_gate(x) for x in (satkit, berry, ina260, bare, diode)],
        "shunt_100mohm_conditional": shunt_screen("0.08", "0.30", "0.1", "0.04",
                                                      "50", "5", "1", "0.5", "3"),
        "shunt_10mohm_conditional": shunt_screen("0.08", "0.30", "0.01", "0.04",
                                                     "50", "5", "1", "0.5", "3"),
        "no_cost_winner_until_shipping_and_calibration": True,
        "requires_independent_cutoff_FOD_thermal_EMI": True,
        "battery_BMS_dock_disconnected": True,
        "hardware_approved": False,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--demo", action="store_true")
    p.add_argument("--out", default="-")
    args = p.parse_args()
    if not args.demo:
        p.error("only --demo is supported; never measures hardware")
    data = json.dumps(demo(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out == "-":
        print(data, end="")
    else:
        Path(args.out).write_text(data, encoding="utf-8")


if __name__ == "__main__":
    main()
