#!/usr/bin/env python3
"""Structural registration tests only; no theorem, repository CI or launch claim."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import hashlib

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("register_wave",HERE/"register_wave.py")
reg=importlib.util.module_from_spec(spec);spec.loader.exec_module(reg)
PARENT="CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE"
CLAIM="D0-A4D-SECOND-ORDER-ENERGY-COVARIANCE-001"

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        (self.root/"00_WORK/tasks").mkdir(parents=True)
        (self.root/"02_REGISTRY").mkdir()
        (self.root/"02_REGISTRY/claims.csv").write_text("claim_id\n"+CLAIM+"\n")
        self.original={"schema":"d0-work/1","limits":{"EXPENSIVE":3,"WORKER":5,"CONTROL":2},
                       "legacy_scaffolds":[],"tasks":[{"id":PARENT,"class":"CONTROL",
                       "parent":"ROOT","state":"REVIEW","affected_claims":[],
                       "exit_condition":"Preserve the existing parent obligation.",
                       "brief":"00_WORK/tasks/"+PARENT+".md"}]}
        self.save(self.original)
    def save(self,x): (self.root/"00_WORK/manifest.json").write_text(json.dumps(x))
    def install_fixture(self):
        changes,added=reg.plan(self.root)
        for p,data in changes.items():reg.atomic_write(self.root/p,data)
        return added
    def test_nine_registered_candidates(self):
        changes,added=reg.plan(self.root)
        self.assertEqual(len(added),9);self.assertEqual(len(changes),10)
    def test_check_writes_nothing(self):
        before=(self.root/"00_WORK/manifest.json").read_bytes()
        reg.plan(self.root)
        self.assertEqual(before,(self.root/"00_WORK/manifest.json").read_bytes())
        self.assertEqual(list((self.root/"00_WORK/tasks").iterdir()),[])
    def test_existing_parent_and_limits_preserved(self):
        changes,_=reg.plan(self.root); after=json.loads(changes["00_WORK/manifest.json"])
        self.assertEqual(after["tasks"][:1],self.original["tasks"])
        self.assertEqual(after["limits"],self.original["limits"])
    def test_idempotent_before_launch(self):
        self.install_fixture();self.assertEqual(reg.plan(self.root),({},[]))
    def test_runtime_state_not_reset(self):
        self.install_fixture()
        path=self.root/"00_WORK/manifest.json";m=json.loads(path.read_text())
        m["tasks"][1]["state"]="IN_PROGRESS";self.save(m)
        self.assertEqual(reg.plan(self.root),({},[]))
    def test_duplicate_rejected(self):
        m=copy.deepcopy(self.original);m["tasks"]*=2;self.save(m)
        with self.assertRaises(ValueError):reg.plan(self.root)
    def test_changed_wip_rejected(self):
        m=copy.deepcopy(self.original);m["limits"]["WORKER"]=10;self.save(m)
        with self.assertRaises(ValueError):reg.plan(self.root)
    def test_missing_parent_rejected(self):
        m=copy.deepcopy(self.original);m["tasks"]=[];self.save(m)
        with self.assertRaises(ValueError):reg.plan(self.root)
    def test_missing_claim_rejected(self):
        (self.root/"02_REGISTRY/claims.csv").write_text("claim_id\nUNKNOWN\n")
        with self.assertRaises(ValueError):reg.plan(self.root)
    def test_foreign_file_rejected(self):
        (self.root/reg.ROWS[0]["brief"]).write_text("someone else's work")
        with self.assertRaises(ValueError):reg.plan(self.root)
    def test_changed_registered_brief_rejected(self):
        self.install_fixture();(self.root/reg.ROWS[0]["brief"]).write_text("changed")
        with self.assertRaises(ValueError):reg.plan(self.root)

    def init_git_fixture(self, fail=False):
        (self.root/"tools").mkdir()
        (self.root/"README.md").write_text("original README")
        (self.root/"00_WORK/STATUS.md").write_text("original STATUS")
        (self.root/"tools/render_work_status.py").write_text(
            "from pathlib import Path\nimport sys\n"
            "if '--check' not in sys.argv:\n"
            " Path('README.md').write_text('fixture generated README')\n"
            " Path('00_WORK/STATUS.md').write_text('fixture generated STATUS')\n")
        (self.root/"tools/validate_work.py").write_text("raise SystemExit("+str(7 if fail else 0)+")\n")
        (self.root/"tools/validate_agent_protocol.py").write_text("raise SystemExit(0)\n")
        for cmd in (["git","init","-q","-b",reg.EXPECTED_BRANCH],
                    ["git","config","user.name","Registration fixture"],
                    ["git","config","user.email","test@example.invalid"],
                    ["git","add","."],["git","commit","-qm","fixture"]):
            subprocess.run(cmd,cwd=self.root,check=True,capture_output=True)
    def test_successful_local_transaction_fixture(self):
        self.init_git_fixture()
        self.assertEqual(len(reg.apply(self.root)),9)
        self.assertEqual((self.root/"README.md").read_text(),"fixture generated README")
    def test_failed_validation_rolls_back_owned_paths(self):
        self.init_git_fixture(fail=True)
        before=(self.root/"00_WORK/manifest.json").read_bytes()
        with self.assertRaises(subprocess.CalledProcessError):reg.apply(self.root)
        self.assertEqual((self.root/"00_WORK/manifest.json").read_bytes(),before)
        self.assertEqual((self.root/"README.md").read_text(),"original README")
        self.assertEqual((self.root/"00_WORK/STATUS.md").read_text(),"original STATUS")
        self.assertFalse((self.root/reg.ROWS[0]["brief"]).exists())
    def test_wrong_branch_never_writes(self):
        self.init_git_fixture()
        subprocess.run(["git","checkout","-qb","wrk/not-owner"],cwd=self.root,check=True)
        with self.assertRaises(ValueError):reg.apply(self.root)
        self.assertFalse((self.root/reg.ROWS[0]["brief"]).exists())

if __name__=="__main__":unittest.main()
