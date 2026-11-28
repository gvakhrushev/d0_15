#!/usr/bin/env python3
"""Exercise feedback certificate checks in isolated normal and optimized runs."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MUTATIONS = {
    "vp_feedback_partition_function.py": (
        "cycle_sum = sum((z**m / m) * trace_power_2x2(r, m) for m in range(1, 16))",
        "cycle_sum = 0.0",
    ),
    "vp_finite_feedback_equation_of_state.py": (
        "pressure = (1.0 / beta) * dlogz_dv",
        "pressure = 0.0",
    ),
    "vp_terminal_feedback_modes.py": (
        'mode = {"eigenmode": True, "near_critical": True, "terminal_projected": True}',
        'mode = {"eigenmode": False, "near_critical": True, "terminal_projected": True}',
    ),
    "vp_pressure_capacity_balance.py": (
        'return "expansion"',
        'return "BROKEN"',
    ),
    "vp_sde_feedback_reduction.py": (
        "return 160 * lam * lam - 480 * lam + 359",
        "return 160 * lam * lam - 480 * lam + 358",
    ),
}


def prepare_tree(directory):
    root = Path(directory)
    certificates = root / "04_CERTIFICATES"
    certificates.mkdir()
    for name in ["cert_runtime.py", *MUTATIONS]:
        shutil.copy2(ROOT / "04_CERTIFICATES" / name, certificates / name)
    passport = root / "05_EXPERIMENTS" / "VacuumFeedback"
    passport.mkdir(parents=True)
    name = "feedback_partition_function_summary.json"
    shutil.copy2(ROOT / "05_EXPERIMENTS" / "VacuumFeedback" / name, passport / name)
    return root


def execute(root, name, optimized):
    env = os.environ.copy()
    env.pop("PYTHONOPTIMIZE", None)
    args = [sys.executable, "-B"]
    if optimized:
        args.append("-O")
    return subprocess.run(args + [str(root / "04_CERTIFICATES" / name)], cwd=root,
                          env=env, capture_output=True, text=True, timeout=30)


class FeedbackOptimizationTest(unittest.TestCase):
    def test_valid_outputs_match_in_both_modes(self):
        with tempfile.TemporaryDirectory(prefix="d0-feedback-optimization-") as directory:
            root = prepare_tree(directory)
            for name in MUTATIONS:
                with self.subTest(certificate=name):
                    plain = execute(root, name, False)
                    optimized = execute(root, name, True)
                    self.assertEqual(plain.returncode, 0, plain.stderr)
                    self.assertEqual(optimized.returncode, 0, optimized.stderr)
                    self.assertEqual((plain.stdout, plain.stderr),
                                     (optimized.stdout, optimized.stderr))

    def test_mutations_are_rejected_in_both_modes(self):
        for name, (source, replacement) in MUTATIONS.items():
            with self.subTest(certificate=name):
                with tempfile.TemporaryDirectory(prefix="d0-feedback-mutation-") as directory:
                    root = prepare_tree(directory)
                    script = root / "04_CERTIFICATES" / name
                    contents = script.read_text(encoding="utf-8")
                    self.assertEqual(contents.count(source), 1)
                    script.write_text(contents.replace(source, replacement), encoding="utf-8")
                    for optimized in (False, True):
                        result = execute(root, name, optimized)
                        self.assertNotEqual(result.returncode, 0, name)
                        self.assertIn("AssertionError", result.stderr)
                        self.assertNotIn("tracked canonical artifact mismatch", result.stderr)


if __name__ == "__main__":
    unittest.main()
