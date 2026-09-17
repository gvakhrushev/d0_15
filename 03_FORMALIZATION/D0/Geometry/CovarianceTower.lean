import D0.Geometry.SpectralTower

namespace D0

structure FiniteSpectralStage where
  points : Type
  fintype : Fintype points
  G : points -> points -> Real
  Delta : points -> points -> Real

attribute [instance] FiniteSpectralStage.fintype

structure Projection (A B : FiniteSpectralStage) where
  map : B.points -> A.points

def ProjectivelyCompatible (A B : FiniteSpectralStage) (P : Projection A B) : Prop :=
  ∀ x y : B.points, B.G x y = A.G (P.map x) (P.map y)

def HasCovarianceTower (stage : Nat -> FiniteSpectralStage)
    (projection : (n : Nat) -> Projection (stage n) (stage (n + 1))) : Prop :=
  ∀ n, ProjectivelyCompatible (stage n) (stage (n + 1)) (projection n)

end D0
