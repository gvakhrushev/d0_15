#!/usr/bin/env python3
"""Isolated Git-fixture tests: no active checkout, network, or Lake writes."""

import csv
from dataclasses import replace
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import c0_reconciliation as c0
from tools import lean_declaration_inventory as inventory_tool


class RepositoryFixture:
    def __init__(self, directory):
        self.root = Path(directory)
        self.git("init", "-q")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Fixture")
        self.source_path = c0.SOURCE_DIR + "A4D_NATIVE_COCHAIN_REFINEMENT.md"
        self.inventory_path = c0.SOURCE_DIR + "sources/test/pilot_inventory.json"
        self.lean_digest = "1" * 64
        self.write(self.source_path,
                   "# Source\n\nTask: existing scientific owner, Draft #310.\n\n"
                   "## 5. One-step estimates and composed fixed-torus failure\n"
                   "Actual fixture source, not a scientific result.\n")
        self.write(c0.LEAN_PATH, "-- fixed fixture Lean source\n")
        self.source_commit = self.commit("source")
        self.source_blob = self.git("rev-parse", f"{self.source_commit}:{self.source_path}")
        inventory = {
            "schema": "d0-lean-declaration-inventory-v1",
            "snapshot_commit": self.source_commit,
            "worktree_dirty": False,
            "public_import_root": "D0.All",
            "inventory_mode": "owning_module_enumeration",
            "lean_source_digest": self.lean_digest,
            "toolchain": "fixture",
            "declarations": [{"name": c0.DECLARATION, "exists": True,
                              "internal_name": False, "declaration_kind": "theorem",
                              "module": c0.MODULE, "source_path": c0.LEAN_PATH,
                              "elaborated_type": c0.EXPECTED_TYPE,
                              "axioms": ["propext"]}],
        }
        self.write_inventory(inventory)
        buf = io.StringIO(newline="")
        writer = csv.DictWriter(buf, fieldnames=["lean_module", "lean_file", "role", "referenced_by"])
        writer.writeheader()
        writer.writerow({"lean_module": c0.MODULE,
                         "lean_file": c0.LEAN_PATH.removeprefix("03_FORMALIZATION/"),
                         "role": "EXPLICIT_SUPPORT", "referenced_by": self.source_path})
        self.write(c0.SUPPORT, buf.getvalue())
        self.write_graph({"nodes": [{"id": c0.CONSUMER, "scope": "fixture",
                                    "status": "fixture", "owners": [self.source_path +
                                    "#5-one-step-estimates-and-composed-fixed-torus-failure"]}]})
        self.write_primary(self.source_blob)
        self.snapshot = self.commit("pilot metadata")
        primary_text = (self.root / c0.PRIMARY).read_text(encoding="utf-8")
        self.pins = c0.PilotPins(
            primary_blob=self.git("rev-parse", f"{self.snapshot}:{c0.PRIMARY}"),
            primary_section_sha256=c0.primary_section_sha256(c0.primary_section(primary_text)),
            source_commit=self.source_commit, source_path=self.source_path,
            source_blob=self.source_blob, source_owner="310",
            source_heading="5. One-step estimates and composed fixed-torus failure",
            consumer_graph_blob=self.git("rev-parse", f"{self.snapshot}:{c0.GRAPH}"),
            consumer_scope="fixture", consumer_status="fixture",
            inventory_path=self.inventory_path,
            inventory_blob=self.git("rev-parse", f"{self.snapshot}:{self.inventory_path}"),
            inventory_sha256=hashlib.sha256((self.root / self.inventory_path).read_bytes()).hexdigest(),
            inventory_snapshot=self.source_commit,
            module_blob=self.git("rev-parse", f"{self.source_commit}:{c0.LEAN_PATH}"))

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode().strip()

    def write(self, path, value):
        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        # Keep fixtures runnable under the repository's older local Python
        # while preserving the same explicit LF bytes as the newer CI runtime.
        with p.open("w", encoding="utf-8", newline="\n") as stream:
            stream.write(value)

    def write_graph(self, graph):
        self.write(c0.GRAPH, json.dumps({"schema": "d0-native-gravity-dependencies/1", **graph}))

    def write_inventory(self, inventory):
        self.write(self.inventory_path, json.dumps(inventory))

    def write_primary(self, expected_source_blob, owner="310", extra=""):
        sha = hashlib.sha256((self.root / self.inventory_path).read_bytes()).hexdigest()
        rel = self.inventory_path.removeprefix(c0.SOURCE_DIR)
        self.write(c0.PRIMARY,
            f"# Primary\n\n### {c0.TARGET_HEADING}\n\n"
            f"The input is §5 of #{owner}'s `A4D_NATIVE_COCHAIN_REFINEMENT.md` at commit\n"
            f"`{self.source_commit}`, blob\n`{expected_source_blob}`. Independent mathematical review\n"
            f"checked the fixture. Its consumer is the existing `{c0.CONSUMER}` scoped obstruction.\n"
            f"Lake jobs at Lean source digest\n`{self.lean_digest}`.\n"
            f"The [compiled declaration inventory]({rel}) records this fixture.\n"
            f"Its SHA-256 is `{sha}`.\n{extra}\n")

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)
        return self.git("rev-parse", "HEAD")


class ReconciliationFixtureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="d0-c0-fixture-")
        self.addCleanup(self.tmp.cleanup)
        self.repo = RepositoryFixture(self.tmp.name)

    def pins_for(self, ref, **kwargs):
        # Fixtures may repin a primary/inventory solely to exercise a deeper
        # structural check. Production CLI always uses immutable DEFAULT_PINS.
        g = c0.GitSnapshot(self.repo.root, ref)
        if "consumer_graph_blob" not in kwargs:
            kwargs["consumer_graph_blob"] = g.blob(ref, c0.GRAPH)
        section = c0.primary_section(g.data(ref, c0.PRIMARY).decode("utf-8"))
        return replace(self.repo.pins,
                       primary_blob=g.blob(ref, c0.PRIMARY),
                       primary_section_sha256=c0.primary_section_sha256(section),
                       **kwargs)

    def inventory_pins(self, ref, **kwargs):
        g = c0.GitSnapshot(self.repo.root, ref)
        blob = g.blob(ref, self.repo.inventory_path)
        digest = hashlib.sha256(g.data(ref, self.repo.inventory_path)).hexdigest()
        return self.pins_for(ref, inventory_blob=blob, inventory_sha256=digest, **kwargs)

    def check_unresolved(self, ref, component, message, **kwargs):
        pins = kwargs.pop("pins", None) or self.pins_for(ref, **kwargs)
        view = c0.reconcile(self.repo.root, ref, pins=pins)
        self.assertEqual(view["pilot"]["state"], "unresolved")
        self.assertEqual(view["checks"][component]["state"], "unresolved")
        self.assertIn(message, view["checks"][component]["reason"])
        self.assertEqual(view["scope"]["c0_acceptance_assessment"], "not_evaluated")
        self.assertTrue(view["scope"]["this_view_does_not_freeze_or_accept"])
        self.assertEqual(view["scope"]["all_other_c0_candidates"], "not_enumerated_unresolved")

    def test_clean_linked_fixture_never_accepts_c0(self):
        view = c0.reconcile(self.repo.root, self.repo.snapshot, pins=self.repo.pins)
        self.assertEqual(view["pilot"]["state"], "reported_metadata_links_consistent_not_c0_acceptance")
        self.assertEqual(view["pilot"]["source"]["blob"], self.repo.source_blob)
        self.assertEqual(view["pilot"]["consumer"]["id"], c0.CONSUMER)
        self.assertEqual(view["pilot"]["compiled_inventory"]["declaration"], c0.DECLARATION)
        self.assertFalse(view["scope"]["coverage_reported"])
        self.assertEqual(view["pilot"]["independent_review"], "not_authenticated")
        self.assertEqual(view["pilot"]["semantic_correspondence"], "not_automatically_checked")
        self.assertEqual(view["pilot"]["consumer_binding_semantics"], "unresolved")

    def test_architecture_cli_reports_unresolved_fixture(self):
        cli = Path(__file__).with_name("proof_architecture.py")
        proc = subprocess.run([sys.executable, str(cli), "--repo-root", str(self.repo.root),
                               "--json", "c0-pilot", "--snapshot", self.repo.snapshot],
                              capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 1, proc.stderr)
        view = json.loads(proc.stdout)
        self.assertEqual(view["pilot"]["state"], "unresolved")
        self.assertEqual(view["scope"]["c0_acceptance_assessment"], "not_evaluated")

    def test_wrong_pinned_blob_is_unresolved(self):
        self.repo.write_primary("a" * 40)
        self.check_unresolved(self.repo.commit("wrong blob"), "source_pin_and_owner", "blob mismatch", source_blob="a" * 40)

    def test_missing_source_locator_is_unresolved(self):
        text = (self.repo.root / c0.PRIMARY).read_text(encoding="utf-8")
        self.repo.write(c0.PRIMARY, text.replace("§5 of #310", "source #310"))
        self.check_unresolved(self.repo.commit("missing locator"), "source_primary_link", "source locator")

    def test_missing_scientific_owner_is_unresolved(self):
        self.repo.write_primary(self.repo.source_blob, owner="311")
        self.check_unresolved(self.repo.commit("wrong owner"), "source_pin_and_owner", "owner not present", source_owner="311")

    def test_missing_consumer_is_unresolved(self):
        self.repo.write_graph({"nodes": []})
        self.check_unresolved(self.repo.commit("missing consumer"), "consumer_and_source_owner", "consumer node")

    def test_missing_consumer_owner_edge_is_unresolved(self):
        self.repo.write_graph({"nodes": [{"id": c0.CONSUMER, "owners": []}]})
        self.check_unresolved(self.repo.commit("missing owner edge"), "consumer_and_source_owner", "consumer source owner")

    def test_ambiguous_source_locator_is_unresolved(self):
        duplicate = (f"§5 of #310's `A4D_NATIVE_COCHAIN_REFINEMENT.md` at commit "
                     f"`{self.repo.source_commit}`, blob `{self.repo.source_blob}`.")
        self.repo.write_primary(self.repo.source_blob, extra=duplicate)
        self.check_unresolved(self.repo.commit("ambiguous source"), "source_primary_link", "found 2")

    def test_missing_compiled_inventory_is_unresolved(self):
        (self.repo.root / self.repo.inventory_path).unlink()
        self.check_unresolved(self.repo.commit("missing inventory"), "compiled_declaration_inventory", "tracked path")

    def test_missing_declaration_is_unresolved(self):
        p = self.repo.root / self.repo.inventory_path
        inv = json.loads(p.read_text(encoding="utf-8"))
        inv["declarations"] = []
        self.repo.write_inventory(inv)
        self.repo.write_primary(self.repo.source_blob)
        ref = self.repo.commit("missing declaration")
        self.check_unresolved(ref, "compiled_declaration_inventory", "compiled declaration", pins=self.inventory_pins(ref))

    def test_wrong_inventory_digest_is_unresolved(self):
        p = self.repo.root / self.repo.inventory_path
        p.write_bytes(p.read_bytes() + b" ")
        self.check_unresolved(self.repo.commit("changed inventory"), "compiled_declaration_inventory", "inventory blob differs")

    def test_ambiguous_compiled_declaration_is_unresolved(self):
        p = self.repo.root / self.repo.inventory_path
        inv = json.loads(p.read_text(encoding="utf-8"))
        inv["declarations"].append(dict(inv["declarations"][0]))
        self.repo.write_inventory(inv)
        self.repo.write_primary(self.repo.source_blob)
        ref = self.repo.commit("ambiguous declaration")
        self.check_unresolved(ref, "compiled_declaration_inventory", "found 2", pins=self.inventory_pins(ref))

    def test_sorry_axiom_cannot_be_classified_as_linked(self):
        p = self.repo.root / self.repo.inventory_path
        inv = json.loads(p.read_text(encoding="utf-8"))
        inv["declarations"][0]["axioms"].append("sorryAx")
        self.repo.write_inventory(inv)
        self.repo.write_primary(self.repo.source_blob)
        ref = self.repo.commit("sorry dependency")
        self.check_unresolved(ref, "compiled_declaration_inventory", "sorryAx", pins=self.inventory_pins(ref))

    def test_changed_lean_source_is_unresolved(self):
        self.repo.write(c0.LEAN_PATH, "-- altered fixture Lean source\n")
        self.check_unresolved(self.repo.commit("changed Lean"), "compiled_declaration_inventory", "no longer matches")

    def symlink_fixture(self, target="../../02_REGISTRY/fixture-source.lean"):
        # Create the Git symlink as an index entry: Windows need not grant the
        # process permission to create host-filesystem symlinks.
        target_path = "02_REGISTRY/fixture-source.lean"
        link_path = "03_FORMALIZATION/D0/fixture-link.lean"
        self.repo.write(target_path, "-- tracked external source\n")
        self.repo.git("add", "--", target_path)
        self.repo.write("link-object.txt", target)
        oid = self.repo.git("hash-object", "-w", "link-object.txt")
        self.repo.git("update-index", "--add", "--cacheinfo", f"120000,{oid},{link_path}")
        self.repo.git("commit", "-q", "-m", "source symlink")
        old = self.repo.git("rev-parse", "HEAD")
        p = self.repo.root / self.repo.inventory_path
        inv = json.loads(p.read_text(encoding="utf-8"))
        inv["snapshot_commit"] = old
        self.repo.write_inventory(inv)
        self.repo.write_primary(self.repo.source_blob)
        self.repo.git("add", "--", self.repo.inventory_path, c0.PRIMARY)
        self.repo.git("commit", "-q", "-m", "inventory metadata")
        ref = self.repo.git("rev-parse", "HEAD")
        pins = self.inventory_pins(ref, inventory_snapshot=old)
        return old, ref, pins, target_path, link_path

    def test_external_symlink_target_change_invalidates_inventory(self):
        old, ref, pins, target, _ = self.symlink_fixture()
        view = c0.reconcile(self.repo.root, ref, pins=pins)
        self.assertEqual(view["checks"]["compiled_declaration_inventory"]["state"],
                         "reported_metadata_links_consistent_not_replayed")
        self.repo.write(target, "-- changed external source\n")
        self.repo.git("add", "--", target)
        self.repo.git("commit", "-q", "-m", "change only symlink target")
        changed = self.repo.git("rev-parse", "HEAD")
        git = c0.GitSnapshot(self.repo.root, changed)
        self.assertEqual(git.object_at(old, "03_FORMALIZATION"),
                         git.object_at(changed, "03_FORMALIZATION"))
        self.check_unresolved(changed, "compiled_declaration_inventory", "no longer matches", pins=pins)

    def test_external_symlink_target_mode_change_invalidates_inventory(self):
        old, ref, pins, target, _ = self.symlink_fixture()
        oid = self.repo.git("rev-parse", f"{old}:{target}")
        self.repo.git("update-index", "--cacheinfo", f"100755,{oid},{target}")
        self.repo.git("commit", "-q", "-m", "change external source mode")
        changed = self.repo.git("rev-parse", "HEAD")
        self.check_unresolved(changed, "compiled_declaration_inventory", "no longer matches", pins=pins)

    def test_symlink_chain_checks_ultimate_target(self):
        _, _, _, target, _ = self.symlink_fixture()
        ultimate = "02_REGISTRY/ultimate.lean"
        self.repo.write(ultimate, "-- original ultimate target\n")
        self.repo.git("add", "--", ultimate)
        self.repo.write("chain-object.txt", "ultimate.lean")
        oid = self.repo.git("hash-object", "-w", "chain-object.txt")
        self.repo.git("update-index", "--cacheinfo", f"120000,{oid},{target}")
        self.repo.git("commit", "-q", "-m", "chain symlink")
        old = self.repo.git("rev-parse", "HEAD")
        self.repo.write(ultimate, "-- altered ultimate target\n")
        self.repo.git("add", "--", ultimate)
        self.repo.git("commit", "-q", "-m", "change ultimate")
        changed = self.repo.git("rev-parse", "HEAD")
        git = c0.GitSnapshot(self.repo.root, changed)
        self.assertEqual(git.object_at(old, "03_FORMALIZATION"),
                         git.object_at(changed, "03_FORMALIZATION"))
        self.assertTrue(git.unchanged_lean_inputs(old, old))
        self.assertFalse(git.unchanged_lean_inputs(old, changed))

    def test_untracked_symlink_target_is_unresolved(self):
        _, ref, pins, target, _ = self.symlink_fixture("../../02_REGISTRY/not-tracked.lean")
        self.repo.write("02_REGISTRY/not-tracked.lean", "-- untracked target\n")
        self.check_unresolved(ref, "compiled_declaration_inventory", "tracked path", pins=pins)

    def test_symlink_parent_after_named_component_is_unresolved(self):
        _, ref, pins, _, _ = self.symlink_fixture("some-symlink/../fixture-link.lean")
        self.check_unresolved(ref, "compiled_declaration_inventory", "ambiguous symlink target", pins=pins)

    def test_noncanonical_symlink_target_is_unresolved(self):
        targets = ("../../02_REGISTRY/fixture-source.lean/",
                   "../../02_REGISTRY/fixture-source.lean/.",
                   "../../02_REGISTRY//fixture-source.lean")
        for index, target in enumerate(targets):
            with self.subTest(target=target):
                if index == 0:
                    _, ref, pins, _, _ = self.symlink_fixture(target)
                    self.check_unresolved(ref, "compiled_declaration_inventory", "noncanonical symlink target", pins=pins)
                else:
                    with tempfile.TemporaryDirectory(prefix="d0-c0-noncanonical-") as directory:
                        other = RepositoryFixture(directory)
                        self.repo, previous = other, self.repo
                        try:
                            _, ref, pins, _, _ = self.symlink_fixture(target)
                            self.check_unresolved(ref, "compiled_declaration_inventory", "noncanonical symlink target", pins=pins)
                        finally:
                            self.repo = previous

    def test_symlink_escape_and_cycle_are_unresolved(self):
        _, ref, pins, _, _ = self.symlink_fixture("../../../../outside.lean")
        self.check_unresolved(ref, "compiled_declaration_inventory", "escapes repository", pins=pins)
        # A separate repository fixture supplies a self-referential link.
        with tempfile.TemporaryDirectory(prefix="d0-c0-cycle-") as directory:
            other = RepositoryFixture(directory)
            self.repo, previous = other, self.repo
            try:
                _, ref, pins, _, _ = self.symlink_fixture("fixture-link.lean")
                self.check_unresolved(ref, "compiled_declaration_inventory", "cyclic tracked symlink", pins=pins)
            finally:
                self.repo = previous

    def test_deleted_tracked_owner_is_not_rescued_by_untracked_shadow(self):
        path = self.repo.root / self.repo.source_path
        contents = path.read_text(encoding="utf-8")
        path.unlink()
        ref = self.repo.commit("delete source owner")
        self.repo.write(self.repo.source_path, contents)  # deliberately untracked
        self.check_unresolved(ref, "source_pin_and_owner", "tracked path")

    def test_changed_source_owner_in_snapshot_is_unresolved(self):
        self.repo.write(self.repo.source_path, "# Changed owner\n")
        self.check_unresolved(self.repo.commit("changed source owner"), "source_pin_and_owner", "changed in selected snapshot")

    def test_anchor_prefix_or_suffix_is_not_accepted(self):
        node = {"id": c0.CONSUMER, "owners": [self.repo.source_path + "#" + c0.SOURCE_ANCHOR + "-different"]}
        self.repo.write_graph({"nodes": [node]})
        self.check_unresolved(self.repo.commit("wrong anchor"), "consumer_and_source_owner", "not exact")

    def test_formal_support_requires_explicit_support_role(self):
        path = self.repo.root / c0.SUPPORT
        text = path.read_text(encoding="utf-8").replace("EXPLICIT_SUPPORT", "REFERENCE_ONLY")
        self.repo.write(c0.SUPPORT, text)
        self.check_unresolved(self.repo.commit("wrong role"), "formal_support", "role is not EXPLICIT_SUPPORT")

    def test_wrong_elaborated_type_is_unresolved(self):
        p = self.repo.root / self.repo.inventory_path
        inv = json.loads(p.read_text(encoding="utf-8"))
        inv["declarations"][0]["elaborated_type"] = "True"
        self.repo.write_inventory(inv)
        self.repo.write_primary(self.repo.source_blob)
        ref = self.repo.commit("wrong elaborated type")
        self.check_unresolved(ref, "compiled_declaration_inventory", "expected exact signature", pins=self.inventory_pins(ref))

    def test_null_axiom_is_unresolved(self):
        p = self.repo.root / self.repo.inventory_path
        inv = json.loads(p.read_text(encoding="utf-8"))
        inv["declarations"][0]["axioms"] = [None]
        self.repo.write_inventory(inv)
        self.repo.write_primary(self.repo.source_blob)
        ref = self.repo.commit("null axiom")
        self.check_unresolved(ref, "compiled_declaration_inventory", "axioms must be", pins=self.inventory_pins(ref))

    def test_malformed_graph_node_is_unresolved(self):
        self.repo.write_graph({"nodes": [None]})
        self.check_unresolved(self.repo.commit("malformed graph"), "consumer_and_source_owner", "node must be an object")

    def test_wrong_graph_schema_is_unresolved(self):
        self.repo.write_graph({"schema": "wrong/1", "nodes": []})
        self.check_unresolved(self.repo.commit("wrong graph schema"), "consumer_and_source_owner", "graph schema")

    def test_malformed_graph_owners_is_unresolved(self):
        self.repo.write_graph({"nodes": [{"id": c0.CONSUMER, "owners": [None]}]})
        self.check_unresolved(self.repo.commit("malformed owners"), "consumer_and_source_owner", "owners must be a list of strings")

    def test_malformed_graph_node_id_is_unresolved(self):
        self.repo.write_graph({"nodes": [{"id": None}]})
        self.check_unresolved(self.repo.commit("malformed id"), "consumer_and_source_owner", "ids must be nonempty strings")

    def test_malformed_inventory_declaration_is_unresolved(self):
        p = self.repo.root / self.repo.inventory_path
        inv = json.loads(p.read_text(encoding="utf-8"))
        inv["declarations"].append(None)
        self.repo.write_inventory(inv)
        self.repo.write_primary(self.repo.source_blob)
        ref = self.repo.commit("malformed declaration")
        self.check_unresolved(ref, "compiled_declaration_inventory", "list of objects", pins=self.inventory_pins(ref))

    def test_null_declaration_name_is_unresolved(self):
        p = self.repo.root / self.repo.inventory_path
        inv = json.loads(p.read_text(encoding="utf-8"))
        inv["declarations"].append({"name": None})
        self.repo.write_inventory(inv)
        self.repo.write_primary(self.repo.source_blob)
        ref = self.repo.commit("null declaration name")
        self.check_unresolved(ref, "compiled_declaration_inventory", "names must be", pins=self.inventory_pins(ref))

    def test_source_snapshot_tree_oid_is_not_a_commit(self):
        tree_oid = self.repo.git("rev-parse", f"{self.repo.source_commit}^{{tree}}")
        self.repo.source_commit = tree_oid
        self.repo.write_primary(self.repo.source_blob)
        ref = self.repo.commit("tree as source snapshot")
        self.check_unresolved(ref, "source_pin_and_owner", "expected commit", source_commit=tree_oid)

    def test_inventory_snapshot_tree_oid_is_not_a_commit(self):
        tree_oid = self.repo.git("rev-parse", f"{self.repo.source_commit}^{{tree}}")
        p = self.repo.root / self.repo.inventory_path
        inv = json.loads(p.read_text(encoding="utf-8"))
        inv["snapshot_commit"] = tree_oid
        self.repo.write_inventory(inv)
        self.repo.write_primary(self.repo.source_blob)
        ref = self.repo.commit("tree as inventory snapshot")
        self.check_unresolved(ref, "compiled_declaration_inventory", "expected commit",
                              pins=self.inventory_pins(ref, inventory_snapshot=tree_oid))

    def test_git_replacement_cannot_hide_missing_consumer(self):
        self.repo.write_graph({"nodes": []})
        bad = self.repo.commit("bad consumer")
        self.repo.git("replace", bad, self.repo.snapshot)
        view = c0.reconcile(self.repo.root, bad, pins=self.repo.pins)
        self.assertEqual(view["pilot"]["state"], "unresolved")
        self.assertIn("consumer graph blob differs", view["checks"]["consumer_and_source_owner"]["reason"])

    def test_unrelated_document_extension_keeps_the_exact_pilot_section_binding(self):
        primary = self.repo.root / c0.PRIMARY
        primary.write_text(primary.read_text(encoding="utf-8") +
                           "\n### Unrelated later result\n\nNew source material.\n",
                           encoding="utf-8")
        ref = self.repo.commit("unrelated primary extension")
        view = c0.reconcile(self.repo.root, ref, pins=self.repo.pins)
        authority = view["authority"]["primary"]
        self.assertEqual(view["checks"]["primary_section"]["state"], "verified_raw_link")
        self.assertNotEqual(authority["blob"], authority["historical_document_blob"])
        self.assertFalse(authority["whole_file_matches_historical_blob"])
        self.assertEqual(authority["section_sha256"], self.repo.pins.primary_section_sha256)
        self.assertEqual(view["pilot"]["state"],
                         "reported_metadata_links_consistent_not_c0_acceptance")
        self.assertEqual(view["pilot"]["independent_review"], "not_authenticated")
        self.assertFalse(view["scope"]["coverage_reported"])
        self.assertEqual(view["scope"]["c0_acceptance_assessment"], "not_evaluated")

    def test_git_replacement_cannot_override_source_blob(self):
        self.repo.write("alternative.txt", "different source with no scientific owner\n")
        other = self.repo.git("hash-object", "-w", "alternative.txt")
        self.repo.git("replace", self.repo.source_blob, other)
        view = c0.reconcile(self.repo.root, self.repo.snapshot, pins=self.repo.pins)
        self.assertEqual(view["pilot"]["state"], "reported_metadata_links_consistent_not_c0_acceptance")
        self.assertEqual(view["pilot"]["source"]["blob"], self.repo.source_blob)

    def test_negative_review_text_cannot_become_automatic_acceptance(self):
        p = self.repo.root / c0.PRIMARY
        text = p.read_text(encoding="utf-8").replace("Independent mathematical review", "No Independent mathematical review")
        self.repo.write(c0.PRIMARY, text)
        ref = self.repo.commit("negative review text")
        # The exact selected section pin rejects changed content.
        self.check_unresolved(ref, "primary_section", "primary section digest differs", pins=self.repo.pins)
        # Even an explicitly repinned fixture reports the literal text only.
        view = c0.reconcile(self.repo.root, ref, pins=self.pins_for(ref))
        self.assertEqual(view["pilot"]["independent_review"], "not_authenticated")
        self.assertEqual(view["checks"]["primary_review_text"]["state"], "pinned_text_only_not_review_verification")

    def test_known_source_pin_cannot_be_replaced_by_same_content_other_commit(self):
        other = self.repo.snapshot
        self.repo.source_commit = other
        self.repo.write_primary(self.repo.source_blob)
        self.check_unresolved(self.repo.commit("different source commit"), "source_primary_link", "differs from exact pinned pilot")

    def test_unrelated_consumer_scope_and_rejected_status_are_unresolved(self):
        node = {"id": c0.CONSUMER, "scope": "unrelated application", "status": "REJECTED",
                "owners": [self.repo.source_path + "#" + c0.SOURCE_ANCHOR]}
        self.repo.write_graph({"nodes": [node]})
        ref = self.repo.commit("unrelated consumer scope")
        self.check_unresolved(ref, "consumer_and_source_owner", "consumer graph blob differs", pins=self.repo.pins)
        # Repinning only the synthetic graph exercises the node check too.
        self.check_unresolved(ref, "consumer_and_source_owner", "scope or status differs")

    def test_git_environment_redirects_and_config_are_ignored(self):
        with tempfile.TemporaryDirectory(prefix="d0-other-repo-") as other:
            other_repo = RepositoryFixture(other)
            bad_env = {"GIT_DIR": str(other_repo.root / ".git"),
                       "GIT_WORK_TREE": str(other_repo.root),
                       "GIT_COMMON_DIR": str(other_repo.root / ".git"),
                       "GIT_INDEX_FILE": str(other_repo.root / ".git" / "index"),
                       "GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "core.bare",
                       "GIT_CONFIG_VALUE_0": "true"}
            with mock.patch.dict(os.environ, bad_env):
                view = c0.reconcile(self.repo.root, self.repo.snapshot, pins=self.repo.pins)
            self.assertEqual(view["snapshot"], self.repo.snapshot)
            self.assertEqual(view["pilot"]["state"], "reported_metadata_links_consistent_not_c0_acceptance")

    def test_regular_git_worktree_file_is_supported(self):
        path = self.repo.root.parent / (self.repo.root.name + "-linked-worktree")
        self.repo.git("worktree", "add", "--detach", str(path), self.repo.snapshot)
        self.addCleanup(lambda: self.repo.git("worktree", "remove", "--force", str(path)))
        self.assertTrue((path / ".git").is_file())
        view = c0.reconcile(path, self.repo.snapshot, pins=self.repo.pins)
        self.assertEqual(view["pilot"]["state"], "reported_metadata_links_consistent_not_c0_acceptance")

    def test_subdirectory_is_not_silently_accepted_as_repo(self):
        view = c0.reconcile(self.repo.root / "02_REGISTRY", self.repo.snapshot, pins=self.repo.pins)
        self.assertEqual(view["pilot"]["state"], "unresolved")
        self.assertEqual(view["checks"]["snapshot"]["state"], "unresolved")

    def test_missing_git_is_unresolved(self):
        with mock.patch.object(c0.subprocess, "run", side_effect=FileNotFoundError("git")):
            view = c0.reconcile(self.repo.root, self.repo.snapshot, pins=self.repo.pins)
        self.assertEqual(view["checks"]["snapshot"]["state"], "unresolved")
        self.assertIn("Git executable unavailable", view["issues"][0]["reason"])

    def test_git_timeout_is_unresolved(self):
        with mock.patch.object(c0.subprocess, "run", side_effect=subprocess.TimeoutExpired("git", 30)):
            view = c0.reconcile(self.repo.root, self.repo.snapshot, pins=self.repo.pins)
        self.assertEqual(view["checks"]["snapshot"]["state"], "unresolved")
        self.assertIn("timed out", view["issues"][0]["reason"])

    def test_primary_mismatch_does_not_hide_stale_inventory_closure(self):
        self.repo.write(c0.PRIMARY, "# changed primary\n")
        self.repo.write(c0.LEAN_PATH, "-- changed Lean source\n")
        ref = self.repo.commit("changed primary and Lean")
        view = c0.reconcile(self.repo.root, ref, pins=self.repo.pins)
        self.assertEqual(view["checks"]["primary_section"]["state"], "unresolved")
        self.assertEqual(view["checks"]["source_primary_link"]["state"], "blocked_by_dependency")
        self.assertEqual(view["checks"]["primary_review_text"]["state"], "blocked_by_dependency")
        self.assertEqual(view["checks"]["compiled_declaration_inventory"]["state"], "unresolved")
        self.assertIn("no longer matches", view["checks"]["compiled_declaration_inventory"]["reason"])
        details = view["checks"]["compiled_declaration_inventory"]["details"]
        self.assertEqual(details["inventory_snapshot"], self.repo.source_commit)
        self.assertEqual(details["selected_snapshot"], ref)
        self.assertEqual(details["module_path"], c0.LEAN_PATH)
        self.assertEqual(details["changed_formalization_paths"], [c0.LEAN_PATH])
        self.assertNotEqual(details["inventory_module_blob"], details["selected_module_blob"])
        self.assertFalse(details["all_tracked_lean_inputs_unchanged"])
        self.assertEqual(details["selected_snapshot_declaration_inventory"], "not_rebuilt")
        self.assertTrue(details["diagnostic_only"])
        self.assertIn("unresolved or blocked", view["interpretation"])


class KernelSectionFixture:
    """A complete isolated source/primary/inventory/application chain."""

    def __init__(self, directory):
        self.root = Path(directory)
        self.git("init", "-q")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Fixture")
        self.source_path = "01_BOOKS/kernel.md"
        self.module_path = "03_FORMALIZATION/D0/Foundation/TheoryTransfer.lean"
        self.module = "D0.Foundation.TheoryTransfer"
        self.inventory_path = "02_REGISTRY/research/sources/test/kernel_inventory.json"
        self.applications_path = "02_REGISTRY/gr_assembly/applications.json"
        self.review_path = "02_REGISTRY/gr_assembly/reviews/kernel.md"
        self.write(self.source_path, "Source theorem\n")
        self.write(self.module_path, "-- fixture source\n")
        self.second_module = "D0.Foundation.FutureExecution"
        self.second_path = "03_FORMALIZATION/D0/Foundation/FutureExecution.lean"
        self.write(self.second_path, "-- second owner fixture source\n")
        self.write("03_FORMALIZATION/lean-toolchain", "fixture-toolchain\n")
        self.write("tools/lean_declaration_inventory.py", Path(inventory_tool.__file__).read_text())
        self.write(self.review_path, "Existing application review, not C0 acceptance.\n")
        self.source_commit = self.commit("source and prior review")
        self.source_blob = self.git("rev-parse", f"HEAD:{self.source_path}")
        module_blob = self.git("rev-parse", f"HEAD:{self.module_path}")
        raw = (self.root / self.source_path).read_bytes()
        self.section_sha = hashlib.sha256(raw).hexdigest()
        app = {"id": "existing-kernel-application", "consumer_location": "existing-consumer",
               "hypothesis_map": {"interpretation": {"target_hypothesis": "interpretation"}},
               "review": {"state": "accepted", "decision": {
                   "ref": self.source_commit, "path": self.review_path,
                   "sha256": hashlib.sha256((self.root / self.review_path).read_bytes()).hexdigest()}}}
        self.write(self.applications_path, json.dumps({"applications": [app]}))
        self.unit = {"atom": "Interpretation.run_commutes", "disposition": "conditional_theorem",
                     "source_range": [0, len(raw)], "hypotheses": "A supplied interpretation.",
                     "statement": "The fixture run diagram commutes.",
                     "declaration": self.module + ".Interpretation.run_commutes",
                     "declaration_kind": "theorem",
                     "type_sha256": hashlib.sha256(b"FixtureType").hexdigest()}
        payload = json.dumps({"schema": "d0-c0-kernel-unit-candidates/1", "units": [self.unit]}, indent=2)
        review_section = ("Fixture source review\n\n" + self.source_commit + "\n" +
                          self.source_blob + "\n" + self.section_sha + "\n" + app["id"] +
                          "\n" + module_blob)
        self.write(c0.PRIMARY, "# Primary\n\n### " + review_section +
                   "\n\n### C0 Book02 mathematical-unit candidates\n\n```json\n" + payload + "\n```\n")
        self.inventory = {"schema": "d0-lean-declaration-inventory-v1",
                          "snapshot_commit": self.source_commit, "worktree_dirty": False,
                          "public_import_root": "D0.All", "inventory_mode": "owning_module_enumeration",
                          "toolchain": "fixture-toolchain", "lean_source_digest": "1" * 64,
                          "requested_modules": [self.module], "module_prefix": None,
                          "collector_sha256": hashlib.sha256(inventory_tool.lean_module_collector(
                              [self.module], "D0.All").encode()).hexdigest(),
                          "declarations": [{"name": self.unit["declaration"], "exists": True,
                                            "internal_name": False, "module": self.module,
                                            "source_path": self.module_path, "declaration_kind": "theorem",
                                            "elaborated_type": "FixtureType", "axioms": ["propext"],
                                            "proof_details_status": "collected",
                                            "proof_dependencies": [], "type_dependencies": []}]}
        self.write(self.inventory_path, json.dumps(self.inventory))
        self.snapshot = self.commit("kernel metadata")
        self.pins = c0.KernelSectionPins(
            primary_heading="Fixture source review",
            primary_sha256=c0.primary_section_sha256(review_section),
            units_sha256=hashlib.sha256(payload.encode()).hexdigest(),
            source_commit=self.source_commit, source_path=self.source_path,
            source_blob=self.source_blob, section_range=(0, len(raw)), section_sha256=self.section_sha,
            module=self.module, module_path=self.module_path, module_blob=module_blob,
            application_id=app["id"], application_sha256=hashlib.sha256(
                json.dumps(app, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest())

    git = RepositoryFixture.git
    write = RepositoryFixture.write
    commit = RepositoryFixture.commit

    def view(self, ref=None, *, expected_sha=None):
        digest = expected_sha or hashlib.sha256((self.root / self.inventory_path).read_bytes()).hexdigest()
        return c0.reconcile_kernel_sections(self.root, ref or self.snapshot, pins=self.pins,
                                            inventory_path=self.inventory_path, inventory_sha256=digest)

    def update_inventory(self, callback):
        callback(self.inventory)
        self.write(self.inventory_path, json.dumps(self.inventory))
        return self.commit("changed inventory")

    def use_multiple_owners(self):
        """Schema-2 fixture whose second namespace deliberately differs from its owner."""
        self.unit["module"] = self.module
        second = dict(self.unit, atom="other_owner", declaration="D0.DifferentNamespace.run",
                      module=self.second_module)
        self.units = [self.unit, second]
        self.inventory["declarations"].append(dict(self.inventory["declarations"][0],
            name=second["declaration"], module=self.second_module, source_path=self.second_path))
        self.inventory["requested_modules"].append(self.second_module)
        self.inventory["collector_sha256"] = hashlib.sha256(inventory_tool.lean_module_collector(
            self.inventory["requested_modules"], "D0.All").encode()).hexdigest()
        blob = self.git("rev-parse", f"{self.source_commit}:{self.second_path}")
        self.pins = replace(self.pins, section_label="Book01 fixture", source_anchor="01.1.8",
                            units_heading="C0 Book01 mathematical-unit candidates",
                            require_unit_module=True, historical_inventory_path="",
                            additional_modules=((self.second_module, self.second_path, blob),))
        self.write(self.inventory_path, json.dumps(self.inventory))
        return self.write_multi_primary()

    def write_multi_primary(self):
        payload = json.dumps({"schema": "d0-c0-kernel-unit-candidates/2", "units": self.units})
        review = (self.pins.primary_heading + "\n\n" + self.source_commit + "\n" +
                  self.source_blob + "\n" + self.section_sha + "\n" + self.pins.application_id +
                  "\n" + self.pins.module_blob + "\n" + self.pins.additional_modules[0][2])
        self.write(c0.PRIMARY, "# Primary\n\n### " + review +
                   "\n\n### " + self.pins.units_heading + "\n\n```json\n" + payload + "\n```\n")
        self.pins = replace(self.pins, primary_sha256=c0.primary_section_sha256(review),
                            units_sha256=hashlib.sha256(payload.encode()).hexdigest())
        self.snapshot = self.commit("multiple pinned owners")
        return self.snapshot


class KernelSectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="d0-kernel-fixture-")
        self.addCleanup(self.tmp.cleanup)
        self.repo = KernelSectionFixture(self.tmp.name)

    def assert_issue(self, view, check, text):
        self.assertEqual(view["checks"][check]["state"], "unresolved")
        self.assertIn(text, view["checks"][check]["reason"])
        self.assertFalse(view["scope"]["coverage_reported"])
        self.assertEqual(view["scope"]["c0_acceptance_assessment"], "not_evaluated")

    def test_clean_kernel_slice_retains_acceptance_boundary(self):
        view = self.repo.view()
        self.assertEqual(view["issues"], [])
        self.assertEqual(len(view["units"]), 1)
        unit = view["units"][0]
        self.assertEqual(unit["semantic_acceptance"], "pending_independent_review")
        self.assertEqual(unit["classification_state"], "proposed_atomization_of_existing_review_ranges")
        self.assertEqual(unit["compiled_declaration"]["axioms"], ["propext"])
        self.assertEqual(unit["existing_application"], "existing-kernel-application")
        self.assertIn(self.repo.source_commit, unit["source_unit_key"])
        self.assertFalse(view["scope"]["coverage_reported"])
        self.assertIn("pending", view["scope"]["book01_01_1_8"])

    def test_primary_semantic_edit_cannot_silently_diverge(self):
        text = (self.repo.root / c0.PRIMARY).read_text().replace(
            "A supplied interpretation.", "No interpretation needed.")
        self.repo.write(c0.PRIMARY, text)
        view = self.repo.view(self.repo.commit("scope inflation"))
        self.assert_issue(view, "source_and_primary", "block digest mismatch")
        self.assertEqual(view["units"], [])

    def test_source_drift_is_not_formalized_by_same_lean_name(self):
        self.repo.write(self.repo.source_path, "Changed theorem\n")
        view = self.repo.view(self.repo.commit("source changed"))
        self.assert_issue(view, "source_and_primary", "source changed")
        self.assertEqual(view["units"], [])

    def test_wrong_inventory_digest_suppresses_compiled_evidence(self):
        view = self.repo.view(expected_sha="0" * 64)
        self.assert_issue(view, "compiled_inventory", "digest mismatch")
        self.assertIsNone(view["units"][0]["compiled_declaration"])

    def test_missing_declaration_does_not_become_coverage(self):
        ref = self.repo.update_inventory(lambda i: i.update(declarations=[]))
        self.assert_issue(self.repo.view(ref), "compiled_inventory", "expected one, found 0")

    def test_duplicate_declaration_fails_closed(self):
        ref = self.repo.update_inventory(lambda i: i["declarations"].append(dict(i["declarations"][0])))
        self.assert_issue(self.repo.view(ref), "compiled_inventory", "expected one, found 2")

    def test_signature_change_fails_after_repinning_inventory(self):
        ref = self.repo.update_inventory(lambda i: i["declarations"][0].update(elaborated_type="ChangedType"))
        self.assert_issue(self.repo.view(ref), "compiled_inventory", "signature mismatch")

    def test_axiom_and_missing_audit_fail_closed(self):
        for axioms in (["sorryAx"], ["UnreviewedAxiom"], None):
            with self.subTest(axioms=axioms):
                ref = self.repo.update_inventory(lambda i: i["declarations"][0].update(axioms=axioms))
                self.assert_issue(self.repo.view(ref), "compiled_inventory", "axiom")

    def test_dirty_inventory_is_not_current_compilation(self):
        ref = self.repo.update_inventory(lambda i: i.update(worktree_dirty=True))
        self.assert_issue(self.repo.view(ref), "compiled_inventory", "must be clean")

    def test_toolchain_mismatch_fails_closed(self):
        ref = self.repo.update_inventory(lambda i: i.update(toolchain="other-toolchain"))
        self.assert_issue(self.repo.view(ref), "compiled_inventory", "toolchain differs")

    def test_transitive_lean_input_change_invalidates_inventory(self):
        self.repo.write("03_FORMALIZATION/D0/Other.lean", "-- changed dependency\n")
        view = self.repo.view(self.repo.commit("new Lean input"))
        self.assert_issue(view, "compiled_inventory", "no longer matches tracked Lean inputs")

    def test_collector_change_invalidates_inventory(self):
        self.repo.write("tools/lean_declaration_inventory.py", "# changed collector\n")
        view = self.repo.view(self.repo.commit("collector changed"))
        self.assert_issue(view, "compiled_inventory", "collector changed")

    def test_application_drift_does_not_inherit_acceptance(self):
        obj = json.loads((self.repo.root / self.repo.applications_path).read_text())
        obj["applications"][0]["hypothesis_map"] = {}
        self.repo.write(self.repo.applications_path, json.dumps(obj))
        view = self.repo.view(self.repo.commit("application changed"))
        self.assert_issue(view, "existing_application", "record differs")
        self.assertIsNone(view["units"][0]["existing_application"])

    def test_parser_rejects_repeated_atom_even_with_matching_payload_pin(self):
        from tools.c0_kernel_units import parse_unit_candidates
        payload = json.dumps({"schema": "d0-c0-kernel-unit-candidates/1",
                              "units": [self.repo.unit, self.repo.unit]})
        text = "### C0 Book02 mathematical-unit candidates\n```json\n" + payload + "\n```\n"
        with self.assertRaisesRegex(ValueError, "duplicate kernel candidate atom"):
            parse_unit_candidates(text, hashlib.sha256(payload.encode()).hexdigest())

    def test_cli_rejects_unpaired_inventory_options(self):
        proc = subprocess.run([sys.executable, str(Path(c0.__file__)), "--repo", str(self.repo.root),
                               "--snapshot", self.repo.snapshot, "--kernel-sections",
                               "--kernel-inventory", self.repo.inventory_path],
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("must be supplied together", proc.stderr)

    def test_later_h2_json_is_outside_candidate_section(self):
        text = (self.repo.root / c0.PRIMARY).read_text()
        self.repo.write(c0.PRIMARY, text + '\n## Later unrelated report\n\n```json\n{}\n```\n')
        self.assertEqual(self.repo.view(self.repo.commit("later report"))["issues"], [])

    def test_second_json_block_inside_candidate_section_is_ambiguous(self):
        text = (self.repo.root / c0.PRIMARY).read_text()
        self.repo.write(c0.PRIMARY, text + '\n```json\n{}\n```\n')
        view = self.repo.view(self.repo.commit("second candidate block"))
        self.assert_issue(view, "source_and_primary", "exactly one primary kernel JSON block")

    def test_multiple_actual_owners_do_not_follow_namespace(self):
        self.repo.use_multiple_owners()
        view = self.repo.view()
        self.assertEqual(view["issues"], [])
        self.assertEqual(len(view["units"]), 2)
        self.assertEqual(view["units"][1]["module"], self.repo.second_module)
        self.assertIn("#01.1.8/", view["units"][1]["source_unit_key"])
        self.assertEqual(view["scope"]["sections"], ["Book01 fixture"])
        self.assertFalse(view["scope"]["coverage_reported"])

    def test_schema_two_requires_per_atom_owner(self):
        self.repo.use_multiple_owners()
        self.repo.units[1].pop("module")
        view = self.repo.view(self.repo.write_multi_primary())
        self.assert_issue(view, "source_and_primary", "candidate fields")

    def test_wrong_but_allowed_owner_does_not_inherit_another_declaration(self):
        self.repo.use_multiple_owners()
        self.repo.units[0]["module"] = self.repo.second_module
        view = self.repo.view(self.repo.write_multi_primary())
        self.assert_issue(view, "compiled_inventory", "metadata mismatch")
        self.assertIsNone(view["units"][0]["compiled_declaration"])

    def test_unpinned_owner_is_rejected_before_inventory(self):
        self.repo.use_multiple_owners()
        self.repo.units[1]["module"] = "D0.UnpinnedOwner"
        view = self.repo.view(self.repo.write_multi_primary())
        self.assert_issue(view, "source_and_primary", "unpinned owner")
        self.assertEqual(view["units"], [])

    def test_additional_owner_blob_mutation_invalidates_slice(self):
        self.repo.use_multiple_owners()
        self.repo.write(self.repo.second_path, "-- changed owner\n")
        view = self.repo.view(self.repo.commit("second owner changed"))
        self.assert_issue(view, "source_and_primary", "pinned reviewed module")
        self.assertEqual(view["units"], [])

    def test_missing_second_owner_declaration_fails_closed(self):
        self.repo.use_multiple_owners()
        ref = self.repo.update_inventory(lambda i: i["declarations"].pop())
        self.assert_issue(self.repo.view(ref), "compiled_inventory", "expected one, found 0")

    def test_wrong_candidate_section_cannot_be_substituted(self):
        self.repo.use_multiple_owners()
        self.repo.pins = replace(self.repo.pins, units_heading="C0 Book02 mathematical-unit candidates")
        self.assert_issue(self.repo.view(), "source_and_primary", "exactly one primary kernel candidate section")

    def test_multiple_owner_section_requires_clean_inventory_override(self):
        self.repo.use_multiple_owners()
        view = c0.reconcile_kernel_sections(self.repo.root, self.repo.snapshot, pins=self.repo.pins)
        self.assert_issue(view, "compiled_inventory", "requires a clean tracked inventory")

    def test_proof_details_and_dependency_lists_are_required(self):
        for change in ({"proof_details_status": "omitted"}, {"proof_dependencies": None},
                       {"type_dependencies": [""]}):
            with self.subTest(change=change):
                self.repo.inventory["declarations"][0].update(
                    proof_details_status="collected", proof_dependencies=[], type_dependencies=[])
                ref = self.repo.update_inventory(lambda i: i["declarations"][0].update(change))
                self.assert_issue(self.repo.view(ref), "compiled_inventory", "complete proof metadata")

    def test_reported_collector_digest_is_checked_against_generated_script(self):
        ref = self.repo.update_inventory(lambda i: i.update(collector_sha256="2" * 64))
        self.assert_issue(self.repo.view(ref), "compiled_inventory", "collector digest differs")

    def test_python_source_hash_is_not_a_lean_collector_hash(self):
        digest = hashlib.sha256(Path(inventory_tool.__file__).read_bytes()).hexdigest()
        ref = self.repo.update_inventory(lambda i: i.update(collector_sha256=digest))
        self.assert_issue(self.repo.view(ref), "compiled_inventory", "generated Lean collector")

    def test_bulk_omitted_proof_collector_is_not_full_proof_evidence(self):
        digest = hashlib.sha256(inventory_tool.lean_module_collector(
            [self.repo.module], "D0.All", include_proof_details=False).encode()).hexdigest()
        ref = self.repo.update_inventory(lambda i: i.update(collector_sha256=digest))
        self.assert_issue(self.repo.view(ref), "compiled_inventory", "generated Lean collector")

    def test_generator_used_to_check_digest_must_match_snapshot(self):
        other = self.repo.root / "different_generator.py"
        other.write_text("# not the pinned generator\n")
        with mock.patch.object(inventory_tool, "__file__", str(other)):
            self.assert_issue(self.repo.view(), "compiled_inventory", "running collector generator differs")

    def test_inventory_request_cannot_omit_secondary_owner(self):
        self.repo.use_multiple_owners()
        ref = self.repo.update_inventory(lambda i: i.update(requested_modules=[self.repo.module]))
        self.assert_issue(self.repo.view(ref), "compiled_inventory", "enumerate every pinned owner")

    def test_cli_book_selector_requires_kernel_mode(self):
        proc = subprocess.run([sys.executable, str(Path(c0.__file__)), "--repo", str(self.repo.root),
                               "--snapshot", self.repo.snapshot, "--kernel-book", "book01"],
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("--kernel-book requires --kernel-sections", proc.stderr)

    def test_cli_selects_book01_and_preserves_book02_default(self):
        for args, anchor in (([], "02.3b"), (["--kernel-book", "book02"], "02.3b"),
                             (["--kernel-book", "book01"], "01.1.8")):
            with self.subTest(args=args), mock.patch.object(sys, "argv", [
                    "c0_reconciliation.py", "--repo", str(self.repo.root), "--snapshot", self.repo.snapshot,
                    "--kernel-sections", *args]), mock.patch.object(
                    c0, "reconcile_kernel_sections", return_value={"issues": []}) as run, \
                    mock.patch("sys.stdout", new_callable=io.StringIO):
                self.assertEqual(c0.main(), 0)
                self.assertEqual(run.call_args.kwargs["pins"].source_anchor, anchor)


if __name__ == "__main__":
    unittest.main()
