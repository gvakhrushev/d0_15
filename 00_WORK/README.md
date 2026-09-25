# Active Work Control Plane

This directory contains the queue/control scaffolding for the D0 research programme.
**GitHub pull requests are the runtime execution plane.**

## GitHub-first execution model

```text
main task brief = queued work
→ create fresh remote branch from current main
→ first branch commit: task state PLANNED → IN_PROGRESS
→ open Draft PR before implementation/research begins
→ work only inside that PR/branch
→ final validation
→ same PR retires task + deletes brief + regenerates views
→ mark PR Ready with Lifecycle: REVIEW
→ CONTROL reviews and merges
→ merge = completion
```

The semantic task ID (for example `WRK-A4D-OBSERVER-FRAME-CAR-LIFT`) names the
research/formalization obligation. The **operational work number is the GitHub PR
number**. Do not call executions “worker 1”, “worker 2”, etc.; say “PR #87” or
“PR #86”. WORKER and EXPENSIVE use the same PR lifecycle.

## Source of truth

1. **GitHub first.** No local implementation/research work starts before a Draft
   PR exists remotely. A local worktree is only an execution workspace for an
   already-open task PR. On the execution branch use
   `python tools/task_lifecycle.py start TASK-ID` before opening the Draft PR.
2. **Runtime status is the PR.**
   - Draft PR + `Lifecycle: IN_PROGRESS` = executing.
   - Draft PR + `Lifecycle: BLOCKED` = blocked, with blocker stated in the PR.
   - Ready PR + `Lifecycle: REVIEW` = waiting for CONTROL acceptance.
   - Merged PR = complete.
3. **`main` manifest is the queue/control plane.** A PLANNED executable task on
   main is available work, not an active execution. Branch-local manifest state
   records the draft lifecycle.
4. **Git history is the only archive.** Completed/abandoned executable tasks are
   not stored under `00_WORK`; accepted PRs retire themselves before merge.
5. **No “done but PR open”.** An agent may report “ready for review”, but the task
   is not complete until the PR is merged.
6. **CONTROL owns acceptance.** Executors do not silently self-merge around a
   blocking review. CONTROL either merges the accepted PR or leaves an explicit
   blocking comment.
7. **No post-merge lifecycle cleanup PR for ordinary tasks.** WORKER/EXPENSIVE
   PRs run `python tools/task_lifecycle.py retire TASK-ID` before becoming Ready.
   That removes the manifest row + brief and regenerates status views in the same
   PR, making merge atomic with lifecycle completion.

## PR contract

Every task PR body uses `.github/pull_request_template.md` and contains exactly:

```text
Task: `TASK-ID`
Class: `WORKER|EXPENSIVE|CONTROL`
Lifecycle: `IN_PROGRESS|BLOCKED|REVIEW`
Baseline: `MAIN-SHA`
```

`tools/validate_pr_contract.py` enforces:

- Draft executable PR: task exists in branch manifest and its state equals
  `IN_PROGRESS` or `BLOCKED`.
- Ready WORKER/EXPENSIVE PR: task row and brief are already retired in that same
  PR and lifecycle is `REVIEW`.
- Ready CONTROL PR: the CONTROL row remains present.
- `CONTROL-PLANE` is reserved for repository-governance PRs that are not a
  scientific task.

## Rules of operation

1. **No completed task storage.** `manifest.json` admits only `PLANNED`,
   `IN_PROGRESS`, `BLOCKED`, `REVIEW`; executable tasks disappear on
   acceptance.
2. **Hierarchy and delegation.** Every EXPENSIVE/WORKER task has an immediate
   CONTROL parent. Agents do not mint child work outside CONTROL.
3. **Claim discipline.** `affected_claims` must name existing claim/alias IDs.
   New claim IDs require an explicit CONTROL decision.
4. **Generated views.** `00_WORK/STATUS.md` and the README status block are
   deterministic outputs of `tools/render_work_status.py`; do not hand-edit.
5. **Closed failed PRs stay closed.** If a task is still valid after an abandoned
   execution, it remains/re-enters PLANNED on main and starts later in a **new**
   PR from fresh main.

## Lean iteration protocol

Lean wall time is treated as an engineering constraint, not as unavoidable
formalization overhead.

Use:

```bash
python tools/lean_task_build.py narrow D0.Geometry.SomeModule
python tools/lean_task_build.py final
```

The helper serializes access to the shared `.lake` cache, refuses a second
concurrent build, detects source edits during a build, and skips duplicate
`D0.All` validation for an unchanged source tree.

Mandatory discipline:

1. **One agent/worktree owns one Lean task PR.** Never let two processes edit the
   same `.lean` file or build against the same shared cache concurrently.
2. **One narrow module per iteration.** Do not run `D0.All` while a target module
   is red.
3. **Batch compiler errors.** Read/fix the whole first useful error cascade before
   the next build; do not spend one build per tactic line.
4. **Split slow modules structurally.** If a module repeatedly costs about a
   minute or more to rebuild, move stable base lemmas into an imported module and
   keep no-go witnesses / finite certificates in downstream modules.
5. **Use the repo-proven proof shapes first.**
   - Matrix algebra: explicit `Matrix.add_mul`, `Matrix.mul_add`,
     `Matrix.smul_mul`, `Matrix.mul_smul` before module/ring closure.
   - Keep both sides of `calc` in the same association/normal form.
   - Type finite indices/matrices explicitly when elaboration is ambiguous.
   - Use `Nat.le_trans (by decide) hn` for small fixed bounds when appropriate.
   - For exact finite matrices already independently checked, prefer
     `native_decide` rather than repeatedly probing kernel `decide`.
6. **One final full build.** Run `python tools/lean_task_build.py final` only
   after all narrow modules are green. Registry/view generation comes after
   that, not during proof iteration.
7. **Remote CI is acceptance truth.** Local timings/builds are supporting
   evidence; the ready PR must satisfy GitHub guards.

## CI build-cache policy

GitHub Lean CI uses the cache built into `leanprover/lean-action@v1`; do not layer a second `actions/cache` over `03_FORMALIZATION/.lake`.

**PR policy:** Draft PRs never run the full `D0.All` release closure. Workers iterate locally with `python tools/lean_task_build.py narrow ...`. When a PR is marked Ready, the `ready_for_review` event runs exactly one full cached release closure over the complete PR formalization diff. Later Ready-state synchronize events run Lean only when the triggering commit itself changes `03_FORMALIZATION/**`; lifecycle-only audit commits skip it.

**Push policy:** main runs Lean only when the push changes `03_FORMALIZATION/**`. Explicit `workflow_dispatch` always runs the full integration build.

The built-in Lake cache key is pinned by runner OS/architecture, `lean-toolchain`, `lake-manifest.json`, and commit SHA with compatible-prefix fallback. Cache reuse is acceleration, not proof evidence.

Lean workflow concurrency is scoped by PR/ref **and head SHA**. This prevents a stuck runner for an obsolete PR head from blocking a newer Ready head; duplicate events for the same head still share one concurrency group.

## CI cost policy

- Feature-branch pushes no longer run a second duplicate CI in addition to the
  PR event.
- Pull-request jobs cancel superseded runs for the same PR.
- Full Lean build is skipped when a PR changes no Lean/formalization source.
- Long registered-certificate suites are skipped when a PR does not touch their
  dependency surface.
- Fast architecture/work/semantic guards still run on every PR.
