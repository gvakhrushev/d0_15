import D0.Analysis.NoncommutingPerturbationProduct

/-!
# Explicit uniform template budgets for the return contrast

This is the finite compiler-budget calculation following equation (12) in
`02_REGISTRY/research/sources/d0_task_faithful_source_2026-10-28/PROOF_RU.md`,
owner commit `fd35893d77e4aa5f819bafa0c6428c8e7a8f1812`, proof blob
`c99e90a8c8e96bae70e700fa88d1c2d824a1831b`.

The actual list length `M` and per-block gain scale `λ` remain visible.
Under `δⱼ ≤ d < 1/2` and `2 M d ≤ 1`, the logarithmic error budget is
at most `2 M d`; after normalization by `Λ = M λ`, the contrast budget is
at most `4 exp(θ+2) d / (|t| λ)`. These sufficient bounds do not assert an
optimal compiler or select a physical cost, information or clock law.
-/

noncomputable section

namespace D0.Analysis

/-- The elementary logarithmic budget on the half-unit interval. -/
theorem neg_log_one_sub_le_two_mul {δ : ℝ} (hδ0 : 0 ≤ δ) (hδ : δ < 1 / 2) :
    -Real.log (1 - δ) ≤ 2 * δ := by
  have hp : 0 < 1 - δ := by linarith
  have hlog := Real.one_sub_inv_le_log_of_pos hp
  have hinv : (1 - δ)⁻¹ ≤ 1 + 2 * δ := by
    rw [inv_eq_one_div]
    apply (div_le_iff₀ hp).mpr
    nlinarith [mul_nonneg hδ0 (show 0 ≤ 1 - 2 * δ by linarith)]
  linarith

/-- A uniform error tolerance pays once for every actual factor in the list. -/
theorem perturbationEta_le_uniform_budget
    {J : Type*} (δ : J → ℝ) (w : List J) (d : ℝ)
    (hδ0 : ∀ j ∈ w, 0 ≤ δ j) (hδd : ∀ j ∈ w, δ j ≤ d) (hd : d < 1 / 2) :
    perturbationEta δ w ≤ 2 * (w.length : ℝ) * d := by
  induction w with
  | nil => simp [perturbationEta]
  | cons j w ih =>
      have hjd := hδd j (by simp)
      have hj := neg_log_one_sub_le_two_mul (hδ0 j (by simp)) (lt_of_le_of_lt hjd hd)
      have ht := ih (fun k hk => hδ0 k (by simp [hk]))
        (fun k hk => hδd k (by simp [hk]))
      simp only [perturbationEta, List.map_cons, List.sum_cons, List.length_cons,
        Nat.cast_add, Nat.cast_one] at *
      linarith

/-- No calculus premise is needed: the tangent inequality for `exp(-2η)`
and monotonicity bound the error when `0 ≤ η ≤ 1`. -/
theorem exp_two_mul_sub_one_le {η : ℝ} (hη0 : 0 ≤ η) (hη1 : η ≤ 1) :
    Real.exp (2 * η) - 1 ≤ 2 * Real.exp 2 * η := by
  have htangent := Real.add_one_le_exp (-(2 * η))
  have hmult := mul_le_mul_of_nonneg_right htangent (Real.exp_pos (2 * η)).le
  have hcancel : Real.exp (-(2 * η)) * Real.exp (2 * η) = 1 := by
    rw [← Real.exp_add]
    simp
  rw [hcancel] at hmult
  have hexp : Real.exp (2 * η) ≤ Real.exp 2 :=
    Real.exp_le_exp.mpr (by linarith)
  have htimes := mul_le_mul_of_nonneg_left hexp (show 0 ≤ 2 * η by linarith)
  nlinarith

/-- The original contrast right-hand side with `Λ = M lam`, retaining the
exact dependence on the number of blocks, comparison step and per-block scale. -/
theorem returnContrast_le_uniform_template_budget
    (M : ℕ) (d η θ t lam : ℝ)
    (hM : 0 < M) (hη0 : 0 ≤ η) (hηM : η ≤ 2 * (M : ℝ) * d)
    (hMd : 2 * (M : ℝ) * d ≤ 1) (ht : t ≠ 0) (hlam : 0 < lam) :
    Real.exp θ * (Real.exp (2 * η) - 1) / (|t| * ((M : ℝ) * lam)) ≤
      4 * Real.exp (θ + 2) * d / (|t| * lam) := by
  have hMr : 0 < (M : ℝ) := by exact_mod_cast hM
  have htpos : 0 < |t| := abs_pos.mpr ht
  have hden : 0 < |t| * ((M : ℝ) * lam) := by positivity
  have he := exp_two_mul_sub_one_le hη0 (hηM.trans hMd)
  calc
    _ ≤ Real.exp θ * (2 * Real.exp 2 * η) / (|t| * ((M : ℝ) * lam)) :=
      div_le_div_of_nonneg_right
        (mul_le_mul_of_nonneg_left he (Real.exp_pos θ).le) hden.le
    _ ≤ Real.exp θ * (2 * Real.exp 2 * (2 * (M : ℝ) * d)) /
        (|t| * ((M : ℝ) * lam)) := by
      apply div_le_div_of_nonneg_right _ hden.le
      apply mul_le_mul_of_nonneg_left _ (Real.exp_pos θ).le
      exact mul_le_mul_of_nonneg_left hηM (by positivity)
    _ = 4 * Real.exp (θ + 2) * d / (|t| * lam) := by
      rw [Real.exp_add]
      field_simp
      ring

/-- The displayed per-block tolerance is sufficient for a prescribed final
error. This inequality retains the real comparison step and gain scale. -/
theorem uniform_template_budget_le_tolerance
    (d θ t lam e : ℝ) (ht : t ≠ 0) (hlam : 0 < lam)
    (hd : d ≤ e * |t| * lam / (4 * Real.exp (θ + 2))) :
    4 * Real.exp (θ + 2) * d / (|t| * lam) ≤ e := by
  have htpos : 0 < |t| := abs_pos.mpr ht
  have hcoef : 0 < 4 * Real.exp (θ + 2) := by positivity
  apply (div_le_iff₀ (mul_pos htpos hlam)).mpr
  have hmul := (le_div_iff₀ hcoef).mp hd
  nlinarith

/-- The explicit minimum budget supplies both the finite-horizon condition
and the prescribed contrast tolerance. No block count is absorbed into a constant. -/
theorem returnContrast_le_tolerance_of_min_budget
    (M : ℕ) (d η θ t lam e : ℝ)
    (hM : 0 < M) (hη0 : 0 ≤ η) (hηM : η ≤ 2 * (M : ℝ) * d)
    (ht : t ≠ 0) (hlam : 0 < lam)
    (hd : d ≤ min (1 / (2 * (M : ℝ)))
      (e * |t| * lam / (4 * Real.exp (θ + 2)))) :
    Real.exp θ * (Real.exp (2 * η) - 1) / (|t| * ((M : ℝ) * lam)) ≤ e := by
  have hMr : 0 < (M : ℝ) := by exact_mod_cast hM
  have hMd : 2 * (M : ℝ) * d ≤ 1 := by
    have h := (le_div_iff₀ (show 0 < 2 * (M : ℝ) by positivity)).mp
      (hd.trans (min_le_left _ _))
    nlinarith
  exact (returnContrast_le_uniform_template_budget M d η θ t lam hM hη0 hηM hMd ht hlam).trans
    (uniform_template_budget_le_tolerance d θ t lam e ht hlam (hd.trans (min_le_right _ _)))

end D0.Analysis

end
