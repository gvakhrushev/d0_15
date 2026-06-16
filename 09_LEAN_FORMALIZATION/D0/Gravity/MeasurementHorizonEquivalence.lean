import Mathlib.Data.Real.Sqrt
import Mathlib.Tactic

/-!
# D0-GRAV-004 — measurement horizon equivalence (capacity seam)

BOOK_07. Python certificate: `05_CERTS/vp_measurement_horizon_equivalence.py`.

The measurement seam between an accessible sector (range of `P`) and its complement (range of `Q`) is
the off-diagonal block `QUP` of a unitary rotation `U` at `θ = π/4` (so `c = s = cos(π/4) = √2/2`). The
cert builds the explicit 4×4 `P, Q, U` and asserts: (1) the cross-block `QUP ≠ 0` (a genuine micro-seam,
`‖QUP‖² = s² > 0`); (2) the capacity operator `F = P Uᵀ Q U P` has top eigenvalue `s² = 1/2`, saturated
but strictly sub-unital `0 < capacity < 1` (a macro horizon); (3) information is inaccessible but NOT
deleted (`capacity ≤ 1`, `U` unitary). The unitarity core at `θ=π/4` is `c² + s² = 2s² = 1`.

This module machine-checks the certified finite numbers governed by `s² = 1/2`: the unitarity identity
`2s² = 1`, the capacity value `s² = 1/2 ∈ (0,1)`, and the nonzero seam `s ≠ 0`. The explicit 4×4
`P/Q/U/QUP/F` seam construction (the scaffold producing these numbers) and the physical
measurement/horizon identification stay in the cert.
-/

namespace D0.Gravity

/-- Rotation entry at `θ = π/4`: `s = cos(π/4) = √2/2`. -/
noncomputable def s : ℝ := Real.sqrt 2 / 2

/-- `s² = 1/2` (the single irrational ingredient, reduced via `Real.sq_sqrt`). -/
theorem s_sq : s ^ 2 = 1 / 2 := by
  unfold s
  have h : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  linear_combination (1 / 4 : ℝ) * h

/-- **Unitarity core** at `θ = π/4`: `c² + s² = 2s² = 1` (the `UᵀU = I` block identity, `c = s`). -/
theorem unitarity_pythagorean : s ^ 2 + s ^ 2 = 1 := by
  rw [s_sq]; norm_num

/-- **Capacity value:** the top eigenvalue of `F` is `s² = 1/2`. -/
theorem capacity_value : s ^ 2 = 1 / 2 := s_sq

/-- **Capacity saturated (seam populated):** `0 < capacity`. -/
theorem capacity_pos : (0 : ℝ) < s ^ 2 := by rw [s_sq]; norm_num

/-- **Strictly sub-unital (information inaccessible, NOT deleted):** `capacity < 1`. -/
theorem capacity_lt_one : s ^ 2 < 1 := by rw [s_sq]; norm_num

/-- **Nonzero micro-seam:** `s ≠ 0`, so the cross-block `QUP` is genuinely nonzero. -/
theorem seam_nonzero : s ≠ 0 := by
  have h : (0 : ℝ) < s := by unfold s; positivity
  exact h.ne'

/-- **D0-GRAV-004.** The measurement-horizon seam at `θ=π/4`: unitarity `2s² = 1`, capacity
`s² = 1/2 ∈ (0,1)` (saturated, sub-unital — inaccessible but not deleted), and a nonzero seam `s ≠ 0`. -/
theorem measurement_horizon_equivalence_cert :
    s ^ 2 = 1 / 2 ∧ s ^ 2 + s ^ 2 = 1 ∧ (0 : ℝ) < s ^ 2 ∧ s ^ 2 < 1 ∧ s ≠ 0 :=
  ⟨s_sq, unitarity_pythagorean, capacity_pos, capacity_lt_one, seam_nonzero⟩

end D0.Gravity
