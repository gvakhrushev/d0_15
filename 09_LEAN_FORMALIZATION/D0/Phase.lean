import D0.Core.DyadABCD
import D0.Core.FiniteTypes
import D0.Combinatorics.PhaseUnfolding
import D0.Combinatorics.ForcedReturnWindows

namespace D0

abbrev ABCD := Role

theorem abcd_cardinality : Fintype.card ABCD = 4 := card_role

theorem v9_cardinality : Fintype.card V9 = 9 := card_v9
theorem v11_cardinality : Fintype.card V11 = 11 := card_v11
theorem v13_cardinality : Fintype.card V13 = 13 := card_v13

theorem forced_terminal_window : Nat.lcm 4 11 = 44 := by
  native_decide

theorem terminal_window_totient : Nat.totient 44 = 20 := totient_44

theorem forced_ew_window : 2 * 5 * 71 = 710 := by
  norm_num

theorem ew_window_totient : Nat.totient 710 = 280 := totient_710

theorem ew_depth : 280 / 8 = 35 := by
  norm_num

end D0
