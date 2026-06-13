import D0.Algebra.Clifford

namespace D0

theorem gamma_clifford_relation :
    ∀ mu nu i j : Fin 4,
      anticommutator (gamma mu) (gamma nu) i j = cliffordRhs mu nu i j :=
  clifford_relation

theorem gamma00_square_positive :
    anticommutator (gamma 0) (gamma 0) = cliffordRhs 0 0 := by
  funext i j
  exact gamma_clifford_relation 0 0 i j

end D0
