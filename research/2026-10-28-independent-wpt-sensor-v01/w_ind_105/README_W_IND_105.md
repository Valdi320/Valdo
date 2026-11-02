# W-IND-105 — Reader-inclusive NFC energy gate

**Date:** 2026-11-02  
**Status:** published digital design/model; no hardware approval  
**Scope:** independent robot architecture only. No Xiaomi OEM hardware, firmware, battery or dock work.

## Result in one sentence

The earlier W-IND-104 result showed that a ST25DV64KC tag could conditionally power a 0.248 mW sensor at the tag side. W-IND-105 adds the reader-side cost and changes the architecture decision: **do not add an ST25R3916B reader solely to power one NFC energy-harvesting sensor.** Treat NFC EH only as opportunistic energy while a reader field is already required for identification/data, pending measurement of the incremental RF cost.

This is a datasheet-based lower-bound screen, not a physical measurement and not a whole-system efficiency result.

## 1. Reproducible calculation

Inputs are the 22 exact ST AN4913 Rev.2 points already validated in W-IND-102, plus ST25R3916B DS13541 Rev.11 Table 127 at VDD = 2.4 V.

- Reader active reference: 14 mA typical / 23 mA maximum = **33.6 / 55.2 mW** at 2.4 V.
- Crucial condition: footnote 7 enables RX and TX but has **RFO output segments disabled**. It is therefore a chip-only active reference; antenna-drive power, host MCU, board, regulator and field losses are not included.
- Reader wake mode: 1.8 µA typical / 5 µA maximum = 4.32 / 12 µW at 2.4 V. This is logic + RC oscillator wake-up; W-IND-105 credits it with **zero generated field and zero tag EH power**.
- W-IND-104 sensor profile retained: 0.248 mW average, 1 s period, 10 ms burst, field available for 50% of the non-burst interval.
- Downstream conversion efficiency: 65%, inherited as an explicit assumption from W-IND-104, not measured.

| Manufacturer point | Tag V_EH output | Assumed sensor rail while field is on | Average sensor rail over W-IND-104 period | Reader chip reference average over W-IND-104 period |
|---|---:|---:|---:|---:|
| AM 10%, 1.0 A/m RMS | 1.035 mW | 0.67275 mW | **0.33301 mW** | 16.632 mW |
| AM 10%, 5.5 A/m RMS (best AN4913 point) | 12.593 mW | 8.18545 mW | **4.05180 mW** | 16.632 mW |

At 1 A/m / AM10 the tag-side average margin over the hypothetical 0.248 mW sensor is 1.343×, so the sensor-side result remains conditional. But the reader chip reference is **49.94×** the tag rail while the field is on. Even at the best AN4913 point, the reader chip reference is **4.10×** the tag rail. All 22 manufacturer points remain below the reader's active chip reference after the assumed 65% downstream conversion.

The ideal linear tag counts needed merely to equal the chip-only active reference are:
- 1 A/m, AM10: 50 tags at typical current / 83 at maximum current.
- Best AN4913 point: 5 / 7 tags.

Those counts are optimistic arithmetic lower bounds only. They ignore mutual loading, coupling changes, reader RF output power, antenna, MCU, regulator and host-board losses. They are not a multi-tag design recommendation.

### Why this changes the decision

The tag output is useful DC at V_EH, but it is not free energy. A reader must create the field. The active-current condition in the reader datasheet has its RF output segments disabled, so it is deliberately a low reference for the reader chip rather than a full field-on input measurement. The actual field-on system cost is unknown and cannot improve the dedicated-energy case.

A low-power reader wake state can reduce idle consumption, but it does not generate the field needed for energy harvesting. It cannot be counted as a continuous power source.

## 2. Architecture decision matrix

| Function / option | Decision | Reason and gate to reconsider |
|---|---|---|
| Dedicated NFC EH reader to power a sensor | **NO-GO** for the ST25R3916B candidate | All 22 tag points are below the chip-only active reference after assumed conversion; actual RF drive and board input are additional. |
| NFC EH while the reader field is already needed for ID/data | **Conditional** | Measure incremental RF input, tag loading, communication margin and duty. Do not claim energy savings before that. |
| WISP5 passive UHF sensor | **Defer** | Only if a passive UHF sensor and compatible UHF reader are already justified. It is not an active module rail. |
| Dock charging | **Keep serviceable contacts as baseline** | NFC EH is not a dock charger. No battery/BMS or lithium charging tests. WPT dock remains unqualified. |
| Power for active modules | **Keyed locking connector by default** | A removable connector is simpler and measurable. Regulated WPT only after load/pulse data and documented FOD, temperature, offset, EMI and independent hardware cut. |
| Simple Wireless Power open-loop reference | **Study only; do not adopt** | Author's results are not ours; no closed-loop receiver feedback. Open issue reports a hot TX switch. |
| Critical stop / safety inhibit | **Local hardwired fail-safe** | Never depend on ESP-NOW, Thread, NFC or a radio timeout for a critical stop. |
| Data between small modules | **ESP-NOW provisional for one hop** | Application ACK, CRC, sequence, timeout, bounded retries, authentication/privacy and local recovery remain required. |
| Data requiring IPv6 mesh / multi-hop | **OpenThread alternative** | Use only if topology requires it; it does not supply power and still needs application-level delivery semantics. |

Keep the three energy/data problems separate:
1. **Dock:** high-power charging and battery safety, not NFC EH.
2. **Distributed module power:** connector first; regulated WPT only with measured loads and independent protection.
3. **Data:** ESP-NOW or OpenThread, with application-level integrity/recovery. Radio never authorizes power or safety cuts.

The 400 mW active-module reference remains far beyond the best tag rail result. Do not put WPT on motors, suction fans or pumps without measured average/pulse consumption and a demonstrated loss/thermal budget.

## 3. BOM screen — not a purchase list

| Item | Diotronic Zaragoza | Alternative / public price | Availability / reason |
|---|---|---|---|
| X-NUCLEO-NFC08A1 reader evaluation board | Exact public reference not found; local stock and final price pending | DigiKey Spain: 33.95 € ex VAT / 41.0795 € incl VAT; 443 shown in stock, MOQ 1, standard lead-time field 13 weeks. Farnell: 34.98 € ex / 42.33 € incl, MOQ 1, 28-week standard lead. RS: 33.96 € ex / 41.09 € incl, temporarily out of stock; next visible quantity dated 11-Dec-2026. | **Not selected.** Evaluation board includes ST25R3916B and a 47 × 34 mm, four-turn 13.56 MHz antenna. Its published up-to-1.7 W differential output is not our measured field or power draw. |
| ST25DV64KC-IE8T3 tag IC | Exact local stock/price pending | DigiKey EU (Germany) page: 1.38 € ex, 2,327 shown; applying Spain's 21% VAT gives an estimate of 1.6698 € incl, not a verified Spain checkout total. Mouser Spain page shows 1.38 € and 3,982 stock/ETA data, but the visible ETA is 2026-08-19 (past); tax treatment and live availability must be reconfirmed at checkout. | **Reference only.** Tag EH output depends on field, antenna and load. |
| EH buffer capacitor | Local passive alternatives can be checked once electrical limits are known; no exact reference approved | No part selected. W-IND-104's 47 µF candidate remains rejected as final hardware because ESR, leakage, tolerance, temperature and life are not qualified. | Do not choose by nominal capacitance alone. |
| MCU / radio | Diotronic availability pending after MCU choice | No board or module selected. | ESP-NOW/OpenThread is a protocol decision, not a power source. |
| Regulated WPT TX/RX, FOD, thermal cut, independent cut | Do not source safety-critical parts from an unqualified catalogue match | Specialist distributors / manufacturer documentation required; no selected part or price. | Need traceable ratings, FOD behavior, thermal limits, offset/EMI data and independent hardware cut. |
| Keyed locking module connector | Diotronic local stock and price pending | TME/Mouser/DigiKey exact family not yet selected. | Default for active modules until WPT demonstrates a net benefit. |

Diotronic is an auxiliary local source, especially for equivalent passives, connectors and prototyping consumables. A catalogue hit is not proof of shelf stock. No purchase was made.

## 4. External project audit — exact refs checked 2026-11-02

No upstream repository, clone, source or CAD was edited. No external code or CAD was copied into W-IND-105.

| Project / owner | Branch and current HEAD | Comparison with 19-alternativas pin | Changelog / PR / issue examined | License and decision |
|---|---|---|---|---|
| mark-belbin/simple-wireless-power | master 7c7858c0dd7040801b6f191df1396115560218f0 | Identical to pin | Latest commit only updates README with coil-gap measurements. Open issue #4 reports BTS6142DAUMA1 TX switch overheating after power-up (updated 2025-09-11). | GPL-3.0. Reference only; do not copy. |
| wisp/wisp5-hw | master 08332bc398aa3350d351ef2aaac163f8007cffda | Identical to pin | Latest commit updates tuning-match values. Open issue #2 asks for an S-882Z alternative. | BSD-2-Clause. Hardware reference only. |
| wisp/wisp5 firmware | master d978a6978ad23ccd6c44dd55430973b04a3d4a9b | Identical to pin | Branch 640kHz HEAD 604eee2dffaeba3a270de61cf3dae887a33309c2: +68 / −11 vs master pin. Branch 436kHz HEAD bf2c8fc1ad1d5eb88835e1ef63f5bcd5fdbc7b32: +73 / −11. 640kHz_AssertInitialized HEAD 9f85603120b8bdb838d83e72141ae5212f0d5762. Issue/PR #36 is closed “640k hz experimental”; #39 is closed “Some minor modification” and its merge commit is on the 436kHz line; #40 is an open “Information update” issue, **not a 436kHz PR**. | BSD-2-Clause. Keep branch divergence explicit; no fast-forward or code reuse. |
| espressif/esp-now | master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 | Identical to pin | Latest commit is ESP-IDF v6 compatibility (WIFI_IF_STA and safe copy from packed config). PR #153 closed. Issue #162 requests a managed ESP-NOW mesh framework and remains open; it is a request, not an implemented mesh. | Apache-2.0. One-hop candidate; add application ACK and authentication. |
| openthread/openthread | main c6872259f4194fb76c7d333bda209343e8c88e71 | 21 commits ahead, 0 behind pin | Merged #13800 (MLE Link Accept scheduling), #13802 (stale router neighbor), #13821 (POSIX max-power-table parameter). Open #13824 (scheduled TX simulation), #13827 (mbedTLS config generation), #13828 (Joiner memory leak). | BSD-3-Clause. Mesh alternative only if needed. |

The prior local WISP pin is the **master** revision, not the 640kHz branch. Branch names and commit histories were resolved explicitly; branch order was not used to infer freshness.

## 5. OOMWOO / VALDO / adaptation ownership audit

- OOMWOO official makerspet/oomwoo main HEAD ad61099e222a9d8e8573bcda546380b4256a1902 is 23 commits ahead of the local pin. PR #79 closed/merged on 2026-11-01; its only official change is the contributions/cleaning-jobs/Valdi320/README.md pointer. It does not contain WPT work.
- OOMWOO CAD HEAD 1e1c4091ca6b4937dc16468dc8034eae7cc96adf is +1 and adds/updates Fusion wheel/assembly artifacts; no WPT interface was adopted.
- OOMWOO PCB HEAD ac8ac0b52254582be3acda9d3fddfd06cbbabd4f is +12; it regenerates the charging-dock output PDF and updates main-phone/sensor schematics. No WPT TX/RX or independent WPT cut was selected.
- OOMWOO firmware HEAD fd8689f3e3f7bcd0dcc35725be4a48cd9fcc8596 is +8; it updates docs/SPEC.md and include/oomwoo_pins.h. No WPT firmware was adopted.
- The other seven local upstream clones remain clean at their recorded pins. None was updated. TME exact references for the reader board/tag were not found in the targeted search; that is not proof of unavailability.
- Local adaptation remains a reference-only copy: WPT_DATOS_V01.md, WPT_LIMITES_D22.md and DECISION_NO_TRASPLANTE.md were read; the adaptation directory has no .git and no *.lock. Its WPT contract/limits have not been changed.
- Codex A67/A68 work is in a separate support repository/branch and is recorded as local-only with a blocked goal and no push/PR. It was not imported or edited.
- The shared X20ProAbierto/Valdo checkout is dirty with untracked work from other branches; it was not touched. The local publication checkout W_IND_12_PUBLISH_OWN_20261028 was not used for this commit sequence.
- VALDO PR #9 was open with W-IND-104 as its last published milestone before W-IND-105. It had no external reviews or review threads. W-IND-104 Python CI was PASS; native KiCad W-IND-18 still had three electrical ERC violations. W-IND-105 does not silence or alter those violations.

## 6. Evidence level and limits

**Evidence level:** manufacturer datasheet/application-note values + deterministic arithmetic + explicit assumptions + automated tests. No physical measurements, no electromagnetic simulation, no reader-input measurement, no field probe, no selected coil, no FOD/thermal/offset/EMI qualification.

The model deliberately does not claim:
- whole-system efficiency;
- reader field-on input power;
- actual coupling at robot module geometry;
- multi-tag behavior or mutual loading;
- a selected capacitor, reader board, MCU, radio or WPT controller;
- battery/BMS charging safety or hardware approval.

Battery and BMS remain disconnected. No dock, firmware, machine, Xiaomi OEM or PR #79 files were modified. No purchases, printing, soldering or energization.

## 7. Reproduction

From repository root, run:

    cd research/2026-10-28-independent-wpt-sensor-v01
    python -m unittest -v w_ind_105.test_w_ind_105
    python -m w_ind_105.w_ind_105 --out w_ind_105/RESULTADO_CI.json

The CI workflow runs the same commands and uploads RESULTADO_CI.json as an artifact. The model imports and validates the exact 22-point w_ind_102/AN4913_REV2_EH.csv file; it does not interpolate manufacturer points.

## Sources

- [ST AN4913 Rev.2 — Energy harvesting delivery](https://www.st.com/resource/en/application_note/an4913-energy-harvesting-delivery-impact-on-st25dvi2c-series-behaviour-during-rf-communication-stmicroelectronics.pdf)
- [ST25R3916B DS13541 Rev.11 — electrical characteristics, Table 127](https://www.st.com/resource/en/datasheet/st25r3916b.pdf)
- [ST25DV64KC product and ordering status](https://www.st.com/en/nfc/st25dv64kc.html)
- [X-NUCLEO-NFC08A1 at DigiKey Spain](https://www.digikey.es/es/products/detail/stmicroelectronics/X-NUCLEO-NFC08A1/16962233)
- [ST25DV64KC-IE8T3 at DigiKey EU](https://www.digikey.de/en/products/detail/stmicroelectronics/ST25DV64KC-IE8T3/14645818)
- [ST25DV64KC series at Mouser Spain](https://www.mouser.es/c/semiconductors/wireless-rf-integrated-circuits/?series=ST25DV64KC)
- [X-NUCLEO-NFC08A1 at Farnell Spain](https://es.farnell.com/stmicroelectronics/x-nucleo-nfc08a1/expansion-board-nfc-card-reader/dp/4458495)
- [X-NUCLEO-NFC08A1 at RS Spain](https://es.rs-online.com/web/p/placas-y-kits-compatibles-con-arduino/0146352)
- [Diotronic Zaragoza](https://www.diotronic.com/) — Av. de Valencia, 5; exact item stock/price not publicly verified.
