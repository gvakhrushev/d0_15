import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.BigOperators.Fin
import D0.Geometry.ArchiveLaplacianRG

open scoped BigOperators

namespace D0

def rectangularMatrixMul {A B C : Type} [Fintype B]
    (M : Matrix A B ℝ) (N : Matrix B C ℝ) : Matrix A C ℝ :=
  fun i k => ∑ j : B, M i j * N j k

def archiveLiftOperator (n : Nat) :
    Matrix (archivePhaseIndex (n+1)) (archivePhaseIndex n) ℝ :=
  fun i j => if archiveRGPhaseProjection n i = j then 1 else 0

def seamFineTransport (n : Nat) :
    Matrix (archivePhaseIndex (n+1)) (archivePhaseIndex n) ℝ :=
  rectangularMatrixMul (archiveCanonicalLaplacian (n+1)) (archiveLiftOperator n)

def seamLiftedCoarseTransport (n : Nat) :
    Matrix (archivePhaseIndex (n+1)) (archivePhaseIndex n) ℝ :=
  rectangularMatrixMul (archiveLiftOperator n) (archiveCanonicalLaplacian n)

def seamCommutator (n : Nat) :
    Matrix (archivePhaseIndex (n+1)) (archivePhaseIndex n) ℝ :=
  seamFineTransport n - seamLiftedCoarseTransport n

def OperatorTransportFlat (n : Nat) : Prop :=
  seamCommutator n = 0

def archiveRefinementSeam (n : Nat)
    (i : archivePhaseIndex (n+1)) (_j : archivePhaseIndex n) : Prop :=
  i.val = 0 ∨ i.val = n + 2

def ArchiveSeamSupport (n : Nat) : Prop :=
  ∀ i j, seamCommutator n i j ≠ 0 → archiveRefinementSeam n i j

def archiveSeamSupportObligation (n : Nat) : Prop :=
  ArchiveSeamSupport n

theorem seamCommutator_zero_iff_operator_transport_flat (n : Nat) :
    seamCommutator n = 0 ↔ OperatorTransportFlat n := by
  rfl

end D0
