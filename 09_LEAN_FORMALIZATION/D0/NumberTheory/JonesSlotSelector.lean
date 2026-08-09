import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.NumberTheory.Real.Irrational

/-!
# D0-JONES-SLOT-SELECTOR-001 — an internal selector for the `n = 5` Jones slot

## The defect this repairs

BOOK_01 §01.21.3 lists the Jones subfactor index as one of four *independent* channels forcing `φ`.
The external half is genuinely independent: Jones (*Invent. Math.* **72** (1983) 1–25) proves that
the index `[M:N]` of a type-II₁ subfactor lies, below `4`, in the discrete series
`{4cos²(π/n) : n = 3, 4, 5, …}` — a quantization owing nothing to D0.

The internal half was not independent. The section selects the slot as "the **first irrational**
member" and then identifies the quantum dimension via the fusion relation `x² = x + 1` — the
detector route's own equation. So the channel imported what it was supposed to corroborate.

## The repair

Select the slot by two conditions, neither of which mentions `x² − x − 1`:

1. **Finite depth ⇒ index `< 4`** — the discrete series, i.e. some `n ≥ 3`. (Internal: D0 carriers
   are finite.)
2. **M1 rational-capture ⇒ the index is irrational.** This is the corpus's already-owned clause,
   used verbatim for rotation numbers at §01.21.1: *a rational value is captured at some finite
   stage, becoming indistinguishable from a periodic catalogue entry, hence `⊥M1`.* Applying the
   same owned clause to the index is a reuse, not a new assumption.

Then the slot is fixed by arithmetic: `4cos²(π/n) = 2 + 2cos(2π/n)` is rational exactly at
`n ∈ {3, 4, 6}` (values `1, 2, 3`) — by Niven's theorem the only rational values of `cos(rπ)` for
rational `r` are `0, ±1/2, ±1` — so the **least** `n ≥ 3` with an irrational slot is `n = 5`, whose
value is `(3+√5)/2 = φ²`.

**The point: `φ` is the OUTPUT.** The route reaches `φ² = (3+√5)/2` from an external quantization
plus an owned M1 clause plus arithmetic; the golden quadratic is then a *consequence* of the value,
not an input to the argument. That makes this a second route genuinely independent of
`p + p² = 1`, as the antifragility claim requires.

Honest scope: Jones's quantization theorem and Niven's rationality classification are cited external
owners (`ASSUMP-JONES-INDEX`, `ASSUMP-NIVEN`), not re-proved. What is machine-checked here is the
slot arithmetic — the rational values at `n = 3, 4, 6`, the value at `n = 5`, and that `n = 5` is
separated from all three rational neighbours.
-/

namespace D0.NumberTheory

open Real

/-- The Jones index slot `4cos²(π/n)` of the discrete series below `4`. -/
noncomputable def jonesSlot (n : ℕ) : ℝ := 4 * Real.cos (Real.pi / (n : ℝ)) ^ 2

/-- `n = 3` is a rational slot: `4cos²(π/3) = 1`. -/
theorem jonesSlot_three : jonesSlot 3 = 1 := by
  unfold jonesSlot
  norm_num [Real.cos_pi_div_three]

/-- `n = 4` is a rational slot: `4cos²(π/4) = 2`. -/
theorem jonesSlot_four : jonesSlot 4 = 2 := by
  unfold jonesSlot
  rw [show ((4 : ℕ) : ℝ) = 4 by norm_num, Real.cos_pi_div_four]
  rw [div_pow, Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 2)]
  norm_num

/-- `n = 6` is a rational slot: `4cos²(π/6) = 3`. -/
theorem jonesSlot_six : jonesSlot 6 = 3 := by
  unfold jonesSlot
  rw [show ((6 : ℕ) : ℝ) = 6 by norm_num, Real.cos_pi_div_six]
  rw [div_pow, Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 3)]
  norm_num

/-- **The `n = 5` slot is `φ²`.** `4cos²(π/5) = (3+√5)/2 = ((1+√5)/2)²`, computed from mathlib's
`cos(π/5) = (1+√5)/4`. The golden ratio appears here as a VALUE, not as an assumed equation. -/
theorem jonesSlot_five : jonesSlot 5 = (3 + Real.sqrt 5) / 2 := by
  unfold jonesSlot
  rw [show ((5 : ℕ) : ℝ) = 5 by norm_num, Real.cos_pi_div_five]
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  field_simp
  nlinarith [h5]

/-- The `n = 5` slot is exactly the square of `(1+√5)/2`. -/
theorem jonesSlot_five_eq_phi_sq : jonesSlot 5 = ((1 + Real.sqrt 5) / 2) ^ 2 := by
  rw [jonesSlot_five]
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  field_simp
  nlinarith [h5]

/-- Bounds on `√5`, used to separate the `n = 5` slot from every rational neighbour. -/
theorem sqrt_five_bounds : 2 < Real.sqrt 5 ∧ Real.sqrt 5 < 3 := by
  constructor
  · have : (2 : ℝ) = Real.sqrt 4 := by
      rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
    rw [this]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  · have : (3 : ℝ) = Real.sqrt 9 := by
      rw [show (9 : ℝ) = 3 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
    rw [this]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)

/-- **Separation.** The `n = 5` slot differs from all three rational slots, so the M1
irrationality condition genuinely discriminates it and does not merely re-describe one of them. -/
theorem jonesSlot_five_ne_rational_slots :
    jonesSlot 5 ≠ jonesSlot 3 ∧ jonesSlot 5 ≠ jonesSlot 4 ∧ jonesSlot 5 ≠ jonesSlot 6 := by
  obtain ⟨hlo, hhi⟩ := sqrt_five_bounds
  rw [jonesSlot_five, jonesSlot_three, jonesSlot_four, jonesSlot_six]
  refine ⟨?_, ?_, ?_⟩ <;> intro h <;> nlinarith [hlo, hhi]

/-- The `n = 5` slot is irrational — the M1 rational-capture clause therefore admits it while
rejecting `n = 3, 4, 6`. -/
theorem jonesSlot_five_irrational : Irrational (jonesSlot 5) := by
  have h5 : Irrational (Real.sqrt 5) := by
    simpa using (by norm_num : Nat.Prime 5).irrational_sqrt
  rw [jonesSlot_five]
  rintro ⟨q, hq⟩
  exact h5 ⟨2 * q - 3, by push_cast; linarith [hq]⟩

/-- **D0-JONES-SLOT-SELECTOR-001.** Below `4` the Jones series is `{4cos²(π/n)}`; the slots at
`n = 3, 4, 6` are the rationals `1, 2, 3`; the slot at `n = 5` is `(3+√5)/2 = φ²`, is irrational,
and is separated from every rational slot. So "finite depth + M1 rational-capture" selects `n = 5`
without any appeal to `x² − x − 1`, and `φ` emerges as the value rather than as an assumption. -/
theorem jones_slot_selector :
    jonesSlot 3 = 1 ∧ jonesSlot 4 = 2 ∧ jonesSlot 6 = 3 ∧
    jonesSlot 5 = ((1 + Real.sqrt 5) / 2) ^ 2 ∧
    Irrational (jonesSlot 5) ∧
    (jonesSlot 5 ≠ jonesSlot 3 ∧ jonesSlot 5 ≠ jonesSlot 4 ∧ jonesSlot 5 ≠ jonesSlot 6) :=
  ⟨jonesSlot_three, jonesSlot_four, jonesSlot_six, jonesSlot_five_eq_phi_sq,
   jonesSlot_five_irrational, jonesSlot_five_ne_rational_slots⟩

end D0.NumberTheory
