# Lean Deferred Run Policy

Purpose: keep Lean useful without letting every theory/code edit block for
20--40 minutes or inflate the repository.

## Storage

Use `tools/lean_dev.ps1` from the repository root. It keeps
`09_LEAN_FORMALIZATION/.lake` as a Windows junction to external storage:

```text
$HOME/.d0_lean_cache/D0_v14/09_LEAN_FORMALIZATION/.lake
```

The repository may contain only the junction, never a real in-project `.lake`
tree. Check with:

```powershell
.\tools\check_lean_storage_hygiene.ps1
```

## Development Loop

During theory/code editing:

```text
edit books / Lean sources / certs
run fast Python guards and text audits
record the touched Lean targets
do not run lake build on every small edit
```

Lean is run in a deferred verification phase after a coherent batch of edits.

## Deferred Lean Phase

Run targets from narrow to broad:

```powershell
.\tools\lean_dev.ps1 build D0.<TouchedModule>
.\tools\lean_dev.ps1 build D0.TheoremLedger.<TouchedIndex>
.\tools\lean_dev.ps1 build D0.All
```

If a build fails, fix the reported Lean errors and rerun only the narrow failed
target first. Full `D0.All` is a release/checkpoint gate, not the normal edit
loop.

## Current Rule

Do not start a long Lean build unless the task is explicitly in the deferred
Lean phase. For ordinary corpus integration, use fast guards first and leave
Lean errors as queued verification work.
