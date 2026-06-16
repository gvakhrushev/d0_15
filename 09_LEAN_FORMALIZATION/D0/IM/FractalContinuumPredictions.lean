import D0.Core.Phi
import D0.Dynamics.PisotContraction
import D0.Cosmology.ArchiveConvexity
import Mathlib.Tactic

/-!
# D0-IM-PRED-001 — fractal continuum predictions (archive increment sign pattern)

BOOK_01/06. Python certificate: `05_CERTS/vp_fractal_continuum_predictions.py`.

For the contracting φ-tick `Aₙ = (1/φ)ⁿ`, the archive increment `ΔBₙ = (1−1/φ)·Aₙ = (1/φ)^{n+2}` is
(i) strictly positive (archive always grows) and (ii) strictly DECREASING in absolute terms
(`Δ²Bₙ < 0`, deceleration), while the RELATIVE archive ratio ACCELERATES (`Δ² > 0`). The opposite
second-difference signs (absolute decelerates, relative accelerates) are the row's "sign corrected"
headline. The key φ-identity is `1 − 1/φ = (1/φ)²`.

The relative-acceleration leg reuses `D0.Cosmology.archive_growth_strictly_convex` verbatim
(`Δ²(φⁿ−1) = φⁿ(φ−1)² > 0`). The continuum-envelope limit `Aₙ ≈ A₀·e^{−(log φ)n}` and the banner
"predictions" readings stay in the cert.
-/

namespace D0.IM

open D0

/-- Archive increment after `n` ticks: `ΔBₙ = (1/φ)^{n+2}` (`= (1−1/φ)·(1/φ)ⁿ`). -/
noncomputable def predIncrement (n : ℕ) : ℝ := phi⁻¹ ^ (n + 2)

/-- The driving φ-identity: `1 − 1/φ = (1/φ)²` (the trace fraction equals the squared rate). -/
theorem pred_one_sub_inv_eq_sq : 1 - phi⁻¹ = phi⁻¹ ^ 2 := by
  rw [phi_inv_eq_primitiveRoot]; linear_combination -primitive_root_satisfies

/-- **Archive increment strictly positive:** `0 < ΔBₙ` for every `n` (archive always grows). -/
theorem pred_increment_pos (n : ℕ) : 0 < predIncrement n := by
  unfold predIncrement
  exact pow_pos (inv_pos.mpr (by linarith [phi_gt_one])) (n + 2)

/-- Closed form of the second difference: `ΔBₙ₊₁ − ΔBₙ = (1/φ)^{n+2}·(1/φ − 1)`. -/
theorem pred_second_difference (n : ℕ) :
    predIncrement (n + 1) - predIncrement n = phi⁻¹ ^ (n + 2) * (phi⁻¹ - 1) := by
  unfold predIncrement; ring

/-- **Absolute deceleration:** `Δ²Bₙ < 0` for every `n` (the increment strictly decreases). -/
theorem pred_second_difference_neg (n : ℕ) : predIncrement (n + 1) - predIncrement n < 0 := by
  rw [pred_second_difference]
  have h0 : 0 < phi⁻¹ ^ (n + 2) := pow_pos (inv_pos.mpr (by linarith [phi_gt_one])) (n + 2)
  have h1 : phi⁻¹ - 1 < 0 := by
    rw [phi_inv_eq_primitiveRoot]; unfold primitiveRoot; linarith [sqrt_five_lt_three]
  exact mul_neg_of_pos_of_neg h0 h1

/-- **Relative acceleration:** the relative archive `φⁿ−1` has strictly positive second difference —
reused verbatim from `D0.Cosmology.archive_growth_strictly_convex` (opposite sign to the absolute one). -/
theorem pred_relative_accelerates (n : ℕ) :
    D0.Cosmology.archiveGrowth (n + 2) - 2 * D0.Cosmology.archiveGrowth (n + 1)
      + D0.Cosmology.archiveGrowth n > 0 :=
  D0.Cosmology.archive_growth_strictly_convex n

/-- **D0-IM-PRED-001.** `1 − 1/φ = (1/φ)²`; the archive increment is strictly positive and strictly
decelerating for every `n`; and the relative archive ratio strictly accelerates (opposite signs). -/
theorem fractal_continuum_predictions_cert :
    (1 - phi⁻¹ = phi⁻¹ ^ 2) ∧
    (∀ n : ℕ, 0 < predIncrement n) ∧
    (∀ n : ℕ, predIncrement (n + 1) - predIncrement n < 0) ∧
    (∀ n : ℕ, D0.Cosmology.archiveGrowth (n + 2) - 2 * D0.Cosmology.archiveGrowth (n + 1)
      + D0.Cosmology.archiveGrowth n > 0) :=
  ⟨pred_one_sub_inv_eq_sq, pred_increment_pos, pred_second_difference_neg, pred_relative_accelerates⟩

end D0.IM
