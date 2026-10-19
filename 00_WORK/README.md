# D0 work flow: compose the gravity derivation

Repository: `gvakhrushev/d0_15`. The [current scientific route](../02_REGISTRY/research/MEMO_A4D_RESOLVED_AFFINE_PROGRAM.md#current-route-to-general-relativity)
defines the remaining transitions to general relativity. This file defines how
to execute them. GitHub PRs hold durable work; `manifest.json` is the queue,
not a live dashboard. Scientific acceptance and use in the parent derivation
are separate from a passing check.

## One integrator, parallel bounded work

The scientific integrator owns the common carrier, full action, source,
variation image, normalization and refinement maps. Executors prove independent
premises of that same argument in separate branches/worktrees with disjoint
write paths. Integrate a usable result immediately; do not wait for an entire
wave to finish.

Use two scientific fronts: preparation/records → full action/source, and exact
joint solutions → nonlinear refinement limit. A verification executor handles
replay/CI when needed. An independent reviewer checks a frozen intake at
acceptance. These are roles, not additional permanent task classes or slots.
Read-only assistants and implementation subtasks inside an owned PR do not
need their own queue rows. Independently owned scientific obligations do.

Before delegating, put the interface in the existing brief and bind its shared
definition in the [gravity assembly](../02_REGISTRY/gr_assembly/README.md).
This is composition data, not a second queue or claim-status registry:

| Field | Required content |
|---|---|
| Statement | Exact conclusion, quantifiers and remaining assumptions |
| Inputs | Owner paths and fixed refs; accepted vs research status |
| Common objects | Carrier, full action, norm, source/comparator and refinement maps used by the consumer |
| Consumer | Parent lemma/equation; where this output is substituted and which premise it removes |
| Write surface | Disjoint paths and one branch/worktree owner |
| Decisive check | Smallest calculation/proof and negative control that can decide the claim |
| Assembly | One `Assembly: TASK-ID` line, a registered interface/work key and separate start/completion premises |

If no parent consumer can be named, keep the idea out of the active wave.
If interfaces conflict, the integrator resolves them before dependent work
starts. An exact obstruction changes the parent route; do not answer it with
another exhaustive census unless that census is needed by a named estimate.
A free WIP slot alone does not establish prerequisites.

For route selection run `python tools/gr_assembly.py next`; it resolves live
executions once and shows the consuming step and reviewable result applications.
For a named task use the ordinary dispatcher below. `why OBLIGATION`, `search
QUERY` and `attempts QUERY` return the exact missing inputs and prior scoped
results without a corpus audit. Potential downstream reach is separate from
the number of newly ready consumers; neither is a probability of success.

## Start or resume once

1. Read `AGENTS.md`, this file and the relevant current scientific route.
   For CONTROL entry/workflow changes, inspect open governance PRs and their
   changed paths once. Shared README/AGENTS, queue, dispatch or CI edits go to
   one existing owner/PR; contributors hand over disjoint content. Task-ID
   lookup alone does not detect two different proposals rewriting the same flow.
2. Fetch current `main` once and resolve the task with:

   ```bash
   python tools/task_dispatch.py TASK-ID
   ```

   The tool checks live PRs, including tasks absent locally. An existing Draft
   is resumed; a Ready PR awaits review. Multiple matches or an unavailable
   lookup need resolution before a new launch. `--offline` is explicitly
   unverified planning; it does not establish that no execution exists.
   Resolution is a snapshot, not an atomic reservation: CONTROL assigns one
   launch owner, who opens the Draft before another executor is dispatched.
3. Read only the brief and its actual inputs. Reuse pinned accepted results;
   do not audit the whole corpus or re-prove delegated dependencies at cold start.
4. For a new executable task, confirm CONTROL registration, mathematical
   prerequisites and WIP including live executions. Start from current `main`;
   run `python tools/task_lifecycle.py start TASK-ID`; open a Draft PR before
   substantive work. Continue in that PR until Ready.

   Gravity start checks also reject a different task with the same scientific
   work key even when its interface changes, unresolved actual start
   prerequisites and live WIP overflow. They run before any lifecycle mutation.
   Conditional lemmas can proceed on declared interfaces while their physical
   assumptions remain open.

Portable dispatch includes both repository and task ID. CI checks brief metadata:

```text
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/...|exp/...`
Primary artifact: `repo/relative/path`
Execution: `GitHub-first`
```

Each executable brief also has `## Why delegated`, `## GitHub execution contract`
and `## Chat handoff`. CONTROL may generate a skeleton with
`python tools/task_brief_scaffold.py --help`; fill in its proof interface before
registration/dispatch. Existing briefs need updating when their interface is
actually revised, not a bulk cosmetic migration.

## Work in short scientific increments

1. Work on the next missing transition; write the derivation in its primary
   artifact. Use representation theory/classification before candidate searches.
2. Apply KILL-FIRST only to unresolved gates:
   type → representation/Hom-space → symmetry → moduli → flat limit → variation
   → constraint quotient → exact finite spectrum → physical interpretation.
   Stop a candidate at its first failure. Do not replay already owned gates.
3. Test the changed argument with the smallest decisive check. A finite exact
   calculation gets a certificate when it bears on the conclusion. An analytic
   proof is not replaced by collecting more numerical ranks. Lean follows
   **classify once, specialize late**, after the mathematical interface stabilizes.
4. At a useful checkpoint, commit/push the result and substitute it in the
   parent argument. Local experiments do not need a remote commit each time.
   Record either the discharged premise or the exact obstruction and route change.

   Record an application with `python tools/gr_assembly.py template TASK-ID`.
   Pin the result, map every hypothesis, name the parent location and obtain
   independent acceptance on the exact application digest. Different interfaces
   require proved maps for carrier, action, variations, source, normalization,
   refinement and scope. A finite check cannot fill a uniform-family premise.
   A scoped no-go can classify the original target or exclude its stated route;
   it cannot fill a positive existence slot. The original raw response and
   positive physical GR remain separate goals.

   Retirement and the Ready PR gate require a complete, scoped, reviewable
   submission for the binding's original completion premises. Proposed intake
   can reach Ready so final replay and independent review can occur. It does not
   discharge an accepted premise or goal until its pinned acceptance exists.
   Parent research can remain open while a narrower result is accepted; do not
   retire an unresolved parent to publish a useful slice.

Preserve all specified components, source terms and resonant directions.
Compare actions only when action equality is necessary; equality of physical
operators or a controlled response remainder may suffice. Do not identify
geometric and full matter responses, fit a source to the output, change a norm,
or assume the desired Einstein equation in admission conditions.

## Validation budget

Choose by the changed surface. These are phase boundaries, not a checklist for
every edit. Record command, checked inputs/ref, environment and result in the PR.
Repeat an expensive run only after a relevant input/environment/mode changes,
a failure, or a concrete unresolved concern. A prose/lifecycle edit alone does
not invalidate unchanged mathematical evidence. An old green badge alone does
not establish input identity.

| Changed surface | During iteration | Before Ready / acceptance |
|---|---|---|
| README / work rules / briefs | Check links and affected work/agent validators | Structural guards and generated-view check; no Lean or mathematical replay for prose alone |
| Tooling / CI | Changed tool's fixture tests, syntax, failure paths | Same focused tests plus structural guards; runners must test isolation, failure and mutation detection |
| Research calculation | Changed entrypoint and inputs it actually reads | Cumulative affected research entrypoints and transitive inputs; broaden if dependencies are uncertain |
| Lean source | `python tools/lean_task_build.py narrow D0.Geometry.SomeModule` | One `python tools/lean_task_build.py final` after narrow targets pass, plus affected guards |
| Registered certificate / BOOK / release inputs | Changed certificate and relevant hostile control | Registered suite when its dependency surface changes; exact evidence stays immutable |

Useful structural commands (select those affected by the change):

```bash
python tools/validate_repo.py
python tools/validate_work.py
python tools/validate_agent_protocol.py
python tools/gr_assembly.py check
python tools/gr_assembly.py render --check
python tools/render_work_status.py --check
python tools/generate_lean_views.py --check
```

Draft CI runs architecture/work/semantic guards and tooling fixture tests.
**Heavy research and registered-certificate replay is deferred until Ready**,
then runs under the workflow's affected-input selection. Main and manual
integration runs retain their required replay. Moving a Ready PR back to Draft
is appropriate while changing its scientific argument.

A Ready synchronize changing only `README.md`, `AGENTS.md` or this work guide
can reuse a successful Ready check on the previous head when the exact base,
scientific files and installed environment match. Structural and semantic guards
still run. Missing evidence, a skipped/failed prior replay, a changed environment
or any other changed path triggers normal cumulative replay. This is a narrow
process-document exemption, not a research dependency cache.

Research replay runs independent certificates in isolated worktrees at one
exact committed ref, with bounded parallelism, per-certificate timeout and
mutation detection. It has no result cache. Use the runner's `--help` for
local replay; uncommitted experiments are not part of a committed snapshot.
Declared dependencies are authoritative; the changed-file selector alone is
not a complete research dependency graph. If a shared input changes without
its certificate changing, replay its consumers explicitly (manual full research
replay when the affected set is uncertain) before accepting that intake.

Lean builds serialize access to a shared `.lake`; independent agents must not
build concurrently against that cache. Keep stable lemmas in imported modules,
batch compiler corrections and preserve caches. CI's built-in Lake cache is an
accelerator, not proof evidence. Draft PRs skip `D0.All`; Ready transitions run
the full affected formalization closure. See `.github/workflows/lean-build.yml` for
exact event selection.

## Accept an integrated result

The handoff names the PR, exact conclusion, consumed parent step (or changed
route), checks and smallest blocker. Keep detailed tables/derivations in Git.
The integrator checks applicability to the common objects; independent review
checks assumptions, non-circularity and the frozen artifact scope.
A useful research slice can be accepted without closing its broader parent.

Before marking a WORKER/EXPENSIVE PR Ready: refresh against current `main`,
run affected final checks, use `python tools/task_lifecycle.py retire TASK-ID`
to remove its queue row and brief and regenerate views in the **same PR**.
Set `Lifecycle: REVIEW`. Do not retire a task whose scientific terminal is open;
use a reviewed CONTROL slice instead. Do not self-merge. Merge is delivery;
being used in the parent derivation is the scientific integration result.

## Queue, PR and ownership contract

- `main` manifest = queue/control. PLANNED on main can correspond to an active
  execution in a PR; do not infer a free slot from local state alone.
- Draft + `IN_PROGRESS` = executing; Draft + `BLOCKED` = explicit blocker;
  Ready + `REVIEW` = awaiting CONTROL acceptance; merged = delivered.
- The semantic task ID names the obligation; the PR number identifies execution.
- Only CONTROL registers independent tasks. Small bounded repairs, README,
  process cleanup and simple CI fixes are direct CONTROL work, not new research.
- WORKER owns a bounded independently reviewable implementation/proof;
  EXPENSIVE owns genuine research uncertainty. Both have an immediate CONTROL
  parent and obey existing WIP limits. Do not change classes/retire parents to
  free slots or bypass lifecycle gates.
- Source/artifact refs remain pinned; local commits are not publication.
  Verify remote head and blob before reporting a result as published.
- Expected evidence is immutable under verification. No rewriting expected
  results, importing hidden premises or weakening scope to obtain PASS.
- Claims/releases stay in their existing registries. Generated `STATUS.md`,
  README status block, Lean views and ClaimMap are not hand-edited.
- Completed executable briefs leave `00_WORK` at retirement; Git history is
  their archive. Closed abandoned PRs stay closed; relaunch valid queued work
  in a fresh PR. There is no ordinary post-merge lifecycle cleanup PR.

Every PR uses `.github/pull_request_template.md` with exactly one of each:

```text
Repository: `gvakhrushev/d0_15`
Task: `TASK-ID`
Class: `WORKER|EXPENSIVE|CONTROL`
Lifecycle: `IN_PROGRESS|BLOCKED|REVIEW`
Baseline: `MAIN-SHA`
Primary-Artifact: `repo/relative/path|N/A`
```

`CONTROL-PLANE` is reserved for repository-governance PRs. Branch prefixes are
`control/`, `wrk/`, `exp/` for the corresponding class. A Draft may retain its
launch Baseline while it remains an ancestor of both main and task head;
at PR-open and Ready, Baseline equals the current base SHA. Ready executables
are self-retired; Ready CONTROL retains its row (CONTROL-PLANE is exempt).
Validation is enforced by `tools/validate_pr_contract.py`.

Feature-branch pushes do not duplicate PR CI; superseded runs for a PR are
cancelled. Heavy suites are scoped to their inputs. Full integration replay is
available manually; there is no new periodic audit or task scheduler.
