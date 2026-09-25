# WRK-NIGHTLY-FORMALIZATION-DEBT-BURN-W1
Repository: \`gvakhrushev/d0_15\`
Base: \`main\`
Branch: \`wrk/nightly-formalization-debt-burn-w1\`
Primary artifact: \`tools/formalization_debt_audit.py\`
Execution: \`GitHub-first\`

Class: \`WORKER\`  
Parent: \`CTRL-NIGHTLY-FORMALIZATION-MAINTENANCE-W1\`

## Why delegated

This is intentionally a large overnight maintenance wave: it requires a
repository-wide audit, many independent low-risk Lean refactors, repeated
narrow builds, build-time profiling, import-graph analysis, generated-view
checks, and one final integration build.  It is too large for a small CONTROL
edit but it has bounded engineering outputs and no open scientific question.

## GitHub execution contract

1. Branch from the current \`main\`.
2. Run:
   \`python tools/task_lifecycle.py start WRK-NIGHTLY-FORMALIZATION-DEBT-BURN-W1\`
   as the first lifecycle change.
3. Open a Draft PR **before** substantive edits.
4. Keep all durable work in that PR.
5. Iterate with \`python tools/lean_task_build.py narrow ...\`; do not run full
   \`D0.All\` while a touched target is red.
6. Before Ready, run the final gates below, retire the task with
   \`python tools/task_lifecycle.py retire WRK-NIGHTLY-FORMALIZATION-DEBT-BURN-W1\`,
   update the PR body to \`Lifecycle: REVIEW\`, and do not self-merge.

## Objective

Burn as much **safe accumulated formalization and repository engineering debt**
as possible in one long pass while preserving all public mathematical
statements and all scientific status boundaries.

This is not a research task.  If a cleanup requires deciding new mathematics,
changing a theorem statement, adding a premise, strengthening a claim, or
choosing between scientifically inequivalent constructions, **skip it** and
record it as outside this worker.

The wave should be large.  Do not stop after fixing one or two obvious files.
Continue through the work packages until the defined safe queue is exhausted or
the exit condition is met.

---

## 0. Collision fence — mandatory before touching code

This worker runs concurrently with scientific/formalization work.

At task start:

1. list every open PR in \`gvakhrushev/d0_15\`;
2. collect the changed-file set of every open PR other than this worker;
3. treat that union as **read-only**;
4. record the PR numbers and read-only paths in this worker PR body.

At registration time PR #175
(\`CTRL-A4D: pressure-test star density through variation and quotient\`) is
active.  A separate formalization PR may appear after this brief was written.

Therefore repeat the open-PR collision check:

- before each broad refactor batch;
- before the final integration build;
- immediately before Ready.

If another PR starts touching a file that this worker already changed, revert
this worker's changes to that file and continue elsewhere.  Never force-resolve
scientific work in favour of maintenance.

The only permitted overlap is deterministic lifecycle/generated work under
\`00_WORK/\` and the README work-status block when retiring this worker.

### Permanently forbidden scientific surfaces

Do not edit:

- \`01_BOOKS/**\`;
- \`02_REGISTRY/research/**\`;
- \`02_REGISTRY/claims.csv\`;
- \`02_REGISTRY/assumptions.csv\`;
- \`02_REGISTRY/frontier/**\`;
- scientific claim/release statuses;
- any active A4D star-density / variation / physical-Hessian artifact or Lean
  module belonging to another open PR.

Mechanical \`02_REGISTRY/formal_support.csv\` path synchronization is allowed
only if this worker itself performs a safe internal refactor that requires it;
do not change claim meaning/status.

---

## 1. Install a durable formalization-debt audit

Create \`tools/formalization_debt_audit.py\`.

It must be deterministic, stdlib-only if practical, and support:

\`\`\`bash
python tools/formalization_debt_audit.py
python tools/formalization_debt_audit.py --json
python tools/formalization_debt_audit.py --check
\`\`\`

The audit must inspect at least:

### Lean source hygiene

- executable \`sorry\` tokens;
- executable \`admit\` tokens;
- \`TODO\` / \`FIXME\` markers;
- direct duplicate imports;
- forbidden \`import D0.All\` from library modules;
- \`set_option maxHeartbeats\` overrides;
- module LOC;
- direct import fan-in/fan-out.

The proof-hole scanner must distinguish executable tokens from occurrences in:

- line comments;
- nested block comments;
- strings/docstrings.

Do not classify a comment saying “sorry-free” as a proof hole.

### Module graph

Construct the local D0 import graph and check:

- every imported local module exists;
- no local import cycle;
- every intended \`03_FORMALIZATION/D0/**/*.lean\` module is reachable from
  \`D0/All.lean\`, or appears in a small explicit allowlist with a reason;
- no module imports itself;
- no duplicate direct import in one file.

### Baseline/non-growth mode

If current main contains debt that cannot be safely removed during this wave,
store a machine-readable baseline (for example
\`tools/formalization_debt_baseline.json\`).

Every baseline entry must include:

- exact path;
- debt kind;
- exact reason it remains.

\`--check\` must reject **new** debt relative to that baseline.

Do not create a giant permanent exemption list for things that can simply be
fixed.

Integrate the stable non-growth audit into \`.github/workflows/guards.yml\`
only after it passes on the cleaned tree.

---

## 2. Proof-hole and placeholder hygiene

Audit all non-excluded Lean modules.

For every executable \`sorry\` / \`admit\`:

1. first try to close it using already-owned definitions/lemmas;
2. preserve the exact theorem statement;
3. do not add a new axiom;
4. do not convert a \`sorry\` into an assumption carrier;
5. do not weaken the theorem;
6. do not add a scientifically stronger lemma merely to make the proof easy.

Explicit bridge-assumption structures are not proof holes merely because they
carry a proposition as data.

If a real proof hole cannot be closed without new mathematics, leave its
scientific file unchanged and baseline it with an exact reason.

Remove stale comments that claim a module has a hole when it no longer does,
or claim “0-sorry” when that is no longer literally true.

---

## 3. Import graph and namespace cleanup

Across the safe source set:

- remove duplicate imports;
- narrow obviously over-broad imports where narrow builds prove the replacement;
- remove accidental umbrella imports;
- remove redundant \`open\` / \`open scoped\` only when the module still compiles;
- eliminate trivial import chains introduced solely by historical refactors;
- fix stale local module comments/import names;
- ensure new helper modules are reachable from the normal \`D0.All\` graph.

Do **not** move public theorem declarations to a new owner module merely to make
the graph prettier.

Public module paths and theorem names are compatibility surfaces.

---

## 4. Build-hotspot profiling and optimization

Profile a meaningful set, not just one favourite module.

Minimum profiling set:

- the 20 largest non-excluded Lean modules by LOC;
- every non-excluded module containing \`set_option maxHeartbeats\`;
- every module this worker materially refactors.

Use the repository build helper and keep a baseline timing table in the PR body.

For genuine hotspots, prefer in this order:

1. import narrowing;
2. moving stable **private/internal** helper lemmas to a lower dependency layer;
3. replacing repeated expensive tactic search with explicit existing lemmas;
4. replacing repeated finite kernel computation with one reusable exact lemma;
5. \`native_decide\` only for genuinely finite decidable facts already suited
   to it;
6. structural module split when it reduces rebuild surface.

Do not optimize by increasing \`maxHeartbeats\`.

### Performance acceptance rule

For every change advertised as a performance optimization:

- compare median narrow-build time before/after under the same environment;
- if it regresses by more than 10% and there is no strong structural reason,
  revert that optimization.

Try to reduce or eliminate existing heartbeat overrides when the refactor makes
them unnecessary.  New heartbeat overrides are forbidden.

---

## 5. Large-module refactor pass

Take the largest/slowest safe modules and inspect at least the top 10.

Attempt at least three structural split candidates.

A split is acceptable only when:

- public theorem names remain unchanged;
- public theorem declarations remain in their existing owner module unless a
  purely internal helper is being extracted;
- no claim semantics or release status changes;
- the import DAG becomes no worse;
- narrow build passes;
- the measured rebuild surface/timing is improved or the split removes a clear
  dependency knot.

Land every safe split that satisfies those conditions.

If fewer than two safe splits survive, do not manufacture them; record the
rejected candidates in the PR body and spend the remaining time on other debt
classes.

---

## 6. Repeated-proof and internal-helper refactoring

Search for repeated low-level proof boilerplate in the safe modules, especially:

- matrix algebra normalization;
- finite-index extensionality;
- repeated \`LinearMap.ext\` / \`Matrix.ext\` wrappers;
- repeated finite rank/nullity witnesses;
- repeated Role/Fock permutation boilerplate;
- repeated exact rational helper code.

Promote a common helper only when:

- the statements are genuinely the same abstraction;
- using it does not create a dependency cycle;
- at least two real call sites become simpler;
- the helper has a natural lower-level owner.

Prefer one generic parameterized lemma over multiple near-identical special
lemmas.

Delete private/internal helpers made dead by the refactor after proving they
have no remaining references.

Do not collapse scientifically distinct negative controls merely because their
proof scripts look similar.

---

## 7. Routine integration hygiene

For all touched formalization code:

- preserve theorem names and theorem statements;
- preserve namespaces unless changing a private/internal helper;
- verify \`D0/All.lean\` reachability;
- mechanically update \`02_REGISTRY/formal_support.csv\` only when necessary;
- do not edit claim strength, release status, book prose, or research verdicts;
- run Python syntax checks for touched tools;
- keep generated files deterministic;
- remove temporary profiling files before Ready.

If a stale artifact is clearly dead but deleting it would change a public
registry/claim owner, do not delete it in this worker.

---

## 8. Quantity target — make this an overnight wave

This worker should produce a substantial diff, not cosmetic churn.

Define one **closed debt item** as one independently verifiable removal of a
pre-existing issue, for example:

- one executable proof placeholder closed;
- one duplicate/bad import removed;
- one orphan/reachability defect repaired;
- one stale TODO resolved without semantic change;
- one heartbeat override removed;
- one build hotspot materially simplified;
- one safe module split;
- one duplicated private proof/helper family consolidated.

Targets:

- close at least **20** real debt items;
- span at least **4** different work-package categories above;
- inspect at least **25** safe Lean modules.

If the deterministic initial audit finds fewer than 20 genuinely actionable
safe items, exhaust **all** of them and report that fact instead of inventing
work.

Whitespace-only, comment-only, formatting-only, or generated-view changes do
not count toward the 20-item target unless they repair a false/stale technical
statement.

---

## 9. Mandatory negative controls

The worker must explicitly demonstrate that it did **not** achieve cleanup by:

- changing theorem statements;
- adding assumptions/axioms;
- adding \`sorry\` / \`admit\`;
- increasing \`maxHeartbeats\`;
- deleting a negative-control theorem;
- weakening CI;
- removing a module from \`D0.All\` merely to avoid compiling it;
- touching another active PR's scientific files;
- changing \`claims.csv\` or a release status;
- replacing exact proof with an unchecked numerical approximation;
- hiding debt in the audit baseline without a path-specific reason.

The final PR body must show before/after audit counts.

---

## 10. Build and validation gates

During iteration:

\`\`\`bash
python tools/lean_task_build.py narrow D0.<TargetModule>
\`\`\`

Run narrow builds for every materially touched owner.

Before Ready:

1. refresh the open-PR collision fence and resolve by backing off, not by
   overwriting concurrent work;
2. run \`python tools/formalization_debt_audit.py --check\`;
3. run \`python -m compileall -q tools\`;
4. run repository fast guards relevant to the touched files;
5. run exactly one final:
   \`python tools/lean_task_build.py final\`;
6. ensure generated registry/work views are fresh;
7. retire the task in the same PR;
8. let GitHub CI be acceptance truth.

No final full build is allowed while any narrow target is red.

---

## Exit condition

The task is ready for CONTROL review only when all of the following are true:

1. the durable formalization-debt audit exists and has useful
   human/\`--json\`/\`--check\` modes;
2. its non-growth checks cover proof placeholders, local import graph/reachability,
   duplicate imports, forbidden umbrella import, and heartbeat overrides;
3. all safe actionable executable \`sorry\`/\`admit\` findings discovered by
   this worker are closed or path-specifically baselined because closure would
   require new mathematics;
4. at least 20 real debt items across at least 4 categories are closed, **or**
   the initial audit proved fewer than 20 safe actionable items existed and all
   were exhausted;
5. at least 25 safe Lean modules were inspected;
6. no public theorem statement/name or scientific status changed;
7. no concurrent active-PR scientific file is modified;
8. no new \`sorry\`, \`admit\`, axiom, heartbeat override, or CI weakening is
   introduced;
9. all materially touched Lean modules pass narrow builds;
10. the final \`D0.All\` integration build and GitHub guards pass;
11. the task is self-retired and the PR is Ready, not self-merged.

## Chat handoff

Return only:

- PR number;
- \`PASS\` or \`BLOCKED\`;
- before → after headline debt counts;
- number of closed debt items;
- number of Lean modules materially changed;
- median/full-build timing headline if measured;
- one exact blocker if not Ready.

Do not paste the maintenance log or large diffs into chat.
