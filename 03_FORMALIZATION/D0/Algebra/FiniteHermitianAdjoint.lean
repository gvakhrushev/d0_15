import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Finite Hermitian adjoints

This module owns the standard finite-coordinate sesquilinear pairing and the
adjoint of an arbitrary linear operator for that pairing. It is algebraic:
it selects neither a weighted metric nor a physical inner product.
-/

namespace D0.Algebra

open Finset

section

variable {ι K : Type*} [Fintype ι] [DecidableEq ι] [Field K] [StarRing K]

/-- The standard finite-coordinate Hermitian pairing. -/
def finiteHermitianPairing (x y : ι → K) : K :=
  ∑ i, star (x i) * y i

omit [DecidableEq ι] in
/-- Conjugate symmetry of the standard finite-coordinate pairing. -/
theorem finiteHermitianPairing_conj (x y : ι → K) :
    star (finiteHermitianPairing x y) = finiteHermitianPairing y x := by
  simp [finiteHermitianPairing, star_sum, star_mul]

/-- The coordinate formula for the adjoint of a finite linear operator under
the standard Hermitian pairing. -/
def finiteHermitianAdjoint
    (A : (ι → K) →ₗ[K] (ι → K)) : (ι → K) →ₗ[K] (ι → K) where
  toFun y i := ∑ j, star (A (Pi.single i 1) j) * y j
  map_add' y z := by
    funext i
    simp [Finset.sum_add_distrib, mul_add]
  map_smul' c y := by
    funext i
    simp [Pi.smul_apply, smul_eq_mul, Finset.mul_sum, mul_assoc,
      mul_comm]

omit [StarRing K] in
private theorem pi_eq_sum_single (x : ι → K) :
    x = ∑ i, x i • Pi.single i (1 : K) := by
  funext j
  simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
  rw [Finset.sum_eq_single j]
  · simp
  · intro i hi hij
    simp [hij]
  · simp

/-- Pairing against a coordinate basis vector reads that coordinate. This is
the nondegeneracy witness used to characterize the adjoint uniquely. -/
theorem finiteHermitianPairing_single_left (i : ι) (z : ι → K) :
    finiteHermitianPairing (Pi.single i (1 : K)) z = z i := by
  classical
  unfold finiteHermitianPairing
  rw [Finset.sum_eq_single i]
  · simp
  · intro j hj hji
    simp [hji]
  · intro hi
    exact (hi (Finset.mem_univ i)).elim

/-- Every finite linear operator satisfies the defining Hermitian-adjoint
identity for the standard coordinate pairing. -/
theorem finiteHermitianPairing_adjoint
    (A : (ι → K) →ₗ[K] (ι → K)) (x y : ι → K) :
    finiteHermitianPairing (A x) y =
      finiteHermitianPairing x (finiteHermitianAdjoint A y) := by
  have hAx : A x = ∑ i, x i • A (Pi.single i (1 : K)) := by
    calc
      A x = A (∑ i, x i • Pi.single i (1 : K)) :=
        congrArg A (pi_eq_sum_single x)
      _ = ∑ i, x i • A (Pi.single i (1 : K)) := by simp
  have hAx_apply (j : ι) :
      A x j = ∑ i, x i * A (Pi.single i (1 : K)) j := by
    rw [hAx]
    simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
  change (∑ j, star (A x j) * y j) =
    ∑ i, star (x i) * (finiteHermitianAdjoint A y) i
  rw [show (∑ i, star (x i) * (finiteHermitianAdjoint A y) i) =
      ∑ i, star (x i) *
        (∑ j, star (A (Pi.single i (1 : K)) j) * y j) by rfl]
  rw [show (∑ j, star (A x j) * y j) =
      ∑ j, star (∑ i, x i * A (Pi.single i (1 : K)) j) * y j by
        apply Finset.sum_congr rfl
        intro j hj
        rw [hAx_apply]]
  calc
    (∑ j, star (∑ i, x i * A (Pi.single i (1 : K)) j) * y j) =
        ∑ j, ∑ i, star (x i) *
          (star (A (Pi.single i (1 : K)) j) * y j) := by
            apply Finset.sum_congr rfl
            intro j hj
            simp only [star_sum, star_mul, Finset.sum_mul]
            apply Finset.sum_congr rfl
            intro i hi
            ring
    _ = ∑ i, ∑ j, star (x i) *
          (star (A (Pi.single i (1 : K)) j) * y j) := Finset.sum_comm
    _ = ∑ i, star (x i) *
          (∑ j, star (A (Pi.single i (1 : K)) j) * y j) := by
            apply Finset.sum_congr rfl
            intro i hi
            rw [← Finset.mul_sum]

/-- The equivalent right-operator form of the Hermitian-adjoint identity. -/
theorem finiteHermitianPairing_adjoint_right
    (A : (ι → K) →ₗ[K] (ι → K)) (x y : ι → K) :
    finiteHermitianPairing (finiteHermitianAdjoint A x) y =
      finiteHermitianPairing x (A y) := by
  have h := finiteHermitianPairing_adjoint A y x
  calc
    finiteHermitianPairing (finiteHermitianAdjoint A x) y =
        star (finiteHermitianPairing y (finiteHermitianAdjoint A x)) :=
      (finiteHermitianPairing_conj y (finiteHermitianAdjoint A x)).symm
    _ = star (finiteHermitianPairing (A y) x) := congrArg star h.symm
    _ = finiteHermitianPairing x (A y) := finiteHermitianPairing_conj (A y) x

omit [DecidableEq ι] in
/-- Additivity of the finite Hermitian pairing in its conjugate-linear
left argument. -/
theorem finiteHermitianPairing_add_left (x y z : ι → K) :
    finiteHermitianPairing (x + y) z =
      finiteHermitianPairing x z + finiteHermitianPairing y z := by
  simp [finiteHermitianPairing, Pi.add_apply, star_add,
    Finset.sum_add_distrib, add_mul]

omit [DecidableEq ι] in
/-- Additivity of the finite Hermitian pairing in its linear right argument. -/
theorem finiteHermitianPairing_add_right (x y z : ι → K) :
    finiteHermitianPairing x (y + z) =
      finiteHermitianPairing x y + finiteHermitianPairing x z := by
  simp [finiteHermitianPairing, Pi.add_apply, Finset.sum_add_distrib, mul_add]

/-- The finite Hermitian Hodge--Dirac operator `A + A†`. -/
noncomputable def finiteHermitianHodgeDirac
    (A : (ι → K) →ₗ[K] (ι → K)) : (ι → K) →ₗ[K] (ι → K) :=
  A + finiteHermitianAdjoint A

/-- The finite Hermitian Hodge--Dirac operator is self-adjoint for the standard
finite-coordinate Hermitian pairing. -/
theorem finiteHermitianHodgeDirac_pairing_self_adjoint
    (A : (ι → K) →ₗ[K] (ι → K)) (x y : ι → K) :
    finiteHermitianPairing (finiteHermitianHodgeDirac A x) y =
      finiteHermitianPairing x (finiteHermitianHodgeDirac A y) := by
  unfold finiteHermitianHodgeDirac
  change finiteHermitianPairing (A x + finiteHermitianAdjoint A x) y =
    finiteHermitianPairing x (A y + finiteHermitianAdjoint A y)
  rw [finiteHermitianPairing_add_left]
  calc
    finiteHermitianPairing (A x) y +
        finiteHermitianPairing (finiteHermitianAdjoint A x) y =
      finiteHermitianPairing x (finiteHermitianAdjoint A y) +
        finiteHermitianPairing x (A y) := by
          rw [finiteHermitianPairing_adjoint A x y,
            finiteHermitianPairing_adjoint_right A x y]
    _ = finiteHermitianPairing x (A y + finiteHermitianAdjoint A y) := by
          rw [finiteHermitianPairing_add_right]
          abel

/-- Nondegeneracy makes the adjoint identity characterize its operator. -/
theorem finiteHermitianAdjoint_unique
    (A B : (ι → K) →ₗ[K] (ι → K))
    (hB : ∀ x y, finiteHermitianPairing (A x) y =
      finiteHermitianPairing x (B y)) :
    finiteHermitianAdjoint A = B := by
  apply LinearMap.ext
  intro y
  funext i
  have hAdj := finiteHermitianPairing_adjoint A (Pi.single i (1 : K)) y
  have hPair := hAdj.symm.trans (hB (Pi.single i (1 : K)) y)
  simpa only [finiteHermitianPairing_single_left] using hPair

/-- The generic finite Hermitian Hodge--Dirac operator is its own typed
Hermitian adjoint, as an operator equality rather than only a pairing law. -/
theorem finiteHermitianAdjoint_finiteHermitianHodgeDirac_eq_self
    (A : (ι → K) →ₗ[K] (ι → K)) :
    finiteHermitianAdjoint (finiteHermitianHodgeDirac A) =
      finiteHermitianHodgeDirac A := by
  apply finiteHermitianAdjoint_unique
  intro x y
  exact finiteHermitianHodgeDirac_pairing_self_adjoint A x y

/-- The Hermitian adjoint reverses composition order. -/
theorem finiteHermitianAdjoint_comp
    (A B : (ι → K) →ₗ[K] (ι → K)) :
    finiteHermitianAdjoint (A.comp B) =
      (finiteHermitianAdjoint B).comp (finiteHermitianAdjoint A) := by
  apply finiteHermitianAdjoint_unique (A.comp B)
  intro x y
  change finiteHermitianPairing (A (B x)) y =
    finiteHermitianPairing x
      (finiteHermitianAdjoint B (finiteHermitianAdjoint A y))
  calc
    finiteHermitianPairing (A (B x)) y =
        finiteHermitianPairing (B x) (finiteHermitianAdjoint A y) :=
      finiteHermitianPairing_adjoint A (B x) y
    _ = finiteHermitianPairing x
        (finiteHermitianAdjoint B (finiteHermitianAdjoint A y)) :=
      finiteHermitianPairing_adjoint B x (finiteHermitianAdjoint A y)

/-- The Hermitian adjoint of the zero operator is zero. -/
theorem finiteHermitianAdjoint_zero :
    finiteHermitianAdjoint (0 : (ι → K) →ₗ[K] (ι → K)) = 0 := by
  ext x i
  simp [finiteHermitianAdjoint]

/-- Nilpotency transfers to the Hermitian adjoint by reversing composition. -/
theorem finiteHermitianAdjoint_comp_self_eq_zero
    (A : (ι → K) →ₗ[K] (ι → K)) (hA : A.comp A = 0) :
    (finiteHermitianAdjoint A).comp (finiteHermitianAdjoint A) = 0 := by
  calc
    (finiteHermitianAdjoint A).comp (finiteHermitianAdjoint A) =
        finiteHermitianAdjoint (A.comp A) :=
      (finiteHermitianAdjoint_comp A A).symm
    _ = finiteHermitianAdjoint 0 := by rw [hA]
    _ = 0 := finiteHermitianAdjoint_zero

/-- If `A² = 0`, the square of the finite Hermitian Hodge--Dirac is the
Hodge anticommutator `A A† + A† A`. -/
theorem finiteHermitianHodgeDirac_square
    (A : (ι → K) →ₗ[K] (ι → K)) (hA : A.comp A = 0) :
    (finiteHermitianHodgeDirac A).comp (finiteHermitianHodgeDirac A) =
      A.comp (finiteHermitianAdjoint A) +
        (finiteHermitianAdjoint A).comp A := by
  have hAdj := finiteHermitianAdjoint_comp_self_eq_zero A hA
  unfold finiteHermitianHodgeDirac
  apply LinearMap.ext
  intro x
  change A (A x + finiteHermitianAdjoint A x) +
      finiteHermitianAdjoint A (A x + finiteHermitianAdjoint A x) =
    A (finiteHermitianAdjoint A x) + finiteHermitianAdjoint A (A x)
  rw [map_add, map_add]
  have hA0 : A (A x) = 0 := by
    have h := congrArg (fun f : (ι → K) →ₗ[K] (ι → K) => f x) hA
    simpa [LinearMap.comp_apply] using h
  have hAdj0 : finiteHermitianAdjoint A (finiteHermitianAdjoint A x) = 0 := by
    have h := congrArg (fun f : (ι → K) →ₗ[K] (ι → K) => f x) hAdj
    simpa [LinearMap.comp_apply] using h
  rw [hA0, hAdj0]
  ext i
  abel

end

end D0.Algebra
