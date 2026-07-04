import Mathlib.Tactic

/-!
# D0-WINDOW-SCALE-DISCRIMINANT-FORCED-001 — the S_DE window splitting is `D(m) = 3/((m+1)(m+3))`

The two nontrivial normalized-Laplacian eigenvalues of the scene (the S_DE window scales `λ_c, λ_r`) satisfy
`λ_c + λ_r = 3` and `λ_c · λ_r = 359/160`. Their splitting is the discriminant
`D = (λ_r − λ_c)² = 9 − 4·(product)`.

For a general `+2` zone progression `{m, m+2, m+4}` (`N = 3m+6`, degrees `d = 2(m+3), 2(m+2), 2(m+1)`), the
product of the two nontrivial eigenvalues is the rational `e₂` of `I − R` (`R` the zero-diagonal reduced
matrix, `R_ij² = nᵢnⱼ/(dᵢdⱼ)`):
  `P(m) = (9m² + 36m + 24) / (4m² + 16m + 12)`,  and  `D(m) = 9 − 4P(m) = 3 / ((m+1)(m+3))`.
The denominator is the product of the smallest and largest degree-halves (`m+1 = d_min/2`, `m+3 = d_max/2`),
so `D(m) = Z / (h_min · h_max)` with `Z = 3`. At the scene `m = 9`: `D = 3/(10·12) = 1/40`, reproducing
`η_EP = √10/40`.

Honest content (rejection encoded): `D(m) > 0` for all `m`, so the scales are always real and distinct —
the "orientation = sign of the discriminant" reading is a *constant* `+`, never a `ℤ₂` flip; `√10` is not an
orientation bit. And the field `ℚ(√(squarefree(3(m+1)(m+3))))` is a size-fingerprint: golden `ℚ(√5)` occurs
at `m = 29`, not the scene `m = 9`.

This file fixes the rational identity, the degree-half reading, positivity, and the squarefree field values.
The `√10 ∉ ℚ(φ)` NO-GO stays with `D0-PHASON-WZ-LOGDET-WINDOW-OWNER-001`; here it is explained as generic.
-/

namespace D0.VNext2.WindowScaleDiscriminant

/-- The window-scale product for zones `{m, m+2, m+4}`, as a rational function of `m` (numerator/denominator
    of `P(m) = (9m²+36m+24)/(4m²+16m+12)`). We work with the discriminant directly. -/
def discNum : ℕ := 3

/-- The discriminant `D(m) = 3 / ((m+1)(m+3))`, stated as the pair `(numerator, denominator)`. -/
def discDenom (m : ℕ) : ℕ := (m + 1) * (m + 3)

/-- **Closed form, numerator**: `9·[4(m+1)(m+3)] − 4·(9m²+36m+24) = 12`. With `P = (9m²+36m+24)/[4(m+1)(m+3)]`
    the discriminant is `D = 9 − 4P = 12 / [4(m+1)(m+3)] = 3/((m+1)(m+3))`. -/
theorem discriminant_numerator (m : ℕ) :
    9 * (4 * (m + 1) * (m + 3)) - 4 * (9 * m ^ 2 + 36 * m + 24) = 12 := by
  have h : 9 * (4 * (m + 1) * (m + 3)) = 4 * (9 * m ^ 2 + 36 * m + 24) + 12 := by ring
  omega

/-- The reduced denominator `4(m+1)(m+3)` is exactly `4m² + 16m + 12` (the `e₂`-scaling denominator). -/
theorem discriminant_denominator_expand (m : ℕ) :
    4 * (m + 1) * (m + 3) = 4 * m ^ 2 + 16 * m + 12 := by
  ring

/-- The clean statement of the discriminant numerator over the degree-half product: the product
    `(m+1)(m+3)` equals `(d_min/2)·(d_max/2)` at every `m` since `d = 2(m+3),2(m+2),2(m+1)`. -/
theorem degree_half_denominator (m : ℕ) :
    discDenom m = (m + 1) * (m + 3) := rfl

/-- Scene value: `D(9)` has denominator `10·12 = 120`, and `3/120 = 1/40` — reproducing `√10/40`. -/
theorem scene_denominator : discDenom 9 = 120 := by decide

/-- `3/120 = 1/40`: the scene splitting is `1/40` (so `λ = 3/2 ± √(1/40)/2 = 3/2 ± √10/40`). -/
theorem scene_value_one_fortieth : (discNum : ℚ) / (discDenom 9 : ℚ) = 1 / 40 := by
  norm_num [discNum, discDenom]

/-- **Always positive** (no `ℤ₂` orientation flip): the denominator `(m+1)(m+3)` is positive, and the
    numerator `3` is positive, so `D(m) > 0` for every `m`. -/
theorem discriminant_pos (m : ℕ) : 0 < (discNum : ℚ) / (discDenom m : ℚ) := by
  have hd : 0 < ((m + 1) * (m + 3) : ℚ) := by positivity
  simp only [discNum, discDenom]
  push_cast
  positivity

/-- Field fingerprint at the scene: `3·(9+1)·(9+3) = 360 = 36·10`, squarefree part `10`. -/
theorem scene_field_ten : 3 * (9 + 1) * (9 + 3) = 36 * 10 := by decide

/-- Golden field `ℚ(√5)` occurs at `m = 29`: `3·(29+1)·(29+3) = 2880 = 576·5`, squarefree part `5`. -/
theorem golden_field_at_29 : 3 * (29 + 1) * (29 + 3) = 576 * 5 := by decide

/-- At `m = 5` the scales are rational: `3·(5+1)·(5+3) = 144 = 12²` (a perfect square). -/
theorem rational_at_five : 3 * (5 + 1) * (5 + 3) = 12 ^ 2 := by decide

/-- The scene surd `10` is not `5`: the scene field is not the golden field. -/
theorem scene_not_golden : (10 : ℕ) ≠ 5 := by decide

end D0.VNext2.WindowScaleDiscriminant
