import D0.Geometry.ArchiveModeExponent
import D0.Geometry.ArchiveSpectralCounting
import D0.Geometry.ArchiveLorentzCompatibility
import D0.Geometry.HigherCurvatureCutoff

namespace D0

def ArchiveHeatTrace4D (tower : Nat -> ArchiveState) : Prop :=
  Nonempty (HasWeylDimension tower 4)

def ArchiveHeatTraceExpansion (tower : Nat -> ArchiveState) : Prop :=
  ArchiveHeatTrace4D tower /\ archiveModeExponent = 4

def ScalarCurvatureCoefficientSlot (tower : Nat -> ArchiveState) : Prop :=
  ArchiveHeatTrace4D tower /\ archiveModeExponent = lorentzCarrierDimension

def HigherCurvatureCutoff (delta : Real) : Prop :=
  0 < delta /\ stopIdeal = delta^12

def LorentzCarrierStable (tower : Nat -> ArchiveState) : Prop :=
  forall n, terminalSignature (tower n).terminal = terminalSignature (tower 0).terminal

structure SpectralActionAdmissible (tower : Nat -> ArchiveState) : Prop where
  spectralDimensionFour : ArchiveHeatTrace4D tower
  heatTraceExpansion : ArchiveHeatTraceExpansion tower
  hasScalarCurvatureCoefficient : ScalarCurvatureCoefficientSlot tower
  higherCurvatureSuppressed : HigherCurvatureCutoff delta0
  lorentzCarrierStable : LorentzCarrierStable tower

theorem d0_higher_curvature_cutoff :
    HigherCurvatureCutoff delta0 := by
  exact ⟨delta0_pos, rfl⟩

theorem d0_archive_lorentz_carrier_stable :
    LorentzCarrierStable archiveTower := by
  intro n
  exact archive_lorentz_carrier_stable n

theorem d0_archive_satisfies_structural_admissibility :
    ArchiveHeatTrace4D archiveTower ->
    HigherCurvatureCutoff delta0 ->
    LorentzCarrierStable archiveTower ->
    SpectralActionAdmissible archiveTower := by
  intro h4 hcut hlor
  exact
    { spectralDimensionFour := h4
      heatTraceExpansion := ⟨h4, archive_mode_exponent_eq_lorentz_dimension⟩
      hasScalarCurvatureCoefficient :=
        ⟨h4, archive_mode_exponent_eq_lorentz_carrier_dimension⟩
      higherCurvatureSuppressed := hcut
      lorentzCarrierStable := hlor }

end D0
