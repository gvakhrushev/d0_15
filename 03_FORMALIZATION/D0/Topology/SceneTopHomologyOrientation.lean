import D0.Topology.GenericTripartiteFiniteTypeTransport
import Mathlib.LinearAlgebra.Matrix.Kronecker
import Mathlib.Algebra.Ring.Int.Units
import Mathlib.Tactic

/-!
# Scene top-homology orientation

The complete tripartite scene has

`H₂(K(p+1,q+1,r+1); R) ≃ R^(Fin p × Fin q × Fin r)`.

This file equips that actual boundary kernel with the action induced by
within-zone permutations.  In the explicit octahedral basis, its matrix is the
Kronecker product of the three reduced permutation matrices.  For the source
scene `(p,q,r)=(8,10,12)`, all three complementary multiplicities are even, so
every automorphism has determinant one on integral top homology.
-/

namespace D0.Topology.SceneTopHomologyOrientation

open scoped Kronecker
open Matrix
open D0.Topology.GenericTripartiteHomology
open D0.Topology.GenericTripartiteTopHomologyRing
open D0.Topology.GenericTripartiteFiniteTypeTransport

variable (R : Type) [CommRing R]
variable {p q r : ℕ}

/-- The natural top boundary kernel on three canonical finite zones. -/
abbrev FinTopKernel (p q r : ℕ) :=
  LinearMap.ker
    (typeBoundary2 R
      (A := Fin (p + 1)) (B := Fin (q + 1)) (C := Fin (r + 1))).mulVecLin

/-- Top-homology coordinates for the identity enumeration of the zones. -/
noncomputable def canonicalCoordinateEquiv :
    FinTopKernel R p q r ≃ₗ[R] (TopCycleIndex p q r → R) :=
  typeTopCoordinateEquiv R
    (Equiv.refl (Fin (p + 1)))
    (Equiv.refl (Fin (q + 1)))
    (Equiv.refl (Fin (r + 1)))

/-- Top-homology coordinates after relabelling each zone. -/
noncomputable def permutedCoordinateEquiv
    (σA : Equiv.Perm (Fin (p + 1)))
    (σB : Equiv.Perm (Fin (q + 1)))
    (σC : Equiv.Perm (Fin (r + 1))) :
    FinTopKernel R p q r ≃ₗ[R] (TopCycleIndex p q r → R) :=
  typeTopCoordinateEquiv R σA σB σC

/-- The genuine chain-reindexing action on the top boundary kernel.  It is the
transition from the relabelled finite-type transport back to the identity
enumeration. -/
noncomputable def topHomologyAction
    (σA : Equiv.Perm (Fin (p + 1)))
    (σB : Equiv.Perm (Fin (q + 1)))
    (σC : Equiv.Perm (Fin (r + 1))) :
    FinTopKernel R p q r ≃ₗ[R] FinTopKernel R p q r :=
  (permutedCoordinateEquiv R σA σB σC).trans
    (canonicalCoordinateEquiv R).symm

/-- The action above is literally pullback of a top chain along the three
within-zone permutations. -/
@[simp] theorem topHomologyAction_coe
    (σA : Equiv.Perm (Fin (p + 1)))
    (σB : Equiv.Perm (Fin (q + 1)))
    (σC : Equiv.Perm (Fin (r + 1)))
    (z : FinTopKernel R p q r)
    (a : Fin (p + 1)) (b : Fin (q + 1)) (c : Fin (r + 1)) :
    ((topHomologyAction R σA σB σC z :
        TypeTriangle (Fin (p + 1)) (Fin (q + 1)) (Fin (r + 1)) → R)
      (a, b, c)) =
      (z :
        TypeTriangle (Fin (p + 1)) (Fin (q + 1)) (Fin (r + 1)) → R)
        (σA.symm a, σB.symm b, σC.symm c) := by
  simp [topHomologyAction, permutedCoordinateEquiv, canonicalCoordinateEquiv,
    typeTopCoordinateEquiv, topKernelEquivCanonical,
    triangleFunctionsEquivCanonical, typeTriangleEquivCanonical]

/-- Matrix-coordinate form of `topHomologyAction` in the canonical octahedral
top-cycle basis. -/
noncomputable def topHomologyCoordinateAction
    (σA : Equiv.Perm (Fin (p + 1)))
    (σB : Equiv.Perm (Fin (q + 1)))
    (σC : Equiv.Perm (Fin (r + 1))) :
    (TopCycleIndex p q r → R) ≃ₗ[R] (TopCycleIndex p q r → R) :=
  (canonicalCoordinateEquiv R).symm.trans
    ((topHomologyAction R σA σB σC).trans (canonicalCoordinateEquiv R))

/-- The augmentation-zero module on one finite zone. -/
def reducedZeroSubmodule (p : ℕ) : Submodule R (Fin (p + 1) → R) where
  carrier := {x | ∑ i, x i = 0}
  zero_mem' := by simp
  add_mem' := by
    intro a b hx hy
    change (∑ i, (a + b) i) = 0
    change (∑ i, a i) = 0 at hx
    change (∑ i, b i) = 0 at hy
    simp [Pi.add_apply, Finset.sum_add_distrib, hx, hy]
  smul_mem' := by
    intro c x hx
    change (∑ i, (c • x) i) = 0
    change (∑ i, x i) = 0 at hx
    simp only [Pi.smul_apply, smul_eq_mul, ← Finset.mul_sum, hx, mul_zero]

abbrev ReducedZero (p : ℕ) := reducedZeroSubmodule R p

/-- Root-difference coordinates identify the augmentation-zero module with
`R^(Fin p)`. -/
noncomputable def reducedCoordinateEquiv :
    ReducedZero R p ≃ₗ[R] (Fin p → R) where
  toFun z i := z.1 i.succ
  invFun g :=
    ⟨Fin.cases (-∑ i, g i) g, by
      change
        (∑ i : Fin (p + 1),
          (Fin.cases (-∑ j : Fin p, g j) (fun j => g j) i : R)) = 0
      rw [Fin.sum_univ_succ]
      simp⟩
  left_inv z := by
    apply Subtype.ext
    funext x
    refine Fin.cases ?_ (fun _ => rfl) x
    have hz := z.2
    change (∑ i, z.1 i) = 0 at hz
    rw [Fin.sum_univ_succ] at hz
    dsimp
    exact (eq_neg_of_add_eq_zero_left hz).symm
  right_inv _ := rfl
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

/-- Pullback of an augmentation-zero vector along a zone permutation. -/
noncomputable def reducedAction
    (σ : Equiv.Perm (Fin (p + 1))) :
    ReducedZero R p ≃ₗ[R] ReducedZero R p where
  toFun z :=
    ⟨fun i => z.1 (σ.symm i), by
      change (∑ i, z.1 (σ.symm i)) = 0
      rw [Equiv.sum_comp σ.symm z.1]
      exact z.2⟩
  invFun z :=
    ⟨fun i => z.1 (σ i), by
      change (∑ i, z.1 (σ i)) = 0
      rw [Equiv.sum_comp σ z.1]
      exact z.2⟩
  left_inv z := by
    apply Subtype.ext
    funext i
    simp
  right_inv z := by
    apply Subtype.ext
    funext i
    simp
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

/-- The one-zone action written in root-difference coordinates. -/
noncomputable def reducedCoordinateAction
    (σ : Equiv.Perm (Fin (p + 1))) :
    (Fin p → R) ≃ₗ[R] (Fin p → R) :=
  (reducedCoordinateEquiv R).symm.trans
    ((reducedAction R σ).trans (reducedCoordinateEquiv R))

/-- Matrix of a zone permutation on the root-difference basis of reduced
zero-homology. -/
def reducedPermutationMatrix
    (σ : Equiv.Perm (Fin (p + 1))) : Matrix (Fin p) (Fin p) R :=
  fun i j => rootDifferenceR R j (σ.symm i.succ)

/-- The concrete reduced permutation matrix is the matrix of the actual
augmentation-zero action. -/
theorem reducedCoordinateAction_toMatrix
    (σ : Equiv.Perm (Fin (p + 1))) :
    LinearMap.toMatrix
        (Pi.basisFun R (Fin p))
        (Pi.basisFun R (Fin p))
        (reducedCoordinateAction R σ).toLinearMap =
      reducedPermutationMatrix R σ := by
  ext i j
  simp [reducedCoordinateAction, reducedAction, reducedCoordinateEquiv,
    reducedPermutationMatrix, rootDifferenceR]
  generalize hx : σ.symm i.succ = x
  refine Fin.cases ?_ (fun k => ?_) x
  · have hne : (0 : Fin (p + 1)) ≠ j.succ := (Fin.succ_ne_zero j).symm
    simp [hne]
  · simp [Pi.single_apply, Fin.succ_inj]

/-- The predicted tensor-product matrix on top homology. -/
def topHomologyTensorMatrix
    (σA : Equiv.Perm (Fin (p + 1)))
    (σB : Equiv.Perm (Fin (q + 1)))
    (σC : Equiv.Perm (Fin (r + 1))) :
    Matrix (TopCycleIndex p q r) (TopCycleIndex p q r) R :=
  reducedPermutationMatrix R σA ⊗ₖ
    (reducedPermutationMatrix R σB ⊗ₖ reducedPermutationMatrix R σC)

/-- The matrix of the actual kernel action in canonical top-cycle
coordinates. -/
noncomputable def topHomologyActionMatrix
    (σA : Equiv.Perm (Fin (p + 1)))
    (σB : Equiv.Perm (Fin (q + 1)))
    (σC : Equiv.Perm (Fin (r + 1))) :
    Matrix (TopCycleIndex p q r) (TopCycleIndex p q r) R :=
  LinearMap.toMatrix
    (Pi.basisFun R (TopCycleIndex p q r))
    (Pi.basisFun R (TopCycleIndex p q r))
    (topHomologyCoordinateAction R σA σB σC).toLinearMap

/-- The induced action on top homology is the tensor product of the three
reduced permutation actions. -/
theorem topHomologyActionMatrix_eq_tensor
    (σA : Equiv.Perm (Fin (p + 1)))
    (σB : Equiv.Perm (Fin (q + 1)))
    (σC : Equiv.Perm (Fin (r + 1))) :
    topHomologyActionMatrix R σA σB σC =
      topHomologyTensorMatrix R σA σB σC := by
  ext i j
  rcases i with ⟨ia, ib, ic⟩
  rcases j with ⟨ja, jb, jc⟩
  simp [topHomologyActionMatrix, topHomologyCoordinateAction,
    topHomologyTensorMatrix, reducedPermutationMatrix,
    canonicalCoordinateEquiv,
    typeTopCoordinateEquiv, topKernelEquivCanonical,
    topCoordinateEquivR, topSynthesisR, topCoordinateR,
    topCoordinateAtR, triangleFunctionsEquivCanonical,
    typeTriangleEquivCanonical, topCycleR, topCycleVecR]
  ring

/-- Determinant formula for the three-factor action. -/
theorem topHomologyActionMatrix_det
    (σA : Equiv.Perm (Fin (p + 1)))
    (σB : Equiv.Perm (Fin (q + 1)))
    (σC : Equiv.Perm (Fin (r + 1))) :
    (topHomologyActionMatrix R σA σB σC).det =
      (reducedPermutationMatrix R σA).det ^ (q * r) *
      (reducedPermutationMatrix R σB).det ^ (p * r) *
      (reducedPermutationMatrix R σC).det ^ (p * q) := by
  rw [topHomologyActionMatrix_eq_tensor]
  simp only [topHomologyTensorMatrix, Matrix.det_kronecker,
    Fintype.card_prod, Fintype.card_fin]
  rw [mul_pow, pow_mul, pow_mul]
  ring

/-- Every integral reduced permutation determinant is a unit. -/
theorem reducedPermutationMatrix_det_isUnit
    (σ : Equiv.Perm (Fin (p + 1))) :
    IsUnit (reducedPermutationMatrix ℤ σ).det := by
  rw [← reducedCoordinateAction_toMatrix]
  exact LinearEquiv.isUnit_det
    (reducedCoordinateAction ℤ σ)
    (Pi.basisFun ℤ (Fin p))
    (Pi.basisFun ℤ (Fin p))

private theorem int_isUnit_pow_eq_one_of_even
    {x : ℤ} (hx : IsUnit x) {n : ℕ} (hn : Even n) :
    x ^ n = 1 := by
  rcases hx with ⟨u, rfl⟩
  rcases Int.units_eq_one_or u with rfl | rfl
  · simp
  · simpa using hn.neg_one_pow (α := ℤ)

/-- **Source-scene orientation theorem.** Every within-zone automorphism of
`K(9,11,13)` acts through determinant `+1` on the integral `960`-dimensional
top-homology lattice. -/
theorem scene_topHomologyAction_det_one
    (σ9 : Equiv.Perm (Fin 9))
    (σ11 : Equiv.Perm (Fin 11))
    (σ13 : Equiv.Perm (Fin 13)) :
    (topHomologyActionMatrix ℤ
      (p := 8) (q := 10) (r := 12) σ9 σ11 σ13).det = 1 := by
  rw [topHomologyActionMatrix_det]
  have hA := reducedPermutationMatrix_det_isUnit (p := 8) σ9
  have hB := reducedPermutationMatrix_det_isUnit (p := 10) σ11
  have hC := reducedPermutationMatrix_det_isUnit (p := 12) σ13
  rw [int_isUnit_pow_eq_one_of_even hA (by decide : Even (10 * 12))]
  rw [int_isUnit_pow_eq_one_of_even hB (by decide : Even (8 * 12))]
  rw [int_isUnit_pow_eq_one_of_even hC (by decide : Even (8 * 10))]
  norm_num

/-- Negative control: for `K(2,2,2)` the same construction detects a genuine
orientation reversal.  Swapping the two vertices in one zone acts by
determinant `-1` on its rank-one top homology. -/
theorem octahedral_topHomology_swap_det_neg_one :
    (topHomologyActionMatrix ℤ
      (p := 1) (q := 1) (r := 1)
      (Equiv.swap (0 : Fin 2) (1 : Fin 2))
      (Equiv.refl (Fin 2)) (Equiv.refl (Fin 2))).det = -1 := by
  rw [topHomologyActionMatrix_det]
  norm_num [reducedPermutationMatrix, rootDifferenceR, Matrix.det_fin_one]

end D0.Topology.SceneTopHomologyOrientation
