#!/usr/bin/env python3
"""Validate the GitHub-first execution contract for task PRs.

Runtime truth:
- main/manifest is the queue/control plane;
- a Draft PR is an active execution;
- a ready PR is a review candidate and must be self-retiring;
- merge is completion;
- every PR is self-identifying without prior chat context.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
from typing import Any

REPO_SLUG = "gvakhrushev/d0_15"
TASK_RE = re.compile(r"(?mi)^Task:\s*`?([A-Z0-9][A-Z0-9_-]*)`?\s*$")
CLASS_RE = re.compile(r"(?mi)^Class:\s*`?(CONTROL|WORKER|EXPENSIVE)`?\s*$")
LIFECYCLE_RE = re.compile(r"(?mi)^Lifecycle:\s*`?(IN_PROGRESS|BLOCKED|REVIEW)`?\s*$")
BASELINE_RE = re.compile(r"(?mi)^Baseline:\s*`?([0-9a-fA-F]{7,40})`?\s*$")
REPOSITORY_RE = re.compile(r"(?mi)^Repository:\s*`?([^\n`]+)`?\s*$")
PRIMARY_RE = re.compile(r"(?mi)^Primary-Artifact:\s*`?([^\n`]+)`?\s*$")
CONTROL_PLANE = "CONTROL-PLANE"
PREFIX = {"WORKER": "wrk/", "EXPENSIVE": "exp/", "CONTROL": "control/"}


class ContractError(Exception):
    pass


def _one(regex: re.Pattern[str], body: str, label: str) -> str:
    hits = regex.findall(body or "")
    if len(hits) != 1:
        raise ContractError(f"PR body must contain exactly one '{label}: ...' line")
    return hits[0].strip()


def _git_is_ancestor(root: pathlib.Path, ancestor: str, descendant: str) -> bool:
    """Return true only when both commits exist and ancestor <= descendant."""
    if not ancestor or not descendant:
        return False
    exists = subprocess.run(
        ["git", "cat-file", "-e", f"{ancestor}^{{commit}}"],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if exists.returncode != 0:
        return False
    check = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return check.returncode == 0


def validate_event(event: dict[str, Any], root: pathlib.Path) -> None:
    pr = event.get("pull_request")
    if not isinstance(pr, dict):
        return

    body = pr.get("body") or ""
    repo_slug = _one(REPOSITORY_RE, body, "Repository")
    task_id = _one(TASK_RE, body, "Task")
    task_class = _one(CLASS_RE, body, "Class")
    lifecycle = _one(LIFECYCLE_RE, body, "Lifecycle")
    baseline = _one(BASELINE_RE, body, "Baseline")
    primary = _one(PRIMARY_RE, body, "Primary-Artifact")

    if repo_slug != REPO_SLUG:
        raise ContractError(f"Repository must be {REPO_SLUG}, got {repo_slug}")

    is_draft = bool(pr.get("draft", False))
    action = (event.get("action") or "").strip()
    base_sha = ((pr.get("base") or {}).get("sha") or "").strip()
    head_sha = ((pr.get("head") or {}).get("sha") or "").strip()
    baseline_matches_base = (
        not base_sha or baseline.lower() == base_sha.lower()
    )

    # A task is created from current main, so PR-open and Ready/REVIEW must
    # identify the current base exactly. During a long-lived Draft execution,
    # main may advance independently; keep the task-start baseline pinned as
    # long as it is still an ancestor of both current main and the task head.
    if base_sha and not baseline_matches_base:
        allow_pinned_draft_baseline = (
            is_draft
            and action != "opened"
            and _git_is_ancestor(root, baseline, base_sha)
            and (not head_sha or _git_is_ancestor(root, baseline, head_sha))
        )
        if not allow_pinned_draft_baseline:
            raise ContractError(
                "Baseline must equal PR base SHA at PR-open/Ready; on later "
                "Draft updates an older Baseline is allowed only when it is "
                f"an ancestor of both current base {base_sha} and head {head_sha}; "
                f"got {baseline}"
            )

    head_ref = ((pr.get("head") or {}).get("ref") or "").strip()
    prefix = PREFIX[task_class]
    if head_ref and not head_ref.startswith(prefix):
        raise ContractError(
            f"{task_class} PR head branch must start with '{prefix}', got {head_ref}"
        )

    if task_class in {"WORKER", "EXPENSIVE"}:
        if primary in {"", "N/A", "none", "None"}:
            raise ContractError(f"{task_class} PR requires a repo-relative Primary-Artifact")
        if primary.startswith(("http://", "https://")):
            raise ContractError("Primary-Artifact must be repo-relative, not a URL")

    number = pr.get("number") or event.get("number")
    if not number:
        raise ContractError("pull_request number missing from event")

    if task_id == CONTROL_PLANE:
        if task_class != "CONTROL":
            raise ContractError("CONTROL-PLANE PR must declare Class: CONTROL")
        if lifecycle != "REVIEW":
            raise ContractError("CONTROL-PLANE PR must declare Lifecycle: REVIEW")
        return

    manifest_path = root / "00_WORK" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    tasks = {t["id"]: t for t in manifest.get("tasks", []) if isinstance(t, dict) and t.get("id")}
    task = tasks.get(task_id)
    brief_path = root / "00_WORK" / "tasks" / f"{task_id}.md"

    if is_draft:
        if event.get("action") == "opened":
            head_sha = ((pr.get("head") or {}).get("sha") or "").strip()
            if base_sha and head_sha:
                diff = subprocess.run(
                    ["git", "diff", "--name-only", base_sha, head_sha],
                    cwd=root,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                allowed_open = {
                    "00_WORK/manifest.json",
                    "00_WORK/STATUS.md",
                    "README.md",
                }
                premature = [
                    p.strip()
                    for p in diff.stdout.splitlines()
                    if p.strip() and p.strip() not in allowed_open
                ]
                if premature:
                    raise ContractError(
                        "Draft PR must be opened before implementation/research work; "
                        f"premature files at open: {', '.join(premature)}"
                    )

        if lifecycle not in {"IN_PROGRESS", "BLOCKED"}:
            raise ContractError(
                f"draft PR #{number} must declare Lifecycle: IN_PROGRESS or BLOCKED, got {lifecycle}"
            )
        if task is None:
            raise ContractError(
                f"draft PR #{number} task {task_id} must still exist in head manifest"
            )
        if task.get("class") != task_class:
            raise ContractError(
                f"PR Class {task_class} disagrees with manifest class {task.get('class')} for {task_id}"
            )
        if task.get("state") != lifecycle:
            raise ContractError(
                f"draft PR lifecycle {lifecycle} disagrees with branch manifest state {task.get('state')}"
            )
        if not brief_path.is_file():
            raise ContractError(f"draft PR #{number} must retain task brief {brief_path.relative_to(root)}")
        return

    if lifecycle != "REVIEW":
        raise ContractError(f"ready PR #{number} must declare Lifecycle: REVIEW")

    if task_class in {"WORKER", "EXPENSIVE"}:
        if task is not None:
            raise ContractError(
                f"ready PR #{number} must self-retire {task_id} from 00_WORK/manifest.json before merge"
            )
        if brief_path.exists():
            raise ContractError(
                f"ready PR #{number} must delete task brief {brief_path.relative_to(root)} before merge"
            )
    elif task_class == "CONTROL":
        if task is None:
            raise ContractError(f"CONTROL PR task {task_id} must remain present in manifest")
        if task.get("class") != "CONTROL":
            raise ContractError(f"{task_id} is not a CONTROL task")


def self_test() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "00_WORK" / "tasks").mkdir(parents=True)
        task = {
            "id": "WRK-TEST-001",
            "class": "WORKER",
            "state": "IN_PROGRESS",
            "parent": "CTRL-TEST",
            "affected_claims": ["D0-X"],
            "exit_condition": "x",
            "brief": "00_WORK/tasks/WRK-TEST-001.md",
        }
        (root / "00_WORK" / "manifest.json").write_text(
            json.dumps({"tasks": [task]}), encoding="utf-8"
        )
        (root / "00_WORK" / "tasks" / "WRK-TEST-001.md").write_text("# task\n", encoding="utf-8")

        base = "a" * 40
        draft = {
            "number": 10,
            "pull_request": {
                "number": 10,
                "draft": True,
                "base": {"sha": base},
                "head": {"sha": "b" * 40, "ref": "wrk/test-001"},
                "body": (
                    f"Repository: `{REPO_SLUG}`\n"
                    "Task: `WRK-TEST-001`\n"
                    "Class: `WORKER`\n"
                    "Lifecycle: `IN_PROGRESS`\n"
                    f"Baseline: `{base}`\n"
                    "Primary-Artifact: `02_REGISTRY/research/certificates/test.py`\n"
                ),
            },
        }
        validate_event(draft, root)

        bad_repo = json.loads(json.dumps(draft))
        bad_repo["pull_request"]["body"] = bad_repo["pull_request"]["body"].replace(
            REPO_SLUG, "other/repo"
        )
        try:
            validate_event(bad_repo, root)
        except ContractError as exc:
            assert "Repository must be" in str(exc)
        else:
            raise AssertionError("wrong repository was not rejected")

        bad_branch = json.loads(json.dumps(draft))
        bad_branch["pull_request"]["head"]["ref"] = "exp/test-001"
        try:
            validate_event(bad_branch, root)
        except ContractError as exc:
            assert "branch must start" in str(exc)
        else:
            raise AssertionError("wrong branch prefix was not rejected")

        bad_base = json.loads(json.dumps(draft))
        bad_base["pull_request"]["body"] = bad_base["pull_request"]["body"].replace(
            base, "c" * 40
        )
        try:
            validate_event(bad_base, root)
        except ContractError as exc:
            assert "Baseline must equal" in str(exc)
        else:
            raise AssertionError("baseline mismatch was not rejected")

        ready = json.loads(json.dumps(draft))
        ready["pull_request"]["draft"] = False
        ready["pull_request"]["body"] = ready["pull_request"]["body"].replace(
            "IN_PROGRESS", "REVIEW"
        )
        try:
            validate_event(ready, root)
        except ContractError:
            pass
        else:
            raise AssertionError("ready executable PR must fail until task is self-retired")

        (root / "00_WORK" / "manifest.json").write_text(
            json.dumps({"tasks": []}), encoding="utf-8"
        )
        (root / "00_WORK" / "tasks" / "WRK-TEST-001.md").unlink()
        validate_event(ready, root)

        control = {
            "number": 11,
            "pull_request": {
                "number": 11,
                "draft": False,
                "base": {"sha": base},
                "head": {"sha": "d" * 40, "ref": "control/test"},
                "body": (
                    f"Repository: `{REPO_SLUG}`\n"
                    "Task: `CONTROL-PLANE`\n"
                    "Class: `CONTROL`\n"
                    "Lifecycle: `REVIEW`\n"
                    f"Baseline: `{base}`\n"
                    "Primary-Artifact: `N/A`\n"
                ),
            },
        }
        validate_event(control, root)

        # Long-lived Drafts keep their task-start baseline while main advances.
        # Build an actual tiny git history so the ancestor rule is exercised.
        (root / "00_WORK" / "manifest.json").write_text(
            json.dumps({"tasks": [task]}), encoding="utf-8"
        )
        (root / "00_WORK" / "tasks" / "WRK-TEST-001.md").write_text("# task\n", encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "self-test@example.invalid"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "self-test"], cwd=root, check=True)
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "task baseline"], cwd=root, check=True)
        pinned = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()

        (root / "main-advance.txt").write_text("main advanced\n", encoding="utf-8")
        subprocess.run(["git", "add", "main-advance.txt"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "advance main"], cwd=root, check=True)
        advanced_base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()

        subprocess.run(["git", "checkout", "-qb", "wrk/test-long", pinned], cwd=root, check=True)
        (root / "draft-work.txt").write_text("draft work\n", encoding="utf-8")
        subprocess.run(["git", "add", "draft-work.txt"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "draft work"], cwd=root, check=True)
        long_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()

        long_draft = json.loads(json.dumps(draft))
        long_draft["action"] = "synchronize"
        long_draft["pull_request"]["base"]["sha"] = advanced_base
        long_draft["pull_request"]["head"]["sha"] = long_head
        long_draft["pull_request"]["head"]["ref"] = "wrk/test-long"
        long_draft["pull_request"]["body"] = long_draft["pull_request"]["body"].replace(
            base, pinned
        )
        validate_event(long_draft, root)

        stale_ready = json.loads(json.dumps(long_draft))
        stale_ready["pull_request"]["draft"] = False
        stale_ready["pull_request"]["body"] = stale_ready["pull_request"]["body"].replace(
            "IN_PROGRESS", "REVIEW"
        )
        try:
            validate_event(stale_ready, root)
        except ContractError as exc:
            assert "Baseline must equal PR base SHA" in str(exc)
        else:
            raise AssertionError("Ready PR with stale pinned baseline was not rejected")

    print("PASS pr_contract self-test")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    event_name = os.environ.get("GITHUB_EVENT_NAME", "")
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if event_name != "pull_request" or not event_path:
        print("PASS pr_contract: non-pull-request event")
        return 0

    root = pathlib.Path(__file__).resolve().parents[1]
    event = json.loads(pathlib.Path(event_path).read_text(encoding="utf-8"))
    try:
        validate_event(event, root)
    except (ContractError, json.JSONDecodeError, OSError, subprocess.CalledProcessError) as exc:
        print(f"FAIL_PR_CONTRACT: {exc}", file=sys.stderr)
        return 1

    print("PASS pr_contract: GitHub-first lifecycle satisfied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
