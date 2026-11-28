#!/usr/bin/env python3
"""Ensure DESI demo code cannot mutate inputs or issue an observational verdict."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CERT_DIR = ROOT / "04_CERTIFICATES"
REAL_RUNNER = CERT_DIR / "vp_desi_bao_sde_real_data.py"
DIAGNOSTIC = CERT_DIR / "vp_desi_bao_sde_failure_diagnostics.py"


def run_python(program):
    return subprocess.run([sys.executable, "-B", "-O", "-c", program], cwd=ROOT,
                          capture_output=True, text=True)


class DesiBaoPipelineBoundaryTest(unittest.TestCase):
    def test_ready_flags_and_missing_file_do_not_create_data_or_issue_verdict(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"status": "READY", "official_data_status": "READY",
                                            "sample_data": False,
                                            "local_path": str(root / "missing.csv")}))
            before = manifest.read_bytes()
            program = f"""
import importlib.util
spec = importlib.util.spec_from_file_location('desi_demo', {str(REAL_RUNNER)!r})
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.ROOT = {str(root)!r}
module.MANIFEST = __import__('pathlib').Path({str(manifest)!r})
module.PASSPORT_DIR = __import__('pathlib').Path({str(root)!r})
module.CACHE_DIR = __import__('pathlib').Path({str(root / 'cache')!r})
raise SystemExit(module.main())
"""
            result = run_python(program)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("SKIP_DESI_BAO_SDE_VALUE_PIPELINE_NOT_IMPLEMENTED", result.stdout)
            self.assertNotIn("FAIL_DESI_BAO_SDE_REAL_DATA", result.stdout)
            self.assertNotIn("PASS_DESI_BAO_SDE_REAL_DATA", result.stdout)
            self.assertEqual(manifest.read_bytes(), before)
            self.assertEqual({p.name for p in root.iterdir()}, {"manifest.json"})

    def test_hash_verified_file_does_not_imply_implemented_confrontation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = root / "data.csv"
            data.write_text("not a validated observational pipeline\n")
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"status": "READY", "sample_data": False,
                                            "local_path": str(data),
                                            "sha256": hashlib.sha256(data.read_bytes()).hexdigest()}))
            program = f"""
import importlib.util, pathlib, sys
sys.path.insert(0, {str(CERT_DIR)!r})
spec = importlib.util.spec_from_file_location('desi_diagnostic', {str(DIAGNOSTIC)!r})
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.MANIFEST = pathlib.Path({str(manifest)!r})
module.output_path = lambda *_: pathlib.Path({str(root / 'result.json')!r})
raise SystemExit(module.main())
"""
            result = run_python(program)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("SKIP_BAO_SDE_VALIDATED_VALUE_PIPELINE_REQUIRED",
                          (root / "result.json").read_text())
            self.assertNotIn("DATA_PRESENT_RUN_REAL_DATA_RUNNER", result.stdout)

    def test_altered_frozen_coefficient_fails_under_optimization(self):
        program = f"""
import importlib.util, sys
sys.path.insert(0, {str(CERT_DIR)!r})
spec = importlib.util.spec_from_file_location('desi_diagnostic', {str(DIAGNOSTIC)!r})
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.POLY_C = 360
module.main()
"""
        result = run_python(program)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("frozen S_DE polynomial coefficients", result.stderr)


if __name__ == "__main__":
    unittest.main()
