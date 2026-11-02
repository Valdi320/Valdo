"""W64 adversarial digital-only tests. No physical radio or battery."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from w_link import DATA, ACK, Frame
from w_ind_64.w64_aead import AeadCodec, EncryptedSender, EncryptedReceiver, WIRE_LEN, NONCE_LEN

SECRET=bytes(range(1,33))    # TEST VECTOR ONLY, not provisionable
EPOCH=bytes(range(101,117))   # TEST VECTOR ONLY, not random

def new(secret=SECRET,epoch=EPOCH,node=7,session=123):
    return AeadCodec(secret,epoch,node,session)

def data(seq=1,value=531):
    return Frame(DATA,7,123,seq,value_milli=value).encode()

def ack(seq=1):
    return Frame(ACK,7,123,seq,ack_seq=seq).encode()

class CryptographyTests(unittest.TestCase):
    def test_nist_aes_gcm_known_vector(self):
        # NIST SP 800-38D: 128-bit zero key, zero IV, empty plaintext/AAD.
        self.assertEqual(AESGCM(b'\x00'*16).encrypt(b'\x00'*12,b'',b'').hex(),
                         '58e2fccefa7e3061367f1d57a4e7455a')

    def test_dimensions_and_roundtrip(self):
        c=new(); encrypted=c.seal(data(),DATA)
        self.assertEqual((WIRE_LEN,NONCE_LEN,len(encrypted)),(54,12,54))
        self.assertEqual(c.open(encrypted,DATA),data())

    def test_plaintext_hidden_from_wire(self):
        encrypted=new().seal(data(value=593),DATA)
        self.assertNotIn(data(value=593),encrypted)
        self.assertNotEqual(encrypted[:22],data(value=593))

    def test_ack_roundtrip(self):
        c=new(); self.assertEqual(c.open(c.seal(ack(),ACK),ACK),ack())

    def test_repeated_seq_and_identical_plaintext_returns_identical_wire(self):
        c=new(); a=c.seal(data(),DATA)
        self.assertEqual(c.seal(data(),DATA),a)

    def test_new_payload_same_seq_blocks_session(self):
        c=new();c.seal(data(),DATA)
        with self.assertRaises(ValueError):c.seal(data(value=700),DATA)
        with self.assertRaises(ValueError):c.seal(data(seq=2),DATA)

    def test_old_seq_after_newer_blocks_session(self):
        c=new();c.seal(data(seq=1),DATA);c.seal(data(seq=2),DATA)
        with self.assertRaises(ValueError):c.seal(data(seq=1),DATA)
        with self.assertRaises(ValueError):c.seal(data(seq=3),DATA)

    def test_monotonic_seq_both_directions_independent(self):
        c=new()
        self.assertEqual(c.open(c.seal(data(seq=1),DATA),DATA),data(seq=1))
        self.assertEqual(c.open(c.seal(ack(seq=1),ACK),ACK),ack(seq=1))
        self.assertEqual(c.open(c.seal(data(seq=2),DATA),DATA),data(seq=2))
        self.assertEqual(c.open(c.seal(ack(seq=2),ACK),ACK),ack(seq=2))
        self.assertNotEqual(c._nonce(ACK,1),c._nonce(DATA,1))

    def test_nonce_sequence_derived_deterministically(self):
        c=new(); w=c.seal(data(seq=123),DATA)
        self.assertEqual(len(w[4:16]),12)
        self.assertEqual(w[4:16][-4:],(123).to_bytes(4,'big'))

    def test_ciphertext_or_tag_bit_flip_rejected(self):
        c=new();pkt=c.seal(data(),DATA)
        for offset in (16,20,35,53):
            p=bytearray(pkt);p[offset]^=1
            with self.subTest(offset=offset):self.assertIsNone(c.open(bytes(p),DATA))

    def test_header_version_flip_rejected(self):
        c=new();p=bytearray(c.seal(data(),DATA));p[2]^=1
        self.assertIsNone(c.open(bytes(p),DATA))

    def test_direction_reflection_rejected(self):
        c=new();self.assertIsNone(c.open(c.seal(data(),DATA),ACK))

    def test_no_peer_cross_key(self):
        pkt=new().seal(data(),DATA)
        self.assertIsNone(new(secret=bytes(range(33,65))).open(pkt,DATA))
        self.assertIsNone(new(epoch=bytes(range(1,17))).open(pkt,DATA))
        self.assertIsNone(new(node=8).open(pkt,DATA))
        self.assertIsNone(new(session=124).open(pkt,DATA))

    def test_nonce_tampering_rejected(self):
        c=new();w=bytearray(c.seal(data(),DATA));w[8]^=1
        self.assertIsNone(c.open(bytes(w),DATA))

    def test_wrong_frame_kind_will_not_encrypt(self):
        with self.assertRaises(ValueError):new().seal(data(),ACK)

    def test_wrong_wire_type_length_rejected(self):
        c=new();w=c.seal(data(),DATA)
        for v in (None,bytearray(w),w[:-1],w+b'\x00',b'',b'0'*54):
            with self.subTest(value=type(v).__name__):self.assertIsNone(c.open(v,DATA))
        self.assertIsNone(c.open(w,True))

    def test_wrong_constructor_inputs(self):
        for bad in (b'',b'\x00'*32,b'x'*31,bytearray(SECRET)):
            with self.assertRaises(ValueError):new(secret=bad)
        for bad in (b'',b'\x00'*16,b'1'*15,bytearray(EPOCH)):
            with self.assertRaises(ValueError):new(epoch=bad)
        for node,session in ((True,123),(-1,123),(65536,123),(7,0),(7,True),(7,2**32)):
            with self.assertRaises(ValueError):new(node=node,session=session)

    def test_same_key_epoch_recreation_danger_visible(self):
        # This is WHY W62+W63 trusted storage is required; no deployed claim.
        a,b=new(),new()
        self.assertEqual(a.seal(data(),DATA),b.seal(data(),DATA))

    def test_seq_exhaustion_protection_at_tracker(self):
        c=new(); tx=EncryptedSender(c);tx.tx.next_seq=0x100000000
        with self.assertRaises(ValueError):tx.start(1,0)

class ApplicationIntegrationTests(unittest.TestCase):
    def test_send_receive_and_authenticated_ack(self):
        c=new();tx=EncryptedSender(c);rx=EncryptedReceiver(c)
        wire=tx.start(55,0); a=rx.receive(wire,1)
        self.assertIsNotNone(a); self.assertTrue(tx.accept_ack(a,2))
        self.assertEqual(tx.tx.acked,1);self.assertEqual(rx.rx.last_seq,1)

    def test_replayed_ack_or_fake_ack_rejected(self):
        c=new();tx=EncryptedSender(c);rx=EncryptedReceiver(c)
        wire=tx.start(55,0)
        self.assertFalse(tx.accept_ack(b'\x00'*54,1))
        ackwire=rx.receive(wire,1);self.assertTrue(tx.accept_ack(ackwire,2))
        self.assertFalse(tx.accept_ack(ackwire,3))

    def test_lost_ack_retry_keeps_same_ciphertext_and_no_freshness_extension(self):
        c=new();tx=EncryptedSender(c);rx=EncryptedReceiver(c)
        first=tx.start(55,0); ack_first=rx.receive(first,1)
        repeat=tx.retry(60);self.assertEqual(repeat,first)
        ack_repeat=rx.receive(repeat,60)
        self.assertEqual(ack_repeat,ack_first)
        self.assertTrue(tx.accept_ack(ack_repeat,61))
        self.assertEqual(rx.rx.last_ms,1)

    def test_max_duplicate_acks_not_unbounded(self):
        c=new();tx=EncryptedSender(c);rx=EncryptedReceiver(c)
        pkt=tx.start(55,0);self.assertIsNotNone(rx.receive(pkt,1))
        self.assertIsNotNone(rx.receive(pkt,60))
        self.assertIsNotNone(rx.receive(pkt,120))
        self.assertIsNone(rx.receive(pkt,180))
        self.assertEqual(rx.rx.last_ms,1)

    def test_invalid_packet_does_not_refresh_timeout(self):
        c=new();tx=EncryptedSender(c);rx=EncryptedReceiver(c)
        pkt=tx.start(55,0);rx.receive(pkt,1)
        self.assertIsNone(rx.receive(b'?'*54,200))
        self.assertEqual(rx.rx.last_ms,1)
        self.assertFalse(rx.tick(252))
        self.assertTrue(rx.rx.latched_fault)
        self.assertIsNone(rx.receive(pkt,253))

    def test_old_epoch_cannot_decrypt_after_new_commission(self):
        old=EncryptedSender(new()).start(55,0)
        rx=EncryptedReceiver(new(epoch=bytes(range(1,17))))
        self.assertIsNone(rx.receive(old,1))
        self.assertEqual(rx.rx.last_seq,0)

    def test_authenticated_packet_not_safety_authority(self):
        c=new();tx=EncryptedSender(c);rx=EncryptedReceiver(c)
        a=rx.receive(tx.start(999,0),1)
        self.assertIsNotNone(a)
        self.assertFalse(rx.rx.latched_fault)
        self.assertFalse(rx.tick(260))
        self.assertTrue(rx.rx.latched_fault)

if __name__ == '__main__':unittest.main()
