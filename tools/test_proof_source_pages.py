"""Bounded source-page retrieval through real historical Git snapshots."""

from __future__ import annotations

import copy
import hashlib
import io
import json
import pathlib
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from tools import proof_architecture as proof
from tools import proof_architecture_cold_start as cold_start


class ProofSourcePagesTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = pathlib.Path(temporary.name)
        self.research = self.root / "02_REGISTRY/research"
        self.research.mkdir(parents=True)
        self.git("init", "-q")
        self.git("config", "user.email", "source-pages@example.invalid")
        self.git("config", "user.name", "Source Page Test")

    def git(self, *args: str) -> str:
        return subprocess.check_output(
            ["git", *args], cwd=self.root, text=True, stderr=subprocess.PIPE
        ).strip()

    def archive(self, sources: dict[str, str]) -> list[dict[str, str]]:
        """Commit sources, then remove working files so only exact pins supply them."""
        for path, content in sources.items():
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        self.git("add", "--", *sources)
        self.git("commit", "-q", "-m", "exact source fixtures")
        commit = self.git("rev-parse", "HEAD")
        refs = []
        for path, content in sources.items():
            refs.append({
                "path": path, "commit": commit,
                "blob": self.git("rev-parse", f"HEAD:{path}"),
                "sha256": hashlib.sha256(content.encode()).hexdigest(),
            })
            (self.root / path).unlink()
        return refs

    def locator(self, query: str, refs: list[dict[str, str]],
                name: str = "index.md") -> str:
        path = self.research / name
        lines = [f"# {query}"]
        for ref in refs:
            lines.append(
                f"{query}: `{ref['path']}`; commit: {ref['commit']}; blob: {ref['blob']}."
            )
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path.relative_to(self.root).as_posix()

    @staticmethod
    def candidates(pages: list[dict]) -> list[dict]:
        return [candidate for page in pages for candidate in page["candidates"]]

    def assert_exact_candidate(self, candidate: dict, reference: dict[str, str]) -> None:
        self.assertEqual(candidate["source"], reference["path"])
        self.assertEqual(candidate["source_commit"], reference["commit"])
        self.assertEqual(candidate["source_blob"], reference["blob"])
        self.assertEqual(candidate["source_sha256"], reference["sha256"])
        self.assertEqual(candidate["source_origin"], "pinned_snapshot")
        self.assertTrue(candidate["direct_content"])
        self.assertTrue(any(row.get("line") is not None
                            and row.get("kind") == "direct_content"
                            for row in candidate["evidence_lines"]))

    def test_crowded_first_window_requires_explicit_source_page(self) -> None:
        query = "cobalt amber zircon nickel indigo sienna ochre quartz"
        refs = self.archive({
            f"02_REGISTRY/research/sources/owner_{index:02d}.md":
                f"# Owner result {index}\nCobalt amber identity on the declared carrier.\n"
            for index in range(7)
        })
        slug = query.replace(" ", "_")
        locator = self.locator(query, refs, f"00_{slug}.md")
        for index in range(17):
            (self.research / f"decoy_{index:02d}_{slug}.md").write_text(
                f"# {query}\nUnrelated ranked discussion, with no owner references.\n",
                encoding="utf-8",
            )

        hits = proof.full_text_search_many(self.root, [query], limit=18)[0]
        self.assertEqual(len(hits), 18)
        self.assertIn(locator, [hit["source"] for hit in hits])
        self.assertTrue({ref["path"] for ref in refs}.isdisjoint(
            hit["source"] for hit in hits))
        for ref in refs:
            self.assertFalse(cold_start._required_source_status([(query, hits)], ref)["found"])

        pages = proof.expand_source_pages(self.root, query, hits)
        self.assertEqual(len(pages), 1)
        page = pages[0]
        self.assertEqual(page["locator_source"], locator)
        self.assertEqual(page["locator_sha256"], hashlib.sha256(
            (self.root / locator).read_bytes()).hexdigest())
        self.assertEqual(page["locator_rank"], 1 + next(
            index for index, hit in enumerate(hits) if hit["source"] == locator))
        self.assertEqual(page["query"], query)
        self.assertEqual(page["page_number"], 1)
        self.assertEqual(page["page_size"], 8)
        self.assertEqual(page["total_references"], 7)
        self.assertEqual(page["remaining_references"], 0)
        returned = self.candidates(pages)
        self.assertEqual({item["source"] for item in returned}, {ref["path"] for ref in refs})
        for ref in refs:
            candidate = next(item for item in returned if item["source"] == ref["path"])
            self.assert_exact_candidate(candidate, ref)
            self.assertTrue(cold_start._required_source_status(
                [(query, hits + returned)], ref)["found"])

    def test_absent_locator_does_not_read_available_pins(self) -> None:
        refs = self.archive({"02_REGISTRY/research/owner.md": "Amberquartz identity.\n"})
        self.locator("amberquartz", refs)
        with patch.object(proof, "_read_pinned_source", side_effect=AssertionError("pin read")):
            self.assertEqual(proof.expand_source_pages(self.root, "amberquartz", []), [])

    def test_changed_locator_hash_fails_before_reading_pins(self) -> None:
        query = "amberquartz"
        refs = self.archive({"02_REGISTRY/research/owner.md": "Amberquartz identity.\n"})
        locator = self.locator(query, refs)
        hits = proof.full_text_search_many(self.root, [query], limit=18)[0]
        with (self.root / locator).open("a", encoding="utf-8") as handle:
            handle.write("Changed after discovery.\n")
        with patch.object(proof, "_read_pinned_source", side_effect=AssertionError("pin read")):
            self.assertEqual(proof.expand_source_pages(self.root, query, hits), [])

    def test_source_references_are_rederived_from_the_observed_locator(self) -> None:
        query = "amberquartz"
        refs = self.archive({
            "02_REGISTRY/research/owner_a.md": "Amberquartz identity A.\n",
            "02_REGISTRY/research/owner_b.md": "Amberquartz identity B.\n",
        })
        locator = self.locator(query, refs[:1])
        hits = proof.full_text_search_many(self.root, [query], limit=18)[0]
        tampered = copy.deepcopy(hits)
        hit = next(row for row in tampered if row["source"] == locator)
        # An extra valid Git object in result metadata is not an observed citation.
        hit["source_refs"] = [dict(refs[1], pin_complete=True)]
        pages = proof.expand_source_pages(self.root, query, tampered)
        self.assertEqual([row["source"] for row in self.candidates(pages)], [refs[0]["path"]])
        self.assert_exact_candidate(self.candidates(pages)[0], refs[0])

    def test_implicit_and_explicit_blob_citations_form_one_exact_reference(self) -> None:
        query = "amberquartz"
        refs = self.archive({"02_REGISTRY/research/owner.md": "Amberquartz identity.\n"})
        ref = refs[0]
        self.locator(query, refs)
        with (self.research / "index.md").open("a", encoding="utf-8") as handle:
            handle.write(f"{query}: `{ref['path']}`; commit: {ref['commit']}.\n")
        hits = proof.full_text_search_many(self.root, [query], limit=18)[0]
        pages = proof.expand_source_pages(self.root, query, hits)
        self.assertEqual(len(pages), 1)
        self.assertEqual(pages[0]["total_references"], 1)
        self.assertEqual(len(pages[0]["reference_statuses"]), 1)
        self.assertEqual(len(pages[0]["candidates"]), 1)
        self.assert_exact_candidate(pages[0]["candidates"][0], ref)
        combined = cold_start._query_hits_with_source_pages(query, hits, pages)
        page_candidates = [hit for hit in combined if hit.get("candidate_stage") == "source_page"]
        self.assertEqual(len(page_candidates), 1)
        self.assertTrue(cold_start._required_source_status([(query, combined)], ref)["found"])

    def test_two_locators_reuse_source_matching_and_keep_both_pages(self) -> None:
        query = "amberquartz"
        refs = self.archive({"02_REGISTRY/research/owner.md": "Amberquartz identity.\n"})
        locators = {self.locator(query, refs, "index_a.md"),
                    self.locator(query, refs, "index_b.md")}
        hits = proof.full_text_search_many(self.root, [query], limit=18)[0]
        original = proof._candidate_record
        source_matches = []

        def track_candidate(*args, **kwargs):
            if kwargs.get("origin") == "pinned_snapshot":
                source_matches.append((args[0], kwargs.get("commit"), kwargs.get("blob")))
            return original(*args, **kwargs)

        with patch.object(proof, "_candidate_record", side_effect=track_candidate):
            pages = proof.expand_source_pages(self.root, query, hits)
        self.assertEqual(source_matches, [(refs[0]["path"], refs[0]["commit"], refs[0]["blob"])])
        self.assertEqual({page["locator_source"] for page in pages}, locators)
        self.assertEqual(len(pages), 2)
        for page in pages:
            self.assertEqual(len(page["candidates"]), 1)
            self.assert_exact_candidate(page["candidates"][0], refs[0])
        combined = cold_start._query_hits_with_source_pages(query, hits, pages)
        self.assertEqual({hit["candidate_locator_source"] for hit in combined
                          if hit.get("candidate_stage") == "source_page"}, locators)

    def test_filename_only_locator_cannot_trigger_expansion(self) -> None:
        query = "amberquartz"
        refs = self.archive({"02_REGISTRY/research/owner.md": "Amberquartz identity.\n"})
        locator = self.locator("unrelated", refs, "amberquartz.md")
        hits = proof.full_text_search_many(self.root, [query], limit=18)[0]
        found = next(hit for hit in hits if hit["source"] == locator)
        self.assertFalse(found["direct_content"])
        with patch.object(proof, "_read_pinned_source", side_effect=AssertionError("pin read")):
            self.assertEqual(proof.expand_source_pages(self.root, query, hits), [])

    def test_filename_only_and_unrelated_source_contents_are_not_returned(self) -> None:
        query = "amberquartz"
        refs = self.archive({
            "02_REGISTRY/research/amberquartz.md": "Entirely unrelated prose.\n",
            "02_REGISTRY/research/irrelevant.md": "Entirely unrelated prose.\n",
        })
        self.locator(query, refs)
        hits = proof.full_text_search_many(self.root, [query], limit=18)[0]
        pages = proof.expand_source_pages(self.root, query, hits)
        self.assertEqual(len(pages), 1)
        self.assertEqual(self.candidates(pages), [])
        statuses = pages[0]["reference_statuses"]
        self.assertEqual({row["path"] for row in statuses}, {ref["path"] for ref in refs})
        self.assertTrue(all(row["content_status"] == "no_direct_content_match"
                            for row in statuses))
        for ref in refs:
            self.assertFalse(cold_start._required_source_status([(query, hits)], ref)["found"])

    def test_wrong_blob_and_nonexistent_commit_are_not_returned(self) -> None:
        query = "amberquartz"
        refs = self.archive({
            "02_REGISTRY/research/owner_a.md": "Amberquartz identity A.\n",
            "02_REGISTRY/research/owner_b.md": "Amberquartz identity B.\n",
        })
        invalid = copy.deepcopy(refs)
        invalid[0]["blob"] = "f" * 40
        invalid[1]["commit"] = "e" * 40
        self.locator(query, invalid)
        hits = proof.full_text_search_many(self.root, [query], limit=18)[0]
        pages = proof.expand_source_pages(self.root, query, hits)
        self.assertEqual(self.candidates(pages), [])
        statuses = {row["path"]: row for page in pages for row in page["reference_statuses"]}
        self.assertEqual(statuses[refs[0]["path"]]["pin_status"], "pin_mismatch")
        self.assertEqual(statuses[refs[1]["path"]]["pin_status"], "external_reference_only")

    def test_finite_pages_respect_per_locator_reference_budget(self) -> None:
        query = "amberquartz"
        refs = self.archive({
            f"02_REGISTRY/research/owner_{index:02d}.md": f"Amberquartz identity {index}.\n"
            for index in range(10)
        })
        self.locator(query, refs)
        hits = proof.full_text_search_many(self.root, [query], limit=18)[0]
        with patch.object(proof, "_read_pinned_source", wraps=proof._read_pinned_source) as read:
            first = proof.expand_source_pages(self.root, query, hits, page_size=8,
                                              pages_per_locator=1)
            self.assertLessEqual(read.call_count, 8)
        self.assertEqual(len(first), 1)
        self.assertEqual(len(self.candidates(first)), 8)
        self.assertEqual(first[0]["total_references"], 10)
        self.assertEqual(first[0]["remaining_references"], 2)
        with patch.object(proof, "_read_pinned_source", wraps=proof._read_pinned_source) as read:
            both = proof.expand_source_pages(self.root, query, hits, page_size=8,
                                             pages_per_locator=2)
            self.assertLessEqual(read.call_count, 16)
        self.assertEqual([page["page_number"] for page in both], [1, 2])
        self.assertEqual([len(page["candidates"]) for page in both], [8, 2])
        self.assertEqual(both[-1]["remaining_references"], 0)
        returned = self.candidates(both)
        self.assertEqual(len({row["source"] for row in returned}), 10)
        self.assertEqual({row["source"] for row in first[0]["candidates"]},
                         {row["source"] for row in both[0]["candidates"]})

    def test_one_successful_scope_does_not_cover_another_query(self) -> None:
        queries = ["amberquartz", "ornatecobalt"]
        refs = self.archive({"02_REGISTRY/research/owner.md": "Amberquartz identity.\n"})
        self.locator(" ".join(queries), refs)
        hits_by_query = proof.full_text_search_many(self.root, queries, limit=18)
        query_pairs = []
        for query, hits in zip(queries, hits_by_query):
            pages = proof.expand_source_pages(self.root, query, hits)
            query_pairs.append((query, hits + self.candidates(pages)))
        required = dict(refs[0], scope_query_indexes=[0, 1])
        status = cold_start._required_source_status(query_pairs, required)
        self.assertFalse(status["found"])
        self.assertEqual(status["status"], "missing_scoped_query")
        self.assertEqual([row["found"] for row in status["scoped_queries"]], [True, False])

    def test_invalid_page_budgets_are_rejected(self) -> None:
        for field in ("page_size", "pages_per_locator"):
            for value in (0, 9):
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    proof.expand_source_pages(self.root, "amberquartz", [], **{field: value})
        with self.assertRaises(ValueError), patch.object(
            proof, "_read_pinned_source", side_effect=AssertionError("pin read")
        ):
            proof.expand_source_pages(self.root, "amberquartz", [{}] * 65)

    def test_cli_renders_all_explicitly_requested_hits_and_source_pages(self) -> None:
        hits = [{"kind": "text-candidate", "key": f"locator-{index}",
                 "source": f"02_REGISTRY/research/locator_{index:02d}.md"}
                for index in range(64)]
        pages = [{"locator_source": hits[index]["source"], "locator_rank": index + 1,
                  "page_number": 1, "candidates": []}
                 for index in range(33)]
        dataset = {"snapshot_commit": "a" * 40, "worktree_dirty": False,
                   "source_digests": {}}
        output = io.StringIO()
        with patch.object(proof, "load_dataset", return_value=dataset), \
             patch.object(proof, "structured_search", return_value=[]), \
             patch.object(proof, "full_text_search", return_value=hits), \
             patch.object(proof, "expand_source_pages", return_value=pages), \
             patch("sys.argv", ["proof_architecture.py", "--repo-root", str(self.root),
                                "search", "amberquartz", "--limit", "64",
                                "--source-pages", "8"]), \
             patch("sys.stdout", output):
            self.assertEqual(proof.main(), 0)
        rendered = json.loads(output.getvalue())
        self.assertEqual(len(rendered["text_candidates"]), 64)
        self.assertEqual(len(rendered["source_pages"]), 33)
        self.assertEqual(rendered["text_candidates"][-1]["source"], hits[-1]["source"])
        self.assertEqual(rendered["source_pages"][-1]["locator_source"],
                         pages[-1]["locator_source"])


if __name__ == "__main__":
    unittest.main()
