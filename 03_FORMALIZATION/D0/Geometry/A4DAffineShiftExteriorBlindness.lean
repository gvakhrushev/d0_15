import Mathlib.Tactic
import D0.Geometry.ArchiveExteriorPathTransport
import D0.Geometry.ArchiveAffineCartanConnection

/-!
# Channel L: affine-shift exterior blindness

PR #103 `exteriorPathTransport` lifts only the linear factor of affine Cartan path
transport to the existing 16-state exterior/Fock carrier. Equality of linear path
values therefore implies equality of exterior transport; a pure translational
affine value `(I, b)` with `b ≠ 0` still yields identity exterior transport.

This classifies Channel L only. It does **not** claim that no affine-sensitive
matter representation exists, that translations cannot act on an enlarged
site-aware carrier, or that the final elementary letter must factor as a product
of independent channel matrices.
-/

namespace D0.Geometry

open D0

noncomputable section

variable {N : ℕ}

/-! ## Dependence only on the linear path factor -/

theorem exteriorPathTransport_eq_exteriorFrameEquiv_covariantLin
    (A : AffineCartanConnection N ℝ RoleSpace)
    (steps : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    exteriorPathTransport A steps x = exteriorFrameEquiv (covariantLin A steps x) :=
  rfl

theorem exteriorPathTransport_eq_exteriorFrameEquiv_affinePath_lin
    (A : AffineCartanConnection N ℝ RoleSpace)
    (steps : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    exteriorPathTransport A steps x =
      exteriorFrameEquiv (affinePath A steps x).lin := by
  rw [exteriorPathTransport_eq_exteriorFrameEquiv_covariantLin,
    affinePath_lin_eq_covariant]

theorem exteriorPathTransport_eq_of_covariantLin_eq
    {M : ℕ}
    (A : AffineCartanConnection N ℝ RoleSpace)
    (B : AffineCartanConnection M ℝ RoleSpace)
    (p : List ChainStep) (x : ArchiveRolePhaseGroup N)
    (q : List ChainStep) (y : ArchiveRolePhaseGroup M)
    (h : covariantLin A p x = covariantLin B q y) :
    exteriorPathTransport A p x = exteriorPathTransport B q y := by
  simp only [exteriorPathTransport, h]

theorem exteriorPathTransport_eq_of_affinePath_lin_eq
    {M : ℕ}
    (A : AffineCartanConnection N ℝ RoleSpace)
    (B : AffineCartanConnection M ℝ RoleSpace)
    (p : List ChainStep) (x : ArchiveRolePhaseGroup N)
    (q : List ChainStep) (y : ArchiveRolePhaseGroup M)
    (h : (affinePath A p x).lin = (affinePath B q y).lin) :
    exteriorPathTransport A p x = exteriorPathTransport B q y := by
  apply exteriorPathTransport_eq_of_covariantLin_eq
  simpa [affinePath_lin_eq_covariant] using h

/-! ## Identity linear part ⇒ identity exterior transport -/

theorem exteriorFrameEquiv_refl :
    exteriorFrameEquiv (LinearEquiv.refl ℝ RoleSpace) =
      LinearEquiv.refl ℝ (ArchiveFockState → ℝ) := by
  apply LinearEquiv.toLinearMap_injective
  simp [exteriorFrameEquiv, archiveExteriorFrameLift_id]

theorem exteriorPathTransport_of_covariantLin_id
    (A : AffineCartanConnection N ℝ RoleSpace)
    (steps : List ChainStep) (x : ArchiveRolePhaseGroup N)
    (h : covariantLin A steps x = LinearEquiv.refl ℝ RoleSpace) :
    exteriorPathTransport A steps x = LinearEquiv.refl ℝ (ArchiveFockState → ℝ) := by
  simp only [exteriorPathTransport, h, exteriorFrameEquiv_refl]

theorem exteriorPathTransport_of_affinePath_lin_id
    (A : AffineCartanConnection N ℝ RoleSpace)
    (steps : List ChainStep) (x : ArchiveRolePhaseGroup N)
    (h : (affinePath A steps x).lin = LinearEquiv.refl ℝ RoleSpace) :
    exteriorPathTransport A steps x = LinearEquiv.refl ℝ (ArchiveFockState → ℝ) := by
  apply exteriorPathTransport_of_covariantLin_id
  simpa [affinePath_lin_eq_covariant] using h

/-! ## Exact L = 3 owned flat-translation witness -/

abbrev channelL_L3 : ℕ := 1

theorem channelL_L3_fibers : archiveFibers channelL_L3 = 3 := by
  unfold channelL_L3 archiveFibers
  rfl

def channelL_xi : LocalRoleVector channelL_L3 :=
  fun x _ => if x A = 0 then (0 : ℝ) else 1

def channelL_flatTranslation : AffineCartanConnection channelL_L3 ℝ RoleSpace :=
  affineGauge (translationGauge channelL_L3 channelL_xi) (flatAffineConnection channelL_L3)

def channelL_origin : ArchiveRolePhaseGroup channelL_L3 := fun _ => 0

def channelL_oneStep : List ChainStep := [ChainStep.fwd A]

theorem channelL_flatTranslation_lin
    (x : ArchiveRolePhaseGroup channelL_L3) (r : Role) :
    (channelL_flatTranslation x r).lin = LinearEquiv.refl ℝ RoleSpace := by
  simp [channelL_flatTranslation, affineGauge_lin, translationGauge, flatAffineConnection]

theorem channelL_oneStep_lin_id :
    (affinePath channelL_flatTranslation channelL_oneStep channelL_origin).lin =
      LinearEquiv.refl ℝ RoleSpace := by
  simp [channelL_oneStep, affinePath, affineStepMap, channelL_flatTranslation_lin]

theorem channelL_oneStep_shift_eq_forwardGauge :
    (affinePath channelL_flatTranslation channelL_oneStep channelL_origin).shift =
      fun a => forwardGaugeCoframe channelL_L3 channelL_xi channelL_origin A a := by
  ext a
  simp only [channelL_oneStep, affinePath, affineStepMap, AffineCartanMap.affine_mul_one,
    channelL_flatTranslation]
  exact affineTranslation_flat_eq_forwardGaugeCoframe channelL_xi channelL_origin A a

theorem channelL_oneStep_shift_ne_zero :
    (affinePath channelL_flatTranslation channelL_oneStep channelL_origin).shift ≠ 0 := by
  intro h
  have ha := congrFun h A
  rw [channelL_oneStep_shift_eq_forwardGauge] at ha
  have hxi0 : channelL_xi channelL_origin A = 0 := by
    simp [channelL_xi, channelL_origin]
  have hneA : roleTranslatePlus channelL_L3 A channelL_origin A ≠ 0 := by
    simp [roleTranslatePlus_apply, roleStep, channelL_origin, A, Pi.add_apply,
      channelL_L3_fibers]
    decide
  have hxi1 : channelL_xi (roleTranslatePlus channelL_L3 A channelL_origin) A = 1 := by
    simp [channelL_xi, hneA]
  have hL : forwardDifferenceScale channelL_L3 = 3 := by
    simp [forwardDifferenceScale, channelL_L3_fibers]
  simp only [forwardGaugeCoframe, forwardDifference_apply, hL, hxi0, hxi1, sub_zero,
    mul_one] at ha
  exact (by norm_num : (3 : ℝ) ≠ 0) ha

theorem channelL_oneStep_exterior_id :
    exteriorPathTransport channelL_flatTranslation channelL_oneStep channelL_origin =
      LinearEquiv.refl ℝ (ArchiveFockState → ℝ) :=
  exteriorPathTransport_of_affinePath_lin_id _ _ _ channelL_oneStep_lin_id

theorem channelL_affine_shift_exterior_blindness_witness :
    (affinePath channelL_flatTranslation channelL_oneStep channelL_origin).lin =
        LinearEquiv.refl ℝ RoleSpace ∧
      (affinePath channelL_flatTranslation channelL_oneStep channelL_origin).shift ≠ 0 ∧
      exteriorPathTransport channelL_flatTranslation channelL_oneStep channelL_origin =
        LinearEquiv.refl ℝ (ArchiveFockState → ℝ) :=
  ⟨channelL_oneStep_lin_id, channelL_oneStep_shift_ne_zero, channelL_oneStep_exterior_id⟩

/-! ## Same-endpoint comparison (pure translation period word) -/

def channelL_pureShift : RoleSpace := fun _ => (1 : ℝ)

def channelL_pureTranslation : AffineCartanConnection channelL_L3 ℝ RoleSpace :=
  fun _ _ => { lin := LinearEquiv.refl ℝ RoleSpace, shift := channelL_pureShift }

def channelL_periodWord : List ChainStep :=
  [ChainStep.fwd A, ChainStep.fwd A, ChainStep.fwd A]

theorem pathEnd_channelL_periodWord (x : ArchiveRolePhaseGroup channelL_L3) :
    pathEnd channelL_L3 channelL_periodWord x = x := by
  have hunfold :
      pathEnd channelL_L3 channelL_periodWord x =
        roleTranslatePlus channelL_L3 A
          (roleTranslatePlus channelL_L3 A (roleTranslatePlus channelL_L3 A x)) := by
    simp [channelL_periodWord, pathEnd, stepTarget]
  rw [hunfold]
  refine funext fun s => ?_
  simp only [roleTranslatePlus_apply, roleStep, Pi.add_apply]
  by_cases hs : s = A
  · subst hs
    have h3 : (3 : ZMod (archiveFibers channelL_L3)) = 0 := by
      refine Eq.trans ?_ (ZMod.natCast_self (archiveFibers channelL_L3))
      exact congrArg (fun n : ℕ => (n : ZMod (archiveFibers channelL_L3)))
        channelL_L3_fibers.symm
    have hsum : (1 + 1 + 1 : ZMod (archiveFibers channelL_L3)) = 3 := by
      norm_num
    have hassoc : x A + 1 + 1 + 1 = x A + (1 + 1 + 1) := by
      abel
    calc
      x A + 1 + 1 + 1 = x A + (1 + 1 + 1) := hassoc
      _ = x A + 3 := by rw [hsum]
      _ = x A + 0 := by rw [h3]
      _ = x A := by simp
  · simp [hs]

theorem channelL_periodWord_lin_id :
    (affinePath channelL_pureTranslation channelL_periodWord channelL_origin).lin =
      LinearEquiv.refl ℝ RoleSpace := by
  simp [channelL_periodWord, affinePath, affineStepMap, channelL_pureTranslation]

theorem channelL_periodWord_shift :
    (affinePath channelL_pureTranslation channelL_periodWord channelL_origin).shift =
      fun _ => (3 : ℝ) := by
  simp only [channelL_periodWord, affinePath, affineStepMap, channelL_pureTranslation,
    AffineCartanMap.mul_shift, AffineCartanMap.affine_mul_one, LinearEquiv.refl_apply]
  ext a
  simp [channelL_pureShift]
  ring

theorem channelL_periodWord_shift_ne_zero :
    (affinePath channelL_pureTranslation channelL_periodWord channelL_origin).shift ≠ 0 := by
  intro h
  have ha := congrFun h A
  rw [channelL_periodWord_shift] at ha
  exact (by norm_num : (3 : ℝ) ≠ 0) ha

theorem channelL_periodWord_exterior_id :
    exteriorPathTransport channelL_pureTranslation channelL_periodWord channelL_origin =
      LinearEquiv.refl ℝ (ArchiveFockState → ℝ) :=
  exteriorPathTransport_of_affinePath_lin_id _ _ _ channelL_periodWord_lin_id

theorem channelL_same_endpoint_exterior_blind_to_shift :
    pathEnd channelL_L3 channelL_periodWord channelL_origin =
        pathEnd channelL_L3 ([] : List ChainStep) channelL_origin ∧
      (affinePath channelL_pureTranslation channelL_periodWord channelL_origin).lin =
        (affinePath channelL_pureTranslation ([] : List ChainStep) channelL_origin).lin ∧
      (affinePath channelL_pureTranslation channelL_periodWord channelL_origin).shift ≠
        (affinePath channelL_pureTranslation ([] : List ChainStep) channelL_origin).shift ∧
      exteriorPathTransport channelL_pureTranslation channelL_periodWord channelL_origin =
        exteriorPathTransport channelL_pureTranslation ([] : List ChainStep) channelL_origin := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · simpa [pathEnd_nil] using pathEnd_channelL_periodWord channelL_origin
  · simp [channelL_periodWord_lin_id, affinePath]
  · intro h
    have h0 : (affinePath channelL_pureTranslation ([] : List ChainStep) channelL_origin).shift =
        0 := by simp [affinePath]
    rw [h0] at h
    exact channelL_periodWord_shift_ne_zero h
  · rw [channelL_periodWord_exterior_id, exteriorPathTransport_nil]

/-! ## Capstone Channel-L package -/

/-- Capstone reading: PR #103 exterior path transport is Channel L and factors
through the linear affine path part; a pure affine translation belongs to a
different missing channel. Typing interpretation of the factorization boundary,
not a universal impossibility theorem. -/
theorem channelL_exterior_factors_through_linear_affine_path
    (A : AffineCartanConnection N ℝ RoleSpace)
    (steps : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    exteriorPathTransport A steps x =
        exteriorFrameEquiv (affinePath A steps x).lin ∧
      ((affinePath A steps x).lin = LinearEquiv.refl ℝ RoleSpace →
        exteriorPathTransport A steps x =
          LinearEquiv.refl ℝ (ArchiveFockState → ℝ)) :=
  ⟨exteriorPathTransport_eq_exteriorFrameEquiv_affinePath_lin A steps x,
    exteriorPathTransport_of_affinePath_lin_id A steps x⟩

theorem channelL_affine_shift_exterior_blindness_package :
    (∀ (A : AffineCartanConnection channelL_L3 ℝ RoleSpace)
        (steps : List ChainStep) (x : ArchiveRolePhaseGroup channelL_L3),
      exteriorPathTransport A steps x =
        exteriorFrameEquiv (affinePath A steps x).lin) ∧
      (affinePath channelL_flatTranslation channelL_oneStep channelL_origin).lin =
        LinearEquiv.refl ℝ RoleSpace ∧
      (affinePath channelL_flatTranslation channelL_oneStep channelL_origin).shift ≠ 0 ∧
      exteriorPathTransport channelL_flatTranslation channelL_oneStep channelL_origin =
        LinearEquiv.refl ℝ (ArchiveFockState → ℝ) ∧
      pathEnd channelL_L3 channelL_periodWord channelL_origin =
        pathEnd channelL_L3 ([] : List ChainStep) channelL_origin ∧
      (affinePath channelL_pureTranslation channelL_periodWord channelL_origin).lin =
        (affinePath channelL_pureTranslation ([] : List ChainStep) channelL_origin).lin ∧
      (affinePath channelL_pureTranslation channelL_periodWord channelL_origin).shift ≠
        (affinePath channelL_pureTranslation ([] : List ChainStep) channelL_origin).shift ∧
      exteriorPathTransport channelL_pureTranslation channelL_periodWord channelL_origin =
        exteriorPathTransport channelL_pureTranslation ([] : List ChainStep)
          channelL_origin := by
  refine ⟨fun A steps x =>
    exteriorPathTransport_eq_exteriorFrameEquiv_affinePath_lin A steps x, ?_⟩
  exact ⟨channelL_oneStep_lin_id, channelL_oneStep_shift_ne_zero,
    channelL_oneStep_exterior_id,
    channelL_same_endpoint_exterior_blind_to_shift.1,
    channelL_same_endpoint_exterior_blind_to_shift.2.1,
    channelL_same_endpoint_exterior_blind_to_shift.2.2.1,
    channelL_same_endpoint_exterior_blind_to_shift.2.2.2⟩

#print axioms exteriorPathTransport_eq_of_covariantLin_eq
#print axioms exteriorPathTransport_of_affinePath_lin_id
#print axioms channelL_affine_shift_exterior_blindness_witness
#print axioms channelL_same_endpoint_exterior_blind_to_shift
#print axioms channelL_exterior_factors_through_linear_affine_path
#print axioms channelL_affine_shift_exterior_blindness_package

end

end D0.Geometry
