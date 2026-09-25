#!/usr/bin/env python3
"""Generate a CI-compliant D0 executable task brief skeleton."""
from __future__ import annotations

import argparse
import pathlib
import sys

REPO = "gvakhrushev/d0_15"

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--class", dest="cls", choices=["WORKER", "EXPENSIVE"], required=True)
    ap.add_argument("--branch", required=True)
    ap.add_argument("--artifact", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--repo-root", type=pathlib.Path, default=None)
    args = ap.parse_args()

    prefix = "wrk/" if args.cls == "WORKER" else "exp/"
    if not args.branch.startswith(prefix):
        print(f"ERROR: {args.cls} branch must start with {prefix}", file=sys.stderr)
        return 2
    if len(args.why.strip()) < 40:
        print("ERROR: --why must explain why CONTROL should delegate this task", file=sys.stderr)
        return 2

    text = f"""# {args.id}
Repository: `{REPO}`
Base: `main`
Branch: `{args.branch}`
Primary artifact: `{args.artifact}`
Execution: `GitHub-first`

Class: `{args.cls}`
Parent: `CTRL-...`

## Why delegated

{args.why.strip()}

## GitHub execution contract

Branch from current main, run `python tools/task_lifecycle.py start {args.id}`,
open a Draft PR before substantive work, write the durable result directly to
the primary artifact, validate, retire the task in the same PR, and mark Ready
with `Lifecycle: REVIEW`.

## Objective

Replace this paragraph with the exact bounded objective.

## Required checks

Replace this section with positive checks and hostile negative controls.

## Scope guard

State what this task must not claim or modify.

## Exit condition

State one auditable completion condition.

## Chat handoff

Return only the PR number, verdict or PASS/FAIL, and one exact blocker if the
task cannot close. Do not paste the full durable artifact into chat.
"""

    if args.write:
        root = (args.repo_root or pathlib.Path(__file__).resolve().parents[1]).resolve()
        path = root / "00_WORK" / "tasks" / f"{args.id}.md"
        if path.exists():
            print(f"ERROR: refusing to overwrite {path}", file=sys.stderr)
            return 2
        path.write_text(text, encoding="utf-8")
        print(path.relative_to(root))
    else:
        print(text, end="")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
