#!/usr/bin/env python3
"""Print a portable, self-contained launch message for a queued D0 task."""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

REPO = "gvakhrushev/d0_15"

def field(text: str, name: str) -> str:
    m = re.search(rf"(?mi)^{re.escape(name)}:\s*`?([^\n`]+)`?\s*$", text)
    if not m:
        raise ValueError(f"brief missing '{name}: ...'")
    return m.group(1).strip()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("task_id")
    ap.add_argument("--repo-root", type=pathlib.Path, default=None)
    args = ap.parse_args()
    root = (args.repo_root or pathlib.Path(__file__).resolve().parents[1]).resolve()

    manifest = json.loads((root / "00_WORK" / "manifest.json").read_text(encoding="utf-8"))
    task = next((t for t in manifest.get("tasks", []) if t.get("id") == args.task_id), None)
    if task is None:
        print(
            f"ERROR: {args.task_id} is not queued on main. Check open PRs before creating a duplicate.",
            file=sys.stderr,
        )
        return 2

    brief_path = root / task["brief"]
    text = brief_path.read_text(encoding="utf-8")
    branch = field(text, "Branch")
    artifact = field(text, "Primary artifact")

    print(f"Repository: {REPO}")
    print(f"Task: {args.task_id}")
    print(f"Class: {task['class']}")
    print(f"Base: main")
    print(f"Brief: {task['brief']}")
    print(f"Branch: {branch}")
    print(f"Primary artifact: {artifact}")
    print("Execute GitHub-first: read the brief from main, open the Draft PR before substantive work,")
    print("write the durable result directly to the PR, and return only PR + verdict/PASS-FAIL + blocker.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
