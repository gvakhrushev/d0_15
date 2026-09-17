import D0.Geometry.ArchiveVariation

open scoped BigOperators

namespace D0

def archiveCurvatureGradient (n : Nat) :
    Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ :=
  fun i j =>
    -2 * ∑ a : archivePhaseIndex (n+1),
      archiveLiftOperator n a i * seamCommutator n a j

def VacuumArchiveEquation (n : Nat) : Prop :=
  ArchiveStationary n

theorem vacuum_equation_iff_stationary (n : Nat) :
    VacuumArchiveEquation n ↔ ArchiveStationary n := by
  rfl

def sourcePairing (n : Nat)
    (T : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ)
    (δ : LaplacianVariation n) : ℝ :=
  matrixInnerProduct T δ.dL

def archiveDivergence {n : Nat}
    (A : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ) :
    archivePhaseIndex n → ℝ :=
  fun i => ∑ j : archivePhaseIndex n, A i j

structure ArchiveStressSource (n : Nat) where
  T : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ
  symmetric : MatrixSymmetric T
  conserved : archiveDivergence T = 0

def SourcedArchiveEquation (n : Nat) (T : ArchiveStressSource n) : Prop :=
  archiveCurvatureGradient n = T.T

def VariationalSourcedEquation (n : Nat) (T : ArchiveStressSource n) : Prop :=
  ∀ δ : LaplacianVariation n,
    matrixInnerProduct (archiveCurvatureGradient n) δ.dL = sourcePairing n T.T δ

theorem sourced_equation_variational_form
    (n : Nat) (T : ArchiveStressSource n) :
    SourcedArchiveEquation n T → VariationalSourcedEquation n T := by
  intro h δ
  unfold sourcePairing
  rw [h]

end D0
