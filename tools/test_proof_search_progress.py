"""Bounded controls for optional early search progress diagnostics."""
import contextlib
import io
import json
import os
import pathlib
import tempfile
import unittest
from unittest import mock

from tools import proof_architecture as proof
from tools import proof_architecture_cold_start_v3 as paged


class SearchProgressTests(unittest.TestCase):
    def test_prefilter_counters_include_the_current_event_even_on_skips(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary).resolve()
            research = root / "02_REGISTRY" / "research"
            research.mkdir(parents=True)
            (research / "owner.md").write_text("amber\n", encoding="utf-8")
            events = [
                json.dumps({"type": "begin"}),
                json.dumps({"type": "match", "data": {}}),
                "not-json",
                json.dumps({"type": "match", "data": {"path": {"text": ""}}}),
                json.dumps({"type": "end"}),
                json.dumps({"type": "match", "data": {
                    "path": {"text": "02_REGISTRY/research/owner.md"},
                    "lines": {"text": "amber"}}}),
            ]
            stderr = io.StringIO()
            with mock.patch.dict(os.environ, {"D0_PROOF_SEARCH_PROGRESS": "1"}), \
                 mock.patch.object(proof, "_SEARCH_PROGRESS_INTERVAL", 2), \
                 mock.patch.object(proof, "_rg_text_lines", return_value=iter(events)), \
                 contextlib.redirect_stderr(stderr):
                proof.full_text_search_many(root, ["amber"], 18)
            logs = [json.loads(line) for line in stderr.getvalue().splitlines()]
            progress = [(row["events"], row["match_events"]) for row in logs
                        if row["proof_search_progress"] == "prefilter_running"]
            self.assertEqual(progress, [(2, 1), (4, 2), (6, 3)])
            complete = next(row for row in logs if row["proof_search_progress"] == "prefilter_complete")
            self.assertEqual((complete["events"], complete["match_events"]), (6, 3))

    def test_progress_preserves_search_and_snapshot_and_is_stderr_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary).resolve()
            research = root / "02_REGISTRY" / "research"
            research.mkdir(parents=True)
            for index, content in enumerate(("# Amber native\nCafé proof\n",
                                             "# Amber\nnative proof\n",
                                             "# Native amber\nproof\n")):
                (research / f"case_{index}.md").write_text(content, encoding="utf-8")
            queries = ["amber native", "café proof", "amber native"]
            observations = []
            for setting in ("0", "1"):
                stdout, stderr = io.StringIO(), io.StringIO()
                with mock.patch.dict(os.environ, {"D0_PROOF_SEARCH_PROGRESS": setting}), \
                     mock.patch.object(proof, "_SEARCH_PROGRESS_INTERVAL", 2), \
                     mock.patch.object(proof, "_rg_text_lines", wraps=proof._rg_text_lines) as scan, \
                     mock.patch.object(proof.subprocess, "run", wraps=proof.subprocess.run) as commands, \
                     contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    snapshot = paged.corpus_snapshot(root)
                    hits = proof.full_text_search_many(root, queries, 18, ranked_pages=2)
                self.assertEqual(stdout.getvalue(), "")
                self.assertEqual(scan.call_count, 1)
                rg_lists = [call for call in commands.call_args_list
                            if call.args and call.args[0][:2] == ["rg", "--files"]]
                self.assertEqual(len(rg_lists), 2)  # snapshot and search, one each
                observations.append((snapshot, hits))
                if setting == "0":
                    self.assertEqual(stderr.getvalue(), "")
                else:
                    events = [json.loads(line) for line in stderr.getvalue().splitlines()]
                    stages = [event["proof_search_progress"] for event in events]
                    for stage in ("corpus_enumeration_started", "corpus_snapshot_started", "corpus_snapshot_running",
                                  "corpus_snapshot_complete", "search_started",
                                  "prefilter_started", "prefilter_running", "prefilter_complete",
                                  "file_enumeration_started", "file_enumeration_complete",
                                  "document_reads_attempted", "candidate_query_running",
                                  "candidate_query_complete", "corpus_candidates_ready"):
                        self.assertIn(stage, stages)
                    self.assertLess(stages.index("prefilter_complete"),
                                    stages.index("corpus_candidates_ready"))
                    self.assertEqual(sum(stage == "candidate_query_complete" for stage in stages),
                                     len(queries))
                    self.assertEqual(next(event["files_hashed"] for event in events
                                          if event["proof_search_progress"] == "corpus_snapshot_complete"), 3)
            self.assertEqual(observations[0], observations[1])

    def test_failed_document_read_is_counted_as_attempt_not_success(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary).resolve()
            research = root / "02_REGISTRY" / "research"
            research.mkdir(parents=True)
            for name in ("a.md", "b.md"):
                (research / name).write_text("amber native\n", encoding="utf-8")
            denied = proof._search_filesystem_path(research / "a.md")
            read_bytes = pathlib.Path.read_bytes
            def fail_one(path):
                if path == denied:
                    raise OSError("fixture: unreadable")
                return read_bytes(path)
            stderr = io.StringIO()
            with mock.patch.dict(os.environ, {"D0_PROOF_SEARCH_PROGRESS": "1"}), \
                 mock.patch.object(proof, "_SEARCH_PROGRESS_INTERVAL", 1), \
                 mock.patch.object(pathlib.Path, "read_bytes", fail_one), \
                 contextlib.redirect_stderr(stderr):
                hits = proof.full_text_search_many(root, ["amber native"], 18)
            events = [json.loads(line) for line in stderr.getvalue().splitlines()]
            attempts = [event["count"] for event in events
                        if event["proof_search_progress"] == "document_reads_attempted"]
            self.assertEqual(attempts, [1, 2])
            self.assertEqual([hit["source"] for hit in hits[0]],
                             ["02_REGISTRY/research/b.md"])


if __name__ == "__main__":
    unittest.main()
