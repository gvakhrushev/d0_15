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
this file does not construct a positive weight operator `W` or a standard-
Hilbert self-adjoint representative. Its legacy owner theorem contains a Boolean
degree-preservation flag. The concrete operator result added here is only for
the existing unweighted `hodgeCarDirac`: its square preserves every
homogeneous Fock degree by the already-owned fibrewise Laplacian identity.
This does not close the weighted claim or select a physical Hodge metric.
The file also supplies the finite diagonal-weight adjoint formula and applies
it to the existing `hodgeCarDiracₗ` for every supplied nonzero profile. The
conditional `cubicalWeightedHodgeDirac_application` additionally constructs
`d + d†_w` from the registered cubical coboundary and proves bilinear
self-adjointness, the Hodge anticommutator, and degree preservation of its
square. The profile may be signed; neither its positivity nor its geometric
origin is derived here. A separate positive-profile specialization below
proves positive definiteness for an auxiliary diagonal pairing supplied by
the caller. It is not the Lorentz-induced Hodge profile, whose finite exterior
pairing is indefinite, and gives no standard-Hilbert or physical result.
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

/-- At the real unit profile, the existing Hodge/CAR weighted adjoint is the
standard finite Hermitian adjoint. This identifies the two algebraic APIs on
their common specialization only; it does not select a profile or identify
the Lorentz-induced geometric Hodge operation. -/
theorem hodgeCarDirac_unit_profile_adjoint_eq_finiteHermitianAdjoint
    (N : ℕ) :
    hodgeCarDiracDiagonalAdjoint N (fun _ => (1 : ℝ)) =
      D0.Algebra.finiteHermitianAdjoint (hodgeCarDiracₗ N) := by
  simpa [hodgeCarDiracDiagonalAdjoint] using
    (D0.Algebra.finiteWeightedAdjoint_one_eq_finiteHermitianAdjoint
      (A := hodgeCarDiracₗ N))

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

/-- The weighted codifferential of the registered cubical coboundary. The
profile is supplied by the caller and is required to be nonzero pointwise;
this definition does not derive a positive or geometric Hodge weight. -/
noncomputable def cubicalCodifferentialDiagonalAdjoint (N : ℕ)
    (w : ArchiveCochainBasis N → ℝ) :
    ArchiveCochain N →ₗ[ℝ] ArchiveCochain N :=
  D0.Algebra.finiteWeightedAdjoint w (cubicalCoboundaryₗ N)

/-- The finite weighted Hodge-Dirac operator `d + d†_w` built from the actual
registered unit-step cubical coboundary and its diagonal weighted adjoint. -/
noncomputable def cubicalWeightedHodgeDiracₗ (N : ℕ)
    (w : ArchiveCochainBasis N → ℝ) :
    ArchiveCochain N →ₗ[ℝ] ArchiveCochain N :=
  D0.Algebra.finiteWeightedHodgeDirac w (cubicalCoboundaryₗ N)

/-- Pointwise form of `cubicalWeightedHodgeDiracₗ`. -/
noncomputable def cubicalWeightedHodgeDirac (N : ℕ)
    (w : ArchiveCochainBasis N → ℝ) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  cubicalWeightedHodgeDiracₗ N w ψ

/-- At the unit profile, the weighted cubical Hodge--Dirac built from the
registered finite cubical coboundary is exactly the generic Hermitian
Hodge--Dirac specialization. -/
theorem cubicalWeightedHodgeDirac_unit_profile_eq_finiteHermitianHodgeDirac
    (N : ℕ) :
    cubicalWeightedHodgeDiracₗ N (fun _ => (1 : ℝ)) =
      D0.Algebra.finiteHermitianHodgeDirac (cubicalCoboundaryₗ N) := by
  change cubicalCoboundaryₗ N +
      D0.Algebra.finiteWeightedAdjoint (fun _ => (1 : ℝ))
        (cubicalCoboundaryₗ N) =
    cubicalCoboundaryₗ N +
      D0.Algebra.finiteHermitianAdjoint (cubicalCoboundaryₗ N)
  rw [D0.Algebra.finiteWeightedAdjoint_one_eq_finiteHermitianAdjoint]

/-- The same concrete unit-profile cubical Hodge--Dirac application is
self-adjoint under the standard finite Hermitian pairing. -/
theorem cubicalWeightedHodgeDirac_unit_profile_hermitian_self_adjoint
    (N : ℕ) (ψ φ : ArchiveCochain N) :
    D0.Algebra.finiteHermitianPairing
        (cubicalWeightedHodgeDirac N (fun _ => (1 : ℝ)) ψ) φ =
      D0.Algebra.finiteHermitianPairing ψ
        (cubicalWeightedHodgeDirac N (fun _ => (1 : ℝ)) φ) := by
  change D0.Algebra.finiteHermitianPairing
      (cubicalWeightedHodgeDiracₗ N (fun _ => (1 : ℝ)) ψ) φ =
    D0.Algebra.finiteHermitianPairing ψ
      (cubicalWeightedHodgeDiracₗ N (fun _ => (1 : ℝ)) φ)
  rw [cubicalWeightedHodgeDirac_unit_profile_eq_finiteHermitianHodgeDirac]
  exact D0.Algebra.finiteHermitianHodgeDirac_pairing_self_adjoint
    (cubicalCoboundaryₗ N) ψ φ

/-- The constructed weighted cubical Hodge-Dirac is self-adjoint for its
supplied diagonal bilinear pairing. Nonzero weights are the only required
algebraic condition. -/
theorem cubicalWeightedHodgeDirac_pairing_self_adjoint (N : ℕ)
    (w : ArchiveCochainBasis N → ℝ) (hw : ∀ p, w p ≠ 0)
    (ψ φ : ArchiveCochain N) :
    D0.Algebra.finiteWeightedPairing w (cubicalWeightedHodgeDirac N w ψ) φ =
      D0.Algebra.finiteWeightedPairing w ψ (cubicalWeightedHodgeDirac N w φ) := by
  simpa [cubicalWeightedHodgeDirac, cubicalWeightedHodgeDiracₗ] using
    (D0.Algebra.finiteWeightedHodgeDirac_pairing_self_adjoint w hw
      (cubicalCoboundaryₗ N) ψ φ)

/-- For a caller-supplied positive comparison profile on the existing finite
cochain carrier, the diagonal pairing is positive definite and the constructed
cubical weighted Hodge-Dirac is self-adjoint for it. This profile is not the
Lorentz-induced Hodge weight and is neither derived nor physically selected. -/
theorem cubicalWeightedHodgeDirac_positive_profile_application :
    (∀ N (w : ArchiveCochainBasis N → ℝ), (∀ p, 0 < w p) →
      ∀ ψ, ψ ≠ 0 → 0 < D0.Algebra.finiteWeightedPairing w ψ ψ) ∧
    (∀ N (w : ArchiveCochainBasis N → ℝ), (∀ p, 0 < w p) →
      ∀ ψ φ, D0.Algebra.finiteWeightedPairing w
        (cubicalWeightedHodgeDirac N w ψ) φ =
          D0.Algebra.finiteWeightedPairing w ψ
            (cubicalWeightedHodgeDirac N w φ)) := by
  refine ⟨?_, ?_⟩
  · intro N w hw ψ hψ
    exact D0.Algebra.finiteWeightedPairing_pos_def w ψ hw hψ
  · intro N w hw ψ φ
    exact cubicalWeightedHodgeDirac_pairing_self_adjoint N w
      (fun p => ne_of_gt (hw p)) ψ φ

/-- Its square is the anticommutator `d d†_w + d†_w d`, using the actual
nilpotency theorem for the normalized cubical coboundary. -/
theorem cubicalWeightedHodgeDirac_square (N : ℕ)
    (w : ArchiveCochainBasis N → ℝ) (hw : ∀ p, w p ≠ 0) :
    (cubicalWeightedHodgeDiracₗ N w).comp (cubicalWeightedHodgeDiracₗ N w) =
      (cubicalCoboundaryₗ N).comp (cubicalCodifferentialDiagonalAdjoint N w) +
        (cubicalCodifferentialDiagonalAdjoint N w).comp (cubicalCoboundaryₗ N) := by
  simpa [cubicalWeightedHodgeDiracₗ, cubicalCodifferentialDiagonalAdjoint] using
    (D0.Algebra.finiteWeightedHodgeDirac_square w hw
      (cubicalCoboundaryₗ N) (cubicalCoboundaryₗ_comp_self_eq_zero N))

/-- The weighted Hodge square preserves the existing CAR form-degree grading
for every supplied nonzero diagonal profile. -/
theorem cubicalWeightedHodgeDirac_square_degree_preserving (N k : ℕ)
    (w : ArchiveCochainBasis N → ℝ) (hw : ∀ p, w p ≠ 0)
    (ψ : ArchiveCochain N) (hψ : HomogeneousCochain N k ψ) :
    HomogeneousCochain N k
      (cubicalWeightedHodgeDirac N w (cubicalWeightedHodgeDirac N w ψ)) := by
  have hRaise : ∀ j x,
      D0.Algebra.finiteDegreeSupported (fun p : ArchiveCochainBasis N => fockDegree p.2)
        j x →
      D0.Algebra.finiteDegreeSupported (fun p : ArchiveCochainBasis N => fockDegree p.2)
        (j + 1) (cubicalCoboundaryₗ N x) := by
    intro j x hx
    have hHomogeneous : HomogeneousCochain N j x := by
      intro site S hS
      exact hx (site, S) hS
    have hRaised := cubicalCoboundaryₗ_degree_raise N j x hHomogeneous
    intro p hp
    exact hRaised p.1 p.2 hp
  have hψ' :
      D0.Algebra.finiteDegreeSupported (fun p : ArchiveCochainBasis N => fockDegree p.2)
        k ψ := by
    intro p hp
    exact hψ p.1 p.2 hp
  have hPreserved := D0.Algebra.finiteWeightedHodgeDirac_square_preserves_degree
    w hw (cubicalCoboundaryₗ N) (fun p : ArchiveCochainBasis N => fockDegree p.2)
    hRaise (cubicalCoboundaryₗ_comp_self_eq_zero N) k ψ hψ'
  intro site S hS
  exact hPreserved (site, S) hS

/-- A compiled application of the generic finite weighted-Hodge API to the
repository's actual nilpotent, degree-raising cubical differential. These
conditional algebraic conclusions do not establish positive metric weights,
their geometric origin, or physical Hodge selection. -/
theorem cubicalWeightedHodgeDirac_application :
    (∀ N (w : ArchiveCochainBasis N → ℝ), (∀ p, w p ≠ 0) →
      ∀ ψ φ, D0.Algebra.finiteWeightedPairing w
        (cubicalWeightedHodgeDirac N w ψ) φ =
          D0.Algebra.finiteWeightedPairing w ψ (cubicalWeightedHodgeDirac N w φ)) ∧
    (∀ N (w : ArchiveCochainBasis N → ℝ), (∀ p, w p ≠ 0) →
      (cubicalWeightedHodgeDiracₗ N w).comp (cubicalWeightedHodgeDiracₗ N w) =
        (cubicalCoboundaryₗ N).comp (cubicalCodifferentialDiagonalAdjoint N w) +
          (cubicalCodifferentialDiagonalAdjoint N w).comp (cubicalCoboundaryₗ N)) ∧
    (∀ N k (w : ArchiveCochainBasis N → ℝ) (ψ : ArchiveCochain N),
      (∀ p, w p ≠ 0) → HomogeneousCochain N k ψ →
        HomogeneousCochain N k
          (cubicalWeightedHodgeDirac N w (cubicalWeightedHodgeDirac N w ψ))) := by
  refine ⟨?_, ?_, ?_⟩
  · intro N w hw ψ φ
    exact cubicalWeightedHodgeDirac_pairing_self_adjoint N w hw ψ φ
  · intro N w hw
    exact cubicalWeightedHodgeDirac_square N w hw
  · intro N k w ψ hw hψ
    exact cubicalWeightedHodgeDirac_square_degree_preserving N k w hw ψ hψ

/-- **D0-ARCHIVE-WEIGHTED-HODGE-DIRAC-001 (Owner locator)**:
The currently compiled package records finite counts and a legacy Boolean
flag, and includes the concrete unweighted Hodge-square degree-preservation
application above. The conditional `cubicalWeightedHodgeDirac_application`
constructs `d + d†_w` from the registered cubical differential for an
arbitrary caller-supplied nonzero diagonal profile; positive, canonical, and
geometrically derived weights remain outside this formalization. -/
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
