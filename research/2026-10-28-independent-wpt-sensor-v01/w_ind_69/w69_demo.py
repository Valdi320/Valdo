"""Reproducible synthetic counterexample: absent second path and open bleeder."""
from dataclasses import replace
import json
from .w69_discharge_envelope import Case, Node, screen


def main():
    base=Case((Node('TX',100e-6,5,1000),),.5,True,True,True)
    data={"milestone":"W-IND-69","measurement_type":"SYNTHETIC_UPPER_BOUND_NOT_HARDWARE",
          "single_ideal_rc":screen(base),
          "open_bleeder_one_hour":screen(replace(base,nodes=(Node('TX',100e-6,5,1000,True),),elapsed_s=3600)),
          "hidden_second_node":screen(replace(base,nodes=(Node('TX',100e-6,5,1000),Node('AUX',.001,5,1e6)))),
          "backfeed_unknown":screen(replace(base,backfeed_excluded=False)),
          "assumptions":["only physically isolated non-recharging capacitors","Rmax/Cmax/Vmax are declared hypothetical bounds","single-open fault model","screen thresholds are NOT safety limits"]}
    print(json.dumps(data,sort_keys=True,indent=2,allow_nan=False))


if __name__ == '__main__':main()
