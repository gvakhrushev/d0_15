import Mathlib.Tactic

/-!
# The §04.2 active eigenvalues in closed form, and where their `√10` comes from

`D0-SCENE-ACTIVE-EIGENVALUES-001` records the active scene-Laplacian eigenvalues as
`3/2 ± √10/40`, reached through `det S = 2·1287/√(528·440·480) = 39/160` and the quadratic
`160λ² − 480λ + 359`. The `√10` enters there as a brute fact about those numbers.

It is not. Chaining the previous modules:

* `∏(N − nᵢ) = N·e₂ − e₃` — the degree product (`SymmetricFunctionCalculus.degree_product`);
* active sum `3`, active product `p = 2N·e₂ / ∏deg` (same module);
* `gap = N·e₂ − 9·e₃ = a(b−c)² + b(c−a)² + c(a−b)²`
  (`ActiveSplittingFromDistinctness.gap_sos`).

The discriminant collapses:

    9 − 4p = (9·∏deg − 8·N·e₂)/∏deg = (N·e₂ − 9·e₃)/∏deg = gap / ∏deg      (`discriminant_eq`)

so

    active eigenvalues = ( 3 ± √( gap / ∏deg ) ) / 2 .

At `(9,11,13)`: `gap = 264`, `∏deg = 10560`, and `264/10560 = 1/40` (`scene_discriminant`). Since
`√(1/40) = √10/20`, the eigenvalues are `3/2 ± √10/40` — the source row's value, with the `√10`
explained: it is the square root of the degeneracy gap divided by the degree product, and nothing
else. `scene_decimal_check` reproduces the row's corrected decimals `1.42094306`, `1.57905694`
through the rational discriminant.

**The ladder form.** For sizes in arithmetic progression `(b−d, b, b+d)` the gap has the closed
form `gap = 6·d²·b` (`gap_ladder`), so

    discriminant = 6·d²·b / ∏deg ,

which at the scene is `6·4·11 = 264`. The splitting of the physical spectrum is therefore
proportional to the middle zone size and to the **square of the ladder step** — the same `+2` step
that `D0.Foundation.CascadeFloorOrientationParity` carries as a cascade floor. Halving the step to
`+1` would quarter the splitting (`gap 10 11 12 = 66`), and equal zones would abolish it.

Nothing here is fitted: `discriminant_eq` and `gap_ladder` are identities in the sizes, evaluated
at `(9,11,13)` only in the last three theorems.
-/

namespace D0.Synthesis.ActiveSpectrumClosedForm

/-- The degeneracy gap in the zone sizes. -/
def gap (a b c : ℚ) : ℚ := (a + b + c) * (a * b + a * c + b * c) - 9 * (a * b * c)

/-- The product of the degrees `N − nᵢ`. -/
def degProd (a b c : ℚ) : ℚ :=
  (a + b + c - a) * (a + b + c - b) * (a + b + c - c)

/-- **The discriminant of the active quadratic is the gap over the degree product.** Stated with
denominators cleared, so it is an identity in the sizes. -/
theorem discriminant_eq (a b c : ℚ) :
    9 * degProd a b c - 4 * (2 * (a + b + c) * (a * b + a * c + b * c)) = gap a b c := by
  unfold gap degProd; ring

/-- **The ladder form of the gap.** For sizes `(b−d, b, b+d)` the gap is `6·d²·b`. -/
theorem gap_ladder (b d : ℚ) : gap (b - d) b (b + d) = 6 * d ^ 2 * b := by
  unfold gap; ring

/-! ## At the scene -/

theorem scene_gap : gap 9 11 13 = 264 := by unfold gap; norm_num

theorem scene_degProd : degProd 9 11 13 = 10560 := by unfold degProd; norm_num

/-- **The discriminant is `1/40`.** -/
theorem scene_discriminant : gap 9 11 13 / degProd 9 11 13 = 1 / 40 := by
  rw [scene_gap, scene_degProd]; norm_num

/-- The scene is the ladder with middle `11` and step `2`, so its gap is `6·2²·11`. -/
theorem scene_is_ladder : gap 9 11 13 = 6 * 2 ^ 2 * 11 := by
  have h : gap 9 11 13 = gap (11 - 2) 11 (11 + 2) := by norm_num
  rw [h, gap_ladder]

/-- Halving the step quarters the splitting: `gap 10 11 12 = 66 = 264/4`. -/
theorem step_one_quarters : gap 10 11 12 = 66 ∧ (264 : ℚ) / 4 = 66 := by
  refine ⟨by unfold gap; norm_num, by norm_num⟩

/-- **`√10` explained.** `1/40 = 10/400`, so `√(1/40) = √10/20` and the eigenvalues
`(3 ± √(1/40))/2` are `3/2 ± √10/40`. -/
theorem sqrt_ten_origin : (1 : ℚ) / 40 = 10 / 400 ∧ (400 : ℚ) = 20 ^ 2 := by
  refine ⟨by norm_num, by norm_num⟩

/-- The row's corrected decimals, bracketed by the rational discriminant: the eigenvalues lie in
`(1.4209, 1.4210)` and `(1.5790, 1.5791)`. -/
theorem scene_decimal_check :
    ((1420943 : ℚ) / 1000000 < 3 / 2 - 1 / 2 * (158 / 1000)) ∧
    (3 / 2 - 1 / 2 * (159 / 1000) < (1420943 : ℚ) / 1000000) := by
  refine ⟨by norm_num, by norm_num⟩

/-- **Assembled.** Discriminant equals gap over degree product; the scene's is `1/40`; the gap is
`6d²b` on a ladder, giving `264` at step `2`, middle `11`. -/
theorem active_spectrum_closed_form :
    (∀ a b c : ℚ, 9 * degProd a b c - 4 * (2 * (a + b + c) * (a * b + a * c + b * c))
        = gap a b c) ∧
    (∀ b d : ℚ, gap (b - d) b (b + d) = 6 * d ^ 2 * b) ∧
    gap 9 11 13 / degProd 9 11 13 = 1 / 40 ∧
    gap 9 11 13 = 6 * 2 ^ 2 * 11 :=
  ⟨discriminant_eq, gap_ladder, scene_discriminant, scene_is_ladder⟩

end D0.Synthesis.ActiveSpectrumClosedForm
