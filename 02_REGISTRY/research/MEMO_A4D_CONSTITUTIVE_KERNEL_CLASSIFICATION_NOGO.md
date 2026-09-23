# Constitutive kernel classification, selector missing

Verdict: `CONSTITUTIVE-KERNEL-FAMILY-CLASSIFIED-SELECTOR-MISSING`.

Secondary:

- `RADIUS-ONE-WARD-NULL-SPACE-DIM-24`
- `ROLE-RELABEL-INVARIANT-WARD-MODULUS-DIM-1`
- `FULL-GRADED-HODGE-RADIUS-ONE-NOGO`
- `NONLINEAR-CONSTITUTIVE-MODULI-OWNED`
- `FLAT-FIRST-JET-NONLINEAR-SELECTOR-NOGO`
- `HOLONOMY-STABILIZER-COMPATIBILITY-NOT-CONNECTION-UNIQUENESS`

Retained:

- `GEOMETRIC-DUAL-CELL-PLACEMENT-PRIMITIVE-REQUIRED`
- `LOCAL-GRADED-ENERGY-DENSITY-SELECTOR-REQUIRED`

The three statements that must stay separate are:

1. Inside the explicit radius-one scalar ansatz, for `L ≥ 4`, the pure-gauge Ward identity leaves a 24-dimensional self-adjoint class. Simultaneous Role relabeling leaves a 1-dimensional subspace. That relabeling is not local Lorentz covariance.
2. A derivative supplied on every uncentered coframe is fixed by extensionality. That is not a geometry-derived uniqueness theorem.
3. The polynomial family `I + H + α H²` shares the flat value `I` and the first jet `H`, and for `α > 1/4` it is positive as a counting quadratic form. It does not select `α`. Counting positivity is not a Lorentzian Hodge statement.

`L ≥ 4` stays on the group-algebra curl classification and on the 24-dimensional count. At `L = 2` a group syzygy can carry a minus-diagonal coefficient. At `L = 3` it can carry a plus-diagonal coefficient. Research Gaussian nullities 26, 10, and 6 are not stated as operator dimensions.

The graded no-go is an `L = 3` corner: `U_s A_r` against `e = L(U_s - I)δ` has a nonzero matrix entry at toroidal distance 2, so a radius-one matter stencil cannot realize it. `flatStaggeredH` is not on this baseline; the family is stated for a supplied symmetric `H`.

Flat curls `T_rs^b(d_f ξ) = 0` use commuting translations. They are not affine torsion at nonzero curvature.

Edgewise metric compatibility of a supplied seed implies every loop product stabilizes that seed. Two distinct compatible connections exist, one with nontrivial holonomy. The owned rotation and shear theorems remain the stabilizer criterion. Nonzero curvature is not claimed to force Hodge ambiguity.

Determinant density `v = ((det Θ)² - 1)²` is Lorentz-right invariant, flat at first jet, and nonzero on a constant diagonal solder. It is not selected. The nondegenerate solder domain contains the flat coframe and is preserved by right Lorentz action and by relabeling an already evaluated solder matrix. Not every coframe is admissible.

Refinement owners record trace numbers only. They do not contain typed maps `B_P`, `B_D`, and they do not select `α`.
