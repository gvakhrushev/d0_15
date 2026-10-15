#!/usr/bin/env python3
"""Structural regressions only. These tests do not verify any D0 theorem."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import d0_handoff as handoff

ROOT = Path(__file__).resolve().parents[1]


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='d0-handoff-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        plan, _, manifest = handoff.load(ROOT)
        files = [handoff.PLAN, handoff.IDEAS, '00_WORK/manifest.json',
                 plan['strategy'], plan['contract'], 'D0_START_HERE_RU.md',
                 '02_REGISTRY/research/D0_HANDOFF_SOURCE_NOTES_RU.md']
        ids = {r['task'] for r in plan['roles'].values()}
        files += [t['brief'] for t in manifest['tasks'] if t['id'] in ids]
        for path in files:
            target = self.root/path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT/path, target)

    def mutate(self, path, fn):
        p = self.root/path
        value = json.loads(p.read_text())
        fn(value)
        p.write_text(json.dumps(value, ensure_ascii=False))

    def test_actual_plan(self):
        self.assertEqual(handoff.validate(self.root)['repository'], handoff.REPO)

    def test_all_roles_are_read_only_and_pinned(self):
        for role in handoff.ROLES:
            text = handoff.dispatch_text(self.root, role)
            self.assertIn('NOT_DISPATCHED', text)
            self.assertIn('read live open PRs', text)
            self.assertIn('Repository: gvakhrushev/d0_15', text)

    def test_live_snapshot_mislabel_rejected(self):
        self.mutate(handoff.PLAN, lambda p:p.update(snapshot_is_live_status=True))
        with self.assertRaises(ValueError):handoff.validate(self.root)

    def test_wip_inflation_rejected(self):
        self.mutate('00_WORK/manifest.json', lambda p:p['limits'].update(EXPENSIVE=4))
        with self.assertRaises(ValueError):handoff.validate(self.root)

    def test_missing_consumer_rejected(self):
        self.mutate(handoff.PLAN, lambda p:p['roles']['foundations'].pop('consumer'))
        with self.assertRaises(ValueError):handoff.validate(self.root)

    def test_duplicate_registration_rejected(self):
        self.mutate('00_WORK/manifest.json', lambda p:p['tasks'].append(copy.deepcopy(p['tasks'][0])))
        with self.assertRaises(ValueError):handoff.validate(self.root)

    def test_idea_erasure_rejected(self):
        self.mutate(handoff.IDEAS, lambda p:p['ideas'].pop())
        with self.assertRaises(ValueError):handoff.validate(self.root)

    def test_false_proof_promotion_rejected(self):
        self.mutate(handoff.IDEAS, lambda p:p['ideas'][0].update(proof_status='CORE'))
        with self.assertRaises(ValueError):handoff.validate(self.root)

    def test_ungated_nonlinear_dispatch_rejected(self):
        self.mutate(handoff.PLAN, lambda p:p['roles']['nonlinear'].update(gate='GO'))
        with self.assertRaises(ValueError):handoff.validate(self.root)

    def test_write_fence_escape_rejected(self):
        self.mutate(handoff.PLAN, lambda p:p['roles']['evidence'].update(write_fence=['../outside']))
        with self.assertRaises(ValueError):handoff.validate(self.root)

    def test_unpinned_input_rejected(self):
        self.mutate(handoff.PLAN, lambda p:p['snapshot']['prs'][0].update(head='main'))
        with self.assertRaises(ValueError):handoff.validate(self.root)


if __name__ == '__main__':
    unittest.main()
