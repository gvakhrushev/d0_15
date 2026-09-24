# WRK-A4D-OBSERVER-FRAME-CAR-LIFT

## Class

WORKER / FORMALIZATION

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Start gate

Do NOT start until:

1. a WORKER slot is free;
2. `EXP-A4D-SOLDERED-CREATOR-OBSERVER-FRAME-LIFT` has a terminal memo;
3. CONTROL selects the exact theorem-ready subset of that memo.

## Objective

Formalize the independently derived exterior/frame lift on the existing 16-state CAR/Fock carrier.

Do not invent the missing construction if the EXP terminal is negative.

Likely modules, conditional on research:

```text
D0/Geometry/ArchiveExteriorFrameLift.lean
D0/Geometry/A4DObserverPositiveExteriorPairing.lean
D0/Geometry/A4DSolderedCARTransport.lean
```

## Metric-star/signature boundary package

This worker also absorbs the common-fiber boundary from the located-star memo; no separate worker is required.

Suggested module: `D0/Geometry/A4DMetricStarSignatureBoundary.lean`.

Formalize:

- the compound/Jacobi complementary-minor identity on one nondegenerate Lorentz fiber;
- the flat Lorentz exterior-star coefficient `epsilon(S) * eta_S`;
- the Lorentzian double-star sign `(-1)^(k*(4-k)+3)`;
- degree-one flat Lorentz metric form is eta, not counting I;
- a purely pointwise coefficient operator cannot have the accepted neighboring scalar first derivative;
- a centered-solder pointwise version is additionally blind to the existing L=2 Nyquist witness.

This is a signature/pointwise boundary theorem, not the physical located star.

## Mandatory baseline package if research is positive

- exterior lift `ρ(Λ)=⊕ Λ^k` in the subset basis;
- group law;
- covariance of `c†(v)` and `c(α)`;
- observer form
  [
  h_n=-η+2(ηn)(ηn)^T;
  ]
- positivity for `η(n,n)=1`;
- `n=e_A` gives counting `I`;
- rational boost covariance with transformed observer;
- local sitewise frame action with sites fixed.

Additional moving-creator/link theorems must follow the EXP terminal exactly.

## Truth boundaries

Do not call the exterior representation a Dirac-spinor representation.

Do not identify `n=e_A` with physical causal time.

Do not select nonlinear `Q(e)` unless separately proved.

Do not claim existing fixed-creator connection covariance covers rotating CAR links unless the required compatibility theorem is proved.
