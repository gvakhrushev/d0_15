import D0.Geometry.A4DNilpotentAffineMatterLift

/-!
# Julia raising query: exact vacuum readout on the finite carrier

This is a finite-carrier application of Eq. (26) in the source pinned at
`02_REGISTRY/research/D0_GR_PRIMARY_POSITIVE_CASE.md` and recorded in PR #334,
commit `fe5cf335da04cac14e50407b03f98b96be17dc52`, file
`02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md`.
The exact consumer is §5.1 of
`02_REGISTRY/research/A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md`.

On the existing 16-state carrier, the frame lift fixes the vacuum. The vector
creator built from the owned Jordan--Wigner `carCreateEnd` matrices agrees with
the exterior creator on that vacuum, so applying `ιInv` recovers `u` exactly.
The CAR-based query and the exterior model query have the same vacuum response;
equality of either complete query operators therefore implies equality of
their shifts, for arbitrary linear frame equivalences.

The proved statement covers only this finite-carrier vacuum readout. It does
not formalize the full Lorentz null inverse (28), its all-jet extension,
coframe/metric recovery, the complete variational pullback, source or price
maps, physical admission, or GR selection.
-/

namespace D0.Geometry

open D0
open ExteriorAlgebra
open scoped BigOperators

local instance archiveJuliaRoleLinearOrder : LinearOrder Role :=
  LinearOrder.lift' roleCode roleCode_injective

noncomputable section

/-- Finite-carrier realization of the raising query `C†(u) ρ(M)`. -/
def archiveJuliaRaisingQuery (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) :=
  (archiveExteriorCreatorLM u).comp (archiveExteriorFrameLift M)

/-- The same vector creator built from the repository's owned Jordan--Wigner
creation matrices on the 16-state carrier. -/
def archiveCARVectorCreator (u : RoleSpace) :
    (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) :=
  ∑ r : Role, u r • carCreateEnd r

/-- The CAR realization of the raising query, using the same exterior frame
lift as the model query. -/
def archiveJuliaCARRaisingQuery (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) :=
  (archiveCARVectorCreator u).comp (archiveExteriorFrameLift M)

/-- Read the degree-one vector from a finite-carrier state. -/
def archiveJuliaVacuumVectorReadout (ψ : ArchiveFockState → ℝ) : RoleSpace :=
  ιInv (archiveFockExteriorEquiv ψ)

private theorem carMatrixEnd_apply_single
    (M : ArchiveFockState → ArchiveFockState → ℝ)
    (s : ArchiveFockState) (α : ℝ) :
    carMatrixEnd M (Pi.single s α) = fun bra => M bra s * α := by
  ext bra
  change (∑ ket : ArchiveFockState,
    M bra ket * ((Pi.single s α : ArchiveFockState → ℝ) ket)) = _
  rw [Finset.sum_eq_single s]
  · simp
  · intro ket _ hket
    simp [hket]
  · intro hs
    exact (hs (Finset.mem_univ s)).elim

/-- A Jordan--Wigner creator acting on the vacuum is the corresponding
one-particle occupation state. -/
theorem carCreateEnd_vacuum (r : Role) :
    carCreateEnd r (Pi.single fockVacuumState (1 : ℝ)) =
      Pi.single (fockSingletonState r) (1 : ℝ) := by
  rw [carCreateEnd, carMatrixEnd_apply_single]
  ext bra
  by_cases hbra : bra = fockSingletonState r
  · subst bra
    rw [carCreate_singleton_vacuum]
    simp [roleDelta]
  · have hzero : carCreate r bra fockVacuumState = 0 := by
      by_contra hne
      have hs := carCreate_support r bra fockVacuumState hne
      rcases hs with ⟨hr, _, hother⟩
      apply hbra
      funext s
      by_cases hs : s = r
      · subst s
        simp [fockSingletonState, hr]
      · rw [hother s hs]
        simp [fockVacuumState, fockSingletonState, hs]
    rw [hzero]
    simp [hbra]

/-- On vacuum, the owned CAR vector creator and exterior creator have exactly
the same exterior image. -/
theorem archiveCARVectorCreator_vacuum_exterior (u : RoleSpace) :
    archiveFockExteriorEquiv
        (archiveCARVectorCreator u (Pi.single fockVacuumState (1 : ℝ))) =
      ι ℝ u := by
  have hu : ∑ r : Role, u r • archiveRoleBasis r = u := by
    ext s
    simp only [Finset.sum_apply, Pi.smul_apply, archiveRoleBasis,
      Pi.basisFun_apply]
    rw [Finset.sum_eq_single s]
    · simp
    · intro r _ hrs
      simp [hrs]
    · intro hs
      exact (hs (Finset.mem_univ s)).elim
  calc
    archiveFockExteriorEquiv
        (archiveCARVectorCreator u (Pi.single fockVacuumState (1 : ℝ))) =
      ∑ r : Role, u r • ι ℝ (archiveRoleBasis r) := by
        simp only [archiveCARVectorCreator, LinearMap.sum_apply,
          LinearMap.smul_apply, map_sum, map_smul]
        apply Finset.sum_congr rfl
        intro r hr
        rw [carCreateEnd_vacuum, archiveFockExteriorEquiv_single,
          archiveFockExteriorBasis_apply]
        have hsupp : archiveFockSupport (fockSingletonState r) = {r} := by
          ext s
          simp [archiveFockSupport, fockSingletonState, eq_comm]
        have hcard : ({r} : Finset Role).card = 1 := by simp
        rw [hsupp, ExteriorAlgebra.basis_apply_ofCard archiveRoleBasis hcard]
        have harg :
            archiveRoleBasis ∘ (Set.powersetCard.ofFinEmbEquiv.symm
              (Set.powersetCard.ofCard hcard)) =
              fun _ : Fin 1 => archiveRoleBasis r := by
          funext i
          have hi : i = 0 := Subsingleton.elim _ _
          subst i
          simp [Set.powersetCard.ofFinEmbEquiv_symm_apply,
            Set.powersetCard.ofCard, Finset.orderEmbOfFin_singleton]
        rw [ExteriorAlgebra.ιMulti_family, harg]
        simp [ExteriorAlgebra.ιMulti_apply]
    _ = ι ℝ (∑ r : Role, u r • archiveRoleBasis r) := by
      simp only [map_sum, map_smul]
    _ = ι ℝ u := by rw [hu]

/-- On the vacuum, the CAR-based and exterior-based query implementations
agree exactly on the existing finite carrier. -/
theorem archiveJuliaCARRaisingQuery_vacuum_eq_model (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    archiveJuliaCARRaisingQuery u M (Pi.single fockVacuumState (1 : ℝ)) =
      archiveJuliaRaisingQuery u M (Pi.single fockVacuumState (1 : ℝ)) := by
  apply archiveFockExteriorEquiv.injective
  simp only [archiveJuliaCARRaisingQuery, archiveJuliaRaisingQuery,
    LinearMap.comp_apply]
  rw [archiveExteriorFrameLift_vacuum M 1]
  rw [archiveCARVectorCreator_vacuum_exterior]
  change ι ℝ u = archiveFockExteriorEquiv
    (archiveExteriorCreator u (Pi.single fockVacuumState (1 : ℝ)))
  exact (archiveExteriorCreator_on_vacuum_eq_ι u).symm

/-- The frame lift leaves the vacuum fixed before creation acts. -/
theorem archiveJuliaRaisingQuery_on_vacuum (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    archiveJuliaRaisingQuery u M (Pi.single fockVacuumState (1 : ℝ)) =
      archiveExteriorCreator u (Pi.single fockVacuumState (1 : ℝ)) := by
  change archiveExteriorCreator u
      (archiveExteriorFrameLift M (Pi.single fockVacuumState (1 : ℝ))) = _
  rw [archiveExteriorFrameLift_vacuum]

/-- Exact model form of the vacuum identity `X |0⟩ = C(u) |0⟩` in Eq. (26). -/
theorem archiveJuliaRaisingQuery_vacuum_exterior (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    archiveFockExteriorEquiv
        (archiveJuliaRaisingQuery u M (Pi.single fockVacuumState (1 : ℝ))) =
      ι ℝ u := by
  rw [archiveJuliaRaisingQuery_on_vacuum]
  exact archiveExteriorCreator_on_vacuum_eq_ι u

/-- The exact vector readout of the query's vacuum response is its shift. -/
theorem archiveJuliaVacuumVectorReadout_query (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    archiveJuliaVacuumVectorReadout
        (archiveJuliaRaisingQuery u M (Pi.single fockVacuumState (1 : ℝ))) = u := by
  change ιInv (archiveFockExteriorEquiv
    (archiveJuliaRaisingQuery u M (Pi.single fockVacuumState (1 : ℝ)))) = u
  rw [archiveJuliaRaisingQuery_vacuum_exterior]
  exact ExteriorAlgebra.ι_leftInverse u

/-- The owned-CAR query has the same exact vacuum vector readout. -/
theorem archiveJuliaVacuumVectorReadout_carQuery (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    archiveJuliaVacuumVectorReadout
        (archiveJuliaCARRaisingQuery u M (Pi.single fockVacuumState (1 : ℝ))) = u := by
  rw [archiveJuliaCARRaisingQuery_vacuum_eq_model]
  exact archiveJuliaVacuumVectorReadout_query u M

/-- The complete query operator determines its shift on the finite carrier. -/
theorem archiveJuliaRaisingQuery_shift_injective
    (u v : RoleSpace) (M N : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (h : archiveJuliaRaisingQuery u M = archiveJuliaRaisingQuery v N) :
    u = v := by
  calc
    u = archiveJuliaVacuumVectorReadout
        (archiveJuliaRaisingQuery u M (Pi.single fockVacuumState (1 : ℝ))) :=
          (archiveJuliaVacuumVectorReadout_query u M).symm
    _ = archiveJuliaVacuumVectorReadout
        (archiveJuliaRaisingQuery v N (Pi.single fockVacuumState (1 : ℝ))) := by
          rw [h]
    _ = v := archiveJuliaVacuumVectorReadout_query v N

/-- Equality of the actual CAR-based query operators also determines their
shifts, through the proved vacuum response. -/
theorem archiveJuliaCARRaisingQuery_shift_injective
    (u v : RoleSpace) (M N : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (h : archiveJuliaCARRaisingQuery u M = archiveJuliaCARRaisingQuery v N) :
    u = v := by
  calc
    u = archiveJuliaVacuumVectorReadout
        (archiveJuliaCARRaisingQuery u M (Pi.single fockVacuumState (1 : ℝ))) :=
          (archiveJuliaVacuumVectorReadout_carQuery u M).symm
    _ = archiveJuliaVacuumVectorReadout
        (archiveJuliaCARRaisingQuery v N (Pi.single fockVacuumState (1 : ℝ))) := by
          rw [h]
    _ = v := archiveJuliaVacuumVectorReadout_carQuery v N

end

end D0.Geometry
