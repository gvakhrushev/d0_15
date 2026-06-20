import Mathlib.Data.Matrix.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic

/-!
# D0-HIGGS-RETURN-QUOTIENT-ACTION-OWNER-001 — the period-44 return is a MODULUS, not a toral period

The toral return operator `T = [[0,1],[1,-1]]` (charpoly `x²+x−1`) has INFINITE order in `GL(2,ℤ)`
(its trace is the signed Lucas sequence, which grows without bound), so `T⁴⁴ ≠ I`. On the residue
quotient `ZMod 44` its order is **30**, not 44: `T³⁰ = I` and `T⁴⁴ ≠ I (mod 44)`. Hence there is **no
canonical period-44 toral return action** — `q_T = 44` is the return *modulus* of the declared finite
quotient, never the statement `T⁴⁴ = I`. (This module proves exactly that, honoring the task's
restriction.) The additive residue carrier `ZMod 44` does have period 44, but its cyclic shift moves no
projector nontrivially; the projector-moving (toral) action has period 30.
-/

namespace D0.Matter.HiggsReturnQuotientAction

/-- The toral return operator over the residue quotient `ZMod 44`. -/
def T : Matrix (Fin 2) (Fin 2) (ZMod 44) := !![0, 1; 1, -1]

/-- **`T³⁰ = I` on `ZMod 44`**: the toral return has order dividing 30 on the residue quotient. -/
theorem return_action_period_30 : T ^ 30 = 1 := by native_decide

/-- **`T⁴⁴ ≠ I` on `ZMod 44`**: the return modulus 44 is NOT a toral period (`T⁴⁴ = T¹⁴ ≠ I`). -/
theorem return_modulus_44_not_toral_period : T ^ 44 ≠ 1 := by native_decide

/-- The order is exactly 30 (no proper divisor returns to `I`): `T¹⁵ ≠ I` and `T¹⁰ ≠ I` and `T⁶ ≠ I`. -/
theorem return_action_order_exactly_30 :
    T ^ 30 = 1 ∧ T ^ 15 ≠ 1 ∧ T ^ 10 ≠ 1 ∧ T ^ 6 ≠ 1 := by
  refine ⟨return_action_period_30, ?_, ?_, ?_⟩ <;> native_decide

/-- **The full-torus return is not assumed**: `T⁴⁴ ≠ I` already on `ZMod 44`, hence also in `GL(2,ℤ)`
(an integer `T⁴⁴ = I` would reduce to `I` mod 44). `q_T = 44` is a return modulus, never `T⁴⁴ = I`. -/
theorem return_action_not_assumed_on_full_torus : T ^ 44 ≠ 1 :=
  return_modulus_44_not_toral_period

/-- **D0-HIGGS-RETURN-QUOTIENT-ACTION-OWNER-001.** The return action on the finite residue quotient has
toral order 30 (not 44); the modulus 44 is not a toral period (`T⁴⁴ ≠ I`, mod 44 and in `GL(2,ℤ)`). No
canonical period-44 toral return action exists. -/
theorem higgs_return_quotient_action_owner :
    T ^ 30 = 1 ∧ T ^ 44 ≠ 1 ∧ T ^ 15 ≠ 1 := by
  exact ⟨return_action_period_30, return_modulus_44_not_toral_period,
    return_action_order_exactly_30.2.1⟩

end D0.Matter.HiggsReturnQuotientAction
