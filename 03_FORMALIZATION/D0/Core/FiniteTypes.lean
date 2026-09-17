import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Fintype.Fin
import Mathlib.Data.Fintype.Prod
import Mathlib.Data.Fintype.Sum
import Mathlib.Tactic

namespace D0

abbrev Dyad := Fin 2
abbrev Role := Dyad × Dyad
abbrev Orient := Bool
abbrev Omega8 := Role × Orient
abbrev Witness := PUnit
abbrev V9 := Sum Omega8 Witness
abbrev V11 := Sum V9 Dyad
abbrev V13 := Sum V9 Role

theorem card_dyad : Fintype.card Dyad = 2 := by
  simp [Dyad]

theorem card_role : Fintype.card Role = 4 := by
  simp [Role, Dyad]

theorem card_omega8 : Fintype.card Omega8 = 8 := by
  simp [Omega8, Role, Dyad, Orient]

theorem card_v9 : Fintype.card V9 = 9 := by
  simp [V9, Omega8, Role, Dyad, Orient, Witness]

theorem card_v11 : Fintype.card V11 = 11 := by
  simp [V11, V9, Omega8, Role, Dyad, Orient, Witness]

theorem card_v13 : Fintype.card V13 = 13 := by
  simp [V13, V9, Omega8, Role, Dyad, Orient, Witness]

theorem scene_card_total : Fintype.card V9 + Fintype.card V11 + Fintype.card V13 = 33 := by
  rw [card_v9, card_v11, card_v13]

end D0
