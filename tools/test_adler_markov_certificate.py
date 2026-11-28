#!/usr/bin/env python3
"""Exercise the scoped golden-endpoint certificate and a faulty multiplication."""
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "04_CERTIFICATES/vp_adler_weiss_internal_markov.py"


class AdlerMarkovCertificateTest(unittest.TestCase):
    def test_certificate_reports_its_scope(self):
        result = subprocess.run([sys.executable, "-B", str(CERTIFICATE)], cwd=ROOT,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS_ADLER_WEISS_INTERNAL_MARKOV", result.stdout)
        self.assertIn("No map from the beta natural extension", result.stdout)

    def test_wrong_golden_arithmetic_is_rejected(self):
        program = f"""
import importlib.util
spec = importlib.util.spec_from_file_location('adler_markov', {str(CERTIFICATE)!r})
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.mul = lambda a, b: (0, 0)
module.main()
"""
        result = subprocess.run([sys.executable, "-B", "-O", "-c", program], cwd=ROOT,
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL GOLDEN_SPLIT", result.stdout)


if __name__ == "__main__":
    unittest.main()
