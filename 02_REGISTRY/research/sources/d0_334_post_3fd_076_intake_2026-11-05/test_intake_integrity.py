#!/usr/bin/env python3
"""Hostile byte substitutions must not pass the local intake verifier."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

P = Path(__file__).resolve().parent

class IntegrityTests(unittest.TestCase):
    def test_pinned_artifacts_reject_modification(self):
        targets = (
            'source_check.py',
            'proof_section.md',
            'owner_reconstructed/check_reader_algebra.py.json',
            'results/source_check.py.optimized.json',
            'results/check_reader_algebra.py.normal.stderr',
        )
        with tempfile.TemporaryDirectory() as temp:
            dst = Path(temp) / 'intake'
            shutil.copytree(P, dst)
            def run():
                return subprocess.run([sys.executable, '-B', str(dst / 'verify_intake.py')], capture_output=True)
            self.assertEqual(run().returncode, 0)
            for target in targets:
                with self.subTest(target=target):
                    path = dst / target
                    original = path.read_bytes()
                    path.write_bytes(original + b'tampered')
                    self.assertNotEqual(run().returncode, 0)
                    path.write_bytes(original)

if __name__ == '__main__':
    unittest.main()
