"""Git-backed controls for the experimental C0 candidate range verifier."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools import c0_candidate_ranges as check


READER = Path(os.environ.get("C0_BOOK_READER", str(Path(__file__).with_name("c0_book_byte_partition.py"))))
BOOK1 = "01_BOOKS/BOOK_01_FIXTURE.md"
BOOK2 = "01_BOOKS/BOOK_02_FIXTURE.md"


class CandidateRangeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = check.load_reader(READER)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "core.autocrlf", "false")
        self.heading1 = b"### 01.1.8 One\n\n"
        self.heading2 = b"## 02.3b Two\n"
        self.data1 = self.heading1 + b"alpha\n\nbeta\n\n"
        self.data2 = self.heading2 + b"\nalpha\n\nbeta\n\n"
        self.write(BOOK1, self.data1)
        self.write(BOOK2, self.data2)
        self.source_commit = self.commit("book inputs")
        self.blob1 = self.git("rev-parse", f"{self.source_commit}:{BOOK1}")
        self.blob2 = self.git("rev-parse", f"{self.source_commit}:{BOOK2}")
        self.primary = self.make_primary()
        self.write(check.PRIMARY, self.primary.encode("utf-8"))
        self.snapshot = self.commit("declared candidate ranges")

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              encoding="utf-8").stdout.strip()

    def write(self, path, data):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def commit(self, message):
        self.git("add", "-A")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-q", "-m", message)
        return self.git("rev-parse", "HEAD")

    def make_primary(self):
        sha1 = hashlib.sha256(self.data1).hexdigest()
        sha2 = hashlib.sha256(self.data2).hexdigest()
        h1, h2 = len(self.heading1), len(self.heading2)
        return (f"### C0 source review candidate: Book01 §01.1.8\n\n"
                f"On snapshot `{self.source_commit}`, `{BOOK1}` has Git blob `{self.blob1}`. "
                f"The complete section is `[0,{len(self.data1)})`, SHA-256 `{sha1}`.\n\n"
                "| Byte range | Candidate disposition and existing support |\n| --- | --- |\n"
                f"| `[0,{h1})` | Heading and separator, structural context. |\n"
                f"| `[{h1},{h1+7})` | First candidate. |\n"
                f"| `[{h1+7},{len(self.data1)})` | Second candidate. |\n\n"
                f"### C0 source review candidate: Book02 §02.3b\n\n"
                f"On the same snapshot `{self.source_commit}`, `{BOOK2}` has Git blob `{self.blob2}`. "
                f"The complete section is the half-open byte range `[0,{len(self.data2)})`, SHA-256 `{sha2}`. "
                f"The heading `[0,{h2})` and the one-byte LF separators between the following ranges are structural; "
                "the final separator is included in the section range.\n\n"
                "| Byte range | Candidate disposition and existing support |\n| --- | --- |\n"
                f"| `[{h2+1},{h2+7})` | First candidate. |\n"
                f"| `[{h2+8},{h2+13})` | Second candidate. |\n")

    def check_rejected(self, primary, message):
        self.write(check.PRIMARY, primary.encode("utf-8"))
        with self.assertRaisesRegex(check.VerificationError, message):
            check.verify(self.reader, self.root, self.commit("bad primary"))

    def test_declared_ranges_cover_pinned_bytes(self):
        result = check.verify(self.reader, self.root, self.snapshot)
        self.assertEqual(result["status"], "candidate_byte_coverage_verified")
        self.assertEqual(len(result["candidates"]), 2)
        self.assertEqual(result["candidates"][0]["table_ranges"][0]["role"], "structural")
        self.assertEqual(len(result["candidates"][0]["table_ranges"]), 3)
        for item in result["candidates"]:
            self.assertEqual(item["acceptance"], "not_assessed")
            self.assertEqual(item["semantic_classification"], "not_assessed")
            self.assertEqual(item["text_boundaries"], "utf8_decodable")

    def test_missing_interval_is_rejected(self):
        h = len(self.heading1)
        self.check_rejected(self.primary.replace(f"| `[{h},{h+7})` | First candidate. |\n", ""), "gap")

    def test_overlapping_interval_is_rejected(self):
        h = len(self.heading1)
        self.check_rejected(self.primary.replace(f"`[{h+7},{len(self.data1)})`", f"`[{h+6},{len(self.data1)})`"), "overlap")

    def test_changed_content_with_old_digest_is_rejected(self):
        self.write(BOOK2, self.data2.replace(b"alpha", b"ALPHA"))
        source = self.commit("mutate source")
        blob = self.git("rev-parse", f"{source}:{BOOK2}")
        changed = self.primary.replace(self.source_commit, source).replace(self.blob2, blob)
        self.check_rejected(changed, "SHA-256 mismatch")

    def test_wrong_blob_is_rejected(self):
        self.check_rejected(self.primary.replace(self.blob2, "a" * 40), "source blob")

    def test_bad_digest_is_rejected(self):
        expected = hashlib.sha256(self.data1).hexdigest()
        self.check_rejected(self.primary.replace(expected, "0" * 64), "SHA-256 mismatch")

    def test_truncated_section_with_matching_sha_and_table_is_rejected(self):
        length = len(self.data1)
        original_sha = hashlib.sha256(self.data1).hexdigest()
        truncated_sha = hashlib.sha256(self.data1[:-1]).hexdigest()
        changed = self.primary.replace(original_sha, truncated_sha).replace(
            f"[0,{length})", f"[0,{length-1})", 1).replace(
            f",{length})` | Second candidate.", f",{length-1})` | Second candidate.", 1)
        self.check_rejected(changed, "complete lexical heading section")

    def test_non_lf_separator_is_rejected_even_with_matching_sha(self):
        separator = len(self.heading2) + 7
        altered = self.data2[:separator] + b"X" + self.data2[separator + 1:]
        self.write(BOOK2, altered)
        source = self.commit("alter separator")
        blob = self.git("rev-parse", f"{source}:{BOOK2}")
        changed = (self.primary.replace(self.source_commit, source).replace(self.blob2, blob)
                   .replace(hashlib.sha256(self.data2).hexdigest(), hashlib.sha256(altered).hexdigest()))
        self.check_rejected(changed, "exactly one LF")

    def test_structural_declaration_is_required(self):
        self.check_rejected(self.primary.replace("one-byte LF separators", "separators"), "LF declarations")

    def test_malformed_table_row_is_not_silently_ignored(self):
        h = len(self.heading1)
        self.check_rejected(self.primary.replace(f"| `[{h},{h+7})`", f"| [{h},{h+7})"), "malformed")

    def test_numerically_complete_ranges_cannot_split_utf8_character(self):
        altered = self.data1.replace(b"alpha", "A§ha".encode("utf-8"))
        self.assertEqual(len(altered), len(self.data1))
        self.write(BOOK1, altered)
        source = self.commit("add multibyte character")
        blob = self.git("rev-parse", f"{source}:{BOOK1}")
        h = len(self.heading1)
        first = f"| `[{h},{h+7})` | First candidate. |"
        split = (f"| `[{h},{h+2})` | First half. |\n"
                 f"| `[{h+2},{h+7})` | Second half. |")
        changed = (self.primary.replace(self.source_commit, source).replace(self.blob1, blob)
                   .replace(hashlib.sha256(self.data1).hexdigest(), hashlib.sha256(altered).hexdigest())
                   .replace(first, split))
        self.check_rejected(changed, "splits UTF-8")

    def test_merged_rows_prove_only_coverage_not_unit_count(self):
        h = len(self.heading1)
        first = (f"| `[{h},{h+7})` | First candidate. |\n"
                 f"| `[{h+7},{len(self.data1)})` | Second candidate. |")
        merged = f"| `[{h},{len(self.data1)})` | Merged review range. |"
        self.write(check.PRIMARY, self.primary.replace(first, merged).encode("utf-8"))
        result = check.verify(self.reader, self.root, self.commit("merge candidate rows"))
        self.assertEqual(len(result["candidates"][0]["table_ranges"]), 2)
        self.assertEqual(result["candidates"][0]["acceptance"], "not_assessed")
        self.assertEqual(result["candidates"][0]["semantic_classification"], "not_assessed")
        self.assertIn("do not establish a mathematical-unit count", result["scope"])

    def test_broken_reader_fails_closed_without_traceback(self):
        script = Path(check.__file__)
        for name, contents in (("syntax.py", b"def invalid(:\n"),
                               ("no_api.py", b"# missing reader API\n"),
                               ("bad_stub.py", b"def _require_repo_root(x): raise RuntimeError('bad')\n")):
            with self.subTest(name=name):
                path = self.root / name
                path.write_bytes(contents)
                result = subprocess.run([sys.executable, "-X", "utf8", str(script),
                    "--repo", str(self.root), "--snapshot", self.snapshot, "--reader", str(path)],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
                self.assertEqual(result.returncode, 1)
                self.assertIn('"status": "unresolved"', result.stdout)
                self.assertNotIn("Traceback", result.stderr)

    def test_untracked_primary_is_not_a_snapshot(self):
        target = self.root / check.PRIMARY
        target.unlink()
        snapshot = self.commit("delete primary")
        self.write(check.PRIMARY, self.primary.encode("utf-8"))
        with self.assertRaisesRegex(check.VerificationError, "tracked path"):
            check.verify(self.reader, self.root, snapshot)

    def test_architecture_cli_checks_declared_ranges(self):
        cli = Path(__file__).with_name("proof_architecture.py")
        proc = subprocess.run([sys.executable, "-X", "utf8", str(cli), "--repo-root", str(self.root),
                               "--json", "c0-ranges", "--snapshot", self.snapshot],
                              capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        view = json.loads(proc.stdout)
        self.assertEqual(view["status"], "candidate_byte_coverage_verified")
        self.assertTrue(all(item["acceptance"] == "not_assessed" for item in view["candidates"]))

    def test_book01_0116_is_explicit_and_checks_actual_source(self):
        repo = Path(__file__).resolve().parent.parent
        raw = (repo / check.PRIMARY).read_bytes()
        default = check.parse_primary(raw)
        selected = check.parse_primary(raw, include_book01_0116=True)
        self.assertEqual({x["title"] for x in default}, set(check.TITLES))
        third, = [x for x in selected if x["title"] == check.BOOK01_0116]
        self.assertEqual(len(selected), 3)
        result = check.verify_candidate(self.reader, repo, third)
        self.assertEqual(result["acceptance"], "not_assessed")
        self.assertEqual(result["semantic_classification"], "not_assessed")

    def test_architecture_cli_opt_in_rejects_missing_third_section(self):
        cli = Path(__file__).with_name("proof_architecture.py")
        proc = subprocess.run([sys.executable, "-X", "utf8", str(cli),
                               "--repo-root", str(self.root), "--json", "c0-ranges",
                               "--snapshot", self.snapshot, "--include-book01-0116"],
                              capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(json.loads(proc.stdout)["status"], "unresolved")
        self.assertNotIn("Traceback", proc.stderr)

    def test_book01_0116_fails_closed_for_wrong_section_digest_or_source(self):
        repo = Path(__file__).resolve().parent.parent
        raw = (repo / check.PRIMARY).read_bytes()
        third, = [x for x in check.parse_primary(raw, include_book01_0116=True)
                  if x["title"] == check.BOOK01_0116]
        for change in ({"title": "Book01 §01.1.8"},
                       {"sha256": "0" * 64},
                       {"blob": "0" * 40}):
            with self.subTest(change=change):
                with self.assertRaises(check.VerificationError):
                    check.verify_candidate(self.reader, repo, {**third, **change})
        with self.assertRaisesRegex(check.VerificationError, "missing"):
            check.parse_primary(self.primary.encode(), include_book01_0116=True)


if __name__ == "__main__":
    unittest.main()
