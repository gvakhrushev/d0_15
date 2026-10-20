#!/usr/bin/env python3
"""Navigation must work without research history or executing proof checks."""
from __future__ import annotations

import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import gr_assembly as gr
import gr_synthesis as synthesis


class SynthesisTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.directory = self.root / synthesis.DIRECTORY
        self.directory.mkdir(parents=True)
        self.result = {"id": "r", "statement": "Conditional vacuum source theorem",
                       "outcome": "positive", "scope_level": "family", "hypotheses": {"h": "Fixed source"},
                       "evidence": [{"ref": "a" * 40, "path": "unfetched.md", "sha256": "b" * 64}]}
        self.piece = {"id": "vacuum", "title": "Стационарный вакуум", "contribution": "Reuse a conditional theorem.",
                      "next_question": "Solve the genuine source.", "consumers": ["A"], "results": ["r"],
                      "tags": ["источник"]}
        self.contract = {"schema": "d0-gr-assembly/1", "obligations": [{"id": "A", "statement": "Physical source"}],
                         "synthesis": [self.piece], "task_bindings": {"TASK": {"obligations": ["A"]}}}
        self.intake = {"schema": "d0-gr-applications/1", "results": [self.result]}

    def save(self):
        for name, value in [("contract.json", self.contract), ("applications.json", self.intake)]:
            (self.directory / name).write_text(json.dumps(value))

    def test_navigation_needs_only_local_metadata_not_unfetched_evidence(self):
        self.save()
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        with patch.object(gr, "load", side_effect=AssertionError("full proof load forbidden")), \
             patch("subprocess.run", side_effect=AssertionError("execution forbidden")), \
             patch("subprocess.check_output", side_effect=AssertionError("Git/network forbidden")), \
             contextlib.redirect_stdout(io.StringIO()) as output:
            rc = gr.main(["--repo-root", str(self.root), "--json", "puzzle", "vacuum"])
        data = json.loads(output.getvalue())
        self.assertEqual(rc, 0)
        self.assertFalse(data["evidence_verified"])
        self.assertFalse(data["scientific_promotion"])
        self.assertFalse(data["live_verified"])
        self.assertEqual(data["pieces"][0]["uses"][0]["hypotheses"], {"h": "Fixed source"})
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_exact_piece_id_beats_mentions_in_other_results(self):
        other = {**self.piece, "id": "roots", "title": "Other vacuum result"}
        self.contract["synthesis"].append(other)
        self.save()
        self.assertEqual([p["id"] for p in synthesis.read(self.root, "vacuum")["pieces"]], ["vacuum"])

    def test_russian_query_and_hypothesis_are_searchable(self):
        self.save()
        self.assertEqual(len(synthesis.read(self.root, "источник")["pieces"]), 1)
        self.assertEqual(len(synthesis.read(self.root, "fixed source")["pieces"]), 1)
        self.assertEqual(synthesis.read(self.root, "unknown")["pieces"], [])

    def test_alias_is_display_only_and_keeps_original_records(self):
        duplicate = {**self.result, "id": "duplicate", "navigation_alias_of": "r",
                     "interface_id": "different-interface", "scope_level": "different-scope",
                     "hypotheses": {"extra": "retained"},
                     "statement": "A separately scoped statement with the same outcome."}
        self.intake["results"].append(duplicate)
        self.piece["results"] = ["duplicate", "r"]
        self.save()
        data = synthesis.read(self.root)
        self.assertEqual(len(data["pieces"][0]["uses"]), 1)
        self.assertEqual(data["pieces"][0]["uses"][0]["also_indexed_as"], ["duplicate"])
        alias = data["pieces"][0]["uses"][0]["alias_records"][0]
        self.assertEqual(alias["interface_id"], "different-interface")
        self.assertEqual(alias["scope_level"], "different-scope")
        self.assertEqual(alias["hypotheses"], {"extra": "retained"})
        rendered = synthesis.render(data)
        self.assertIn("A separately scoped statement with the same outcome.", rendered)
        self.assertIn("different-interface", rendered)
        self.assertEqual(len(json.loads((self.directory / "applications.json").read_text())["results"]), 2)

    def test_shared_evidence_does_not_automatically_merge_distinct_results(self):
        self.intake["results"].append({**self.result, "id": "other-theorem"})
        self.piece["results"].append("other-theorem")
        self.save()
        self.assertEqual(len(synthesis.read(self.root)["pieces"][0]["uses"]), 2)

    def test_alias_cycles_unknown_targets_and_opposite_outcomes_rejected(self):
        for alias in ["r", "missing"]:
            self.result["navigation_alias_of"] = alias
            with self.assertRaises(ValueError):
                synthesis.validate_navigation(self.contract, self.intake)
        self.result.pop("navigation_alias_of")
        self.intake["results"].append({**self.result, "id": "negative", "outcome": "negative",
                                        "navigation_alias_of": "r"})
        with self.assertRaisesRegex(ValueError, "preserve outcome"):
            synthesis.validate_navigation(self.contract, self.intake)

    def test_dangling_consumer_and_result_rejected(self):
        for field in ["consumers", "results"]:
            contract = copy.deepcopy(self.contract)
            contract["synthesis"][0][field] = ["missing"]
            with self.assertRaises(ValueError):
                synthesis.validate_navigation(contract, self.intake)

    def test_fixed_readings_reject_moving_ref_and_path_traversal(self):
        for ref, path in [("main", "proof.md"), ("a" * 40, "../proof.md"), ("a" * 40, "/proof.md")]:
            self.piece["readings"] = [{"ref": ref, "path": path, "label": "Lead"}]
            with self.assertRaises(ValueError):
                synthesis.validate_navigation(self.contract, self.intake)

    def test_evidence_links_reject_malformed_refs_and_unsafe_paths(self):
        for ref, path in [("main", "proof.md"), ("a" * 40, "../proof.md"),
                          ("a" * 40, "/proof.md"), ("a" * 40, "a\\b.md")]:
            self.result["evidence"] = [{"ref": ref, "path": path}]
            with self.assertRaisesRegex(ValueError, "evidence pointer"):
                synthesis.validate_navigation(self.contract, self.intake)
        self.result["evidence"] = [{"ref": "a" * 40, "path": "proof.md"}]
        self.save()
        self.assertIn("/blob/" + "a" * 40 + "/proof.md",
                      synthesis.render(synthesis.read(self.root)))

    def test_optional_navigation_adds_no_result_registration_requirement(self):
        self.contract.pop("synthesis")
        self.save()
        self.assertEqual(synthesis.read(self.root)["pieces"], [])

    def test_render_points_to_fixed_proof_and_existing_dispatch(self):
        self.save()
        output = synthesis.render(synthesis.read(self.root))
        self.assertIn("/blob/" + "a" * 40 + "/unfetched.md", output)
        self.assertIn("task_dispatch.py TASK-ID", output)
        self.assertIn("окончательная проверка", output)

    def test_evidence_link_encodes_markdown_and_url_delimiters(self):
        self.result["evidence"] = [{"ref": "a" * 40, "path": "proof (current)#1.md"}]
        self.save()
        output = synthesis.render(synthesis.read(self.root))
        self.assertIn("proof%20%28current%29%231.md", output)


if __name__ == "__main__":
    unittest.main()
