import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import D0.Geometry.ArchivePhaseDistance
import D0.Geometry.ArchiveWeightedGraph

open scoped BigOperators

namespace D0

def archiveDirichletEnergy (n : Nat) (f : archivePhaseIndex n → ℝ) : ℝ :=
  ∑ i : archivePhaseIndex n, ∑ j : archivePhaseIndex n,
    if archiveAdjacent n i j then (f i - f j)^2 else 0

end D0
