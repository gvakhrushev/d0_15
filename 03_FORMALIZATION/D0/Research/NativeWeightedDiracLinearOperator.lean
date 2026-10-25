import D0.Research.NativeWeightedDiracBoundary
import D0.Geometry.ArchiveHodgeCARDiracSquare
import Mathlib.LinearAlgebra.Matrix.ToLin

/-! A reusable typed linear-map and coordinate-matrix interface for the
caller-weighted Hodge--Dirac operator on the existing finite cochain carrier.
The supplied equivalence remains an explicit parameter; this module selects
no weight, pairing, or physical realization. -/
namespace D0.Research.NativeWeightedDiracLinearOperator
open D0.Geometry D0.Research.NativeWeightedDiracBoundary
noncomputable section

/-- The weighted codifferential as a typed linear map, obtained by conjugating
the owned Hodge/CAR codifferential by the caller-supplied linear equivalence. -/
def weightedCodiffLinear (N : ℕ)
    (W : ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N) :
    ArchiveCochain N →ₗ[ℝ] ArchiveCochain N :=
  W.symm.toLinearMap.comp ((hodgeCodifferentialₗ N).comp W.toLinearMap)

@[simp] theorem weightedCodiffLinear_apply (N : ℕ)
    (W : ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N) (ψ : ArchiveCochain N) :
    weightedCodiffLinear N W ψ = weightedCodiff N W ψ := rfl

/-- The caller-weighted Hodge--Dirac operator as a typed linear map on the
same site×Fock cochain coordinates. -/
def weightedDiracLinear (N : ℕ)
    (W : ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N) :
    ArchiveCochain N →ₗ[ℝ] ArchiveCochain N :=
  dForwardₗ N + weightedCodiffLinear N W

@[simp] theorem weightedDiracLinear_apply (N : ℕ)
    (W : ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N) (ψ : ArchiveCochain N) :
    weightedDiracLinear N W ψ = weightedDirac N W ψ := rfl

/-- The matrix of the weighted Hodge--Dirac operator in the actual
`ArchiveCochainBasis` coordinates, with no change of basis or carrier. -/
noncomputable def weightedDiracMatrix (N : ℕ)
    (W : ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N) :
    Matrix (ArchiveCochainBasis N) (ArchiveCochainBasis N) ℝ :=
  LinearMap.toMatrix' (weightedDiracLinear N W)

/-- Matrix multiplication by the registered matrix is exactly the original
function-level weighted-operator action. -/
theorem weightedDiracMatrix_mulVec (N : ℕ)
    (W : ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N) (ψ : ArchiveCochain N) :
    Matrix.mulVec (weightedDiracMatrix N W) ψ = weightedDirac N W ψ := by
  rw [weightedDiracMatrix, LinearMap.toMatrix'_mulVec, weightedDiracLinear_apply]

/-- At the identity transport, the generic weighted operator is the
repository's existing real Hodge/CAR operator as a typed linear map. -/
theorem weightedCodiffLinear_identity_eq_hodgeCodifferential (N : ℕ) :
    weightedCodiffLinear N (LinearEquiv.refl ℝ (ArchiveCochain N)) =
      hodgeCodifferentialₗ N := by
  ext ψ
  simp [weightedCodiffLinear, hodgeCodifferentialₗ]

theorem weightedDiracLinear_identity_eq_hodgeCarDirac (N : ℕ) :
    weightedDiracLinear N (LinearEquiv.refl ℝ (ArchiveCochain N)) =
      hodgeCarDiracₗ N := by
  change dForwardₗ N +
      weightedCodiffLinear N (LinearEquiv.refl ℝ (ArchiveCochain N)) =
    hodgeCarDiracₗ N
  rw [weightedCodiffLinear_identity_eq_hodgeCodifferential]
  calc
    dForwardₗ N + hodgeCodifferentialₗ N =
        dForwardₗ N + D0.Algebra.finiteHermitianAdjoint (dForwardₗ N) := by
          rw [finiteHermitianAdjoint_dForwardₗ_eq_hodgeCodifferentialₗ]
    _ = D0.Algebra.finiteHermitianHodgeDirac (dForwardₗ N) := rfl
    _ = hodgeCarDiracₗ N :=
      (hodgeCarDiracₗ_eq_finiteHermitianHodgeDirac N).symm

/-- The coordinate matrix of the existing Hodge/CAR operator acts on the
actual site×Fock cochain vector by its registered function-level formula. -/
theorem hodgeCarDiracMatrix_mulVec (N : ℕ) (ψ : ArchiveCochain N) :
    Matrix.mulVec
        (weightedDiracMatrix N (LinearEquiv.refl ℝ (ArchiveCochain N))) ψ =
      hodgeCarDirac N ψ := by
  rw [weightedDiracMatrix_mulVec, ← weightedDiracLinear_apply,
    weightedDiracLinear_identity_eq_hodgeCarDirac, hodgeCarDiracₗ_apply]

#print axioms weightedCodiffLinear_apply
#print axioms weightedDiracLinear_apply
#print axioms weightedDiracMatrix_mulVec
#print axioms weightedCodiffLinear_identity_eq_hodgeCodifferential
#print axioms weightedDiracLinear_identity_eq_hodgeCarDirac
#print axioms hodgeCarDiracMatrix_mulVec
end
end D0.Research.NativeWeightedDiracLinearOperator
