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
