import D0.Topology.SimplicialIncidence

namespace D0

theorem boundary_boundary_zero {m n k : ℕ} (I : IncidencePair m n k) :
    I.d1 * I.d2 = 0 :=
  I.compatible

end D0
