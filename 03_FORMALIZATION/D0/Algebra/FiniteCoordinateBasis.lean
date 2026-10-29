import Mathlib.LinearAlgebra.Pi

/-!
# Finite coordinate basis expansions

This module owns basis expansion facts for finite function spaces. It is
independent of any choice of pairing or operator.
-/

namespace D0.Algebra

open Finset

variable {ι K : Type*} [Fintype ι] [DecidableEq ι] [Semiring K]

/-- Every finite coordinate vector is the sum of its coordinates times the
corresponding standard basis vectors. -/
theorem finiteCoordinate_eq_sum_single (x : ι → K) :
    x = ∑ i, x i • Pi.single i (1 : K) := by
  funext j
  simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
  rw [Finset.sum_eq_single j]
  · simp
  · intro i hi hij
    simp [hij]
  · simp

/-- Each coordinate of a finite linear-map image is the corresponding sum
over the images of the standard basis vectors. -/
theorem finiteLinearMap_apply_eq_sum_single
    (A : (ι → K) →ₗ[K] (ι → K)) (x : ι → K) (j : ι) :
    A x j = ∑ i, x i * A (Pi.single i (1 : K)) j := by
  have hExpand : A x = ∑ i, x i • A (Pi.single i (1 : K)) := by
    calc
      A x = A (∑ i, x i • Pi.single i (1 : K)) :=
        congrArg A (finiteCoordinate_eq_sum_single x)
      _ = ∑ i, x i • A (Pi.single i (1 : K)) := by simp
  rw [hExpand]
  simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul]

end D0.Algebra
