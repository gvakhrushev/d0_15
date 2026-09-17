import Mathlib.Tactic

/-!
# No transport mode of the scene is golden

The corpus names `φ`-recursion as the engine of the whole construction ("Engine: `φ`-recursion",
BOOK_01 §01.6.1c) and the spatial `3` of the `(3,1)` signature as the three transport modes of the
scene — the non-zero eigenvalues of the adjacency of `K(9,11,13)`. Those eigenvalues have never
been placed arithmetically.

They are the roots of

    λ³ − 359λ − 2574

(the characteristic polynomial of the quotient matrix `Q = ![![0,11,13],![9,0,13],![9,11,0]]`;
`359` is the sum of principal `2×2` minors and `2574` the determinant, both computed in
`D0.Spectral.JointCommutant`). Numerically `λ ≈ 21.837, −9.758, −12.079`.

**Theorem.** None of them lies in `ℚ(√5) = ℚ(φ)`.

Writing a candidate root as `a + b√5` with `a, b ∈ ℚ` and expanding,

    (a + b√5)³ − 359(a + b√5) − 2574
        = (a³ + 15ab² − 359a − 2574) + (3a²b + 5b³ − 359b)·√5 ,

so both components must vanish. The `√5` component factors as `b(3a² + 5b² − 359)`:

* if `b = 0` the rational component is `a³ − 359a − 2574 = 0`, which has no rational solution;
* if `b ≠ 0` then `5b² = 359 − 3a²`, and substituting into the rational component gives
  `−8a³ + 718a − 2574 = 0`, i.e. `4a³ − 359a + 1287 = 0`, which also has no rational solution.

`golden_component_reduction` proves the substitution step; the two root-freeness facts are decided
over the candidate lists the rational root theorem supplies (denominators dividing the leading
coefficient, numerators dividing the constant term).

**What this does NOT mean — retraction of an earlier reading.** It is tempting to conclude that
`φ`-recursion "cannot reach" the transport spectrum. That inference is wrong and is withdrawn.
A construction driven by `φ` can perfectly well output numbers outside `ℚ(φ)`: the chain here is
`dyad → Ω₈ → 9, 11, 13 → adjacency → spectrum`, and the characteristic polynomial of a `3 × 3`
integer matrix lands in a cubic field as a matter of course. Deriving a quantity and that quantity
lying in a given field are different things, and only the second is settled here.

**What it is.** A plain arithmetic fact about the scene's spectrum, with no target in the corpus:
no row claims the transport eigenvalues are golden. It rules out one shape of numerological fit
(`λ = φ^k · c` with `c` rational) and nothing more. Recorded because the computation is exact and
the eigenvalues had not been placed arithmetically anywhere, not because it constrains the engine.
-/

namespace D0.Spectral.TransportNotGolden

/-- The transport cubic: the characteristic polynomial of the quotient matrix. -/
def transport (x : ℚ) : ℚ := x ^ 3 - 359 * x - 2574

/-- The reduced cubic governing the `b ≠ 0` branch. -/
def reduced (x : ℚ) : ℚ := 4 * x ^ 3 - 359 * x + 1287

/-- Integer divisors of `2574` — the only possible rational roots of the monic `transport`. -/
def transportDivisors : List ℤ :=
  [1, 2, 3, 6, 9, 11, 13, 18, 22, 26, 33, 39, 66, 78, 99, 117, 143, 198, 234, 286, 429, 858,
   1287, 2574, -1, -2, -3, -6, -9, -11, -13, -18, -22, -26, -33, -39, -66, -78, -99, -117,
   -143, -198, -234, -286, -429, -858, -1287, -2574]

/-- Divisors of `1287`, the constant term of `reduced`. -/
def redNumerators : List ℤ :=
  [1, 3, 9, 11, 13, 33, 39, 99, 117, 143, 429, 1287,
   -1, -3, -9, -11, -13, -33, -39, -99, -117, -143, -429, -1287]

/-- Divisors of `4`, the leading coefficient of `reduced`. -/
def redDenominators : List ℤ := [1, 2, 4]

/-- **`transport` has no rational root.** Monic, so a rational root is an integer dividing `2574`;
none is. -/
theorem transport_no_rational_root :
    ∀ n ∈ transportDivisors, n ^ 3 - 359 * n - 2574 ≠ 0 := by decide

/-- **`reduced` has no rational root.** Clearing denominators in `4(p/q)³ − 359(p/q) + 1287 = 0`
gives `4p³ − 359pq² + 1287q³ = 0`; no admissible pair satisfies it. -/
theorem reduced_no_rational_root :
    ∀ p ∈ redNumerators, ∀ q ∈ redDenominators,
      4 * p ^ 3 - 359 * p * q ^ 2 + 1287 * q ^ 3 ≠ 0 := by decide

/-- **The substitution step.** If the `√5` component vanishes with `b ≠ 0`, then `5b² = 359 − 3a²`,
and the rational component becomes the reduced cubic (up to the factor `−2`). -/
theorem golden_component_reduction (a b : ℚ) (hb : b ≠ 0)
    (h2 : 3 * a ^ 2 * b + 5 * b ^ 3 - 359 * b = 0) :
    5 * b ^ 2 = 359 - 3 * a ^ 2 ∧
    (a ^ 3 + 15 * a * b ^ 2 - 359 * a - 2574 = 0 → reduced a = 0) := by
  have hfac : b * (3 * a ^ 2 + 5 * b ^ 2 - 359) = 0 := by ring_nf; linarith [h2]
  have hz : 3 * a ^ 2 + 5 * b ^ 2 - 359 = 0 := by
    rcases mul_eq_zero.mp hfac with h | h
    · exact absurd h hb
    · exact h
  have hb2 : 5 * b ^ 2 = 359 - 3 * a ^ 2 := by linarith
  refine ⟨hb2, ?_⟩
  intro h1
  have : a ^ 3 + 3 * a * (5 * b ^ 2) - 359 * a - 2574 = 0 := by linarith [h1]
  rw [hb2] at this
  unfold reduced
  linarith [this]

/-- **No root of the transport cubic lies in `ℚ(√5)`.** Both components of
`(a + b√5)³ − 359(a + b√5) − 2574` cannot vanish together: the `b = 0` branch needs a rational root
of `transport`, the `b ≠ 0` branch a rational root of `reduced`, and neither exists. -/
theorem no_golden_transport_mode (a b : ℚ)
    (h1 : a ^ 3 + 15 * a * b ^ 2 - 359 * a - 2574 = 0)
    (h2 : 3 * a ^ 2 * b + 5 * b ^ 3 - 359 * b = 0) :
    (b = 0 → transport a = 0) ∧ (b ≠ 0 → reduced a = 0) := by
  refine ⟨?_, ?_⟩
  · intro hb; subst hb; unfold transport; linarith [h1]
  · intro hb; exact (golden_component_reduction a b hb h2).2 h1

/-- **The three modes are real and separated**, bracketed by integer sign changes:
one root in `(21, 22)`, one in `(-10, -9)`, one in `(-13, -12)`. -/
theorem transport_roots_bracketed :
    transport 21 < 0 ∧ 0 < transport 22 ∧
    0 < transport (-10) ∧ transport (-9) < 0 ∧
    transport (-13) < 0 ∧ 0 < transport (-12) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;> · unfold transport; norm_num

end D0.Spectral.TransportNotGolden
