import D0.Geometry.ArchiveRefinementTower
import D0.Geometry.ArchiveLorentzCompatibility
import D0.Phase

namespace D0

def archiveModeExponent : Nat :=
  Fintype.card ABCD

def lorentzCarrierDimension : Nat :=
  positiveRoles + negativeRoles

theorem archive_mode_exponent_eq_abcd :
    archiveModeExponent = Fintype.card ABCD := by
  rfl

theorem archive_mode_exponent_eq_lorentz_dimension :
    archiveModeExponent = 4 := by
  rw [archive_mode_exponent_eq_abcd, abcd_cardinality]

theorem lorentzCarrierDimension_eq_four :
    lorentzCarrierDimension = 4 := by
  unfold lorentzCarrierDimension
  rw [role_signature_1_3.1, role_signature_1_3.2]

theorem archive_mode_exponent_eq_lorentz_carrier_dimension :
    archiveModeExponent = lorentzCarrierDimension := by
  rw [archive_mode_exponent_eq_lorentz_dimension, lorentzCarrierDimension_eq_four]

theorem archive_modes_forced (n : Nat) :
    archiveModes n = archiveFibers n ^ Fintype.card ABCD := by
  rw [abcd_cardinality]
  rfl

theorem archive_modes_forced_by_lorentz_carrier (n : Nat) :
    archiveModes n = archiveFibers n ^ lorentzCarrierDimension := by
  rw [lorentzCarrierDimension_eq_four]
  rfl

end D0
