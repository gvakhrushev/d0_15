"""Hostile workspace-source expansion against real bounded producer results."""
from __future__ import annotations

import copy
import hashlib
import contextlib
import io
import sys
import json
import os
import pathlib
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from tools import proof_architecture as proof
from tools import proof_architecture_cold_start as cold
from tools import proof_architecture_cold_start_v3 as paged
from tools import compact_proof_architecture_cold_start_v3 as compactor


class WorkspaceSourcePagesTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = pathlib.Path(temporary.name)
        self.research = self.root / "02_REGISTRY/research"
        self.research.mkdir(parents=True)
        self.git("init", "-q")
        self.git("config", "user.name", "Workspace page test")
        self.git("config", "user.email", "workspace-page@example.invalid")

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root,
                                       stderr=subprocess.PIPE, text=True).strip()

    def source(self, relative, content):
        path = self.research / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def locator(self, query, targets, name="00_locator.md"):
        return self.source(name, "# " + query + "\n" + "".join(
            f"{query}: [source]({target})\n" for target in targets))

    def hits(self, query, locator, limit=18):
        hits = proof.full_text_search_many(self.root, [query], limit=limit)[0]
        locator_rel = locator.relative_to(self.root).as_posix()
        self.assertIn(locator_rel, [hit["source"] for hit in hits])
        return hits

    @staticmethod
    def candidates(pages):
        return [candidate for page in pages for candidate in page["candidates"]]

    def test_crowded_window_expands_actual_direct_content(self):
        query = "cobalt amber zircon nickel indigo sienna ochre quartz"
        slug = query.replace(" ", "_")
        paths = [self.source(f"sources/owner_{i:02d}.md", "cobalt amber mathematical owner\n")
                 for i in range(7)]
        locator = self.locator(query, [f"sources/owner_{i:02d}.md" for i in range(7)],
                               f"00_{slug}.md")
        for i in range(17):
            self.source(f"decoy_{i:02d}_{slug}.md", query + "\n")
        self.git("add", "02_REGISTRY")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "commit", "-qm", "fixtures")
        hits = self.hits(query, locator)
        source_paths = {p.relative_to(self.root).as_posix() for p in paths}
        self.assertTrue(source_paths.isdisjoint(hit["source"] for hit in hits))
        pages = proof.expand_workspace_source_pages(self.root, query, hits)
        candidates = self.candidates(pages)
        self.assertEqual({hit["source"] for hit in candidates}, source_paths)
        for hit in candidates:
            self.assertTrue(hit["direct_content"])
            self.assertEqual(hit["source_origin"], "workspace")
            self.assertEqual(hit["source_sha256"], hashlib.sha256((self.root / hit["source"]).read_bytes()).hexdigest())
            self.assertTrue(any(row.get("kind") == "direct_content" for row in hit["evidence_lines"]))
            self.assertNotIn("source_commit", hit)
            self.assertNotIn("source_blob", hit)
            self.assertEqual(hit["locator_source"], locator.relative_to(self.root).as_posix())
            self.assertGreater(hit["citation_line"], 0)

    def test_absent_stale_and_metadata_injection_do_not_open_unobserved_targets(self):
        query = "amberquartz"
        observed = self.source("sources/actual.md", "amberquartz real content\n")
        injected = self.source("sources/injected.md", "amberquartz unrelated target\n")
        locator = self.locator(query, ["sources/actual.md"])
        hits = self.hits(query, locator)
        one = [next(hit for hit in hits if hit["source"] == locator.relative_to(self.root).as_posix())]
        self.assertEqual(proof.expand_workspace_source_pages(self.root, query, []), [])
        forged = copy.deepcopy(one)
        forged[0]["source_refs"].append({"path": injected.relative_to(self.root).as_posix()})
        pages = proof.expand_workspace_source_pages(self.root, query, forged)
        sources = {hit["source"] for hit in self.candidates(pages)}
        self.assertIn(observed.relative_to(self.root).as_posix(), sources)
        self.assertNotIn(injected.relative_to(self.root).as_posix(), sources)
        locator.write_text(locator.read_text() + "changed after discovery\n", encoding="utf-8")
        self.assertEqual(proof.expand_workspace_source_pages(self.root, query, one), [])

    def test_source_body_must_meet_full_query_threshold(self):
        query = "amberquartz cobaltindigo greenruby purplegold silvergranite"
        incomplete = self.source("sources/cobaltindigo.md", "amberquartz only\n")
        complete = self.source("sources/complete.md", "amberquartz cobaltindigo\n")
        locator = self.locator(query, ["sources/cobaltindigo.md", "sources/complete.md"])
        hits = self.hits(query, locator)
        sources = {hit["source"] for hit in self.candidates(
            proof.expand_workspace_source_pages(self.root, query, hits))}
        self.assertIn(complete.relative_to(self.root).as_posix(), sources)
        self.assertNotIn(incomplete.relative_to(self.root).as_posix(), sources)

    def test_unsafe_paths_and_symlinks_never_expose_external_contents(self):
        query = "amberquartz"
        with tempfile.TemporaryDirectory() as external:
            outside = pathlib.Path(external) / "secret.md"
            outside.write_text("amberquartz private external content\n", encoding="utf-8")
            (self.research / "escape").symlink_to(pathlib.Path(external), target_is_directory=True)
            bait = self.source("secret.md", "amberquartz bait local content\n")
            safe = self.source("sources/safe.md", "amberquartz correct content\n")
            unsafe = ["../secret.md", str(bait), "https://example.org/secret.md",
                      "C:\\secret.md", "..%2fsecret.md", "escape/secret.md",
                      "sources/%2e%2e/secret.md", "sources/\x01secret.md"]
            locator = self.locator(query, unsafe + ["sources/safe.md"])
            hits = self.hits(query, locator)
            locator_only = [hit for hit in hits if hit["source"] == locator.relative_to(self.root).as_posix()]
            original_read = os.read
            outside_inode = outside.stat().st_ino
            def checked_read(fd, size):
                if os.fstat(fd).st_ino == outside_inode:
                    raise AssertionError("outside source was read")
                return original_read(fd, size)
            with patch.object(os, "read", checked_read):
                pages = proof.expand_workspace_source_pages(self.root, query, locator_only,
                                                             pages_per_locator=2)
            found = {hit["source"] for hit in self.candidates(pages)}
            self.assertEqual(found, {safe.relative_to(self.root).as_posix()})
            for page in pages:
                for hit in page["candidates"]:
                    self.assertNotIn("private external", str(hit))

    def test_missing_directory_and_oversized_sources_are_not_candidates(self):
        query = "amberquartz"
        safe = self.source("sources/safe.md", "amberquartz correct\n")
        oversized = self.source("sources/large.md", "amberquartz " + "x" * 4_000_001)
        directory = self.research / "sources" / "directory.md"
        directory.mkdir()
        locator = self.locator(query, ["sources/missing.md", "sources/directory.md",
                                       "sources/large.md", "sources/safe.md"])
        hits = self.hits(query, locator)
        pages = proof.expand_workspace_source_pages(self.root, query, hits)
        found = {hit["source"] for hit in self.candidates(pages)}
        self.assertIn(safe.relative_to(self.root).as_posix(), found)
        self.assertNotIn(oversized.relative_to(self.root).as_posix(), found)
        self.assertNotIn(directory.relative_to(self.root).as_posix(), found)
        self.assertNotIn((self.research / "sources/missing.md").relative_to(self.root).as_posix(), found)
        statuses = {row["citation_path"]: row["content_status"]
                    for page in pages for row in page["reference_statuses"]}
        self.assertEqual(statuses["sources/large.md"], "oversized")
        self.assertIn(statuses["sources/missing.md"], {"unsearchable_target", "missing_or_unreadable"})

    def test_bounded_pages_and_required_pin_and_query_scope(self):
        query, other = "amberquartz", "ornatecobalt"
        targets = [self.source(f"sources/a{i:02d}.md", "amberquartz valid\n") for i in range(10)]
        locator = self.locator(query + " " + other, [f"sources/a{i:02d}.md" for i in range(10)])
        hits = self.hits(query, locator)
        first = proof.expand_workspace_source_pages(self.root, query, hits, pages_per_locator=1)
        both = proof.expand_workspace_source_pages(self.root, query, hits, pages_per_locator=2)
        self.assertEqual([len(p["candidates"]) for p in first], [8])
        self.assertEqual([len(p["candidates"]) for p in both], [8, 2])
        self.assertEqual(first[0]["remaining_references"], 2)
        path = targets[0].relative_to(self.root).as_posix()
        candidates = self.candidates(both)
        ordinary = cold._required_source_status([(query, hits + candidates)], {"path": path})
        self.assertTrue(ordinary["found"])
        pinned = cold._required_source_status([(query, hits + candidates)],
                                               {"path": path, "commit": "a" * 40, "blob": "b" * 40})
        self.assertFalse(pinned["found"])
        other_hits = proof.full_text_search_many(self.root, [other], 18)[0]
        other_pages = proof.expand_workspace_source_pages(self.root, other, other_hits)
        scoped = cold._required_source_status([(query, hits + candidates),
                                                (other, other_hits + self.candidates(other_pages))],
                                               {"path": path, "scope_query_indexes": [0, 1]})
        self.assertFalse(scoped["found"])
        self.assertEqual([row["found"] for row in scoped["scoped_queries"]], [True, False])
        for key in ("page_size", "pages_per_locator"):
            for value in (0, 9):
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    proof.expand_workspace_source_pages(self.root, query, hits, **{key: value})


    def test_reference_cap_and_page_offset_report_truncation(self):
        query = "amberquartz"
        for i in range(70):
            self.source(f"sources/target_{i:02d}.md", query + " valid\n")
        locator = self.locator(query, [f"sources/target_{i:02d}.md" for i in range(70)])
        hits = self.hits(query, locator)
        one = [hit for hit in hits if hit["source"] == locator.relative_to(self.root).as_posix()]
        pages = proof.expand_workspace_source_pages(self.root, query, one, pages_per_locator=8)
        self.assertEqual(len(pages), 8)
        self.assertEqual(sum(len(page["candidates"]) for page in pages), 64)
        self.assertTrue(all(page["reference_set_may_be_truncated"] for page in pages))
        self.assertEqual(pages[-1]["remaining_references"], 0)
        tail = proof.expand_workspace_source_pages(self.root, query, one,
                                                    page_offset=7, pages_per_locator=2)
        self.assertEqual([p["page_number"] for p in tail], [8])
        self.assertEqual(tail[0]["candidates"], pages[7]["candidates"])
        for offset in (-1, 8):
            with self.subTest(offset=offset), self.assertRaises(ValueError):
                proof.expand_workspace_source_pages(self.root, query, one, page_offset=offset)

    def test_v3_rejects_forged_workspace_page_content_and_provenance(self):
        query = "amberquartz cobaltindigo"
        source = self.source("sources/owner.md", query + " exact source\n")
        alternate = self.source("sources/alternate.md", query + " unrelated source\n")
        locator = self.locator(query, ["sources/owner.md"])
        self.git("add", "02_REGISTRY")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "commit", "-qm", "fixtures")
        hits = proof.full_text_search_many(self.root, [query], limit=18, ranked_pages=2)[0]
        pages = paged.workspace_source_pages(self.root, query, hits, set(paged.corpus_paths(self.root)))
        self.assertEqual({h["source"] for h in self.candidates(pages)},
                         {source.relative_to(self.root).as_posix()})
        result = {"query": query, "ranked_pages": paged._ranked_pages(hits),
                  "source_pages": paged.source_pages(self.root, query, hits), "workspace_source_pages": pages}
        verified = paged.verified_query(self.root, query, result)
        self.assertTrue(any(hit.get("candidate_stage") == "workspace_source_page"
                            and hit["source"] == source.relative_to(self.root).as_posix()
                            for hit in verified))
        for mutation in ("locator_sha", "locator_rank", "citation_path", "citation_line",
                         "citation_text", "target", "source_hash", "evidence", "fake_commit", "fake_blob"):
            with self.subTest(mutation=mutation):
                forged = copy.deepcopy(result)
                page = forged["workspace_source_pages"][0]
                candidate = page["candidates"][0]
                if mutation == "locator_sha": page["locator_sha256"] = "f" * 64
                elif mutation == "locator_rank": page["locator_rank"] = len(hits) + 1
                elif mutation == "citation_path": candidate["citation_path"] = "sources/alternate.md"
                elif mutation == "citation_line": candidate["citation_line"] += 1
                elif mutation == "citation_text": candidate["citation_text"] = query + " forged line"
                elif mutation == "target": candidate["source"] = alternate.relative_to(self.root).as_posix()
                elif mutation == "source_hash": candidate["source_sha256"] = "a" * 64
                elif mutation == "evidence": candidate["evidence_lines"][0]["text"] = "forged evidence"
                elif mutation == "fake_commit": candidate["source_commit"] = "b" * 40
                else: candidate["source_blob"] = "a" * 40
                with self.assertRaises((ValueError, OSError)):
                    paged.verified_query(self.root, query, forged)



    def test_untrusted_code_fence_inline_code_and_image_are_not_links(self):
        query = "amberquartz"
        safe = self.source("sources/safe.md", "amberquartz valid\n")
        self.source("sources/poison.md", "amberquartz poison\n")
        locator = self.source("00_locator.md", "# amberquartz\n"
            "```text\namberquartz [bad](sources/poison.md)\n```\n"
            "amberquartz `[bad](sources/poison.md)` ![bad](sources/poison.md)\n"
            "amberquartz [good](sources/safe.md)\n")
        hits = self.hits(query, locator)
        pages = proof.expand_workspace_source_pages(self.root, query, hits, pages_per_locator=2)
        self.assertEqual({hit["source"] for hit in self.candidates(pages)},
                         {safe.relative_to(self.root).as_posix()})

    def test_unsupported_safe_open_fails_closed(self):
        query = "amberquartz"
        self.source("sources/safe.md", "amberquartz valid\n")
        locator = self.locator(query, ["sources/safe.md"])
        hits = self.hits(query, locator)
        with patch.object(os, "supports_dir_fd", set()):
            self.assertEqual(proof.expand_workspace_source_pages(self.root, query, hits), [])

    def test_target_changed_during_read_fails_closed(self):
        query = "amberquartz"
        target = self.source("sources/racing.md", "amberquartz original file\n")
        locator = self.locator(query, ["sources/racing.md"])
        hits = self.hits(query, locator)
        one = [hit for hit in hits if hit["source"] == locator.relative_to(self.root).as_posix()]
        inode = target.stat().st_ino
        original_read = os.read
        changed = False
        def racing_read(fd, size):
            nonlocal changed
            data = original_read(fd, size)
            if not changed and os.fstat(fd).st_ino == inode:
                changed = True
                target.write_text("amberquartz altered while reading target\n", encoding="utf-8")
            return data
        with patch.object(os, "read", racing_read):
            pages = proof.expand_workspace_source_pages(self.root, query, one)
        self.assertTrue(changed)
        self.assertEqual(self.candidates(pages), [])
        self.assertEqual(pages[0]["reference_statuses"][0]["content_status"], "changed_during_read")

    def test_cli_workspace_pages_include_actual_provenance_and_validate_offset(self):
        query = "amberquartz cobaltindigo"
        target = self.source("sources/owner.md", query + " actual\n")
        locator = self.locator(query, ["sources/owner.md"])
        dataset = {"snapshot_commit": "fixture", "worktree_dirty": False, "source_digests": {}}
        output = io.StringIO()
        argv = ["proof_architecture.py", "--repo-root", str(self.root), "search", "--limit", "18",
                "--workspace-source-pages", "1", query]
        with patch.object(sys, "argv", argv), patch.object(proof, "load_dataset", return_value=dataset), \
             patch.object(proof, "structured_search", return_value=[]), contextlib.redirect_stdout(output):
            self.assertEqual(proof.main(), 0)
        result = json.loads(output.getvalue())
        candidate = next(hit for page in result["workspace_source_pages"] for hit in page["candidates"]
                         if hit["source"] == target.relative_to(self.root).as_posix())
        self.assertEqual(candidate["locator_source"], locator.relative_to(self.root).as_posix())
        self.assertEqual(candidate["citation_path"], "sources/owner.md")
        self.assertEqual(candidate["citation_line"], 2)
        self.assertEqual(candidate["source_origin"], "workspace")
        self.assertTrue(candidate["direct_content"])
        self.assertNotIn("source_commit", candidate)
        self.assertNotIn("source_blob", candidate)
        bad = ["proof_architecture.py", "--repo-root", str(self.root), "search",
               "--workspace-page-offset", "1", query]
        with patch.object(sys, "argv", bad), patch.object(proof, "load_dataset", return_value=dataset), \
             contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
            proof.main()
        self.assertEqual(raised.exception.code, 2)

    def test_v3_independent_checks_when_producer_repeats_forgery(self):
        query = "amberquartz cobaltindigo"
        source = self.source("sources/owner.md", query + " owner actual\n")
        alternate = self.source("sources/alternate.md", query + " alternate actual\n")
        locator = self.source("00_locator.md", "# " + query + "\n"
            "```text\n" + query + " [bad](sources/alternate.md)\n```\n" +
            query + " [good](sources/owner.md)\n")
        hits = proof.full_text_search_many(self.root, [query], limit=18, ranked_pages=2)[0]
        pages = paged.workspace_source_pages(self.root, query, hits, set(paged.corpus_paths(self.root)))
        self.assertEqual(len(self.candidates(pages)), 1)
        result = {"query": query, "ranked_pages": paged._ranked_pages(hits),
                  "source_pages": paged.source_pages(self.root, query, hits),
                  "workspace_source_pages": pages}
        for mutation in ("locator_sha", "wrong_target", "fake_commit", "fake_blob", "evidence", "fence"):
            with self.subTest(mutation=mutation):
                forged = copy.deepcopy(result)
                page = forged["workspace_source_pages"][0]
                candidate, status = page["candidates"][0], page["reference_statuses"][0]
                if mutation == "locator_sha":
                    page["locator_sha256"] = "f" * 64
                elif mutation in {"wrong_target", "fence"}:
                    terms = proof._query_terms(query)
                    alt_rel = alternate.relative_to(self.root).as_posix()
                    replacement = proof._candidate_record(alt_rel, alternate.read_text(), terms,
                                                           origin="workspace")[1]
                    replacement.update({key: candidate[key] for key in
                                        ("locator_source", "citation_path", "citation_line", "citation_text")})
                    if mutation == "fence":
                        replacement.update({"citation_path": "sources/alternate.md", "citation_line": 3,
                                            "citation_text": locator.read_text().splitlines()[2]})
                        status.update({"citation_path": replacement["citation_path"],
                                       "citation_line": replacement["citation_line"],
                                       "citation_text": replacement["citation_text"]})
                    page["candidates"][0] = replacement
                    status["source"] = alt_rel
                elif mutation == "fake_commit": candidate["source_commit"] = "b" * 40
                elif mutation == "fake_blob": candidate["source_blob"] = "a" * 40
                else: candidate["evidence_lines"][0]["text"] = "forged evidence"
                with patch.object(paged, "workspace_source_pages", return_value=forged["workspace_source_pages"]):
                    with self.assertRaises((ValueError, OSError)):
                        paged.verified_query(self.root, query, forged)

    def test_compactor_rejects_forged_workspace_target_and_locator(self):
        query = "amberquartz cobaltindigo"
        source = self.source("sources/owner.md", query + " exact source\n")
        alternate = self.source("sources/alternate.md", query + " unrelated\n")
        self.locator(query, ["sources/owner.md"])
        self.git("add", "-A")
        self.git("commit", "-qm", "corpus")
        head = self.git("rev-parse", "HEAD")
        fixture = {"id": "workspace-page-check", "queries": [query],
                   "required_refs": [], "required_sources": [
                       {"path": source.relative_to(self.root).as_posix()}],
                   "scope_review": "Manual scope remains open."}
        dataset = {"snapshot_commit": head, "worktree_dirty": False, "source_digests": {}}
        impact = {"id": "exact-source-vs-unrelated-prose", "status": "pass",
                  "source_hash_changed": True, "unrelated_prose_left_source_hash": True,
                  "declared_application": "native-result-to-obligation"}
        with patch.object(cold, "CASES", [fixture]), \
             patch.object(proof, "load_dataset", return_value=dataset), \
             patch.object(cold, "_case10_change_impact_regression", return_value=impact):
            report = paged.run(self.root)
            summary = compactor.compact(json.dumps(report).encode(), self.root)
            self.assertEqual(summary["schema"], compactor.SUMMARY_SCHEMA)
            for mutation in ("target", "locator", "omission"):
                forged = copy.deepcopy(report)
                result = forged["cases"][0]["query_results"][0]
                page = result["workspace_source_pages"][0]
                if mutation == "target":
                    page["candidates"][0]["source"] = alternate.relative_to(self.root).as_posix()
                elif mutation == "locator":
                    page["locator_sha256"] = "f" * 64
                else:
                    result.pop("workspace_source_pages")
                with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                    compactor.compact(json.dumps(forged).encode(), self.root)


if __name__ == "__main__":
    unittest.main()
