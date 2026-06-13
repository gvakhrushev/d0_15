import D0.NumberTheory.PhiAdmissibility

namespace D0

/-!
This module deliberately proves only the D0 positive-response forcing result.
The global Hurwitz/minimax continued-fraction theorem is not faked here.
-/

theorem D0_phi_forced_before_Hurwitz_layer :
    ∃! theta : Real, ∃ x : Real, D0ResponseRoot x ∧ theta = x^2 :=
  D0_admissible_rotation_unique

end D0
