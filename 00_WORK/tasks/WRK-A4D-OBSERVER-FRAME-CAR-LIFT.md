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
2. `EXP-A4D-SOLDERED-CREATOR-OBSERVER-FRAME-LIFT` has a terminal memo naming exactly one terminal verdict;
3. CONTROL selects the exact theorem-ready subset of that memo;
4. if the selected theorems mention `H(e)` or located pairing types, the required flux/star APIs are merged or explicitly accepted by CONTROL.

## Three-star dictionary — keep these objects distinct

| Name | Meaning |
|---|---|
| `J` | Two-color center-matched primal/dual placement/pairing. Topological complement sign `(-1)^(k*(4-k))`. In 4D it preserves Fock parity. It is not a metric constitutive selector. |
| `h_n` / metric `*_eta` | Observer/Lorentz metric structure. The Lorentzian double-star carries the additional signature exponent `q=3`. This is not cell placement. |
| scalar reverse-star | A one-color local inverse/reverse stencil used only in the scoped two-sided-locality no-go. It is neither `J` nor the Lorentz metric star and it does not select `Q(e)`. |

Never transfer a theorem or no-go from one row to another without an explicit typed bridge.

## Objective

Formalize the independently derived exterior/frame lift on the existing 16-state CAR/Fock carrier.

Do not invent the missing construction if the EXP terminal is negative. In particular, do not invent `rho(Λ)`, a rotating-CAR link law, or an observer pairing that the memo did not justify. If the EXP terminal is a no-go, formalize the no-go/boundary instead.

Do not touch nonlinear `Q(e)` selection in this worker.

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
