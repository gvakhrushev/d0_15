import D0.Core.Phi
import D0.Core.Delta
import Mathlib.Tactic

/-!
# D0-PI0-DISCRETE-ANGLE-001 — the seam holonomy angle `2π₀(2−φ) = 12/5` exactly in ℚ(φ)

`π₀ = (6/5)φ²` is the angular measure of the discrete minimal cycle, whose value is derived in
BOOK_04 §04.6.π.4 from the δ₀-closure balance (REUSED, not re-derived). The new exact identity here —
the algebraic content the α closure-holonomy depends on (`vp_seam_holonomy_alpha.py`) — is that the
seam holonomy angle `2·π₀·(2−φ)` is the closed rational `12/5`, using only `φ² = φ + 1`.

Cert: `05_CERTS/vp_pi0_discrete_angle.py` (symbolic ℚ(φ) + the π-vs-π₀ exactness control).
-/

namespace D0.Geometry

open D0

/-- `π₀ = (6/5)φ²`, the discrete-minimal-cycle angular measure (value owned by BOOK_04 §04.6.π.4). -/
noncomputable def pi0 : ℝ := (6 / 5) * phi ^ 2

/-- **D0-PI0-DISCRETE-ANGLE-001.** The seam holonomy angle is the closed rational `12/5`:
`2·π₀·(2−φ) = 12/5` exactly (in ℚ(φ), via `φ² = φ + 1`). -/
theorem seam_angle_eq_twelve_fifths : 2 * pi0 * (2 - phi) = 12 / 5 := by
  unfold pi0
  linear_combination (12 / 5 * (1 - phi)) * phi_sq

/-- **THE 04.6.π.4, machine-checked.** `π₀ = (6/5)φ²` is *forced*, not chosen: the δ₀-closure balance
`δ₀ = 3/(5·π₀·φ)` (the angular-microquantum closure of BOOK_04 §04.6.π.1/π.C) together with the owned
`δ₀ = 1/(2φ³)` (`D0.Core.Delta`) pins `π₀` uniquely to `(6/5)φ²`. Any `p ≠ 0` satisfying the same closure
balance equals `pi0`; this closes the "cone-angle `2π₀` micro-derivation" named gap that the α
closure-holonomy and the PMNS seam-topology rule lean on. -/
theorem pi0_forced_by_closure_balance (p : ℝ) (hp : p ≠ 0)
    (hbal : delta0 = 3 / (5 * p * phi)) : p = pi0 := by
  have hφ : phi ≠ 0 := by
    have hpos : (0 : ℝ) < phi := by unfold phi; positivity
    exact ne_of_gt hpos
  rw [delta_phi_cubed] at hbal
  have h2c : (2 : ℝ) * phi ^ 3 ≠ 0 := mul_ne_zero (by norm_num) (pow_ne_zero 3 hφ)
  have h5p : (5 : ℝ) * p * phi ≠ 0 := mul_ne_zero (mul_ne_zero (by norm_num) hp) hφ
  rw [div_eq_div_iff h2c h5p] at hbal
  unfold pi0
  have hx : (5 * p) * phi = (6 * phi ^ 2) * phi := by linear_combination hbal
  have hgoal : 5 * p = 6 * phi ^ 2 := mul_right_cancel₀ hφ hx
  linarith [hgoal]

end D0.Geometry
