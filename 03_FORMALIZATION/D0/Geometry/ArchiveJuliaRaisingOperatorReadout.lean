import D0.Geometry.A4DNilpotentAffineMatterLift

/-!
# Julia raising query: full finite-carrier creator identity

This is a finite-carrier application of Eq. (26) in the published #334 source
at commit `fe5cf335da04cac14e50407b03f98b96be17dc52`, path
`02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md`,
blob `1c8d59e5533b443d9a015dc4512cfbc160ae7e62`, §8.4. Its exact consumer is
§5.1 of `02_REGISTRY/research/A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md`
at the same commit, blob `734e21ae6bc04ff3446ad15858936d417fdd2e55`.

On the existing 16-state carrier, the owned Jordan--Wigner creator agrees with
exterior-algebra left multiplication on every occupation basis state. Linearity
therefore gives equality of the complete creator operators and, after the same
frame lift, equality of the complete CAR and exterior Julia query operators for
arbitrary shifts and linear frame equivalences. The vacuum readout follows as a
special case and applying `ιInv` recovers `u` exactly.

This remains a finite-carrier algebraic application of the pinned source. It
does not formalize the full Lorentz null inverse (28), its all-jet extension,
coframe/metric recovery, the complete variational pullback, source or price
maps, physical admission, or GR selection.
-/

namespace D0.Geometry

open D0
open ExteriorAlgebra
open scoped BigOperators

local instance archiveJuliaRoleLinearOrder : LinearOrder Role :=
  LinearOrder.lift' roleOrderIndex roleOrderIndex_injective

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

private theorem precedingOccupationCount_update (s : ArchiveFockState) (r : Role) :
    precedingOccupationCount (Function.update s r true) r =
      precedingOccupationCount s r := by
  unfold precedingOccupationCount
  congr 1
  ext q
  by_cases hqr : q = r
  · subst q
    simp
  · simp [Function.update_of_ne hqr]

private theorem jwPhase_update (s : ArchiveFockState) (r : Role) :
    jwPhase (Function.update s r true) r = jwPhase s r := by
  unfold jwPhase
  rw [precedingOccupationCount_update]

/-- The owned Jordan--Wigner creator has its expected signed occupation-basis
action on every one of the 16 carrier states.  The sign counts occupied roles
before `r` in the same order used by the exterior basis. -/
theorem carCreateEnd_single_state (r : Role) (s : ArchiveFockState) :
    carCreateEnd r (Pi.single s (1 : ℝ)) =
      if s r = true then 0 else
        jwPhase s r • Pi.single (Function.update s r true) (1 : ℝ) := by
  ext bra
  unfold carCreateEnd
  rw [carMatrixEnd_apply_single]
  by_cases hsr : s r = true
  · simp [carCreate, carAnnihilate, hsr]
  · have hsf : s r = false := by cases h : s r <;> simp_all
    by_cases hbra : bra = Function.update s r true
    · subst bra
      have hcond :
          Function.update s r true r = true ∧ s r = false ∧
            (∀ t : Role, t ≠ r → s t = Function.update s r true t) := by
        refine ⟨by simp, hsf, ?_⟩
        intro t ht
        simp [Function.update_of_ne ht]
      change (if Function.update s r true r = true ∧ s r = false ∧
          (∀ t : Role, t ≠ r → s t = Function.update s r true t)
        then jwPhase (Function.update s r true) r else 0) * 1 = _
      rw [if_pos hcond]
      rw [jwPhase_update]
      simp [hsf]
    · have hnot : ¬ (bra r = true ∧
          (∀ t : Role, t ≠ r → s t = bra t)) := by
        intro h
        apply hbra
        funext t
        by_cases ht : t = r
        · subst t
          simp [Function.update, h.1]
        · simp [Function.update_of_ne ht, h.2 t ht]
      have hz : carCreate r bra s = 0 := by
        change (if bra r = true ∧ s r = false ∧
            (∀ t : Role, t ≠ r → s t = bra t) then jwPhase bra r else 0) = 0
        simp only [hsf, true_and]
        rw [if_neg hnot]
      change carCreate r bra s * 1 = _
      rw [hz]
      simp [hsf, hbra]

private theorem archiveRoleBasis_singleton_exterior (r : Role) :
    (archiveRoleBasis.ExteriorAlgebra) ({r} : Finset Role) =
      ι ℝ (archiveRoleBasis r) := by
  have hcard : ({r} : Finset Role).card = 1 := by simp
  rw [ExteriorAlgebra.basis_apply_ofCard archiveRoleBasis hcard]
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

/-- On the fixed four-role carrier, inserting one mode into the ordered
exterior subset basis has the same sign as the owned Jordan--Wigner phase.
This finite permutation-sign calculation is checked over all role/state pairs. -/
private theorem archiveCreatorPermSign (r : Role) (s : ArchiveFockState)
    (hs : s r = false) :
    (Equiv.Perm.sign (Set.powersetCard.permOfDisjoint
      (m := 1) (n := (archiveFockSupport s).card)
      (s := (⟨{r}, by simp⟩ : Set.powersetCard Role 1))
      (t := (⟨archiveFockSupport s, rfl⟩ :
        Set.powersetCard Role (archiveFockSupport s).card))
      (Finset.disjoint_singleton_left.mpr (by
        simp [archiveFockSupport, hs])))).val = jwSignInt s r := by
  classical
  native_decide +revert

private theorem archiveExteriorBasis_create_step (r : Role)
    (s : ArchiveFockState) (hs : s r = false) :
    ι ℝ (archiveRoleBasis r) * archiveFockExteriorBasis s =
      jwPhase s r • archiveFockExteriorBasis (Function.update s r true) := by
  classical
  let U : Set.powersetCard Role 1 := ⟨{r}, by simp⟩
  let T : Set.powersetCard Role (archiveFockSupport s).card :=
    ⟨archiveFockSupport s, rfl⟩
  have hdis : Disjoint U.val T.val :=
    Finset.disjoint_singleton_left.mpr (by simp [T, archiveFockSupport, hs])
  have hmul := ExteriorAlgebra.basis_mul_of_disjoint archiveRoleBasis U T hdis
  have hsign : (Equiv.Perm.sign
      (Set.powersetCard.permOfDisjoint hdis)).val = jwSignInt s r := by
    simpa [U, T] using archiveCreatorPermSign r s hs
  have hunion :
      (Set.powersetCard.disjUnion hdis : Finset Role) =
        archiveFockSupport (Function.update s r true) := by
    ext q
    simp [U, T, archiveFockSupport, Function.update]
  calc
    ι ℝ (archiveRoleBasis r) * archiveFockExteriorBasis s =
        archiveRoleBasis.ExteriorAlgebra ({r} : Finset Role) *
          archiveRoleBasis.ExteriorAlgebra (archiveFockSupport s) := by
      rw [← archiveRoleBasis_singleton_exterior, archiveFockExteriorBasis_apply]
    _ = Equiv.Perm.sign (Set.powersetCard.permOfDisjoint hdis) •
        archiveRoleBasis.ExteriorAlgebra
          (Set.powersetCard.disjUnion hdis : Finset Role) := by
      simpa [U, T] using hmul
    _ = jwPhase s r • archiveFockExteriorBasis (Function.update s r true) := by
      rw [Units.smul_def, ← Int.cast_smul_eq_zsmul ℝ, hsign,
        ← jwPhase_eq_intCast, hunion, archiveFockExteriorBasis_apply]

/-- The owned CAR creator agrees with exterior-algebra left multiplication on
every occupation basis state of the 16-state carrier. -/
theorem carCreateEnd_exterior_basis (r : Role) (s : ArchiveFockState) :
    archiveFockExteriorEquiv (carCreateEnd r (Pi.single s (1 : ℝ))) =
      ι ℝ (archiveRoleBasis r) * archiveFockExteriorBasis s := by
  classical
  rw [carCreateEnd_single_state]
  by_cases hs : s r = true
  · have hnot : ¬ Disjoint
        ({r} : Finset Role) (archiveFockSupport s) := by
      intro hdis
      have hr : r ∈ archiveFockSupport s := by
        simp [archiveFockSupport, hs]
      exact (Finset.disjoint_left.mp hdis) (by simp) hr
    have hzero : ι ℝ (archiveRoleBasis r) * archiveFockExteriorBasis s = 0 := by
      rw [← archiveRoleBasis_singleton_exterior, archiveFockExteriorBasis_apply]
      simpa using ExteriorAlgebra.basis_mul_of_not_disjoint archiveRoleBasis
        (⟨{r}, by simp⟩ : Set.powersetCard Role 1)
        (⟨archiveFockSupport s, rfl⟩ :
          Set.powersetCard Role (archiveFockSupport s).card) (by
            simpa using hnot)
    simp only [if_pos hs, map_zero]
    exact hzero.symm
  · have hsf : s r = false := by cases h : s r <;> simp_all
    rw [if_neg hs]
    simp only [map_smul, archiveFockExteriorEquiv_single]
    rw [archiveExteriorBasis_create_step r s hsf]

private theorem archiveRoleBasis_weighted_sum (u : RoleSpace) :
    ∑ r : Role, u r • archiveRoleBasis r = u := by
  ext q
  simp only [Finset.sum_apply, Pi.smul_apply, archiveRoleBasis,
    Pi.basisFun_apply]
  rw [Finset.sum_eq_single q]
  · simp
  · intro r _ hrq
    simp [hrq]
  · intro hn
    exact (hn (Finset.mem_univ q)).elim

/-- The CAR vector creator and exterior creator agree on every occupation
basis vector, not only the vacuum. -/
theorem archiveCARVectorCreator_basis_exterior (u : RoleSpace)
    (s : ArchiveFockState) :
    archiveFockExteriorEquiv
        (archiveCARVectorCreator u (Pi.single s (1 : ℝ))) =
      ι ℝ u * archiveFockExteriorBasis s := by
  have huι : ∑ r : Role, u r • ι ℝ (archiveRoleBasis r) = ι ℝ u := by
    calc
      ∑ r : Role, u r • ι ℝ (archiveRoleBasis r) =
          ι ℝ (∑ r : Role, u r • archiveRoleBasis r) := by
        simp only [map_sum, map_smul]
      _ = ι ℝ u := by rw [archiveRoleBasis_weighted_sum]
  calc
    archiveFockExteriorEquiv
        (archiveCARVectorCreator u (Pi.single s (1 : ℝ))) =
        ∑ r : Role, u r •
          archiveFockExteriorEquiv (carCreateEnd r (Pi.single s (1 : ℝ))) := by
      simp only [archiveCARVectorCreator, LinearMap.sum_apply,
        LinearMap.smul_apply, map_sum, map_smul]
    _ = ∑ r : Role, u r •
        (ι ℝ (archiveRoleBasis r) * archiveFockExteriorBasis s) := by
      apply Finset.sum_congr rfl
      intro r hr
      rw [carCreateEnd_exterior_basis]
    _ = (∑ r : Role, u r • ι ℝ (archiveRoleBasis r)) *
        archiveFockExteriorBasis s := by
      rw [Finset.sum_mul]
      apply Finset.sum_congr rfl
      intro r hr
      simp only [smul_mul_assoc]
    _ = ι ℝ u * archiveFockExteriorBasis s := by rw [huι]

/-- Equality of the CAR and exterior vector creators as linear operators on the
entire existing 16-state coefficient carrier. -/
theorem archiveCARVectorCreator_eq_archiveExteriorCreatorLM (u : RoleSpace) :
    archiveCARVectorCreator u = archiveExteriorCreatorLM u := by
  classical
  apply LinearMap.ext
  intro ψ
  have hrepr : ψ = ∑ s : ArchiveFockState, ψ s • Pi.single s (1 : ℝ) := by
    ext t
    simp [Finset.sum_apply, Pi.smul_apply, Pi.single_apply]
  rw [hrepr]
  simp only [map_sum, map_smul]
  apply Finset.sum_congr rfl
  intro s hs
  have hbasis : archiveCARVectorCreator u (Pi.single s (1 : ℝ)) =
      archiveExteriorCreatorLM u (Pi.single s (1 : ℝ)) := by
    apply archiveFockExteriorEquiv.injective
    rw [archiveCARVectorCreator_basis_exterior]
    simp [archiveExteriorCreatorLM, archiveExteriorCreator,
      archiveFockExteriorEquiv_single]
  exact congrArg (fun v => ψ s • v) hbasis

/-- With the same frame lift, the CAR and exterior Julia queries are identical
as operators on the full existing finite carrier. -/
theorem archiveJuliaCARRaisingQuery_eq_model (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    archiveJuliaCARRaisingQuery u M = archiveJuliaRaisingQuery u M := by
  change (archiveCARVectorCreator u).comp (archiveExteriorFrameLift M) =
    (archiveExteriorCreatorLM u).comp (archiveExteriorFrameLift M)
  rw [archiveCARVectorCreator_eq_archiveExteriorCreatorLM]

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
  have hvac : archiveFockExteriorBasis fockVacuumState = 1 := by
    rw [archiveFockExteriorBasis_apply, archiveFockSupport_vacuum,
      archiveRoleBasis_ExteriorAlgebra_empty]
  rw [archiveCARVectorCreator_basis_exterior, hvac, mul_one]

/-- On the vacuum, the CAR-based and exterior-based query implementations
agree exactly on the existing finite carrier. -/
theorem archiveJuliaCARRaisingQuery_vacuum_eq_model (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    archiveJuliaCARRaisingQuery u M (Pi.single fockVacuumState (1 : ℝ)) =
      archiveJuliaRaisingQuery u M (Pi.single fockVacuumState (1 : ℝ)) := by
  exact congrArg (fun Q => Q (Pi.single fockVacuumState (1 : ℝ)))
    (archiveJuliaCARRaisingQuery_eq_model u M)

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
