import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Tactic

/-!
# D0.Geometry.A4DMetricNullHessianComplex

Exact Lean owner for the metric-null Hessian complex of merged #270/#292.
The response symbol C(d) is reconstructed from the accepted coefficient
ledger, independently of any orbit census.

Firewall: this is a finite linear symbol theorem. It does not assert a
nonlinear diffeomorphism gauge symmetry.
-/

namespace D0.Geometry.A4DMetricNullHessianComplex

open BigOperators Matrix

/-- Repository symmetric-slot order:
(00),(01),(02),(03),(11),(12),(13),(22),(23),(33). -/
def symPair : Fin 10 → Fin 4 × Fin 4
  | ⟨0, _⟩ => (0,0) | ⟨1, _⟩ => (0,1) | ⟨2, _⟩ => (0,2)
  | ⟨3, _⟩ => (0,3) | ⟨4, _⟩ => (1,1) | ⟨5, _⟩ => (1,2)
  | ⟨6, _⟩ => (1,3) | ⟨7, _⟩ => (2,2) | ⟨8, _⟩ => (2,3)
  | ⟨9, _⟩ => (3,3)

/-- Exact rational coefficient ledger C_r from merged #292. -/
def cCoeff (r : Fin 4) (i : Fin 24) (j : Fin 10) : ℚ :=
  match i.val, j.val, r.val with
  | 0,5,2 => -1/2 | 0,6,3 => -1/2 | 0,7,1 => 1/2 | 0,9,1 => 1/2
  | 1,4,2 => 1/2 | 1,5,1 => -1/2 | 1,8,3 => -1/2 | 1,9,2 => 1/2
  | 2,4,3 => 1/2 | 2,6,1 => -1/2 | 2,7,3 => 1/2 | 2,8,2 => -1/2
  | 3,1,2 => 1/2 | 3,2,1 => -1/2
  | 4,1,3 => 1/2 | 4,3,1 => -1/2
  | 5,2,3 => 1/2 | 5,3,2 => -1/2
  | 6,2,2 => 1/2 | 6,3,3 => 1/2 | 6,7,0 => -1/2 | 6,9,0 => -1/2
  | 7,1,2 => -1/2 | 7,5,0 => 1/2
  | 8,1,3 => -1/2 | 8,6,0 => 1/2
  | 9,0,2 => -1/2 | 9,2,0 => 1/2 | 9,8,3 => -1/2 | 9,9,2 => 1/2
  | 10,0,3 => -1/2 | 10,3,0 => 1/2 | 10,7,3 => 1/2 | 10,8,2 => -1/2
  | 11,5,3 => -1/2 | 11,6,2 => 1/2
  | 12,2,1 => -1/2 | 12,5,0 => 1/2
  | 13,1,1 => 1/2 | 13,3,3 => 1/2 | 13,4,0 => -1/2 | 13,9,0 => -1/2
  | 14,2,3 => -1/2 | 14,8,0 => 1/2
  | 15,0,1 => 1/2 | 15,1,0 => -1/2 | 15,6,3 => 1/2 | 15,9,1 => -1/2
  | 16,5,3 => -1/2 | 16,8,1 => 1/2
  | 17,0,3 => -1/2 | 17,3,0 => 1/2 | 17,4,3 => 1/2 | 17,6,1 => -1/2
  | 18,3,1 => -1/2 | 18,6,0 => 1/2
  | 19,3,2 => -1/2 | 19,8,0 => 1/2
  | 20,1,1 => 1/2 | 20,2,2 => 1/2 | 20,4,0 => -1/2 | 20,7,0 => -1/2
  | 21,6,2 => -1/2 | 21,8,1 => 1/2
  | 22,0,1 => 1/2 | 22,1,0 => -1/2 | 22,5,2 => 1/2 | 22,7,1 => -1/2
  | 23,0,2 => 1/2 | 23,2,0 => -1/2 | 23,4,2 => -1/2 | 23,5,1 => 1/2
  | _,_,_ => 0

/-- The exact 24 x 10 response symbol C(d)=sum_r d_r C_r. -/
def C (d : Fin 4 → ℚ) : Matrix (Fin 24) (Fin 10) ℚ :=
  fun i j => ∑ r, d r * cCoeff r i j

/-- Symmetric-slot vectorization of d d^T. -/
def qNull (d : Fin 4 → ℚ) : Fin 10 → ℚ :=
  fun j =>
    let p := symPair j
    d p.1 * d p.2

/-- Exact finite Hessian compatibility C(d) vec_sym(d d^T)=0. -/
theorem C_mulVec_qNull (d : Fin 4 → ℚ) :
    (C d).mulVec (qNull d) = 0 := by
  funext i
  fin_cases i <;>
    simp [C, qNull, symPair, cCoeff, Matrix.mulVec, dotProduct,
      Fin.sum_univ_succ] <;> ring

/-- Scalar multiples of the Hessian line lie in the response kernel. -/
theorem C_mulVec_qNull_smul (d : Fin 4 → ℚ) (a : ℚ) :
    (C d).mulVec (fun j => a * qNull d j) = 0 := by
  funext i
  simp only [Matrix.mulVec, dotProduct]
  rw [← Finset.mul_sum]
  simpa [Matrix.mulVec, dotProduct] using congrFun (C_mulVec_qNull d) i

/-- At the trivial character difference the response symbol vanishes. -/
theorem C_zero : C (fun _ => 0) = 0 := by
  ext i j
  simp [C]

end D0.Geometry.A4DMetricNullHessianComplex
