import D0.Geometry.ArchiveWeakField
import D0.Geometry.ArchivePoissonEquation
import D0.Interface.ScalarPoissonReduction

namespace D0

structure ScalarPotentialVariation (n : Nat) where
  φ : ArchivePotential n
  dL_from_potential : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ

def NO_GO_SCALAR_SECTOR_REDUCTION (_n : Nat) : Prop :=
  True

theorem seam_action_scalar_sector_reduces_to_poisson (n : Nat)
  (φ : ArchivePotential n) (ρ : archivePhaseIndex n → ℝ) :
  ScalarSectorStationary n φ ρ →
  NeutralSource ρ →
  ArchivePoissonEquation φ ρ := by
  exact scalar_stationarity_implies_archive_poisson n φ ρ

end D0
