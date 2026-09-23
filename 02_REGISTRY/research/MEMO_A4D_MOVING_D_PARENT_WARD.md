# Moving differential, path-Hodge stabilizer, and mixed parent Ward

## Status

Lean ownership for `WRK-A4D-MOVING-D-HODGE-OBSTRUCTION-PARENT-WARD`, on the graded differential, primal/dual, Hodge-boundary, and Ward half of the path-word Cartan/Hodge parent synthesis.

Primary verdict: `MOVING-D-PRIMAL-DUAL-PARENT-WARD-OWNED`.

Secondary verdicts:

- `COEFFICIENT-CURVATURE-SQUARE-OWNED`
- `HODGE-PATH-STABILIZER-CRITERION-OWNED`
- `FULL-SCALAR-CLOSURE-FIXED-HODGE-NOGO`
- `CENTERED-METRIC-ONLY-HODGE-NOGO`
- `FLAT-FIRST-JET-NONLINEAR-HODGE-NONUNIQUENESS`

Retained verdict: `HODGE-CONSTITUTIVE-PRIMITIVE-REQUIRED`.

## What is owned

`dConn_sq_eq_curvature` writes `d_Ω²` as `L²` times the strict creator sum of transport commutators. `dConn_sq_apply_eq_curvature` evaluates `[T_r,T_s]ψ(x)` as the open-path curvature acting at `x+r+s`. Vanishing open-path curvature implies `d_Ω² = 0`. The converse is not claimed.

`movingDifferential` is `d'_k = Q_{k+1} ∘ d_k ∘ Q_k⁻¹` for supplied linear equivalences. Composition, curvature conjugation, and preservation of an already-vanishing square are proved. The infinitesimal law is the formal identity `δd_k = G_{k+1} d_k - d_k G_k`, with the quadratic remainder kept. Nilpotency of a covariant differential is not assumed.

A perfect pairing forces one dual equivalence of a primal equivalence. In dot-product coordinates that dual is inverse transpose. `movingHodge` is passive covariance of a supplied map. `fixesHodge` is the stricter condition that the supplied map is unchanged. Those agree only on the stabilizer of that map. Neither statement selects a constitutive kernel.

Path dressing of a supplied seed agrees for two transports if and only if their relative holonomy stabilizes the seed. For a supplied family, dressing is path-independent if and only if every relative holonomy lies in that stabilizer. Nonzero curvature is not a hypothesis and is not claimed to force Hodge ambiguity. An orientation-preserving pair preserves the seed while a shear pair does not.

The algebraic scalar closure `{G | G 1 = 0}`, for at least two points and characteristic not 2, admits no nonzero fixed bilinear kernel. This hypothesis is stated directly and does not depend on a Lie-closure theorem.

Constant commuting translations have vanishing plaquette commutators and a nontrivial full-cycle period. Contractible flatness stays separate from global period triviality.

On the 3-cycle the accepted staggered tangent of `e = Δ δ_0` has an off-diagonal entry, so no pointwise multiplication kernel realizes it. At period 2 the centered solder metric of the Nyquist coframe is the flat Lorentz matrix for every scale, while the one-form component changes with that scale. A readout of the centered solder metric alone cannot match that component. The flat value and the linear coefficient of `I + t H + α t² H²` do not determine `α`.

The exact finite moves of `d_P`, `d_D`, `S_0`, and `S_1`, with the dual equivalences forced by the pairings, send the mixed constraint by the top dual equivalence and preserve the inverse-free mixed action. The infinitesimal identity keeps every product-rule term and gives `δC = H_4 C` and `δA = 0` from pairing compatibility. Setting both differential variations to zero recovers the previous fixed-chain Ward. A rational witness shows that dropping those differential terms breaks the identity. Promotion to a background action is conditional on hypotheses that the four operator transformations come from that action and its symmetry.

## Remaining primitive

The missing package is an independently constructed graded discrete constitutive energy/Hodge kernel on the full uncentered geometric/cell carrier, plus dual-cell placement/pairing data, and path-dressing provenance whenever holonomy leaves its stabilizer.

That is narrower than a missing Hodge star. This memo does not construct the kernel.

## Stress boundary

`movingWard_keeps_independentFieldEuler` records that a cancelled parent scalar leaves the sum of an independent connection Euler term and a constitutive Euler term. It is not a divergence theorem. `A4DParentWardStressDescent` still requires the auxiliary and coframe equations. `∇ · T = 0` is not concluded.
