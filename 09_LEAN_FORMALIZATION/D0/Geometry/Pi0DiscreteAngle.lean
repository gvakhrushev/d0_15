import D0.Core.Phi
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

end D0.Geometry
