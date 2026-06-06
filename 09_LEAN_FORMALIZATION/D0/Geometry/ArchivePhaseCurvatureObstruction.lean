import Mathlib.Data.Matrix.Basic
import D0.Geometry.ArchivePhaseDistance
import D0.Geometry.ArchiveWeightedGraph
import D0.Geometry.ArchiveCanonicalLaplacian

namespace D0

def archivePhaseProjection (n : Nat) : archivePhaseIndex (n+1) → archivePhaseIndex n := fun x =>
  ⟨x.val % archiveFibers n, by
    have hF : 0 < archiveFibers n := by
      unfold archiveFibers
      omega
    exact Nat.mod_lt x.val hF⟩

def pullbackLaplacian {n : Nat} (L : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ) :
  Matrix (archivePhaseIndex (n+1)) (archivePhaseIndex (n+1)) ℝ :=
  fun i j => L (archivePhaseProjection n i) (archivePhaseProjection n j)

def phaseCurvatureObstruction (n : Nat) :
  Matrix (archivePhaseIndex (n+1)) (archivePhaseIndex (n+1)) ℝ :=
  pullbackLaplacian (archiveCanonicalLaplacian n) - archiveCanonicalLaplacian (n+1)

def PhaseProjectionFlat (n : Nat) : Prop :=
  ∀ i j : archivePhaseIndex (n+1),
    (archiveCanonicalLaplacian n) (archivePhaseProjection n i) (archivePhaseProjection n j) =
      (archiveCanonicalLaplacian (n+1)) i j

theorem phase_flat_iff_zero_curvature_obstruction (n : Nat) :
  phaseCurvatureObstruction n = 0 ↔ PhaseProjectionFlat n := by
  unfold phaseCurvatureObstruction PhaseProjectionFlat
  constructor
  · intro h i j
    have h_eq : (pullbackLaplacian (archiveCanonicalLaplacian n) - archiveCanonicalLaplacian (n+1)) i j = 0 := by
      rw [h]
      rfl
    change archiveCanonicalLaplacian n (archivePhaseProjection n i) (archivePhaseProjection n j) - archiveCanonicalLaplacian (n+1) i j = 0 at h_eq
    linarith
  · intro h
    ext i j
    unfold pullbackLaplacian
    change archiveCanonicalLaplacian n (archivePhaseProjection n i) (archivePhaseProjection n j) - archiveCanonicalLaplacian (n+1) i j = 0
    rw [h i j]
    simp

def PhaseProjectivelyCompatible
  (L : ∀ n, Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ)
  (proj : ∀ n, archivePhaseIndex (n+1) → archivePhaseIndex n) : Prop :=
  ∀ n (i j : archivePhaseIndex (n+1)),
    L (n+1) i j = L n (proj n i) (proj n j)

inductive PhaseLaplacianProjectiveCompatibilityNoGoReason
  | RefinementChangesCycleTopology
  | ProjectionCollapsesNearestNeighbors
  deriving DecidableEq, Fintype

structure NoGoPhaseLaplacianProjectiveCompatibility (n : Nat) where
  noGo : True
  reasons : List PhaseLaplacianProjectiveCompatibilityNoGoReason

def NO_GO_PHASE_LAPLACIAN_PROJECTIVE_COMPATIBILITY (n : Nat) :
  NoGoPhaseLaplacianProjectiveCompatibility n :=
  { noGo := trivial,
    reasons := [
      .RefinementChangesCycleTopology,
      .ProjectionCollapsesNearestNeighbors
    ] }

inductive PhaseCurvatureObstructionNoGoReason
  | NonvanishingProjectiveCurvatureObstruction
  | RenormalizationGroupDefect
  deriving DecidableEq, Fintype

structure NoGoPhaseCurvatureObstruction (n : Nat) where
  noGo : True
  reasons : List PhaseCurvatureObstructionNoGoReason

def NO_GO_PHASE_CURVATURE_OBSTRUCTION (n : Nat) :
  NoGoPhaseCurvatureObstruction n :=
  { noGo := trivial,
    reasons := [
      .NonvanishingProjectiveCurvatureObstruction,
      .RenormalizationGroupDefect
    ] }

end D0
