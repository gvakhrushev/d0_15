"""Bounded hostile controls for the opt-in cold-start v3 format."""
from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from tools import proof_architecture as proof
from tools import proof_architecture_cold_start as legacy
from tools import proof_architecture_cold_start_v3 as paged
from tools import compact_proof_architecture_cold_start as old_compactor
from tools import compact_proof_architecture_cold_start_v3 as compactor


class PagedColdStartTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = pathlib.Path(tmp.name).resolve()
        self.research = self.root / "02_REGISTRY/research"
        self.research.mkdir(parents=True)
        self.git("init", "-q")
        self.git("config", "user.email", "v3@example.invalid")
        self.git("config", "user.name", "Paged Test")
        source = self.research / "owner.md"
        source.write_text("# amberquartz nativekappa\nactual source proof\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-q", "-m", "source")
        commit = self.git("rev-parse", "HEAD")
        blob = self.git("rev-parse", "HEAD:02_REGISTRY/research/owner.md")
        source.unlink()
        self.locator = self.research / "00_locator.md"
        self.locator.write_text(
            f"# amberquartz nativekappa\namberquartz nativekappa: `02_REGISTRY/research/owner.md`; "
            f"commit: {commit}; blob: {blob}.\n", encoding="utf-8")
        for i in range(23):
            (self.research / f"a_{i:02d}.md").write_text(
                "# amberquartz nativekappa\nactual matching text\n", encoding="utf-8")
        target = self.research / "sources" / "z_retained" / "replay.py"
        target.parent.mkdir(parents=True)
        target.write_text("# amberquartz nativekappa\nactual checker\n", encoding="utf-8")
        self.target_path = target.relative_to(self.root).as_posix()
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "corpus")
        self.head = self.git("rev-parse", "HEAD")
        self.fixture = {"id": "bounded-v3", "queries": ["amberquartz nativekappa", "ornatecobalt"],
                        "required_refs": [], "required_sources": [
                            {"path": self.target_path, "scope_query_indexes": [0, 1]}],
                        "scope_review": "Manual scientific scope remains open."}
        self.dataset = {"snapshot_commit": self.head, "worktree_dirty": False, "source_digests": {}}
        self.impact = {"id": "exact-source-vs-unrelated-prose", "status": "pass",
                       "source_hash_changed": True, "unrelated_prose_left_source_hash": True,
                       "declared_application": "native-result-to-obligation"}

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root,
                                       text=True, stderr=subprocess.PIPE).strip()

    def execute(self):
        with patch.object(legacy, "CASES", [self.fixture]), \
             patch.object(proof, "load_dataset", return_value=self.dataset), \
             patch.object(legacy, "_case10_change_impact_regression", return_value=self.impact), \
             patch.object(proof, "full_text_search_many", wraps=proof.full_text_search_many) as scan:
            report = paged.run(self.root)
        self.assertEqual(scan.call_count, 1)
        self.assertEqual(scan.call_args.args[1], self.fixture["queries"])
        self.assertEqual(scan.call_args.kwargs["ranked_pages"], 2)
        return report

    def test_single_batched_run_compacts_without_cross_query_leak(self):
        report = self.execute()
        row = report["cases"][0]
        self.assertTrue(row["query_results"][0]["ranked_pages"][0]["may_have_more"])
        self.assertFalse(row["query_results"][0]["ranked_pages"][1]["may_have_more"])
        self.assertEqual(row["query_results"][1]["ranked_pages"][1]["start"], 0)
        self.assertFalse(row["found_all_required_sources"])
        receipt = row["required_sources"][self.target_path]
        self.assertEqual([x["found"] for x in receipt["scoped_queries"]], [False, False])
        self.assertEqual(receipt["scoped_queries"][0]["status"],
                         "evidence_verified_discovery_unattested")
        self.assertEqual(receipt["scoped_queries"][0]["candidate_stage"], "ranked_page")
        with patch.object(legacy, "CASES", [self.fixture]), \
             patch.object(proof, "load_dataset", return_value=self.dataset):
            summary = compactor.compact(json.dumps(report).encode(), self.root)
        self.assertEqual(summary["schema"], compactor.SUMMARY_SCHEMA)
        self.assertIsNone(summary["search_cases_found_all_sources"])
        self.assertEqual(summary["discovery_validation"], "unattested")
        self.assertFalse(summary["cases"][0]["all_required_sources_found"])
        with patch.object(legacy, "CASES", [self.fixture]), \
             patch.object(proof, "load_dataset", return_value=self.dataset), \
             patch.object(proof, "full_text_search_many", wraps=proof.full_text_search_many) as scan:
            replay_summary = compactor.compact(json.dumps(report).encode(), self.root,
                                               verify_discovery=True)
        self.assertEqual(scan.call_count, 1)
        self.assertEqual(replay_summary["discovery_validation"], "batched_rerun_same_implementation")
        self.assertEqual(replay_summary["search_cases_found_all_sources"], 0)
        self.assertTrue(replay_summary["cases"][0]["required_sources"][self.target_path]
                        ["scoped_queries"][0]["found"])
        tampered = json.loads(json.dumps(report))
        tampered["cases"][0]["query_results"][0]["ranked_pages"][0]["candidates"] = []
        with self.assertRaisesRegex(ValueError, "ranked pages disagree"), \
             patch.object(legacy, "CASES", [self.fixture]), \
             patch.object(proof, "load_dataset", return_value=self.dataset):
            compactor.compact(json.dumps(tampered).encode(), self.root, verify_discovery=True)
        with self.assertRaises(ValueError), patch.object(legacy, "CASES", [self.fixture]):
            old_compactor._compact_cases(report, [self.fixture])

    def test_first_page_preserves_legacy_window_on_stable_corpus(self):
        q = self.fixture["queries"]
        first = proof.full_text_search_many(self.root, q, limit=18)
        extended = proof.full_text_search_many(self.root, q, limit=18, ranked_pages=2)
        clean = [{k: v for k, v in hit.items()
                  if k not in {"rank_score", "rank_sort_key", "pin_discovery"}}
                 for hit in extended[0][:18]]
        self.assertEqual(first[0], clean)

    def test_large_unread_evidence_is_not_promoted_in_any_mode(self):
        target = self.research / "large_amberquartz.md"
        target.write_text("# amberquartz nativekappa\n" + "x" * 4_000_010,
                          encoding="utf-8")
        old = proof.full_text_search_many(self.root, ["amberquartz nativekappa"], limit=18)[0]
        new = proof.full_text_search_many(self.root, ["amberquartz nativekappa"], limit=18,
                                           ranked_pages=2)[0]
        rel = target.relative_to(self.root).as_posix()
        before = next(hit for hit in old if hit["source"] == rel)
        after = next(hit for hit in new if hit["source"] == rel)
        self.assertFalse(before["direct_content"])
        self.assertEqual(before["source_freshness"], "unverified_missing_evidence")
        self.assertFalse(after["direct_content"])
        self.assertEqual(after["source_freshness"], "unverified_missing_evidence")
        self.assertIsNone(after["source_sha256"])
        self.assertEqual(after["evidence_lines"], [])
        self.assertFalse(legacy._required_source_status(
            [("amberquartz nativekappa", old)], {"path": rel})["found"])

    def test_unreadable_ranked_source_is_not_promoted_in_any_mode(self):
        target = self.research / "a_00.md"
        original_read = pathlib.Path.read_bytes
        for extended in (False, True):
            count = 0
            def fail_evidence_read(path):
                nonlocal count
                if path == target:
                    count += 1
                    if count >= 2:
                        raise OSError("unreadable after discovery")
                return original_read(path)
            with self.subTest(extended=extended), patch.object(pathlib.Path, "read_bytes", fail_evidence_read):
                hits = proof.full_text_search_many(self.root, ["amberquartz nativekappa"],
                    limit=18, **({"ranked_pages": 2} if extended else {}))[0]
            hit = next(item for item in hits if item["source"] == target.relative_to(self.root).as_posix())
            self.assertFalse(hit["direct_content"])
            self.assertEqual(hit["source_freshness"], "unverified_missing_evidence")
            self.assertIsNone(hit["source_sha256"])
            self.assertEqual(hit["evidence_lines"], [])

    def test_legacy_runner_and_compactor_reject_forged_unread_direct_hit(self):
        path = "02_REGISTRY/research/forged.md"
        query = "amberquartz"
        hit = {"source": path, "direct_content": True, "source_sha256": None,
               "evidence_lines": [], "source_origin": "workspace", "source_refs": [],
               "matched_terms": 1, "matched_term_names": [query], "query_terms": 1,
               "source_commit": None, "source_blob": None, "pin_status": None}
        self.assertFalse(legacy._required_source_status([(query, [hit])], {"path": path})["found"])
        fixture = {"id": "forged", "queries": [query], "required_refs": [path],
                   "required_sources": [], "scope_review": "manual"}
        fake = legacy._required_source_status([(query, [{**hit, "source_sha256": "a" * 64,
                    "evidence_lines": [{"kind": "direct_content", "line": 1, "text": query,
                                        "matched_terms": [query]}]}])], {"path": path})
        self.assertTrue(fake["found"])
        case = {"id": "forged", "queries": [query], "scope_review": "manual",
                "query_results": [{"query": query, "top_candidates": [{**hit, "path": path}]}],
                "required_sources": {path: fake}, "found_all_required_sources": True}
        with self.assertRaisesRegex(ValueError, "no matching direct hit"):
            old_compactor._summarize_case(case, fixture, 18)

    def test_v3_search_implementation_is_not_its_own_source(self):
        tools_dir = self.root / "tools"
        tools_dir.mkdir()
        for name in ("proof_architecture_cold_start_v3.py",
                     "compact_proof_architecture_cold_start_v3.py"):
            (tools_dir / name).write_text("amberquartz nativekappa\n", encoding="utf-8")
        hits = proof.full_text_search_many(self.root, ["amberquartz nativekappa"], limit=18,
                                           ranked_pages=2)[0]
        self.assertTrue(hits)
        self.assertFalse(any(hit["source"].startswith("tools/") for hit in hits))

    def test_changed_locator_and_forged_evidence_fail_closed(self):
        report = self.execute()
        result = report["cases"][0]["query_results"][0]
        self.assertTrue(result["source_pages"])
        forged = copy.deepcopy(result)
        candidate = next(hit for page in forged["ranked_pages"] for hit in page["candidates"]
                         if hit.get("direct_content") is True)
        candidate["evidence_lines"][0]["heading"] = "# forged section 999"
        with self.assertRaises(ValueError):
            paged.verified_query(self.root, result["query"], forged)
        forged = copy.deepcopy(result)
        candidate = next(hit for page in forged["ranked_pages"] for hit in page["candidates"]
                         if hit.get("direct_content") is True)
        candidate["source_sha256"] = None
        candidate["evidence_lines"] = []
        with self.assertRaises(ValueError):
            paged.verified_query(self.root, result["query"], forged)
        forged = copy.deepcopy(result)
        page = next(page for page in forged["source_pages"] if page["reference_statuses"])
        page["reference_statuses"][0]["blob"] = "f" * 40
        with self.assertRaises(ValueError):
            paged.verified_query(self.root, result["query"], forged)
        forged = copy.deepcopy(result)
        ranked = next(hit for page in forged["ranked_pages"] for hit in page["candidates"]
                      if hit.get("direct_content") is True)
        ranked["rank_score"] += 0.001
        with self.assertRaises(ValueError):
            paged.verified_query(self.root, result["query"], forged)
        forged = copy.deepcopy(result)
        forged["ranked_pages"][1]["start"] += 1
        with self.assertRaises(ValueError):
            paged.verified_query(self.root, result["query"], forged)
        forged = copy.deepcopy(result)
        ranked = next(hit for page in forged["ranked_pages"] for hit in page["candidates"]
                      if hit.get("source_origin") == "workspace")
        ranked["source"] = "02_REGISTRY/research/../research/00_locator.md"
        ranked["key"] = ranked["rank_sort_key"] = ranked["source"]
        with self.assertRaises(ValueError):
            paged.verified_query(self.root, result["query"], forged)
        self.locator.write_text("# changed after ranking\n", encoding="utf-8")
        with self.assertRaises((ValueError, OSError)):
            paged.verified_query(self.root, result["query"], result)

    def test_ranked_pin_requires_observed_bounded_locator_reference(self):
        report = self.execute()
        result = report["cases"][0]["query_results"][0]
        source = next(hit for page in result["ranked_pages"] for hit in page["candidates"]
                      if hit.get("source_origin") == "pinned_snapshot" and hit.get("direct_content"))
        for mutation in ("missing", "wrong_digest", "wrong_reference_rank"):
            forged_hit = copy.deepcopy(source)
            if mutation == "missing":
                forged_hit.pop("pin_discovery")
            elif mutation == "wrong_digest":
                forged_hit["pin_discovery"]["locator_sha256"] = "f" * 64
            else:
                forged_hit["pin_discovery"]["reference_rank"] = 8
            forged = {"query": result["query"], "ranked_pages": paged._ranked_pages([forged_hit]),
                      "source_pages": []}
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                paged.verified_query(self.root, result["query"], forged)

    def test_locator_outside_pin_window_is_unattested_and_replay_rejects_forged_rank(self):
        initial = self.execute()
        old_result = initial["cases"][0]["query_results"][0]
        pinned = copy.deepcopy(next(hit for page in old_result["ranked_pages"]
                                    for hit in page["candidates"]
                                    if hit.get("source_origin") == "pinned_snapshot"
                                    and hit.get("direct_content")))
        locator = self.locator.rename(self.research / "z_locator.md")
        pinned["pin_discovery"]["locator_source"] = locator.relative_to(self.root).as_posix()
        pinned["pin_discovery"]["pin_window_rank"] = 1
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "move locator outside pin window")
        self.head = self.git("rev-parse", "HEAD")
        self.dataset["snapshot_commit"] = self.head
        self.fixture["queries"] = [self.fixture["queries"][0]]
        self.fixture["required_sources"] = [{"path": pinned["source"],
                                             "commit": pinned["source_commit"],
                                             "blob": pinned["source_blob"]}]
        actual = proof.full_text_search_many(self.root, self.fixture["queries"], limit=18,
                                             ranked_pages=2)[0]
        locator_rank = next(i for i, item in enumerate(actual, 1)
                            if item["source"] == locator.relative_to(self.root).as_posix())
        self.assertGreater(locator_rank, 18)
        self.assertFalse(any(item.get("source_origin") == "pinned_snapshot" for item in actual))
        report = self.execute()
        result = {"query": self.fixture["queries"][0],
                  "ranked_pages": paged._ranked_pages([pinned]), "source_pages": []}
        hits = paged.verified_query(self.root, result["query"], result)
        required = paged._requirements(self.fixture, [(result["query"], hits)])
        self.assertEqual(required[pinned["source"]]["status"],
                         "evidence_verified_discovery_unattested")
        self.assertFalse(required[pinned["source"]]["found"])
        report["cases"][0].update(query_results=[result], required_sources=required,
                                  found_all_required_sources=False)
        encoded = json.dumps(report).encode()
        with patch.object(legacy, "CASES", [self.fixture]), \
             patch.object(proof, "load_dataset", return_value=self.dataset):
            summary = compactor.compact(encoded, self.root)
            self.assertIsNone(summary["search_cases_found_all_sources"])
            self.assertFalse(summary["cases"][0]["required_sources"][pinned["source"]]["found"])
            with self.assertRaisesRegex(ValueError, "ranked pages disagree"):
                compactor.compact(encoded, self.root, verify_discovery=True)

    def test_ranked_non_direct_scores_and_duplicate_keys_cannot_be_forged(self):
        report = self.execute()
        result = report["cases"][0]["query_results"][0]
        source = next(hit for page in result["ranked_pages"] for hit in page["candidates"]
                      if hit.get("source_origin") == "workspace" and hit.get("direct_content"))
        forged_hit = {**source, "source_origin": "filename_only", "direct_content": False,
                      "rank_score": 999.0}
        forged = {"query": result["query"], "ranked_pages": paged._ranked_pages([forged_hit]),
                  "source_pages": []}
        with self.assertRaises(ValueError):
            paged.verified_query(self.root, result["query"], forged)
        duplicate = {"query": result["query"],
                     "ranked_pages": paged._ranked_pages([copy.deepcopy(source), copy.deepcopy(source)]),
                     "source_pages": []}
        with self.assertRaisesRegex(ValueError, "duplicate"):
            paged.verified_query(self.root, result["query"], duplicate)

    def test_nonmatching_and_wrong_blob_ranked_pins_remain_unresolved(self):
        paths = [self.research / "irrelevant.md", self.research / "unrelated.md"]
        for path in paths:
            path.write_text("unrelated prose only\n", encoding="utf-8")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "unrelated pinned sources")
        commit = self.git("rev-parse", "HEAD")
        refs = [{"path": path.relative_to(self.root).as_posix(), "commit": commit,
                 "blob": self.git("rev-parse", f"HEAD:{path.relative_to(self.root).as_posix()}")}
                for path in paths]
        refs[1]["blob"] = "f" * 40
        for path in paths:
            path.unlink()
        with self.locator.open("a", encoding="utf-8") as out:
            for ref in refs:
                out.write(f"amberquartz nativekappa: `{ref['path']}`; commit: {ref['commit']}; "
                          f"blob: {ref['blob']}.\n")
        query = "amberquartz nativekappa"
        hits = proof.full_text_search_many(self.root, [query], limit=18, ranked_pages=2)[0]
        result = {"query": query, "ranked_pages": paged._ranked_pages(hits),
                  "source_pages": paged.source_pages(self.root, query, hits)}
        verified = paged.verified_query(self.root, query, result)
        rows = [row for row in verified if row.get("candidate_stage") != "source_page"]
        no_match = next(row for row in rows if row["source"] == refs[0]["path"])
        wrong = next(row for row in rows if row["source"] == refs[1]["path"])
        self.assertEqual(no_match["pin_status"], "verified_no_content_match")
        self.assertEqual(wrong["pin_status"], "pin_mismatch")
        self.assertFalse(no_match["direct_content"])
        self.assertFalse(wrong["direct_content"])

    def test_compactor_rejects_tampered_budgets_receipts_and_corpus(self):
        report = self.execute()
        for label in ("budget", "receipt", "corpus"):
            with self.subTest(label=label):
                forged = copy.deepcopy(report)
                if label == "budget":
                    forged["source_page_budget"]["pages_per_locator"] += 1
                elif label == "receipt":
                    forged["cases"][0]["required_sources"][self.target_path]["found"] = True
                else:
                    forged["corpus_snapshot"]["sha256"] = "0" * 64
                with patch.object(legacy, "CASES", [self.fixture]), \
                     patch.object(proof, "load_dataset", return_value=self.dataset), \
                     self.assertRaises(ValueError):
                    compactor.compact(json.dumps(forged).encode(), self.root)

    def test_runner_fails_if_corpus_changes_during_one_run(self):
        snap = {"sha256": "a" * 64, "file_count": 1, "scope": "fixture"}
        changed = {**snap, "sha256": "b" * 64}
        with patch.object(legacy, "CASES", [self.fixture]), \
             patch.object(proof, "load_dataset", return_value=self.dataset), \
             patch.object(legacy, "_case10_change_impact_regression", return_value=self.impact), \
             patch.object(paged, "corpus_snapshot", side_effect=[snap, changed]), \
             self.assertRaisesRegex(ValueError, "corpus changed"):
            paged.run(self.root)

    def test_source_page_budget_reaches_verified_pins_after_64(self):
        paths = []
        for i in range(72):
            path = self.research / "sources" / f"owner_{i:02d}.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"Amberquartz actual source {i}.\n", encoding="utf-8")
            paths.append(path)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "72 sources")
        commit = self.git("rev-parse", "HEAD")
        refs = [{"path": path.relative_to(self.root).as_posix(), "commit": commit,
                 "blob": self.git("rev-parse", f"HEAD:{path.relative_to(self.root).as_posix()}")}
                for path in paths]
        refs[-2]["blob"] = "f" * 40
        locator = self.research / "many_pages.md"
        locator.write_text("# Amberquartz\n" + "".join(
            f"amberquartz: `{ref['path']}`; commit: {ref['commit']}; blob: {ref['blob']}.\n"
            for ref in refs), encoding="utf-8")
        hit = {"source": locator.relative_to(self.root).as_posix(),
               "source_sha256": hashlib.sha256(locator.read_bytes()).hexdigest(),
               "source_origin": "workspace", "direct_content": True, "source_refs": [refs[0]]}
        pages = paged.source_pages(self.root, "amberquartz", [hit])
        self.assertEqual([page["page_number"] for page in pages], list(range(1, 11)))
        self.assertTrue(pages[-1]["page_exhausted"])
        self.assertTrue(all(page["locator_rank"] == 1 for page in pages))
        statuses = {row["path"]: row for page in pages for row in page["reference_statuses"]}
        self.assertEqual(statuses[refs[-2]["path"]]["pin_status"], "pin_mismatch")
        self.assertEqual(statuses[refs[-1]["path"]]["pin_status"], "pinned_snapshot")
        self.assertTrue(any(row["source"] == refs[-1]["path"]
                            for page in pages for row in page["candidates"]))
        self.assertLessEqual(len(pages), paged.SOURCE_PAGES)
        rel = locator.relative_to(self.root).as_posix()
        text = locator.read_text(encoding="utf-8")
        terms = proof._query_terms("amberquartz")
        score, ranked = proof._candidate_record(rel, text, terms, origin="workspace",
                                                 content_sha256=hit["source_sha256"])
        ranked.update(rank_score=score, rank_sort_key=ranked["key"], source_refs=[refs[0]])
        result = {"query": "amberquartz", "ranked_pages": paged._ranked_pages([ranked]),
                  "source_pages": pages}
        verified = paged.verified_query(self.root, "amberquartz", result)
        self.assertTrue(any(row.get("source") == refs[-1]["path"] and
                            row.get("candidate_page_number") == 9 for row in verified))


if __name__ == "__main__":
    unittest.main()
