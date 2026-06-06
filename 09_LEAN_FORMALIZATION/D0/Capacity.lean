import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Fintype.Prod
import Mathlib.Data.Fintype.Sum
import Mathlib.Tactic

namespace D0

inductive D2 where
  | direct | return
  deriving DecidableEq, Repr, Fintype

abbrev ABCD2 := D2 × D2
abbrev Omega8V12 := ABCD2 × Bool
abbrev V9V12 := Option Omega8V12
abbrev V11V12 := Sum V9V12 D2
abbrev V13V12 := Sum V9V12 ABCD2

theorem d2_cardinality : Fintype.card D2 = 2 := by
  native_decide

theorem abcd2_cardinality : Fintype.card ABCD2 = 4 := by
  simp [ABCD2, d2_cardinality]

theorem omega8_v12_cardinality : Fintype.card Omega8V12 = 8 := by
  simp [Omega8V12, ABCD2, d2_cardinality]

theorem v9_v12_cardinality : Fintype.card V9V12 = 9 := by
  simp [V9V12, Omega8V12, ABCD2, d2_cardinality]

theorem v11_v12_cardinality : Fintype.card V11V12 = 11 := by
  simp [V11V12, V9V12, Omega8V12, ABCD2, d2_cardinality]

theorem v13_v12_cardinality : Fintype.card V13V12 = 13 := by
  simp [V13V12, V9V12, Omega8V12, ABCD2, d2_cardinality]

end D0
