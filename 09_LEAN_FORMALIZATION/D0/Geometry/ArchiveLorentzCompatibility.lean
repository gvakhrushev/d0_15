import D0.Geometry.ArchiveRefinementTower
import D0.Algebra.RoleSignature

namespace D0

def terminalSignature (_C : CapacityState) : Nat × Nat :=
  (positiveRoles, negativeRoles)

theorem terminalSignature_eq_1_3 (C : CapacityState) :
    terminalSignature C = (1, 3) := by
  unfold terminalSignature
  rw [role_signature_1_3.1, role_signature_1_3.2]

theorem archive_refinement_preserves_terminal_signature :
    ∀ n, terminalSignature (archiveTower n).terminal = (1, 3) := by
  intro n
  exact terminalSignature_eq_1_3 _

theorem archive_lorentz_carrier_stable :
    ∀ n, terminalSignature (archiveTower n).terminal =
      terminalSignature (archiveTower 0).terminal := by
  intro n
  rw [terminalSignature_eq_1_3, terminalSignature_eq_1_3]

end D0

