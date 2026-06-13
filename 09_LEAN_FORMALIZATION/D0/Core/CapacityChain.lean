import D0.Core.FiniteTypes

namespace D0

theorem capacity_chain_cards :
    Fintype.card Role = 4 ∧
    Fintype.card Omega8 = 8 ∧
    Fintype.card V9 = 9 ∧
    Fintype.card V11 = 11 ∧
    Fintype.card V13 = 13 := by
  exact ⟨card_role, card_omega8, card_v9, card_v11, card_v13⟩

theorem no_three_role_terminal_capacity : ¬ Fintype.card Role = 3 := by
  rw [card_role]
  norm_num

theorem no_five_role_minimality : ¬ Fintype.card Role = 5 := by
  rw [card_role]
  norm_num

end D0
