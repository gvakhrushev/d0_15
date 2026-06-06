import D0.Algebra.Clifford13

namespace D0

theorem clifford_relation :
    ∀ mu nu i j : Fin 4,
      anticommutator (gamma mu) (gamma nu) i j = cliffordRhs mu nu i j :=
  gamma_anticomm

end D0
