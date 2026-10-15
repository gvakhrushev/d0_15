# AGENTS.md — D0 cold-start execution contract

Repository: `gvakhrushev/d0_15`  
Canonical remote: `https://github.com/gvakhrushev/d0_15`  
Default base: `main`

This file is the cold-start contract for any new AI agent, researcher, worker, or
automation process entering the repository without prior chat context.

## 1. Never ask which project when a D0 task ID is provided

If the user gives a task ID such as `EXP-...`, `WRK-...`, or `CTRL-...`,
this repository is the project unless the user explicitly names another repo.

Start by reading:

1. `AGENTS.md`;
2. `00_WORK/README.md`;
3. `00_WORK/manifest.json`;
4. the task brief named by the manifest.

If the task is absent from `main`, check open GitHub PRs before creating
anything. It may already be executing. Do not create a duplicate execution.

Use `python tools/task_dispatch.py TASK-ID` for live resolution, including when
the task is absent locally. An offline printout is unverified planning, not
authorization to create a competing execution. Read only the task's inputs and
the relevant current route; do not begin every session by auditing the corpus.

## Scientific priority and parallel execution

The [current gravity route](02_REGISTRY/research/MEMO_A4D_RESOLVED_AFFINE_PROGRAM.md#current-route-to-general-relativity)
is the working scientific entry point. One integrator owns its end-to-end
argument, definitions, norms and source conventions. Delegate independent
premises with a named consumer in that argument; integrate each result as it
arrives. Do not wait for every research lane to finish before composing results.

Use separate branches/worktrees and disjoint write paths for independent
executors. Read-only assistants and bounded implementation subtasks within one
owned PR do not require new task rows. Register a separate scientific execution
through CONTROL when it owns an independent research/proof obligation. Existing
prerequisites and WIP limits still apply, including live PRs whose queue rows on
main remain PLANNED. A free slot alone does not establish mathematical inputs.

Each new or revised scientific brief records, in its existing text: exact
statement and remaining assumptions; input refs; carrier/norm/source convention;
write paths; the consuming parent step; the smallest decisive check. No new
status registry is needed. A certificate is useful when it resolves that step;
do not produce rank catalogues, audit memos or formalizations without a consumer.

When an interface does not type-check, the integrator resolves that mismatch
before dispatching dependent work. A scoped no-go must change the parent route,
not trigger an unbounded new census. Keep independent work moving.

## Validation budget

Follow the [change-based matrix](00_WORK/README.md#validation-budget).
During iteration run the changed calculation, targeted tool test or narrow Lean
module. Documentation/process edits do not call for a full mathematical replay.
At Ready, run the affected integration gates once on the final inputs; broaden
when transitive dependencies are uncertain. Re-run after a relevant input,
environment or execution-mode change, or a failure; do not repeat an unchanged
expensive run merely for a prose/lifecycle update. Preserve exact input provenance.

Draft CI runs structural guards and tooling tests. Heavy research/registered
certificate replay runs at Ready, on main and on explicit integration runs.
Independent research checks use isolated worktrees. Never rewrite expected
evidence, skip a failing premise or weaken a scientific statement to get green CI.

## 2. GitHub is the durable execution plane

Do not use chat as the primary notebook or task database.

For queued `WORKER` and `EXPENSIVE` tasks:

1. branch from current `main`;
2. run the lifecycle start command from the brief;
3. open a Draft PR before substantive work;
4. write the primary artifact directly into that PR;
5. keep derivations, exact witnesses, certificates, and research memos in Git;
6. retire the task in the same PR before marking Ready;
7. merge is completion.

Chat handoff is short by default: PR, exact conclusion and consuming parent step
(or route change), checks, and one blocker.

Commit/push at a durable mathematical or engineering checkpoint; local iterations
within the open PR do not need a remote commit for every calculation. Report the
consumed result or removed premise with its blocker, not a count of PASS labels.

If a task already exists in `00_WORK/tasks/`, do not paste or regenerate the
full task in chat. Use the Git brief.

## 3. Dispatch must be self-contained

Every executable task brief must state:

- repository slug;
- base ref;
- branch name;
- primary artifact;
- GitHub-first execution mode;
- why the task is delegated;
- short chat handoff contract.

A portable dispatch message must include both repository and task ID. Preferred:

```text
Repository: gvakhrushev/d0_15
Task: TASK-ID
Read 00_WORK/tasks/TASK-ID.md on main and execute GitHub-first.
```

Use `python tools/task_dispatch.py TASK-ID` to print the canonical launch text.

## 4. Triage before creating a task

Do not create a worker/research task merely because delegation is possible.

### CONTROL does it directly

Prefer direct CONTROL execution when the work is a small bounded repair, for
example:

- a few related file edits;
- a short deterministic calculation;
- registry/README/process cleanup;
- a simple CI fix;
- a review correction that does not benefit from independent execution.

If CONTROL can safely finish the change in the current PR without meaningful
research uncertainty or expensive build work, do it directly.

### WORKER

Create a `WORKER` only when there is a bounded, independently reviewable
artifact such as:

- an exact certificate;
- a Lean module/proof target;
- a deterministic migration;
- a reproducible finite computation;
- a substantial implementation with meaningful validation.

### EXPENSIVE

Create an `EXPENSIVE` task only for real research uncertainty:

- classification;
- competing mathematical constructions;
- theorem/no-go discovery;
- pressure testing;
- large search where the correct result is not known in advance.

Only CONTROL registers new tasks. Executors do not mint child tasks from chat.

## 5. Research strategy: KILL-FIRST

Do not search by accumulating attractive candidates.

Use the following gates, stopping as soon as a candidate dies:

```text
TYPE
→ REPRESENTATION / Hom-space
→ SYMMETRY
→ MODULI DIMENSION
→ FLAT LIMIT
→ VARIATION
→ GAUGE / CONSTRAINT QUOTIENT
→ EXACT FINITE SPECTRUM
→ PHYSICAL INTERPRETATION
```

Prefer known mathematical classification results and invariant theory before
inventing new formulas. Reverse-engineering a target mathematical structure is
allowed; importing the desired physical equation as an axiom is not.

Track separately:

[
d_A=dim(	ext{action family}),qquad
d_E=dim(	ext{independent Euler--Lagrange family}),qquad
d_P=dim(	ext{physical operator family after quotient}).
]

Do not demand a selector at the action level before checking whether the
physical equations/operators actually differ.

## 6. Lean strategy: classify once, specialize late

Lean is a boundary checker, not the primary search engine.

Preferred order:

1. manual/representation-theoretic classification;
2. exact rational/Python certificate for finite rank/nullity/witnesses;
3. hostile negative controls;
4. one generic Lean theorem for the surviving family;
5. specialize named physical cases only as corollaries.

Do not formalize each candidate separately when a generic parameterized theorem
can classify the whole family.

Use `python tools/lean_task_build.py narrow ...` while iterating and one final
`python tools/lean_task_build.py final` only after narrow targets are green.

## 7. Scientific status discipline

Do not promote a research memo to a public/CORE claim merely because its
calculation passes.

Keep explicit distinctions among:

- owned/formalized theorem;
- exact finite certificate;
- research classification;
- conditional physical interpretation;
- missing selector/principle.

Do not call spatial stiffness a wave equation, a Role direction physical time,
or a Palatini-like density Einstein gravity until the required downstream
variation/constraint/dynamics theorems exist.

## 8. Reviewed checkpoints and response-memory scope

Read `02_REGISTRY/research/CONTROL_RESPONSE_MEMORY_CONSOLIDATION.md` before
resuming the consolidation / response-memory program. A CONTROL checkpoint may
integrate a reviewed artifact slice while its original EXPENSIVE parent remains
open. Do not change an executable task's class or retire it merely to bypass a
lifecycle gate. Keep the unresolved obligation and its original PR discoverable.

On one fixed exact metric source, Xi(K1)=h^2*tau=Xi(K2). A negative response
terminal must compare an admitted exact refining sequence with the designated
comparator; two exact roots of one source cannot have different Xi. A finite
stencil does not by itself prove finite-dimensional sufficient memory, and
undetermined current memory can be response-invisible. Do not revive these
rejected shortcuts from a chat summary.

A local commit is not a publication. Before reporting a result as stored in
GitHub, verify its remote head and artifact blob. Preserve the source SHA and
checker/ledger pair in checkpoint intake. The read-only history workflow exports
published branch/tag/PR histories; its artifact has finite retention and cannot
recover a commit that was never sent to a published ref.
