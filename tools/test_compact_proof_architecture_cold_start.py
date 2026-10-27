"""Focused controls for cold-start receipt compaction; no search is run."""
from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch

from tools import compact_proof_architecture_cold_start as compact


def example_case():
    path = "02_REGISTRY/research/example.md"
    commit, blob = "a" * 40, "b" * 40
    fixture = {
        "id": "example", "queries": ["example query"],
        "required_refs": [path],
        "required_sources": [{"path": path, "commit": commit, "blob": blob,
                              "scope_query_indexes": [0]}],
        "scope_review": "Manual scientific review remains necessary.",
    }
    scoped = {"query_index": 0, "query": "example query", "found": True,
              "status": "found_direct_content", "required_sections": [],
              "sections_found": [], "missing_sections": [], "candidate_rank": 2,
              "evidence_lines": [{"line": 5, "text": "direct evidence"}]}
    receipt = {"path": path, "status": "found_direct_content", "found": True,
               "source_origin": "pinned_snapshot", "expected_commit": commit,
               "expected_blob": blob, "required_sections": [], "sections_found": [],
               "missing_sections": [], "scoped_queries": [scoped],
               "candidate_rank": 2, "query": "example query",
               "evidence_lines": [{"line": 5, "text": "direct evidence"}],
               "citation_only_refs": []}
    hit = {"path": path, "direct_content": True, "source_origin": "pinned_snapshot",
           "source_commit": commit, "source_blob": blob, "matched_terms": 1,
           "matched_term_names": ["example"], "query_terms": 1, "source_sha256": "c" * 64,
           "pin_status": "pinned_snapshot", "evidence_lines": [], "source_refs": []}
    unrelated = {**hit, "path": "unrelated", "direct_content": False}
    case = {"id": "example", "queries": fixture["queries"],
            "required_sources": {path: receipt}, "found_all_required_sources": True,
            "query_results": [{"query": "example query",
                               "top_candidates": [unrelated, hit]}],
            "scope_review": fixture["scope_review"]}
    return fixture, case


def example_complete_replay(head):
    queries = [f"query {index}" for index in range(20)]
    entries = [
        ("A4D_EXACT_NONVACUUM_GR_MIDPOINT_C2_RECOVERY_2026_10_20.md", 14, ["7.2"]),
        ("nonvacuum_compact_pointwise_margin_2026-10-27.json", 17, []),
        ("NonvacuumBrinkmannStencil.lean", 18, []),
        ("nonvacuum_cubic_profile_car_margin_2026-10-27.json", 18, []),
        ("NonvacuumBrinkmannStencil.lean", 19, []),
        ("nonvacuum_cubic_profile_same_record_euclidean_refinement_2026-10-27.json", 19, []),
    ]
    fixture = {"id": "positive-nonvacuum-recovery", "queries": queries,
               "required_refs": [], "required_sources": [], "scope_review": "manual scope"}
    results = [{"query": query, "top_candidates": []} for query in queries]
    receipts = {}
    for number, (name, index, sections) in enumerate(entries, 1):
        path = "source/" + name
        commit, blob = f"{number:040x}", f"{number + 10:040x}"
        required = {"path": path, "commit": commit, "blob": blob,
                    "scope_query_indexes": [index]}
        if sections:
            required.update(sections=sections, scope_query_sections={str(index): sections})
        fixture["required_sources"].append(required)
        rank = len(results[index]["top_candidates"]) + 1
        hit = {"path": path, "matched_terms": 1, "matched_term_names": ["query"],
               "query_terms": 1, "source_sha256": "c" * 64, "source_origin": "pinned_snapshot",
               "direct_content": True, "source_commit": commit, "source_blob": blob,
               "pin_status": "pinned_snapshot", "evidence_lines": [], "source_refs": []}
        results[index]["top_candidates"].append(hit)
        scoped = {"query_index": index, "query": queries[index], "found": True,
                  "status": "found_direct_content", "required_sections": sections,
                  "sections_found": sections, "missing_sections": [], "candidate_rank": rank,
                  "evidence_lines": []}
        receipt = {"path": path, "status": "found_direct_content", "found": True,
                   "source_origin": "pinned_snapshot", "expected_commit": commit,
                   "expected_blob": blob, "required_sections": sections,
                   "sections_found": sections, "missing_sections": [], "scoped_queries": [scoped],
                   "candidate_rank": rank, "query": queries[index], "evidence_lines": [],
                   "citation_only_refs": []}
        key = path if path not in receipts else f"{path}@{commit}"
        receipts[key] = receipt
    case = {"id": fixture["id"], "queries": queries, "required_sources": receipts,
            "found_all_required_sources": True, "query_results": results,
            "scope_review": fixture["scope_review"]}
    authority = {"02_REGISTRY/claims.csv": "d" * 64}
    full = {"snapshot_commit": head, "worktree_dirty": False,
            "authority_source_digests": authority, "search_limit": 18,
            "search_cases_found_all_sources": 1, "search_cases_total": 1,
            "benchmark_cases_total": 2, "cases": [case],
            "change_impact_regression": {"id": "exact-source-vs-unrelated-prose", "status": "pass",
                                         "source_hash_changed": True,
                                         "unrelated_prose_left_source_hash": True,
                                         "declared_application": "native-result-to-obligation"},
            "semantic_scope_review_is_manual": True}
    return fixture, full, authority


class ColdStartCompactorTests(unittest.TestCase):
    def test_preserves_source_receipt_and_extracts_exact_pinned_hit(self):
        fixture, case = example_case()
        result = compact._summarize_case(case, fixture, 18)
        self.assertEqual(result["required_source_count"], 1)
        self.assertEqual(result["required_sources"], case["required_sources"])
        self.assertTrue(result["all_required_sources_found"])
        retrieval = compact._exact_retrieval(case, fixture, "example.md", 0)
        self.assertTrue(retrieval["found"])
        self.assertEqual(retrieval["candidate_rank"], 2)
        self.assertEqual(retrieval["commit"], "a" * 40)
        self.assertEqual(retrieval["blob"], "b" * 40)

    def test_rejects_missing_queries_and_forged_success_for_wrong_blob(self):
        fixture, case = example_case()
        missing = copy.deepcopy(case)
        missing["query_results"] = []
        with self.assertRaisesRegex(ValueError, "incomplete query results"):
            compact._summarize_case(missing, fixture, 18)
        wrong_pin = copy.deepcopy(case)
        wrong_pin["query_results"][0]["top_candidates"][1]["source_blob"] = "c" * 40
        with self.assertRaisesRegex(ValueError, "no exact pinned hit"):
            compact._exact_retrieval(wrong_pin, fixture, "example.md", 0)

    def test_retains_a_failed_scoped_retrieval_without_promoting_it(self):
        fixture, case = example_case()
        receipt = next(iter(case["required_sources"].values()))
        receipt.update(found=False, status="source_pin_mismatch")
        receipt["scoped_queries"][0].update(found=False, status="source_pin_mismatch")
        case["found_all_required_sources"] = False
        case["query_results"][0]["top_candidates"][1]["source_blob"] = "c" * 40
        result = compact._summarize_case(case, fixture, 18)
        self.assertFalse(result["all_required_sources_found"])
        self.assertEqual(result["missing_paths"], [receipt["path"]])
        retrieval = compact._exact_retrieval(case, fixture, "example.md", 0)
        self.assertFalse(retrieval["found"])
        self.assertEqual(retrieval["status"], "source_pin_mismatch")

    def test_rejects_dirty_or_stale_snapshot_and_stale_authority(self):
        head = "a" * 40
        full = {"snapshot_commit": head, "worktree_dirty": False,
                "authority_source_digests": {"claims": "sha"}}
        compact._validate_snapshot(full, head, False, {"claims": "sha"})
        with self.assertRaisesRegex(ValueError, "must both be clean"):
            compact._validate_snapshot(full, head, True, {"claims": "sha"})
        with self.assertRaisesRegex(ValueError, "current HEAD"):
            compact._validate_snapshot(full, "b" * 40, False, {"claims": "sha"})
        with self.assertRaisesRegex(ValueError, "authority"):
            compact._validate_snapshot(full, head, False, {"claims": "different"})

    def test_compacts_complete_fixture_and_omits_unverified_old_results(self):
        head = "a" * 40
        fixture, full, authority = example_complete_replay(head)
        raw = (json.dumps(full) + "\n").encode()
        dataset = {"snapshot_commit": head, "worktree_dirty": False,
                   "source_digests": authority}
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            for path in (compact.RUNNER_PATH, compact.SEARCH_PATH,
                         compact.TEST_PATH, compact.COMPACTOR_PATH):
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(path, encoding="utf-8")

            def fake_git(_root, *args):
                if args[:2] == ("rev-parse", "HEAD"):
                    return head
                if args[0] == "status":
                    return ""
                if args[0] == "rev-parse":
                    return "b" * 40
                raise AssertionError(args)

            with patch.object(compact.cold_start, "CASES", [fixture]), \
                 patch.object(compact.proof, "load_dataset", return_value=dataset), \
                 patch.object(compact, "_candidate_view", return_value={"path": "candidate-view"}), \
                 patch.object(compact, "_git", side_effect=fake_git):
                summary = compact.compact(raw, root)
        self.assertEqual(summary["required_source_ref_count"], 6)
        self.assertEqual(summary["replay"]["full_output_sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(summary["replay"]["full_output_bytes"], len(raw))
        self.assertEqual(summary["cases"][0]["same_record_euclidean_refinement_retrieval"]
                         ["inventory_candidate_rank"], 2)
        self.assertTrue(summary["semantic_scope_review_is_manual"])
        self.assertNotIn("lean_validation", summary)
        self.assertNotIn("comparison_replay", summary)


if __name__ == "__main__":
    unittest.main()
