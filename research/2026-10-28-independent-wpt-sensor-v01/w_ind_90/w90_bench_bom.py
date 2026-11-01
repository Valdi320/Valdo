"""W-IND-90: reproducible supplier-priced NFC bench procurement screen.

Digital arithmetic only. No hardware authority, no procurement, no WPT qualification.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
import json

D = Decimal
VAT = D('0.21')
SOURCE_DATE = '2026-11-01'


@dataclass(frozen=True)
class Part:
    sku: str
    qty: int
    unit_eur_ex_vat: str
    url: str
    manufacturer: str
    supplier: str
    stock_kind: str

    def extended_net(self) -> Decimal:
        if not self.sku or self.manufacturer != 'STMicroelectronics':
            raise ValueError('unverified manufacturer/SKU')
        if type(self.qty) is not int or self.qty < 1:
            raise ValueError('invalid quantity')
        if not isinstance(self.unit_eur_ex_vat, str):
            raise ValueError('price must be exact decimal text')
        try:
            p = D(self.unit_eur_ex_vat)
        except Exception as exc:
            raise ValueError('invalid unit price') from exc
        if not p.is_finite() or p <= 0:
            raise ValueError('nonpositive or nonfinite price')
        if not self.url.startswith('https://www.digikey.es/') or self.supplier != 'DigiKey ES':
            raise ValueError('supplier URL unverified')
        if self.stock_kind != 'distributor_online_only':
            raise ValueError('stock cannot claim Zaragoza storefront')
        return p * self.qty


READER = Part('X-NUCLEO-NFC08A1', 1, '33.95',
              'https://www.digikey.es/es/products/detail/stmicroelectronics/X-NUCLEO-NFC08A1/16962233',
              'STMicroelectronics', 'DigiKey ES', 'distributor_online_only')
TAG_BOARD = Part('X-NUCLEO-NFC07A1', 1, '15.35',
                 'https://www.digikey.es/en/products/detail/stmicroelectronics/X-NUCLEO-NFC07A1/16284297',
                 'STMicroelectronics', 'DigiKey ES', 'distributor_online_only')
MCU = Part('NUCLEO-L476RG', 1, '20.28',
           'https://www.digikey.es/en/products/detail/stmicroelectronics/NUCLEO-L476RG/5347711',
           'STMicroelectronics', 'DigiKey ES', 'distributor_online_only')


def evaluate(parts: tuple[Part, ...], *, claim_ready: bool = False,
             exact_w89_tag: bool = False, instrumented: bool = False,
             independent_cut_tested: bool = False) -> dict:
    """Compute a *partial* kit component cost; refuse physical viability claims.

    'instrumented' is a declaration, not a certification. Tests cannot verify
    isolation, FOD, thermometry, EMC, analog measurement or certification.
    """
    if not parts or len({p.sku for p in parts}) != len(parts):
        raise ValueError('nonempty unique SKU set required')
    net = sum((p.extended_net() for p in parts), D('0'))
    gross = net * (D('1') + VAT)
    by_sku = {p.sku: p.qty for p in parts}
    physical_core = by_sku.get(READER.sku, 0) >= 1 and by_sku.get(TAG_BOARD.sku, 0) >= 1
    max_mcus = by_sku.get(MCU.sku, 0)
    reasons = []
    if not physical_core:
        reasons.append('MISSING_READER_OR_TAG_ANTENNA_EVAL_BOARD')
    if max_mcus < 2:
        reasons.append('TWO_SIDED_APP_FIRMWARE_HOSTS_NOT_COVERED')
    if not instrumented:
        reasons.append('ANALOG_V_I_TIMING_AND_CALIBRATION_UNCOSTED')
    if not independent_cut_tested:
        reasons.append('FOD_THERMAL_EMI_OFFSETS_AND_INDEPENDENT_CUT_UNQUALIFIED')
    if not exact_w89_tag:
        reasons.append('TAG_BOARD_ST25DV64KC_NOT_W89_ST25DV04KC_DEVICE')
    reasons.append('DELIVERY_ASSEMBLY_DUMMY_LOAD_AND_FINAL_COST_UNKNOWN')
    if claim_ready:
        reasons.append('UNSUPPORTED_HARDWARE_READY_CLAIM')
    return {
        'source_date': SOURCE_DATE,
        'parts': [{'sku': p.sku, 'qty': p.qty, 'unit_eur_ex_vat': p.unit_eur_ex_vat,
                   'manufacturer': p.manufacturer, 'supplier': p.supplier,
                   'stock_provenance': p.stock_kind, 'url': p.url} for p in parts],
        'subtotal_ex_vat_eur': str(net.quantize(D('.01'))),
        'subtotal_inc_21pct_vat_eur': str(gross.quantize(D('.01'))),
        'unrounded_vat_inclusive_eur': str(gross),
        'price_scope': 'partial_distributor_board_bom_no_shipping_no_instrumentation',
        'system_cost_complete': False,
        'bench_hardware_release': 'BLOCKED',
        'rf_energy_performance': 'UNMEASURED',
        'reject_reasons': reasons,
    }


def report() -> dict:
    basic = evaluate((READER, TAG_BOARD, MCU))
    dual = evaluate((READER, TAG_BOARD, Part(MCU.sku, 2, MCU.unit_eur_ex_vat,
                                           MCU.url, MCU.manufacturer, MCU.supplier, MCU.stock_kind)))
    return {
        'milestone': 'W-IND-90',
        'date': SOURCE_DATE,
        'purpose': 'price and interface audit, not a WPT safety or feasibility test',
        'baseline_one_host_for_reader_tag_board_unprogrammed': basic,
        'two_host_digital_telemetry_demonstrator': dual,
        'tag_device_different_from_W89': 'X-NUCLEO-NFC07A1 has ST25DV64KC and 54mm antenna, W89 sampled ST25DV04KC; no power curve transfer',
        'obsolete_board_avoid': 'X-NUCLEO-NFC06A1 obsolete; X-NUCLEO-NFC08A1 manufacturer-active',
        'diotronic_zaragoza_stock': 'NOT_VERIFIED',
        'tme_mouser_price_for_exact_basket': 'PENDING',
        'actual_procurement_authorized': False,
        'battery_BMS_dock': 'DISCONNECTED_AND_OUT_OF_SCOPE',
        'WPT_MOTOR_PUMP': 'NOT_PROPOSED',
        'RF_ESP_NOW_OpenThread': 'DATA_ONLY_NOT_SAFETY_STOP',
        'next_decisive_evidence': 'authorized isolated resistive bench measurement: RF field, V/I EH, cold start, reader input, offset, app ACK, thermal/FOD and independent cutoff',
    }


if __name__ == '__main__':
    print(json.dumps(report(), sort_keys=True, indent=2, ensure_ascii=False))
