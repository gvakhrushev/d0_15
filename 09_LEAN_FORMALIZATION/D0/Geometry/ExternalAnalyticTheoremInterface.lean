import D0.Geometry.ArchiveResolventCompactness
import D0.Geometry.SpectralActionAdmissibility

namespace D0

def D0ArchiveHeatTrace4D : Prop :=
  ArchiveHeatTrace4D archiveTower

def D0ArchiveHeatTraceExists : Prop :=
  D0ArchiveHeatTrace4D

def D0ArchiveHasAsymptoticExpansion : Prop :=
  ArchiveHeatTraceExpansion archiveTower

structure HeatKernelAdmissible : Prop where
  selfAdjoint : D0ArchiveSelfAdjoint
  nonnegative : D0ArchiveNonnegative
  compactResolvent : D0ArchiveCompactResolvent
  heatTraceExists : D0ArchiveHeatTraceExists
  hasAsymptoticExpansion : D0ArchiveHasAsymptoticExpansion
  spectralDimensionFour : D0ArchiveHeatTrace4D

def D0HasA0VolumeTerm : Prop :=
  D0ArchiveHeatTrace4D

def D0HasA1ScalarCurvatureTerm : Prop :=
  ScalarCurvatureCoefficientSlot archiveTower

def D0HigherTermsSuppressed : Prop :=
  HigherCurvatureCutoff delta0

structure ExternalSpectralActionAdmissible : Prop where
  heatKernel : HeatKernelAdmissible
  hasA0VolumeTerm : D0HasA0VolumeTerm
  hasA1ScalarCurvatureTerm : D0HasA1ScalarCurvatureTerm
  higherTermsSuppressed : D0HigherTermsSuppressed

theorem D0_archive_matches_heat_kernel_interface :
    D0ArchiveHeatTrace4D ->
    D0ArchiveSelfAdjoint ->
    D0ArchiveNonnegative ->
    D0ArchiveCompactResolvent ->
    HeatKernelAdmissible := by
  intro h4 hself hnon hcompact
  exact
    { selfAdjoint := hself
      nonnegative := hnon
      compactResolvent := hcompact
      heatTraceExists := h4
      hasAsymptoticExpansion :=
        ⟨h4, archive_mode_exponent_eq_lorentz_dimension⟩
      spectralDimensionFour := h4 }

theorem D0_archive_matches_spectral_action_interface :
    HeatKernelAdmissible ->
    HigherCurvatureCutoff delta0 ->
    ExternalSpectralActionAdmissible := by
  intro hk hcut
  exact
    { heatKernel := hk
      hasA0VolumeTerm := hk.spectralDimensionFour
      hasA1ScalarCurvatureTerm :=
        ⟨hk.spectralDimensionFour,
          archive_mode_exponent_eq_lorentz_carrier_dimension⟩
      higherTermsSuppressed := hcut }

end D0
