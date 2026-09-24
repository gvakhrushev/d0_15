import Mathlib.LinearAlgebra.CliffordAlgebra.Contraction
import Mathlib.LinearAlgebra.ExteriorAlgebra.Basis
import Mathlib.LinearAlgebra.ExteriorPower.Basis
import Mathlib.LinearAlgebra.Dual.Defs
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic
import D0.Geometry.ArchiveCARFockCarrier
import D0.Geometry.ArchiveCARRelations
import D0.Geometry.A4DRolePairMetricCarrier
import D0.Geometry.ArchiveRoleEquivalence

/-!
# Exterior lift on the archive CAR carrier

The 16 occupation states are identified with the subset basis of the exterior
algebra on the four-dimensional role space.  The ordered basis uses
`roleOrderIndex`, the same order as the owned Jordan–Wigner CAR matrices.
The frame action is the ordinary exterior-algebra functor `ρ(g) = ⋀ g`.
It is not a Spin representation and it is not a Dirac-spinor representation.
No cell-energy law and no constitutive comparison `C_N` is asserted.
-/

namespace D0.Geometry

open D0
open scoped BigOperators

local instance : LinearOrder Role := LinearOrder.lift' roleCode roleCode_injective

noncomputable section

abbrev RoleSpace := Role → ℝ
abbrev RoleExterior := ExteriorAlgebra ℝ RoleSpace

def archiveFockSupport (s : ArchiveFockState) : Finset Role :=
  Finset.univ.filter fun r => s r

def archiveFockSupportEquiv : ArchiveFockState ≃ Finset Role where
  toFun := archiveFockSupport
  invFun S := fun r => decide (r ∈ S)
  left_inv s := by
    funext r
    simp [archiveFockSupport]
  right_inv S := by
    ext r
    simp [archiveFockSupport]

def archiveRoleBasis : Module.Basis Role ℝ RoleSpace := Pi.basisFun ℝ Role

def archiveFockExteriorBasis : Module.Basis ArchiveFockState ℝ RoleExterior :=
  (archiveRoleBasis.ExteriorAlgebra).reindex archiveFockSupportEquiv.symm

def archiveFockExteriorEquiv : (ArchiveFockState → ℝ) ≃ₗ[ℝ] RoleExterior :=
  (Pi.basisFun ℝ ArchiveFockState).repr.trans archiveFockExteriorBasis.repr.symm

@[simp] theorem archiveFockExteriorEquiv_single (s : ArchiveFockState) :
    archiveFockExteriorEquiv (Pi.single s (1 : ℝ)) = archiveFockExteriorBasis s := by
  unfold archiveFockExteriorEquiv
  simp only [LinearEquiv.trans_apply]
  rw [show Pi.single s (1 : ℝ) = (Pi.basisFun ℝ ArchiveFockState) s by
    ext t
    simp]
  rw [Module.Basis.repr_self]
  simp

/-- The finite-dimensional GL action, transported to the existing 16-state
coefficient carrier. -/
def archiveExteriorFrameLift (L : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) :=
  archiveFockExteriorEquiv.symm.toLinearMap.comp
    ((ExteriorAlgebra.map L.toLinearMap).toLinearMap.comp
      archiveFockExteriorEquiv.toLinearMap)

@[simp] theorem archiveExteriorFrameLift_apply (L : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (v : ArchiveFockState → ℝ) :
    archiveExteriorFrameLift L v =
      archiveFockExteriorEquiv.symm (ExteriorAlgebra.map L.toLinearMap
        (archiveFockExteriorEquiv v)) := rfl

/-- On an occupation basis vector the lift is the induced exterior-algebra map.
Its subset coefficients are therefore the usual minors. -/
theorem archiveExteriorFrameLift_basis (L : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (s : ArchiveFockState) :
    archiveFockExteriorEquiv
      (archiveExteriorFrameLift L (Pi.single s (1 : ℝ))) =
      ExteriorAlgebra.map L.toLinearMap (archiveFockExteriorBasis s) := by
  simp [archiveExteriorFrameLift]

theorem archiveExteriorFrameLift_id :
    archiveExteriorFrameLift (LinearEquiv.refl ℝ RoleSpace) = LinearMap.id := by
  ext v
  simp [archiveExteriorFrameLift, ExteriorAlgebra.map_id]

theorem archiveExteriorFrameLift_comp (L M : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    (archiveExteriorFrameLift L).comp (archiveExteriorFrameLift M) =
      archiveExteriorFrameLift (M.trans L) := by
  apply LinearMap.ext
  intro v
  apply archiveFockExteriorEquiv.injective
  simp [archiveExteriorFrameLift]
  change AlgHom.comp (ExteriorAlgebra.map L.toLinearMap)
      (ExteriorAlgebra.map M.toLinearMap) (archiveFockExteriorEquiv v) =
    ExteriorAlgebra.map (M.trans L).toLinearMap (archiveFockExteriorEquiv v)
  rw [ExteriorAlgebra.map_comp_map M.toLinearMap L.toLinearMap]
  rfl

theorem archiveExteriorFrameLift_inverse (L : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    (archiveExteriorFrameLift L).comp (archiveExteriorFrameLift L.symm) = LinearMap.id ∧
      (archiveExteriorFrameLift L.symm).comp (archiveExteriorFrameLift L) = LinearMap.id := by
  constructor <;> rw [archiveExteriorFrameLift_comp]
  · simpa using archiveExteriorFrameLift_id
  · simpa using archiveExteriorFrameLift_id

/-- Exterior-algebra creator on the transported finite carrier. -/
def archiveExteriorCreator (v : RoleSpace) (ψ : ArchiveFockState → ℝ) :
    ArchiveFockState → ℝ :=
  archiveFockExteriorEquiv.symm
    (ExteriorAlgebra.ι ℝ v * archiveFockExteriorEquiv ψ)

theorem archiveExteriorFrameLift_creator_covariant
    (L : RoleSpace ≃ₗ[ℝ] RoleSpace) (v : RoleSpace)
    (ψ : ArchiveFockState → ℝ) :
    archiveExteriorFrameLift L (archiveExteriorCreator v ψ) =
      archiveExteriorCreator (L v) (archiveExteriorFrameLift L ψ) := by
  apply archiveFockExteriorEquiv.injective
  simp [archiveExteriorCreator, archiveExteriorFrameLift, map_mul]

/-- The canonical dual/exterior-power pairing is invariant when vectors are
transported by `L` and covectors by the contragredient `α ↦ α ∘ L⁻¹`.  This is
the common-fibre duality identity underlying algebraic contraction transport;
it does not identify the dual action with the located placement `J`. -/
theorem archiveExteriorPower_pairingDual_frame_natural (k : ℕ)
    (L : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (α : ⋀[ℝ]^k (Module.Dual ℝ RoleSpace))
    (z : ⋀[ℝ]^k RoleSpace) :
    exteriorPower.pairingDual ℝ RoleSpace k
      (exteriorPower.map k (L.symm.toLinearMap.dualMap) α)
      (exteriorPower.map k L.toLinearMap z) =
    exteriorPower.pairingDual ℝ RoleSpace k α z := by
  let P := exteriorPower.pairingDual ℝ RoleSpace k
  let C := exteriorPower.map k L.toLinearMap
  let D := exteriorPower.map k (L.symm.toLinearMap.dualMap)
  have hmap : C.dualMap.comp (P.comp D) = P := by
    apply LinearMap.ext_on
      (exteriorPower.ιMulti_span ℝ k (Module.Dual ℝ RoleSpace))
    rintro α ⟨f, rfl⟩
    apply LinearMap.ext_on (exteriorPower.ιMulti_span ℝ k RoleSpace)
    rintro z ⟨v, rfl⟩
    simp only [P, C, D, LinearMap.comp_apply, LinearMap.dualMap_apply,
      exteriorPower.map_apply_ιMulti,
      exteriorPower.pairingDual_ιMulti_ιMulti, Function.comp_apply]
    congr 1
    ext i
    simp [LinearEquiv.symm_apply_apply]
  have hα := congrArg (fun F : _ →ₗ[ℝ] _ => F α) hmap
  have hαz := congrArg (fun φ : Module.Dual ℝ (⋀[ℝ]^k RoleSpace) => φ z) hα
  simpa [P, C, D, LinearMap.comp_apply, LinearMap.dualMap_apply] using hαz

theorem archiveFockExteriorBasis_apply (s : ArchiveFockState) :
    archiveFockExteriorBasis s =
    (archiveRoleBasis.ExteriorAlgebra) (archiveFockSupport s) := by
  simp [archiveFockExteriorBasis, archiveFockSupportEquiv]

/-- The actual `k`th compound coefficient of a frame, expressed as the
determinant of the corresponding ordered minor.  The row index is the input
subset and the column index is the output subset under Mathlib's `ιMulti`
convention. -/
def archiveExteriorMinor (k : ℕ) (L : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (S T : Set.powersetCard Role k) : ℝ :=
  (Matrix.of fun i j =>
    archiveRoleBasis.coord (Set.powersetCard.ofFinEmbEquiv.symm T j)
      (L (archiveRoleBasis (Set.powersetCard.ofFinEmbEquiv.symm S i)))).det

theorem archiveExteriorPower_coefficient_minor (k : ℕ)
    (L : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (S T : Set.powersetCard Role k) :
    (archiveRoleBasis.exteriorPower k).repr
      (exteriorPower.map k L.toLinearMap
        (archiveRoleBasis.exteriorPower k S)) T =
      archiveExteriorMinor k L S T := by
  rw [exteriorPower.basis_repr_apply, exteriorPower.basis_apply,
    exteriorPower.map_apply_ιMulti_family]
  unfold exteriorPower.ιMulti_family
  rw [exteriorPower.ιMultiDual_apply_ιMulti]
  rfl

/-- The 16-state frame lift restricts to Mathlib's `k`th exterior-power map.
This is the degree-preservation statement for every homogeneous subset basis
sector, with no larger representation substituted for the archive carrier. -/
theorem archiveExteriorFrameLift_basis_degree (k : ℕ)
    (L : RoleSpace ≃ₗ[ℝ] RoleSpace) (S : Set.powersetCard Role k) :
    archiveFockExteriorEquiv
      (archiveExteriorFrameLift L
        (Pi.single (archiveFockSupportEquiv.symm S.val) (1 : ℝ))) =
      ((exteriorPower.map k L.toLinearMap
        (archiveRoleBasis.exteriorPower k S) : ⋀[ℝ]^k RoleSpace) : RoleExterior) := by
  rw [archiveExteriorFrameLift_basis, archiveFockExteriorBasis_apply]
  simp only [show archiveFockSupport (archiveFockSupportEquiv.symm S.val) = S.val
    from archiveFockSupportEquiv.apply_symm_apply S.val]
  rw [ExteriorAlgebra.basis_eq_coe_basis]
  simp only [exteriorPower.basis_apply, exteriorPower.map_apply_ιMulti_family]
  unfold exteriorPower.ιMulti_family
  simp [ExteriorAlgebra.map_apply_ιMulti, exteriorPower.ιMulti_apply_coe]
  rfl

/-- The homogeneous degree sector of the *existing* coefficient carrier,
identified through its exterior subset basis. -/
def archiveFockDegreeSector (k : ℕ) :
    Submodule ℝ (ArchiveFockState → ℝ) :=
  (ExteriorAlgebra.exteriorPower ℝ k RoleSpace).comap
    archiveFockExteriorEquiv.toLinearMap

theorem exteriorAlgebra_map_preserves_degree (k : ℕ)
    (L : RoleSpace ≃ₗ[ℝ] RoleSpace) (z : RoleExterior)
    (hz : z ∈ ExteriorAlgebra.exteriorPower ℝ k RoleSpace) :
    ExteriorAlgebra.map L.toLinearMap z ∈
      ExteriorAlgebra.exteriorPower ℝ k RoleSpace := by
  rw [← ExteriorAlgebra.ιMulti_span_fixedDegree] at hz ⊢
  induction hz using Submodule.span_induction with
  | mem z hz =>
      rcases hz with ⟨v, rfl⟩
      rw [ExteriorAlgebra.map_apply_ιMulti]
      exact Submodule.subset_span ⟨L.toLinearMap ∘ v, rfl⟩
  | zero => simp
  | add x y _ _ hx hy => simpa using Submodule.add_mem _ hx hy
  | smul c x _ hx => simpa using Submodule.smul_mem _ c hx

theorem archiveExteriorFrameLift_preserves_degree (k : ℕ)
    (L : RoleSpace ≃ₗ[ℝ] RoleSpace) (ψ : ArchiveFockState → ℝ)
    (hψ : ψ ∈ archiveFockDegreeSector k) :
    archiveExteriorFrameLift L ψ ∈ archiveFockDegreeSector k := by
  change archiveFockExteriorEquiv (archiveExteriorFrameLift L ψ) ∈
    ExteriorAlgebra.exteriorPower ℝ k RoleSpace
  simpa [archiveExteriorFrameLift] using
    exteriorAlgebra_map_preserves_degree k L (archiveFockExteriorEquiv ψ) hψ

/-! ## Algebraic contraction and CAR

`C(α)` is Clifford contraction on the zero quadratic form, which is the
exterior algebra.  Together with wedge multiplication it is the CAR pair on
this same carrier.  The covariance `ρ(g) C(α) ρ(g)⁻¹ = C(g⁻ᵀ α)` is the
contragredient of creator covariance.
-/

def archiveExteriorContraction (α : Module.Dual ℝ RoleSpace) :
    (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) :=
  archiveFockExteriorEquiv.symm.toLinearMap.comp
    ((CliffordAlgebra.contractLeft α).comp archiveFockExteriorEquiv.toLinearMap)

theorem exteriorContractLeft_natural (L : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (α : Module.Dual ℝ RoleSpace) (z : RoleExterior) :
    ExteriorAlgebra.map L.toLinearMap (CliffordAlgebra.contractLeft α z) =
      CliffordAlgebra.contractLeft (α.comp L.symm.toLinearMap)
        (ExteriorAlgebra.map L.toLinearMap z) := by
  induction z using CliffordAlgebra.left_induction with
  | algebraMap r =>
      simp [CliffordAlgebra.contractLeft_algebraMap]
  | add x y ihx ihy =>
      simp [map_add, ihx, ihy]
  | ι_mul x m ih =>
      rw [CliffordAlgebra.contractLeft_ι_mul, map_sub, map_smul, map_mul,
        ExteriorAlgebra.map_apply_ι, ih]
      have hα : (α.comp L.symm.toLinearMap) (L m) = α m := by
        simp [LinearMap.comp_apply, LinearEquiv.symm_apply_apply]
      rw [← hα]
      conv_rhs => rw [map_mul, ExteriorAlgebra.map_apply_ι]
      unfold ExteriorAlgebra.ι
      exact (CliffordAlgebra.contractLeft_ι_mul
        (α.comp L.symm.toLinearMap) (L m) (ExteriorAlgebra.map L.toLinearMap x)).symm

theorem archiveExteriorFrameLift_contraction_covariant
    (L : RoleSpace ≃ₗ[ℝ] RoleSpace) (α : Module.Dual ℝ RoleSpace)
    (ψ : ArchiveFockState → ℝ) :
    archiveExteriorFrameLift L (archiveExteriorContraction α ψ) =
      archiveExteriorContraction (α.comp L.symm.toLinearMap)
        (archiveExteriorFrameLift L ψ) := by
  apply archiveFockExteriorEquiv.injective
  convert exteriorContractLeft_natural L α (archiveFockExteriorEquiv ψ) using 1 <;>
    simp [archiveExteriorFrameLift, archiveExteriorContraction, LinearMap.comp_apply,
      LinearEquiv.apply_symm_apply, LinearEquiv.symm_apply_apply]

theorem exterior_ι_anticomm (v w : RoleSpace) :
    ExteriorAlgebra.ι ℝ v * ExteriorAlgebra.ι ℝ w =
      -(ExteriorAlgebra.ι ℝ w * ExteriorAlgebra.ι ℝ v) := by
  have h := CliffordAlgebra.ι_mul_ι_comm (Q := (0 : QuadraticForm ℝ RoleSpace)) v w
  have hp : QuadraticMap.polar (0 : QuadraticForm ℝ RoleSpace) v w = 0 := by
    simp [QuadraticMap.polar]
  rw [hp, map_zero, zero_sub] at h
  exact h

theorem archiveExteriorCreator_anticommute (v w : RoleSpace)
    (ψ : ArchiveFockState → ℝ) :
    archiveExteriorCreator v (archiveExteriorCreator w ψ) +
        archiveExteriorCreator w (archiveExteriorCreator v ψ) = 0 := by
  apply archiveFockExteriorEquiv.injective
  simp only [archiveExteriorCreator, map_add, map_zero, LinearEquiv.apply_symm_apply]
  have h := exterior_ι_anticomm v w
  calc
    ExteriorAlgebra.ι ℝ v * (ExteriorAlgebra.ι ℝ w * archiveFockExteriorEquiv ψ) +
        ExteriorAlgebra.ι ℝ w * (ExteriorAlgebra.ι ℝ v * archiveFockExteriorEquiv ψ) =
      (ExteriorAlgebra.ι ℝ v * ExteriorAlgebra.ι ℝ w) * archiveFockExteriorEquiv ψ +
        (ExteriorAlgebra.ι ℝ w * ExteriorAlgebra.ι ℝ v) * archiveFockExteriorEquiv ψ := by
          rw [mul_assoc, mul_assoc]
    _ = (-(ExteriorAlgebra.ι ℝ w * ExteriorAlgebra.ι ℝ v)) * archiveFockExteriorEquiv ψ +
        (ExteriorAlgebra.ι ℝ w * ExteriorAlgebra.ι ℝ v) * archiveFockExteriorEquiv ψ := by
          rw [h]
    _ = 0 := by
          rw [show (-(ExteriorAlgebra.ι ℝ w * ExteriorAlgebra.ι ℝ v)) *
                archiveFockExteriorEquiv ψ =
              -((ExteriorAlgebra.ι ℝ w * ExteriorAlgebra.ι ℝ v) *
                archiveFockExteriorEquiv ψ) from neg_mul _ _]
          abel

theorem archiveExterior_contraction_creator_car
    (α : Module.Dual ℝ RoleSpace) (v : RoleSpace) (ψ : ArchiveFockState → ℝ) :
    archiveExteriorContraction α (archiveExteriorCreator v ψ) +
        archiveExteriorCreator v (archiveExteriorContraction α ψ) =
      α v • ψ := by
  apply archiveFockExteriorEquiv.injective
  have h := CliffordAlgebra.contractLeft_ι_mul (Q := (0 : QuadraticForm ℝ RoleSpace))
    α v (archiveFockExteriorEquiv ψ)
  have hsum :
      CliffordAlgebra.contractLeft α (ExteriorAlgebra.ι ℝ v * archiveFockExteriorEquiv ψ) +
          ExteriorAlgebra.ι ℝ v * CliffordAlgebra.contractLeft α (archiveFockExteriorEquiv ψ) =
        α v • archiveFockExteriorEquiv ψ := by
    rw [h]
    abel
  convert hsum using 1 <;>
    simp [archiveExteriorContraction, archiveExteriorCreator, map_add, map_smul,
      LinearMap.comp_apply, LinearEquiv.apply_symm_apply, LinearEquiv.symm_apply_apply]

theorem archiveExteriorContraction_anticommute
    (α β : Module.Dual ℝ RoleSpace) (ψ : ArchiveFockState → ℝ) :
    archiveExteriorContraction α (archiveExteriorContraction β ψ) =
      -archiveExteriorContraction β (archiveExteriorContraction α ψ) := by
  apply archiveFockExteriorEquiv.injective
  convert CliffordAlgebra.contractLeft_comm α β (archiveFockExteriorEquiv ψ) using 1 <;>
    simp [archiveExteriorContraction, LinearMap.comp_apply, map_neg,
      LinearEquiv.apply_symm_apply, LinearEquiv.symm_apply_apply]

/-! ## Coordinate CAR matrices

`carCreateEnd` and `carAnnihilateEnd` are the owned Jordan–Wigner matrices as
endomorphisms of the same 16-state carrier.  Their anticommutators are the
theorems in `ArchiveCARRelations`.
-/

def carMatrixEnd (M : ArchiveFockState → ArchiveFockState → ℝ) :
    (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) where
  toFun ψ bra := ∑ ket : ArchiveFockState, M bra ket * ψ ket
  map_add' ψ φ := by
    ext bra
    simp [mul_add, Finset.sum_add_distrib]
  map_smul' c ψ := by
    ext bra
    simp only [Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
    refine Finset.sum_congr rfl ?_
    intro ket _
    simp [RingHom.id_apply, mul_left_comm, mul_assoc]

def carCreateEnd (r : Role) : (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) :=
  carMatrixEnd (carCreate r)

def carAnnihilateEnd (r : Role) : (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) :=
  carMatrixEnd (carAnnihilate r)


end

end D0.Geometry
