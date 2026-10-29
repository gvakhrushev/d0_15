"""Hostile controls for the unresolved Git-backed book byte-partition view."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from tools import c0_book_byte_partition as candidate


class BytePartitionTests(unittest.TestCase):
    def verify_partition(self, data: bytes, expected_titles: list[str]) -> None:
        spans = candidate.partition(data, "a" * 40, "01_BOOKS/BOOK_00.md")
        self.assertEqual([s["heading_text"] for s in spans if s["kind"] == "heading_section"],
                         expected_titles)
        self.assertEqual(spans[0]["kind"], "preamble")
        self.assertEqual(spans[0]["byte_start"], 0)
        self.assertEqual(spans[-1]["byte_end_exclusive"], len(data))
        self.assertEqual([s["byte_end_exclusive"] for s in spans[:-1]],
                         [s["byte_start"] for s in spans[1:]])
        self.assertEqual(b"".join(data[s["byte_start"]:s["byte_end_exclusive"]] for s in spans), data)
        for span in spans:
            raw = data[span["byte_start"]:span["byte_end_exclusive"]]
            self.assertEqual(span["span_sha256"], hashlib.sha256(raw).hexdigest())
            self.assertEqual(span["disposition"], "unresolved")
            self.assertEqual(span["mathematical_units"], "not_assessed")

    def test_preamble_utf8_crlf_nested_duplicates_and_last_byte(self) -> None:
        self.verify_partition("Преамбула ё\r\n# Top\r\n## Same\r\nβ\r\n### Same\r\nend".encode(),
                              ["Top", "Same", "Same"])

    def test_fences_with_different_markers_lengths_and_nonclosing_tail(self) -> None:
        data = (b"# Root\n````lean\n## not-heading\n```\n### still-code\n"
                b"```` trailing\n# still-code\n````\n~~~math\n# fake\n~~~\n"
                b"## Real ##\n")
        self.verify_partition(data, ["Root", "Real"])

    def test_unclosed_fence_empty_headings_and_indent(self) -> None:
        data = b"before\n#\n##  \n    # indented\n> ## quote\n#not-a-heading\n~~~\n# in-code\n"
        self.verify_partition(data, ["", ""])

    def test_empty_and_heading_free_sources_keep_every_byte(self) -> None:
        self.verify_partition(b"", [])
        self.verify_partition(b"no heading\nlast", [])

    def test_utf8_bom_does_not_prevent_first_heading_detection(self) -> None:
        self.verify_partition(b"\xef\xbb\xbf# Heading\ntext", ["Heading"])

    def test_only_the_declared_lexical_grammar_is_claimed(self) -> None:
        # No CommonMark or LaTeX semantics is inferred from this split: list
        # fences and math interiors can yield candidate headings for review.
        self.verify_partition(b"- ```\n  # candidate\n- ```\n\\[\n# also candidate\n\\]",
                              ["candidate", "also candidate"])

    def test_non_utf8_is_explicitly_unresolved(self) -> None:
        with self.assertRaises(candidate.EvidenceError):
            candidate.partition(b"# Heading\n\xff", "a" * 40, "x")


class GitEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="d0-book-spans-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.git("init", "-q")
        self.git("config", "core.autocrlf", "false")
        (self.root / "01_BOOKS").mkdir()
        self.names = ("BOOK_00_one.md", "BOOK_01_two.md")
        self.data = ("# Первый\n## proof\ntext ё\n".encode(), b"raw preamble\n# Second\nend")
        for name, data in zip(self.names, self.data):
            (self.root / "01_BOOKS" / name).write_bytes(data)
        self.git("add", "--all")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "commit", "-q", "-m", "books")
        self.head = self.git("rev-parse", "HEAD").decode().strip()

    def git(self, *args: str) -> bytes:
        return subprocess.run(["git", "-C", str(self.root), *args], check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              env=candidate._git_env()).stdout

    def capture(self) -> dict:
        return candidate.capture(self.root, self.head, self.names)

    def test_architecture_cli_exposes_unresolved_book_set_and_all_spans(self) -> None:
        cli = Path(__file__).with_name("proof_architecture.py")
        proc = subprocess.run([sys.executable, str(cli), "--repo-root", str(self.root),
                               "--json", "c0-books", "--snapshot", self.head],
                              capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 1, proc.stderr)
        view = json.loads(proc.stdout)
        self.assertEqual(view["capture_status"], "unresolved_book_set")
        self.assertEqual(len(view["sources"]), 2)
        self.assertTrue(all(s["disposition"] == "unresolved" for source in view["sources"]
                            for s in source["spans"]))

    def test_architecture_cli_preserves_long_heading(self) -> None:
        title = "x" * 9000
        (self.root / "01_BOOKS" / self.names[0]).write_text("# " + title + "\n", encoding="utf-8")
        self.git("add", "--all")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "commit", "-q", "-m", "long heading")
        head = self.git("rev-parse", "HEAD").decode().strip()
        cli = Path(__file__).with_name("proof_architecture.py")
        proc = subprocess.run([sys.executable, str(cli), "--repo-root", str(self.root),
                               "--json", "c0-books", "--snapshot", head],
                              capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 1, proc.stderr)
        view = json.loads(proc.stdout)
        self.assertEqual(view["sources"][0]["spans"][1]["heading_text"], title)

    def test_pinned_git_bytes_ignore_dirty_and_untracked_checkout(self) -> None:
        (self.root / "01_BOOKS" / self.names[0]).write_bytes(b"uncommitted replacement")
        (self.root / "01_BOOKS" / "BOOK_02_untracked.md").write_bytes(b"untracked")
        view = self.capture()
        self.assertEqual(view["capture_status"], "expected_book_blob_bytes_reconstructed")
        self.assertEqual([x["path"] for x in view["sources"]], ["01_BOOKS/" + n for n in self.names])
        for item, expected in zip(view["sources"], self.data):
            self.assertEqual(item["sha256"], hashlib.sha256(expected).hexdigest())
            self.assertEqual(b"".join(expected[s["byte_start"]:s["byte_end_exclusive"]]
                                      for s in item["spans"]), expected)

    def test_git_environment_redirects_and_config_injection_are_ignored(self) -> None:
        other = tempfile.TemporaryDirectory(prefix="d0-other-git-")
        self.addCleanup(other.cleanup)
        subprocess.run(["git", "-C", other.name, "init", "-q"], check=True,
                       env=candidate._git_env())
        with mock.patch.dict(os.environ, {"GIT_DIR": str(Path(other.name) / ".git"),
                                         "GIT_WORK_TREE": other.name,
                                         "GIT_CONFIG_COUNT": "1",
                                         "GIT_CONFIG_KEY_0": "core.worktree",
                                         "GIT_CONFIG_VALUE_0": other.name}):
            self.assertEqual(self.capture()["snapshot_commit"], self.head)

    def test_git_replace_commit_does_not_modify_pinned_objects(self) -> None:
        (self.root / "01_BOOKS" / self.names[0]).write_bytes(b"# replaced\n")
        self.git("add", "--all")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "commit", "-q", "-m", "replacement")
        replacement = self.git("rev-parse", "HEAD").decode().strip()
        self.git("replace", self.head, replacement)
        view = self.capture()
        self.assertEqual(view["sources"][0]["sha256"], hashlib.sha256(self.data[0]).hexdigest())

    def test_git_replace_blob_does_not_modify_pinned_bytes(self) -> None:
        blob = self.git("rev-parse", f"{self.head}:01_BOOKS/{self.names[0]}").decode().strip()
        other = subprocess.run(["git", "-C", str(self.root), "hash-object", "-w", "--stdin"],
                               input=b"different source", stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, check=True, env=candidate._git_env()).stdout.decode().strip()
        self.git("replace", blob, other)
        self.assertEqual(self.capture()["sources"][0]["sha256"], hashlib.sha256(self.data[0]).hexdigest())

    def test_missing_or_noncommit_snapshot_is_unresolved(self) -> None:
        with self.assertRaises(candidate.EvidenceError):
            candidate.capture(self.root, "f" * 40, self.names)
        tree = self.git("rev-parse", "HEAD^{tree}").decode().strip()
        with self.assertRaises(candidate.EvidenceError):
            candidate.capture(self.root, tree, self.names)
        with self.assertRaises(candidate.EvidenceError):
            candidate.capture(self.root, "HEAD", self.names)

    def test_missing_and_extra_book_are_visible_not_silently_dropped(self) -> None:
        view = candidate.capture(self.root, self.head, (self.names[0], "BOOK_02_missing.md"))
        self.assertEqual(view["capture_status"], "unresolved_book_set")
        self.assertEqual(view["missing_expected_books"], ["BOOK_02_missing.md"])
        self.assertEqual(view["unexpected_book_candidates"], [self.names[1]])
        self.assertEqual(len(view["sources"]), 2)

    def test_repository_subdirectory_is_not_a_repository_root(self) -> None:
        with self.assertRaises(candidate.EvidenceError):
            candidate.capture(self.root / "01_BOOKS", self.head, self.names)

    def test_case_variant_new_book_is_an_unexpected_candidate(self) -> None:
        (self.root / "01_BOOKS" / "book_02_new.MD").write_bytes(b"# New book\n")
        self.git("add", "--all")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "commit", "-q", "-m", "new book candidate")
        newer = self.git("rev-parse", "HEAD").decode().strip()
        view = candidate.capture(self.root, newer, self.names)
        self.assertEqual(view["capture_status"], "unresolved_book_set")
        self.assertEqual(view["unexpected_book_candidates"], ["book_02_new.MD"])

    def test_forged_raw_git_object_is_rejected(self) -> None:
        real = candidate._git
        def forged(repo: Path, *args: str) -> bytes:
            if args[:2] == ("cat-file", "blob"):
                return b"wrong bytes"
            return real(repo, *args)
        with mock.patch.object(candidate, "_git", side_effect=forged):
            with self.assertRaisesRegex(candidate.EvidenceError, "bytes do not match"):
                self.capture()

    def test_git_unavailable_is_controlled(self) -> None:
        with mock.patch.object(candidate.subprocess, "run", side_effect=FileNotFoundError):
            with self.assertRaisesRegex(candidate.EvidenceError, "unavailable"):
                self.capture()

    def test_tracked_symlink_source_is_not_followed(self) -> None:
        blob = self.git("rev-parse", f"{self.head}:01_BOOKS/{self.names[0]}").decode().strip()
        self.git("update-index", "--cacheinfo", "120000", blob, "01_BOOKS/" + self.names[0])
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "commit", "-q", "-m", "symlink mode")
        revised = self.git("rev-parse", "HEAD").decode().strip()
        with self.assertRaisesRegex(candidate.EvidenceError, "not a regular tracked file"):
            candidate.capture(self.root, revised, self.names)

    def test_malformed_tree_is_controlled(self) -> None:
        with self.assertRaises(candidate.EvidenceError):
            candidate._tree_entries(b"100644 entry\0truncated")


if __name__ == "__main__":
    unittest.main()
