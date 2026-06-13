import D0.Geometry.ArchiveRefinementTower

namespace D0

def archiveCurvatureObstruction (n : Nat) (a b : ArchivePoints (n+1)) : Real :=
  archiveDelta n (archiveProjection n a) (archiveProjection n b) - archiveDelta (n+1) a b

def ArchiveProjectionFlat (n : Nat) : Prop :=
  ∀ a b : ArchivePoints (n+1), archiveDelta n (archiveProjection n a) (archiveProjection n b) = archiveDelta (n+1) a b

theorem flat_archive_iff_zero_curvature_obstruction (n : Nat) :
  (∀ a b, archiveCurvatureObstruction n a b = 0) ↔ ArchiveProjectionFlat n := by
  unfold archiveCurvatureObstruction ArchiveProjectionFlat
  constructor
  · intro h a b
    have h_sub := h a b
    linarith
  · intro h a b
    rw [h a b, sub_self]

end D0
