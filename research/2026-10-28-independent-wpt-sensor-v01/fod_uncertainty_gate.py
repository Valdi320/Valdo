"""W-IND-10: offline FOD loss-uncertainty gate; original VALDO code.
NO physical FOD, Qi approval, GPIO, charging, radio control or energization.
"""
from dataclasses import dataclass
from enum import Enum
from math import isfinite

class Verdict(str, Enum):
    NOT_COMPARABLE = "not_comparable"
    SUSPECTED_EXCESS = "suspected_excess"
    INDETERMINATE = "indeterminate"
    BELOW_THRESHOLD = "below_threshold_NOT_fod_clear"

def num(label, x, minimum=0.0):
    if type(x) not in (int,float) or not isfinite(x) or x < minimum:
        raise ValueError(label + ": invalid finite number")
    return float(x)

@dataclass(frozen=True)
class Observation:
    scenario: str
    fixture: str
    coils: str
    load: str
    provenance: str
    pin_w: float
    pout_w: float
    uin_w: float
    uout_w: float
    xy_x_mm: float
    xy_y_mm: float
    gap_mm: float
    ambient_c: float

    def validate(self):
        for field in ("scenario","fixture","coils","load"):
            s=getattr(self,field)
            if type(s) is not str or not s.strip():
                raise ValueError("missing label: "+field)
        if self.provenance not in ("synthetic","bench_measured"):
            raise ValueError("must identify physical or synthetic provenance")
        pin,pout=num("pin_w",self.pin_w),num("pout_w",self.pout_w)
        if pout > pin: raise ValueError("output power > input; check units")
        num("uin_w",self.uin_w);num("uout_w",self.uout_w)
        num("gap_mm",self.gap_mm,0.01)
        for field in ("xy_x_mm","xy_y_mm","ambient_c"):
            x=getattr(self,field)
            if type(x) not in (int,float) or not isfinite(x):
                raise ValueError("invalid geometry/temperature "+field)
        if not -40<=self.ambient_c<=100: raise ValueError("ambient outside assumed domain")
        return self

@dataclass(frozen=True)
class Result:
    verdict: Verdict
    extra_loss_w: float | None
    uncertainty_bound_w: float | None
    lower_w: float | None
    upper_w: float | None
    reason: str
    installation_approved: bool = False
    physical_tx_enable_allowed: bool = False
    demonstrated_fod_clear: bool = False

def compare(base:Observation, evt:Observation, *, drift_w:float,
            diagnostic_threshold_w:float=.25, max_xy_mm:float=.5,
            max_gap_mm:float=.2, max_ambient_c:float=2.)->Result:
    """Worst-case DIFFERENTIAL DC loss bound, not metal-heating estimate.
    U=sum four independent absolute uncertainty bounds + drift (NOT RSS).
    """
    base.validate();evt.validate()
    udrift=num("drift_w",drift_w)
    threshold=num("threshold",diagnostic_threshold_w,0.000001)
    xy=num("max_xy_mm",max_xy_mm)
    gap=num("max_gap_mm",max_gap_mm)
    amb=num("max_ambient_c",max_ambient_c)
    if any(getattr(base,f)!=getattr(evt,f)
           for f in ("fixture","coils","load","provenance")):
        return Result(Verdict.NOT_COMPARABLE,None,None,None,None,
                      "fixture/coil/load/provenance mismatch")
    if (abs(base.xy_x_mm-evt.xy_x_mm)>xy+1e-12 or
        abs(base.xy_y_mm-evt.xy_y_mm)>xy+1e-12 or
        abs(base.gap_mm-evt.gap_mm)>gap+1e-12 or
        abs(base.ambient_c-evt.ambient_c)>amb+1e-12):
        return Result(Verdict.NOT_COMPARABLE,None,None,None,None,
                      "position, gap or temperature changed; recalibrate")
    delta=(evt.pin_w-evt.pout_w)-(base.pin_w-base.pout_w)
    u=base.uin_w+base.uout_w+evt.uin_w+evt.uout_w+udrift
    lower,upper=delta-u,delta+u
    if lower>=threshold:
        verdict=Verdict.SUSPECTED_EXCESS
    elif upper<threshold:
        verdict=Verdict.BELOW_THRESHOLD
    else:
        verdict=Verdict.INDETERMINATE
    return Result(verdict,delta,u,lower,upper,
                  "diagnostic only; neither low loss nor alarm proves metal state")

def example():
    p=dict(fixture="SYNTHETIC_NO_HARDWARE",coils="UNSELECTED_5V_PAIR",
           load="DUMMY_RESISTOR",provenance="synthetic",
           uin_w=.04,uout_w=.03,xy_x_mm=0.,xy_y_mm=0.,
           gap_mm=4.,ambient_c=25.)
    base=Observation("reference",pin_w=2.,pout_w=1.,**p)
    return {name:compare(base,Observation(name,pin_w=v,pout_w=1.,**p),drift_w=.05)
            for name,v in (("no_extra_loss",2.),("small_loss",2.12),
                           ("large_loss",2.5))}

if __name__=="__main__":
    for name,r in example().items():
        print(name,r.verdict.value,round(r.extra_loss_w,3),
              round(r.uncertainty_bound_w,3),"approved",r.installation_approved)
