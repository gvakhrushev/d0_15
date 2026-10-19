#!/usr/bin/env python3
"""Contract, mutation and workflow controls for gravity composition.

All scientific results here are synthetic fixtures, not claims about D0.
GitHub is mocked. Acceptance decisions use real immutable fixture Git commits.
"""
from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import gr_assembly as gr
import task_dispatch
import task_lifecycle
import validate_pr_contract

TASK = "WRK-A4D-ONE"
OTHER = "WRK-A4D-TWO"


class AssemblyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.directory = self.root / gr.DIRECTORY
        (self.directory / "sources").mkdir(parents=True)
        (self.root / "00_WORK/tasks").mkdir(parents=True)
        old = {"nodes": [{"id": "old", "scope": "A finite scoped obstruction.",
                          "status": "PROVED_SCOPED", "terminal_class": "NO-GO", "depends_on": [],
                          "hypotheses": ["A fixed finite carrier."], "owners": ["proof.md"]}]}
        legacy = self.snapshot("legacy.json", json.dumps(old).encode())
        legacy["node_count"] = 1
        route = self.snapshot("route.md", b"Existing parent route.\n")
        (self.root / "route.md").write_text("# Parent step\nExisting parent route.\n")
        self.proof = self.snapshot("proof.md", b"Synthetic exact evidence.\n")
        self.contract = {"schema": "d0-gr-assembly/1", "route": "route.md",
                         "legacy_import": legacy, "route_input": route,
                         "interfaces": {k: {f: f"{k} {f}" for f in gr.INTERFACE_FIELDS} for k in ["native", "other"]},
                         "goals": [{"id": "GR", "requires": ["D"], "outcome": "positive"}],
                         "obligations": [self.obligation(n, deps) for n, deps in
                                         [("A", []), ("B", ["A"]), ("C", ["A"]), ("D", ["B", "C"])]],
                         "task_bindings": {TASK: self.binding("A", "question-a"), OTHER: self.binding("B", "question-b")}}
        self.intake = {"schema": "d0-gr-applications/1", "results": [], "applications": [], "attempts": [],
                       "migration": {"old": {"result": "legacy:old", "obligation": None}}}
        self.queue = {"limits": {"WORKER": 3, "EXPENSIVE": 3, "CONTROL": 2}, "tasks": []}
        for tid in [TASK, OTHER]:
            brief = f"00_WORK/tasks/{tid}.md"
            self.queue["tasks"].append({"id": tid, "class": "WORKER", "state": "PLANNED", "brief": brief})
            (self.root / brief).write_text(f"# {tid}\nBase: `main`\nBranch: `wrk/{tid.lower()}`\n"
                                         f"Primary artifact: `proof.md`\nAssembly: `{tid}`\n")
        self.save()

    def snapshot(self, name, data):
        path = f"{gr.DIRECTORY}/sources/{name}"
        (self.root / path).write_bytes(data)
        return {"ref": "a" * 40, "path": name, "snapshot": path, "sha256": hashlib.sha256(data).hexdigest()}

    def obligation(self, name, deps=()):
        return {"id": name, "statement": "Synthetic conclusion " + name, "interface": "native",
                "scope_level": "family", "outcome": "positive", "group": "fixture", "consumer": "D",
                "methods": [{"id": "direct", "requires": list(deps)}]}

    def binding(self, ob, key):
        return {"obligations": [ob], "interface": "native", "work_key": key, "statement": "Prove " + ob,
                "consumer": "D", "mode": "proof", "assumes": [], "write_paths": ["proof.md"],
                "start_requires": [], "completion_requires": [ob]}

    def save(self):
        for name, data in [("contract.json", self.contract), ("applications.json", self.intake)]:
            (self.directory / name).write_text(json.dumps(data))
        (self.root / "00_WORK/manifest.json").write_text(json.dumps(self.queue))

    def model(self):
        self.save()
        return gr.load(self.root)

    def add_result(self, name="r", outcome="positive", interface="native", hypotheses=None,
                   kind="analytic", scope="family"):
        self.intake["results"].append({"id": name, "owner": "author", "statement": "Synthetic result " + name,
                                       "outcome": outcome, "interface": interface, "hypotheses": hypotheses or {},
                                       "kind": kind, "scope_level": scope, "evidence": [self.proof]})
        return name

    def add_app(self, name="app", result="r", target="A", bindings=None):
        app = {"id": name, "result": result, "obligation": target, "method": "direct",
               "consumer_location": "route.md#parent-step", "hypothesis_map": bindings or {},
               "review": {"state": "proposed"}}
        self.intake["applications"].append(app)
        return app

    def sign(self, app):
        model = self.model()
        value = gr.application_digest(model, model["applications"][app["id"]])
        return self.sign_record(app, value)

    def sign_record(self, app, value):
        decision = self.root / "decisions.md"
        previous = decision.read_text() if decision.exists() else ""
        decision.write_text(previous + f"Assembly-Acceptance: {app['id']} {value}\n")
        if not (self.root / ".git").exists():
            self.git("init", "-q")
        self.git("add", "decisions.md")
        self.git("-c", "user.name=Fixture reviewer", "-c", "user.email=fixture@example.invalid",
                 "commit", "-q", "-m", "Fixture independent decision")
        ref = self.git("rev-parse", "HEAD").strip()
        app["review"] = {"state": "accepted", "by": "independent reviewer", "digest": value,
                         "decision": {"ref": ref, "path": "decisions.md",
                                      "sha256": hashlib.sha256(decision.read_bytes()).hexdigest()}}
        return app

    def sign_attempt(self, attempt):
        model = self.model()
        return self.sign_record(attempt, gr.attempt_digest(model, model["attempts"][attempt["id"]]))

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, stderr=subprocess.PIPE, text=True)

    def pr(self, task=TASK, number=12, draft=True, lifecycle="IN_PROGRESS"):
        return {"number": number, "state": "open", "draft": draft,
                "html_url": f"https://github.com/gvakhrushev/d0_15/pull/{number}",
                "head": {"ref": "wrk/" + task.lower(), "sha": "a" * 40},
                "body": f"Task: `{task}`\nClass: `WORKER`\nLifecycle: `{lifecycle}`\n"}

    def cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = gr.main(["--repo-root", str(self.root), *args])
        return code, out.getvalue(), err.getvalue()

    def test_import_preserves_every_id_without_promoting_any_result(self):
        model = self.model()
        self.assertEqual(set(model["results"]), {"legacy:old"})
        self.assertEqual(gr.evaluate(model)["closed"], set())
        self.assertFalse(gr.evaluate(model)["goals"]["GR"])

    def test_missing_historical_migration_is_rejected(self):
        self.intake["migration"] = {}
        with self.assertRaisesRegex(gr.AssemblyError, "every historical id"):
            self.model()

    def test_frozen_snapshot_mutation_fails(self):
        (self.root / self.contract["legacy_import"]["snapshot"]).write_text("{}")
        with self.assertRaisesRegex(gr.AssemblyError, "SHA-256 mismatch"):
            self.model()

    def test_cycle_and_dangling_input_fail(self):
        for dep in ["D", "unknown"]:
            with self.subTest(dep=dep):
                self.contract["obligations"][0]["methods"][0]["requires"] = [dep]
                with self.assertRaisesRegex(gr.AssemblyError, "cycle|dangling"):
                    self.model()

    def test_negative_result_cannot_fill_positive_existence(self):
        self.add_result(outcome="negative")
        self.add_app()
        with self.assertRaisesRegex(gr.AssemblyError, "negative result cannot supply a positive"):
            self.model()

    def test_historical_no_go_is_not_automatically_an_application(self):
        self.add_app(result="legacy:old")
        with self.assertRaisesRegex(gr.AssemblyError, "typed intake"):
            self.model()

    def test_finite_certificate_cannot_claim_uniform_family(self):
        self.add_result(kind="exact-finite")
        with self.assertRaisesRegex(gr.AssemblyError, "finite certificate"):
            self.model()

    def test_finite_result_does_not_fill_family_premise(self):
        self.add_result(kind="exact-finite", scope="finite")
        self.add_app()
        with self.assertRaisesRegex(gr.AssemblyError, "finite scope"):
            self.model()

    def test_passport_does_not_close_internal_goal(self):
        self.add_result(kind="passport")
        self.add_app()
        with self.assertRaisesRegex(gr.AssemblyError, "passport"):
            self.model()

    def test_same_carrier_different_action_needs_transport(self):
        self.contract["interfaces"]["other"] = copy.deepcopy(self.contract["interfaces"]["native"])
        self.contract["interfaces"]["other"]["action"] = "A different complete action"
        self.add_result(interface="other")
        self.add_app()
        with self.assertRaisesRegex(gr.AssemblyError, "every transport map"):
            self.model()

    def test_complete_proved_transport_can_be_accepted(self):
        self.add_result(interface="other")
        app = self.add_app()
        app["transport"] = {"proof": self.proof, "maps": {k: "Proved fixture map for " + k for k in gr.INTERFACE_FIELDS}}
        self.sign(app)
        self.assertIn("A", gr.evaluate(self.model())["closed"])

    def test_every_hypothesis_needs_a_binding(self):
        self.add_result(hypotheses={"h1": "Remaining hypothesis"})
        self.add_app()
        with self.assertRaisesRegex(gr.AssemblyError, "every hypothesis"):
            self.model()

    def test_retained_assumption_prevents_closure_even_after_review(self):
        self.add_result(hypotheses={"h1": "Admission remains open"})
        app = self.add_app(bindings={"h1": {"assumption": "Admission remains open"}})
        self.sign(app)
        self.assertNotIn("A", gr.evaluate(self.model())["closed"])

    def test_passing_or_proposed_evidence_does_not_discharge_premise(self):
        self.add_result()
        self.add_app()
        self.assertEqual(gr.evaluate(self.model())["closed"], set())

    def test_independent_pinned_acceptance_discharges_exact_target(self):
        self.add_result()
        self.sign(self.add_app())
        model = self.model()
        self.assertEqual(gr.evaluate(model)["closed"], {"A"})
        gr.validate(model)
        self.assertEqual(gr.evaluate(model)["closed"], {"A"})

    def test_self_review_is_rejected(self):
        self.add_result()
        app = self.sign(self.add_app())
        app["review"]["by"] = "author"
        with self.assertRaisesRegex(gr.AssemblyError, "differ"):
            self.model()

    def test_multiple_independent_proofs_of_one_obligation_are_allowed(self):
        self.add_result("r1")
        self.add_result("r2")
        self.sign(self.add_app("app1", "r1"))
        self.sign(self.add_app("app2", "r2"))
        self.assertEqual(gr.evaluate(self.model())["closed"], {"A"})

    def test_named_target_hypothesis_preserves_a_scoped_conditional_theorem(self):
        self.contract["obligations"][0]["hypotheses"] = {"smooth": "A declared smooth test domain"}
        self.add_result(hypotheses={"h": "A declared smooth test domain"})
        self.sign(self.add_app(bindings={"h": {"target_hypothesis": "smooth"}}))
        self.assertEqual(gr.evaluate(self.model())["closed"], {"A"})
        self.assertFalse(gr.evaluate(self.model())["goals"]["GR"])

    def test_unlisted_target_hypothesis_is_rejected(self):
        self.add_result(hypotheses={"h": "A missing admission condition"})
        self.add_app(bindings={"h": {"target_hypothesis": "admitted"}})
        with self.assertRaisesRegex(gr.AssemblyError, "target hypothesis"):
            self.model()

    def test_nonexistent_consumer_does_not_count_as_a_parent_substitution(self):
        self.add_result()
        self.add_app()["consumer_location"] = "missing.md#parent"
        with self.assertRaisesRegex(gr.AssemblyError, "consumer location"):
            self.model()

    def test_classification_can_close_separately_without_positive_gr(self):
        ob = self.obligation("raw")
        ob.update(outcome="classification", scope_level="finite")
        self.contract["obligations"].append(ob)
        self.contract["goals"].append({"id": "RAW", "requires": ["raw"], "outcome": "classification"})
        self.add_result(outcome="negative", scope="finite", kind="exact-finite")
        self.sign(self.add_app(target="raw"))
        state = gr.evaluate(self.model())
        self.assertTrue(state["goals"]["RAW"])
        self.assertFalse(state["goals"]["GR"])

    def test_classification_cannot_be_relabelled_as_a_positive_goal(self):
        self.contract["obligations"][3]["outcome"] = "classification"
        with self.assertRaisesRegex(gr.AssemblyError, "positive goal"):
            self.model()

    def test_repository_global_closure_is_classification_not_positive_gr(self):
        root = Path(__file__).resolve().parents[1]
        model = gr.load(root)
        d0_goal = next(g for g in model["contract"]["goals"] if g["id"] == "D0-CLOSURE")
        self.assertEqual(d0_goal["outcome"], "classification")
        self.assertEqual(model["obligations"]["global_classification"]["outcome"], "classification")

    def test_reviewed_no_go_stops_only_its_scoped_attempt(self):
        self.add_result(outcome="negative")
        attempt = {"id": "dead-a", "result": "r", "interface": "native", "work_key": "question-a",
                   "scope": "Only this synthetic A route", "reopen_when": "Its actual hypotheses change",
                   "question": {"statement": "Prove A", "assumes": []},
                   "question_digest": gr.work_digest(self.model(), self.contract["task_bindings"][TASK]),
                   "review": {"state": "proposed"}}
        self.intake["attempts"].append(attempt)
        self.sign_attempt(attempt)
        model = self.model()
        self.assertFalse(gr.launch_check(model, TASK, [])["allowed"])
        self.assertTrue(gr.launch_check(model, OTHER, [])["allowed"])
        self.assertEqual(gr.evaluate(model)["closed"], set())
        self.assertTrue(gr.attempts(model, "synthetic")[0]["enforced"])

    def test_prior_attempt_digest_is_available_to_reviewer(self):
        self.add_result(outcome="negative")
        self.intake["attempts"].append({"id": "dead", "result": "r", "interface": "native", "work_key": "q",
                                       "scope": "Finite scope", "reopen_when": "A changed hypothesis",
                                       "question": {"statement": "Prove A", "assumes": []},
                                       "question_digest": gr.work_digest(self.model(), {**self.contract["task_bindings"][TASK], "work_key": "q"}),
                                       "review": {"state": "proposed"}})
        self.save()
        code, out, err = self.cli("application-digest", "dead")
        self.assertEqual((code, err), (0, ""))
        self.assertIn("Assembly-Acceptance: dead", out)

    def test_attempt_search_includes_exact_question_and_assumptions(self):
        self.add_result(outcome="negative")
        self.add_result(name="unrelated-zero-mode", outcome="negative")
        self.intake["results"][-1]["statement"] = "For every zero mode, the synthetic source vanishes."
        question = {"statement": "For every z in the declared carrier, nullity A(z)=2.",
                    "assumes": ["The full complex torus domain is retained."]}
        binding = {"interface": "native", "work_key": "question-z",
                   "statement": question["statement"], "assumes": question["assumes"]}
        attempt = {"id": "nullity-counterexample", "result": "r", "interface": "native",
                   "work_key": "question-z", "scope": "A finite exact obstruction",
                   "reopen_when": "The domain excludes the witness", "question": question,
                   "question_digest": gr.work_digest(self.model(), binding),
                   "review": {"state": "proposed"}}
        self.intake["attempts"].append(attempt)
        model = self.model()

        by_question = gr.attempts(model, "For every z")
        by_assumption = gr.attempts(model, "complex torus domain")

        self.assertEqual([row["id"] for row in by_question], ["nullity-counterexample"])
        self.assertEqual([row["id"] for row in by_assumption], ["nullity-counterexample"])

    def test_search_includes_pinned_evidence_and_snapshot_paths(self):
        self.add_result(name="source-result")
        model = self.model()

        rows = gr.search(model, "sources/proof.md")

        self.assertEqual([row["id"] for row in rows], ["source-result"])
        self.assertEqual(rows[0]["evidence_paths"],
                         ["02_REGISTRY/gr_assembly/sources/proof.md", "proof.md"])

    def test_changed_hypothesis_reopens_only_with_explicit_delta(self):
        self.add_result(outcome="negative")
        question = gr.work_digest(self.model(), self.contract["task_bindings"][TASK])
        attempt = {"id": "dead", "result": "r", "interface": "native", "work_key": "question-a",
                   "scope": "Old exact hypothesis class", "reopen_when": "A proved change of hypothesis",
                   "question": {"statement": "Prove A", "assumes": []},
                   "question_digest": question, "review": {"state": "proposed"}}
        self.intake["attempts"].append(attempt)
        self.sign_attempt(attempt)
        self.contract["task_bindings"][TASK]["assumes"] = ["A genuinely different declared hypothesis"]
        self.assertFalse(gr.launch_check(self.model(), TASK, [])["allowed"])
        self.contract["task_bindings"][TASK]["reopens"] = {"attempt": "dead", "delta": "The fixed old hypothesis is replaced by this independently justified new one."}
        self.assertTrue(gr.launch_check(self.model(), TASK, [])["allowed"])

    def test_acceptance_is_invalidated_by_interface_or_statement_change(self):
        self.add_result()
        self.sign(self.add_app())
        self.contract["interfaces"]["native"]["normalization"] = "A different norm and coefficient"
        with self.assertRaisesRegex(gr.AssemblyError, "stale acceptance"):
            self.model()

    def test_acceptance_marker_cannot_be_replaced_by_arbitrary_green_receipt(self):
        self.add_result()
        app = self.sign(self.add_app())
        decision = self.root / "decisions.md"
        decision.write_text("PASS every fixture\n")
        self.git("add", "decisions.md")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-q", "-m", "Unrelated receipt")
        app["review"]["decision"]["ref"] = self.git("rev-parse", "HEAD").strip()
        app["review"]["decision"]["sha256"] = hashlib.sha256(decision.read_bytes()).hexdigest()
        with self.assertRaisesRegex(gr.AssemblyError, "acceptance marker missing"):
            self.model()

    def test_and_dependencies_do_not_close_from_only_one_premise(self):
        self.add_result("ra")
        self.add_result("rb")
        self.sign(self.add_app("appb", "rb", "B"))
        self.assertEqual(gr.evaluate(self.model())["closed"], set())
        self.sign(self.add_app("appa", "ra", "A"))
        self.assertEqual(gr.evaluate(self.model())["closed"], {"A", "B"})
        self.assertNotIn("D", gr.readiness(self.model(), {"A", "B"}))

    def test_or_methods_remain_alternatives(self):
        self.contract["obligations"][1]["methods"].append({"id": "alternative", "requires": []})
        self.add_result()
        app = self.add_app(target="B")
        app["method"] = "alternative"
        self.sign(app)
        self.assertEqual(gr.evaluate(self.model())["closed"], {"B"})

    def test_hidden_cycle_in_hypothesis_bindings_fails(self):
        self.add_result(hypotheses={"h": "D is assumed"})
        self.add_app(bindings={"h": {"obligation": "D"}})
        with self.assertRaisesRegex(gr.AssemblyError, "cycle"):
            self.model()

    def test_independent_conditional_lemma_can_start_before_parent_inputs(self):
        self.assertTrue(gr.launch_check(self.model(), OTHER, [])["allowed"])
        self.contract["task_bindings"][OTHER]["start_requires"] = ["A"]
        self.assertIn("unproved start prerequisites", " ".join(gr.launch_check(self.model(), OTHER, [])["reasons"]))

    def test_different_task_label_does_not_avoid_duplicate_gate(self):
        self.contract["task_bindings"][OTHER]["work_key"] = "question-a"
        check = gr.launch_check(self.model(), OTHER, [self.pr()])
        self.assertFalse(check["allowed"])
        self.assertIn("same scientific work", check["reasons"][0])

    def test_named_independent_verification_is_allowed(self):
        self.contract["task_bindings"][OTHER]["work_key"] = "question-a"
        self.contract["task_bindings"][OTHER]["mode"] = "verification"
        self.assertTrue(gr.launch_check(self.model(), OTHER, [self.pr()])["allowed"])

    def test_wip_counts_live_executions_even_when_main_queue_is_planned(self):
        self.queue["limits"]["WORKER"] = 1
        check = gr.launch_check(self.model(), OTHER, [self.pr()])
        self.assertFalse(check["allowed"])
        self.assertIn("WIP is 1/1", " ".join(check["reasons"]))

    def test_live_next_resumes_existing_pr_and_never_starts_a_duplicate(self):
        actions = gr.next_actions(self.model(), [self.pr()])
        row = next(a for a in actions if a["task"] == TASK)
        self.assertEqual(row["action"], "resume")
        self.assertIn("#12", row["reasons"][0])

    def test_ready_pr_is_review_and_ambiguous_execution_fails(self):
        row = next(a for a in gr.next_actions(self.model(), [self.pr(draft=False, lifecycle="REVIEW")]) if a["task"] == TASK)
        self.assertEqual(row["action"], "review")
        with self.assertRaisesRegex(gr.AssemblyError, "ambiguous"):
            gr.next_actions(self.model(), [self.pr(), self.pr(number=13)])

    def test_retired_binding_does_not_reappear_as_unfinished_work(self):
        self.queue["tasks"] = [t for t in self.queue["tasks"] if t["id"] != TASK]
        model = self.model()
        self.assertNotIn(TASK, {a["task"] for a in gr.next_actions(model, [])})
        actions = gr.next_actions(model, [self.pr(draft=False, lifecycle="REVIEW")])
        self.assertEqual(next(a for a in actions if a["task"] == TASK)["action"], "review")

    def test_offline_next_does_not_call_github_or_authorize_launch(self):
        self.save()
        with patch.object(task_dispatch, "open_prs") as gh:
            code, out, err = self.cli("next", "--offline")
        self.assertEqual((code, err), (0, ""))
        gh.assert_not_called()
        self.assertIn("no launch authorized", out)

    def test_failed_live_lookup_is_not_an_empty_queue(self):
        with patch.object(task_dispatch, "open_prs", side_effect=ValueError("GitHub unavailable")):
            code, out, err = self.cli("next")
        self.assertEqual(code, 2)
        self.assertNotIn("eligible-for-control", out)
        self.assertIn("unavailable", err)

    def test_missing_semantic_binding_or_brief_marker_is_rejected(self):
        del self.contract["task_bindings"][TASK]
        with self.assertRaisesRegex(gr.AssemblyError, "register a scientific interface"):
            gr.validate_queue(self.root, self.model())
        self.contract["task_bindings"][TASK] = self.binding("A", "question-a")
        (self.root / self.queue["tasks"][0]["brief"]).write_text("Base: main\n")
        with self.assertRaisesRegex(gr.AssemblyError, "exactly one Assembly"):
            gr.validate_queue(self.root, self.model())

    def test_dispatch_duplicate_gate_runs_before_launch_text(self):
        self.contract["task_bindings"][OTHER]["work_key"] = "question-a"
        self.save()
        out, err = io.StringIO(), io.StringIO()
        with patch.object(task_dispatch, "open_prs", return_value=[self.pr()]):
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = task_dispatch.main([OTHER, "--repo-root", str(self.root)])
        self.assertEqual(code, 2)
        self.assertNotIn("Execute GitHub-first", out.getvalue())
        self.assertIn("same scientific work", err.getvalue())

    def test_lifecycle_start_failure_preserves_queue_and_brief(self):
        self.save()
        before = (self.root / "00_WORK/manifest.json").read_bytes()
        with patch.object(task_lifecycle, "ROOT", self.root), patch.object(task_lifecycle, "MANIFEST", self.root / "00_WORK/manifest.json"):
            with patch.object(task_dispatch, "open_prs", return_value=[self.pr()]):
                with self.assertRaisesRegex(task_lifecycle.LifecycleError, "existing execution"):
                    task_lifecycle.transition(TASK, "start")
        self.assertEqual((self.root / "00_WORK/manifest.json").read_bytes(), before)
        self.assertTrue((self.root / self.queue["tasks"][0]["brief"]).exists())

    def test_retire_requires_actual_accepted_completion(self):
        with self.assertRaisesRegex(gr.AssemblyError, "complete reviewable terminal"):
            gr.retirement_check(self.model(), TASK)
        self.add_result()
        self.sign(self.add_app())
        gr.retirement_check(self.model(), TASK)

    def test_manual_retirement_cannot_bypass_ready_pr_gate(self):
        self.queue["tasks"] = [t for t in self.queue["tasks"] if t["id"] != TASK]
        (self.root / f"00_WORK/tasks/{TASK}.md").unlink()
        self.save()
        event = {"number": 17, "pull_request": {"number": 17, "draft": False, "head": {"ref": "wrk/one"},
                 "body": f"Repository: `gvakhrushev/d0_15`\nTask: `{TASK}`\nClass: `WORKER`\nLifecycle: `REVIEW`\n"
                         f"Baseline: `{'a' * 40}`\nPrimary-Artifact: `proof.md`\n"}}
        with self.assertRaisesRegex(validate_pr_contract.ContractError, "complete reviewable terminal"):
            validate_pr_contract.validate_event(event, self.root)

    def test_ready_review_candidate_does_not_need_its_later_scientific_acceptance(self):
        self.add_result()
        self.add_app()
        model = self.model()
        gr.retirement_check(model, TASK)
        self.assertEqual(gr.evaluate(model)["closed"], set())
        self.assertEqual(gr.evaluate(model, submission=True)["closed"], {"A"})

    def test_ready_rejects_a_partial_result_with_remaining_physical_assumptions(self):
        self.add_result(hypotheses={"admission": "The needed admission is unproved"})
        self.add_app(bindings={"admission": {"assumption": "The needed admission is unproved"}})
        with self.assertRaisesRegex(gr.AssemblyError, "complete reviewable terminal"):
            gr.retirement_check(self.model(), TASK)

    def test_consumed_prerequisite_statement_is_bound_into_acceptance(self):
        self.add_result()
        self.sign(self.add_app(target="B"))
        self.contract["obligations"][0]["statement"] = "A weaker replacement for A"
        with self.assertRaisesRegex(gr.AssemblyError, "stale acceptance"):
            self.model()

    def test_consumed_hypothesis_contract_is_bound_into_acceptance(self):
        self.contract["obligations"][1]["methods"][0]["requires"] = []
        self.add_result(hypotheses={"h": "Exact B"})
        self.sign(self.add_app(bindings={"h": {"obligation": "B"}}))
        self.contract["obligations"][1]["statement"] = "A changed statement for the consumed B hypothesis"
        with self.assertRaisesRegex(gr.AssemblyError, "stale acceptance"):
            self.model()

    def test_unused_alternative_method_does_not_invalidate_existing_proof(self):
        self.add_result()
        self.sign(self.add_app())
        self.contract["obligations"][0]["methods"].append({"id": "another", "requires": []})
        self.assertEqual(gr.evaluate(self.model())["closed"], {"A"})

    def test_negative_result_replacement_invalidates_attempt_acceptance(self):
        self.add_result(outcome="negative")
        attempt = {"id": "dead", "result": "r", "interface": "native", "work_key": "question-a",
                   "scope": "The old exact negative theorem", "reopen_when": "A changed hypothesis",
                   "question": {"statement": "Prove A", "assumes": []},
                   "question_digest": gr.work_digest(self.model(), self.contract["task_bindings"][TASK]),
                   "review": {"state": "proposed"}}
        self.intake["attempts"].append(attempt)
        self.sign_attempt(attempt)
        self.intake["results"][0]["statement"] = "A completely different negative theorem"
        with self.assertRaisesRegex(gr.AssemblyError, "stale acceptance"):
            self.model()

    def test_case_insensitive_live_metadata_matches_the_canonical_dispatcher(self):
        candidate = self.pr()
        candidate["body"] = candidate["body"].replace("Task:", "task:").replace("Class:", "class:").replace("Lifecycle:", "lifecycle:")
        self.contract["task_bindings"][OTHER]["work_key"] = "question-a"
        model = self.model()
        self.assertFalse(gr.launch_check(model, OTHER, [candidate])["allowed"])
        self.assertEqual(next(a for a in gr.next_actions(model, [candidate]) if a["task"] == TASK)["action"], "resume")
        self.queue["limits"]["WORKER"] = 1
        self.contract["task_bindings"][OTHER]["work_key"] = "question-b"
        self.assertIn("WIP is 1/1", " ".join(gr.launch_check(self.model(), OTHER, [candidate])["reasons"]))

    def test_independent_verification_does_not_block_resuming_the_original_work(self):
        self.contract["task_bindings"][OTHER]["work_key"] = "question-a"
        self.contract["task_bindings"][OTHER]["mode"] = "verification"
        model = self.model()
        self.assertTrue(gr.launch_check(model, TASK, [self.pr(task=OTHER)])["allowed"])
        actions = gr.next_actions(model, [self.pr(), self.pr(task=OTHER, number=13)])
        self.assertEqual({a["action"] for a in actions}, {"resume"})

    def test_impact_reuses_existing_dependency_selector_without_replay(self):
        import research_input_closure
        with patch.object(research_input_closure, "select", return_value={"changed": ["shared.py"], "selected": [
                {"certificate": "consumer.py", "reasons": ["changed-input"]}], "provenance_ok": True}) as selector:
            report = gr.impact(self.model(), "base", "head")
        selector.assert_called_once_with(self.root.resolve(), "head", "base")
        self.assertEqual(report["certificate_selection"][0]["path"], "consumer.py")
        self.assertFalse(report["ran"])

    def test_impact_marks_snapshot_and_parent_consumer_changes(self):
        import research_input_closure
        self.add_result()
        app = self.add_app()
        model = self.model()
        changes = [self.proof["path"], self.proof["snapshot"], "route.md",
                   self.contract["route_input"]["snapshot"]]
        for path in changes:
            with self.subTest(path=path), patch.object(
                    research_input_closure, "select",
                    return_value={"changed": [path], "selected": [], "provenance_ok": True}):
                report = gr.impact(model, "base", "head")
            self.assertEqual([row["application"] for row in report["applications_to_review"]], [app["id"]])
            row = report["applications_to_review"][0]
            self.assertEqual(row["changed_paths"], [path])
            if path == "route.md":
                self.assertEqual(row["change_kinds"][path],
                                 ["named parent consumer", "pinned route input"])
            if path == self.contract["route_input"]["snapshot"]:
                self.assertEqual(row["change_kinds"][path], ["pinned route input"])

    def test_impact_marks_pinned_acceptance_decision_changes(self):
        import research_input_closure
        self.add_result()
        app = self.add_app()
        self.sign(app)
        model = self.model()
        path = "decisions.md"
        with patch.object(research_input_closure, "select", return_value={
                "changed": [path], "selected": [], "provenance_ok": True}):
            report = gr.impact(model, "base", "head")
        self.assertEqual([row["application"] for row in report["applications_to_review"]], [app["id"]])
        self.assertEqual(report["applications_to_review"][0]["change_kinds"][path],
                         ["pinned acceptance decision"])

    def test_generated_view_mutation_is_detected(self):
        self.assertEqual(self.cli("render")[0], 0)
        self.assertEqual(self.cli("render", "--check")[0], 0)
        (self.directory / "VIEW.md").write_text("Fabricated closure\n")
        self.assertEqual(self.cli("render", "--check")[0], 2)

    def test_query_commands_leave_all_source_bytes_unchanged(self):
        self.save()
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        for args in [("check",), ("show",), ("why", "A"), ("search", "finite"), ("attempts",),
                     ("next", "--offline"), ("template", TASK)]:
            with self.subTest(args=args):
                self.assertEqual(self.cli(*args)[0], 0)
        after = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_path_traversal_is_rejected(self):
        self.proof["snapshot"] = gr.DIRECTORY + "/sources/../../../outside.md"
        self.add_result()
        with self.assertRaisesRegex(gr.AssemblyError, "unsafe repository path"):
            self.model()


if __name__ == "__main__":
    unittest.main()
