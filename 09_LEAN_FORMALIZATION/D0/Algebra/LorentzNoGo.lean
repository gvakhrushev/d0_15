import D0.Algebra.RoleSignature

namespace D0

def roleSignature : Nat × Nat := (positiveRoles, negativeRoles)

theorem roleSignature_eq_1_3 :
    roleSignature = (1, 3) := by
  unfold roleSignature
  rw [role_signature_1_3.1, role_signature_1_3.2]

theorem no_euclidean_SO4 :
    roleSignature ≠ (4, 0) := by
  rw [roleSignature_eq_1_3]
  decide

theorem no_split_SO22 :
    roleSignature ≠ (2, 2) := by
  rw [roleSignature_eq_1_3]
  decide

theorem no_deSitter_SO14 :
    Fintype.card RoleSig = 4 -> ¬ 5 ≤ Fintype.card RoleSig := by
  intro h h5
  rw [h] at h5
  omega

end D0
