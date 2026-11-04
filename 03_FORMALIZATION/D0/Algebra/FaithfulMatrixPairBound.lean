import Mathlib.Data.Matrix.Basis
import Mathlib.LinearAlgebra.Matrix.ToLin
import Mathlib.LinearAlgebra.Prod
import Mathlib.LinearAlgebra.Dimension.Finite
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Tactic

/-!
# Capacity of a faithful representation of two full matrix blocks

The matrix-unit argument below is an algebraic component of the existing
three-tick future-memory result.  It does not construct the original Kraus
operators or assert their effect span, physical admission, or a clock price.
-/

noncomputable section
namespace D0.Algebra.FaithfulMatrixPairBound

open scoped BigOperators

abbrev Blocks (n : ℕ) := Matrix (Fin n) (Fin n) ℂ × Matrix (Fin n) (Fin n) ℂ

/-- Matrix units, with a Boolean selecting one of the two direct summands. -/
def blockUnit {n : ℕ} (b : Bool) (i j : Fin n) : Blocks n :=
  if b then (0, Matrix.single i j 1) else (Matrix.single i j 1, 0)

theorem blockUnit_ne_zero {n : ℕ} (b : Bool) (i : Fin n) :
    blockUnit b i i ≠ 0 := by
  intro h
  have h' := congrArg (fun a : Blocks n => if b then a.2 i i else a.1 i i) h
  cases b <;> simp [blockUnit, Matrix.single] at h'

theorem blockUnit_mul {n : ℕ} (b c : Bool) (i j k l : Fin n) :
    blockUnit b i j * blockUnit c k l =
      if b = c ∧ j = k then blockUnit b i l else 0 := by
  cases b <;> cases c <;> by_cases h : j = k <;>
    simp [blockUnit, h, Matrix.single_mul_single_same, Matrix.single_mul_single_of_ne]

variable {V : Type*} [AddCommGroup V] [Module ℂ V]

/-- Faithfulness forces each diagonal matrix unit to have a nonzero action. -/
theorem blockUnit_nonzero_action {n : ℕ} (π : Blocks n →ₐ[ℂ] Module.End ℂ V)
    (hπ : Function.Injective π) (b : Bool) (i : Fin n) :
    ∃ v : V, π (blockUnit b i i) v ≠ 0 := by
  have hmap : π (blockUnit b i i) ≠ 0 := by
    intro h
    apply blockUnit_ne_zero b i
    apply hπ
    simpa using h
  by_contra h
  push Not at h
  apply hmap
  ext v
  simpa using h v

/-- Chosen nonzero image vector in the selected diagonal corner. -/
def cornerSeed {n : ℕ} (π : Blocks n →ₐ[ℂ] Module.End ℂ V)
    (hπ : Function.Injective π) (i : Fin n) (b : Bool) : V :=
  π (blockUnit b i i) (Classical.choose (blockUnit_nonzero_action π hπ b i))

theorem cornerSeed_ne_zero {n : ℕ} (π : Blocks n →ₐ[ℂ] Module.End ℂ V)
    (hπ : Function.Injective π) (i : Fin n) (b : Bool) :
    cornerSeed π hπ i b ≠ 0 :=
  Classical.choose_spec (blockUnit_nonzero_action π hπ b i)

theorem cornerSeed_fixed {n : ℕ} (π : Blocks n →ₐ[ℂ] Module.End ℂ V)
    (hπ : Function.Injective π) (i : Fin n) (b : Bool) :
    π (blockUnit b i i) (cornerSeed π hπ i b) = cornerSeed π hπ i b := by
  unfold cornerSeed
  rw [← Module.End.mul_apply, ← map_mul, blockUnit_mul]
  simp

/-- One vector per row of each block, obtained from the two corner seeds. -/
def cornerVector {n : ℕ} (π : Blocks n →ₐ[ℂ] Module.End ℂ V)
    (hπ : Function.Injective π) (i : Fin n) (p : Bool × Fin n) : V :=
  π (blockUnit p.1 p.2 i) (cornerSeed π hπ i p.1)

def rowProbe {n : ℕ} (π : Blocks n →ₐ[ℂ] Module.End ℂ V)
    (i : Fin n) (p : Bool × Fin n) : Module.End ℂ V :=
  π (blockUnit p.1 i p.2)

theorem rowProbe_cornerVector {n : ℕ} (π : Blocks n →ₐ[ℂ] Module.End ℂ V)
    (hπ : Function.Injective π) (i : Fin n) (p q : Bool × Fin n) :
    rowProbe π i p (cornerVector π hπ i q) =
      if p = q then cornerSeed π hπ i p.1 else 0 := by
  unfold rowProbe cornerVector
  rw [← Module.End.mul_apply, ← map_mul, blockUnit_mul]
  by_cases hpq : p = q
  · subst q
    simp [cornerSeed_fixed]
  · have hcomponents : ¬ (p.1 = q.1 ∧ p.2 = q.2) := by
      intro h
      exact hpq (Prod.ext h.1 h.2)
    simp [hpq, hcomponents]

theorem cornerVector_linearIndependent {n : ℕ} (π : Blocks n →ₐ[ℂ] Module.End ℂ V)
    (hπ : Function.Injective π) (i : Fin n) :
    LinearIndependent ℂ (cornerVector π hπ i) := by
  rw [Fintype.linearIndependent_iff]
  intro g hg p
  have h := congrArg (rowProbe π i p) hg
  simp only [map_sum, map_smul, map_zero, rowProbe_cornerVector] at h
  have h' : g p • cornerSeed π hπ i p.1 = 0 := by simpa using h
  exact (smul_eq_zero.mp h').resolve_right (cornerSeed_ne_zero π hπ i p.1)

/-- A faithful unital action of two `n × n` blocks needs dimension at least `2n`.
The proof derives all independent vectors from the action; it assumes no rank
or dimension bound. It applies, in particular, to faithful unital star actions. -/
theorem faithful_pair_finrank_lower_bound {n : ℕ} (hn : 0 < n)
    [FiniteDimensional ℂ V] (π : Blocks n →ₐ[ℂ] Module.End ℂ V)
    (hπ : Function.Injective π) : 2 * n ≤ Module.finrank ℂ V := by
  let i : Fin n := ⟨0, hn⟩
  have h := (cornerVector_linearIndependent π hπ i).fintype_card_le_finrank
  simpa using h

section Continuous

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
  [CompleteSpace H] [FiniteDimensional ℂ H]

/-- Forget continuity while preserving the operator algebra. -/
def forgetContinuousEnd : (H →L[ℂ] H) →ₐ[ℂ] Module.End ℂ H where
  toFun := ContinuousLinearMap.toLinearMap
  map_one' := rfl
  map_mul' _ _ := rfl
  map_zero' := rfl
  map_add' _ _ := rfl
  commutes' _ := rfl

omit [CompleteSpace H] [FiniteDimensional ℂ H] in
theorem forgetContinuousEnd_injective :
    Function.Injective (forgetContinuousEnd : (H →L[ℂ] H) →ₐ[ℂ] Module.End ℂ H) := by
  intro f g h
  ext x
  exact congrArg (fun k : Module.End ℂ H => k x) h

/-- The source's faithful unital star-representation is a direct consumer of
the algebraic bound; no independent dimension or vector family is assumed. -/
theorem faithful_star_pair_finrank_lower_bound {n : ℕ} (hn : 0 < n)
    (π : Blocks n →⋆ₐ[ℂ] (H →L[ℂ] H)) (hπ : Function.Injective π) :
    2 * n ≤ Module.finrank ℂ H := by
  apply faithful_pair_finrank_lower_bound hn (forgetContinuousEnd.comp π.toAlgHom)
  exact forgetContinuousEnd_injective.comp hπ

theorem faithful_star_pair_eight_lower_bound
    (π : Blocks 8 →⋆ₐ[ℂ] (H →L[ℂ] H)) (hπ : Function.Injective π) :
    16 ≤ Module.finrank ℂ H := by
  simpa using faithful_star_pair_finrank_lower_bound (by decide : 0 < 8) π hπ

end Continuous

abbrev PairCarrier (n : ℕ) := (Fin n → ℂ) × (Fin n → ℂ)

/-- The two defining matrix actions on their own vector blocks. -/
def standardPairAction (n : ℕ) : Blocks n →ₐ[ℂ] Module.End ℂ (PairCarrier n) :=
  let matrixAction : Matrix (Fin n) (Fin n) ℂ →ₐ[ℂ] Module.End ℂ (Fin n → ℂ) :=
    Matrix.toLinAlgEquiv'.toAlgHom
  (LinearMap.prodMapAlgHom ℂ (Fin n → ℂ) (Fin n → ℂ)).comp
    (matrixAction.prodMap matrixAction)

theorem standardPairAction_injective (n : ℕ) : Function.Injective (standardPairAction n) := by
  intro a b h
  apply Prod.ext
  · apply (Matrix.toLinAlgEquiv' : Matrix (Fin n) (Fin n) ℂ ≃ₐ[ℂ]
        Module.End ℂ (Fin n → ℂ)).injective
    apply LinearMap.ext
    intro v
    have h' := congrArg (fun f : Module.End ℂ (PairCarrier n) => (f (v, 0)).1) h
    simpa [standardPairAction] using h'
  · apply (Matrix.toLinAlgEquiv' : Matrix (Fin n) (Fin n) ℂ ≃ₐ[ℂ]
        Module.End ℂ (Fin n → ℂ)).injective
    apply LinearMap.ext
    intro v
    have h' := congrArg (fun f : Module.End ℂ (PairCarrier n) => (f (0, v)).2) h
    simpa [standardPairAction] using h'

theorem pairCarrier_finrank (n : ℕ) : Module.finrank ℂ (PairCarrier n) = 2 * n := by
  simp [PairCarrier, Module.finrank_prod]
  omega

/-- The bound is attained by the explicit direct sum of defining actions. -/
theorem standardPairAction_attains_bound (n : ℕ) :
    Function.Injective (standardPairAction n) ∧ Module.finrank ℂ (PairCarrier n) = 2 * n :=
  ⟨standardPairAction_injective n, pairCarrier_finrank n⟩

/-- Forgetting a block remains a unital algebra action but cannot be faithful. -/
def firstBlockAction (n : ℕ) : Blocks n →ₐ[ℂ] Module.End ℂ (Fin n → ℂ) :=
  Matrix.toLinAlgEquiv'.toAlgHom.comp (AlgHom.fst ℂ _ _)

theorem firstBlockAction_not_injective {n : ℕ} (hn : 0 < n) :
    ¬ Function.Injective (firstBlockAction n) := by
  intro h
  let i : Fin n := ⟨0, hn⟩
  have heq : firstBlockAction n (blockUnit true i i) = firstBlockAction n 0 := by
    simp [firstBlockAction, blockUnit]
  exact blockUnit_ne_zero true i (h heq)

end D0.Algebra.FaithfulMatrixPairBound
end
