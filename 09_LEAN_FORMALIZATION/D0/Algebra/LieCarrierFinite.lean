import D0.Algebra.Clifford13

namespace D0

structure FiniteLieCarrier where
  gammaLaw : ∀ mu nu i j : Fin 4,
    anticommutator (gamma mu) (gamma nu) i j = cliffordRhs mu nu i j
  bivectors : Nat.choose 4 2 = 6

def clifford13FiniteCarrier : FiniteLieCarrier where
  gammaLaw := gamma_anticomm
  bivectors := bivector_count

end D0
