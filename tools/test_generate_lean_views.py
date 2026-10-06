#!/usr/bin/env python3
"""Regress the two independent claim-status axes and deterministic Lean views."""
from __future__ import annotations
import copy
import re
import unittest
from unittest.mock import patch
import generate_lean_views as gen


def row(**changes):
    result = dict(claim_id='TEST', lean_module='D0.Test', lean_theorem='test',
                  lean_status='LEAN_PROVED', release_status='CORE-FORMALIZED',
                  uses_bridge_assumptions='false')
    result.update(changes)
    return result


class SummaryTests(unittest.TestCase):
    def test_open_release_dominates_every_proof_status(self):
        for release in gen.OPEN_RELEASE_STATUSES:
            for proof in ['LEAN_PROVED', 'LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS',
                          'PYTHON_CERTIFIED', 'OPEN', 'UNPROVED']:
                with self.subTest(release=release, proof=proof):
                    self.assertEqual(gen.claim_status(row(lean_status=proof,
                        release_status=release)), 'openObligation')

    def test_open_and_unproved_dominates_closed_labels(self):
        for proof in ['OPEN', 'UNPROVED']:
            for release in ['CERT-CLOSED', 'NO-GO', 'CORE-FORMALIZED', 'BRIDGE-CLOSED']:
                self.assertEqual(gen.claim_status(row(lean_status=proof,
                    release_status=release)), 'openObligation')

    def test_open_without_lean_module(self):
        self.assertEqual(gen.claim_status(row(lean_module='', lean_status='OPEN')),
                         'openObligation')

    def test_deprecated_proof(self):
        self.assertEqual(gen.claim_status(row(lean_status='DEPRECATED')),'deprecated')

    def test_deprecated_release_dominates_open(self):
        self.assertEqual(gen.claim_status(row(lean_status='OPEN',
                         release_status='DEPRECATED')), 'deprecated')

    def test_core_requires_core_release(self):
        self.assertEqual(gen.claim_status(row()), 'leanCoreProved')
        self.assertEqual(gen.claim_status(row(release_status='CORE_FORMALIZED')),
                         'leanCoreProved')

    def test_noncore_proved_fact_is_not_core(self):
        for release in ['CERT-CLOSED', 'FORMALISM', 'CORE_BRIDGE_SPLIT',
                        'BRIDGE-CALIBRATION']:
            self.assertEqual(gen.claim_status(row(release_status=release)), 'leanFactProved')

    def test_no_go_is_distinct(self):
        for release in ['NO-GO', 'NO_GO_PROVED']:
            self.assertEqual(gen.claim_status(row(release_status=release)), 'leanNoGoProved')

    def test_conditional_no_go_keeps_assumptions(self):
        self.assertEqual(gen.claim_status(row(lean_status='LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS',
            release_status='NO-GO', uses_bridge_assumptions='true')), 'leanBridgeAssumptionsExplicit')

    def test_python_is_not_lean(self):
        self.assertEqual(gen.claim_status(row(lean_status='PYTHON_CERTIFIED',
            release_status='CERT-CLOSED')), 'pythonCertClosed')

    def test_python_bridge_is_not_lean(self):
        self.assertEqual(gen.claim_status(row(lean_status='PYTHON_CERTIFIED',
            release_status='CERT-CLOSED', uses_bridge_assumptions='true')), 'pythonCertClosed')

    def test_inconsistent_hidden_bridge_is_not_core(self):
        self.assertEqual(gen.claim_status(row(uses_bridge_assumptions='true')),
                         'openObligation')

    def test_empirical_remains_empirical(self):
        self.assertEqual(gen.claim_status(row(release_status='EMPIRICAL-PASSPORT')),
                         'empiricalDataRequired')

    def test_empirical_proof_label(self):
        self.assertEqual(gen.claim_status(row(lean_status='EMPIRICAL_PASSPORT')),
                         'empiricalDataRequired')

    def test_unknown_status_fails_closed(self):
        self.assertEqual(gen.claim_status(row(lean_status='NOT_A_PROOF',release_status='UNKNOWN')),
                         'pythonCertRequired')

    def test_whitespace(self):
        self.assertEqual(gen.claim_status(row(lean_status=' LEAN_PROVED ',
            release_status=' PROOF-TARGET ')), 'openObligation')

    def test_no_mutation(self):
        data=row(release_status='PROOF-TARGET'); before=copy.deepcopy(data)
        gen.claim_status(data)
        self.assertEqual(data,before)


class RenderingTests(unittest.TestCase):
    def test_both_status_axes_survive(self):
        data=row(release_status='PROOF-TARGET')
        with patch.object(gen, 'rows', return_value=[data]): text=gen.render_claimmap()
        self.assertIn('leanStatus := "LEAN_PROVED"', text)
        self.assertIn('releaseStatus := "PROOF-TARGET"', text)
        self.assertIn('status := ClaimStatus.openObligation', text)

    def test_names_are_preserved_not_interpreted_as_proofs(self):
        data=row(lean_module='D0.A;D0.B',lean_theorem='foo;Bar.baz')
        with patch.object(gen,'rows',return_value=[data]): text=gen.render_claimmap()
        self.assertIn('moduleName := "D0.A;D0.B"',text)
        self.assertIn('theoremName := "foo;Bar.baz"',text)
        self.assertIn('metadata, not elaborated references',text)

    def test_escaping(self):
        self.assertEqual(gen.esc('A"B\\C\nD'),'A\\"B\\\\C D')

    def test_no_lean_rows_remain_outside_lean_view(self):
        with patch.object(gen,'rows',return_value=[row(),row(claim_id='PY',lean_module='')]):
            text=gen.render_claimmap()
        self.assertIn('claimId := "TEST"',text)
        self.assertNotIn('claimId := "PY"',text)

    def test_generator_deterministic(self):
        self.assertEqual(gen.render_claimmap(),gen.render_claimmap())
        self.assertEqual(gen.render_all(),gen.render_all())

    def test_all_actual_open_obligations_stay_open(self):
        for r in gen.rows('claims.csv'):
            if r['release_status'] in gen.OPEN_RELEASE_STATUSES:
                self.assertEqual(gen.claim_status(r),'openObligation',r['claim_id'])

    def test_actual_entries_preserve_source_axes(self):
        text=gen.render_claimmap()
        rows=[r for r in gen.rows('claims.csv') if r['lean_module'].strip()]
        self.assertEqual(text.count('claimId :='),len(rows))
        self.assertEqual(text.count('leanStatus :='),len(rows))
        self.assertEqual(text.count('releaseStatus :='),len(rows))
        for r in rows:
            self.assertIn('leanStatus := "'+gen.esc(r['lean_status'].strip())+'", '
                          'releaseStatus := "'+gen.esc(r['release_status'].strip())+'"',text)

    def test_import_closure_sorted_and_unique(self):
        imports=re.findall(r'^import (.+)$',gen.render_all(),re.M)
        self.assertEqual(imports,sorted(set(imports)))

    def test_default_open_label_set_matches_coverage_validator(self):
        import importlib.util
        spec=importlib.util.spec_from_file_location('coverage', gen.ROOT / '03_FORMALIZATION/tools/check_claim_map_coverage.py')
        coverage=importlib.util.module_from_spec(spec); spec.loader.exec_module(coverage)
        self.assertEqual(gen.OPEN_RELEASE_STATUSES,coverage.OPEN_RELEASE_STATUSES)


if __name__ == '__main__':
    unittest.main()
