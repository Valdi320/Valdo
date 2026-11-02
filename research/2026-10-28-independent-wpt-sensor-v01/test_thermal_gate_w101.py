"""W-IND-101 independent W-only fail-closed NTC ratio input regressions.
OFFLINE model ONLY: fake readings, no physical WPT, sensor, battery or TX.
"""
from dataclasses import replace
from decimal import Decimal
from fractions import Fraction
import unittest

from tx_thermal_window import window_clear, assumed_channel, TxInterlock

class Convertible:
    def __float__(self):
        return 0.5

class W101ThermalInputGate(unittest.TestCase):
    def test_text_looking_like_good_ratio_is_not_adc(self):
        self.assertFalse(window_clear("0.5"))

    def test_bytes_looking_like_good_ratio_are_not_adc(self):
        self.assertFalse(window_clear(b"0.5"))

    def test_decimal_ratio_requires_explicit_validation(self):
        self.assertFalse(window_clear(Decimal("0.5")))

    def test_fraction_ratio_requires_explicit_validation(self):
        self.assertFalse(window_clear(Fraction(1, 2)))

    def test_custom_convertible_object_cannot_represent_sensor(self):
        self.assertFalse(window_clear(Convertible()))

    def test_boolean_cannot_represent_sensor(self):
        self.assertFalse(window_clear(True))

    def test_nonfinite_window_limits_fail_closed(self):
        for kw in ({"low": float("nan")}, {"low": -float("inf")},
                   {"high": float("inf")}, {"high": float("nan")}):
            with self.subTest(kw=kw):
                self.assertFalse(window_clear(0.5, **kw))

    def test_textual_window_limits_fail_closed(self):
        self.assertFalse(window_clear(0.5, low="0.1"))
        self.assertFalse(window_clear(0.5, high="0.9"))

    def test_reversed_or_out_of_range_thresholds_fail_closed(self):
        for low, high in ((0.8,0.2), (-0.1,0.9), (0.1,1.1), (0.5,0.5)):
            with self.subTest(low=low,high=high):
                self.assertFalse(window_clear(0.5,low=low,high=high))

    def test_normal_numeric_ratio_unchanged(self):
        self.assertTrue(window_clear(0.5))
        self.assertTrue(window_clear(0.5,low=0.28,high=0.87))
        self.assertFalse(window_clear(0.27))
        self.assertFalse(window_clear(0.88))

    def test_malformed_channel_cannot_power_abstract_tx(self):
        good=assumed_channel()
        for bad in ("0.5",Decimal("0.5"),Fraction(1,2),Convertible()):
            with self.subTest(bad=type(bad).__name__):
                monitor=TxInterlock()
                result=monitor.step(replace(good,ntc_ratio_read=bad),good,
                                    local_request=True,local_reset=True)
                self.assertFalse(result["energized"])
                self.assertFalse(result["installation_approved"])

    def test_malformed_channel_trips_an_already_armed_model(self):
        good=assumed_channel()
        monitor=TxInterlock()
        self.assertTrue(monitor.step(good,good,local_request=True,
                                     local_reset=True)["energized"])
        bad=replace(good,ntc_ratio_read="0.5")
        result=monitor.step(good,bad,local_request=True)
        self.assertFalse(result["energized"])
        self.assertFalse(result["latched_a"])
        self.assertFalse(result["latched_b"])
        # Restored readings cannot auto-rearm without a new local reset edge.
        self.assertFalse(monitor.step(good,good,local_request=True)["energized"])

    def test_single_weld_does_not_override_malformed_both_channels(self):
        good=assumed_channel()
        bad=replace(good,ntc_ratio_read="0.5")
        for a,b in (("welded_closed","normal"),("normal","welded_closed")):
            with self.subTest(a=a,b=b):
                monitor=TxInterlock()
                result=monitor.step(bad,bad,local_request=True,
                                    local_reset=True,cut_a_fault=a,cut_b_fault=b)
                self.assertFalse(result["energized"])

if __name__=="__main__":
    unittest.main()
