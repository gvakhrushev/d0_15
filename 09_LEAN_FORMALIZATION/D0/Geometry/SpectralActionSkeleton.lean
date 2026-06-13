import D0.Geometry.ArchiveSpectralCounting

namespace D0

structure HeatKernelEHAdmissible (tower : Nat -> ArchiveState) where
  spectralDimension4 : Prop
  hasA0 : Prop
  hasA1ScalarCurvatureTerm : Prop
  higherCurvatureSuppressed : Prop

def EinsteinHilbertLeadingTerm (tower : Nat -> ArchiveState) : Prop :=
  Nonempty (HeatKernelEHAdmissible tower)

theorem EH_leading_term_if_admissible :
    HeatKernelEHAdmissible archiveTower ->
      EinsteinHilbertLeadingTerm archiveTower := by
  intro h
  exact ⟨h⟩

end D0
