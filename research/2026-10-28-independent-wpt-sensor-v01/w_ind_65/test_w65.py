"""W65 synthetic policy tests, no radio or battery."""
import json
import unittest
from dataclasses import asdict, replace
from w_ind_65.w65_rf_policy import RFProfile, assess, app_byte_budget
from w_ind_65.w65_rf_policy import RAW_FRAME_BYTES, W64_AESGCM_BYTES

def esp(mode="native_ccmp"):
    return RFProfile(1,"esp_now",mode,"sensor_telemetry",True,True,16,True,
                     mode=="dual_aead",True,True,True,240,2,True,False,
                     False,250,"SYNTHETIC_CONFIGURATION_ONLY")

def ot():
    return RFProfile(1,"openthread","app_aead","sensor_telemetry",True,True,
                     0,False,True,True,True,True,240,2,True,False,
                     False,0,"SYNTHETIC_CONFIGURATION_ONLY")

class PolicyTests(unittest.TestCase):
    def test_contract_lengths_in_real_prior_modules(self):
        # This MUST run on CI against real committed modules, no skip.
        from w_link import FRAME_LEN
        from w_ind_64.w64_aead import WIRE_LEN
        self.assertEqual((FRAME_LEN,WIRE_LEN),(RAW_FRAME_BYTES,W64_AESGCM_BYTES))

    def test_ccmp_unicast_digital_only(self):
        v=assess(esp())
        self.assertTrue(v.bench_candidate)
        self.assertFalse(v.production_approved)
        self.assertEqual(v.frame_bytes,22)

    def test_dual_aead_digital_only(self):
        v=assess(esp("dual_aead"))
        self.assertTrue(v.bench_candidate)
        self.assertEqual(v.frame_bytes,54)
        self.assertIn("antirollback"," ".join(v.notes))

    def test_openthread_app_aead_digital_only(self):
        v=assess(ot())
        self.assertTrue(v.bench_candidate)
        self.assertFalse(v.production_approved)

    def test_roundtrip_canonical_json(self):
        p=esp()
        self.assertEqual(RFProfile.from_mapping(json.loads(json.dumps(asdict(p)))),p)

    def test_no_missing_or_unknown_fields(self):
        d=asdict(esp())
        d.pop("peer_unicast")
        with self.assertRaises(ValueError): RFProfile.from_mapping(d)
        d=asdict(esp())
        d["permit_motors"]=True
        with self.assertRaises(ValueError): RFProfile.from_mapping(d)

    def test_no_bool_to_int_or_text_to_bool_coercion(self):
        for key,value in (("custom_pmk","false"),("expiry_ms",True),
                          ("max_retries",2.0),("peer_bound",1)):
            d=asdict(esp());d[key]=value
            with self.subTest(key=key):
                with self.assertRaises(ValueError): RFProfile.from_mapping(d)

    def test_direct_dataclass_cannot_bypass_schema(self):
        for key,value in (("peer_bound","false"),("expiry_ms",True),
                          ("custom_pmk","true")):
            with self.subTest(key=key):
                v=assess(replace(esp(),**{key:value}))
                self.assertFalse(v.bench_candidate)
                self.assertFalse(v.production_approved)

    def test_never_approve_production_even_if_epoch_claims_qualified(self):
        for p in (esp(),esp("dual_aead"),ot()):
            v=assess(replace(p,persistent_epoch_anchor_qualified=True))
            self.assertFalse(v.production_approved)

    def test_no_critical_roles(self):
        for role in ("motor","pump","dock","safety_cutoff",""):
            self.assertFalse(assess(replace(esp(),role=role)).bench_candidate)

    def test_no_rf_control_of_safety(self):
        self.assertFalse(assess(replace(esp(),cutoff_independent_of_rf=False)).bench_candidate)

    def test_no_broadcast_even_with_all_crypto_claims(self):
        for p in (esp(),esp("dual_aead"),ot()):
            self.assertFalse(assess(replace(p,peer_unicast=False)).bench_candidate)

    def test_no_unbound_peer(self):
        self.assertFalse(assess(replace(esp(),peer_bound=False)).bench_candidate)

    def test_esp_lmk_exact_16(self):
        for keysize in (0,15,17,32):
            self.assertFalse(assess(replace(esp(),peer_lmk_bytes=keysize)).bench_candidate)

    def test_esp_default_pmk_rejected(self):
        self.assertFalse(assess(replace(esp(),custom_pmk=False)).bench_candidate)

    def test_no_mac_callback_as_app_ack(self):
        self.assertFalse(assess(replace(esp(),mac_callback_as_app_ack=True)).bench_candidate)

    def test_ack_crc_and_sequence_required(self):
        for f in ("application_ack","crc16","sequence_numbers"):
            self.assertFalse(assess(replace(esp(),**{f:False})).bench_candidate)

    def test_timeout_and_retry_bounded(self):
        for expiry in (-1,0,251,1000):
            self.assertFalse(assess(replace(esp(),expiry_ms=expiry)).bench_candidate)
        for retries in (-1,3,10):
            self.assertFalse(assess(replace(esp(),max_retries=retries)).bench_candidate)

    def test_ccmp_requires_no_app_aead_flag(self):
        self.assertFalse(assess(replace(esp(),application_aead=True)).bench_candidate)

    def test_dual_requires_app_aead(self):
        self.assertFalse(assess(replace(esp("dual_aead"),application_aead=False)).bench_candidate)

    def test_esp_only_ccmp_based_modes(self):
        self.assertFalse(assess(replace(esp(),privacy="app_aead")).bench_candidate)

    def test_thread_requires_app_aead_not_link_only(self):
        self.assertFalse(assess(replace(ot(),application_aead=False)).bench_candidate)
        self.assertFalse(assess(replace(ot(),privacy="native_ccmp")).bench_candidate)

    def test_thread_no_esp_keys_or_fake_mtu(self):
        self.assertFalse(assess(replace(ot(),peer_lmk_bytes=16)).bench_candidate)
        self.assertFalse(assess(replace(ot(),custom_pmk=True)).bench_candidate)
        self.assertFalse(assess(replace(ot(),app_payload_limit_bytes=250)).bench_candidate)

    def test_no_esp_v2_mtu_masquerade(self):
        for mtu in (0,22,1470):
            self.assertFalse(assess(replace(esp(),app_payload_limit_bytes=mtu)).bench_candidate)

    def test_no_false_evidence_or_protocol(self):
        self.assertFalse(assess(replace(esp(),evidence_type="RF_MEASURED")).bench_candidate)
        self.assertFalse(assess(replace(esp(),version=99)).bench_candidate)
        self.assertFalse(assess(replace(esp(),transport="bluetooth")).bench_candidate)
        self.assertFalse(assess(replace(esp(),privacy="cleartext")).bench_candidate)

    def test_enumeration_512_has_exactly_one_reference_candidate(self):
        names=("peer_unicast","peer_bound","custom_pmk","application_ack",
               "crc16","sequence_numbers","cutoff_independent_of_rf",
               "mac_callback_as_app_ack","application_aead")
        good=0
        for bits in range(1<<len(names)):
            v=assess(replace(esp(),**{name:bool((bits>>i)&1) for i,name in enumerate(names)}))
            good+=v.bench_candidate
            self.assertFalse(v.production_approved)
        self.assertEqual(good,1)

    def test_byte_budget_not_rf_energy(self):
        x=app_byte_budget(22);y=app_byte_budget(54)
        self.assertEqual((x["data_plus_ack_bytes_nominal"],y["data_plus_ack_bytes_nominal"]),(44,108))
        self.assertEqual((x["scenario_max_payload_bytes"],y["scenario_max_payload_bytes"]),(132,324))

    def test_byte_budget_invalid(self):
        for kw in ({"frame_bytes":38},{"frame_bytes":22,"data_attempts":4},
                   {"frame_bytes":54,"ack_emissions":4},{"frame_bytes":True}):
            with self.assertRaises(ValueError):app_byte_budget(**kw)

    def test_wrong_object_rejected(self):
        with self.assertRaises(ValueError):assess(asdict(esp()))

if __name__=="__main__":unittest.main()
