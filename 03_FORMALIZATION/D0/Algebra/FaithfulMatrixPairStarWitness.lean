import D0.Algebra.FaithfulMatrixPairBound
import Mathlib.Data.Matrix.Block

/-! A conditional *-representation witness for the block-pair bound.
It does not identify the original CAR effects or prove physical admission. -/

namespace D0.Algebra.FaithfulMatrixPairStarWitness
open D0.Algebra.FaithfulMatrixPairBound

noncomputable section

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
  [FiniteDimensional ℂ H]

def continuousEndOfLinear : Module.End ℂ H →ₐ[ℂ] (H →L[ℂ] H) where
  toFun := LinearMap.toContinuousLinearMap
  map_one' := rfl
  map_mul' _ _ := rfl
  map_zero' := rfl
  map_add' _ _ := rfl
  commutes' _ := rfl

/-- The standard matrix action on an orthonormal Euclidean basis. -/
def euclideanMatrixStarAction (ι : Type*) [Fintype ι] [DecidableEq ι] :
    Matrix ι ι ℂ →⋆ₐ[ℂ] (EuclideanSpace ℂ ι →L[ℂ] EuclideanSpace ℂ ι) where
  toAlgHom := continuousEndOfLinear.comp
    (Matrix.toLinAlgEquiv (EuclideanSpace.basisFun ι ℂ).toBasis).toAlgHom
  map_star' A := by
    change (Matrix.toEuclideanLin A.conjTranspose).toContinuousLinearMap =
      star (Matrix.toEuclideanLin A).toContinuousLinearMap
    rw [Matrix.toEuclideanLin_conjTranspose_eq_adjoint,
      LinearMap.adjoint_toContinuousLinearMap, ContinuousLinearMap.star_eq_adjoint]

theorem euclideanMatrixStarAction_injective (ι : Type*) [Fintype ι] [DecidableEq ι] :
    Function.Injective (euclideanMatrixStarAction ι) := by
  intro a b h
  apply (Matrix.toLinAlgEquiv (EuclideanSpace.basisFun ι ℂ).toBasis).injective
  apply LinearMap.ext
  intro x
  exact congrArg (fun f : EuclideanSpace ℂ ι →L[ℂ] EuclideanSpace ℂ ι => f x) h

/-- Block diagonal inclusion, preserving the matrix adjoint. -/
def pairMatrixInclusion (n : ℕ) :
    Blocks n →⋆ₐ[ℂ] Matrix (Fin n ⊕ Fin n) (Fin n ⊕ Fin n) ℂ where
  toFun p := Matrix.fromBlocks p.1 0 0 p.2
  map_one' := by ext i j; cases i <;> cases j <;> simp [Matrix.fromBlocks, Matrix.one_apply]
  map_mul' a b := by simp [Matrix.fromBlocks_multiply]
  map_zero' := by ext i j; cases i <;> cases j <;> simp [Matrix.fromBlocks]
  map_add' a b := by ext i j; cases i <;> cases j <;> simp [Matrix.fromBlocks]
  commutes' r := by
    ext i j; cases i <;> cases j <;>
      simp [Matrix.fromBlocks, Matrix.algebraMap_matrix_apply]
  map_star' a := by
    change Matrix.fromBlocks a.1.conjTranspose 0 0 a.2.conjTranspose =
      (Matrix.fromBlocks a.1 0 0 a.2).conjTranspose
    simp [Matrix.fromBlocks_conjTranspose]

theorem pairMatrixInclusion_injective (n : ℕ) : Function.Injective (pairMatrixInclusion n) := by
  intro a b h
  apply Prod.ext
  · ext i j
    have h' := congrArg (fun m : Matrix (Fin n ⊕ Fin n) (Fin n ⊕ Fin n) ℂ =>
      m (Sum.inl i) (Sum.inl j)) h
    simpa [pairMatrixInclusion, Matrix.fromBlocks] using h'
  · ext i j
    have h' := congrArg (fun m : Matrix (Fin n ⊕ Fin n) (Fin n ⊕ Fin n) ℂ =>
      m (Sum.inr i) (Sum.inr j)) h
    simpa [pairMatrixInclusion, Matrix.fromBlocks] using h'

def standardPairStarAction (n : ℕ) :
    Blocks n →⋆ₐ[ℂ] (EuclideanSpace ℂ (Fin n ⊕ Fin n) →L[ℂ]
      EuclideanSpace ℂ (Fin n ⊕ Fin n)) :=
  (euclideanMatrixStarAction (Fin n ⊕ Fin n)).comp (pairMatrixInclusion n)

theorem standardPairStarAction_injective (n : ℕ) :
    Function.Injective (standardPairStarAction n) :=
  (euclideanMatrixStarAction_injective _).comp (pairMatrixInclusion_injective n)

theorem standardPairStarAction_attains (n : ℕ) :
    Function.Injective (standardPairStarAction n) ∧
      Module.finrank ℂ (EuclideanSpace ℂ (Fin n ⊕ Fin n)) = 2 * n := by
  refine ⟨standardPairStarAction_injective n, ?_⟩
  simp [finrank_euclideanSpace]
  omega

/-- The abstract two-eight-block case has a faithful sixteen-dimensional witness. -/
theorem standardPairStarAction_eight_attains :
    Function.Injective (standardPairStarAction 8) ∧
      Module.finrank ℂ (EuclideanSpace ℂ (Fin 8 ⊕ Fin 8)) = 16 := by
  simpa using standardPairStarAction_attains 8

/-- Dropping the second block preserves the star-algebra laws but loses faithfulness. -/
def firstBlockStarAction (n : ℕ) :
    Blocks n →⋆ₐ[ℂ] (EuclideanSpace ℂ (Fin n) →L[ℂ] EuclideanSpace ℂ (Fin n)) :=
  (euclideanMatrixStarAction (Fin n)).comp (StarAlgHom.fst ℂ _ _)

theorem firstBlockStarAction_not_injective {n : ℕ} (hn : 0 < n) :
    ¬ Function.Injective (firstBlockStarAction n) := by
  intro h
  let i : Fin n := ⟨0, hn⟩
  have heq : firstBlockStarAction n (blockUnit true i i) = firstBlockStarAction n 0 := by
    simp [firstBlockStarAction, blockUnit]
  exact blockUnit_ne_zero true i (h heq)

/-- A one-block eight-dimensional unital star action is the negative control. -/
theorem firstBlockStarAction_eight_control :
    ¬ Function.Injective (firstBlockStarAction 8) ∧
      Module.finrank ℂ (EuclideanSpace ℂ (Fin 8)) = 8 := by
  refine ⟨firstBlockStarAction_not_injective (by decide), ?_⟩
  simp [finrank_euclideanSpace]

end
end D0.Algebra.FaithfulMatrixPairStarWitness
