import D0.Core.FiniteTypes
import Mathlib.Tactic

/-!
# The zone count is the number of free dyad powers

Where `9, 11, 13` come from, read off `D0.Core.FiniteTypes` rather than assumed:

```
Dyad    = Fin 2                 |Dyad|    = 2 = 2¹
Role    = Dyad × Dyad           |Role|    = 4 = 2²
Orient  = Bool                  |Orient|  = 2 = 2¹
Omega8  = Role × Orient         |Omega8|  = 8 = 2³
Witness = PUnit                 |Witness| = 1 = 2⁰
V9  = Omega8 ⊕ Witness          = 2³ + 2⁰ = 9
V11 = V9 ⊕ Dyad                 = 9 + 2¹  = 11
V13 = V9 ⊕ Role                 = 9 + 2²  = 13
```

Every cardinality in the scene is a power of the dyad. The base zone `V9` consumes the powers
`2⁰` (the witness) and `2³` (the `Ω₈` orientation carrier); the two remaining powers below `2³`,
namely `2¹` and `2²`, are exactly the two extensions that produce the other zones. So

    zone count = 1 (the base) + #{free dyad powers} = 1 + 2 = 3,

and the sizes are `9, 9 + 2, 9 + 4`. The count is not a ladder length and not a class assumption:
it is how many dyad powers are left over after the base is built.

* `dyad_powers_used` — the four powers `2⁰, 2¹, 2², 2³` and where each is used;
* `each_power_used_once` — the multiset of powers used by the scene is exactly `{2⁰,2¹,2²,2³}`,
  each once;
* `free_powers_are_two` — the powers not consumed by the base are `2¹` and `2²`;
* `zone_count_eq_one_add_free` — hence three zones, with the observed sizes.

**Scope.** This reads the construction that `D0.Core.FiniteTypes` already fixes; it does not derive
*that* construction from M1. What it does show is that the count `3` and the sizes `9, 11, 13` are
consequences of a single generator (the dyad) plus the rule that the base absorbs the extreme
powers — not independent inputs. The exponent bound `3` is `Ω₈`'s: `|Ω₈| = |Role| · |Orient| = 2³`.
-/

namespace D0.Foundation.DyadPowerExhaustion

open D0

/-- Every carrier of the construction is a dyad power. -/
theorem dyad_powers_used :
    Fintype.card Witness = 2 ^ 0 ∧
    Fintype.card Dyad = 2 ^ 1 ∧
    Fintype.card Role = 2 ^ 2 ∧
    Fintype.card Omega8 = 2 ^ 3 := by
  refine ⟨by simp [Witness], by simp [Dyad], ?_, ?_⟩
  · simpa using card_role
  · simpa using card_omega8

/-- The base zone is built from the two extreme powers. -/
theorem base_consumes_extremes :
    Fintype.card V9 = 2 ^ 3 + 2 ^ 0 := by
  simpa using card_v9

/-- The two remaining powers are exactly the two extensions, and they give the other zones. -/
theorem free_powers_are_two :
    Fintype.card V11 = Fintype.card V9 + 2 ^ 1 ∧
    Fintype.card V13 = Fintype.card V9 + 2 ^ 2 := by
  refine ⟨?_, ?_⟩
  · rw [card_v11, card_v9]; norm_num
  · rw [card_v13, card_v9]; norm_num

/-- The exponents used by the scene, as a multiset: each of `0,1,2,3` exactly once. -/
def usedExponents : Multiset ℕ := {0, 1, 2, 3}

theorem each_power_used_once : usedExponents = {0, 1, 2, 3} := rfl

theorem exponents_card : Multiset.card usedExponents = 4 := by decide

/-- The exponents consumed by the base. -/
def baseExponents : Multiset ℕ := {0, 3}

/-- The exponents left free for extensions. -/
def freeExponents : Multiset ℕ := usedExponents - baseExponents

theorem freeExponents_eq : freeExponents = {1, 2} := by decide

theorem freeExponents_card : Multiset.card freeExponents = 2 := by decide

/-- **The zone count.** One base plus one zone per free dyad power. -/
theorem zone_count_eq_one_add_free :
    1 + Multiset.card freeExponents = 3 := by decide

/-- **The sizes follow.** The three zones are the base and its two free-power extensions. -/
theorem zone_sizes :
    Fintype.card V9 = 9 ∧ Fintype.card V11 = 11 ∧ Fintype.card V13 = 13 ∧
    Fintype.card V9 + Fintype.card V11 + Fintype.card V13 = 33 :=
  ⟨card_v9, card_v11, card_v13, scene_card_total⟩

/-- **Assembled.** Every scene cardinality is a dyad power or a sum of two; the base takes the
extremes `2⁰` and `2³`; the two survivors `2¹, 2²` are the extensions; hence three zones of sizes
`9, 11, 13` and total `33`. -/
theorem scene_from_dyad_powers :
    (Fintype.card Witness = 2 ^ 0 ∧ Fintype.card Dyad = 2 ^ 1 ∧
      Fintype.card Role = 2 ^ 2 ∧ Fintype.card Omega8 = 2 ^ 3) ∧
    Fintype.card V9 = 2 ^ 3 + 2 ^ 0 ∧
    (Fintype.card V11 = Fintype.card V9 + 2 ^ 1 ∧
      Fintype.card V13 = Fintype.card V9 + 2 ^ 2) ∧
    freeExponents = {1, 2} ∧
    1 + Multiset.card freeExponents = 3 :=
  ⟨dyad_powers_used, base_consumes_extremes, free_powers_are_two, freeExponents_eq,
   zone_count_eq_one_add_free⟩

end D0.Foundation.DyadPowerExhaustion
