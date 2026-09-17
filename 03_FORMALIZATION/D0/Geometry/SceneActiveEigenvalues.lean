import Mathlib.Data.Real.Sqrt
import Mathlib.Tactic

/-!
# D0-SCENE-ACTIVE-EIGENVALUES-001 — exact active eigenvalues of the reduced scene Laplacian

BOOK_04 §04.2 reduces the normalized scene Laplacian `L_sym(K(9,11,13))` on the part-constant
subspace to a 3×3 operator whose spectrum is `{0, λ₁, λ₂}`. The reduced off-diagonal operator `S`
has `det(S) = 2·(9·11·13)/√(528·440·480) = 2574/10560 = 39/160` (since `√(528·440·480) = 10560`),
so `λ₁+λ₂ = 3` (trace) and `λ₁λ₂ = 2 + det(S) = 359/160`. Hence `λ₁, λ₂` are the roots of
`160λ² − 480λ + 359` — i.e. EXACTLY `3/2 ± √10/40`. This replaces §04.2's numerical readout (which was
also slightly wrong: its decimals summed to `2.999997… ≠ 3`). Cert: `vp_scene_active_eigenvalues_exact.py`.
-/

namespace D0

/-- The upper active eigenvalue `3/2 + √10/40` is a root of `160λ² − 480λ + 359`. -/
theorem scene_active_eigenvalue_plus :
    160 * (3 / 2 + Real.sqrt 10 / 40) ^ 2 - 480 * (3 / 2 + Real.sqrt 10 / 40) + 359 = 0 := by
  have h : Real.sqrt 10 ^ 2 = 10 := Real.sq_sqrt (by norm_num)
  linear_combination (1 / 10 : ℝ) * h

/-- The lower active eigenvalue `3/2 − √10/40` is a root of `160λ² − 480λ + 359`. -/
theorem scene_active_eigenvalue_minus :
    160 * (3 / 2 - Real.sqrt 10 / 40) ^ 2 - 480 * (3 / 2 - Real.sqrt 10 / 40) + 359 = 0 := by
  have h : Real.sqrt 10 ^ 2 = 10 := Real.sq_sqrt (by norm_num)
  linear_combination (1 / 10 : ℝ) * h

/-- The two active eigenvalues sum to exactly `3` (= trace of the reduced Laplacian). -/
theorem scene_active_eigenvalues_sum :
    (3 / 2 + Real.sqrt 10 / 40) + (3 / 2 - Real.sqrt 10 / 40) = 3 := by ring

/-- The two active eigenvalues multiply to exactly `359/160` (= `2 + det(S)`, `det(S)=39/160`). -/
theorem scene_active_eigenvalues_prod :
    (3 / 2 + Real.sqrt 10 / 40) * (3 / 2 - Real.sqrt 10 / 40) = 359 / 160 := by
  have h : Real.sqrt 10 ^ 2 = 10 := Real.sq_sqrt (by norm_num)
  linear_combination (-1 / 1600 : ℝ) * h

end D0
