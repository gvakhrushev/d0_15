# D0 to GR assembly

Use this layer to find the next missing transition, its current owner and the
results that can actually be substituted into the derivation. The
[scientific route](../research/MEMO_A4D_RESOLVED_AFFINE_PROGRAM.md#current-route-to-general-relativity)
owns the argument. [VIEW.md](VIEW.md) is a generated composition overview.
Claims, proof owners, the work queue and live GitHub execution keep their
existing authorities. No graph label by itself promotes a scientific claim.

## Enter with one relevant query

```bash
# A named task: existing execution, exact interface, assumptions and consumer.
python tools/task_dispatch.py TASK-ID

# Select work: live owners, scoped intake and conditional readiness.
python tools/gr_assembly.py next

# Read only the relevant missing inputs and previous results.
python tools/gr_assembly.py why positive_gr
python tools/gr_assembly.py search source
python tools/gr_assembly.py attempts volume
```

`next` and the dispatcher each obtain one live PR snapshot. Use the one that
answers the current question. An existing Draft is resumed; a Ready PR awaits
review. Offline mode prints **unverified planning** and never authorizes a new
execution. An unavailable live lookup fails closed. These commands do not
reserve a task, create branches, message other agents or change statuses.

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

## Register or revise an execution

CONTROL adds the semantic binding in `contract.json` while registering the
ordinary task. Add exactly one line to its brief:

```text
Assembly: `TASK-ID`
```

The binding records its exact statement, interface version, scientific work
key, named consumer, disjoint write paths, `start_requires`, retained `assumes`
and `completion_requires`. These are scientific interface data, not task
states. Existing classes and WIP limits apply unchanged.

The dispatcher and lifecycle start reject a competing task with the same work
key/interface, an already discharged objective, unresolved actual start inputs,
a reviewed scoped no-go or live WIP overflow. Changing a task name does not make
its science independent. A bounded independent verification uses explicit
`mode: verification`; it still needs registration, inputs and capacity.

Only `start_requires` gate an otherwise independent conditional lemma's start.
Logical method requirements gate acceptance. A negative existence result is
never a satisfied positive existence input. An obstruction is recorded with
its exact scope and reopening condition; a revised question needs an explicit
new interface or scientific work key and its parent consumer. For a changed
question under the same key/interface, record `reopens.attempt` and the actual
hypothesis/scope `delta`; changing a label alone does not reopen the old question.

## Record a result and its actual use

```bash
python tools/gr_assembly.py template TASK-ID
python tools/gr_assembly.py check
python tools/gr_assembly.py application-digest APPLICATION-ID
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

`search` exposes the historical statements, hypotheses and owner paths without
printing accumulated verification prose. `attempts` lists reported negative
results with their original scope; historical entries require a typed intake
before automatic enforcement. A new typed attempt in `applications.json` names
the exact work key/interface, negative result, scope and reopening condition.
Its independent acceptance uses the same pinned marker/digest discipline.
The intake template supplies the readable scientific question and its digest;
include both in an attempt. A reviewed obstruction applies to that frozen
question. Use `application-digest ATTEMPT-ID` to obtain its acceptance marker.

```bash
python tools/gr_assembly.py impact --base origin/main --ref HEAD
```

`impact` reuses `research_input_closure.select` for changed scientific files,
transitive inputs and unknown dependencies. It separately identifies result
applications needing compatibility review against proposed inputs. Old pinned
theorems do not become false because a new version is proposed. Selection is
not replay: the query never executes certificates or rewrites receipts.

`potential_downstream` counts reachable obligations;
`newly_ready_if_proved` assumes the specified output and checks the actual AND
inputs/OR methods. Neither is a probability, a claim that proof will succeed,
or authorization to auto-dispatch. Prefer a ready intake or a decisive premise
with a named consumer; keep independent work moving.

## Verify a change

```bash
python tools/test_gr_assembly.py
python tools/gr_assembly.py check
python tools/gr_assembly.py render
python tools/gr_assembly.py render --check
python tools/validate_agent_protocol.py
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
