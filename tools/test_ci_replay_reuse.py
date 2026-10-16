#!/usr/bin/env python3
"""Focused reuse fixtures: real temporary Git history, mocked read-only API."""
from __future__ import annotations

import contextlib
import copy
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import ci_replay_reuse as reuse

REPO = "example/d0"
BRANCH = "exp/source"
ENV = "e" * 64


class ReuseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Fixture")
        for path in ["README.md", "AGENTS.md", "00_WORK/README.md", "science.py",
                     "tools/ci_replay_reuse.py", ".github/workflows/guards.yml"]:
            dest = self.root / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text("base\n")
        self.base = self.commit()
        (self.root / "science.py").write_text("certified scientific input\n")
        self.before = self.commit()
        (self.root / "README.md").write_text("updated route\n")
        self.head = self.commit()
        self.event = {"action": "synchronize", "before": self.before, "number": 7,
                      "repository": {"full_name": REPO},
                      "pull_request": {"number": 7, "draft": False, "state": "open",
                                       "head": {"sha": self.head, "ref": BRANCH, "repo": {"full_name": REPO}},
                                       "base": {"sha": self.base, "ref": "main", "repo": {"full_name": REPO}}}}
        repo_url = f"https://api.github.com/repos/{REPO}"
        self.run = {"id": 100, "run_attempt": 2, "name": "D0 guards", "path": reuse.WORKFLOW,
                    "head_sha": self.before, "head_branch": BRANCH, "event": "pull_request",
                    "status": "completed", "conclusion": "success",
                    "repository": {"full_name": REPO}, "head_repository": {"full_name": REPO},
                    "pull_requests": [{"number": 7, "url": f"{repo_url}/pulls/7",
                                       "head": {"sha": self.before, "ref": BRANCH, "repo": {"url": repo_url}},
                                       "base": {"sha": self.base, "ref": "main", "repo": {"url": repo_url}}}]}
        self.job = {"id": 200, "run_id": 100, "run_attempt": 2, "name": "guards",
                    "status": "completed", "conclusion": "success",
                    "steps": [{"name": reuse.RESEARCH_STEP, "status": "completed", "conclusion": "success"}]}
        self.runs = [self.run]
        self.jobs = [self.job]
        self.logs = f"2026-10-15T12:34:56.1234567Z D0_REPLAY_ENV_SHA256={ENV}\n"
        self.calls = []

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, stderr=subprocess.PIPE).decode().strip()

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")
        return self.git("rev-parse", "HEAD")

    def api(self, root, endpoint, **options):
        self.assertEqual(root, self.root)
        self.calls.append((endpoint, options))
        if "/workflows/guards.yml/runs?" in endpoint:
            self.assertIn("head_sha=" + self.before, endpoint)
            self.assertTrue(options.get("paginate"))
            return [{"workflow_runs": []}, {"workflow_runs": self.runs}]
        if "/attempts/2/jobs?" in endpoint:
            self.assertTrue(options.get("paginate"))
            return [{"jobs": self.jobs}]
        if endpoint.endswith("/actions/jobs/200/logs"):
            self.assertTrue(options.get("raw"))
            return self.logs
        raise ValueError("unexpected fixture endpoint")

    def decide(self, **kwargs):
        return reuse.decide(self.event, REPO, self.root, ENV, api=self.api, **kwargs)

    def test_allowed_docs_reuse_same_actual_replay_and_environment(self):
        result = self.decide()
        self.assertTrue(result.reuse)
        self.assertEqual(result.run_url, f"https://github.com/{REPO}/actions/runs/100/attempts/2")
        self.assertEqual(len(self.calls), 3)
        for path in ("AGENTS.md", "00_WORK/README.md"):
            (self.root / path).write_text("new docs\n")
        self.event["pull_request"]["head"]["sha"] = self.commit()
        self.assertTrue(self.decide().reuse)

    def test_other_events_draft_and_missing_before_never_query_evidence(self):
        changes = [{"action": "ready_for_review"}, {"action": "opened"}, {"before": ""},
                   {"before": "0" * 40}, {"before": "main"}, {"before": self.head}]
        for change in changes:
            with self.subTest(change=change):
                event = copy.deepcopy(self.event)
                event.update(change)
                self.assertFalse(reuse.decide(event, REPO, self.root, ENV, api=self.api).reuse)
        self.event["pull_request"]["draft"] = True
        self.assertFalse(self.decide().reuse)
        self.event["pull_request"]["draft"] = False
        for name in ("push", "workflow_dispatch", "pull_request_target", ""):
            self.assertFalse(self.decide(event_name=name).reuse)
        self.assertEqual(self.calls, [])

    def test_scientific_code_workflow_and_helper_changes_force_replay(self):
        for path in ("science.py", "tools/ci_replay_reuse.py", ".github/workflows/guards.yml", "other.md"):
            with self.subTest(path=path):
                self.git("reset", "--hard", self.head)
                (self.root / path).write_text("different input\n")
                self.event["pull_request"]["head"]["sha"] = self.commit()
                self.assertFalse(self.decide().reuse)
        self.assertEqual(self.calls, [])

    def test_current_base_not_ancestor_of_before_forces_replay(self):
        self.event["pull_request"]["base"]["sha"] = self.head
        self.assertFalse(self.decide().reuse)
        self.assertEqual(self.calls, [])

    def test_uncommitted_tracked_or_index_changes_force_replay(self):
        (self.root / "science.py").write_text("mutation by an earlier guard\n")
        self.assertFalse(self.decide().reuse)
        self.git("add", "science.py")
        self.assertFalse(self.decide().reuse)
        self.assertEqual(self.calls, [])

    def test_clean_but_wrong_checked_tree_cannot_reuse(self):
        self.git("checkout", "-q", "--detach", self.before)
        self.assertFalse(self.decide().reuse)
        self.assertEqual(self.calls, [])

    def test_synthetic_merge_sha_with_current_head_tree_is_supported(self):
        tree = self.git("rev-parse", f"{self.head}^{{tree}}")
        synthetic = self.git("commit-tree", tree, "-p", self.base, "-p", self.head,
                             "-m", "synthetic PR checkout")
        self.assertNotEqual(synthetic, self.head)
        self.git("checkout", "-q", "--detach", synthetic)
        self.assertTrue(self.decide().reuse)

    def test_force_push_docs_only_heads_with_different_synthetic_merge_cannot_reuse(self):
        common = self.before  # science X
        self.git("checkout", "-q", "--detach", common)
        (self.root / "science.py").write_text("base now has science Y\n")
        advanced_base = self.commit()
        (self.root / "science.py").write_text("certified scientific input\n")
        prior = self.commit()  # contains advanced base, but restores X
        self.git("checkout", "-q", "--detach", common)
        (self.root / "README.md").write_text("force-pushed docs\n")
        current = self.commit()  # science X, but lacks advanced base
        self.assertEqual(self.git("diff", "--name-only", prior, current), "README.md")
        self.event["before"] = prior
        self.event["pull_request"]["base"]["sha"] = advanced_base
        self.event["pull_request"]["head"]["sha"] = current
        self.assertFalse(self.decide().reuse)
        self.assertEqual(self.calls, [])

    def test_wrong_recorded_base_pr_repository_branch_or_workflow(self):
        original = copy.deepcopy(self.run)
        changes = [lambda r: r["pull_requests"][0]["base"].update(sha=self.before),
                   lambda r: r["pull_requests"][0].update(number=8),
                   lambda r: r["repository"].update(full_name="wrong/repo"),
                   lambda r: r["head_repository"].update(full_name="wrong/repo"),
                   lambda r: r.update(head_branch="other"),
                   lambda r: r.update(path=".github/workflows/other.yml"),
                   lambda r: r.update(head_sha=self.head),
                   lambda r: r["pull_requests"][0]["head"].update(sha=self.head),
                   lambda r: r["pull_requests"][0]["head"]["repo"].update(url="https://api.github.com/repos/wrong/repo"),
                   lambda r: r.update(pull_requests=[])]
        for change in changes:
            self.runs = [copy.deepcopy(original)]
            change(self.runs[0])
            self.assertFalse(self.decide().reuse)

    def test_missing_failed_cancelled_or_running_latest_run_cannot_reuse_older_green(self):
        self.runs = []
        self.assertFalse(self.decide().reuse)
        for status, conclusion in [("completed", "failure"), ("completed", "cancelled"),
                                   ("in_progress", None)]:
            self.runs = [copy.deepcopy(self.run), {**copy.deepcopy(self.run), "id": 101,
                                                  "status": status, "conclusion": conclusion}]
            self.assertFalse(self.decide().reuse)

    def test_skipped_draft_or_reuse_chain_step_is_not_successful_replay(self):
        for conclusion in ("skipped", "failure", "cancelled", None):
            self.job["steps"][0]["conclusion"] = conclusion
            self.assertFalse(self.decide().reuse)
        self.job["steps"] = []
        self.assertFalse(self.decide().reuse)

    def test_job_success_exact_attempt_and_unique_research_step_required(self):
        original = copy.deepcopy(self.job)
        for change in [lambda j: j.update(run_id=101), lambda j: j.update(run_attempt=1),
                       lambda j: j.update(conclusion="failure"), lambda j: j.update(status="in_progress"),
                       lambda j: j["steps"].append(copy.deepcopy(j["steps"][0]))]:
            self.jobs = [copy.deepcopy(original)]
            change(self.jobs[0])
            self.assertFalse(self.decide().reuse)
        self.jobs = []
        self.assertFalse(self.decide().reuse)

    def test_environment_log_missing_ambiguous_changed_or_command_echo(self):
        valid = self.logs
        for logs in ("", valid + valid, valid.replace(ENV, "f" * 64),
                     f"2026-10-15T12:34:56Z echo D0_REPLAY_ENV_SHA256={ENV}\n",
                     f"D0_REPLAY_ENV_SHA256={ENV}\n"):
            self.logs = logs
            self.assertFalse(self.decide().reuse)

    def test_api_or_git_errors_always_return_normal_replay(self):
        def unavailable(*args, **kwargs):
            raise subprocess.CalledProcessError(1, "gh", stderr="private API detail")
        result = reuse.decide(self.event, REPO, self.root, ENV, api=unavailable)
        self.assertFalse(result.reuse)
        self.assertNotIn("private", result.reason)
        with patch.object(reuse.subprocess, "run", side_effect=FileNotFoundError("git unavailable")):
            self.assertFalse(self.decide().reuse)

    def test_malformed_api_or_missing_job_logs_fail_closed(self):
        def malformed(*args, **kwargs):
            return "not paginated JSON"
        self.assertFalse(reuse.decide(self.event, REPO, self.root, ENV, api=malformed).reuse)
        real_api = self.api
        def missing_logs(root, endpoint, **kwargs):
            if kwargs.get("raw"):
                raise OSError("logs unavailable")
            return real_api(root, endpoint, **kwargs)
        self.assertFalse(reuse.decide(self.event, REPO, self.root, ENV, api=missing_logs).reuse)

    def test_cli_always_logs_one_fingerprint_and_safe_github_outputs(self):
        event_path = self.root / "event.json"
        event_path.write_text(json.dumps(self.event))
        output_path = self.root / "outputs"
        output = io.StringIO()
        with patch.object(reuse, "environment_fingerprint", return_value=ENV), \
             patch.object(reuse, "decide", return_value=reuse.Decision(False, "normal\nreplay", "\r\n")), \
             contextlib.redirect_stdout(output):
            code = reuse.main(["--event-path", str(event_path), "--repository", REPO,
                               "--event-name", "push", "--output", str(output_path)])
        self.assertEqual(code, 0)
        self.assertEqual(output.getvalue(), f"D0_REPLAY_ENV_SHA256={ENV}\n")
        self.assertEqual(output_path.read_text(), "reuse=false\nreason=normal replay\nrun_url=\n")

    def test_environment_hash_tracks_packages_python_and_image_without_paths(self):
        class Distribution:
            def __init__(self, name, version):
                self.metadata, self.version = {"Name": name}, version
        with patch.object(reuse.importlib.metadata, "distributions", return_value=[Distribution("a", "1")]), \
             patch.dict(os.environ, {"ImageOS": "ubuntu24", "ImageVersion": "one"}):
            first = reuse.environment_fingerprint()
            with patch.dict(os.environ, {"ImageVersion": "two"}):
                self.assertNotEqual(first, reuse.environment_fingerprint())
            with patch.object(reuse.sys, "version", "different Python"):
                self.assertNotEqual(first, reuse.environment_fingerprint())
            with patch.object(reuse.importlib.metadata, "distributions", return_value=[Distribution("a", "2")]):
                self.assertNotEqual(first, reuse.environment_fingerprint())


if __name__ == "__main__":
    unittest.main()
