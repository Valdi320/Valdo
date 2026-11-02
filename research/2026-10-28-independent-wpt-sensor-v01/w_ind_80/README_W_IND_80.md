# W-IND-80 — audit of incompatible 3.3 V supervisor threshold window

31 October 2026. Own W-only contribution for a NEW open, repairable robot. No Xiaomi OEM electronics, BMS, battery, dock, firmware, motors, or OOMWOO code changed. No hardware fabricated, energized, purchased or installed.

## New material finding

For the **synthetic** first low-power sensor requirements of a 3.30 V regulated rail with ±5% tolerance and minimum functional voltage 3.00 V, the normal rail can reach 3.135 V. TI's TPS3840 family specifies a fixed falling threshold 1.6–4.9 V in nominal 0.1 V increments and **±1.5% maximum threshold error** (manufacturer statement; see source). A supervisor nominal threshold T must satisfy both:

- Worst-case low falling threshold T×(1−0.015) >= 3.00 V, so T >= **3.045685 V**.
- Worst-case high falling threshold T×(1+0.015) <= 3.135 V, so T <= **3.088670 V**.

**None of the 34 0.1 V grid values lies in that interval.** This is a static impossibility result for that particular family and synthetic system envelope, even BEFORE release hysteresis and transient delay:
- 2.80 V: low trip 2.758 V, below 3.00 V floor.
- 3.00 V: low trip 2.955 V, below floor.
- 3.10 V: low trip 3.0535 V, but high trip 3.1465 V exceeds minimum normal rail 3.135 V.
- 3.05 V would meet both *static* inequalities but is **not** a 0.1 V family-grid value and is not asserted to be purchasable.

Do not select or purchase a TPS3840 fixed-threshold variant for this rail + floor envelope without revisiting the **actual measured regulator and load specifications**. This finding does not prove that any existing robot rail is 3.3 V ±5%, nor that its sensor requires 3.0 V; both inputs are hypotheses taken from the previous W77–W79 synthetic exploration.

The published verifier uses Python Decimal arithmetic, rejects nonfinite/invalid configurations and enumerates the full nominal threshold grid. Its safety outputs remain FALSE even when a static mathematical candidate exists. A passing static inequality is NEVER permission to power hardware. No datasheet release-hysteresis worst-case bound, independent monitor rail, propagation to a normally-OFF transistor, latch retention, transient recovery, FOD, heat, EMI, wetness or coil-offset test is certified here.

## Reproduce, software only

Run from this directory with Python 3.10+ stdlib:

    python3 -m unittest -v test_w80.py
    python3 w80_threshold_window.py --input SCENARIO_SYNTHETIC.json --output W80_REPORT.json

The dedicated GitHub workflow runs these checks and uploads the deterministic W80_REPORT.json artifact tied to the published commit. The report is a mathematical decision gate, not a simulator of semiconductor dynamics.

## Design decision and boundaries

The existing W79 independent asynchronous monitor and sticky OFF trace remains a DIGITAL MODEL. W80 adds a *component tolerance feasibility gate* that W79 did not have. TI TPS3840PL28DBVR had been discussed by a separate Codex assistant in A62 as a conceptual 2.8 V supervisor, **not** published here as our hardware and not copied as code. This W80 evaluation prevents mistaking that candidate for a guaranteed 3.0 V minimum rail protector.

Three different interfaces remain separate: (1) dock wireless charge **out of scope**, no lithium or charging; (2) low-power detachable module WPT requires a qualified independently cut, thermally/FOD-protected TX and a validated regulated RX; (3) radio data (ESP-NOW tentative, OpenThread alternative) needs private commissioning, application ACK/CRC/sequence/epoch/timeout. Neither ACK nor RFID harvesting stops a motor. WISP remains micropower RFID research, no adopted sensor. A removable short wired harness remains the default until whole-life economics and safe measured WPT prove an advantage.

Options: choose a different proven supervisor architecture / regulator window after measuring real values; adopt a separately qualified cutoff and energy reserve; or keep a repairable cable. No WPT for motors or pumps from this calculation. Mechanic C retains CAD and geometry; no PR #79 cleaning-jobs changes.

## Provenance and fresh author revisions (checked 31 Oct 2026)

- mark-belbin/simple-wireless-power GPL-3.0, master HEAD 7c7858c0dd7040801b6f191df1396115560218f0 = pinned, latest 8 Jun 2021; historical merged PR #1. Its 100 W transmitter does not establish a safe 3 mW sensor.
- wisp/wisp5-hw BSD-2-Clause master HEAD 08332bc398aa3350d351ef2aaac163f8007cffda = pinned, 16 Jun 2017.
- wisp/wisp5 BSD-2-Clause default **640kHz** HEAD 604eee2dffaeba3a270de61cf3dae887a33309c2 **diverged** from pinned d978a6978ad23ccd6c44dd55430973b04a3d4a9b (68 ahead, 11 behind). Latest HEAD commit 25 Apr 2022, PR #40 open. No assumed fast-forward.
- espressif/esp-now Apache-2.0 master HEAD c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 = pinned, last 10 Sep 2026 (IDF v6 fixes).
- openthread/openthread BSD-3-Clause main HEAD b6d0f06db304055f5866ff6e3c67370b54c81b15 (18 ahead of pinned 7009584dadc20cf20c20a6062f357dd572ba6885). 31 Oct radio target-power & CLI changes; author PR #13821/#13822 open; not incorporated.
- makerspet/oomwoo main HEAD f01a1b295f462da5ab8d5f021a3f741cbd2b47df (29 Oct chart change), PR #79 is separate cleaning-jobs and not touched. Valdi320/Valdo master HEAD 8a6030bda52a159493a42dc4bed245e722b876e8; W branch is the owned PR #9. Local Valdo checkout is dirty on a colleague branch and intentionally untouched.
- Master instructions read: decision 28 Oct, 19-alternativas, D22, cableado coordinator, VALDO_OOMWOO LEEME and WPT_DATOS_V01; C owns mechanical geometry and W owns electricity/RF.
- Other scheduled tasks checked: only independent W automation active; no other worktree touched. Source code and numeric analysis written independently (not copied from any external project).

Manufacturer: https://www.ti.com/product/TPS3840/part-details/TPS3840PL28DBVR ; datasheet identification TI SNVSB03E. Commercial checking: https://www.digikey.es/es/products/detail/texas-instruments/TPS3840DL28DBVR/10445099 is a *different open-drain DL28* listed around EUR 1.02850 incl VAT for one, excluding transport, and is NOT an approved drop-in substitute for PL28. No confirmed price or Zaragoza stock for the exact PL28 from Diotronic/TME/Mouser/DigiKey; buyer must verify current stock, VAT, MOQ, total delivery, datasheet revision and electrical characteristics before any purchase. Zero spending.

## Reproducible limits / next gate

The family specs are manufacturer documentation; all rail/sensor voltages are **synthetic hypotheses**, calculations are exact Decimal arithmetic, supplier price is a catalog observation, and real measurements = ZERO. This only rejects a specific static combination and cannot be extended to timing, pulse capture, source brownout, startup or release. Need a measured minimum RX voltage, guaranteed sensor operating range, supply tolerance, independent monitor supply, full VIT+/delay data, normally-OFF cut/backfeed/ERC, FOD/temperature/offset/EMI and authorization for an isolated resistive bench (battery/BMS disconnected).
