#!/usr/bin/env python3
"""Check that the four reviewed archive certificates can fail with python -O."""
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
CASES = {
    "vp_archive_cochain_refinement.py": (
        """
original = module.build_b1
module.build_b1 = lambda L, mutate=False: original(L, False)
module.test_1d_refinement()
""",
        "Mutation control failed to catch error",
    ),
    "vp_archive_graded_rg_extrinsic_curvature.py": (
        """
original = module.make_eye
module.make_eye = lambda n: [[0] * n for _ in range(n)] if n == 2 else original(n)
module.test_rg_extrinsic_curvature_algebra()
""",
        "J* J != I",
    ),
    "vp_archive_hodge_weight_owner.py": (
        """
module.trace_1d_mass = lambda L, mutate=False: 3
module.test_hodge_weights()
""",
        "Mutation control failed",
    ),
    "vp_archive_weighted_hodge_dirac.py": (
        """
original = module.mat_mul
def without_block_mutation(A, B):
    if len(A) == len(B) == len(A[0]) == len(B[0]) == 2:
        return [[0, 0], [0, 0]]
    return original(A, B)
module.mat_mul = without_block_mutation
module.test_weighted_hodge_dirac_small()
""",
        "Mutation control failed",
    ),
}


class ArchiveCertificateOptimizationTest(unittest.TestCase):
    def test_normal_and_optimized_outputs_match(self):
        for name in CASES:
            with self.subTest(certificate=name):
                path = str(ROOT / "04_CERTIFICATES" / name)
                plain = subprocess.run([sys.executable, "-B", path], cwd=ROOT,
                                       capture_output=True, text=True)
                optimized = subprocess.run([sys.executable, "-B", "-O", path], cwd=ROOT,
                                           capture_output=True, text=True)
                self.assertEqual(plain.returncode, 0, plain.stderr)
                self.assertEqual(optimized.returncode, 0, optimized.stderr)
                self.assertEqual((plain.stdout, plain.stderr),
                                 (optimized.stdout, optimized.stderr))
                self.assertIn("PASS:", optimized.stdout)

    def test_faults_are_rejected_under_optimization(self):
        for name, (mutation, expected_message) in CASES.items():
            with self.subTest(certificate=name):
                path = str(ROOT / "04_CERTIFICATES" / name)
                program = f"""
import importlib.util
spec = importlib.util.spec_from_file_location('certificate_under_test', {path!r})
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
{mutation}
"""
                result = subprocess.run([sys.executable, "-B", "-O", "-c", program],
                                        cwd=ROOT, capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected_message, result.stderr)


if __name__ == "__main__":
    unittest.main()
