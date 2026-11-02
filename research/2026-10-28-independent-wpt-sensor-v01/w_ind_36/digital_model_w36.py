"""W-IND-36 synthetic digital truth table; NOT real analog, timing or safety testing."""
from __future__ import annotations

class Rearm:
    def __init__(self):
        self.q_a = False
        self.q_b = False
        self.last_a = False
        self.last_b = False

    def step(self, pg_mon, pg_rx, clk_a=False, clk_b=False):
        # Two redundant ANDs release two async CLR_N inputs only if BOTH PGs are good.
        # Clocks are physical buttons in the schematic; RF messages have no input path.
        both = bool(pg_mon and pg_rx)
        if not both:
            self.q_a = self.q_b = False
        else:
            if clk_a and not self.last_a: self.q_a = True
            if clk_b and not self.last_b: self.q_b = True
        self.last_a, self.last_b = bool(clk_a), bool(clk_b)
        return bool(pg_mon and self.q_a), bool(pg_rx and self.q_b)

def threshold_window(nominal, tolerance=0.015):
    return (nominal * (1-tolerance), nominal * (1+tolerance))

def low_rail_guard(vmin, threshold):
    return vmin - threshold_window(threshold)[1]
