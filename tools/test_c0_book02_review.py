"""Fail-closed active Book02 review corrections and historical behaviour."""
import json
from pathlib import Path
import re
import unittest
from dataclasses import replace

from tools import c0_reconciliation as c0
from tools.c0_kernel_units import parse_unit_candidates

ROOT = Path(__file__).resolve().parents[1]

class FakeGit:
    def __init__(self, history=True):
        self.history = history
        self.files = {c0.BOOK02_REVIEW: (ROOT / c0.BOOK02_REVIEW).read_bytes(),
                      c0.BOOK02_REVIEW_DIR + c0.BOOK02_CONTROL:
                          (ROOT / c0.BOOK02_REVIEW_DIR / c0.BOOK02_CONTROL).read_bytes()}
    def git(self, *args):
        if args == ('merge-base', c0.BOOK02_REVIEW_BASE, 'snapshot'):
            return (c0.BOOK02_REVIEW_BASE + '\n').encode()
        assert args == ('log', '--ancestry-path', '--format=%H', '-1',
                        c0.BOOK02_REVIEW_BASE + '..snapshot', '--', c0.BOOK02_REVIEW)
        return b'1234567890abcdef\n' if self.history else b''
    def data(self, snapshot, path):
        if path not in self.files:
            raise c0.MissingEvidence('missing tracked review artifact')
        return self.files[path]

class ReviewCorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.primary = (ROOT / c0.PRIMARY).read_text()
        pins = c0.KernelSectionPins()
        cls.units = parse_unit_candidates(cls.primary, pins.units_sha256, heading=pins.units_heading)
        cls.pins = pins

    def run_overlay(self, git=None, primary=None, active=None, units=None, pins=None):
        return c0.book02_reviewed_corrections(
            git or FakeGit(), 'snapshot', pins or self.pins,
            self.primary if primary is None else primary,
            {'version': 'corrected'} if active is None else active,
            self.units if units is None else units)

    def test_historical_snapshot_has_no_overlay(self):
        self.assertIsNone(self.run_overlay(FakeGit(history=False)))

    def test_active_exact_review_preserves_historical_statement(self):
        fixes = self.run_overlay()
        obs = fixes['Interpretation.translate_future_observation']
        self.assertIn('logically equivalent', obs['statement'])
        self.assertIn('equals the actual', obs['historical_statement'])
        run = fixes['Interpretation.verifiedRun_image']
        self.assertTrue(run['proof_dependency'].endswith('verifiedStateImageEquiv_representedState'))
        self.assertEqual(run['control'], c0.BOOK02_CONTROL)
        self.assertEqual(len(self.units), 30)

    def test_wrong_or_removed_tracked_review_fails_closed(self):
        for state in ('modified', 'deleted', 'control_modified', 'control_deleted'):
            with self.subTest(state=state):
                git = FakeGit()
                path = c0.BOOK02_REVIEW if state.startswith(('modified', 'deleted')) else c0.BOOK02_REVIEW_DIR+c0.BOOK02_CONTROL
                if state.endswith('deleted') or state == 'deleted':
                    del git.files[path]
                else:
                    git.files[path] += b'changed'
                with self.assertRaises(c0.MissingEvidence):
                    self.run_overlay(git)

    def test_pointer_and_corrected_version_are_required(self):
        with self.assertRaisesRegex(c0.MissingEvidence, 'pointer'):
            self.run_overlay(primary=self.primary.replace('book02_023b_complete_review_2026-11-06/SUMMARY_RU.md', 'removed'))
        with self.assertRaisesRegex(c0.MissingEvidence, 'corrected source'):
            self.run_overlay(active={'version': 'historical'})

    def test_historical_candidate_tampering_fails(self):
        altered = [dict(x) for x in self.units]
        u = next(x for x in altered if x['atom'] == 'Interpretation.translate_future_observation')
        u['statement'] = 'A misleading original.'
        with self.assertRaisesRegex(c0.MissingEvidence, 'historical candidates'):
            self.run_overlay(units=altered)

    def test_other_selected_book_is_unaffected(self):
        self.assertIsNone(self.run_overlay(pins=c0.BOOK01_PINS))
        self.assertIsNone(self.run_overlay(pins=c0.BOOK01_0116_PINS))

if __name__ == '__main__':
    unittest.main()
