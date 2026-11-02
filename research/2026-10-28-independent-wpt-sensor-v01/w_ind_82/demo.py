"""Deterministic, synthetic brownout and ACK-loss scenario; no physical radio."""
import json
from w82_lease import Receiver, Sensor, FRAME_BYTES

KEY = b"SYNTHETIC-NOT-A-DEPLOYMENT-KEY".ljust(32, b"_")
r = Receiver(7, KEY, encrypted_unicast=True, lease_ms=250)
s = Sensor(7, KEY, b"A" * 16)
events = []

def record(event, time_ms):
    events.append({"event": event, "t_ms": time_ms, "valid": r.poll(time_ms)})

hello = s.hello(r.begin(0, b"a" * 16))
record(r.receive(hello, 1).event, 1)
data = s.send(1234, 2)
record(r.receive(data, 2).event, 2)
# Drop first application ACK; radio's MAC status is not an application ACK.
assert s.pending is not None
replay = s.retry(62)
assert replay == data
received = r.receive(replay, 62)
assert s.ack(received.ack)
record(received.event, 62)
record("LEASE_EXPIRED", 253)
s.reboot(b"B" * 16)
record(r.receive(data, 253).event, 253)
hello2 = s.hello(r.begin(254, b"b" * 16))
record(r.receive(hello2, 255).event, 255)
record(r.receive(s.send(777, 256), 256).event, 256)
print(json.dumps({"model": "W-IND-82", "evidence": "synthetic-python-only", "hardware_approved": False,
                  "packet_bytes": FRAME_BYTES, "events": events}, indent=2, sort_keys=True))
