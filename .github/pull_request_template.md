Task: `TASK-ID`
Class: `WORKER|EXPENSIVE|CONTROL`
Lifecycle: `IN_PROGRESS|BLOCKED|REVIEW`
Baseline: `MAIN-SHA`

## Scope

Briefly state what this PR owns and what it explicitly does not own.

## Primary artifact

For `EXPENSIVE`, name the durable research memo/certificate path written by this PR.
For `WORKER`, name the implementation/certificate/formalization path(s) owned by this PR.

## Validation

List narrow validation while iterating. A ready Lean PR must include one final
`python tools/lean_task_build.py final` result plus the required guards.

## Handoff

For executable WORKER/EXPENSIVE PRs:
- open as **Draft** before source/research work starts;
- keep the branch task state equal to the draft lifecycle;
- before marking Ready, retire the task from `00_WORK/manifest.json`, delete its
  brief, regenerate status views, and set `Lifecycle: REVIEW`;
- do not report the task complete until this PR is merged.
