import D0.Geometry.ArchiveLaplacianProperties

namespace D0

def FiniteStageResolventCompact (n : Nat) : Prop :=
  Nonempty (Fintype (ArchivePoints n))

def ArchiveProjectionCompatible : Prop :=
  forall n, Function.Surjective (archiveProjection n)

def ArchiveSpectralTightness : Prop :=
  forall n, (archiveTower n).modes <= (archiveTower (n + 1)).modes

structure ProfiniteResolventCompactness : Prop where
  finiteStageCompact : forall n, FiniteStageResolventCompact n
  projectionCompatible : ArchiveProjectionCompatible
  spectralTightness : ArchiveSpectralTightness

theorem finite_stage_resolvent_compact (n : Nat) :
    FiniteStageResolventCompact n := by
  exact ⟨inferInstance⟩

theorem archive_resolvent_projection_compatible :
    ArchiveProjectionCompatible := by
  intro n
  exact archive_projection_surjective n

theorem archive_spectral_tightness_from_mode_growth :
    ArchiveSpectralTightness := by
  intro n
  exact Nat.le_of_lt (spectral_modes_strictly_increase n)

theorem d0_archive_profinite_resolvent_compactness :
    ProfiniteResolventCompactness := by
  exact
    { finiteStageCompact := finite_stage_resolvent_compact
      projectionCompatible := archive_resolvent_projection_compatible
      spectralTightness := archive_spectral_tightness_from_mode_growth }

def D0ArchiveCompactResolvent : Prop :=
  ProfiniteResolventCompactness

theorem d0_archive_compact_resolvent :
    D0ArchiveCompactResolvent := by
  exact d0_archive_profinite_resolvent_compactness

end D0
