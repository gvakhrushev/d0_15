# EXP-SM-GAUGE-REPRESENTATION-COMMUTANT

## Class
EXPENSIVE

## Parent
CTRL-REVIEW-SEMANTIC-HARDENING

## State
IN_PROGRESS

## Baseline

Use current `main` at launch. Repository edits: NONE.

## Frozen inputs

The raw 16-state CAR/Fock commutant question is no longer the frontier:

- intrinsic fixed-site CAR commutant is already classified as scalars in the owned lane;
- signed/diagonal Role transport is owned and commutes with the corrected `D_H`;
- Fock number `N` does not commute with `D_H`, while it does commute with `D_H^2`;
- parity anticommutes with `D_H` and commutes with `D_H^2`;
- dimension 70 is the full degree-preserving endomorphism algebra, not a claim that it is the span of CAR bilinears;
- Albert/12-dimensional/anomaly data remain comparisons and frozen ledgers, not definitions of the gauge group.

## New objective

Classify the commutant on the actual archive cochain representation, jointly with the owned dynamics/symmetry:

```math
Comm( D_H , diagonalRoleTransport(S_4) )
```

on `ArchiveCochain`, and separately the corresponding commutant for `D_H^2` where `U(1)_N` is available.

The research question is one precise thing:

> after imposing the corrected Hodge Dirac and the diagonal signed Role action on the full archive cochain carrier, is the intrinsic internal symmetry algebra/group exhausted by the owned diagonal Role image (and, for the square, the number-phase `U(1)_N`), or is there a strictly larger commutant?

Do not start from the 16-dimensional vacuum fiber alone. Site dependence and the translation action of `D_H` are part of the representation.

## Required separations

- distinguish `Comm(D_H, …)` from `Comm(D_H^2, …)`;
- distinguish continuous commutant from the discrete image of `Perm Role`;
- distinguish fixed-site Fock endomorphisms from archive cochain operators;
- distinguish degree-preserving endomorphisms from number-phase symmetries;
- do not identify a larger commutant with the Standard Model unless an actual representation/isomorphism theorem is proved.

## Hostile controls

- fixed-site scalar commutant;
- parity;
- number phase;
- Role-A stabilizer versus full `S_4`;
- shell restriction versus full cochain carrier;
- at least one site-dependent operator that fails to commute with translations.

## Forbidden promotions

- do not derive SM from dimension matching;
- do not use `End(ker D_H) = M_16` as a gauge owner;
- do not call the 70-dimensional degree-preserving algebra a CAR-bilinear Lie algebra;
- do not use Albert projection/anomaly cancellation as the definition of the commutant;
- do not infer particle generations or species from multiplicities.

## Deliverable

`MEMO_52_SM_GAUGE_REPRESENTATION_COMMUTANT.md`

Return one terminal verdict describing the actual joint commutant on `ArchiveCochain` and the square-level enlargement, with theorem-ready Lean handoff if nontrivial.

Repository edits: NONE.
