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

    assembly_line = f"Assembly: `{args.id}`\n" if "A4D" in args.id else ""

    text = f"""# {args.id}
Repository: `{REPO}`
Base: `main`
Branch: `{args.branch}`
Primary artifact: `{args.artifact}`
Execution: `GitHub-first`
{assembly_line}

Class: `{args.cls}`
Parent: `CTRL-...`

## Why delegated

{args.why.strip()}

## GitHub execution contract

Read `AGENTS.md`, `00_WORK/README.md` and the
[prospective-minimality programme](../../02_REGISTRY/research/MEMO_A4D_RESOLVED_AFFINE_PROGRAM.md#prospective-minimality-and-physical-execution),
then only the assigned premise's relevant inputs.

Branch from current main, run `python tools/task_lifecycle.py start {args.id}`,
open a Draft PR before substantive work, write the durable result directly to
the primary artifact, validate, retire the task in the same PR, and mark Ready
with `Lifecycle: REVIEW`.

## Objective

State the exact missing transition in the existing parent argument and the
result that supplies it. Reuse owned results; keep their remaining hypotheses
explicit. Place this work in verification kernel, theory transfer, native
realization or final composition.

## Parent proof interface

- Statement and remaining assumptions: exact conclusion and quantifiers.
- Input owners and fixed refs: distinguish accepted main from research inputs;
  name what is reused and the changed input if an owned proof must be repeated.
- Common objects: carrier, full action, norm, source/comparator, preparation,
  retained history/clock and refinement maps. For minimality work fix the
  admissible alternatives and task, generator, price and physical selection law.
- Consumer: exact parent premise and substitution location; for a supporting
  result, state the application or transport that remains to be proved.
- Write paths: disjoint artifact paths owned by this execution.
- Decisive check: smallest proof/calculation and relevant negative control;
  prefer a structural inequality, invariant or classification before a census.
- For gravity work: register this Assembly binding in gr_assembly/contract.json;
  distinguish start prerequisites from retained proof assumptions, and reuse
  `python tools/gr_assembly.py template {args.id}` for the result application.

## Required checks

Name the narrow iteration check and the affected integration checks at Ready.
Do not require a corpus-wide replay for each local edit.

## Scope guard

State what this task must not claim or modify.
Keep any assumed optimum or physical selector explicit; prove its native
origin before claiming that D0 determines execution. Minimum gate count alone
does not identify the full Cost-Info action.

## Exit condition

State one auditable completion condition.

## Chat handoff

Return the PR number, exact conclusion and consumed parent premise (or missing
application/changed route), checks, and one exact blocker if the task cannot
close. Keep the handoff short; do not paste the full durable artifact into chat.
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
