#!/usr/bin/env python3
"""Hostile CSV controls for the repository's actual structural validator."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


VALIDATOR = Path(__file__).with_name("validate_repo.py")


class RegistryCsvShapeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="d0-registry-shape-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in ("tools", "01_BOOKS", "02_REGISTRY", "03_FORMALIZATION/D0",
                          "04_CERTIFICATES", "05_EXPERIMENTS"):
            (self.root / directory).mkdir(parents=True, exist_ok=True)
        shutil.copyfile(VALIDATOR, self.root / "tools/validate_repo.py")
        (self.root / "03_FORMALIZATION/D0/Test.lean").write_text("-- fixture\n")
        self.claim_header = "claim_id,lean_module,lean_theorem,python_cert,release_status,notes\n"
        self.claim = "D0-TEST-001,D0.Test,theorem_name,,PROOF-TARGET,Finite scope only\n"
        self.write("claims.csv", self.claim_header + self.claim)
        self.write("assumptions.csv", "assumption_id,lean_file,claim_id,status\n"
                   "D0-ASSUMPTION-001,D0/Test.lean,D0-TEST-001,OPEN\n")
        self.write("formal_support.csv", "lean_module,lean_file,role,referenced_by\n"
                   "D0.Test,D0/Test.lean,fixture,D0-TEST-001\n")
        self.write("aliases.csv", "legacy_id,kind,canonical_claim_id,first_reference,note\n"
                   "D0-OLD-001,fixture,D0-TEST-001,BOOK_00,Finite scope\n")

    def write(self, name, text):
        (self.root / "02_REGISTRY" / name).write_text(text, encoding="utf-8")

    def run_validator(self):
        return subprocess.run([sys.executable, str(self.root / "tools/validate_repo.py")],
                              cwd=self.root, capture_output=True, text=True, check=False)

    def assert_rejected(self, diagnostic):
        result = self.run_validator()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(diagnostic, result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_valid_quoted_note_retains_commas(self):
        self.write("claims.csv", self.claim_header + self.claim.replace(
            "Finite scope only", '"Symmetry, divergence and cutoff are separate witnesses"'))
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unquoted_note_overflow_is_rejected(self):
        self.write("claims.csv", self.claim_header + self.claim.replace(
            "Finite scope only", "Finite scope, not continuum closure"))
        self.assert_rejected("claims.csv:2: extra CSV fields")

    def test_truncated_row_is_rejected_without_traceback(self):
        self.write("claims.csv", self.claim_header + "D0-TEST-001,D0.Test,theorem_name\n")
        self.assert_rejected("claims.csv:2: missing CSV fields")

    def test_duplicate_header_is_rejected(self):
        self.write("claims.csv", self.claim_header.rstrip() + ",notes\n" + self.claim)
        self.assert_rejected("claims.csv: duplicate column names")

    def test_missing_header_is_rejected_without_traceback(self):
        self.write("claims.csv", self.claim_header.replace("lean_theorem,", "") + self.claim)
        self.assert_rejected("claims.csv: missing columns ['lean_theorem']")

    def test_malformed_quote_is_rejected(self):
        self.write("claims.csv", self.claim_header + self.claim.replace(
            "Finite scope only", '"unterminated'))
        self.assert_rejected("claims.csv: CSV parse error")

    def test_other_registries_also_reject_overflow(self):
        for name in ("assumptions.csv", "formal_support.csv", "aliases.csv"):
            with self.subTest(registry=name):
                path = self.root / "02_REGISTRY" / name
                original = path.read_text()
                path.write_text(original.rstrip() + ",unexpected\n")
                self.assert_rejected(name + ":2: extra CSV fields")
                path.write_text(original)


if __name__ == "__main__":
    unittest.main()
