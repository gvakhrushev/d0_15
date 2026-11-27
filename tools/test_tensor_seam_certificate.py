#!/usr/bin/env python3
"""Ensure the tensor-seam certificate stays failable under optimization."""
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = "04_CERTIFICATES/vp_archive_tensor_seam_metric_measure.py"


class TensorSeamCertificateTest(unittest.TestCase):
    def test_optimized_run_passes(self):
        result = subprocess.run(
            [sys.executable, "-B", "-O", CERTIFICATE],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS:", result.stdout)

    def test_disabled_mutation_is_rejected_under_optimization(self):
        program = """
import importlib.util

spec = importlib.util.spec_from_file_location("tensor_seam", CERTIFICATE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
original = module.conductance
module.conductance = lambda r, x, mutate=False: original(r, x, False)
module.test_metric_measure()
""".replace("CERTIFICATE", repr(CERTIFICATE))
        result = subprocess.run(
            [sys.executable, "-B", "-O", "-c", program],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Mutation control failed", result.stderr)


if __name__ == "__main__":
    unittest.main()
