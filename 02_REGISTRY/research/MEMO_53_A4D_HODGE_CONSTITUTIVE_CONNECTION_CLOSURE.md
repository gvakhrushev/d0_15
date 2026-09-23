# MEMO_53_A4D_HODGE_CONSTITUTIVE_CONNECTION_CLOSURE

## Status

Frontier memo after the Lean landing on `work/a4d-hodge-constitutive-connection`, based on `origin/main` `131dbab`.

Primary verdict: `HODGE-CONSTITUTIVE-PRIMITIVE-REQUIRED`.

Secondary: flat Hodge adjoint and parity are Lean-owned; the operator square `D_H^2` is not. Radius-one centered closure, axis-conductance shear, and noncommuting lapse multiplication are no-gos. The mixed parent Ward stays conditional on a supplied constitutive map.

## 0. What this memo does not repeat

The landed modules now own the statements below. This memo only marks the boundary they leave open.

- `D0.Geometry.ArchiveHodgeCARDirac.hodgeCarDirac_self_adjoint`: the counting pairing satisfies `⟨D_H ψ, φ⟩ = ⟨ψ, D_H φ⟩`.
- `D0.Geometry.ArchiveHodgeCARDirac.hodgeCarDirac_parity_odd`: `(-1)^F D_H = -D_H (-1)^F`.
- `hoppingCarDirac` is a public alias of `carDirac`. It is not `hodgeCarDirac`.
- `D0.Geometry.ArchiveHodgeCARDiracSquare.scalarDifferenceLaplacian_apply` and `hodge_difference_diagonal_double_metric_at_l2`: the oriented scalar Laplacian is `L^2 ∑_r (2f(x)-f(x+e_r)-f(x-e_r))`, and at `L=2` its diagonal is twice the undirected metric-graph diagonal.
- `D0.Geometry.ArchiveCARDegreePreserving.carEnd_lie` and `degreePreservingEndomorphismDimension`: `E_sr = c_s† c_r` obeys the stated bracket, and `⊕_k End(F^k)` has dimension 70. That unit group is not a gauge group.
- `D0.Geometry.FinitePrimalDualHodgeParent.mixedPrimalDualWard_invariant`: the inverse-free mixed action is invariant when chain covariance, pairing invariance, and `δ★ = G_D ★ - ★ G_P` are supplied. No physical `★` is selected.
- `D0.Geometry.A4DCenteredCartanClosureNoGo.centered_generator_family_not_closed` and `radius_one_correction_cannot_cancel_distance_two`: on the rational five-cycle, the centered family is not commutator-closed, and a radius-one correction cannot cancel the exhibited distance-two entry.
- `D0.Geometry.A4DMetricStressInterface.symFrobenius_factor_two`: off-diagonal independent coordinates enter with factor two.
- `temporalVariation_reads_same_tensor`: the temporal probe reads `t * Λ_AA` from the same `Λ`.
- `axis_conductance_misses_shear`: a pure `BC` shear is outside every spatial axis-diagonal tensor.
- `symmetric_mul_iff_commute` and `lapseWitness_fails_to_commute`: for symmetric `M,H`, `MH` is symmetric if and only if `MH=HM`; a nonconstant diagonal multiplier fails to commute with a symmetric hop. `symmetrizedProduct_symmetric` is not a physical selection.
- `D0.Gravity.A4DParentWardStressDescent.centeredRoleDivergence_zero_of_parentWard`: centered divergence zero follows when the readout of `df xi` equals `symmetricRoleGradient xi`, and the parent Ward, auxiliary EOM, and coframe EOM are assumed.

## 1. Exact remaining gap

The package that is still not derived is

\[
(\Omega,\ \delta_\xi^{\rm conn}\Omega,\ \mathcal S).
\]

What has been removed from that package:

1. The flat counting operator's adjoint and parity are no longer part of the missing package. They are `hodgeCarDirac`.
2. The `L=2` graph collision is a scalar convention fact, not a missing Dirac primitive. The diagonal identity is proved. The full matrix intertwiner `Δ_diff = Δ_metric` for `L≥3`, and `Δ_diff = 2 Δ_metric` for `L=2`, is not the theorem that landed: only the diagonal comparison at `L=2` is.
3. Three spatial axis conductances cannot be the six-dimensional spatial metric fibre. Witness: `pureShearBC`.
4. A radius-one correction of the centered scalar generator cannot absorb the five-cycle distance-two commutator. A curvature-capable elementary-link law is not a rewrite of that centered family.
5. The 70-dimensional degree-preserving fibre algebra is an upper coefficient envelope. No selector identifies its unit group with `Ω`.
6. The mixed parent action is theorem-ready only with `★`, `δ★`, and the chain generators supplied. Those hypotheses are the constitutive primitive, not a consequence of the parent algebra.

What is still missing inside the flat operator, and is not the constitutive primitive:

\[
D_H^2 = -\sum_r \nabla_r^-\nabla_r^+ \otimes I_{16}
\]

is not a Lean theorem. `dForward_sq_zero` is owned. The codifferential square and the mixed CAR cancellation that turn `dδ+δd` into the fibrewise Laplacian were not closed. Kernel dimension 16 for `D_H`, the rank-96 shell, and `E→2π` stay unproved for that reason. They must not be read off `hoppingCarDirac`.

## 2. Why no constitutive family was selected

The audited classes fail before a family can be named.

- Sitewise axis weights see at most the diagonal spatial slots. `axis_conductance_misses_shear` is the witness. A diagonal constitutive map cannot be the full metric parent.
- The centered Cartan family on the five-cycle is not a radius-one connection law. `radius_one_correction_cannot_cancel_distance_two` blocks the repair that stays inside that support class.
- Nonconstant multiplication does not commute with a symmetric hop, so `M_N H` is not symmetric. Symmetrizing it is an extra choice. `lapseWitness_product_not_symmetric` records the obstruction. It does not choose the symmetrized product.
- `mixedPrimalDualWard_invariant` uses `δ★ = G_D ★ - ★ G_P` as a hypothesis. The theorem does not produce `★ = S(e,n,Ω)`.

No admissible curved family was constructed, so there is no moduli space to classify and no uniqueness theorem to state. Calling any supplied `★` canonical would invent the missing principle.

## 3. Pre-registered attack

The strongest attack on this memo is that the flat square was treated as optional. It is not optional for the massless owner. The attack succeeds against any reading that says phase 1 of the campaign fully landed. It does not revive a constitutive map: even after `D_H^2` is proved, `S(e,n,Ω)` and `δ_ξ Ω` are still not determined by the owned flat counting adjoint.

A second attack is carrier mismatch. `degreePreservingEndomorphismDimension = 70` is the dimension of degree-preserving matrices on the 16-state Fock space. It is not a count of particle species, and it is not the dimension of a selected connection group.

A third attack is the temporal probe. `temporalVariation_reads_same_tensor` shows one slot. It does not by itself project the mixed and spatial slots. Those remain the factor-two identity plus the shear no-go, not three independent stress formulas.

## 4. Reopening hook

The constitutive primitive can be reopened only by an explicit bounded-local family `★ = S(e,n,Ω)` that matches `hodgeCarDirac` at the flat point, sees a pure shear, and satisfies the parent Ward hypotheses already stated in `mixedPrimalDualWard_invariant`. A uniqueness theorem has to be proved from stated premises. A definition that merely fits the flat point does not fire this hook.

The operator square can be reopened separately, without any metric law, by proving `hodgeCarDirac (hodgeCarDirac ψ) = cochainDifferenceLaplacian ψ`.

## 5. Not claimed

No continuum diffeomorphism, no local Lorentz gauge, no identification of the 16 Fock states with particles, no selected rank-96 state, no nonlinear Einstein equation, and no use of `hoppingCarDirac` as the massless owner.
