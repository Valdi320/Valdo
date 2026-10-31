"""Idealised asynchronous local reset model. Does not calculate electrical delays."""
from dataclasses import dataclass

@dataclass
class Local:
    a: bool = False
    b: bool = False
    prev_a: bool = False
    prev_b: bool = False

    def tick(self, pg33, pg5, alert_ok, arm_a=False, arm_b=False):
        good = bool(pg33 and pg5 and alert_ok)
        if not good:
            self.a = self.b = False
        else:
            if arm_a and not self.prev_a: self.a = True
            if arm_b and not self.prev_b: self.b = True
        self.prev_a, self.prev_b = bool(arm_a), bool(arm_b)
        return (bool(self.a and good), bool(self.b and good))
