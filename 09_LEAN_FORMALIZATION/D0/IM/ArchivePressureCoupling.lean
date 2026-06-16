import D0.Cosmology.ArchiveConvexity
import D0.Core.Phi
import D0.Dynamics.PisotContraction
import Mathlib.Tactic

/-!
# D0-IM-COSMO-002 — archive pressure coupling from relative acceleration

BOOK_06/08. Python certificate: `05_CERTS/vp_archive_pressure_coupling_from_relative_acceleration.py`.

The relative archive ratio accelerates: its discrete second difference is the strictly-positive
`φⁿ(φ−1)²` (the same convexity kernel as `D0.Cosmology.ArchiveConvexity`). The loop pressure split
couples a positive internal coefficient `C_R > 0` to this acceleration, so the relative pressure
increment `C_R · Δ²Rₙ > 0`; the wrong-sign coupling `−C_R` gives a strictly negative increment and the
zero coupling gives exactly `0` (the cert's two negative controls).

This module machine-checks that finite sign content (reusing `archive_growth_strictly_convex`). No
survey/H₀/scale-factor fit is claimed — that stays in the cert.
-/

namespace D0.IM

open D0

/-- The relative archive acceleration `Δ²Rₙ` (the strictly-convex `φⁿ(φ−1)²` second difference). -/
noncomputable def relAccel (n : ℕ) : ℝ :=
  D0.Cosmology.archiveGrowth (n + 2) - 2 * D0.Cosmology.archiveGrowth (n + 1)
    + D0.Cosmology.archiveGrowth n

/-- **Relative archive accelerates:** `Δ²Rₙ > 0` (reused from `ArchiveConvexity`). -/
theorem relAccel_pos (n : ℕ) : 0 < relAccel n :=
  D0.Cosmology.archive_growth_strictly_convex n

/-- **Pressure increment positive:** `C_R · Δ²Rₙ > 0` for any positive internal coupling `C_R`. -/
theorem pressure_increment_pos (cR : ℝ) (hcR : 0 < cR) (n : ℕ) : 0 < cR * relAccel n :=
  mul_pos hcR (relAccel_pos n)

/-- **Negative control (wrong-sign coupling):** `−C_R · Δ²Rₙ` is NOT positive. -/
theorem neg_coupling_not_pos (cR : ℝ) (hcR : 0 < cR) (n : ℕ) : ¬ (0 < (-cR) * relAccel n) := by
  intro h; nlinarith [mul_pos hcR (relAccel_pos n)]

/-- **Negative control (zero coupling):** `0 · Δ²Rₙ = 0` (not positive). -/
theorem zero_coupling_zero (n : ℕ) : (0 : ℝ) * relAccel n = 0 := by ring

/-- **D0-IM-COSMO-002.** The relative archive accelerates (`Δ²Rₙ>0`), a positive coupling gives a
positive pressure increment, and the wrong-sign / zero couplings fail positivity. -/
theorem relative_pressure_bridge_law :
    (∀ n : ℕ, 0 < relAccel n) ∧
    (∀ cR : ℝ, 0 < cR → ∀ n : ℕ, 0 < cR * relAccel n) ∧
    (∀ cR : ℝ, 0 < cR → ∀ n : ℕ, ¬ (0 < (-cR) * relAccel n)) ∧
    (∀ n : ℕ, (0 : ℝ) * relAccel n = 0) :=
  ⟨relAccel_pos, pressure_increment_pos, neg_coupling_not_pos, zero_coupling_zero⟩

end D0.IM
