# W-IND-88 — decisions, component sourcing and owner/license audit (1 Nov 2026)

**Scope W ONLY**; read master local decision 28 Oct no Xiaomi transplant, alternatives list SHAs, D22, W/C coordination agreement, VALDO_OOMWOO LEEME_PRIMERO and WPT_DATOS_V01. The shared local Valdo checkout is **dirty** and belongs to Codex: unchanged. Makerspet OOMWOO, adaptation, CAD of C, PR #79 and upstream authors are untouched. This milestone adds only original W88 Python, tests, documentation and CI to own Github W PR #9. No real measurements, buys, assembly or hardware release.

## Decision matrix

| Candidate | Power/data & protections/cost constraints | Decision |
|---|---|---|
| Serviceable retained cable | Cheapest/simplest candidate; physical retention, length, cost/cycles C still unknown | **BASELINE**, not removed |
| Simple unregulated inductive WPT | No verified offset, FOD, thermal, EMI or autonomous cutoff | **BLOCKED**, not selected |
| Regulated WPT with independent FOD/thermal/EMI/offset and fail-OFF cut | Safety-aware reference concept only; no hardware qualifications/efficiency/total cost | **BLOCKED** |
| ST25DV04KC NFC harvesting | ST manufacturer mW points, unregulated EH, reader/antenna absent; RF exchange may cause harvested-power blackout; retries cost energy | Candidate **optional noncritical intermittent** microsensor only |
| WISP5 RFID sensors | Very-low-energy research architecture, needs specific reader/ecosystem | Secondary |
| ESP-NOW vs OpenThread | Both radio **data**, neither power: app ACK + CRC + sequence/epoch + timeout + replay recovery + privacy encryption; no critical RF-controlled stop | Choice deferred to power/radio data |
| Dock charging, Li-ion/BMS, pumps/motors | Higher power and independent safety certification | Out of W88 test; no physical activity |

## BOM exploratory, Diotronic AUXILIARY (prices historic; not ordered)

| Item | Diotronic / alternative | Price incl 21% VAT, MOQ | Zaragoza store availability and selection |
|---|---|---|---|
| ST25DV04KC-IE8S3 **SO8N** EH tag | Diotronic unverified / [Farnell ES 3972494](https://es.farnell.com/stmicroelectronics/st25dv04kc-ie8s3/rfid-leer-escribir-13-567mhz-nsoic/dp/3972494) | previously ≈**1.12€**, MOQ 1, no shipping | **UNVERIFIED local**, reparable SO8N; chip only |
| Same tag SO8N | Diotronic unverified / [RS ES 248-7495](https://es.rs-online.com/web/p/modulos-rf/2487495) | previously **5.83€/5**, MOQ5 | external stock not store stock, delivery pending |
| Different ST25DV04KC-IE8C3 **UFDFPN** | Diotronic unverified / [DigiKey ES](https://www.digikey.es/es/products/detail/stmicroelectronics/ST25DV04KC-IE8C3/16359660), [Mouser ES](https://www.mouser.es/es/ProductDetail/STMicroelectronics/ST25DV04KC-IE8C3?qs=QNEnbhJQKvY88dTRgPa5uw%3D%3D) | previous ≈1.34€/≈1.23€, MOQ1, shipping pending | **NOT** pin/footprint replacement for SO8N |
| Full reader+antenna matching/transmitter | Diotronic pending / TME, Mouser, DigiKey, manufacturer | No verified SKU, price, MOQ | critical cost/field/consumption **missing** |
| Effective-cap reservoir, regulator, shunt | Diotronic pasivos if equivalent; TME/DigiKey/Mouser | No verified SKU, price, MOQ | 2126.984µF **effective** ideal theoretical, not approved |
| FOD/thermal/supervisor/independent cutoff | specialist traced stock/datasheet, Diotronic only if documented | No validated SKU or price | needs max response, electrical rating and real tests |
| Serviceable cable baseline | Diotronic / TME/Mouser/DigiKey | pinout, MOQ, cost pending | reference lifecycle comparison, C owns mechanics |

**Prices are catalogue observations, not confirmed today; no verified stock at Zaragoza branch, no VAT+shipping checkout totals, no order.** Never decide safety electronics by proximity.

## Five author repositories: branch and HEAD against registered 28 Oct SHA (checked GitHub 1 Nov)

| Creator/licence | HEAD & comparison | PR/changelog examined |
|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power), GPL-3.0 | master `7c7858c0dd7040801b6f191df1396115560218f0` same 0/0 | PR #1 closed 2021, no GPL code copied |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw), BSD-2-Clause | master `08332bc398aa3350d351ef2aaac163f8007cffda` same 0/0 | PR #1 historical closed |
| [wisp/wisp5](https://github.com/wisp/wisp5/tree/640kHz), BSD-2-Clause | **640kHz** `604eee2dffaeba3a270de61cf3dae887a33309c2`, diverged **+68/−11** vs `d978a6978ad23ccd6c44dd55430973b04a3d4a9b` | CCS11 2022, PR #40 open; never rank by branch names |
| [espressif/esp-now](https://github.com/espressif/esp-now), Apache-2.0 | master `c3b5f9be245f1a80db9cb938600566aa6a8dd1e5` same 0/0 | PR #151/#153 closed 2026 |
| [openthread/openthread](https://github.com/openthread/openthread), BSD-3-Clause | main `c6872259f4194fb76c7d333bda209343e8c88e71` **+21/−0** vs `7009584dadc20cf20c20a6062f357dd572ba6885` | Oct31 #13800 LinkAccept/#13821 POSIX, Nov1 PRs #13814/#13826 open |

[makerspet/oomwoo](https://github.com/makerspet/oomwoo) official main `f01a1b295f462da5ab8d5f021a3f741cbd2b47df`, PR #79 remains outside scope; Valdo master `8a6030bda52a159493a42dc4bed245e722b876e8`. Zero external code, schematics or CAD copied or relicensed.
