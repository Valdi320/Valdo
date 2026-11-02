"""Reproducible SYNTHETIC ONLY proof of W67 false-safe model repair."""
import json
from dataclasses import replace
from tx_cut_power_screen import Fault, Interlocks, Switch, evaluate


def case(source_ok, supply_present, welded, qod):
    interlocks = Interlocks(source_ok=source_ok)
    fault = Fault.CLOSED if welded else Fault.HEALTHY
    out = evaluate(interlocks, Switch(fault, qod), Switch(fault, qod),
                   supply_present=supply_present)
    return dict(monitor_source_ok=source_ok, physical_forward_supply_present_assumed=supply_present,
                both_pass_elements_welded=welded, qod_connected=qod,
                permission_granted=out.command_on, possible_TX_energized=out.supply_to_tx,
                possible_sustained_QOD_shunt=out.any_sustained_qod_shunt)


def generate():
    return dict(evidence_type="SYNTHETIC_DC_TOPOLOGY_ONLY",
                physical_tests=0, hardware_approved=False,
                externally_powered=False, independent_protection_verified=False,
                source_monitor_deny_both_welded=case(False, True, True, False),
                physical_source_absent_both_welded=case(False, False, True, False),
                source_monitor_deny_welded_qod=case(False, True, True, True),
                source_monitor_deny_healthy_switches=case(False, True, False, False),
                known_unmodelled=["reverse_feed", "stored_energy", "transients",
                                  "FOD", "thermal", "EMI", "supply_voltage", "cutoff_response"])


if __name__ == "__main__":
    print(json.dumps(generate(), indent=2, sort_keys=True))
