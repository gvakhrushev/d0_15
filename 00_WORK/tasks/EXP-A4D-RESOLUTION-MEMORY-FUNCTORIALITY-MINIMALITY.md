# EXP-A4D-RESOLUTION-MEMORY-FUNCTORIALITY-MINIMALITY

## Class
EXPENSIVE / DEEP RESEARCH

## Parent
`CTRL-A4D-EQUIVARIANT-MIXED-BACKGROUND-CLOSURE`

## State
PLANNED

## Start gate
OPEN NOW.

## Read first

Read completely:

- `02_REGISTRY/research/MEMO_A4D_SELECTED_DIAGONAL_RANK_TRANSITION_CONTINUITY.md` (PR #130);
- `02_REGISTRY/research/MEMO_A4D_CLASSICAL_KINEMATIC_INTERFACE_PRESSURE.md` (PR #128);
- landed formal owners from #125, #127 and #129.

Do not reopen the pointwise continuity classification.

## Frozen resolution from #130

Local rank transition is resolved by an orthogonal projector-incidence datum

[
Pi_yinmathfrak P(B_y),
qquad
B_yPi_y=B_y,
]

with the intrinsic projector (P_{(ker B_y)^perp}) only one section.

The global selector seam is resolved by a projector (Q_o) on the appropriate loop-fixed / parallel-kernel fibre.

Package

[
Xi=((Pi_y)_y,Q_o).
]

PR #130 proves that retaining such resolution data makes the selected finite interface continuous, and that no unrestricted globally continuous unresolved selection can preserve the current pure-shift and Nyquist/corner controls.

## Main objective

Determine whether (Xi) can be promoted from "sufficient continuation memory" to a precise **functorial background datum**, and whether it is minimal.

The output must be one of:

- a constructed exact resolution groupoid/functor;
- a sharp minimality classification;
- a terminal obstruction proving that some part of (Xi) is irreducible history/approach memory rather than pointwise geometry.

## Mandatory questions

### 1. Local functoriality

For frame/background changes, derive the exact transport law for

[
(B,Pi)mapsto(B',Pi').
]

Require:

- incidence preservation;
- composition;
- inverse/reverse;
- pure-linear frame covariance;
- compatibility with the relative A/e active-span relation.

Do not silently use a Moore–Penrose convention as physical input.

### 2. Global holonomy-kernel functoriality

For the selected post-source kernel projector (Q_o):

- derive basepoint change;
- path change;
- loop conjugation;
- frame covariance;
- exact composition.

Separate "fixed space as a subspace" from "chosen projector/continuation of that subspace".

### 3. Minimality

Classify all forgetful maps

[
Xi	oXi'
]

that still determine the selected ((delta,kappa)) continuously on every admitted family.

Prove whether (Xi) is minimal up to natural equivalence, or exhibit a strictly smaller sufficient datum.

A dimension/rank label alone is not accepted: #130 already shows Grassmannian direction data matter.

### 4. History reconstruction

Test whether (Xi) is reconstructible from:

- a finite labelled path history;
- the full free-path word;
- a finite parameter jet;
- the current pointwise pair ((A,e)).

PR #130 already rules out universal finite-jet reconstruction. Preserve that firewall.

If history suffices, give the exact reconstruction and equivalence relation on histories.

### 5. Raw-control preservation

Any quotient of (Xi) must retain:

- pure shift;
- L=2 Nyquist;
- L=3 corner;
- exact gauge rank drop;
- the mandatory rank-transition mismatch.

## Required witnesses

At minimum:

- the exact L=3 discontinuity family of #130;
- two approach families with the same endpoint and rank labels but different projector limits;
- two loop families with the same endpoint fixed-space dimension but different limiting fixed subspaces;
- an exact gauge family where resolution is invisible;
- a coframe-only Nyquist/corner family where maximal and intrinsic lifts differ.

## Terminal names

Preferred positive:
`RANK-HOLONOMY-RESOLUTION-GROUPOID-CONSTRUCTED`

Preferred classification:
`RESOLUTION-MEMORY-MINIMALITY-CLASSIFIED`

Preferred no-go:
`POINTWISE-RESOLUTION-RECONSTRUCTION-OBSTRUCTED`

A vague "extra memory is needed" is not sufficient.

## Formalization handoff

End with a small theorem-ready package; do not bury the task in Lean.

## Firewalls

No finite dressing construction, no second-order Hessian/stress, no GR/QFT/time/golden.

## GitHub-first

1. fresh current main;
2. lifecycle start;
3. Draft PR before research edits;
4. one durable memo;
5. exact finite checker;
6. self-retire before Ready;
7. `Lifecycle: REVIEW`;
8. do not self-merge.
