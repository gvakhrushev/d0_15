#!/usr/bin/env python3
"""Controls for lexical Lean registry reference auditing."""
import csv
from pathlib import Path
import tempfile
import unittest

import audit_lean_claim_references as audit


class LeanReferenceAuditTest(unittest.TestCase):
    def test_comments_strings_and_nested_comments_do_not_define_names(self):
        source = '''
/- theorem hidden : True := by
   /- theorem nested : True := by -/
-/
-- def lineComment : Nat := 1
def label : String := "theorem inString"
@[simp] theorem visible' : True := by trivial
theorem Name.θ₁ : True := by trivial
'''
        source += "\ndef quote : Char := " + chr(39) + '"' + chr(39)
        source += "\ntheorem afterQuote : True := by trivial\n"
        declarations = set(audit.DECLARATION.findall(audit.erase_comments_and_strings(source)))
        self.assertEqual(
            declarations, {"label", "visible'", "Name.θ₁", "quote", "afterQuote"}
        )

    def test_unterminated_comment_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unterminated"):
            audit.erase_comments_and_strings("/- theorem hidden")

    def test_registry_scan_reports_missing_names(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lean_dir = root / "03_FORMALIZATION" / "D0"
            lean_dir.mkdir(parents=True)
            (lean_dir / "Example.lean").write_text(
                "namespace D0\ntheorem present : True := by trivial\n"
                "theorem Name.θ₁ : True := by trivial\nend D0\n",
                encoding="utf-8",
            )
            registry = root / "02_REGISTRY"
            registry.mkdir()
            with (registry / "claims.csv").open("w", newline="", encoding="utf-8") as out:
                writer = csv.DictWriter(
                    out, fieldnames=["claim_id", "lean_module", "lean_theorem"]
                )
                writer.writeheader()
                writer.writerow({
                    "claim_id": "D0-EXAMPLE-001",
                    "lean_module": "D0.Example",
                    "lean_theorem": "present;Name.θ₁;missing",
                })
                writer.writerow({
                    "claim_id": "D0-NO-MODULE-001",
                    "lean_module": "",
                    "lean_theorem": "ignored",
                })
            missing, checked = audit.find_unresolved(root)
            self.assertEqual(checked, 3)
            self.assertEqual(missing, {("D0-EXAMPLE-001", "missing")})


if __name__ == "__main__":
    unittest.main()
