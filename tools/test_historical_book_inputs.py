#!/usr/bin/env python3
"""Tamper, restoration and isolation controls for original book-input replay."""
from pathlib import Path
import json
import shutil
import subprocess
import tempfile
import unittest

import historical_book_inputs as books
import native_checkpoint_inputs as native
import research_input_closure as closure


ROOT = Path(__file__).resolve().parents[1]
ENTRY = books.CERT + "a4d_book03_feedback_variation_check.py"


class HistoricalBookInputTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="d0-book-input-test-")
        self.addCleanup(self.temp.cleanup)
        self.parent = Path(self.temp.name)
        self.repo = self.parent / "repo"
        self.repo.mkdir()
        self.copy_files(books.BOOK_PATHS | books.SNAPSHOTS | books.ENTRYPOINTS |
                        books.RECEIPTS | {books.MANIFEST}, self.repo)
        self.git(self.repo, "init", "-q")
        self.git(self.repo, "config", "user.name", "Fixture")
        self.git(self.repo, "config", "user.email", "fixture@example.invalid")
        self.git(self.repo, "add", ".")
        self.git(self.repo, "commit", "-qm", "fixture")
        self.isolation_temp = tempfile.TemporaryDirectory(prefix="d0-research-cert-")
        self.addCleanup(self.isolation_temp.cleanup)
        self.isolation = Path(self.isolation_temp.name).resolve()
        self.tree = self.isolation / "tree"
        self.git(self.repo, "worktree", "add", "--detach", str(self.tree), "HEAD")
        self.binding, self.prepared = books.validate(self.tree, ENTRY)
        # The fixture always has genuinely revised prose, independently of the
        # source checkout's current editorial changes.
        for item in self.prepared:
            path = self.tree / item["path"]
            path.write_bytes(path.read_bytes() + b"\nEditorial revision fixture.\n")
        self.maintained = {item["path"]: (self.tree / item["path"]).read_bytes()
                           for item in self.prepared}

    @staticmethod
    def git(repo, *args):
        return subprocess.run(["git", "-C", str(repo), *args],
                              capture_output=True, check=True)

    @staticmethod
    def copy_files(paths, destination):
        for path in paths:
            target = destination / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, target)

    def apply(self, entry=ENTRY):
        return books.apply(self.tree, entry, isolation_parent=self.isolation)

    def assert_maintained(self):
        for path, content in self.maintained.items():
            self.assertEqual((self.tree / path).read_bytes(), content)

    def test_all_twenty_seven_exact_bindings_validate(self):
        self.assertEqual(len(books.ENTRYPOINTS), 27)
        for entry in sorted(books.ENTRYPOINTS):
            binding, prepared = books.validate(self.tree, entry)
            self.assertTrue(prepared)
            self.assertTrue(binding["book_pins"])

    def test_original_inputs_and_provenance_then_lossless_restore(self):
        overlay = self.apply()
        self.assertEqual(overlay.provenance["mode"], books.SCOPE)
        self.assertFalse(overlay.provenance["current_book_prose_certified"])
        for item in self.prepared:
            self.assertEqual((self.tree / item["path"]).read_bytes(), item["snapshot"])
        self.assertFalse(overlay.restore())
        self.assert_maintained()

    def test_modified_snapshot_fails_before_any_overlay(self):
        path = self.tree / self.prepared[0]["snapshot_path"]
        path.write_bytes(path.read_bytes() + b"tampered")
        with self.assertRaisesRegex(ValueError, "snapshot hash/blob mismatch"):
            self.apply()
        self.assert_maintained()

    def test_missing_snapshot_fails_before_any_overlay(self):
        (self.tree / self.prepared[0]["snapshot_path"]).unlink()
        with self.assertRaisesRegex(ValueError, "missing or outside"):
            self.apply()
        self.assert_maintained()

    def test_modified_checker_is_not_granted_old_inputs(self):
        path = self.tree / ENTRY
        path.write_bytes(path.read_bytes() + b"\n# new checker\n")
        with self.assertRaisesRegex(ValueError, "checker binding mismatch"):
            self.apply()
        self.assert_maintained()

    def test_modified_receipt_is_rejected(self):
        path = self.tree / self.binding["receipt"]
        path.write_bytes(path.read_bytes() + b" ")
        with self.assertRaisesRegex(ValueError, "receipt binding mismatch"):
            self.apply()
        self.assert_maintained()

    def test_modified_manifest_is_rejected(self):
        path = self.tree / books.MANIFEST
        data = json.loads(path.read_text())
        data["scope"] = "CURRENT_BOOK_PROOF"
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "manifest hash mismatch"):
            self.apply()

    def test_unregistered_consumer_gets_no_overlay(self):
        self.assertIsNone(self.apply(books.CERT + "new_checker.py"))
        self.assert_maintained()

    def test_earlier_revision_without_manifest_keeps_normal_inputs(self):
        (self.tree / books.MANIFEST).unlink()
        self.assertIsNone(self.apply())
        self.assert_maintained()

    def test_execution_mutation_is_reported_and_not_overwritten(self):
        overlay = self.apply()
        target = self.tree / self.prepared[0]["path"]
        target.write_bytes(b"modified during execution")
        self.assertTrue(overlay.restore())
        self.assertEqual(target.read_bytes(), b"modified during execution")
        other = self.prepared[1]["path"]
        self.assertEqual((self.tree / other).read_bytes(), self.maintained[other])

    def test_symlink_substitution_does_not_write_outside_tree(self):
        overlay = self.apply()
        outside = self.parent / "outside.md"
        outside.write_bytes(b"untouched")
        target = self.tree / self.prepared[0]["path"]
        target.unlink()
        target.symlink_to(outside)
        self.assertTrue(overlay.restore())
        self.assertEqual(outside.read_bytes(), b"untouched")

    def test_nonisolated_primary_checkout_is_rejected(self):
        with self.assertRaises(ValueError):
            books.apply(self.repo, ENTRY, isolation_parent=self.parent)

    def test_incorrect_isolation_parent_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "isolated worktree"):
            books.apply(self.tree, ENTRY, isolation_parent=self.parent)

    def test_attached_worktree_in_runner_layout_is_rejected(self):
        self.git(self.tree, "switch", "-c", "attached-fixture")
        with self.assertRaisesRegex(ValueError, "detached HEAD"):
            self.apply()
        self.assert_maintained()

    def test_linked_worktrees_outside_runner_temp_layout_are_rejected(self):
        layouts = (
            (self.parent / "d0-research-cert-nested", "tree"),
            (self.parent, "tree"),
            (self.isolation, "not-tree"),
        )
        for parent, name in layouts:
            with self.subTest(parent=parent.name, name=name):
                parent.mkdir(exist_ok=True)
                tree = parent / name
                self.git(self.repo, "worktree", "add", "--detach", str(tree), "HEAD")
                before = {path: (tree / path).read_bytes() for path in books.BOOK_PATHS}
                with self.assertRaisesRegex(ValueError, "isolated worktree"):
                    books.apply(tree, ENTRY, isolation_parent=parent)
                self.assertEqual(before, {path: (tree / path).read_bytes()
                                          for path in books.BOOK_PATHS})

    def test_imported_helper_change_selects_all_bound_book_consumers(self):
        # A helper-only change must select these named consumers even when
        # their source imports do not expose the runner's overlay dependency.
        repo = self.parent / "selection-repo"
        repo.mkdir()
        self.git(repo, "init", "-q")
        self.git(repo, "config", "user.name", "Fixture")
        self.git(repo, "config", "user.email", "fixture@example.invalid")
        unrelated = books.CERT + "unrelated_check.py"
        for entry in books.ENTRYPOINTS | {unrelated}:
            path = repo / entry
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("PASS = True\n", encoding="utf-8")
        dependency = repo / "tools/native_pairing_refinement_inputs.py"
        dependency.parent.mkdir()
        dependency.write_text("VALUE = 1\n", encoding="utf-8")
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-qm", "selection fixture")
        base = self.git(repo, "rev-parse", "HEAD").stdout.decode().strip()
        dependency.write_text("VALUE = 2\n", encoding="utf-8")
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-qm", "helper-only change")
        head = self.git(repo, "rev-parse", "HEAD").stdout.decode().strip()
        report = closure.select(repo, head, base)
        self.assertEqual(report["changed"], ["tools/native_pairing_refinement_inputs.py"])
        selected = {item["certificate"]: item["reasons"] for item in report["selected"]}
        self.assertEqual(set(selected), books.ENTRYPOINTS)
        self.assertTrue(all(reasons == ["historical-book-input-binding"]
                            for reasons in selected.values()))
        self.assertIn(unrelated, report["unselected"])

    def test_composes_with_existing_native_checkpoint_overlay(self):
        # Exercise the real prior binding and its unchanged receipts; only
        # inputs are validated/restored here, no scientific computation runs.
        self.copy_files(native.ENTRYPOINTS | native.RECEIPTS | native.CAPSULES |
                        native.REPORT_ENTRYPOINTS | native.REPORT_RECEIPTS |
                        {native.MANIFEST, native.TARGET, native.SNAPSHOT,
                         native.REPORT_TARGET, native.REPORT_SNAPSHOT}, self.tree)
        entry = books.CERT + "a4d_native_code_price_resolution_check.py"
        old_source = (self.tree / native.TARGET).read_bytes()
        prior = native.apply(self.tree, entry)
        overlay = self.apply(entry)
        self.assertIsNotNone(prior)
        self.assertIsNotNone(overlay)
        self.assertFalse(overlay.restore())
        self.assertFalse(prior.restore())
        self.assertEqual((self.tree / native.TARGET).read_bytes(), old_source)
        self.assert_maintained()


if __name__ == "__main__":
    unittest.main()
