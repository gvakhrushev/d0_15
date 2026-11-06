import D0.Geometry.OriginalBookEffectParity
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.LinearAlgebra.Dimension.StrongRankCondition
import Mathlib.Tactic

/-!
# A 128-dimensional upper bound for the actual source effect span

The existing source/Fock parity on Fin16 has eight even and eight odd basis
states. Every actual chronological effect was proved to commute with that
parity. Restricting such matrices to their two diagonal blocks is injective,
so the complex span of all finite actual effects has dimension at most 128.
No lower bound, equality of spans, modular-to-complex transfer, physical
admission, or GR conclusion is claimed.
-/
open D0
open Matrix
open scoped BigOperators
open D0.Geometry.OriginalBookCreatorParity
open D0.Geometry.OriginalBookJuliaWords
open D0.Geometry.OriginalBookJuliaParity
open D0.Geometry.OriginalBookEffectWords
open D0.Geometry.OriginalBookEffectParity

namespace D0.Geometry.OriginalBookEffectSpanUpper

abbrev EvenState := {i : Fin 16 // sourceParityInt i = 1}
abbrev OddState := {i : Fin 16 // sourceParityInt i = -1}

lemma evenState_card : Fintype.card EvenState = 8 := by decide
lemma oddState_card : Fintype.card OddState = 8 := by decide

lemma sign_cases (i : Fin 16) : sourceParityInt i = 1 ∨ sourceParityInt i = -1 := by
  unfold sourceParityInt
  split_ifs <;> simp

/-- All parity-even source matrices form a complex linear subspace. -/
def evenSubmodule : Submodule ℂ Operator where
  carrier := IsEven
  zero_mem' := Commute.zero_right _
  add_mem' := fun hx hy => hx.add_right hy
  smul_mem' := fun c _ hx => hx.smul_right c

/-- A matrix commuting with parity has no cross-parity entries. -/
lemma mixed_entry_zero {X : Operator} (hX : IsEven X) (i j : Fin 16)
    (hij : sourceParityInt i ≠ sourceParityInt j) : X i j = 0 := by
  have h := congrArg (fun M : Operator => M i j) hX.eq
  simp only [sourceParity, Matrix.diagonal_mul, Matrix.mul_diagonal] at h
  have hc : (sourceParityInt i : ℂ) ≠ (sourceParityInt j : ℂ) := by exact_mod_cast hij
  have hz : ((sourceParityInt i : ℂ) - (sourceParityInt j : ℂ)) * X i j = 0 := by
    linear_combination h
  exact (mul_eq_zero.mp hz).resolve_left (sub_ne_zero.mpr hc)

/-- Read the two actual parity blocks; no surjectivity is assumed. -/
def readBlocks : evenSubmodule →ₗ[ℂ]
    Matrix EvenState EvenState ℂ × Matrix OddState OddState ℂ where
  toFun X := (fun i j => X.val i j, fun i j => X.val i j)
  map_add' := by intros; ext <;> rfl
  map_smul' := by intros; ext <;> rfl

/-- Mixed entries vanish, so the two actual blocks determine an even matrix. -/
theorem readBlocks_injective : Function.Injective readBlocks := by
  intro X Y h
  apply Subtype.ext
  ext i j
  rcases sign_cases i with hi | hi <;> rcases sign_cases j with hj | hj
  · exact congrArg (fun pair : Matrix EvenState EvenState ℂ × Matrix OddState OddState ℂ =>
        pair.1 ⟨i, hi⟩ ⟨j, hj⟩) h
  · have hn : sourceParityInt i ≠ sourceParityInt j := by rw [hi, hj]; norm_num
    rw [mixed_entry_zero X.property i j hn, mixed_entry_zero Y.property i j hn]
  · have hn : sourceParityInt i ≠ sourceParityInt j := by rw [hi, hj]; norm_num
    rw [mixed_entry_zero X.property i j hn, mixed_entry_zero Y.property i j hn]
  · exact congrArg (fun pair : Matrix EvenState EvenState ℂ × Matrix OddState OddState ℂ =>
        pair.2 ⟨i, hi⟩ ⟨j, hj⟩) h

/-- Fock parity permits at most two 8×8 complex blocks. -/
theorem evenSubmodule_finrank_le : Module.finrank ℂ evenSubmodule ≤ 128 := by
  have h := LinearMap.finrank_le_finrank_of_injective readBlocks_injective
  have hdim : Module.finrank ℂ
      (Matrix EvenState EvenState ℂ × Matrix OddState OddState ℂ) = 128 := by
    simp [Module.finrank_prod, Module.finrank_matrix, evenState_card, oddState_card]
  simpa [hdim] using h

/-- Span over ℂ of all actual no-reset finite chronological source effects. -/
noncomputable def sourceEffectSpan : Submodule ℂ Operator :=
  Submodule.span ℂ (Set.range sourceEffect)

theorem sourceEffectSpan_le_even : sourceEffectSpan ≤ evenSubmodule := by
  apply Submodule.span_le.mpr
  rintro _ ⟨path, rfl⟩
  exact sourceEffect_even path

/-- Exact parity-based upper bound; independence and equality remain open. -/
theorem sourceEffectSpan_finrank_le : Module.finrank ℂ sourceEffectSpan ≤ 128 := by
  exact (Submodule.finrank_mono sourceEffectSpan_le_even).trans evenSubmodule_finrank_le

end D0.Geometry.OriginalBookEffectSpanUpper
