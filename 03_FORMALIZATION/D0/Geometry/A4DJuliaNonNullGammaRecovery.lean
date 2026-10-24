import Mathlib.LinearAlgebra.Determinant
import D0.Geometry.ArchiveJuliaRaisingOperatorReadout

/-!
# Non-null Lorentz-Clifford recovery for the finite Julia query

This formalizes the algebraic inverse in Eq. (27) of the published #334 source
at commit `fe5cf335da04cac14e50407b03f98b96be17dc52`, path
`02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md`,
blob `1c8d59e5533b443d9a015dc4512cfbc160ae7e62`, §8.4. The source consumer is
§5.1 of
`02_REGISTRY/research/A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md`,
blob `734e21ae6bc04ff3446ad15858936d417fdd2e55`.

The gamma-square identity is derived from the existing creator/contraction
CAR on the full 16-state exterior carrier. The recovery theorem then composes
that identity with the exact finite query `C(u) ρ(M)`. The fixed source-chart
CAR volume equivalence proves its creator-conjugation identity, and
nonidentity endpoint covariance follows from metric isometry, creator and
contraction transport, and preservation of the oriented volume vector. Thus
Eq. (27) is compiled for oriented isometries of this fixed source chart. The
source's concrete endpoint package must still prove those metric/orientation
hypotheses, and joining the non-null chart to Eq. (28) remains separate work.
It makes no physical admission or GR-selection claim.
-/

namespace D0.Geometry

noncomputable section

/-- The Lorentz-Clifford operator `C(u) + i_(P u)` on the owned finite
exterior carrier. `P u` is the metric-dual covector at the source endpoint. -/
def archiveJuliaLorentzGamma (P : ArchiveRoleBilinear) (u : RoleSpace) :
    (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) :=
  archiveExteriorCreatorLM u + archiveExteriorContraction (P u)

/-- The Clifford square on the full 16-state carrier is the endpoint quadratic
form. This follows from the existing creator/contraction CAR, not an assumed
square identity. -/
theorem archiveJuliaLorentzGamma_square (P : ArchiveRoleBilinear)
    (u : RoleSpace) :
    (archiveJuliaLorentzGamma P u).comp (archiveJuliaLorentzGamma P u) =
      (P u u) • LinearMap.id := by
  apply LinearMap.ext
  intro ψ
  let C := archiveExteriorCreatorLM u
  let I := archiveExteriorContraction (P u)
  have hC : C (C ψ) = 0 := by
    change archiveExteriorCreator u (archiveExteriorCreator u ψ) = 0
    have h := archiveExteriorCreator_anticommute u u ψ
    have hzero : (2 : ℝ) • archiveExteriorCreator u
        (archiveExteriorCreator u ψ) = 0 := by
      simpa [two_smul] using h
    rcases smul_eq_zero.mp hzero with htwo | hcc
    · norm_num at htwo
    · exact hcc
  have hI : I (I ψ) = 0 := by
    change archiveExteriorContraction (P u)
        (archiveExteriorContraction (P u) ψ) = 0
    have h := archiveExteriorContraction_anticommute (P u) (P u) ψ
    have hsum : archiveExteriorContraction (P u)
        (archiveExteriorContraction (P u) ψ) +
      archiveExteriorContraction (P u)
        (archiveExteriorContraction (P u) ψ) = 0 := by
      exact (add_eq_zero_iff_eq_neg).2 h
    have hzero : (2 : ℝ) • archiveExteriorContraction (P u)
        (archiveExteriorContraction (P u) ψ) = 0 := by
      simpa [two_smul] using hsum
    rcases smul_eq_zero.mp hzero with htwo | hii
    · norm_num at htwo
    · exact hii
  have hmixed : C (I ψ) + I (C ψ) = (P u u) • ψ := by
    change archiveExteriorCreator u
        (archiveExteriorContraction (P u) ψ) +
      archiveExteriorContraction (P u) (archiveExteriorCreator u ψ) =
        (P u u) • ψ
    rw [archiveExteriorContraction_creator]
    abel
  change (C + I) ((C + I) ψ) = (P u u) • ψ
  change C (C ψ + I ψ) + I (C ψ + I ψ) = (P u u) • ψ
  rw [map_add, map_add, hC, hI]
  simpa [add_zero, zero_add] using hmixed

/-- The gamma/creator anticommutator is the metric pairing. This is the mixed
CAR identity on the same 16-state carrier, with no endpoint covariance
assumption. -/
theorem archiveJuliaLorentzGamma_creator_anticommutator
    (P : ArchiveRoleBilinear) (u v : RoleSpace) :
    (archiveJuliaLorentzGamma P u).comp (archiveExteriorCreatorLM v) +
      (archiveExteriorCreatorLM v).comp (archiveJuliaLorentzGamma P u) =
        (P u v) • LinearMap.id := by
  apply LinearMap.ext
  intro ψ
  simp only [LinearMap.add_apply, LinearMap.comp_apply, LinearMap.smul_apply,
    LinearMap.id_apply, archiveJuliaLorentzGamma, map_add]
  simp only [archiveExteriorCreatorLM, LinearMap.coe_mk, AddHom.coe_mk]
  calc
    _ =
        (archiveExteriorCreator u (archiveExteriorCreator v ψ) +
          archiveExteriorCreator v (archiveExteriorCreator u ψ)) +
        (archiveExteriorContraction (P u) (archiveExteriorCreator v ψ) +
          archiveExteriorCreator v (archiveExteriorContraction (P u) ψ)) := by
          abel
    _ = 0 + (P u v) • ψ := by
          rw [archiveExteriorCreator_anticommute,
            archiveExterior_contraction_creator_car]
    _ = _ := by simp

/-- Polarized Clifford relation, derived from the creator and contraction CAR
on the full carrier. -/
theorem archiveJuliaLorentzGamma_anticommutator
    (P : ArchiveRoleBilinear) (u v : RoleSpace) :
    (archiveJuliaLorentzGamma P u).comp (archiveJuliaLorentzGamma P v) +
      (archiveJuliaLorentzGamma P v).comp (archiveJuliaLorentzGamma P u) =
        ((P u v) + (P v u)) • LinearMap.id := by
  apply LinearMap.ext
  intro ψ
  simp only [LinearMap.add_apply, LinearMap.comp_apply, LinearMap.smul_apply,
    LinearMap.id_apply, archiveJuliaLorentzGamma, map_add]
  simp only [archiveExteriorCreatorLM, LinearMap.coe_mk, AddHom.coe_mk]
  calc
    _ =
        (archiveExteriorCreator u (archiveExteriorCreator v ψ) +
          archiveExteriorCreator v (archiveExteriorCreator u ψ)) +
        (archiveExteriorContraction (P u) (archiveExteriorCreator v ψ) +
          archiveExteriorCreator v (archiveExteriorContraction (P u) ψ)) +
        (archiveExteriorContraction (P v) (archiveExteriorCreator u ψ) +
          archiveExteriorCreator u (archiveExteriorContraction (P v) ψ)) +
        (archiveExteriorContraction (P u)
            (archiveExteriorContraction (P v) ψ) +
          archiveExteriorContraction (P v)
            (archiveExteriorContraction (P u) ψ)) := by
          abel
    _ = 0 + (P u v) • ψ + (P v u) • ψ + 0 := by
          rw [archiveExteriorCreator_anticommute,
            archiveExterior_contraction_creator_car,
            archiveExterior_contraction_creator_car]
          have hI := archiveExteriorContraction_anticommute (P u) (P v) ψ
          rw [hI]
          simp
    _ = _ := by
          simp [add_smul, add_comm]

/-- The signature in the source's fixed oriented Role frame: A is timelike and
B,C,D are spacelike. This is a coordinate-frame adapter, not a selector for
the physical endpoint metric. -/
def archiveJuliaSourceLorentzSign (r : Role) : ℝ :=
  if r = D0.A then 1 else -1

/-- Metric dual covector for the source's fixed diagonal Lorentz form. -/
noncomputable def archiveJuliaSourceLorentzCovector (u : RoleSpace) :
    Module.Dual ℝ RoleSpace :=
  ∑ r : Role, (archiveJuliaSourceLorentzSign r * u r) • archiveRoleBasis.coord r

/-- The source's fixed diagonal Lorentz pairing on the four-role coordinate
space. -/
noncomputable def archiveJuliaSourceLorentzForm : ArchiveRoleBilinear where
  toFun := archiveJuliaSourceLorentzCovector
  map_add' u v := by
    ext w
    simp [archiveJuliaSourceLorentzCovector, Pi.add_apply, add_mul,
      smul_eq_mul, Finset.sum_add_distrib, mul_add]
  map_smul' c u := by
    ext w
    simp [archiveJuliaSourceLorentzCovector, archiveRoleBasis,
      Module.Basis.coord, Finsupp.lapply_apply,
      smul_eq_mul, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro r hr
    ring

theorem archiveJuliaSourceLorentzCovector_basis (r : Role) :
    archiveJuliaSourceLorentzCovector (archiveRoleBasis r) =
      archiveJuliaSourceLorentzSign r • archiveRoleBasis.coord r := by
  classical
  ext v
  simp [archiveJuliaSourceLorentzCovector, archiveJuliaSourceLorentzSign,
    archiveRoleBasis, Module.Basis.coord, Pi.single_apply]

theorem archiveJuliaSourceLorentzForm_basis_basis (r s : Role) :
    archiveJuliaSourceLorentzForm (archiveRoleBasis r) (archiveRoleBasis s) =
      if r = s then archiveJuliaSourceLorentzSign r else 0 := by
  change archiveJuliaSourceLorentzCovector
    (archiveRoleBasis r) (archiveRoleBasis s) = _
  rw [archiveJuliaSourceLorentzCovector_basis]
  have hcoord : archiveRoleBasis.coord r (archiveRoleBasis s) =
      if r = s then 1 else 0 := by
    rw [archiveRoleBasis.coord_apply, archiveRoleBasis.repr_self]
    simp [Finsupp.single_apply, eq_comm]
  change archiveJuliaSourceLorentzSign r *
    archiveRoleBasis.coord r (archiveRoleBasis s) = _
  rw [hcoord]
  by_cases hrs : r = s
  · subst s
    simp [archiveJuliaSourceLorentzSign]
  · simp [hrs]

/-- The four canonical Clifford generators in the source's fixed Role chart.
Their signature is explicit in `archiveJuliaSourceLorentzSign`. -/
noncomputable def archiveJuliaSourceGamma (r : Role) :
    (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) :=
  archiveJuliaLorentzGamma archiveJuliaSourceLorentzForm (archiveRoleBasis r)

noncomputable def archiveJuliaSourceContraction (r : Role) :
    (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) :=
  archiveExteriorContraction (archiveJuliaSourceLorentzCovector (archiveRoleBasis r))

theorem archiveJuliaSourceGamma_square (r : Role) :
    (archiveJuliaSourceGamma r).comp (archiveJuliaSourceGamma r) =
      archiveJuliaSourceLorentzSign r • LinearMap.id := by
  simpa [archiveJuliaSourceGamma, archiveJuliaSourceLorentzForm_basis_basis] using
    archiveJuliaLorentzGamma_square archiveJuliaSourceLorentzForm (archiveRoleBasis r)

theorem archiveJuliaSourceLorentzSign_sq (r : Role) :
    archiveJuliaSourceLorentzSign r * archiveJuliaSourceLorentzSign r = 1 := by
  by_cases hr : r = A <;> simp [archiveJuliaSourceLorentzSign, hr]

noncomputable def archiveJuliaSourceGammaEquiv (r : Role) :
    (ArchiveFockState → ℝ) ≃ₗ[ℝ] (ArchiveFockState → ℝ) where
  toFun := archiveJuliaSourceGamma r
  invFun ψ := archiveJuliaSourceLorentzSign r • archiveJuliaSourceGamma r ψ
  left_inv ψ := by
    have hSquareψ : archiveJuliaSourceGamma r (archiveJuliaSourceGamma r ψ) =
        archiveJuliaSourceLorentzSign r • ψ := by
      simpa [LinearMap.comp_apply, LinearMap.smul_apply,
        LinearMap.id_apply] using
        congrArg (fun T : (ArchiveFockState → ℝ) →ₗ[ℝ]
          (ArchiveFockState → ℝ) => T ψ) (archiveJuliaSourceGamma_square r)
    change archiveJuliaSourceLorentzSign r •
      archiveJuliaSourceGamma r (archiveJuliaSourceGamma r ψ) = ψ
    rw [hSquareψ, smul_smul]
    simp [archiveJuliaSourceLorentzSign_sq]
  right_inv ψ := by
    have hSquareψ : archiveJuliaSourceGamma r (archiveJuliaSourceGamma r ψ) =
        archiveJuliaSourceLorentzSign r • ψ := by
      simpa [LinearMap.comp_apply, LinearMap.smul_apply,
        LinearMap.id_apply] using
        congrArg (fun T : (ArchiveFockState → ℝ) →ₗ[ℝ]
          (ArchiveFockState → ℝ) => T ψ) (archiveJuliaSourceGamma_square r)
    change archiveJuliaSourceGamma r
      (archiveJuliaSourceLorentzSign r • archiveJuliaSourceGamma r ψ) = ψ
    rw [(archiveJuliaSourceGamma r).map_smul, hSquareψ, smul_smul]
    simp [archiveJuliaSourceLorentzSign_sq]
  map_add' := (archiveJuliaSourceGamma r).map_add
  map_smul' := (archiveJuliaSourceGamma r).map_smul

theorem archiveJuliaSourceGamma_creator_anticommutator (r s : Role) :
    (archiveJuliaSourceGamma r).comp (archiveExteriorCreatorLM (archiveRoleBasis s)) +
      (archiveExteriorCreatorLM (archiveRoleBasis s)).comp (archiveJuliaSourceGamma r) =
        (if r = s then archiveJuliaSourceLorentzSign r else 0) • LinearMap.id := by
  simpa [archiveJuliaSourceGamma, archiveJuliaSourceLorentzForm_basis_basis] using
    archiveJuliaLorentzGamma_creator_anticommutator archiveJuliaSourceLorentzForm
      (archiveRoleBasis r) (archiveRoleBasis s)

/-- Distinct source-chart gamma generators anticommute. -/
theorem archiveJuliaSourceGamma_anticommute {r s : Role} (hrs : r ≠ s) :
    (archiveJuliaSourceGamma r).comp (archiveJuliaSourceGamma s) +
      (archiveJuliaSourceGamma s).comp (archiveJuliaSourceGamma r) = 0 := by
  simpa [archiveJuliaSourceGamma, archiveJuliaSourceLorentzForm_basis_basis,
    hrs, Ne.symm hrs] using
    archiveJuliaLorentzGamma_anticommutator archiveJuliaSourceLorentzForm
      (archiveRoleBasis r) (archiveRoleBasis s)

theorem archiveJuliaSourceContraction_eq_gamma_sub_creator (r : Role) :
    archiveJuliaSourceContraction r = archiveJuliaSourceGamma r -
      archiveExteriorCreatorLM (archiveRoleBasis r) := by
  have hP : archiveJuliaSourceLorentzForm (archiveRoleBasis r) =
      archiveJuliaSourceLorentzCovector (archiveRoleBasis r) := rfl
  change archiveExteriorContraction
      (archiveJuliaSourceLorentzCovector (archiveRoleBasis r)) =
    archiveJuliaLorentzGamma archiveJuliaSourceLorentzForm (archiveRoleBasis r) -
      archiveExteriorCreatorLM (archiveRoleBasis r)
  simp only [archiveJuliaLorentzGamma]
  rw [hP]
  simp

theorem archiveJuliaSourceGamma_creator_same (r : Role) :
    (archiveJuliaSourceGamma r).comp (archiveExteriorCreatorLM (archiveRoleBasis r)) =
      (archiveJuliaSourceContraction r).comp (archiveJuliaSourceGamma r) := by
  let Γ := archiveJuliaSourceGamma r
  let C := archiveExteriorCreatorLM (archiveRoleBasis r)
  let I := archiveJuliaSourceContraction r
  have hI : I = Γ - C := archiveJuliaSourceContraction_eq_gamma_sub_creator r
  have hAnti := archiveJuliaSourceGamma_creator_anticommutator r r
  have hSquare := archiveJuliaSourceGamma_square r
  apply LinearMap.ext
  intro ψ
  have hAntiψ : Γ (C ψ) + C (Γ ψ) =
      archiveJuliaSourceLorentzSign r • ψ := by
    simpa [Γ, C, LinearMap.add_apply, LinearMap.comp_apply,
      LinearMap.smul_apply, LinearMap.id_apply] using
        congrArg (fun T : (ArchiveFockState → ℝ) →ₗ[ℝ]
          (ArchiveFockState → ℝ) => T ψ) hAnti
  have hSquareψ : Γ (Γ ψ) = archiveJuliaSourceLorentzSign r • ψ := by
    simpa [Γ, LinearMap.comp_apply, LinearMap.smul_apply,
      LinearMap.id_apply] using
        congrArg (fun T : (ArchiveFockState → ℝ) →ₗ[ℝ]
          (ArchiveFockState → ℝ) => T ψ) hSquare
  have hIψ : I (Γ ψ) = Γ (Γ ψ) - C (Γ ψ) := by
    simpa [I, Γ, C, LinearMap.sub_apply] using
      congrArg (fun T : (ArchiveFockState → ℝ) →ₗ[ℝ]
        (ArchiveFockState → ℝ) => T (Γ ψ)) hI
  calc
    Γ (C ψ) = (Γ (C ψ) + C (Γ ψ)) - C (Γ ψ) := by abel
    _ = archiveJuliaSourceLorentzSign r • ψ - C (Γ ψ) := by rw [hAntiψ]
    _ = I (Γ ψ) := by rw [hIψ, hSquareψ]

theorem archiveJuliaSourceGamma_creator_swap (r s : Role) :
    (archiveJuliaSourceGamma r).comp (archiveExteriorCreatorLM (archiveRoleBasis s)) =
      if r = s then
        (archiveJuliaSourceContraction r).comp (archiveJuliaSourceGamma r)
      else -((archiveExteriorCreatorLM (archiveRoleBasis s)).comp
        (archiveJuliaSourceGamma r)) := by
  by_cases hrs : r = s
  · subst s
    simpa using archiveJuliaSourceGamma_creator_same r
  · have hzero :
        (archiveJuliaSourceGamma r).comp (archiveExteriorCreatorLM (archiveRoleBasis s)) +
          (archiveExteriorCreatorLM (archiveRoleBasis s)).comp
            (archiveJuliaSourceGamma r) = 0 := by
      simpa [hrs] using archiveJuliaSourceGamma_creator_anticommutator r s
    simpa [hrs] using (add_eq_zero_iff_eq_neg.mp hzero)

theorem archiveJuliaSourceGamma_contraction_anticommute
    {r s : Role} (hrs : r ≠ s) :
    (archiveJuliaSourceGamma r).comp (archiveJuliaSourceContraction s) +
      (archiveJuliaSourceContraction s).comp (archiveJuliaSourceGamma r) = 0 := by
  let Γr := archiveJuliaSourceGamma r
  let Γs := archiveJuliaSourceGamma s
  let Cs := archiveExteriorCreatorLM (archiveRoleBasis s)
  let Is := archiveJuliaSourceContraction s
  have hI : Is = Γs - Cs := archiveJuliaSourceContraction_eq_gamma_sub_creator s
  have hG := archiveJuliaSourceGamma_anticommute hrs
  have hC := archiveJuliaSourceGamma_creator_anticommutator r s
  apply LinearMap.ext
  intro ψ
  have hGψ : Γr (Γs ψ) + Γs (Γr ψ) = 0 := by
    simpa [Γr, Γs, LinearMap.add_apply, LinearMap.comp_apply] using
      congrArg (fun T : (ArchiveFockState → ℝ) →ₗ[ℝ]
        (ArchiveFockState → ℝ) => T ψ) hG
  have hCψ : Γr (Cs ψ) + Cs (Γr ψ) = 0 := by
    simpa [Γr, Cs, hrs, LinearMap.add_apply, LinearMap.comp_apply,
      LinearMap.smul_apply, LinearMap.id_apply] using
        congrArg (fun T : (ArchiveFockState → ℝ) →ₗ[ℝ]
          (ArchiveFockState → ℝ) => T ψ) hC
  have hIψ : Is ψ = Γs ψ - Cs ψ := by
    simpa [Is, Γs, Cs, LinearMap.sub_apply] using
      congrArg (fun T : (ArchiveFockState → ℝ) →ₗ[ℝ]
        (ArchiveFockState → ℝ) => T ψ) hI
  have hIΓψ : Is (Γr ψ) = Γs (Γr ψ) - Cs (Γr ψ) := by
    simpa [Is, Γs, Cs, LinearMap.sub_apply] using
      congrArg (fun T : (ArchiveFockState → ℝ) →ₗ[ℝ]
        (ArchiveFockState → ℝ) => T (Γr ψ)) hI
  change Γr (Is ψ) + Is (Γr ψ) = 0
  rw [hIψ, hIΓψ, map_sub]
  calc
    _ = (Γr (Γs ψ) + Γs (Γr ψ)) -
        (Γr (Cs ψ) + Cs (Γr ψ)) := by abel
    _ = 0 - 0 := by rw [hGψ, hCψ]
    _ = 0 := by simp

theorem archiveJuliaSourceGamma_contraction_swap {r s : Role}
    (hrs : r ≠ s) :
    (archiveJuliaSourceGamma r).comp (archiveJuliaSourceContraction s) =
      -((archiveJuliaSourceContraction s).comp (archiveJuliaSourceGamma r)) := by
  exact (add_eq_zero_iff_eq_neg.mp
    (archiveJuliaSourceGamma_contraction_anticommute hrs))

theorem archiveJuliaSourceGamma_creator_swap_apply (r s : Role)
    (ψ : ArchiveFockState → ℝ) :
    archiveJuliaSourceGamma r
        (archiveExteriorCreatorLM (archiveRoleBasis s) ψ) =
      if r = s then
        archiveJuliaSourceContraction r (archiveJuliaSourceGamma r ψ)
      else -archiveExteriorCreatorLM (archiveRoleBasis s)
        (archiveJuliaSourceGamma r ψ) := by
  simpa [LinearMap.comp_apply, DFunLike.ite_apply] using
    congrArg (fun T : (ArchiveFockState → ℝ) →ₗ[ℝ]
      (ArchiveFockState → ℝ) => T ψ)
      (archiveJuliaSourceGamma_creator_swap r s)

theorem archiveJuliaSourceGamma_contraction_swap_apply {r s : Role}
    (hrs : r ≠ s) (ψ : ArchiveFockState → ℝ) :
    archiveJuliaSourceGamma r (archiveJuliaSourceContraction s ψ) =
      -archiveJuliaSourceContraction s (archiveJuliaSourceGamma r ψ) := by
  simpa [LinearMap.comp_apply] using
    congrArg (fun T : (ArchiveFockState → ℝ) →ₗ[ℝ]
      (ArchiveFockState → ℝ) => T ψ)
      (archiveJuliaSourceGamma_contraction_swap hrs)

/-- The source volume element in its fixed ordered Role frame. -/
noncomputable def archiveJuliaSourceVolumeElement :
    (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) :=
  (((archiveJuliaSourceGamma A).comp (archiveJuliaSourceGamma B)).comp
    (archiveJuliaSourceGamma C)).comp (archiveJuliaSourceGamma D)

noncomputable def archiveJuliaSourceVolumeEquiv :
    (ArchiveFockState → ℝ) ≃ₗ[ℝ] (ArchiveFockState → ℝ) :=
  (((archiveJuliaSourceGammaEquiv D).trans (archiveJuliaSourceGammaEquiv C)).trans
    (archiveJuliaSourceGammaEquiv B)).trans (archiveJuliaSourceGammaEquiv A)

theorem archiveJuliaSourceVolumeEquiv_apply (ψ : ArchiveFockState → ℝ) :
    archiveJuliaSourceVolumeEquiv ψ = archiveJuliaSourceVolumeElement ψ := by
  simp [archiveJuliaSourceVolumeEquiv, archiveJuliaSourceVolumeElement,
    archiveJuliaSourceGammaEquiv, LinearMap.comp_apply,
    LinearEquiv.trans_apply]

theorem archiveJuliaSourceVolumeEquiv_toLinearMap :
    archiveJuliaSourceVolumeEquiv.toLinearMap =
      archiveJuliaSourceVolumeElement := by
  apply LinearMap.ext
  intro ψ
  exact archiveJuliaSourceVolumeEquiv_apply ψ

theorem archiveJuliaSourceVolumeEquiv_symm_comp :
    archiveJuliaSourceVolumeEquiv.toLinearMap.comp
        archiveJuliaSourceVolumeEquiv.symm.toLinearMap = LinearMap.id := by
  apply LinearMap.ext
  intro ψ
  exact archiveJuliaSourceVolumeEquiv.apply_symm_apply ψ

/-- The volume element conjugates each source creator to minus its metric-dual
contraction, derived from the canonical CAR on all 16 states. -/
theorem archiveJuliaSourceVolumeElement_creator (r : Role) :
    archiveJuliaSourceVolumeElement.comp
        (archiveExteriorCreatorLM (archiveRoleBasis r)) =
      -((archiveJuliaSourceContraction r).comp archiveJuliaSourceVolumeElement) := by
  apply LinearMap.ext
  intro ψ
  fin_cases r <;>
    simp [archiveJuliaSourceVolumeElement, LinearMap.comp_apply,
      archiveJuliaSourceGamma_creator_swap_apply,
      archiveJuliaSourceGamma_contraction_swap_apply, A, B, C, D]

private theorem archiveJuliaSourceRoleBasis_weighted_sum (u : RoleSpace) :
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

private theorem archiveJuliaSourceCreatorLM_smul (a : ℝ) (u : RoleSpace) :
    archiveExteriorCreatorLM (a • u) = a • archiveExteriorCreatorLM u := by
  apply LinearMap.ext
  intro ψ
  apply archiveFockExteriorEquiv.injective
  simp [archiveExteriorCreatorLM, archiveExteriorCreator, map_smul]

private theorem archiveJuliaSourceCreatorLM_sum (s : Finset Role)
    (a : Role → ℝ) (v : Role → RoleSpace) :
    archiveExteriorCreatorLM (∑ r ∈ s, a r • v r) =
      ∑ r ∈ s, a r • archiveExteriorCreatorLM (v r) := by
  classical
  induction s using Finset.induction_on with
  | empty => simp [archiveExteriorCreatorLM_zero]
  | @insert r s hrs ih =>
      simp only [Finset.sum_insert hrs]
      rw [archiveExteriorCreatorLM_add, archiveJuliaSourceCreatorLM_smul, ih]

private theorem archiveJuliaSourceCreator_sum (u : RoleSpace) :
    archiveExteriorCreatorLM u =
      ∑ r : Role, u r • archiveExteriorCreatorLM (archiveRoleBasis r) := by
  calc
    archiveExteriorCreatorLM u =
        archiveExteriorCreatorLM
          (∑ r : Role, u r • archiveRoleBasis r) := by
            congr 1
            exact (archiveJuliaSourceRoleBasis_weighted_sum u).symm
    _ = ∑ r : Role, u r • archiveExteriorCreatorLM (archiveRoleBasis r) := by
      simpa using archiveJuliaSourceCreatorLM_sum Finset.univ
        (fun r => u r) archiveRoleBasis

private theorem archiveJuliaSourceContraction_sum (u : RoleSpace) :
    archiveExteriorContraction (archiveJuliaSourceLorentzCovector u) =
      ∑ r : Role, (archiveJuliaSourceLorentzSign r * u r) •
        archiveExteriorContraction (archiveRoleBasis.coord r) := by
  apply LinearMap.ext
  intro ψ
  apply archiveFockExteriorEquiv.injective
  simp [archiveJuliaSourceLorentzCovector, archiveExteriorContraction,
    LinearMap.comp_apply, map_sum, map_smul]

private theorem archiveJuliaSourceContraction_basis (r : Role) :
    archiveJuliaSourceContraction r =
      archiveJuliaSourceLorentzSign r •
        archiveExteriorContraction (archiveRoleBasis.coord r) := by
  rw [archiveJuliaSourceContraction, archiveJuliaSourceLorentzCovector_basis]
  apply LinearMap.ext
  intro ψ
  apply archiveFockExteriorEquiv.injective
  simp [archiveExteriorContraction, LinearMap.comp_apply, map_smul]

/-- The fixed-chart endpoint volume identity extends from the four canonical
roles to every vector and its metric-dual covector. This discharges Eq. (27)'s
creator-conjugation input for this source chart. -/
theorem archiveJuliaSourceVolumeElement_creator_vector (u : RoleSpace) :
    archiveJuliaSourceVolumeElement.comp (archiveExteriorCreatorLM u) =
      -((archiveExteriorContraction (archiveJuliaSourceLorentzCovector u)).comp
        archiveJuliaSourceVolumeElement) := by
  rw [archiveJuliaSourceCreator_sum u, archiveJuliaSourceContraction_sum u]
  apply LinearMap.ext
  intro ψ
  simp only [LinearMap.comp_apply, LinearMap.sum_apply, LinearMap.smul_apply,
    LinearMap.neg_apply, map_sum, map_smul]
  calc
    (∑ r : Role, u r •
        archiveJuliaSourceVolumeElement
          (archiveExteriorCreatorLM (archiveRoleBasis r) ψ)) =
      ∑ r : Role, u r •
        -(archiveJuliaSourceContraction r
          (archiveJuliaSourceVolumeElement ψ)) := by
        apply Finset.sum_congr rfl
        intro r hr
        have h := LinearMap.congr_fun
          (archiveJuliaSourceVolumeElement_creator r) ψ
        simpa [LinearMap.comp_apply] using congrArg (fun x => u r • x) h
    _ = -(∑ r : Role, u r •
        archiveJuliaSourceContraction r (archiveJuliaSourceVolumeElement ψ)) := by
        simp_rw [smul_neg]
        rw [← Finset.sum_neg_distrib]
    _ = -(∑ r : Role,
        (archiveJuliaSourceLorentzSign r * u r) •
          archiveExteriorContraction (archiveRoleBasis.coord r)
            (archiveJuliaSourceVolumeElement ψ)) := by
        congr 1
        apply Finset.sum_congr rfl
        intro r hr
        rw [archiveJuliaSourceContraction_basis]
        simp only [LinearMap.smul_apply]
        rw [smul_smul, mul_comm]

theorem archiveJuliaSourceVolumeEquiv_creator_conjugation (u : RoleSpace) :
    archiveJuliaSourceVolumeEquiv.toLinearMap.comp
        ((archiveExteriorCreatorLM u).comp
          archiveJuliaSourceVolumeEquiv.symm.toLinearMap) =
      -(archiveExteriorContraction (archiveJuliaSourceLorentzCovector u)) := by
  calc
    archiveJuliaSourceVolumeEquiv.toLinearMap.comp
        ((archiveExteriorCreatorLM u).comp
          archiveJuliaSourceVolumeEquiv.symm.toLinearMap) =
      (archiveJuliaSourceVolumeEquiv.toLinearMap.comp
        (archiveExteriorCreatorLM u)).comp
          archiveJuliaSourceVolumeEquiv.symm.toLinearMap := by
            simp [LinearMap.comp_assoc]
    _ = (archiveJuliaSourceVolumeElement.comp
        (archiveExteriorCreatorLM u)).comp
          archiveJuliaSourceVolumeEquiv.symm.toLinearMap := by
            rw [archiveJuliaSourceVolumeEquiv_toLinearMap]
    _ = (-((archiveExteriorContraction
        (archiveJuliaSourceLorentzCovector u)).comp
          archiveJuliaSourceVolumeElement)).comp
            archiveJuliaSourceVolumeEquiv.symm.toLinearMap := by
            rw [archiveJuliaSourceVolumeElement_creator_vector]
    _ = -((archiveExteriorContraction
        (archiveJuliaSourceLorentzCovector u)).comp
          (archiveJuliaSourceVolumeElement.comp
            archiveJuliaSourceVolumeEquiv.symm.toLinearMap)) := by
            ext ψ
            simp [LinearMap.comp_apply]
    _ = -(archiveExteriorContraction
        (archiveJuliaSourceLorentzCovector u)) := by
            rw [← archiveJuliaSourceVolumeEquiv_toLinearMap,
              archiveJuliaSourceVolumeEquiv_symm_comp]
            simp

/-- The oriented source-volume vector used to express properness of a
source-frame map. Fixing this single vector is the orientation condition; it
is weaker than, and does not assume, covariance of the volume operator on the
full 16-state carrier. -/
noncomputable def archiveJuliaSourceVolumeVacuum : ArchiveFockState → ℝ :=
  archiveJuliaSourceVolumeEquiv (Pi.single fockVacuumState (1 : ℝ))

private noncomputable def archiveJuliaSourceCreatorWord : List Role →
    (ArchiveFockState → ℝ) → (ArchiveFockState → ℝ)
  | [], ψ => ψ
  | r :: rs, ψ => archiveExteriorCreatorLM (archiveRoleBasis r)
      (archiveJuliaSourceCreatorWord rs ψ)

private theorem archiveJuliaSourceContraction_vacuum
    (α : Module.Dual ℝ RoleSpace) :
    archiveExteriorContraction α (Pi.single fockVacuumState (1 : ℝ)) = 0 := by
  apply archiveFockExteriorEquiv.injective
  simp [archiveExteriorContraction, archiveFockExteriorEquiv_single,
    archiveFockExteriorBasis_apply, archiveFockSupport_vacuum,
    archiveRoleBasis_ExteriorAlgebra_empty]

private theorem archiveJuliaSourceGamma_vacuum (r : Role) :
    archiveJuliaSourceGamma r (Pi.single fockVacuumState (1 : ℝ)) =
      archiveExteriorCreatorLM (archiveRoleBasis r)
        (Pi.single fockVacuumState (1 : ℝ)) := by
  simp only [archiveJuliaSourceGamma, archiveJuliaLorentzGamma,
    LinearMap.add_apply]
  rw [archiveJuliaSourceContraction_vacuum]
  simp

private theorem archiveJuliaSourceGamma_creatorWord (r : Role) :
    ∀ rs : List Role, r ∉ rs → rs.Nodup →
      archiveJuliaSourceGamma r
          (archiveJuliaSourceCreatorWord rs
            (Pi.single fockVacuumState (1 : ℝ))) =
        archiveJuliaSourceCreatorWord (r :: rs)
          (Pi.single fockVacuumState (1 : ℝ)) := by
  intro rs
  induction rs with
  | nil =>
      intro _ _
      simpa [archiveJuliaSourceCreatorWord] using
        archiveJuliaSourceGamma_vacuum r
  | cons s rs ih =>
      intro hr hnd
      have hrs : r ≠ s := by
        intro h
        apply hr
        simp [h]
      have hrrest : r ∉ rs := by
        intro h
        exact hr (List.mem_cons_of_mem s h)
      have hnd' := List.nodup_cons.mp hnd
      have htail := ih hrrest hnd'.2
      have hswap : archiveJuliaSourceGamma r
          (archiveExteriorCreatorLM (archiveRoleBasis s)
            (archiveJuliaSourceCreatorWord rs
              (Pi.single fockVacuumState (1 : ℝ)))) =
          -archiveExteriorCreatorLM (archiveRoleBasis s)
            (archiveJuliaSourceGamma r
              (archiveJuliaSourceCreatorWord rs
                (Pi.single fockVacuumState (1 : ℝ)))) := by
        simpa [hrs] using archiveJuliaSourceGamma_creator_swap_apply r s
          (archiveJuliaSourceCreatorWord rs
            (Pi.single fockVacuumState (1 : ℝ)))
      have hcreator := archiveExteriorCreator_anticommute
        (archiveRoleBasis r) (archiveRoleBasis s)
        (archiveJuliaSourceCreatorWord rs
          (Pi.single fockVacuumState (1 : ℝ)))
      have hcomm : archiveExteriorCreatorLM (archiveRoleBasis r)
          (archiveExteriorCreatorLM (archiveRoleBasis s)
            (archiveJuliaSourceCreatorWord rs
              (Pi.single fockVacuumState (1 : ℝ)))) =
          -archiveExteriorCreatorLM (archiveRoleBasis s)
            (archiveExteriorCreatorLM (archiveRoleBasis r)
              (archiveJuliaSourceCreatorWord rs
                (Pi.single fockVacuumState (1 : ℝ)))) := by
        exact eq_neg_iff_add_eq_zero.mpr hcreator
      calc
        archiveJuliaSourceGamma r
            (archiveJuliaSourceCreatorWord (s :: rs)
              (Pi.single fockVacuumState (1 : ℝ))) =
          -archiveExteriorCreatorLM (archiveRoleBasis s)
            (archiveJuliaSourceGamma r
              (archiveJuliaSourceCreatorWord rs
                (Pi.single fockVacuumState (1 : ℝ)))) := by
                simpa [archiveJuliaSourceCreatorWord] using hswap
        _ = -archiveExteriorCreatorLM (archiveRoleBasis s)
            (archiveJuliaSourceCreatorWord (r :: rs)
              (Pi.single fockVacuumState (1 : ℝ))) := by
              rw [htail]
        _ = archiveJuliaSourceCreatorWord (r :: s :: rs)
            (Pi.single fockVacuumState (1 : ℝ)) := by
              simpa [archiveJuliaSourceCreatorWord] using hcomm.symm

private theorem archiveJuliaSourceRole_ne_of_index_ne {r s : Role}
    (h : roleOrderIndex r ≠ roleOrderIndex s) : r ≠ s := by
  intro hrs
  exact h (congrArg roleOrderIndex hrs)

/-- The oriented source-volume vector is exactly the ordered product of its
four source creators acting on the Fock vacuum. This identifies its concrete
finite-carrier representative without yet replacing vector preservation by a
coordinate determinant condition. -/
theorem archiveJuliaSourceVolumeVacuum_eq_ordered_creator_product :
    archiveJuliaSourceVolumeVacuum =
      archiveExteriorCreatorLM (archiveRoleBasis A)
        (archiveExteriorCreatorLM (archiveRoleBasis B)
          (archiveExteriorCreatorLM (archiveRoleBasis C)
            (archiveExteriorCreatorLM (archiveRoleBasis D)
              (Pi.single fockVacuumState (1 : ℝ))))) := by
  have hAB : A ≠ B := by
    apply archiveJuliaSourceRole_ne_of_index_ne
    norm_num [roleOrderIndex, D0.A, D0.B, D0.C, D0.D]
  have hAC : A ≠ C := by
    apply archiveJuliaSourceRole_ne_of_index_ne
    norm_num [roleOrderIndex, D0.A, D0.B, D0.C, D0.D]
  have hAD : A ≠ D := by
    apply archiveJuliaSourceRole_ne_of_index_ne
    norm_num [roleOrderIndex, D0.A, D0.B, D0.C, D0.D]
  have hBC : B ≠ C := by
    apply archiveJuliaSourceRole_ne_of_index_ne
    norm_num [roleOrderIndex, D0.A, D0.B, D0.C, D0.D]
  have hBD : B ≠ D := by
    apply archiveJuliaSourceRole_ne_of_index_ne
    norm_num [roleOrderIndex, D0.A, D0.B, D0.C, D0.D]
  have hCD : C ≠ D := by
    apply archiveJuliaSourceRole_ne_of_index_ne
    norm_num [roleOrderIndex, D0.A, D0.B, D0.C, D0.D]
  have hCnotD : C ∉ [D] := by simpa using hCD
  have hBnotCD : B ∉ [C, D] := by simp [hBC, hBD]
  have hAnotBCD : A ∉ [B, C, D] := by simp [hAB, hAC, hAD]
  have hNCD : ([C, D] : List Role).Nodup := by
    simp [List.nodup_cons, hCD]
  have hNBCD : ([B, C, D] : List Role).Nodup := by
    simp [List.nodup_cons, hBC, hBD, hCD]
  have hD := archiveJuliaSourceGamma_creatorWord D [] (by simp) List.nodup_nil
  have hC := archiveJuliaSourceGamma_creatorWord C [D]
    hCnotD (by simp)
  have hB := archiveJuliaSourceGamma_creatorWord B [C, D]
    hBnotCD hNCD
  have hA := archiveJuliaSourceGamma_creatorWord A [B, C, D]
    hAnotBCD hNBCD
  rw [archiveJuliaSourceVolumeVacuum, archiveJuliaSourceVolumeEquiv_apply]
  rw [archiveJuliaSourceVolumeElement]
  simp only [archiveJuliaSourceCreatorWord] at hD hC hB hA
  change archiveJuliaSourceGamma A
    (archiveJuliaSourceGamma B (archiveJuliaSourceGamma C
      (archiveJuliaSourceGamma D (Pi.single fockVacuumState (1 : ℝ))))) = _
  rw [hD, hC, hB, hA]

private theorem archiveJuliaSourceVolume_creator_right (u : RoleSpace) :
    archiveJuliaSourceVolumeEquiv.toLinearMap.comp
        (archiveExteriorCreatorLM u) =
      -(archiveExteriorContraction (archiveJuliaSourceLorentzCovector u)).comp
        archiveJuliaSourceVolumeEquiv.toLinearMap := by
  apply LinearMap.ext
  intro ψ
  have h := LinearMap.congr_fun
    (archiveJuliaSourceVolumeEquiv_creator_conjugation u)
    (archiveJuliaSourceVolumeEquiv ψ)
  simpa [LinearMap.comp_apply, LinearEquiv.apply_symm_apply] using h

private theorem archiveJuliaSourceVolume_inverse_contraction (u : RoleSpace) :
    archiveJuliaSourceVolumeEquiv.symm.toLinearMap.comp
        (archiveExteriorContraction (archiveJuliaSourceLorentzCovector u)) =
      -(archiveExteriorCreatorLM u).comp
        archiveJuliaSourceVolumeEquiv.symm.toLinearMap := by
  apply LinearMap.ext
  intro ψ
  have h := LinearMap.congr_fun
    (archiveJuliaSourceVolume_creator_right u)
    (archiveJuliaSourceVolumeEquiv.symm ψ)
  have h' := congrArg archiveJuliaSourceVolumeEquiv.symm h
  have h'' : archiveExteriorCreatorLM u
      (archiveJuliaSourceVolumeEquiv.symm ψ) =
        -(archiveJuliaSourceVolumeEquiv.symm
          (archiveExteriorContraction
            (archiveJuliaSourceLorentzCovector u) ψ)) := by
    simpa [LinearMap.comp_apply, LinearEquiv.apply_symm_apply,
      map_neg] using h'
  have hneg := congrArg (fun x : ArchiveFockState → ℝ => -x) h''
  simpa only [neg_neg] using hneg.symm

set_option maxRecDepth 2048 in
private theorem archiveJuliaSourceVolumeEquiv_symm_toLinearMap_comp :
    archiveJuliaSourceVolumeEquiv.symm.toLinearMap.comp
        archiveJuliaSourceVolumeEquiv.toLinearMap = LinearMap.id := by
  apply LinearMap.ext
  intro ψ
  exact archiveJuliaSourceVolumeEquiv.left_inv ψ

private theorem archiveJuliaSourceLorentzCovector_preimage
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (hIso : ∀ x y, archiveJuliaSourceLorentzForm (M x) (M y) =
      archiveJuliaSourceLorentzForm x y) (u : RoleSpace) :
    (archiveJuliaSourceLorentzCovector (M.symm u)).comp
        M.symm.toLinearMap = archiveJuliaSourceLorentzCovector u := by
  apply LinearMap.ext
  intro v
  change archiveJuliaSourceLorentzForm (M.symm u) (M.symm v) =
    archiveJuliaSourceLorentzForm u v
  simpa using (hIso (M.symm u) (M.symm v)).symm

private theorem archiveJuliaSourceVolume_conjugate_creator
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (hIso : ∀ x y, archiveJuliaSourceLorentzForm (M x) (M y) =
      archiveJuliaSourceLorentzForm x y)
    (u : RoleSpace) :
    ((archiveExteriorFrameLift M).comp
        (archiveJuliaSourceVolumeEquiv.toLinearMap.comp
          (archiveExteriorFrameLift M.symm))).comp
          (archiveExteriorCreatorLM u) =
      -(archiveExteriorContraction (archiveJuliaSourceLorentzCovector u)).comp
        ((archiveExteriorFrameLift M).comp
          (archiveJuliaSourceVolumeEquiv.toLinearMap.comp
            (archiveExteriorFrameLift M.symm))) := by
  let U := archiveExteriorFrameLift M
  let Uinv := archiveExteriorFrameLift M.symm
  let V := archiveJuliaSourceVolumeEquiv.toLinearMap
  let C := archiveExteriorCreatorLM
  let I := archiveExteriorContraction
  have hUinvCreator : Uinv.comp (C u) = (C (M.symm u)).comp Uinv := by
    apply LinearMap.ext
    intro ψ
    exact archiveExteriorFrameLift_creator_covariant M.symm u ψ
  have hUContraction : U.comp (I (archiveJuliaSourceLorentzCovector (M.symm u))) =
      (I ((archiveJuliaSourceLorentzCovector (M.symm u)).comp
        M.symm.toLinearMap)).comp U := by
    apply LinearMap.ext
    intro ψ
    exact archiveExteriorFrameLift_contraction_covariant M
      (archiveJuliaSourceLorentzCovector (M.symm u)) ψ
  have hCovector := archiveJuliaSourceLorentzCovector_preimage M hIso u
  have hV := archiveJuliaSourceVolume_creator_right (M.symm u)
  apply LinearMap.ext
  intro ψ
  simp only [LinearMap.comp_apply, LinearMap.neg_apply]
  have hCreator := LinearMap.congr_fun hUinvCreator ψ
  have hCreator' : Uinv (C u ψ) = C (M.symm u) (Uinv ψ) := by
    simpa only [LinearMap.comp_apply] using hCreator
  rw [hCreator']
  have hVolumeCreator := LinearMap.congr_fun hV (Uinv ψ)
  have hVolumeCreator' : V (C (M.symm u) (Uinv ψ)) =
      -(I (archiveJuliaSourceLorentzCovector (M.symm u))
        (V (Uinv ψ))) := by
    simpa only [LinearMap.comp_apply, LinearMap.neg_apply] using hVolumeCreator
  rw [hVolumeCreator', map_neg]
  have hContract := LinearMap.congr_fun hUContraction (V (Uinv ψ))
  have hContract' : U (I (archiveJuliaSourceLorentzCovector (M.symm u))
      (V (Uinv ψ))) =
      I ((archiveJuliaSourceLorentzCovector (M.symm u)).comp
        M.symm.toLinearMap) (U (V (Uinv ψ))) := by
    simpa only [LinearMap.comp_apply] using hContract
  rw [hContract', hCovector]

private theorem archiveFockLinearMap_eq_id_of_creator_commutation
    (T : (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ))
    (hCreator : ∀ v, T.comp (archiveExteriorCreatorLM v) =
      (archiveExteriorCreatorLM v).comp T)
    (hVacuum : T (Pi.single fockVacuumState (1 : ℝ)) =
      Pi.single fockVacuumState (1 : ℝ)) :
    T = LinearMap.id := by
  let S : RoleExterior →ₗ[ℝ] RoleExterior :=
    archiveFockExteriorEquiv.toLinearMap.comp
      (T.comp archiveFockExteriorEquiv.symm.toLinearMap)
  have hVacuumRep : archiveFockExteriorEquiv.symm (1 : RoleExterior) =
      Pi.single fockVacuumState (1 : ℝ) := by
    apply archiveFockExteriorEquiv.injective
    calc
      archiveFockExteriorEquiv (archiveFockExteriorEquiv.symm (1 : RoleExterior)) =
          1 := archiveFockExteriorEquiv.apply_symm_apply _
      _ = archiveFockExteriorEquiv (Pi.single fockVacuumState (1 : ℝ)) := by
        simpa using (archiveFockExteriorEquiv_single_vacuum (1 : ℝ)).symm
  have hSone : S 1 = 1 := by
    change archiveFockExteriorEquiv
      (T (archiveFockExteriorEquiv.symm (1 : RoleExterior))) = 1
    rw [hVacuumRep, hVacuum]
    simpa using archiveFockExteriorEquiv_single_vacuum (1 : ℝ)
  have hCreatorEquiv (v : RoleSpace) (ψ : ArchiveFockState → ℝ) :
      archiveFockExteriorEquiv (archiveExteriorCreatorLM v ψ) =
        ExteriorAlgebra.ι ℝ v * archiveFockExteriorEquiv ψ := by
    simp [archiveExteriorCreatorLM, archiveExteriorCreator]
  have hScreator : ∀ v z, S (ExteriorAlgebra.ι ℝ v * z) =
      ExteriorAlgebra.ι ℝ v * S z := by
    intro v z
    have harg : archiveFockExteriorEquiv.symm (ExteriorAlgebra.ι ℝ v * z) =
        archiveExteriorCreatorLM v (archiveFockExteriorEquiv.symm z) := by
      apply archiveFockExteriorEquiv.injective
      calc
        archiveFockExteriorEquiv
            (archiveFockExteriorEquiv.symm (ExteriorAlgebra.ι ℝ v * z)) =
              ExteriorAlgebra.ι ℝ v * z :=
          archiveFockExteriorEquiv.apply_symm_apply _
        _ = archiveFockExteriorEquiv
            (archiveExteriorCreatorLM v (archiveFockExteriorEquiv.symm z)) :=
          by simpa using (hCreatorEquiv v
            (archiveFockExteriorEquiv.symm z)).symm
    have hT := LinearMap.congr_fun (hCreator v)
      (archiveFockExteriorEquiv.symm z)
    have hT' : T (archiveExteriorCreatorLM v
        (archiveFockExteriorEquiv.symm z)) =
        archiveExteriorCreatorLM v
          (T (archiveFockExteriorEquiv.symm z)) := by
      simpa only [LinearMap.comp_apply] using hT
    calc
      S (ExteriorAlgebra.ι ℝ v * z) = archiveFockExteriorEquiv
          (T (archiveFockExteriorEquiv.symm
            (ExteriorAlgebra.ι ℝ v * z))) := rfl
      _ = archiveFockExteriorEquiv
          (T (archiveExteriorCreatorLM v
            (archiveFockExteriorEquiv.symm z))) := by rw [harg]
      _ = archiveFockExteriorEquiv
          (archiveExteriorCreatorLM v
            (T (archiveFockExteriorEquiv.symm z))) := by rw [hT']
      _ = ExteriorAlgebra.ι ℝ v * S z := hCreatorEquiv v
        (T (archiveFockExteriorEquiv.symm z))
  have hSleft : ∀ a z : RoleExterior, S (a * z) = a * S z := by
    intro a
    refine ExteriorAlgebra.induction
      (C := fun a => ∀ z : RoleExterior, S (a * z) = a * S z)
      (fun r => ?_) (fun v => ?_) (fun a b iha ihb => ?_)
      (fun a b iha ihb => ?_) a
    · intro z
      calc
        S (algebraMap ℝ RoleExterior r * z) = S (r • z) := by
          rw [Algebra.smul_def]
        _ = r • S z := S.map_smul r z
        _ = algebraMap ℝ RoleExterior r * S z := by
          rw [Algebra.smul_def]
    · intro z
      exact hScreator v z
    · intro z
      calc
        S ((a * b) * z) = S (a * (b * z)) := by rw [mul_assoc]
        _ = a * S (b * z) := iha (b * z)
        _ = a * (b * S z) := by rw [ihb z]
        _ = (a * b) * S z := by rw [mul_assoc]
    · intro z
      calc
        S ((a + b) * z) = S (a * z + b * z) := by rw [add_mul]
        _ = S (a * z) + S (b * z) := S.map_add _ _
        _ = a * S z + b * S z := by rw [iha z, ihb z]
        _ = (a + b) * S z := by rw [add_mul]
  have hSid : S = LinearMap.id := by
    apply LinearMap.ext
    intro z
    have h := hSleft z 1
    simpa [hSone] using h
  apply LinearMap.ext
  intro ψ
  apply archiveFockExteriorEquiv.injective
  have h := congrArg (fun F : RoleExterior →ₗ[ℝ] RoleExterior =>
    F (archiveFockExteriorEquiv ψ)) hSid
  simpa [S, LinearMap.comp_apply] using h

/-- Proper source-frame transport makes the volume equivalence covariant.
The proof uses metric preservation to transport contractions, creator
covariance to transport the Clifford product, and preservation of the oriented
volume vector to fix the remaining scalar. It does not assume the desired
endpoint operator covariance. -/
theorem archiveJuliaSourceVolumeEquiv_frameLift_commute
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (hIso : ∀ x y, archiveJuliaSourceLorentzForm (M x) (M y) =
      archiveJuliaSourceLorentzForm x y)
    (hOrientation : archiveExteriorFrameLift M
      archiveJuliaSourceVolumeVacuum = archiveJuliaSourceVolumeVacuum) :
    archiveJuliaSourceVolumeEquiv.toLinearMap.comp
        (archiveExteriorFrameLift M) =
      (archiveExteriorFrameLift M).comp
        archiveJuliaSourceVolumeEquiv.toLinearMap := by
  let U := archiveExteriorFrameLift M
  let Uinv := archiveExteriorFrameLift M.symm
  let V := archiveJuliaSourceVolumeEquiv.toLinearMap
  let Vinv := archiveJuliaSourceVolumeEquiv.symm.toLinearMap
  let C := archiveExteriorCreatorLM
  let I := archiveExteriorContraction
  let Vprime := U.comp (V.comp Uinv)
  let R := Vinv.comp Vprime
  have hVprimeCreator : ∀ u, Vprime.comp (C u) =
      -(I (archiveJuliaSourceLorentzCovector u)).comp Vprime := by
    intro u
    simpa only [Vprime, U, Uinv, V, C, I] using
      archiveJuliaSourceVolume_conjugate_creator M hIso u
  have hVinverseI : ∀ u, Vinv.comp (I (archiveJuliaSourceLorentzCovector u)) =
      -(C u).comp Vinv := by
    intro u
    exact archiveJuliaSourceVolume_inverse_contraction u
  have hRcreator : ∀ u, R.comp (C u) = (C u).comp R := by
    intro u
    calc
      R.comp (C u) = Vinv.comp (Vprime.comp (C u)) := by
        simp [R, LinearMap.comp_assoc]
      _ = Vinv.comp (-(I (archiveJuliaSourceLorentzCovector u)).comp Vprime) := by
        rw [hVprimeCreator u]
      _ = (C u).comp (Vinv.comp Vprime) := by
        rw [LinearMap.comp_neg, ← LinearMap.comp_assoc, hVinverseI u]
        simp [LinearMap.comp_assoc]
      _ = (C u).comp R := rfl
  have hUinvVacuum : Uinv (Pi.single fockVacuumState (1 : ℝ)) =
      Pi.single fockVacuumState (1 : ℝ) := by
    exact archiveExteriorFrameLift_vacuum M.symm 1
  have hOrientation' : U (V (Pi.single fockVacuumState (1 : ℝ))) =
      V (Pi.single fockVacuumState (1 : ℝ)) := by
    simpa only [archiveJuliaSourceVolumeVacuum, U, V] using hOrientation
  have hVprimeVacuum : Vprime (Pi.single fockVacuumState (1 : ℝ)) =
      V (Pi.single fockVacuumState (1 : ℝ)) := by
    calc
      Vprime (Pi.single fockVacuumState (1 : ℝ)) =
          U (V (Uinv (Pi.single fockVacuumState (1 : ℝ)))) := rfl
      _ = U (V (Pi.single fockVacuumState (1 : ℝ))) := by rw [hUinvVacuum]
      _ = V (Pi.single fockVacuumState (1 : ℝ)) := hOrientation'
  have hVinvV : Vinv.comp V = LinearMap.id := by
    exact archiveJuliaSourceVolumeEquiv_symm_toLinearMap_comp
  have hvac : R (Pi.single fockVacuumState (1 : ℝ)) =
      Pi.single fockVacuumState (1 : ℝ) := by
    calc
      R (Pi.single fockVacuumState (1 : ℝ)) =
          Vinv (Vprime (Pi.single fockVacuumState (1 : ℝ))) := rfl
      _ = Vinv (V (Pi.single fockVacuumState (1 : ℝ))) := by rw [hVprimeVacuum]
      _ = Pi.single fockVacuumState (1 : ℝ) := by
        have h := LinearMap.congr_fun hVinvV
          (Pi.single fockVacuumState (1 : ℝ))
        simpa only [LinearMap.comp_apply, LinearMap.id_apply] using h
  have hR : R = LinearMap.id := by
    apply archiveFockLinearMap_eq_id_of_creator_commutation R hRcreator hvac
  have hVprimeEq : Vprime = V := by
    calc
      Vprime = (V.comp Vinv).comp Vprime := by
        rw [archiveJuliaSourceVolumeEquiv_symm_comp]
        simp
      _ = V.comp (Vinv.comp Vprime) := by
        rw [LinearMap.comp_assoc]
      _ = V.comp R := rfl
      _ = V := by rw [hR]; simp
  have hUU : Uinv.comp U = LinearMap.id :=
    (archiveExteriorFrameLift_inverse M).2
  have hCommute : U.comp V = V.comp U := by
    apply LinearMap.ext
    intro ψ
    have h := LinearMap.congr_fun hVprimeEq (U ψ)
    have h' : U (V (Uinv (U ψ))) = V (U ψ) := by
      simpa only [Vprime, LinearMap.comp_apply] using h
    have hUinv : Uinv (U ψ) = ψ := by
      have h := LinearMap.congr_fun hUU ψ
      simpa only [LinearMap.comp_apply, LinearMap.id_apply] using h
    have h'' := congrArg (fun x => U (V x)) hUinv
    exact h''.symm.trans h'
  exact hCommute.symm

/-- Eq. (27) on one actual finite-carrier Julia query. The endpoint volume
identities are explicit inputs; when they hold, the nonzero Lorentz norm
recovers the full frame lift on all 16 grades. -/
theorem archiveJuliaRaisingQuery_nonNull_gamma_recovery
    (P : ArchiveRoleBilinear) (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (χₓ χᵧ : (ArchiveFockState → ℝ) ≃ₗ[ℝ] (ArchiveFockState → ℝ))
    (hConjugation : χₓ.toLinearMap.comp
        ((archiveExteriorCreatorLM u).comp χₓ.symm.toLinearMap) =
      -(archiveExteriorContraction (P u)))
    (hEndpointCovariance : χₓ.toLinearMap.comp (archiveExteriorFrameLift M) =
      (archiveExteriorFrameLift M).comp χᵧ.toLinearMap)
    (hq : P u u ≠ 0) :
    archiveExteriorFrameLift M = (P u u)⁻¹ •
      (archiveJuliaLorentzGamma P u).comp
        (archiveJuliaRaisingQuery u M -
          χₓ.toLinearMap.comp
            ((archiveJuliaRaisingQuery u M).comp χᵧ.symm.toLinearMap)) := by
  let C := archiveExteriorCreatorLM u
  let I := archiveExteriorContraction (P u)
  let U := archiveExteriorFrameLift M
  let q := P u u
  have hTransportInverse : U.comp χᵧ.symm.toLinearMap =
      χₓ.symm.toLinearMap.comp U := by
    calc
      U.comp χᵧ.symm.toLinearMap =
          χₓ.symm.toLinearMap.comp
            ((χₓ.toLinearMap.comp U).comp χᵧ.symm.toLinearMap) := by
              simp [LinearMap.comp_assoc]
      _ = χₓ.symm.toLinearMap.comp
            ((U.comp χᵧ.toLinearMap).comp χᵧ.symm.toLinearMap) := by
              rw [hEndpointCovariance]
      _ = χₓ.symm.toLinearMap.comp U := by
            simp [LinearMap.comp_assoc]
  have hConjugationLocal :
      (χₓ.toLinearMap.comp C).comp χₓ.symm.toLinearMap = -I := by
    simpa [C, I, LinearMap.comp_assoc] using hConjugation
  have hConjugatedQuery :
      χₓ.toLinearMap.comp ((C.comp U).comp χᵧ.symm.toLinearMap) =
        -(I.comp U) := by
    calc
      χₓ.toLinearMap.comp ((C.comp U).comp χᵧ.symm.toLinearMap) =
          (χₓ.toLinearMap.comp C).comp
            (U.comp χᵧ.symm.toLinearMap) := by
              simp [LinearMap.comp_assoc]
      _ = (χₓ.toLinearMap.comp C).comp
            (χₓ.symm.toLinearMap.comp U) := by
              rw [hTransportInverse]
      _ = ((χₓ.toLinearMap.comp C).comp χₓ.symm.toLinearMap).comp U := by
            simp [LinearMap.comp_assoc]
      _ = -(I.comp U) := by
            rw [hConjugationLocal]
            simp
  have hDifference :
      archiveJuliaRaisingQuery u M -
          χₓ.toLinearMap.comp
            ((archiveJuliaRaisingQuery u M).comp χᵧ.symm.toLinearMap) =
        (archiveJuliaLorentzGamma P u).comp U := by
    change (C.comp U) -
        χₓ.toLinearMap.comp ((C.comp U).comp χᵧ.symm.toLinearMap) =
      (C + I).comp U
    rw [hConjugatedQuery]
    ext ψ
    simp [LinearMap.comp_assoc]
  have hGammaDifference :
      (archiveJuliaLorentzGamma P u).comp
          (archiveJuliaRaisingQuery u M -
            χₓ.toLinearMap.comp
              ((archiveJuliaRaisingQuery u M).comp χᵧ.symm.toLinearMap)) =
        q • U := by
    rw [hDifference]
    calc
      (archiveJuliaLorentzGamma P u).comp
          ((archiveJuliaLorentzGamma P u).comp U) =
        ((archiveJuliaLorentzGamma P u).comp
          (archiveJuliaLorentzGamma P u)).comp U := by
            simp [LinearMap.comp_assoc]
      _ = ((P u u) • LinearMap.id).comp U := by
            rw [archiveJuliaLorentzGamma_square]
      _ = q • U := by
        ext ψ
        simp [q]
  calc
    U = (q⁻¹ * q) • U := by
      rw [inv_mul_cancel₀ hq]
      simp
    _ = q⁻¹ • (q • U) := by rw [smul_smul]
    _ = q⁻¹ • (archiveJuliaLorentzGamma P u).comp
          (archiveJuliaRaisingQuery u M -
            χₓ.toLinearMap.comp
              ((archiveJuliaRaisingQuery u M).comp χᵧ.symm.toLinearMap)) := by
            rw [← hGammaDifference]
    _ = _ := rfl

/-- The same Eq. (27) recovery holds for the owned Jordan--Wigner query because
its complete 16-state operator equals the exterior-model query. -/
theorem archiveJuliaCARRaisingQuery_nonNull_gamma_recovery
    (P : ArchiveRoleBilinear) (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (χₓ χᵧ : (ArchiveFockState → ℝ) ≃ₗ[ℝ] (ArchiveFockState → ℝ))
    (hConjugation : χₓ.toLinearMap.comp
        ((archiveExteriorCreatorLM u).comp χₓ.symm.toLinearMap) =
      -(archiveExteriorContraction (P u)))
    (hEndpointCovariance : χₓ.toLinearMap.comp (archiveExteriorFrameLift M) =
      (archiveExteriorFrameLift M).comp χᵧ.toLinearMap)
    (hq : P u u ≠ 0) :
    archiveExteriorFrameLift M = (P u u)⁻¹ •
      (archiveJuliaLorentzGamma P u).comp
        (archiveJuliaCARRaisingQuery u M -
          χₓ.toLinearMap.comp
            ((archiveJuliaCARRaisingQuery u M).comp χᵧ.symm.toLinearMap)) := by
  rw [archiveJuliaCARRaisingQuery_eq_model]
  exact archiveJuliaRaisingQuery_nonNull_gamma_recovery
    P u M χₓ χᵧ hConjugation hEndpointCovariance hq

/-- Eq. (27) for a nonidentity transport preserving the source Lorentz form
and its oriented volume vector. The endpoint covariance is derived in
`archiveJuliaSourceVolumeEquiv_frameLift_commute`; it is not an input to this
application. The finite source-chart result leaves physical endpoint
instantiation and admission open. -/
theorem archiveJuliaSourceCARRaisingQuery_nonNull_gamma_recovery_of_oriented_isometry
    (u : RoleSpace) (M : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (hIso : ∀ x y, archiveJuliaSourceLorentzForm (M x) (M y) =
      archiveJuliaSourceLorentzForm x y)
    (hOrientation : archiveExteriorFrameLift M
      archiveJuliaSourceVolumeVacuum = archiveJuliaSourceVolumeVacuum)
    (hq : archiveJuliaSourceLorentzForm u u ≠ 0) :
    archiveExteriorFrameLift M =
      (archiveJuliaSourceLorentzForm u u)⁻¹ •
        (archiveJuliaLorentzGamma archiveJuliaSourceLorentzForm u).comp
          (archiveJuliaCARRaisingQuery u M -
            archiveJuliaSourceVolumeEquiv.toLinearMap.comp
              ((archiveJuliaCARRaisingQuery u M).comp
                archiveJuliaSourceVolumeEquiv.symm.toLinearMap)) := by
  exact archiveJuliaCARRaisingQuery_nonNull_gamma_recovery
    archiveJuliaSourceLorentzForm u M archiveJuliaSourceVolumeEquiv
    archiveJuliaSourceVolumeEquiv
    (archiveJuliaSourceVolumeEquiv_creator_conjugation u)
    (archiveJuliaSourceVolumeEquiv_frameLift_commute M hIso hOrientation)
    hq

/-- Identity-transport corollary of the oriented-isometry Eq. (27) recovery in
the source's fixed Lorentz chart. This is a finite-carrier algebraic result;
it does not close physical endpoint selection. -/
theorem archiveJuliaSourceIdentityCARRaisingQuery_nonNull_gamma_recovery
    (u : RoleSpace)
    (hq : archiveJuliaSourceLorentzForm u u ≠ 0) :
    archiveExteriorFrameLift (LinearEquiv.refl ℝ RoleSpace) =
      (archiveJuliaSourceLorentzForm u u)⁻¹ •
        (archiveJuliaLorentzGamma archiveJuliaSourceLorentzForm u).comp
          (archiveJuliaCARRaisingQuery u (LinearEquiv.refl ℝ RoleSpace) -
            archiveJuliaSourceVolumeEquiv.toLinearMap.comp
              ((archiveJuliaCARRaisingQuery u
                (LinearEquiv.refl ℝ RoleSpace)).comp
                archiveJuliaSourceVolumeEquiv.symm.toLinearMap)) := by
  exact archiveJuliaSourceCARRaisingQuery_nonNull_gamma_recovery_of_oriented_isometry
    u (LinearEquiv.refl ℝ RoleSpace)
    (by intro x y; rfl)
    (by rw [archiveExteriorFrameLift_id]; rfl) hq

/-! ### Coordinate determinant adapter for the oriented volume vector

The oriented vector above is the top exterior product of the four role basis
vectors in the source order `A,B,C,D`. The next lemmas identify its frame
action with the ordinary determinant of the role-space linear equivalence.
This replaces vector preservation by the usual determinant-one condition;
it does not instantiate a physical endpoint map.
-/

open ExteriorAlgebra

local instance archiveJuliaSourceRoleLinearOrder : LinearOrder Role :=
  LinearOrder.lift' roleOrderIndex roleOrderIndex_injective

-- Keep sorting and the lifted order on `Role` coherent in this local adapter.
local instance archiveJuliaSourceRoleLE : LE Role :=
  archiveJuliaSourceRoleLinearOrder.toLE

/-- The unique four-element subset of the four-role source space. -/
def archiveJuliaSourceTopSubset : Set.powersetCard Role 4 :=
  ⟨Finset.univ, by simp⟩

private theorem archiveJuliaSourceRoleList_nodup : roleList.Nodup := by
  simp [roleList, D0.A, D0.B, D0.C, D0.D]

private theorem archiveJuliaSourceRoleList_toFinset :
    roleList.toFinset = (Finset.univ : Finset Role) := by
  ext r
  fin_cases r <;> simp [roleList, D0.A, D0.B, D0.C, D0.D]

private theorem archiveJuliaSourceRoleList_pairwise :
    roleList.Pairwise (fun x y => x ≤ y) := by
  have hAB : A ≤ B := by
    change roleOrderIndex A ≤ roleOrderIndex B
    norm_num [roleOrderIndex, D0.A, D0.B, D0.C, D0.D]
  have hAC : A ≤ C := by
    change roleOrderIndex A ≤ roleOrderIndex C
    norm_num [roleOrderIndex, D0.A, D0.B, D0.C, D0.D]
  have hAD : A ≤ D := by
    change roleOrderIndex A ≤ roleOrderIndex D
    norm_num [roleOrderIndex, D0.A, D0.B, D0.C, D0.D]
  have hBC : B ≤ C := by
    change roleOrderIndex B ≤ roleOrderIndex C
    norm_num [roleOrderIndex, D0.A, D0.B, D0.C, D0.D]
  have hBD : B ≤ D := by
    change roleOrderIndex B ≤ roleOrderIndex D
    norm_num [roleOrderIndex, D0.A, D0.B, D0.C, D0.D]
  have hCD : C ≤ D := by
    change roleOrderIndex C ≤ roleOrderIndex D
    norm_num [roleOrderIndex, D0.A, D0.B, D0.C, D0.D]
  simp [List.pairwise_cons, roleList, hAB, hAC, hAD, hBC, hBD, hCD]

private theorem archiveJuliaSourceRoleList_sorted :
    Finset.univ.sort (fun x y => x ≤ y) = roleList := by
  classical
  rw [← archiveJuliaSourceRoleList_toFinset]
  exact
    (List.toFinset_sort (r := fun x y => x ≤ y)
      archiveJuliaSourceRoleList_nodup).2 archiveJuliaSourceRoleList_pairwise

private theorem archiveJuliaSourceTopOrderEmbedding_apply (i : Fin 4) :
    (Set.powersetCard.ofFinEmbEquiv.symm archiveJuliaSourceTopSubset) i =
      roleList[i.val]! := by
  have hmap :
      (List.finRange 4).map
          (Set.powersetCard.ofFinEmbEquiv.symm archiveJuliaSourceTopSubset) =
        roleList := by
    simp only [Set.powersetCard.ofFinEmbEquiv_symm_apply,
      Finset.listMap_orderEmbOfFin_finRange]
    simp only [archiveJuliaSourceTopSubset]
    change Finset.univ.sort (fun a b => a ≤ b) = roleList
    exact archiveJuliaSourceRoleList_sorted
  have hi := congrArg (fun l : List Role => l[i.val]!) hmap
  simpa using hi

private theorem archiveJuliaSourceRoleBasis_top_product :
    archiveRoleBasis.ExteriorAlgebra Finset.univ =
      ι ℝ (archiveRoleBasis A) * ι ℝ (archiveRoleBasis B) *
        ι ℝ (archiveRoleBasis C) * ι ℝ (archiveRoleBasis D) := by
  change archiveRoleBasis.ExteriorAlgebra
    (archiveJuliaSourceTopSubset : Finset Role) = _
  rw [ExteriorAlgebra.basis_apply_powersetCard
    (b := archiveRoleBasis) (s := archiveJuliaSourceTopSubset)]
  simp only [ExteriorAlgebra.ιMulti_family, ExteriorAlgebra.ιMulti_apply]
  simp only [Function.comp_apply, archiveJuliaSourceTopOrderEmbedding_apply]
  simp [List.ofFn, Fin.foldr_succ, roleList, D0.A, D0.B, D0.C, D0.D, mul_assoc]

private def archiveJuliaSourceFullyOccupiedState : ArchiveFockState := fun _ => true

private theorem archiveJuliaSourceSupport_fullyOccupied :
    archiveFockSupport archiveJuliaSourceFullyOccupiedState = Finset.univ := by
  ext r
  simp [archiveFockSupport, archiveJuliaSourceFullyOccupiedState]

private theorem archiveJuliaSourceCreatorLM_equiv (b : RoleSpace)
    (ψ : ArchiveFockState → ℝ) :
    archiveFockExteriorEquiv (archiveExteriorCreatorLM b ψ) =
      ι ℝ b * archiveFockExteriorEquiv ψ := by
  change archiveFockExteriorEquiv (archiveExteriorCreator b ψ) = _
  simp [archiveExteriorCreator]

private theorem archiveJuliaSourceVolumeVacuum_eq_fullyOccupiedState :
    archiveJuliaSourceVolumeVacuum =
      Pi.single archiveJuliaSourceFullyOccupiedState (1 : ℝ) := by
  apply archiveFockExteriorEquiv.injective
  rw [archiveJuliaSourceVolumeVacuum_eq_ordered_creator_product,
    archiveFockExteriorEquiv_single, archiveFockExteriorBasis_apply,
    archiveJuliaSourceSupport_fullyOccupied]
  rw [archiveJuliaSourceCreatorLM_equiv, archiveJuliaSourceCreatorLM_equiv,
    archiveJuliaSourceCreatorLM_equiv, archiveJuliaSourceCreatorLM_equiv,
    archiveFockExteriorEquiv_single_vacuum]
  simpa [mul_assoc] using archiveJuliaSourceRoleBasis_top_product.symm

private theorem archiveJuliaSourceFockExteriorBasis_fullyOccupied :
    archiveFockExteriorBasis archiveJuliaSourceFullyOccupiedState =
      (archiveRoleBasis.exteriorPower 4 archiveJuliaSourceTopSubset : RoleExterior) := by
  rw [archiveFockExteriorBasis_apply, archiveJuliaSourceSupport_fullyOccupied]
  exact ExteriorAlgebra.basis_eq_coe_basis archiveRoleBasis archiveJuliaSourceTopSubset

private theorem archiveJuliaSourceTopSubset_unique
    (T : Set.powersetCard Role 4) : T = archiveJuliaSourceTopSubset := by
  apply Subtype.ext
  apply Finset.eq_of_subset_of_card_le (Finset.subset_univ _)
  have hT : T.val.card = 4 := T.property
  have htop : (Finset.univ : Finset Role).card = 4 := by simp
  rw [htop, hT]

/-- The top exterior-power action is the determinant scalar, derived from
the full 4-by-4 minor on the unique top basis sector. -/
theorem archiveJuliaSourceTopExteriorMap_scale
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    exteriorPower.map 4 M.toLinearMap
        (archiveRoleBasis.exteriorPower 4 archiveJuliaSourceTopSubset) =
      archiveExteriorMinor 4 M archiveJuliaSourceTopSubset
          archiveJuliaSourceTopSubset •
        archiveRoleBasis.exteriorPower 4 archiveJuliaSourceTopSubset := by
  apply (archiveRoleBasis.exteriorPower 4).repr.injective
  ext T
  have hT := archiveJuliaSourceTopSubset_unique T
  subst T
  rw [archiveExteriorPower_coefficient_minor]
  simp

private def archiveJuliaSourceRoleIndex (r : Role) : Fin 4 :=
  ⟨roleOrderIndex r, by
    rcases r with ⟨i, j⟩
    fin_cases i <;> fin_cases j <;>
      norm_num [roleOrderIndex, D0.A, D0.B, D0.C, D0.D]⟩

private theorem archiveJuliaSourceRoleIndex_bijective :
    Function.Bijective archiveJuliaSourceRoleIndex := by
  constructor
  · intro r s h
    apply roleOrderIndex_injective
    exact congrArg Fin.val h
  · intro i
    fin_cases i
    · exact ⟨A, by decide⟩
    · exact ⟨B, by decide⟩
    · exact ⟨C, by decide⟩
    · exact ⟨D, by decide⟩

private def archiveJuliaSourceRoleEquivFin : Role ≃ Fin 4 :=
  Equiv.ofBijective archiveJuliaSourceRoleIndex
    archiveJuliaSourceRoleIndex_bijective

private def archiveJuliaSourceFiniteRoleBasis : Module.Basis (Fin 4) ℝ RoleSpace :=
  archiveRoleBasis.reindex archiveJuliaSourceRoleEquivFin

private theorem archiveJuliaSourceRoleIndex_topEmbedding (i : Fin 4) :
    archiveJuliaSourceRoleIndex
        ((Set.powersetCard.ofFinEmbEquiv.symm archiveJuliaSourceTopSubset) i) = i := by
  fin_cases i <;> norm_num [archiveJuliaSourceTopOrderEmbedding_apply,
    archiveJuliaSourceRoleIndex, roleList, roleOrderIndex,
    D0.A, D0.B, D0.C, D0.D]

private theorem archiveJuliaSourceTopEmbedding_eq_roleEquiv (i : Fin 4) :
    (Set.powersetCard.ofFinEmbEquiv.symm archiveJuliaSourceTopSubset) i =
      archiveJuliaSourceRoleEquivFin.symm i := by
  apply archiveJuliaSourceRoleIndex_bijective.1
  calc
    archiveJuliaSourceRoleIndex
        ((Set.powersetCard.ofFinEmbEquiv.symm archiveJuliaSourceTopSubset) i) = i :=
      archiveJuliaSourceRoleIndex_topEmbedding i
    _ = archiveJuliaSourceRoleIndex (archiveJuliaSourceRoleEquivFin.symm i) :=
      (archiveJuliaSourceRoleEquivFin.apply_symm_apply i).symm

/-- The full top minor uses the usual coordinate determinant on the role
basis, so the exterior orientation scalar is exactly `LinearMap.det M`. -/
theorem archiveJuliaSourceTopMinor_eq_linearMap_det
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    archiveExteriorMinor 4 M archiveJuliaSourceTopSubset
        archiveJuliaSourceTopSubset =
      LinearMap.det M.toLinearMap := by
  unfold archiveExteriorMinor
  rw [← Matrix.det_transpose]
  rw [← LinearMap.det_toMatrix archiveJuliaSourceFiniteRoleBasis M.toLinearMap]
  congr 1
  ext i j
  simp [archiveJuliaSourceFiniteRoleBasis, LinearMap.toMatrix_apply,
    archiveJuliaSourceTopEmbedding_eq_roleEquiv]

/-- On the source-volume vector, the finite frame lift acts by the ordinary
determinant of its role-space map. -/
theorem archiveJuliaSourceVolumeVacuum_frameLift_eq_det_smul
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    archiveExteriorFrameLift M archiveJuliaSourceVolumeVacuum =
      (LinearMap.det M.toLinearMap) • archiveJuliaSourceVolumeVacuum := by
  have hscaled : archiveExteriorFrameLift M archiveJuliaSourceVolumeVacuum =
      archiveExteriorMinor 4 M archiveJuliaSourceTopSubset
        archiveJuliaSourceTopSubset • archiveJuliaSourceVolumeVacuum := by
    rw [archiveJuliaSourceVolumeVacuum_eq_fullyOccupiedState]
    nth_rw 1 [show archiveJuliaSourceFullyOccupiedState =
        archiveFockSupportEquiv.symm archiveJuliaSourceTopSubset.val by
      funext r
      simp [archiveJuliaSourceFullyOccupiedState, archiveFockSupportEquiv,
        archiveJuliaSourceTopSubset]]
    apply archiveFockExteriorEquiv.injective
    rw [archiveExteriorFrameLift_basis_degree 4 M archiveJuliaSourceTopSubset,
      map_smul, archiveFockExteriorEquiv_single,
      archiveJuliaSourceFockExteriorBasis_fullyOccupied,
      archiveJuliaSourceTopExteriorMap_scale]
    rfl
  rw [hscaled, archiveJuliaSourceTopMinor_eq_linearMap_det]

/-- The finite oriented-vector condition is exactly determinant one. This
replaces the vector-valued endpoint hypothesis in the non-null recovery
corollary while retaining the separate physical endpoint-instantiation
obligation. -/
theorem archiveJuliaSourceVolumeVacuum_frameLift_preserved_iff_det_one
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    archiveExteriorFrameLift M archiveJuliaSourceVolumeVacuum =
        archiveJuliaSourceVolumeVacuum ↔
      LinearMap.det M.toLinearMap = 1 := by
  rw [archiveJuliaSourceVolumeVacuum_frameLift_eq_det_smul]
  constructor
  · intro h
    have h' := congrArg
      (fun z : ArchiveFockState → ℝ => z archiveJuliaSourceFullyOccupiedState) h
    simpa [Pi.smul_apply, archiveJuliaSourceVolumeVacuum_eq_fullyOccupiedState] using h'
  · intro h
    rw [h, one_smul]

/-- Eq. (27) recovery for the owned CAR query under a metric isometry with
ordinary determinant one. The determinant adapter proves the oriented-vector
hypothesis internally; endpoint maps and physical admission remain separate. -/
theorem archiveJuliaSourceCARRaisingQuery_nonNull_gamma_recovery_of_det_one
    (u : RoleSpace) (M : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (hIso : ∀ x y, archiveJuliaSourceLorentzForm (M x) (M y) =
      archiveJuliaSourceLorentzForm x y)
    (hDet : LinearMap.det M.toLinearMap = 1)
    (hq : archiveJuliaSourceLorentzForm u u ≠ 0) :
    archiveExteriorFrameLift M =
      (archiveJuliaSourceLorentzForm u u)⁻¹ •
        (archiveJuliaLorentzGamma archiveJuliaSourceLorentzForm u).comp
          (archiveJuliaCARRaisingQuery u M -
            archiveJuliaSourceVolumeEquiv.toLinearMap.comp
              ((archiveJuliaCARRaisingQuery u M).comp
                archiveJuliaSourceVolumeEquiv.symm.toLinearMap)) := by
  exact archiveJuliaSourceCARRaisingQuery_nonNull_gamma_recovery_of_oriented_isometry
    u M hIso
    ((archiveJuliaSourceVolumeVacuum_frameLift_preserved_iff_det_one M).2 hDet) hq

end
end D0.Geometry
