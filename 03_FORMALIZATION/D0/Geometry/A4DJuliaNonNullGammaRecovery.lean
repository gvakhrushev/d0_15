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
that identity with the exact finite query `C(u) ρ(M)`. Its two endpoint
Clifford identities remain explicit hypotheses: conjugating the creator by
the source volume element gives negative metric contraction, and the endpoint
volume elements intertwine the frame lift. They are not inferred from a
query name or from the desired recovered frame. Thus this is the compiled
Eq. (27) algebraic adapter; proving those identities for the source's
proper-Lorentz endpoint package and joining the non-null chart to Eq. (28)
remain separate work. It makes no physical admission or GR-selection claim.
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

/-- Eq. (27) is fully instantiated for the source's fixed Lorentz chart and
identity frame transport, using the CAR volume equivalence at both endpoints.
The theorem is a finite-carrier algebraic specialization, not a general
proper-Lorentz endpoint transport theorem. -/
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
  let M := LinearEquiv.refl ℝ RoleSpace
  let C := archiveExteriorCreatorLM u
  let I := archiveExteriorContraction (archiveJuliaSourceLorentzCovector u)
  let Γ := archiveJuliaLorentzGamma archiveJuliaSourceLorentzForm u
  let X := archiveJuliaCARRaisingQuery u M
  have hQuery : X = C := by
    dsimp [X, C, M]
    rw [archiveJuliaCARRaisingQuery_eq_model, archiveJuliaRaisingQuery,
      archiveExteriorFrameLift_id]
    simp
  have hConjugation := archiveJuliaSourceVolumeEquiv_creator_conjugation u
  have hConjugatedQuery :
      archiveJuliaSourceVolumeEquiv.toLinearMap.comp
          (X.comp archiveJuliaSourceVolumeEquiv.symm.toLinearMap) = -I := by
    rw [hQuery]
    exact hConjugation
  have hDifference :
      X - archiveJuliaSourceVolumeEquiv.toLinearMap.comp
        (X.comp archiveJuliaSourceVolumeEquiv.symm.toLinearMap) = Γ := by
    calc
      X - archiveJuliaSourceVolumeEquiv.toLinearMap.comp
          (X.comp archiveJuliaSourceVolumeEquiv.symm.toLinearMap) =
        C - (-I) := by rw [hConjugatedQuery, hQuery]
      _ = C + I := by ext ψ; simp
      _ = Γ := rfl
  calc
    archiveExteriorFrameLift M = LinearMap.id := by
      dsimp [M]
      exact archiveExteriorFrameLift_id
    _ = (archiveJuliaSourceLorentzForm u u)⁻¹ •
        Γ.comp (X - archiveJuliaSourceVolumeEquiv.toLinearMap.comp
          (X.comp archiveJuliaSourceVolumeEquiv.symm.toLinearMap)) := by
        rw [hDifference, archiveJuliaLorentzGamma_square]
        rw [smul_smul, inv_mul_cancel₀ hq]
        simp

end
end D0.Geometry
