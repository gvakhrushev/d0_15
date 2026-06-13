import D0.Combinatorics.Tripartite

namespace D0

theorem no_three_simplices_K_9_11_13 (a b c d : Part) :
    ¬ FourCliqueParts a b c d :=
  no_3_simplices_clique_complex a b c d

end D0
