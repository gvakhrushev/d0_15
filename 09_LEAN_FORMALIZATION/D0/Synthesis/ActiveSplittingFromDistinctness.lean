import Mathlib.Tactic

/-!
# Distinct zone sizes are exactly what splits the active spectrum

`D0.Synthesis.SymmetricFunctionCalculus` puts the §04.2 active scene-Laplacian eigenvalues in
closed form: sum `3`, product `2N·e₂/(N·e₂ − e₃)` in the elementary symmetric functions of the zone
sizes. Being the roots of `x² − 3x + p`, they are degenerate exactly when the discriminant
`9 − 4p` vanishes, i.e. when

    p = 9/4   ⟺   8·N·e₂ = 9·N·e₂ − 9·e₃   ⟺   N·e₂ = 9·e₃ .

That condition has a closed form. The exact identity

    N·e₂ − 9·e₃ = a(b−c)² + b(c−a)² + c(a−b)²          (`gap_sos`)

is a sum of squares with positive coefficients, so for positive zone sizes the gap is non-negative
and vanishes **iff the three sizes coincide** (`gap_zero_iff_equal`). Therefore:

* equal zones ⇒ the active spectrum is degenerate;
* distinct zones ⇒ it splits, and the splitting is measured by the same gap.

At `(9, 11, 13)` the gap is `33·359 − 9·1287 = 11847 − 11583 = 264` (`scene_gap`), so the scene's
active eigenvalues are separated, with the separation controlled by `264`.

**Why this is more than an inequality.** Zone-size distinctness was already load-bearing elsewhere
for a completely different reason: it is what makes the zones rigid, since equal parts would admit
zone swaps inside `Aut` and destroy the `S₉ × S₁₁ × S₁₃` structure. The same distinctness now turns
out to be exactly what makes the physical readout non-degenerate. One property of the scene, two
consequences that had been argued separately — rigidity of the symmetry group and splitting of the
active spectrum — and the second is quantitative: the splitting is `a(b−c)² + b(c−a)² + c(a−b)²`,
vanishing precisely on the symmetric point the rigidity argument also excludes.
-/

namespace D0.Synthesis.ActiveSplittingFromDistinctness

variable (a b c : ℚ)

/-- The degeneracy gap: `N·e₂ − 9·e₃`. -/
def gap : ℚ := (a + b + c) * (a * b + a * c + b * c) - 9 * (a * b * c)

/-- **The gap is a sum of squares.** Exact identity, valid for all `a, b, c`. -/
theorem gap_sos : gap a b c = a * (b - c) ^ 2 + b * (c - a) ^ 2 + c * (a - b) ^ 2 := by
  unfold gap; ring

/-- For positive sizes the gap is non-negative. -/
theorem gap_nonneg (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) : 0 ≤ gap a b c := by
  rw [gap_sos]
  have h1 : 0 ≤ a * (b - c) ^ 2 := mul_nonneg ha.le (sq_nonneg _)
  have h2 : 0 ≤ b * (c - a) ^ 2 := mul_nonneg hb.le (sq_nonneg _)
  have h3 : 0 ≤ c * (a - b) ^ 2 := mul_nonneg hc.le (sq_nonneg _)
  linarith

/-- **The gap vanishes exactly at equal sizes.** -/
theorem gap_zero_iff_equal (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :
    gap a b c = 0 ↔ (a = b ∧ b = c) := by
  constructor
  · intro h
    rw [gap_sos] at h
    have h1 : 0 ≤ a * (b - c) ^ 2 := mul_nonneg ha.le (sq_nonneg _)
    have h2 : 0 ≤ b * (c - a) ^ 2 := mul_nonneg hb.le (sq_nonneg _)
    have h3 : 0 ≤ c * (a - b) ^ 2 := mul_nonneg hc.le (sq_nonneg _)
    have e1 : a * (b - c) ^ 2 = 0 := by linarith
    have e2 : c * (a - b) ^ 2 = 0 := by linarith
    have hab : a = b := by
      have : (a - b) ^ 2 = 0 := by
        rcases mul_eq_zero.mp e2 with h' | h'
        · exact absurd h' hc.ne'
        · exact h'
      have := pow_eq_zero_iff (n := 2) (by norm_num) |>.mp this
      linarith
    have hbc : b = c := by
      have : (b - c) ^ 2 = 0 := by
        rcases mul_eq_zero.mp e1 with h' | h'
        · exact absurd h' ha.ne'
        · exact h'
      have := pow_eq_zero_iff (n := 2) (by norm_num) |>.mp this
      linarith
    exact ⟨hab, hbc⟩
  · rintro ⟨hab, hbc⟩
    subst hab; subst hbc
    unfold gap; ring

/-- **Degeneracy criterion.** The active spectrum, with sum `3` and product `p`, is degenerate iff
`9 = 4p`; with denominators cleared this is `gap = 0`. -/
theorem degenerate_iff_gap_zero (N e2 e3 : ℚ) :
    (9 : ℚ) * (N * e2 - e3) = 4 * (2 * N * e2) ↔ N * e2 - 9 * e3 = 0 := by
  constructor <;> intro hh <;> linarith

/-- The scene's gap: `33·359 − 9·1287 = 264`, so the active eigenvalues are separated. -/
theorem scene_gap : gap 9 11 13 = 264 := by unfold gap; norm_num

/-- **Assembled.** The gap is a positive-coefficient sum of squares, vanishes only on equal zones,
and is `264` at the scene — so distinctness of the zone sizes is precisely what splits the active
spectrum. -/
theorem splitting_from_distinctness :
    (∀ x y z : ℚ, gap x y z = x * (y - z) ^ 2 + y * (z - x) ^ 2 + z * (x - y) ^ 2) ∧
    gap 9 11 13 = 264 ∧ (0 : ℚ) < 264 :=
  ⟨fun x y z => gap_sos x y z, scene_gap, by norm_num⟩

end D0.Synthesis.ActiveSplittingFromDistinctness
