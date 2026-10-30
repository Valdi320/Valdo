# W-IND-42 — Positive driven HEALTH line; open wire means OFF

2026-10-30. VALDO independent robot, sector W. **DIGITAL / HYPOTHETICAL ONLY. NOT APPROVED FOR ENERGIZING.**

## Finding and design change

Previously selected TI TPS3700 OUTA is open-drain, asserting low on fault. With an upstream open-drain fault line and pull-up on its receiver, a broken wire, unpowered supervisor, or high-impedance fault appears indistinguishable from *healthy*. Merely inverting the signal after the break does not solve continuity. Datasheet entry: https://www.ti.com/product/TPS3700 .

**Proposed interface contract only:** a supervisor actively drives HEALTH=HIGH when healthy, with the *receiver-side* input pulled LOW. Before allowing either of the two normally-off eFuses, independently qualified upstream 5V, explicit local rearm and other local hardware protections must also agree. No radio is allowed to perform a safety stop or rearm. This cannot be implemented by connecting the existing TPS3700 OUTA unchanged. Push-pull output supervisor families to screen, not approved part numbers: https://www.ti.com/product/TPS37 and https://www.ti.com/product/TPS3704-Q1 . Choose exact active-high-healthy SKU only after reading VDD/POR/voltage-domain requirements and safety characterization.

## Reproducible falsification model

- Run from this directory: `python3 -m unittest -v test_w42` (23 deterministic unit tests PASS locally).
- Run: `python3 w42_positive_health.py --out W42_EVIDENCE.json` (same stdlib; 128 logical combinations per topology, 256 total).
- Sweeps: rail 3V3 healthy/dead; upstream qualified 5V true/false; local arming; other hardware interlocks ideal; eight fault modes (none, wire open, unpowered monitor, stuck HiZ/high, shorts to high/GND, falsely healthy supervisor).
- Under rail dead + 5V qualified + ideal local permissions, **6 of 8** cases request ON for current open-drain/pull-up; **3 of 8** for proposed actively-driven-high/pull-down. A broken wire, monitor death and driver HiZ request OFF in new model. Short-to-high, stuck-high and false-healthy still request ON and are **unresolved**. The counts are not probabilities, coverage or real functional-safety certification.
- Hypothetical 47k ohm receiver pull-down at 5V consumes 0.532 mW when driven HIGH; fictional 1uA leakage causes 47mV across it. The 0.8V logic low comparison and leakage are examples, NOT device specifications. No source/sink, POR, propagation, EMI, leakage or backfeeding measured.
- GitHub Actions workflow `w-ind-42-positive-health.yml` reruns tests and exports JSON named **W42-POSITIVE-HEALTH-256-LOGIC-CASES-NOT-HARDWARE**.

## Safety/engineering limits

Safety approval stays FALSE. This is NOT a KiCad/netlist, PCB, physical sensor, independent protection cutoff, functional-safety argument or operating robot. Both eFuse enables still require electrical integration, W37 release-and-rearm, cold start and brownout verification. Existing W-IND-18 historic ERC fault remains blocking. Shunt, 5V domain, backfeed, high-wire short, comparator false-health, supply loss and time response remain possible common faults. No real FOD, temperature, moisture, offset/air gap, coils, efficiency or EMI test. No battery, BMS, dock or motors connected.

Distinct subsystems: dock lithium charging UNTOUCHED; WPT distributed-to-module experimental *sensor only* hypothesized 5V 0.4W average / 1.5W peak; RF ESP-NOW or OpenThread is **data only** requiring application ACK/CRC/sequence/timeouts/recovery/transport encryption and cannot substitute a safety circuit; WISP RFID harvesting only if justified for tiny intermittent sensors. Never extrapolate sensor WPT to pumps/motors.

## Decision / BOM / supply

See `MATRIZ_W_IND_42.csv` and `BOM_W_IND_42.csv`. Prioritize the active-driven HEALTH interlock for *next schematic study*, **not procurement**. Exact push-pull supervisor part, its POR and thresholds, pull-down value, layout and independent qualification all pending. TPS37/TPS3704-Q1 are *families*, not chosen replacements. Example comparator TLC3704IPWR RS Spain 5-pack EUR 9.51 VAT included (EUR 1.902 each within package) is **not a drop-in supervisor**. Catalog price is not local stock or delivered cost. Diotronic in Zaragoza remains AUXILIARY; no exact 47k 1% resistor reference, stock, final VAT price or MOQ confirmed. TME/Mouser/DigiKey exact part and landed comparisons pending. Reparable retention-connector cable remains candidate: prove energy/cost/maintenance benefit before eliminating it.

## Provenance / ownership / latest heads checked 2026-10-30

Master decision of 2026-10-28 cancels Xiaomi X20 Pro OEM transplant. Consulted local `00_DECISION_20261028_NO_TRASPLANTE_X20.md`, `19-alternativas-abiertas-para-robot-independiente.md`, D22 report/contract, coordination W/C agreement and Codex handoffs, VALDO_OOMWOO `LEEME_PRIMERO.md` and `adaptacion/contratos/WPT_DATOS_V01.md`. Only own W branch may be modified; OOMWOO #79, all upstream clones/CAD/Codex work untouched. One currently enabled automation: this W one; OOMWOO hourly paused.

| Owner / license | branch HEAD (vs pin from alternatives) |
|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), GPL-3.0 | master `7c7858c0dd7040801b6f191df1396115560218f0` identical. Author 81.3% at ~100W / 1-2mm is *author result only*, not ours. |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw), BSD-2-Clause | master `08332bc398aa3350d351ef2aaac163f8007cffda` identical |
| [wisp/wisp5](https://github.com/wisp/wisp5), BSD-2-Clause | **640kHz** `604eee2dffaeba3a270de61cf3dae887a33309c2`, **diverged** 68 ahead, 11 behind pin `d978a6978ad23ccd6c44dd55430973b04a3d4a9b`; no blind fast-forward |
| [espressif/esp-now](https://github.com/espressif/esp-now), Apache-2.0 | master `c3b5f9be245f1a80db9cb938600566aa6a8dd1e5` identical |
| [openthread/openthread](https://github.com/openthread/openthread), BSD-3-Clause | main `e577777c308f6c87e5da3056239231a8fc147cb2`, 14 commits ahead pin `7009584dadc20cf20c20a6062f357dd572ba6885`, API/CLI/CI changes; review PRs before any integration |

OOMWOO official makerspet/oomwoo main `f01a1b295f462da5ab8d5f021a3f741cbd2b47df`, oomwoo-one jazzy `a630d1c77255072d280a2a41a7a2bd1a1c98cadd`, oomwoo-cad main `038002ddc5586d711960545ecf76a038eec48656`, all READ ONLY. No third-party source/CAD copied. Local VALDO W own tests/models and code original, no author attribution confusion.

**Next gate:** choose documented active-high healthy supervisor and receiver logic, design two independently normally-off EN paths including loss-of-rail and anti-backfeed in KiCad; ERC/netlist, partial-power and transient digital/SPICE tests; independent FOD/thermal/overcurrent and isolated resistive bench only with separate authorization/safety process. Never energize from this model.
