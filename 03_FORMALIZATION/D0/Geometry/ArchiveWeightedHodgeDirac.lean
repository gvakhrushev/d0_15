import Mathlib.Data.Real.Basic
import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import D0.Algebra.FiniteWeightedAdjoint
import D0.Geometry.ArchiveCubicalCochainCarrier
import D0.Geometry.ArchiveCubicalCoboundary
import D0.Geometry.ArchiveHodgeCARDiracSquare
import D0.Geometry.ArchiveHodgeCARDiracKernel

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
The file also supplies the finite diagonal-weight adjoint formula and applies
it to the existing `hodgeCarDiracₗ` for every supplied nonzero profile. This
remains a conditional algebraic application, not a derivation of geometric
Hodge weights.
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

/-- The adjoint of the existing Hodge/CAR operator for a supplied diagonal
cochain weight. The weight need only be nonzero at every basis coordinate;
this definition makes no positivity or metric-selection claim. -/
noncomputable def hodgeCarDiracDiagonalAdjoint (N : ℕ)
    (w : ArchiveCochainBasis N → ℝ) :
    ArchiveCochain N →ₗ[ℝ] ArchiveCochain N :=
  D0.Algebra.finiteWeightedAdjoint w (hodgeCarDiracₗ N)

/-- Concrete application of the finite weighted-adjoint construction to the
repository-owned Hodge/CAR operator at every lattice refinement. -/
theorem hodgeCarDirac_diagonal_weight_adjoint (N : ℕ)
    (w : ArchiveCochainBasis N → ℝ) (ψ φ : ArchiveCochain N) :
    (∀ p, w p ≠ 0) →
    D0.Algebra.finiteWeightedPairing w (hodgeCarDirac N ψ) φ =
      D0.Algebra.finiteWeightedPairing w ψ
        (hodgeCarDiracDiagonalAdjoint N w φ) := by
  intro hw
  exact D0.Algebra.finiteWeightedPairing_adjoint w hw (hodgeCarDiracₗ N) ψ φ

/-- The weighted adjoint of the squared Hodge/CAR operator is the square of
the supplied-profile adjoint. This is a concrete application of the generic
composition law and does not assert that the profile is geometrically selected. -/
theorem hodgeCarDirac_square_diagonal_weight_adjoint (N : ℕ)
    (w : ArchiveCochainBasis N → ℝ) (hw : ∀ p, w p ≠ 0) :
    D0.Algebra.finiteWeightedAdjoint w
        ((hodgeCarDiracₗ N).comp (hodgeCarDiracₗ N)) =
      (hodgeCarDiracDiagonalAdjoint N w).comp
        (hodgeCarDiracDiagonalAdjoint N w) := by
  simpa [hodgeCarDiracDiagonalAdjoint] using
    (D0.Algebra.finiteWeightedAdjoint_comp w hw
      (hodgeCarDiracₗ N) (hodgeCarDiracₗ N))

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
    (∀ N (ψ : ArchiveCochain N),
      cubicalCoboundary N (cubicalCoboundary N ψ) = 0) ∧
    (∀ N k (ψ : ArchiveCochain N), HomogeneousCochain N k ψ →
      HomogeneousCochain N k (hodgeCarDirac N (hodgeCarDirac N ψ))) ∧
    (∀ N (ψ φ : ArchiveCochain N),
      cochainPairing N (hodgeCarDirac N ψ) φ =
        cochainPairing N ψ (hodgeCarDirac N φ)) ∧
    (∀ N (w : ArchiveCochainBasis N → ℝ) (ψ φ : ArchiveCochain N),
      (∀ p, w p ≠ 0) →
      D0.Algebra.finiteWeightedPairing w (hodgeCarDirac N ψ) φ =
        D0.Algebra.finiteWeightedPairing w ψ
          (hodgeCarDiracDiagonalAdjoint N w φ)) ∧
    (∀ N (w : ArchiveCochainBasis N → ℝ), (∀ p, w p ≠ 0) →
      D0.Algebra.finiteWeightedAdjoint w
          ((hodgeCarDiracₗ N).comp (hodgeCarDiracₗ N)) =
        (hodgeCarDiracDiagonalAdjoint N w).comp
          (hodgeCarDiracDiagonalAdjoint N w)) := by
  refine ⟨formDegreeCount4D_eq_five, card_archive_fock_state, rfl, card_role,
    ?_, ?_, ?_, ?_, ?_⟩
  · intro N ψ
    exact d_squared_eq_zero N ψ
  · intro N k ψ hψ
    exact unweightedHodgeSquare_degree_preserving N k ψ hψ
  · intro N ψ φ
    exact hodgeCarDirac_self_adjoint N ψ φ
  · intro N w ψ φ hw
    exact hodgeCarDirac_diagonal_weight_adjoint N w ψ φ hw
  · intro N w hw
    exact hodgeCarDirac_square_diagonal_weight_adjoint N w hw

end D0.Geometry
