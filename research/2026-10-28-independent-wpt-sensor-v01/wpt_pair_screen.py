"""W-IND-05: evidence-gated purchasing/safety screen (not WPT simulation).
Original VALDO W-only Python 3.10+, standard library only. No hardware approval.
Do not use this software for real TX shutdown, FOD, lithium charging or safety.
"""
from __future__ import annotations
from decimal import Decimal, InvalidOperation
import json
import math
from pathlib import Path

MANDATORY_PHYSICAL_GATES = (
    'tx_independent_normally_off_cutoff',
    'tx_foreign_object_detection_shutdown',
    'tx_independent_temperature_cutoff',
    'rx_short_overcurrent_and_brownout',
    'power_rail_under_burst_and_inrush',
    'xy_offset_gap_and_thermal_sweep',
    'metal_water_dust_tests',
    'emi_radio_coexistence',
    'measured_full_link_efficiency',
    'coil_lead_replaceability_and_cycles',
)

class InvalidCatalog(ValueError):
    pass

def _money(raw: str) -> Decimal:
    if not isinstance(raw, str):
        raise InvalidCatalog('monetary amounts must be decimal strings')
    try:
        d = Decimal(raw)
    except InvalidOperation as exc:
        raise InvalidCatalog('bad amount') from exc
    if not d.is_finite() or d < 0 or d.as_tuple().exponent < -2:
        raise InvalidCatalog('negative, nonfinite or subcent amount')
    return d

def load_catalog(path: str | Path) -> dict:
    obj = json.loads(Path(path).read_text(encoding='utf-8'))
    if type(obj) is not dict or obj.get('schema') != 'wpt-pair-v1':
        raise InvalidCatalog('schema missing/unknown')
    if not isinstance(obj.get('candidates'), list) or len(obj['candidates']) < 2:
        raise InvalidCatalog('need two distinct candidates')
    if len({p.get('id') for p in obj['candidates']}) != len(obj['candidates']):
        raise InvalidCatalog('duplicate pair IDs')
    for p in obj['candidates']:
        for key in ('id','vendor','tx_model','rx_model','seller_url','manufacturer_url'):
            if type(p.get(key)) is not str or not p[key].strip():
                raise InvalidCatalog('missing identity: '+key)
        for key in ('output_nominal_v','rx_rating_a','gap_min_mm','gap_max_mm'):
            n=p.get(key)
            if type(n) not in (float,int) or not math.isfinite(n) or n <= 0:
                raise InvalidCatalog('invalid rating: '+key)
        if p['gap_min_mm'] > p['gap_max_mm']:
            raise InvalidCatalog('invalid gap interval')
        quotes=p.get('prices_eur_vat_incl')
        if not isinstance(quotes,list) or not quotes:
            raise InvalidCatalog('missing price quote(s)')
        for v in quotes: _money(v)
        for key in ('tx_fod_physical_verified','tx_thermal_cut_physical_verified',
                    'independent_cut_physical_verified','vendor_pair_compatibility_claimed'):
            if type(p.get(key)) is not bool:
                raise InvalidCatalog('unverified/missing evidence flag: '+key)
        if not isinstance(p.get('limitations'), list) or not p['limitations']:
            raise InvalidCatalog('missing limitations')
    _money(obj['shipping_eur_from'])
    _money(obj['free_shipping_threshold_eur'])
    return obj

def cost_bounds_eur(catalog:dict, candidate:dict, quantity:int=1) -> tuple[Decimal,Decimal]:
    """Price floor only; shipping advertisement not checkout price, no tax/fees elsewhere."""
    if type(quantity) is not int or not 1 <= quantity <= 100:
        raise ValueError('quantity 1..100')
    prices=sorted(_money(x) for x in candidate['prices_eur_vat_incl'])
    ship=_money(catalog['shipping_eur_from'])
    threshold=_money(catalog['free_shipping_threshold_eur'])
    if threshold <= 0:
        raise InvalidCatalog('invalid shipping threshold')
    def bound(p:Decimal)->Decimal:
        subtotal=p*quantity
        return subtotal if subtotal>=threshold else subtotal+ship
    return bound(prices[0]),bound(prices[-1])

def screen_pair(catalog:dict,candidate:dict,*,load_w:float=1.5,required_gap_mm:float=4.0)->dict:
    """NAMEPLATE only: No assertion of power at offset, heat, EMI, voltage or FOD."""
    if type(load_w) not in (float,int) or not math.isfinite(load_w) or load_w<=0:
        raise ValueError('bad load')
    if type(required_gap_mm) not in (float,int) or not math.isfinite(required_gap_mm) or required_gap_mm<=0:
        raise ValueError('bad gap')
    nominal_power=candidate['output_nominal_v']*candidate['rx_rating_a']
    floor,ceil=cost_bounds_eur(catalog,candidate)
    paper_fit=(nominal_power>=load_w and candidate['gap_min_mm']<=required_gap_mm<=candidate['gap_max_mm'] and candidate['vendor_pair_compatibility_claimed'])
    return {
        'id':candidate['id'],
        'paper_fit_at_nominal_only':paper_fit,
        'rated_output_w_not_measured':round(nominal_power,3),
        'rated_power_to_pilot_peak_ratio':round(nominal_power/load_w,3),
        'one_pair_advertised_min_cost_eur_range':[str(floor),str(ceil)],
        'safety_gates_missing':list(MANDATORY_PHYSICAL_GATES),
        'installation_approved':False,
        'physical_bench_approved':False,
        'warn_no_output_voltage_tolerance_guarantee':True,
        'assumed_load_w_not_measured':load_w,
        'assumed_gap_mm_not_measured':required_gap_mm,
    }

def report(path:str | Path, quantity:int=1)->dict:
    c=load_catalog(path)
    screened=[]
    for p in c['candidates']:
        o=screen_pair(c,p)
        o['quantity']=quantity
        o['advertised_minimum_order_bounds_eur']=list(map(str,cost_bounds_eur(c,p,quantity)))
        o['limitations']=p['limitations']
        screened.append(o)
    return {'revision':'W-IND-05','as_of':c['as_of'],
            'domains':{'dock_battery':'deferred; disconnected',
                       'distributed_power':'5V low-power dummy resistive load only, NOT energized',
                       'rf_data':'ESP-NOW/OpenThread independent; no power from RF'},
            'screened':screened,'physical_tests':0,'vendor_price_is_order_quote':False,
            'selection_for_installation':'NONE',
            'disclaimer':'Product advertising and numerical paper fit are NOT thermal/FOD/EMI/independent shutdown proof.'}

if __name__=='__main__':
    print(json.dumps(report(Path(__file__).with_name('WPT_PAIR_CATALOG_W_IND_05.json')),indent=2,ensure_ascii=False))
