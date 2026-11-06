#!/usr/bin/env python3
"""Reject substitution of the retained evidence and a falsely claimed raw file."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

P = Path(__file__).resolve().parent

class IntegrityTests(unittest.TestCase):
    def test_evidence_changes_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            dst = Path(temp) / 'receipt'
            shutil.copytree(P, dst, ignore=shutil.ignore_patterns('parts'))
            def run(*args):
                return subprocess.run([sys.executable, '-B', str(dst/'verify_receipt.py'), *args], capture_output=True)
            self.assertEqual(run().returncode, 0)
            for name in ('summary.json.gz', 'producer_progress.jsonl.gz', 'compactor_progress.jsonl.gz'):
                with self.subTest(name=name):
                    f = dst/name
                    raw = f.read_bytes()
                    f.write_bytes(raw + b'X')
                    self.assertNotEqual(run().returncode, 0)
                    f.write_bytes(raw)
            bad_raw = dst/'fake_raw.json'
            bad_raw.write_text('{}')
            self.assertNotEqual(run('--check-raw', str(bad_raw)).returncode, 0)

if __name__ == '__main__':
    unittest.main()
