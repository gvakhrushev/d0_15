# WRK-A4D-LABELLED-PATH-HOLONOMY-DESCENT

## Class

WORKER

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Start gate

SATISFIED on current `main` after merged PR #107, PR #108 and PR #103.

Read completely:

- `02_REGISTRY/research/MEMO_A4D_PATH_GROUPOID_CROSSED_MATTER_LIFT.md`;
- `03_FORMALIZATION/D0/Geometry/ArchivePathWordAlgebra.lean`;
- `03_FORMALIZATION/D0/Geometry/ArchiveAffineCartanConnection.lean`;
- `03_FORMALIZATION/D0/Geometry/ArchiveExteriorPathTransport.lean`.

## Objective

Lean-own the **slot-faithful labelled-path descent theorem** that PR #107 deliberately left theorem-ready.

The existing theorem

`pathEval_factors_pairGroupoid_iff_trivial_holonomy`

is literal ownership for `ChainPath E` with a Prop-valued edge relation. It must remain untouched in scope.

The new owner must work on the archive's literal labelled step words

```text
List ChainStep
```

so that at `L=2` the parallel labels `.fwd r` and `.bwd r` are not identified merely because they have the same ordered endpoints.

## Mandatory results

### 1. Generic labelled transport evaluator

For a generic family of invertible positive edge transports, define/equivalently package evaluation on

```text
(x, steps : List ChainStep)
```

with source `x` and target `pathEnd N steps x`.

Negative steps must be the shifted inverse of the positive edge.

Do not specialize this theorem to the physical constitutive link.

### 2. Exact append and reverse

Prove the literal pull-order laws for:

- empty word;
- append;
- reversed word with `reverseStep`;
- inverse transport.

Reuse existing path conventions exactly.

### 3. Labelled endpoint-descent iff trivial labelled holonomy

Prove the slot-faithful analogue:

```text
all labelled paths with the same source/target evaluate equally
iff
every labelled loop evaluates to identity.
```

The proof may reuse the cancellation pattern of PR #70, but it must be a new theorem over the labelled step carrier.

### 4. Explicit L=2 collision boundary

For `N=0`, prove that `.fwd r` and `.bwd r` from the same site have the same endpoint but remain distinct step labels.

Derive from endpoint descent the required local length-two period law for the positive edge:

```text
ell(x,r) * ell(x+r,r) = 1
```

in the repository's actual pull-order convention.

This is the key reason for this task.

### 5. Finite-torus presentation

If short and natural with the existing path lemmas, package a theorem that labelled plaquette relations plus four fundamental period relations imply trivial labelled loop holonomy.

If this requires a large new combinatorial normal-form development, stop after the exact iff and the explicit L=2 period consequence; record the finite presentation as a theorem-ready follow-up rather than faking it.

## Truth firewall

Do not claim:

- PR #70 already owns the labelled L=2 theorem;
- trivial holonomy for the actual missing matter link;
- existence of the affine-sensitive constitutive link;
- endpoint descent on generic curl/harmonic backgrounds;
- Spin, stress, Einstein, physical time, or golden/phi statements.

This is a generic path theorem.

## Suggested module

`D0/Geometry/A4DLabelledPathHolonomyDescent.lean`

Prefer importing and reusing `ChainStep`, `pathEnd`, `reverseStep` and existing append/reverse infrastructure.

## Validation

Narrow build first, then one final D0 build and normal repository guards.
No `sorry`, no new axiom.

## GitHub-first flow

1. fresh branch from current `main`;
2. `python tools/task_lifecycle.py start WRK-A4D-LABELLED-PATH-HOLONOMY-DESCENT`;
3. open Draft PR immediately before source edits;
4. implement and validate;
5. before Ready self-retire the task;
6. set `Lifecycle: REVIEW`;
7. Ready for review;
8. do not self-merge.

## Exit condition

The labelled `List ChainStep` path evaluator has exact append/reverse and endpoint-independence iff trivial labelled holonomy, with the `L=2` parallel-slot collision and its length-two period consequence Lean-owned without conflating it with the older Prop-edge theorem.
