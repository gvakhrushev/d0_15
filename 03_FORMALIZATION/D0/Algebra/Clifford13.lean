import D0.Algebra.GammaMatrices

namespace D0

theorem gamma_anticomm :
    ∀ mu nu i j : Fin 4,
      anticommutator (gamma mu) (gamma nu) i j = cliffordRhs mu nu i j :=
  gamma_anticomm_entries

end D0
