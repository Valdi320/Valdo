"""W-IND-30: original directional cut-set and brownout-rearm laboratory.

No component model, SPICE analysis, real circuit or physical safety approval.
RCB represents contractual IDEAL reverse blocking, not a promise for
any real eFuse or welded silicon.
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from itertools import product
import argparse
import json
import unittest

@dataclass(frozen=True)
class Stage:
    technology: str
    enabled: bool = False
    welded: bool = False

    def arcs(self, upstream: str, downstream: str):
        if self.technology not in ('rcb', 'body_diode'):
            raise ValueError('unqualified switching technology')
        if self.welded:
            return ((upstream, downstream), (downstream, upstream))
        if self.technology == 'rcb':
            return ((upstream, downstream),) if self.enabled else ()
        # Historical TPS22918-like abstract reverse path: not a Vf model.
        return ((upstream, downstream), (downstream, upstream)) if self.enabled else ((downstream, upstream),)

def cut_paths(a: Stage, b: Stage, bypass_both: bool = False):
    """Find directed forward/reverse paths. No leakage, delay or R_ON."""
    edges = [
        ('SOURCE', 'SHUNT'), ('SHUNT', 'SOURCE'),
        ('SHUNT', 'A_IN'), ('A_IN', 'SHUNT'),
        ('A_OUT', 'B_IN'), ('B_IN', 'A_OUT'),
        ('B_OUT', 'LOAD'), ('LOAD', 'B_OUT'),
    ]
    edges.extend(a.arcs('A_IN', 'A_OUT'))
    edges.extend(b.arcs('B_IN', 'B_OUT'))
    if bypass_both:
        edges.extend((('SOURCE', 'LOAD'), ('LOAD', 'SOURCE')))
    adj = {}
    for src, dst in edges:
        adj.setdefault(src, []).append(dst)
    def witness(start, target):
        queue = deque([(start,)])
        visited = {start}
        while queue:
            path = queue.popleft()
            if path[-1] == target:
                return list(path)
            for node in adj.get(path[-1], []):
                if node not in visited:
                    visited.add(node)
                    queue.append(path + (node,))
        return []
    return {'forward': witness('SOURCE', 'LOAD'), 'reverse': witness('LOAD', 'SOURCE')}

class LocalArmGuard:
    """Behavioral REQUIREMENT for a hardware-local circuit, NOT a firmware stop."""
    def __init__(self):
        self.armed = False
        self.released_after_trip = False
        self.last_button = True

    def sample(self, *, power_good: bool, current_ok: bool,
               temperature_ok: bool, fod_ok: bool, local_button: bool):
        healthy = power_good and current_ok and temperature_ok and fod_ok
        if not healthy:
            self.armed = False
            self.released_after_trip = False
            self.last_button = local_button
            return False
        if not local_button:
            self.released_after_trip = True
        if local_button and not self.last_button and self.released_after_trip:
            self.armed = True
            self.released_after_trip = False
        self.last_button = local_button
        return self.armed

def evaluate(*, armed: bool, power_good: bool, current_ok: bool,
             temperature_ok: bool, fod_ok: bool, welded_a=False, welded_b=False,
             stuck_enable_a=False, stuck_enable_b=False, bypass_both=False,
             a_technology='rcb', b_technology='rcb'):
    health = power_good and current_ok and temperature_ok and fod_ok
    requested = bool(armed and health)
    a = Stage(a_technology, requested or stuck_enable_a, welded_a)
    b = Stage(b_technology, requested or stuck_enable_b, welded_b)
    paths = cut_paths(a, b, bypass_both)
    should_be_off = not requested
    return {'requested_on': requested,
            'forward_conducts': bool(paths['forward']),
            'reverse_conducts': bool(paths['reverse']),
            'unsafe_forward_when_off': should_be_off and bool(paths['forward']),
            'unsafe_reverse_when_off': should_be_off and bool(paths['reverse']),
            'forward_witness': paths['forward'],
            'reverse_witness': paths['reverse'],
            'approval_for_power': False}

def evidence():
    # 4 health flags, 2 welded, 2 stuck enables, 1 source-load bypass = 512.
    samples = 0
    unsafe = 0
    single_fault_misses = 0
    first_witness = None
    for flags in product((False, True), repeat=9):
        pg, current, temp, fod, wa, wb, ea, eb, bypass = flags
        result = evaluate(armed=True, power_good=pg, current_ok=current,
            temperature_ok=temp, fod_ok=fod, welded_a=wa, welded_b=wb,
            stuck_enable_a=ea, stuck_enable_b=eb, bypass_both=bypass)
        samples += 1
        if result['unsafe_forward_when_off'] or result['unsafe_reverse_when_off']:
            unsafe += 1
            if first_witness is None:
                first_witness = {'flags':dict(zip(('power_good','current_ok','temperature_ok',
                    'fod_ok','welded_a','welded_b','stuck_a','stuck_b','bypass'), flags)),
                    'paths':result}
        # Only an idealized single actuator fault with no bypass.
        if not bypass and sum((wa, wb, ea, eb)) <= 1 and not all(flags[:4]):
            if result['forward_conducts']:
                single_fault_misses += 1
    return {'schema':'VALDO-W30-DIGITAL-CUTSET-V1','cases':samples,
        'unsafe_off_cases_expected':unsafe,'single_actuator_fault_misses':single_fault_misses,
        'first_unsafe_witness':first_witness,
        'assumptions':['ideal directional switches','two distinct high-side cuts in series',
            'fault signal truthfulness','no leakage, voltage, timing or thermal behavior',
            'NO physical circuit'],
        'real_reverse_blocking_verified':False,'independent_cutoff_hardware_verified':False,
        'fod_thermal_emi_hardware_verified':False,'battery_connected':False,
        'physical_power_authorized':False}

class CutsetTests(unittest.TestCase):
    def test_authorized_forward_not_reverse(self):
        x=evaluate(armed=True,power_good=True,current_ok=True,temperature_ok=True,fod_ok=True)
        self.assertTrue(x['forward_conducts'])
        self.assertFalse(x['reverse_conducts'])

    def test_no_arm_isolation(self):
        x=evaluate(armed=False,power_good=True,current_ok=True,temperature_ok=True,fod_ok=True)
        self.assertFalse(x['forward_conducts'])
        self.assertFalse(x['reverse_conducts'])

    def test_fault_flags_shut_both(self):
        for i in range(4):
            flags=[True]*4
            flags[i]=False
            x=evaluate(armed=True,power_good=flags[0],current_ok=flags[1],
                temperature_ok=flags[2],fod_ok=flags[3])
            self.assertFalse(x['forward_conducts'])
            self.assertFalse(x['reverse_conducts'])

    def test_one_weld_still_isolates_during_trip(self):
        for fault in ({'welded_a':True},{'welded_b':True}):
            x=evaluate(armed=True,power_good=True,current_ok=False,
                temperature_ok=True,fod_ok=True,**fault)
            self.assertFalse(x['forward_conducts'])
            self.assertFalse(x['reverse_conducts'])

    def test_stuck_one_enable_still_isolates(self):
        for fault in ({'stuck_enable_a':True},{'stuck_enable_b':True}):
            x=evaluate(armed=True,power_good=False,current_ok=True,
                temperature_ok=True,fod_ok=True,**fault)
            self.assertFalse(x['forward_conducts'])

    def test_two_welds_are_unsafe(self):
        x=evaluate(armed=True,power_good=False,current_ok=True,
            temperature_ok=True,fod_ok=True,welded_a=True,welded_b=True)
        self.assertTrue(x['unsafe_forward_when_off'])
        self.assertTrue(x['unsafe_reverse_when_off'])

    def test_two_stuck_en_are_unsafe(self):
        x=evaluate(armed=True,power_good=False,current_ok=True,
            temperature_ok=True,fod_ok=True,stuck_enable_a=True,stuck_enable_b=True)
        self.assertTrue(x['unsafe_forward_when_off'])

    def test_bypass_both_detected(self):
        x=evaluate(armed=False,power_good=False,current_ok=False,
            temperature_ok=False,fod_ok=False,bypass_both=True)
        self.assertTrue(x['unsafe_forward_when_off'])
        self.assertTrue(x['unsafe_reverse_when_off'])

    def test_old_two_diode_stages_reverse_feed_when_off(self):
        x=evaluate(armed=False,power_good=True,current_ok=True,
            temperature_ok=True,fod_ok=True,a_technology='body_diode',
            b_technology='body_diode')
        self.assertFalse(x['forward_conducts'])
        self.assertTrue(x['unsafe_reverse_when_off'])

    def test_mixed_diode_rcb_block_reverse_unwelded(self):
        x=evaluate(armed=False,power_good=True,current_ok=True,
            temperature_ok=True,fod_ok=True,a_technology='body_diode')
        self.assertFalse(x['reverse_conducts'])

    def test_mixed_diode_rcb_weld_reopens_reverse(self):
        x=evaluate(armed=False,power_good=True,current_ok=True,
            temperature_ok=True,fod_ok=True,a_technology='body_diode',
            welded_b=True)
        self.assertTrue(x['reverse_conducts'])

    def test_unknown_part_type_is_rejected(self):
        with self.assertRaises(ValueError):
            Stage('magic').arcs('a','b')

    def test_brownout_stuck_button_does_not_restart(self):
        g=LocalArmGuard()
        safe={'power_good':True,'current_ok':True,
              'temperature_ok':True,'fod_ok':True}
        self.assertFalse(g.sample(**safe,local_button=True))
        self.assertFalse(g.sample(**safe,local_button=False))
        self.assertTrue(g.sample(**safe,local_button=True))
        self.assertFalse(g.sample(**{**safe,'power_good':False},local_button=True))
        self.assertFalse(g.sample(**safe,local_button=True))
        self.assertFalse(g.sample(**safe,local_button=False))
        self.assertTrue(g.sample(**safe,local_button=True))

    def test_trip_has_priority_over_local_button(self):
        g=LocalArmGuard()
        safe={'power_good':True,'current_ok':True,
              'temperature_ok':True,'fod_ok':True}
        g.sample(**safe,local_button=False)
        self.assertTrue(g.sample(**safe,local_button=True))
        self.assertFalse(g.sample(**{**safe,'fod_ok':False},local_button=True))
        self.assertFalse(g.sample(**safe,local_button=True))

    def test_enumeration_produces_expected_hazard_not_false_green(self):
        result=evidence()
        self.assertEqual(result['cases'],512)
        self.assertEqual(result['single_actuator_fault_misses'],0)
        self.assertGreater(result['unsafe_off_cases_expected'],0)
        self.assertFalse(result['physical_power_authorized'])
        self.assertIsNotNone(result['first_unsafe_witness'])

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--json',action='store_true')
    args=parser.parse_args()
    if args.json:
        print(json.dumps(evidence(),sort_keys=True,indent=2))
    else:
        unittest.main(argv=['w30_cutset'],verbosity=2)
