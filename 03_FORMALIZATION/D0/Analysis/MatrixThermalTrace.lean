import D0.Analysis.MatrixTraceExponentialDerivative
import Mathlib.Analysis.Matrix.Order
import Mathlib.Analysis.Matrix.PosDef
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.Complex.RealDeriv
import Mathlib.Tactic

/-! Finite-matrix thermal trace calculus. No physical admission is asserted. -/

namespace D0.Analysis

open scoped Matrix.Norms.Frobenius ComplexOrder

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- The exponential of a Hermitian matrix is positive definite. -/
theorem matrix_exp_posDef (A : Matrix ι ι ℂ) (hA : star A = A) :
    (NormedSpace.exp A).PosDef := by
  let X : Matrix ι ι ℂ := (1 / 2 : ℝ) • A
  have hX : star X = X := by simp [X, hA]
  have hhalf : X + X = A := by
    dsimp [X]
    ext i j
    simp only [Matrix.add_apply, Matrix.smul_apply, Complex.real_smul]
    norm_num
    ring
  have hexp : NormedSpace.exp A = NormedSpace.exp X * NormedSpace.exp X := by
    rw [← hhalf]
    exact Matrix.exp_add_of_commute X X (Commute.refl X)
  have hstar : star (NormedSpace.exp X) = NormedSpace.exp X := by
    rw [NormedSpace.star_exp, hX]
  have hpsd : (NormedSpace.exp A).PosSemidef := by
    have heq : NormedSpace.exp A = star (NormedSpace.exp X) * NormedSpace.exp X := by
      rw [hstar]
      exact hexp
    rw [heq]
    simpa only [Matrix.star_eq_conjTranspose] using
      Matrix.posSemidef_conjTranspose_mul_self (NormedSpace.exp X)
  exact hpsd.posDef_iff_isUnit.mpr (Matrix.isUnit_exp A)

/-- A nonempty finite carrier has strictly positive heat partition function. -/
theorem matrix_exp_trace_re_pos [Nonempty ι] (A : Matrix ι ι ℂ) (hA : star A = A) :
    0 < (Matrix.trace (NormedSpace.exp A)).re := by
  exact (Complex.pos_iff.mp (matrix_exp_posDef A hA).trace_pos).1

/-- The heat exponential commutes with its Hermitian or non-Hermitian input. -/
theorem matrix_exp_smul_commutes (A : Matrix ι ι ℂ) (β : ℝ) :
    NormedSpace.exp ((-β) • A) * A = A * NormedSpace.exp ((-β) • A) := by
  exact ((Commute.refl A).smul_left (-β)).exp_left.eq

/-- A trace weight commuting with A kills its infinitesimal commutator. -/
theorem matrix_exp_trace_commutator_zero (A K : Matrix ι ι ℂ) (β : ℝ) :
    Matrix.trace (NormedSpace.exp ((-β) • A) * (K * A - A * K)) = 0 := by
  let E := NormedSpace.exp ((-β) • A)
  have hEA : E * A = A * E := matrix_exp_smul_commutes A β
  simp only [mul_sub, Matrix.trace_sub, ← mul_assoc]
  rw [Matrix.trace_mul_cycle E K A, ← hEA, sub_self]

/-- The real finite-dimensional heat partition function. -/
noncomputable def matrixHeatPartition (β : ℝ) (Δ : Matrix ι ι ℂ) : ℝ :=
  (Matrix.trace (NormedSpace.exp ((-β) • Δ))).re

/--
The heat log-partition derivative uses the same curve and keeps an arbitrary
common transport generator `K`. No commutativity between the curve and its
derivative is assumed.
-/
theorem hasDerivAt_matrix_heat_log_partition [Nonempty ι]
    {Δ : ℝ → Matrix ι ι ℂ} {dΔ K : Matrix ι ι ℂ} {t : ℝ} (β : ℝ)
    (hβ : β ≠ 0) (hΔ : HasDerivAt Δ dΔ t) (hHerm : star (Δ t) = Δ t) :
    let E := NormedSpace.exp ((-β) • Δ t)
    let Z := matrixHeatPartition β (Δ t)
    HasDerivAt (fun s => β⁻¹ * Real.log (matrixHeatPartition β (Δ s)))
      (-((Matrix.trace (E * (dΔ - (K * Δ t - Δ t * K)))).re) / Z) t := by
  let E : Matrix ι ι ℂ := NormedSpace.exp ((-β) • Δ t)
  let Z : ℝ := matrixHeatPartition β (Δ t)
  have hSelf : star ((-β) • Δ t) = (-β) • Δ t := by simp [hHerm]
  have hZ : 0 < Z := matrix_exp_trace_re_pos ((-β) • Δ t) hSelf
  have hA : HasDerivAt (fun s => (-β) • Δ s) ((-β) • dΔ) t :=
    hΔ.const_smul (-β)
  have htrace := hasDerivAt_matrix_trace_exp hA
  have hre := Complex.reCLM.hasFDerivAt.comp_hasDerivAt t htrace
  have hpartition : HasDerivAt (fun s => matrixHeatPartition β (Δ s))
      ((-β) * (Matrix.trace (E * dΔ)).re) t := by
    simpa only [matrixHeatPartition, Complex.reCLM_apply, mul_smul_comm,
      Matrix.trace_smul, Complex.smul_re, smul_eq_mul, E] using hre
  have hlog := (hpartition.log (ne_of_gt hZ)).const_mul β⁻¹
  have hcomm : Matrix.trace (E * (K * Δ t - Δ t * K)) = 0 :=
    matrix_exp_trace_commutator_zero (Δ t) K β
  have hrelative : Matrix.trace (E * (dΔ - (K * Δ t - Δ t * K))) =
      Matrix.trace (E * dΔ) := by
    rw [mul_sub, Matrix.trace_sub, hcomm, sub_zero]
  apply hlog.congr_deriv
  rw [hrelative]
  change β⁻¹ * (((-β) * (Matrix.trace (E * dΔ)).re) / Z) =
    -((Matrix.trace (E * dΔ)).re) / Z
  field_simp

end D0.Analysis
