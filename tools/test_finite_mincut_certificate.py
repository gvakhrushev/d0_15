#!/usr/bin/env python3
"""Regression tests for the original finite min-cut certificate inputs."""
from itertools import combinations, product
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "04_CERTIFICATES" / "vp_finite_mincut_holographic_entropy.py"
sys.path.insert(0, str(CERT.parent))
spec = importlib.util.spec_from_file_location("finite_mincut", CERT)
certificate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(certificate)


def brute_min_cut(cap, source, sink, n):
    others = [v for v in range(n) if v not in (source, sink)]
    return min(
        sum(c for (u, v), c in cap.items() if u in side and v not in side)
        for size in range(len(others) + 1)
        for subset in combinations(others, size)
        for side in [{source, *subset}]
    )


class FiniteMincutTest(unittest.TestCase):
    def test_all_small_directed_graphs(self):
        edges = [(u, v) for u in range(3) for v in range(3) if u != v]
        for capacities in product(range(3), repeat=len(edges)):
            cap = dict(zip(edges, capacities))
            flow, cut = certificate.max_flow_min_cut(cap, 0, 2, 3)
            expected = brute_min_cut(cap, 0, 2, 3)
            self.assertEqual((flow, cut), (expected, expected), cap)

    def test_reverse_zero_does_not_erase_forward_capacity(self):
        self.assertEqual(certificate.max_flow_min_cut({(0, 1): 2, (1, 0): 0}, 0, 1, 2),
                         (2, 2))

    def test_original_inputs_and_optimized_mode(self):
        program = f"""
import importlib.util, json, pathlib, sys
sys.path.insert(0, {str(CERT.parent)!r})
spec = importlib.util.spec_from_file_location('finite_mincut_under_test', {str(CERT)!r})
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.output_path = lambda *args: pathlib.Path('result.json')
module.run_certificate()
"""
        for flags in ([], ["-O"]):
            with self.subTest(flags=flags), tempfile.TemporaryDirectory() as temp:
                result = subprocess.run([sys.executable, "-B", *flags, "-c", program],
                                        cwd=temp, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                data = json.loads((Path(temp) / "result.json").read_text())
                self.assertEqual(data["max_flow"], 0)
                self.assertEqual(data["min_cut"], 0)
                self.assertEqual(data["fixed_partition_cut"], 4)
                self.assertEqual(data["S_EE"], 1)
                self.assertIn("not computed quantum entropy", data["S_EE_scope"])
                self.assertNotIn("PASS_FINITE_MINCUT_ENTANGLEMENT_A4", result.stdout)

    def test_false_historical_equality_fails_under_optimization(self):
        program = f"""
import importlib.util, sys
sys.path.insert(0, {str(CERT.parent)!r})
spec = importlib.util.spec_from_file_location('finite_mincut_under_test', {str(CERT)!r})
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.max_flow_min_cut = lambda *args: (4.0, 4.0)
module.run_certificate()
"""
        result = subprocess.run([sys.executable, "-B", "-O", "-c", program],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("original 0->3 network", result.stderr)

    def test_disagreeing_flow_and_cut_fails_under_optimization(self):
        program = f"""
import importlib.util, sys
sys.path.insert(0, {str(CERT.parent)!r})
spec = importlib.util.spec_from_file_location('finite_mincut_under_test', {str(CERT)!r})
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.max_flow_min_cut = lambda *args: (0.0, 4.0)
module.run_certificate()
"""
        result = subprocess.run([sys.executable, "-B", "-O", "-c", program],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("differs from independently computed min-cut", result.stderr)


if __name__ == "__main__":
    unittest.main()
