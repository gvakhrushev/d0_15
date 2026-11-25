"""Controls for pinned book replay isolation and input corruption."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest

import historical_book_inputs as binding


class HistoricalBookInputsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source = Path(__file__).resolve().parents[1]
        self.manifest = json.loads((source / binding.MANIFEST).read_text())
        self.entry = next(iter(self.manifest["entrypoints_sha256"]))
        paths = [binding.MANIFEST, self.entry]
        for name, spec in self.manifest["books"].items():
            paths.extend((name, spec["snapshot"]))
        for name in paths:
            dest = self.root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / name, dest)
        self.book = next(iter(self.manifest["books"]))
        (self.root / self.book).write_text("edited current book")

    def test_scope_restore_and_mutation_detection(self):
        self.assertIsNone(binding.apply(self.root, "unrelated.py"))
        overlay = binding.apply(self.root, self.entry)
        self.assertEqual(binding.digest((self.root / self.book).read_bytes()),
                         self.manifest["books"][self.book]["sha256"])
        self.assertFalse(overlay.restore())
        self.assertEqual((self.root / self.book).read_text(), "edited current book")
        overlay = binding.apply(self.root, self.entry)
        (self.root / self.book).write_text("unexpected mutation")
        self.assertTrue(overlay.restore())

    def test_rejects_tampered_snapshot_and_checker(self):
        snapshot = self.root / self.manifest["books"][self.book]["snapshot"]
        snapshot.write_text("tampered")
        with self.assertRaisesRegex(ValueError, "snapshot hash mismatch"):
            binding.apply(self.root, self.entry)
        (self.root / self.entry).write_text("tampered")
        with self.assertRaisesRegex(ValueError, "checker hash mismatch"):
            binding.apply(self.root, self.entry)


if __name__ == "__main__":
    unittest.main()
