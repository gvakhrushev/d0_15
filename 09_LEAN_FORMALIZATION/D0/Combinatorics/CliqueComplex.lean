import D0.Combinatorics.CompleteTripartite

namespace D0

def FourCliqueParts (a b c d : Part) : Prop :=
  a ≠ b ∧ a ≠ c ∧ a ≠ d ∧ b ≠ c ∧ b ≠ d ∧ c ≠ d

theorem no_four_clique_parts (a b c d : Part) : ¬ FourCliqueParts a b c d :=
  no_four_distinct_parts a b c d

end D0
