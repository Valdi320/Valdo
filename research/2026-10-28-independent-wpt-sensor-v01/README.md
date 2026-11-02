# VALDO W-IND-01 — independent robot: sensor-power and telemetry bench specification (2026-10-28)

**Scope: NEW independent open robot, not Xiaomi X20 Pro or its charger, firmware or battery.** This is one original, experimental software design with a hypothetical electrical sizing model. No lithium charging, coils, PCBs, motor operation or real RF tests have been performed. Hardware power cutoff, foreign-object detection (FOD), thermal safety and cryptographic peer authentication are **not implemented**.

## One measurable first pilot

A removable, NON-SAFETY-CRITICAL sensor module powered inductively from a fixed low-voltage host interface, while its sensor telemetry uses separately authenticated radio:

| Dimension | INITIAL TEST TARGET; NOT a measurement |
|---|---|
| Sensor rail | regulated 5 V; preliminary 80 mA mean (0.40 W), 300 mA peak (1.50 W) |
| Radio | encrypted unicast ESP-NOW if choosing compatible ESP32 nodes; alternative OpenThread with genuine 802.15.4 radios |
| Frame | fixed 22-byte network-order frame with CRC-16/CCITT-FALSE |
| Message validity | explicit application ACK, monotonically increasing sequence, nonzero locally commissioned session, nonzero node ID |
| Retry | at most 3 sends, retry each 60 ms, expiry after 240 ms |
| Link freshness | 250 ms from last accepted data, local-monotonic clock, expired/rollback state **latched** until local recommission |
| Emergency stop/charger cutoff | wholly independent HARDWARE paths, never remotely authorized by the radio |
| Pilot fixture | only isolated low-voltage bench with resistive dummy load and verified current/temperature limits when independently authorized; **not performed** |

**Three physically separate problems:** (1) station charging of batteries, explicitly postponed; (2) optional induction for a sub-1.5-W removable sensor, evaluated here; (3) radio for data, never power. No default WPT for motors, pump, vacuum fan or safety sensors. A robust cable with a service connector may remain cheaper and safer; the trade-off is not prejudged.

## Reproduce the verified experiment

Python 3.10+ standard library only. From this directory:

```sh
python3 -m unittest -v test_w_link
python3 -m py_compile w_link.py power_screen.py test_w_link.py
```

The original sandbox run passed **27/27 deterministic tests** (framing, independent application ACK, wrong session, replay, 176 single-bit flips + 1000 seeded single-bit faults, missing radio ACK, stale ACK, bounded retries, timeout latch, rollback and power budget). Tests on a Linux PC, not on ESP32 silicon or OOMWOO. CRC detects accidents; **CRC is NOT authentication**. In `w_link.py`, `authenticated_transport=True` represents an **external test assumption**; real deployment needs verified paired keys, encrypt+authenticate at radio stack, replay rules, independent local re-commissioning and privacy testing.

## Simplified power model — hypothetical, not a coil simulation

The separate `power_screen.py` screening model assumes `Pout=V*I`, `eta_effective=nominal_eta*offset_factor` and `Pin=Pout/eta_effective`. At 5 V × 300 mA and **ASSUMED** 75% total efficiency, 2.0 W source and 0.5 W loss; at a made-up 0.5 offset multiplier, source 4.0 W and loss 2.5 W. These assumptions **cannot predict temperature or metallic FOD**, coil alignment or EMI and must not be attributed to third-party devices. Hold-up capacitor estimate ignores ESR, capacitance derating and regulator efficiency.

Physical acceptance blockers: real module draw and burst current, actual TX/RX coupled characteristics at several gaps and XY offsets, heating including metallic objects/water/dirt, near-field EMI, TX/RX rail fault injection, independent normally-OFF output cut and thermal comparator, current limit and FOD shutdown **independent of firmware or radio**, restart failures and prolonged repair-cycle checks. A welded dual switch remains a hazard until hardware fault analysis and destructive-safe tests. No Li-ion/BMS/dock connections in phase one.

## Technology selection / license provenance

| External creator | Checked default HEAD on 2026-10-28 | Contribution to understanding; **not imported** |
|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) GPL-3.0 | `master 7c7858c0dd7040801b6f191df1396115560218f0` | 100-kHz open-loop induction demonstration; author's quoted 81.3% at ~1–2mm NOT our efficiency, and no independent closed-loop FOD authorization |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) BSD-2-Clause | `master 08332bc398aa3350d351ef2aaac163f8007cffda` | ultralow power RFID energy harvesting, not continuous ESP32 power |
| [wisp/wisp5](https://github.com/wisp/wisp5) BSD-2-Clause | `640kHz 604eee2dffaeba3a270de61cf3dae887a33309c2` | **diverged** from recorded `d978a697...`: 68 ahead, 11 behind, merge base `f8243221...`, not a fast-forward |
| [espressif/esp-now](https://github.com/espressif/esp-now) Apache-2.0 | `master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5` | preferred low-friction RF link for ESP32 nodes; application receipt is separate from radio send callback |
| [openthread/openthread](https://github.com/openthread/openthread) BSD-3-Clause | `main 7009584dadc20cf20c20a6062f357dd572ba6885` | 802.15.4 Thread IPv6 alternative, ESP32-S3 requires separate 802.15.4 RCP or 802.15.4-capable SoC |

Releases/PRs inspected: [Belbin PR 1](https://github.com/mark-belbin/simple-wireless-power/pull/1); [WISP-HW PR 1](https://github.com/wisp/wisp5-hw/pull/1); [WISP firmware PR 38](https://github.com/wisp/wisp5/pull/38); [ESP-NOW PR 153](https://github.com/espressif/esp-now/pull/153); [OpenThread Oct 2026 release](https://github.com/openthread/openthread/releases/tag/v2026.10.0) and [PR 13802](https://github.com/openthread/openthread/pull/13802). More exact metadata: `UPSTREAM_AUDIT.json`.

OOMWOO official firmware `main` advanced **one** commit from `33ee70d...` to `e8f0f175...` (front IR receiver pin docs only). Other pinned OOMWOO `main` remained `1c2bd43...`; upstream OOMWOO PR #79 belongs to **cleaning-jobs** and is NOT a target for this WPT code. No upstream repositories, clones, CAD or colleagues' files altered.

## Full preliminary BOM, procurement and repair

See `BOM.csv`. This is a block-level, **incomplete BOM for procurement**: every unit price and availability is **TBD**, because no safe matched TX/RX, regulator, FOD and cutoff were qualified or priced (including VAT, shipping, repair stock). Hardware remain replaceable, source/firmware documented locally, protected from water. If a wired bus is cheaper and maintains replaceability, retain it. No purchase authorized. No mechanical clips, cable runs or mounting drawings in this W contribution; C owns those interfaces.

## Licensing and safety boundary

All Python here newly authored for this specific experiment; **no code/CAD copied from external projects**. Original external creators retain their own rights and licenses. The overall Valdo repository still has **no license selected**; no downstream redistribution license is granted implicitly until the owner chooses one. Evaluation via this public PR is not commercial or certified safety approval.

Next: choose one genuinely available **regulated** low-voltage inductive pair with datasheets, measured FOD/thermal/cutoff and a realistic all-in bill (in Spain). Then proceed to an authorized isolated resistive bench; keep actual battery/BMS and charging station entirely disconnected.
