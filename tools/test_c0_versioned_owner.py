"""Fail-closed controls for a versioned C0 Lean owner and its inventory."""
from dataclasses import replace
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from tools import c0_reconciliation as c0
from tools.test_c0_reconciliation import KernelSectionFixture


class VersionedOwnerTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="d0-c0-versioned-owner-")
        self.addCleanup(temp.cleanup)
        self.repo = KernelSectionFixture(temp.name)
        self.historical_snapshot = self.repo.snapshot
        self.old = self.repo.pins.module_blob
        self.historical_inventory_sha = hashlib.sha256(
            (self.repo.root / self.repo.inventory_path).read_bytes()).hexdigest()
        self.repo.write(self.repo.module_path, "-- reviewed proof-only fixture\n")
        self.active_snapshot = self.repo.commit("proof-only owner")
        self.new = self.repo.git("rev-parse", f"{self.active_snapshot}:{self.repo.module_path}")
        key = (self.repo.module, self.repo.module_path, self.old)
        policy = mock.patch.dict(c0.VERSIONED_OWNER_BLOBS, {key: frozenset((self.old, self.new))})
        policy.start()
        self.addCleanup(policy.stop)
        self.repo.inventory["snapshot_commit"] = self.active_snapshot
        self.final = self.repo.update_inventory(lambda inv: None)

    def issue(self, ref, check, fragment):
        view = self.repo.view(ref)
        self.assertEqual(view["checks"][check]["state"], "unresolved")
        self.assertIn(fragment, view["checks"][check]["reason"])
        self.assertEqual(view["scope"]["c0_acceptance_assessment"], "not_evaluated")
        return view

    def test_exact_production_version_policy(self):
        key = ("D0.Foundation.FutureShortlexAdapter",
               "03_FORMALIZATION/D0/Foundation/FutureShortlexAdapter.lean",
               "a4a390673994ecbe7529ebae636ddd3fd6e2db7d")
        self.assertEqual(c0.VERSIONED_OWNER_BLOBS[key], frozenset((key[2],
            "b4ec8b60a52aaa1bb3e5b1fcc40b57ba1087d43b")))

    def test_old_and_exact_active_owner_with_matching_inventory(self):
        historic = self.repo.view(self.historical_snapshot, expected_sha=self.historical_inventory_sha)
        self.assertEqual(historic["issues"], [])
        h = historic["authority"]["source"]["owner_modules"][0]
        self.assertEqual((h["historical_blob"], h["active_blob"]), (self.old, self.old))
        view = self.repo.view(self.final)
        self.assertEqual(view["issues"], [])
        owner = view["authority"]["source"]["owner_modules"][0]
        self.assertEqual((owner["historical_blob"], owner["active_blob"]), (self.old, self.new))
        self.assertEqual(view["scope"]["c0_acceptance_assessment"], "not_evaluated")
        self.assertEqual(view["scope"]["running_reconciliation_helper"],
                         "current_runtime_not_authenticated_against_selected_snapshot")
        self.assertEqual(view["units"][0]["semantic_acceptance"], "pending_independent_review")

    def test_third_owner_blob_fails_closed(self):
        self.repo.write(self.repo.module_path, "-- unreviewed third version\n")
        self.issue(self.repo.commit("third owner"), "source_and_primary", "pinned reviewed module")

    def test_wrong_historical_pin_fails_even_if_primary_is_rehashed(self):
        primary = Path(self.repo.root / c0.PRIMARY).read_text()
        bad = "f" * 40
        primary = primary.replace(self.old, bad, 1)
        self.repo.write(c0.PRIMARY, primary)
        section = primary.split("### ", 1)[1].split("\n\n### ", 1)[0]
        self.repo.pins = replace(self.repo.pins, module_blob=bad,
                                 primary_sha256=c0.primary_section_sha256(section))
        self.issue(self.repo.commit("false old pin"), "source_and_primary", "historical source differs")

    def test_stale_inventory_cannot_follow_new_owner(self):
        self.repo.inventory["snapshot_commit"] = self.repo.source_commit
        ref = self.repo.update_inventory(lambda inv: None)
        self.issue(ref, "compiled_inventory", "no longer matches tracked Lean inputs")

    def test_active_blob_missing_or_different_fails_closed(self):
        (self.repo.root / self.repo.module_path).unlink()
        self.issue(self.repo.commit("missing active owner"), "source_and_primary", "expected one, found 0")

    def test_missing_proof_metadata_remains_unresolved(self):
        ref = self.repo.update_inventory(lambda inv: inv["declarations"][0].pop("proof_dependencies"))
        self.issue(ref, "compiled_inventory", "lacks complete proof metadata")


if __name__ == "__main__":
    unittest.main()
