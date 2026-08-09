import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Sqrt

/-!
# D0-PHI-HURWITZ-CLASS-CANONIZATION-001 — the arithmetic route to φ, with the equation as OUTPUT

## The defect this repairs

`D0-PHI-HURWITZ-001` is presented in BOOK_01 §01.6.1a / §01.21.1 as a forcing route to `φ`
*independent* of the detector route `p + p² = 1`. As formalised it was not: the owner
`D0.NumberTheory.HurwitzMinimaxPhi` quantifies over `D0PhaseGeneratorAdmissible α := ∃ x,
D0ResponseRoot x ∧ α = x²` with `D0ResponseRoot x := 0 < x ∧ x + x² = 1` — i.e. it maximises
*inside the detector route's own equation family*, so the "second route" imported the first route's
conclusion as a hypothesis.

Two further facts sharpen the problem, both checked:

* for a quadratic irrational of discriminant `D`, `liminf q²|α − p/q| = 1/√D`, so "maximally
  badly approximable" carries no information beyond the minimal polynomial's discriminant;
* Hurwitz's theorem selects a **class**, not a number: `φ`, `1/φ`, `2+φ`, `(φ+1)/(φ+2)`,
  `(3φ+2)/(5φ+3)` all attain the extremal constant `1/√5` — the whole `GL(2,ℤ)` orbit
  (the *noble* numbers).

## The repair

Split the route into two steps, neither of which may mention `x² − x − 1`:

1. **Hurwitz (external, over ALL reals).** The extremal set of `liminf q²|α − p/q|` is the noble
   class. No D0 input; owner `ASSUMP-HURWITZ` (Hurwitz, *Math. Ann.* **39** (1891) 279).
2. **M1⁺ canonization (internal).** Choosing a representative of a class is exactly the situation
   `M1⁺` governs: *fix the canonical representative, or pay for the choice index*. The canonical
   representative of a purely periodic continued fraction is the one of minimal description —
   minimal period, then minimal partial quotient.

This module owns step 2 as finite arithmetic. A period-one purely periodic continued fraction
`[n; n, n, …]` is the positive root of `x = n + 1/x`, i.e. of

  `x² − n·x − 1 = 0`,  discriminant  `n² + 4`.

`n ↦ n² + 4` is strictly increasing, so the minimal partial quotient `n = 1` is the unique
minimiser, and it returns discriminant `5` — the Hurwitz-extremal discriminant — with root
`(1 + √5)/2`.

**The point: at `n = 1` the equation `x² − x − 1 = 0` is the CONCLUSION.** It is produced by
minimal-description selection over the period-one family, not assumed. So the arithmetic route now
reaches `φ` without the detector route's equation anywhere in its hypotheses, and the two routes are
independent in the sense the antifragility claim needs: killing `p + p² = 1` does not kill this one.

Honest scope: step 1 (Hurwitz extremality, and that its extremal set is the noble class) is the
cited external theorem, not re-proved here. What is machine-checked here is step 2 — that within the
period-one family, minimal description uniquely selects `n = 1`, and that this yields the golden
quadratic and `(1+√5)/2`.
-/

namespace D0.NumberTheory

open Real

/-- The value of the purely periodic continued fraction `[n; n, n, …]`: the positive root of
`x = n + 1/x`. -/
noncomputable def periodOneValue (n : ℕ) : ℝ := ((n : ℝ) + Real.sqrt ((n : ℝ) ^ 2 + 4)) / 2

/-- The discriminant of the period-one family member `n`. -/
def periodOneDisc (n : ℕ) : ℕ := n ^ 2 + 4

/-- `[n;n,n,…]` is a root of `x² − n·x − 1` — the family equation, parametrised by the partial
quotient. Nothing golden is assumed: `n` is free. -/
theorem periodOneValue_isRoot (n : ℕ) :
    (periodOneValue n) ^ 2 - (n : ℝ) * (periodOneValue n) - 1 = 0 := by
  have h : (0 : ℝ) ≤ (n : ℝ) ^ 2 + 4 := by positivity
  have hs : Real.sqrt ((n : ℝ) ^ 2 + 4) ^ 2 = (n : ℝ) ^ 2 + 4 := Real.sq_sqrt h
  unfold periodOneValue
  field_simp
  nlinarith [hs]

/-- The period-one value is positive for every partial quotient. -/
theorem periodOneValue_pos (n : ℕ) (hn : 1 ≤ n) : 0 < periodOneValue n := by
  have h : (0 : ℝ) ≤ (n : ℝ) ^ 2 + 4 := by positivity
  have h1 : (1 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
  have := Real.sqrt_nonneg ((n : ℝ) ^ 2 + 4)
  unfold periodOneValue
  linarith

/-- **Minimal description selects `n = 1`.** The discriminant is strictly increasing in the partial
quotient, so among all period-one continued fractions the minimal partial quotient is the unique
minimiser of the discriminant. -/
theorem periodOneDisc_strict_mono {m n : ℕ} (h : m < n) : periodOneDisc m < periodOneDisc n := by
  unfold periodOneDisc
  have : m ^ 2 < n ^ 2 := Nat.pow_lt_pow_left h (by norm_num)
  omega

/-- The minimal admissible partial quotient is `1`, and it returns discriminant `5`. -/
theorem periodOneDisc_one : periodOneDisc 1 = 5 := by decide

/-- **Uniqueness of the canonical representative.** For any other admissible partial quotient the
discriminant is strictly larger, so `n = 1` is the unique minimal-description member. -/
theorem periodOneDisc_min {n : ℕ} (hn : 1 ≤ n) (hne : n ≠ 1) : periodOneDisc 1 < periodOneDisc n :=
  periodOneDisc_strict_mono (by omega)

/-- **The golden quadratic is the OUTPUT.** At the canonically selected `n = 1`, the family equation
`x² − n·x − 1 = 0` becomes `x² − x − 1 = 0`. It was never a hypothesis of this module. -/
theorem canonical_equation_is_golden :
    (periodOneValue 1) ^ 2 - (periodOneValue 1) - 1 = 0 := by
  have h := periodOneValue_isRoot 1
  simpa using h

/-- And the canonical representative is `φ = (1 + √5)/2`. -/
theorem periodOneValue_one_eq_phi : periodOneValue 1 = (1 + Real.sqrt 5) / 2 := by
  unfold periodOneValue
  norm_num

/-- **Negative control (the selector is load-bearing).** Drop minimality and the family immediately
offers a different member: `n = 2` gives discriminant `8 ≠ 5` and the value `1 + √2 ≠ φ`, which is
*not* Hurwitz-extremal. So the canonization step is doing real work — without it the arithmetic
route does not reach `φ` at all. -/
theorem period_two_is_a_genuine_rival :
    periodOneDisc 2 = 8 ∧ periodOneDisc 2 ≠ periodOneDisc 1 ∧
    periodOneValue 2 = 1 + Real.sqrt 2 := by
  refine ⟨by decide, by decide, ?_⟩
  unfold periodOneValue
  have : ((2 : ℕ) : ℝ) ^ 2 + 4 = 8 := by norm_num
  rw [this]
  have h8 : Real.sqrt 8 = 2 * Real.sqrt 2 := by
    rw [show (8 : ℝ) = 2 ^ 2 * 2 by norm_num, Real.sqrt_mul (by positivity),
      Real.sqrt_sq (by norm_num)]
  rw [h8]
  push_cast
  ring

/-- **D0-PHI-HURWITZ-CLASS-CANONIZATION-001.** Within the period-one continued-fraction family,
minimal description uniquely selects the partial quotient `1`; that member has the Hurwitz-extremal
discriminant `5`, equals `(1+√5)/2`, and *satisfies* `x² − x − 1 = 0` as a derived consequence. The
rival at `n = 2` is exhibited, so the selection step can fail and is not vacuous. -/
theorem hurwitz_class_canonization :
    periodOneDisc 1 = 5 ∧
    (∀ n : ℕ, 1 ≤ n → n ≠ 1 → periodOneDisc 1 < periodOneDisc n) ∧
    periodOneValue 1 = (1 + Real.sqrt 5) / 2 ∧
    ((periodOneValue 1) ^ 2 - (periodOneValue 1) - 1 = 0) ∧
    periodOneDisc 2 = 8 :=
  ⟨periodOneDisc_one, fun _ hn hne => periodOneDisc_min hn hne,
   periodOneValue_one_eq_phi, canonical_equation_is_golden, by decide⟩

end D0.NumberTheory
