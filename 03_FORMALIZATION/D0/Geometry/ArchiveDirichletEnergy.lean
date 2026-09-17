import D0.Geometry.ArchiveFiberGraph

open scoped BigOperators

namespace D0

def graphQuadraticForm {n : Nat} (G : ArchiveFiberGraph n) (L : G.V → G.V → Real) (f : G.V → Real) : Real :=
  haveI : Fintype G.V := G.fintypeV
  Finset.sum Finset.univ (fun u =>
    Finset.sum Finset.univ (fun v =>
      f u * L u v * f v
    )
  )

structure ExternalDirichletEnergyInterface (n : Nat) where
  quadraticFormNonnegative : ∀ f : (archiveFiberGraph n).V → Real,
    0 ≤ graphQuadraticForm (archiveFiberGraph n) (graphLaplacian (archiveFiberGraph n)) f

end D0
