#!/usr/bin/env python3
"""Focused controls for declaration-name resolution and Lean source generation."""
from __future__ import annotations

import contextlib
import json
import pathlib
import subprocess
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lean_declaration_inventory as inventory


class DeclarationInventoryTests(unittest.TestCase):
    def test_candidate_names_keep_alternate_registry_qualification_forms(self):
        self.assertEqual(
            inventory.candidate_names("D0.Matter.ArchiveStressCoupling", "Matter.matterStressMatrix_symmetric"),
            [
                "D0.Matter.ArchiveStressCoupling.Matter.matterStressMatrix_symmetric",
                "D0.Matter.matterStressMatrix_symmetric",
            ],
        )

    def test_all_claim_requests_keep_unresolved_rows_and_deduplicate_exact_names(self):
        mapping, names = inventory.all_claim_requests([
            {"claim_id": "CLM-1", "lean_module": "D0.Foo", "lean_theorem": "bar; D0.Baz.qux"},
            {"claim_id": "CLM-2", "lean_module": "D0.Foo", "lean_theorem": "bar"},
            {"claim_id": "CLM-3", "lean_module": "", "lean_theorem": ""},
        ])
        self.assertEqual(mapping["claim_rows"], 3)
        self.assertEqual(names, ["D0.Foo.bar", "D0.bar", "D0.Baz.qux"])
        unresolved = [row for row in mapping["mappings"] if row["claim_id"] == "CLM-3"]
        self.assertEqual(unresolved[0]["candidate_names"], [])
        self.assertIsNone(unresolved[0]["theorem_atom"])

    def test_exact_d0_names_are_not_requalified(self):
        self.assertEqual(
            inventory.candidate_names("D0.Foundation.VerificationCore", "D0.Foundation.VerificationCore.verification_core"),
            ["D0.Foundation.VerificationCore.verification_core"],
        )

    def test_name_expression_escapes_component_text(self):
        rendered = inventory.name_expr("D0.Test.a\"b")
        self.assertIn('"a\\\"b"', rendered)
        self.assertTrue(rendered.startswith("Lean.Name.str ("))

    def test_collector_queries_elaborated_environment_and_axioms(self):
        script = inventory.lean_collector(["D0.Foundation.VerificationCore.verification_core"], "D0.All")
        self.assertIn("import D0.All", script)
        self.assertIn("env.find? target", script)
        self.assertIn("(\"exists\", toJson false)", script)
        self.assertIn("collectAxioms target", script)
        self.assertIn("forallTelescope info.type", script)
        self.assertIn("withTransparency .default (whnf localDecl.type)", script)
        self.assertIn("withTransparency .default (whnf target)", script)
        self.assertIn('("conclusion_whnf", toJson conclusionWhnf)', script)
        self.assertIn("open Lean Meta Elab Command", script)
        self.assertIn("proof_dependencies", script)
        self.assertIn("is_proposition", script)
        self.assertIn(inventory.PREFIX, script)

    def test_import_root_rejects_lean_source_injection(self):
        with self.assertRaises(ValueError):
            inventory.lean_collector([], "D0.All\n#eval IO.println 1")

    def test_inventory_builds_import_root_before_reading_environment(self):
        declaration = "D0.Foo.bar"
        record = {
            "name": declaration,
            "exists": True,
            "elaborated_type": "D0.StatusAlias",
            "binders": [],
            "conclusion_whnf": "True",
            "type_dependencies": [],
            "proof_dependencies": [],
            "axioms": [],
            "module": "D0.Foo",
            "declaration_ranges": None,
        }
        build = subprocess.CompletedProcess(["lake", "build", "D0.Foo"], 0, "", "")
        collect = subprocess.CompletedProcess(
            ["lake", "env", "lean"], 0,
            inventory.PREFIX + json.dumps(record) + "\n", "",
        )
        with patch.object(inventory.lean_task_build, "build_lock",
                          side_effect=lambda _path: contextlib.nullcontext()) as lock:
            with patch.object(inventory.lean_task_build, "source_digest",
                              side_effect=["current", "current", "current"]):
                with patch.object(inventory.subprocess, "run",
                                  side_effect=[build, collect]) as run:
                    rows, _collector_sha, source_sha = inventory.run_inventory(
                        [declaration], "D0.Foo")

        self.assertEqual(run.call_args_list[0].args[0], ["lake", "build", "D0.Foo"])
        self.assertEqual(rows[0]["name"], declaration)
        self.assertEqual(rows[0]["elaborated_type"], "D0.StatusAlias")
        self.assertEqual(rows[0]["conclusion_whnf"], "True")
        self.assertEqual(source_sha, "current")
        lock.assert_called_once()

    def test_inventory_discards_build_when_lean_sources_change(self):
        build = subprocess.CompletedProcess(["lake", "build", "D0.Foo"], 0, "", "")
        with patch.object(inventory.lean_task_build, "build_lock",
                          side_effect=lambda _path: contextlib.nullcontext()):
            with patch.object(inventory.lean_task_build, "source_digest",
                              side_effect=["before-build", "after-build"]):
                with patch.object(inventory.subprocess, "run", return_value=build) as run:
                    with self.assertRaisesRegex(RuntimeError, "changed while the import root"):
                        inventory.run_inventory(["D0.Foo.bar"], "D0.Foo")
        run.assert_called_once()


if __name__ == "__main__":
    unittest.main()
