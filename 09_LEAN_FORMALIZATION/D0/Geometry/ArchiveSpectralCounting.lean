import D0.Geometry.ArchiveHeatTrace

namespace D0

noncomputable def eigenCountBelow (n : Nat) (Λ : Real) : Nat := by
  classical
  exact ((Finset.univ : Finset (ArchivePoints n)).filter
    (fun x => archiveEigenvalue n x ≤ Λ)).card

structure HasWeylDimension
    (tower : Nat -> ArchiveState) (d : Real) where
  countingAsymptotic : Prop
  heatTraceScaling : Prop
  noSpectralPollution : Prop
  dimensionValue : d = 4

theorem eigenCountBelow_le_modes (n : Nat) (Λ : Real) :
    eigenCountBelow n Λ ≤ (archiveTower n).modes := by
  classical
  unfold eigenCountBelow
  have h :=
    Finset.card_filter_le (s := (Finset.univ : Finset (ArchivePoints n)))
      (p := fun x => archiveEigenvalue n x ≤ Λ)
  simpa [ArchivePoints] using h

theorem eigenCountBelow_nonnegative (n : Nat) (Λ : Real) :
    0 ≤ eigenCountBelow n Λ := by
  exact Nat.zero_le _

end D0
