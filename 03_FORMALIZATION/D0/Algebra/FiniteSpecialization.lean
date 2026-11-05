import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.LinearIndependent.Defs

/- A nonzero finite specialization is an exact certificate over any other
injective specialization of the same coefficient ring. This theorem does not
compute the determinant, identify a coefficient matrix, or assert one exists. -/
namespace D0.Algebra.FiniteSpecialization

variable {R F K ι : Type*} [CommRing R] [CommRing F] [CommRing K]
variable [Fintype ι] [DecidableEq ι]

theorem mapped_det_ne_zero (reduce : R →+* F) (embed : R →+* K)
    (hembed : Function.Injective embed) (M : Matrix ι ι R)
    (hmod : (reduce.mapMatrix M).det ≠ 0) : (embed.mapMatrix M).det ≠ 0 := by
  have hM : M.det ≠ 0 := by
    intro hz
    apply hmod
    rw [← reduce.map_det, hz, map_zero]
  rw [← embed.map_det]
  intro hz
  apply hM
  apply hembed
  simpa only [map_zero] using hz

theorem mapped_rows_independent [IsDomain K] (reduce : R →+* F) (embed : R →+* K)
    (hembed : Function.Injective embed) (M : Matrix ι ι R)
    (hmod : (reduce.mapMatrix M).det ≠ 0) :
    LinearIndependent K (fun i => (embed.mapMatrix M) i) :=
  Matrix.linearIndependent_rows_of_det_ne_zero
    (mapped_det_ne_zero reduce embed hembed M hmod)

end D0.Algebra.FiniteSpecialization
