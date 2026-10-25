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

end D0.Algebra
