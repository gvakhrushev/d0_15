import D0.Analysis.MatchedBranchReturnDerivative
import D0.Analysis.PositiveMatrixLogDet

/-!
# Positive determinant chart for matched branch returns

A positive identity offset and a nonnegative coefficient regularize the
return of any matrix through a fixed positive semidefinite history. Thus the
positive-real determinant hypothesis of the existing matched-branch price
calculus follows for every parameter value, without requiring the branch
return to be self-adjoint. Separately, a real weighted sum of self-adjoint
projectors is self-adjoint. These are finite matrix facts, not physical
admission, a complete physical source, or GR recovery.
-/

noncomputable section
namespace D0.Analysis.MatchedBranchReturn

open Filter
open scoped BigOperators Topology Matrix.Norms.Frobenius ComplexOrder

variable {ι θ : Type*} [Fintype ι] [DecidableEq ι]

/-- Positivity of the affine return pencil, including singular and zero
history, with no self-adjointness condition on the branch return C. -/
theorem return_pencil_posDef
    (A C : Matrix ι ι ℂ) (d eta : ℝ) (hA : A.PosSemidef)
    (hd : 0 < d) (heta : 0 ≤ eta) :
    (d • (1 : Matrix ι ι ℂ) + eta • (C * A * star C)).PosDef := by
  have hgram : (C * A * star C).PosSemidef := by
    simpa only [Matrix.star_eq_conjTranspose] using hA.mul_mul_conjTranspose_same C
  exact (Matrix.PosDef.one.smul hd).add_posSemidef (hgram.smul heta)

/-- The determinant is strictly positive and real, not merely positive in
its real component. -/
theorem return_pencil_det_positive_real
    (A C : Matrix ι ι ℂ) (d eta : ℝ) (hA : A.PosSemidef)
    (hd : 0 < d) (heta : 0 ≤ eta) :
    ∃ q : ℝ, 0 < q ∧
      (d • (1 : Matrix ι ι ℂ) + eta • (C * A * star C)).det = (q : ℂ) := by
  let D : Matrix ι ι ℂ := d • (1 : Matrix ι ι ℂ) + eta • (C * A * star C)
  have hdet : 0 < D.det := (return_pencil_posDef A C d eta hA hd heta).det_pos
  have hreal := Complex.pos_iff.mp hdet
  refine ⟨D.det.re, hreal.1, ?_⟩
  change D.det = (D.det.re : ℂ)
  apply Complex.ext
  · simp
  · simpa using hreal.2.symm

omit [Fintype ι] [DecidableEq ι] in
/-- Real branch amplitudes and self-adjoint component matrices give a
self-adjoint branch return. Idempotence and completeness are not needed. -/
theorem branchReturn_selfadjoint
    (s : Finset θ) (amp : θ → ℝ → ℝ) (proj : θ → ℝ → Matrix ι ι ℂ)
    (y : ℝ) (hproj : ∀ i ∈ s, star (proj i y) = proj i y) :
    star (branchReturn s amp proj y) = branchReturn s amp proj y := by
  unfold branchReturn
  simp only [star_sum, star_smul, star_trivial]
  apply Finset.sum_congr rfl
  intro i hi
  rw [hproj i hi]

/-- The independently varying-branch price derivative on the actual positive
semidefinite-history chart. All previous matched/completeness inputs remain. -/
theorem branchReturn_price_hasDerivAt_independent_branches_of_psd
    (s : Finset θ) (amp : θ → ℝ → ℝ) (proj : θ → ℝ → Matrix ι ι ℂ)
    (damp : θ → ℝ) (dproj : θ → Matrix ι ι ℂ) (p t d eta nu : ℝ)
    (A : Matrix ι ι ℂ)
    (hamp : ∀ i ∈ s, HasDerivAt (amp i) (damp i) p)
    (hproj : ∀ i ∈ s, HasDerivAt (proj i) (dproj i) p)
    (hmatch : ∀ i ∈ s, amp i p = t)
    (hcomplete : ∀ᶠ y in 𝓝 p, ∑ i ∈ s, proj i y = 1)
    (hA : A.PosSemidef) (hd : 0 < d) (heta : 0 ≤ eta) :
    let C := branchReturn s amp proj p
    let D := d • (1 : Matrix ι ι ℂ) + eta • (C * A * star C)
    HasDerivAt (fun y => -nu * Real.log
      ((d • (1 : Matrix ι ι ℂ) + eta •
        (branchReturn s amp proj y * A * star (branchReturn s amp proj y))).det.re))
      (-nu * eta * ∑ i ∈ s, damp i *
        ((D⁻¹ * (proj i p * A * star C + C * A * star (proj i p))).trace).re) p := by
  apply branchReturn_price_hasDerivAt_independent_branches s amp proj damp dproj p t d eta nu A
    hamp hproj hmatch hcomplete
  exact Filter.Eventually.of_forall fun y =>
    return_pencil_det_positive_real A (branchReturn s amp proj y) d eta hA hd heta

end D0.Analysis.MatchedBranchReturn
end
