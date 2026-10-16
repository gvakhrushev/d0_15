#!/usr/bin/env python3
"""Fail-closed reuse of a prior Ready research replay after three allowed docs.

No result cache is created. Evidence is an actual successful guards job and
research step in the latest run at the exact previous PR head, same recorded
base, with the same scientific environment fingerprint in its job log.
Every missing/invalid input falls back to the normal replay, never a red gate.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ALLOWED_DOCS = {"README.md", "AGENTS.md", "00_WORK/README.md"}
WORKFLOW = ".github/workflows/guards.yml"
RESEARCH_STEP = "Replay research certificates in isolated worktrees"
SHA = re.compile(r"[0-9a-f]{40}")
MARKER = re.compile(
    r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z[ \t]+"
    r"D0_REPLAY_ENV_SHA256=([0-9a-f]{64})$", re.MULTILINE)


@dataclass(frozen=True)
class Decision:
    reuse: bool
    reason: str
    run_url: str = ""


def environment_fingerprint() -> str:
    """Hash versions/image identity only: no paths, package list or secrets log."""
    distributions = sorted((str(d.metadata["Name"]), str(d.version))
                           for d in importlib.metadata.distributions())
    data = {"python": sys.version, "ImageOS": os.environ.get("ImageOS", ""),
            "ImageVersion": os.environ.get("ImageVersion", ""),
            "distributions": distributions}
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def github_api(root: Path, endpoint: str, *, paginate=False, raw=False):
    command = ["gh", "api", "--hostname", "github.com", "--method", "GET"]
    if paginate:
        command += ["--paginate", "--slurp"]
    result = subprocess.run(command + [endpoint], cwd=root, check=True,
                            capture_output=True, text=True, timeout=45)
    return result.stdout if raw else json.loads(result.stdout)


def page_items(pages, key):
    if not isinstance(pages, list) or not pages:
        raise ValueError("missing paginated API evidence")
    values = []
    for page in pages:
        if not isinstance(page, dict) or not isinstance(page.get(key), list):
            raise ValueError("invalid paginated API evidence")
        values.extend(page[key])
    if any(not isinstance(value, dict) for value in values):
        raise ValueError("invalid API object")
    return values


def decide(event, repository: str, root: Path, environment_sha: str,
           *, event_name="pull_request", api=github_api) -> Decision:
    """Read-only decision. A false result means perform the normal replay."""
    try:
        pr = event.get("pull_request", {})
        if (event_name != "pull_request" or event.get("action") != "synchronize"
                or pr.get("draft") is not False or pr.get("state") != "open"):
            return Decision(False, "only Ready pull_request synchronize is eligible")
        before, current, base = event.get("before", ""), pr["head"]["sha"], pr["base"]["sha"]
        if any(not isinstance(x, str) or not SHA.fullmatch(x) or x == "0" * 40
               for x in (before, current, base)) or before == current:
            return Decision(False, "missing or invalid previous/current/base head")
        number, branch, base_branch = pr["number"], pr["head"]["ref"], pr["base"]["ref"]
        head_repo = pr["head"]["repo"]["full_name"]
        if (not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository)
                or event["repository"]["full_name"] != repository
                or pr["base"]["repo"]["full_name"] != repository
                or type(number) is not int or number != event.get("number")
                or not isinstance(branch, str) or not branch
                or not isinstance(base_branch, str) or not base_branch
                or not isinstance(head_repo, str) or not head_repo
                or not re.fullmatch(r"[0-9a-f]{64}", environment_sha)):
            return Decision(False, "inconsistent event/repository identity")
        tracked = subprocess.run(["git", "status", "--porcelain=v1", "--untracked-files=no"],
                                 cwd=root, check=True, capture_output=True, timeout=15)
        if tracked.stdout:
            return Decision(False, "tracked checkout/index changed after the committed snapshot")
        trees = subprocess.run(["git", "rev-parse", "HEAD^{tree}", f"{current}^{{tree}}"],
                               cwd=root, check=True, capture_output=True, timeout=15).stdout.splitlines()
        if len(trees) != 2 or trees[0] != trees[1]:
            return Decision(False, "checked tree is not the current PR head tree")
        # Both heads must contain the current base. A force-pushed, older fork
        # can have a docs-only head tree diff yet a different synthetic merge.
        for head in (before, current):
            ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", base, head],
                                      cwd=root, capture_output=True, timeout=15)
            if ancestor.returncode != 0:
                return Decision(False, "current PR base is not a verified ancestor of both heads")
        diff = subprocess.run(["git", "diff", "--no-renames", "--name-only", "-z", before, current, "--"],
                              cwd=root, check=True, capture_output=True, timeout=15)
        paths = {os.fsdecode(p) for p in diff.stdout.split(b"\0") if p}
        if not paths or not paths <= ALLOWED_DOCS:
            return Decision(False, "changed paths include inputs outside the three allowed docs")

        runs = page_items(api(root, f"repos/{repository}/actions/workflows/guards.yml/runs"
                              f"?event=pull_request&head_sha={before}&per_page=100", paginate=True), "workflow_runs")
        if not runs or any(type(run.get("id")) is not int for run in runs):
            return Decision(False, "no complete previous-head workflow evidence")
        # A failed/cancelled latest run must not be hidden by an older success.
        run = max(runs, key=lambda item: item["id"])
        refs = run.get("pull_requests", [])
        if not isinstance(refs, list) or len(refs) != 1 or not isinstance(refs[0], dict):
            return Decision(False, "run has missing or ambiguous PR evidence")
        ref = refs[0]
        attempt = run.get("run_attempt")
        repo_url = f"https://api.github.com/repos/{repository}"
        head_repo_url = f"https://api.github.com/repos/{head_repo}"
        if (run.get("name") != "D0 guards" or run.get("path") != WORKFLOW
                or run.get("head_sha") != before or run.get("head_branch") != branch
                or run.get("event") != "pull_request" or run.get("status") != "completed"
                or run.get("conclusion") != "success"
                or run.get("repository", {}).get("full_name") != repository
                or run.get("head_repository", {}).get("full_name") != head_repo
                or type(attempt) is not int or attempt < 1
                or ref.get("number") != number
                or ref.get("url") != f"{repo_url}/pulls/{number}"
                or ref.get("base", {}).get("sha") != base
                or ref.get("base", {}).get("ref") != base_branch
                or ref.get("base", {}).get("repo", {}).get("url") != repo_url
                or ref.get("head", {}).get("sha") != before
                or ref.get("head", {}).get("ref") != branch
                or ref.get("head", {}).get("repo", {}).get("url") != head_repo_url):
            return Decision(False, "latest run does not prove the same successful PR/base/workflow")
        jobs = page_items(api(root, f"repos/{repository}/actions/runs/{run['id']}/attempts/{attempt}/jobs"
                                  "?per_page=100", paginate=True), "jobs")
        matches = [job for job in jobs if job.get("name") == "guards"]
        if len(matches) != 1:
            return Decision(False, "missing or ambiguous guards job")
        job = matches[0]
        steps = job.get("steps", [])
        research = [step for step in steps if isinstance(step, dict) and step.get("name") == RESEARCH_STEP]
        if (type(job.get("id")) is not int or job.get("run_id") != run["id"]
                or job.get("run_attempt") != attempt or job.get("status") != "completed"
                or job.get("conclusion") != "success" or len(research) != 1
                or research[0].get("status") != "completed" or research[0].get("conclusion") != "success"):
            return Decision(False, "guards job/research step did not actually succeed in that attempt")
        logs = api(root, f"repos/{repository}/actions/jobs/{job['id']}/logs", raw=True)
        markers = MARKER.findall(logs.replace("\r\n", "\n"))
        if len(markers) != 1 or markers[0] != environment_sha:
            return Decision(False, "missing, ambiguous or changed scientific environment")
        return Decision(True, "same base and scientific environment; only three allowed docs changed",
                        f"https://github.com/{repository}/actions/runs/{run['id']}/attempts/{attempt}")
    except Exception as error:
        # API/git/log availability is an optimization input, never a new gate.
        return Decision(False, f"replay evidence unavailable or invalid ({type(error).__name__})")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event-path", type=Path, default=os.environ.get("GITHUB_EVENT_PATH"))
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY", ""))
    parser.add_argument("--event-name", default=os.environ.get("GITHUB_EVENT_NAME", ""))
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, help="append GitHub step outputs; stdout when omitted")
    args = parser.parse_args(argv)
    try:
        fingerprint = environment_fingerprint()
    except Exception:
        fingerprint = hashlib.sha256(b"ENVIRONMENT_FINGERPRINT_UNAVAILABLE").hexdigest()
        decision = Decision(False, "scientific environment fingerprint unavailable")
    else:
        try:
            event = json.loads(Path(args.event_path).read_text())
            decision = decide(event, args.repository, args.repo_root, fingerprint, event_name=args.event_name)
        except Exception as error:
            decision = Decision(False, f"event evidence unavailable or invalid ({type(error).__name__})")
    print(f"D0_REPLAY_ENV_SHA256={fingerprint}")
    reason = " ".join(str(decision.reason).split())
    run_url = " ".join(str(decision.run_url).split())
    output = (f"reuse={str(decision.reuse).lower()}\nreason={reason}\n"
              f"run_url={run_url}\n")
    if args.output is None:
        print(output, end="")
    else:
        try:
            with args.output.open("a", encoding="utf-8") as stream:
                stream.write(output)
        except OSError:
            # A missing output is treated as false by the workflow condition.
            print("reuse=false\nreason=GitHub output unavailable\nrun_url=")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
