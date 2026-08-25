import Mathlib.NumberTheory.Real.GoldenRatio
import Mathlib.Tactic

/-!
# The role-orientation ambiguity of the equation of state, derived

The ROLE leg of `D0-PHASON-WZ-TRANSFER-OWNER-001` establishes that fixing the carriers does not fix
the dark-energy equation of state: two admissible pressure/energy role-orientations give different
values. Its certificate carries this with **illustrative** witnesses —
`05_CERTS/vp_phason_wz_transfer_owner.py:58-61` sets `w_A = 9/10`, `w_B = 10/9` with the comment
*"the point is w_A != w_B at fixed carriers"* and asserts only `w_A * w_B = 1`.

The reciprocal structure is the real content: swapping the pressure and energy roles inverts the
ratio, so the role freedom is the involution

    w ↦ 1/w ,

whose fixed points are exactly `w = ±1` (`involution_fixed_points`). The witnesses `9/10, 10/9`
illustrate that; they are not scene quantities and their spread `19/90` is arbitrary.

But the corpus owns a value. `D0-PHASON-WDE-SIGN-NORMALIZATION-OWNER-001` fixes the dark-energy
sign Galois-forced negative with the retained reading `w = −φ`. Feeding *that* through the
involution gives the pair the theory actually predicts:

    w_A = −φ ,      w_B = 1/w_A = −1/φ = −(φ − 1) ,

with

* `eos_product` — `w_A · w_B = 1` (the reciprocity the certificate asserts);
* `eos_spread` — `w_B − w_A = 1`, **exactly one**, because `φ − 1/φ = 1` is the defining identity
  of the golden ratio;
* `eos_sum_sq` — `(w_A + w_B)² = 5`, i.e. the sum is `−√5`, so the two values are the roots of
  `w² + √5·w + 1 = 0`;
* `eos_not_fixed` — neither is a fixed point of the involution, so the ambiguity is live at the
  corpus's own value;
* `eos_brackets_minus_one` — `w_A < −1 < w_B`: the pair straddles the cosmological constant.

**What this adds.** The ROLE no-go was carried by two numbers chosen to differ. It is now carried by
the theory's own value: the ambiguity is not "some two values" but the golden pair `(−φ, −1/φ)`,
its size is exactly `1`, and it would vanish only at `w = ±1` — that is, only for a cosmological
constant (or its positive mirror). Any future attempt to make the transfer unique must either move
the owned sign reading off `−φ` or explain why one role-orientation is preferred; the numerical
witnesses gave no such handle, the golden pair does.
-/

namespace D0.Synthesis.RoleOrientationEOS

open Real
open scoped goldenRatio

/-- **The role involution has only `±1` as fixed points.** -/
theorem involution_fixed_points (w : ℝ) (hw : w ≠ 0) : w = 1 / w ↔ (w = 1 ∨ w = -1) := by
  constructor
  · intro h
    have hsq : w ^ 2 = 1 := by
      field_simp at h
      nlinarith [h]
    rcases mul_self_eq_one_iff.mp (by nlinarith [hsq] : w * w = 1) with h1 | h1
    · exact Or.inl h1
    · exact Or.inr h1
  · rintro (rfl | rfl) <;> norm_num

/-- The owned dark-energy reading: `w_A = −φ`. -/
noncomputable def wA : ℝ := -φ

/-- Its role-swapped partner: `w_B = 1/w_A`. -/
noncomputable def wB : ℝ := -φ⁻¹

theorem phi_pos : 0 < φ := goldenRatio_pos

theorem phi_ne_zero : φ ≠ 0 := ne_of_gt phi_pos

/-- **Reciprocity**, the property the certificate asserts of its illustrative pair. -/
theorem eos_product : wA * wB = 1 := by
  unfold wA wB
  field_simp

/-- **The spread is exactly one**, because `φ − φ⁻¹ = 1` defines the golden ratio. -/
theorem eos_spread : wB - wA = 1 := by
  unfold wA wB
  have h : φ - φ⁻¹ = 1 := by
    rw [inv_goldenRatio]; ring
  linarith [h]

/-- **The sum squares to five**, so the pair are the roots of `w² + √5 w + 1 = 0`. -/
theorem eos_sum_sq : (wA + wB) ^ 2 = 5 := by
  have hp : wA * wB = 1 := eos_product
  have hs : wB - wA = 1 := eos_spread
  nlinarith [hp, hs]

/-- **The ambiguity is live**: neither value is fixed by the involution. -/
theorem eos_not_fixed : wA ≠ wB := by
  intro h
  have := eos_spread
  rw [h] at this
  linarith [this]

/-- **The pair straddles the cosmological constant** `w = −1`. -/
theorem eos_brackets_minus_one : wA < -1 ∧ -1 < wB := by
  have h1 : (1 : ℝ) < φ := one_lt_goldenRatio
  constructor
  · unfold wA; linarith
  · unfold wB
    have : φ⁻¹ < 1 := by
      rw [inv_lt_one_iff₀]
      exact Or.inr h1
    linarith

/-- **Assembled.** The role freedom is `w ↦ 1/w`; at the owned reading `w = −φ` it produces the
golden pair, reciprocal, of spread exactly one, summing to `−√5`, straddling `−1`. -/
theorem role_orientation_pair :
    wA * wB = 1 ∧ wB - wA = 1 ∧ (wA + wB) ^ 2 = 5 ∧ wA ≠ wB ∧ (wA < -1 ∧ -1 < wB) :=
  ⟨eos_product, eos_spread, eos_sum_sq, eos_not_fixed, eos_brackets_minus_one⟩

end D0.Synthesis.RoleOrientationEOS
