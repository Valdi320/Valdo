# W-IND-29 — KiCad RX Kelvin current monitor (DIGITAL REVIEW ONLY)

**2026-10-29 · VALDO W-sector · independent new repairable robot · NO Xiaomi OEM transplant.**

## Measurable improvement and scope

W-IND-28 mathematically rejected reusing a **346.4 mA receiver overcurrent limit on the transmitter input**, because efficiency variation makes a single threshold ambiguous. W-IND-29 implements a **source-generated, editable KiCad schematic** of the **receiver-side monitor only**, and a strict checker of **KiCad-exported native XML**. The drawing uses a four-terminal 0.1Ω conceptual shunt, distinct supply/load nets, distinct Kelvin sense nets, verified 8-pin TI INA301A1 mapping, a LIMIT 8.66kΩ resistor and open-drain ALERT pullup 10kΩ.

**This does not implement a transmitter, induction, motor supply, charging dock, battery, BMS, regulator, FOD, thermistor, reverse blocking, or even an autonomous receiver power cut.** ALERT_N is solely a monitor, never a shutdown. A supply brownout can make its alert unavailable. Symbols J1/J2 are **declarations of hypothetical 5V external supply and load**, not approved or purchased connectors. Four-terminal RSH1 is a **generic, unqualified concept**, not a purchasable/footprinted part. No hardware energizing permitted.

## Schematic contract

| Net | Required pins | Meaning |
|---|---|---|
| RX5_SOURCE | J1.1 RSH1.1 U1.1 U1.5 R2.1 | 5V receiver source and monitor bias, RESET high for study |
| RX5_LOAD | RSH1.2 J2.1 | Load separate from source, current measured through shunt |
| KELVIN_PLUS | RSH1.3 U1.8 | Sense upstream without sharing main current track |
| KELVIN_MINUS | RSH1.4 U1.7 | Sense downstream without sharing main current track |
| LIMIT | U1.3 R1.1 | Threshold-setting resistor, other end grounded |
| ALERT_N_MONITOR_ONLY | U1.6 R2.2 | Telemetry-only open drain output |
| GND | J1.2 J2.2 U1.4 R1.2 | Declared local return |
| U1.2 | marked unconnected | OUT intentionally unused |

TI official INA301 DGK pinout (see [datasheet SBOS713A](https://www.ti.com/lit/ds/symlink/ina301.pdf)): **1 VS, 2 OUT, 3 LIMIT, 4 GND, 5 RESET, 6 ALERT, 7 IN−, 8 IN+**. INA301A1 has **20 V/V** gain and max ±125 μV offset, not A3's offset. With *hypothetical* 0.1Ω Rsh, 8.66kΩ and 80μA LIMIT bias, nominal 0.6928V / (20×0.1Ω)=**0.3464 A**. This ignores real tolerance/time response/pulse behavior/thermal/FOD/PCB effects and does not promise a 400mA fault disconnect. RESET is tied high as a mode study; its latch resets when supply collapses and is **not** persistent safety state.

## Reproduction

Original Python 3.11+ standard library only, no imported source code from third parties. In the published directory:

~~~sh
python3 generate_w29.py
python3 generate_w29.py --verify
python3 -m unittest -v test_w29
mkdir -p native_out
kicad-cli sch erc --format json --severity-all --exit-code-violations -o native_out/erc.json W29_RX_KELVIN_MONITOR_ONLY.kicad_sch
kicad-cli sch export netlist --format kicadxml -o native_out/rx_native.xml W29_RX_KELVIN_MONITOR_ONLY.kicad_sch
python3 netlist_gate_w29.py native_out/rx_native.xml --output native_out/review.json
~~~

GitHub Actions workflow w-ind-29-rx-kelvin.yml runs Python and **native KiCad 9.0.2** (Docker) and archives ERC, XML, topology JSON even on failure. Schematic symbols are **generated** and checked reproducibly; do not edit generated files by hand. Tests include adversarial injection of reversed shunt/INA sense, shorted source/load, lost LIMIT, swapped variant, bypass nets, duplicate pins, unexpected components. **29 synthetic Python tests passed in the isolated authoring environment**. Native CI proof must be checked separately: green ERC + XML topology is *connectivity review*, not electrical qualification.

## Explicit decision matrix / safety limits

- **Power to removable sensor:** first pilot 5V, 0.4W mean /1.5W peak is hypothetical, not measured. Compare protected inductive approach with a replaceable connector and its lifecycle cost; avoid multiple constantly-idling transmitters without real consumption results.
- **TX input and RX output:** distinct current domains. Our RX-only 346.4mA threshold **must never be copied to TX**; TX needs independent fault budget and autonomous power cut.
- **Dock charge:** separate system with regulated charge/BMS safety process; keep battery and station disconnected.
- **FOD/temperature/offset/EMI:** independent hardwired controls unselected and unmeasured; loss of power, stuck switches, reverse-feed and wetness not qualified.
- **RF data:** ESP-NOW (Apache-2.0) or OpenThread (BSD-3-Clause) are *alternatives*, not both needed; require authentication/privacy, CRC, application ACK, session+sequence, timeout, replay rejection and local recovery. RF never authorizes a critical shutdown or conveys power.
- **WISP5:** deferred to sub-milliwatt intermittent microsensing study; no claim that RFID harvesting supplies a continuous 1.5W module. No inductive motors or pumps without load/power/thermal economics.
- **Service:** accessible and replaceable sensor and wire/coil module, local printing of mechanical housing only, no shared fragile moving flex; no BOM sourcing decision until confirmed prices with VAT+MOQ+stock.
- See BOM_W_IND_29.csv and MATRIZ_W_IND_29.csv for traceable candidates and open gates. Diotronic Zaragoza is **auxiliary**, local inventory unverified, no purchases.

## Official upstream audit, 29 October 2026 — read-only, compared with pinned SHAs in 19-alternativas

| Author / license | Current branch and HEAD | 28 Oct reference | Recent development |
|---|---|---|---|
| mark-belbin/simple-wireless-power GPL-3.0 | master 7c7858c0 | 7c7858c0 | unchanged; creator PR #1 merged 2021; cannot inherit his efficiency claims |
| wisp/wisp5-hw BSD-2-Clause | master 08332bc3 | 08332bc3 | unchanged, PR #1 in 2015 |
| wisp/wisp5 BSD-2-Clause | **640kHz** 604eee2d | d978a697 | diverged **+68/-11**, NOT a fast-forward |
| espressif/esp-now Apache-2.0 | master c3b5f9be | c3b5f9be | unchanged, PR #153 closed Feb 2026 |
| openthread/openthread BSD-3-Clause | main e577777c | 7009584d | +14/-0, link/radio/CLI changes, open PR #13819 updated 29 Oct; release v2026.10.0 |

Only original ideas and maker datasheet pinout referenced, **zero external code or CAD copied**. OOMWOO official main f01a1b2, its #79 cleaning-jobs, C mechanics, Codex counterpart and legacy dirty Xiaomi worktree untouched. We publish only to **our** Valdi320/Valdo W branch/PR #9 and keep author licenses with owners.

## Measured versus not measured

**Software:** source generator + 29 synthetic tests; native KiCad CI will attest ERC and netlist when successful. **Physics:** 0 fabricated PCB, 0 power tests, 0 calibrated shunts, 0 FOD tests, 0 RF, 0 EMI, 0 thermal, 0 real dock, 0 lithium, 0 batteries connected. ERC zero would not validate pin analog behavior or a PCB footprint. **Next gate:** independent normally-OFF RX power-good/cut + TX-side FOD and thermal protection with qualified real parts and reverse blocking, in native schematic, then SPICE/vendor models; any resistive hardware trial requires separate authorization and safety process.
