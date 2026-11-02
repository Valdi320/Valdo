"""Deterministic W65 evidence, strictly synthetic (no connected radio)."""
import json
from dataclasses import replace
from w_ind_65.test_w65 import esp,ot
from w_ind_65.w65_rf_policy import assess,app_byte_budget

def main():
    cases = {
        "esp_now_native_ccmp":esp(),
        "esp_now_native_plus_app_aead":esp("dual_aead"),
        "openthread_application_aead":ot(),
        "esp_now_no_lmk":replace(esp(),peer_lmk_bytes=0),
        "esp_now_default_pmk":replace(esp(),custom_pmk=False),
        "esp_now_broadcast":replace(esp(),peer_unicast=False),
        "esp_now_mac_ack_is_app_ack":replace(esp(),mac_callback_as_app_ack=True),
        "openthread_link_only":replace(ot(),application_aead=False),
        "radio_controls_critical_cut":replace(esp(),cutoff_independent_of_rf=False),
    }
    out={
        "evidence_type":"SYNTHETIC_RF_POLICY_ONLY",
        "hardware_approved":False,
        "physical_radio_measured":False,
        "battery_or_BMS_connected":False,
        "profiles":{n:assess(p).as_dict() for n,p in cases.items()},
        "application_payload_bytes":{
            "native_ccmp":app_byte_budget(22),
            "app_aead_or_dual":app_byte_budget(54)},
        "comparison_limit":"Application bytes only: no MAC/CCMP overhead, airtime or energy claim",
        "pending":["actual RF peer/key provision verification",
                   "on-air packet loss/latency and consumption",
                   "persistent antirollback anchor",
                   "physical independent power cutoff and FOD/temperature/EMI"]}
    print(json.dumps(out,sort_keys=True,indent=2))
if __name__=="__main__":main()
