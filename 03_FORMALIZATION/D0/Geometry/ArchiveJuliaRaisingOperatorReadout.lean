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

The module now also extracts the grade-one-to-grade-two contraction block of
the same complete query, derives the projected endpoint-metric identity from
Lorentz isometry, and proves the square-root/correction inverse (28) for the
whole affine covector. The canonical Euclidean witness `z=b/(bᵀb)` is built in
the fixed four-role basis and normalized when `b` is nonzero; in the null case,
nondegeneracy and `u≠0` supply that nonzero premise. Endpoint-form hypotheses,
the chart normalization, and the positive branch remain explicit inputs.

This remains a finite-carrier algebraic application of the pinned source. It
does not formalize the source's concrete endpoint `Jx,Jy` realization and
proper-Lorentz constraint as one instantiated package, the non-null gamma
formula (27), its all-jet extension, coframe/metric recovery, the complete
variational pullback, source or price maps, physical admission, or GR selection.
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

private theorem archiveFockExteriorEquiv_contraction
    (α : Module.Dual ℝ RoleSpace) (ψ : ArchiveFockState → ℝ) :
    archiveFockExteriorEquiv (archiveExteriorContraction α ψ) =
      CliffordAlgebra.contractLeft α (archiveFockExteriorEquiv ψ) := by
  simp [archiveExteriorContraction, LinearMap.comp_apply]

private theorem archiveFockExteriorEquiv_creator (u : RoleSpace)
    (ψ : ArchiveFockState → ℝ) :
    archiveFockExteriorEquiv (archiveExteriorCreator u ψ) =
      ι ℝ u * archiveFockExteriorEquiv ψ := by
  simp [archiveExteriorCreator]

/-- CAR contraction obeys the exact contraction-creator relation on the
existing finite carrier. -/
theorem archiveExteriorContraction_creator (α : Module.Dual ℝ RoleSpace)
    (u : RoleSpace) (ψ : ArchiveFockState → ℝ) :
    archiveExteriorContraction α (archiveExteriorCreator u ψ) =
      α u • ψ - archiveExteriorCreator u (archiveExteriorContraction α ψ) := by
  apply archiveFockExteriorEquiv.injective
  rw [archiveFockExteriorEquiv_contraction,
    archiveFockExteriorEquiv_creator,
    CliffordAlgebra.contractLeft_ι_mul]
  simp only [map_sub, map_smul, archiveFockExteriorEquiv_creator,
    archiveFockExteriorEquiv_contraction]

/-- Rank-one map `v ↦ α(v)u`, used to express the exact projected block. -/
def archiveJuliaNullRankOne (u : RoleSpace) (α : Module.Dual ℝ RoleSpace) :
    RoleSpace →ₗ[ℝ] RoleSpace where
  toFun v := α v • u
  map_add' v w := by simp [map_add, add_smul]
  map_smul' c v := by simp [map_smul, smul_smul]

/-- Bundled real bilinear form on the fixed four-role carrier. -/
abbrev ArchiveRoleBilinear := RoleSpace →ₗ[ℝ] (RoleSpace →ₗ[ℝ] ℝ)

/-- The degree-one-to-degree-two contraction block of the actual raising
query. This is `P₁ i_α X P₁` with `X=C†(u)ρ(M)`, read in the existing role
space; the condition `α u = 1` is the source's affine chart normalization. -/
def archiveJuliaNullBlock (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) (α : Module.Dual ℝ RoleSpace) :
    RoleSpace →ₗ[ℝ] RoleSpace :=
  M.toLinearMap - archiveJuliaNullRankOne u (α.comp M.toLinearMap)

theorem archiveJuliaNullBlock_decomposition (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) (α : Module.Dual ℝ RoleSpace)
    (x : RoleSpace) :
    M x = archiveJuliaNullBlock u M α x + α (M x) • u := by
  dsimp [archiveJuliaNullBlock, archiveJuliaNullRankOne]
  abel

/-- In the null case `P(u,u)=0`, nondegeneracy of the endpoint form and
invertibility of `M` make the projected metric covector nonzero whenever
`u` is nonzero. This supplies the existence premise for the source's
Euclidean normalized chart witness. -/
theorem archiveJuliaNullBlock_covector_ne_zero
    (P : ArchiveRoleBilinear) (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) (α : Module.Dual ℝ RoleSpace)
    (hNondegenerate : ∀ x, (∀ y, P x y = 0) → x = 0)
    (hu : u ≠ 0) (hNull : P u u = 0) :
    (P u).comp (archiveJuliaNullBlock u M α) ≠ 0 := by
  intro hbzero
  have hBzero (x : RoleSpace) : P u (archiveJuliaNullBlock u M α x) = 0 := by
    have h := congrArg (fun f : RoleSpace →ₗ[ℝ] ℝ => f x) hbzero
    simpa [LinearMap.comp_apply] using h
  have hMzero (x : RoleSpace) : P u (M x) = 0 := by
    rw [archiveJuliaNullBlock_decomposition u M α x]
    simp only [map_add, map_smul, smul_eq_mul]
    rw [hBzero x, hNull]
    simp
  have hall (y : RoleSpace) : P u y = 0 := by
    simpa using hMzero (M.symm y)
  exact hu (hNondegenerate u hall)

/-- The projected metric identity behind the null chart in Eq. (28). `Pₓ`
and `Pᵧ` are the two endpoint bilinear forms, `M` is their Lorentz isometry,
and `B` is read from the complete CAR/exterior query above. -/
theorem archiveJuliaNullProjectedMetric
    (Pₓ Pᵧ : ArchiveRoleBilinear) (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) (α : Module.Dual ℝ RoleSpace)
    (hSymm : ∀ x y, Pₓ x y = Pₓ y x)
    (hIso : ∀ x y, Pₓ (M x) (M y) = Pᵧ x y) :
    ∀ x y,
      Pᵧ x y -
          Pₓ (archiveJuliaNullBlock u M α x)
            (archiveJuliaNullBlock u M α y) =
        ((Pₓ u).comp (archiveJuliaNullBlock u M α)) x * α (M y) +
          α (M x) * ((Pₓ u).comp (archiveJuliaNullBlock u M α)) y +
          (Pₓ u u) * α (M x) * α (M y) := by
  let B := archiveJuliaNullBlock u M α
  have hdecomp (x : RoleSpace) : M x = B x + α (M x) • u := by
    simpa [B] using archiveJuliaNullBlock_decomposition u M α x
  intro x y
  have hexpand :
      Pₓ (B x + α (M x) • u) (B y + α (M y) • u) =
        Pₓ (B x) (B y) +
          α (M y) * Pₓ (B x) u +
          α (M x) * Pₓ u (B y) +
          α (M x) * α (M y) * Pₓ u u := by
    simp only [map_add, map_smul, LinearMap.add_apply,
      LinearMap.smul_apply, smul_eq_mul]
    ring
  calc
    Pᵧ x y - Pₓ (B x) (B y) =
        Pₓ (M x) (M y) - Pₓ (B x) (B y) := by rw [hIso]
    _ = Pₓ (B x + α (M x) • u) (B y + α (M y) • u) -
        Pₓ (B x) (B y) := by
          nth_rewrite 1 [hdecomp x]
          nth_rewrite 1 [hdecomp y]
          rfl
    _ = ((Pₓ u).comp B) x * α (M y) +
        α (M x) * ((Pₓ u).comp B) y +
        (Pₓ u u) * α (M x) * α (M y) := by
      rw [hexpand, hSymm (B x) u]
      simp only [LinearMap.comp_apply]
      ring

/-- The diagonal scalar of the projected metric remainder, corresponding to
`s = zᵀ S z` in the source's null-chart inverse. -/
def archiveJuliaNullS (S : RoleSpace → RoleSpace → ℝ) (z : RoleSpace) : ℝ :=
  S z z

/-- The positive root used by the null-chart inverse. -/
def archiveJuliaNullD (S : RoleSpace → RoleSpace → ℝ) (q : ℝ)
    (z : RoleSpace) : ℝ :=
  Real.sqrt (1 + q * archiveJuliaNullS S z)

/-- The scalar correction `t=s/(1+d)` in the null-chart inverse. -/
def archiveJuliaNullT (S : RoleSpace → RoleSpace → ℝ) (q : ℝ)
    (z : RoleSpace) : ℝ :=
  archiveJuliaNullS S z / (1 + archiveJuliaNullD S q z)

/-- Coordinate vector corresponding to a covector under the fixed Euclidean
role basis used by the source's `z=b/(bᵀb)` normalization. -/
def archiveJuliaNullCovectorRiesz (b : Module.Dual ℝ RoleSpace) : RoleSpace :=
  fun r => b (archiveRoleBasis r)

/-- Euclidean squared norm of a covector in the fixed role basis. -/
def archiveJuliaNullCovectorNormSq (b : Module.Dual ℝ RoleSpace) : ℝ :=
  ∑ r : Role, (b (archiveRoleBasis r)) ^ 2

/-- The canonical normalized witness `z=b/(bᵀb)` in role coordinates. -/
noncomputable def archiveJuliaNullEuclideanWitness
    (b : Module.Dual ℝ RoleSpace) : RoleSpace :=
  (archiveJuliaNullCovectorNormSq b)⁻¹ • archiveJuliaNullCovectorRiesz b

theorem archiveJuliaNullCovector_coordinates (b : Module.Dual ℝ RoleSpace)
    (v : RoleSpace) :
    b v = ∑ r : Role, v r * b (archiveRoleBasis r) := by
  calc
    b v = b (∑ r : Role, (archiveRoleBasis.repr v r) • archiveRoleBasis r) := by
      rw [archiveRoleBasis.sum_repr]
    _ = ∑ r : Role, v r * b (archiveRoleBasis r) := by
      simp only [map_sum, map_smul, smul_eq_mul, archiveRoleBasis,
        Pi.basisFun_repr]

theorem archiveJuliaNullCovectorNormSq_pos (b : Module.Dual ℝ RoleSpace)
    (hb : b ≠ 0) : 0 < archiveJuliaNullCovectorNormSq b := by
  have hcoeff : ∃ r : Role, b (archiveRoleBasis r) ≠ 0 := by
    by_contra h
    push Not at h
    have hzero : b = 0 := archiveRoleBasis.ext (fun r => by simp [h r])
    exact hb hzero
  rcases hcoeff with ⟨r, hr⟩
  apply Finset.sum_pos'
  · intro s hs
    positivity
  · exact ⟨r, Finset.mem_univ r, sq_pos_of_ne_zero hr⟩

theorem archiveJuliaNullEuclideanWitness_normalized
    (b : Module.Dual ℝ RoleSpace) (hb : b ≠ 0) :
    b (archiveJuliaNullEuclideanWitness b) = 1 := by
  have hcoordinates :
      b (archiveJuliaNullCovectorRiesz b) = archiveJuliaNullCovectorNormSq b := by
    rw [archiveJuliaNullCovector_coordinates]
    simp [archiveJuliaNullCovectorRiesz, archiveJuliaNullCovectorNormSq,
      pow_two]
  have hnorm := archiveJuliaNullCovectorNormSq_pos b hb
  rw [archiveJuliaNullEuclideanWitness, map_smul, hcoordinates,
    smul_eq_mul]
  exact inv_mul_cancel₀ (ne_of_gt hnorm)

/-- Exact algebraic null-chart inversion. If the projected metric remainder
has the Lorentz-isometry form
`S(x,y)=b(x)a(y)+a(x)b(y)+q a(x)a(y)`, then any normalized witness `b(z)=1`
recovers the complete functional `a` by the source's Eq. (28) square-root
and correction formula. -/
theorem archiveJuliaNullReconstructCovector
    (a b : Module.Dual ℝ RoleSpace)
    (S : RoleSpace → RoleSpace → ℝ) (q : ℝ) (z : RoleSpace)
    (hS : ∀ x y, S x y = b x * a y + a x * b y + q * a x * a y)
    (hbz : b z = 1)
    (hbranch : 0 < 1 + q * a z) :
    ∀ x, a x =
      (S x z - b x * archiveJuliaNullT S q z) /
        archiveJuliaNullD S q z := by
  let s := archiveJuliaNullS S z
  let d := archiveJuliaNullD S q z
  let t := archiveJuliaNullT S q z
  have hs : s = 2 * a z + q * a z * a z := by
    dsimp [s, archiveJuliaNullS]
    rw [hS z z, hbz]
    ring
  have hrad : 1 + q * s = (1 + q * a z) ^ 2 := by
    rw [hs]
    ring
  have hd : d = 1 + q * a z := by
    dsimp [d, archiveJuliaNullD]
    rw [hrad, Real.sqrt_sq_eq_abs, abs_of_pos hbranch]
  have hden : 1 + (1 + q * a z) ≠ 0 := by
    nlinarith
  have ht : t = a z := by
    change s / (1 + d) = a z
    rw [hs, hd]
    apply (div_eq_iff hden).2
    ring
  have hdpos : 0 < d := by rw [hd]; exact hbranch
  intro x
  have hcross : S x z = b x * a z + a x + q * a x * a z := by
    rw [hS x z, hbz]
    ring
  have hnum : S x z - b x * t = a x * d := by
    rw [hcross, ht, hd]
    ring
  calc
    a x = (a x * d) / d := by field_simp [ne_of_gt hdpos]
    _ = (S x z - b x * t) / d := by rw [hnum]

/-- Apply the exact scalar inversion to the actual null block read from the
complete raising query, under the endpoint isometry, symmetry and branch
hypotheses. The normalized witness remains an explicit chart input. -/
theorem archiveJuliaNullBlock_reconstructsAffineFunctional
    (Pₓ Pᵧ : ArchiveRoleBilinear) (u z : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) (α : Module.Dual ℝ RoleSpace)
    (hSymm : ∀ x y, Pₓ x y = Pₓ y x)
    (hIso : ∀ x y, Pₓ (M x) (M y) = Pᵧ x y)
    (hbz : ((Pₓ u).comp (archiveJuliaNullBlock u M α)) z = 1)
    (hbranch : 0 < 1 + (Pₓ u u) * α (M z)) :
    ∀ x, α (M x) =
      ((Pᵧ x z - Pₓ (archiveJuliaNullBlock u M α x)
        (archiveJuliaNullBlock u M α z)) -
        ((Pₓ u).comp (archiveJuliaNullBlock u M α)) x *
          archiveJuliaNullT
            (fun v w => Pᵧ v w -
              Pₓ (archiveJuliaNullBlock u M α v)
                (archiveJuliaNullBlock u M α w))
            (Pₓ u u) z) /
        archiveJuliaNullD
          (fun v w => Pᵧ v w -
            Pₓ (archiveJuliaNullBlock u M α v)
              (archiveJuliaNullBlock u M α w))
          (Pₓ u u) z := by
  let B := archiveJuliaNullBlock u M α
  let a : Module.Dual ℝ RoleSpace := α.comp M.toLinearMap
  let b : Module.Dual ℝ RoleSpace := (Pₓ u).comp B
  let q : ℝ := Pₓ u u
  let S : RoleSpace → RoleSpace → ℝ := fun x y => Pᵧ x y - Pₓ (B x) (B y)
  have hS : ∀ x y, S x y = b x * a y + a x * b y + q * a x * a y := by
    intro x y
    have h := archiveJuliaNullProjectedMetric Pₓ Pᵧ u M α hSymm hIso x y
    simpa [S, b, a, q, B, LinearMap.comp_apply]
      using h
  have hnorm : b z = 1 := by simpa [b, B] using hbz
  have hbranch' : 0 < 1 + q * a z := by
    simpa [a, q, LinearMap.comp_apply] using hbranch
  have hrec := archiveJuliaNullReconstructCovector a b S q z hS hnorm hbranch'
  simpa [a, b, q, S, B, archiveJuliaNullS, archiveJuliaNullD,
    archiveJuliaNullT, LinearMap.comp_apply]
    using hrec

theorem archiveJuliaNullBlock_readout (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) (α : Module.Dual ℝ RoleSpace)
    (hαu : α u = 1) (v : RoleSpace) :
    archiveJuliaVacuumVectorReadout
      (archiveExteriorContraction α
        (archiveJuliaRaisingQuery u M
          (archiveExteriorCreator v
            (Pi.single fockVacuumState (1 : ℝ))))) =
      archiveJuliaNullBlock u M α v := by
  let vacuum : ArchiveFockState → ℝ := Pi.single fockVacuumState (1 : ℝ)
  have hframe : archiveExteriorFrameLift M
      (archiveExteriorCreator v vacuum) =
      archiveExteriorCreator (M v) vacuum := by
    rw [archiveExteriorFrameLift_creator_covariant, archiveExteriorFrameLift_vacuum]
  have hquery : archiveJuliaRaisingQuery u M
      (archiveExteriorCreator v vacuum) =
      archiveExteriorCreator u (archiveExteriorCreator (M v) vacuum) := by
    change archiveExteriorCreator u
      (archiveExteriorFrameLift M (archiveExteriorCreator v vacuum)) = _
    rw [hframe]
  have hvacContract : archiveExteriorContraction α vacuum = 0 := by
    apply archiveFockExteriorEquiv.injective
    rw [archiveFockExteriorEquiv_contraction,
      archiveFockExteriorEquiv_single_vacuum]
    simp
  rw [hquery, archiveExteriorContraction_creator,
    archiveExteriorContraction_creator, hvacContract]
  have hcreatorNested :
      archiveExteriorCreator u
        (α (M v) • vacuum - archiveExteriorCreator (M v) 0) =
      α (M v) • archiveExteriorCreator u vacuum := by
    change archiveExteriorCreatorLM u
        (α (M v) • vacuum - archiveExteriorCreator (M v) 0) = _
    rw [map_sub, map_smul]
    simp [archiveExteriorCreatorLM, archiveExteriorCreator]
  rw [hcreatorNested]
  simp only [archiveJuliaVacuumVectorReadout, map_sub, map_smul,
    archiveExteriorCreator_on_vacuum_eq_ι, vacuum]
  rw [ExteriorAlgebra.ι_leftInverse, ExteriorAlgebra.ι_leftInverse, hαu]
  simp [archiveJuliaNullBlock, archiveJuliaNullRankOne, LinearMap.sub_apply,
    LinearMap.comp_apply]

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
