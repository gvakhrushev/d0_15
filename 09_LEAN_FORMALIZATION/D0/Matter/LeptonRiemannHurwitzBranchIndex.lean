import D0.Edge.RamificationFromUeEffCompanion
import Mathlib.Tactic

/-!
# D0-LEPTON-RIEMANN-HURWITZ-BRANCH-INDEX-001 — cyclic-cover branch index + genus-0 consistency

Python certificate: `05_CERTS/vp_lepton_riemann_hurwitz_branch_index.py`.

Front F3 (narrow, NO uniqueness). The charged-lepton shell-torus cover is built from two cyclic
companion blocks (`D0-EDGE-RAMIFICATION-001`): the 4-cycle `C4` (charpoly `x⁴ − λ`) and the 3-cycle
`R3` (charpoly `x³ − λ`). At a branch point the cover `zⁿ − λ` solves as `z = λ^{1/n}`, so the
**Puiseux / ramification exponent** of the `n`-cycle is `1/n` and the **ramification index** is `n`.
This module machine-checks, over `ℚ` and `ℤ` with finite/decidable tactics:

* the **cyclic relations** `C4⁴ = λ·I` and `R3³ = λ·I` (reused from `D0.Edge`);
* the **ramification exponent** `1/n` (encoded as `ramIndex n = n`, `puiseuxExp n = 1/n`), for `n = 3,4`
  and as the general definitional identity;
* the **Riemann–Hurwitz genus-0 CONSISTENCY identity**: for a connected cyclic degree-`n` cover of `ℙ¹`
  with total ramification defect `2(n−1)` (totally ramified over two points), the genus `g` solves
  `2 − 2g = 2n − 2(n−1)`, which forces `g = 0` **for every** `n` (proved by `omega`/`decide`).

HONESTY BOUNDARY — what is **NOT** claimed. Riemann–Hurwitz does **NOT** force the pair `(4, 3)`
uniquely: EVERY connected cyclic cover is genus `0`, so the genus identity is satisfied by `n = 2,3,4,5,…`
alike. The "branch index determines the operator" shortcut is independently FORBIDDEN
(`D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001`, two distinct operators with the same index `1/4`). No
PDG mass enters. The finite Green resolvent + branch-index uniqueness stay PROOF-TARGET
(`D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001`).
-/

namespace D0.Matter

open D0.Edge Matrix

/-- **Ramification index** of an `n`-cycle companion cover `zⁿ − λ`: the index is `n`
(all `n` sheets collapse at the branch point `λ = 0`). -/
def ramIndex (n : ℕ) : ℕ := n

/-- **Puiseux / ramification exponent** of an `n`-cycle cover `zⁿ − λ`: `z = λ^{1/n}`, exponent `1/n`. -/
def puiseuxExp (n : ℕ) : ℚ := 1 / (n : ℚ)

/-- The 4-cycle ramification index is `4` and the muon Puiseux exponent is `1/4`. -/
theorem ramification_C4 : ramIndex 4 = 4 ∧ puiseuxExp 4 = 1 / 4 := by
  unfold ramIndex puiseuxExp; norm_num

/-- The 3-cycle ramification index is `3` and the tau Puiseux exponent is `1/3`. -/
theorem ramification_R3 : ramIndex 3 = 3 ∧ puiseuxExp 3 = 1 / 3 := by
  unfold ramIndex puiseuxExp; norm_num

/-- **The Puiseux exponent is the reciprocal of the ramification index**, definitionally, for any
`n ≥ 1` (`puiseuxExp n = 1 / ramIndex n`). -/
theorem puiseux_is_reciprocal_of_index (n : ℕ) :
    puiseuxExp n = 1 / (ramIndex n : ℚ) := by
  simp only [puiseuxExp, ramIndex]

/-- **Cyclic relation reused for the 4-cycle:** `C4⁴ = λ·I` (`D0.Edge.companionC4_cyclic`). -/
theorem branch_C4_cyclic (lam : ℚ) :
    (companionC4 lam) ^ 4 = lam • (1 : Matrix (Fin 4) (Fin 4) ℚ) :=
  companionC4_cyclic lam

/-- **Cyclic relation reused for the 3-cycle:** `R3³ = λ·I` (`D0.Edge.companionR3_cyclic`). -/
theorem branch_R3_cyclic (lam : ℚ) :
    (companionR3 lam) ^ 3 = lam • (1 : Matrix (Fin 3) (Fin 3) ℚ) :=
  companionR3_cyclic lam

/-- **Total ramification defect** of a connected cyclic degree-`n` cover of `ℙ¹` that is totally
ramified over two branch points: each totally-ramified fibre contributes `n − 1`, so the total defect
is `2(n − 1)`. -/
def ramDefect (n : ℕ) : ℤ := 2 * ((n : ℤ) - 1)

/-- **Riemann–Hurwitz Euler-characteristic balance** for the cover. The base `ℙ¹` has Euler
characteristic `2`; a degree-`n` cover with total ramification defect `R` has Euler characteristic
`n · 2 − R`. With `R = ramDefect n = 2(n − 1)` this equals `2n − 2(n − 1)`. We package the cover's
Euler characteristic as a definition for the genus extraction below. -/
def coverEuler (n : ℕ) : ℤ := (n : ℤ) * 2 - ramDefect n

/-- **The cover Euler characteristic is identically `2` for every `n`** — the arithmetic core of
Riemann–Hurwitz: `2n − 2(n − 1) = 2`. Proved over `ℤ` by `ring`-style simplification (`omega`). -/
theorem coverEuler_eq_two (n : ℕ) : coverEuler n = 2 := by
  unfold coverEuler ramDefect; ring

/-- **Genus-0 consistency identity.** If the genus `g : ℤ` satisfies the Riemann–Hurwitz balance
`2 − 2g = coverEuler n` (i.e. `2 − 2g = 2n − 2(n−1)`), then `g = 0` — for EVERY `n`. -/
theorem genus_is_zero (n : ℕ) (g : ℤ) (h : 2 - 2 * g = coverEuler n) : g = 0 := by
  rw [coverEuler_eq_two] at h
  omega

/-- **Explicit genus-0 check for `n = 4` (muon 4-cycle).** The balance `2 − 2g = coverEuler 4`
forces `g = 0`. -/
theorem genus_zero_n4 (g : ℤ) (h : 2 - 2 * g = coverEuler 4) : g = 0 :=
  genus_is_zero 4 g h

/-- **Explicit genus-0 check for `n = 3` (tau 3-cycle).** The balance `2 − 2g = coverEuler 3`
forces `g = 0`. -/
theorem genus_zero_n3 (g : ℤ) (h : 2 - 2 * g = coverEuler 3) : g = 0 :=
  genus_is_zero 3 g h

/-- **NOT a uniqueness statement.** Riemann–Hurwitz gives genus `0` for `n = 2, 3, 4, 5` ALL alike, so
the genus identity does NOT single out the pair `(4, 3)`: the Euler characteristic is `2` for every one
of them (each instance of the general `coverEuler_eq_two`). -/
theorem genus_zero_not_unique :
    coverEuler 2 = 2 ∧ coverEuler 3 = 2 ∧ coverEuler 4 = 2 ∧ coverEuler 5 = 2 :=
  ⟨coverEuler_eq_two 2, coverEuler_eq_two 3, coverEuler_eq_two 4, coverEuler_eq_two 5⟩

/-- **D0-LEPTON-RIEMANN-HURWITZ-BRANCH-INDEX-001 (CERT-CLOSED — narrow arithmetic + identity, NO
uniqueness).** The cyclic companion cover carries: the relations `C4⁴ = λI`, `R3³ = λI`; ramification
indices `4` and `3` with Puiseux exponents `1/4` and `1/3`; and the Riemann–Hurwitz genus-0 consistency
identity `2 − 2g = coverEuler n ⇒ g = 0`, which holds for EVERY `n` (so it does NOT make `(4,3)` unique).
No PDG mass enters; the operator-uniqueness and finite Green resolvent stay external. -/
theorem lepton_riemann_hurwitz_branch_index :
    -- (a) cyclic relations
    (∀ lam : ℚ, (companionC4 lam) ^ 4 = lam • (1 : Matrix (Fin 4) (Fin 4) ℚ))
      ∧ (∀ lam : ℚ, (companionR3 lam) ^ 3 = lam • (1 : Matrix (Fin 3) (Fin 3) ℚ))
      -- (b) ramification indices / Puiseux exponents 1/n for n = 4, 3
      ∧ (ramIndex 4 = 4 ∧ puiseuxExp 4 = 1 / 4)
      ∧ (ramIndex 3 = 3 ∧ puiseuxExp 3 = 1 / 3)
      ∧ (∀ n : ℕ, puiseuxExp n = 1 / (ramIndex n : ℚ))
      -- (c) Riemann–Hurwitz genus-0 consistency for every n (the Euler char is identically 2)
      ∧ (∀ n : ℕ, coverEuler n = 2)
      ∧ (∀ (n : ℕ) (g : ℤ), 2 - 2 * g = coverEuler n → g = 0)
      -- (d) NOT unique: genus 0 for n = 2,3,4,5 alike (R-H does NOT force the pair (4,3))
      ∧ (coverEuler 2 = 2 ∧ coverEuler 3 = 2 ∧ coverEuler 4 = 2 ∧ coverEuler 5 = 2) :=
  ⟨branch_C4_cyclic, branch_R3_cyclic, ramification_C4, ramification_R3,
   puiseux_is_reciprocal_of_index, coverEuler_eq_two, genus_is_zero, genus_zero_not_unique⟩

end D0.Matter
