import Mathlib.Analysis.Normed.Operator.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic

/-!
# Ordered products of bounded operator perturbations

For the actual ordered product `M = ∏ (1 + Bⱼ)`, with `‖Bⱼ‖ ≤ δⱼ < 1`,
this module proves two-sided vector norm bounds by `∏ (1 ± δⱼ)` and by
`exp(±η)`, where `η = ∑ -log(1 - δⱼ)`. No commutation, positivity,
self-adjointness or inverse of an earlier operator is assumed.

The motivating consumer is equation (10) of the task-faithful return-source
proof, owner commit `fd35893d77e4aa5f819bafa0c6428c8e7a8f1812`, file
`02_REGISTRY/research/sources/d0_task_faithful_source_2026-10-28/PROOF_RU.md`,
blob `c99e90a8c8e96bae70e700fa88d1c2d824a1831b`. A separate adapter supplies
its actual return defects. These estimates are not log-determinant price or
physical-admission statements.
-/

noncomputable section

namespace D0.Analysis

variable {J E : Type*} [NormedAddCommGroup E] [NormedSpace ℂ E]

/-- List order is retained: the head factor acts after the tail product. -/
def perturbationProduct (B : J → E →L[ℂ] E) (w : List J) : E →L[ℂ] E :=
  (w.map fun j => 1 + B j).prod

/-- Logarithmic error budget for the same ordered list of factors. -/
def perturbationEta (δ : J → ℝ) (w : List J) : ℝ :=
  (w.map fun j => -Real.log (1 - δ j)).sum

/-- A single perturbation has upper and lower vector bounds. -/
theorem one_add_operator_norm_bounds (B : E →L[ℂ] E) (δ : ℝ)
    (hB : ‖B‖ ≤ δ) (x : E) :
    (1 - δ) * ‖x‖ ≤ ‖(1 + B) x‖ ∧ ‖(1 + B) x‖ ≤ (1 + δ) * ‖x‖ := by
  have hb : ‖B x‖ ≤ δ * ‖x‖ :=
    (B.le_opNorm x).trans (mul_le_mul_of_nonneg_right hB (norm_nonneg x))
  have hupper : ‖x + B x‖ ≤ ‖x‖ + ‖B x‖ := norm_add_le _ _
  have hlower : ‖x‖ ≤ ‖x + B x‖ + ‖B x‖ := by
    simpa using norm_sub_le (x + B x) (B x)
  change (1 - δ) * ‖x‖ ≤ ‖x + B x‖ ∧ ‖x + B x‖ ≤ (1 + δ) * ‖x‖
  constructor <;> nlinarith

/-- The product bounds do not reorder any operator factors. -/
theorem perturbationProduct_norm_bounds
    (B : J → E →L[ℂ] E) (δ : J → ℝ) (w : List J)
    (hB : ∀ j ∈ w, ‖B j‖ ≤ δ j) (hδ : ∀ j ∈ w, δ j < 1) (x : E) :
    (w.map fun j => 1 - δ j).prod * ‖x‖ ≤ ‖perturbationProduct B w x‖ ∧
      ‖perturbationProduct B w x‖ ≤ (w.map fun j => 1 + δ j).prod * ‖x‖ := by
  induction w with
  | nil => simp [perturbationProduct]
  | cons j w ih =>
      have hb := hB j (by simp)
      have hd := hδ j (by simp)
      have hd0 : 0 ≤ δ j := (norm_nonneg _).trans hb
      have ht := ih (fun k hk => hB k (by simp [hk]))
        (fun k hk => hδ k (by simp [hk]))
      have hone := one_add_operator_norm_bounds (B j) (δ j) hb
        (perturbationProduct B w x)
      change ((1 - δ j) * (w.map fun k => 1 - δ k).prod) * ‖x‖ ≤
          ‖(1 + B j) (perturbationProduct B w x)‖ ∧
        ‖(1 + B j) (perturbationProduct B w x)‖ ≤
          ((1 + δ j) * (w.map fun k => 1 + δ k).prod) * ‖x‖
      constructor
      · calc
          _ = (1 - δ j) * ((w.map fun k => 1 - δ k).prod * ‖x‖) := by ring
          _ ≤ (1 - δ j) * ‖perturbationProduct B w x‖ :=
            mul_le_mul_of_nonneg_left ht.1 (by linarith)
          _ ≤ _ := hone.1
      · calc
          _ ≤ (1 + δ j) * ‖perturbationProduct B w x‖ := hone.2
          _ ≤ (1 + δ j) * ((w.map fun k => 1 + δ k).prod * ‖x‖) :=
            mul_le_mul_of_nonneg_left ht.2 (by linarith)
          _ = _ := by ring

/-- The lower product is exactly the negative exponential error budget. -/
theorem perturbation_lower_product_eq_exp
    (δ : J → ℝ) (w : List J) (hδ : ∀ j ∈ w, δ j < 1) :
    (w.map fun j => 1 - δ j).prod = Real.exp (-perturbationEta δ w) := by
  induction w with
  | nil => simp [perturbationEta]
  | cons j w ih =>
      have hj : 0 < 1 - δ j := by linarith [hδ j (by simp)]
      have ht := ih (fun k hk => hδ k (by simp [hk]))
      simp only [List.map_cons, List.prod_cons, perturbationEta, List.sum_cons] at *
      rw [neg_add, neg_neg, Real.exp_add, Real.exp_log hj, ht]

/-- The upper product is bounded by the positive exponential budget. -/
theorem perturbation_upper_product_le_exp
    (δ : J → ℝ) (w : List J)
    (hδ0 : ∀ j ∈ w, 0 ≤ δ j) (hδ : ∀ j ∈ w, δ j < 1) :
    (w.map fun j => 1 + δ j).prod ≤ Real.exp (perturbationEta δ w) := by
  induction w with
  | nil => simp [perturbationEta]
  | cons j w ih =>
      have hj0 := hδ0 j (by simp)
      have hj : 0 < 1 - δ j := by linarith [hδ j (by simp)]
      have ht := ih (fun k hk => hδ0 k (by simp [hk]))
        (fun k hk => hδ k (by simp [hk]))
      have hfactor : 1 + δ j ≤ Real.exp (-Real.log (1 - δ j)) := by
        rw [Real.exp_neg, Real.exp_log hj, inv_eq_one_div]
        apply (le_div_iff₀ hj).mpr
        nlinarith [sq_nonneg (δ j)]
      simp only [List.map_cons, List.prod_cons, perturbationEta, List.sum_cons,
        Real.exp_add] at *
      exact (mul_le_mul_of_nonneg_left ht (by linarith)).trans
        (mul_le_mul_of_nonneg_right hfactor (Real.exp_pos _).le)

/-- `η` is nonnegative under the stated finite tolerances. -/
theorem perturbationEta_nonneg
    (δ : J → ℝ) (w : List J)
    (hδ0 : ∀ j ∈ w, 0 ≤ δ j) (hδ : ∀ j ∈ w, δ j < 1) :
    0 ≤ perturbationEta δ w := by
  apply List.sum_nonneg
  intro a ha
  obtain ⟨j, hj, rfl⟩ := List.mem_map.mp ha
  have hpos : 0 < 1 - δ j := by linarith [hδ j hj]
  have hle : 1 - δ j ≤ 1 := by linarith [hδ0 j hj]
  exact neg_nonneg.mpr (Real.log_nonpos hpos.le hle)

/-- Two-sided exponential bounds hold on every vector, with no inverse premise. -/
theorem perturbationProduct_exp_norm_bounds
    (B : J → E →L[ℂ] E) (δ : J → ℝ) (w : List J)
    (hB : ∀ j ∈ w, ‖B j‖ ≤ δ j) (hδ : ∀ j ∈ w, δ j < 1) (x : E) :
    Real.exp (-perturbationEta δ w) * ‖x‖ ≤ ‖perturbationProduct B w x‖ ∧
      ‖perturbationProduct B w x‖ ≤ Real.exp (perturbationEta δ w) * ‖x‖ := by
  have h := perturbationProduct_norm_bounds B δ w hB hδ x
  constructor
  · rw [← perturbation_lower_product_eq_exp δ w hδ]
    exact h.1
  · exact h.2.trans (mul_le_mul_of_nonneg_right
      (perturbation_upper_product_le_exp δ w (fun j hj => (norm_nonneg _).trans (hB j hj))
        hδ) (norm_nonneg x))

/-- The squared vector sandwich also applies after a possibly singular history. -/
theorem perturbationProduct_exp_sq_norm_bounds
    (B : J → E →L[ℂ] E) (δ : J → ℝ) (w : List J)
    (hB : ∀ j ∈ w, ‖B j‖ ≤ δ j) (hδ : ∀ j ∈ w, δ j < 1) (x : E) :
    Real.exp (-2 * perturbationEta δ w) * ‖x‖ ^ 2 ≤
        ‖perturbationProduct B w x‖ ^ 2 ∧
      ‖perturbationProduct B w x‖ ^ 2 ≤
        Real.exp (2 * perturbationEta δ w) * ‖x‖ ^ 2 := by
  have h := perturbationProduct_exp_norm_bounds B δ w hB hδ x
  have hlo := (sq_le_sq₀ (mul_nonneg (Real.exp_pos _).le (norm_nonneg x))
    (norm_nonneg _)).mpr h.1
  have hhi := (sq_le_sq₀ (norm_nonneg _) (mul_nonneg (Real.exp_pos _).le
    (norm_nonneg x))).mpr h.2
  have hexp (r : ℝ) : (Real.exp r) ^ 2 = Real.exp (2 * r) := by
    rw [pow_two, ← Real.exp_add]
    congr 1
    ring
  constructor
  · simpa only [mul_pow, hexp, mul_neg, neg_mul] using hlo
  · simpa only [mul_pow, hexp] using hhi

end D0.Analysis

end
