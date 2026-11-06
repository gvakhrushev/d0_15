#!/usr/bin/env python3
"""Detect substitution of retained inputs and falsely attributed outputs."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

P = Path(__file__).resolve().parent

class IntegrityTests(unittest.TestCase):
    def test_mutated_evidence_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix='d0-7fy-integrity-', dir='/tmp') as temp:
            dst = Path(temp) / 'intake'
            shutil.copytree(P, dst)
            def verify():
                return subprocess.run([sys.executable, '-B', str(dst / 'verify_intake.py')], capture_output=True)
            self.assertEqual(verify().returncode, 0)
            for name in ('complete_delta.patch.xz', 'owner_7fy.md', 'inputs/native_execution.py', 'results/check_guard.py.stdout', 'independent_replay.json', 'HANDOFF_RU.md'):
                with self.subTest(name=name):
                    path = dst / name
                    original = path.read_bytes()
                    path.write_bytes(original + b'bad')
                    self.assertNotEqual(verify().returncode, 0)
                    path.write_bytes(original)

if __name__ == '__main__':
    unittest.main()
