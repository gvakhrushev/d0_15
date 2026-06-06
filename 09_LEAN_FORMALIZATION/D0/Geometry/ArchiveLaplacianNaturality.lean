import D0.Geometry.ArchiveLocalQuadraticForm

namespace D0

structure UniquenessProof (n : Nat) where
  unique : ∀ Q1 Q2 : ArchiveLocalQuadraticForm n, ∃ c : Real, Q1.Q = c • Q2.Q

inductive ArchiveLaplacianUniquenessNoGoReason
  | TooWeakLocalityAxioms
  | NeedsOrientation
  | NeedsNormalization
  | NeedsPhaseDistanceStructure
  deriving DecidableEq, Fintype

structure NoGoArchiveLaplacianUniqueness (n : Nat) where
  noGo : True
  reasons : List ArchiveLaplacianUniquenessNoGoReason

def NO_GO_ARCHIVE_LAPLACIAN_UNIQUENESS (n : Nat) :
  NoGoArchiveLaplacianUniqueness n :=
  { noGo := trivial,
    reasons := [
      .TooWeakLocalityAxioms,
      .NeedsOrientation,
      .NeedsNormalization,
      .NeedsPhaseDistanceStructure
    ] }

end D0
