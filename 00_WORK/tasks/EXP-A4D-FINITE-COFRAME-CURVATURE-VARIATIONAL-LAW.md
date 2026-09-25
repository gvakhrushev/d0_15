# EXP-A4D-FINITE-COFRAME-CURVATURE-VARIATIONAL-LAW

Class: `EXPENSIVE`
Parent: `CTRL-A4D-VARIATIONAL-FRONTIER`
Mode: research-only, theory-first.

## Central question

Determine whether the already-owned D0 structures force a finite variational law
[
S[e,mathscr A]=sum_clangle mathfrak B_c(e,F),mathfrak C_c(P(mathscr A))angle
]
or whether action selection requires a genuinely new axiom/principle.

## Frozen inputs

1. Shared-F mixed sector:
   [
   P^{mix}_{rs}=F T_{Omega_{rs}}F^{-1},qquad
   Omega_{rs}=kappa_r+	au_rkappa_s-	au_skappa_r-kappa_s.
   ]
   Its local even plaquette curvature is exactly zero.

2. Independent affine carrier:
   [
   P^{aff}_{rs}=T_{Theta_{rs}}ho(Lambda_{rs}),
   ]
   with the exact finite `Theta` and `Lambda` formulas from
   `MEMO_A4D_MIXED_LETTER_PLAQUETTE_CURVATURE.md`.

3. Under affine base-frame change `(c,E)`,
   [
   Lambdamapsto ELambda E^{-1},qquad
   Thetamapsto ETheta+(I-ELambda E^{-1})c.
   ]

4. Ordinary polynomial trace/character actions erase the translation block.

5. Existing locality/gauge/symmetry assumptions admit inequivalent finite actions with inequivalent Hessian spectra, so curvature alone does not select operator shape.

## Required work

### A. Typing audit

Classify each required datum as `OWNED-AND-CANONICAL`, `OWNED-BUT-NOT-LINKED`, `MULTIPLE-CHOICES`, or `MISSING`:

- coframe carrier;
- orientation/internal epsilon data;
- primal/dual cells and dual area;
- curvature representation and dual;
- fibre transport;
- finite cell product/wedge;
- measure/top-cell sum;
- Riesz/pairing;
- admissible variations;
- nondegenerate flat coframe;
- odd/translation curvature treatment.

Matching dimensions do not count as a map.

### B. Candidate coframe-curvature pairing

Attempt to construct the finite analogue of the two-coframe-leg insertion from owned carriers only. Prove exact covariance and transport typing. Do not import continuum wedge notation as a definition.

### C. Curvature extraction

Classify equivariant extractions from group-valued holonomy: `P-I`, antisymmetric projection, local logarithm, representation differential, and any already-owned projection. State domain, range, covariance, locality and branch restrictions.

### D. Odd sector

Determine whether existing degree-dual/Riesz data can see `Theta` invariantly. A naive `||Theta||^2` is not acceptable when `Lambda != I`. If an affine section or coframe contraction cancels origin dependence, derive it; otherwise prove the obstruction.

### E. Action-selection classification

Classify all competing lowest-order invariant finite actions allowed by the same owned principles. In particular test independent curvature-square, translation-square, volume and parity-odd additions. Determine whether operator shape is unique up to one overall normalization.

### F. Nondegenerate flat background and Hessian

If a candidate survives, identify an admissible stationary `e0 != 0` and derive the complete quadratic block Hessian in `(h,a,...)`. Separate gauge, harmonic, algebraic constraint and physical directions.

### G. L=3 physical pressure test

If action selection is positive, compute exact physical coframe Hessian spectra at
[
p_1=(2pi/3,0,ldots),qquad
p_2=(2pi/3,2pi/3,ldots)
]
after legitimate connection elimination and gauge/constraint reduction. No hand-inserted Laplacian.

## Mandatory negative controls

- remove orientation;
- remove inter-fibre transport;
- construct a competing invariant;
- add an allowed R^2 term;
- ordinary trace blindness to `Theta`;
- affine-origin shift with nonzero `c`;
- zero-coframe Hessian;
- nondegenerate-background stationarity;
- two-momentum comparison;
- hand-inserted Laplacian rejection.

## Verdict

Return exactly one:

- `VARIATIONAL-LAW-FORCED`
- `VARIATIONAL-LAW-FORCED-UP-TO-FINITE-FAMILY`
- `ACTION-SELECTION-NEW-AXIOM-REQUIRED`
- `COFRAME-CURVATURE-PAIRING-NOT-TYPABLE`

If a finite family survives, give its dimension and basis. If a positive action survives, return the exact L=3 physical spectrum in the same packet.

## Forbidden scope

No Lean. No GitHub mutation. No Einstein equation import. No fitted coefficients. No golden-ratio phenomenology. No new 2-cocycle. No continuum limit before the finite Hessian. No claim that `Theta` is torsion without a typed coframe derivative map.

## Exit condition

The finite action-selection problem is terminally classified by one verdict, with a complete typing/uniqueness argument and, if positive, an exact L=3 physical Hessian spectrum derived from the selected action.
