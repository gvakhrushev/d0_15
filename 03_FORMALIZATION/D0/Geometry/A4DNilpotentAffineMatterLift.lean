import Mathlib.Tactic
import D0.Geometry.ArchiveExteriorFrameLift
import D0.Geometry.ArchiveCARRelations

/-!
# Channel B: nilpotent affine matter lift on the 16-state carrier

Lean-owns the PR #109 nilpotent affine translation response
`T_b = I + C†(b) P₀`, `R_nil(L,b) = T_b ρ(L)` on the 16-state carrier,
with grading firewall. No κ / finite E dressing / B-E letter claims.
-/

namespace D0.Geometry

open D0
open ExteriorAlgebra

local instance nilpotentAffineRoleLinearOrder : LinearOrder Role :=
  LinearOrder.lift' roleCode roleCode_injective

set_option linter.unusedSimpArgs false

noncomputable section

/-- Rank-one vacuum projector `P₀ = |0⟩⟨0|`. -/
def vacuumProjector : (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) where
  toFun ψ := Pi.single fockVacuumState (ψ fockVacuumState)
  map_add' ψ φ := by
    ext s; by_cases h : s = fockVacuumState <;> simp [h, Pi.add_apply]
  map_smul' c ψ := by
    ext s; by_cases h : s = fockVacuumState <;> simp [h, Pi.smul_apply, smul_eq_mul]

@[simp] theorem vacuumProjector_apply (ψ : ArchiveFockState → ℝ) :
    vacuumProjector ψ = Pi.single fockVacuumState (ψ fockVacuumState) := rfl

theorem archiveFockSupport_vacuum :
    archiveFockSupport fockVacuumState = (∅ : Finset Role) := by
  ext r; simp [archiveFockSupport, fockVacuumState]

theorem archiveRoleBasis_ExteriorAlgebra_empty :
    (archiveRoleBasis.ExteriorAlgebra) (∅ : Finset Role) = (1 : RoleExterior) := by
  rw [ExteriorAlgebra.basis_apply, ιMulti_family]
  exact ExteriorAlgebra.ιMulti_zero_apply _

theorem archiveFockExteriorEquiv_single_vacuum (α : ℝ) :
    archiveFockExteriorEquiv (Pi.single fockVacuumState α) =
      algebraMap ℝ RoleExterior α := by
  have h1 : archiveFockExteriorEquiv (Pi.single fockVacuumState (1 : ℝ)) = (1 : RoleExterior) := by
    rw [archiveFockExteriorEquiv_single, archiveFockExteriorBasis_apply,
      archiveFockSupport_vacuum, archiveRoleBasis_ExteriorAlgebra_empty]
  have hα : Pi.single fockVacuumState α = α • Pi.single fockVacuumState (1 : ℝ) := by
    ext t; by_cases ht : t = fockVacuumState <;> simp [ht, Pi.smul_apply]
  rw [hα, map_smul, h1, Algebra.algebraMap_eq_smul_one]

@[simp] theorem algebraMapInv_ι (v : RoleSpace) : algebraMapInv (ι ℝ v) = (0 : ℝ) := by
  simp [algebraMapInv, ExteriorAlgebra.lift_ι_apply]

theorem algebraMapInv_ι_mul (v : RoleSpace) (z : RoleExterior) :
    algebraMapInv (ι ℝ v * z) = 0 := by
  rw [map_mul, algebraMapInv_ι, zero_mul]

theorem archiveFockExteriorEquiv_symm_basis (s : ArchiveFockState) :
    archiveFockExteriorEquiv.symm (archiveFockExteriorBasis s) = Pi.single s (1 : ℝ) :=
  (LinearEquiv.symm_apply_eq _).2 (archiveFockExteriorEquiv_single s).symm

theorem algebraMapInv_ιMulti_pos {n : ℕ} (hn : 0 < n) (v : Fin n → RoleSpace) :
    algebraMapInv (ExteriorAlgebra.ιMulti ℝ n v) = 0 := by
  cases n with
  | zero => exact (lt_irrefl _ hn).elim
  | succ n => rw [ExteriorAlgebra.ιMulti_succ_apply, algebraMapInv_ι_mul]

theorem algebraMapInv_exteriorBasis (S : Finset Role) :
    algebraMapInv ((archiveRoleBasis.ExteriorAlgebra) S) =
      if S = ∅ then (1 : ℝ) else 0 := by
  by_cases hS : S = ∅
  · subst hS; simp [archiveRoleBasis_ExteriorAlgebra_empty]
  · have hpos : 0 < S.card := Finset.card_pos.mpr (Finset.nonempty_of_ne_empty hS)
    rw [if_neg hS, ExteriorAlgebra.basis_apply, ιMulti_family]
    exact algebraMapInv_ιMulti_pos hpos _

theorem vacuum_coeff_eq_algebraMapInv (z : RoleExterior) :
    archiveFockExteriorEquiv.symm z fockVacuumState = algebraMapInv z := by
  classical
  have hbasis : ∀ s : ArchiveFockState,
      archiveFockExteriorEquiv.symm (archiveFockExteriorBasis s) fockVacuumState =
        algebraMapInv (archiveFockExteriorBasis s) := by
    intro s
    rw [archiveFockExteriorEquiv_symm_basis, archiveFockExteriorBasis_apply,
      algebraMapInv_exteriorBasis]
    by_cases hs : s = fockVacuumState
    · subst hs; simp [archiveFockSupport_vacuum]
    · have hsup : archiveFockSupport s ≠ ∅ := by
        intro hempty; apply hs; funext r
        have hmem : r ∈ archiveFockSupport s ↔ False := by simp [hempty]
        have hr : ¬ s r := by simpa [archiveFockSupport] using hmem
        simp [fockVacuumState, hr]
      have hcoeff : (Pi.single s (1 : ℝ) : ArchiveFockState → ℝ) fockVacuumState = 0 :=
        Pi.single_eq_of_ne (Ne.symm hs) 1
      simp [hcoeff, hsup]
  have hz := (archiveFockExteriorBasis.sum_repr z).symm
  rw [hz, map_sum, Finset.sum_apply, map_sum]
  refine Finset.sum_congr rfl fun s _ => ?_
  simp only [map_smul, Pi.smul_apply, smul_eq_mul, hbasis]

theorem archiveExteriorCreator_vacuum_coeff (v : RoleSpace) (ψ : ArchiveFockState → ℝ) :
    archiveExteriorCreator v ψ fockVacuumState = 0 := by
  change archiveFockExteriorEquiv.symm (ι ℝ v * archiveFockExteriorEquiv ψ)
    fockVacuumState = 0
  rw [vacuum_coeff_eq_algebraMapInv, algebraMapInv_ι_mul]

def archiveExteriorCreatorLM (b : RoleSpace) :
    (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) where
  toFun := archiveExteriorCreator b
  map_add' ψ φ := by
    refine archiveFockExteriorEquiv.injective ?_
    simp [archiveExteriorCreator, map_add, mul_add]
  map_smul' c ψ := by
    refine archiveFockExteriorEquiv.injective ?_
    simp [archiveExteriorCreator, map_smul, mul_smul_comm]

theorem archiveExteriorCreatorLM_add (b c : RoleSpace) :
    archiveExteriorCreatorLM (b + c) =
      archiveExteriorCreatorLM b + archiveExteriorCreatorLM c := by
  apply LinearMap.ext; intro ψ
  refine archiveFockExteriorEquiv.injective ?_
  simp [archiveExteriorCreatorLM, archiveExteriorCreator, map_add, add_mul, LinearMap.add_apply]

theorem archiveExteriorCreatorLM_zero :
    archiveExteriorCreatorLM (0 : RoleSpace) = 0 := by
  apply LinearMap.ext; intro ψ
  change archiveExteriorCreator (0 : RoleSpace) ψ = 0
  refine archiveFockExteriorEquiv.injective ?_
  simp [archiveExteriorCreator]

/-- `N_b = C†(b) P₀`. -/
def nilpotentAffineGenerator (b : RoleSpace) :
    (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) :=
  (archiveExteriorCreatorLM b).comp vacuumProjector

/-- `T_b = I + N_b`. -/
def nilpotentAffineTranslation (b : RoleSpace) :
    (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) :=
  LinearMap.id + nilpotentAffineGenerator b

/-- `R_nil(L,b) = T_b ρ(L)`. -/
def nilpotentAffineRep (L : RoleSpace ≃ₗ[ℝ] RoleSpace) (b : RoleSpace) :
    (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) :=
  (nilpotentAffineTranslation b).comp (archiveExteriorFrameLift L)

theorem nilpotentAffineGenerator_apply (b : RoleSpace) (ψ : ArchiveFockState → ℝ) :
    nilpotentAffineGenerator b ψ =
      archiveExteriorCreator b (Pi.single fockVacuumState (ψ fockVacuumState)) := rfl

theorem nilpotentAffineGenerator_zero :
    nilpotentAffineGenerator (0 : RoleSpace) = 0 := by
  simp [nilpotentAffineGenerator, archiveExteriorCreatorLM_zero]

theorem nilpotentAffineGenerator_add (b c : RoleSpace) :
    nilpotentAffineGenerator (b + c) =
      nilpotentAffineGenerator b + nilpotentAffineGenerator c := by
  simp only [nilpotentAffineGenerator, archiveExteriorCreatorLM_add, LinearMap.add_comp]

/-- Mandatory 1: `N_b N_c = 0`. -/
theorem nilpotentAffineGenerator_mul_eq_zero (b c : RoleSpace) :
    (nilpotentAffineGenerator b).comp (nilpotentAffineGenerator c) = 0 := by
  apply LinearMap.ext; intro ψ
  simp only [LinearMap.comp_apply, LinearMap.zero_apply, nilpotentAffineGenerator]
  have hkill : vacuumProjector (archiveExteriorCreatorLM c (vacuumProjector ψ)) = 0 := by
    funext t
    by_cases ht : t = fockVacuumState
    · subst ht
      change archiveExteriorCreator c (vacuumProjector ψ) fockVacuumState = 0
      exact archiveExteriorCreator_vacuum_coeff _ _
    · simp [vacuumProjector_apply, Pi.single_eq_of_ne ht]
  rw [hkill, map_zero]

/-- Mandatory 2a: `T_b T_c = T_{b+c}`. -/
theorem nilpotentAffineTranslation_mul (b c : RoleSpace) :
    (nilpotentAffineTranslation b).comp (nilpotentAffineTranslation c) =
      nilpotentAffineTranslation (b + c) := by
  apply LinearMap.ext; intro ψ
  have hnil : nilpotentAffineGenerator b (nilpotentAffineGenerator c ψ) = 0 :=
    congrArg (fun F : _ →ₗ[ℝ] _ => F ψ) (nilpotentAffineGenerator_mul_eq_zero b c)
  have hadd :
      nilpotentAffineGenerator (b + c) ψ =
        nilpotentAffineGenerator b ψ + nilpotentAffineGenerator c ψ :=
    congrArg (fun F : _ →ₗ[ℝ] _ => F ψ) (nilpotentAffineGenerator_add b c)
  simp only [nilpotentAffineTranslation, LinearMap.comp_apply, LinearMap.add_apply,
    LinearMap.id_apply, hnil, add_zero]
  have hlin : nilpotentAffineGenerator b (ψ + nilpotentAffineGenerator c ψ) =
      nilpotentAffineGenerator b ψ + nilpotentAffineGenerator b (nilpotentAffineGenerator c ψ) :=
    map_add _ _ _
  rw [hlin, hnil, add_zero, hadd]
  ac_rfl

/-- Mandatory 2b: `T_b⁻¹ = T_{-b}`. -/
theorem nilpotentAffineTranslation_zero :
    nilpotentAffineTranslation (0 : RoleSpace) = LinearMap.id := by
  simp [nilpotentAffineTranslation, nilpotentAffineGenerator_zero]

theorem nilpotentAffineTranslation_inverse (b : RoleSpace) :
    (nilpotentAffineTranslation b).comp (nilpotentAffineTranslation (-b)) = LinearMap.id ∧
      (nilpotentAffineTranslation (-b)).comp (nilpotentAffineTranslation b) = LinearMap.id := by
  constructor
  · rw [nilpotentAffineTranslation_mul, add_neg_cancel, nilpotentAffineTranslation_zero]
  · rw [nilpotentAffineTranslation_mul, neg_add_cancel, nilpotentAffineTranslation_zero]

theorem archiveExteriorFrameLift_vacuum (L : RoleSpace ≃ₗ[ℝ] RoleSpace) (α : ℝ) :
    archiveExteriorFrameLift L (Pi.single fockVacuumState α) =
      Pi.single fockVacuumState α := by
  refine archiveFockExteriorEquiv.injective ?_
  simp [archiveExteriorFrameLift_apply, archiveFockExteriorEquiv_single_vacuum]

theorem algebraMapInv_comp_map (L : RoleSpace ≃ₗ[ℝ] RoleSpace) (z : RoleExterior) :
    algebraMapInv (ExteriorAlgebra.map L.toLinearMap z) = algebraMapInv z := by
  refine ExteriorAlgebra.induction
    (C := fun w => algebraMapInv (ExteriorAlgebra.map L.toLinearMap w) = algebraMapInv w)
    (fun r => by simp [algebraMapInv])
    (fun v => by simp [algebraMapInv, ExteriorAlgebra.map_apply_ι, ExteriorAlgebra.lift_ι_apply])
    (fun a b ha hb => by simp [map_mul, ha, hb])
    (fun a b ha hb => by simp [map_add, ha, hb]) z

theorem archiveExteriorFrameLift_vacuum_coeff (L : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (ψ : ArchiveFockState → ℝ) :
    archiveExteriorFrameLift L ψ fockVacuumState = ψ fockVacuumState := by
  change archiveFockExteriorEquiv.symm
      (ExteriorAlgebra.map L.toLinearMap (archiveFockExteriorEquiv ψ)) fockVacuumState =
    ψ fockVacuumState
  rw [vacuum_coeff_eq_algebraMapInv, algebraMapInv_comp_map]
  simpa [LinearEquiv.symm_apply_apply] using
    (vacuum_coeff_eq_algebraMapInv (archiveFockExteriorEquiv ψ)).symm

theorem vacuumProjector_conjugate (L : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    (archiveExteriorFrameLift L).comp
        (vacuumProjector.comp (archiveExteriorFrameLift L.symm)) =
      vacuumProjector := by
  apply LinearMap.ext; intro ψ; funext s
  simp only [LinearMap.comp_apply, vacuumProjector_apply,
    archiveExteriorFrameLift_vacuum_coeff, archiveExteriorFrameLift_vacuum]

theorem nilpotentAffineGenerator_conjugate (L : RoleSpace ≃ₗ[ℝ] RoleSpace) (b : RoleSpace) :
    (archiveExteriorFrameLift L).comp
        ((nilpotentAffineGenerator b).comp (archiveExteriorFrameLift L.symm)) =
      nilpotentAffineGenerator (L b) := by
  apply LinearMap.ext; intro ψ
  change archiveExteriorFrameLift L
      (archiveExteriorCreator b (vacuumProjector (archiveExteriorFrameLift L.symm ψ))) =
    archiveExteriorCreator (L b) (vacuumProjector ψ)
  rw [archiveExteriorFrameLift_creator_covariant]
  congr 1
  exact LinearMap.congr_fun (vacuumProjector_conjugate L) ψ

/-- Mandatory 3: `ρ(L) T_b ρ(L)⁻¹ = T_{L b}`. -/
theorem nilpotentAffineTranslation_covariant (L : RoleSpace ≃ₗ[ℝ] RoleSpace) (b : RoleSpace) :
    (archiveExteriorFrameLift L).comp
        ((nilpotentAffineTranslation b).comp (archiveExteriorFrameLift L.symm)) =
      nilpotentAffineTranslation (L b) := by
  apply LinearMap.ext; intro ψ
  have hid : archiveExteriorFrameLift L (archiveExteriorFrameLift L.symm ψ) = ψ :=
    LinearMap.congr_fun (archiveExteriorFrameLift_inverse L).1 ψ
  have hN := LinearMap.congr_fun (nilpotentAffineGenerator_conjugate L b) ψ
  simp only [nilpotentAffineTranslation, LinearMap.comp_apply, LinearMap.add_apply,
    LinearMap.id_apply, map_add, hid]
  exact congrArg (fun z => ψ + z) hN

private theorem frameLift_commute_translation (L : RoleSpace ≃ₗ[ℝ] RoleSpace) (c : RoleSpace) :
    (archiveExteriorFrameLift L).comp (nilpotentAffineTranslation c) =
      (nilpotentAffineTranslation (L c)).comp (archiveExteriorFrameLift L) := by
  have hcov := nilpotentAffineTranslation_covariant L c
  have hR := (archiveExteriorFrameLift_inverse L).2
  apply LinearMap.ext; intro ψ
  have h := LinearMap.congr_fun hcov (archiveExteriorFrameLift L ψ)
  simp only [LinearMap.comp_apply] at h ⊢
  have hψ : archiveExteriorFrameLift L.symm (archiveExteriorFrameLift L ψ) = ψ :=
    LinearMap.congr_fun hR ψ
  rw [hψ] at h
  exact h

/-- Mandatory 4: semidirect law matching `archiveExteriorFrameLift_comp`. -/
theorem nilpotentAffineRep_mul (L M : RoleSpace ≃ₗ[ℝ] RoleSpace) (b c : RoleSpace) :
    (nilpotentAffineRep L b).comp (nilpotentAffineRep M c) =
      nilpotentAffineRep (M.trans L) (b + L c) := by
  apply LinearMap.ext; intro ψ
  simp only [nilpotentAffineRep, LinearMap.comp_apply]
  have hmid := LinearMap.congr_fun (frameLift_commute_translation L c)
    (archiveExteriorFrameLift M ψ)
  simp only [LinearMap.comp_apply] at hmid
  rw [hmid]
  have hT := LinearMap.congr_fun (nilpotentAffineTranslation_mul b (L c))
    (archiveExteriorFrameLift L (archiveExteriorFrameLift M ψ))
  simp only [LinearMap.comp_apply] at hT
  rw [hT]
  have hρ := LinearMap.congr_fun (archiveExteriorFrameLift_comp L M) ψ
  simp only [LinearMap.comp_apply] at hρ
  rw [hρ]

/-- Concrete nonzero Role-basis shift `b = e_A`. -/
def nilpotentWitnessShift : RoleSpace := Pi.single A (1 : ℝ)

theorem nilpotentWitnessShift_ne_zero : nilpotentWitnessShift ≠ 0 := by
  intro h
  have := congrArg (fun v : RoleSpace => v A) h
  simp [nilpotentWitnessShift] at this

theorem archiveExteriorCreator_on_vacuum_eq_ι (b : RoleSpace) :
    archiveFockExteriorEquiv
        (archiveExteriorCreator b (Pi.single fockVacuumState (1 : ℝ))) =
      ι ℝ b := by
  simp only [archiveExteriorCreator, LinearEquiv.apply_symm_apply,
    archiveFockExteriorEquiv_single_vacuum]
  exact mul_one _

/-- Mandatory 5: vacuum witness. -/
theorem nilpotentAffineTranslation_vacuum (b : RoleSpace) :
    nilpotentAffineTranslation b (Pi.single fockVacuumState (1 : ℝ)) =
      Pi.single fockVacuumState (1 : ℝ) +
        archiveExteriorCreator b (Pi.single fockVacuumState (1 : ℝ)) := by
  simp [nilpotentAffineTranslation, LinearMap.add_apply, nilpotentAffineGenerator_apply]

theorem nilpotentAffineTranslation_ne_id (b : RoleSpace) (hb : b ≠ 0) :
    nilpotentAffineTranslation b ≠ LinearMap.id := by
  intro h
  have hv := LinearMap.congr_fun h (Pi.single fockVacuumState (1 : ℝ))
  rw [nilpotentAffineTranslation_vacuum, LinearMap.id_apply] at hv
  have hcrea :
      archiveExteriorCreator b (Pi.single fockVacuumState (1 : ℝ)) = 0 :=
    add_eq_left.mp hv
  have hι : ι ℝ b = 0 := by
    rw [← archiveExteriorCreator_on_vacuum_eq_ι, hcrea, map_zero]
  exact hb ((ExteriorAlgebra.ι_eq_zero_iff b).1 hι)

theorem nilpotentAffineTranslation_witness_ne_id :
    nilpotentAffineTranslation nilpotentWitnessShift ≠ LinearMap.id :=
  nilpotentAffineTranslation_ne_id _ nilpotentWitnessShift_ne_zero

theorem fockDegree_vacuum_eq_zero : fockDegree fockVacuumState = 0 := by
  simp [fockDegree, fockVacuumState]

/-- Mandatory 6: degree-mixing via `ιInv` of the pure-shift response. -/
theorem nilpotentAffineTranslation_mixes_degree :
    let ψ := nilpotentAffineTranslation nilpotentWitnessShift
      (Pi.single fockVacuumState (1 : ℝ))
    let δ := ψ - Pi.single fockVacuumState (1 : ℝ)
    δ ≠ 0 ∧
      ιInv (archiveFockExteriorEquiv δ) = nilpotentWitnessShift ∧
      nilpotentWitnessShift ≠ 0 ∧
      fockDegree fockVacuumState = 0 := by
  refine ⟨?_, ?_, nilpotentWitnessShift_ne_zero, fockDegree_vacuum_eq_zero⟩
  · intro h0
    have hδ : archiveExteriorCreator nilpotentWitnessShift
        (Pi.single fockVacuumState (1 : ℝ)) = 0 := by
      simpa [nilpotentAffineTranslation_vacuum] using h0
    have hι : ι ℝ nilpotentWitnessShift = 0 := by
      rw [← archiveExteriorCreator_on_vacuum_eq_ι, hδ, map_zero]
    exact nilpotentWitnessShift_ne_zero ((ExteriorAlgebra.ι_eq_zero_iff _).1 hι)
  · have hδ :
        (nilpotentAffineTranslation nilpotentWitnessShift
            (Pi.single fockVacuumState (1 : ℝ)) -
          Pi.single fockVacuumState (1 : ℝ)) =
          archiveExteriorCreator nilpotentWitnessShift
            (Pi.single fockVacuumState (1 : ℝ)) := by
      simp [nilpotentAffineTranslation_vacuum]
    rw [hδ, archiveExteriorCreator_on_vacuum_eq_ι]
    exact ExteriorAlgebra.ι_leftInverse _

def PreservesArchiveFockDegrees
    (F : (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ)) : Prop :=
  ∀ k : ℕ, ∀ ψ : ArchiveFockState → ℝ,
    ψ ∈ archiveFockDegreeSector k → F ψ ∈ archiveFockDegreeSector k

theorem nilpotentAffineGenerator_vacuum_ne_zero (b : RoleSpace) (hb : b ≠ 0) :
    nilpotentAffineGenerator b (Pi.single fockVacuumState (1 : ℝ)) ≠ 0 := by
  intro h
  have hι : ι ℝ b = 0 := by
    have := congrArg archiveFockExteriorEquiv h
    simpa [nilpotentAffineGenerator_apply, archiveExteriorCreator_on_vacuum_eq_ι,
      map_zero] using this
  exact hb ((ExteriorAlgebra.ι_eq_zero_iff b).1 hι)


/-- Creation from the vacuum is a literal degree-one exterior vector. -/
theorem archiveExteriorCreator_vacuum_mem_degree_one (b : RoleSpace) :
    archiveExteriorCreator b (Pi.single fockVacuumState (1 : ℝ)) ∈
      archiveFockDegreeSector 1 := by
  change archiveFockExteriorEquiv
      (archiveExteriorCreator b (Pi.single fockVacuumState (1 : ℝ))) ∈
    ExteriorAlgebra.exteriorPower ℝ 1 RoleSpace
  rw [archiveExteriorCreator_on_vacuum_eq_ι]
  change ExteriorAlgebra.ι ℝ b ∈
    (LinearMap.range (ExteriorAlgebra.ι ℝ : RoleSpace →ₗ[ℝ] RoleExterior)) ^ 1
  simpa using
    (LinearMap.mem_range_self
      (ExteriorAlgebra.ι ℝ : RoleSpace →ₗ[ℝ] RoleExterior) b)

/-- Mandatory degree/parity witness: the nonzero response added to the degree-zero
vacuum lies in exterior degree one, hence in the opposite degree parity sector. -/
theorem nilpotentAffineTranslation_degree_parity_witness :
    let vac := Pi.single fockVacuumState (1 : ℝ)
    let δ := nilpotentAffineTranslation nilpotentWitnessShift vac - vac
    δ ≠ 0 ∧
      δ ∈ archiveFockDegreeSector 1 ∧
      fockDegree fockVacuumState = 0 ∧
      (0 : ℕ) % 2 ≠ (1 : ℕ) % 2 := by
  dsimp
  have hδ :
      nilpotentAffineTranslation nilpotentWitnessShift
          (Pi.single fockVacuumState (1 : ℝ)) -
        Pi.single fockVacuumState (1 : ℝ) =
      archiveExteriorCreator nilpotentWitnessShift
        (Pi.single fockVacuumState (1 : ℝ)) := by
    rw [nilpotentAffineTranslation_vacuum]
    abel
  refine ⟨?_, ?_, fockDegree_vacuum_eq_zero, by norm_num⟩
  · rw [hδ]
    simpa [nilpotentAffineGenerator_apply] using
      nilpotentAffineGenerator_vacuum_ne_zero
        nilpotentWitnessShift nilpotentWitnessShift_ne_zero
  · rw [hδ]
    exact archiveExteriorCreator_vacuum_mem_degree_one nilpotentWitnessShift

/-- Preferred remnant: conjugated generator stays nonzero. -/
theorem conjugate_generator_ne_zero
    (F : (ArchiveFockState → ℝ) ≃ₗ[ℝ] (ArchiveFockState → ℝ))
    (b : RoleSpace) (hb : b ≠ 0) :
    F.toLinearMap.comp
        ((nilpotentAffineGenerator b).comp F.symm.toLinearMap) ≠ 0 := by
  intro h
  have hN : nilpotentAffineGenerator b = 0 := by
    apply LinearMap.ext; intro ψ
    have h1 : F (nilpotentAffineGenerator b ψ) = 0 := by
      have := LinearMap.congr_fun h (F ψ)
      simpa [LinearMap.comp_apply, LinearMap.zero_apply,
        LinearEquiv.symm_apply_apply] using this
    have h2 : F (nilpotentAffineGenerator b ψ) = F 0 := by simpa [map_zero] using h1
    exact F.injective h2
  exact nilpotentAffineGenerator_vacuum_ne_zero b hb (by rw [hN]; rfl)

/-- Mandatory 7: conjugation cannot erase a nonzero shift. -/
theorem conjugate_translation_ne_id
    (F : (ArchiveFockState → ℝ) ≃ₗ[ℝ] (ArchiveFockState → ℝ))
    (b : RoleSpace) (hb : b ≠ 0) :
    F.toLinearMap.comp
        ((nilpotentAffineTranslation b).comp F.symm.toLinearMap) ≠ LinearMap.id := by
  intro h
  have hT : nilpotentAffineTranslation b = LinearMap.id := by
    apply LinearMap.ext; intro ψ
    have h1 : F (nilpotentAffineTranslation b ψ) = F ψ := by
      have := LinearMap.congr_fun h (F ψ)
      simpa [LinearMap.comp_apply, LinearMap.id_apply,
        LinearEquiv.symm_apply_apply] using this
    exact F.injective h1
  exact nilpotentAffineTranslation_ne_id b hb hT

theorem degreePreserving_conjugate_translation_ne_id
    (F : (ArchiveFockState → ℝ) ≃ₗ[ℝ] (ArchiveFockState → ℝ))
    (_hF : PreservesArchiveFockDegrees F.toLinearMap)
    (b : RoleSpace) (hb : b ≠ 0) :
    F.toLinearMap.comp
        ((nilpotentAffineTranslation b).comp F.symm.toLinearMap) ≠ LinearMap.id :=
  conjugate_translation_ne_id F b hb

/-- Mandatory 8: `[I, T_b] = 0`. -/
theorem id_commute_nilpotentAffineTranslation (b : RoleSpace) :
    LinearMap.id.comp (nilpotentAffineTranslation b) -
      (nilpotentAffineTranslation b).comp LinearMap.id = 0 := by
  simp [LinearMap.id_comp, LinearMap.comp_id, sub_self]

end

end D0.Geometry
