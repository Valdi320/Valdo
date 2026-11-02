# W-IND-101 — thermal-window malformed-input fail closed (2026-11-01)

**Scope / ownership:** NEW autonomous open robot; original VALDO W code and digital model only. Own branch `w/independent-sensor-wpt-link-20261028`, PR #9. Never an OEM X20 transplant, cleaning-jobs PR #79, dock battery charger, or another author's source. Local coordination documents D22, 19-alternativas and VALDO_OOMWOO/WPT_DATOS_V01 reviewed before editing; the CAD/C sector remains untouched.

## Material digital defect reproduced before correction

`window_clear("0.5")`, `window_clear(Decimal("0.5"))`, and even `window_clear(0.5,high=float("inf"))` previously returned `True`. The abstract `TxInterlock`, when fed that convertible string as a channel's `ntc_ratio_read` and all other synthetic conditions as clear, could report `energized=True`. The string/object is **not a validated analog ADC measurement**, and a nonfinite comparator limit defeats strict input screening. This is a *model acceptance defect*, not an observed energized transmitter or a proven physical hazard.

**Change:** accept only built-in `int`/`float` representations of ratio and window limits; require ALL finite and `0 <= low < high <= 1`, with strictly `low < ratio < high`. Reject text, byte strings, Decimal/Fraction, bool, custom `__float__`, infinities, NaN, reversed/out-of-range thresholds. Existing legitimate ratiometric inputs remain accepted. A faulted channel inhibits both simulated cuts via the preexisting joint latch, never auto-rearms. If a legitimate ADC adapter uses Decimal, it must **separately validate, bound and convert** its data at its trust boundary; do not interpret this patch as hardware calibration.

## Digital verification (reproducible, no energization)

Copy `tx_thermal_window.py`, `test_tx_thermal_window.py`, `test_thermal_gate_w101.py` into the same clean directory and run:

```sh
python3 -B -m unittest discover -v
# In complete own repository test directory:
python3 -B -m unittest -v test_thermal_gate_w101 test_tx_thermal_window
```

Local controlled differential run: original file at PR #9 prior SHA `bc186bb2988ca85d7ae8731464ca785ec674bc75` **56 tests, 16 failed + 1 error**, including malformed input permitting hypothetical ON. Corrected source **56/56 PASS** (13 new tests and 43 preexisting thermal tests). A failing baseline is intentional evidence of bug, not CI approval. Report `EVIDENCIA.json` records provenance and limitations; full GitHub CI results must be linked only after executed on the published exact commit.

## Independent system decision matrix

| System | Low-cost/simple alternative | More controlled alternative | Decision/evidence |
|---|---|---|---|
| Dock and battery charge | Repairable exposed contacts with appropriate protection | Regulated WPT with autonomous FOD, independent cut, thermal trip, offset/wetness/EMI qualification | **No charging decision.** Battery/BMS isolated, 0 physical tests. |
| Distributed sensor module | Retained short, replaceable, strain-relieved cable/connector | WPT for *hypothetical* 5 V, 0.4 W mean, 1.5 W peak sensor with thermal window and mechanical alignment | **No physical WPT acceptance.** THIS change is input-validation only; do not extend to motors or pumps. |
| Telemetry | Shielded/local cable | ESP-NOW with application ACK/CRC/session/sequence/deadline vs OpenThread IPv6/802.15.4 | Transport-neutral software available, RF hardware and identity not tested; no radio governs motor stopping or TX safety. |
| Micropower RFID | Conventional sensor power | WISP5 energy harvesting | Research only when sub-milliwatt energy budget supports intermittent RFID; not selected for continuous WPT. |

**External attribution/pin check (2026-11-01, without copying external code/CAD):** Mark Belbin simple-wireless-power GPL-3.0 `master 7c7858c0` unchanged; WISP5 hardware BSD-2-Clause `master 08332bc3` unchanged; WISP5 FW BSD-2-Clause **640kHz** `604eee2d` diverges +68/-11 from documented `d978a697`; Espressif ESP-NOW Apache-2.0 `master c3b5f9be` unchanged; OpenThread BSD-3-Clause `main c6872259` +21 commits from `7009584d`, recent router-link PR #13800. Official makerspet/oomwoo `main f01a1b29` untouched; adaptations and their locks/owners not modified. Upstream source: https://github.com/mark-belbin/simple-wireless-power ; https://github.com/wisp/wisp5-hw ; https://github.com/wisp/wisp5 ; https://github.com/espressif/esp-now ; https://github.com/openthread/openthread .

## Safety gates and limitations

**NOT** an implemented physical thermal comparator, ADC, watchdog, FOD, cut-off, EMI shield or WPT converter. Real FOD, coil offset, overcurrent, independent cut, reference/rail, thermistor latency, heating in wet conditions and recovery MUST be characterized with a safety-approved isolated dummy-load bench. Existing KiCad W18 still has **3 ERC violations**; no PCB approved to print or energize. Do not connect lithium cells, BMS, station, motors or pumps. No new hardware/BOM cost, no local stock established, no purchases. Do not mistake abstract `energized=True` for hardware powered.

Next step: independently validated WPT TX safety schematic (fix ERC without fake power flags); then only after separate permission characterize thermal/FOD/offset/EMI/power in isolated bench. No work in OEM code, other's branches or PR #79.
