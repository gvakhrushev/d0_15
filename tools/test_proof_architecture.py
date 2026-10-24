from __future__ import annotations

import pathlib
import hashlib
import subprocess
import tempfile
import unittest

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

    def test_result_crosswalk_keeps_compiled_candidates_separate_from_application_acceptance(self) -> None:
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
            source_sha = hashlib.sha256(pinned_bytes).hexdigest()
            data = dataset(root)
            data["assembly"]["results"] = [{
                "id": "r1", "statement": "Exact vector reconstruction",
                "owner": "owner", "reported_state": "scoped result",
                "evidence": [{"ref": ref, "path": source_rel, "sha256": source_sha}],
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

        self.assertEqual(view["evidence_crosswalks"][0]["pin"]["pin_status"], "verified")
        self.assertEqual(
            view["evidence_crosswalks"][0]["pin"]["current_source_status"], "matches_pin"
        )
        self.assertEqual(view["compiled_declarations"][0]["elaborated_type"], "True")
        self.assertEqual(view["compiled_declarations"][0]["proof_details_status"],
                         "collected_for_exact_claim_locator")
        self.assertEqual(view["claim_locator_candidates"][0]["claim_id"], "CLM-1")
        self.assertEqual(view["formal_support_candidates"][0]["lean_module"], "D0.Foo")
        self.assertEqual(view["declaration_disposition"], "candidate")
        self.assertEqual(view["semantic_relation_status"], "unresolved")
        self.assertFalse(view["acceptance_inferred"])
        self.assertEqual(view["declared_relations"]["declared_applications"][0]["review"]["state"],
                         "accepted")

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


if __name__ == "__main__":
    unittest.main()
