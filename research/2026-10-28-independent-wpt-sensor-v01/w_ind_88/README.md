# W-IND-88 — NFC blackouts, retries and instantaneous energy gate

**1 November 2026. Digital W-only milestone, new independent repairable robot. No Xiaomi OEM, battery/BMS, charger dock, motor, purchase, energy or fabrication.**

## Verified improvement

W87 checked continuous average load and a *single* event. W88 adds an original analytic **time-ordered energy ledger** for communication blackouts, instant clustered retransmission costs, recovery and capacitor saturation. It reports precisely the first failure: `BURST`, `RF_BLACKOUT` or `RECHARGE_WINDOW`. Source points are from **ST AN4913 Rev2 p7** (manufacturer bench, not our measurement), reused from own W86 module; radio blackout (no EH during communication), constant conversion efficiency, event energy and effective capacitor are *hypotheses*, not observations.

**One synthetic case:** ST H=0.5 A/m AM100 2.310mW; 80% hypothetical converter, idle 0.1mW, each attempt 1mJ, 100ms blackout per second, 1200µF **effective** ideal capacitor, 3.30→3.00V window, precharged initially. Reserve 1.134mJ. **One attempt** leaves 0.124mJ after blackout and the model recovers. **Two immediate attempts**, including a retry, fail in cycle 1 by 0.866mJ even though the hypothetical 3-cycle mean budget remains *positive*. Required ideal capacity for 2 attempts + blackout idle ≥**2126.984µF effective**, 77.25% more; does not account for ESR, V droop or cold start. ST AM10 at this weak field (0.360mW author point) with 1s intervals **fails cycle 2**; 10s intervals survive 3 modeled cycles, which does NOT prove RF communication, FOD or continuous harvesting. The model never authorizes hardware.

| Pilot | Result |
|---|---|
| AM100 one attempt/1s, three cycles | Model PASS, *hardware BLOCKED* |
| AM100 retry clustered with first attempt | Model FAIL (burst), 0.866mJ short |
| AM10 one attempt/1s | Model FAIL cycle 2 |
| AM10 one attempt/10s | Model PASS, *hardware BLOCKED* |

**Reproduce** from repo root:

```sh
python3 -m unittest discover -s research/2026-10-28-independent-wpt-sensor-v01/w_ind_88 -p 'test_*.py' -v
python3 research/2026-10-28-independent-wpt-sensor-v01/w_ind_88/w88_nfc_rf_window.py > /tmp/w88.json
sha256sum -c research/2026-10-28-independent-wpt-sensor-v01/w_ind_88/expected.sha256
```

23 adversarial Python tests and deterministic JSON SHA256; dedicated GitHub Actions artifact. No real radio/NFC protocol simulation. Instant burst assumed before harvesting, one fixed ST setup; no actual field pose or offset, RFID+EH coexistence, cold start, capacitor ESR/fuga, load/voltage regulation, thermal, EMI, FOD, metal/water or autonomous cutoff. `hardware_release=BLOCKED` on **every** result.

**Three distinct subsystems:** Dock charging needs separate controlled WPT/FOD/temp/EMI and independent normally-OFF cutoff, battery/BMS disconnected. Intermodule WPT only a possible *noncritical intermittent microsensor*; serviceable cable remains economic baseline. ESP-NOW vs OpenThread are **data links**, not power, and require application ACK, CRC, sequence, timeout, privacy via real encryption, recovery, retry power and independent emergency stop. WISP only micro-sensing. No motor/pump WPT.

**Sources:** [ST AN4913 Rev2 p7](https://www.st.com/resource/en/application_note/an4913-energy-harvesting-delivery-impact-on-st25dvi2c-series-behaviour-during-rf-communication-stmicroelectronics.pdf#page=7) and [ST25DV04KC datasheet](https://www.st.com/resource/en/datasheet/st25dv04kc.pdf). Third-party code not copied; creators/HEAD comparison and provisional BOM in [BOM_DECISION.md](BOM_DECISION.md).

**Next gate:** source concrete reader+antenna and receiver characteristics, measure field, total reader energy, complete radio events/retries and capacitor cold-start (only if later approved isolated resistive bench), qualify FOD/temp/EMI/cutoff; compare delivered cost vs retained cable. No real testing or lithium until safety protocol and explicit authorization.
