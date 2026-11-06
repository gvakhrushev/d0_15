import D0.Analysis.MatchedBranchResolventWeights

/-!
# Normalized matched branch price

The exact derivative of the finite return price is composed with the
resolvent trace weights on the same real-parameter curve. The result does not
construct field/action maps, physical admission, a total source or GR recovery.
-/

noncomputable section
namespace D0.Analysis.MatchedBranchReturn

open Filter Matrix D0.Analysis.PositiveMatrixLogDet
open scoped BigOperators Topology Matrix.Norms.Frobenius ComplexOrder MatrixOrder

variable {ι θ : Type*} [Fintype ι] [DecidableEq ι]

/-- The matched branch pencil is the previously used affine history pencil. -/
theorem matched_pencil_eq_affine (A : Matrix ι ι ℂ) (d eta t : ℝ) :
    d • (1 : Matrix ι ι ℂ) + eta • ((t • (1 : Matrix ι ι ℂ)) * A * star (t • (1 : Matrix ι ι ℂ))) =
      affinePencil A d (eta * t ^ 2) := by
  simp only [star_smul, star_trivial, star_one, smul_mul_assoc, mul_smul_comm,
    one_mul, mul_one, smul_smul, affinePencil]
  ext i j
  simp only [Matrix.add_apply, Matrix.smul_apply, Complex.real_smul, Complex.ofReal_mul,
    Complex.ofReal_pow]
  ring

/-- The actual finite return price has the normalized independent-branch
source on the same curve. `gamma` is a signed amplitude coefficient; it is
not assumed positive and may vanish when eta or t is zero. -/
theorem branchReturn_price_normalized_derivative
    (s : Finset θ) (amp : θ → ℝ → ℝ) (proj : θ → ℝ → Matrix ι ι ℂ)
    (damp : θ → ℝ) (dproj : θ → Matrix ι ι ℂ) (p t d eta nu : ℝ)
    (A : Matrix ι ι ℂ)
    (hamp : ∀ i ∈ s, HasDerivAt (amp i) (damp i) p)
    (hproj : ∀ i ∈ s, HasDerivAt (proj i) (dproj i) p)
    (hmatch : ∀ i ∈ s, amp i p = t)
    (hcomplete : ∀ᶠ y in 𝓝 p, ∑ i ∈ s, proj i y = 1)
    (hself : ∀ i ∈ s, star (proj i p) = proj i p)
    (hid : ∀ i ∈ s, proj i p * proj i p = proj i p)
    (hA : A.PosSemidef) (hAne : A ≠ 0) (hd : 0 < d) (heta : 0 ≤ eta) :
    let R := (affinePencil A d (eta * t^2))⁻¹
    let w := (R * A).trace.re
    let pi := fun i => (proj i p * R * A).trace.re / w
    let gamma := 2 * nu * eta * t * w
    0 < w ∧ (∀ i ∈ s, 0 ≤ pi i) ∧ (∑ i ∈ s, pi i) = 1 ∧
      HasDerivAt (fun y => -nu * Real.log
        ((d • (1 : Matrix ι ι ℂ) + eta •
          (branchReturn s amp proj y * A * star (branchReturn s amp proj y))).det.re))
        (-gamma * ∑ i ∈ s, damp i * pi i) p := by
  let R := (affinePencil A d (eta * t^2))⁻¹
  let w := (R * A).trace.re
  let pi := fun i => (proj i p * R * A).trace.re / w
  have hq : 0 ≤ eta * t^2 := mul_nonneg heta (sq_nonneg t)
  have hw : 0 < w := resolvent_history_trace_pos A d (eta * t^2) hA hAne hd hq
  have hweights := normalized_resolvent_branch_weights s (fun i => proj i p)
    A d (eta * t^2) hA hAne hd hq hself hid hcomplete.self_of_nhds
  have hC := (branchReturn_hasDerivAt_matched s amp proj damp dproj p t
    hamp hproj hmatch hcomplete).1
  have hD : d • (1 : Matrix ι ι ℂ) + eta •
      (branchReturn s amp proj p * A * star (branchReturn s amp proj p)) =
      affinePencil A d (eta * t^2) := by
    rw [hC]
    exact matched_pencil_eq_affine A d eta t
  have hRA : R * A = A * R := affine_resolvent_commutes A d (eta * t^2) hA hd hq
  have hraw := branchReturn_price_hasDerivAt_independent_branches_of_psd
    s amp proj damp dproj p t d eta nu A hamp hproj hmatch hcomplete hA hd heta
  have hcoef : ∀ i ∈ s,
      (((d • (1 : Matrix ι ι ℂ) + eta •
        (branchReturn s amp proj p * A * star (branchReturn s amp proj p)))⁻¹ *
        (proj i p * A * star (branchReturn s amp proj p) +
          branchReturn s amp proj p * A * star (proj i p))).trace).re =
      2 * t * (proj i p * R * A).trace.re := by
    intro i hi
    rw [hD, hC]
    exact matched_branch_trace_coefficient (proj i p) R A t (hself i hi) hRA
  have hsum : (∑ i ∈ s, damp i *
      (((d • (1 : Matrix ι ι ℂ) + eta •
        (branchReturn s amp proj p * A * star (branchReturn s amp proj p)))⁻¹ *
        (proj i p * A * star (branchReturn s amp proj p) +
          branchReturn s amp proj p * A * star (proj i p))).trace).re) =
      ∑ i ∈ s, damp i * (2 * t * (proj i p * R * A).trace.re) := by
    apply Finset.sum_congr rfl
    intro i hi
    rw [hcoef i hi]
  refine ⟨hw, ?_, ?_, ?_⟩
  · simpa [pi, w, R, mul_assoc] using hweights.1
  · simpa [pi, w, R, mul_assoc] using hweights.2
  · apply hraw.congr_deriv
    rw [hsum]
    dsimp only [pi]
    simp only [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i hi
    change -nu * eta * (damp i * (2 * t * (proj i p * R * A).trace.re)) =
      -(2 * nu * eta * t * w) * (damp i * ((proj i p * R * A).trace.re / w))
    field_simp [ne_of_gt hw]

end D0.Analysis.MatchedBranchReturn
end
