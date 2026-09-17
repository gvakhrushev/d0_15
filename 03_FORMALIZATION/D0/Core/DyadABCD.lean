import D0.Core.FiniteTypes

namespace D0

def A : Role := (0, 0)
def B : Role := (1, 1)
def C : Role := (0, 1)
def D : Role := (1, 0)

def roleList : List Role := [A, B, C, D]

theorem roleList_length : roleList.length = 4 := by
  rfl

theorem ABCD_cardinality : Fintype.card Role = 4 := card_role

theorem omega8_cardinality : Fintype.card Omega8 = 8 := card_omega8

end D0
