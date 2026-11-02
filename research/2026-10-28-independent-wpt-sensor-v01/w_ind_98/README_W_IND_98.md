# W-IND-98 — Monotonic clock at the PUBLIC telemetry freshness boundary

**1 November 2026 · OWN VALDO W · experimental Python 3, non-safety telemetry.** This isolated, source-and-test improvement applies to a NEW open robot; **no Xiaomi OEM transplant**, no OOMWOO changes, and no physical energization.

## Reproducible defect and patch
W97 protected local recommission and `receive/tick` against a clock rollback, but the public `ModuleReceiver.fresh()` method previously compared its argument only to `last_ms`, not `last_clock_ms`. Counterexample with authenticated_transport=True as a **TEST STUB** (not cryptography): commission session 123 at 0 ms, receive sample at 10 ms, call `fresh(200)`, then call `fresh(20)`. **Old** method returned `True` for both: a backdated read appeared current after a newer observation. It did not latch a clock fault. The same bypass occurred after `tick(200)`.

**Patch:** for exact integer timestamps, `fresh` now visits the same monotonic `_clock` gate as `receive` and `tick`. Any rollback latches the receiver fault; equal or increasing time remains allowed. Noninteger inputs still yield False without altering receiver state, preserving W95's prior adversarial-test contract. A fault requires a higher locally commissioned epoch and monotonic time; across a real reboot, durable provisioning/crypto remain external obligations. No change to packet bits (22 bytes, CRC16), application ACK policy, expiry, retries, or power interlocks. Public freshness state is **diagnostic only**, never a motor-stop, FOD, charger or electrical-cut controller.

## Reproduction / test
From `research/2026-10-28-independent-wpt-sensor-v01`:
```sh
python3 -B -m unittest -v test_w_link.TestFreshnessMonotonicW98
python3 -B -m unittest -v test_w_link test_power_restart_gate
```
Nine deterministic adversarial methods cover direct query rollback, prior tick/receive, stale-data resurrection, invalid values, negative time, epoch recovery, equal timestamps and unchanged duplicate ACK. The existing `.github/workflows/wpt-sensor-v01.yml` already includes `test_w_link` in the PR/push general suite. GitHub CI run and exact SHA are the public validation; no invented physical measurements. Before the patch, the two-query counterexample is TRUE/TRUE; afterwards TRUE/FALSE and fault latched.

## Three separate interfaces and design decision
| Problem | Current baseline | Candidate | Approval gates |
| --- | --- | --- | --- |
| Dock charging | Removable wired mechanical contacts as reference | **Regulated** inductive station only as separate study | Li-ion charger+BMS separate; FOD, thermal, humidity, XY/angle offset, EMI, independent power cut, efficiency and battery safety all UNTESTED |
| Power to low-consumption detachable module | Serviceable cable | 0.3 W **hypothetical** first sensor, regulated WPT; simple open-loop coil REJECTED | Measure net sensor+RX+TX input, startup, loss, temperature, offset, interference, cutoff, service cost; cable not removed |
| Telemetry/data | Locally wired fallback | ESP-NOW **or** OpenThread; WISP only if ultra-low-power RFID budget justifies reader | Real encrypted/authenticated link, per-application ACK+CRC+sequence+timeout+privacy+recovery, supply measured independently |

Never use radio for safety-critical physical stops; motors, pumps and vacuum turbina stay wired until real peak/continuous requirements and WPT losses are demonstrated. Comparing app ACK logic is NOT a radio or energy measurement. Normal-off protections are unqualified.

## Sources & ownership audit (GitHub HEAD vs 28 Oct pinned SHA, checked 1 Nov 2026)
| Project, copyright/licensing | Branch HEAD checked | Pin difference / meaning |
| --- | --- | --- |
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) (GPL-3.0), author mark-belbin | master `7c7858c0dd7040801b6f191df1396115560218f0` | identical; open-loop transmitter demo not a protected regulated design |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) (BSD-2-Clause), author wisp | master `08332bc398aa3350d351ef2aaac163f8007cffda` | identical; RFID microsensor only |
| [wisp/wisp5](https://github.com/wisp/wisp5) (BSD-2-Clause), author wisp | **640kHz** `604eee2dffaeba3a270de61cf3dae887a33309c2` | vs `d978a6978ad23ccd6c44dd55430973b04a3d4a9b`: diverged +68/-11; [PR #40](https://github.com/wisp/wisp5/pull/40) is from separate 436kHz branch, not evidence 640kHz is newer by name |
| [espressif/esp-now](https://github.com/espressif/esp-now) (Apache-2.0), author Espressif | master `c3b5f9be245f1a80db9cb938600566aa6a8dd1e5` | identical; MAC send callback != APP ACK, see [Espressif documentation](https://docs.espressif.com/projects/esp-idf/en/v5.5/esp32/api-reference/network/esp_now.html) |
| [openthread/openthread](https://github.com/openthread/openthread) (BSD-3-Clause), author OpenThread | main `c6872259f4194fb76c7d333bda209343e8c88e71` | vs `7009584dadc20cf20c20a6062f357dd572ba6885`: +21 commits, include radio/link API and CI; [PR #13800](https://github.com/openthread/openthread/pull/13800) closed Oct 31; do not extrapolate efficiency |
| [makerspet/oomwoo](https://github.com/makerspet/oomwoo) (Apache-2.0) | main `f01a1b295f462da5ab8d5f021a3f741cbd2b47df` | reference only; own W does not alter official repos or cleaning-jobs PR #79 |

All code in this W98 is original VALDO work. No borrowed GPL, BSD, Apache code, CAD or firmware. References: local 28 Oct NO-TRASPLANTE decision, `19-alternativas-abiertas...`, D22 W/C contract, `VALDO_OOMWOO/LEEME_PRIMERO.md` and `WPT_DATOS_V01.md`. A separate dirty mechanical/Codex checkout was **not touched**; sole running related automation is W, and OOMWOO automation is paused.

## Limits and purchasing
**Synthetic CPU-only**, 0 physical sensor, 0 RF or NFC link, 0 proven autonomous FOD/temperature/offset/EMI/electrical isolation, 0 lithium charge/dock, 0 purchases or prints. Current **W18 electrical ERC has 3 known violations** (one dangling label, two undriven power pins) and remains a deliberate build-blocker. `authenticated_transport=True` is a simulated caller assertion, **not an identity proof**. Future bench must use a resistive load, isolated supply and independent review/authorization.

Incremental component BOM: **€0**, not including labor. Diotronic remains **auxiliary**, never default; neither local availability, MOQ nor IVA-inclusive price is verified. Specialized suppliers (TME/Mouser/DigiKey/manufacturer) are required where safety-critical traceability warrants. See BOM_W_IND_98.csv and MATRIZ_W_IND_98.csv. **Next material gate:** measured RF receiver/reader and load energy with autonomous cutoff, *only with formal permission*, no battery/BMS/dock.
