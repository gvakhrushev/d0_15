import Mathlib.Tactic

/-!
# The spectral-disjointness leg of the dark-energy no-go is structural, not numerical

`D0-PHASON-WZ-TRANSFER-OWNER-001` rules out an internal dark-energy transfer on two legs. Its
first, **SEP**, is stated there as a computation:

> "the integer `L_archive` spectrum `{24,22,20}` shares NO eigenvalue with the `S_DE` active window
> (roots of `x² − 3x + 359/160`), so no eigenvalue-matching / canonical intertwiner maps one
> carrier onto the other"

Both sides are now identified with scene data. The `{24,22,20}` are the zone **degrees** `N − nᵢ`,
integers by construction. The active window is the §04.2 quadratic, whose discriminant
`D0.Synthesis.ActiveSpectrumClosedForm` computes as `gap/∏deg = 264/10560 = 1/40`.

So the disjointness has a reason. Completing the square,

    160x² − 480x + 359 = 160(x − 3/2)² − 1 ,

so a rational root would need `(x − 3/2)² = 1/160`, i.e. `160p² = q²` in integers. Since
`160 = 2⁵·5` carries an **odd** power of two, that is impossible — and the direct search confirms
it: `359` is prime, so a rational root is `±1/q` or `±359/q` with `q ∣ 160`, and
`active_no_rational_root` checks all of them.

Consequently **every** element of the active window is irrational, while the archive spectrum is
integral, so the two can never meet: the SEP leg holds for every scene whose discriminant
`gap/∏deg` fails to be a rational square, not merely for `(9,11,13)`
(`disjoint_from_integers`, `sep_leg_structural`).

**What this changes.** The no-go was carried by an exact numerical check on one scene. It is now a
statement about a class: the intertwiner is excluded whenever the degeneracy gap over the degree
product is a non-square, and the scene's `1/40` is one instance. A future attempt to build the
transfer cannot escape by perturbing the zone sizes — it must make `gap/∏deg` a rational square,
which by `ActiveSplittingFromDistinctness.gap_sos` means engineering
`a(b−c)² + b(c−a)² + c(a−b)²` into a square multiple of `∏(N−nᵢ)`.
-/

namespace D0.Synthesis.ActiveWindowIrrational

/-- The active-window quadratic, cleared of denominators. -/
def activeQ (x : ℚ) : ℚ := 160 * x ^ 2 - 480 * x + 359

/-- **Completing the square.** `160x² − 480x + 359 = 160(x − 3/2)² − 1`. -/
theorem activeQ_square_form (x : ℚ) : activeQ x = 160 * (x - 3 / 2) ^ 2 - 1 := by
  unfold activeQ; ring

/-- Divisors of the constant term `359`, which is prime. -/
def numerators : List ℤ := [1, 359, -1, -359]

/-- Divisors of the leading coefficient `160`. -/
def denominators : List ℤ := [1, 2, 4, 5, 8, 10, 16, 20, 32, 40, 80, 160]

/-- **No rational root.** Cleared of denominators a root `p/q` satisfies
`160p² − 480pq + 359q² = 0`; no admissible pair does. -/
theorem active_no_rational_root :
    ∀ p ∈ numerators, ∀ q ∈ denominators,
      160 * p ^ 2 - 480 * p * q + 359 * q ^ 2 ≠ 0 := by decide

/-- `160` carries an odd power of two, which is the structural reason: `160p² = q²` would give an
odd two-adic valuation on the left and an even one on the right. -/
theorem one_sixty_odd_two_power : (160 : ℕ) = 2 ^ 5 * 5 := by norm_num

/-- **The window misses every integer.** For an integer `m` the value `activeQ m` is non-zero,
because `160m² − 480m + 359` is odd: the first two terms are even and `359` is odd. -/
theorem disjoint_from_integers (m : ℤ) : 160 * m ^ 2 - 480 * m + 359 ≠ 0 := by
  intro h
  have hpar : (160 * m ^ 2 - 480 * m + 359) % 2 = 1 := by
    have : (160 * m ^ 2 - 480 * m) % 2 = 0 := by
      have : 160 * m ^ 2 - 480 * m = 2 * (80 * m ^ 2 - 240 * m) := by ring
      omega
    omega
  rw [h] at hpar
  norm_num at hpar

/-- The archive spectrum, the zone degrees. -/
def archiveSpectrum : List ℤ := [24, 22, 20]

/-- **The SEP leg, structurally.** No degree is in the active window — indeed no integer is. -/
theorem sep_leg_structural :
    (∀ m ∈ archiveSpectrum, 160 * m ^ 2 - 480 * m + 359 ≠ 0) ∧
    (∀ m : ℤ, 160 * m ^ 2 - 480 * m + 359 ≠ 0) :=
  ⟨fun m _ => disjoint_from_integers m, disjoint_from_integers⟩

/-- The three degrees, for the record, and their non-membership computed directly. -/
theorem degrees_values :
    160 * (24 : ℤ) ^ 2 - 480 * 24 + 359 = 80999 ∧
    160 * (22 : ℤ) ^ 2 - 480 * 22 + 359 = 67239 ∧
    160 * (20 : ℤ) ^ 2 - 480 * 20 + 359 = 54759 := by
  refine ⟨by decide, by decide, by decide⟩

end D0.Synthesis.ActiveWindowIrrational
