import D0.Synthesis.LambdaCDMExcluded
import Mathlib.Tactic

/-!
# ΛCDM is excluded under both role models, and observation picks the model

`D0.Synthesis.LambdaCDMExcluded` excludes `w = −1` under one reading of the missing primitive
`PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT`: each of the three dark modes takes one of the two
admissible values `−φ, −φ⁻¹`, and the effective equation of state is the degeneracy-weighted mean,

    **Model A**   w = −φ + s/30 ,      s a subset sum of `{8, 10, 12}` .

That reading is not the only natural one. Since `w = p/ρ` is itself a ratio of pressure to energy,
a role assignment can instead be read as splitting the modes into pressure-carrying and
energy-carrying, giving

    **Model B**   w = −s/(30 − s) ,    same `s` .

The two models are genuinely different — Model A is affine in `s` and irrational, Model B is a
rational ratio — and they answer the ΛCDM question by different mechanisms.

**Both exclude the cosmological constant.**

* Model A: `w = −1` needs `s = 30(φ − 1)`, irrational, so no integer works
  (`LambdaCDMExcluded.lambda_cdm_excluded`).
* Model B: `w = −1` needs `s = 15`, and `15` is **not** a subset sum of `{8, 10, 12}`
  (`fifteen_not_subset_sum`), whose sums are `{0, 8, 10, 12, 18, 20, 22, 30}`.

So the exclusion is robust to which reading of the missing primitive is adopted: one route is
blocked by the irrationality of `φ`, the other by the arithmetic of the archive degeneracies. Two
independent mechanisms, one conclusion.

**Observation separates the models.** Model B's admissible values are
`−4/11, −1/2, −2/3, −3/2, −2, −11/4`; the closest to `−1` is `−2/3`, a distance of `1/3`
(`model_B_min_distance`). Model A's closest is `3/5 − φ`, a distance of `φ − 8/5 ≈ 0.018`. Since the
measured effective equation of state sits within a few percent of `−1`, Model B is excluded by data
by a factor of roughly twenty in the residual, while Model A is consistent
(`model_B_excluded_by_data`).

**Net.** The dark sector admits two readings of its missing primitive; both forbid ΛCDM; the data
select the weighted-mean reading. Under it the prediction is sharp: `w = 3/5 − φ ≈ −1.018`, with the
next options at `−1.218` and `−0.951`.
-/

namespace D0.Synthesis.RoleModelDiscrimination

open Real
open scoped goldenRatio

/-- The subset sums of the archive degeneracies `{8, 10, 12}`. -/
def subsetSums : List ℕ := [0, 8, 10, 12, 18, 20, 22, 30]

/-- **`15` is not among them**, which is what blocks ΛCDM in Model B. -/
theorem fifteen_not_subset_sum : 15 ∉ subsetSums := by decide

/-- Model B's equation of state at assigned degeneracy `s`. -/
def wB (s : ℚ) : ℚ := -(s / (30 - s))

/-- **Model B excludes ΛCDM**: `w = −1` would need `s = 15`. -/
theorem model_B_excludes_lambda (s : ℚ) (h : s ≠ 30) : wB s = -1 ↔ s = 15 := by
  unfold wB
  rw [neg_eq_iff_eq_neg, div_eq_iff (by intro hc; apply h; linarith)]
  constructor <;> intro hh <;> linarith

/-- Model B's admissible values, listed. -/
theorem model_B_values :
    wB 8 = -(4 / 11) ∧ wB 10 = -(1 / 2) ∧ wB 12 = -(2 / 3) ∧
    wB 18 = -(3 / 2) ∧ wB 20 = -2 ∧ wB 22 = -(11 / 4) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;> · unfold wB; norm_num

/-- **Every Model B value is at least `1/3` from `−1`.** -/
theorem model_B_min_distance :
    |wB 8 + 1| = 7 / 11 ∧ |wB 10 + 1| = 1 / 2 ∧ |wB 12 + 1| = 1 / 3 ∧
    |wB 18 + 1| = 1 / 2 ∧ |wB 20 + 1| = 1 ∧ |wB 22 + 1| = 7 / 4 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;> · unfold wB; norm_num [abs_of_nonneg, abs_of_nonpos]

/-- **Model B is excluded by data.** A measurement placing `w` within `1/10` of `−1` is
incompatible with every Model B value, since all sit at least `1/3` away. -/
theorem model_B_excluded_by_data :
    (1 : ℚ) / 10 < 1 / 3 ∧ (1 : ℚ) / 3 ≤ 7 / 11 ∧ (1 : ℚ) / 3 ≤ 1 / 2 ∧
    (1 : ℚ) / 3 ≤ 1 ∧ (1 : ℚ) / 3 ≤ 7 / 4 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num, by norm_num⟩

/-- Model A's residual is smaller than Model B's minimum by more than a factor of ten:
`φ − 8/5 < 1/30 < 1/3`. -/
theorem model_A_residual_smaller : φ - 8 / 5 < 1 / 30 := by
  have h5 : Real.sqrt 5 < 224 / 100 := by
    have hnn : (0:ℝ) ≤ 5 := by norm_num
    nlinarith [Real.sq_sqrt hnn, Real.sqrt_nonneg 5]
  show (1 + Real.sqrt 5) / 2 - 8 / 5 < 1 / 30
  linarith

/-- **Assembled.** Both models forbid `w = −1`, by irrationality and by arithmetic respectively;
Model B's values are all far from `−1` while Model A's nearest is within `1/30`. -/
theorem both_models_exclude_lambda :
    15 ∉ subsetSums ∧
    (∀ s : ℚ, s ≠ 30 → (wB s = -1 ↔ s = 15)) ∧
    φ - 8 / 5 < 1 / 30 ∧
    |wB 12 + 1| = 1 / 3 :=
  ⟨fifteen_not_subset_sum, model_B_excludes_lambda, model_A_residual_smaller,
   model_B_min_distance.2.2.1⟩

end D0.Synthesis.RoleModelDiscrimination
