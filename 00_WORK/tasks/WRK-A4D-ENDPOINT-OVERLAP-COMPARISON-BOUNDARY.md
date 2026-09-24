# WRK-A4D-ENDPOINT-OVERLAP-COMPARISON-BOUNDARY

## Class

WORKER / FORMALIZATION

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Start gate

SATISFIED.

Primary durable packet:

`02_REGISTRY/research/MEMO_A4D_ENDPOINT_COMPARISON_JET_OVERLAP_LAW.md`.

Frozen formal inputs include:

- PR #70: `ArchiveAffineCartanConnection`, `ArchivePathWordAlgebra`;
- PR #75: complete flat first jet / flux-energy kernel;
- PR #76: located topological `J`;
- PR #80: second-order congruence and scalar advective package.

This worker formalizes the theorem-ready **boundary** from PR #84. It does not construct the missing constitutive path-word law `C_N`.

## Objective

Lean-own the strongest exact content of the endpoint/overlap terminal:

1. one unlabelled invertible center factorization forces trivial loop transport;
2. nontrivial owned relative holonomy therefore obstructs that scoped class;
3. the mandatory scalar distance-two comparison constraints are algebraically soluble;
4. an explicit constants-preserving two-edge `S_patch` satisfies the L=5 delta and non-delta controls;
5. a continuous nearest-neighbor correction family preserves the mandatory entries, proving nonselection.

Terminal target:

`ENDPOINT-OVERLAP-COMPARISON-BOUNDARY-LEAN-OWNED`.

This terminal does **not** mean the missing path-resolved comparison/action exists.

## Mandatory packages

### 1. `A4DUnlabelledCenterHolonomyNoGo.lean`

Formalize a typed abstract center-factorization class sufficient for the memo theorem.

For endpoint fibers/maps, prove:

- endpoint transport from center quotients;
- reversal;
- center-gauge left action leaves endpoint quotients unchanged;
- overlap map independence when two shared endpoints reproduce the same transport;
- cyclic loop telescoping to identity;
- scoped no-go: a specified nontrivial loop/relative holonomy cannot admit such an unlabelled single-center factorization.

Where practical, connect the abstract theorem to the existing PR #70 path-word holonomy owner rather than reimplementing path algebra.

Do not turn this into a universal local-matter no-go.

### 2. `A4DScalarComparisonPatch.lean`

Formalize the scalar two-edge bilinear comparison witness from the memo.

Required properties:

- bilinear in the two coframe inputs;
- symmetric in those inputs;
- symmetric matrix output for the displayed witness;
- translation covariance on the scalar cycle;
- constants preservation / row-sum zero;
- support restricted to the stated two-edge patch;
- exact mandatory distance-two entries.

Formalize the complete L=5 delta witness and L=5 non-delta witness with `G^2 != 0`.

Use exact rational arithmetic. If the final finite matrices are already independently certified, `native_decide` is acceptable under the repository pattern.

### 3. `A4DComparisonJetNonselection.lean`

Formalize a one-parameter nearest-neighbor correction family corresponding to the memo's edge-Laplacian freedom.

Prove:

- constants are still preserved;
- mandatory distance-two entries are unchanged;
- at least two parameter values give distinct comparison jets;
- therefore the stated scalar support/composition constraints do not select a unique `S`.

This is a nonselection theorem inside the stated family, not a universal nonuniqueness theorem for every geometric law.

### 4. `A4DPathResolvedComparisonBoundary.lean`

Package the formal boundary against the existing path-word owner:

- endpoint-only factorization collapses loops;
- owned path-word endpoint reduction is valid only under trivial loop holonomy;
- nontrivial relative holonomy forces path information to remain present.

Do not define a physical matter action `C_N`.
Do not duplicate the observer worker's exterior path-transport implementation.

Optional exact hostile controls from the memo, if cleanly theorem-ready:

- arithmetic path averaging fails reversal/inversion on the displayed 2x2 example;
- fixed Role ordering fails an equivariance witness when the two square paths differ.

## Non-overlap with current workers

This worker owns only the PR #84 terminal algebra/boundary.

It must not edit or own:

- `ArchiveExteriorFrameLift.lean`;
- `A4DObserverPositiveExterior.lean`;
- `ArchiveAffineExteriorLink.lean`;
- `ArchiveExteriorPathTransport.lean`;
- the new research law `C_N(w;e,n)`.

The observer/frame worker owns the exterior transport substrate.
The EXPENSIVE path-word task owns the missing constitutive law.

## Truth firewall

Do not claim:

- universal local-matter no-go;
- unique `S`;
- universal `K`;
- all-order energy/action;
- observer/frame selection;
- metric interpretation of `J`;
- golden refinement;
- stress/Einstein closure.

## Lean throughput

Use the GitHub-first execution contract.

1. fresh branch from current `main`;
2. `python tools/task_lifecycle.py start WRK-A4D-ENDPOINT-OVERLAP-COMPARISON-BOUNDARY`;
3. immediately open Draft PR before Lean edits;
4. use narrow builds only while iterating;
5. one final `python tools/lean_task_build.py final`;
6. run repository validators / no-sorry / generated-view checks;
7. `#print axioms` principal capstones;
8. self-retire task in the same PR;
9. Ready with `Lifecycle: REVIEW`;
10. do not self-merge.

No `lake clean`, no `sorry`, no `sorryAx`, no new axioms.

## Exit condition

The task is complete when the scoped center-holonomy no-go, exact `S_patch` witnesses and the explicit nonselection family are Lean-owned, with a clean boundary leaving the path-resolved constitutive action to research.
