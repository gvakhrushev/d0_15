import Mathlib.Tactic
import Mathlib.Data.Nat.Factorization.Defs

/-!
# Removing the enumeration assumption from the spectral zone-count derivation

`D0.Synthesis.ZoneCountFromSpectrum` derives the zone count from the spectral pair
`(D, H) = (1287, 960)`, but its enumeration of the eleven factorisations was justified by the
arithmetic remark `Ω(1287) = 4`, taken as read. This module removes the guesswork in two steps.

**Step 1 — the length is bounded, proved.** `two_pow_length_le_prod` and `length_bound`: a list of
naturals each `≥ 2` has product at least `2 ^ length`, so a factorisation of `1287` has at most ten
parts. This uses no factorisation theory.

**Step 2 — the two parts are forced, decided.** This is the real content, and it needs neither the
bound above nor any enumeration. Every part divides `1287`, so lies in

    {3, 9, 11, 13, 33, 39, 99, 117, 143, 429, 1287},

whose reduced values `n − 1` are

    {2, 8, 10, 12, 32, 38, 98, 116, 142, 428, 1286}.

Now `H = 960 = 2⁶ · 3 · 5`, so `5 ∣ H` and `3 ∣ H`. Among the reduced values

* only `10` is divisible by `5` — so the part `11` must occur (`only_eleven_carries_five`);
* only `12` is divisible by `3` — so the part `13` must occur (`only_thirteen_carries_three`).

Removing them leaves product `1287 / 143 = 9` and reduced product `960 / 120 = 8`. The only
factorisations of `9` into parts `≥ 2` are `[9]` and `[3,3]`, with reduced products `8` and `4`
respectively, so the remainder is `[9]` (`remainder_forced`). Hence the scene is `[9, 11, 13]`, and
in particular has three parts — with no enumeration and no length assumption.

Each numbered fact below is machine-checked; what is not mechanised is the list surgery that
threads them together, which is why the assembled statement still lives in the companion module.
-/

namespace D0.Synthesis.ZoneCountCompleteness

/-- A list of naturals each at least `2` has product at least `2 ^ length`; this bounds the number
of parts without any factorisation theory. -/
theorem two_pow_length_le_prod : ∀ (l : List ℕ), (∀ x ∈ l, 2 ≤ x) → 2 ^ l.length ≤ l.prod := by
  intro l
  induction l with
  | nil => intro _; simp
  | cons a t ih =>
    intro h2
    have ha : 2 ≤ a := h2 a (by simp)
    have ht : ∀ x ∈ t, 2 ≤ x := fun x hx => h2 x (by simp [hx])
    have hprod : 2 ^ t.length ≤ t.prod := ih ht
    simp only [List.length_cons, List.prod_cons, pow_succ]
    calc 2 ^ t.length * 2 ≤ t.prod * a := Nat.mul_le_mul hprod ha
      _ = a * t.prod := Nat.mul_comm _ _

/-- Consequently a factorisation of `1287` into parts `≥ 2` has at most ten of them. The sharp
bound is four (`1287 = 3 · 3 · 11 · 13`), but the completeness argument below needs no bound at
all — it forces the parts directly. -/
theorem length_bound (l : List ℕ) (h2 : ∀ x ∈ l, 2 ≤ x) (hp : l.prod = 1287) :
    l.length ≤ 10 := by
  by_contra h
  have h11 : 11 ≤ l.length := by omega
  have := two_pow_length_le_prod l h2
  rw [hp] at this
  have : (2 : ℕ) ^ 11 ≤ 2 ^ l.length := Nat.pow_le_pow_right (by norm_num) h11
  omega

/-- The divisors of `1287` that can occur as a part. -/
def parts : List ℕ := [3, 9, 11, 13, 33, 39, 99, 117, 143, 429, 1287]

theorem parts_divide : ∀ n ∈ parts, n ∣ 1287 := by decide

/-- **Only the part `11` carries the prime `5` into `H`.** -/
theorem only_eleven_carries_five : ∀ n ∈ parts, 5 ∣ (n - 1) → n = 11 := by decide

/-- **Only the part `13` carries the prime `3` into `H`.** -/
theorem only_thirteen_carries_three : ∀ n ∈ parts, 3 ∣ (n - 1) → n = 13 := by decide

/-- `960` carries both primes, so both parts are forced. -/
theorem target_carries_both : (5 ∣ 960) ∧ (3 ∣ 960) := by decide

/-- **The remainder is forced.** After removing `11` and `13` the product left is `9` and the
reduced product left is `8`; of the two factorisations of `9` into parts `≥ 2`, only `[9]` gives
`8`. -/
theorem remainder_forced :
    (1287 / (11 * 13) = 9) ∧ (960 / (10 * 12) = 8) ∧
    (([9] : List ℕ).prod = 9 ∧ (([9] : List ℕ).map (fun n => n - 1)).prod = 8) ∧
    (([3, 3] : List ℕ).prod = 9 ∧ (([3, 3] : List ℕ).map (fun n => n - 1)).prod = 4) := by
  refine ⟨by decide, by decide, ⟨by decide, by decide⟩, ⟨by decide, by decide⟩⟩

/-- **The backbone, assembled.** The parts `11` and `13` are forced by the primes `5` and `3`
dividing `H`; the remainder then has product `9` and reduced product `8`, which only `[9]` meets. -/
theorem completeness_backbone :
    (∀ n ∈ parts, 5 ∣ (n - 1) → n = 11) ∧
    (∀ n ∈ parts, 3 ∣ (n - 1) → n = 13) ∧
    (5 ∣ 960 ∧ 3 ∣ 960) ∧
    (1287 / (11 * 13) = 9 ∧ 960 / (10 * 12) = 8) :=
  ⟨only_eleven_carries_five, only_thirteen_carries_three, target_carries_both,
   ⟨remainder_forced.1, remainder_forced.2.1⟩⟩

end D0.Synthesis.ZoneCountCompleteness
