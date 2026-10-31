"""Adversarial tests for W69: no physical tests or Li-ion work."""
from dataclasses import replace
from math import exp
import unittest
from w_ind_69.w69_discharge_envelope import Node, Case, screen


def sample(**kw):
    return replace(Case((Node('TX', 100e-6, 5.0, 1000.0),), .5, True, True, True), **kw)


class W69(unittest.TestCase):
    def test_single_rc_matches_analytic(self):
        d = screen(sample())
        self.assertAlmostEqual(d['nodes'][0]['upper_voltage_v'], 5*exp(-5))
        self.assertFalse(d['hardware_approved'])
        self.assertEqual(d['classification'], 'BELOW_HYPOTHETICAL_SCREEN_NOT_SAFE')

    def test_open_bleeder_defeats_normal_decay(self):
        normal = screen(sample(elapsed_s=3600))
        opened = screen(sample(nodes=(Node('TX', 100e-6, 5.0, 1000, True),), elapsed_s=3600))
        self.assertLess(normal['nodes'][0]['upper_voltage_v'], .5)
        self.assertEqual(opened['nodes'][0]['upper_voltage_v'], 5)
        self.assertEqual(opened['classification'], 'OPEN_BLEEDER_FAULT')

    def test_second_independent_node_retains_energy(self):
        d=screen(sample(nodes=(Node('TX',100e-6,5,1000),Node('AUX',.001,5,1e6))))
        self.assertEqual(d['classification'], 'RESIDUAL_ABOVE_HYPOTHETICAL_SCREEN')
        self.assertGreater(d['total_energy_upper_j'], .012)
        self.assertGreater(d['nodes'][1]['upper_voltage_v'], 4.9)

    def test_energy_summed_not_only_largest(self):
        # Each below hypothetical 1 mJ; sum above.
        d=screen(sample(nodes=(Node('A',50e-6,5,1e7),Node('B',50e-6,5,1e7)),elapsed_s=0))
        self.assertGreater(d['total_energy_upper_j'], .001)
        self.assertEqual(d['classification'], 'RESIDUAL_ABOVE_HYPOTHETICAL_SCREEN')

    def test_missing_topological_proofs_are_unknown(self):
        for name, classification in [('source_cut_verified','SOURCE_CUT_UNVERIFIED'),
            ('backfeed_excluded','BACKFEED_NOT_EXCLUDED'),
            ('nodes_independent_verified','NODE_COUPLING_UNKNOWN')]:
            with self.subTest(name=name):
                d=screen(sample(**{name:False}))
                self.assertIsNone(d['total_energy_upper_j'])
                self.assertEqual(d['classification'],classification)

    def test_missing_resistor_is_unknown_not_infinite_decay(self):
        d=screen(sample(nodes=(Node('TX',100e-6,5,None),)))
        self.assertEqual(d['classification'],'BLEED_PATH_UNKNOWN')
        self.assertIsNone(d['total_energy_upper_j'])

    def test_fault_open_with_missing_resistance_is_still_open(self):
        d=screen(sample(nodes=(Node('TX',100e-6,5,None,True),)))
        self.assertEqual(d['classification'],'OPEN_BLEEDER_FAULT')
        self.assertEqual(d['nodes'][0]['upper_voltage_v'],5)

    def test_worst_case_is_monotone_with_capacitance_and_rmax(self):
        base=screen(sample(nodes=(Node('TX',100e-6,5,1000),)))
        larger_c=screen(sample(nodes=(Node('TX',200e-6,5,1000),)))
        larger_r=screen(sample(nodes=(Node('TX',100e-6,5,2000),)))
        self.assertGreater(larger_c['total_energy_upper_j'],base['total_energy_upper_j'])
        self.assertGreater(larger_r['total_energy_upper_j'],base['total_energy_upper_j'])

    def test_energy_nonincreasing_over_time_if_closed(self):
        previous=float('inf')
        for t in (0,.001,.1,.5,10,3600,86400):
            d=screen(sample(elapsed_s=t))
            self.assertLessEqual(d['total_energy_upper_j'],previous)
            previous=d['total_energy_upper_j']

    def test_open_fault_remains_constant(self):
        for t in (0, 1, 100, 86400):
            d=screen(sample(nodes=(Node('TX',100e-6,5,1e3,True),),elapsed_s=t))
            self.assertAlmostEqual(d['total_energy_upper_j'],.00125)

    def test_wrong_flags_fail_closed(self):
        for v in (None,0,1,'false',[],float('nan')):
            with self.subTest(v=str(v)):
                with self.assertRaises(ValueError):screen(sample(source_cut_verified=v))

    def test_numeric_domain_and_bool_coercion_rejected(self):
        for v in (float('nan'),float('inf'),True,-1,86401,'10'):
            with self.subTest(t=v):
                with self.assertRaises(ValueError):screen(sample(elapsed_s=v))
        for node in (Node('X',0,5,1000), Node('X',1e-6,float('nan'),1000),
            Node('X',1e-6,5,True),Node('X',1e-6,5,-1),Node('X',1e-6,5,1000,1)):
            with self.subTest(node=node):
                with self.assertRaises(ValueError):screen(sample(nodes=(node,)))

    def test_duplicated_unknown_nodes_rejected(self):
        with self.assertRaises(ValueError):screen(sample(nodes=(Node('TX',1e-6,5,100),Node('TX',1e-6,5,100))))
        with self.assertRaises(ValueError):screen(sample(nodes=()))
        with self.assertRaises(ValueError):screen(sample(nodes=[Node('X',1e-6,5,100)]))

    def test_provenance_never_claims_approval(self):
        for d in (screen(sample()), screen(sample(nodes=(Node('X',1e-3,5,1000,True),))),
                  screen(sample(backfeed_excluded=False))):
            self.assertFalse(d['hardware_approved'])
            self.assertEqual(d['physical_tests'],0)
            self.assertFalse(d['lithium_connected'])
            self.assertEqual(d['evidence_type'],'SYNTHETIC_INDEPENDENT_RC_UPPER_BOUND')

    def test_screen_limits_are_hypothetical_and_accepted_only_as_scalars(self):
        with self.assertRaises(ValueError):screen(sample(screening_v=0))
        with self.assertRaises(ValueError):screen(sample(screening_j=True))


if __name__ == '__main__':unittest.main()
