# W-IND-99 — Sender ACK lease cannot rewind across successive telemetry frames

**2026-11-01 · VALDO own W branch, new independent robot.** Experimental host-only Python, no hardware operation. No Xiaomi OEM electronics, firmware, BMS or dock; no changes to makerspet/oomwoo or cleaning-jobs PR #79.

## Reproduced defect and fix
The W98 receiver checks monotonic clocks, but `AckTracker` tracked the current packet's start/last time without remembering the latest timestamp **across** completed packets and failed authentication/CRC ACKs. Two synthetic counterexamples:
1. `start(55,100)`, valid app ACK at 200, then `start(66,10)` previously succeeded, creating a new ACK/retry lease using a reversed clock.
2. `start(55,0)`, malformed or unauthenticated ACK observed at 150, then `retry(60)` previously emitted the old frame, even though a later local clock observation had happened.

A single monotonic sender checkpoint now covers `start`, `retry` and `accept_ack`. Failed CRC/unauthenticated ACKs **observe the caller's local time** without crediting an ACK. A rollback on pending retry/ACK fails closed by expiring that pending frame. An attempted rollback on `start` raises `ValueError` before consuming a sequence number. Equal timestamps and forward recovery are allowed. No packet layout, CRC16, session, ACK policy or timeout duration changed. Sender does **not** provide a safety-graded latch: a new forward timestamp may start another diagnostic frame; a system monotonic clock that wraps or resets needs an explicit independent reboot/session policy.

## Reproduction and evidence
From `research/2026-10-28-independent-wpt-sensor-v01`:
```sh
python3 -B -m unittest -v test_w_link.TestSenderMonotonicClockW99
python3 -B -m unittest -v test_w_link
```
The existing WPT Python GitHub Actions job executes `test_w_link` and its historical regression suite on push and PR. Ten new deterministic test methods cover both counterexamples, auth/CRC failures, retries, equal/invalid clock inputs, rejected payloads, sequence preservation and forward ACK recovery. **This document does not claim a physical/RF test**; GitHub run results are the authoritative evidence after publication.

## Three independent functions
| Interface | Baseline | Candidate | Decision / remaining gate |
|---|---|---|---|
| Dock charging | Serviceable contact dock | Regulated WPT station | **NOT APPROVED:** battery/BMS isolated, autonomous thermal/FOD/cutoff, moisture, offset, EMI and efficiency unmeasured |
| Low-power detachable sensor | Serviceable wiring | Regulated WPT to hypothetical 0.3 W test load | **TEST ONLY:** measure output/input energy including startup, standby, no USB backfeed, thermal, offset; simple open-loop WPT cannot be adopted |
| Telemetry | Wired reference | ESP-NOW **or** OpenThread | 22-byte frame, CRC, app ACK, seq/timeout and session; real RF authentication/encryption, retries, power and recovery **UNTESTED** |

WISP5 is only a conceptual reference for RFID microsensors with measured power budgets; it is not a motor/pump supply. Radio never gates physical emergency stop or charger TX cutoff. External autonomous safety cut, FOD and temperature are required before any WPT bench authorization. KiCad W18 ERC retains three historical violations and therefore blocks energization.

## External sources, owners and current branch comparisons (verified 2026-11-01)
| Upstream creator/repo (license) | Author branch HEAD; SHA pinned 2026-10-28 | Relevant recent changes / disposition |
|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) GPL-3.0 | master `7c7858c0`; pin identical | PR #1 merged 2021; unregulated proof of concept, not a qualified FOD/cutoff solution |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) BSD-2-Clause | master `08332bc3`; identical | PR #1 2015; external RFID reader and ultra-low duty cycle, not WPT for continuous loads |
| [wisp/wisp5](https://github.com/wisp/wisp5) BSD-2-Clause | **640kHz** `604eee2d` vs `d978a697`, compare **diverged +68/-11** | CCS11 support in 2022 HEAD; PR #40 still open, separate 436kHz lineage—never rank branches by name |
| [espressif/esp-now](https://github.com/espressif/esp-now) Apache-2.0 | master `c3b5f9be`; identical | PR #153 closed 2026; vendor explicitly states MAC send-success != app receipt: application ACK required |
| [openthread/openthread](https://github.com/openthread/openthread) BSD-3-Clause | main `c6872259` vs `7009584d`, **ahead 21** | latest link-request/neighbour/radio changes Oct 31, 2026; release v2026.11.0 Nov 1; no assumption on energy savings |
| [makerspet/oomwoo](https://github.com/makerspet/oomwoo) Apache-2.0 | main `f01a1b29` Oct 29 | PR #79 cleaning-jobs remains open/independent; reference only |

Source contracts: master decision 28 October no transplant, 19-alternativas, D22, mechanical/W ownership agreement, `VALDO_OOMWOO/LEEME_PRIMERO.md`, `WPT_DATOS_V01.md`; third-party licenses and attribution retained without incorporating external code. This change is 100% original local W code, not a PR into external upstream.

## Supply, limits and next gate
No BOM changes or purchases: €0 incremental physical parts, excluding engineering time. Diotronic is auxiliary only, stock and VAT prices **unverified**; critical WPT/FOD/cutoff parts require traceability through TME, Mouser, DigiKey or manufacturer and safety review. See BOM and decision matrix alongside this document.

**Evidence grade:** digital logic/code only; not a radio, EMI, thermography, FOD, Li-ion or power-delivery test. Next meaningful step remains isolated, authorized **resistive** low-power bench with power+loss measurements and independent electrical safety gate. Until then retain serviceable wired fallback.
