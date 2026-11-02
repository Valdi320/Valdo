# W-IND-28: TX/RX current sensing and WPT efficiency are NOT interchangeable

**29 October 2026 · VALDO own W sector · independent new robot · digital only.**

## Real engineering correction

W-IND-27 calculates a candidate **346.4mA nominal** INA301A1 trip from a 0.1-ohm shunt and 8.66-kohm LIMIT resistor for a hypothetical 5V / 300mA healthy / 400mA abnormal pilot. **The RX load and the TX input are different current domains.** A TX shunt must not inherit an RX threshold without rederivation.

Hypotheses: TX supply 5V, regulated RX 5V, healthy RX 0.300A (1.5W), fault RX 0.400A (2W), input-to-output WPT efficiency between 55% and 90%. No selected coil, power stage, regulator or measurement. Auxiliary TX draw initially zero (optimistic). Formula: I_TX = (V_RX * I_RX / efficiency + TX_aux_W) / V_TX.

| Hypothetical case | TX input current |
|---|---:|
| Healthy RX 300mA at 90% | 333.33mA |
| Healthy RX 300mA at 75% | 400.00mA |
| Healthy RX 300mA at 55% | 545.45mA |
| Abnormal RX 400mA at 90% | 444.44mA |

To never trip during a healthy load, TX threshold must exceed **545.45mA**. To detect even the lowest TX draw of a 400mA RX fault, it must not exceed **444.44mA**. This is **impossible**, already before INA301, FOD, temperature, startup, transients and parasitic tolerances. At 75% a healthy RX demands 400mA input: W-IND-27's 346.4mA would falsely trip on TX. A strictly optimistic window would require efficiency_min > (300/400)*efficiency_max = **67.5%** (with eta_max 90%, no variable auxiliary draw), not yet demonstrated. That mathematical condition does NOT mean the protection works in real hardware.

## Decisions

| Location or subsystem | Result | Constraint |
|---|---|---|
| W-IND-27 threshold directly on TX input | REJECTED | Cross-stage threshold, healthy false trips |
| INA301 and shunt on regulated RX output | CANDIDATE ONLY | Local RX cutoff; loss of RX supply may disable sensing |
| Independent TX-side overcurrent cutoff | REQUIRED | Set with actual TX input range and switching transients |
| Independent primary FOD, temperature and reverse blocking | REQUIRED | Current-only test cannot ensure foreign metal safety |
| ESP-NOW/OpenThread with application ACK/CRC/sequence/timeout | DATA ONLY | Never an emergency-power path; neither transports power |
| WISP RFID energy harvesting | DEFERRED | Not an established 1.5W continuous supply |
| Charging dock, lithium cell, BMS | SEPARATE AND DISCONNECTED | No charging tests |
| Motors and pumps | NOT WPT DEFAULT | Power and losses have not been characterized |

Simple unregulated WPT reference and regulated protected WPT are not interchangeable; neither has measured losses, offset/EMI or FOD on our robot. This result prevents designing the INA301 in the wrong location in KiCad. Next step: establish a separate TX fault budget and a monitored RX power-good/cutoff schematic *before* electrical approval.

## Reproducible evidence

Original Python 3.10+ code: \`stage_current_envelope.py\` and \`test_stage_current_envelope.py\`. CI in \`.github/workflows/w-ind-28-stage-current.yml\` executes 28 unit tests and archives \`W_IND_28_EVIDENCE.json\`.

\`\`\`bash
cd research/2026-10-28-independent-wpt-sensor-v01/w_ind_28
python3 -m unittest -v test_stage_current_envelope
python3 stage_current_envelope.py > W_IND_28_EVIDENCE.json
\`\`\`

**Evidence level:** symbolic energy conservation and deterministic synthetic tests, NOT measurement/SPICE/ERC/EMC/hardware. The 55%-90% range is deliberately hypothetical; mark-belbin's measured 81.3% at his own operating point is NOT transferred to our device. A zero-current or brownout RX may fail silently, so current sense alone is insufficient for primary shutdown. Zero physical tests, no power approval.

## BOM: no new purchases

Parts from previous W-IND-27 are retained as unapproved **options**, not a new purchase instruction:

| Candidate | Diotronic / alternative | Historical VAT-inclusive estimate | Zaragoza local stock |
|---|---|---:|---|
| INA301A1IDGKR | Diotronic pending / DigiKey or TME | ~3.35 EUR | NOT VERIFIED |
| Vishay WSL2512R1000FEA 0.1ohm | Diotronic pending / TME | ~0.64 EUR | NOT VERIFIED |
| VPG Y44880R10000F9R 0.1ohm 4-terminal | Diotronic pending / Farnell | ~19.51 EUR | NOT VERIFIED |
| Independent eFuse / FOD / thermal sensor / supervisor | Diotronic only if traceable / Mouser, DigiKey, TME | PENDING selection | NOT VERIFIED |

Prices above are **historical estimates**, not current supplier quotes, no shipping included. Diotronic is auxiliary only; local existence, minimum purchase and traceability require checking before physical design. There is no authorization to buy. See BOM_W_IND_28.csv.

## Upstream provenance reviewed before write (2026-10-29)

The local owner's 00_DECISION_20261028_NO_TRASPLANTE_X20.md, 19-alternativas, D22, WPT_DATOS_V01 and W/C agreement were read. GitHub official HEAD compared with local recorded SHA: mark-belbin/simple-wireless-power GPL-3.0 **master 7c7858c unchanged**; wisp/wisp5-hw BSD-2-Clause **master 08332bc unchanged**; wisp/wisp5 BSD-2-Clause **640kHz 604eee2 vs saved d978a69, diverged +68/-11**; espressif/esp-now Apache-2.0 **master c3b5f9b unchanged**; openthread/openthread BSD-3-Clause **main e577777 vs saved 7009584, +14 commits** (radio/API/CLI changes). Relevant creator PRs #1, #1, #38, #153, #13819 examined; none grants safety. Only ideas and vendor specifications cited, **zero upstream code or CAD copied**. OOMWOO official main f01a1b2 reviewed; [OOMWOO PR #79](https://github.com/makerspet/oomwoo/pull/79) and other contributors completely untouched. Own [VALDO PR #9](https://github.com/Valdi320/Valdo/pull/9) only.

Reference: [TI INA301 SBOS713A](https://www.ti.com/lit/ds/symlink/ina301.pdf), [Simple Wireless Power](https://github.com/mark-belbin/simple-wireless-power), [W-IND-27](../w_ind_27/README_W_IND_27.md). No lithium connection, hardware, real dock or OEM transport.
