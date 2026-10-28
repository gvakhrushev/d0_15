"""Small Git-backed controls for proof-architecture receipt freshness.

Historical validity and freshness of the current inputs are distinct.  These
tests never replay the real corpus or change an actual scientific registry.
"""
from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from tools import proof_architecture as proof


AUTHORITY_PATHS = (
    "02_REGISTRY/claims.csv",
    "02_REGISTRY/assumptions.csv",
    "02_REGISTRY/formal_support.csv",
    "02_REGISTRY/aliases.csv",
    "02_REGISTRY/gr_assembly/applications.json",
    "02_REGISTRY/gr_assembly/contract.json",
    "02_REGISTRY/presupposition_edges.json",
)
RUNNER = "tools/proof_architecture_cold_start.py"
SEARCH = "tools/proof_architecture.py"
COMPACTOR = "tools/compact_proof_architecture_cold_start.py"
COMPARISON = "tools/proof_architecture_process_comparison.py"
TESTS = "tools/test_proof_architecture.py"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class ReceiptFreshnessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="d0-receipt-freshness-")
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.git("init", "-q")
        self.git("config", "core.autocrlf", "false")
        self.contents = {}
        for path in (*AUTHORITY_PATHS, RUNNER, SEARCH, COMPACTOR, COMPARISON, TESTS):
            data = ("fixture for " + path + "\n").encode("utf-8")
            self.write(path, data)
            self.contents[path] = data
        self.git("add", "--all")
        self.git("-c", "user.name=Receipt Test", "-c", "user.email=test@example.invalid",
                 "commit", "-q", "-m", "fixture")
        self.head = self.git("rev-parse", "HEAD").strip()
        self.report = {
            "schema": "d0-proof-architecture-cold-start-summary-v2",
            "snapshot_commit": self.head,
            "worktree_dirty": False,
            "authority_source_digests": {
                path: digest(self.contents[path]) for path in AUTHORITY_PATHS
            },
            "replay": {
                "source_commit": self.head,
                "runner_sha256": digest(self.contents[RUNNER]),
                "search_engine_sha256": digest(self.contents[SEARCH]),
                "compactor_sha256": digest(self.contents[COMPACTOR]),
                "test_sha256": digest(self.contents[TESTS]),
            },
        }

    def git(self, *args: str) -> str:
        result = subprocess.run(["git", *args], cwd=self.root, check=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, encoding="utf-8")
        return result.stdout

    def write(self, path: str, data: bytes) -> None:
        destination = self.root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)

    def status(self, report: dict | None = None) -> dict:
        return proof.receipt_status(self.root, self.report if report is None else report)

    def test_legacy_clean_receipt_is_historical_not_current(self) -> None:
        result = self.status()
        self.assertEqual(result["historical_selected_bindings_status"], "verified")
        self.assertEqual(result["authority_status"], "current")
        self.assertEqual(result["tool_status"], "current")
        self.assertEqual(result["search_corpus_status"], "unverified")
        self.assertEqual(result["overall_status"], "unverified")

    def test_authority_mutation_does_not_damage_historical_pin(self) -> None:
        path = "02_REGISTRY/formal_support.csv"
        self.write(path, self.contents[path] + b"new support row\n")
        result = self.status()
        self.assertEqual(result["historical_selected_bindings_status"], "verified")
        self.assertEqual(result["authority_status"], "changed")
        self.assertEqual(result["tool_status"], "current")
        self.assertEqual(result["overall_status"], "stale")
        self.assertTrue(result["authority_changes"])

    def test_tool_mutation_is_detected_without_changing_history(self) -> None:
        self.write(SEARCH, self.contents[SEARCH] + b"# changed query semantics\n")
        result = self.status()
        self.assertEqual(result["historical_selected_bindings_status"], "verified")
        self.assertEqual(result["authority_status"], "current")
        self.assertEqual(result["tool_status"], "changed")
        self.assertEqual(result["overall_status"], "stale")
        self.assertTrue(result["tool_changes"])

    def test_deleted_current_authority_keeps_historical_binding(self) -> None:
        path = "02_REGISTRY/formal_support.csv"
        (self.root / path).unlink()
        result = self.status()
        self.assertEqual(result["historical_selected_bindings_status"], "verified")
        self.assertEqual(result["authority_status"], "changed")
        self.assertIn(path, result["current_missing"])
        self.assertEqual(result["overall_status"], "stale")

    def test_deleted_current_tool_keeps_historical_binding(self) -> None:
        (self.root / SEARCH).unlink()
        result = self.status()
        self.assertEqual(result["historical_selected_bindings_status"], "verified")
        self.assertEqual(result["tool_status"], "changed")
        self.assertIn(SEARCH, result["current_missing"])
        self.assertEqual(result["overall_status"], "stale")

    def test_byte_change_to_line_endings_is_not_silently_normalized(self) -> None:
        path = "02_REGISTRY/formal_support.csv"
        self.write(path, self.contents[path].replace(b"\n", b"\r\n"))
        result = self.status()
        self.assertEqual(result["historical_selected_bindings_status"], "verified")
        self.assertEqual(result["authority_status"], "changed")
        self.assertEqual(result["overall_status"], "stale")

    def test_added_search_source_makes_retrieval_stale(self) -> None:
        path = "02_REGISTRY/research/new_candidate.md"
        self.write(path, b"A newly indexed source\n")
        result = self.status()
        self.assertEqual(result["historical_selected_bindings_status"], "verified")
        self.assertEqual(result["authority_status"], "current")
        self.assertEqual(result["tool_status"], "current")
        self.assertEqual(result["search_corpus_status"], "possibly_changed")
        self.assertIn(path, result["checked_potential_search_input_changes"])
        self.assertEqual(result["overall_status"], "unverified")

    def test_corpus_candidate_limit_is_explicit_and_bounded(self) -> None:
        for index in range(130):
            self.write(f"02_REGISTRY/research/candidate_{index:03}.md", b"source\n")
        result = self.status()
        self.assertEqual(result["checked_corpus_candidate_count"], 128)
        self.assertTrue(result["corpus_candidates_truncated"])
        self.assertEqual(result["checked_potential_search_input_change_count"], 128)
        self.assertEqual(len(result["checked_potential_search_input_changes"]), 20)
        self.assertTrue(result["checked_potential_search_input_changes_truncated"])
        self.assertEqual(result["historical_selected_bindings_status"], "verified")
        self.assertEqual(result["search_corpus_status"], "possibly_changed")
        self.assertEqual(result["overall_status"], "unverified")

    def test_git_unavailable_keeps_candidate_scope_unknown(self) -> None:
        with mock.patch.object(proof.subprocess, "run", side_effect=OSError("git unavailable")):
            result = self.status()
        self.assertEqual(result["historical_selected_bindings_status"], "unverified")
        self.assertEqual(result["search_corpus_status"], "unverified")
        self.assertIsNone(result["checked_corpus_candidate_count"])
        self.assertIsNone(result["corpus_candidates_truncated"])
        self.assertIsNone(result["checked_potential_search_input_change_count"])
        self.assertEqual(result["checked_potential_search_input_changes"], [])
        self.assertEqual(result["overall_status"], "unverified")

    def test_excluded_report_does_not_prove_corpus_change(self) -> None:
        path = ("02_REGISTRY/research/sources/"
                "d0_proof_architecture_formalization_2026-10-24/reports/new.json")
        self.write(path, b"{}\n")
        result = self.status()
        self.assertEqual(result["search_corpus_status"], "unverified")
        self.assertEqual(result["overall_status"], "unverified")

    def test_unrelated_nested_ignore_is_not_a_search_input(self) -> None:
        self.write("unrelated/.gitignore", b"*.md\n")
        self.assertEqual(self.status()["search_corpus_status"], "unverified")
        self.write("02_REGISTRY/.gitignore", b"*.md\n")
        self.assertEqual(self.status()["search_corpus_status"], "possibly_changed")

    def test_mode_only_change_does_not_prove_search_content_change(self) -> None:
        path = "02_REGISTRY/research/candidate.md"
        self.write(path, b"same content\n")
        self.git("add", "--", path)
        self.git("-c", "user.name=Receipt Test", "-c", "user.email=test@example.invalid",
                 "commit", "-q", "-m", "candidate")
        head = self.git("rev-parse", "HEAD").strip()
        report = {**self.report, "snapshot_commit": head,
                  "replay": {**self.report["replay"], "source_commit": head}}
        self.git("update-index", "--chmod=+x", "--", path)
        result = self.status(report)
        self.assertEqual(result["historical_selected_bindings_status"], "verified")
        self.assertEqual(result["search_corpus_status"], "unverified")
        self.assertFalse(result["corpus_candidates_truncated"])
        self.assertEqual(result["overall_status"], "unverified")

    def test_missing_historical_commit_is_unverified(self) -> None:
        report = dict(self.report)
        report["snapshot_commit"] = "f" * 40
        report["replay"] = {**self.report["replay"], "source_commit": "f" * 40}
        result = self.status(report)
        self.assertEqual(result["historical_selected_bindings_status"], "unverified")
        self.assertNotEqual(result["overall_status"], "current")

    def test_tree_object_cannot_be_used_as_a_commit_snapshot(self) -> None:
        tree = self.git("rev-parse", "HEAD^{tree}").strip()
        report = {**self.report, "snapshot_commit": tree,
                  "replay": {**self.report["replay"], "source_commit": tree}}
        result = self.status(report)
        self.assertEqual(result["historical_selected_bindings_status"], "mismatch")
        self.assertIn("snapshot_commit:not_commit", result["snapshot_mismatches"])
        self.assertNotEqual(result["overall_status"], "current")

    def test_cold_receipt_requires_nested_replay(self) -> None:
        report = {key: value for key, value in self.report.items() if key != "replay"}
        report.update({key: value for key, value in self.report["replay"].items()
                       if key != "source_commit"})
        result = self.status(report)
        self.assertEqual(result["historical_selected_bindings_status"], "unverified")
        self.assertEqual(result["tool_status"], "unverified")
        self.assertIn("replay", result["missing_or_unverified"])

    def test_cold_replay_requires_its_source_commit(self) -> None:
        report = {**self.report, "replay": dict(self.report["replay"])}
        del report["replay"]["source_commit"]
        result = self.status(report)
        self.assertEqual(result["historical_selected_bindings_status"], "unverified")
        self.assertIn("replay.source_commit", result["missing_or_unverified"])
        report["replay"]["source_commit"] = "0" * 40
        result = self.status(report)
        self.assertEqual(result["historical_selected_bindings_status"], "mismatch")
        self.assertIn("replay.source_commit", result["snapshot_mismatches"])

    def test_selected_bindings_do_not_claim_unchecked_history(self) -> None:
        report = {**self.report, "replay": {**self.report["replay"],
            "test_sha256": "0" * 64, "runner_git_blob": "0" * 40,
            "full_output_sha256": "0" * 64}}
        result = self.status(report)
        self.assertEqual(result["historical_selected_bindings_status"], "verified")
        self.assertNotIn("historical_status", result)
        self.assertIn("test_sha256", result["boundary"])
        self.assertIn("Git blob IDs", result["boundary"])
        self.assertIn("full output hash", result["boundary"])
        self.assertIn("not checked", result["boundary"])

    def test_wrong_digest_is_historical_mismatch(self) -> None:
        report = dict(self.report)
        report["authority_source_digests"] = {
            **self.report["authority_source_digests"],
            "02_REGISTRY/formal_support.csv": "0" * 64,
        }
        result = self.status(report)
        self.assertEqual(result["historical_selected_bindings_status"], "mismatch")
        self.assertEqual(result["authority_status"], "unverified")
        self.assertEqual(result["overall_status"], "unverified")

    def test_wrong_tool_digest_is_not_proof_of_drift(self) -> None:
        report = dict(self.report)
        report["replay"] = {**self.report["replay"], "search_engine_sha256": "0" * 64}
        result = self.status(report)
        self.assertEqual(result["historical_selected_bindings_status"], "mismatch")
        self.assertEqual(result["tool_status"], "unverified")
        self.assertEqual(result["overall_status"], "unverified")

    def test_missing_tool_digest_is_not_current(self) -> None:
        report = dict(self.report)
        report["replay"] = dict(self.report["replay"])
        del report["replay"]["search_engine_sha256"]
        result = self.status(report)
        self.assertEqual(result["tool_status"], "unverified")
        self.assertNotEqual(result["overall_status"], "current")

    def test_missing_authority_digest_is_not_current(self) -> None:
        report = dict(self.report)
        report["authority_source_digests"] = dict(self.report["authority_source_digests"])
        del report["authority_source_digests"]["02_REGISTRY/claims.csv"]
        result = self.status(report)
        self.assertEqual(result["authority_status"], "unverified")
        self.assertNotEqual(result["overall_status"], "current")

    def test_unexpected_authority_is_not_silently_verified(self) -> None:
        report = dict(self.report)
        report["authority_source_digests"] = {
            **self.report["authority_source_digests"], "02_REGISTRY/extra.csv": "0" * 64,
        }
        result = self.status(report)
        self.assertEqual(result["historical_selected_bindings_status"], "unverified")
        self.assertEqual(result["authority_status"], "unverified")
        self.assertEqual(result["unexpected_authority_key_count"], 1)
        self.assertNotEqual(result["overall_status"], "current")

    def test_comparison_uses_its_own_runner_and_query_fixture(self) -> None:
        report = {
            "schema": "d0-proof-architecture-search-comparison-v2",
            "snapshot_commit": self.head,
            "worktree_dirty": False,
            "authority_source_digests": self.report["authority_source_digests"],
            "runner_sha256": digest(self.contents[COMPARISON]),
            "query_fixture_sha256": digest(self.contents[RUNNER]),
        }
        result = self.status(report)
        # Legacy comparison records its runner and fixture but not the search
        # engine, so neither historical tool provenance nor freshness is complete.
        self.assertEqual(result["historical_selected_bindings_status"], "unverified")
        self.assertEqual(result["tool_status"], "unverified")
        self.assertEqual(result["search_corpus_status"], "unverified")
        self.write(RUNNER, self.contents[RUNNER] + b"# changed fixture\n")
        changed = self.status(report)
        self.assertEqual(changed["historical_selected_bindings_status"], "unverified")
        self.assertEqual(changed["tool_status"], "changed")
        self.assertEqual(changed["overall_status"], "stale")

    def test_cli_reports_status_and_rejects_path_traversal(self) -> None:
        path = "02_REGISTRY/receipt.json"
        import json
        self.write(path, json.dumps(self.report).encode("utf-8"))
        cmd = [sys.executable, str(proof.ROOT / "tools/proof_architecture.py"),
               "--repo-root", str(self.root), "receipt-status"]
        result = subprocess.run([*cmd, path], capture_output=True, text=True,
                                encoding="utf-8", check=True)
        view = json.loads(result.stdout)
        self.assertEqual(view["historical_selected_bindings_status"], "verified")
        self.assertEqual(view["search_corpus_status"], "possibly_changed")
        self.assertEqual(view["overall_status"], "unverified")
        rejected = subprocess.run([*cmd, "../outside.json"], capture_output=True,
                                  text=True, encoding="utf-8")
        self.assertNotEqual(rejected.returncode, 0)


if __name__ == "__main__":
    unittest.main()
