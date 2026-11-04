import D0.Research.TaskFaithfulReturnProduct
import D0.Analysis.GramMatrixOrder
import D0.Analysis.MatrixRelativeLogDetBound

/-!
# The actual task-faithful return product's relative price bound

This is the composed finite-matrix consumer of equation (11) in
`02_REGISTRY/research/sources/d0_task_faithful_source_2026-10-28/PROOF_RU.md`,
owner commit `fd35893d77e4aa5f819bafa0c6428c8e7a8f1812`, proof blob
`c99e90a8c8e96bae70e700fa88d1c2d824a1831b`.

The supplied full-input effect errors, same isometric preparations and exact
scalar reference corners determine the actual ordered return product. Its
already proved vector bounds are transported through an explicit orthonormal
input basis to positive-semidefinite Gram order. Logdet monotonicity and the
scalar spectral estimate then give the full return-price error with the
actual reference resolvent-trace gain. No separate matrix sandwich or
endpoint price-error hypothesis is inserted.

The retained history may be singular or zero; no inverse of it is taken.
This is pointwise finite mathematics. It does not choose the physical task,
prepare an admitted execution, estimate derivatives from value tolerances,
or remove independent heat, clock, work, or preparation contributions.
-/

noncomputable section

namespace D0.Research

open D0.Analysis
open scoped ComplexOrder

variable {J I X : Type*}
  [NormedAddCommGroup I] [InnerProductSpace ℂ I] [FiniteDimensional ℂ I]
  [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X]

/-- Equation (11) for the actual noncommuting return product after arbitrary
retained history. The reference Gram matrix includes the exact `z T` scale,
where `T = (∏ cⱼ)²`; the gain is the resolvent trace of that same matrix. -/
theorem taskReturnProduct_price_bound
    {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℂ V] [FiniteDimensional ℂ V]
    {n : Type*} [Fintype n] [DecidableEq n]
    (prepare : J → X →ₗᵢ[ℂ] I) (reference actual : J → I →ₗ[ℂ] I)
    (c ε : J → ℝ) (w : List J)
    (hc : ∀ j ∈ w, 0 < c j)
    (hcorner : ∀ j ∈ w,
      taskReturnCompression (prepare j).toLinearMap (reference j) = (c j : ℂ) • 1)
    (heffect : ∀ j ∈ w, ‖(actual j - reference j).toContinuousLinearMap‖ ≤ ε j)
    (hsmall : ∀ j ∈ w, 2 * ε j / c j < 1)
    (K : V →L[ℂ] X) (b : OrthonormalBasis n ℂ V)
    (z : ℝ) (hz : 0 ≤ z) (hzOne : z < 1) :
    let T := (w.map c).prod ^ 2
    let η := perturbationEta (fun j => 2 * ε j / c j) w
    let S : Matrix n n ℂ := ((z * T : ℝ) : ℂ) • gramMatrix K.toLinearMap b
    let H : Matrix n n ℂ := (z : ℂ) •
      gramMatrix (taskReturnProduct prepare actual w ∘L K).toLinearMap b
    |regularizedReturnPrice (1 - z) H - regularizedReturnPrice (1 - z) S| ≤
      (Real.exp (2 * η) - 1) * regularizedReturnGain (1 - z) S := by
  let T := (w.map c).prod ^ 2
  let δ : J → ℝ := fun j => 2 * ε j / c j
  let η := perturbationEta δ w
  let L := taskReturnProduct prepare actual w ∘L K
  let S : Matrix n n ℂ := ((z * T : ℝ) : ℂ) • gramMatrix K.toLinearMap b
  let H : Matrix n n ℂ := (z : ℂ) • gramMatrix L.toLinearMap b
  change |regularizedReturnPrice (1 - z) H - regularizedReturnPrice (1 - z) S| ≤
    (Real.exp (2 * η) - 1) * regularizedReturnGain (1 - z) S
  have hT : 0 ≤ T := sq_nonneg _
  have hδ : ∀ j ∈ w, 0 ≤ δ j := by
    intro j hj
    exact (norm_nonneg (taskReturnRelativeDefect (prepare j) (actual j) (c j))).trans
      (taskReturnRelativeDefect_norm_le (prepare j) (reference j) (actual j)
        (c j) (ε j) (hc j hj) (hcorner j hj) (heffect j hj))
  have hη : 0 ≤ η := perturbationEta_nonneg δ w hδ hsmall
  have hnorm (x : V) :
      Real.exp (-2 * η) * T * ‖K x‖ ^ 2 ≤ ‖L x‖ ^ 2 ∧
      ‖L x‖ ^ 2 ≤ Real.exp (2 * η) * T * ‖K x‖ ^ 2 :=
    taskReturnProduct_history_sq_bounds prepare reference actual c ε w
      hc hcorner heffect hsmall K x
  have hS : S.PosSemidef :=
    (gramMatrix_posSemidef K.toLinearMap b).smul
      (Complex.zero_le_real.mpr (mul_nonneg hz hT))
  have hH : H.PosSemidef :=
    (gramMatrix_posSemidef L.toLinearMap b).smul (Complex.zero_le_real.mpr hz)
  have hlower0 := gramMatrix_smul_sub_smul_posSemidef
    K.toLinearMap L.toLinearMap b (Real.exp (-2 * η) * (z * T)) z (by
      intro x
      calc
        (Real.exp (-2 * η) * (z * T)) * ‖K x‖ ^ 2 =
            z * (Real.exp (-2 * η) * T * ‖K x‖ ^ 2) := by ring
        _ ≤ z * ‖L x‖ ^ 2 := mul_le_mul_of_nonneg_left (hnorm x).1 hz)
  have hupper0 := gramMatrix_smul_sub_smul_posSemidef
    L.toLinearMap K.toLinearMap b z (Real.exp (2 * η) * (z * T)) (by
      intro x
      calc
        z * ‖L x‖ ^ 2 ≤ z * (Real.exp (2 * η) * T * ‖K x‖ ^ 2) :=
          mul_le_mul_of_nonneg_left (hnorm x).2 hz
        _ = (Real.exp (2 * η) * (z * T)) * ‖K x‖ ^ 2 := by ring)
  have hlower : (H - (Real.exp (-2 * η) : ℂ) • S).PosSemidef := by
    simpa only [H, S, smul_smul, Complex.ofReal_mul] using hlower0
  have hupper : ((Real.exp (2 * η) : ℂ) • S - H).PosSemidef := by
    simpa only [H, S, smul_smul, Complex.ofReal_mul] using hupper0
  exact regularizedReturnPrice_sandwich_bound S H hS hH (1 - z) η
    (sub_pos.mpr hzOne) hη hlower hupper

end D0.Research

end
