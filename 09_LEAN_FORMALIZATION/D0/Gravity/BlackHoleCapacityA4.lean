import Mathlib.Tactic

/-!
# D0-BH-CAPACITY-A4-001 — seam entropy `S(n) = n/4` (the area law `A/4`)

The §07 black-hole seam entropy is `S(n) = n/4` — the discrete area law `S = A/4`, with the divisor
`4 = |ABCD|` (the role count). This module proves the exact rational facts: `S(n)·4 = n`, the
unit-area law `S(4) = 1`, and the negative controls that the divisor is `4`, not `2` or `8`.

**Scope (honest):** exact rational structural identity. The Bekenstein–Hawking `S = A/(4Għ)` continuum
identification (the dimensionful bridge) stays the cert/owner-edge.
-/

namespace D0.Gravity

/-- Seam entropy `S(n) = n/4` (area law `A/4`): `S(n)·4 = n`, `S(4) = 1`, and the divisor is `4`
(`= |ABCD|`) — not `2` or `8`. -/
theorem bh_entropy_a4 :
    (∀ n : ℤ, (n : ℚ) / 4 * 4 = n) ∧ ((4 : ℚ) / 4 = 1) ∧ ((4 : ℚ) / 2 ≠ 1) ∧ ((4 : ℚ) / 8 ≠ 1) :=
  ⟨fun n => by ring, by norm_num, by norm_num, by norm_num⟩

end D0.Gravity
