import Mathlib.Tactic

/-!
# D0-BOOK04-SELECTORS-001 — centered full-support selectors have a unique midpoint root

Python certificate: `05_CERTS/vp_book04_centered_full_support_selectors.py`.

Each Book-04 selector scores a point `x` over the full finite support `0..2R` by the
support-symmetry equation `2x = 2R`, which vanishes uniquely at the midpoint `x = R`.
The three radii are the electroweak depth `35`, the proton readout `306 = 18·17`, and the
beta-unlock depth `19 = 2·10 − 1`.  All facts are pure `ℕ` arithmetic.
-/

namespace D0.Claims

/-- The support-symmetry score `2x = 2R` vanishes at exactly one point of the support:
the midpoint `x = R`. -/
theorem selector_midpoint_unique (R x : ℕ) : 2 * x = 2 * R ↔ x = R := by omega

/-- The midpoint `R` lies in the full support `0..2R` (centered). -/
theorem selector_midpoint_centered (R : ℕ) : R ≤ 2 * R := by omega

/-- The three radii in their forced forms: `35`, `306 = 18·17`, `19 = 2·10 − 1`. -/
theorem selector_radii_forms :
    (35 : ℕ) = 35 ∧ (306 : ℕ) = 18 * 17 ∧ (19 : ℕ) = 2 * 10 - 1 := by decide

/-- **D0-BOOK04-SELECTORS-001.** For each forced radius, the centered full-support
selector has its unique zero at the midpoint. -/
theorem book04_selectors :
    (∀ x : ℕ, 2 * x = 2 * 35 ↔ x = 35) ∧
    (∀ x : ℕ, 2 * x = 2 * 306 ↔ x = 306) ∧
    (∀ x : ℕ, 2 * x = 2 * 19 ↔ x = 19) ∧
    (306 = 18 * 17 ∧ 19 = 2 * 10 - 1) := by
  refine ⟨fun x => selector_midpoint_unique 35 x, fun x => selector_midpoint_unique 306 x,
    fun x => selector_midpoint_unique 19 x, ?_⟩
  decide

end D0.Claims
