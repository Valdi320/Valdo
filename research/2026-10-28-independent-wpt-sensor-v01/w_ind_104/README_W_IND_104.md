# W-IND-104 — burst-energy and capacitor-recharge gate

Date: 2026-11-02. Scope: **new independent robot**, original W-only analysis in VALDO. This milestone does not use Xiaomi hardware, firmware, battery, BMS or dock. It corrects the first-microsensor energy budget before any component is selected.

## Material improvement

W-IND-102 calculated a 36.28 uF nominal buffer from the ST reference point, 3.3-to-2.0 V window, 80% discharge-path efficiency and 50% capacitance retention. That nominal figure did not also apply the **20% minimum capacitance tolerance** stated for the 47 uF candidate in the prior BOM.

W-IND-104 now accounts for both tolerance and retention, plus ESR, leakage, burst timing and recharge time. Under the explicit baseline assumptions below, the required nominal capacitance rises to **45.36 uF**. A 47 uF / ±20% candidate with a separate 50% retention stress factor has only **3.6% energy margin**. It is not a robust selection and is not approved.

## Reproducible baseline

Manufacturer point: ST AN4913 Rev. 2, Table 4/5, exact AM=10%, H=1.0 A/m RMS: **1.035 mW** at V_EH/I_EH. No interpolation is used.

Hypothetical non-critical sensor load:
- idle: 0.20 mW;
- burst: 5.0 mW for 10 ms every 1 s;
- arithmetic average at the load: 0.248 mW;
- burst energy at the load: 50 uJ;
- assumed capacitor discharge-path efficiency: 80%, so the buffer must provide 62.5 uJ.

Buffer stress assumptions (not measured component data):
- 47 uF nominal;
- minimum tolerance factor 0.80;
- separate capacitance-retention factor 0.50;
- 3.3 V down to 2.0 V;
- ESR 2 ohm;
- leakage 5 uA at 3.3 V;
- assumed source conditioning efficiency 65%;
- field present during 50% of the off-time;
- no harvested energy credited during the 10 ms burst.

Calculated result at AM10 / 1.0 A/m:
- effective capacitance: 18.8 uF;
- usable capacitor energy: 64.77 uJ;
- required buffer energy: 62.50 uJ;
- energy ratio: 1.036 (3.6% margin);
- end-of-burst terminal voltage after the 2 ohm ESR model: about 2.054 V;
- required reader-field duty during off-time: **41.57%**;
- at 50% field duty, recharge takes about **0.521 s** of the 0.990 s off-time: conditional pass;
- at 40% field duty, recharge is about 1.19 s and misses the next burst: no-go.

Sensitivity gates:
- 40% capacitance retention: insufficient stored energy;
- 25 ohm ESR: terminal voltage falls below 2.0 V;
- 30 uA leakage: recharge misses the next burst;
- 20 uA leakage: only a narrow conditional pass;
- AM10 / 0.5 A/m: required field duty exceeds 100%, so no-go even if the field were continuously present.

All 20 manufacturer points at H >= 1.0 A/m pass the analytical 50%-off-time scenario, but that is **not** an antenna, reader, board or robot qualification. The ST data uses its Class 1 antenna / 13.6 MHz tuning / 10 nF V_EH setup. It does not qualify the 54 mm X-NUCLEO tag antenna or the final printed geometry.

## Why this matters

The earlier 47 uF candidate appeared comfortable when tolerance was not included. With the actual ±20% minimum and a separate retention allowance, it is barely over the calculated energy threshold. A future capacitor must be selected from a full datasheet with minimum capacitance under DC bias and temperature, ESR at the pulse condition, leakage, voltage rating and lifetime. A 68–100 uF nominal part is only a value range to investigate, not a selected part.

The ST25DV64KC V_EH output is unregulated and can become high impedance when field or load conditions are insufficient. The reader is a separate powered device. Reader input energy, RF field generation, antenna matching, cold start, and the complete reader-to-tag efficiency are **excluded**. This is a sensor-side feasibility screen, not a claim that NFC is energy-efficient for the robot as a whole.

## Architecture decision — keep the three problems separate

| Problem | Current decision | Evidence / boundary |
|---|---|---|
| Dock charging | Keep the current OOMWOO contact-dock baseline; do not insert WPT into its charger/BMS path | Official dock is 20 V contact charging through replaceable pogo pins, 5 A fuse, SMAJ22A TVS, P-FET soft-start, current sense and MCU contact detection. No WPT in upstream. |
| Active modules (~400 mW mean / 1.5 W peak) | ST25DV energy harvesting is NO-GO. Default to keyed locking low-voltage connector; consider regulated WPT only after FOD, temperature, offset, EMI and independent local cut are evidenced | ST reference maximum is 12.593 mW, far below 400 mW. |
| First non-critical microsensor | NFC energy harvesting is conditional only if a reader/field already exists and the actual tag antenna passes field/duty/cold-start tests | This model requires at least 41.6% field duty during off-time at the selected reference point and assumptions. Reader overhead is excluded. |
| Passive micro-sensor alternative | WISP5 remains a research option only where a UHF RFID reader is already justified | It is a passive RFID/sensor platform, not a supply rail for motors, pumps or active modules. |
| Data | ESP-NOW is provisional for a small one-hop Espressif network; OpenThread only if IPv6 mesh/multi-hop is needed | Both need application ACK, CRC, sequence, timeout, bounded retries, authenticated privacy and explicit recovery. CRC is not authentication. |
| Critical stop | Local hardwired fail-safe only | No safety stop, motor inhibit or power cut may depend on radio. |

### WPT trade-off

- mark-belbin/simple-wireless-power is an open-loop series-series resonant demonstrator. Its author reports up to 100 W and 81.3% at 1–2 mm, but also reports hot resonant capacitors (up to about 70 C) and no feedback regulation/FOD. Those are author measurements, not ours. It is not a safety-qualified robot dock or module supply.
- A regulated WPT transmitter/receiver with FOD, thermal sensing, offset tolerance, EMI limits and an independent hardware cut is the only inductive route worth qualifying for an active module or dock. No controller, coil or safety part is selected; cost and efficiency remain pending.
- A locking connector remains the default for modules above the microsensor envelope until measured WPT losses and repairability justify removing the contacts.

## Data-link comparison

| Option | Strength | Cost/complexity | Decision |
|---|---|---|---|
| ESP-NOW | Connectionless Wi-Fi, one-hop peer network, simple for a few ESP32 modules; official component guide includes enhanced security examples | Must provision PMK/LMK or application AEAD; MAC send status is not application delivery; multicast privacy needs explicit treatment | First candidate if all nodes are Espressif and single-hop |
| OpenThread | IPv6/6LoWPAN, Thread mesh and sleepy end-device options; MAC/network security | More stack, commissioning and router/border-router work; mesh is unnecessary for modules on one chassis | Use only if multi-hop/interoperability is actually needed |
| WISP5 | Passive UHF backscatter/energy harvesting for very low-power sensing | Reader, antenna and timing infrastructure; not a general active data bus or power rail | Defer unless a passive sensor use-case exists |

The existing VALDO w_link.py protocol model has CRC16, session/sequence, application ACK, timeout, bounded retries and duplicate rejection. Its authenticated_transport field is still a **test stub**, not production cryptography. This milestone does not claim RF privacy has been implemented. ESP-NOW's send callback or a Thread MAC ACK is not a substitute for an application ACK. No radio can trigger the safety cut.

## BOM and local sourcing

No purchase, print, soldering or energization. The exact local Diotronic store is [Diotronic Zaragoza](https://www.diotronic.com/), Av. de Valencia 5, Zaragoza. A public exact listing for the selected ST tag IC or 47 uF candidate was not found; counter stock, MOQ and local final price remain pending.

| Item | Diotronic | Alternative / price with VAT | Availability | Decision |
|---|---|---|---|---|
| ST25DV64KC-IE8T3 tag IC | Exact public listing not found; local stock/price pending | DigiKey Spain: 1.37 EUR ex / **1.6577 EUR incl. VAT**, 2,838 shown, MOQ 1, 14-week manufacturer lead. Mouser Spain: 1.57 EUR shown (about **1.8997 EUR incl.** if ex-VAT at 21%), 1,267 shown, MOQ 1. TME exact IE8T3 not found | Online listings only; recheck before any purchase | Reference IC only; not a reader and not selected |
| Panasonic EEE-HA1A470WR, 47 uF / 10 V | Exact public listing not found; local stock/price pending | DigiKey Spain: 0.39 EUR ex / **0.4719 EUR incl. VAT**, 1,371 shown, MOQ 1 | DigiKey listing flags it **not recommended for new designs** | Rejected; ±20% tolerance leaves only 3.6% model margin before unqualified ESR/leakage/DC-bias effects |
| Buffer capacitor >=68 uF, low leakage | Diotronic catalogue search did not establish an equivalent with ESR/leakage data; local stock/price pending | No exact TME/Mouser/DigiKey part selected | Pending datasheet and stock check | Specification only; do not buy a generic 100 uF part by value alone |
| NFC reader and matched antenna | No exact part selected; stock/price pending | No qualified reader/antenna BOM | Pending | Reader input power and antenna geometry must be measured |
| Regulated WPT TX/RX, FOD and independent cut | Not sourced locally as a safety-critical set | Specialist distributors required; cost pending | Pending | No part selected; traceable electrical/thermal/FOD documentation required |
| W-IND-104 analysis and tests | Not applicable | 0.00 EUR incremental hardware cost | Published source and CI | No hardware BOM change |

The X-NUCLEO-NFC07A1 is a tag/evaluation board, not the RF reader that generates the field. Do not treat its catalogue price as the complete system cost.

## Upstream and ownership audit — 2026-11-02

No external code or CAD was copied. No external repository, OOMWOO source, adaptation copy, Xiaomi hardware or PR #79 was modified.

| Project / license | Branch HEAD checked | Comparison to registered pin / relevant review |
|---|---|---|
| [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) / GPL-3.0 | master 7c7858c0dd7040801b6f191df1396115560218f0 | Same as pin; PR #1 merged. Open-loop demonstrator only. |
| [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) / BSD-2-Clause | master 08332bc398aa3350d351ef2aaac163f8007cffda | Same as pin; PR #1 merged. |
| [wisp/wisp5](https://github.com/wisp/wisp5) / BSD-2-Clause | explicitly queried branch 640kHz, HEAD 604eee2dffaeba3a270de61cf3dae887a33309c2 | Registered pin d978a6978ad23ccd6c44dd55430973b04a3d4a9b: 68 ahead / 11 behind. PR #40 is on 436kHz; PR #36 merged to 640kHz_experimental, not current 640kHz. No fast-forward or code reuse. |
| [espressif/esp-now](https://github.com/espressif/esp-now) / Apache-2.0 | master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 | Same as pin; PR #153 closed unmerged; component guide has ECDH/AES-CCM security examples. |
| [openthread/openthread](https://github.com/openthread/openthread) / BSD-3-Clause | main c6872259f4194fb76c7d333bda209343e8c88e71 | 21 commits ahead of pin 7009584dadc20cf20c20a6062f357dd572ba6885; #13800/#13821 merged; #13813, #13819, #13824, #13825, #13827 and #13828 reviewed as open/active work. No code reuse. |

OOMWOO local clones remain clean at the pins in VERSIONES_UPSTREAM_BLOQUEADAS.json; official upstream has moved:
- makerspet/oomwoo main ad61099e222a9d8e8573bcda546380b4256a1902, 23 commits ahead of local pin 1c2bd43. PR #79 merged on 2026-11-01; it changes only the contributions/cleaning-jobs/Valdi320/README.md pointer plus star-history images. It is not a WPT PR.
- makerspet/oomwoo-pcb main ac8ac0b52254582be3acda9d3fddfd06cbbabd4f, 12 commits ahead of local pin 5a81c12. Updates add front/side/cliff/Hall/rear-IR sensor boards, pin/header/BOM changes and dock mounting holes/reference renumbering. The dock electrical topology remains contact/pogo based; no WPT.
- makerspet/oomwoo-firmware main fd8689f3, 8 commits ahead of local pin 33ee70d. Open PR #3 by xbattlax adds a watchdog; it remains another contributor's work and was not touched.
- makerspet/oomwoo-cad main 1e1c4091, 1 commit ahead; drive-wheel prototype update.
- oomwoo-one, oomwoo-install, oomwoo-ros2-tools, oomwoo_urdf, oomwoo_gazebo and oomwoo-esp32s3-cm are unchanged at their recorded pins.

The local adaptacion tree has no Git root; its WPT_DATOS_V01 contract and upstream pins were read, and no adaptation files changed. The shared local VALDO checkout has unrelated dirty/untracked work, so it was not used. This update is only on the owned remote W branch of VALDO, using a non-forced expected-head update. No other enabled automation or active Git/KiCad/FreeCAD/Codex process was found.

## Reproduce

From research/2026-10-28-independent-wpt-sensor-v01:

~~~
python3 -m py_compile w_ind_102/w_ind_102.py w_ind_104/w_ind_104.py w_ind_104/test_w_ind_104.py
python3 -m unittest -v w_ind_102.test_w_ind_102 w_ind_103.test_w_ind_103 w_ind_104.test_w_ind_104
python3 -m w_ind_104.w_ind_104 --out w_ind_104/RESULTADO_CI.json
~~~

The workflow runs the complete existing W suite plus 16 W-IND-104 tests and uploads RESULTADO_CI.json as an artifact.

## Limits and next gate

Classification: deterministic analytical software model using ST manufacturer data and explicitly labelled assumptions. It is not an electromagnetic simulation or physical measurement. Physical measurements: 0. Battery/BMS: disconnected. Motors/pumps/dock: untouched. Hardware approved: false.

The next gate is not another optimistic simulation: it is an authorized isolated low-voltage measurement of the actual reader/tag field, V_EH/I_EH, cold start, capacitor minimum C/ESR/leakage, reader input energy, offset and temperature. No lithium, battery, BMS, motor, pump or station connection.
