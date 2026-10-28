# W-IND-02 — ESR/derating and low-power sensor supply hold-up (2026-10-28)

**NEW independent, open, local robot only.** No Xiaomi electronics, firmware, battery or dock transplant; no third-party OOMWOO clone, CAD, or cleaning-jobs PR #79 touched. **Simulation and vendor catalog comparison only. No powered bench, coils, hardware, safety certification or battery charge.** Original VALDO Python, no third-party code/CAD imported. Overall Valdo license remains unselected.

## Material finding: capacitance rating alone is not enough

W-IND-01's ideal capacitor calculation was **35.294 mF** for a hypothetical 1.5-W, 150-ms interruption with capacitor 5.0→3.5 V. It omitted converter losses, equivalent series resistance (**ESR**) and capacity derating. To maintain a real **5-V sensor rail** when the capacitor falls below 5 V, an **input-3.5-V-capable buck-boost regulator** would be necessary; no unit is yet qualified.

| Modeled case, 1.5 W / 150 ms | Needed *nominal* capacitance |
|---|---:|
| 100% regulator efficiency, ESR 0 Ω, no derating | 35.28 mF (closed-form 35.294 mF) |
| 85% converter, ESR 0.2 Ω, capacity retains 60% | **74.77 mF** |
| 75% converter, ESR 0.5 Ω, retains 50% | **119.04 mF** |
| ESR 4 Ω (75% converter), threshold regulator VIN ≥3.5V | **Infeasible initially** |
| Eaton KW-5R5C224-R **0.22 F, 50 Ω ESR** at 0.4 or 1.5 W | **Infeasible initially** despite nominal capacity |

The Eaton rejection is the actionable improvement: [Farnell Spain](https://es.farnell.com/eaton-electronics/kw-5r5c224-r/conden-0-22f-5-5v-super-radial/dp/2302171) lists that **exact** KW-5R5C224-R part at **5.5 V, 0.22 F, ESR 50 Ω**, **€3.25 excl. VAT**, and **18-week manufacturer lead time** (as seen 28 Oct 2026; stock/price may change). Verify the vendor's ESR frequency/test definition in the manufacturer datasheet before any later selection. This is a vendor listing **not** our measurement. Using P=η·I·(Vcap−I·ESR), a 5-V source with 50 Ω simply cannot initially supply the hypothetical 0.4-W or 1.5-W loads.

Additional modeled sensitivities at η=0.85, ESR=0.2 Ω, capacity fraction 0.6: 0.4 W for 150 ms → **18.83 mF**; 1.5 W for 50 ms → **24.91 mF**. Steps are 0.25 ms; tests check analytical limit, monotonicity, parameter invalidity, source energy conservation and 1-ms vs 0.05-ms numerical convergence (<0.2% relative).

**Decision: do NOT mandate 150-ms supercapacitor hold-up for the first non-safety-critical sensor.** A power interruption should end the observation and restart the replaceable module in a non-authorized telemetry state; any renewed session must require *actual local commissioning* and fresh non-replay identifiers (integration still pending). Collect real dropout/load measurements first. This removes an unverified expensive/leaky component, not a safety guarantee.

A [Pololu S13V10F5](https://www.pololu.com/product/4083) 2.8–22 V input → 5 V regulated buck-boost is a commercial **unapproved** reference; manufacturer typical 85–95% efficiency but 10–20 mA no-load current, potentially material relative to our assumed 80-mA sensor mean. It has not been purchased, connected or characterized.

## Three problems that must remain separate

| Domain | Candidate | Remaining physical blocks |
|---|---|---|
| Robot dock→future battery/BMS | Not in first pilot | independently reviewed battery charging, BMS, FOD, thermal, isolation |
| Fixed host→detachable sensor 0.4-W mean/1.5-W peak (ASSUMED) | **Regulated** matched WPT pair *only if* it beats a mechanically robust connector | TX/RX, offset, wetness, metal FOD and temperatures, independent normally-off cutoff, inrush, EMI, cost |
| Sensor→host messages | encrypted unicast ESP-NOW with application ACK, CRC, monotonic session/seq and timeout; OpenThread 802.15.4 an alternative | actual provisioning and privacy tests, RF coverage, resynchronization; radio **never** authorizes emergency cutoff |

Mark Belbin's GPL-3.0 open-loop power demonstrator is not a transmitter with verified regulation/FOD; WISP5 BSD-2 applies to ultra-low-energy RFID sensors, **not** 1.5 W. Do not copy author code. Supply-side normally-off cuts, FOD and thermal shutdown must be **independent of ESP-NOW/OpenThread**, including on MCU reset; software model does not implement any of them. Read the block-complete but **not purchasable** `BOM_W_IND_02.csv`; unmatched TX/RX, safety circuitry, VAT, shipping, production costs remain TBD.

## Exact owner/HEAD review 28 October 2026 before publication

- [mark-belbin/simple-wireless-power master](https://github.com/mark-belbin/simple-wireless-power/tree/master) GPL-3.0: HEAD `7c7858c0dd7040801b6f191df1396115560218f0` unchanged vs 19-alternativas; PR #1 merged.
- [wisp/wisp5-hw master](https://github.com/wisp/wisp5-hw/tree/master) BSD-2-Clause: `08332bc398aa3350d351ef2aaac163f8007cffda` unchanged; PR #1 merged.
- [wisp/wisp5 640kHz](https://github.com/wisp/wisp5/tree/640kHz) BSD-2-Clause: `604eee2dffaeba3a270de61cf3dae887a33309c2`, **68 ahead/11 behind** pinned `d978a6978ad23ccd6c44dd55430973b04a3d4a9b`, non-fast-forward; PR #38 merged.
- [espressif/esp-now master](https://github.com/espressif/esp-now/tree/master) Apache-2.0: `c3b5f9be245f1a80db9cb938600566aa6a8dd1e5` unchanged; PR #153 closed **unmerged**. [Espressif's API](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c5/api-reference/network/esp_now.html) says MAC send success is not application ACK; LMK must be provisioned for encrypted unicast.
- [openthread/openthread main](https://github.com/openthread/openthread/tree/main) BSD-3-Clause: **`3d645eb9106cb1d5c2ff11891e84dc14e52e293a`**, [5 commits ahead](https://github.com/openthread/openthread/compare/7009584dadc20cf20c20a6062f357dd572ba6885...3d645eb9106cb1d5c2ff11891e84dc14e52e293a) of recorded `7009584dadc20cf20c20a6062f357dd572ba6885` (radio address filtering docs, sub-MAC and heap); PR #13802 still open. No upstream source imported.
- [makerspet/oomwoo main](https://github.com/makerspet/oomwoo) `1c2bd43abcf74288afcf2d8b64514cc325f9b905` in checked default branch, OOMWOO PR #79 active cleaning-jobs and **outside** W scope; companion task owns it. Newer oomwoo-firmware commit exists but not imported; this pilot does not modify either project.

## Reproduction and limits

```bash
cd research/2026-10-28-independent-wpt-sensor-v01
python3 -m unittest -v test_w_link test_hold_up_envelope
python3 hold_up_envelope.py
```

W-IND-02 adds **14/14 new Python tests PASS locally** to W-IND-01's existing **27/27**, with no hardware. The model assumes ideal constant-power buck-boost, constant ESR/efficiency, simplistic capacitor derating, no leakage/charge/inrush, finite simulation steps, and **no WPT coils/heat/EMI/FOD**, so cannot predict measured device behavior or authorize installation.

**Next independent engineering gate:** compare two currently supplied, programmable low-power TX/RX pairs with published *actual* FOD/thermal and cutoff evidence; select only after 5-V peak load, standby, offset and total EU cost are verified. Before any energized bench, explicit human safety authorization, isolation and dummy resistor are required; lithium/dock stay disconnected.
