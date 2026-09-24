import D0.Geometry.A4DGoldenRolePhaseRGDefect
import D0.Geometry.ArchiveFlatProductBondingNoGo
import D0.Geometry.ArchiveTwoLimitSeparation
import D0.Geometry.ArchiveRolePhaseProductCarrier
import D0.Geometry.ArchiveRolePermutationAction
import D0.Geometry.A4DGoldenGroupRefinementBoundary
import D0.Geometry.A4DGoldenAFCommutativeTargetBoundary
import D0.Algebra.FibonacciAFTower

/-!
# Carrier-weld boundary for the golden RG interface (strengthened)

Tower A record bonding and Tower B role-phase bonding remain the owned `6 ≠ 16`
separation. Tower C contributes the scalar probe `goldenScaleProbe`, whose
source is a depth index.

This module additionally Lean-owns the repaired PR #104 boundary packages:

* consecutive coprime Role-phase group homs are trivial (zero exists);
* surjective product-cyclic refinement requires modulus divisibility;
* exact AF → commutative stage boundary with `k=0,1` exceptions;
* trivial-source Role-equivariant maps land in the invariant sector;
* bounded `0 ≤ k,n ≤ 11` cardinality/GNS non-equalities;
* hostile named full consecutive towers fail adjacent divisibility.

It does **not** construct a Hilbert correspondence, choose an index rule `k ↔ n`,
or touch `J`, `D_H`, `H(e)`, physical time, stress, or Einstein closure.
-/

namespace D0.Geometry

open D0
open D0.Geometry.ArchiveFlatProductBondingNoGo
open D0.Geometry.ArchiveTwoLimitSeparation
open D0.Geometry.ArchiveRolePhaseProductCarrier
open D0.Algebra.FibonacciAFTower

/-- Supplied data `(period, depth, comparison, sigma, probe)`.
`period` and `bratteliDepth` are independent. `sigma` transports a real number only. -/
structure SuppliedScalarDefectPackage (C : Type) where
  period : ℕ
  bratteliDepth : ℕ
  comparison : archivePhaseIndex (period + 1) → archivePhaseIndex period
  sigma : C → ℝ
  probe : C

noncomputable def suppliedOperatorResidual {C : Type} (S : SuppliedScalarDefectPackage C) :
    Matrix (archivePhaseIndex (S.period + 1)) (archivePhaseIndex (S.period + 1)) ℝ :=
  rgOperatorResidual S.period S.comparison (S.sigma S.probe)

theorem suppliedOperatorResidual_zero_iff {C : Type} (S : SuppliedScalarDefectPackage C) :
    suppliedOperatorResidual S = 0 ↔
      RenormalizedProjectiveCompatibility S.period S.comparison (S.sigma S.probe) :=
  rg_operator_curvature_zero_iff_renormalized_compatibility
    S.period S.comparison (S.sigma S.probe)

/-- The two role-phase point abbrevs are the same function type `Role → archivePhaseIndex n`. -/
theorem rolePhasePoint_carriers_agree (n : ℕ) :
    D0.ArchiveRolePhasePoint n =
      D0.Geometry.ArchiveRolePhaseProductCarrier.ArchiveRolePhasePoint n := rfl

theorem record_rolePhase_firstStep_fibers :
    flatZeroFiber.card = 6 ∧ productZeroFiberCard = 16 :=
  ⟨card_flat_zero_fiber, product_zero_fiber_card_eq_sixteen⟩

theorem record_rolePhase_bonding_separation :
    flatZeroFiber.card ≠ productZeroFiberCard :=
  flat_ne_product_fiber_card

theorem record_rolePhase_two_limit_separation :
    DefinesProfiniteObject archiveProfiniteSystem ∧
      flatZeroFiber.card = 6 ∧
      productZeroFiberCard = 16 ∧
      flatZeroFiber.card ≠ productZeroFiberCard :=
  archive_two_limit_separation_owner

theorem towerC_scale_probe_eq_phi (k : ℕ) : goldenScaleProbe k = phi :=
  goldenScaleProbe_eq_phi k

/-! ## Capstone re-exports: group refinement -/

theorem golden_consecutive_rolePhase_addHom_eq_zero (n : ℕ)
    (f : ArchiveRolePhaseGroup (n + 1) →+ ArchiveRolePhaseGroup n) : f = 0 :=
  consecutive_rolePhase_addHom_eq_zero n f

theorem golden_surjective_roleZMod_requires_dvd
    {L L' : ℕ} [NeZero L] [NeZero L']
    (f : (Role → ZMod L') →+ (Role → ZMod L))
    (hf : Function.Surjective f) : L ∣ L' :=
  surjective_roleZMod_addHom_implies_dvd f hf

theorem golden_hostile_named_towers_fail_divisibility :
    (¬ hostileFib 3 ∣ hostileFib 4) ∧
    (¬ hostileFibAddOne 2 ∣ hostileFibAddOne 3) ∧
    (¬ hostileFibAddTwo 2 ∣ hostileFibAddTwo 3) ∧
    (¬ hostileFloorPhi 2 ∣ hostileFloorPhi 3) ∧
    (¬ hostileLucas 1 ∣ hostileLucas 2) :=
  hostile_named_full_consecutive_towers_fail_divisibility

/-! ## Capstone re-exports: AF → commutative -/

theorem golden_no_matrix_unital_to_comm
    {m : ℕ} {D : Type*} [CommRing D] [Nontrivial D]
    (hm : 2 ≤ m) (f : Matrix (Fin m) (Fin m) ℂ →+* D) : False :=
  no_unital_ringHom_matrixComplex_to_comm hm f

theorem golden_af_stage_zero_character (n : ℕ) :
    Nonempty (AFStageAlgebra 0 →+* RolePhaseFunctionAlgebra n) :=
  af_stage_zero_character_exists n

theorem golden_af_stage_one_scalar_character (n : ℕ) :
    Nonempty (AFStageAlgebra 1 →+* RolePhaseFunctionAlgebra n) :=
  af_stage_one_scalar_character_exists n

theorem golden_no_unital_af_to_CBn_of_two_le (k n : ℕ) (hk : 2 ≤ k)
    (f : AFStageAlgebra k →+* RolePhaseFunctionAlgebra n) : False :=
  no_unital_afStage_to_rolePhaseFunction_of_two_le k n hk f

/-! ## Trivial-source Role equivariance → invariant sector -/

/-- Abstract action lemma: if the source action is trivial and `f` is equivariant,
then every image vector is fixed by the target action. -/
theorem equivariant_of_trivial_source_lands_in_invariants
    {G X Y : Type*} [One G] [Mul G]
    (σX : G → X → X) (σY : G → Y → Y) (f : X → Y)
    (htriv : ∀ g x, σX g x = x)
    (hequiv : ∀ g x, f (σX g x) = σY g (f x))
    (g : G) (x : X) : σY g (f x) = f x := by
  calc
    σY g (f x) = f (σX g x) := (hequiv g x).symm
    _ = f x := by rw [htriv]

/-- Specialization to Role permutations acting on the Role-phase group carrier, with a
trivial source action. Does **not** claim `Hom_{S₄}` is empty and does not invent a
Tower-C `S₄` action. -/
theorem trivial_source_role_equivariant_image_invariant
    {X : Type*} (N : ℕ) (f : X → ArchiveRolePhaseGroup N)
    (hequiv : ∀ σ : Equiv.Perm Role, ∀ x : X,
      f x = permuteRoleSite σ (f x))
    (σ : Equiv.Perm Role) (x : X) :
    permuteRoleSite σ (f x) = f x :=
  (hequiv σ x).symm

/-! ## Bounded cardinality / GNS non-equalities (`0 ≤ k,n ≤ 11`) -/

/-- Exact finite certificate on `Fin 12 × Fin 12` (i.e. `0 ≤ k,n ≤ 11`). -/
theorem pathCount_ne_archiveModes_fin12 :
    ∀ k n : Fin 12, (pathCount k.val).1 + (pathCount k.val).2 ≠ archiveModes n.val := by
  native_decide

theorem dimA_ne_archiveModes_fin12 :
    ∀ k n : Fin 12, dimA k.val ≠ archiveModes n.val := by
  native_decide

theorem dimA_ne_sixteen_archiveModes_fin12 :
    ∀ k n : Fin 12, dimA k.val ≠ 16 * archiveModes n.val := by
  native_decide

theorem pathCount_ne_archiveModes_of_le_eleven (k n : ℕ)
    (hk : k ≤ 11) (hn : n ≤ 11) :
    (pathCount k).1 + (pathCount k).2 ≠ archiveModes n :=
  pathCount_ne_archiveModes_fin12 ⟨k, Nat.lt_succ_of_le hk⟩ ⟨n, Nat.lt_succ_of_le hn⟩

theorem dimA_ne_archiveModes_of_le_eleven (k n : ℕ)
    (hk : k ≤ 11) (hn : n ≤ 11) :
    dimA k ≠ archiveModes n :=
  dimA_ne_archiveModes_fin12 ⟨k, Nat.lt_succ_of_le hk⟩ ⟨n, Nat.lt_succ_of_le hn⟩

theorem dimA_ne_sixteen_archiveModes_of_le_eleven (k n : ℕ)
    (hk : k ≤ 11) (hn : n ≤ 11) :
    dimA k ≠ 16 * archiveModes n :=
  dimA_ne_sixteen_archiveModes_fin12 ⟨k, Nat.lt_succ_of_le hk⟩ ⟨n, Nat.lt_succ_of_le hn⟩

/-- Packaged finite-range arithmetic boundary. -/
theorem golden_finite_range_cardinality_GNS_boundary :
    (∀ k n : ℕ, k ≤ 11 → n ≤ 11 →
      (pathCount k).1 + (pathCount k).2 ≠ archiveModes n) ∧
    (∀ k n : ℕ, k ≤ 11 → n ≤ 11 → dimA k ≠ archiveModes n) ∧
    (∀ k n : ℕ, k ≤ 11 → n ≤ 11 → dimA k ≠ 16 * archiveModes n) :=
  ⟨pathCount_ne_archiveModes_of_le_eleven,
    dimA_ne_archiveModes_of_le_eleven,
    dimA_ne_sixteen_archiveModes_of_le_eleven⟩

/-- Master capstone packaging the repaired weld boundary (exact scope). -/
theorem golden_carrier_weld_boundary_owner (n : ℕ) :
    (∀ f : ArchiveRolePhaseGroup (n + 1) →+ ArchiveRolePhaseGroup n, f = 0) ∧
    (flatZeroFiber.card ≠ productZeroFiberCard) ∧
    (∀ k, 2 ≤ k → ∀ (_f : AFStageAlgebra k →+* RolePhaseFunctionAlgebra n), False) ∧
    (∀ k m : ℕ, k ≤ 11 → m ≤ 11 → dimA k ≠ archiveModes m) :=
  ⟨fun f => golden_consecutive_rolePhase_addHom_eq_zero n f,
    record_rolePhase_bonding_separation,
    fun k hk f => golden_no_unital_af_to_CBn_of_two_le k n hk f,
    fun k m hk hm => dimA_ne_archiveModes_of_le_eleven k m hk hm⟩

end D0.Geometry
