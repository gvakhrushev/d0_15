#!/usr/bin/env python3
"""Ensure the toral-SFT trace control remains failable under optimization."""
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = "04_CERTIFICATES/vp_toral_sft_conjugacy_nogo.py"


class ToralSftCertificateTest(unittest.TestCase):
    def test_optimized_run_passes(self):
        result = subprocess.run(
            [sys.executable, "-B", "-O", CERTIFICATE],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS_TORAL_SFT_TOPOLOGICAL_CONJUGACY_NOGO", result.stdout)

    def test_invalid_trace_is_rejected_under_optimization(self):
        program = """
import importlib.util

spec = importlib.util.spec_from_file_location("toral_sft", CERTIFICATE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.trace2 = lambda _: 0
module.main()
""".replace("CERTIFICATE", repr(CERTIFICATE))
        result = subprocess.run(
            [sys.executable, "-B", "-O", "-c", program],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unexpected trace for the toral matrix", result.stderr)


if __name__ == "__main__":
    unittest.main()
