import D0.Combinatorics.InfinitePhaseTower
import D0.Geometry.CovarianceTower

namespace D0

def branchKernel (n : Nat) (a b : Branches n) : Real :=
  if a.val = b.val then 1 else 0

def branchLaplacian (n : Nat) (a b : Branches n) : Real :=
  if a.val = b.val then 1 else 0

def infiniteStage (n : Nat) : FiniteSpectralStage :=
  { points := Branches n,
    fintype := inferInstance,
    G := branchKernel n,
    Delta := branchLaplacian n }

def infiniteProjection (n : Nat) :
    Projection (infiniteStage n) (infiniteStage (n + 1)) :=
  { map := P n }

theorem kernel_projection_compatible (n : Nat)
    (x y : Branches (n + 1)) :
    branchKernel (n + 1) x y =
      branchKernel n (P n x) (P n y) := by
  simp [branchKernel, P]

theorem laplacian_projection_compatible (n : Nat)
    (x y : Branches (n + 1)) :
    branchLaplacian (n + 1) x y =
      branchLaplacian n (P n x) (P n y) := by
  simp [branchLaplacian, P]

theorem covariance_compatible_all :
    HasCovarianceTower infiniteStage infiniteProjection := by
  intro n x y
  exact kernel_projection_compatible n x y

theorem projection_surjective_all :
    ∀ n, Function.Surjective (infiniteProjection n).map :=
  projection_surjective

end D0

