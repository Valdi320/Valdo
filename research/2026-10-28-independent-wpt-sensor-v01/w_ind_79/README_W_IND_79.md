# W-IND-79 — Asynchronous undervoltage fault latch: detect what ADC sampling misses

**31 October 2026.** Original digital work in VALDO scope W. Robot NEW/open/locally repairable; Xiaomi X20 Pro battery, firmware, station and circuit transplant CANCELLED. W79 modifies no shared local checkout, author repo, OOMWOO, or cleaning-jobs PR #79. No installed or approved physical protection.

## One meaningful improvement beyond W78
W78 derives a conditional lower voltage bound from *globally bounded slew rate*. A rapid step/dropout can invalidate that assumption. W79 models a DIFFERENT necessary safeguard: a separately supplied, asynchronous undervoltage detector whose FAULT persists until a local, stable, explicitly authorized reset, and whose output cuts an optional noncritical WPT sensor independently of ACK or radio availability.

The executable model tests **continuous piecewise-constant synthetic events**, not physical RF or comparator response:
- RX reads 3.30 V at 0 and 10 ms, but is 2.50 V from 4 to 5 ms. Both sampled values pass; one hidden 1000-us fault exists.
- With **assumed, NOT datasheet-certified** 200-us maximum detector reaction, the ideal monitor captures this 1000-us event.
- A 100-us excursion is MISSED by that same assumed 200-us monitor. If the monitor supply itself disappears, detection/latch retention is UNKNOWN and blocked.
- The separate StickyPermit logic model starts OFF; a power fault latches OFF; radio ACK never rearms; explicit local reset requires stable voltage for 100 ms (hypothetical) plus alive monitor, temperature and FOD permissions.

These observations **do not prove** real capture, independent supply hold-up, retention across full collapse, comparator response, latch, external switching path or safety. The code does NOT actually sample asynchronously: event traces are synthetic inputs. Every result says hardware_approved=false, real_pulse_capture_proven=false and critical_stop_authorized=false. A bench_claim is not authenticated evidence. Neither a generic comparator module nor GPIO/firmware alone qualifies.

## Reproduce
From this directory, on Python 3.10+ (stdlib only):

    python3 -m unittest -v test_w79.py
    python3 w79_async_uvlo_gate.py --input TRACE_SYNTHETIC.json --output W79_REGENERATED.json
    cmp W79_EVIDENCE_SYNTHETIC.json W79_REGENERATED.json

26/26 digital tests passed locally before publication. GitHub CI verifies tests and byte-identical JSON. No battery, motor, station, printer, instrument, workshop power or third-party firmware was touched.

## Interfaces and verification gates
1. **Power for detachable sensor**, not dock: the first candidate is a noncritical sensor 1–20 mW. Require independent UVLO detecting the actual regulated RX rail, threshold tolerance/hysteresis, worst-case over-temperature response, monitor supply survival through drop, sticky trip and local-only rearm. No wire to the moving bumper by default.
2. **Independent cut**: comparator+qualified latch+normally-OFF switch is a block diagram/requirement, NOT a ready schematic. Hardware must fail OFF even if the MCU, app ACK, ESP-NOW or OpenThread disappear. Confirm backfeed paths, FOD, temperature, EMI, moisture and coil offset in an authorized isolated resistive bench; no Li-ion/BMS.
3. **Dock charging**: independent, unimplemented. No lithium charging, BMS modification or OEM transplant.
4. **RF data**: ESP-NOW preferred only tentatively, OpenThread alternative; app ACK, CRC, seq, epoch/timeout, local private keys and recovery all remain required independently. WISP5 is only a secondary micropower RFID sensor study. No RF for cliff, bumper or motor emergency stops.
5. **Mechanical ownership**: C owns retention/geometry and physical offset; W owns electrical safety and WPT; no cross-overwriting or IF14 edits.

## Source provenance, branch heads and reviews (checked 31 October 2026)
Recorded baseline SHAs are from 19-alternativas-abiertas... (28 October); independent author HEADs queried, no code or CAD copied:
- mark-belbin/simple-wireless-power GPL-3.0, master 7c7858c0dd7040801b6f191df1396115560218f0 = baseline; power-stage author test does not qualify our sensor FOD/regulation.
- wisp/wisp5-hw BSD-2-Clause, master 08332bc398aa3350d351ef2aaac163f8007cffda = baseline.
- wisp/wisp5 BSD-2-Clause, 640kHz HEAD 604eee2dffaeba3a270de61cf3dae887a33309c2 **diverged** from baseline d978a6978ad23ccd6c44dd55430973b04a3d4a9b (68 ahead/11 behind; not a linear update). Author HEAD last commit 25 Apr 2022, PR #40 open.
- espressif/esp-now Apache-2.0, master c3b5f9be245f1a80db9cb938600566aa6a8dd1e5 = baseline.
- openthread/openthread BSD-3-Clause, main b6d0f06db304055f5866ff6e3c67370b54c81b15 +18/0 from baseline 7009584d..., 31 Oct 2026 commits include radio target power API and CLI updates; PR #13821/#13822 OPEN, not imported.
- makerspet/oomwoo official main f01a1b295f462da5ab8d5f021a3f741cbd2b47df (29 Oct chart only); PCB main 87aa7d386af2cef9fd083141b3a733598b3d3f5a and firmware main ce05f2660f899c3f78c8df2b6391d0f3442e3bff (31 Oct) owned by OOMWOO. VALDO master 8a6030bd... and PR #9 owned by Valdi320. Local shared Valdo checkout is dirty on codex/instrucciones-punto-dulce-20261029: leave UNTOUCHED. Current W79 only adds new files to own W branch via GitHub.

Links: https://github.com/mark-belbin/simple-wireless-power ; https://github.com/wisp/wisp5-hw ; https://github.com/wisp/wisp5/tree/640kHz ; https://github.com/espressif/esp-now ; https://github.com/openthread/openthread ; https://github.com/makerspet/oomwoo .

## Candidate sourcing, unapproved
TI TPS3700 voltage monitor has adjustable threshold, OD output, 5.5 uA **typical** supply current (manufacturer source: https://www.ti.com/product/TPS3700). An RS product page calls 2.2 us a **typical** response for TPS3700DDCT, not verified worst-case or a full latched cut (https://es.rs-online.com/web/p/comparadores/8120449). Treat as evidence for investigation only, NOT a selected component. Diotronic public listing MDIO3468 LM393 module says EUR 4.24 incl VAT, catalog AVAILABLE, but no traceable response, independent fault latch, or Zaragoza in-store stock verified: https://diotronic.com/varios/18038-modcomparador-voltaje-lm393 . Neither candidate has a finished safe circuit; no purchase. TME/Mouser/DigiKey exact quantities/final VAT+shipping quote PENDING. BOM_W79.csv lists their status and baseline service cable.

## Blocked next gate
Obtain actual RX/regulator behavior, worst-case comparator delay over temperature/voltage, latch behavior under loss of its OWN supply, hardware independent cut and real probe requirements, and a supplier-traceable BOM with local inventory checks. Follow with authorized isolated low-power **resistive** bench tests and calibrated pulse injection. Historic W18 ERC has three electrical issues; FOD/heat/EMI and full-system WPT remain unvalidated. A theoretical fault detector is not permission to energize any system.
