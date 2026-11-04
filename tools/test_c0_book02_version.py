"""Controls for the exact Book02 version gate and byte-boundary mapping."""
import hashlib
from pathlib import Path
import re
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from tools import c0_book02_version as version
from tools import c0_candidate_ranges as ranges
from tools import c0_book_byte_partition as reader


class Book02VersionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corrected = (Path(__file__).resolve().parents[1] / version.PATH).read_bytes()
        if cls.corrected.count(version.CORRECTED) != 1:
            raise AssertionError("corrected Book02 text is missing or ambiguous")
        cls.original = cls.corrected.replace(version.CORRECTED, version.ORIGINAL)

    def test_exact_versions_and_historical_evidence(self):
        old = version.classify(self.original, version.ORIGINAL_BLOB,
                               self.original, version.ORIGINAL_BLOB)
        new = version.classify(self.original, version.ORIGINAL_BLOB,
                               self.corrected, version.CORRECTED_BLOB)
        self.assertEqual(old["version"], "historical")
        self.assertEqual(new["version"], "corrected")
        self.assertEqual(old["section_range"], [12086, 15801])
        self.assertEqual(new["section_range"], [12086, 15810])
        self.assertEqual(new["semantic_acceptance"], "not_assessed")
        self.assertEqual(hashlib.sha256(self.corrected[12086:15810]).hexdigest(),
                         version.SECTION_CORRECTED_SHA256)

    def test_mutations_and_false_blob_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "source changed"):
            version.classify(self.original, version.ORIGINAL_BLOB,
                             self.corrected + b"x", version.CORRECTED_BLOB)
        with self.assertRaisesRegex(ValueError, "source changed"):
            version.classify(self.original, version.ORIGINAL_BLOB,
                             self.corrected, version.ORIGINAL_BLOB)
        with self.assertRaisesRegex(ValueError, "historical"):
            version.classify(self.original + b"x", version.ORIGINAL_BLOB,
                             self.corrected, version.CORRECTED_BLOB)

    def test_ranges_check_historical_and_exact_active_source(self):
        root = Path(__file__).resolve().parents[1]
        primary_text = (root / ranges.PRIMARY).read_text(encoding="utf-8")
        heading = "### C0 source review candidate: Book02 §02.3b"
        book02_section = heading + re.split(r"(?m)^#{1,3} ", primary_text.split(heading, 1)[1], maxsplit=1)[0]
        book1_path = "01_BOOKS/BOOK_01_FIXTURE.md"
        book1_heading = b"### 01.1.8 Fixture\n\n"
        book1 = book1_heading + b"independent fixture\n\n"
        book1_sha = hashlib.sha256(book1).hexdigest()
        fixture_commit = "c" * 40
        book1_section = ("### C0 source review candidate: Book01 §01.1.8\n\n"
            f"On snapshot `{fixture_commit}`, `{book1_path}` has Git blob `{version.git_blob(book1)}`. "
            f"The complete section is `[0,{len(book1)})`, SHA-256 `{book1_sha}`.\n\n"
            "| Byte range | Candidate disposition and existing support |\n| --- | --- |\n"
            f"| `[0,{len(book1_heading)})` | Heading and separator, structural context. |\n"
            f"| `[{len(book1_heading)},{len(book1)})` | Independent fixture. |\n\n")
        primary = (book1_section + book02_section).encode("utf-8")
        snapshot = "a" * 40
        fake_reader = SimpleNamespace(_require_repo_root=lambda repo: None, partition=reader.partition)

        def run(active):
            def objects(_reader, _repo, commit, path):
                if path == ranges.PRIMARY:
                    return "b" * 40, primary
                if path == book1_path:
                    return version.git_blob(book1), book1
                if path == version.PATH:
                    data = active if commit == snapshot else self.original
                    return version.git_blob(data), data
                raise AssertionError(path)
            with patch.object(ranges, "object_at", side_effect=objects):
                return ranges.verify(fake_reader, root, snapshot)

        for content, expected in ((self.original, "historical"), (self.corrected, "corrected")):
            with self.subTest(version=expected):
                result = run(content)
                item = next(x for x in result["candidates"] if x["title"] == "Book02 §02.3b")
                self.assertEqual(item["active_source_version"]["version"], expected)
                self.assertEqual(item["acceptance"], "not_assessed")
                if expected == "corrected":
                    mapped = item["active_source_version"]["mapped_candidate"]
                    self.assertEqual(mapped["section"]["end"], 15810)
                    self.assertEqual(mapped["semantic_classification"], "not_assessed")
        with self.assertRaisesRegex(ranges.VerificationError, "beyond the pinned"):
            run(self.corrected + b"hostile")

    def test_mapping_does_not_hide_internal_boundaries(self):
        self.assertEqual(version.translate_offset(version.OFFSET), version.OFFSET)
        self.assertEqual(version.translate_offset(version.OFFSET + len(version.ORIGINAL)),
                         version.OFFSET + len(version.CORRECTED))
        with self.assertRaisesRegex(ValueError, "inside"):
            version.translate_offset(version.OFFSET + 1)


if __name__ == "__main__":
    unittest.main()
