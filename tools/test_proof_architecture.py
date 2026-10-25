from __future__ import annotations

import pathlib
import hashlib
import io
import json
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from tools import proof_architecture as proof
from tools import proof_architecture_cold_start as cold_start


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
        self.assertEqual(view["declared_applications"], [])

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

    def test_compiled_reuse_follows_explicit_canonical_claim_alias(self) -> None:
        data = dataset()
        data["claims"][0]["release_status"] = "CORE-FORMALIZED"
        data["aliases"] = [{
            "legacy_id": "OLD-CLAIM-1", "kind": "CANONICAL_TARGET",
            "canonical_claim_id": "CLM-1", "first_reference": "BOOK.md:10",
            "note": "Renamed claim locator.",
        }]

        class InventoryStub:
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

    def test_car_zero_mode_cold_start_keeps_hopping_and_hodge_scopes(self) -> None:
        case = next(
            item for item in cold_start.CASES
            if item["id"] == "car-hopping-zero-mode-vs-hodge-kernel"
        )
        hits_by_query = proof.full_text_search_many(
            proof.ROOT, case["queries"], limit=18
        )
        query_pairs = list(zip(case["queries"], hits_by_query))

        for path in case["required_refs"]:
            status = cold_start._required_source_status(query_pairs, {"path": path})
            self.assertTrue(status["found"], f"cold-start search missed {path}")

        support_modules = {
            row["lean_module"] for row in proof.load_dataset(proof.ROOT)["formal_support"]
        }
        self.assertIn("D0.Geometry.ArchiveHodgeCARDiracKernel", support_modules)
        self.assertNotIn("D0.Geometry.ArchiveCARDirac", support_modules)
        self.assertIn("remains OPEN", case["scope_review"])
        self.assertIn("distinct", case["scope_review"])
        self.assertIn("cannot discharge the CAR claim", case["scope_review"])
        self.assertIn("formal_support.csv", case["scope_review"])
        self.assertIn("no exact heading", case["scope_review"])
        self.assertTrue(any("actual carDirac" in query for query in case["queries"]))
        self.assertTrue(any("hodgeCarDirac_kernel_finrank" in query
                            for query in case["queries"]))

    def test_claim_source_candidates_use_exact_headings_and_preserve_ambiguity(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            books = root / "01_BOOKS"
            books.mkdir()
            (books / "BOOK_01_TEST.md").write_bytes(
                b"### 01.8.1 Main source\n## 01.20 First section\n## 01.24 Second section\n"
            )
            (books / "BOOK_02_TEST.md").write_bytes(b"## 02.34 Master section\n")
            (books / "BOOK_03_TEST.md").write_bytes(
                b"## 03.1 First copy\n## 03.1 Second copy\n"
            )
            (books / "BOOK_04_TEST.md").write_bytes(
                b"# Intro\nThe body mentions 04.7 but does not define it.\n"
                b"```markdown\n## 04.7 Example in a code fence\n```\n"
                b"### 04.7.1 Child only\n"
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
                {"claim_id": "NON-BOOK", "book": "METROLOGY", "section": "scope"},
                {"claim_id": "MISMATCH", "book": "BOOK_01/02", "section": "01.8.1"},
            ]

            view = proof.claim_source_candidate_view(data)
            by_id = {row["claim_id"]: row for row in view["rows"]}

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
        self.assertEqual(by_id["NON-BOOK"]["resolution_status"], "non_book_locator")
        self.assertEqual(by_id["MISMATCH"]["resolution_status"], "malformed_locator")
        self.assertEqual(view["counts"]["fully_unique_claim_rows"], 2)
        self.assertEqual(view["counts"]["ambiguous_claim_rows"], 1)
        self.assertEqual(view["counts"]["non_book_claim_rows"], 1)
        self.assertEqual(view["counts"]["malformed_claim_rows"], 1)
        self.assertEqual(view["counts"]["unresolved_claim_rows"], 1)
        self.assertIn("do not accept the claim statement", view["interpretation"])


if __name__ == "__main__":
    unittest.main()
