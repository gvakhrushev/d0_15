import D0.Combinatorics.CompleteTripartite
import D0.Topology.NoThreeSimplices

namespace D0

theorem vertex_count_K_9_11_13 : numVertices = 33 := num_vertices

theorem edge_count_K_9_11_13 :
    9 * 11 + 9 * 13 + 11 * 13 = 359 := by
  norm_num

theorem triangle_count_K_9_11_13 :
    9 * 11 * 13 = 1287 := by
  norm_num

theorem no_four_partite_clique (a b c d : Part) :
    ¬ FourCliqueParts a b c d :=
  no_four_clique_parts a b c d

theorem no_four_clique_K_9_11_13 (a b c d : Part) :
    ¬ FourCliqueParts a b c d :=
  no_four_partite_clique a b c d

theorem no_3_simplices_clique_complex (a b c d : Part) :
    ¬ FourCliqueParts a b c d :=
  no_3_simplices a b c d

end D0
