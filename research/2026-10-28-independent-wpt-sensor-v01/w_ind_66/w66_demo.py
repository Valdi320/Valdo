"""W66 JSON evidence of synthetic cross trip only; NO physical protection proof."""
import json
from tx_thermal_window import TxInterlock, assumed_channel
good=assumed_channel()
hot=assumed_channel(60)
def case(a,b,fa="normal",fb="normal"):
    g=TxInterlock()
    g.step(good,good,local_request=True,local_reset=True)
    g.step(good,good,local_request=True,local_reset=False)
    r=g.step(a,b,local_request=True,cut_a_fault=fa,cut_b_fault=fb)
    recovery=g.step(good,good,local_request=True)
    return {"fault_energized":r["energized"],
            "latches_both_off":not r["latched_a"] and not r["latched_b"],
            "recovery_without_reset_energized":recovery["energized"],
            "hardware_approved":r["installation_approved"]}
d={"evidence_type":"SYNTHETIC_BOOLEAN_MODEL_ONLY","physical_tests":0,
   "radio_tested":False,"battery_connected":False,"hardware_approved":False,
   "weld_a_hot_a":case(hot,good,"welded_closed"),
   "weld_b_hot_b":case(good,hot,"normal","welded_closed"),
   "double_weld_unresolved":case(hot,good,"welded_closed","welded_closed")}
print(json.dumps(d,sort_keys=True,indent=2))
