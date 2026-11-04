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
# Keep receipt-status controls in the existing fast compaction CI gate.
from tools.test_receipt_freshness import ReceiptFreshnessTests
from tools.test_c0_reconciliation import ReconciliationFixtureTests
from tools.test_c0_book_byte_partition import BytePartitionTests, GitEvidenceTests
from tools.test_c0_candidate_ranges import CandidateRangeTests
from tools.test_proof_search_streaming import StreamingTextTests
from tools import test_proof_architecture as proof_tests


class DirectContentThresholdTests(unittest.TestCase):
    test_direct_content_requires_content_alone_to_meet_threshold = (
        proof_tests.ProofArchitectureTests.test_direct_content_requires_content_alone_to_meet_threshold
    )


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


def example_paged_case():
    fixture, case = example_case()
    result = case["query_results"][0]
    owner = result["top_candidates"][1]
    native = {**owner, "source": owner["path"], "kind": "text-candidate",
              "key": owner["path"] + "@" + owner["source_commit"],
              "label": "example direct evidence", "pin_status": "verified",
              "evidence_lines": [{"line": 5, "text": "example direct evidence",
                                  "matched_terms": ["example"], "kind": "direct_content"}]}
    del native["path"]
    ref = {"path": owner["path"], "commit": owner["source_commit"],
           "blob": owner["source_blob"], "pin_status": "pinned_snapshot",
           "content_status": "direct_content_match"}
    locator = {**owner, "path": "02_REGISTRY/research/locator.md",
               "source_origin": "workspace", "source_commit": None, "source_blob": None,
               "pin_status": None, "source_refs": [ref]}
    result["top_candidates"] = [locator]
    result["source_pages"] = [{
        "query": result["query"], "locator_source": locator["path"],
        "locator_sha256": locator["source_sha256"], "locator_rank": 1,
        "page_number": 1, "page_size": 8, "total_references": 1,
        "remaining_references": 0, "reference_scan_limit": 64,
        "reference_set_may_be_truncated": False,
        "candidates": [native], "reference_statuses": [ref],
    }]
    hits = compact._query_candidates(result)
    receipt = compact.cold_start._required_source_status(
        [(result["query"], hits)], fixture["required_sources"][0])
    case["required_sources"] = {owner["path"]: receipt}
    return fixture, case


class ColdStartCompactorTests(unittest.TestCase):
    def test_source_page_receipt_has_its_own_stage_rank_and_locator(self):
        fixture, case = example_paged_case()
        summary = compact._summarize_case(case, fixture, 18)
        self.assertTrue(summary["all_required_sources_found"])
        self.assertEqual(summary["source_page_count"], 1)
        retrieval = compact._exact_retrieval(case, fixture, "example.md", 0)
        self.assertEqual(retrieval["candidate_rank"], 1)
        self.assertEqual(retrieval["candidate_stage"], "source_page")
        self.assertEqual(retrieval["candidate_locator_source"],
                         "02_REGISTRY/research/locator.md")
        self.assertEqual(retrieval["candidate_page_number"], 1)
        self.assertEqual(len(case["query_results"][0]["top_candidates"]), 1)

    def test_source_page_success_cannot_be_presented_as_top_window_success(self):
        fixture, case = example_paged_case()
        for field, value in (("candidate_stage", "top_candidates"),
                             ("candidate_locator_source", "different.md"),
                             ("candidate_page_number", 2), ("candidate_rank", 2)):
            with self.subTest(field=field):
                forged = copy.deepcopy(case)
                receipt = next(iter(forged["required_sources"].values()))
                receipt["scoped_queries"][0][field] = value
                with self.assertRaisesRegex(ValueError, "scoped success has no matching direct hit"):
                    compact._summarize_case(forged, fixture, 18)

    def test_source_page_requires_actual_candidate_not_content_status(self):
        fixture, case = example_paged_case()
        case["query_results"][0]["source_pages"][0]["candidates"] = []
        with self.assertRaisesRegex(ValueError, "content status has no returned candidate"):
            compact._summarize_case(case, fixture, 18)

    def test_source_page_rejects_incomplete_filename_only_or_wrong_pin_records(self):
        fixture, case = example_paged_case()
        mutations = [
            ("source_sha256", None), ("source_blob", "f" * 40),
            ("source_commit", "f" * 40), ("direct_content", False),
            ("source_origin", "filename_only"), ("evidence_lines", []),
            ("evidence_lines", [{"line": None, "text": "Filename: example",
                                 "kind": "filename_only", "matched_terms": ["example"]}]),
        ]
        for field, value in mutations:
            with self.subTest(field=field, value=value):
                forged = copy.deepcopy(case)
                forged["query_results"][0]["source_pages"][0]["candidates"][0][field] = value
                with self.assertRaisesRegex(ValueError, "source-page candidate"):
                    compact._summarize_case(forged, fixture, 18)
        del case["query_results"][0]["source_pages"][0]["candidates"][0]["kind"]
        with self.assertRaisesRegex(ValueError, "incomplete source-page candidate"):
            compact._summarize_case(case, fixture, 18)

    def test_source_page_must_come_from_an_observed_unchanged_workspace_locator(self):
        fixture, case = example_paged_case()
        for field, value in (("locator_rank", 2), ("locator_source", "unseen.md"),
                             ("locator_sha256", "e" * 64), ("query", "other query")):
            with self.subTest(field=field):
                forged = copy.deepcopy(case)
                forged["query_results"][0]["source_pages"][0][field] = value
                with self.assertRaises(ValueError):
                    compact._summarize_case(forged, fixture, 18)
        case["query_results"][0]["top_candidates"][0]["source_refs"] = []
        with self.assertRaisesRegex(ValueError, "reference was not observed"):
            compact._summarize_case(case, fixture, 18)

    def test_source_page_accepts_commit_only_locator_after_exact_blob_resolution(self):
        fixture, case = example_paged_case()
        # The exact blob is resolved from the pinned commit/path by the producer.
        case["query_results"][0]["top_candidates"][0]["source_refs"] = [
            {**case["query_results"][0]["top_candidates"][0]["source_refs"][0], "blob": None}]
        compact._summarize_case(case, fixture, 18)

    def test_source_page_keeps_truncation_flag_after_unpinned_references_filtered(self):
        fixture, case = example_paged_case()
        case["query_results"][0]["source_pages"][0]["reference_set_may_be_truncated"] = True
        compact._summarize_case(case, fixture, 18)

    def test_source_page_budget_and_duplicates_are_rejected(self):
        fixture, case = example_paged_case()
        for field, value in (("page_number", 2), ("page_size", 9),
                             ("remaining_references", 1), ("total_references", 65)):
            with self.subTest(field=field):
                forged = copy.deepcopy(case)
                forged["query_results"][0]["source_pages"][0][field] = value
                with self.assertRaises(ValueError):
                    compact._summarize_case(forged, fixture, 18)
        pages = case["query_results"][0]["source_pages"]
        pages.append(copy.deepcopy(pages[0]))
        with self.assertRaisesRegex(ValueError, "bounds or query"):
            compact._summarize_case(case, fixture, 18)

    def test_source_page_for_one_query_does_not_cover_another_scoped_query(self):
        fixture, case = example_paged_case()
        required = fixture["required_sources"][0]
        required["scope_query_indexes"] = [0, 1]
        fixture["queries"].append("unmatched query")
        case["query_results"].append({"query": "unmatched query", "top_candidates": [],
                                      "source_pages": []})
        pairs = [(row["query"], compact._query_candidates(row)) for row in case["query_results"]]
        receipt = compact.cold_start._required_source_status(pairs, required)
        case["required_sources"] = {required["path"]: receipt}
        case["found_all_required_sources"] = False
        self.assertEqual(receipt["status"], "missing_scoped_query")
        self.assertEqual([row["found"] for row in receipt["scoped_queries"]], [True, False])
        self.assertEqual(receipt["scoped_queries"][0]["candidate_stage"], "source_page")
        compact._summarize_case(case, fixture, 18)

    def test_runner_expands_actual_returned_hits_without_expected_paths(self):
        fixture, case = example_paged_case()
        query_result = case["query_results"][0]
        native_hits = [{**row, "source": row["path"]} for row in query_result["top_candidates"]]
        pages = query_result["source_pages"]
        for index in range(2, 8):
            ref = {"path": f"source/missing{index}.md", "commit": "a" * 40,
                   "blob": "b" * 40, "pin_status": "missing_commit", "content_status": "not_loaded"}
            native_hits[0]["source_refs"].append(ref)
        pages[0]["total_references"] = 7
        # The fixture starts with shared lists; clone to show all seven refs
        # survive runner serialization, including those beyond the old limit5.
        pages[0]["reference_statuses"] = copy.deepcopy(native_hits[0]["source_refs"])
        native_hits.extend({**native_hits[0], "source": f"unrelated{index}.md",
                            "direct_content": False, "source_refs": []}
                           for index in range(17))
        dataset = {"snapshot_commit": "a" * 40, "worktree_dirty": False, "source_digests": {}}
        cold = compact.cold_start
        with patch.object(cold, "CASES", [fixture]), \
                patch.object(cold.proof, "full_text_search_many", return_value=[native_hits]), \
                patch.object(cold.proof, "expand_source_pages", return_value=pages) as expand, \
                patch.object(cold.proof, "load_dataset", return_value=dataset), \
                patch.object(cold, "_case10_change_impact_regression", return_value={}):
            replay = cold.run(pathlib.Path("/unused"))
        expand.assert_called_once_with(pathlib.Path("/unused"), fixture["queries"][0],
                                       native_hits, page_size=8, pages_per_locator=1)
        returned = replay["cases"][0]
        self.assertTrue(returned["found_all_required_sources"])
        self.assertEqual(returned["query_results"][0]["source_pages"], pages)
        self.assertEqual(len(returned["query_results"][0]["top_candidates"]), 18)
        self.assertEqual(len(returned["query_results"][0]["top_candidates"][0]["source_refs"]), 7)
        compact._summarize_case(returned, fixture, 18)

    def test_exact_pinned_content_outside_window_is_not_reported_as_lexical_miss(self):
        path, commit, blob = "02_REGISTRY/research/owner.md", "a" * 40, "b" * 40
        locator = {"source": "owner-index.md", "direct_content": True,
                   "source_refs": [{"path": path, "commit": commit, "blob": blob,
                                    "pin_status": "pinned_snapshot",
                                    "content_status": "direct_content_match"}]}
        required = {"path": path, "commit": commit, "blob": blob,
                    "scope_query_indexes": [0]}

        receipt = compact.cold_start._required_source_status([("owner query", [locator])],
                                                              required)

        self.assertFalse(receipt["found"])
        self.assertEqual(receipt["status"], "verified_direct_content_outside_search_window")
        self.assertIsNone(receipt["candidate_rank"])

        locator["source_refs"][0]["content_status"] = "no_direct_content_match"
        no_match = compact.cold_start._required_source_status([("owner query", [locator])],
                                                               required)
        self.assertFalse(no_match["found"])
        self.assertEqual(no_match["status"], "pinned_source_loaded_no_content_match")

    def test_content_receipt_for_wrong_exact_pin_is_not_an_outside_window_match(self):
        path, commit, blob = "02_REGISTRY/research/owner.md", "a" * 40, "b" * 40
        required = {"path": path, "commit": commit, "blob": blob,
                    "scope_query_indexes": [0]}
        for field in ("commit", "blob"):
            with self.subTest(wrong_pin=field):
                reference = {"path": path, "commit": commit, "blob": blob,
                             "pin_status": "pinned_snapshot",
                             "content_status": "direct_content_match", field: "c" * 40}
                locator = {"source": "owner-index.md", "direct_content": True,
                           "source_refs": [reference]}
                receipt = compact.cold_start._required_source_status(
                    [("owner query", [locator])], required
                )
                self.assertFalse(receipt["found"])
                self.assertEqual(receipt["status"], "external_reference_only")
                self.assertEqual(receipt["scoped_queries"][0]["status"],
                                 "external_reference_only")

    def test_returned_owner_in_one_query_does_not_cover_another_query(self):
        path, commit, blob = "02_REGISTRY/research/owner.md", "a" * 40, "b" * 40
        required = {"path": path, "commit": commit, "blob": blob,
                    "scope_query_indexes": [0, 1]}
        owner = {"source": path, "direct_content": True,
                 "source_commit": commit, "source_blob": blob,
                 "source_origin": "pinned_snapshot"}
        locator = {"source": "owner-index.md", "direct_content": True,
                   "source_refs": [{"path": path, "commit": commit, "blob": blob,
                                    "pin_status": "pinned_snapshot",
                                    "content_status": "no_direct_content_match"}]}
        receipt = compact.cold_start._required_source_status(
            [("matching query", [owner]), ("unmatched query", [locator])], required
        )
        self.assertFalse(receipt["found"])
        self.assertEqual(receipt["status"], "missing_scoped_query")
        self.assertEqual([query["found"] for query in receipt["scoped_queries"]], [True, False])
        self.assertEqual([query["status"] for query in receipt["scoped_queries"]],
                         ["found_direct_content", "pinned_source_loaded_no_content_match"])

    def test_one_pinned_source_retains_distinct_scoped_queries(self):
        fixture, case = example_case()
        fixture["queries"].append("second query")
        fixture["required_sources"][0]["scope_query_indexes"].append(1)
        case["query_results"].append({"query": "second query", "top_candidates":
                                      copy.deepcopy(case["query_results"][0]["top_candidates"])})
        receipt = next(iter(case["required_sources"].values()))
        second = copy.deepcopy(receipt["scoped_queries"][0])
        second.update(query_index=1, query="second query")
        receipt["scoped_queries"].append(second)
        compact._summarize_case(case, fixture, 18)
        for index in (0, 1):
            retrieval = compact._exact_retrieval(case, fixture, "example.md", index)
            self.assertTrue(retrieval["found"])
            self.assertEqual(retrieval["query_index"], index)
            self.assertEqual(retrieval["candidate_rank"], 2)

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
