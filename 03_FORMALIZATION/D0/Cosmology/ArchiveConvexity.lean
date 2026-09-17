import D0.Core.Phi
import D0.Dynamics.PisotContraction
import Mathlib.Tactic

/-!
# D0-ARCHIVE-CONVEXITY-001 — forced convexity of the φ-archive growth `Rₙ = φⁿ − 1`

The discrete kernel shared by the cosmological "phason-thawing / accelerating-expansion" readings: the
archive growth `Rₙ = φⁿ − 1` has a forced positive second difference
`Δ²Rₙ = R_{n+2} − 2R_{n+1} + Rₙ = φⁿ (φ − 1)² > 0` — strict discrete convexity, an exact φ-algebra
identity (it does not even need `φ² = φ + 1`, only `φ > 1`). Reuses `D0.Core.Phi` + the φ-bounds from
`D0.Dynamics.PisotContraction`.

**Scope (honest):** this is the discrete convexity kernel only. The cosmological `w > −1` /
accelerating-expansion / DESI-DR readings built on top stay empirical certs/passports.
-/

namespace D0.Cosmology

open D0

/-- The φ-archive growth `Rₙ = φⁿ − 1`. -/
noncomputable def archiveGrowth (n : ℕ) : ℝ := phi ^ n - 1

/-- **Forced second difference:** `Δ²Rₙ = φⁿ (φ − 1)²` — an exact φ-algebra identity. -/
theorem archive_convexity_second_difference (n : ℕ) :
    archiveGrowth (n + 2) - 2 * archiveGrowth (n + 1) + archiveGrowth n = phi ^ n * (phi - 1) ^ 2 := by
  unfold archiveGrowth; ring

/-- **Strict discrete convexity:** the second difference is strictly positive (`φ > 1`). -/
theorem archive_convexity_positive (n : ℕ) : 0 < phi ^ n * (phi - 1) ^ 2 := by
  have h1 : (0 : ℝ) < phi := by linarith [phi_gt_one]
  have h2 : phi - 1 ≠ 0 := by have := phi_gt_one; linarith
  positivity

/-- **D0-ARCHIVE-CONVEXITY-001.** `Rₙ = φⁿ − 1` is strictly convex: `Δ²Rₙ = φⁿ(φ−1)² > 0`. -/
theorem archive_growth_strictly_convex (n : ℕ) :
    archiveGrowth (n + 2) - 2 * archiveGrowth (n + 1) + archiveGrowth n > 0 := by
  rw [archive_convexity_second_difference]; exact archive_convexity_positive n

end D0.Cosmology
