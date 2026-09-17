import Mathlib.Tactic

/-!
# D0-PROTON-001 (readout leg) — the proton readout `306` as an exact rational identity

The §04 proton readout `306 = 3960/13 + 3960/(13·20·11)` is an exact rational identity (the
electroweak window `13`, the `+2`-ladder factors `20, 11`). This module promotes that structural
readout identity to a machine-checked Lean theorem, with the divisor-`12` control failing.

**Scope (honest):** this is the structural READOUT identity only. The downstream physical
`M_p ≈ 938 MeV` vs PDG comparison stays an empirical cert/passport (a float-vs-measurement check, not
a Lean theorem).
-/

namespace D0.Matter

/-- The proton readout `306` is the exact rational `3960/13 + 3960/(13·20·11)`. -/
theorem proton_readout306_rational : (3960 : ℚ) / 13 + 3960 / (13 * 20 * 11) = 306 := by norm_num

/-- Control: the divisor-`12` variant does not give `306` — the electroweak window `13` is forced. -/
theorem proton_readout306_control : (3960 : ℚ) / 12 + 3960 / (12 * 20 * 11) ≠ 306 := by norm_num

end D0.Matter
