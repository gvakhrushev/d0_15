# WRK-A4D-OBSERVER-FRAME-CAR-LIFT

## Class

WORKER / FORMALIZATION

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Start gate

Research gate is SATISFIED with terminal:

`FRAME-LIFT-CONSTRUCTED-STAGGERED-JET-MISSING`

This worker is READY when a WORKER slot is assigned.

The located-star API is accepted on current `main` via merged PR #76, so the located-frame compatibility theorem is unblocked.

Durable research packet: `02_REGISTRY/research/MEMO_A4D_SOLDERED_CREATOR_OBSERVER_FRAME_LIFT.md`.

The missing `A4DSolderedCellEnergyJet` is NOT part of the positive formalization. Do not define the target `H(e)` coefficients as an axiom merely to close the worker.

## Three-star dictionary — keep these objects distinct

| Name | Meaning |
|---|---|
| `J` | Two-color center-matched primal/dual placement/pairing. Topological complement sign `(-1)^(k*(4-k))`. In 4D it preserves Fock parity. It is not a metric constitutive selector. |
| `h_n` / metric `*_eta` | Observer/Lorentz metric structure. The Lorentzian double-star carries the additional signature exponent `q=3`. This is not cell placement. |
| scalar reverse-star | A one-color local inverse/reverse stencil used only in the scoped two-sided-locality no-go. It is neither `J` nor the Lorentz metric star and it does not select `Q(e)`. |

Never transfer a theorem or no-go from one row to another without an explicit typed bridge.

## Objective

Formalize the independently derived exterior/frame lift on the existing 16-state CAR/Fock carrier.

The EXP terminal is positive for the exterior/observer/link construction and negative only for deriving the complete staggered cell-energy jet. Formalize exactly the positive subset below; do not extend it into the missing cell-energy law.

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

## Accepted theorem-ready packages

1. `ArchiveExteriorFrameLift.lean`
   - exterior lift by minors on the existing 16-state carrier;
   - identity/composition/inverse/degree preservation;
   - creator and algebraic contraction covariance;
   - explicitly NOT a Spin representation.

2. `A4DObserverPositiveExterior.lean`
   - `h_n=-η+2 n^♭⊗n^♭`, positivity for unit timelike `n`;
   - `n=e_A` gives counting only as a reference observer gauge;
   - all-degree exterior congruence and observer adjoints;
   - exact rational A/B boost control.

3. `A4DRawSolderFrameAction.lean`
   - raw row/covector and vector conventions;
   - local frame action on uncentered solder;
   - exact centered-frame defect and transported-center repair;
   - preserve the raw Nyquist field independently.

4. `ArchiveAffineExteriorLink.lean`
   - Lorentz-restricted lift of the linear part of PR #70 pull links;
   - same-CAR-fiber creator/contraction intertwining;
   - covariant finite differential with flat limit `dForward` and `D_H`;
   - keep affine translation action on the coframe separate;
   - separate link curvature from nonparallel-solder terms.

5. `A4DLocatedFrameCompatibilityBoundary.lean`
   - when the located-star API is available, prove the common-fiber cofactor identity;
   - prove the explicit shifted-anchor obstruction to a naive sitewise Lorentz action on both colors;
   - do not modify the located placement `J`.

Do NOT formalize `A4DSolderedCellEnergyJet` as solved. The terminal explicitly says that common-center/half-edge cell energy and the full staggered first jet are still missing.
