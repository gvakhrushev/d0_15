import D0.Analysis.MatchedBranchReturnPositiveChart
import D0.Analysis.PositiveMatrixLogDet
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Instances

/-!
# Matched return-price trace coefficients

Finite matrix algebra for the existing matched branch return. The PSD history
and positive regularized pencil are mathematical inputs. This work does not
select a native execution or identify a physical source, clock, work or GR.
-/

noncomputable section
namespace D0.Analysis.MatchedBranchReturn

open Matrix D0.Analysis.PositiveMatrixLogDet
open scoped BigOperators ComplexOrder MatrixOrder Matrix.Norms.Frobenius

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- The matched branch coefficient reduces to one trace when the branch is
self-adjoint and the inverse pencil commutes with the history. -/
theorem matched_branch_trace_coefficient
    (P R A : Matrix ι ι ℂ) (t : ℝ) (hP : star P = P)
    (hRA : R * A = A * R) :
    ((R * (P * A * star (t • (1 : Matrix ι ι ℂ)) +
      (t • (1 : Matrix ι ι ℂ)) * A * star P)).trace).re =
        2 * t * ((P * R * A).trace).re := by
  have h₁ : (R * P * A).trace = (P * R * A).trace := by
    calc
      (R * P * A).trace = (A * R * P).trace := Matrix.trace_mul_cycle R P A
      _ = (R * A * P).trace := by rw [← hRA]
      _ = (P * R * A).trace := Matrix.trace_mul_cycle R A P
  have h₂ : (R * A * P).trace = (P * R * A).trace := by
    simpa only [mul_assoc] using (Matrix.trace_mul_cycle R A P)
  simp only [star_smul, star_trivial, star_one, hP, mul_smul_comm,
    smul_mul_assoc, mul_one, one_mul, mul_add, Matrix.trace_add,
    Matrix.trace_smul, Complex.add_re, Complex.smul_re, smul_eq_mul]
  simp only [← mul_assoc, h₁, h₂]
  ring


/-- The regularized inverse commutes with the actual PSD history. -/
theorem affine_resolvent_commutes (A : Matrix ι ι ℂ) (d q : ℝ)
    (hA : A.PosSemidef) (hd : 0 < d) (hq : 0 ≤ q) :
    (affinePencil A d q)⁻¹ * A = A * (affinePencil A d q)⁻¹ := by
  let D := affinePencil A d q
  have hD : D * A = A * D := by
    dsimp [D, affinePencil]
    simp only [add_mul, mul_add, smul_mul_assoc, mul_smul_comm, one_mul, mul_one]
  have hunit : IsUnit D.det := isUnit_iff_ne_zero.mpr
    (ne_of_gt (affinePencil_posDef A hA hd hq).det_pos)
  exact D0.Algebra.MovingProjectorTransport.inverse_commutes_of_commutes D A D⁻¹ hD
    (Matrix.nonsing_inv_mul D hunit) (Matrix.mul_nonsing_inv D hunit)

/-- The unscaled resolvent history is positive semidefinite. -/
theorem resolvent_history_posSemidef (A : Matrix ι ι ℂ) (d q : ℝ)
    (hA : A.PosSemidef) (hd : 0 < d) (hq : 0 ≤ q) :
    ((affinePencil A d q)⁻¹ * A).PosSemidef := by
  have hR : ((affinePencil A d q)⁻¹).PosSemidef :=
    (affinePencil_posDef A hA hd hq).posSemidef.inv
  have hcomm : Commute (affinePencil A d q)⁻¹ A :=
    affine_resolvent_commutes A d q hA hd hq
  exact (Commute.mul_nonneg hR.nonneg hA.nonneg hcomm).posSemidef

/-- Nonzero PSD history has strictly positive unscaled resolvent trace, even
at q=0. This is not positivity of q times that trace. -/
theorem resolvent_history_trace_pos (A : Matrix ι ι ℂ) (d q : ℝ)
    (hA : A.PosSemidef) (hAne : A ≠ 0) (hd : 0 < d) (hq : 0 ≤ q) :
    0 < (((affinePencil A d q)⁻¹ * A).trace).re := by
  let D := affinePencil A d q
  let B := D⁻¹ * A
  have hB : B.PosSemidef := resolvent_history_posSemidef A d q hA hd hq
  have hunit : IsUnit D.det := isUnit_iff_ne_zero.mpr
    (ne_of_gt (affinePencil_posDef A hA hd hq).det_pos)
  have hBne : B ≠ 0 := by
    intro h
    apply hAne
    have h' := congrArg (fun M : Matrix ι ι ℂ => D * M) h
    dsimp [B] at h'
    simpa only [← mul_assoc, Matrix.mul_nonsing_inv D hunit, one_mul, mul_zero] using h'
  have htrace : B.trace ≠ 0 := fun h => hBne (hB.trace_eq_zero_iff.mp h)
  have hnonneg := Complex.nonneg_iff.mp hB.trace_nonneg
  have hre : B.trace.re ≠ 0 := by
    intro h
    apply htrace
    apply Complex.ext
    · simpa using h
    · simpa using hnonneg.2.symm
  exact lt_of_le_of_ne hnonneg.1 (Ne.symm hre)


omit [DecidableEq ι] in
/-- An orthogonal projector has a nonnegative trace against a PSD matrix,
even when the two matrices do not commute. -/
theorem projector_trace_nonneg (P B : Matrix ι ι ℂ)
    (hself : star P = P) (hid : P * P = P) (hB : B.PosSemidef) :
    0 ≤ (P * B).trace.re := by
  have hgram : (P * B * P).PosSemidef := by
    have h := hB.conjTranspose_mul_mul_same P
    simpa only [← Matrix.star_eq_conjTranspose, hself] using h
  have htrace : (P * B * P).trace = (P * B).trace := by
    calc
      (P * B * P).trace = (P * P * B).trace := Matrix.trace_mul_cycle P B P
      _ = (P * B).trace := by rw [hid]
  have h := hgram.trace_nonneg
  rw [htrace] at h
  exact (Complex.nonneg_iff.mp h).1

/-- All normalized fibre coefficients are nonnegative and sum to one.
No commutation is assumed between any branch projector and the history. -/
theorem normalized_resolvent_branch_weights
    {θ : Type*} (s : Finset θ) (P : θ → Matrix ι ι ℂ)
    (A : Matrix ι ι ℂ) (d q : ℝ)
    (hA : A.PosSemidef) (hAne : A ≠ 0) (hd : 0 < d) (hq : 0 ≤ q)
    (hself : ∀ i ∈ s, star (P i) = P i)
    (hid : ∀ i ∈ s, P i * P i = P i)
    (hcomplete : ∑ i ∈ s, P i = 1) :
    let B := (affinePencil A d q)⁻¹ * A
    let w := B.trace.re
    (∀ i ∈ s, 0 ≤ (P i * B).trace.re / w) ∧
      (∑ i ∈ s, (P i * B).trace.re / w) = 1 := by
  let B := (affinePencil A d q)⁻¹ * A
  have hB : B.PosSemidef := resolvent_history_posSemidef A d q hA hd hq
  have hw : 0 < B.trace.re := resolvent_history_trace_pos A d q hA hAne hd hq
  have hsum : (∑ i ∈ s, (P i * B).trace.re) = B.trace.re := by
    rw [← Complex.re_sum, ← Matrix.trace_sum, ← Finset.sum_mul, hcomplete, one_mul]
  constructor
  · intro i hi
    exact div_nonneg (projector_trace_nonneg (P i) B (hself i hi) (hid i hi) hB) hw.le
  · rw [← Finset.sum_div, hsum, div_self (ne_of_gt hw)]

end D0.Analysis.MatchedBranchReturn
end
