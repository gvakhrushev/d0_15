import D0.Analysis.NoncommutingPerturbationProduct
import D0.Research.TaskFaithfulReturnBound

/-!
# Noncommuting task-faithful return products with retained history

This is the concrete consumer of the compression-error transport in
`TaskFaithfulReturnBound`. The unchanged finite return blocks, their supplied
isometric preparations, reference scalar corners and full-input effect errors
give the relative defects. The ordered product is then factored exactly into
its scalar amplitude and the corresponding noncommuting perturbation product.

The final theorem proves equation (10)'s vector quadratic-form sandwich for
the actual return product after any retained-history map `K`, including
singular `K`. Source: owner commit `fd35893d77e4aa5f819bafa0c6428c8e7a8f1812`,
`02_REGISTRY/research/sources/d0_task_faithful_source_2026-10-28/PROOF_RU.md`,
blob `c99e90a8c8e96bae70e700fa88d1c2d824a1831b`, section 5.

The estimate is pointwise in the supplied preparations and effects. No
derivative bound, log-determinant price estimate, or physical admission is
deduced. All factors retain their list order.
-/

noncomputable section

namespace D0.Research

open D0.Analysis

variable {J I X : Type*}
  [NormedAddCommGroup I] [InnerProductSpace ℂ I] [FiniteDimensional ℂ I]
  [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X]

/-- The relative defect of the actual existing return compression at scale `c`. -/
def taskReturnRelativeDefect (prepare : X →ₗᵢ[ℂ] I) (effect : I →ₗ[ℂ] I)
    (c : ℝ) : X →L[ℂ] X :=
  ((c : ℂ)⁻¹) • (taskReturnCompression prepare.toLinearMap effect).toContinuousLinearMap - 1

/-- Product of the actual return blocks, in the given list order. -/
def taskReturnProduct (prepare : J → X →ₗᵢ[ℂ] I)
    (effect : J → I →ₗ[ℂ] I) (w : List J) : X →L[ℂ] X :=
  (w.map fun j => (taskReturnCompression (prepare j).toLinearMap
    (effect j)).toContinuousLinearMap).prod

/-- The actual product is exactly the scalar amplitude times its defect product. -/
theorem taskReturnProduct_factorization
    (prepare : J → X →ₗᵢ[ℂ] I) (effect : J → I →ₗ[ℂ] I)
    (c : J → ℝ) (w : List J) (hc : ∀ j ∈ w, 0 < c j) :
    taskReturnProduct prepare effect w =
      (((w.map c).prod : ℝ) : ℂ) •
        perturbationProduct (fun j => taskReturnRelativeDefect (prepare j) (effect j) (c j)) w := by
  induction w with
  | nil => simp [taskReturnProduct, perturbationProduct]
  | cons j w ih =>
      have hj := taskReturnCompression_relative_factorization
        (prepare j).toLinearMap (effect j) (c j) (hc j (by simp))
      have ht := ih (fun k hk => hc k (by simp [hk]))
      change (taskReturnCompression (prepare j).toLinearMap (effect j)).toContinuousLinearMap *
          taskReturnProduct prepare effect w =
        ((c j * (w.map c).prod : ℝ) : ℂ) •
          ((1 + taskReturnRelativeDefect (prepare j) (effect j) (c j)) *
            perturbationProduct (fun k => taskReturnRelativeDefect (prepare k) (effect k) (c k)) w)
      rw [hj, ht, smul_mul_smul_comm, Complex.ofReal_mul]
      rfl

/-- Actual effect tolerances supply the hypotheses of the generic product
bound; the defect-norm hypothesis is derived, not inserted as a new input. -/
theorem taskReturnRelativeDefect_norm_le
    (prepare : X →ₗᵢ[ℂ] I) (reference actual : I →ₗ[ℂ] I)
    (c ε : ℝ) (hc : 0 < c)
    (hcorner : taskReturnCompression prepare.toLinearMap reference = (c : ℂ) • 1)
    (heffect : ‖(actual - reference).toContinuousLinearMap‖ ≤ ε) :
    ‖taskReturnRelativeDefect prepare actual c‖ ≤ 2 * ε / c :=
  taskReturnCompression_scalarCorner_relative_error_le prepare reference actual c hc
    hcorner heffect

/-- Equation (10) in vector quadratic-form form for the actual full ordered
return product and arbitrary retained history. Write `T = (∏ cⱼ)²` and
`η = ∑ -log(1 - 2 εⱼ / cⱼ)`. No invertibility or lower singular-value bound
on `K` is required, and no blocks are commuted. -/
theorem taskReturnProduct_history_sq_bounds
    {V : Type*} [NormedAddCommGroup V] [NormedSpace ℂ V]
    (prepare : J → X →ₗᵢ[ℂ] I) (reference actual : J → I →ₗ[ℂ] I)
    (c ε : J → ℝ) (w : List J)
    (hc : ∀ j ∈ w, 0 < c j)
    (hcorner : ∀ j ∈ w,
      taskReturnCompression (prepare j).toLinearMap (reference j) = (c j : ℂ) • 1)
    (heffect : ∀ j ∈ w, ‖(actual j - reference j).toContinuousLinearMap‖ ≤ ε j)
    (hsmall : ∀ j ∈ w, 2 * ε j / c j < 1)
    (K : V →L[ℂ] X) (x : V) :
    Real.exp (-2 * perturbationEta (fun j => 2 * ε j / c j) w) *
        (w.map c).prod ^ 2 * ‖K x‖ ^ 2 ≤
          ‖(taskReturnProduct prepare actual w ∘L K) x‖ ^ 2 ∧
      ‖(taskReturnProduct prepare actual w ∘L K) x‖ ^ 2 ≤
        Real.exp (2 * perturbationEta (fun j => 2 * ε j / c j) w) *
          (w.map c).prod ^ 2 * ‖K x‖ ^ 2 := by
  let B : J → X →L[ℂ] X := fun j =>
    taskReturnRelativeDefect (prepare j) (actual j) (c j)
  have hb : ∀ j ∈ w, ‖B j‖ ≤ 2 * ε j / c j := by
    intro j hj
    exact taskReturnRelativeDefect_norm_le (prepare j) (reference j) (actual j)
      (c j) (ε j) (hc j hj) (hcorner j hj) (heffect j hj)
  have h := perturbationProduct_exp_sq_norm_bounds B (fun j => 2 * ε j / c j)
    w hb hsmall (K x)
  have hscale : 0 ≤ (w.map c).prod := by
    apply List.prod_nonneg
    intro a ha
    obtain ⟨j, hj, rfl⟩ := List.mem_map.mp ha
    exact (hc j hj).le
  have hnorm : ‖(taskReturnProduct prepare actual w ∘L K) x‖ =
      (w.map c).prod * ‖perturbationProduct B w (K x)‖ := by
    rw [taskReturnProduct_factorization prepare actual c w hc]
    change ‖(((w.map c).prod : ℝ) : ℂ) • perturbationProduct B w (K x)‖ = _
    rw [norm_smul, Complex.norm_real, Real.norm_eq_abs, abs_of_nonneg hscale]
  rw [hnorm, mul_pow]
  constructor
  · calc
      _ = (w.map c).prod ^ 2 *
          (Real.exp (-2 * perturbationEta (fun j => 2 * ε j / c j) w) * ‖K x‖ ^ 2) := by ring
      _ ≤ _ := mul_le_mul_of_nonneg_left h.1 (sq_nonneg _)
  · calc
      _ ≤ (w.map c).prod ^ 2 *
          (Real.exp (2 * perturbationEta (fun j => 2 * ε j / c j) w) * ‖K x‖ ^ 2) :=
        mul_le_mul_of_nonneg_left h.2 (sq_nonneg _)
      _ = _ := by ring

end D0.Research

end
