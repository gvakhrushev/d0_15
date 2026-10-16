#!/usr/bin/env python3
"""Second-wave contract/adapter tests. No real registration, dispatch or science replay."""
import copy
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
import register_wave2 as adapter

PARENT='CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE'
CLAIM='D0-A4D-SECOND-ORDER-ENERGY-COVARIANCE-001'

class WaveTests(unittest.TestCase):
    def setUp(self):
        self.module=adapter.load_transaction()
        self.tmp=tempfile.TemporaryDirectory(prefix='d0-w2-contract-')
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.manifest={'schema':'d0-work/1','limits':{'EXPENSIVE':3,'WORKER':5,'CONTROL':2},
          'legacy_scaffolds':[], 'tasks':[
          {'id':PARENT,'class':'CONTROL','parent':'ROOT','state':'REVIEW'},
          {'id':'WRK-A4D-MOVING-SCALE-VARIATION','class':'WORKER','parent':PARENT,'state':'IN_PROGRESS'}]}
        (self.root/'00_WORK').mkdir()
        (self.root/'02_REGISTRY').mkdir()
        (self.root/'02_REGISTRY/claims.csv').write_text('claim_id\n'+CLAIM+'\n')
        self.save()

    def save(self):
        (self.root/'00_WORK/manifest.json').write_text(json.dumps(self.manifest))

    def files(self):
        return {str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}

    def materialize(self,changes):
        for rel,data in changes.items():
            p=self.root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)

    def test_nine_unique_new_ids(self):
        self.assertEqual(len(adapter.IDS),9)
        self.assertEqual(len(set(adapter.IDS)),9)
        self.assertNotIn('WRK-A4D-MOVING-SCALE-VARIATION',adapter.IDS)
        self.assertNotIn('WRK-A4D-LEAN-SOURCE-REFLECTION',adapter.IDS)

    def test_adapter_uses_real_existing_transaction(self):
        self.assertEqual(self.module.EXPECTED_BRANCH,adapter.BRANCH)
        self.assertEqual(self.module.HERE,adapter.HERE)
        self.assertEqual(tuple(r['id'] for r in self.module.ROWS),adapter.IDS)
        self.assertEqual(self.module.apply.__code__.co_filename,str(adapter.OLD))

    def test_read_only_nine_row_plan(self):
        before=self.files(); changes,added=self.module.plan(self.root)
        self.assertEqual(self.files(),before)
        self.assertEqual(added,list(adapter.IDS));self.assertEqual(len(changes),10)

    def test_preserve_live_task_parent_and_limits(self):
        changes,_=self.module.plan(self.root)
        new=json.loads(changes['00_WORK/manifest.json'])
        self.assertEqual(new['limits'],self.manifest['limits'])
        self.assertEqual(new['tasks'][:2],self.manifest['tasks'])
        self.assertTrue(all(r['state']=='PLANNED' and r['parent']==PARENT for r in new['tasks'][2:]))

    def test_idempotent_registration_without_reset(self):
        changes,_=self.module.plan(self.root);self.materialize(changes)
        self.manifest=json.loads((self.root/'00_WORK/manifest.json').read_text())
        self.manifest['tasks'][2]['state']='IN_PROGRESS';self.save()
        self.assertEqual(self.module.plan(self.root),({},[]))

    def test_missing_control_rejected(self):
        self.manifest['tasks'][0]['class']='EXPENSIVE';self.save()
        with self.assertRaisesRegex(ValueError,'CONTROL parent'):self.module.plan(self.root)

    def test_unregistered_claim_rejected(self):
        (self.root/'02_REGISTRY/claims.csv').write_text('claim_id\nOTHER\n')
        with self.assertRaisesRegex(ValueError,'unregistered affected claim'):self.module.plan(self.root)

    def test_wip_change_rejected(self):
        self.manifest['limits']['WORKER']=10;self.save()
        with self.assertRaisesRegex(ValueError,'WIP differs'):self.module.plan(self.root)

    def test_duplicate_existing_id_rejected(self):
        self.manifest['tasks'].append(copy.deepcopy(self.manifest['tasks'][0]));self.save()
        with self.assertRaisesRegex(ValueError,'duplicate current'):self.module.plan(self.root)

    def test_unowned_destination_rejected(self):
        p=self.root/'00_WORK/tasks'/(adapter.IDS[0]+'.md');p.parent.mkdir();p.write_text('other work')
        with self.assertRaisesRegex(ValueError,'unowned task file'):self.module.plan(self.root)

    def test_existing_brief_not_overwritten(self):
        changes,_=self.module.plan(self.root);self.materialize(changes)
        p=self.root/'00_WORK/tasks'/(adapter.IDS[0]+'.md');p.write_text('changed by another owner')
        with self.assertRaisesRegex(ValueError,'brief changed'):self.module.plan(self.root)

    def test_changed_helper_blocked_before_import(self):
        bad=self.root/'foreign_helper.py';sentinel=self.root/'must_not_exist'
        bad.write_text('open('+repr(str(sentinel))+',"w").write("executed")')
        with patch.object(adapter,'OLD',bad):
            with self.assertRaisesRegex(ValueError,'helper changed'):adapter.load_transaction()
        self.assertFalse(sentinel.exists())

    def test_complete_briefs_and_nonoverlapping_owned_paths(self):
        seen=[]
        for tid in adapter.IDS:
            text=(adapter.HERE/(tid+'.md')).read_text()
            self.assertTrue(text.startswith('# '+tid+'\n'))
            for heading in ('## Точное обязательство','## Закреплённые входы','## Потребитель',
                            '## Зависимости и запуск','## Решающая проверка',
                            '## Why delegated','## GitHub execution contract','## Chat handoff'):
                self.assertEqual(text.count(heading),1)
            self.assertIn('74e62cdc716e10883accba9d34ccf0e21d58eb65',text)
            fences=text.split('## Разрешённая запись\n',1)[1].split('\n\nТолько',1)[0]
            paths=re.findall(r'^- `([^`]+)`$',fences,re.M)
            self.assertTrue(paths)
            for a in paths:
                self.assertNotIn('..',a.split('/'))
                for b in seen:self.assertFalse(a==b or a.startswith(b.rstrip('/')+'/') or b.startswith(a.rstrip('/')+'/'))
                seen.append(a)

    def test_ten_assignments_and_dependency_boundaries(self):
        entry=(adapter.ROOT/'02_REGISTRY/research/D0_SECOND_MEDIUM_AGENT_WAVE_2026-10-16.md').read_text()
        for n in range(1,11):self.assertIn('[N'+str(n).zfill(2)+']',entry)
        self.assertIn('#331',entry); self.assertIn('N05/N06',entry)
        self.assertIn('не запуск агентов',entry)
        self.assertTrue((adapter.HERE/'CONTROL_WAVE2_INTAKE.md').is_file())

if __name__=='__main__':unittest.main(verbosity=2)
