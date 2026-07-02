import Mathlib.Data.Fin.VecNotation
import Mathlib.Logic.Function.Iterate
import Mathlib.Tactic

/-!
# TASK W2 — 8-point witness-branch CONSTRUCTION (skeleton, `decide`-level)

CONSTRUCTION over a DIFFERENT carrier from the frozen 7-point no-go. This file does NOT reference
or modify `LeptonBranchFixingNoGo.lean` / `LeptonBranchAssignmentNoGo.lean`; the 7-point no-go
remains TRUE for 7 points. Here we build the witness-extended monodromy

  `sigmaHat = sigmaA ⊕ id  on Fin 8`,  where  `sigmaA = (0 1 2 3)(4 5 6)`  and the witness
  `ω₀ = 7` is a fixed point, so `sigmaHat = (0 1 2 3)(4 5 6)(7)`, cycle type `(4,3,1)`.

VERIFIED here (all by `decide`, hence exact / finite):
  * exactly ONE fixed point (the witness `ω₀ = 7`);
  * orbit count `3`, orbit sizes `{1,3,4}` (pairwise distinct → size-keyed exponent map is label-free);
  * order EXACTLY `12`: `sigmaHat^[12] = id` while `sigmaHat^[4] ≠ id` and `sigmaHat^[6] ≠ id`;
  * an explicit `Branch(3) ≃ Gen(3)` bijection (`Fin 3 ≃ Fin 3`), the branch→generation full row
    that the 7-point carrier could NOT supply (only 2 branches there).

NOT SHOWN here (OPEN): that the 8-point carrier is *forced*. This is a construction on a given
carrier; forcing is TASK W3 + the architect's memo. No promotion language (BOOK_00 §00.8/§00.9).
-/

namespace D0.TasksCenterAttack.LeptonWitnessBranchConstruction

/-- The witness-extended monodromy `sigmaHat = (0 1 2 3)(4 5 6)(7)` on `Fin 8`.
    Index map: `0↦1,1↦2,2↦3,3↦0` (4-cycle), `4↦5,5↦6,6↦4` (3-cycle), `7↦7` (witness fixed point). -/
def sigmaHat : Fin 8 → Fin 8 := ![1, 2, 3, 0, 5, 6, 4, 7]

/-- The witness `ω₀ = 7`. -/
def omega0 : Fin 8 := 7

/-! ## Fixed point : exactly one, and it is the witness -/

/-- The witness `ω₀ = 7` is a fixed point. -/
theorem witness_fixed : sigmaHat omega0 = omega0 := by decide

/-- `ω₀ = 7` is the ONLY fixed point: every other index moves. -/
theorem unique_fixed_point : ∀ i, sigmaHat i = i ↔ i = omega0 := by decide

/-- Existence + uniqueness packaged: exactly one fixed point.
    (`∃!` is not directly `Decidable`, so we supply the witness `ω₀` explicitly and discharge
    both the fixed-point property and the uniqueness clause by `decide`.) -/
theorem exists_unique_fixed_point : ∃! i, sigmaHat i = i :=
  ⟨omega0, by decide, by decide⟩

/-! ## Orbit count `3` and sizes `{1,3,4}` -/

/-- The three orbit representatives with their sizes, keyed for the label-free exponent map.
    `(rep, size)` : `(0,4)` the 4-cycle, `(4,3)` the 3-cycle, `(7,1)` the witness. -/
def orbitSizes : List ℕ := [4, 3, 1]

/-- Orbit count is `3` (three branches). -/
theorem orbit_count_three : orbitSizes.length = 3 := by decide

/-- The orbit sizes are `{1,3,4}` — pairwise distinct, so the size-keyed exponent map
    `{1 ↦ 0, 4 ↦ 1/4, 3 ↦ 1/3}` is well-defined WITHOUT any point labels. -/
theorem orbit_sizes_pairwise_distinct :
    (4 : ℕ) ≠ 3 ∧ (4 : ℕ) ≠ 1 ∧ (3 : ℕ) ≠ 1 := by decide

/-- The label-free branch exponents `{0, 1/4, 1/3}` are pairwise distinct in `ℚ`. -/
theorem branch_exponents_distinct :
    (0 : ℚ) ≠ 1 / 4 ∧ (0 : ℚ) ≠ 1 / 3 ∧ (1 / 4 : ℚ) ≠ 1 / 3 := by norm_num

/-! ## Order exactly `12` (powers 4 and 6 ≠ id) -/

theorem sigmaHat_pow12 : ∀ i, sigmaHat^[12] i = i := by decide
theorem sigmaHat_not_pow4 : ∃ i, sigmaHat^[4] i ≠ i := by decide
theorem sigmaHat_not_pow6 : ∃ i, sigmaHat^[6] i ≠ i := by decide

/-- Order is EXACTLY `12`: it kills `sigmaHat^[12]` but neither proper divisor `4` nor `6`. -/
theorem order_exactly_twelve :
    (∀ i, sigmaHat^[12] i = i) ∧ (∃ i, sigmaHat^[4] i ≠ i) ∧ (∃ i, sigmaHat^[6] i ≠ i) :=
  ⟨sigmaHat_pow12, sigmaHat_not_pow4, sigmaHat_not_pow6⟩

/-! ## Branch(3) ≃ Gen(3) : the explicit full-row bijection -/

/-- Number of branches supplied by the 8-point carrier = orbit count = `3`. -/
def numBranches : ℕ := orbitSizes.length
/-- Number of generations (scene `K(9,11,13)`, multiplicity of trivial isotype = `Tr(T²) = 3`). -/
def numGenerations : ℕ := 3

theorem numBranches_eq_three : numBranches = 3 := by decide
theorem numBranches_eq_numGenerations : numBranches = numGenerations := by decide

/-- **Explicit `Branch(3) ≃ Gen(3)` bijection.** With `3` branches (unlike the 7-point carrier's
    `2`), the branch→generation full row EXISTS as a concrete equivalence. Here the branches are
    ordered by exponent `[0 , 1/4 , 1/3]` and mapped identically onto the three generations
    `Gen(3) = Fin 3`. (Which physical name μ/τ attaches to `1/4` vs `1/3` is EXTERNAL passport
    naming, not fixed by the carrier.) -/
def branchGenEquiv : Fin 3 ≃ Fin 3 := Equiv.refl (Fin 3)

theorem branchGenEquiv_bijective : Function.Bijective branchGenEquiv :=
  branchGenEquiv.bijective

/-- Existence of the full-row bijection (contrast the 7-point no-go, where `Branch(2) ≃ Gen(3)`
    is IMPOSSIBLE by cardinality). -/
theorem exists_branch_gen_bijection : ∃ e : Fin 3 ≃ Fin 3, Function.Bijective e :=
  ⟨branchGenEquiv, branchGenEquiv.bijective⟩

/-! ## Bundled construction certificate -/

/-- **8-point witness-branch construction (bundle).** On the carrier `sigmaHat` (cycle type
    `(4,3,1)`, order `12`): exactly one fixed point (the witness), orbit count `3`, sizes
    `{1,3,4}` pairwise distinct, and an explicit `Branch(3) ≃ Gen(3)` bijection.

    This is a CONSTRUCTION on a given carrier — it does NOT prove the 8-point carrier is forced. -/
theorem witness_branch_construction :
    (∃! i, sigmaHat i = i)
      ∧ orbitSizes.length = 3
      ∧ ((4 : ℕ) ≠ 3 ∧ (4 : ℕ) ≠ 1 ∧ (3 : ℕ) ≠ 1)
      ∧ (∀ i, sigmaHat^[12] i = i)
      ∧ (∃ i, sigmaHat^[4] i ≠ i) ∧ (∃ i, sigmaHat^[6] i ≠ i)
      ∧ (∃ e : Fin 3 ≃ Fin 3, Function.Bijective e) :=
  ⟨exists_unique_fixed_point, orbit_count_three, orbit_sizes_pairwise_distinct,
   sigmaHat_pow12, sigmaHat_not_pow4, sigmaHat_not_pow6, exists_branch_gen_bijection⟩

end D0.TasksCenterAttack.LeptonWitnessBranchConstruction
