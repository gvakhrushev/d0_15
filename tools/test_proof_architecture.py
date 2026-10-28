from __future__ import annotations

import ast
import pathlib
import copy
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools import proof_architecture as proof
from tools import proof_architecture_cold_start as cold_start
from tools import proof_architecture_process_comparison as process_comparison
from tools import lean_task_build

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lean_declaration_inventory as inventory


HISTORICAL_LEAN_SNAPSHOT_COMMIT = "f337b30e039efcc1fd30d355df35e7e6bbaf5478"
HISTORICAL_LEAN_SOURCE_DIGEST = "33d522c7340f186f551d2560ec694833548068c528523378d3503b5558c1d21a"
VERSIONED_LEAN_SNAPSHOT_COMMIT = "9f673b6a3fd305ffdb22245937041e4a1c02fee5"
VERSIONED_LEAN_SOURCE_DIGEST = "a366fc93f44672cb9b48da60c3f76658b2a299b4b7ab601b186454deb2e1337b"


def assert_historical_compiled_inventory(test: unittest.TestCase, inventory: dict) -> None:
    expected_digests = {
        HISTORICAL_LEAN_SNAPSHOT_COMMIT: HISTORICAL_LEAN_SOURCE_DIGEST,
        VERSIONED_LEAN_SNAPSHOT_COMMIT: VERSIONED_LEAN_SOURCE_DIGEST,
    }
    snapshot = inventory["snapshot_commit"]
    test.assertIn(snapshot, expected_digests)
    test.assertEqual(inventory["lean_source_digest"], expected_digests[snapshot])
    test.assertFalse(inventory["worktree_dirty"])
    test.assertEqual(inventory["public_import_root"], "D0.All")


def dataset(root: pathlib.Path | None = None) -> dict:
    return {
        "root": root or pathlib.Path("."),
        "claims": [{"claim_id": "CLM-1", "book": "B1", "section": "2",
                    "lean_module": "D0.Foo", "lean_theorem": "D0.Foo.bar",
                    "lean_status": "FORMALIZED", "notes": ""}],
        "assumptions": [{"assumption_id": "ASSUMP-1", "lean_name": "D0.Foo.Hypothesis",
                         "lean_file": "D0/Foo.lean", "used_by_theorem": "D0.Foo.bar",
                         "claim_id": "CLM-1", "assumption_type": "EXTERNAL",
                         "status": "EXPLICIT", "justification": "Retained hypothesis.",
                         "external_source_or_cert": "source.md", "failure_meaning": "Scope remains conditional."}],
        "formal_support": [{"lean_module": "D0.Foo", "lean_file": "D0/Foo.lean",
                             "role": "EXPLICIT_SUPPORT", "referenced_by": "D0/Consumer.lean"}],
        "aliases": [{"legacy_id": "OLD-1", "kind": "LEGACY_BOOK_LABEL",
                     "canonical_claim_id": "", "first_reference": "BOOK.md:10",
                     "note": "Lookup only."}],
        "assembly": {
            "results": [{"id": "r1", "statement": "Exact vector reconstruction", "outcome": "positive",
                         "evidence": [{"path": "02_REGISTRY/research/reuse.md"}]}],
            "applications": [{"id": "r1-to-o1", "result": "r1", "obligation": "o1",
                              "hypothesis_map": {"h": {"target_hypothesis": "h"}},
                              "review": {"state": "accepted"}}],
            "attempts": [{"id": "a1", "result": "r1", "scope": "counterexample"}],
        },
        "contract": {
            "obligations": [{"id": "o1", "statement": "Recover the vector", "interface": "i1",
                             "hypotheses": {"h": "given"}}],
            "interfaces": [{"id": "i1", "carrier": "exterior-four-space", "action": "creator",
                             "variations": "all role vectors", "source": "Julia raising operator",
                             "normalization": "unit vacuum", "refinement": "finite exact",
                             "scope": "model-level"}],
            "goals": [], "anti_substitutions": [], "synthesis": [],
            "source_fork_reconciliations": [],
        },
        "presuppositions": {"edges": [{"claim": "CLM-1", "presupposes": "CLM-2",
                                         "evidence": "conceptual quote"}]},
        "source_digests": {}, "snapshot_commit": "test-sha",
    }


class ProofArchitectureTests(unittest.TestCase):
    def test_cli_stdout_uses_utf8_for_non_ascii_json(self) -> None:
        sink = io.BytesIO()
        stream = io.TextIOWrapper(sink, encoding="cp1251")
        proof._configure_stdout_utf8(stream)
        stream.write("φ — доказательство")
        stream.flush()
        self.assertEqual(sink.getvalue(), "φ — доказательство".encode("utf-8"))

    def test_all_current_crosswalk_render_preserves_complete_result_arrays(self) -> None:
        rows = [{"id": f"result-{index}"} for index in range(40)]

        complete = json.loads(proof._render_text({"results": rows}, complete_arrays=True))
        bounded = json.loads(proof._render_text({"results": rows}))

        self.assertEqual(complete["results"], rows)
        self.assertEqual(len(bounded["results"]), 33)
        self.assertEqual(bounded["results"][-1], {"_omitted_items": 8})

    def test_source_locator_preserves_multiple_explicit_sections(self) -> None:
        commit = "a" * 40
        path = "02_REGISTRY/research/example.md"
        evidence = {"section_refs": ["L5: The event record", "L30: The inverse"]}
        pin = {
            "ref": commit,
            "path": path,
            "pin_status": "verified",
            "current_source_status": "source_missing",
        }

        locator = proof._source_locator_crosswalk(
            pathlib.Path("."), evidence, pin, "Recover the complete source"
        )

        source = f"source:{commit}:{path}"
        self.assertEqual(locator["section_refs"], ["L5: The event record", "L30: The inverse"])
        self.assertEqual(locator["exact_unit_key_candidates"], [
            f"{source}#L5: The event record",
            f"{source}#L30: The inverse",
        ])
        self.assertEqual(locator["ranked_section_candidates"], [])

    def test_exact_identifier_ranks_before_textual_candidate(self) -> None:
        data = dataset()
        hits = proof.structured_search(data, "r1")
        self.assertGreaterEqual(len(hits), 1)
        self.assertEqual(hits[0]["kind"], "assembly-result")
        self.assertEqual(hits[0]["key"], "r1")

    def test_structured_search_does_not_treat_bag_of_words_as_authority(self) -> None:
        data = dataset()
        data["contract"]["interfaces"] = [{
            "id": "generic-source",
            "statement": "A source is retained.",
            "unindexed_comment": "native raising operator inverse null leg",
        }]
        self.assertEqual(
            proof.structured_search(data, "native source raising operator null leg"), []
        )

    def test_structured_search_resolves_exact_declared_phrase(self) -> None:
        data = dataset()
        data["assembly"]["results"].extend([
            {"id": "generic", "statement": "A source field is retained."},
            {"id": "raising", "statement":
             "Native raising operator inverse reconstructs the null leg."},
        ])
        hits = proof.structured_search(
            data, "Native raising operator inverse reconstructs the null leg."
        )
        self.assertEqual(hits[0]["key"], "raising")

    def test_reuse_reads_explicit_application_and_keeps_review_state(self) -> None:
        data = dataset()
        result = next(x for x in proof.records(data) if x["kind"] == "assembly-result")
        view = proof.relation_view(data, result)
        self.assertEqual([a["id"] for a in view["declared_applications"]], ["r1-to-o1"])
        self.assertEqual(view["declared_applications"][0]["review"]["state"], "accepted")

    def test_claim_module_string_does_not_create_application_edge(self) -> None:
        data = dataset()
        claim = next(x for x in proof.records(data) if x["kind"] == "claim-metadata")
        self.assertEqual(proof.relation_view(data, claim)["declared_applications"], [])

    def test_scoped_attempts_require_explicit_matching_result_or_obligation(self) -> None:
        data = dataset()
        data["assembly"]["attempts"] = [
            {"id": "result-match", "result": "r1"},
            {"id": "other-result", "result": "r2"},
            {"id": "obligation-match", "obligation": "o1"},
            {"id": "other-obligation", "obligation": "o2"},
            {"id": "both-match", "result": "r1", "obligation": "o1"},
            {"id": "neither"},
            {"id": "empty-ids", "result": "", "obligation": ""},
        ]
        expected = {
            ("claim-metadata", "CLM-1"): [],
            ("assembly-result", "r1"): ["result-match", "both-match"],
            ("obligation", "o1"): ["obligation-match", "both-match"],
            ("application", "r1-to-o1"): ["result-match", "obligation-match", "both-match"],
        }
        indexed = {(item["kind"], item["key"]): item for item in proof.records(data)}
        for key, expected_ids in expected.items():
            with self.subTest(kind=key[0]):
                view = proof.relation_view(data, indexed[key])
                self.assertEqual([a["id"] for a in view["scoped_attempts"]], expected_ids)
        empty_application = {"kind": "application", "record": {"result": "", "obligation": ""}}
        self.assertEqual(proof.relation_view(data, empty_application)["scoped_attempts"], [])

    def test_compiled_claim_reuse_does_not_attach_unrelated_attempts(self) -> None:
        data = dataset()
        data["assembly"]["attempts"] = [
            {"id": "unrelated", "result": "another-result"},
            {"id": "no-result-or-obligation"},
        ]
        data["claims"].append({"claim_id": "CLM-2", "lean_module": "D0.Foo",
                               "lean_theorem": "D0.Foo.lower", "notes": ""})

        class InventoryStub:
            claim_locator_crosswalk = staticmethod(inventory.claim_locator_crosswalk)

            @staticmethod
            def candidate_names(module: str, atom: str) -> list[str]:
                return [atom]

            @staticmethod
            def run_inventory(names: list[str], import_root: str):
                return ([{"name": "D0.Foo.bar", "exists": True, "module": "D0.Foo",
                          "proof_dependencies": ["D0.Foo.lower"]}], "collector", "digest")

            @staticmethod
            def module_source_path(module: str | None) -> str | None:
                return "D0/Foo.lean"

        compiled = proof.reuse_view(data, "CLM-1", lean_inventory=InventoryStub)["compiled_claim_reuse"][0]
        self.assertEqual(compiled["declared_metadata_relations"]["scoped_attempts"], [])
        self.assertEqual(compiled["declared_metadata_relations"]["declared_applications"], [])
        self.assertEqual(compiled["compiled_dependency_claim_links"][0]["dependency_declaration"],
                         "D0.Foo.lower")
        self.assertIn("semantic claim acceptance are not inferred", compiled["interpretation"])

    def test_source_change_invalidates_its_declared_application_not_unrelated_prose(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            source = root / "02_REGISTRY" / "research" / "reuse.md"
            source.parent.mkdir(parents=True)
            source.write_text("Exact source and normalization premise.", encoding="utf-8")
            unrelated = root / "notes.md"
            unrelated.write_text("Unrelated prose.", encoding="utf-8")
            data = dataset(root)
            first = proof.impact_view(data, "02_REGISTRY/research/reuse.md")
            first_hash = first["source_snapshot"]["source_sha256"]
            self.assertEqual(first["declared_impact"][0]["item"]["key"], "r1")
            self.assertEqual(first["declared_impact"][0]["declared_applications"][0]["id"],
                             "r1-to-o1")

            source.write_text("Changed source normalization premise.", encoding="utf-8")
            second = proof.impact_view(data, "02_REGISTRY/research/reuse.md")
            self.assertNotEqual(first_hash, second["source_snapshot"]["source_sha256"])

            relevant_hash = second["source_snapshot"]["source_sha256"]
            unrelated.write_text("Changed unrelated prose.", encoding="utf-8")
            self.assertEqual(
                relevant_hash,
                proof.impact_view(data, "02_REGISTRY/research/reuse.md")
                ["source_snapshot"]["source_sha256"],
            )
            self.assertEqual(proof.impact_view(data, "notes.md")["matches"], [])

    def test_alias_and_conceptual_edge_remain_separate_from_application(self) -> None:
        data = dataset()
        alias = proof.find_exact(data, "OLD-1")
        self.assertEqual(alias[0]["kind"], "alias-lookup")
        claim = next(x for x in proof.records(data) if x["kind"] == "claim-metadata")
        view = proof.relation_view(data, claim)
        self.assertEqual(view["conceptual_presupposition_edges"][0]["presupposes"], "CLM-2")
        self.assertEqual(view["registered_assumptions"][0]["assumption_id"], "ASSUMP-1")
        self.assertEqual(view["claim_assumption_links"], [])
        self.assertEqual(view["declared_applications"], [])

    def test_claim_assumption_ids_resolve_independently_of_owner_claim(self) -> None:
        data = dataset()
        data["claims"][0]["assumption_ids"] = " ASSUMP-1, ASSUMP-2; ASSUMP-MISSING "
        data["assumptions"][0]["claim_id"] = "CLM-OWNER-1"
        data["assumptions"].append({
            "assumption_id": "ASSUMP-2",
            "claim_id": "CLM-OWNER-2",
            "lean_name": "D0.Bar.OtherHypothesis",
        })
        claim = next(x for x in proof.records(data) if x["kind"] == "claim-metadata")

        view = proof.relation_view(data, claim)

        links = view["claim_assumption_links"]
        self.assertEqual([link["assumption_id"] for link in links],
                         ["ASSUMP-1", "ASSUMP-2", "ASSUMP-MISSING"])
        self.assertEqual([link["resolution_status"] for link in links],
                         ["resolved", "resolved", "unresolved"])
        self.assertEqual([link["assumption_owner_claim_id"] for link in links],
                         ["CLM-OWNER-1", "CLM-OWNER-2", None])
        self.assertEqual([row["assumption_id"] for row in view["registered_assumptions"]], [])

    def test_bridge_claim_resolves_all_six_registry_assumption_ids(self) -> None:
        data = proof.load_dataset()
        claim = proof.find_exact(data, "D0-LEAN-BRIDGE-001")[0]

        view = proof.relation_view(data, claim)
        links = view["claim_assumption_links"]

        self.assertEqual([link["assumption_id"] for link in links], [
            "ASSUMP-HURWITZ-GOLDEN",
            "ASSUMP-RG-SMOOTH-INTERP",
            "ASSUMP-LORENTZ-MACRO",
            "ASSUMP-SMOOTH-COVARIANCE",
            "ASSUMP-SMOOTH-HEATTRACE",
            "ASSUMP-HST-EXTERNAL",
        ])
        self.assertTrue(all(link["resolution_status"] == "resolved" for link in links))
        self.assertEqual([link["assumption_owner_claim_id"] for link in links], [
            "D0-PHI-HURWITZ-001",
            "D0-RG-001",
            "D0-CARRIER-003",
            "D0-SMOOTH-001",
            "D0-SMOOTH-001",
            "D0-LEAN-BRIDGE-001",
        ])
        self.assertEqual(
            [row["assumption_id"] for row in view["registered_assumptions"]],
            ["ASSUMP-HST-EXTERNAL"],
        )

    def test_assumption_is_an_explicit_metadata_record_with_failure_scope(self) -> None:
        match = proof.find_exact(dataset(), "ASSUMP-1")
        self.assertEqual(match[0]["kind"], "assumption-metadata")
        self.assertEqual(match[0]["record"]["failure_meaning"], "Scope remains conditional.")

    def test_why_preserves_obligation_hypotheses_and_declared_edge(self) -> None:
        view = proof.why_view(dataset(), "o1")
        self.assertEqual(view["obligation"]["hypotheses"], {"h": "given"})
        self.assertEqual(view["interface"]["carrier"], "exterior-four-space")
        self.assertEqual(view["interface"]["source"], "Julia raising operator")
        self.assertEqual(view["interface"]["normalization"], "unit vacuum")
        self.assertEqual([a["id"] for a in view["declared_applications"]], ["r1-to-o1"])
        self.assertEqual(view["declared_applications"][0]["hypothesis_mapping_gaps"], [])

    def test_why_reports_unmapped_hypotheses_without_closing_them(self) -> None:
        data = dataset()
        data["assembly"]["applications"][0]["hypothesis_map"] = {}
        view = proof.why_view(data, "o1")
        self.assertEqual(view["declared_applications"][0]["hypothesis_mapping_gaps"], ["h"])
        self.assertEqual(view["declared_applications"][0]["hypothesis_mapping_status"], "unmapped")

    def test_why_distinguishes_unknown_empty_and_invalid_hypothesis_maps(self) -> None:
        data = dataset()
        del data["contract"]["obligations"][0]["hypotheses"]
        view = proof.why_view(data, "o1")
        self.assertEqual(view["hypotheses_status"], "unknown")
        self.assertEqual(view["declared_applications"][0]["hypothesis_mapping_status"], "unknown")

        data = dataset()
        data["contract"]["obligations"][0]["hypotheses"] = {}
        data["assembly"]["applications"][0]["hypothesis_map"] = {}
        view = proof.why_view(data, "o1")
        self.assertEqual(view["hypotheses_status"], "declared_empty")
        self.assertEqual(view["declared_applications"][0]["hypothesis_mapping_status"],
                         "declared_empty")

        data = dataset()
        data["assembly"]["applications"][0]["hypothesis_map"] = {
            "h": {"target_hypothesis": "not-an-obligation-hypothesis"}
        }
        view = proof.why_view(data, "o1")
        self.assertEqual(view["declared_applications"][0]["hypothesis_mapping_status"],
                         "unknown_target")

        data["assembly"]["applications"][0]["hypothesis_map"] = {
            "h": {"target_hypothesis": 7}
        }
        view = proof.why_view(data, "o1")
        self.assertEqual(view["declared_applications"][0]["hypothesis_mapping_status"], "unknown")
        self.assertEqual(len(view["declared_applications"][0]["invalid_hypothesis_map_entries"]), 1)

    def test_reuse_of_application_exposes_its_exact_result_and_obligation(self) -> None:
        data = dataset()
        item = next(x for x in proof.records(data)
                    if x["kind"] == "application" and x["key"] == "r1-to-o1")
        view = proof.relation_view(data, item)
        self.assertEqual(view["declared_result"]["id"], "r1")
        self.assertEqual(view["target_obligation"]["id"], "o1")
        self.assertEqual(view["target_interface"]["carrier"], "exterior-four-space")
        self.assertEqual([x["id"] for x in view["declared_applications"]], ["r1-to-o1"])

    def test_compiled_reuse_joins_exact_claim_locator_and_proof_dependencies(self) -> None:
        data = dataset()
        data["claims"].append({"claim_id": "CLM-2", "book": "B2", "section": "3",
                               "lean_module": "D0.Foo", "lean_theorem": "D0.Foo.lower",
                               "lean_status": "FORMALIZED", "notes": "Supporting locator."})

        class InventoryStub:
            claim_locator_crosswalk = staticmethod(inventory.claim_locator_crosswalk)

            @staticmethod
            def candidate_names(module: str, atom: str) -> list[str]:
                return [atom]

            @staticmethod
            def run_inventory(names: list[str], import_root: str):
                self.assertEqual(names, ["D0.Foo.bar"])
                self.assertEqual(import_root, "D0.All")
                return ([{"name": "D0.Foo.bar", "exists": True,
                          "module": "D0.Foo", "proof_dependencies": ["D0.Foo.lower"],
                          "elaborated_type": "D0.Foo.Hypothesis → D0.Result"}],
                        "collector-sha", "lean-source-sha")

            @staticmethod
            def module_source_path(module: str | None) -> str | None:
                return "D0/Foo.lean" if module == "D0.Foo" else None

        view = proof.reuse_view(data, "CLM-1", lean_inventory=InventoryStub)
        compiled = view["compiled_claim_reuse"][0]

        self.assertEqual(compiled["claim_locator_mappings"][0]["resolution_status"], "resolved")
        self.assertEqual(compiled["compiled_declarations"][0]["source_path"], "D0/Foo.lean")
        self.assertEqual(compiled["compiled_dependency_claim_links"], [{
            "source_claim_id": "CLM-1", "source_declaration": "D0.Foo.bar",
            "dependency_declaration": "D0.Foo.lower",
            "target_claim_locators": [{"claim_id": "CLM-2", "theorem_atom": "D0.Foo.lower",
                                        "module_locator": "D0.Foo"}],
            "relation": "compiled-proof-dependency-to-claim-locator",
        }])
        self.assertEqual(compiled["declared_metadata_relations"]["declared_applications"], [])
        self.assertIn("not inferred", compiled["interpretation"])

    def test_compiled_reuse_keeps_assembly_application_metadata_separate(self) -> None:
        data = dataset()

        class NeverCompile:
            @staticmethod
            def run_inventory(names: list[str], import_root: str):
                raise AssertionError("assembly application keys are not claim locators")

        view = proof.reuse_view(data, "r1-to-o1", lean_inventory=NeverCompile)

        self.assertEqual(view["compiled_claim_reuse"], [])
        self.assertEqual(view["compiled_claim_reuse_status"], "key_is_not_an_exact_claim_id")
        self.assertEqual([row["id"] for row in view["matches"][0]["declared_applications"]],
                         ["r1-to-o1"])

    def test_compiled_reuse_classifies_owner_without_changing_name_presence_or_acceptance(self) -> None:
        cases = [
            ("D0.Foo", "result", ["D0.result"], ["D0.Other"],
             "resolved", "resolved_outside_declared_modules", [False]),
            ("D0.Foo", "result", ["D0.result"], ["D0.Foo"],
             "resolved", "resolved_in_declared_module", [True]),
            ("D0.Foo", "result", ["D0.result", "D0.Foo.result"],
             ["D0.Other", "D0.Foo"], "resolved",
             "ambiguous_across_declared_and_other_modules", [False, True]),
            ("", "result", ["D0.result"], ["D0.Other"],
             "resolved", "resolved_without_module_locator", [False]),
            ("D0.Foo", "", [], [], "unresolved", "no_theorem_locator", []),
            ("D0.Foo", "result", ["D0.result"], [], "unresolved", "unresolved", []),
        ]
        for module, atom, names, owners, presence, owner_status, flags in cases:
            with self.subTest(module=module, atom=atom, owners=owners):
                data = dataset()
                data["claims"][0].update(lean_module=module, lean_theorem=atom)
                data["claims"].append({
                    "claim_id": "CLM-2", "lean_module": "D0.Dependency",
                    "lean_theorem": "D0.Dependency.lemma", "notes": "",
                })
                declarations = [
                    {"name": name, "exists": True, "module": owner,
                     "proof_dependencies": ["D0.Dependency.lemma"],
                     "elaborated_type": "D0.Hypothesis → D0.Result"}
                    for name, owner in zip(names, owners)
                ]
                # Inventory source-path enrichment is expected, but must not
                # let mutations of the returned rows change the test oracle.
                expected_declarations = copy.deepcopy(declarations)
                for declaration in expected_declarations:
                    declaration.setdefault("source_path", None)

                class InventoryStub:
                    claim_locator_crosswalk = staticmethod(inventory.claim_locator_crosswalk)

                    @staticmethod
                    def candidate_names(module_name: str, theorem: str) -> list[str]:
                        return names if theorem == "result" else [theorem]

                    @staticmethod
                    def run_inventory(requested: list[str], import_root: str):
                        return declarations, "collector-sha", "lean-source-sha"

                    @staticmethod
                    def module_source_path(module_name: str | None) -> str | None:
                        return None

                view = proof.reuse_view(data, "CLM-1", lean_inventory=InventoryStub)
                compiled = view["compiled_claim_reuse"][0]
                mapping = compiled["claim_locator_mappings"][0]
                self.assertEqual(mapping["resolution_status"], presence)
                self.assertEqual(mapping["owner_resolution_status"], owner_status)
                self.assertEqual(
                    [row["owner_matches_locator"] for row in mapping["owner_resolution_matches"]],
                    flags,
                )
                self.assertEqual(mapping["resolved_declarations"], expected_declarations)
                self.assertEqual(compiled["compiled_declarations"], expected_declarations)
                self.assertEqual(len(compiled["compiled_dependency_claim_links"]), len(declarations))
                self.assertEqual(compiled["declared_metadata_relations"]["declared_applications"], [])
                self.assertIn("semantic claim acceptance are not inferred", compiled["interpretation"])

    def test_compiled_reuse_keeps_owner_flags_local_to_each_claim_locator(self) -> None:
        data = dataset()
        data["claims"].append({
            "claim_id": "CLM-2", "lean_module": "D0.Other",
            "lean_theorem": "D0.Foo.bar", "notes": "",
        })
        shared = {"name": "D0.Foo.bar", "exists": True, "module": "D0.Foo",
                  "proof_dependencies": [], "elaborated_type": "D0.Result"}
        expected = copy.deepcopy(shared)
        expected["source_path"] = "D0/Foo.lean"

        class InventoryStub:
            claim_locator_crosswalk = staticmethod(inventory.claim_locator_crosswalk)

            @staticmethod
            def candidate_names(module: str, atom: str) -> list[str]:
                return [atom]

            @staticmethod
            def run_inventory(names: list[str], import_root: str):
                return [shared], "collector-sha", "lean-source-sha"

            @staticmethod
            def module_source_path(module: str | None) -> str | None:
                return "D0/Foo.lean" if module == "D0.Foo" else None

        first = proof.reuse_view(data, "CLM-1", lean_inventory=InventoryStub)["compiled_claim_reuse"][0]
        second = proof.reuse_view(data, "CLM-2", lean_inventory=InventoryStub)["compiled_claim_reuse"][0]
        first_mapping = first["claim_locator_mappings"][0]
        second_mapping = second["claim_locator_mappings"][0]
        self.assertEqual(first_mapping["owner_resolution_status"], "resolved_in_declared_module")
        self.assertEqual(second_mapping["owner_resolution_status"], "resolved_outside_declared_modules")
        self.assertTrue(first_mapping["owner_resolution_matches"][0]["owner_matches_locator"])
        self.assertFalse(second_mapping["owner_resolution_matches"][0]["owner_matches_locator"])
        self.assertEqual(first_mapping["resolved_declarations"], [expected])
        self.assertEqual(second_mapping["resolved_declarations"], [expected])
        self.assertEqual(shared, expected)
        self.assertNotIn("owner_matches_locator", shared)

    def test_compiled_reuse_follows_explicit_canonical_claim_alias(self) -> None:
        data = dataset()
        data["claims"][0]["release_status"] = "CORE-FORMALIZED"
        data["aliases"] = [{
            "legacy_id": "OLD-CLAIM-1", "kind": "CANONICAL_TARGET",
            "canonical_claim_id": "CLM-1", "first_reference": "BOOK.md:10",
            "note": "Renamed claim locator.",
        }]

        class InventoryStub:
            claim_locator_crosswalk = staticmethod(inventory.claim_locator_crosswalk)

            @staticmethod
            def candidate_names(module: str, atom: str) -> list[str]:
                return [atom]

            @staticmethod
            def run_inventory(names: list[str], import_root: str):
                self.assertEqual(names, ["D0.Foo.bar"])
                self.assertEqual(import_root, "D0.All")
                return ([{"name": "D0.Foo.bar", "exists": True,
                          "module": "D0.Foo", "proof_dependencies": [],
                          "elaborated_type": "D0.Foo.Hypothesis → D0.Result"}],
                        "collector-sha", "lean-source-sha")

            @staticmethod
            def module_source_path(module: str | None) -> str | None:
                return "D0/Foo.lean" if module == "D0.Foo" else None

        view = proof.reuse_view(data, "OLD-CLAIM-1", lean_inventory=InventoryStub)

        self.assertEqual(view["compiled_claim_reuse"], [])
        self.assertEqual(view["compiled_claim_reuse_status"], "controlled_alias_candidate")
        self.assertEqual(len(view["compiled_claim_alias_reuse"]), 1)
        alias = view["compiled_claim_alias_reuse"][0]
        self.assertEqual(alias["alias_id"], "OLD-CLAIM-1")
        self.assertEqual(alias["canonical_claim_id"], "CLM-1")
        self.assertTrue(alias["target_claim_found"])
        self.assertEqual(alias["canonical_claim"]["release_status"], "CORE-FORMALIZED")
        self.assertEqual(alias["canonical_claim"]["lean_status"], "FORMALIZED")
        self.assertEqual(alias["compiled_claim_reuse"]["claim_id"], "CLM-1")
        self.assertEqual(
            alias["compiled_claim_reuse"]["compiled_declarations"][0]["name"],
            "D0.Foo.bar",
        )
        self.assertIn("no semantic equivalence", view["compiled_claim_reuse_interpretation"])

    def test_compiled_reuse_does_not_expand_lookup_only_alias(self) -> None:
        data = dataset()

        class NeverCompile:
            @staticmethod
            def run_inventory(names: list[str], import_root: str):
                raise AssertionError("lookup-only aliases are not claim locators")

        view = proof.reuse_view(data, "OLD-1", lean_inventory=NeverCompile)

        self.assertEqual(view["compiled_claim_alias_reuse"], [])
        self.assertEqual(view["compiled_claim_reuse_status"], "key_is_not_an_exact_claim_id")
        self.assertIn("Lookup-only aliases", view["compiled_claim_reuse_interpretation"])

    def test_compiled_reuse_reports_missing_canonical_alias_target_without_compiling(self) -> None:
        data = dataset()
        data["aliases"] = [{
            "legacy_id": "OLD-MISSING", "kind": "CANONICAL_TARGET",
            "canonical_claim_id": "MISSING-CLAIM", "first_reference": "BOOK.md:11",
            "note": "Stale canonical target control.",
        }]

        class NeverCompile:
            @staticmethod
            def run_inventory(names: list[str], import_root: str):
                raise AssertionError("missing alias target must not trigger a Lean query")

        view = proof.reuse_view(data, "OLD-MISSING", lean_inventory=NeverCompile)

        self.assertEqual(view["compiled_claim_reuse_status"], "controlled_alias_target_missing")
        self.assertEqual(view["compiled_claim_alias_reuse"], [{
            "alias_id": "OLD-MISSING", "alias_kind": "CANONICAL_TARGET",
            "canonical_claim_id": "MISSING-CLAIM", "target_claim_found": False,
        }])
        self.assertIn("absent from claims.csv", view["compiled_claim_reuse_interpretation"])

    def test_exact_claim_and_canonical_alias_target_are_reported_separately(self) -> None:
        data = dataset()
        data["claims"].append({
            "claim_id": "CLM-2", "book": "B2", "section": "4",
            "lean_module": "D0.Foo", "lean_theorem": "D0.Foo.lower",
            "lean_status": "FORMALIZED", "release_status": "NO-GO", "notes": "Target.",
        })
        data["aliases"] = [{
            "legacy_id": "CLM-1", "kind": "CANONICAL_TARGET",
            "canonical_claim_id": "CLM-2", "first_reference": "BOOK.md:12",
            "note": "Explicit rename target.",
        }]

        class InventoryStub:
            claim_locator_crosswalk = staticmethod(inventory.claim_locator_crosswalk)

            declarations = {
                "D0.Foo.bar": {"name": "D0.Foo.bar", "exists": True,
                               "module": "D0.Foo", "proof_dependencies": [],
                               "elaborated_type": "D0.Result"},
                "D0.Foo.lower": {"name": "D0.Foo.lower", "exists": True,
                                 "module": "D0.Foo", "proof_dependencies": [],
                                 "elaborated_type": "D0.LowerResult"},
            }

            @staticmethod
            def candidate_names(module: str, atom: str) -> list[str]:
                return [atom]

            @staticmethod
            def run_inventory(names: list[str], import_root: str):
                self.assertEqual(import_root, "D0.All")
                return ([InventoryStub.declarations[name] for name in names],
                        "collector-sha", "lean-source-sha")

            @staticmethod
            def module_source_path(module: str | None) -> str | None:
                return "D0/Foo.lean" if module == "D0.Foo" else None

        view = proof.reuse_view(data, "CLM-1", lean_inventory=InventoryStub)

        self.assertEqual(view["compiled_claim_reuse"][0]["claim_id"], "CLM-1")
        self.assertEqual(view["compiled_claim_alias_reuse_status"],
                         "exact_claim_and_controlled_alias")
        self.assertEqual(view["compiled_claim_alias_reuse"][0]["canonical_claim_id"], "CLM-2")
        self.assertEqual(view["compiled_claim_alias_reuse"][0]["canonical_claim"]["release_status"],
                         "NO-GO")
        self.assertEqual(
            view["compiled_claim_alias_reuse"][0]["compiled_claim_reuse"]["claim_id"],
            "CLM-2",
        )
        self.assertIn("reported separately", view["compiled_claim_alias_reuse_interpretation"])

    def test_result_crosswalk_keeps_compiled_candidates_separate_from_application_acceptance(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            source_rel = "03_FORMALIZATION/D0/Foo.lean"
            source = root / source_rel
            source.parent.mkdir(parents=True)
            source.write_text("theorem bar : True := True.intro", encoding="utf-8")
            research_rel = "02_REGISTRY/research/reuse.md"
            research_source = root / research_rel
            research_source.parent.mkdir(parents=True)
            research_source.write_bytes(b"## Theorem 1\nA pinned result.\n")
            historical_rel = "02_REGISTRY/research/historical.md"
            historical_source = root / historical_rel
            historical_source.write_bytes(
                b"# Exact vector reconstruction\n\n"
                b"Pinned historical evidence for exact vector reconstruction.\n"
            )
            candidate_rel = "02_REGISTRY/research/candidate.md"
            candidate_source = root / candidate_rel
            candidate_source.write_bytes(
                b"# Exact vector reconstruction\n\n"
                b"This section records the exact vector reconstruction result.\n"
            )
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run([
                "git", "add", source_rel, research_rel, historical_rel, candidate_rel
            ], cwd=root, check=True)
            subprocess.run([
                "git", "-c", "user.name=Test", "-c", "user.email=test@example.com",
                "commit", "-q", "-m", "pin Lean source",
            ], cwd=root, check=True)
            ref = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=root, text=True
            ).strip()
            pinned_bytes = subprocess.check_output(
                ["git", "cat-file", "blob", f"{ref}:{source_rel}"], cwd=root
            )
            source_sha = hashlib.sha256(pinned_bytes).hexdigest()
            research_sha = hashlib.sha256(
                subprocess.check_output(
                    ["git", "cat-file", "blob", f"{ref}:{research_rel}"], cwd=root
                )
            ).hexdigest()
            historical_sha = hashlib.sha256(
                subprocess.check_output(
                    ["git", "cat-file", "blob", f"{ref}:{historical_rel}"], cwd=root
                )
            ).hexdigest()
            candidate_sha = hashlib.sha256(
                subprocess.check_output(
                    ["git", "cat-file", "blob", f"{ref}:{candidate_rel}"], cwd=root
                )
            ).hexdigest()
            historical_source.unlink()
            data = dataset(root)
            data["assembly"]["results"] = [{
                "id": "r1", "statement": "Exact vector reconstruction",
                "owner": "owner", "reported_state": "scoped result",
                "evidence": [
                    {"ref": ref, "path": source_rel, "sha256": source_sha,
                     "declaration_names": [
                         "D0.Foo.bar", "D0.Foo.missing", "D0.Other.bar",
                         "D0.Foo.owner_mismatch"
                     ]},
                    {"ref": ref, "path": research_rel, "sha256": research_sha,
                     "section_ref": "Theorem 1"},
                    {"ref": ref, "path": research_rel, "sha256": "0" * 64,
                     "section_ref": "Theorem 1"},
                    {"ref": ref, "path": historical_rel, "sha256": historical_sha},
                    {"ref": ref, "path": candidate_rel, "sha256": candidate_sha},
                ],
            }]

            class InventoryStub:
                @staticmethod
                def run_module_inventory(modules: list[str], import_root: str,
                                         include_proof_details: bool = True):
                    self.assertEqual(modules, ["D0.Foo"])
                    self.assertEqual(import_root, "D0.All")
                    self.assertFalse(include_proof_details)
                    return ([{
                        "name": "D0.Foo.bar", "module": "D0.Foo",
                        "source_path": source_rel,
                        "elaborated_type": "True", "binders": [],
                        "conclusion_whnf": "True", "type_dependencies": ["True"],
                        "proof_dependencies": ["True.intro"], "axioms": [],
                        "declaration_ranges": {"declaration": {"start": {"line": 1}}},
                        "proof_details_status": "omitted_by_bulk_mode",
                    }, {
                        "name": "D0.Foo.owner_mismatch", "module": "D0.Foo",
                        "source_path": source_rel,
                        "elaborated_type": "True", "binders": [],
                        "conclusion_whnf": "True", "type_dependencies": ["True"],
                        "proof_dependencies": ["True.intro"], "axioms": [],
                        "declaration_ranges": {"declaration": {"start": {"line": 1}}},
                        "proof_details_status": "omitted_by_bulk_mode",
                    }], "collector-sha", "lean-source-sha")

                @staticmethod
                def run_inventory(names: list[str], import_root: str):
                    self.assertEqual(names, ["D0.Foo.bar", "D0.Foo.owner_mismatch"])
                    self.assertEqual(import_root, "D0.All")
                    return ([{
                        "name": "D0.Foo.bar", "exists": True, "module": "D0.Foo",
                        "elaborated_type": "True", "binders": [], "conclusion_whnf": "True",
                        "type_dependencies": ["True"], "proof_dependencies": ["True.intro"],
                        "axioms": [],
                        "declaration_ranges": {"declaration": {"start": {"line": 1}}},
                    }, {
                        "name": "D0.Foo.owner_mismatch", "exists": True,
                        "module": "D0.Other", "elaborated_type": "True",
                        "binders": [], "conclusion_whnf": "True",
                        "type_dependencies": ["True"],
                        "proof_dependencies": ["True.intro"], "axioms": [],
                        "declaration_ranges": {"declaration": {"start": {"line": 1}}},
                    }], "detail-collector-sha", "lean-source-sha")

                @staticmethod
                def candidate_names(module: str, atom: str) -> list[str]:
                    return [atom] if atom.startswith("D0.") else [f"{module}.{atom}"]

                @staticmethod
                def module_source_path(module: str | None) -> str | None:
                    return source_rel if module == "D0.Foo" else None

            view = proof.result_declaration_crosswalk_view(
                data, InventoryStub, result_id="r1"
            )
            all_current_view = proof.result_declaration_crosswalk_view(
                data, InventoryStub, all_current=True
            )

        self.assertEqual(view["evidence_crosswalks"][0]["pin"]["pin_status"], "verified")
        self.assertEqual(
            view["evidence_crosswalks"][0]["pin"]["current_source_status"], "matches_pin"
        )
        source_locators = view["source_locator_crosswalks"]
        self.assertEqual(len(source_locators), 5)
        self.assertEqual(
            source_locators[0]["locator"]["source_file_key"],
            f"source:{ref}:{source_rel}",
        )
        self.assertEqual(source_locators[0]["locator"]["unit_locator_status"],
                         "section_locator_not_recorded")
        self.assertEqual(source_locators[0]["locator"]["exact_unit_key_candidates"], [])
        self.assertEqual(
            source_locators[1]["locator"]["exact_unit_key_candidates"],
            [f"source:{ref}:{research_rel}#Theorem 1"],
        )
        self.assertEqual(source_locators[1]["locator"]["unit_locator_status"],
                         "candidate_section_keys_need_review")
        self.assertEqual(source_locators[2]["locator"]["pin_status"],
                         "pinned_sha256_mismatch")
        self.assertIsNone(source_locators[2]["locator"]["source_file_key"])
        self.assertEqual(source_locators[2]["locator"]["exact_unit_key_candidates"], [])
        self.assertEqual(source_locators[2]["locator"]["ranked_section_candidates"], [])
        self.assertEqual(source_locators[2]["locator"]["unit_locator_status"],
                         "section_reference_without_verified_source_pin")
        self.assertEqual(source_locators[3]["locator"]["pin_status"], "verified")
        self.assertEqual(source_locators[3]["locator"]["current_source_status"],
                         "source_missing")
        self.assertEqual(
            source_locators[3]["locator"]["source_file_key"],
            f"source:{ref}:{historical_rel}",
        )
        self.assertEqual(
            source_locators[3]["locator"]["ranked_section_candidates"][0][
                "candidate_source_unit_key"
            ],
            f"source:{ref}:{historical_rel}#L1: Exact vector reconstruction",
        )
        self.assertEqual(
            source_locators[4]["locator"]["ranked_section_candidates"][0][
                "candidate_source_unit_key"
            ],
            f"source:{ref}:{candidate_rel}#L1: Exact vector reconstruction",
        )
        self.assertEqual(source_locators[4]["locator"]["unit_locator_status"],
                         "ranked_heading_candidates_need_review")
        self.assertEqual(view["compiled_declarations"][0]["elaborated_type"], "True")
        self.assertEqual(view["compiled_declarations"][0]["proof_details_status"],
                         "collected_for_explicit_declaration_locator")
        self.assertEqual(view["claim_locator_candidates"][0]["claim_id"], "CLM-1")
        self.assertEqual(view["formal_support_candidates"][0]["lean_module"], "D0.Foo")
        self.assertEqual(view["declaration_disposition"], "ambiguous")
        self.assertEqual(
            view["explicit_declaration_locator_disposition"], "partially_resolved"
        )
        self.assertEqual(
            [locator["resolution_status"] for locator in view["explicit_declaration_locators"]],
            ["resolved", "not_found_in_pinned_module", "not_found_in_pinned_module",
             "declaration_owner_module_mismatch"],
        )
        self.assertEqual(
            view["explicit_declaration_locators"][0]["compiled_declaration"][
                "proof_dependencies"
            ],
            ["True.intro"],
        )
        self.assertEqual(view["semantic_relation_status"], "unresolved")
        self.assertFalse(view["acceptance_inferred"])
        self.assertEqual(view["declared_relations"]["declared_applications"][0]["review"]["state"],
                         "accepted")
        self.assertEqual(all_current_view["result_count"], 1)
        self.assertEqual(
            all_current_view["source_locator_summary"]["pin_status_counts"],
            {"verified": 4, "pinned_sha256_mismatch": 1},
        )
        self.assertEqual(
            all_current_view["source_locator_summary"]["current_source_status_counts"],
            {"matches_pin": 3, "unverified_pin": 1, "source_missing": 1},
        )
        self.assertEqual(
            all_current_view["source_locator_summary"]["ranked_section_candidate_count"], 2
        )
        self.assertEqual(
            all_current_view["source_locator_summary"]["results_with_ranked_section_candidates"],
            1,
        )
        self.assertEqual(
            all_current_view["source_locator_summary"]["results_with_incomplete_section_mapping"],
            0,
        )

    def test_metric_provenance_pins_proper_lorentz_orbit_without_acceptance(self) -> None:
        crosswalk_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "metric_provenance_crosswalk_2026-10-26_46328dbe.json"
        )
        payload = crosswalk_path.read_bytes()
        self.assertEqual(
            hashlib.sha256(payload).hexdigest(),
            "203bee133a15faf74ab3db9088de8074287407fe9e08e720af8149d94bff5a7c",
        )
        crosswalk = json.loads(payload)
        self.assertEqual(crosswalk["snapshot_commit"],
                         "46328dbe01473c2188f715b9b15676cbb9ec8661")
        self.assertFalse(crosswalk["worktree_dirty"])
        self.assertEqual(crosswalk["explicit_declaration_locator_disposition"],
                         "all_resolved")
        locators = [
            row for row in crosswalk["explicit_declaration_locators"]
            if row.get("name")
        ]
        self.assertEqual(len(locators), 32)
        self.assertEqual(
            [row for row in crosswalk["explicit_declaration_locators"]
             if "_omitted_items" in row],
            [{"_omitted_items": 1}],
        )
        locators = {
            row["name"]: row for row in locators
        }
        required = {
            "D0.Geometry.IsProperRoleLorentz",
            "D0.Geometry.a4dSameFrameOrientation",
            "D0.Geometry.a4dRightLorentz_sameOrientation_isProper",
            "D0.Geometry.a4dRightProperLorentz_gram_complete",
        }
        for name in required:
            locator = locators[name]
            self.assertEqual(locator["resolution_status"], "resolved")
            self.assertEqual(locator["source"]["ref"],
                             "89d80ef66a9cf1fe540360e258209c2b98bf84e8")
            self.assertEqual(locator["compiled_declaration"]["module"],
                             "D0.Geometry.A4DStarFiniteLorentzQuotient")
        supplement_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "proper_role_lorentz_orbit_declarations_2026-10-26.json"
        )
        supplement = json.loads(supplement_path.read_text(encoding="utf-8"))
        # Preserve this clean source receipt as historical evidence.
        self.assertEqual(
            supplement["snapshot_commit"],
            "32d9281e3f22d2d1bb5c7b919c8578f7599aef46",
        )
        self.assertFalse(supplement["worktree_dirty"])
        self.assertEqual(
            supplement["lean_source_digest"],
            "dabf250dc4288c227cfc51c8f6b2352dae221b14717d78c8b08d705445db19de",
        )
        self.assertEqual(supplement["public_import_root"], "D0.All")
        declarations = {row["name"]: row for row in supplement["declarations"]}
        self.assertEqual(set(declarations), required | {
            "D0.Geometry.a4d_complete_proper_orbit_coordinates"
        })
        proper_field_orbit = declarations[
            "D0.Geometry.a4d_complete_proper_orbit_coordinates"
        ]
        self.assertEqual(proper_field_orbit["declaration_kind"], "theorem")
        self.assertIn("a4dSameFrameOrientation", proper_field_orbit["elaborated_type"])
        self.assertIn("IsProperRoleLorentz", proper_field_orbit["elaborated_type"])
        self.assertIn("time orientation unrestricted", crosswalk["reported_state"])
        self.assertEqual(crosswalk["semantic_relation_status"], "unresolved")
        self.assertFalse(crosswalk["acceptance_inferred"])

    def test_result_crosswalk_stale_current_source_is_citation_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            source_rel = "03_FORMALIZATION/D0/Foo.lean"
            source = root / source_rel
            source.parent.mkdir(parents=True)
            source.write_text("theorem bar : True := True.intro", encoding="utf-8")
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "add", source_rel], cwd=root, check=True)
            subprocess.run([
                "git", "-c", "user.name=Test", "-c", "user.email=test@example.com",
                "commit", "-q", "-m", "pin Lean source",
            ], cwd=root, check=True)
            ref = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=root, text=True
            ).strip()
            pinned_bytes = subprocess.check_output(
                ["git", "cat-file", "blob", f"{ref}:{source_rel}"], cwd=root
            )
            pinned_sha = hashlib.sha256(pinned_bytes).hexdigest()
            source.write_text("theorem bar : False := by trivial", encoding="utf-8")
            data = dataset(root)
            data["assembly"]["results"] = [{
                "id": "r1", "evidence": [{"ref": ref, "path": source_rel,
                                             "sha256": pinned_sha}],
            }]

            class NeverCompile:
                @staticmethod
                def run_module_inventory(*_args, **_kwargs):
                    raise AssertionError("stale working sources must not be called current declarations")

                @staticmethod
                def candidate_names(module: str, atom: str) -> list[str]:
                    return [atom] if atom.startswith("D0.") else [f"{module}.{atom}"]

            view = proof.result_declaration_crosswalk_view(
                data, NeverCompile, result_id="r1"
            )

        self.assertEqual(view["evidence_crosswalks"][0]["pin"]["pin_status"], "verified")
        self.assertEqual(view["evidence_crosswalks"][0]["pin"]["current_source_status"],
                         "changed_since_pin")
        self.assertEqual(view["compiled_declarations"], [])
        self.assertEqual(view["declaration_disposition"], "unresolved")

    def test_result_crosswalk_all_summary_keeps_results_without_lean_evidence_unresolved(self) -> None:
        data = dataset()

        class NeverCompile:
            @staticmethod
            def run_module_inventory(*_args, **_kwargs):
                raise AssertionError("non-Lean evidence must not trigger Lean enumeration")

            @staticmethod
            def candidate_names(module: str, atom: str) -> list[str]:
                return [atom] if atom.startswith("D0.") else [f"{module}.{atom}"]

        view = proof.result_declaration_crosswalk_view(data, NeverCompile)
        self.assertEqual(view["result_count"], 1)
        self.assertEqual(view["results"][0]["lean_evidence_count"], 0)
        self.assertEqual(view["results"][0]["declaration_disposition"], "unresolved")
        self.assertEqual(view["results"][0]["semantic_relation_status"], "unresolved")

    def test_all_current_crosswalk_enumerates_verified_modules_once(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            sources = {
                "03_FORMALIZATION/D0/Foo.lean": "theorem bar : True := True.intro\n",
                "03_FORMALIZATION/D0/Bar.lean": "theorem baz : True := True.intro\n",
            }
            for relative, content in sources.items():
                source = root / relative
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_bytes(content.encode("utf-8"))
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "add", *sources], cwd=root, check=True)
            subprocess.run([
                "git", "-c", "user.name=Test", "-c", "user.email=test@example.com",
                "commit", "-q", "-m", "pin Lean sources",
            ], cwd=root, check=True)
            ref = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=root, text=True
            ).strip()
            evidence = []
            for relative in sources:
                pinned = subprocess.check_output(
                    ["git", "cat-file", "blob", f"{ref}:{relative}"], cwd=root
                )
                evidence.append({
                    "ref": ref, "path": relative,
                    "sha256": hashlib.sha256(pinned).hexdigest(),
                })
            data = dataset(root)
            data["assembly"]["results"] = [
                {"id": "r-foo", "evidence": [evidence[0]]},
                {"id": "r-bar", "evidence": [evidence[1]]},
            ]

            class InventoryStub:
                @staticmethod
                def run_module_inventory(modules: list[str], import_root: str,
                                         include_proof_details: bool = True):
                    self.assertEqual(modules, ["D0.Bar", "D0.Foo"])
                    self.assertEqual(import_root, "D0.All")
                    self.assertFalse(include_proof_details)
                    return ([{
                        "name": "D0.Foo.bar", "module": "D0.Foo",
                        "source_path": "03_FORMALIZATION/D0/Foo.lean",
                        "elaborated_type": "True", "binders": [],
                        "conclusion_whnf": "True", "type_dependencies": ["True"],
                        "proof_dependencies": None, "axioms": None,
                        "declaration_ranges": {"declaration": {"start": {"line": 1}}},
                        "proof_details_status": "omitted_by_bulk_mode",
                    }, {
                        "name": "D0.Bar.baz", "module": "D0.Bar",
                        "source_path": "03_FORMALIZATION/D0/Bar.lean",
                        "elaborated_type": "True", "binders": [],
                        "conclusion_whnf": "True", "type_dependencies": ["True"],
                        "proof_dependencies": None, "axioms": None,
                        "declaration_ranges": {"declaration": {"start": {"line": 1}}},
                        "proof_details_status": "omitted_by_bulk_mode",
                    }], "collector-sha", "lean-source-sha")

                @staticmethod
                def run_inventory(names: list[str], import_root: str):
                    self.assertEqual(names, ["D0.Foo.bar"])
                    self.assertEqual(import_root, "D0.All")
                    return ([{
                        "name": "D0.Foo.bar", "exists": True, "module": "D0.Foo",
                        "elaborated_type": "True", "binders": [], "conclusion_whnf": "True",
                        "type_dependencies": ["True"], "proof_dependencies": ["True.intro"],
                        "axioms": [],
                        "declaration_ranges": {"declaration": {"start": {"line": 1}}},
                    }], "detail-sha", "lean-source-sha")

                @staticmethod
                def candidate_names(module: str, atom: str) -> list[str]:
                    return [atom] if atom.startswith("D0.") else [f"{module}.{atom}"]

                @staticmethod
                def module_source_path(module: str | None) -> str | None:
                    return f"03_FORMALIZATION/{module.replace('.', '/')}.lean" if module else None

            view = proof.result_declaration_crosswalk_view(
                data, InventoryStub, all_current=True
            )

        self.assertEqual(view["enumerated_current_modules"], ["D0.Bar", "D0.Foo"])
        self.assertEqual(view["source_digests"], data["source_digests"])
        self.assertEqual(
            set(view["tool_source_digests"]),
            {"tools/proof_architecture.py", "tools/lean_declaration_inventory.py"},
        )
        self.assertEqual(view["result_count"], 2)
        by_id = {row["result_id"]: row for row in view["results"]}
        self.assertEqual([row["name"] for row in by_id["r-foo"]["compiled_declarations"]],
                         ["D0.Foo.bar"])
        self.assertEqual([row["name"] for row in by_id["r-bar"]["compiled_declarations"]],
                         ["D0.Bar.baz"])
        self.assertEqual(by_id["r-foo"]["claim_locator_disposition"], "candidate")
        self.assertEqual(by_id["r-bar"]["claim_locator_disposition"], "unresolved")
        self.assertEqual(by_id["r-foo"]["semantic_relation_status"], "unresolved")
        self.assertFalse(by_id["r-foo"]["acceptance_inferred"])

    def test_text_search_returns_candidate_not_accepted_relation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            (root / "02_REGISTRY").mkdir()
            (root / "02_REGISTRY" / "OWNER.md").write_text(
                "Native raising operator inverse reconstructs the null leg.\n", encoding="utf-8"
            )
            hits = proof.full_text_search(root, "native raising operator null leg")
        self.assertEqual(hits[0]["kind"], "text-candidate")
        self.assertEqual(hits[0]["source"], "02_REGISTRY/OWNER.md")
        self.assertEqual(hits[0]["matched_terms"], hits[0]["query_terms"])

    def test_batched_search_keeps_overlapping_julia_declaration_matches(self) -> None:
        case = next(
            item for item in cold_start.CASES
            if item["id"] == "julia-query-principal-frame-coframe-recovery"
        )
        declarations = [
            "principalFrameJuliaQueryFamily_nonzero_shift_chart_coverage",
            "principalFrameJuliaQueryFamily_nonNull_open_chart_joint_recovery_of_proper_roleLorentz",
        ]
        queries = {
            declaration: next(query for query in case["queries"] if declaration in query)
            for declaration in declarations
        }
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            research = root / "02_REGISTRY" / "research"
            research.mkdir(parents=True)
            source = research / "chart-coverage-owner.json"
            source.write_text(
                json.dumps({"names": declarations, "scope": "Eq27 Eq28"}) + "\n",
                encoding="utf-8",
            )
            hits_by_query = proof.full_text_search_many(root, case["queries"], limit=18)

        for query in queries.values():
            hits = hits_by_query[case["queries"].index(query)]
            direct = next(hit for hit in hits
                          if hit["source"] == source.relative_to(root).as_posix()
                          and hit["direct_content"])
            self.assertEqual(direct["matched_terms"], direct["query_terms"])

    def test_julia_null_chart_query_retrieves_its_pinned_source_section(self) -> None:
        case = next(
            item for item in cold_start.CASES
            if item["id"] == "julia-query-principal-frame-coframe-recovery"
        )
        query_index = 5
        query = case["queries"][query_index]
        required = next(
            source for source in case["required_sources"]
            if source["path"].endswith("A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md")
        )
        hits = proof.full_text_search(proof.ROOT, query, limit=18)

        status = cold_start._required_source_status(
            [(query, hits)],
            {**required, "scope_query_indexes": [0],
             "scope_query_sections": {"0": ["8.4"]}},
        )

        self.assertTrue(status["found"], f"pinned Eq. (28) source was not retrieved: {status}")
        self.assertEqual(status["status"], "found_direct_content")

    def test_multi_pattern_matcher_keeps_nested_and_partial_overlaps(self) -> None:
        variants = {
            "abc": [(0, "short")],
            "abcd": [(1, "long")],
            "cd": [(2, "middle")],
            "bcde": [(3, "shifted")],
        }
        matcher = proof._build_multi_pattern_matcher(variants)
        self.assertEqual(
            proof._multi_pattern_matches("abcde", matcher),
            {0: {"short"}, 1: {"long"}, 2: {"middle"}, 3: {"shifted"}},
        )

    def test_search_candidate_card_bounds_details_and_preserves_source_pins(self) -> None:
        candidate = {
            "kind": "text-candidate", "key": "02_REGISTRY/owner.md",
            "label": "L" * 900, "source": "02_REGISTRY/owner.md",
            "source_sha256": "a" * 64, "source_origin": "workspace",
            "direct_content": True, "matched_terms": 4,
            "matched_term_names": ["owner", "scope", "source", "map"],
            "query_terms": 4, "source_commit": "b" * 40,
            "source_blob": "c" * 40,
            "evidence_lines": [
                {"line": n, "heading": "H" * 400, "matched_terms": ["owner"],
                 "text": "T" * 400, "kind": "direct_content"}
                for n in range(10)
            ],
            "source_refs": [
                {"path": f"02_REGISTRY/source-{n}.md", "commit": "d" * 40,
                 "blob": "e" * 40, "section_refs": ["8.4"],
                 "pin_complete": True, "hashes": ["f" * 40], "context": "C" * 400}
                for n in range(10)
            ],
        }
        card = proof._search_candidate_summary(candidate)
        self.assertEqual(len(card["evidence_lines"]), proof.MAX_SEARCH_EVIDENCE)
        self.assertEqual(card["evidence_lines_omitted"], 10 - proof.MAX_SEARCH_EVIDENCE)
        self.assertLessEqual(len(card["evidence_lines"][0]["text"]),
                             proof.MAX_SEARCH_DETAIL_CHARS)
        self.assertEqual(len(card["source_refs"]), proof.MAX_SEARCH_SOURCE_REFS)
        self.assertEqual(card["source_refs_omitted"], 10 - proof.MAX_SEARCH_SOURCE_REFS)
        self.assertEqual(card["source_refs"][0]["commit"], "d" * 40)
        self.assertEqual(card["source_refs"][0]["blob"], "e" * 40)
        self.assertTrue(card["source_refs"][0]["pin_complete"])
        self.assertEqual(card["source_commit"], "b" * 40)
        self.assertEqual(card["source_blob"], "c" * 40)

    def test_structured_search_summary_exposes_registered_owner_and_scope(self) -> None:
        data = dataset()
        result = data["assembly"]["results"][0]
        result.update({
            "owner": "Recorded research owner",
            "statement": "Exact model-level statement.",
            "interface": "i1",
            "outcome": "positive",
            "scope_level": "model",
            "hypotheses": {"h": "explicit retained condition"},
            "evidence": [{
                "ref": "a" * 40,
                "path": "02_REGISTRY/research/reuse.md",
                "sha256": "b" * 64,
                "section_refs": ["L5: exact statement"],
            }],
        })
        item = next(
            row for row in proof.records(data)
            if row["kind"] == "assembly-result" and row["key"] == "r1"
        )

        summary = proof._search_summary(item)

        self.assertEqual(summary["owner"], "Recorded research owner")
        self.assertEqual(summary["interface"], "i1")
        self.assertEqual(summary["scope_level"], "model")
        self.assertEqual(summary["hypotheses"], {"h": "explicit retained condition"})
        self.assertEqual(summary["evidence"][0]["path"], "02_REGISTRY/research/reuse.md")

    def test_text_candidate_shows_only_exact_declared_owner_and_application_links(self) -> None:
        data = dataset()
        result = data["assembly"]["results"][0]
        source_path = "02_REGISTRY/research/reuse.md"
        result.update({
            "owner": "Recorded research owner",
            "interface": "i1",
            "hypotheses": {"source_condition": "retained"},
            "evidence": [{
                "ref": "a" * 40,
                "path": source_path,
                "sha256": "b" * 64,
                "section_refs": ["L5: exact source"],
            }],
        })
        data["formal_support"][0]["referenced_by"] = source_path
        candidate = {
            "kind": "text-candidate", "key": source_path, "source": source_path,
            "source_refs": [], "evidence_lines": [],
        }

        card = proof._search_candidate_summary(candidate, data)
        links = card["declared_source_links"]
        exact_result = links["assembly_results"][0]
        application = exact_result["declared_applications"][0]
        locator = links["formal_support_locators"][0]

        self.assertEqual(links["link_basis"], "exact source-path field match only")
        self.assertEqual(links["owner_status"], "declared_by_exact_assembly_evidence_link")
        self.assertEqual(links["owners"], ["Recorded research owner"])
        self.assertEqual(exact_result["result_id"], "r1")
        self.assertEqual(exact_result["evidence"][0]["path"], source_path)
        self.assertEqual(exact_result["hypotheses"], {"source_condition": "retained"})
        self.assertEqual(application["id"], "r1-to-o1")
        self.assertEqual(application["hypothesis_map"], {"h": {"target_hypothesis": "h"}})
        self.assertEqual(application["target_hypotheses"], {"h": "given"})
        self.assertEqual(locator["status"], "metadata_locator_only")

        unmatched = proof._declared_source_links(
            data, "02_REGISTRY/research/other/reuse.md"
        )
        self.assertEqual(unmatched["owner_status"], "no_exact_assembly_owner_link")
        self.assertEqual(unmatched["assembly_results"], [])

    def test_explicit_source_header_owner_stays_separate_from_assembly_owner(self) -> None:
        data = dataset()
        source_path = "02_REGISTRY/research/positive-recovery.md"
        content = (
            "# Positive recovery\n\n"
            "Date: 20 October 2026\n"
            "**Existing owner:** PR #334, `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`\n"
        )
        candidate = {
            "kind": "text-candidate", "key": source_path, "source": source_path,
            "source_refs": [], "evidence_lines": [],
            "source_header_owner_declarations":
                proof._source_header_owner_declarations(content),
        }

        card = proof._search_candidate_summary(candidate, data)

        self.assertEqual(
            card["source_header_owner_declarations"],
            [{
                "line": 4,
                "field": "Existing owner",
                "value": "PR #334, `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`",
                "status": "source_document_declaration_only",
            }],
        )
        self.assertEqual(
            card["declared_source_links"]["owner_status"],
            "no_exact_assembly_owner_link",
        )
        self.assertEqual(
            proof._source_header_owner_declarations(
                "# A memo\n\nContinuation of existing Draft #334.\n"
            ),
            [],
        )

    def test_text_search_finds_russian_content_and_reports_section_line(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            research = root / "02_REGISTRY" / "research"
            research.mkdir(parents=True)
            owner = research / "A4D_NULL_LEG_INVERSE.md"
            owner.write_text(
                "## 8.4 Точное восстановление нулевой ножки\n"
                "Обратный оператор восстанавливает поперечные компоненты.\n",
                encoding="utf-8",
            )
            hits = proof.full_text_search(root, "точное восстановление нулевой ножки", limit=5)
        self.assertEqual(hits[0]["source"], "02_REGISTRY/research/A4D_NULL_LEG_INVERSE.md")
        self.assertTrue(hits[0]["direct_content"])
        self.assertTrue(any(row["line"] == 1 and row["heading"].startswith("## 8.4")
                            for row in hits[0]["evidence_lines"]))

    def test_text_search_excludes_its_derived_comparison_reports(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            reports = (
                root
                / "02_REGISTRY/research/sources/"
                / "d0_proof_architecture_formalization_2026-10-24/reports"
            )
            reports.mkdir(parents=True)
            (reports / "comparison.json").write_text(
                '{"query":"derivedreporttoken proof architecture"}',
                encoding="utf-8",
            )

            hits = proof.full_text_search(
                root, "derivedreporttoken proof architecture", limit=10
            )

        self.assertEqual(hits, [])

    def test_text_search_follows_exact_verified_git_source_pin(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            research = root / "02_REGISTRY" / "research"
            research.mkdir(parents=True)
            source_rel = "02_REGISTRY/research/NATIVE_RAISING_OWNER.md"
            source = root / source_rel
            source.write_text(
                "## 8.4 Native raising operator inverse for the null leg\n"
                "The exact inverse recovers the null component.\n",
                encoding="utf-8",
            )
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.invalid"],
                           cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Proof Architecture Test"],
                           cwd=root, check=True)
            subprocess.run(["git", "add", source_rel], cwd=root, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "source fixture"], cwd=root, check=True)
            commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True,
                                    capture_output=True, text=True).stdout.strip()
            blob = subprocess.run(["git", "rev-parse", f"HEAD:{source_rel}"], cwd=root,
                                  check=True, capture_output=True, text=True).stdout.strip()
            (research / "ARCHITECTURE.md").write_text(
                f"Native raising operator inverse null leg uses selected owner {source_rel}; "
                f"published commit {commit}; blob {blob}; section 8.4.\n",
                encoding="utf-8",
            )
            query = "native raising operator inverse null leg"
            hits = proof.full_text_search(root, query, limit=12)

        pinned = next(hit for hit in hits
                      if hit["source"] == source_rel and hit.get("source_commit") == commit)
        self.assertEqual(pinned["source_blob"], blob)
        self.assertEqual(pinned["source_origin"], "pinned_snapshot")
        self.assertTrue(pinned["direct_content"])
        status = cold_start._required_source_status(
            [(query, hits)], {"path": source_rel, "commit": commit, "blob": blob,
                              "sections": ["8.4"]},
        )
        self.assertEqual(status["status"], "found_direct_content")

    def test_text_search_resolves_github_commit_path_links(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            research = root / "02_REGISTRY" / "research"
            research.mkdir(parents=True)
            source_rel = "02_REGISTRY/research/NATIVE_RAISING_OWNER.md"
            (root / source_rel).write_text(
                "## 8.4. Native raising operator inverse for the null leg\n"
                "The exact inverse recovers the null component.\n",
                encoding="utf-8",
            )
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.invalid"],
                           cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Proof Architecture Test"],
                           cwd=root, check=True)
            subprocess.run(["git", "add", source_rel], cwd=root, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "source fixture"], cwd=root, check=True)
            commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True,
                                    capture_output=True, text=True).stdout.strip()
            url = f"https://github.com/owner/repo/blob/{commit}/{source_rel}"
            (research / "ARCHITECTURE.md").write_text(
                f"Native raising operator inverse null leg uses the pinned source [{source_rel}]({url}).\n",
                encoding="utf-8",
            )
            query = "native raising operator inverse null leg"
            hits_by_query = proof.full_text_search_many(root, [query, query], limit=12)

        for hits in hits_by_query:
            pinned = next(hit for hit in hits
                          if hit["source"] == source_rel and hit.get("source_commit") == commit)
            self.assertEqual(pinned["source_origin"], "pinned_snapshot")
            self.assertRegex(pinned.get("source_blob", ""), r"^[0-9a-f]{40}$")
            self.assertTrue(pinned["direct_content"])
            self.assertIn("8.4", cold_start._section_refs(pinned))

    def test_section_refs_accepts_punctuated_and_nested_heading_numbers(self) -> None:
        refs = cold_start._section_refs({"evidence_lines": [
            {"heading": "### 5.1. Direct native execution"},
            {"heading": "#### 8.4.2 Full inverse map"},
        ]})
        self.assertIn("5.1", refs)
        self.assertIn("8.4", refs)
        self.assertIn("8.4.2", refs)

    def test_text_citation_alone_does_not_satisfy_required_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            research = root / "02_REGISTRY" / "research"
            research.mkdir(parents=True)
            source_rel = "02_REGISTRY/research/NATIVE_RAISING_OWNER.md"
            commit = "a" * 40
            blob = "b" * 40
            (research / "ARCHITECTURE.md").write_text(
                f"Native raising operator inverse null leg; source {source_rel}; "
                f"published commit {commit}; blob {blob}; section 8.4.\n",
                encoding="utf-8",
            )
            query = "native raising operator inverse null leg"
            hits = proof.full_text_search(root, query, limit=12)
        status = cold_start._required_source_status(
            [(query, hits)], {"path": source_rel, "commit": commit, "blob": blob,
                              "sections": ["8.4"]},
        )
        self.assertFalse(status["found"])
        self.assertEqual(status["status"], "external_reference_only")

    def test_required_source_scope_checks_each_query_and_shows_section_evidence(self) -> None:
        source_rel = "02_REGISTRY/research/NATIVE_RAISING_OWNER.md"
        commit = "a" * 40
        blob = "b" * 40

        def pinned_hit(section: str, line: int) -> dict:
            return {
                "source": source_rel, "direct_content": True,
                "source_commit": commit, "source_blob": blob,
                "source_origin": "pinned_snapshot",
                "evidence_lines": [{
                    "line": line, "heading": f"## {section}. Full tangent inverse",
                    "text": "All coframe and link tangent directions are retained.",
                    "kind": "direct_content",
                }],
            }

        required = {
            "path": source_rel, "commit": commit, "blob": blob,
            "sections": ["8.4", "8.5"],
            "scope_query_indexes": [0, 1],
            "scope_query_sections": {"0": ["8.4"], "1": ["8.5"]},
        }
        incomplete = cold_start._required_source_status(
            [("inverse null leg", [pinned_hit("8.4", 7340)]),
             ("all 16 coframe 24 links full tangent", [])],
            required,
        )
        self.assertFalse(incomplete["found"])
        self.assertEqual(incomplete["status"], "missing_scoped_query")
        self.assertFalse(incomplete["scoped_queries"][1]["found"])

        complete = cold_start._required_source_status(
            [("inverse null leg", [pinned_hit("8.4", 7340)]),
             ("all 16 coframe 24 links full tangent", [pinned_hit("8.5", 7344)])],
            required,
        )
        self.assertTrue(complete["found"])
        self.assertIn("8.4", complete["sections_found"])
        self.assertIn("8.5", complete["sections_found"])
        self.assertIn(7344, [line["line"] for line in complete["evidence_lines"]])

    def test_text_search_prefers_current_owner_and_keeps_pin_context(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            owner = root / "02_REGISTRY" / "research"
            copied = root / "02_REGISTRY" / "research" / "sources" / "snapshot"
            owner.mkdir(parents=True)
            copied.mkdir(parents=True)
            term = "A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md"
            (owner / "D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md").write_text(
                f"Selected source 02_REGISTRY/research/{term}; published commit fe5cf335da04cac14e50407b03f98b96be17dc52; blob 1c8d59e5533b443d9a015dc4512cfbc160ae7e62; sections 8.4-8.5.\n",
                encoding="utf-8",
            )
            (copied / "old.md").write_text(f"See {term}.\n", encoding="utf-8")
            hits = proof.full_text_search(root, term)
        self.assertEqual(hits[0]["source"],
                         "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md")
        self.assertIn("blob 1c8d59e5533b443d9a015dc4512cfbc160ae7e62", hits[0]["label"])
        self.assertEqual(hits[0]["source_refs"][0]["path"],
                         "02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md")
        self.assertIn("1c8d59e5533b443d9a015dc4512cfbc160ae7e62",
                      hits[0]["source_refs"][0]["hashes"])

    def test_text_filename_can_disambiguate_a_pinned_owner(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            research = root / "02_REGISTRY" / "research"
            research.mkdir(parents=True)
            (research / "D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md").write_text(
                "Native raising operator inverse null leg appears in this summary.",
                encoding="utf-8",
            )
            owner = research / "A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md"
            owner.write_text(
                "Native raising operator inverse reconstructs the null leg.",
                encoding="utf-8",
            )
            hits = proof.full_text_search(root, "native raising operator inverse null leg")
        self.assertEqual(hits[0]["source"],
                         "02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md")

    def test_text_search_can_find_a_source_by_its_title(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            research = root / "02_REGISTRY" / "research"
            research.mkdir(parents=True)
            owner = research / "A4D_NATIVE_PAIRING_REFINEMENT_SOURCE.md"
            owner.write_text("Different operator details live here.", encoding="utf-8")
            hits = proof.full_text_search(root, "native pairing refinement source")
        self.assertEqual(hits[0]["source"],
                         "02_REGISTRY/research/A4D_NATIVE_PAIRING_REFINEMENT_SOURCE.md")
        self.assertFalse(hits[0]["direct_content"])
        self.assertEqual(hits[0]["source_origin"], "filename_only")
        self.assertEqual(hits[0]["evidence_lines"][0]["kind"], "filename_only")

    def test_english_scope_query_finds_russian_full_tangent_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            research = root / "02_REGISTRY" / "research"
            research.mkdir(parents=True)
            source = research / "NATIVE_FULL_TANGENT_SOURCE.md"
            source.write_text(
                "## 8.5 Полнота геометрического чтения\n"
                "На полном касательном пространстве сохраняются все16 coframe "
                "и24 link направления на узел, а не только null- или "
                "pp-wave-ansatz variations. При изменении observer n сохраняются jets.\n",
                encoding="utf-8",
            )
            query = ("all 16 coframe 24 link directions at node not only null "
                     "pp-wave ansatz variations observer jets tangent")
            hits = proof.full_text_search(root, query, limit=5)

        owner = next(hit for hit in hits
                     if hit["source"] == "02_REGISTRY/research/NATIVE_FULL_TANGENT_SOURCE.md")
        self.assertTrue(owner["direct_content"])
        self.assertIn("direction", owner["matched_term_names"])
        self.assertIn("observer", owner["matched_term_names"])
        self.assertIn("tangent", owner["matched_term_names"])

    def test_source_reference_ranking_keeps_late_context_relevant_exact_pin(self) -> None:
        query = "all 16 coframe 24 link directions at node not only null pp-wave ansatz variations"
        terms = proof._query_terms(query)
        pattern = proof._term_pattern(terms)
        lines = [
            f"all coframe direction link in broad context; source docs/archive_{index}.md"
            for index in range(20)
        ]
        owner = "02_REGISTRY/research/NATIVE_FULL_TANGENT_SOURCE.md"
        commit = "a" * 40
        blob = "b" * 40
        lines.append(
            "all 16 coframe 24 link directions at node not only null pp-wave "
            f"ansatz variations; source {owner}; published commit {commit}; blob {blob}; §8.5"
        )

        references = proof._source_references(lines, terms, pattern)

        self.assertEqual(references[0]["path"], owner)
        self.assertEqual(references[0]["commit"], commit)
        self.assertEqual(references[0]["blob"], blob)
        self.assertIn("8.5", references[0]["section_refs"])

    def test_cold_start_uses_minimum_window_for_pinned_source_retrieval(self) -> None:
        def empty_hits(_root: pathlib.Path, queries: list[str], _limit: int):
            return [[] for _ in queries]

        snapshot = {"snapshot_commit": "test", "worktree_dirty": False,
                    "source_digests": {}}
        with patch.object(cold_start.proof, "full_text_search_many",
                          side_effect=empty_hits) as search, \
             patch.object(cold_start.proof, "load_dataset", return_value=snapshot):
            cold_start.run(pathlib.Path("."), limit=5)

        self.assertEqual(search.call_args.args[2], 18)

    def test_process_comparison_uses_only_query_scoped_sources(self) -> None:
        case = {
            "required_refs": ["unscoped.md"],
            "required_sources": [
                {"path": "owner/source.md", "scope_query_indexes": [1]},
                {"path": "owner/other.md", "scope_query_indexes": [1, 2]},
            ],
        }

        self.assertEqual(process_comparison.expected_sources(case, 0), [])
        self.assertEqual(
            process_comparison.expected_sources(case, 1),
            ["owner/other.md", "owner/source.md"],
        )
        self.assertEqual(
            process_comparison.expected_sources(case, 2), ["owner/other.md"]
        )
        self.assertTrue(
            process_comparison._matches_expected(
                ["02_REGISTRY/owner/source.md"], ["owner/source.md"]
            )
        )
        self.assertFalse(
            process_comparison._matches_expected(
                ["02_REGISTRY/other/source.md"], ["owner/source.md"]
            )
        )

    def test_process_comparison_selects_a_scoped_question_per_episode(self) -> None:
        case = {
            "queries": ["broad question", "source-specific question", "alternate"],
            "required_sources": [
                {"path": "owner/source.md", "scope_query_indexes": [1, 2]},
            ],
        }
        fallback = {"queries": ["first", "second"], "required_sources": []}

        self.assertEqual(process_comparison.selected_query(case), (1, "source-specific question"))
        self.assertEqual(process_comparison.selected_query(fallback), (0, "first"))

    def test_process_comparison_separates_assembly_owners_from_support_locators(self) -> None:
        def detail(source: str, *, owner: bool = False,
                   support: int = 0, source_header: bool = False) -> dict:
            return {
                "source": source,
                "owners": ["registered owner"] if owner else [],
                "formal_support_locators": [{} for _ in range(support)],
                "source_header_owner_declarations": ([{"value": "source claim"}]
                                                      if source_header else []),
            }

        scoped = [
            {
                "expected_sources": ["support.md", "assembly.md"],
                "current": {
                    "expected_source_assembly_owner_links": [{"source": "assembly.md"}],
                    "expected_source_link_details": [
                        detail("support.md", support=2),
                        detail("assembly.md", owner=True),
                    ],
                    "expected_sources_without_assembly_owner_link": ["support.md"],
                },
            },
            {
                "expected_sources": ["support.md", "unlinked.md"],
                "current": {
                    "expected_source_assembly_owner_links": [],
                    "expected_source_link_details": [
                        detail("support.md", support=2),
                        detail("unlinked.md", source_header=True),
                    ],
                    "expected_sources_without_assembly_owner_link": [
                        "support.md", "unlinked.md"
                    ],
                },
            },
        ]

        metrics = process_comparison.exact_source_link_metrics(scoped)

        self.assertEqual(metrics["expected_source_reference_count"], 4)
        self.assertEqual(metrics["unique_expected_source_path_count"], 3)
        self.assertEqual(
            metrics["current_scoped_queries_with_expected_source_assembly_owner_link"],
            1,
        )
        self.assertEqual(metrics["current_expected_source_assembly_owner_link_count"], 1)
        self.assertEqual(
            metrics["current_expected_source_references_with_formal_support_locator"],
            2,
        )
        self.assertEqual(metrics["current_expected_source_formal_support_locator_count"], 4)
        self.assertEqual(
            metrics["current_unique_expected_source_paths_with_formal_support_locator"],
            1,
        )
        self.assertEqual(
            metrics["current_expected_source_references_without_assembly_or_formal_support"],
            1,
        )
        self.assertEqual(
            metrics["current_unique_expected_source_paths_without_assembly_or_formal_support"],
            1,
        )
        self.assertEqual(
            metrics["current_expected_source_header_owner_declaration_count"], 1
        )

    def test_default_search_window_surfaces_scoped_julia_source(self) -> None:
        case = next(
            item for item in cold_start.CASES
            if item["id"] == "julia-query-principal-frame-coframe-recovery"
        )
        source = next(item for item in case["required_sources"]
                      if 1 in item.get("scope_query_indexes", []))
        query = case["queries"][1]
        hits = proof.full_text_search(proof.ROOT, query)

        self.assertEqual(proof.MAX_SEARCH_RESULTS, 5)
        self.assertLessEqual(len(hits), proof.MAX_SEARCH_RESULTS)
        owner_source = next(
            (hit for hit in hits
             if cold_start._path_matches(hit["source"], source["path"])),
            None,
        )
        self.assertIsNotNone(owner_source)
        self.assertTrue(owner_source["direct_content"])
        self.assertEqual(owner_source["source_origin"], "pinned_snapshot")
        self.assertEqual(owner_source["pin_status"], "verified")
        self.assertEqual(owner_source["source_commit"], source["commit"])
        self.assertEqual(owner_source["source_blob"], source["blob"])

    def test_nonnull_julia_query_surfaces_pinned_section(self) -> None:
        case = next(item for item in cold_start.CASES
                    if item["id"] == "julia-query-principal-frame-coframe-recovery")
        source = next(item for item in case["required_sources"]
                      if 8 in item.get("scope_query_indexes", []))
        query = case["queries"][8]
        hits = proof.full_text_search(proof.ROOT, query, limit=18)
        scoped_source = {**source, "scope_query_indexes": [8],
                         "sections": ["8.4"], "scope_query_sections": {"8": ["8.4"]}}
        result = cold_start._required_source_status([("", [])] * 8 + [(query, hits)], scoped_source)
        self.assertTrue(result["found"], result)
        self.assertEqual(result["source_origin"], "pinned_snapshot")
        self.assertEqual(result["expected_commit"], source["commit"])
        self.assertEqual(result["expected_blob"], source["blob"])
        self.assertEqual(result["missing_sections"], [])

    def test_nonvacuum_inventory_query_returns_direct_content(self) -> None:
        case = next(item for item in cold_start.CASES
                    if item["id"] == "positive-nonvacuum-recovery")
        query = case["queries"][-1]
        path = ("02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/"
                "nonvacuum_brinkmann_stencil_midpoint_refinement_declarations_2026-10-26.json")
        hits = proof.full_text_search(proof.ROOT, query, limit=18)
        result = cold_start._required_source_status([(query, hits)], {"path": path})
        self.assertTrue(result["found"], result)
        self.assertEqual(result["source_origin"], "workspace")
        self.assertLessEqual(result["candidate_rank"], 18)

    def test_nonvacuum_stencil_cold_start_retrieves_the_compiled_application(self) -> None:
        case = next(
            item for item in cold_start.CASES
            if item["id"] == "positive-nonvacuum-recovery"
        )
        module = "03_FORMALIZATION/D0/Geometry/NonvacuumBrinkmannStencil.lean"
        support_rows = proof.load_dataset()["formal_support"]
        self.assertTrue(any(row["lean_file"] == module.removeprefix("03_FORMALIZATION/")
                            for row in support_rows))
        self.assertTrue(any("transverseFivePoint_nonvacuumBrinkmannProfile_eq_source" in query
                            for query in case["queries"]))
        self.assertTrue(any("nonvacuumProfile_source_eq_finiteMidpointMatterNorm" in query
                            for query in case["queries"]))
        self.assertTrue(any("finiteTimeNonvacuumProfile_source_eq_midpointHistoryNorm" in query
                            for query in case["queries"]))
        self.assertTrue(any("finiteMatterMidpointHistory_eq_base_add_rateSum" in query
                            for query in case["queries"]))
        self.assertTrue(any("twoComponentMatterHistorySquaredGradientSum_eq_rateEnergySum" in query
                            for query in case["queries"]))
        self.assertTrue(any("finiteMatterMidpointHistory_error_le_refinementBound" in query
                            for query in case["queries"]))
        self.assertTrue(any("midpointQuadrature_error_abs_le_of_thirdDerivative_bound" in query
                            for query in case["queries"]))
        self.assertTrue(any("D0.Analysis.MidpointQuadrature" in query
                            for query in case["queries"]))
        self.assertTrue(any("sampledMatterMidpointHistory_error_le_refinementBound" in query
                            for query in case["queries"]))
        self.assertTrue(any(
            "sampledVectorMidpointHistory_error_le_refinementBound" in query
            for query in case["queries"]
        ))
        self.assertTrue(any(
            "sampledMatterMidpointCARComplement_positive_of_vectorMargin" in query
            for query in case["queries"]
        ))
        self.assertTrue(any(
            "sampledMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes"
            in query for query in case["queries"]
        ))
        self.assertTrue(any(
            "sampledMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes_on_interval"
            in query for query in case["queries"]
        ))
        self.assertTrue(any(
            "sampledMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes_of_pointwiseMargin"
            in query for query in case["queries"]
        ))
        self.assertIn(
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/"
            "nonvacuum_interval_local_car_refinement_2026-10-27.json",
            case["required_refs"],
        )
        self.assertIn(
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/"
            "nonvacuum_compact_pointwise_margin_2026-10-27.json",
            case["required_refs"],
        )
        compact_margin_source = next(
            source for source in case["required_sources"]
            if source["path"].endswith("nonvacuum_compact_pointwise_margin_2026-10-27.json")
        )
        self.assertEqual(
            compact_margin_source["commit"],
            "a2c20a4dc9feeb5446b41e9e49ea8094bd14f40b",
        )
        self.assertEqual(
            compact_margin_source["blob"],
            "82574aafa3ea94c61ca28ad9e08980c2974d4b22",
        )
        self.assertEqual(compact_margin_source["scope_query_indexes"], [17])
        self.assertIn(module, case["required_refs"])
        self.assertIn("03_FORMALIZATION/D0/Analysis/MidpointQuadrature.lean",
                      case["required_refs"])
        self.assertIn(
            "D0.Analysis.MidpointQuadrature,D0/Analysis/MidpointQuadrature.lean,"
            "EXPLICIT_SUPPORT,03_FORMALIZATION/D0/Geometry/NonvacuumBrinkmannStencil.lean;"
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md",
            (proof.ROOT / "02_REGISTRY/formal_support.csv").read_text(encoding="utf-8"),
        )
        self.assertIn(
            "import D0.Analysis.MidpointQuadrature",
            (proof.ROOT / "03_FORMALIZATION/D0/All.lean").read_text(encoding="utf-8"),
        )
        self.assertIn(
            "D0.Analysis.midpointQuadrature_error_abs_le_of_thirdDerivative_bound",
            (proof.ROOT / module).read_text(encoding="utf-8"),
        )
        self.assertIn("all 16+24+2 Euler rows", case["scope_review"])
        self.assertIn(
            "shared D0.Analysis Taylor theorem derives its O(h^3) defect from C^3 regularity",
            case["scope_review"],
        )
        self.assertIn("dimension-free constant in Euclidean norm", case["scope_review"])
        self.assertIn("transported through an isometric Euclidean lift", case["scope_review"])
        self.assertIn("every N >= N0 with h=duration/N", case["scope_review"])
        self.assertIn("physical native Book/clock/source selection remain separate and open",
                      case["scope_review"])

        hits_by_query = proof.full_text_search_many(
            proof.ROOT, case["queries"], limit=18
        )
        query_pairs = list(zip(case["queries"], hits_by_query))
        for path in case["required_refs"]:
            status = cold_start._required_source_status(query_pairs, {"path": path})
            self.assertTrue(status["found"], f"cold-start search missed {path}")
        module_hits = [hit for hits in hits_by_query for hit in hits
                       if hit.get("source") == module and hit.get("direct_content")]
        self.assertTrue(module_hits, "cold-start result must surface the Lean module itself")

        for source in case["required_sources"]:
            source_status = cold_start._required_source_status(query_pairs, source)
            self.assertTrue(
                source_status["found"],
                f"cold-start missed pinned §§7.1–7.2: {source_status}",
            )

        inventory_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "nonvacuum_brinkmann_stencil_midpoint_refinement_current_declarations_2026-10-26.json"
        )
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        self.assertEqual(inventory["schema"], "d0-lean-declaration-inventory-v1")
        self.assertEqual(
            inventory["snapshot_commit"],
            "7094905859ac217241e2d467161662b794c7c61e",
        )
        self.assertEqual(inventory["public_import_root"], "D0.All")
        self.assertFalse(inventory["worktree_dirty"])
        self.assertEqual(
            inventory["lean_source_digest"],
            "d5de0891dde960dc4f7495f9eda1afdaec7fe11d15bd9e1d061810852e232c9c",
        )
        declarations = {row["name"]: row for row in inventory["declarations"]}
        module_name = "D0.Geometry.NonvacuumBrinkmannStencil"
        required_theorems = {
            "D0.Geometry.transverseFivePoint_harmonicBrinkmannCubic_eq_zero",
            "D0.Geometry.transverseFivePoint_radialQuadratic_eq_four",
            "D0.Geometry.transverseFivePoint_nonvacuumBrinkmannProfile_eq_source",
            "D0.Geometry.finiteMatterForwardGradient_midpointStep",
            "D0.Geometry.twoComponentMatterNormSq_midpointGradient_eq_rate",
            "D0.Geometry.nonvacuumProfile_source_eq_finiteMidpointMatterNorm",
            "D0.Geometry.cubicMatterMidpointSample_eq_profile_sub_cubic_error",
            "D0.Geometry.cubicMatterMidpointSample_error_bound",
            "D0.Geometry.nonvacuumCubicMidpointSource_matches_record",
            "D0.Geometry.finiteMatterMidpointHistory_eq_base_add_rateSum",
            "D0.Geometry.finiteTimeNonvacuumProfile_source_eq_midpointHistoryNorm",
            "D0.Geometry.twoComponentMatterHistorySquaredGradientSum_eq_rateEnergySum",
        }
        self.assertTrue(required_theorems.issubset(declarations))
        historical_nonvacuum = json.loads(
            (
                proof.ROOT
                / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
                / "nonvacuum_brinkmann_stencil_declarations_2026-10-25.json"
            ).read_text(encoding="utf-8")
        )
        stable_nonvacuum_names = {
            row["name"]
            for row in historical_nonvacuum["declarations"]
            if row.get("module") == module_name
            and not row["name"].startswith("_private.")
            and not row["name"].endswith(".match_1")
        }
        self.assertEqual(len(stable_nonvacuum_names), 30)
        self.assertTrue(stable_nonvacuum_names.issubset(declarations))
        self.assertTrue(all(declarations[name]["exists"] for name in stable_nonvacuum_names))
        standard_axioms = {"Classical.choice", "Quot.sound", "propext"}
        for name in required_theorems:
            row = declarations[name]
            self.assertEqual(row["module"], module_name)
            self.assertEqual(set(row["axioms"]), standard_axioms)
            self.assertEqual(row["source_path"], module)
            self.assertGreater(row["declaration_ranges"]["declaration"]["start"]["line"], 0)
        sourced = declarations[
            "D0.Geometry.nonvacuumProfile_source_eq_finiteMidpointMatterNorm"
        ]
        self.assertIn(
            "D0.Geometry.transverseFivePoint_nonvacuumBrinkmannProfile_eq_source",
            sourced["proof_dependencies"],
        )
        self.assertIn(
            "D0.Geometry.twoComponentMatterNormSq_midpointGradient_eq_rate",
            sourced["proof_dependencies"],
        )
        self.assertIn("h ≠ 0", sourced["elaborated_type"])
        cubic_source = declarations[
            "D0.Geometry.nonvacuumCubicMidpointSource_matches_record"
        ]
        self.assertEqual(cubic_source["module"], module_name)
        self.assertIn("h ≠ 0", cubic_source["elaborated_type"])
        self.assertIn(
            "D0.Geometry.nonvacuumProfile_source_eq_finiteMidpointMatterNorm",
            cubic_source["proof_dependencies"],
        )

        cubic_refinement_inventory_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "nonvacuum_cubic_profile_same_record_euclidean_refinement_2026-10-27.json"
        )
        cubic_refinement_inventory = json.loads(
            cubic_refinement_inventory_path.read_text(encoding="utf-8")
        )
        self.assertEqual(
            cubic_refinement_inventory["snapshot_commit"],
            "423ec9a87553a14c6f484e429a6d3309eeae256a",
        )
        self.assertEqual(
            cubic_refinement_inventory["lean_source_digest"],
            "4ec16ca28dc47e05615ac0d08d665b0ce9b897bca0d43d8f51f7e3c37e4b97c5",
        )
        self.assertFalse(cubic_refinement_inventory["worktree_dirty"])
        cubic_refinement_declarations = {
            row["name"]: row for row in cubic_refinement_inventory["declarations"]
        }
        same_record_refinement_names = {
            "D0.Geometry.cubicMatterMidpointSample_euclideanError_eq_remainder",
            "D0.Geometry.cubicMatterMidpointSample_euclideanError_le_refinementBound",
            "D0.Geometry.nonvacuumCubicCARComplement_positive_with_sameRecordStencilSource_and_refinement",
        }
        self.assertTrue(same_record_refinement_names.issubset(cubic_refinement_declarations))
        for name in same_record_refinement_names:
            row = cubic_refinement_declarations[name]
            self.assertEqual(row["module"], module_name)
            self.assertEqual(set(row["axioms"]), standard_axioms)
            self.assertEqual(row["source_path"], module)
        composed_refinement = cubic_refinement_declarations[
            "D0.Geometry.nonvacuumCubicCARComplement_positive_with_sameRecordStencilSource_and_refinement"
        ]
        self.assertIn(
            "D0.Geometry.cubicMatterMidpointSample_euclideanError_le_refinementBound",
            composed_refinement["proof_dependencies"],
        )

        historical_cubic_inventory = json.loads(
            (
                proof.ROOT
                / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
                / "nonvacuum_brinkmann_stencil_cubic_midpoint_declarations_2026-10-26.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            historical_cubic_inventory["snapshot_commit"],
            "c42d0e3f91f937676f8a3c14255835144bb65e9b",
        )
        self.assertEqual(
            historical_cubic_inventory["lean_source_digest"],
            "62572197322b69a5ed4427cb71eafbb2b8100a86972f03c5dff4b1e291d62db2",
        )
        self.assertFalse(historical_cubic_inventory["worktree_dirty"])
        historical_cubic_names = {
            row["name"] for row in historical_cubic_inventory["declarations"]
        }
        self.assertTrue(historical_cubic_names.issubset(declarations))

        refinement_declarations = {
            "D0.Geometry.finiteMatterMidpointLocalDefect",
            "D0.Geometry.finiteMatterMidpointHistory_error_eq_localDefectSum",
            "D0.Geometry.finiteMatterMidpointHistory_error_abs_le_localDefectSum",
            "D0.Geometry.finiteMatterMidpointHistory_error_abs_le_localDefectBound",
            "D0.Geometry.finiteMatterMidpointHistory_error_le_refinementBound",
        }
        self.assertTrue(refinement_declarations.issubset(declarations))
        for name in refinement_declarations:
            row = declarations[name]
            self.assertEqual(row["module"], module_name)
            self.assertEqual(set(row["axioms"]), standard_axioms)
            self.assertEqual(row["source_path"], module)
            self.assertGreater(row["declaration_ranges"]["declaration"]["start"]["line"], 0)
        refinement = declarations[
            "D0.Geometry.finiteMatterMidpointHistory_error_le_refinementBound"
        ]
        self.assertIn(
            "D0.Geometry.finiteMatterMidpointHistory_error_abs_le_localDefectBound",
            refinement["proof_dependencies"],
        )
        self.assertIn("∀ n ≤ N", refinement["elaborated_type"])
        self.assertIn("M * h ^ 3 / 24", refinement["elaborated_type"])
        self.assertIn("duration * M * h ^ 2 / 24", refinement["elaborated_type"])

        historical_energy_inventory = json.loads(
            (
                proof.ROOT
                / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
                / "nonvacuum_brinkmann_stencil_current_declarations_2026-10-26.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            historical_energy_inventory["snapshot_commit"],
            "fea233e0d5909ac07963c06dbe42cd9a6b8fc9d0",
        )
        self.assertEqual(
            historical_energy_inventory["lean_source_digest"],
            "9bf1508a0ee6d25ab420dac401d83f5add1e12216731a9da1aa6dd46e0abdfe6",
        )
        self.assertFalse(historical_energy_inventory["worktree_dirty"])
        historical_energy_names = {
            row["name"] for row in historical_energy_inventory["declarations"]
        }
        self.assertTrue(historical_energy_names.issubset(declarations))

        historical_refinement_inventory = json.loads(
            (
                proof.ROOT
                / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
                / "nonvacuum_brinkmann_stencil_midpoint_refinement_declarations_2026-10-26.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            historical_refinement_inventory["snapshot_commit"],
            "d27cafffe9592416556c9f5eb4bd069a355dca44",
        )
        self.assertEqual(
            historical_refinement_inventory["lean_source_digest"],
            "369d1159021853c3ec8726a1b9c32518dfb288a0238fdd43440f31df7c4b33e5",
        )
        self.assertFalse(historical_refinement_inventory["worktree_dirty"])
        historical_refinement_names = {
            row["name"] for row in historical_refinement_inventory["declarations"]
        }
        self.assertTrue(historical_refinement_names.issubset(declarations))

        c3_inventory_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "nonvacuum_brinkmann_stencil_midpoint_c3_error_declarations_2026-10-26.json"
        )
        c3_inventory = json.loads(c3_inventory_path.read_text(encoding="utf-8"))
        self.assertEqual(c3_inventory["schema"], "d0-lean-declaration-inventory-v1")
        self.assertEqual(c3_inventory["public_import_root"], "D0.All")
        self.assertFalse(c3_inventory["worktree_dirty"])
        self.assertEqual(c3_inventory["snapshot_commit"],
                         "986c05d72956f95c1eeeab7e17df0e3824992db5")
        self.assertEqual(
            c3_inventory["lean_source_digest"],
            "00788714716bf31665b8f7bedcf058b9e40dd454e2d7f737e15a20dae88d2e0f",
        )
        c3_declarations = {row["name"]: row for row in c3_inventory["declarations"]}
        c3_required = {
            "D0.Geometry.midpointQuadrature_error_abs_le_of_thirdDerivative_bound",
            "D0.Geometry.sampledMatterExactValues",
            "D0.Geometry.sampledMatterMidpointRate",
            "D0.Geometry.sampledMatterMidpointLocalDefect_abs_le",
            "D0.Geometry.sampledMatterMidpointHistory_error_le_refinementBound",
        }
        self.assertTrue(c3_required.issubset(c3_declarations))
        for name in c3_required:
            row = c3_declarations[name]
            self.assertEqual(row["module"], module_name)
            self.assertEqual(set(row["axioms"]), standard_axioms)
            self.assertEqual(row["source_path"], module)
            self.assertGreater(row["declaration_ranges"]["declaration"]["start"]["line"], 0)
        c3_local = c3_declarations[
            "D0.Geometry.midpointQuadrature_error_abs_le_of_thirdDerivative_bound"
        ]
        c3_sampled = c3_declarations[
            "D0.Geometry.sampledMatterMidpointLocalDefect_abs_le"
        ]
        self.assertIn(
            "D0.Geometry.midpointQuadrature_error_abs_le_of_thirdDerivative_bound",
            c3_sampled["proof_dependencies"],
        )
        self.assertIn("ContDiff", c3_local["elaborated_type"])
        self.assertIn("iteratedDeriv", c3_local["elaborated_type"])
        self.assertIn("Set.Icc", c3_local["elaborated_type"])
        self.assertIn("0 ≤ h", c3_local["elaborated_type"])
        self.assertIn("M * h ^ 3 / 24", c3_local["elaborated_type"])
        c3_global = c3_declarations[
            "D0.Geometry.sampledMatterMidpointHistory_error_le_refinementBound"
        ]
        self.assertIn(
            "D0.Geometry.finiteMatterMidpointHistory_error_le_refinementBound",
            c3_global["proof_dependencies"],
        )
        self.assertIn(
            "D0.Geometry.sampledMatterMidpointLocalDefect_abs_le",
            c3_global["proof_dependencies"],
        )
        self.assertIn("duration * M * h ^ 2 / 24", c3_global["elaborated_type"])

        pre_refactor_inventory_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "nonvacuum_brinkmann_stencil_midpoint_c3_error_pre_refactor_declarations_2026-10-26.json"
        )
        pre_refactor_inventory = json.loads(
            pre_refactor_inventory_path.read_text(encoding="utf-8")
        )
        self.assertEqual(
            pre_refactor_inventory["snapshot_commit"],
            "9b0eeec8fb7bc234cfe532c5b7497a19ca6796ed",
        )
        self.assertEqual(
            pre_refactor_inventory["lean_source_digest"],
            "f2a18ec9b50d8235603fb1d64ac2b3d75020100738afd95280d542a150c2769c",
        )
        self.assertFalse(pre_refactor_inventory["worktree_dirty"])
        self.assertEqual(
            hashlib.sha256(pre_refactor_inventory_path.read_bytes()).hexdigest(),
            "9aedab993f6af0d896a09fb850fc40ca3ef4d4632a9159d2312126892caa7bb7",
        )

        refactor_inventory_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "nonvacuum_brinkmann_stencil_midpoint_c3_refactor_declarations_2026-10-26.json"
        )
        refactor_inventory = json.loads(
            refactor_inventory_path.read_text(encoding="utf-8")
        )
        self.assertEqual(refactor_inventory["schema"], "d0-lean-declaration-inventory-v1")
        self.assertEqual(refactor_inventory["public_import_root"], "D0.All")
        self.assertFalse(refactor_inventory["worktree_dirty"])
        self.assertEqual(
            refactor_inventory["snapshot_commit"],
            "102e76893f1fd68d4ab7762e5d2dfd370bc9778b",
        )
        self.assertEqual(
            refactor_inventory["lean_source_digest"],
            "6120fc0d9b4961e5563cb43bb4abcd59f657a240b275ecd7e28f7dd8ff461a33",
        )
        self.assertEqual(len(refactor_inventory["declarations"]), 48)
        self.assertEqual(
            hashlib.sha256(refactor_inventory_path.read_bytes()).hexdigest(),
            "8e4a7319d50069718da54d60c067816f0ded8bf09c157e8eaeba3ffdb0a461f9",
        )
        refactor_declarations = {
            row["name"]: row for row in refactor_inventory["declarations"]
        }
        generic_midpoint = refactor_declarations[
            "D0.Analysis.midpointQuadrature_error_abs_le_of_thirdDerivative_bound"
        ]
        self.assertEqual(generic_midpoint["module"], "D0.Analysis.MidpointQuadrature")
        self.assertEqual(
            generic_midpoint["source_path"],
            "03_FORMALIZATION/D0/Analysis/MidpointQuadrature.lean",
        )
        self.assertEqual(set(generic_midpoint["axioms"]), standard_axioms)
        self.assertIn("ContDiff", generic_midpoint["elaborated_type"])
        self.assertIn("M * h ^ 3 / 24", generic_midpoint["elaborated_type"])

        self.assertNotIn(
            "D0.Geometry.midpointQuadrature_error_abs_le_of_thirdDerivative_bound",
            refactor_declarations,
        )
        sampled_local = refactor_declarations[
            "D0.Geometry.sampledMatterMidpointLocalDefect_abs_le"
        ]
        self.assertEqual(sampled_local["module"], module_name)
        self.assertEqual(sampled_local["source_path"], module)
        self.assertEqual(set(sampled_local["axioms"]), standard_axioms)
        self.assertIn(
            "D0.Analysis.midpointQuadrature_error_abs_le_of_thirdDerivative_bound",
            sampled_local["proof_dependencies"],
        )
        sampled_history = refactor_declarations[
            "D0.Geometry.sampledMatterMidpointHistory_error_le_refinementBound"
        ]
        self.assertIn(
            "D0.Geometry.sampledMatterMidpointLocalDefect_abs_le",
            sampled_history["proof_dependencies"],
        )
        self.assertIn(
            "D0.Geometry.finiteMatterMidpointHistory_error_le_refinementBound",
            sampled_history["proof_dependencies"],
        )
        self.assertEqual(set(sampled_history["axioms"]), standard_axioms)

        history_inventory_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "nonvacuum_brinkmann_stencil_midpoint_history_declarations_2026-10-26.json"
        )
        history_inventory = json.loads(history_inventory_path.read_text(encoding="utf-8"))
        self.assertEqual(history_inventory["schema"], "d0-lean-declaration-inventory-v1")
        self.assertEqual(history_inventory["public_import_root"], "D0.All")
        self.assertEqual(
            history_inventory["snapshot_commit"],
            "82c617ae0c9ce120730819f68f7a80e76c9473eb",
        )
        self.assertEqual(
            history_inventory["lean_source_digest"],
            "6c73bc54dfdcbe972a58bdd615c173c2bf8cf051a3c394a57120a2112e664644",
        )
        self.assertFalse(history_inventory["worktree_dirty"])
        history_declarations = {row["name"]: row for row in history_inventory["declarations"]}
        required_history_declarations = {
            "D0.Geometry.finiteMatterMidpointHistory",
            "D0.Geometry.finiteMatterMidpointHistory_next",
            "D0.Geometry.finiteMatterMidpointHistory_eq_base_add_rateSum",
            "D0.Geometry.finiteMatterForwardGradient_midpointHistory",
            "D0.Geometry.twoComponentMatterNormSq_midpointHistoryGradient_eq_rate",
            "D0.Geometry.twoComponentMatterHistorySquaredGradientSum_eq_rateEnergySum",
            "D0.Geometry.finiteTimeNonvacuumBrinkmannProfile",
            "D0.Geometry.finiteTimeNonvacuumProfile_source_eq_midpointHistoryNorm",
        }
        self.assertTrue(required_history_declarations.issubset(history_declarations))
        for name in required_history_declarations:
            row = history_declarations[name]
            self.assertEqual(row["module"], module_name)
            self.assertEqual(set(row["axioms"]), standard_axioms)
            self.assertEqual(row["source_path"], module)
            self.assertGreater(row["declaration_ranges"]["declaration"]["start"]["line"], 0)
        chronological_source = history_declarations[
            "D0.Geometry.finiteTimeNonvacuumProfile_source_eq_midpointHistoryNorm"
        ]
        self.assertIn(
            "D0.Geometry.transverseFivePoint_nonvacuumBrinkmannProfile_eq_source",
            chronological_source["proof_dependencies"],
        )
        self.assertIn(
            "D0.Geometry.twoComponentMatterNormSq_midpointHistoryGradient_eq_rate",
            chronological_source["proof_dependencies"],
        )
        self.assertIn("ℕ", chronological_source["elaborated_type"])
        self.assertIn("h ≠ 0", chronological_source["elaborated_type"])
        accumulated_history = history_declarations[
            "D0.Geometry.finiteMatterMidpointHistory_eq_base_add_rateSum"
        ]
        self.assertIn("D0.Geometry.finiteMatterMidpointHistory_next",
                      accumulated_history["proof_dependencies"])
        self.assertIn("Finset.range", accumulated_history["elaborated_type"])
        accumulated_energy = history_declarations[
            "D0.Geometry.twoComponentMatterHistorySquaredGradientSum_eq_rateEnergySum"
        ]
        self.assertIn(
            "D0.Geometry.twoComponentMatterNormSq_midpointHistoryGradient_eq_rate",
            accumulated_energy["proof_dependencies"],
        )
        self.assertIn("Finset.range", accumulated_energy["elaborated_type"])

    def test_nonvacuum_vector_norm_c3_and_car_margin_inventory_is_compiled(self) -> None:
        inventory_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "nonvacuum_vector_norm_uniform_mesh_2026-10-26.json"
        )
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        self.assertEqual(inventory["schema"], "d0-lean-declaration-inventory-v1")
        self.assertEqual(inventory["public_import_root"], "D0.All")
        self.assertFalse(inventory["worktree_dirty"])
        self.assertRegex(inventory["snapshot_commit"], r"^[0-9a-f]{40}$")
        self.assertRegex(inventory["lean_source_digest"], r"^[0-9a-f]{64}$")
        self.assertRegex(inventory["collector_sha256"], r"^[0-9a-f]{64}$")

        declarations = {row["name"]: row for row in inventory["declarations"]}
        required = {
            "D0.Analysis.midpointQuadrature_error_norm_le_of_thirdDerivative_bound",
            "D0.Analysis.finiteVectorMidpointHistory_error_eq_localDefectSum",
            "D0.Analysis.sampledVectorMidpointHistory_error_le_refinementBound",
            "D0.Geometry.twoComponentMatterEuclidean_norm_sq",
            "D0.Geometry.vectorCARComplementAmplitude",
            "D0.Geometry.sampledVectorMidpointCARComplement_positive_of_vectorSlack",
            "D0.Geometry.sampledMatterMidpointCARComplement_positive_of_vectorSlack",
            "D0.Geometry.sampledMatterMidpointCARComplement_positive_of_vectorMargin",
            "D0.Geometry.sampledMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes",
        }
        self.assertTrue(required.issubset(declarations))
        analysis_module = "D0.Analysis.MidpointQuadrature"
        geometry_module = "D0.Geometry.NonvacuumBrinkmannStencil"
        standard_axioms = {"Classical.choice", "Quot.sound", "propext"}
        for name in required:
            row = declarations[name]
            expected_module = analysis_module if name.startswith("D0.Analysis.") else geometry_module
            self.assertTrue(row["exists"])
            self.assertEqual(row["module"], expected_module)
            self.assertEqual(set(row["axioms"]), standard_axioms)
            self.assertGreater(row["declaration_ranges"]["declaration"]["start"]["line"], 0)

        history = declarations[
            "D0.Analysis.sampledVectorMidpointHistory_error_le_refinementBound"
        ]
        self.assertIn("duration * M * h ^ 2 / 24", history["elaborated_type"])
        local = declarations[
            "D0.Analysis.midpointQuadrature_error_norm_le_of_thirdDerivative_bound"
        ]
        self.assertIn("M * h ^ 3 / 24", local["elaborated_type"])
        margin = declarations[
            "D0.Geometry.sampledMatterMidpointCARComplement_positive_of_vectorMargin"
        ]
        self.assertIn("/ 2", margin["elaborated_type"])
        self.assertIn(
            "D0.Geometry.sampledMatterMidpointCARComplement_positive_of_vectorSlack",
            margin["proof_dependencies"],
        )
        eventual = declarations[
            "D0.Geometry.sampledMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes"
        ]
        self.assertIn("N₀ ≤ N", eventual["elaborated_type"])
        self.assertIn("duration / ↑N", eventual["elaborated_type"])
        self.assertIn(
            "D0.Geometry.sampledMatterMidpointCARComplement_positive_of_vectorMargin",
            eventual["proof_dependencies"],
        )
        previous_inventory = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "nonvacuum_vector_norm_car_margin_2026-10-26.json"
        )
        self.assertEqual(
            hashlib.sha256(previous_inventory.read_bytes()).hexdigest(),
            "c896eb2bbec77094b3ad2aec6b9e0fc6bcc2a1edb96a51e8a9b25e8e68bb1cbe",
        )

    def test_nonvacuum_interval_local_car_refinement_inventory_is_compiled(self) -> None:
        inventory_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "nonvacuum_interval_local_car_refinement_2026-10-27.json"
        )
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        self.assertEqual(inventory["schema"], "d0-lean-declaration-inventory-v1")
        self.assertEqual(inventory["public_import_root"], "D0.All")
        self.assertFalse(inventory["worktree_dirty"])
        declarations = {row["name"]: row for row in inventory["declarations"]}
        local_names = {
            "D0.Analysis.midpointQuadrature_error_norm_le_of_thirdDerivative_bound_on_interval",
            "D0.Analysis.sampledVectorMidpointHistory_error_le_refinementBound_on_interval",
            "D0.Geometry.sampledMatterMidpointCARComplement_positive_of_vectorMargin_on_interval",
            "D0.Geometry.sampledMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes_on_interval",
        }
        self.assertTrue(local_names.issubset(declarations))
        legacy_wrapper = declarations[
            "D0.Geometry.sampledMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes"
        ]
        self.assertIn(
            "D0.Geometry.sampledMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes_on_interval",
            legacy_wrapper["proof_dependencies"],
        )
        local_mesh = declarations[
            "D0.Geometry.sampledMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes_on_interval"
        ]
        self.assertIn("ContDiffAt", local_mesh["elaborated_type"])
        self.assertIn("Icc", local_mesh["elaborated_type"])
        for name in local_names:
            self.assertTrue(declarations[name]["exists"])
            self.assertEqual(
                set(declarations[name]["axioms"]),
                {"Classical.choice", "Quot.sound", "propext"},
            )

    def test_nonvacuum_pointwise_margin_compactness_application_is_compiled(self) -> None:
        inventory_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "nonvacuum_compact_pointwise_margin_2026-10-27.json"
        )
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        self.assertEqual(inventory["schema"], "d0-lean-declaration-inventory-v1")
        self.assertEqual(inventory["public_import_root"], "D0.All")
        self.assertFalse(inventory["worktree_dirty"])
        declaration = next(
            row for row in inventory["declarations"]
            if row["name"] == (
                "D0.Geometry.sampledMatterMidpointCARComplement_positive_for_all_"
                "sufficiently_fine_meshes_of_pointwiseMargin"
            )
        )
        self.assertEqual(declaration["module"], "D0.Geometry.NonvacuumBrinkmannStencil")
        self.assertIn("ContDiff ℝ 3 ψ", declaration["elaborated_type"])
        self.assertIn("‖ψ t‖ < √(1 - p)", declaration["elaborated_type"])
        self.assertIn("∃ N₀", declaration["elaborated_type"])
        self.assertIn(
            "D0.Geometry.sampledMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes_on_interval",
            declaration["proof_dependencies"],
        )
        self.assertEqual(
            set(declaration["axioms"]),
            {"Classical.choice", "Quot.sound", "propext"},
        )

    def test_nonvacuum_cubic_profile_car_application_is_compiled(self) -> None:
        inventory_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "nonvacuum_cubic_profile_car_margin_2026-10-27.json"
        )
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        self.assertEqual(inventory["schema"], "d0-lean-declaration-inventory-v1")
        self.assertRegex(inventory["snapshot_commit"], r"^[0-9a-f]{40}$")
        self.assertRegex(inventory["lean_source_digest"], r"^[0-9a-f]{64}$")
        self.assertFalse(inventory["worktree_dirty"])
        self.assertEqual(inventory["snapshot_commit"], "ea2c9d5602880ff059e75a2967444f54bdf242f4")
        self.assertEqual(inventory["public_import_root"], "D0.All")
        declarations = {row["name"]: row for row in inventory["declarations"]}
        required = {
            "D0.Geometry.cubicMatterEuclideanProfile_apply",
            "D0.Geometry.cubicMatterEuclideanProfile_norm_le_coefficientNorm",
            "D0.Geometry.cubicMatterProfile_hasDerivAt",
            "D0.Geometry.cubicMatterEuclideanProfile_sampledRate_eq",
            "D0.Geometry.cubicMatterMidpointSample_eq_sampledHistory",
            "D0.Geometry.nonvacuumCubicMidpointSource_matches_record",
            "D0.Geometry.sampledCubicMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes",
            "D0.Geometry.nonvacuumCubicCARComplement_positive_with_sameRecordStencilSource",
        }
        self.assertEqual(set(declarations), required)
        application = declarations[
            "D0.Geometry.nonvacuumCubicCARComplement_positive_with_sameRecordStencilSource"
        ]
        self.assertEqual(application["module"], "D0.Geometry.NonvacuumBrinkmannStencil")
        self.assertIn("c1 ≠ 0", application["elaborated_type"])
        self.assertIn("∃ N₀", application["elaborated_type"])
        self.assertIn("√(1 - p)", application["elaborated_type"])
        self.assertIn("cubicMatterMidpointSample", application["elaborated_type"])
        self.assertIn("finiteMatterForwardGradient", application["elaborated_type"])
        self.assertIn("transverseFivePointLaplacian", application["elaborated_type"])
        car_application = declarations[
            "D0.Geometry.sampledCubicMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes"
        ]
        self.assertIn(
            "D0.Geometry.cubicMatterEuclideanProfile_norm_le_coefficientNorm",
            car_application["proof_dependencies"],
        )
        self.assertIn(
            "D0.Geometry.cubicMatterMidpointSample_eq_sampledHistory",
            car_application["proof_dependencies"],
        )
        self.assertIn(
            "D0.Geometry.sampledCubicMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes",
            application["proof_dependencies"],
        )
        self.assertIn(
            "D0.Geometry.nonvacuumCubicMidpointSource_matches_record",
            application["proof_dependencies"],
        )
        for name in required:
            self.assertTrue(declarations[name]["exists"])
            self.assertEqual(declarations[name]["module"], "D0.Geometry.NonvacuumBrinkmannStencil")
            self.assertEqual(
                set(declarations[name]["axioms"]),
                {"Classical.choice", "Quot.sound", "propext"},
            )
        self.assertEqual(
            set(application["axioms"]),
            {"Classical.choice", "Quot.sound", "propext"},
        )
        case = next(
            row for row in cold_start.CASES
            if row["id"] == "positive-nonvacuum-recovery"
        )
        self.assertEqual(
            case["queries"][18],
            application["name"]
            + " cubicMatterCoefficientNorm cubicMatterMidpointSample "
            + "finiteMatterForwardGradient transverseFivePointLaplacian",
        )
        source = next(
            row for row in case["required_sources"]
            if row["path"] == "03_FORMALIZATION/D0/Geometry/NonvacuumBrinkmannStencil.lean"
        )
        self.assertEqual(source["commit"], "423ec9a87553a14c6f484e429a6d3309eeae256a")
        self.assertEqual(source["blob"], "07a988011a77ee87aa13d5d816680920d51a3007")
        self.assertEqual(source["scope_query_indexes"], [18, 19])
        inventory_source = next(
            row for row in case["required_sources"]
            if row["path"] == "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/nonvacuum_cubic_profile_car_margin_2026-10-27.json"
        )
        self.assertEqual(inventory_source["commit"], "119c31ba6df9f02a4b8b491e7658de2e7432a797")
        self.assertEqual(inventory_source["blob"], "9cfb08a3cbe8ef09d5f1311b6b96ea27378ab611")
        self.assertEqual(inventory_source["scope_query_indexes"], [18])

    def test_proper_lorentz_orbit_is_discoverable_from_pinned_owner_and_lean(self) -> None:
        case = next(
            item for item in cold_start.CASES
            if item["id"] == "proper-lorentz-same-orientation-orbit"
        )
        hits_by_query = proof.full_text_search_many(
            proof.ROOT, case["queries"], limit=18
        )
        query_pairs = list(zip(case["queries"], hits_by_query))
        for path in case["required_refs"]:
            status = cold_start._required_source_status(query_pairs, {"path": path})
            self.assertTrue(status["found"], f"cold-start search missed {path}")
        for source in case["required_sources"]:
            status = cold_start._required_source_status(query_pairs, source)
            self.assertTrue(status["found"], f"cold-start missed pinned owner: {status}")
        module = "03_FORMALIZATION/D0/Geometry/A4DStarFiniteLorentzQuotient.lean"
        exact_query = next(
            query for query in case["queries"]
            if "a4d_complete_proper_orbit_coordinates" in query
        )
        exact_hits = hits_by_query[case["queries"].index(exact_query)]
        self.assertTrue(any(
            hit.get("source") == module and hit.get("direct_content")
            for hit in exact_hits
        ), "exact proper-orbit query must surface its Lean source directly")
        gram_api_query = (
            "FiniteGramTangent finiteGram_right_orbit_complete "
            "finiteGram_dressed_transport_compatible"
        )
        gram_api_hits = proof.full_text_search(
            proof.ROOT, gram_api_query, limit=18
        )
        self.assertTrue(any(
            hit.get("source") ==
                "03_FORMALIZATION/D0/Algebra/FiniteGramTangent.lean"
            and hit.get("direct_content")
            for hit in gram_api_hits
        ), "shared Gram-orbit query must surface its algebra API directly")
        self.assertIn("time orientation", case["scope_review"])

    def test_generic_finite_gram_orbit_api_is_used_by_lorentz_specialization(self) -> None:
        inventory_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "finite_gram_orbit_shared_api_declarations_2026-10-26_julia_base_link_frechet_v2.json"
        )
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        self.assertEqual(inventory["schema"], "d0-lean-declaration-inventory-v1")
        self.assertRegex(inventory["snapshot_commit"], r"^[0-9a-f]{40}$")
        self.assertFalse(inventory["worktree_dirty"])
        assert_historical_compiled_inventory(self, inventory)
        self.assertEqual(inventory["public_import_root"], "D0.All")
        declarations = {row["name"]: row for row in inventory["declarations"]}
        self.assertEqual(set(inventory["request"]["full_names"]), set(declarations))

        for generic_name in (
            "D0.Algebra.finiteGram_symmetric",
            "D0.Algebra.finiteGram_right_invariant",
        ):
            generic = declarations[generic_name]
            self.assertIn("Fintype ι", generic["elaborated_type"])
            self.assertNotIn("DecidableEq ι", generic["elaborated_type"])

        affine = declarations["D0.Algebra.finiteGram_add_smul_expand"]
        self.assertEqual(affine["module"], "D0.Algebra.FiniteGramTangent")
        self.assertNotIn("DecidableEq ι", affine["elaborated_type"])
        for fragment in (
            "finiteGram η (Θ + t • C)",
            "C * η * Θ.transpose",
            "Θ * η * C.transpose",
            "t ^ 2 • (C * η * C.transpose)",
        ):
            self.assertIn(fragment, affine["elaborated_type"])
        self.assertIn(
            "D0.Algebra.finiteGram_add_smul_expand._abel_1_1",
            affine["proof_dependencies"],
        )
        self.assertNotIn("sorryAx", affine["axioms"])
        for specialization_name in (
            "D0.Algebra.finiteGram_smul_expand",
            "D0.Algebra.finiteGram_one_smul_expand",
        ):
            specialization = declarations[specialization_name]
            self.assertIn(
                "D0.Algebra.finiteGram_add_smul_expand",
                specialization["proof_dependencies"],
            )
            self.assertNotIn("sorryAx", specialization["axioms"])

        geometry_consumers = (
            (
                "D0.Geometry.solderMetric_smul_expand",
                "D0.Algebra.finiteGram_smul_expand",
                "D0.Geometry.solderMetric_realizes_symmetric_tangent",
            ),
            (
                "D0.Geometry.j2DetectorMetricPath_smul_expand",
                "D0.Algebra.finiteGram_one_smul_expand",
                "D0.Geometry.j2DetectorMetricPath_symmetric_tangent",
            ),
        )
        for consumer_name, specialization_name, application_name in geometry_consumers:
            self.assertIn(
                specialization_name,
                declarations[consumer_name]["proof_dependencies"],
            )
            self.assertIn(
                consumer_name,
                declarations[application_name]["proof_dependencies"],
            )
            self.assertNotIn("sorryAx", declarations[consumer_name]["axioms"])
            self.assertNotIn("sorryAx", declarations[application_name]["axioms"])

        quotient = declarations[
            "D0.Algebra.finiteGram_add_smul_difference_quotient"
        ]
        self.assertEqual(quotient["module"], "D0.Algebra.FiniteGramTangent")
        self.assertNotIn("DecidableEq ι", quotient["elaborated_type"])
        for fragment in (
            "t ≠ 0",
            "finiteGram η (Θ + t • C)",
            "C * η * Θ.transpose + Θ * η * C.transpose",
            "t • (C * η * C.transpose)",
        ):
            self.assertIn(fragment, quotient["elaborated_type"])
        self.assertIn(
            "D0.Algebra.finiteGram_add_smul_expand",
            quotient["proof_dependencies"],
        )
        self.assertIn(
            "D0.Algebra.finiteGram_add_smul_difference_quotient._abel_1_1",
            quotient["proof_dependencies"],
        )
        self.assertNotIn("sorryAx", quotient["axioms"])
        for consumer_name in (
            "D0.Geometry.solderMetric_flat_tangent",
            "D0.Geometry.j2DetectorMetricPath_symmetric_difference_quotient",
        ):
            consumer = declarations[consumer_name]
            self.assertIn(
                "D0.Algebra.finiteGram_add_smul_difference_quotient",
                consumer["proof_dependencies"],
            )
            self.assertNotIn("sorryAx", consumer["axioms"])

        generic = declarations["D0.Algebra.finiteGram_right_orbit_complete"]
        self.assertEqual(generic["module"], "D0.Algebra.FiniteGramTangent")
        self.assertIn("IsUnit Θ.det", generic["elaborated_type"])
        self.assertNotIn("IsUnit η.det", generic["elaborated_type"])
        self.assertIn("D0.Algebra.finiteGram_right_invariant",
                      generic["proof_dependencies"])
        self.assertEqual(
            set(generic["axioms"]),
            {"Classical.choice", "Quot.sound", "propext"},
        )

        specialization = declarations[
            "D0.Geometry.a4dRightLorentz_gram_complete"
        ]
        self.assertEqual(
            specialization["module"],
            "D0.Geometry.A4DStarFiniteLorentzQuotient",
        )
        self.assertIn(
            "D0.Algebra.finiteGram_right_orbit_complete",
            specialization["proof_dependencies"],
        )
        self.assertNotIn("sorryAx", specialization["axioms"])

        dressed = declarations[
            "D0.Algebra.finiteGram_dressed_transport_compatible"
        ]
        self.assertEqual(dressed["module"], "D0.Algebra.FiniteGramTangent")
        self.assertIn("IsUnit Θy.det", dressed["elaborated_type"])
        self.assertNotIn("IsUnit Θx.det", dressed["elaborated_type"])
        self.assertNotIn("IsUnit η.det", dressed["elaborated_type"])

        endpoint = declarations[
            "D0.Geometry.a4dDressedLink_metric_compatible"
        ]
        self.assertIn(
            "D0.Algebra.finiteGram_dressed_transport_compatible",
            endpoint["proof_dependencies"],
        )

        frame_action = declarations[
            "D0.Algebra.finiteMatrix_dressed_transport_frame_invariant"
        ]
        self.assertEqual(frame_action["module"], "D0.Algebra.FiniteGramTangent")
        self.assertIn("IsUnit Λx.det", frame_action["elaborated_type"])
        self.assertIn("IsUnit Λy.det", frame_action["elaborated_type"])
        self.assertNotIn("IsUnit Θy.det", frame_action["elaborated_type"])
        self.assertNotIn("sorryAx", frame_action["axioms"])

        frame_specialization = declarations[
            "D0.Geometry.a4dDressedLink_frame_invariant"
        ]
        self.assertNotIn("IsUnit Θy.det", frame_specialization["elaborated_type"])
        self.assertIn(
            "D0.Algebra.finiteMatrix_dressed_transport_frame_invariant",
            frame_specialization["proof_dependencies"],
        )
        self.assertNotIn("sorryAx", frame_specialization["axioms"])

        generic_equivalence = declarations[
            "D0.Algebra.finiteMatrix_dressed_transport_eq_iff_frame_action"
        ]
        for premise in (
            "IsUnit Θx.det",
            "IsUnit Θy.det",
            "IsUnit Λx.det",
            "IsUnit Λy.det",
        ):
            self.assertIn(premise, generic_equivalence["elaborated_type"])
        self.assertIn(
            "D0.Algebra.finiteMatrix_dressed_transport_frame_invariant",
            generic_equivalence["proof_dependencies"],
        )
        self.assertNotIn("sorryAx", generic_equivalence["axioms"])

        equivalence_specialization = declarations[
            "D0.Geometry.a4dDressedLink_eq_iff_rightAction"
        ]
        self.assertIn(
            "D0.Algebra.finiteMatrix_dressed_transport_eq_iff_frame_action",
            equivalence_specialization["proof_dependencies"],
        )
        self.assertNotIn("sorryAx", equivalence_specialization["axioms"])

    def test_historical_metric_provenance_crosswalk_pins_shared_orbit_application(self) -> None:
        crosswalk_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "metric_provenance_crosswalk_2026-10-26_fe15cd8c.json"
        )
        crosswalk = json.loads(crosswalk_path.read_text(encoding="utf-8"))
        self.assertEqual(crosswalk["result_id"], "metric-provenance")
        self.assertEqual(
            crosswalk["snapshot_commit"],
            "e89fbab65d24613875fcbbde4cf5b14dcffee760",
        )
        self.assertFalse(crosswalk["worktree_dirty"])
        self.assertEqual(
            crosswalk["lean_source_digest"],
            "0cac96c00908285378d7eb922ac268eb69cc67737afad40f0a7b41cb83b95df5",
        )
        self.assertEqual(
            crosswalk["explicit_declaration_locator_disposition"], "all_resolved"
        )
        self.assertEqual(crosswalk["claim_locator_disposition"], "unresolved")
        self.assertEqual(crosswalk["semantic_relation_status"], "unresolved")
        self.assertFalse(crosswalk["acceptance_inferred"])
        declarations = {
            row["name"]: row for row in crosswalk["compiled_declarations"]
            if row.get("name")
        }
        lorentz = declarations["D0.Geometry.a4dRightLorentz_gram_complete"]
        self.assertIn(
            "D0.Algebra.finiteGram_right_orbit_complete",
            lorentz["proof_dependencies"],
        )
        endpoint = declarations[
            "D0.Geometry.a4dDressedLink_metric_compatible"
        ]
        self.assertIn(
            "D0.Algebra.finiteGram_dressed_transport_compatible",
            endpoint["proof_dependencies"],
        )

    def test_historical_cold_start_summary_preserves_original_denominator(self) -> None:
        summary_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "proof_architecture_cold_start_summary_2026-10-25_5be41d7c.json"
        )
        summary_bytes = summary_path.read_bytes()
        summary = json.loads(summary_bytes)
        self.assertLess(len(summary_bytes), 100_000)
        self.assertEqual(
            summary["schema"], "d0-proof-architecture-cold-start-summary-v2"
        )
        self.assertEqual(
            summary["snapshot_commit"],
            "5be41d7cb83e0a7dbeaa55491d8a8fcc99dce1fd",
        )
        self.assertFalse(summary["worktree_dirty"])
        self.assertEqual(summary["search_cases_found_all_sources"], 21)
        self.assertEqual(summary["search_cases_total"], 21)
        self.assertEqual(summary["benchmark_cases_total"], 22)
        self.assertTrue(summary["change_impact_regression"]["status"] == "pass")
        self.assertEqual(
            summary["authority_source_digests"]["02_REGISTRY/formal_support.csv"],
            "b538abd4bfbb919f948cbf619dbf2e24859223532e0443ece644c512d050568a",
        )
        self.assertTrue(all(
            row["all_required_sources_found"] and not row["missing_paths"]
            for row in summary["cases"]
        ))
        self.assertEqual(
            sum(row["required_source_count"] for row in summary["cases"]), 127
        )
        self.assertTrue(summary["semantic_scope_review_is_manual"])
        replay = summary["replay"]
        self.assertEqual(replay["source_commit"], summary["snapshot_commit"])
        self.assertEqual(
            replay["command"], "python3 tools/proof_architecture_cold_start.py"
        )
        self.assertRegex(replay["full_output_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(
            replay["runner_sha256"],
            "67362b36a94a7ec338af265637ce814c482199ab9b2c682fd7b906750e40daf9",
        )
        self.assertEqual(
            replay["search_engine_sha256"],
            "aaed4194af38484de97db60c821374955f90dc5cc290d20a6fb8e53f94624262",
        )

    def test_current_cold_start_summary_covers_proper_lorentz_orbit_case(self) -> None:
        summary_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/"
            / "d0_proof_architecture_formalization_2026-10-24/reports"
            / "proof_architecture_cold_start_summary_2026-10-28_integrated.json"
        )
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        pinned_runner_source = subprocess.check_output([
            "git", "show",
            f"{summary['snapshot_commit']}:tools/proof_architecture_cold_start.py",
        ], text=True)
        pinned_cases_value = None
        for node in ast.parse(pinned_runner_source).body:
            if (isinstance(node, ast.AnnAssign)
                    and isinstance(node.target, ast.Name)
                    and node.target.id == "CASES"):
                pinned_cases_value = node.value
                break
            if (isinstance(node, ast.Assign)
                    and any(isinstance(target, ast.Name) and target.id == "CASES"
                            for target in node.targets)):
                pinned_cases_value = node.value
                break
        self.assertIsNotNone(pinned_cases_value)
        pinned_cases = ast.literal_eval(pinned_cases_value)
        self.assertEqual(summary["schema"], "d0-proof-architecture-cold-start-summary-v2")
        self.assertRegex(summary["snapshot_commit"], r"^[0-9a-f]{40}$")
        self.assertFalse(summary["worktree_dirty"])
        self.assertEqual(summary["search_cases_found_all_sources"], len(pinned_cases))
        self.assertEqual(summary["search_cases_total"], len(pinned_cases))
        self.assertEqual(summary["benchmark_cases_total"], 25)
        self.assertEqual(
            [row["id"] for row in summary["cases"]],
            [case["id"] for case in pinned_cases],
        )
        self.assertTrue(all(
            row["all_required_sources_found"] and not row["missing_paths"]
            for row in summary["cases"]
        ))
        expected_required_count = sum(
            len(case.get("required_sources", []))
            + sum(
                path not in {source["path"] for source in case.get("required_sources", [])}
                for path in case["required_refs"]
            )
            for case in pinned_cases
        )
        self.assertEqual(
            sum(row["required_source_count"] for row in summary["cases"]),
            expected_required_count,
        )
        self.assertEqual(summary["required_source_ref_count"], expected_required_count)
        positive_nonvacuum = next(
            row for row in summary["cases"]
            if row["id"] == "positive-nonvacuum-recovery"
        )
        positive_case = next(
            case for case in pinned_cases
            if case["id"] == "positive-nonvacuum-recovery"
        )
        self.assertEqual(positive_nonvacuum["query_count"], len(positive_case["queries"]))
        exact_retrieval = positive_nonvacuum["exact_application_retrieval"]
        self.assertTrue(exact_retrieval["found"])
        self.assertEqual(exact_retrieval["status"], "found_direct_content")
        self.assertEqual(exact_retrieval["source_origin"], "pinned_snapshot")
        self.assertEqual(exact_retrieval["query_index"], 17)
        self.assertEqual(exact_retrieval["candidate_rank"], 3)
        self.assertEqual(
            exact_retrieval["commit"],
            "a2c20a4dc9feeb5446b41e9e49ea8094bd14f40b",
        )
        self.assertEqual(
            exact_retrieval["blob"],
            "82574aafa3ea94c61ca28ad9e08980c2974d4b22",
        )
        cubic_retrieval = positive_nonvacuum["cubic_family_retrieval"]
        self.assertTrue(cubic_retrieval["found"])
        self.assertEqual(cubic_retrieval["status"], "found_direct_content")
        self.assertEqual(cubic_retrieval["source_origin"], "pinned_snapshot")
        self.assertEqual(cubic_retrieval["query_index"], 18)
        self.assertEqual(cubic_retrieval["candidate_rank"], 2)
        self.assertEqual(
            cubic_retrieval["commit"],
            "119c31ba6df9f02a4b8b491e7658de2e7432a797",
        )
        self.assertEqual(
            cubic_retrieval["blob"],
            "9cfb08a3cbe8ef09d5f1311b6b96ea27378ab611",
        )
        lean_retrieval = positive_nonvacuum["cubic_lean_source_retrieval"]
        self.assertTrue(lean_retrieval["found"])
        self.assertEqual(lean_retrieval["status"], "found_direct_content")
        self.assertEqual(lean_retrieval["source_origin"], "pinned_snapshot")
        self.assertEqual(lean_retrieval["query_index"], 18)
        self.assertEqual(lean_retrieval["candidate_rank"], 6)
        self.assertEqual(
            lean_retrieval["commit"],
            "423ec9a87553a14c6f484e429a6d3309eeae256a",
        )
        self.assertEqual(
            lean_retrieval["blob"],
            "07a988011a77ee87aa13d5d816680920d51a3007",
        )
        euclidean_refinement = positive_nonvacuum[
            "same_record_euclidean_refinement_retrieval"
        ]
        self.assertTrue(euclidean_refinement["found"])
        self.assertEqual(euclidean_refinement["status"], "found_direct_content")
        self.assertEqual(euclidean_refinement["query_index"], 19)
        self.assertEqual(euclidean_refinement["lean_source_commit"],
                         "423ec9a87553a14c6f484e429a6d3309eeae256a")
        self.assertEqual(euclidean_refinement["lean_source_blob"],
                         "07a988011a77ee87aa13d5d816680920d51a3007")
        self.assertEqual(euclidean_refinement["inventory_commit"],
                         "de9fc93ff5a159486a8404ba945ab3e3655f0729")
        self.assertEqual(euclidean_refinement["inventory_blob"],
                         "40171d8756ccf09c1b0627c20bca03a91637b56c")
        self.assertEqual(
            positive_nonvacuum["required_source_count"],
            len(positive_case.get("required_sources", []))
            + sum(
                path not in {source["path"] for source in positive_case.get("required_sources", [])}
                for path in positive_case["required_refs"]
            ),
        )
        labelled = next(
            row for row in summary["cases"]
            if row["id"] == "labelled-native-raising-inverse"
        )
        self.assertEqual(labelled["query_count"], 18)
        self.assertEqual(labelled["required_source_count"], 13)
        historical_refinement_summary = json.loads(
            (
                proof.ROOT
                / "02_REGISTRY/research/sources/"
                / "d0_proof_architecture_formalization_2026-10-24/reports"
                / "proof_architecture_cold_start_summary_2026-10-26_midpoint_refinement.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            historical_refinement_summary["snapshot_commit"],
            "fc76e2a221d629297af93e74583b6d413c0b97d5",
        )
        positive = next(
            row for row in historical_refinement_summary["cases"]
            if row["id"] == "positive-nonvacuum-recovery"
        )
        self.assertEqual(positive["query_count"], 8)
        self.assertEqual(positive["required_source_count"], 3)
        proper = next(
            row for row in summary["cases"]
            if row["id"] == "proper-lorentz-same-orientation-orbit"
        )
        self.assertEqual(proper["query_count"], 4)
        self.assertEqual(proper["required_source_count"], 6)
        gram = next(
            row for row in summary["cases"]
            if row["id"] == "finite-gram-affine-quadratic-expansion"
        )
        self.assertEqual(gram["query_count"], 5)
        self.assertEqual(gram["required_source_count"], 4)
        self.assertTrue(summary["change_impact_regression"]["status"] == "pass")
        self.assertTrue(summary["semantic_scope_review_is_manual"])
        for path, digest in summary["authority_source_digests"].items():
            pinned_source = subprocess.check_output([
                "git", "show", f"{summary['snapshot_commit']}:{path}"
            ])
            self.assertEqual(
                hashlib.sha256(pinned_source).hexdigest(),
                digest,
                f"cold-start summary digest does not match pinned source {path}",
            )
        replay = summary["replay"]
        self.assertEqual(replay["source_commit"], summary["snapshot_commit"])
        self.assertEqual(
            replay["command"], "python3 tools/proof_architecture_cold_start.py"
        )
        self.assertEqual(
            replay["runner_sha256"],
            hashlib.sha256(
                subprocess.check_output([
                    "git", "show",
                    f"{summary['snapshot_commit']}:tools/proof_architecture_cold_start.py",
                ])
            ).hexdigest(),
        )
        self.assertEqual(
            replay["search_engine_sha256"],
            hashlib.sha256(subprocess.check_output([
                "git", "show", f"{summary['snapshot_commit']}:tools/proof_architecture.py"
            ])).hexdigest(),
        )
        # The receipt records the test fixture at its clean source commit.
        # The current test may point at a newer receipt, so comparing to its
        # working-tree bytes would create a self-referential digest.
        self.assertEqual(
            replay["test_sha256"],
            hashlib.sha256(subprocess.check_output([
                "git", "show",
                f"{summary['snapshot_commit']}:tools/test_proof_architecture.py",
            ], cwd=proof.ROOT)).hexdigest(),
        )

    def test_historical_final_v4_cold_start_receipt_is_preserved(self) -> None:
        summary_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/"
            / "d0_proof_architecture_formalization_2026-10-24/reports"
            / "proof_architecture_cold_start_summary_2026-10-26_final_v4.json"
        )
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        self.assertEqual(summary["snapshot_commit"], "5183b7bb07109cf42a0248c5a46dcea6e5c9ad55")
        self.assertFalse(summary["worktree_dirty"])
        self.assertEqual(summary["search_cases_found_all_sources"], 24)
        self.assertEqual(summary["required_source_ref_count"], 158)
        self.assertEqual(summary["benchmark_cases_total"], 25)
        self.assertEqual(
            summary["replay"]["full_output_sha256"],
            "ee319034ab6fa3e02571c2adea0337a7752f105f02ca94745b166b0727352fa3",
        )
        self.assertEqual(
            summary["replay"]["test_sha256"],
            "66f92ca67b8e24ec0d21145fe4ab417784e5c5c738d524927b76b0d35f14de2d",
        )

    def test_historical_integrated_cold_start_summary_tracks_cubic_queries(self) -> None:
        summary_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/"
            / "d0_proof_architecture_formalization_2026-10-24/reports"
            / "proof_architecture_cold_start_summary_2026-10-25_combined.json"
        )
        summary_bytes = summary_path.read_bytes()
        summary = json.loads(summary_bytes)
        self.assertLess(len(summary_bytes), 100_000)
        self.assertEqual(summary["schema"], "d0-proof-architecture-cold-start-summary-v2")
        self.assertEqual(summary["snapshot_commit"], "1820d940d3b1b5ab61ef7ad505980eea077cf553")
        self.assertFalse(summary["worktree_dirty"])
        self.assertEqual(summary["search_cases_found_all_sources"], 20)
        self.assertEqual(summary["search_cases_total"], 20)
        self.assertEqual(summary["benchmark_cases_total"], 21)
        self.assertEqual(summary["change_impact_regression"]["status"], "pass")
        self.assertEqual(
            summary["authority_source_digests"]["02_REGISTRY/formal_support.csv"],
            "4520818e1940d8844ba94198f3d9107803ec63202b3f4f6dec67146237c66e94",
        )
        self.assertEqual(len(summary["cases"]), 20)
        self.assertEqual(len({row["id"] for row in summary["cases"]}), 20)
        self.assertTrue(all(
            row["all_required_sources_found"] and not row["missing_paths"]
            for row in summary["cases"]
        ))
        self.assertEqual(
            sum(row["required_source_count"] for row in summary["cases"]), 123
        )
        cubic_case = next(
            row for row in summary["cases"]
            if row["id"] == "positive-nonvacuum-recovery"
        )
        self.assertEqual(cubic_case["query_count"], 6)
        self.assertEqual(cubic_case["required_source_count"], 3)
        self.assertTrue(cubic_case["all_required_sources_found"])
        replay = summary["replay"]
        self.assertEqual(replay["source_commit"], summary["snapshot_commit"])
        self.assertEqual(
            replay["command"], "python3 tools/proof_architecture_cold_start.py"
        )
        self.assertRegex(replay["full_output_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(
            replay["runner_sha256"],
            "52b3c30544fdc448ef21139a0b0f76094fc9a24b20b0508d34be3ad41583146e",
        )
        self.assertEqual(
            replay["search_engine_sha256"],
            "aaed4194af38484de97db60c821374955f90dc5cc290d20a6fb8e53f94624262",
        )
        self.assertEqual(
            replay["full_output_sha256"],
            "f54ba8b489f3cfb23172fe7b382a9b38b76051dc958f75543d790d9b28a519db",
        )
        self.assertRegex(replay["full_output_sha256"], r"^[0-9a-f]{64}$")
        verification_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/"
            / "d0_proof_architecture_formalization_2026-10-24/reports"
            / "proof_architecture_historical_combined_replay_2026-10-26.json"
        )
        verification = json.loads(verification_path.read_text(encoding="utf-8"))
        verification_replay = verification["verification_replay"]
        self.assertEqual(
            verification["source_summary_path"],
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/reports/proof_architecture_cold_start_summary_2026-10-25_combined.json",
        )
        self.assertEqual(
            verification["recorded_replay"]["full_output_sha256"],
            replay["full_output_sha256"],
        )
        self.assertEqual(verification["source_commit"], summary["snapshot_commit"])
        self.assertEqual(verification_replay["snapshot_commit"], summary["snapshot_commit"])
        self.assertEqual(verification_replay["runner_sha256"], replay["runner_sha256"])
        self.assertEqual(
            verification_replay["search_engine_sha256"], replay["search_engine_sha256"]
        )
        self.assertEqual(verification_replay["search_cases_found_all_sources"], 20)
        self.assertEqual(verification_replay["required_source_ref_count"], 123)
        self.assertEqual(verification_replay["benchmark_cases_total"], 21)
        self.assertEqual(verification_replay["missing_required_sources"], 0)
        self.assertTrue(verification_replay["authority_source_digests_match_recorded"])
        self.assertFalse(verification_replay["matches_recorded_full_output_sha256"])
        self.assertNotEqual(
            verification_replay["full_output_sha256"], replay["full_output_sha256"]
        )
        self.assertEqual(verification_replay["full_output_bytes"], 7_099_884)

    def test_search_process_comparison_is_pinned_and_semantically_scoped(self) -> None:
        comparison_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/"
            / "d0_proof_architecture_formalization_2026-10-24/reports"
            / "proof_architecture_search_process_comparison_2026-10-27_assumption_links_v18.json"
        )
        comparison = json.loads(comparison_path.read_text(encoding="utf-8"))
        self.assertEqual(
            comparison["schema"], "d0-proof-architecture-search-comparison-v1"
        )
        self.assertFalse(comparison["worktree_dirty"])
        self.assertRegex(comparison["snapshot_commit"], r"^[0-9a-f]{40}$")
        self.assertIn("five bounded text candidates",
                      comparison["comparison_scope"]["current"])
        self.assertEqual(comparison["metrics"]["query_count"], 24)
        self.assertEqual(
            comparison["metrics"]["query_count_with_explicit_source_scope"], 7
        )
        self.assertEqual(
            comparison["metrics"]["legacy_scoped_queries_with_expected_source"], 0
        )
        self.assertEqual(
            comparison["metrics"]["current_scoped_queries_with_expected_source"], 7
        )
        self.assertEqual(
            comparison["metrics"]["current_serialized_answer_bytes_total"],
            529927,
        )
        self.assertEqual(
            comparison["metrics"]["current_average_answer_bytes"], 22080.3
        )
        self.assertTrue(
            comparison["metrics"]["semantic_review_required_for_all_queries"]
        )
        self.assertEqual(
            comparison["metrics"]["current_scoped_queries_with_expected_source_owner_link"],
            1,
        )
        self.assertEqual(
            comparison["metrics"]["current_expected_source_owner_link_count"], 1
        )
        julia = next(
            row for row in comparison["cases"]
            if row["case_id"] == "julia-query-principal-frame-coframe-recovery"
        )
        julia_source = julia["current"]["expected_source_link_details"][0]
        self.assertTrue(julia_source["candidate_surfaced"])
        self.assertTrue(julia_source["direct_content"])
        self.assertEqual(julia_source["pin_status"], "verified")
        self.assertEqual(
            julia_source["source_commit"],
            "fe5cf335da04cac14e50407b03f98b96be17dc52",
        )
        self.assertEqual(
            julia_source["source_blob"],
            "1c8d59e5533b443d9a015dc4512cfbc160ae7e62",
        )
        self.assertEqual(
            comparison["metrics"][
                "current_scoped_queries_with_expected_source_header_owner_declaration"
            ],
            1,
        )
        self.assertEqual(
            comparison["metrics"][
                "current_expected_source_header_owner_declaration_count"
            ],
            1,
        )
        positive = next(
            row for row in comparison["cases"]
            if row["case_id"] == "positive-nonvacuum-recovery"
        )
        nonvacuum_detail = next(
            detail for detail in positive["current"]["expected_source_link_details"]
            if detail["source"].endswith(
                "A4D_EXACT_NONVACUUM_GR_MIDPOINT_C2_RECOVERY_2026_10_20.md"
            )
        )
        self.assertEqual(
            nonvacuum_detail["owner_status"], "no_exact_assembly_owner_link"
        )
        self.assertEqual(
            nonvacuum_detail["source_header_owner_declarations"][0]["line"], 4
        )
        self.assertEqual(
            nonvacuum_detail["source_header_owner_declarations"][0]["status"],
            "source_document_declaration_only",
        )
        self.assertEqual(nonvacuum_detail["source_origin"], "pinned_snapshot")
        self.assertEqual(nonvacuum_detail["pin_status"], "verified")
        self.assertEqual(
            nonvacuum_detail["source_commit"],
            "8b94198c8dfbdf5983ad0b350b058fb30bb68a54",
        )
        self.assertEqual(
            nonvacuum_detail["source_blob"],
            "63c36b18af67fc1f113f9e33deb13cf43ddf4556",
        )
        self.assertTrue(nonvacuum_detail["source_sha256"])
        lorentz = next(
            row for row in comparison["cases"]
            if row["case_id"] == "proper-lorentz-same-orientation-orbit"
        )
        owner_detail = next(
            detail for detail in lorentz["current"]["expected_source_link_details"]
            if detail["source"].endswith("MEMO_A4D_NONLINEAR_EINSTEIN_J2_BRIDGE.md")
        )
        self.assertTrue(owner_detail["candidate_surfaced"])
        self.assertEqual(
            owner_detail["owner_status"],
            "declared_by_exact_assembly_evidence_link",
        )
        self.assertEqual(owner_detail["owners"], ["existing CONTROL/main research owner"])
        self.assertEqual(
            [result["result_id"] for result in owner_detail["assembly_results"]],
            ["metric-provenance"],
        )
        self.assertEqual(
            owner_detail["assembly_results"][0]["interface_contract"]["id"],
            "star-metric-v1",
        )
        self.assertEqual(
            owner_detail["assembly_results"][0]["evidence"][0]["ref"],
            "77d3ab6059bd1a3ce48637b97b9f30aa8825fc5f",
        )
        labelled = next(
            row for row in comparison["cases"]
            if row["case_id"] == "labelled-native-raising-inverse"
        )
        labelled_detail = labelled["current"]["expected_source_link_details"][0]
        self.assertEqual(
            labelled_detail["owner_status"], "no_exact_assembly_owner_link"
        )
        self.assertEqual(
            len(labelled_detail["formal_support_locators"]), 3
        )
        self.assertTrue(all(
            link["status"] == "metadata_locator_only"
            for link in labelled_detail["formal_support_locators"]
        ))
        self.assertTrue(all(
            row["semantic_review"]["hypothesis_preservation"]
            == "not_assessed_by_search_output"
            for row in comparison["cases"]
        ))
        self.assertTrue(all(
            row["semantic_review"]["owner_correctness"]
            == "exact registered links are shown; independent owner correctness is not assessed by search output"
            for row in comparison["cases"]
        ))
        self.assertEqual(
            comparison["runner_sha256"],
            hashlib.sha256(
                subprocess.check_output([
                    "git", "show",
                    f"{comparison['snapshot_commit']}:tools/proof_architecture_process_comparison.py",
                ])
            ).hexdigest(),
        )

    def test_current_v2_search_comparison_separates_owner_and_support_links(self) -> None:
        comparison_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/"
            / "d0_proof_architecture_formalization_2026-10-24/reports"
            / "proof_architecture_search_process_comparison_2026-10-28_integrated.json"
        )
        comparison = json.loads(comparison_path.read_text(encoding="utf-8"))
        self.assertEqual(
            comparison["schema"], "d0-proof-architecture-search-comparison-v2"
        )
        self.assertFalse(comparison["worktree_dirty"])
        self.assertRegex(comparison["snapshot_commit"], r"^[0-9a-f]{40}$")
        for path, digest in comparison["authority_source_digests"].items():
            pinned_source = subprocess.check_output([
                "git", "show", f"{comparison['snapshot_commit']}:{path}"
            ])
            self.assertEqual(
                hashlib.sha256(pinned_source).hexdigest(),
                digest,
                f"search comparison digest does not match pinned source {path}",
            )
        self.assertEqual(comparison["metrics"]["query_count"], 24)
        metrics = comparison["metrics"]
        self.assertEqual(metrics["query_count_with_explicit_source_scope"], 7)
        self.assertEqual(metrics["expected_source_reference_count"], 8)
        self.assertEqual(metrics["unique_expected_source_path_count"], 7)
        self.assertEqual(metrics["legacy_scoped_queries_with_expected_source"], 0)
        self.assertEqual(metrics["current_scoped_queries_with_expected_source"], 7)
        self.assertEqual(
            metrics["current_scoped_queries_with_expected_source_assembly_owner_link"],
            1,
        )
        self.assertEqual(metrics["current_expected_source_assembly_owner_link_count"], 1)
        self.assertEqual(
            metrics["current_expected_source_references_with_formal_support_locator"],
            4,
        )
        self.assertEqual(metrics["current_expected_source_formal_support_locator_count"], 8)
        self.assertEqual(
            metrics["current_unique_expected_source_paths_with_formal_support_locator"],
            3,
        )
        self.assertEqual(
            metrics["current_expected_source_references_without_assembly_or_formal_support"],
            3,
        )
        self.assertEqual(
            metrics["current_unique_expected_source_paths_without_assembly_or_formal_support"],
            3,
        )
        self.assertEqual(
            metrics["current_expected_source_header_owner_declaration_count"], 1
        )
        self.assertTrue(metrics["semantic_review_required_for_all_queries"])

        labelled = next(
            row for row in comparison["cases"]
            if row["case_id"] == "labelled-native-raising-inverse"
        )
        labelled_detail = labelled["current"]["expected_source_link_details"][0]
        self.assertEqual(labelled_detail["owners"], [])
        self.assertEqual(len(labelled_detail["formal_support_locators"]), 3)
        self.assertTrue(all(
            locator["status"] == "metadata_locator_only"
            for locator in labelled_detail["formal_support_locators"]
        ))
        self.assertEqual(
            comparison["runner_sha256"],
            hashlib.sha256(
                subprocess.check_output([
                    "git", "show",
                    f"{comparison['snapshot_commit']}:tools/proof_architecture_process_comparison.py",
                ])
            ).hexdigest(),
        )

    def test_cyclic_af_cold_start_reports_are_pinned_to_one_clean_snapshot(self) -> None:
        report_dir = (
            proof.ROOT
            / "02_REGISTRY/research/sources/"
            / "d0_proof_architecture_formalization_2026-10-24/reports"
        )
        cold_path = report_dir / (
            "proof_architecture_cold_start_summary_2026-10-28_cyclic_af.json"
        )
        comparison_path = report_dir / (
            "proof_architecture_search_process_comparison_2026-10-28_cyclic_af.json"
        )
        cold = json.loads(cold_path.read_text(encoding="utf-8"))
        comparison = json.loads(comparison_path.read_text(encoding="utf-8"))

        expected_snapshot = "404acc9c8be4fb642509ebfa29ca9a7d7f3ac47d"
        self.assertEqual(cold["schema"], "d0-proof-architecture-cold-start-summary-v2")
        self.assertEqual(comparison["schema"], "d0-proof-architecture-search-comparison-v2")
        for report in (cold, comparison):
            self.assertEqual(report["snapshot_commit"], expected_snapshot)
            self.assertFalse(report["worktree_dirty"])
            for path, digest in report["authority_source_digests"].items():
                pinned_source = subprocess.check_output([
                    "git", "show", f"{expected_snapshot}:{path}"
                ])
                self.assertEqual(
                    hashlib.sha256(pinned_source).hexdigest(),
                    digest,
                    f"report digest does not match {expected_snapshot}:{path}",
                )

        for path, key in (
            ("tools/proof_architecture_cold_start.py", "runner_sha256"),
            ("tools/proof_architecture.py", "search_engine_sha256"),
            ("tools/test_proof_architecture.py", "test_sha256"),
            ("tools/compact_proof_architecture_cold_start.py", "compactor_sha256"),
        ):
            pinned_source = subprocess.check_output([
                "git", "show", f"{expected_snapshot}:{path}"
            ])
            self.assertEqual(
                hashlib.sha256(pinned_source).hexdigest(),
                cold["replay"][key],
                f"cold-start provenance does not match {expected_snapshot}:{path}",
            )
        comparison_runner = subprocess.check_output(
            [
                "git",
                "show",
                f"{expected_snapshot}:tools/proof_architecture_process_comparison.py",
            ]
        )
        self.assertEqual(
            hashlib.sha256(comparison_runner).hexdigest(),
            comparison["runner_sha256"],
        )

        self.assertEqual(cold["search_cases_found_all_sources"], 26)
        self.assertEqual(cold["search_cases_total"], 26)
        self.assertEqual(cold["benchmark_cases_total"], 27)
        self.assertEqual(cold["required_source_ref_count"], 173)
        self.assertTrue(cold["semantic_scope_review_is_manual"])
        cyclic = next(
            row for row in cold["cases"]
            if row["id"] == "cyclic-af-return-without-extra-blank-flag"
        )
        self.assertTrue(cyclic["all_required_sources_found"])
        source_path = (
            "02_REGISTRY/research/"
            "A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"
        )
        owner = cyclic["required_sources"][source_path]
        self.assertEqual(owner["candidate_rank"], 1)
        self.assertEqual(
            owner["citation_only_refs"][0]["commit"],
            "d53ef61c8c578c5a6cf16b88d17f8576ced0f64d",
        )
        self.assertEqual(
            owner["citation_only_refs"][0]["blob"],
            "069f16ed168c43e483dc5b6bc5eaabbac6e848fa",
        )
        self.assertTrue(owner["citation_only_refs"][0]["pin_complete"])
        architecture = cyclic["required_sources"][
            "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md"
        ]
        self.assertEqual(architecture["candidate_rank"], 2)

        metrics = comparison["metrics"]
        self.assertEqual(metrics["query_count"], 26)
        self.assertEqual(metrics["query_count_with_explicit_source_scope"], 9)
        self.assertEqual(metrics["legacy_scoped_queries_with_expected_source"], 0)
        self.assertEqual(metrics["current_scoped_queries_with_expected_source"], 9)
        self.assertEqual(
            metrics["current_scoped_queries_with_expected_source_assembly_owner_link"],
            1,
        )
        self.assertEqual(
            metrics["current_expected_source_references_with_formal_support_locator"],
            6,
        )
        self.assertEqual(
            metrics[
                "current_expected_source_references_without_assembly_or_formal_support"
            ],
            5,
        )
        self.assertTrue(metrics["semantic_review_required_for_all_queries"])

    def test_canonical_tower_source_transport_is_retrievable_at_latest_owner_head(self) -> None:
        case = next(
            item for item in cold_start.CASES
            if item["id"] == "canonical-af-tower-source-transport"
        )
        hits = proof.full_text_search_many(
            proof.ROOT, case["queries"], limit=cold_start.COLD_START_MIN_RESULT_WINDOW
        )
        self.assertEqual(len(hits), len(case["queries"]))
        query_pairs = list(zip(case["queries"], hits))
        for source in case["required_sources"]:
            status = cold_start._required_source_status(query_pairs, source)
            self.assertTrue(
                status["found"],
                f"cold-start missed pinned tower source {source['path']}: {status}",
            )
            if source.get("commit"):
                self.assertEqual(status["source_origin"], "pinned_snapshot")
                self.assertEqual(
                    status["expected_commit"],
                    "48500384e9a25b25a6a0f54911f5af50c2bc1625",
                )
                self.assertEqual(status["expected_blob"], source["blob"])
        self.assertIn("physical AF actuation", case["scope_review"])
        self.assertIn("GR_closed=false", case["scope_review"])

    def test_nontrivial_prefix_source_is_retrievable_at_latest_owner_head(self) -> None:
        case = next(
            item for item in cold_start.CASES
            if item["id"] == "nontrivial-canonical-prefix-source-correction"
        )
        hits = proof.full_text_search_many(
            proof.ROOT, case["queries"], limit=cold_start.COLD_START_MIN_RESULT_WINDOW
        )
        self.assertEqual(len(hits), len(case["queries"]))
        query_pairs = list(zip(case["queries"], hits))
        for source in case["required_sources"]:
            status = cold_start._required_source_status(query_pairs, source)
            self.assertTrue(
                status["found"],
                f"cold-start missed latest prefix source {source['path']}: {status}",
            )
            if source.get("commit"):
                self.assertEqual(status["source_origin"], "pinned_snapshot")
                self.assertEqual(
                    status["expected_commit"],
                    "d8d4e15488e483992fa63d6acc5d8053c2752ef5",
                )
                self.assertEqual(
                    status["expected_blob"], "c79e6019579f716c2935aee8de9314d0607b3a1a"
                )
        self.assertIn("matrix-past source term", case["scope_review"])
        self.assertIn("GR_closed=false", case["scope_review"])

    def test_binary_af_source_and_result_are_pinned_to_latest_owner_head(self) -> None:
        case = next(
            item for item in cold_start.CASES
            if item["id"] == "canonical-binary-af-endpoint-and-finite-source"
        )
        hits = proof.full_text_search_many(
            proof.ROOT, case["queries"], limit=cold_start.COLD_START_MIN_RESULT_WINDOW
        )
        self.assertEqual(len(hits), len(case["queries"]))
        query_pairs = list(zip(case["queries"], hits))
        for source in case["required_sources"]:
            status = cold_start._required_source_status(query_pairs, source)
            self.assertTrue(
                status["found"],
                f"cold-start missed binary AF source {source['path']}: {status}",
            )
            if source.get("commit"):
                self.assertEqual(status["source_origin"], "pinned_snapshot")
                self.assertEqual(
                    status["expected_commit"],
                    "9f5b757f699d7310ea69c0c889037f614533b4f7",
                )
                self.assertEqual(status["expected_blob"], source["blob"])
        self.assertIn("physical binary-interface admission", case["scope_review"])
        self.assertIn("GR_closed=false", case["scope_review"])

    def test_binary_af_rle_manifest_binds_all_emitted_word_files(self) -> None:
        word_dir = (
            proof.ROOT
            / "02_REGISTRY/research/sources/"
            / "d0_proof_architecture_formalization_2026-10-24/reports/"
            / "canonical_binary_af_words_2026-10-28"
        )
        manifest = json.loads((word_dir / "replay_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema"], "d0-canonical-binary-af-actuation-replay-v1")
        self.assertEqual(manifest["owner"]["commit"], "9f5b757f699d7310ea69c0c889037f614533b4f7")
        self.assertEqual(manifest["owner"]["checker_sha256"], "07c40e179d0446c52650e7a148c82ef33cd03d0349b0875b5b6af5acd7d9f3a5")
        self.assertEqual(manifest["owner"]["result_sha256"], "bc2addf30982c3c8ba219358d63f7913485c6877763c3e65dd824766b3620f1a")
        self.assertTrue(manifest["replay"]["stdout_byte_identical_across_modes"])
        self.assertTrue(manifest["replay"]["rle_files_identical_across_modes"])
        self.assertTrue(manifest["replay"]["matches_owner_result_except_environment"])
        self.assertEqual(manifest["replay"]["stderr_bytes"], 485)
        self.assertEqual(manifest["result"]["checks"], 12202)
        self.assertFalse(manifest["result"]["physical_binary_interface_admission_proved"])
        self.assertFalse(manifest["result"]["physical_input_preparation_executed"])
        for row in manifest["generated_words"]:
            data = (word_dir / row["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"])
            self.assertEqual(len(data), row["bytes"])
            word = json.loads(data)
            self.assertEqual(word["format"], "native-binary-rle-v1")
            self.assertEqual(word["full_binary_carrier_bits"], 16)
            self.assertEqual(word["stage_count"], 107530502)
            self.assertEqual(len(word["instructions"]), row["rle_instruction_records"])
            self.assertEqual(
                sum(int(instruction["repeat"]) for instruction in word["instructions"]),
                word["stage_count"],
            )
            self.assertTrue(all(
                instruction["op"] in {"G", "CX", "SourceI"}
                and not (set(instruction["wires"]) & (set(range(7, 13)) | {15}))
                for instruction in word["instructions"]
            ))

    def test_latest_canonical_tower_reports_are_pinned_to_the_clean_source_snapshot(self) -> None:
        report_dir = (
            proof.ROOT
            / "02_REGISTRY/research/sources/"
            / "d0_proof_architecture_formalization_2026-10-24/reports"
        )
        cold = json.loads(
            (report_dir / "proof_architecture_cold_start_summary_2026-10-28_cyclic_tower.json")
            .read_text(encoding="utf-8")
        )
        comparison = json.loads(
            (report_dir / "proof_architecture_search_process_comparison_2026-10-28_cyclic_tower.json")
            .read_text(encoding="utf-8")
        )
        snapshot = "17c9ca1e87c32ecdda209cf5ff515de6ca735792"
        for report in (cold, comparison):
            self.assertEqual(report["snapshot_commit"], snapshot)
            self.assertFalse(report["worktree_dirty"])
            for path, digest in report["authority_source_digests"].items():
                pinned_source = subprocess.check_output(["git", "show", f"{snapshot}:{path}"])
                self.assertEqual(hashlib.sha256(pinned_source).hexdigest(), digest)

        for path, key in (
            ("tools/proof_architecture_cold_start.py", "runner_sha256"),
            ("tools/proof_architecture.py", "search_engine_sha256"),
            ("tools/test_proof_architecture.py", "test_sha256"),
            ("tools/compact_proof_architecture_cold_start.py", "compactor_sha256"),
        ):
            pinned_source = subprocess.check_output(["git", "show", f"{snapshot}:{path}"])
            self.assertEqual(hashlib.sha256(pinned_source).hexdigest(), cold["replay"][key])
        comparison_runner = subprocess.check_output(
            ["git", "show", f"{snapshot}:tools/proof_architecture_process_comparison.py"]
        )
        self.assertEqual(
            hashlib.sha256(comparison_runner).hexdigest(), comparison["runner_sha256"]
        )

        self.assertEqual(cold["search_cases_found_all_sources"], 27)
        self.assertEqual(cold["search_cases_total"], 27)
        self.assertEqual(cold["benchmark_cases_total"], 28)
        self.assertEqual(cold["required_source_ref_count"], 175)
        self.assertTrue(cold["semantic_scope_review_is_manual"])
        tower_case = next(
            row for row in cold["cases"]
            if row["id"] == "canonical-af-tower-source-transport"
        )
        self.assertTrue(tower_case["all_required_sources_found"])
        owner = tower_case["required_sources"][
            "02_REGISTRY/research/A4D_CANONICAL_AF_TOWER_SOURCE_TRANSPORT_2026_10_28.md"
        ]
        self.assertEqual(owner["candidate_rank"], 1)
        self.assertEqual(owner["expected_commit"], "48500384e9a25b25a6a0f54911f5af50c2bc1625")
        self.assertEqual(owner["expected_blob"], "d8a4c467c225587e88525b2d42dcb785e381b38d")
        self.assertEqual(owner["citation_only_refs"][0]["pin_status"], "pinned_snapshot")

        metrics = comparison["metrics"]
        self.assertEqual(metrics["query_count"], 27)
        self.assertEqual(metrics["query_count_with_explicit_source_scope"], 10)
        self.assertEqual(metrics["legacy_scoped_queries_with_expected_source"], 0)
        self.assertEqual(metrics["current_scoped_queries_with_expected_source"], 10)
        self.assertEqual(metrics["current_scoped_queries_with_expected_source_assembly_owner_link"], 1)
        self.assertEqual(metrics["current_expected_source_references_with_formal_support_locator"], 7)
        self.assertEqual(metrics["current_expected_source_references_without_assembly_or_formal_support"], 6)
        self.assertTrue(metrics["semantic_review_required_for_all_queries"])

    def test_julia_cold_start_tracks_nonzero_chart_composition_boundary(self) -> None:
        case = next(
            item for item in cold_start.CASES
            if item["id"] == "julia-query-principal-frame-coframe-recovery"
        )
        scope = case["scope_review"]
        source_pin = next(
            source for source in case["required_sources"]
            if source["path"].endswith("A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md")
        )

        self.assertIn(
            "principalFrameJuliaQueryFamily_nonzero_shift_chart_coverage", scope
        )
        self.assertIn("det M = 1", scope)
        self.assertIn(
            "archiveJuliaSourceCARRaisingQuery_nonNull_recovery_of_proper_roleLorentz",
            scope,
        )
        self.assertIn(
            "principalFrameJuliaQueryFamily_nonNull_open_chart_joint_recovery_of_proper_roleLorentz",
            scope,
        )
        self.assertTrue(any(
            "principalFrameJuliaQueryFamily_recoveredInverseCoframe_hasFDerivAt" in query
            for query in case["queries"]
        ))
        self.assertTrue(any(
            "principalFrameJuliaQueryFamily_joint_coframe_endpoint_recovery_of_proper_roleLorentz"
            in query for query in case["queries"]
        ))
        self.assertTrue(any(
            "principalFrameJuliaQueryFamily_joint_coframe_all_role_endpoint_chart_coverage_of_proper_roleLorentz"
            in query for query in case["queries"]
        ))
        self.assertIn("composes the exact right-link transport to identity", scope)
        self.assertIn("identity derivative", scope)
        self.assertIn("24 link jets", scope)
        exact_query = next(
            query for query in case["queries"]
            if "principalFrameJuliaQueryFamily_recoveredInverseCoframe_hasFDerivAt" in query
        )
        hits = proof.full_text_search(proof.ROOT, exact_query, limit=3)
        self.assertEqual(
            [row["source"] for row in hits[:2]],
            [
                "03_FORMALIZATION/D0/Geometry/A4DJuliaPrincipalFrameRecovery.lean",
                "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/"
                "julia_principal_frame_fixed_link_recovered_derivative_declarations_2026-10-26.json",
            ],
        )
        joint_query = next(
            query for query in case["queries"]
            if "principalFrameJuliaQueryFamily_joint_coframe_endpoint_recovery_of_proper_roleLorentz"
            in query
        )
        joint_hits = proof.full_text_search(proof.ROOT, joint_query, limit=3)
        self.assertTrue(joint_hits)
        self.assertEqual(
            [row["source"] for row in joint_hits[:2]],
            [
                "03_FORMALIZATION/D0/Geometry/A4DJuliaRecoveryComposition.lean",
                "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/"
                "julia_all_role_coframe_endpoint_chart_declarations_2026-10-26.json",
            ],
        )
        all_role_query = next(
            query for query in case["queries"]
            if "principalFrameJuliaQueryFamily_joint_coframe_all_role_endpoint_chart_coverage_of_proper_roleLorentz"
            in query
        )
        all_role_hits = proof.full_text_search(proof.ROOT, all_role_query, limit=3)
        self.assertEqual(
            [row["source"] for row in all_role_hits[:2]],
            [
                "03_FORMALIZATION/D0/Geometry/A4DJuliaRecoveryComposition.lean",
                "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/"
                "julia_all_role_coframe_endpoint_chart_declarations_2026-10-26.json",
            ],
        )
        self.assertIn(15, source_pin["scope_query_indexes"])
        self.assertNotIn(14, source_pin["scope_query_indexes"])
        self.assertIn("IsRoleLorentz Λ", scope)
        self.assertIn("physical application must still bind the admitted endpoint", scope)
        self.assertIn(
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/proper_role_lorentz_endpoint_inventory_2026-10-25.json",
            case["required_refs"],
        )
        self.assertIn(
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/proper_role_lorentz_joint_recovery_inventory_2026-10-25.json",
            case["required_refs"],
        )
        self.assertIn(
            "03_FORMALIZATION/D0/Geometry/A4DJuliaRecoveryComposition.lean",
            case["required_refs"],
        )
        self.assertTrue(any(
            "principalFrameJuliaQueryFamily_nonzero_shift_chart_coverage" in query
            for query in case["queries"]
        ))
        self.assertTrue(any(
            "principalFrameJuliaQueryFamily_nonNull_open_chart_joint_recovery_of_proper_roleLorentz"
            in query
            for query in case["queries"]
        ))
        exact_joint_recovery_query = next(
            query for query in case["queries"]
            if query.startswith(
                "principalFrameJuliaQueryFamily_nonNull_open_chart_joint_recovery_of_proper_roleLorentz"
            )
        )
        exact_joint_recovery_hits = proof.full_text_search(
            proof.ROOT, exact_joint_recovery_query, limit=18
        )
        self.assertIn(
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/"
            "proper_role_lorentz_joint_recovery_inventory_2026-10-25.json",
            [row["source"] for row in exact_joint_recovery_hits],
        )

    def test_julia_tangent_cold_start_reuses_exact_24_dimensional_api(self) -> None:
        case = next(
            item for item in cold_start.CASES
            if item["id"] == "labelled-native-raising-inverse"
        )
        self.assertTrue(any(
            "roleLorentzTangentParameters_finrank" in query
            for query in case["queries"]
        ))
        self.assertIn("real dimension 24", case["scope_review"])
        self.assertIn("RolePair → ℝ", case["scope_review"])
        self.assertIn("same constructed Julia query family", case["scope_review"])
        self.assertIn("joint directional derivative", case["scope_review"])
        self.assertIn("any supplied proper rolewise Lorentz link", case["scope_review"])
        self.assertIn("right-translates those same tangent coordinates", case["scope_review"])
        self.assertIn("not a claim that the exponential is a global chart", case["scope_review"])
        self.assertIn(
            "full Fréchet derivative on the 16 coframe matrix entries and 24 canonical Lorentz tangent coordinates",
            case["scope_review"],
        )
        self.assertTrue(any(
            "principalFrameJuliaEndpointChartReadoutAlongLorentzTangentInCoordinates_hasFDerivAt"
            in query
            for query in case["queries"]
        ))
        self.assertTrue(any(
            "principalFrameJuliaJointCoframeEndpointReadoutAlongLorentzTangent_hasDerivAt"
            in query
            for query in case["queries"]
        ))
        self.assertTrue(any(
            "principalFrameJuliaJointCoframeEndpointReadoutInCoordinates_hasFDerivAt"
            in query
            for query in case["queries"]
        ))
        self.assertTrue(any(
            "principalFrameJuliaJointCoframeEndpointReadoutAtBaseInCoordinates_hasFDerivAt"
            in query
            for query in case["queries"]
        ))
        self.assertIn(
            "03_FORMALIZATION/D0/Geometry/A4DSolderMetricCompletion.lean",
            case["required_refs"],
        )
        self.assertIn(
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/"
            "julia_lorentz_tangent_dimension_reuse_declarations_2026-10-26.json",
            case["required_refs"],
        )
        base_link_inventory_rel = (
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/"
            "julia_joint_coframe_base_link_frechet_declarations_2026-10-26_v2.json"
        )
        self.assertIn(base_link_inventory_rel, case["required_refs"])
        coordinate_inventory_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/"
            "julia_joint_coframe_local_frechet_derivative_declarations_2026-10-26_julia_base_link_frechet_v2.json"
        )
        self.assertIn(
            coordinate_inventory_path.relative_to(proof.ROOT).as_posix(),
            case["required_refs"],
        )
        joint_frechet_inventory_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/"
            "julia_joint_coframe_local_frechet_derivative_declarations_2026-10-26_julia_base_link_frechet_v2.json"
        )
        self.assertIn(
            joint_frechet_inventory_path.relative_to(proof.ROOT).as_posix(),
            case["required_refs"],
        )
        joint_frechet_inventory = json.loads(
            joint_frechet_inventory_path.read_text(encoding="utf-8")
        )
        self.assertEqual(
            joint_frechet_inventory["schema"], "d0-lean-declaration-inventory-v1"
        )
        self.assertRegex(joint_frechet_inventory["snapshot_commit"], r"^[0-9a-f]{40}$")
        assert_historical_compiled_inventory(self, joint_frechet_inventory)
        joint_frechet_declarations = {
            row["name"]: row for row in joint_frechet_inventory["declarations"]
        }
        joint_frechet = joint_frechet_declarations[
            "D0.Geometry.principalFrameJuliaJointCoframeEndpointReadoutInCoordinates_hasFDerivAt"
        ]
        self.assertEqual(
            joint_frechet["module"], "D0.Geometry.A4DJuliaLinkPathDifferential"
        )
        self.assertEqual(joint_frechet["declaration_kind"], "theorem")
        self.assertIn("Matrix D0.Role D0.Role ℝ", joint_frechet["elaborated_type"])
        joint_coordinates = joint_frechet_declarations[
            "D0.Geometry.principalFrameJuliaJointCoframeEndpointReadoutInCoordinates"
        ]
        self.assertIn("D0.Geometry.RolePair → ℝ", joint_coordinates["elaborated_type"])
        joint_differential_apply = joint_frechet_declarations[
            "D0.Geometry.principalFrameJuliaJointCoframeEndpointFDerivInCoordinates_apply"
        ]
        self.assertIn("D0.Geometry.RolePair → ℝ", joint_differential_apply["elaborated_type"])
        self.assertIn("(H, fun r =>", joint_differential_apply["elaborated_type"])
        self.assertIn(
            "D0.Geometry.rolePairsEquivLorentzTangent",
            joint_differential_apply["proof_dependencies"],
        )
        self.assertIn(
            "D0.Geometry.principalFrameJuliaQueryFamily_recoveredInverseCoframe",
            joint_frechet["proof_dependencies"],
        )
        self.assertEqual(
            set(joint_frechet["axioms"]),
            {
                "Classical.choice",
                "Quot.sound",
                "propext",
                "_private.D0.Geometry.ArchiveJuliaRaisingOperatorReadout.0.D0.Geometry.archiveCreatorPermSign._native.native_decide.ax_1_1",
            },
        )
        base_link_inventory = json.loads(
            (proof.ROOT / base_link_inventory_rel).read_text(encoding="utf-8")
        )
        self.assertEqual(
            base_link_inventory["schema"], "d0-lean-declaration-inventory-v1"
        )
        self.assertRegex(base_link_inventory["snapshot_commit"], r"^[0-9a-f]{40}$")
        self.assertFalse(base_link_inventory["worktree_dirty"])
        assert_historical_compiled_inventory(self, base_link_inventory)
        base_link_declarations = {
            row["name"]: row for row in base_link_inventory["declarations"]
        }
        self.assertEqual(
            set(base_link_inventory["request"]["full_names"]),
            set(base_link_declarations),
        )
        base_link_frechet = base_link_declarations[
            "D0.Geometry.principalFrameJuliaJointCoframeEndpointReadoutAtBaseInCoordinates_hasFDerivAt"
        ]
        self.assertEqual(
            base_link_frechet["module"], "D0.Geometry.A4DJuliaLinkPathDifferential"
        )
        self.assertEqual(base_link_frechet["declaration_kind"], "theorem")
        self.assertIn("D0.Geometry.IsRoleLorentz", base_link_frechet["elaborated_type"])
        self.assertIn(".det = 1", base_link_frechet["elaborated_type"])
        self.assertIn(
            "D0.Geometry.principalFrameJuliaQueryFamily_recoveredInverseCoframe",
            base_link_frechet["proof_dependencies"],
        )
        self.assertIn(
            "D0.Geometry.principalFrameJuliaEndpointChartReadout_eq",
            base_link_frechet["proof_dependencies"],
        )
        self.assertIn(
            "D0.Geometry.archiveJuliaProperRoleLorentzEquiv_form_isometry",
            base_link_frechet["proof_dependencies"],
        )
        self.assertEqual(
            set(base_link_frechet["axioms"]), set(joint_frechet["axioms"])
        )
        base_link_differential = base_link_declarations[
            "D0.Geometry.principalFrameJuliaJointCoframeEndpointFDerivAtBaseInCoordinates_apply"
        ]
        self.assertIn("RolePair → ℝ", base_link_differential["elaborated_type"])
        self.assertIn("Λ₀ r", base_link_differential["elaborated_type"])
        inventory = json.loads(coordinate_inventory_path.read_text(encoding="utf-8"))
        self.assertEqual(inventory["schema"], "d0-lean-declaration-inventory-v1")
        self.assertFalse(inventory["worktree_dirty"])
        assert_historical_compiled_inventory(self, inventory)
        declarations = {row["name"]: row for row in inventory["declarations"]}
        self.assertEqual(set(inventory["request"]["full_names"]), set(declarations))
        self.assertEqual(
            declarations[
                "D0.Geometry.roleLorentzTangentParametersEquivCoordinates"
            ]["module"],
            "D0.Geometry.A4DJuliaLinkPathDifferential",
        )
        self.assertIn(
            "D0.Geometry.rolePairsEquivLorentzTangent",
            declarations[
                "D0.Geometry.roleLorentzTangentEndpointFDerivInCoordinates_apply"
            ]["proof_dependencies"],
        )
        self.assertIn(
            "D0.Role → D0.Geometry.RolePair → ℝ",
            declarations[
                "D0.Geometry.roleLorentzTangentEndpointFDerivInCoordinates"
            ]["elaborated_type"],
        )
        coordinate_chart_derivative = declarations[
            "D0.Geometry.principalFrameJuliaEndpointChartReadoutAlongLorentzTangentInCoordinates_hasFDerivAt"
        ]
        self.assertEqual(
            coordinate_chart_derivative["module"],
            "D0.Geometry.A4DJuliaLinkPathDifferential",
        )
        self.assertIn(
            "D0.Geometry.principalFrameJuliaEndpointChartReadoutAlongLorentzTangent_hasFDerivAt",
            coordinate_chart_derivative["proof_dependencies"],
        )
        self.assertIn(
            "D0.Geometry.roleLorentzTangentParametersEquivCoordinates",
            coordinate_chart_derivative["proof_dependencies"],
        )
        joint_path_derivative = declarations[
            "D0.Geometry.principalFrameJuliaJointCoframeEndpointReadoutAlongLorentzTangent_hasDerivAt"
        ]
        self.assertEqual(
            joint_path_derivative["module"],
            "D0.Geometry.A4DJuliaLinkPathDifferential",
        )
        self.assertIn(
            "D0.Geometry.principalFrameJuliaQueryFamily_recoveredInverseCoframe",
            joint_path_derivative["proof_dependencies"],
        )
        self.assertIn(
            "D0.Geometry.principalFrameJuliaEndpointChartReadout_hasDerivAt_of_jointCoframeAndLorentzTangent",
            joint_path_derivative["proof_dependencies"],
        )
        self.assertIn(
            "D0.Geometry.roleLorentzTangentParametersEquivCoordinates",
            joint_path_derivative["proof_dependencies"],
        )
        self.assertIn(
            "principalFrameJuliaJointCoframeEndpointReadoutAlongLorentzTangent",
            joint_path_derivative["elaborated_type"],
        )
        self.assertIn("(H, fun r =>", joint_path_derivative["elaborated_type"])
        self.assertIn("RolePair → ℝ", joint_path_derivative["elaborated_type"])
        coordinate_query = next(
            query for query in case["queries"]
            if "principalFrameJuliaEndpointChartReadoutAlongLorentzTangentInCoordinates_hasFDerivAt"
            in query
        )
        coordinate_hits = proof.full_text_search(
            proof.ROOT, coordinate_query,
            limit=cold_start.COLD_START_MIN_RESULT_WINDOW,
        )
        surfaced = {hit["source"] for hit in coordinate_hits}
        self.assertIn(
            "03_FORMALIZATION/D0/Geometry/A4DJuliaLinkPathDifferential.lean",
            surfaced,
        )
        self.assertIn(
            coordinate_inventory_path.relative_to(proof.ROOT).as_posix(),
            surfaced,
        )
        joint_path_query = next(
            query for query in case["queries"]
            if "principalFrameJuliaJointCoframeEndpointReadoutAlongLorentzTangent_hasDerivAt"
            in query
        )
        joint_path_hits = proof.full_text_search(
            proof.ROOT, joint_path_query,
            limit=cold_start.COLD_START_MIN_RESULT_WINDOW,
        )
        joint_path_surfaced = {hit["source"] for hit in joint_path_hits}
        self.assertIn(
            "03_FORMALIZATION/D0/Geometry/A4DJuliaLinkPathDifferential.lean",
            joint_path_surfaced,
        )
        self.assertIn(
            coordinate_inventory_path.relative_to(proof.ROOT).as_posix(),
            joint_path_surfaced,
        )
        joint_frechet_query = next(
            query for query in case["queries"]
            if "principalFrameJuliaJointCoframeEndpointReadoutInCoordinates_hasFDerivAt"
            in query
            and "julia_joint_coframe_local_frechet_derivative_declarations_2026-10-26_julia_base_link_frechet_v2"
            in query
        )
        joint_frechet_hits = proof.full_text_search(
            proof.ROOT, joint_frechet_query,
            limit=cold_start.COLD_START_MIN_RESULT_WINDOW,
        )
        joint_frechet_surfaced = {hit["source"] for hit in joint_frechet_hits}
        self.assertIn(
            "03_FORMALIZATION/D0/Geometry/A4DJuliaLinkPathDifferential.lean",
            joint_frechet_surfaced,
        )
        self.assertIn(
            joint_frechet_inventory_path.relative_to(proof.ROOT).as_posix(),
            joint_frechet_surfaced,
        )
        base_link_query = next(
            query for query in case["queries"]
            if "principalFrameJuliaJointCoframeEndpointReadoutAtBaseInCoordinates_hasFDerivAt"
            in query
        )
        base_link_hits = proof.full_text_search(
            proof.ROOT, base_link_query,
            limit=cold_start.COLD_START_MIN_RESULT_WINDOW,
        )
        base_link_surfaced = {hit["source"] for hit in base_link_hits}
        self.assertIn(
            "03_FORMALIZATION/D0/Geometry/A4DJuliaLinkPathDifferential.lean",
            base_link_surfaced,
        )
        self.assertIn(base_link_inventory_rel, base_link_surfaced)

    def test_transfer_cold_start_pins_actual_controls_and_conditional_bridge(self) -> None:
        case = next(
            item for item in cold_start.CASES
            if item["id"] == "verification-kernel-transfer-outside-gr"
        )
        required_names = (
            "visible_only_memory_cannot_decode_hiddenBit_futures",
            "sufficient_encoder_injective_of_profile_injective",
            "sufficient_memory_cardinality_lower_bound",
            "erased_hiddenBit_operation_map_is_impossible",
            "verified_visibleFalseReadout_transfers_to_common_execution",
            "connes_reconstruction_conditional",
        )

        self.assertIn(
            "03_FORMALIZATION/D0/Foundation/VerificationTransferApplication.lean",
            case["required_refs"],
        )
        self.assertIn(
            "03_FORMALIZATION/D0/Bridge/ConnesReconstructionBridge.lean",
            case["required_refs"],
        )
        self.assertIn(
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/future_profile_memory_cardinality_declarations_2026-10-25.json",
            case["required_refs"],
        )
        for declaration in required_names:
            self.assertTrue(any(declaration in query for query in case["queries"]))
            self.assertIn(declaration, case["scope_review"])
        self.assertTrue(any(
            "sufficient_memory_reflects_future" in query for query in case["queries"]
        ))
        self.assertIn("sufficient_memory_reflects_future", case["scope_review"])
        self.assertIn("conditional on supplied ConnesReconstruction fields",
                      case["scope_review"])
        self.assertIn("do not select a physical execution", case["scope_review"])

    def test_native_weighted_dirac_cold_start_keeps_source_and_transfer_scopes(self) -> None:
        case = next(
            item for item in cold_start.CASES
            if item["id"] == "native-weighted-dirac-matrix-application"
        )

        self.assertIn(
            "03_FORMALIZATION/D0/Research/NativeWeightedDiracLinearOperator.lean",
            case["required_refs"],
        )
        self.assertIn(
            "03_FORMALIZATION/D0/Research/NativeWeightedDiracNyquistApplication.lean",
            case["required_refs"],
        )
        self.assertIn(
            "03_FORMALIZATION/D0/Geometry/ArchiveLorentzianFourierApplication.lean",
            case["required_refs"],
        )
        self.assertIn(
            "03_FORMALIZATION/D0/Geometry/ArchiveLorentzianCARDiracApplication.lean",
            case["required_refs"],
        )
        self.assertIn(
            "03_FORMALIZATION/D0/Research/NativeWeightedDiracFourierNullModes.lean",
            case["required_refs"],
        )
        self.assertIn(
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/native_weighted_dirac_fourier_null_modes_declarations_2026-10-25.json",
            case["required_refs"],
        )
        self.assertIn(
            "03_FORMALIZATION/D0/Algebra/FiniteWeightedAdjoint.lean",
            case["required_refs"],
        )
        self.assertIn(
            "03_FORMALIZATION/D0/Geometry/ArchiveWeightedHodgeDirac.lean",
            case["required_refs"],
        )
        self.assertIn(
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/weighted_cubical_hodge_standard_representative_claim_reuse_2026-10-25.json",
            case["required_refs"],
        )
        self.assertIn(
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/archive_lorentzian_fourier_module_declarations_2026-10-25.json",
            case["required_refs"],
        )
        self.assertIn(
            "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/archive_lorentzian_car_fourier_fiber_action_declarations_2026-10-25.json",
            case["required_refs"],
        )
        self.assertIn(
            "02_REGISTRY/research/certificates/a4d_native_weighted_dirac_boundary.lean",
            case["required_refs"],
        )
        self.assertIn("db3091aded8f6cfe8d39dcd973ccf30ec40dfb08", case["scope_review"])
        self.assertIn("c3ceba511bab5c435d715fd56382615fc1dc1505", case["scope_review"])
        self.assertIn("a6ff3f2fc7e0e6b94d673c2cd713cb4faeb94004", case["scope_review"])
        self.assertIn("not physically derived", case["scope_review"])
        self.assertTrue(any("weightedDiracMatrix_mulVec" in query for query in case["queries"]))
        self.assertTrue(any("hodgeCarDiracMatrix_mulVec" in query
                            for query in case["queries"]))
        self.assertTrue(any("weightedDiracLinear_identity_eq_hodgeCarDirac" in query
                            for query in case["queries"]))
        self.assertTrue(any("hodgeCarDiracMatrix_symmetric" in query
                            for query in case["queries"]))
        self.assertTrue(any(
            "archiveLorentzian_full_cochain_kernel_finrank_ge_diagonal_family" in query
            for query in case["queries"]
        ))
        self.assertTrue(any(
            "null_mode_kernel_eq_range null_mode_kernel_half_dimension DivisionRing" in query
            for query in case["queries"]
        ))
        self.assertTrue(any(
            "finiteHermitianPairing_weightSquareRoot finiteWeightedConjugate_self_adjoint" in query
            for query in case["queries"]
        ))
        self.assertTrue(any(
            "cubicalWeightedHodgeDirac_standard_representative_application" in query
            for query in case["queries"]
        ))
        self.assertTrue(any("weightedDiracMatrix_symmetric_of_finiteHermitianAdjoint_eq_self"
                            in query for query in case["queries"]))
        self.assertTrue(any("spatialNyquist_weightedDirac_matrix_block" in query
                            for query in case["queries"]))
        self.assertTrue(any("spatialNyquistEven_weightedDirac_matrix_block" in query
                            for query in case["queries"]))
        self.assertTrue(any("flatLorentzWeightedDiracEven_no_positive_selfadjoint_pairing"
                            in query for query in case["queries"]))
        self.assertIn("even archive period N+2", case["scope_review"])
        self.assertIn("all-size character eigenbasis", case["scope_review"])
        self.assertIn("explicitly role-signed first-order CAR operator", case["scope_review"])
        self.assertIn("all-size squared-mode law", case["scope_review"])
        self.assertIn("direct first-order Fourier action", case["scope_review"])
        self.assertIn("finite CAR map on each Fock profile", case["scope_review"])
        self.assertIn("does not make an arbitrary profile a first-order eigenvector",
                      case["scope_review"])
        self.assertIn("physical action/source selection", case["scope_review"])
        self.assertTrue(any("archiveLorentzianDifferenceLaplacian_fourier" in query
                            for query in case["queries"]))
        self.assertTrue(any("archiveLorentzianDifferenceOperator_fourier_mode" in query
                            for query in case["queries"]))
        self.assertTrue(any("archiveLorentzianCARDirac_square_fourier_mode" in query
                            for query in case["queries"]))
        self.assertTrue(any("roleWeightedArchiveCARDirac_fourier_mode" in query
                            for query in case["queries"]))
        self.assertTrue(any("roleWeightedArchiveFourierFockAction_square" in query
                            for query in case["queries"]))
        self.assertTrue(any("archiveLorentzianCARFourierFockAction_square" in query
                            for query in case["queries"]))
        self.assertTrue(any("archiveRoleFourierInversion" in query
                            for query in case["queries"]))

    def test_car_hodge_cold_start_keeps_distinct_operator_claims(self) -> None:
        case = next(
            item for item in cold_start.CASES
            if item["id"] == "car-scaffolds-vs-hodge-operator-claims"
        )
        hits_by_query = proof.full_text_search_many(
            proof.ROOT, case["queries"], limit=18
        )
        query_pairs = list(zip(case["queries"], hits_by_query))

        for path in case["required_refs"]:
            status = cold_start._required_source_status(query_pairs, {"path": path})
            self.assertTrue(status["found"], f"cold-start search missed {path}")

        inventory_root = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
        )
        standard_axioms = {"Classical.choice", "Quot.sound", "propext"}
        hodge_square_axioms = standard_axioms | {
            "D0.Geometry.car_create_anticommutator_int._native.native_decide.ax_1_1",
            "D0.Geometry.car_mixed_anticommutator_int._native.native_decide.ax_1_1",
        }
        car_square_l2_no_go_axioms = standard_axioms | {
            "D0.Geometry.carAnnihilateInt_support._native.native_decide.ax_1_1",
            "D0.Geometry.carCreateInt_singleton_vacuum._native.native_decide.ax_1_1",
        }
        car_l2_square_axioms = standard_axioms | {
            "D0.Geometry.car_annihilate_anticommutator_int._native.native_decide.ax_1_1",
            "D0.Geometry.car_create_anticommutator_int._native.native_decide.ax_1_1",
            "D0.Geometry.car_mixed_anticommutator_int._native.native_decide.ax_1_1",
            "_private.D0.Geometry.ArchiveCARDirac.0.D0.Geometry.spatialL2Int_comm_pointwise._native.native_decide.ax_1_1",
            "_private.D0.Geometry.ArchiveCARDirac.0.D0.Geometry.spatialL2Int_sq_pointwise._native.native_decide.ax_1_1",
        }

        def declarations(filename: str, *, require_current: bool = False) -> dict[str, dict]:
            inventory = json.loads((inventory_root / filename).read_text(encoding="utf-8"))
            self.assertEqual(inventory["schema"], "d0-lean-declaration-inventory-v1")
            self.assertTrue(inventory.get("snapshot_commit"), f"missing snapshot in {filename}")
            self.assertTrue(inventory.get("collector_sha256"), f"missing collector pin in {filename}")
            if require_current:
                self.assertEqual(
                    inventory["lean_source_digest"], lean_task_build.source_digest(),
                    f"stale Lean source digest in {filename}",
                )
            else:
                assert_historical_compiled_inventory(self, inventory)
            return {
                row["name"]: row
                for row in inventory["declarations"]
                if row.get("exists")
            }

        current_inventory = declarations(
            "car_hodge_diagonal_transpose_current_declaration_inventory_2026-10-26_julia_base_link_frechet.json",
            require_current=False,
        )

        def has_type(
            name: str, *fragments: str, expected_axioms=None,
        ) -> dict:
            row = current_inventory.get(name)
            self.assertIsNotNone(row, f"compiled inventory missed {name}")
            assert row is not None
            signature = row.get("elaborated_type", "")
            for fragment in fragments:
                self.assertIn(fragment, signature, f"unexpected type for {name}")
            self.assertEqual(row.get("declaration_kind"), "theorem")
            self.assertIsInstance(row.get("axioms"), list)
            if expected_axioms is not None:
                self.assertEqual(
                    set(row["axioms"]), expected_axioms,
                    f"changed trust footprint for {name}",
                )
            return row

        has_type("D0.Geometry.car_zero_mode_independent_of_L",
                 "carDiracKernelDim = 16", expected_axioms=set())
        has_type("D0.Geometry.carDiracSquareScalarSectorFactor_eq_fock_dim",
                 "carDiracSquareScalarSectorFactor = Fintype.card",
                 expected_axioms=standard_axioms)
        has_type(
            "D0.Geometry.carDirac_square_ne_archiveMetricProductLaplacian_at_zero",
            "D0.Geometry.carDirac 0 * D0.Geometry.carDirac 0 ≠",
            "D0.Geometry.tensorProduct",
            "archiveMetricProductLaplacian 0",
            expected_axioms=car_square_l2_no_go_axioms,
        )
        has_type(
            "D0.Geometry.carDirac_square_eq_four_id_at_zero",
            "D0.Geometry.carDirac 0 * D0.Geometry.carDirac 0 = 4 • 1",
            expected_axioms=car_l2_square_axioms,
        )
        has_type(
            "D0.Geometry.carDirac_zero_kernel_trivial_at_zero",
            "D0.Geometry.CARHilbertPoint 0 → ℝ",
            "Matrix.mulVec (D0.Geometry.carDirac 0) v = 0 → v = 0",
            expected_axioms=car_l2_square_axioms,
        )
        has_type("D0.Geometry.car_amplification_times_spinor_eq_sixteen",
                 "carDiracAmplificationFactor * 4 = Fintype.card",
                 expected_axioms=standard_axioms)
        has_type("D0.Geometry.diracHeatTraceMultiplicity_eq_fock_dim",
                 "diracHeatTraceMultiplicity = Fintype.card",
                 expected_axioms=standard_axioms)

        has_type(
            "D0.Geometry.hodgeCarDirac_sq",
            "ArchiveCochain N",
            "hodgeCarDirac N (D0.Geometry.hodgeCarDirac N ψ) =",
            "cochainDifferenceLaplacian N ψ",
            expected_axioms=hodge_square_axioms,
        )
        has_type(
            "D0.Geometry.hodgeCarDirac_kernel_finrank",
            "Module.finrank ℝ",
            "hodgeCarDiracₗ N",
            ".ker = 16",
            expected_axioms=hodge_square_axioms,
        )
        has_type(
            "D0.Geometry.cochainDifferenceLaplacian_eq_backward_forward",
            "∑ r, -D0.Geometry.backwardSite",
            "D0.Geometry.forwardSite",
            expected_axioms=standard_axioms,
        )
        has_type(
            "D0.Geometry.hodge_difference_diagonal_double_metric_at_l2",
            "=\n    2 * D0.Geometry.ArchiveRoleProductLaplacian.archiveMetricProductLaplacian",
            expected_axioms=standard_axioms,
        )
        has_type(
            "D0.Geometry.spatialShellSubmodule_finrank",
            "3 ≤ D0.archiveFibers N",
            "= 96",
            expected_axioms=standard_axioms,
        )
        has_type(
            "D0.Geometry.shellEnergy_tendsto_two_pi",
            "nhds (2 * Real.pi)",
            expected_axioms=standard_axioms,
        )
        has_type(
            "D0.Geometry.spatial_shell_rank_l2",
            "= 48",
            expected_axioms=standard_axioms,
        )
        tensor_square = has_type(
            "D0.Algebra.finiteMatrixTensorProduct_sum_square_eq_diagonal",
            "finiteMatrixTensorProduct",
            "G i * G j + G j * G i",
            "if i = j then 2 else 0",
            expected_axioms=standard_axioms,
        )
        self.assertEqual(
            {binder["name"] for binder in tensor_square["binders"]
             if binder["is_proposition"]},
            {"hAcomm", "hGanti"},
        )
        tensor_square_dependencies = set(tensor_square["proof_dependencies"])
        self.assertIn(
            "D0.Algebra.finiteMatrixTensorProduct_add_right",
            tensor_square_dependencies,
        )
        self.assertIn(
            "D0.Algebra.finiteMatrixTensorProduct_smul_right",
            tensor_square_dependencies,
        )
        has_type(
            "D0.Algebra.finiteMatrixTensorProduct_mul",
            "D0.Algebra.finiteMatrixTensorProduct A B * "
            "D0.Algebra.finiteMatrixTensorProduct C D",
            "D0.Algebra.finiteMatrixTensorProduct (A * C) (B * D)",
            expected_axioms=standard_axioms,
        )
        has_type(
            "D0.Algebra.finiteMatrixTensorProduct_add_right",
            "D0.Algebra.finiteMatrixTensorProduct A (B + C)",
            "D0.Algebra.finiteMatrixTensorProduct A B + "
            "D0.Algebra.finiteMatrixTensorProduct A C",
            expected_axioms={"Quot.sound", "propext"},
        )
        has_type(
            "D0.Algebra.finiteMatrixTensorProduct_smul_right",
            "D0.Algebra.finiteMatrixTensorProduct A (c • B)",
            "c • D0.Algebra.finiteMatrixTensorProduct A B",
            expected_axioms={"Quot.sound", "propext"},
        )
        tensor_transpose = has_type(
            "D0.Algebra.finiteMatrixTensorProduct_transpose",
            "D0.Algebra.finiteMatrixTensorProduct A B).transpose",
            "D0.Algebra.finiteMatrixTensorProduct A.transpose B.transpose",
            expected_axioms={"Quot.sound", "propext"},
        )
        self.assertFalse(any(
            binder["is_proposition"] for binder in tensor_transpose["binders"]
        ))
        spatial_identity_symmetry = has_type(
            "D0.Geometry.spatialIdMatrix_symmetric",
            "D0.Geometry.spatialIdMatrix n).transpose",
            "D0.Geometry.spatialIdMatrix n",
            expected_axioms=standard_axioms,
        )
        fock_parity_symmetry = has_type(
            "D0.Geometry.fockParityMatrix_symmetric",
            "D0.Geometry.fockParityMatrix.transpose",
            "D0.Geometry.fockParityMatrix",
            expected_axioms=standard_axioms,
        )
        self.assertIn(
            "Matrix.diagonal_transpose",
            spatial_identity_symmetry["proof_dependencies"],
        )
        self.assertIn(
            "Matrix.diagonal_transpose",
            fock_parity_symmetry["proof_dependencies"],
        )
        has_type(
            "D0.Algebra.finiteMatrixTensorProduct_one",
            "D0.Algebra.finiteMatrixTensorProduct 1 1 = 1",
            expected_axioms={"Quot.sound", "propext"},
        )
        tensor_mul = has_type(
            "D0.Geometry.tensorProduct_mul",
            "D0.Geometry.tensorProduct A B * D0.Geometry.tensorProduct C D",
            expected_axioms=standard_axioms,
        )
        self.assertIn(
            "D0.Algebra.finiteMatrixTensorProduct_mul",
            tensor_mul["proof_dependencies"],
        )
        tensor_product_transpose = has_type(
            "D0.Geometry.tensorProduct_transpose",
            "D0.Geometry.tensorProduct A B).transpose",
            "D0.Geometry.tensorProduct A.transpose B.transpose",
            expected_axioms=standard_axioms,
        )
        self.assertIn(
            "D0.Algebra.finiteMatrixTensorProduct_transpose",
            tensor_product_transpose["proof_dependencies"],
        )
        parity_symmetry = has_type(
            "D0.Geometry.totalParityOperator_symmetric",
            "Matrix.transpose (D0.Geometry.totalParityOperator n) =",
            expected_axioms=standard_axioms,
        )
        for dependency in (
            "D0.Geometry.tensorProduct_transpose",
            spatial_identity_symmetry["name"],
            fock_parity_symmetry["name"],
        ):
            self.assertIn(dependency, parity_symmetry["proof_dependencies"])

        dataset = proof.load_dataset(proof.ROOT)
        support_modules = {row["lean_module"] for row in dataset["formal_support"]}
        self.assertIn("D0.Geometry.ArchiveHodgeCARDiracKernel", support_modules)
        self.assertIn("D0.Geometry.ArchiveHodgeCARDiracSquare", support_modules)
        self.assertIn("D0.Geometry.ArchiveHodgeCARDiracShell", support_modules)
        self.assertNotIn("D0.Geometry.ArchiveCARDirac", support_modules)
        claims = {row["claim_id"]: row for row in dataset["claims"]}
        source_view = json.loads(
            (inventory_root / "claim_source_candidates_current.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(source_view["schema"], "d0-claim-source-candidate-view-v3")
        source_rows = {row["claim_id"]: row for row in source_view["rows"]}
        for claim_id in (
            "D0-ARCHIVE-CAR-ZERO-MODE-OWNER-001",
            "D0-ARCHIVE-CAR-DIRAC-SQUARE-001",
            "D0-ARCHIVE-CAR-SPECTRUM-AMPLIFICATION-001",
            "D0-ARCHIVE-DIRAC-HEATTRACE-MULTIPLICITY-001",
        ):
            self.assertEqual(claims[claim_id]["lean_status"], "OPEN")
            source_row = source_rows[claim_id]
            self.assertEqual(source_row["resolution_status"], "unresolved")
            self.assertEqual(source_row["literal_claim_id_mentions"], [])
            self.assertFalse(any(
                pair.get("candidates") for pair in source_row["locator_pairs"]
            ))
        square_note = claims["D0-ARCHIVE-CAR-DIRAC-SQUARE-001"]["notes"]
        self.assertIn("ArchiveHodgeCARDiracSquare proves the exact square", square_note)
        self.assertIn("typed map from hodgeCarDirac", square_note)
        self.assertIn("Keep OPEN", square_note)
        self.assertNotIn("EXACT MISSING: D_H squared", square_note)
        self.assertEqual(
            claims["D0-SPATIAL-HODGE-SHELL-OPERATOR-001"]["lean_status"],
            "LEAN_PROVED",
        )
        self.assertIn("remain OPEN", case["scope_review"])
        self.assertIn("finite L=2 no-kernel theorem", case["scope_review"])
        self.assertIn("no operator intertwiner", case["scope_review"])
        self.assertIn("formal_support.csv", case["scope_review"])
        self.assertIn("no exact heading", case["scope_review"])
        self.assertIn("L=2 shell rank is 48", case["scope_review"])
        self.assertTrue(any("actual" in query and "carDirac" in query
                            for query in case["queries"]))
        self.assertTrue(any("car_amplification_times_spinor_eq_sixteen" in query
                            for query in case["queries"]))
        self.assertTrue(any("diracHeatTraceMultiplicity_eq_fock_dim" in query
                            for query in case["queries"]))
        self.assertTrue(any("hodgeCarDirac_sq" in query for query in case["queries"]))
        self.assertTrue(any("hodgeCarDirac_kernel_finrank" in query
                            for query in case["queries"]))

    def test_shared_linear_map_coordinate_action_is_rediscoverable(self) -> None:
        case = next(
            item for item in cold_start.CASES
            if item["id"] == "finite-hermitian-adjoint-twisted-car-application"
        )
        query = "finiteLinearMap_apply_eq_sum_single finite coordinate basis action"
        source = "03_FORMALIZATION/D0/Algebra/FiniteCoordinateBasis.lean"
        self.assertIn(query, case["queries"])
        self.assertIn(source, case["required_refs"])
        hits = proof.full_text_search_many(proof.ROOT, [query], limit=18)[0]
        self.assertTrue(any(
            hit["source"] == source and hit["direct_content"]
            for hit in hits
        ))

    def test_shared_finite_coordinate_expansion_is_in_both_adjoint_proofs(self) -> None:
        inventory_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "car_hodge_diagonal_transpose_current_declaration_inventory_2026-10-26_julia_base_link_frechet_v2.json"
        )
        inventory_bytes = inventory_path.read_bytes()
        inventory = json.loads(inventory_bytes)
        self.assertEqual(inventory["schema"], "d0-lean-declaration-inventory-v1")
        self.assertRegex(inventory["snapshot_commit"], r"^[0-9a-f]{40}$")
        assert_historical_compiled_inventory(self, inventory)
        self.assertEqual(inventory["public_import_root"], "D0.All")
        self.assertEqual(inventory["toolchain"], "leanprover/lean4:v4.30.0")

        declarations = {row["name"]: row for row in inventory["declarations"]}
        basis = declarations["D0.Algebra.finiteCoordinate_eq_sum_single"]
        linear_map_action = declarations[
            "D0.Algebra.finiteLinearMap_apply_eq_sum_single"
        ]
        hermitian = declarations["D0.Algebra.finiteHermitianPairing_adjoint"]
        weighted = declarations["D0.Algebra.finiteWeightedPairing_adjoint"]
        standard_axioms = {"Classical.choice", "Quot.sound", "propext"}

        self.assertEqual(basis["module"], "D0.Algebra.FiniteCoordinateBasis")
        self.assertEqual(basis["conclusion_whnf"], "x = ∑ i, x i • Pi.single i 1")
        self.assertEqual(set(basis["axioms"]), standard_axioms)
        self.assertFalse(any(binder["is_proposition"] for binder in basis["binders"]))
        self.assertEqual(linear_map_action["module"], "D0.Algebra.FiniteCoordinateBasis")
        self.assertEqual(
            linear_map_action["conclusion_whnf"],
            "A x j = ∑ i, x i * A (Pi.single i 1) j",
        )
        self.assertIn(
            "D0.Algebra.finiteCoordinate_eq_sum_single",
            linear_map_action["proof_dependencies"],
        )
        self.assertEqual(set(linear_map_action["axioms"]), standard_axioms)
        for consumer in (hermitian, weighted):
            self.assertEqual(consumer["declaration_kind"], "theorem")
            self.assertIn(
                "D0.Algebra.finiteLinearMap_apply_eq_sum_single",
                consumer["proof_dependencies"],
            )
            self.assertEqual(set(consumer["axioms"]), standard_axioms)
        self.assertFalse(any(binder["is_proposition"] for binder in hermitian["binders"]))
        self.assertEqual(
            {binder["name"] for binder in weighted["binders"]
             if binder["is_proposition"]},
            {"hw"},
        )

        dataset = proof.load_dataset(proof.ROOT)
        support = {row["lean_module"]: row for row in dataset["formal_support"]}
        self.assertIn("D0.Algebra.FiniteCoordinateBasis", support)
        consumers = support["D0.Algebra.FiniteCoordinateBasis"]["referenced_by"]
        self.assertIn("FiniteHermitianAdjoint.lean", consumers)
        self.assertIn("FiniteWeightedAdjoint.lean", consumers)

    def test_spectrum_and_matter_wrappers_consume_shared_finite_matrix_tensor_api(self) -> None:
        inventory_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "car_hodge_diagonal_transpose_current_declaration_inventory_2026-10-26_julia_base_link_frechet_v2.json"
        )
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        assert_historical_compiled_inventory(self, inventory)
        self.assertEqual(inventory["public_import_root"], "D0.All")
        declarations = {row["name"]: row for row in inventory["declarations"]}

        tensor = declarations["D0.Algebra.finiteMatrixTensorProduct"]
        self.assertEqual(tensor["declaration_kind"], "definition")
        self.assertIn("[Mul R]", tensor["elaborated_type"])
        self.assertNotIn("[Fintype", tensor["elaborated_type"])
        # The shared alias inherits Mathlib's standard quotient soundness
        # dependency from Matrix.kronecker; pin that exact trust footprint.
        self.assertEqual(tensor["axioms"], ["Quot.sound"])

        trace_law = declarations[
            "D0.Algebra.finiteMatrixTensorProduct_trace_one_left"
        ]
        self.assertEqual(trace_law["declaration_kind"], "theorem")
        self.assertIn("(D0.Algebra.finiteMatrixTensorProduct 1 B).trace",
                      trace_law["elaborated_type"])
        self.assertIn("Fintype.card X • B.trace", trace_law["elaborated_type"])
        self.assertEqual(
            set(trace_law["axioms"]),
            {"Classical.choice", "Quot.sound", "propext"},
        )
        self.assertIn("D0.Algebra.finiteMatrixTensorProduct",
                      trace_law["proof_dependencies"])

        for name in (
            "D0.Spectrum.tensor_product_I",
            "D0.Spectrum.kronecker_C_I",
        ):
            wrapper = declarations[name]
            self.assertEqual(wrapper["declaration_kind"], "definition")
            self.assertNotIn("[Fintype N]", wrapper["elaborated_type"])
            self.assertIn("D0.Algebra.finiteMatrixTensorProduct",
                          wrapper["proof_dependencies"])

        transpose_api = declarations[
            "D0.Algebra.finiteMatrixTensorProduct_transpose"
        ]
        self.assertNotIn("Fintype", transpose_api["elaborated_type"])

        matter_wrapper = declarations["D0.Matter.kronecker_I_C"]
        self.assertEqual(matter_wrapper["declaration_kind"], "definition")
        self.assertNotIn("[Fintype N]", matter_wrapper["elaborated_type"])
        self.assertIn("D0.Spectrum.tensor_product_I",
                      matter_wrapper["proof_dependencies"])

        spectrum_trace = declarations["D0.Spectrum.stage3_trace_relation"]
        self.assertIn("D0.Algebra.finiteMatrixPartialTraceLeft_trace",
                      spectrum_trace["proof_dependencies"])
        self.assertIn("D0.Algebra.finiteMatrixPartialTraceLeft_tensorProduct",
                      spectrum_trace["proof_dependencies"])
        partial_trace = declarations[
            "D0.Matter.partial_trace_commutes_with_shift"
        ]
        self.assertIn("D0.Matter.kronecker_I_C",
                      partial_trace["proof_dependencies"])

        support = {
            row["lean_module"]: row
            for row in proof.load_dataset(proof.ROOT)["formal_support"]
        }
        consumers = support["D0.Algebra.FiniteMatrixTensorProduct"]["referenced_by"]
        self.assertIn("D0/Spectrum/GenerationTensorExactness.lean", consumers)
        self.assertIn("D0/Matter/ArchivePartialTrace.lean", consumers)
        self.assertIn("D0/Gauge/FlatTensorNoGo.lean", consumers)

    def test_partial_trace_consumes_generic_finite_matrix_api(self) -> None:
        inventory_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "finite_matrix_partial_trace_current_declarations_2026-10-26_julia_base_link_frechet_v2.json"
        )
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        self.assertFalse(inventory["worktree_dirty"])
        assert_historical_compiled_inventory(self, inventory)
        self.assertEqual(inventory["public_import_root"], "D0.All")
        declarations = {row["name"]: row for row in inventory["declarations"]}

        generic_trace = declarations[
            "D0.Algebra.finiteMatrixPartialTraceLeft_trace"
        ]
        self.assertIn("D0.Algebra.finiteMatrixPartialTraceLeft",
                      generic_trace["proof_dependencies"])
        generic_tensor = declarations[
            "D0.Algebra.finiteMatrixPartialTraceLeft_tensorProduct"
        ]
        self.assertIn("CommSemiring R", generic_tensor["elaborated_type"])
        self.assertIn("D0.Algebra.finiteMatrixTensorProduct",
                      generic_tensor["proof_dependencies"])
        generic_intertwiner = declarations[
            "D0.Algebra.finiteMatrixPartialTraceLeft_commutes_rightTensor"
        ]
        self.assertIn("CommSemiring R", generic_intertwiner["elaborated_type"])
        self.assertIn("DecidableEq V", generic_intertwiner["elaborated_type"])
        self.assertIn("Fintype N", generic_intertwiner["elaborated_type"])
        self.assertNotIn("DecidableEq N", generic_intertwiner["elaborated_type"])
        self.assertIn("D0.Algebra.finiteMatrixTensorProduct",
                      generic_intertwiner["proof_dependencies"])
        self.assertFalse(any(
            "sorryAx" in axiom
            for name in (
                "D0.Algebra.finiteMatrixPartialTraceLeft_trace",
                "D0.Algebra.finiteMatrixPartialTraceLeft_tensorProduct",
                "D0.Algebra.finiteMatrixPartialTraceLeft_commutes_rightTensor",
            )
            for axiom in declarations[name]["axioms"]
        ))

        consumer_trace = declarations["D0.Matter.trace_partialTrace"]
        self.assertIn("D0.Algebra.finiteMatrixPartialTraceLeft_trace",
                      consumer_trace["proof_dependencies"])
        consumer_intertwiner = declarations[
            "D0.Matter.partial_trace_commutes_with_shift"
        ]
        self.assertIn("Fintype N", consumer_intertwiner["elaborated_type"])
        self.assertNotIn("DecidableEq N", consumer_intertwiner["elaborated_type"])
        self.assertIn(
            "D0.Algebra.finiteMatrixPartialTraceLeft_commutes_rightTensor",
            consumer_intertwiner["proof_dependencies"],
        )
        generation_lift = declarations[
            "D0.Matter.partial_trace_generation_lift"
        ]
        self.assertIn("Fintype.card G", generation_lift["elaborated_type"])
        self.assertIn(
            "D0.Algebra.finiteMatrixPartialTraceLeft_tensorProduct",
            generation_lift["proof_dependencies"],
        )
        generation_neutrality = declarations[
            "D0.Matter.generation_trace_neutrality_connection"
        ]
        self.assertIn(
            "D0.Matter.partial_trace_generation_lift",
            generation_neutrality["proof_dependencies"],
        )
        for name in (
            "D0.Matter.partial_trace_generation_lift",
            "D0.Matter.generation_trace_neutrality_connection",
        ):
            self.assertNotIn("sorryAx", declarations[name]["axioms"])

        support = {
            row["lean_module"]: row
            for row in proof.load_dataset(proof.ROOT)["formal_support"]
        }
        consumers = support["D0.Algebra.FiniteMatrixPartialTrace"]["referenced_by"]
        self.assertIn("03_FORMALIZATION/D0/Matter/ArchivePartialTrace.lean",
                      consumers)
        self.assertIn("03_FORMALIZATION/D0/Spectrum/GenerationTensorExactness.lean",
                      consumers)

    def test_archive_shift_adapters_consume_generic_topology_theorems(self) -> None:
        inventory_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "archive_shift_topology_current_declarations_2026-10-26_julia_base_link_frechet_v2.json"
        )
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        self.assertFalse(inventory["worktree_dirty"])
        self.assertRegex(inventory["snapshot_commit"], r"^[0-9a-f]{40}$")
        assert_historical_compiled_inventory(self, inventory)
        self.assertEqual(inventory["public_import_root"], "D0.All")
        self.assertEqual(inventory["toolchain"], "leanprover/lean4:v4.30.0")
        declarations = {row["name"]: row for row in inventory["declarations"]}
        self.assertEqual(
            set(inventory["request"]["full_names"]), set(declarations)
        )
        previous_names = json.loads(
            (
                proof.ROOT
                / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
                / "archive_shift_topology_current_declarations_2026-10-26_lorentz_tangent_joint_coframe_frechet.json"
            ).read_text(encoding="utf-8")
        )["request"]["full_names"]
        self.assertTrue(set(previous_names).issubset(declarations))

        generic_diagonal = declarations[
            "D0.Topology.abstract_shift_commute_implies_diagonal_constant"
        ]
        self.assertEqual(generic_diagonal["declaration_kind"], "theorem")
        self.assertIn(
            "D0.Topology.commute_with_shift_iterate",
            generic_diagonal["proof_dependencies"],
        )
        self.assertIn("∀ (i j : N)", generic_diagonal["elaborated_type"])
        generic_entries = declarations["D0.Topology.commute_with_shift_entries"]
        self.assertIn("M i j = M (f i) (f j)", generic_entries["elaborated_type"])
        self.assertIn(
            "D0.Topology.shift_matrix_mul_right",
            generic_entries["proof_dependencies"],
        )
        self.assertIn(
            "D0.Topology.commute_with_shift_entries",
            declarations["D0.Topology.commute_with_shift_step"]["proof_dependencies"],
        )

        shift_matrix = declarations["D0.Geometry.archiveShiftMatrix"]
        self.assertIn("NeZero n", shift_matrix["elaborated_type"])
        self.assertIn("D0.Topology.shiftMatrix", shift_matrix["proof_dependencies"])
        right = declarations["D0.Geometry.shift_matrix_mul_right"]
        left = declarations["D0.Geometry.shift_matrix_mul_left"]
        self.assertIn("M i (j - 1)", right["elaborated_type"])
        self.assertIn("M (i + 1) j", left["elaborated_type"])
        self.assertIn("D0.Topology.shift_matrix_mul_right", right["proof_dependencies"])
        self.assertIn("D0.Topology.shift_matrix_mul_left", left["proof_dependencies"])

        commute_k = declarations["D0.Geometry.commute_with_shift_k"]
        self.assertIn("M (i + ↑k) (i + ↑k)", commute_k["elaborated_type"])
        self.assertIn(
            "D0.Topology.commute_with_shift_iterate",
            commute_k["proof_dependencies"],
        )
        diagonal = declarations[
            "D0.Geometry.commute_with_shift_implies_diagonal_constant"
        ]
        self.assertIn("M i i = M j j", diagonal["elaborated_type"])
        self.assertIn(
            "D0.Topology.abstract_shift_commute_implies_diagonal_constant",
            diagonal["proof_dependencies"],
        )
        matter_step = declarations["D0.Matter.diag_eq_of_comm_shift"]
        self.assertIn(
            "D0.Topology.commute_with_shift_step",
            matter_step["proof_dependencies"],
        )
        matter_iterate = declarations["D0.Matter.diag_eq_of_comm_shift_k"]
        self.assertIn(
            "D0.Topology.commute_with_shift_iterate",
            matter_iterate["proof_dependencies"],
        )
        matter_uniform = declarations[
            "D0.Matter.partial_trace_density_uniform_under_shift"
        ]
        self.assertIn(
            "D0.Topology.abstract_shift_commute_implies_diagonal_constant",
            matter_uniform["proof_dependencies"],
        )
        spectrum_adapter = declarations[
            "D0.Spectrum.cyclicShiftMatrix_eq_topology_shift"
        ]
        self.assertIn(
            "D0.Topology.shiftMatrix",
            spectrum_adapter["proof_dependencies"],
        )
        self.assertIn(
            "D0.Spectrum.shift_g_one_eq_finRotate",
            declarations["D0.Spectrum.shift_g_eq_finRotate_iterate"]["proof_dependencies"],
        )
        self.assertIn(
            "D0.Spectrum.shift_g_eq_finRotate_iterate",
            declarations["D0.Matter.diag_eq_of_comm_shift_k"]["proof_dependencies"],
        )
        flavor_step = declarations["D0.Spectrum.flavor_blindness_step_of_commute"]
        self.assertNotIn("h_off", flavor_step["elaborated_type"])
        self.assertIn(
            "D0.Topology.commute_with_shift_entries",
            flavor_step["proof_dependencies"],
        )
        self.assertIn(
            "D0.Spectrum.flavor_blindness_step_of_commute",
            declarations["D0.Spectrum.flavor_blindness_step"]["proof_dependencies"],
        )
        self.assertIn(
            "D0.Spectrum.flavor_blindness_step_k_of_commute",
            declarations["D0.Spectrum.flavor_blindness_step_k"]["proof_dependencies"],
        )
        flavor_step_k = declarations[
            "D0.Spectrum.flavor_blindness_step_k_of_commute"
        ]
        self.assertNotIn("g1 ≠ g2", flavor_step_k["elaborated_type"])
        self.assertIn(
            "D0.Spectrum.flavor_blindness_step_of_commute",
            flavor_step_k["proof_dependencies"],
        )
        stage2 = declarations["D0.Spectrum.stage2_flavor_blindness_of_commute"]
        self.assertNotIn("g1 ≠ g2", stage2["elaborated_type"])
        self.assertIn(
            "D0.Spectrum.flavor_blindness_step_k_of_commute",
            stage2["proof_dependencies"],
        )
        self.assertIn(
            "D0.Spectrum.stage2_flavor_blindness_of_commute",
            declarations["D0.Spectrum.stage2_flavor_blindness"]["proof_dependencies"],
        )
        self.assertIn(
            "g1 ≠ g2",
            declarations["D0.Spectrum.stage2_flavor_blindness"]["elaborated_type"],
        )
        stage3 = declarations["D0.Spectrum.stage3_tensor_exactness"]
        self.assertIn("g1 ≠ g2", stage3["elaborated_type"])
        self.assertIn(
            "D0.Spectrum.stage2_flavor_blindness_of_commute",
            stage3["proof_dependencies"],
        )
        self.assertNotIn(
            "D0.Spectrum.stage2_flavor_blindness",
            stage3["proof_dependencies"],
        )
        self.assertTrue(all(
            "sorryAx" not in axiom
            for name in (
                "D0.Topology.abstract_shift_commute_implies_diagonal_constant",
                "D0.Geometry.archiveShiftMatrix",
                "D0.Geometry.shift_matrix_mul_right",
                "D0.Geometry.shift_matrix_mul_left",
                "D0.Geometry.commute_with_shift_k",
                "D0.Geometry.commute_with_shift_implies_diagonal_constant",
                "D0.Matter.diag_eq_of_comm_shift",
                "D0.Matter.diag_eq_of_comm_shift_k",
                "D0.Matter.partial_trace_density_uniform_under_shift",
                "D0.Topology.commute_with_shift_entries",
                "D0.Spectrum.cyclicShiftMatrix_eq_topology_shift",
                "D0.Spectrum.shift_g_one_eq_finRotate",
                "D0.Spectrum.shift_g_eq_finRotate_iterate",
                "D0.Spectrum.flavor_blindness_step_of_commute",
                "D0.Spectrum.flavor_blindness_step",
                "D0.Spectrum.flavor_blindness_step_k",
                "D0.Spectrum.flavor_blindness_step_k_of_commute",
                "D0.Spectrum.stage2_flavor_blindness_of_commute",
                "D0.Spectrum.stage2_flavor_blindness",
                "D0.Spectrum.stage3_tensor_exactness",
            )
            for axiom in declarations[name]["axioms"]
        ))

        support = {
            row["lean_module"]: row
            for row in proof.load_dataset(proof.ROOT)["formal_support"]
        }
        self.assertIn("D0/Geometry/ArchivePhaseShift.lean",
                      support["D0.Topology.ArchiveShiftTopology"]["referenced_by"])
        self.assertIn("D0/Matter/ArchivePartialTrace.lean",
                      support["D0.Topology.ArchiveShiftTopology"]["referenced_by"])
        self.assertIn("D0/Spectrum/GenerationTensorExactness.lean",
                      support["D0.Topology.ArchiveShiftTopology"]["referenced_by"])

    def test_archive_shift_reuse_is_discoverable_from_a_cold_start_query(self) -> None:
        case = next(
            item for item in cold_start.CASES
            if item["id"] == "archive-phase-shift-reuses-transitive-permutation-theorem"
        )
        queries = case["queries"]
        self.assertIn("stage2_flavor_blindness_of_commute", queries[4])
        self.assertIn(
            "03_FORMALIZATION/D0/Topology/ArchiveShiftTopology.lean",
            case["required_refs"],
        )
        hits_by_query = proof.full_text_search_many(proof.ROOT, queries, limit=18)
        sources = {hit["source"] for hits in hits_by_query for hit in hits}
        for path in (
            "03_FORMALIZATION/D0/Topology/ArchiveShiftTopology.lean",
            "03_FORMALIZATION/D0/Geometry/ArchivePhaseShift.lean",
            "03_FORMALIZATION/D0/Matter/ArchivePartialTrace.lean",
            "03_FORMALIZATION/D0/Spectrum/GenerationTensorExactness.lean",
        ):
            self.assertIn(path, sources)
        exact_generation_hits = proof.full_text_search(
            proof.ROOT, queries[4], limit=18
        )
        self.assertIn(
            "03_FORMALIZATION/D0/Spectrum/GenerationTensorExactness.lean",
            [hit["source"] for hit in exact_generation_hits],
        )

    def test_fixed_sine_weak_readout_c0_pilot_is_discoverable(self) -> None:
        case = next(
            item for item in cold_start.CASES
            if item["id"] == "fixed-sine-weak-readout-c0-pilot"
        )
        query_hits = proof.full_text_search_many(
            proof.ROOT, case["queries"], limit=cold_start.COLD_START_MIN_RESULT_WINDOW
        )
        self.assertEqual(len(query_hits), len(case["queries"]))
        query_pairs = list(zip(case["queries"], query_hits))
        for path in case["required_refs"]:
            status = cold_start._required_source_status(query_pairs, {"path": path})
            self.assertTrue(status["found"], f"cold-start search missed {path}: {status}")
        for source in case["required_sources"]:
            status = cold_start._required_source_status(query_pairs, source)
            self.assertTrue(
                status["found"], f"cold-start missed scoped source {source}: {status}"
            )
        self.assertIn("scoped weak-convergence obstruction", case["scope_review"])
        self.assertIn("does not rule out other readouts", case["scope_review"])

    def test_cyclic_af_return_source_is_retrievable_at_its_pinned_owner_head(self) -> None:
        case = next(
            item for item in cold_start.CASES
            if item["id"] == "cyclic-af-return-without-extra-blank-flag"
        )
        hits = proof.full_text_search_many(
            proof.ROOT, case["queries"], limit=cold_start.COLD_START_MIN_RESULT_WINDOW
        )
        self.assertEqual(len(hits), len(case["queries"]))
        query_pairs = list(zip(case["queries"], hits))
        for ref in case["required_refs"]:
            status = cold_start._required_source_status(query_pairs, {"path": ref})
            self.assertTrue(status["found"], f"cold-start search missed {ref}: {status}")
        owner_source = next(
            source for source in case["required_sources"]
            if source["path"].endswith("A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md")
        )
        status = cold_start._required_source_status(query_pairs, owner_source)
        self.assertTrue(status["found"], f"cold-start missed #334 source content: {status}")
        owner_path = owner_source["path"]
        pins = [
            reference
            for _, query_results in query_pairs
            for hit in query_results
            for reference in hit.get("source_refs", [])
            if reference.get("path", "").endswith(owner_path)
            and reference.get("commit") == "d53ef61c8c578c5a6cf16b88d17f8576ced0f64d"
            and reference.get("blob") == "069f16ed168c43e483dc5b6bc5eaabbac6e848fa"
            and reference.get("pin_status") == "pinned_snapshot"
        ]
        self.assertTrue(pins, "the surfaced owner source must retain its exact #334 commit/blob pin")
        self.assertIn("Physical AF port admission", case["scope_review"])
        self.assertIn("GR_closed=false", case["scope_review"])

    def test_source_port_preparation_consumes_shared_tensor_api(self) -> None:
        inventory_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "source_port_preparation_tensor_inventory_2026-10-26_julia_base_link_frechet_v2.json"
        )
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        self.assertRegex(inventory["snapshot_commit"], r"^[0-9a-f]{40}$")
        self.assertFalse(inventory["worktree_dirty"])
        assert_historical_compiled_inventory(self, inventory)
        self.assertEqual(inventory["public_import_root"], "D0.All")
        declarations = {row["name"]: row for row in inventory["declarations"]}

        for name in (
            "D0.Representation.SourcePortPreparation.coupled",
            "D0.Representation.SourcePortPreparation.jointMetric",
            "D0.Representation.SourcePortPreparation.interactionGenerator",
        ):
            self.assertIn(
                "D0.Algebra.finiteMatrixTensorProduct",
                declarations[name]["proof_dependencies"],
            )

        quarter_turn = declarations[
            "D0.Representation.SourcePortPreparation.coupled_fourth"
        ]
        self.assertIn("coupled ^ 4 = 1", quarter_turn["elaborated_type"])
        self.assertIn(
            "D0.Algebra.finiteMatrixTensorProduct_mul",
            quarter_turn["proof_dependencies"],
        )
        self.assertIn(
            "D0.Algebra.finiteMatrixTensorProduct_one",
            quarter_turn["proof_dependencies"],
        )

        product_control = declarations[
            "D0.Representation.SourcePortPreparation.independent_actions_zero_minor"
        ]
        self.assertIn(
            "interactionMinor (D0.Algebra.finiteMatrixTensorProduct A B) = 0",
            product_control["elaborated_type"],
        )
        nonfactorization = declarations[
            "D0.Representation.SourcePortPreparation.coupled_not_independent"
        ]
        self.assertIn(
            "D0.Algebra.finiteMatrixTensorProduct A B",
            nonfactorization["elaborated_type"],
        )
        self.assertIn(
            "D0.Representation.SourcePortPreparation.independent_actions_zero_minor",
            nonfactorization["proof_dependencies"],
        )
        self.assertIn(
            "D0.Representation.SourcePortPreparation.coupled_interaction_witness",
            nonfactorization["proof_dependencies"],
        )
        self.assertFalse(any(
            "sorryAx" in axiom
            for declaration in inventory["declarations"]
            for axiom in declaration.get("axioms", [])
        ))

        support = {
            row["lean_module"]: row
            for row in proof.load_dataset(proof.ROOT)["formal_support"]
        }
        consumers = support["D0.Algebra.FiniteMatrixTensorProduct"]["referenced_by"]
        self.assertIn("D0/Representation/SourcePortPreparation.lean", consumers)

        hits = proof.full_text_search(
            proof.ROOT, "SourcePortPreparation finiteMatrixTensorProduct", limit=10
        )
        self.assertTrue(any(
            hit["source"] == "03_FORMALIZATION/D0/Representation/SourcePortPreparation.lean"
            and hit["direct_content"]
            for hit in hits
        ))

    def test_flat_tensor_compatibility_wrapper_uses_shared_operator_and_transpose_law(self) -> None:
        inventory_path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "flat_tensor_shared_api_declarations_2026-10-26_julia_base_link_frechet_v2.json"
        )
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        assert_historical_compiled_inventory(self, inventory)
        self.assertEqual(inventory["public_import_root"], "D0.All")
        declarations = {row["name"]: row for row in inventory["declarations"]}

        flat_tensor = declarations["D0.Gauge.flatTensor"]
        self.assertEqual(flat_tensor["declaration_kind"], "definition")
        self.assertIn(
            "D0.Algebra.finiteMatrixTensorProduct",
            flat_tensor["proof_dependencies"],
        )
        self.assertNotIn("Fintype", flat_tensor["elaborated_type"])

        symmetry = declarations[
            "D0.Gauge.flat_tensor_of_two_skew_is_symmetric"
        ]
        self.assertEqual(symmetry["declaration_kind"], "theorem")
        self.assertNotIn("Fintype", symmetry["elaborated_type"])
        self.assertIn(
            "D0.Algebra.finiteMatrixTensorProduct_transpose",
            symmetry["proof_dependencies"],
        )
        self.assertEqual(
            set(symmetry["axioms"]),
            {"Classical.choice", "Quot.sound", "propext"},
        )

        boundary_proof = declarations[
            "D0.Gauge.naive_flat_tensor_nonabelian_boundary_proof"
        ]
        self.assertIn(
            "D0.Gauge.flat_tensor_of_two_skew_is_symmetric",
            boundary_proof["proof_dependencies"],
        )

        hits = proof.full_text_search(
            proof.ROOT, "flatTensor finiteMatrixTensorProduct", limit=5
        )
        self.assertEqual(
            hits[0]["source"],
            "03_FORMALIZATION/D0/Gauge/FlatTensorNoGo.lean",
        )
        self.assertTrue(hits[0]["direct_content"])
        self.assertEqual(hits[0]["matched_terms"], hits[0]["query_terms"])

    def test_claim_source_candidates_use_exact_headings_and_preserve_ambiguity(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            books = root / "01_BOOKS"
            books.mkdir()
            (books / "BOOK_01_TEST.md").write_bytes(
                b"### 01.8.1 Primitive positive response source\n"
                b"The cited result has a unique positive root.\n"
                b"## 01.20 First section\n## 01.24 Second section\n"
                b"## 01.99 Unlisted retained lemma\n"
            )
            (books / "BOOK_02_TEST.md").write_bytes(b"## 02.34 Master section\n")
            (books / "BOOK_03_TEST.md").write_bytes(
                b"## 03.1 First copy\n## 03.1 Second copy\n"
            )
            (books / "BOOK_04_TEST.md").write_bytes(
                b"# Intro\nThe body mentions 04.7 but does not define it.\n"
                b"Claim BODY-ONLY is referenced here.\n"
                b"PREFIX-BODY-ONLY-SUFFIX is a distinct token.\n"
                b"```markdown\n```python\nFENCE-ONLY appears only in code.\n"
                b"## 04.7 Example in a code fence\n```\n"
                b"### 04.7.1 Child only\n"
            )
            (books / "BOOK_05_TEST.md").write_bytes(
                b"## 05.32 Other topic\nNo Bianchi result is recorded here.\n"
            )
            (books / "BOOK_06_TEST.md").write_bytes(
                b"## 06.32.1 Boundary status for Hurwitz, Bianchi and gauge transformations\n"
                b"The exact Bianchi statement is closed on the graded incidence complex.\n"
            )
            data = dataset(root)
            data["snapshot_commit"] = "source-snapshot"
            data["worktree_dirty"] = False
            data["claims"] = [
                {"claim_id": "PAIR", "book": "BOOK_01/02",
                 "section": "01.8.1 / 02.34"},
                {"claim_id": "ONE-TO-MANY", "book": "BOOK_01",
                 "section": "01.20/01.24"},
                {"claim_id": "AMBIGUOUS", "book": "BOOK_03", "section": "03.1"},
                {"claim_id": "BODY-ONLY", "book": "BOOK_04", "section": "04.7"},
                {"claim_id": "FENCE-ONLY", "book": "BOOK_04", "section": "04.99"},
                {"claim_id": "NON-BOOK", "book": "METROLOGY", "section": "scope"},
                {"claim_id": "MISMATCH", "book": "BOOK_01/02", "section": "01.8.1"},
                {"claim_id": "SHARED-DESCRIPTION", "book": "BOOK_01/02",
                 "section": "primitive positive response"},
                {"claim_id": "SHARED-BIANCHI", "book": "BOOK_05/06",
                 "section": "graded incidence Bianchi closure"},
            ]

            view = proof.claim_source_candidate_view(data)
            by_id = {row["claim_id"]: row for row in view["rows"]}
            heading_candidates = view["book_heading_source_candidates"]
            by_heading = {
                (row["book_locator"], row["heading"]): row
                for row in heading_candidates
            }

        self.assertEqual(view["schema"], "d0-claim-source-candidate-view-v3")
        self.assertEqual(view["counts"]["book_heading_count"], len(heading_candidates))
        self.assertEqual(
            view["counts"]["book_headings_without_claim_heading_candidate"],
            sum(not row["exact_heading_candidate_claim_ids"]
                and not row["ranked_heading_candidate_claim_ids"]
                for row in heading_candidates),
        )
        unlisted = by_heading[("BOOK_01", "01.99 Unlisted retained lemma")]
        self.assertIsNone(unlisted["candidate_source_unit_key"])
        self.assertEqual(unlisted["exact_heading_candidate_claim_ids"], [])
        self.assertEqual(unlisted["ranked_heading_candidate_claim_ids"], [])
        exact_heading = by_heading[("BOOK_01", "01.8.1 Primitive positive response source")]
        self.assertIn("PAIR", exact_heading["exact_heading_candidate_claim_ids"])
        self.assertIn("SHARED-DESCRIPTION", exact_heading["ranked_heading_candidate_claim_ids"])
        self.assertIn("Neither kind identifies accepted mathematical units",
                      view["interpretation"])
        self.assertEqual(by_id["PAIR"]["resolution_status"], "unique")
        self.assertEqual([x["book_locator"] for x in by_id["PAIR"]["locator_pairs"]],
                         ["BOOK_01", "BOOK_02"])
        self.assertIsNone(
            by_id["PAIR"]["locator_pairs"][0]["candidates"][0][
                "candidate_source_unit_key"
            ]
        )
        self.assertEqual(by_id["ONE-TO-MANY"]["resolution_status"], "unique")
        self.assertEqual(len(by_id["ONE-TO-MANY"]["locator_pairs"]), 2)
        self.assertEqual(by_id["AMBIGUOUS"]["resolution_status"], "ambiguous")
        self.assertEqual(len(by_id["AMBIGUOUS"]["locator_pairs"][0]["candidates"]), 2)
        self.assertEqual(by_id["BODY-ONLY"]["resolution_status"], "unresolved")
        self.assertEqual(by_id["BODY-ONLY"]["locator_pairs"][0]["candidates"], [])
        body_mentions = by_id["BODY-ONLY"]["literal_claim_id_mentions"]
        self.assertEqual(len(body_mentions), 1)
        self.assertEqual(body_mentions[0]["line"], 3)
        self.assertEqual(body_mentions[0]["nearest_heading"], "Intro")
        self.assertEqual(body_mentions[0]["nearest_heading_line"], 1)
        self.assertIsNone(body_mentions[0]["candidate_coordinate_key"])
        self.assertEqual(
            body_mentions[0]["review_status"],
            "unreviewed_literal_claim_id_mention_candidate",
        )
        self.assertEqual(by_id["FENCE-ONLY"]["literal_claim_id_mentions"], [])
        self.assertNotIn(
            "ranked_heading_candidates",
            by_id["BODY-ONLY"]["locator_pairs"][0],
        )
        self.assertEqual(by_id["NON-BOOK"]["resolution_status"], "non_book_locator")
        self.assertEqual(by_id["MISMATCH"]["resolution_status"], "unresolved")
        self.assertEqual(
            by_id["MISMATCH"]["resolution_reason"],
            "multiple_books_share_one_unpaired_section_locator",
        )
        self.assertEqual(by_id["MISMATCH"]["locator_pairs"], [])
        self.assertEqual(
            by_id["MISMATCH"]["book_heading_candidates"][0]["candidates"][0]["match_kind"],
            "exact_heading",
        )
        self.assertEqual(by_id["SHARED-DESCRIPTION"]["resolution_status"], "unresolved")
        self.assertEqual(
            by_id["SHARED-DESCRIPTION"]["book_heading_candidates"][0]["candidates"][0][
                "match_kind"
            ],
            "lexical_heading_candidate",
        )
        self.assertEqual(
            by_id["SHARED-DESCRIPTION"]["book_heading_candidates"][0]["candidates"][0][
                "review_status"
            ],
            "unreviewed_lexical_candidate",
        )
        self.assertEqual(by_id["SHARED-BIANCHI"]["resolution_status"], "unresolved")
        self.assertEqual(
            by_id["SHARED-BIANCHI"]["resolution_reason"],
            "multiple_books_share_one_unpaired_section_locator",
        )
        bianchi = by_id["SHARED-BIANCHI"]["book_heading_candidates"][1]["candidates"]
        self.assertEqual(len(bianchi), 1)
        self.assertEqual(bianchi[0]["path"], "01_BOOKS/BOOK_06_TEST.md")
        self.assertEqual(bianchi[0]["match_kind"], "lexical_heading_candidate")
        self.assertEqual(bianchi[0]["review_status"], "unreviewed_lexical_candidate")
        self.assertEqual(set(bianchi[0]["matched_terms"]),
                         {"graded", "incidence", "bianchi"})
        self.assertEqual(view["counts"]["fully_unique_claim_rows"], 2)
        self.assertEqual(view["counts"]["ambiguous_claim_rows"], 1)
        self.assertEqual(view["counts"]["non_book_claim_rows"], 1)
        self.assertEqual(view["counts"]["malformed_claim_rows"], 0)
        self.assertEqual(view["counts"]["unresolved_claim_rows"], 5)
        self.assertEqual(view["counts"]["unpaired_multi_book_claim_rows"], 3)
        self.assertEqual(view["counts"]["claim_rows_with_ranked_heading_candidates"], 2)
        self.assertEqual(view["counts"]["ranked_heading_candidate_count"], 2)
        self.assertEqual(view["counts"]["literal_claim_id_mention_count"], 1)
        self.assertEqual(view["counts"]["claim_rows_with_literal_claim_id_mentions"], 1)
        self.assertEqual(
            view["counts"]["book_source_files_with_literal_claim_id_mentions"], 1
        )
        self.assertIn("None of these fields accepts a claim statement", view["interpretation"])

    def test_alias_source_candidates_separate_locator_integrity_from_semantic_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            books = root / "01_BOOKS"
            books.mkdir()
            (books / "BOOK_01_TEST.md").write_text(
                "## Alias source candidates\n"
                "`OLD-EXACT` names the historical assertion.\n"
                "An equation is recorded here without the legacy label.\n"
                "Later label: `OLD-DELAYED`.\n"
                "The longer token OLD-SUBSTRING-EXTENDED is not an exact label.\n",
                encoding="utf-8",
            )
            data = dataset(root)
            data["aliases"] = [
                {"legacy_id": "OLD-EXACT", "kind": "LEGACY_BOOK_LABEL",
                 "canonical_claim_id": "", "first_reference": "BOOK_01_TEST.md:2",
                 "note": "Historical label."},
                {"legacy_id": "OLD-DELAYED", "kind": "LEGACY_BOOK_LABEL",
                 "canonical_claim_id": "", "first_reference": "BOOK_01_TEST.md:3",
                 "note": "Equation anchor."},
                {"legacy_id": "OLD-MISSING", "kind": "LEGACY_BOOK_LABEL",
                 "canonical_claim_id": "", "first_reference": "BOOK_99_MISSING.md:1",
                 "note": "Missing source control."},
                {"legacy_id": "OLD-INVALID", "kind": "LEGACY_BOOK_LABEL",
                 "canonical_claim_id": "", "first_reference": "../BOOK_01_TEST.md:1",
                 "note": "Traversal control."},
                {"legacy_id": "OLD-SUBSTRING", "kind": "LEGACY_BOOK_LABEL",
                 "canonical_claim_id": "", "first_reference": "BOOK_01_TEST.md:1",
                 "note": "Longer-token control."},
                {"legacy_id": "OLD-CANONICAL", "kind": "CANONICAL_TARGET",
                 "canonical_claim_id": "CLM-1", "first_reference": "BOOK_01_TEST.md",
                 "note": "Explicit target."},
            ]

            view = proof.alias_source_candidate_view(data)

        by_id = {row["alias_id"]: row for row in view["rows"]}
        self.assertEqual(view["schema"], "d0-alias-source-candidate-view-v1")
        self.assertEqual(view["counts"]["legacy_book_label_count"], 5)
        self.assertEqual(view["counts"]["legacy_ids_with_existing_book_locator_count"], 3)
        self.assertEqual(view["counts"]["legacy_ids_with_label_in_designated_book_count"], 2)
        self.assertEqual(view["counts"]["legacy_locator_line_with_label_count"], 1)
        self.assertEqual(by_id["OLD-EXACT"]["resolution_status"],
                         "existing_line_anchor_with_label")
        self.assertEqual(by_id["OLD-DELAYED"]["resolution_status"],
                         "existing_line_anchor_without_label_text")
        self.assertEqual(by_id["OLD-DELAYED"]["first_alias_occurrence_line_in_designated_book"], 4)
        self.assertEqual(by_id["OLD-MISSING"]["resolution_status"], "book_source_missing")
        self.assertEqual(by_id["OLD-INVALID"]["resolution_status"],
                         "invalid_book_line_reference")
        self.assertEqual(by_id["OLD-SUBSTRING"]["resolution_status"],
                         "existing_line_anchor_without_label_text")
        self.assertEqual(by_id["OLD-SUBSTRING"]["alias_occurrence_count_in_designated_book"], 0)
        self.assertTrue(by_id["OLD-CANONICAL"]["target_claim_found"])
        self.assertIn("do not establish semantic equivalence", view["interpretation"])

    def test_current_claim_source_view_lists_unlocated_book_headings_as_candidates(self) -> None:
        path = (
            proof.ROOT
            / "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24"
            / "claim_source_candidates_current.json"
        )
        view_bytes = path.read_bytes()
        view = json.loads(view_bytes)
        self.assertEqual(view["schema"], "d0-claim-source-candidate-view-v3")
        self.assertRegex(view["snapshot_commit"], r"^[0-9a-f]{40}$")
        self.assertEqual(view["claim_registry_sha256"], hashlib.sha256(
            (proof.ROOT / "02_REGISTRY/claims.csv").read_bytes()
        ).hexdigest())
        for source_path, pin in view["book_sources"].items():
            self.assertEqual(pin["source_sha256"], hashlib.sha256(
                (proof.ROOT / source_path).read_bytes()
            ).hexdigest())

        headings = view["book_heading_source_candidates"]
        coordinates = {(row["path"], row["line"]) for row in headings}
        self.assertEqual(len(coordinates), len(headings))
        self.assertEqual(view["counts"]["book_heading_count"], len(headings))
        self.assertEqual(view["counts"]["book_heading_count"], 711)
        self.assertEqual(
            view["counts"]["book_headings_with_exact_heading_candidate"], 43
        )
        self.assertEqual(view["counts"]["book_headings_with_ranked_heading_candidate"], 219)
        self.assertEqual(
            view["counts"]["book_headings_with_both_exact_and_ranked_heading_candidates"],
            25,
        )
        self.assertEqual(
            view["counts"]["book_headings_without_claim_heading_candidate"], 474
        )
        mention_rows = [
            (claim_row["claim_id"], mention)
            for claim_row in view["rows"]
            for mention in claim_row["literal_claim_id_mentions"]
        ]
        self.assertEqual(
            view["counts"]["literal_claim_id_mention_count"], len(mention_rows)
        )
        self.assertEqual(
            view["counts"]["claim_rows_with_literal_claim_id_mentions"],
            len({claim_id for claim_id, _mention in mention_rows}),
        )
        self.assertEqual(view["counts"]["literal_claim_id_mention_count"], 840)
        self.assertEqual(
            view["counts"]["claim_rows_with_literal_claim_id_mentions"], 430
        )
        self.assertEqual(
            view["counts"]["book_source_files_with_literal_claim_id_mentions"], 9
        )
        for _claim_id, mention in mention_rows:
            pin = view["book_sources"][mention["path"]]
            self.assertEqual(mention["matches_snapshot_commit"],
                             pin["matches_snapshot_commit"])
            expected_key = (
                f"source:{view['snapshot_commit']}:{mention['path']}"
                f"#L{mention['line']}:O[{mention['start_offset_0based']}"
                f",{mention['end_offset_0based_exclusive']})"
                if pin["matches_snapshot_commit"] else None
            )
            self.assertEqual(mention["candidate_coordinate_key"], expected_key)
            self.assertEqual(
                mention["review_status"],
                "unreviewed_literal_claim_id_mention_candidate",
            )
        bridge = next(
            row for row in view["rows"]
            if row["claim_id"] == "D0-NONRECIPROCAL-ACTIVE-DYNAMICS-FORMALISM-BRIDGE-001"
        )
        self.assertEqual(bridge["resolution_status"], "unique")
        self.assertEqual(
            [(mention["path"], mention["line"], mention["nearest_heading_line"])
             for mention in bridge["literal_claim_id_mentions"]],
            [(
                "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md",
                289,
                277,
            )],
        )
        bridge_mention = bridge["literal_claim_id_mentions"][0]
        self.assertEqual(bridge_mention["claim_id_text"], bridge["claim_id"])
        self.assertEqual(
            bridge_mention["nearest_heading"],
            "03.3.2 The closed feedback action component",
        )
        self.assertIn(bridge["claim_id"], bridge_mention["literal_text_excerpt"])
        self.assertEqual(bridge_mention["match_kind"], "literal_claim_id_mention")
        self.assertTrue(bridge_mention["matches_snapshot_commit"])
        for row in headings:
            pin = view["book_sources"][row["path"]]
            self.assertEqual(row["matches_snapshot_commit"], pin["matches_snapshot_commit"])
            expected_key = (
                f"source:{view['snapshot_commit']}:{row['path']}#L{row['line']}: {row['heading']}"
                if pin["matches_snapshot_commit"] else None
            )
            self.assertEqual(row["candidate_source_unit_key"], expected_key)
        self.assertTrue(any(
            not row["exact_heading_candidate_claim_ids"]
            and not row["ranked_heading_candidate_claim_ids"]
            for row in headings
        ))
        self.assertIn("Neither kind identifies accepted mathematical units",
                      view["interpretation"])


    def test_chat_moving_cut_source_is_retrievable_without_physical_owner_inference(self) -> None:
        data = proof.load_dataset(proof.ROOT)
        hits = proof.full_text_search(proof.ROOT, "moving-cut")
        by_source = {item["source"]: item for item in hits}
        source_path = "02_REGISTRY/research/A4D_ROOT_BOOTSTRAP_MOVING_CUT_SOURCE_2026_10_28.md"
        integration_path = "02_REGISTRY/research/D0_CHAT_RESULTS_INTEGRATION_2026_10_28.md"
        self.assertIn(source_path, by_source)
        self.assertIn(integration_path, by_source)
        integration_text = (proof.ROOT / integration_path).read_text(encoding="utf-8")
        self.assertIn("1f4b85f14292dfac07f61db27ff47a961e525d03", integration_text)
        self.assertIn("fd35893d77e4aa5f819bafa0c6428c8e7a8f1812", integration_text)
        self.assertIn("97 controls", integration_text)
        self.assertIn("79 controls", integration_text)
        self.assertIn("171 controls", integration_text)
        self.assertIn("off-copy", integration_text)
        self.assertIn("same-task tangent", integration_text)
        self.assertIn("not a Lean formalization of complex-matrix effect tomography", integration_text)
        declaration_inventory_path = (
            proof.ROOT / "02_REGISTRY/research/sources/"
            "d0_proof_architecture_formalization_2026-10-24/reports/"
            "moving_projector_current_declarations_2026-10-28_pr402_f19.json"
        )
        self.assertEqual(
            hashlib.sha256(declaration_inventory_path.read_bytes()).hexdigest(),
            "b735a5b2ee94db17f31b22d974a50d4101765611d7aa80a865a86bde26bd96d9",
        )
        declaration_inventory = json.loads(declaration_inventory_path.read_text(encoding="utf-8"))
        self.assertEqual(
            declaration_inventory["snapshot_commit"],
            "f19c8762622932b970facc24340907a6fb004b86",
        )
        self.assertEqual(
            declaration_inventory["lean_source_digest"],
            "e66a40d0f1b4498f68ddc6d1b3445ffe676c8bcd1c68013baff32daf18d838aa",
        )
        self.assertFalse(declaration_inventory["worktree_dirty"])
        declarations = {row["name"]: row for row in declaration_inventory["declarations"]}
        self.assertEqual(set(declarations), {
            "D0.Analysis.MovingProjectorBookPrice.hasDerivAt_moving_projector_book03_price",
            "D0.Analysis.MovingProjectorBookPrice.hasDerivAt_variable_moving_projector_book03_price",
        })
        self.assertTrue(all(row["exists"] for row in declarations.values()))
        self.assertTrue(all(
            row["axioms"] == ["Classical.choice", "Quot.sound", "propext"]
            for row in declarations.values()
        ))

        links = proof._declared_source_links(data, source_path)
        self.assertEqual(links["owner_status"], "no_exact_assembly_owner_link")
        self.assertEqual(
            [row["lean_module"] for row in links["formal_support_locators"]],
            [
                "D0.Algebra.MovingProjectorCalculus",
                "D0.Algebra.MovingProjectorPositiveChart",
                "D0.Algebra.MovingProjectorTransport",
                "D0.Analysis.MovingProjectorBookPrice",
            ],
        )
        self.assertTrue(all(row["status"] == "metadata_locator_only"
                            for row in links["formal_support_locators"]))

        module_hits = proof.structured_search(data, "D0.Algebra.MovingProjectorTransport")
        self.assertEqual(module_hits[0]["kind"], "formal-support-metadata")
        self.assertEqual(module_hits[0]["key"], "D0.Algebra.MovingProjectorTransport")
        refinement_hits = proof.structured_search(
            data, "D0.Geometry.ArchiveGradedRefinementComposedReadout"
        )
        self.assertEqual(refinement_hits[0]["kind"], "formal-support-metadata")
        self.assertIn(
            "D0-ARCHIVE-GRADED-REFINEMENT-CHAIN-MAP-001",
            refinement_hits[0]["record"]["referenced_by"],
        )

    def test_latest_334_offcopy_replay_packet_matches_its_manifest(self) -> None:
        packet = (
            proof.ROOT / "02_REGISTRY/research/sources/"
            "d0_334_post_1f_offcopy_frame_delta_2026-10-28"
        )
        manifest = json.loads((packet / "MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(
            manifest["source_commit"],
            "fd35893d77e4aa5f819bafa0c6428c8e7a8f1812",
        )
        self.assertEqual(manifest["execution"]["checks"], 171)
        self.assertEqual(manifest["execution"]["status"], "PASS")
        self.assertTrue(manifest["local_matches_owner_receipt_byte_for_byte"])
        self.assertTrue(manifest["local_normal_optimized_byte_identical"])

        search_hits = proof.full_text_search(proof.ROOT, "off-copy AF frame", limit=20)
        self.assertIn(
            "02_REGISTRY/research/sources/"
            "d0_334_post_1f_offcopy_frame_delta_2026-10-28/README.md",
            {row["source"] for row in search_hits},
        )

        for row in manifest["packet_files"]:
            content = (packet / row["path"]).read_bytes()
            self.assertEqual(len(content), row["bytes"], row["path"])
            self.assertEqual(
                hashlib.sha256(content).hexdigest(), row["sha256"], row["path"]
            )

        receipt = (packet / "replay/owner_receipt.json").read_bytes()
        self.assertEqual(
            hashlib.sha256(receipt).hexdigest(), manifest["owner_receipt_sha256"]
        )
        self.assertEqual(receipt, (packet / "replay/normal.json").read_bytes())
        self.assertEqual(receipt, (packet / "replay/optimized.json").read_bytes())

    def test_current_post_fd_ready_reflection_packet_is_retrievable_and_scoped(self) -> None:
        packet = (
            proof.ROOT / "02_REGISTRY/research/sources/"
            "d0_334_post_fd_delta_2026-10-28"
        )
        manifest_bytes = (packet / "MANIFEST.json").read_bytes()
        manifest = json.loads(manifest_bytes)
        self.assertEqual(
            hashlib.sha256(manifest_bytes).hexdigest(),
            (packet / "MANIFEST.sha256").read_text(encoding="ascii").split()[0],
        )
        self.assertEqual(
            manifest["source_range"],
            {
                "base_commit": "fd35893d77e4aa5f819bafa0c6428c8e7a8f1812",
                "head_commit": "4a57cfd948226704b9561dec287d7f60154985ea",
                "commits": 8,
            },
        )

        replay = manifest["replays"]["ready_reflection"]
        normal = (packet / replay["normal_output"]).read_bytes()
        optimized = (packet / replay["optimized_output"]).read_bytes()
        owner = (packet / replay["owner_result"]).read_bytes()
        self.assertEqual(normal, optimized)
        self.assertEqual(normal, owner)
        result = json.loads(normal)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["checks"], 359)
        self.assertEqual(result["checker_sha256"], replay["expected_checker_sha256"])
        self.assertEqual(result["source"]["raw_new_gate_basis_rows"], 260)
        self.assertEqual(result["source"]["nonzero_Hermitian_rows"], 20)
        self.assertFalse(result["AF_schedule"]["binary_AF_physical_admission"])
        self.assertIn("No physical flag/actuator admission", result["scope"])
        self.assertIn("GR closure", result["scope"])

        inventory_path = (
            proof.ROOT / "02_REGISTRY/research/sources/"
            "d0_proof_architecture_formalization_2026-10-24/reports/"
            "ready_reflection_gain_declarations_2026-10-28.json"
        )
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        self.assertEqual(
            inventory["snapshot_commit"], "915e283ab1b505ca673dabb79fb9adae3c63e9a7"
        )
        self.assertFalse(inventory["worktree_dirty"])
        self.assertEqual(inventory["public_import_root"], "D0.All")
        self.assertEqual(
            inventory["lean_source_digest"],
            "d19513df16bc00ff285081b8470fb16df2eaed64f10d54c8c53a4a8ea77f5d40",
        )
        declarations = {row["name"]: row for row in inventory["declarations"]}
        normalized = declarations["D0.Research.readinessNormalizedSource_eq"]
        self.assertTrue(normalized["exists"])
        self.assertEqual(
            normalized["module"], "D0.Research.CalibratedQuerySourceFloor"
        )
        for hypothesis in ("0 < γ", "γ ≤ 1", "0 < c", "0 < gain"):
            self.assertIn(hypothesis, normalized["elaborated_type"])
        self.assertEqual(
            normalized["axioms"], ["Classical.choice", "Quot.sound", "propext"]
        )

        data = proof.load_dataset(proof.ROOT)
        hits = proof.full_text_search(
            proof.ROOT, "Emit the readiness reflection", limit=100
        )
        by_source = {row["source"]: row for row in hits}
        intake_path = "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md"
        source_path = (
            "02_REGISTRY/research/sources/d0_334_post_fd_delta_2026-10-28/"
            "upstream/02_REGISTRY/research/"
            "A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"
        )
        self.assertIn(intake_path, by_source)
        self.assertIn(source_path, by_source)
        support = proof.structured_search(
            data, "D0.Research.CalibratedQuerySourceFloor"
        )
        self.assertEqual(support[0]["kind"], "formal-support-metadata")
        self.assertIn(
            source_path
            + "#7dk-emit-the-readiness-reflection-and-retain-its-complete-control-covector",
            support[0]["record"]["referenced_by"],
        )

    def test_current_fixed_sine_declaration_inventory_is_compiled_and_scoped(self) -> None:
        inventory_path = (
            proof.ROOT / "02_REGISTRY/research/sources/"
            "d0_proof_architecture_formalization_2026-10-24/reports/"
            "weak_test_declarations_current_fc7adabf_2026-10-28.json"
        )
        raw = inventory_path.read_bytes()
        self.assertEqual(
            hashlib.sha256(raw).hexdigest(),
            "f38683cc84484ee89db398a13c3990fd8001d33bc5360f47202e89dfed44bb3c",
        )
        inventory = json.loads(raw)
        self.assertEqual(
            inventory["snapshot_commit"], "fc7adabf9414f4de4f274267143797fc426ef7cb"
        )
        self.assertFalse(inventory["worktree_dirty"])
        self.assertEqual(inventory["public_import_root"], "D0.All")
        self.assertEqual(inventory["toolchain"], "leanprover/lean4:v4.30.0")
        self.assertEqual(
            inventory["lean_source_digest"],
            "d19513df16bc00ff285081b8470fb16df2eaed64f10d54c8c53a4a8ea77f5d40",
        )

        declarations = {row["name"]: row for row in inventory["declarations"]}
        theorem = declarations["D0.Geometry.archive_doubling_sine_weak_pairing_tendsto"]
        self.assertTrue(theorem["exists"])
        self.assertEqual(
            theorem["module"], "D0.Geometry.ArchiveGradedRefinementWeakTest"
        )
        self.assertEqual(
            theorem["source_path"],
            "03_FORMALIZATION/D0/Geometry/ArchiveGradedRefinementWeakTest.lean",
        )
        module_blob = subprocess.run(
            [
                "git",
                "rev-parse",
                f"{inventory['snapshot_commit']}:{theorem['source_path']}",
            ],
            cwd=proof.ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.assertEqual(module_blob, "4e6b5419f46a542091cec0d4f82d3b693f99cd26")
        self.assertEqual(
            theorem["elaborated_type"],
            "∀ (r : D0.Role),\n"
            "  Filter.Tendsto\n"
            "    (fun N =>\n"
            "      D0.Geometry.archiveSineWeakPairing (N + (N + 2))\n"
            "        (D0.Geometry.archiveRepeatedGradedPullback N "
            "(D0.Geometry.archiveUnitSingletonCochain N r) (N + 2)) r)\n"
            "    Filter.atTop (nhds (2 / Real.pi))",
        )
        self.assertIn(
            "D0.Geometry.archive_doubling_weak_pairing_eq_half_sine",
            theorem["proof_dependencies"],
        )
        self.assertIn(
            "D0.Geometry.archive_half_sine_mean_tendsto",
            theorem["proof_dependencies"],
        )
        self.assertEqual(
            theorem["axioms"], ["Classical.choice", "Quot.sound", "propext"]
        )

    def test_refoliation_delta_is_retrievable_without_physical_owner_inference(self) -> None:
        data = proof.load_dataset(proof.ROOT)
        hits = proof.full_text_search(
            proof.ROOT, "root cut refoliation closure", limit=100
        )
        by_source = {item["source"]: item for item in hits}
        intake_path = "02_REGISTRY/research/D0_CHAT_RESULTS_INTEGRATION_2026_10_28.md"
        proof_path = (
            "02_REGISTRY/research/sources/"
            "d0_334_refoliation_delta_2026-10-28/upstream/"
            "A4D_ROOT_CUT_TO_REFOLIATION_CLOSURE_2026_10_28.md"
        )
        self.assertIn(intake_path, by_source)
        self.assertIn(proof_path, by_source)
        links = proof._declared_source_links(data, intake_path)
        self.assertEqual(links["owner_status"], "no_exact_assembly_owner_link")
        self.assertEqual(
            [row["lean_module"] for row in links["formal_support_locators"]],
            [
                "D0.Algebra.MovingProjectorCalculus",
                "D0.Algebra.DirectFeedbackSource",
                "D0.Algebra.MovingProjectorPositiveChart",
                "D0.Algebra.MovingProjectorTransport",
                "D0.Analysis.MatrixDeterminantDerivative",
            ],
        )
        self.assertEqual(links["formal_support_locators_omitted"], 4)
        self.assertTrue(all(
            row["status"] == "metadata_locator_only"
            for row in links["formal_support_locators"]
        ))
        coefficient_hits = proof.structured_search(
            data, "D0.Geometry.RefoliationWitnessCoefficientExtraction"
        )
        self.assertEqual(coefficient_hits[0]["kind"], "formal-support-metadata")
        self.assertIn(
            "02_REGISTRY/research/sources/d0_334_refoliation_delta_2026-10-28/upstream/PROOF_RU.md#4",
            coefficient_hits[0]["record"]["referenced_by"],
        )

    def test_boundary_rigidity_delta_is_retrievable_without_physical_owner_inference(self) -> None:
        data = proof.load_dataset(proof.ROOT)
        hits = proof.full_text_search(
            proof.ROOT,
            "A4D ORIGINAL RETURN BOUNDARY AND CANONICAL RIGIDITY 2026 10 28",
            limit=100,
        )
        by_source = {item["source"]: item for item in hits}
        intake_path = "02_REGISTRY/research/D0_CHAT_RESULTS_INTEGRATION_2026_10_28.md"
        source_path = (
            "02_REGISTRY/research/sources/"
            "d0_334_boundary_rigidity_delta_2026-10-28/upstream/"
            "02_REGISTRY/research/A4D_ORIGINAL_RETURN_BOUNDARY_AND_CANONICAL_RIGIDITY_2026_10_28.md"
        )
        self.assertIn(intake_path, by_source)
        self.assertIn(source_path, by_source)
        links = proof._declared_source_links(data, source_path)
        self.assertEqual(links["owner_status"], "no_exact_assembly_owner_link")
        self.assertEqual(links["formal_support_locators"], [])

    def test_paid_source_delta_and_finite_matrix_support_are_retrievable(self) -> None:
        data = proof.load_dataset(proof.ROOT)
        hits = proof.full_text_search(
            proof.ROOT,
            "A4D NONVACUUM SAME REPRESENTATIVE PAID SOURCE RESIDUAL 2026 10 20",
            limit=100,
        )
        by_source = {item["source"]: item for item in hits}
        intake_path = "02_REGISTRY/research/D0_CHAT_RESULTS_INTEGRATION_2026_10_28.md"
        source_path = (
            "02_REGISTRY/research/sources/"
            "d0_334_paid_source_delta_2026-10-28/upstream/"
            "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"
        )
        self.assertIn(intake_path, by_source)
        self.assertIn(source_path, by_source)
        links = proof._declared_source_links(data, source_path)
        self.assertEqual(links["owner_status"], "no_exact_assembly_owner_link")
        self.assertEqual(
            [row["lean_module"] for row in links["formal_support_locators"]],
            [
                "D0.Analysis.MovingCutQueryDerivativeAdapter",
                "D0.Geometry.MovingCutQueryCancellation",
            ],
        )
        self.assertTrue(all(
            row["status"] == "metadata_locator_only"
            for row in links["formal_support_locators"]
        ))
        for module in (
            "D0.Analysis.MovingCutQueryDerivativeAdapter",
            "D0.Geometry.MovingCutQueryCancellation",
        ):
            with self.subTest(module=module):
                support_hits = proof.structured_search(data, module)
                self.assertEqual(support_hits[0]["kind"], "formal-support-metadata")
                self.assertIn(
                    source_path,
                    support_hits[0]["record"]["referenced_by"],
                )

    def test_generated_cut_application_is_retrievable_without_false_lean_or_owner_link(self) -> None:
        data = proof.load_dataset(proof.ROOT)
        hits = proof.full_text_search(
            proof.ROOT,
            "QUERY ORBIT APPLICATION RU",
            limit=100,
        )
        by_source = {item["source"]: item for item in hits}
        intake_path = "02_REGISTRY/research/D0_CHAT_RESULTS_INTEGRATION_2026_10_28.md"
        application_path = (
            "02_REGISTRY/research/sources/"
            "d0_334_generated_cut_application_delta_2026-10-28/upstream/"
            "02_REGISTRY/research/sources/d0_root_boundary_reduction_2026-10-28/"
            "QUERY_ORBIT_APPLICATION_RU.md"
        )
        self.assertIn(intake_path, by_source)
        self.assertIn(application_path, by_source)
        links = proof._declared_source_links(data, application_path)
        self.assertEqual(links["owner_status"], "no_exact_assembly_owner_link")
        self.assertEqual(links["formal_support_locators"], [])

    def test_final_composition_delta_is_retrievable_without_false_lean_or_owner_link(self) -> None:
        data = proof.load_dataset(proof.ROOT)
        hits = proof.full_text_search(
            proof.ROOT,
            "A4D RETAINED HISTORY FINAL COMPOSITION 2026 10 28",
            limit=100,
        )
        by_source = {item["source"]: item for item in hits}
        intake_path = "02_REGISTRY/research/D0_CHAT_RESULTS_INTEGRATION_2026_10_28.md"
        source_path = (
            "02_REGISTRY/research/sources/"
            "d0_334_final_composition_delta_2026-10-28/upstream/"
            "02_REGISTRY/research/A4D_RETAINED_HISTORY_FINAL_COMPOSITION_2026_10_28.md"
        )
        self.assertIn(intake_path, by_source)
        self.assertIn(source_path, by_source)
        links = proof._declared_source_links(data, source_path)
        self.assertEqual(links["owner_status"], "no_exact_assembly_owner_link")
        self.assertEqual(links["formal_support_locators"], [])

    def test_closed_history_delta_is_retrievable_without_false_lean_or_owner_link(self) -> None:
        data = proof.load_dataset(proof.ROOT)
        hits = proof.full_text_search(
            proof.ROOT,
            "A4D CLOSED HISTORY DIRECT PROOF 2026 10 28",
            limit=100,
        )
        by_source = {item["source"]: item for item in hits}
        intake_path = "02_REGISTRY/research/D0_CHAT_RESULTS_INTEGRATION_2026_10_28.md"
        source_path = (
            "02_REGISTRY/research/sources/"
            "d0_334_closed_history_direct_delta_2026-10-28/upstream/"
            "02_REGISTRY/research/A4D_CLOSED_HISTORY_DIRECT_PROOF_2026_10_28.md"
        )
        self.assertIn(intake_path, by_source)
        self.assertIn(source_path, by_source)
        links = proof._declared_source_links(data, source_path)
        self.assertEqual(links["owner_status"], "no_exact_assembly_owner_link")
        self.assertEqual(links["formal_support_locators"], [])



if __name__ == "__main__":
    unittest.main()

