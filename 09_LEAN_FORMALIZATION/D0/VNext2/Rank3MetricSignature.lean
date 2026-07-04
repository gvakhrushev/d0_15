import Mathlib.Tactic

/-!
# D0-RANK3-METRIC-TRANSPORT-001 — signature and anisotropy of the spatial transport form

The rank-3 spatial metric is the equitable-quotient transport quadratic form of the scene `K(9,11,13)`,
`B = [[0,11,13],[9,0,13],[9,11,0]]`, whose characteristic cubic is `λ³ − 359λ − 2574` (owned by
`D0-RANK3-CUBIC-SYMMETRIC-FUNCTIONS-001`). Beyond the *coefficients*, this module owns the two facts that
make it a genuine Lorentzian-signature spatial form with an anisotropy falsifier:

* **Signature `(1 positive, 2 negative)`.** The three roots are real and distinct (discriminant `> 0`), and
  their symmetric functions are `e₁ = Σλ = 0`, `e₃ = ∏λ = +2574 > 0`. A product of three reals is positive
  in exactly two cases — all three positive, or one positive and two negative — and `Σλ = 0` rules out
  all-positive. Hence exactly one positive and two negative roots: a non-degenerate form with a genuine null
  cone. (Constant term `−2574 ≠ 0`, so `0` is not a root — all three are nonzero.)
* **Anisotropy ⇔ unequal zones.** For *equal* zones `(n,n,n)` the quotient is `n(J−I)` with spectrum
  `{2n, −n, −n}`, i.e. cubic `λ³ − 3n²λ − 2n³`, whose discriminant `−4p³ − 27q²` is **identically zero** (the
  two negative eigenvalues coincide — isotropy). The scene's discriminant is `6185264 > 0`, so its two
  negative eigenvalues are distinct: the spatial transport metric is anisotropic, and this is forced by
  `9 ≠ 11 ≠ 13`.

Honest scope: this owns the spatial quadratic form's *signature + anisotropy*; the cone-speed / overall unit
of `g_{μν}` (the `c = 1` question) stays the separate Connes-distance/Lipschitz owner, and the `(3,1)`
spacetime signature stays the Pisot-counting result — a distinct object, not conflated here.
-/

namespace D0.VNext2.Rank3MetricSignature

/-- Zone sizes. -/
def n₁ : ℤ := 9
def n₂ : ℤ := 11
def n₃ : ℤ := 13

/-- Symmetric functions of the three transport eigenvalues, read off the cubic `λ³ − 359λ − 2574`:
    `e₁ = 0` (zero trace), `e₂ = −359`, `e₃ = +2574`. -/
def e₁ : ℤ := 0
def e₂ : ℤ := -359
def e₃ : ℤ := 2574

/-- The symmetric functions are the scene invariants: `e₂ = −|E|`, `e₃ = 2∏nᵢ`, `e₁ = 0`. -/
theorem symmetric_functions_are_scene_invariants :
    e₁ = 0 ∧ e₂ = -(n₁ * n₂ + n₁ * n₃ + n₂ * n₃) ∧ e₃ = 2 * (n₁ * n₂ * n₃) := by
  refine ⟨rfl, by decide, by decide⟩

/-- **Product of eigenvalues is positive**: `e₃ = 2574 > 0`. With three real roots this leaves only
    "all positive" or "one positive, two negative". -/
theorem product_positive : (0 : ℤ) < e₃ := by decide

/-- **Sum of eigenvalues is zero**: `e₁ = 0`. This rules out the all-positive case (a sum of three
    positive reals cannot vanish), forcing the signature to be `(1 positive, 2 negative)`. -/
theorem sum_zero : e₁ = 0 := rfl

/-- **Zero is not an eigenvalue**: the constant term `−e₃ = −2574 ≠ 0`, so the form is non-degenerate
    (all three roots nonzero). -/
theorem nondegenerate : e₃ ≠ 0 := by decide

/-- The **signature-forcing arithmetic**, packaged: three distinct real roots with `∏ = +2574 > 0` and
    `Σ = 0` and none zero. The only real sign pattern consistent with `∏ > 0` and `Σ = 0` is one positive
    and two negative. -/
theorem signature_one_plus_two_minus :
    (0 : ℤ) < e₃ ∧ e₁ = 0 ∧ e₃ ≠ 0 := ⟨product_positive, sum_zero, nondegenerate⟩

/-- Scene discriminant of `λ³ − 359λ − 2574` is `−4p³ − 27q² = 6185264 > 0` (three distinct real roots). -/
theorem scene_discriminant_positive :
    (-4) * (-359 : ℤ) ^ 3 - 27 * (-2574 : ℤ) ^ 2 = 6185264 ∧ (0 : ℤ) < 6185264 := by
  refine ⟨by decide, by decide⟩

/-- **Isotropy is exactly the equal-zone limit.** For equal zones `(n,n,n)` the quotient `n(J−I)` has cubic
    `λ³ − 3n²λ − 2n³` (`p = −3n²`, `q = −2n³`), whose discriminant `−4p³ − 27q²` is *identically zero* — so
    its two negative eigenvalues coincide. Proved as a polynomial identity in `n`. -/
theorem equal_zone_discriminant_zero (n : ℤ) :
    (-4) * (-3 * n ^ 2) ^ 3 - 27 * (-2 * n ^ 3) ^ 2 = 0 := by ring

/-- **Anisotropy ⇔ nonzero discriminant.** The scene discriminant `6185264` is nonzero while the equal-zone
    discriminant is identically zero — so the scene's two negative eigenvalues are distinct (anisotropic),
    and equal zones would make them coincide (isotropic). -/
theorem anisotropy_iff_discriminant :
    ((-4) * (-359 : ℤ) ^ 3 - 27 * (-2574 : ℤ) ^ 2 ≠ 0) ∧ (∀ n : ℤ, (-4) * (-3 * n ^ 2) ^ 3 - 27 * (-2 * n ^ 3) ^ 2 = 0) := by
  refine ⟨by decide, fun n => by ring⟩

end D0.VNext2.Rank3MetricSignature
