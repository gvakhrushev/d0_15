#!/usr/bin/env python3
"""Deterministic branch-local task lifecycle transitions.

main keeps queued PLANNED executable tasks. An execution branch uses:
  start  -> IN_PROGRESS
  block  -> BLOCKED
  resume -> IN_PROGRESS
  retire -> remove executable task + brief before Ready PR

Every transition regenerates 00_WORK/STATUS.md and the README status block.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

from render_work_status import generate_views

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "00_WORK" / "manifest.json"


class LifecycleError(Exception):
    pass


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def write_manifest(manifest: dict) -> None:
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def render_views() -> None:
    status_text, readme_text, status_path, readme_path = generate_views(ROOT)
    status_path.write_text(status_text, encoding="utf-8")
    readme_path.write_text(readme_text, encoding="utf-8")


def find_task(manifest: dict, task_id: str) -> dict:
    hits = [t for t in manifest.get("tasks", []) if t.get("id") == task_id]
    if len(hits) != 1:
        raise LifecycleError(f"expected exactly one task {task_id}, found {len(hits)}")
    return hits[0]


def transition(task_id: str, action: str) -> None:
    manifest = load_manifest()
    task = find_task(manifest, task_id)
    cls = task.get("class")
    state = task.get("state")

    if cls not in {"WORKER", "EXPENSIVE"}:
        raise LifecycleError(
            f"{task_id} is class {cls}; this helper only manages executable WORKER/EXPENSIVE tasks"
        )

    if action == "start":
        if state != "PLANNED":
            raise LifecycleError(f"start requires PLANNED, got {state}")
        if "A4D" in task_id or (ROOT / "02_REGISTRY/gr_assembly/contract.json").is_file():
            import gr_assembly
            import task_dispatch
            try:
                model = gr_assembly.load(ROOT)
                if task_id in model["contract"]["task_bindings"] or "A4D" in task_id:
                    gr_assembly.brief_binding(ROOT, task, model)
                    prs = task_dispatch.open_prs(ROOT)
                    branch = task_dispatch.field((ROOT / task["brief"]).read_text(), "Branch")
                    existing, _ = task_dispatch.existing_execution(prs, task_id, branch)
                    if existing:
                        raise LifecycleError(f"existing execution #{existing['number']}; resume its owner instead of starting")
                    check = gr_assembly.launch_check(model, task_id, prs)
                    if not check["allowed"]:
                        raise LifecycleError("assembly start gate: " + "; ".join(check["reasons"]))
            except (ValueError, KeyError, TypeError) as exc:
                raise LifecycleError(str(exc)) from exc
        task["state"] = "IN_PROGRESS"

    elif action == "block":
        if state != "IN_PROGRESS":
            raise LifecycleError(f"block requires IN_PROGRESS, got {state}")
        task["state"] = "BLOCKED"

    elif action == "resume":
        if state != "BLOCKED":
            raise LifecycleError(f"resume requires BLOCKED, got {state}")
        task["state"] = "IN_PROGRESS"

    elif action == "retire":
        if state != "IN_PROGRESS":
            raise LifecycleError(f"retire requires IN_PROGRESS after all blockers are cleared, got {state}")
        if (ROOT / "02_REGISTRY/gr_assembly/contract.json").is_file() or "A4D" in task_id:
            import gr_assembly
            try:
                gr_assembly.retirement_check(gr_assembly.load(ROOT), task_id)
            except (ValueError, KeyError, TypeError) as exc:
                raise LifecycleError(str(exc)) from exc
        brief = task.get("brief")
        if not isinstance(brief, str) or not brief:
            raise LifecycleError(f"{task_id} has no owned brief")
        brief_path = ROOT / brief
        manifest["tasks"] = [t for t in manifest.get("tasks", []) if t.get("id") != task_id]
        write_manifest(manifest)
        if brief_path.exists():
            brief_path.unlink()
        render_views()
        print(f"RETIRED {task_id}; ready PR must declare Lifecycle: REVIEW")
        return

    write_manifest(manifest)
    render_views()
    print(f"{task_id}: {state} -> {task['state']}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["start", "block", "resume", "retire"])
    ap.add_argument("task_id")
    args = ap.parse_args()
    try:
        transition(args.task_id, args.action)
    except (LifecycleError, OSError, json.JSONDecodeError) as exc:
        print(f"FAIL_TASK_LIFECYCLE: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
