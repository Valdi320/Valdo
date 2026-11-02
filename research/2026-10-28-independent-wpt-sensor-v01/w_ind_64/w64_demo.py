"""Deterministic, synthetic, no hardware. No secret in output."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from w_ind_64.w64_aead import AeadCodec,EncryptedSender,EncryptedReceiver,WIRE_LEN
secret=bytes(range(1,33));epoch=bytes(range(101,117))
codec=AeadCodec(secret,epoch,7,123)
tx=EncryptedSender(codec);rx=EncryptedReceiver(codec)
wire=tx.start(77,0);ack=rx.receive(wire,1)
retry=tx.retry(60);duplicate_ack=rx.receive(retry,60)
tampered=bytearray(duplicate_ack);tampered[-1]^=1
print(json.dumps({
 "hito":"W-IND-64","evidence_type":"SYNTHETIC_AESGCM_SOFTWARE_ONLY",
 "wire_bytes":WIRE_LEN,"previous_hmac_wire_bytes":38,
 "plaintext_frame_visible":False,
 "retry_byte_identical":retry==wire,
 "duplicate_ack_byte_identical":ack==duplicate_ack,
 "duplicate_does_not_refresh_freshness":rx.rx.last_ms==1,
 "tampered_ack_rejected":not tx.accept_ack(bytes(tampered),61),
 "valid_ack_accepted":tx.accept_ack(duplicate_ack,62),
 "physical_radio_test":False,"secure_epoch_or_key_storage_proven":False,
 "real_antirollback_anchor_proven":False,
 "battery_or_BMS_connected":False,"hardware_approved":False
},sort_keys=True,indent=2))
