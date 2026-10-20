# D0 to GR assembly

Use this layer to find the next missing transition, its current owner and the
results that can actually be substituted into the derivation. The
[scientific route](../research/MEMO_A4D_RESOLVED_AFFINE_PROGRAM.md#current-route-to-general-relativity)
owns the argument. [VIEW.md](VIEW.md) is a generated composition overview.
Claims, proof owners, the work queue and live GitHub execution keep their
existing authorities. No graph label by itself promotes a scientific claim.

For scientific synthesis, start with the short [working map](SYNTHESIS.md):

```bash
python3 tools/gr_assembly.py puzzle
python3 tools/gr_assembly.py puzzle vacuum
python3 tools/gr_assembly.py puzzle source
```

Each piece names reusable published inputs, its consuming steps and the next
mathematical question. Exact piece IDs select one card; other queries search
the indexed statements and hypotheses. `--json puzzle QUERY` includes those
hypotheses and display aliases. The map reads local metadata only, so it works
without fetching historical branches, checking every receipt or running any
calculation. It proposes uses; it neither accepts a proof nor authorizes launch.

Synthesis is the working loop: use a result, write the next argument, run the
changed calculation or narrow tool test when it helps decide that argument.
Final affected replay and independent acceptance stay at the existing Ready
boundary. Reading and combining inputs requires no new task, receipt, status
row or scientific registration form.

The optional `synthesis` links live in the existing `contract.json`; add a link
when it helps a concrete consumer. `navigation_alias_of` groups explicitly
duplicated result entries for display, retaining both IDs, interfaces, evidence
and applications. Shared evidence alone never merges different theorems.
`render` regenerates both views; no long research owner needs to be moved or
rewritten to keep the short map current.

## Enter with one relevant query

```bash
# A named task: existing execution, exact interface, assumptions and consumer.
python3 tools/task_dispatch.py TASK-ID

# Select work: live owners, scoped intake and conditional readiness.
python3 tools/gr_assembly.py next

# Read only the relevant missing inputs and previous results.
python3 tools/gr_assembly.py why positive_gr
python3 tools/gr_assembly.py search source
python3 tools/gr_assembly.py attempts volume
```

`next` and the dispatcher each obtain one live PR snapshot. Use the one that
answers the current question. An existing Draft is resumed; a Ready PR awaits
review. Offline mode prints **unverified planning** and never authorizes a new
execution. An unavailable live lookup fails closed. These commands do not
reserve a task, create branches, message other agents or change statuses.
If several open PRs claim one task, `next` checks whether they form one direct,
same-repository branch stack. A stack is reported as
`reconcile-stacked-source`, with parent/child branches and the relevant head
SHAs, so CONTROL can compare the child-only delta and pin the exact child head
consumed by its parent. This relation is only GitHub branch structure; it does
not prove that the parent contains or accepts the child's result. Other
multiple-owner patterns remain `resolve-overlap` and require reconciliation to
one owner before dispatch. Both actions are ranked ahead of ordinary resume,
and neither authorizes another execution.

`next` also checks each registered live owner's exact same-repository branch
descendants, even when a child PR omits or uses different `Task` metadata. It
reports one linear chain as `reconcile-stacked-source`; separate child branches
are reported as `reconcile-source-fork` so CONTROL can compare their exact
questions and child-only deltas without calling them duplicates by default.
Related PRs appear under `related_prs`. Branch relations do not register a child
as an owner, accept its result, or authorize another execution.

After CONTROL records an exact source-fork comparison in `contract.json`,
`next` suppresses only that repeated comparison while the parent identity, base
SHA and Task metadata and the complete child PR set still match. If the parent
head advances, it checks only the recorded child-delta paths at that exact
commit through one bounded GraphQL query. Unchanged path blobs keep the source
comparison valid; a changed path, changed child pin, new descendant, or
unavailable path check reopens it. The current and comparison head SHAs remain
visible in `reconciled_source_forks`. Child results stay result-only and
unaccepted, regardless of whether their source files later appear in the
parent. This avoids repeating a full fork review for unrelated parent commits
without treating branch ancestry as scientific acceptance.

`next` also lists `ready_obligations`: open obligations whose declared logical
inputs are already accepted, the downstream obligations that would become
ready if each were proved, and the current registered task/PR action. An
unowned obligation points to CONTROL registration or reopening; a proposed
application points to independent scoped review. This readiness is only a
dependency calculation. It does not assert evidence, physical admission, proof
success or launch permission, and unlock counts do not estimate proof success.

The three goals remain separate: positive native `GR`, the original `RAW-216`
contract, and global `D0-CLOSURE` classification. A classification or typed
passport is not positive internal GR. The two scientific fronts can prove
independent conditional premises in parallel, with their assumptions retained.

## Data and ownership

| Data | Authoritative location and owner |
|---|---|
| Scientific statements and proof status | Existing claims, Lean, certificates, research owners and CONTROL ledger |
| Current obligations, interfaces and execution bindings | `contract.json`, maintained by the integrator through CONTROL |
| Typed result pointers, applications and scoped attempts | `applications.json`, with pinned independent acceptance for each use |
| Historical research | Immutable `sources/` with original full commit, path and SHA-256 |
| Queue and lifecycle | Existing `00_WORK/manifest.json` and briefs; no copied queue states here |
| Live execution | GitHub PRs resolved by the existing dispatcher |
| Composition overview | Generated `VIEW.md`; never edit it by hand |

In this schema, an obligation is the assembly slot; do not create a parallel
`slots.json`. Add a result node only when it changes an open slot's route,
readiness or a material substitution decision. New evidence should point to
the existing research owner by commit/path/SHA. Copy source bytes only when
they are otherwise unavailable at the pinned Git commit. Active result nodes
are capped at 50; strengthen an existing node when new evidence supports the
same scoped result.

The frozen gravity graph preserves all 44 IDs and its complete source bytes.
`migration` maps each original ID to a searchable `legacy:ID`; unresolved
historical scope stays historical. Its old root pin, next-step prose and
reported statuses are not current launch instructions or accepted applications.
The current route's input is frozen separately. Source snapshots are read for
integrity and targeted lookup, not mandatory reading for every agent.

The typed main inputs and endpoint-probe candidate have exact statement/scope
boundaries. Their indexing introduces no scientific acceptance. An existing
proof can be reused in multiple applications; a new owner does not require
re-proving the mathematics.

A load-bearing result may be indexed before a compatible application is ready.
It remains searchable context only and closes no obligation until a typed,
independently accepted application records the exact substitution. Keep such a
result on its own interface when it does not yet transport to
`native-programme-v1`.

## Current scientific gate

The geometric side is no longer the immediate bottleneck: the pinned #334
`brinkmann-j2-null-family` result has the exact unrestricted 40→3→1 reduction,
the forced one-step null-link stagger, and a constructed two-tick J2 source
with arbitrary time-dependent null energy and transverse discrete harmonics.
That is a mathematical carrier/price family, not proof that the compulsory
full D0 action selects it. The `lorentz-null-conjugacy-cost-blindness` and
`full128-opposite-null-two-round-shannon-order-source` results narrow the
memory question: scalar single-plaquette class Costs erase null amplitude,
while an oriented retained-history readout can detect order, but literal
`fullStep` admission and payment remain open.

The shortest vacuum gate is now sharper than full off-shell price matching:
after solving the actual preparation, clock, work, oldRIGHT and internal
history Euler equations, check on the true zero-density shell that the selected
source has one value and `DS = Σ w_i df_i` with nonzero site weights. In a
regular chart, a locally bounded squared-ideal remainder then protects the exact
nonlinear vacuum stationary set and the raw 16+24 linearized kernel even when
the Book price has vertical history dependence away from the shell. The
48-field sourced-root Hessian test remains a separate check for the nonvacuum
response. Full Golden17 pointer Shannon and allowed Cost≥1 shape terms are
hostile controls, not substitutes for the selected total action. Only after
the selected source is shown to be local and linear on the five-point
Brinkmann stratum should four harmonic profiles identify its stencil. The
later recovery gate still needs a same-metric null system, full Ward transfer,
boundary/seam flux balance and refinement. These are decision criteria for the
existing route, not extra result nodes or permission to start a parallel task.

The four-profile stencil argument is a conditional identification lemma, not a
result about the compulsory action: after independently establishing linearity
and five-site support, testing `1`, `x`, `y`, and `x²−y²` fixes the coefficients
to a multiple of the central Laplacian; one nonzero matter source then fixes
the remaining ratio. It says nothing about a nonlocal or nonlinear native
operator. The assigned positive Julia model already composes `AB` and `BA`
exactly when it uses distinct fresh flag banks; reusing a flag has a known
identity-point defect. What remains open is whether the literal native
`fullStep` admits and pays those two operations and realizes the same ordered
readout. The next discriminating observation is one full old
LEFT/RIGHT/reference experiment for `AB` and `BA`, with both orders, all
outcomes, a boost control, and the observable composition defect between that
physical execution and the assigned Julia model. The opposite-branch
plaquette Euler equations must still be derived from the original action
before calling this a nonlinear gravitational completion.

Keep the connection normalization fixed when checking the proposed finite
Ricci/Weyl matrix. In the pinned #334 plaquette convention,
`K_link(u,x,y) = ½[H(u+h,x,y)−H(u+h,x−h,y)] = h K_u(u+h,x,y)`, where
`K_u = (H−H_-)/(2h)` is the connection per unit length. The cubic harmonic
`W=x³−3xy²` gives the proposed `h²` matrix from differences of `K_link`; taking
differences of `K_u` directly gives that matrix divided by `h`. The
common-center trace/tracefree test must therefore use the link-integrated
variables, include the forced one-step shift in `u`, and retain the transverse
plaquette staggering.

The pinned local Poisson law also gives a finite-domain balance: the summed
curvature trace is the boundary flux and equals `2 λ E(u) Area_h(D)` in the
stated normalization. On a periodic transverse torus the summed Laplacian is
zero, so a single-valued periodic profile cannot support nonzero mean source
when `λ ≠ 0`. Global completion therefore needs an actual boundary flux, chart
seam, or balancing source; the fixed local Dirichlet family alone does not
supply one.

## Register or revise an execution

CONTROL adds the semantic binding in `contract.json` while registering the
ordinary task. Add these exact lines to its brief:

```text
Assembly: `TASK-ID`
Assembly-Slot: `constitutive`
Assembly-Carrier: `native-programme-v1`
```

`Assembly-Slot` names the primary obligation; `Assembly-Carrier` names the
interface whose full carrier/action/source contract dispatch will print. These
must match the registered binding. A different carrier requires an explicit
`distinct-from` edge in `carrier_distinctions` and an
`Assembly-Distinct-From: edge-id` line in its brief; it remains separate until
a reviewed transport proves it can fill the slot. A slot already accepted on
the same carrier is blocked before a new branch starts.

The binding records its exact statement, interface version, scientific work
key, named consumer, disjoint write paths, `start_requires`, retained `assumes`
and `completion_requires`. These are scientific interface data, not task
states. Existing classes and WIP limits apply unchanged.

The dispatcher and lifecycle start reject a competing task with the same
scientific work key, even if its carrier or interface changes, an already
discharged objective, unresolved actual start inputs, a reviewed scoped no-go or
live WIP overflow. Changing a task name or interface does not make its question
independent. CONTROL assigns a new work key only when the exact question and
parent consumer are genuinely different. A different interface still needs
explicit transport maps and pinned proof before a result can be substituted. A
bounded independent verification uses explicit `mode: verification`; it still
needs registration, inputs and capacity.

Only `start_requires` gate an otherwise independent conditional lemma's start.
Logical method requirements gate acceptance. A negative existence result is
never a satisfied positive existence input. An obstruction is recorded with
its exact scope and reopening condition. A genuinely different question gets a
new scientific work key and named consumer. Reopening the same scoped question
requires `reopens.attempt` and the actual hypothesis/scope `delta`; changing a
task label or carrier/interface alone does not reopen the old question.

## Record a result and its actual use

```bash
python3 tools/gr_assembly.py template TASK-ID
python3 tools/gr_assembly.py check
python3 tools/gr_assembly.py application-digest APPLICATION-ID
```

Use the template in the existing result/intake workflow; fill it into
`applications.json`. It is a skeleton, not evidence. The result needs a full
published commit, source path, SHA-256, proof kind, scope level, exact statement
and every remaining named hypothesis. Read the pinned owner rather than a chat
summary. A frozen source copy may preserve bytes from a research branch; record
its real published origin and verify that origin at intake.

An application identifies its result, target obligation, proof method and exact
parent substitution location. Map every hypothesis by one of these means:

- `obligation`: an actual required result, which must be discharged;
- `evidence`: a pinned proof of this hypothesis;
- `target_hypothesis`: a named condition already quantified in the exact scoped
  conclusion, such as the endpoint theorem's declared smooth pencil;
- `assumption`: a still-open premise, which keeps the application conditional.

Target hypotheses describe the theorem's declared mathematical domain. They
must not smuggle in physical admission, a selected action, or the Einstein
equation. A universal physical conclusion cannot silently inherit a restricted
or conditional proof. The reviewer checks that distinction.

If interfaces differ, provide a pinned transport proof and explicit maps for
carrier, action, variations, source, normalization, refinement and scope. The
same carrier with a different action is not compatible automatically. A finite
certificate cannot fill a refinement-uniform family premise. A passport cannot
fill an internal premise. A classification target may consume a scoped no-go;
that does not discharge the positive GR goal.

The digest command prints the exact acceptance marker. An independent reviewer
records it in the existing parent/intake artifact, on a published fixed commit:

```text
Assembly-Acceptance: APPLICATION-ID DIGEST
```

Then set the application review to `accepted`, with that reviewer, digest and
the decision's full ref/path/SHA-256. The reviewer differs from the result owner.
The marker binds the statement, method, interfaces, maps, source evidence,
quantifiers, hypothesis map and exact consumed prerequisite contracts. Changing
any of these requires a new decision. An unrelated unused alternative method
does not invalidate the existing proof.
Rejected/proposed applications do not close anything. Ordinary prose changes
outside the bound contract do not manufacture a new scientific result.

All inputs of one method are required together; alternative methods are OR
branches. Multiple accepted proofs may supply the same obligation. Accepted
conditional applications retain their open assumptions. Machine validation
checks the declared contract and immutable evidence, while mathematical
applicability and the truth of a transport remain the reviewer's responsibility.

Retirement and Ready PR validation require a complete scoped terminal submission
for every original completion premise. Proposed applications can satisfy this
submission check, with all inputs supplied and no remaining extrinsic physical
assumption. This lets a review candidate reach Ready for final replay and
independent acceptance. Submission readiness never discharges a scientific
premise or goal. CONTROL checks the pinned acceptance before scientific delivery
and parent use. A useful reviewed slice may be consumed while its parent PR
remains open; the original raw terminal still prevents retiring that parent on
an intermediate positive construction.

## Prior attempts and input changes

`search` indexes result statements, hypotheses, owners and pinned evidence paths
without printing accumulated verification prose. `attempts` also searches the
exact typed question and its assumptions, alongside the reported scope; historical
entries require a typed intake before automatic enforcement. A new typed attempt
in `applications.json` names the exact work key/interface, negative result, scope
and reopening condition.
Its independent acceptance uses the same pinned marker/digest discipline.
The intake template supplies the readable scientific question and its digest;
include both in an attempt. A reviewed obstruction applies to that frozen
question. Use `application-digest ATTEMPT-ID` to obtain its acceptance marker.

```bash
python3 tools/gr_assembly.py impact --base origin/main --ref HEAD
```

`impact` reuses `research_input_closure.select` for changed scientific files,
transitive inputs and unknown dependencies. It identifies applications whose
pinned result source or snapshot, acceptance decision, route input or named
parent consumer changed, so CONTROL can review compatibility and refresh any
affected provenance. Old pinned theorems do not become false because a new
version is proposed. Selection is not replay: the query never executes
certificates or rewrites receipts.

`potential_downstream` counts reachable obligations;
`newly_ready_if_proved` assumes the specified output and checks the actual AND
inputs/OR methods. Neither is a probability, a claim that proof will succeed,
or authorization to auto-dispatch. Prefer a ready intake or a decisive premise
with a named consumer; keep independent work moving.

## Verify a change

```bash
python3 tools/test_gr_assembly.py
python3 tools/gr_assembly.py check
python3 tools/gr_assembly.py render
python3 tools/gr_assembly.py render --check
python3 tools/validate_agent_protocol.py
```

The CI guard covers graph cycles, missing references, stale source/acceptance
hashes, all hypothesis bindings, outcome/scope mismatches and generated-view
drift. Fixture controls cover duplicate execution, WIP, live lookup failure,
independent conditional work, retirement bypass and read-only behavior.
Scientific certificates and Lean are replayed only under the existing
change-based validation budget.

Measure usefulness by bounded lookup cost, time from result publication to
actual substitution, avoided repeated attempts and the cost of maintaining an
intake. Node, document and PASS counts are not scientific progress. Do not add
a recurring audit or a second task scheduler to maintain this layer.
