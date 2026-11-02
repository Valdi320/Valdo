# W-IND-15 — KiCad pin-level prototype of dual TX cutoff (29 October 2026)

**Scope: our new independent open vacuum robot, W electrical work ONLY.** Does NOT modify or depend on Xiaomi OEM electronics/battery/dock, OOMWOO upstream, C mechanical sector, cleaning-jobs PR #79, or third-party sources.

## Material improvement
The previous W-IND-14 diagnostic was a *two-resistor abstract switch model*. This increment provides a **reviewable editable KiCad schematic** and a separate canonical pin/net contract of two **actual Texas Instruments TPS22918DBVR SOT-23-6** candidates in series on a nominal **5 V** bench-only TX rail. Pin mapping (per TI): VIN1, GND2, ON3, CT4, QOD5, VOUT6. The reference explicitly leaves CT/QOD unconnected; the manufacturer's datasheet allows unused CT and QOD to float, but **this is not approval of our power architecture**. The external ON_A / ON_B nets are distinct and individually pulled to ground through hypothetical 100 kΩ resistors. MID has 22 kΩ to ground and TX_OUTPUT has 1 kΩ to ground for a proposed unloaded diagnostic. The QOD issue from W-IND-08 cannot be masked as a safety-rated cutoff.

```text
VIN_5V -- U1 TPS22918 -- MID -- U2 TPS22918 -- TX_5V_CUT
                          |                       |
                        22 kΩ                  1 kΩ
                          |                       |
                         GND                     GND
ON(U1) = EN_A -- 100 kΩ --> GND
ON(U2) = EN_B -- 100 kΩ --> GND
```

**Do not build, energize, use for charging, or connect any TX coil or robot.** The power path is only a drafting/coordination skeleton. No connector, decoupling, protection fuse/eFuse, real reverse-block mechanism, powered independent supervisor, FOD circuit, temperature shutdown, physical cutoff qualification, PCB, ground isolation, load transient, damping, ESD or probe validation has been established. An ordinary load switch is not a safety-rated isolation device. The two EN nets being named differently does **not** guarantee independence: driving both from a shared MCU or rail still creates a common-cause fault. No KiCad CLI/ngspice available; **no ERC, SPICE, fabrication check, or hardware measurement was run**.

## Reproducible checks
Edit in KiCad (v7-compatible reference syntax; not yet opened in KiCad). The standalone JSON records each physical pin and label position as a second representation to check. Run in this directory:

```sh
python3 -m unittest -v test_w_ind_15_pin_contract
```

The tests verify expected pin/connectivity maps against label anchor coordinates, explicitly unconnected QOD/CT pins, the six component instances, and intentional negative cases (shared EN, bypass, QOD short, missing bleeder, bad pin numbering, false safety claims). They are **static/software tests**, not electrical rule checking or a real test of a two-cut safety function.

## Independent systems and decision
- Sensor WPT: draft this power-cut *interface only* and preserve a removable wired fallback until efficiency, heat, offset, EMI, FOD, no-load consumption and real failure response are measured.
- Dock power + lithium charging: **separate scope, still disconnected and not part of this schematic**.
- ESP-NOW telemetry vs OpenThread: independent **data** links; ACK at application, CRC, epoch+sequence, expiration, authenticated transport required. Neither can grant local emergency safety or physical TX permissive.
- WISP5 is relevant only to suitably low-duty RFID sensing, not motors/pumps.
- Mechanical C owns printed supports, mating, dimensions and fatigue. No compatibility is assumed.

## Source owner, branches, licenses and 29/10/2026 audit
The 28/10 pinned SHAs in `19-alternativas-abiertas-para-robot-independiente.md` were compared with project HEAD, not copied: [mark-belbin/simple-wireless-power](https://github.com/mark-belbin/simple-wireless-power) GPL-3.0 master **7c7858c**, unchanged; [wisp/wisp5-hw](https://github.com/wisp/wisp5-hw) BSD-2-Clause master **08332bc**, unchanged; [wisp/wisp5](https://github.com/wisp/wisp5) BSD-2-Clause default branch **640kHz** HEAD **604eee2** vs pin d978a69 is **68 ahead / 11 behind** (DO NOT fast-forward); [espressif/esp-now](https://github.com/espressif/esp-now) Apache-2.0 master **c3b5f9b**, unchanged; [openthread/openthread](https://github.com/openthread/openthread) BSD-3-Clause main HEAD **51aa078** is **9 ahead** of pinned 7009584. Relevant [OpenThread v2026.10.0 release](https://github.com/openthread/openthread/releases/tag/v2026.10.0) exists; not imported. [makerspet/oomwoo](https://github.com/makerspet/oomwoo) master/main HEAD **1c2bd43**; own W PR #9 only. Source data for TPS22918 pin and limits: [TI product/datasheet](https://www.ti.com/product/TPS22918). Original VALDO schematic symbols and contract created without copying third-party code or CAD.

## BOM/pricing and actionable next gate
See `BOM_W_IND_15.csv`. Diotronic is an **auxiliary** source for passives, not an assumed supplier of TPS22918 or safety devices. Exact Diotronic branch inventory, 22k/100k resistor options, minimum orders and shipping; TME/Mouser/DigiKey landed prices are **unverified**. Every unqualified part remains **not selected**. The schematic intentionally does not imply the robot is cheap, powered or safe.

**Next gate:** perform KiCad schematic open + ERC, independently test component-specific reverse-current/body diode/ESD/EN brownout behavior, add separate local FOD+thermal and physically independent inhibit path, then electrical SPICE and fault injection. Only afterward can an independently authorized isolated resistive bench experiment be proposed. Battery/BMS/dock must stay disconnected.
