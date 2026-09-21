# Active Work Control Plane

This directory contains the active work and control scaffolding for the D0 research programme.

## Operating Flow

```text
CONTROL decides
→ EXPENSIVE/WORKER executes
→ task enters REVIEW
→ CONTROL accepts/rejects
→ accepted result distilled into Lean/cert/registry/books
→ task + brief deleted
```

## Rules of Operation

1. **Git history is the only archive.** There are no `done/`, `archive/`, or `history/` directories. Completed or abandoned tasks are deleted from `manifest.json` along with their task briefs in the integration commit.
2. **No completed task storage.** `manifest.json` admits only active states: `PLANNED`, `IN_PROGRESS`, `BLOCKED`, `REVIEW`.
3. **Hierarchy and delegation.** No agent or worker may create child work bypassing CONTROL. Every `EXPENSIVE` and `WORKER` task must have an immediate parent of class `CONTROL`.
4. **Claim discipline.** `affected_claims` for worker and expensive tasks must name existing claim IDs from `02_REGISTRY/claims.csv` or `02_REGISTRY/aliases.csv`. New claim IDs require a formal CONTROL decision; no automatic claim minting is permitted.
5. **Canonical shared state.** The authoritative shared state is the remote `origin/main` branch on GitHub.
6. **Generated status views.** The active task listing and status metrics are rendered deterministically into `00_WORK/STATUS.md` and `README.md` by `tools/render_work_status.py`. Do not edit generated status views manually.

## Worker Restart Discipline

1. **Only tasks in `IN_PROGRESS` may be executed.** `PLANNED` is a queue, not authorization.
2. **One ordinary worker task at a time by default.** Finish it to a green PR and `REVIEW`, then stop for CONTROL.
3. **Fresh branch from current `origin/main`.** A stale local branch, dirty tree, old olean cache, or closed PR is never the execution baseline.
4. **Remote CI is acceptance truth.** Local build output is supporting evidence only; GitHub `D0 Lean build` and `D0 guards` must be green.
5. **No autonomous queue advance.** The worker must not start the next PLANNED task after opening a PR.
6. **Closed failed PRs stay closed.** Git history is reference material, not a branch to repair unless CONTROL explicitly says otherwise.
