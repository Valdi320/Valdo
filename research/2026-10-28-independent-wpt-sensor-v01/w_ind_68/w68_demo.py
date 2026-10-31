"""Print deterministic synthetic evidence; no physical measurements."""
import json
from dataclasses import replace
from tx_cut_power_screen import Interlocks, Switch, Fault
from .w68_residual import ResidualCase, screen


def main():
    base = ResidualCase(Interlocks(), Switch(), Switch(),
                        physical_source_present=False,
                        reverse_feed_excluded=True,
                        initial_downstream_v=5.0,
                        downstream_c_f=100e-6,
                        independent_bleeder_ohm=1000.0)
    data = {
        "hito": "W-IND-68",
        "evidence_type": "SYNTHETIC_RC_TOPOLOGY_ONLY",
        "hardware_approved": False,
        "physical_tests": 0,
        "lithium_connected": False,
        "source_disconnected_cap_still_charged": screen(base).as_dict(),
        "source_disconnected_after_500ms": screen(replace(base, elapsed_s=0.5)).as_dict(),
        "reverse_feed_not_excluded": screen(replace(base, reverse_feed_excluded=None)).as_dict(),
        "double_weld_source_present": screen(replace(base, physical_source_present=True,
            switch_a=Switch(Fault.CLOSED), switch_b=Switch(Fault.CLOSED))).as_dict(),
        "assumptions": ["single ideal lumped downstream capacitor", "ideal permanent bleed resistor",
            "no load", "no reverse feed only when explicitly assumed",
            "voltage/energy thresholds are illustrative, not certified"],
    }
    print(json.dumps(data, sort_keys=True, indent=2, allow_nan=False))


if __name__ == "__main__": main()
