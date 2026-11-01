# W-IND-103 — finite-value gate for manufacturer WPT data

Date: 2026-11-01. Scope: original W-only analysis in VALDO. This milestone hardens the existing ST AN4913 Rev. 2 data parser; it does not change the power architecture or any hardware.

## Material defect reproduced

The W-IND-102 parser checked positivity with `min(... ) <= 0` and checked the power identity with `abs(V_EH * I_EH - P_EH) > 0.0051`. IEEE-754 NaN makes both comparisons false. The old guard therefore accepted:

- `P_EH = NaN` while H, V and I were positive;
- `V_EH = +Inf` and `P_EH = +Inf`, because `Inf - Inf = NaN`.

A report could then carry NaN into max/min results; Python's default JSON encoder emits the non-standard token `NaN`. That can poison a manufacturer-data power gate and downstream BOM decisions without an obvious exception.

The two false acceptances are reproduced in the regression test and deterministic evidence script against the exact pre-fix guard at baseline commit `be2dbbbc`.

## Implemented correction

The shared W-IND-102 validator now rejects malformed rows before any power calculation:

- all four analog columns must be exact built-in int/float values (booleans, strings and None rejected);
- every value must be finite and positive;
- AM must be an exact integer 10 or 100;
- V_EH × I_EH must remain finite and agree with P_EH within the existing 0.0051 mW tolerance;
- missing fields, overflow, wrong point count, wrong H-field grid and duplicate points remain rejected.

The valid 22-point dataset is unchanged. W-IND-102 maxima and the original conditional decisions remain unchanged.

## Reproduce

From `research/2026-10-28-independent-wpt-sensor-v01`:

```sh
python3 -m py_compile w_ind_102/w_ind_102.py w_ind_103/w_ind_103.py w_ind_103/test_w_ind_103.py
python3 -m unittest -v w_ind_102.test_w_ind_102 w_ind_103.test_w_ind_103
python3 w_ind_103/w_ind_103.py --out w_ind_103/RESULTADO_CI.json
```

W-IND-103 adds 10 deterministic test methods (with subtests covering each analog field and malformed type). The existing W-IND-102 tests remain in the same workflow. The GitHub Actions artifact is generated from the exact branch commit; no test result is claimed until that run completes.

## Architecture decision remains separate

| Problem | Decision |
|---|---|
| Dock charging | Separate battery/BMS/charger safety case; disconnected and out of scope |
| Active module around 400 mW mean / 1.5 W peak | NFC EH is NO-GO; use a qualified regulated WPT design only after FOD, thermal, offset, EMI and independent local cut evidence; otherwise retain a locking service connector |
| First non-critical microsensor | Conditional target <=0.25 mW mean, <=5 mW for <=10 ms with local buffer; actual tag antenna field, cold-start, ESR, leakage and recharge remain unmeasured |
| Data | ESP-NOW first candidate for a small one-hop Espressif network; OpenThread only if IPv6 mesh/multi-hop is needed; application ACK, CRC, sequence, timeout, bounded retries and authenticated privacy required |
| WISP5 | Only worth considering for passive micro-sensors if reader/antenna/cost are justified; firmware branch is divergent, no code reused |
| Critical stop | Local hardwired fail-safe; never rely on radio |

The ST source remains [AN4913 Rev. 2](https://www.st.com/resource/en/application_note/an4913-energy-harvesting-delivery-impact-on-st25dvi2c-series-behaviour-during-rf-communication-stmicroelectronics.pdf), Tables 1, 4 and 5. The source table is retained unchanged in `w_ind_102/AN4913_REV2_EH.csv`. The ST25DV64KC EH reference maximum remains 12.593 mW at AM10 / 5.5 A/m RMS and 8.640 mW at AM100; that is not a qualification of the 54 mm X-NUCLEO antenna.

## BOM and local procurement

No hardware changes or purchases. The parser fix adds **0.00 EUR** incremental component cost. Diotronic Zaragoza remains an auxiliary source; exact ST25DV64KC/X-NUCLEO listings, local stock, MOQ and VAT-inclusive price are not verified. Existing external reference only: DigiKey ST25DV64KC-IE8T3 1.8876 EUR VAT-inclusive (chip only; stock indication and shipping are not local Diotronic stock). The 47 uF buffer remains an unselected calculation candidate; ESR, leakage, DC-bias derating and temperature rating are not yet specified. Critical WPT/FOD/cutoff parts remain unselected and require traceable specialist documentation.

## Ownership and upstream review (2026-11-01)

No external code or CAD copied and no external repository edited.

| Owner/project | Current branch HEAD | Pin comparison / review |
|---|---|---|
| mark-belbin/simple-wireless-power, GPL-3.0 | master `7c7858c0dd7040801b6f191df1396115560218f0` | Matches registered pin; PR #1 merged (TX board v1.1); its 100 kHz series-series demonstrator and author's efficiency are not our qualification |
| wisp/wisp5-hw, BSD-2-Clause | master `08332bc398aa3350d351ef2aaac163f8007cffda` | Matches pin; PR #1 merged (TX/RX breakout pins and tuning changes) |
| wisp/wisp5, BSD-2-Clause | branch 640kHz `604eee2dffaeba3a270de61cf3dae887a33309c2` | Diverged from recorded `d978a6978ad23ccd6c44dd55430973b04a3d4a9b`: 68 ahead / 11 behind, merge base `f8243221...`; PR #40 is an old information-only PR on 436kHz; PR #36 merged to 640kHz_experimental, not the current 640kHz branch. Current README confirms 640 kHz link frequency. No fast-forward or reuse |
| espressif/esp-now, Apache-2.0 | master `c3b5f9be245f1a80db9cb938600566aa6a8dd1e5` | Matches pin; PR #153 closed unmerged; README describes one-to-many/many-to-many transport and security example, not power delivery |
| openthread/openthread, BSD-3-Clause | main `c6872259f4194fb76c7d333bda209343e8c88e71` | 21 commits ahead of pin `7009584d...`; #13800 and #13821 merged 31 Oct; #13824 scheduled-TX simulation, #13827 mbedTLS config and #13828 joiner memory PRs open. No code reused |

OOMWOO official `makerspet/oomwoo` main is `f01a1b295f462da5ab8d5f021a3f741cbd2b47df` (29 Oct, star-history refresh). Upstream cleaning-jobs PR #79 remains open at `8f444b5a...`; this WPT milestone does not target it. The local VALDO_OOMWOO adaptation audit still marks copied CAD references as reference-only/not installed; WPT_DATOS_V01 remains bench-only. No adaptation files changed.

VALDO own PR #9 is still draft/open, head `be2dbbbc...` before this milestone; no review submissions or inline review threads were returned. The local checkout is stale at W-IND-12 and has an unrelated untracked Python cache; it was not modified. This update is applied only to the verified remote W branch with an expected-head lease.

## Evidence limits and next gate

Classification: deterministic software/data-integrity tests over manufacturer-supplied values. This is not an electromagnetic simulation, a measurement of the tag board, or a safety approval. Physical measurements: 0; EM simulations: 0; battery/BMS/dock connected: false; hardware approved: false.

Next useful physical gate remains blocked until an explicit safety process and authorization exist: measure actual field at the selected tag antenna, V_EH/I_EH under the real duty cycle, cold start, buffer ESR/leakage/derating, reader input energy, offset and temperature on an isolated low-voltage fixture. No lithium, battery, BMS, motor, pump or station connection.