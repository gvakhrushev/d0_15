import Mathlib.Tactic
import D0.Core.Phi

/-!
# D0-EW-002 — the Higgs scalar-anchor projector: `dim = 3·13 = 39` and the `δ₀` norm identity

The Higgs scalar anchor is the image of the projector `Π_H = I` on the `N = rank·V₁₃ = 3·13 = 39`-dim
scalar-anchor space. The dimensionless norm-defect amplitude is `defect = (δ₀/√39)·𝟙₃₉`, whose Euclidean
norm is exactly `δ₀`:

* `dim(Im Π_H) = 3·13 = 39` (rank of the transport carrier × terminal shell `V₁₃`);
* `‖defect‖² = 39·(δ₀/√39)² = δ₀²`, i.e. `‖defect‖ = δ₀` — the `√39` in the per-component amplitude
  cancels the `√39` from summing `39` equal components, an exact real-algebra identity;
* `δ₀ = (√5 − 2)/2 = 1/(2φ³) > 0`.

Honest scope (from the cert): this is the dimensionless scalar norm-defect amplitude only; the GeV
normalization of the Higgs VEV is a runtime metrology bridge, not fixed here.
-/

namespace D0.VNext2.HiggsAnchorProjector

open D0

/-- `δ₀ = (√5 − 2)/2`, the closure defect. -/
noncomputable def δ₀ : ℝ := (Real.sqrt 5 - 2) / 2

/-- Anchor dimension `N = rank·V₁₃ = 3·13 = 39`. -/
theorem anchor_dim : 3 * 13 = 39 := by decide

private lemma sqrt5_sq : (Real.sqrt 5) ^ 2 = 5 := Real.sq_sqrt (by norm_num)

/-- `δ₀ = 1/(2φ³)` — the same closure defect used across the ledger. -/
theorem delta0_eq_phi : δ₀ = 1 / (2 * phi ^ 3) := by
  unfold δ₀ phi
  have h5 : (Real.sqrt 5) ^ 2 = 5 := sqrt5_sq
  have hs : Real.sqrt 5 > 0 := Real.sqrt_pos.mpr (by norm_num)
  field_simp
  nlinarith [h5, hs]

/-- `δ₀ > 0`. -/
theorem delta0_pos : (0 : ℝ) < δ₀ := by
  unfold δ₀
  have : (2 : ℝ) < Real.sqrt 5 := by
    have h : (2:ℝ)^2 < (Real.sqrt 5)^2 := by rw [sqrt5_sq]; norm_num
    nlinarith [Real.sqrt_nonneg 5, h]
  linarith

/-- **The norm identity**: summing `39` equal components `(δ₀/√39)²` gives `δ₀²`. The `39` cancels the
    `(√39)²` in the denominator — exact, no numerics. -/
theorem defect_norm_sq :
    (39 : ℝ) * (δ₀ / Real.sqrt 39) ^ 2 = δ₀ ^ 2 := by
  have h39 : (Real.sqrt 39) ^ 2 = 39 := Real.sq_sqrt (by norm_num)
  have h39ne : Real.sqrt 39 ≠ 0 := by
    have : (0:ℝ) < Real.sqrt 39 := Real.sqrt_pos.mpr (by norm_num)
    exact ne_of_gt this
  field_simp
  rw [h39]
  ring

/-- Hence `‖defect‖ = δ₀`: the Euclidean norm of the `39`-component defect vector is exactly `δ₀`. -/
theorem defect_norm_eq_delta0 :
    Real.sqrt ((39 : ℝ) * (δ₀ / Real.sqrt 39) ^ 2) = δ₀ := by
  rw [defect_norm_sq, Real.sqrt_sq (le_of_lt delta0_pos)]

end D0.VNext2.HiggsAnchorProjector
