"""Diagnostics for unsupported safe workspace-source opening."""
import contextlib
import io
import json
import pathlib
import sys
import unittest
from unittest.mock import patch

from tools import proof_architecture as proof
from tools import proof_architecture_cold_start as legacy
from tools import proof_architecture_cold_start_v3 as paged
from tools import compact_proof_architecture_cold_start_v3 as compactor
from tools import test_proof_cold_start_v3 as v3_fixtures


class WorkspaceSafeOpenDiagnosticTests(unittest.TestCase):
    def cli(self, enabled, requested):
        data = {"snapshot_commit": "a" * 40, "source_digests": {}, "worktree_dirty": False}
        args = ["proof_architecture.py", "--json", "search", "query"]
        if requested:
            args += ["--workspace-source-pages", "1"]
        stdout = io.StringIO()
        with patch.object(sys, "argv", args), \
             patch.object(proof, "_configure_stdout_utf8"), \
             patch.object(proof, "load_dataset", return_value=data), \
             patch.object(proof, "structured_search", return_value=[]), \
             patch.object(proof, "full_text_search", return_value=[]), \
             patch.object(proof, "expand_workspace_source_pages", return_value=[]), \
             patch.object(proof, "workspace_page_safe_open_supported", return_value=enabled), \
             contextlib.redirect_stdout(stdout):
            self.assertEqual(proof.main(), 0)
        return json.loads(stdout.getvalue())

    def test_search_reports_unsupported_only_for_requested_feature(self):
        unsupported = self.cli(False, True)
        self.assertEqual(unsupported["workspace_source_access"]["status"], "unsupported_safe_open")
        self.assertEqual(unsupported["workspace_source_pages"], [])
        for control in (self.cli(True, True), self.cli(False, False)):
            self.assertNotIn("workspace_source_access", control)

    def test_verified_query_never_credits_or_rechecks_unsupported_pages(self):
        root = pathlib.Path.cwd()
        query = "arbitrary request"
        result = {"query": query, "ranked_pages": paged._ranked_pages([]),
                  "source_pages": [], "workspace_source_pages": []}
        with patch.object(proof, "workspace_page_safe_open_supported", return_value=False):
            self.assertEqual(paged.verified_query(root, query, result, set()), [])
            missing = legacy._required_source_status([(query, [])], {"path": "02_REGISTRY/missing.md"})
            self.assertFalse(missing["found"])
            forged = {**result, "workspace_source_pages": [{"candidates": [{"direct_content": True}]}]}
            with self.assertRaisesRegex(ValueError, "unsupported_safe_open"):
                paged.verified_query(root, query, forged, set())

    def test_compactor_labels_its_own_current_capability(self):
        fixture = v3_fixtures.PagedColdStartTests("test_single_batched_run_compacts_without_cross_query_leak")
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        with patch.object(proof, "workspace_page_safe_open_supported", return_value=False):
            report = fixture.execute()
            with patch.object(legacy, "CASES", [fixture.fixture]), \
                 patch.object(proof, "load_dataset", return_value=fixture.dataset):
                summary = compactor.compact(json.dumps(report).encode(), fixture.root)
            self.assertEqual(summary["workspace_source_verification"]["status"], "unsupported_safe_open")
            self.assertIn("current verification only", summary["workspace_source_verification"]["scope"])
            self.assertIsNone(summary["search_cases_found_all_sources"])
            self.assertFalse(summary["cases"][0]["all_required_sources_found"])
            self.assertEqual(summary["cases"][0]["workspace_source_page_count"], 0)
            old = json.loads(json.dumps(report))
            old.pop("workspace_source_page_budget")
            for case in old["cases"]:
                for result in case["query_results"]:
                    result.pop("workspace_source_pages")
            with patch.object(legacy, "CASES", [fixture.fixture]), \
                 patch.object(proof, "load_dataset", return_value=fixture.dataset):
                old_summary = compactor.compact(json.dumps(old).encode(), fixture.root)
            self.assertNotIn("workspace_source_verification", old_summary)
        with patch.object(proof, "workspace_page_safe_open_supported", return_value=True), \
             patch.object(paged, "workspace_source_pages", return_value=[]), \
             patch.object(legacy, "CASES", [fixture.fixture]), \
             patch.object(proof, "load_dataset", return_value=fixture.dataset):
            supported_summary = compactor.compact(json.dumps(report).encode(), fixture.root)
        self.assertNotIn("workspace_source_verification", supported_summary)


if __name__ == "__main__":
    unittest.main()
