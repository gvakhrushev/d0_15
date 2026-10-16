#!/usr/bin/env python3
"""Focused dispatch regressions; all GitHub calls are mocked and read-only."""
from __future__ import annotations

import contextlib
import io
import json
import pathlib
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import task_dispatch as dispatch

TASK = "EXP-TEST-001"
BRANCH = "exp/test-001"


def pr(number=12, task=TASK, lifecycle="IN_PROGRESS", draft=True, branch=BRANCH):
    return {
        "number": number, "state": "open", "html_url": f"https://github.com/{dispatch.REPO}/pull/{number}",
        "body": (f"Task: `{task}`\n" if task else "") + f"Lifecycle: `{lifecycle}`\n",
        "draft": draft, "head": {"ref": branch, "sha": "a" * 40},
    }


class DispatchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        (self.root / "00_WORK/tasks").mkdir(parents=True)
        self.queue()
        (self.root / f"00_WORK/tasks/{TASK}.md").write_text(
            f"Base: `main`\nBranch: `{BRANCH}`\nPrimary artifact: `memo.md`\n", encoding="utf-8",
        )

    def queue(self, state="PLANNED", present=True):
        tasks = [{"id": TASK, "class": "EXPENSIVE", "state": state,
                  "brief": f"00_WORK/tasks/{TASK}.md"}] if present else []
        (self.root / "00_WORK/manifest.json").write_text(json.dumps({"tasks": tasks}), encoding="utf-8")

    def run_dispatch(self, pages=None, extra=(), error=None, raw=None):
        result = subprocess.CompletedProcess([], 0, stdout=raw if raw is not None else json.dumps(pages or [[]]))
        out, err = io.StringIO(), io.StringIO()
        with patch.object(dispatch.subprocess, "run", return_value=result, side_effect=error) as gh:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = dispatch.main([TASK, "--repo-root", str(self.root), *extra])
        return code, out.getvalue(), err.getvalue(), gh

    def test_new_launch_requires_successful_lookup_and_planned_queue(self):
        code, out, err, gh = self.run_dispatch()
        self.assertEqual((code, err), (0, ""))
        self.assertIn("Open execution: none (GitHub checked)", out)
        self.assertIn("open the Draft PR", out)
        command = gh.call_args.args[0]
        self.assertIn("--paginate", command)
        self.assertIn("--slurp", command)
        self.assertEqual(command[command.index("--method") + 1], "GET")
        self.assertEqual(gh.call_args.kwargs["cwd"], self.root.resolve())

    def test_exact_metadata_resumes_pr_on_later_page_with_different_branch(self):
        unrelated = pr(task=TASK + "-OTHER", branch="exp/other")
        code, out, err, _ = self.run_dispatch([[unrelated], [pr(branch="exp/existing")]])
        self.assertEqual((code, err), (0, ""))
        self.assertIn("PR: #12", out)
        self.assertIn("Head: exp/existing @ " + "a" * 40, out)
        self.assertIn("Resume this PR", out)
        self.assertNotIn("open the Draft PR", out)

    def test_existing_pr_is_found_after_queue_and_brief_retirement(self):
        self.queue(present=False)
        (self.root / f"00_WORK/tasks/{TASK}.md").unlink()
        code, out, err, _ = self.run_dispatch([[pr(draft=False, lifecycle="REVIEW")]])
        self.assertEqual((code, err), (0, ""))
        self.assertIn("Status: READY; Lifecycle: REVIEW", out)
        self.assertIn("Continue review", out)
        self.assertNotIn("Resume this PR", out)

    def test_crlf_pr_metadata_is_resolved_without_branch_or_queue(self):
        self.queue(present=False)
        candidate = pr(branch="exp/existing")
        candidate["body"] = candidate["body"].replace("\n", "\r\n")
        code, out, err, _ = self.run_dispatch([[candidate]])
        self.assertEqual((code, err), (0, ""))
        self.assertIn("PR: #12", out)
        self.assertIn("Lifecycle: IN_PROGRESS", out)

    def test_blocked_execution_requires_existing_blocker_resolution(self):
        code, out, err, _ = self.run_dispatch([[pr(lifecycle="BLOCKED")]])
        self.assertEqual((code, err), (0, ""))
        self.assertIn("Resolve the blocker in this PR", out)

    def test_lifecycle_mismatch_does_not_restart_research(self):
        code, out, err, _ = self.run_dispatch([[pr(draft=False)]])
        self.assertEqual((code, err), (0, ""))
        self.assertIn("Inspect/fix this PR's lifecycle", out)
        self.assertNotIn("Resume this PR", out)

    def test_multiple_exact_executions_fail_without_launch(self):
        code, out, err, _ = self.run_dispatch([[pr(), pr(number=13)]])
        self.assertEqual(code, 2)
        self.assertIn("ambiguous open execution", err)
        self.assertIn("#12, #13", err)
        self.assertNotIn("Execute GitHub-first", out)

    def test_repeated_task_metadata_is_not_a_safe_match(self):
        candidate = pr()
        candidate["body"] += f"Task: `{TASK}`\n"
        code, out, err, _ = self.run_dispatch([[candidate]])
        self.assertEqual(code, 2)
        self.assertIn("ambiguous Task metadata", err)
        self.assertNotIn("Execute GitHub-first", out)

    def test_branch_fallback_resumes_legacy_pr_without_task_metadata(self):
        code, out, err, _ = self.run_dispatch([[pr(task=None)]])
        self.assertEqual((code, err), (0, ""))
        self.assertIn("branch fallback; Task metadata missing", out)
        self.assertIn("Resume this PR", out)

    def test_conflicting_task_metadata_on_queued_branch_blocks_new_execution(self):
        code, out, err, _ = self.run_dispatch([[pr(task="EXP-OTHER")]])
        self.assertEqual(code, 2)
        self.assertIn("conflicting Task metadata", err)
        self.assertNotIn("Execute GitHub-first", out)

    def test_task_mentions_in_prose_or_title_are_not_task_metadata(self):
        candidate = pr(task="EXP-OTHER", branch="exp/other")
        candidate["title"] = TASK
        candidate["body"] += f"Depends on {TASK}.\nTask: `{TASK}-LONGER`\n"
        code, out, err, _ = self.run_dispatch([[candidate]])
        self.assertEqual((code, err), (0, ""))
        self.assertIn("Open execution: none", out)

    def test_lookup_failures_never_print_launch(self):
        errors = [FileNotFoundError("gh unavailable"), subprocess.TimeoutExpired("gh", 30),
                  subprocess.CalledProcessError(1, "gh", stderr="authentication required\nmore detail")]
        for error in errors:
            with self.subTest(error=error):
                code, out, err, _ = self.run_dispatch(error=error)
                self.assertEqual(code, 2)
                self.assertIn("GitHub open-PR lookup unavailable", err)
                self.assertIn("No launch authorized", err)
                self.assertNotIn("Execute GitHub-first", out)

    def test_invalid_github_response_fails_closed(self):
        for raw in ["not json", "[]", "{}", '[{"number":12}]', '[[{"state":"closed"}]]',
                    '[[{"state":"open","body":""}]]']:
            with self.subTest(raw=raw):
                code, out, err, _ = self.run_dispatch(raw=raw)
                self.assertEqual(code, 2)
                self.assertIn("Invalid GitHub PR response", err)
                self.assertNotIn("Execute GitHub-first", out)

    def test_multiple_legacy_prs_on_queued_branch_are_ambiguous(self):
        code, out, err, _ = self.run_dispatch([[pr(task=None), pr(number=13, task=None)]])
        self.assertEqual(code, 2)
        self.assertIn("ambiguous open execution", err)
        self.assertNotIn("Execute GitHub-first", out)

    def test_offline_is_explicitly_unverified_and_never_calls_github(self):
        code, out, err, gh = self.run_dispatch(extra=("--offline",))
        self.assertEqual((code, err), (0, ""))
        gh.assert_not_called()
        self.assertIn("GitHub status: UNVERIFIED", out)
        self.assertIn("no launch authorized", out)
        self.assertNotIn("Execute GitHub-first", out)

    def test_absent_queue_without_execution_is_not_launchable(self):
        self.queue(present=False)
        code, out, err, _ = self.run_dispatch()
        self.assertEqual(code, 2)
        self.assertIn("not in the local queue; no open execution found", err)
        self.assertNotIn("Execute GitHub-first", out)

    def test_absent_queue_offline_does_not_claim_no_execution_exists(self):
        self.queue(present=False)
        code, out, err, gh = self.run_dispatch(extra=("--offline",))
        self.assertEqual(code, 2)
        gh.assert_not_called()
        self.assertIn("GitHub status UNVERIFIED", err)
        self.assertNotIn("no open execution found", err)

    def test_nonplanned_queue_without_pr_requires_reconciliation(self):
        self.queue(state="IN_PROGRESS")
        code, out, err, _ = self.run_dispatch()
        self.assertEqual(code, 2)
        self.assertIn("reconcile before launching", err)
        self.assertNotIn("Execute GitHub-first", out)


if __name__ == "__main__":
    unittest.main()
