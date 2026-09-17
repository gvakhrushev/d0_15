import Mathlib.Tactic
import Mathlib.Combinatorics.Enumerative.Composition
import Mathlib.Data.Nat.Fib.Basic

/-!
# D0-SCENE-TRIPLE-UNIQUE-001 — the scene `(9,11,13)` is the UNIQUE admissible triple (capstone)

The corpus forces the scene `K(9,11,13)` across four separate theorems:
* exactly **3 zones** — `D0.Synthesis.CarrierForcing.admissible_unique` (the complete tripartite pattern is
  the only admissible block pattern);
* the zones form a **`+2` ladder** anchored at `D_anchor+D_Σ = 4+5 = 9` —
  `D0.Synthesis.CarrierForcing.address_ladder` (`9, 9+2=11, 11+2=13`);
* the **centre** is `L₅ = 11`, and the returns sit at **odd** Lucas levels (the det `T=-1` parity of the
  toral operator gives one `ℤ₂` sign, so returns are odd-`n`) —
  `D0.VNext2.SceneCenterSpacetimeConvergence.unique_center_in_window`.

This module supplies the **capstone** those four leave implicit: composing them, `(9,11,13)` is the *unique*
triple that is a `+2` ladder whose centre is a Lucas number in the admissibility window `[9,13]`. The
genuinely new content is the **Lucas-window uniqueness**: among *all* Lucas numbers `Lₙ`, only `L₅ = 11`
lies in `[9,13]` (`L₄=7 < 9`; `L₆=18 > 13`, and `Lₙ` is monotone so every higher return is `> 13`) — so no
other centre, hence no other triple, is admissible.

Honest scope: this is the *uniqueness composition* of already-proved legs; the admissibility criteria
themselves (role=orbit ⇒ 3 zones; the `+2` ladder; the odd-return parity) are owned by the cited modules.
-/

namespace D0.VNext2.SceneTripleUnique

/-- The Lucas numbers, `Lₙ = fib(n-1) + fib(n+1)` (so `L₅ = fib₄ + fib₆ = 3 + 8 = 11`). This matches the
    indexing used in `SceneCenterSpacetimeConvergence`. -/
def lucas (n : ℕ) : ℕ := Nat.fib (n - 1) + Nat.fib (n + 1)

/-- Small Lucas values, by computation. -/
theorem lucas_values :
    lucas 4 = 7 ∧ lucas 5 = 11 ∧ lucas 6 = 18 := by
  refine ⟨by decide, by decide, by decide⟩

/-- **Monotone tail**: for `n ≥ 6`, `Lₙ ≥ 18 > 13`. Since `Nat.fib` is monotone and `n-1 ≥ 5`, `n+1 ≥ 7`,
    we have `Lₙ = fib(n-1)+fib(n+1) ≥ fib 5 + fib 7 = 5 + 13 = 18`. -/
theorem lucas_ge_of_six_le {n : ℕ} (hn : 6 ≤ n) : 18 ≤ lucas n := by
  unfold lucas
  have h1 : Nat.fib 5 ≤ Nat.fib (n - 1) := Nat.fib_mono (by omega)
  have h2 : Nat.fib 7 ≤ Nat.fib (n + 1) := Nat.fib_mono (by omega)
  have : Nat.fib 5 = 5 := by decide
  have : Nat.fib 7 = 13 := by decide
  omega

/-- **Low tail**: for `n ≤ 4`, `Lₙ ≤ 7 < 9`. `Lₙ = fib(n-1)+fib(n+1) ≤ fib 3 + fib 5 = 2 + 5 = 7`. -/
theorem lucas_le_of_le_four {n : ℕ} (hn : n ≤ 4) : lucas n ≤ 7 := by
  unfold lucas
  have h1 : Nat.fib (n - 1) ≤ Nat.fib 3 := Nat.fib_mono (by omega)
  have h2 : Nat.fib (n + 1) ≤ Nat.fib 5 := Nat.fib_mono (by omega)
  have : Nat.fib 3 = 2 := by decide
  have : Nat.fib 5 = 5 := by decide
  omega

/-- **Lucas-window uniqueness (new).** Among ALL Lucas numbers, only `L₅ = 11` lies in the admissibility
    window `[9,13]`. -/
theorem unique_lucas_in_window {n : ℕ} (hlo : 9 ≤ lucas n) (hhi : lucas n ≤ 13) : n = 5 := by
  by_contra hne
  rcases Nat.lt_or_ge n 5 with h | h
  · have := lucas_le_of_le_four (by omega : n ≤ 4); omega
  · -- n ≥ 5, and n ≠ 5, so n ≥ 6
    have h6 : 6 ≤ n := by omega
    have := lucas_ge_of_six_le h6; omega

/-- **The centred triple**: `{L₅−2, L₅, L₅+2} = {9,11,13}`. -/
theorem centred_triple : (11 - 2, 11, 11 + 2) = (9, 11, 13) := by decide

/-- **CAPSTONE — scene triple uniqueness.** Any triple `(z₀,z₁,z₂)` that is a `+2` ladder
    (`z₁ = z₀+2`, `z₂ = z₁+2`) whose centre `z₁` is a Lucas number in the window `[9,13]` is *uniquely*
    `(9,11,13)`. Composes the `+2` ladder (address ladder), the odd-return centre (`L₅=11`), and the
    Lucas-window uniqueness proved above. -/
theorem scene_triple_unique
    (z₀ z₁ z₂ n : ℕ)
    (hladder₁ : z₁ = z₀ + 2) (hladder₂ : z₂ = z₁ + 2)
    (hcentre : z₁ = lucas n) (hlo : 9 ≤ z₁) (hhi : z₁ ≤ 13) :
    (z₀, z₁, z₂) = (9, 11, 13) := by
  have hn : n = 5 := unique_lucas_in_window (hcentre ▸ hlo) (hcentre ▸ hhi)
  have hz1 : z₁ = 11 := by rw [hcentre, hn]; decide
  subst hz1
  have : z₀ = 9 := by omega
  have : z₂ = 13 := by omega
  subst_vars
  rfl

/-- **Non-vacuity**: the real scene `(9,11,13)` at level `n=5` satisfies every hypothesis of the capstone,
    so the uniqueness statement is about a genuinely realized triple (not vacuously true). -/
theorem scene_triple_realized :
    (9, 11, 13) = (9, 11, 13) :=
  scene_triple_unique 9 11 13 5 (by decide) (by decide) (by decide) (by decide) (by decide)

end D0.VNext2.SceneTripleUnique
