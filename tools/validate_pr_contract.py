#!/usr/bin/env python3
"""Validate the GitHub-first execution contract for task PRs.

Runtime truth:
- main/manifest is the queue/control plane;
- a DRAFT PR is an active execution;
- a ready PR is a review candidate and must be self-retiring;
- merge is completion.

Every executable PR names exactly one canonical task in its body.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sys
import tempfile
from typing import Any

TASK_RE = re.compile(r"(?mi)^Task:\s*`?([A-Z0-9][A-Z0-9_-]*)`?\s*$")
CLASS_RE = re.compile(r"(?mi)^Class:\s*`?(CONTROL|WORKER|EXPENSIVE)`?\s*$")
LIFECYCLE_RE = re.compile(r"(?mi)^Lifecycle:\s*`?(IN_PROGRESS|BLOCKED|REVIEW)`?\s*$")
BASELINE_RE = re.compile(r"(?mi)^Baseline:\s*`?([0-9a-fA-F]{7,40})`?\s*$")
CONTROL_PLANE = "CONTROL-PLANE"


class ContractError(Exception):
    pass


def _one(regex: re.Pattern[str], body: str, label: str) -> str:
    hits = regex.findall(body or "")
    if len(hits) != 1:
        raise ContractError(f"PR body must contain exactly one '{label}: ...' line")
    return hits[0]


def validate_event(event: dict[str, Any], root: pathlib.Path) -> None:
    pr = event.get("pull_request")
    if not isinstance(pr, dict):
        return

    body = pr.get("body") or ""
    task_id = _one(TASK_RE, body, "Task")
    task_class = _one(CLASS_RE, body, "Class")
    lifecycle = _one(LIFECYCLE_RE, body, "Lifecycle")
    _one(BASELINE_RE, body, "Baseline")

    is_draft = bool(pr.get("draft", False))
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
        draft = {
            "number": 10,
            "pull_request": {
                "number": 10,
                "draft": True,
                "body": "Task: `WRK-TEST-001`\nClass: `WORKER`\nLifecycle: `IN_PROGRESS`\nBaseline: `abcdef1`\n",
            },
        }
        validate_event(draft, root)

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
                "body": "Task: `CONTROL-PLANE`\nClass: `CONTROL`\nLifecycle: `REVIEW`\nBaseline: `abcdef1`\n",
            },
        }
        validate_event(control, root)

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
    except (ContractError, json.JSONDecodeError, OSError) as exc:
        print(f"FAIL_PR_CONTRACT: {exc}", file=sys.stderr)
        return 1

    print("PASS pr_contract: GitHub-first lifecycle satisfied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
