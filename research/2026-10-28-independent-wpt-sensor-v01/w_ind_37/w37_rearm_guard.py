"""W-IND-37: abstract positive-local-rearm release-before-press reference model.

NO HARDWARE AUTHORISATION. The sample clock and all thresholds are hypothetical.
Power, charging, FOD, thermal, overcurrent and EMI are not qualified here.
This is original VALDO W-only specification/test logic, not embedded firmware.
"""
from __future__ import annotations
from dataclasses import dataclass
import argparse
import itertools
import json
from pathlib import Path

GOOD_SAMPLES = 3
RELEASE_SAMPLES = 2
PRESS_SAMPLES = 2
SAMPLE_MS_ASSUMED = 10

@dataclass(frozen=True)
class Frame:
    pg_mon: bool
    pg_rx: bool
    btn_a: bool = False
    btn_b: bool = False

@dataclass(frozen=True)
class Verdict:
    en_a: bool
    en_b: bool
    stage: str
    rail_good_streak: int
    cause: str

class GuardedRearm:
    """Requires healthy rails, both buttons RELEASED, then stable presses.

    All state is cleared immediately if either PG goes low. Power-up is OFF.
    A loss-of-power input is treated as a digital event; analog POR/pin failure
    remains unqualified. This does NOT describe the present W36 KiCad gates.
    """
    def __init__(self, good_samples=GOOD_SAMPLES, release_samples=RELEASE_SAMPLES,
                 press_samples=PRESS_SAMPLES):
        if min(good_samples, release_samples, press_samples) < 2:
            raise ValueError("sample thresholds must be >= 2 in this model")
        self.good_samples = good_samples
        self.release_samples = release_samples
        self.press_samples = press_samples
        self._reset()

    def _reset(self):
        self.stage = "WAIT_PG"
        self.good = 0
        self.release = 0
        self.press_a = 0
        self.press_b = 0
        self.seen_a = False
        self.seen_b = False

    def tick(self, f: Frame) -> Verdict:
        if not f.pg_mon or not f.pg_rx:
            self._reset()
            return Verdict(False, False, self.stage, self.good, "PG_LOST")
        if self.stage == "WAIT_PG":
            self.good = min(self.good + 1, self.good_samples)
            if self.good == self.good_samples:
                self.stage = "WAIT_BOTH_RELEASED"
                self.release = 0
            return Verdict(False, False, self.stage, self.good, "PG_QUALIFY")
        if self.stage == "WAIT_BOTH_RELEASED":
            self.release = self.release + 1 if not(f.btn_a or f.btn_b) else 0
            if self.release >= self.release_samples:
                self.stage = "WAIT_FRESH_PRESSES"
                self.press_a = self.press_b = 0
            return Verdict(False, False, self.stage, self.good, "NEED_RELEASE")
        if self.stage == "WAIT_FRESH_PRESSES":
            if not self.seen_a:
                self.press_a = self.press_a + 1 if f.btn_a else 0
                if self.press_a >= self.press_samples:
                    self.seen_a = True
            if not self.seen_b:
                self.press_b = self.press_b + 1 if f.btn_b else 0
                if self.press_b >= self.press_samples:
                    self.seen_b = True
            if self.seen_a and self.seen_b:
                self.stage = "ARMED"
            else:
                return Verdict(False, False, self.stage, self.good, "NEED_BOTH_PRESSES")
        # Atomic permission: never enable just one of the two series switches.
        assert self.stage == "ARMED"
        return Verdict(True, True, self.stage, self.good, "BOTH_LOCAL_EDGES")

def sample_trace(rows):
    model = GuardedRearm()
    return [model.tick(Frame(*row)) for row in rows]

def baseline_w36_counterexample():
    """W36 abstract model starts without requiring observed release."""
    return {"initial": (False, False), "first_good_sample": (True, True)}

def evaluate():
    # Software state-space enumeration, NOT physical/failure-exhaustive testing.
    states = list(itertools.product((False, True), repeat=4))
    checked = 0
    for trace in itertools.product(states, repeat=4):
        m = GuardedRearm()
        for vals in trace:
            verdict = m.tick(Frame(*vals))
            if verdict.en_a or verdict.en_b:
                raise AssertionError("uncommanded early enable: " + repr(trace))
        checked += 1
    held = [(True, True, True, True)] * 12
    cold_held = sample_trace(held)
    after_release = sample_trace(held + [(True,True,False,False)]*2 + [(True,True,True,True)]*2)
    qualified = sample_trace([(True,True,False,False)]*5 + [(True,True,True,True)]*2)
    assert not any(x.en_a or x.en_b for x in cold_held)
    assert after_release[-1].en_a and after_release[-1].en_b
    assert qualified[-1].en_a and qualified[-1].en_b
    return {
        "schema": "VALDO-W-IND-37-REARM-GUARD-V1",
        "finding": "W36 abstract digital model allows both enabled at first healthy sample if both buttons are already high; release-before-press is not enforced",
        "w36_baseline_expected": baseline_w36_counterexample(),
        "w37_held_on_cold_boot": {"samples": len(held), "ever_enabled": any(x.en_a or x.en_b for x in cold_held)},
        "w37_release_then_press": {"enabled_after_fresh_sequence": after_release[-1].en_a and after_release[-1].en_b},
        "short_trace_exhaustive_checked": checked,
        "assumed_sample_period_ms": SAMPLE_MS_ASSUMED,
        "good_samples": GOOD_SAMPLES,
        "both_release_samples": RELEASE_SAMPLES,
        "both_press_samples": PRESS_SAMPLES,
        "software_model_only": True,
        "actual_w36_kicad_modified": False,
        "hardware_tested": False,
        "safe_to_energize": False,
        "battery_or_dock_connected": False,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()
    report = evaluate()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))

if __name__ == "__main__":
    main()
