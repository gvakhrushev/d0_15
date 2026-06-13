import D0.Combinatorics.EulerPhi
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic

/-!
# D0-WINDOW44-GROUP-SPECTRUM-001 — (Z/44)* spectrum and the 20 = 4×5 window budget

The terminal return window `q_T = 44` has unit group `(Z/44)* ≅ Z2 × Z2 × Z5`.
This leaf module pins the exact finite facts asserted by the Python certificate
`05_CERTS/vp_window44_group_spectrum.py`:

* `[1]` `|(Z/44)*| = φ_E(44) = 20 = d13`   (reuses `D0.totient_44`).
* `[2]` structure `Z2 × Z2 × Z5`: the 2-torsion `{u : u² = 1}` has order 4
  (so `Z2 × Z2`, not `Z4`), the odd part `{u²}` has order 5, and the group
  exponent (max element order) is 10.
* `[3]` characteristic-subgroup orders are `{1, 4, 5, 20}` and `20 = 4 × 5`
  (= |ABCD| × D_Σ, the orientation budget times the operational budget).
* `[4]` the window is phase-neutral: the product of all units mod 44 is `+1`
  (generalized Wilson).

Everything is finite/decidable over `ZMod 44`, so the proofs are by
`native_decide` on the real propositions (no contrived restatement).
-/

namespace D0.Claims

/-- The units of `ZMod 44`, as a concrete `Finset`. -/
def units44 : Finset (ZMod 44) :=
  Finset.univ.filter (fun u => IsUnit u)

/-- `[1]` `|(Z/44)*| = 20 = d13`. Reuses the frozen `D0.totient_44`. -/
theorem window44_unit_count : units44.card = 20 ∧ Nat.totient 44 = 20 := by
  refine ⟨by native_decide, D0.totient_44⟩

/-- `[2a]` The 2-torsion `{u : u² = 1}` of `(Z/44)*` has order 4 (⇒ `Z2 × Z2`). -/
theorem window44_two_torsion_card :
    (units44.filter (fun u => u ^ 2 = 1)).card = 4 := by
  native_decide

/-- `[2b]` The odd part — the set of squares of units — has order 5 (⇒ `Z5`). -/
theorem window44_odd_part_card :
    (units44.image (fun u => u ^ 2)).card = 5 := by
  native_decide

/-- `[2c]` The group exponent (max element order) is 10: every unit `u`
satisfies `u^10 = 1`, and some unit does not satisfy `u^k = 1` for `k = 2,5`. -/
theorem window44_exponent_10 :
    (∀ u ∈ units44, u ^ 10 = 1) ∧
    (∃ u ∈ units44, u ^ 2 ≠ 1) ∧
    (∃ u ∈ units44, u ^ 5 ≠ 1) := by
  refine ⟨by native_decide, by native_decide, by native_decide⟩

/-- `[3]` Characteristic-subgroup orders `{1, 4, 5, 20}` with `20 = 4 × 5`.
The orders are the cardinalities of `{1}`, the 2-torsion, the odd part, and
the whole unit group. -/
theorem window44_characteristic_orders :
    ({1,
      (units44.filter (fun u => u ^ 2 = 1)).card,
      (units44.image (fun u => u ^ 2)).card,
      units44.card} : Finset ℕ) = {1, 4, 5, 20} ∧
    (4 * 5 = 20) := by
  refine ⟨by native_decide, by norm_num⟩

/-- `[4]` Window phase-neutral: the product of all units mod 44 is `+1`. -/
theorem window44_phase_neutral : units44.prod id = 1 := by
  native_decide

/-- Bundled D0 claim: the full (Z/44)* spectrum and the 20 = 4×5 window budget. -/
theorem window44_group_spectrum :
    units44.card = 20 ∧
    (units44.filter (fun u => u ^ 2 = 1)).card = 4 ∧
    (units44.image (fun u => u ^ 2)).card = 5 ∧
    ({1,
      (units44.filter (fun u => u ^ 2 = 1)).card,
      (units44.image (fun u => u ^ 2)).card,
      units44.card} : Finset ℕ) = {1, 4, 5, 20} ∧
    units44.prod id = 1 := by
  refine ⟨window44_unit_count.1, window44_two_torsion_card,
    window44_odd_part_card, window44_characteristic_orders.1,
    window44_phase_neutral⟩

end D0.Claims
