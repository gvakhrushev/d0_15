# WRK-A4D-RESOLVED-CORRELATED-ACTION-PASSPORT

## Class
WORKER

## Parent
`CTRL-A4D-EQUIVARIANT-MIXED-BACKGROUND-CLOSURE`

## State
PLANNED

## Baseline
Start from fresh current `main`, at least `a14fb1c629766c1bf25fb66c8a00f575cd07d20e`.

## Research owner
Read:

- `02_REGISTRY/research/MEMO_A4D_SELECTED_DIAGONAL_RANK_TRANSITION_CONTINUITY.md` (#130), especially §§27–32;
- `03_FORMALIZATION/D0/Geometry/A4DRelativeAEComparisonSpan.lean`.

Do not reopen topology/continuity research.

## Goal

Lean-own the finite algebraic resolved correlated-action passport.

For synthesis maps

[
B,S:E_{m lab}	o V,
]

reuse the landed coefficient kernel/complement and canonical split

[
C=S P_H,qquad D=S P_K.
]

For a lost-direction subspace

[
Wle K=ker B,
]

use the admissible resolution projector

[
Pi=P_H+P_W
]

and define

[
widetilde C=SPi.
]

## Mandatory theorems

Own exactly:

[
BPi=B,
]

[
oxed{widetilde C-C=D P_W},
]

intrinsic lift (W=ot):

[
widetilde C=C,
]

maximal lift (W=K):

[
widetilde C=S,
qquad
widetilde C-C=D.
]

For Role basis vectors, specialize the maximal jump to the landed Role residual.

## Exact-gauge invisibility

If

[
S=TB
]

and (BPi=B), prove

[
SPi=S.
]

No full-fibre selector is introduced.

## Coframe-only boundary

For (B=0):

- intrinsic lift gives (widetilde C=0);
- maximal lift gives (widetilde C=S).

Add the exact separation theorem for (S
e0).

## Preferred module

`03_FORMALIZATION/D0/Geometry/A4DResolvedCorrelatedActionPassport.lean`

## Firewalls

No sequence limits, Moore–Penrose continuity, cluster projectors, global (Q_o), finite dressing, stress/Einstein, continuum, physical time or golden refinement.

## Validation

No `sorry`, no new axioms.
Run narrow build, then full `D0.All` and repository guards.

## GitHub-first

1. fresh branch from current main;
2. `python tools/task_lifecycle.py start WRK-A4D-RESOLVED-CORRELATED-ACTION-PASSPORT`;
3. commit only lifecycle-generated control-plane changes;
4. open Draft PR before Lean edits;
5. implement / port the already-audited theorem module;
6. validate;
7. self-retire before Ready;
8. `Lifecycle: REVIEW`;
9. do not self-merge.
