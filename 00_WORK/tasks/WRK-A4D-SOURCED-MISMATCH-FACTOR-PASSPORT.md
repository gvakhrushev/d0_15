# WRK-A4D-SOURCED-MISMATCH-FACTOR-PASSPORT

## Class
WORKER

## Parent
`CTRL-A4D-EQUIVARIANT-MIXED-BACKGROUND-CLOSURE`

## State
PLANNED

## Goal

Lean-own the sourced mismatch factorization from the landed relative A/e and sourced-diagonal stack:

[
oxed{kappa(x,r)=L_{x,r}(R_r(y)+h_r(y))}
]

under the sourced ansatz (delta=a+h), with literal source/predecessor indices and pull order.

## Research / formal inputs

Reuse, do not re-prove:

- `D0.Geometry.A4DConditionalSourcedDiagonalTransport` (#125);
- `D0.Geometry.A4DRoleOverlapTwistedCocycle`;
- landed relative A/e comparison owners.

Expected algebraic chain includes the already-researched identities
(ho=a-R), (kappa=L(delta-ho)), and hence (kappa=L(R+h)).

## Preferred module

`03_FORMALIZATION/D0/Geometry/A4DSourcedMismatchFactorPassport.lean`

## Required theorem surface

Own clear named theorems for:

- predecessor torsion / predecessor defect relation;
- (kappa=L(delta-ho));
- (delta=a+hRightarrowkappa=L(R+h));
- a direct passport alias exposing the boxed factorization.

Keep all orientations and indices explicit.

## Firewalls

No new (J) selector, no finite dressing, no (A=A(e)), no stress/Einstein/continuum/time/golden, no new axioms, no `sorry`.

## GitHub-first

Fresh current main; lifecycle start; lifecycle-only commit; Draft PR before Lean edits; port/reimplement the previously tested module; narrow build + `D0.All`; regenerate views; self-retire before Ready; do not self-merge.
