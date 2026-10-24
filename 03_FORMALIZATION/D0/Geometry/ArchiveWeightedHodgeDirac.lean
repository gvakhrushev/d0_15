import Mathlib.Data.Real.Basic
import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import D0.Geometry.ArchiveCubicalCochainCarrier
import D0.Geometry.ArchiveCubicalCoboundary
import D0.Geometry.ArchiveHodgeCARDiracSquare

namespace D0.Geometry

open D0

/-!
# D0.Geometry.ArchiveWeightedHodgeDirac

Owner: `D0-ARCHIVE-WEIGHTED-HODGE-DIRAC-001`.

The registered weighted-Hodge claim is broader than the current implementation:
this file does not construct a positive weight operator `W`, a weighted adjoint,
or a self-adjoint representative. Its legacy owner theorem contains a Boolean
degree-preservation flag. The concrete operator result added here is only for
the existing unweighted `hodgeCarDirac`: its square preserves every
homogeneous Fock degree by the already-owned fibrewise Laplacian identity.
This does not close the weighted claim or select a physical Hodge metric.
-/

/-- The number of form degrees, derived from the four role directions. -/
def formDegreeCount4D : ℕ := Fintype.card Role + 1

theorem formDegreeCount4D_eq_five : formDegreeCount4D = 5 := by
  unfold formDegreeCount4D
  rw [card_role]

/-- Legacy Boolean field; it is not a proposition about an operator. -/
def DegreePreservingLaplacian (preserves : Bool) : Prop :=
  preserves = true

/-- The existing unweighted Hodge/CAR square preserves each homogeneous Fock degree. -/
theorem unweightedHodgeSquare_degree_preserving (N k : ℕ)
    (ψ : ArchiveCochain N) (hψ : HomogeneousCochain N k ψ) :
    HomogeneousCochain N k (hodgeCarDirac N (hodgeCarDirac N ψ)) := by
  intro x S hS
  rw [hodgeCarDirac_sq_fibre]
  have hcomponent : (fun y : ArchiveRolePhaseGroup N => ψ (y, S)) = fun _ => 0 := by
    funext y
    exact hψ y S hS
  rw [hcomponent]
  simp [scalarDifferenceLaplacian, backwardDifference, forwardDifference]

/-- **D0-ARCHIVE-WEIGHTED-HODGE-DIRAC-001 (Owner locator)**:
The currently compiled package records finite counts and a legacy Boolean
flag, and includes the concrete unweighted Hodge-square degree-preservation
application above. It does not construct the weighted operator claimed by the
registry row. -/
theorem archive_weighted_hodge_dirac_owner :
    (formDegreeCount4D = 5) ∧
    (Fintype.card CubicalCellType = 16) ∧
    (DegreePreservingLaplacian true) ∧
    (Fintype.card Role = 4) ∧
    (∀ N k (ψ : ArchiveCochain N), HomogeneousCochain N k ψ →
      HomogeneousCochain N k (hodgeCarDirac N (hodgeCarDirac N ψ))) := by
  refine ⟨formDegreeCount4D_eq_five, card_archive_fock_state, rfl, card_role, ?_⟩
  intro N k ψ hψ
  exact unweightedHodgeSquare_degree_preserving N k ψ hψ

end D0.Geometry
