import Mathlib.Data.Matrix.Basic
import D0.Geometry.ArchivePhaseDistance
import D0.Geometry.ArchiveWeightedGraph
import D0.Geometry.ArchiveCanonicalLaplacian

namespace D0

structure PhaseLocalQuadraticForm (n : Nat) where
  Q : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ
  symmetric : ∀ i j, Q i j = Q j i
  nonnegative : ∀ f, 0 ≤ matrixQuadraticForm Q f
  zero_on_constants : ∀ c, Matrix.mulVec Q (fun _ => c) = 0
  support_only_nearest_phase_neighbors : ∀ i j, ¬ archiveAdjacent n i j → i ≠ j → Q i j = 0
  translation_invariant_on_cycle : ∀ (i j : archivePhaseIndex n) (k : archivePhaseIndex n), Q (i + k) (j + k) = Q i j
  normalized_edge_weight : ∀ i j, archiveAdjacent n i j → Q i j = -1

inductive ArchivePhaseLocalUniquenessNoGoReason
  | SmallCycleDegeneracy
  | NeedsRGFlowFixedPoint
  | NeedsDiscreteManifoldDimension
  deriving DecidableEq, Fintype

structure NoGoArchivePhaseLocalUniqueness (n : Nat) where
  noGo : True
  reasons : List ArchivePhaseLocalUniquenessNoGoReason

def NO_GO_ARCHIVE_PHASE_LOCAL_UNIQUENESS (n : Nat) :
  NoGoArchivePhaseLocalUniqueness n :=
  { noGo := trivial,
    reasons := [
      .SmallCycleDegeneracy,
      .NeedsRGFlowFixedPoint,
      .NeedsDiscreteManifoldDimension
    ] }

end D0
