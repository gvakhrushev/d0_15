import Mathlib.Tactic
import D0.Geometry.A4DTransportedReferenceMismatch

/-!
# Scoped constant source/target/shift linear reference-candidate no-go

Lean-owns theorem-ready handoff A/B from
`MEMO_A4D_SOLDER_REFERENCE_LEG_SECTION.md` (PR #114 research):

the constant-coefficient source-typed ansatz

\[
q_{a,c,d}
=
a\,v_y + c\,L^{-1}v_x + d\,L^{-1}b
\]

cannot simultaneously satisfy flat normalization, exact pure-gauge cancellation
on the explicit L=3 equal-neighbour witness, and nonzero pure affine-shift
visibility.

This is a **candidate-class** no-go only. It does not choose a physical `q`,
does not claim a universal obstruction against nonlinear / nonlocal / observer /
path selectors, and does not start finite E dressing.
-/

namespace D0.Geometry

open D0

local instance referenceLocalCandidateNoGoRoleLinearOrder : LinearOrder Role :=
  LinearOrder.lift' roleCode roleCode_injective

set_option linter.unusedSimpArgs false

noncomputable section

/-! ## 1. Candidate definition (RoleSpace / source-typed) -/

/-- Constant-coefficient source-typed linear ansatz
`q = a • v_y + c • L.symm v_x + d • L.symm b`. -/
def constantLinearReferenceCandidate (a c d : ℝ)
    (L : RoleSpace ≃ₗ[ℝ] RoleSpace) (v_y v_x b : RoleSpace) : RoleSpace :=
  a • v_y + c • (L.symm v_x) + d • (L.symm b)

/-- Edge mismatch for an affine pull `(L,b)` against target solder `v_x`:
`κ = L q + b - v_x` (= `AffineCartanMap.apply` form). -/
def candidateEdgeMismatch (L : RoleSpace ≃ₗ[ℝ] RoleSpace) (b v_x q : RoleSpace) :
    RoleSpace :=
  L q + b - v_x

theorem candidateEdgeMismatch_eq_apply (L : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (b v_x q : RoleSpace) :
    candidateEdgeMismatch L b v_x q =
      AffineCartanMap.apply ({ lin := L, shift := b } : AffineCartanMap ℝ RoleSpace) q - v_x := by
  rfl

theorem constantLinearReferenceCandidate_mismatch (a c d : ℝ)
    (L : RoleSpace ≃ₗ[ℝ] RoleSpace) (v_y v_x b : RoleSpace) :
    candidateEdgeMismatch L b v_x
        (constantLinearReferenceCandidate a c d L v_y v_x b) =
      a • (L v_y) + c • v_x + (d + 1) • b - v_x := by
  simp only [candidateEdgeMismatch, constantLinearReferenceCandidate, map_add, map_smul,
    LinearEquiv.apply_symm_apply, add_smul, one_smul]
  abel

/-! ## 2. Flat normalization ⇒ a + c = 1 -/

theorem constantLinearReferenceCandidate_flat
    (a c d : ℝ) (r : Role) :
    constantLinearReferenceCandidate a c d (LinearEquiv.refl ℝ RoleSpace)
        (archiveRoleBasis r) (archiveRoleBasis r) (0 : RoleSpace) =
      (a + c) • archiveRoleBasis r := by
  simp [constantLinearReferenceCandidate, add_smul]

theorem candidateEdgeMismatch_flat_basis (a c d : ℝ) (r : Role) :
    candidateEdgeMismatch (LinearEquiv.refl ℝ RoleSpace) 0 (archiveRoleBasis r)
        (constantLinearReferenceCandidate a c d (LinearEquiv.refl ℝ RoleSpace)
          (archiveRoleBasis r) (archiveRoleBasis r) 0) =
      (a + c - 1) • archiveRoleBasis r := by
  simp only [constantLinearReferenceCandidate_flat, candidateEdgeMismatch,
    LinearEquiv.refl_apply, add_zero]
  module

/-- Flat control `κ = 0` on `archiveRoleBasis r` forces `a + c = 1`. -/
theorem flat_normalization_forces_sum_coeff (a c d : ℝ) (r : Role)
    (hκ : candidateEdgeMismatch (LinearEquiv.refl ℝ RoleSpace) 0 (archiveRoleBasis r)
      (constantLinearReferenceCandidate a c d (LinearEquiv.refl ℝ RoleSpace)
        (archiveRoleBasis r) (archiveRoleBasis r) 0) = 0) :
    a + c = 1 := by
  have h := candidateEdgeMismatch_flat_basis a c d r
  rw [hκ] at h
  have hr : (archiveRoleBasis r : RoleSpace) ≠ 0 := by
    intro hz
    have := congrArg (fun v : RoleSpace => v r) hz
    simp [archiveRoleBasis, Pi.basisFun_apply, Pi.single_apply] at this
  have hcoeff : a + c - 1 = 0 := (smul_eq_zero.mp h.symm).resolve_right hr
  linarith

/-- Matching flat force via `transportedReferenceMismatch` on the constant ansatz field. -/
theorem flat_normalization_forces_sum_coeff_transported (N : ℕ) (a c d : ℝ)
    (x : ArchiveRolePhaseGroup N) (r : Role)
    (hκ : transportedReferenceMismatch (flatAffineConnection N) (0 : LocalCoframeField N)
      (fun _ s => constantLinearReferenceCandidate a c d (LinearEquiv.refl ℝ RoleSpace)
        (archiveRoleBasis s) (archiveRoleBasis s) 0) x r = 0) :
    a + c = 1 := by
  have hflat :
      transportedReferenceMismatch (flatAffineConnection N) (0 : LocalCoframeField N)
        (fun _ s => constantLinearReferenceCandidate a c d (LinearEquiv.refl ℝ RoleSpace)
          (archiveRoleBasis s) (archiveRoleBasis s) 0) x r =
      candidateEdgeMismatch (LinearEquiv.refl ℝ RoleSpace) 0 (archiveRoleBasis r)
        (constantLinearReferenceCandidate a c d (LinearEquiv.refl ℝ RoleSpace)
          (archiveRoleBasis r) (archiveRoleBasis r) 0) := by
    simp only [transportedReferenceMismatch, flatAffineConnection, AffineCartanMap.apply,
      AffineCartanMap.one_lin, AffineCartanMap.one_shift, LinearEquiv.refl_apply,
      solderLegVector_zero, candidateEdgeMismatch, add_zero]
  exact flat_normalization_forces_sum_coeff a c d r (hflat ▸ hκ)

/-! ## 3. Explicit L = 3 equal-neighbour pure-gauge witness (memo §6) -/

/-- Period `L = N+2 = 3`. -/
abbrev equalNeighbourN : ℕ := 1

theorem equalNeighbourN_fibers : archiveFibers equalNeighbourN = 3 := by
  unfold equalNeighbourN archiveFibers
  rfl

/-- Potential with sole internal Role-B component `φ^B = (0,1,2)` on the A-cycle. -/
def equalNeighbourPhi : LocalRoleVector equalNeighbourN :=
  fun x a =>
    if a = B then
      if x A = 0 then (0 : ℝ) else if x A = 1 then (1 : ℝ) else (2 : ℝ)
    else 0

def equalNeighbourCoframe : LocalCoframeField equalNeighbourN :=
  forwardGaugeCoframe equalNeighbourN equalNeighbourPhi

def equalNeighbourConnection : AffineCartanConnection equalNeighbourN ℝ RoleSpace :=
  affineGauge (translationGauge equalNeighbourN equalNeighbourPhi)
    (flatAffineConnection equalNeighbourN)

def equalNeighbourOrigin : ArchiveRolePhaseGroup equalNeighbourN := fun _ => 0

theorem equalNeighbourConnection_lin
    (x : ArchiveRolePhaseGroup equalNeighbourN) (r : Role) :
    (equalNeighbourConnection x r).lin = LinearEquiv.refl ℝ RoleSpace := by
  simp [equalNeighbourConnection, affineGauge_lin, translationGauge, flatAffineConnection]

theorem equalNeighbour_shift_eq_forwardGauge
    (x : ArchiveRolePhaseGroup equalNeighbourN) (r a : Role) :
    (equalNeighbourConnection x r).shift a =
      forwardGaugeCoframe equalNeighbourN equalNeighbourPhi x r a :=
  affineTranslation_flat_eq_forwardGaugeCoframe equalNeighbourPhi x r a

private theorem equalNeighbour_fwd_scale :
    forwardDifferenceScale equalNeighbourN = 3 := by
  simp [forwardDifferenceScale, equalNeighbourN_fibers]

private theorem equalNeighbour_origin_A_ne_zero :
    roleTranslatePlus equalNeighbourN A equalNeighbourOrigin A ≠ 0 := by
  simp [roleTranslatePlus_apply, roleStep, equalNeighbourOrigin, A, Pi.add_apply,
    equalNeighbourN_fibers]
  decide

private theorem equalNeighbour_phi_origin_B :
    equalNeighbourPhi equalNeighbourOrigin B = 0 := by
  simp [equalNeighbourPhi, equalNeighbourOrigin]

private theorem equalNeighbour_phi_one_B :
    equalNeighbourPhi (roleTranslatePlus equalNeighbourN A equalNeighbourOrigin) B = 1 := by
  have hne : (1 : ZMod (archiveFibers equalNeighbourN)) ≠ 0 := by
    simp [equalNeighbourN_fibers]; decide
  have hone : (1 : ZMod (archiveFibers equalNeighbourN)) = 1 := rfl
  simp [equalNeighbourPhi, roleTranslatePlus_apply, roleStep, equalNeighbourOrigin, A,
    Pi.add_apply, hne, equalNeighbourN_fibers]

private theorem equalNeighbour_phi_two_B :
    equalNeighbourPhi
      (roleTranslatePlus equalNeighbourN A
        (roleTranslatePlus equalNeighbourN A equalNeighbourOrigin)) B = 2 := by
  have hne1 : (1 : ZMod (archiveFibers equalNeighbourN)) ≠ 0 := by
    simp [equalNeighbourN_fibers]; decide
  have hne2 : (1 + 1 : ZMod (archiveFibers equalNeighbourN)) ≠ 0 := by
    simp [equalNeighbourN_fibers]; decide
  have hne21 : (1 + 1 : ZMod (archiveFibers equalNeighbourN)) ≠ 1 := by
    simp [equalNeighbourN_fibers]; decide
  simp [equalNeighbourPhi, roleTranslatePlus_apply, roleStep, equalNeighbourOrigin, A,
    Pi.add_apply, hne1, hne2, hne21]

/-- A-row coframe strain vanishes off Role B. -/
theorem equalNeighbour_coframe_A_off_B
    (x : ArchiveRolePhaseGroup equalNeighbourN) {a : Role} (ha : a ≠ B) :
    equalNeighbourCoframe x A a = 0 := by
  simp only [equalNeighbourCoframe, forwardGaugeCoframe, forwardDifference_apply,
    equalNeighbourPhi]
  rw [if_neg ha, if_neg ha]
  simp

/-- First A-edge B-strain at the origin is `3` (memo `(3,3,-6)e_B`). -/
theorem equalNeighbour_origin_A_B_strain :
    equalNeighbourCoframe equalNeighbourOrigin A B = 3 := by
  simp [equalNeighbourCoframe, forwardGaugeCoframe, forwardDifference_apply,
    equalNeighbour_fwd_scale, equalNeighbour_phi_origin_B, equalNeighbour_phi_one_B]

theorem equalNeighbour_origin_A_shift_B :
    (equalNeighbourConnection equalNeighbourOrigin A).shift B = 3 := by
  rw [equalNeighbour_shift_eq_forwardGauge]
  simpa [equalNeighbourCoframe] using equalNeighbour_origin_A_B_strain

theorem equalNeighbour_origin_shift_eq :
    (equalNeighbourConnection equalNeighbourOrigin A).shift =
      (3 : ℝ) • (Pi.single B (1 : ℝ) : RoleSpace) := by
  ext a
  rw [equalNeighbour_shift_eq_forwardGauge, Pi.smul_apply, Pi.single_apply, smul_eq_mul]
  by_cases ha : a = B
  · subst ha
    simpa [equalNeighbourCoframe, mul_one] using equalNeighbour_origin_A_B_strain
  · have h := equalNeighbour_coframe_A_off_B equalNeighbourOrigin ha
    simp only [equalNeighbourCoframe] at h
    simp [h, ha]

theorem equalNeighbour_origin_shift_ne_zero :
    (equalNeighbourConnection equalNeighbourOrigin A).shift ≠ 0 := by
  intro h
  have := congrArg (fun v : RoleSpace => v B) h
  simp [equalNeighbour_origin_A_shift_B] at this

/-- Neighbour site `0+A` also has A-edge B-strain `3`. -/
theorem equalNeighbour_neighbour_A_B_strain :
    equalNeighbourCoframe (roleTranslatePlus equalNeighbourN A equalNeighbourOrigin) A B = 3 := by
  simp only [equalNeighbourCoframe, forwardGaugeCoframe, forwardDifference_apply,
    equalNeighbour_fwd_scale, equalNeighbour_phi_one_B, equalNeighbour_phi_two_B]
  norm_num

private theorem equalNeighbour_solder_A_of_strain
    (x : ArchiveRolePhaseGroup equalNeighbourN)
    (hB : equalNeighbourCoframe x A B = 3)
    (hoff : ∀ a : Role, a ≠ B → equalNeighbourCoframe x A a = 0) :
    solderLegVector equalNeighbourN equalNeighbourCoframe x A =
      archiveRoleBasis A - (3 : ℝ) • (Pi.single B (1 : ℝ) : RoleSpace) := by
  ext s
  simp only [solderLegVector, rawSolderMatrix, roleLorentzMetric, Matrix.mulVec_diagonal,
    Matrix.diagonal_apply, archiveRoleBasis, Pi.basisFun_apply, Pi.single_apply, Pi.sub_apply,
    Pi.smul_apply, smul_eq_mul]
  have hAB : A ≠ B := by decide
  by_cases hsB : s = B
  · subst hsB
    simp [hB, hAB, roleLorentzSign_B, Ne.symm hAB]
  · by_cases hsA : s = A
    · subst hsA
      have he : equalNeighbourCoframe x A A = 0 := hoff A (by decide)
      simp [hsB, he, roleLorentzSign_A, roleLorentzSign_mul_self]
    · have he : equalNeighbourCoframe x A s = 0 := hoff s hsB
      simp [hsB, hsA, he, roleLorentzMetric, Matrix.diagonal_apply, mul_zero]
      intro hAs
      exact (hsA hAs.symm).elim

/-- Equal-neighbour property: adjacent A solder legs coincide (= `e_A - 3 e_B`). -/
theorem equalNeighbour_solder_legs_equal :
    solderLegVector equalNeighbourN equalNeighbourCoframe equalNeighbourOrigin A =
      solderLegVector equalNeighbourN equalNeighbourCoframe
        (roleTranslatePlus equalNeighbourN A equalNeighbourOrigin) A := by
  have h0 := equalNeighbour_solder_A_of_strain equalNeighbourOrigin
    equalNeighbour_origin_A_B_strain
    (fun a ha => equalNeighbour_coframe_A_off_B equalNeighbourOrigin ha)
  have h1 := equalNeighbour_solder_A_of_strain
    (roleTranslatePlus equalNeighbourN A equalNeighbourOrigin)
    equalNeighbour_neighbour_A_B_strain
    (fun a ha => equalNeighbour_coframe_A_off_B _ ha)
  rw [h0, h1]

theorem equalNeighbour_solder_leg_explicit :
    solderLegVector equalNeighbourN equalNeighbourCoframe equalNeighbourOrigin A =
      archiveRoleBasis A - (3 : ℝ) • (Pi.single B (1 : ℝ) : RoleSpace) :=
  equalNeighbour_solder_A_of_strain equalNeighbourOrigin
    equalNeighbour_origin_A_B_strain
    (fun _ ha => equalNeighbour_coframe_A_off_B equalNeighbourOrigin ha)

/-! ## 3b. Flat-normalized cancellation on the L=3 witness ⇒ d = -1 -/

private theorem candidate_eq_v_add_d_smul (a c d : ℝ) (hac : a + c = 1)
    (v b : RoleSpace) :
    constantLinearReferenceCandidate a c d (LinearEquiv.refl ℝ RoleSpace) v v b =
      v + d • b := by
  simp [constantLinearReferenceCandidate, ← add_smul, hac, one_smul]

/-- Under `a+c=1` and equal neighbours with `L = I`, exact cancellation forces `d = -1`. -/
theorem equalNeighbour_forces_d_neg_one (a c d : ℝ) (hac : a + c = 1)
    (v b : RoleSpace)
    (hb : b = (equalNeighbourConnection equalNeighbourOrigin A).shift)
    (hκ : candidateEdgeMismatch (LinearEquiv.refl ℝ RoleSpace) b v
      (constantLinearReferenceCandidate a c d (LinearEquiv.refl ℝ RoleSpace) v v b) = 0) :
    d = -1 := by
  have hvb := candidate_eq_v_add_d_smul a c d hac v b
  have hmis :
      candidateEdgeMismatch (LinearEquiv.refl ℝ RoleSpace) b v
        (constantLinearReferenceCandidate a c d (LinearEquiv.refl ℝ RoleSpace) v v b) =
        (d + 1) • b := by
    simp only [hvb, candidateEdgeMismatch, LinearEquiv.refl_apply, add_smul, one_smul]
    abel
  have hbne : b ≠ 0 := by
    rw [hb]
    exact equalNeighbour_origin_shift_ne_zero
  have hzero : (d + 1) • b = 0 := by
    simpa [hmis] using hκ
  have hcoeff : d + 1 = 0 := (smul_eq_zero.mp hzero).resolve_right hbne
  linarith

/-- Explicit B-coordinate form of the same force (nonzero witness component `3`). -/
theorem equalNeighbour_forces_d_neg_one_coord (a c d : ℝ) (hac : a + c = 1)
    (hκ : candidateEdgeMismatch (LinearEquiv.refl ℝ RoleSpace)
      ((equalNeighbourConnection equalNeighbourOrigin A).shift)
      (solderLegVector equalNeighbourN equalNeighbourCoframe equalNeighbourOrigin A)
      (constantLinearReferenceCandidate a c d (LinearEquiv.refl ℝ RoleSpace)
        (solderLegVector equalNeighbourN equalNeighbourCoframe equalNeighbourOrigin A)
        (solderLegVector equalNeighbourN equalNeighbourCoframe equalNeighbourOrigin A)
        (equalNeighbourConnection equalNeighbourOrigin A).shift) = 0) :
    d = -1 := by
  set v := solderLegVector equalNeighbourN equalNeighbourCoframe equalNeighbourOrigin A
  set b := (equalNeighbourConnection equalNeighbourOrigin A).shift
  have hvb := candidate_eq_v_add_d_smul a c d hac v b
  have hB :
      (candidateEdgeMismatch (LinearEquiv.refl ℝ RoleSpace) b v
        (constantLinearReferenceCandidate a c d (LinearEquiv.refl ℝ RoleSpace) v v b)) B =
        (d + 1) * 3 := by
    have hbB : b B = 3 := equalNeighbour_origin_A_shift_B
    simp only [hvb, candidateEdgeMismatch, LinearEquiv.refl_apply, Pi.add_apply, Pi.sub_apply,
      Pi.smul_apply, smul_eq_mul, hbB]
    ring
  have hκB := congrArg (fun w : RoleSpace => w B) hκ
  have : (d + 1) * (3 : ℝ) = 0 := by
    simpa [hB] using hκB
  have h3 : (3 : ℝ) ≠ 0 := by norm_num
  have hcoeff : d + 1 = 0 := (mul_eq_zero.mp this).resolve_right h3
  linarith

/-! ## 4. Pure-shift contradiction for forced coefficients -/

/-- Forced coefficients on a pure affine shift give `q = e_r - b`. -/
theorem forced_candidate_pureShift_q (a c : ℝ) (b : RoleSpace) (r : Role)
    (hac : a + c = 1) :
    constantLinearReferenceCandidate a c (-1) (LinearEquiv.refl ℝ RoleSpace)
        (archiveRoleBasis r) (archiveRoleBasis r) b =
      archiveRoleBasis r - b := by
  simp [constantLinearReferenceCandidate, ← add_smul, hac, one_smul, neg_smul]
  abel

/-- Forced coefficients erase pure-shift visibility: `κ = 0`. -/
theorem forced_candidate_pureShift_mismatch_zero (a c : ℝ) (b : RoleSpace) (r : Role)
    (hac : a + c = 1) :
    candidateEdgeMismatch (LinearEquiv.refl ℝ RoleSpace) b (archiveRoleBasis r)
      (constantLinearReferenceCandidate a c (-1) (LinearEquiv.refl ℝ RoleSpace)
        (archiveRoleBasis r) (archiveRoleBasis r) b) = 0 := by
  simp only [forced_candidate_pureShift_q a c b r hac, candidateEdgeMismatch,
    LinearEquiv.refl_apply]
  abel

/-- Same statement via `transportedReferenceMismatch` / `pureShiftAffineConnection`. -/
theorem forced_candidate_pureShift_transported_zero (N : ℕ) (a c : ℝ) (b : RoleSpace)
    (x : ArchiveRolePhaseGroup N) (r : Role) (hac : a + c = 1) :
    transportedReferenceMismatch (pureShiftAffineConnection N b) (0 : LocalCoframeField N)
      (fun _ s => constantLinearReferenceCandidate a c (-1) (LinearEquiv.refl ℝ RoleSpace)
        (archiveRoleBasis s) (archiveRoleBasis s) b) x r = 0 := by
  simp only [transportedReferenceMismatch, pureShiftAffineConnection, AffineCartanMap.apply,
    LinearEquiv.refl_apply, solderLegVector_zero, forced_candidate_pureShift_q a c b r hac]
  abel

/-- Required pure-shift visibility for `archiveRoleBasisReference` is `κ = b`. -/
theorem archiveRoleBasisReference_pureShift_visibility (N : ℕ) (b : RoleSpace)
    (x : ArchiveRolePhaseGroup N) (r : Role) :
    transportedReferenceMismatch (pureShiftAffineConnection N b) (0 : LocalCoframeField N)
      (archiveRoleBasisReference N) x r = b :=
  transportedReferenceMismatch_pureShift b x r

/-- Scoped no-go: no constant linear combination in this candidate class closes all controls. -/
theorem constantLinearReferenceCandidate_no_go (a c d : ℝ) (r : Role)
    (hflat : candidateEdgeMismatch (LinearEquiv.refl ℝ RoleSpace) 0 (archiveRoleBasis r)
      (constantLinearReferenceCandidate a c d (LinearEquiv.refl ℝ RoleSpace)
        (archiveRoleBasis r) (archiveRoleBasis r) 0) = 0)
    (hgauge : candidateEdgeMismatch (LinearEquiv.refl ℝ RoleSpace)
      ((equalNeighbourConnection equalNeighbourOrigin A).shift)
      (solderLegVector equalNeighbourN equalNeighbourCoframe equalNeighbourOrigin A)
      (constantLinearReferenceCandidate a c d (LinearEquiv.refl ℝ RoleSpace)
        (solderLegVector equalNeighbourN equalNeighbourCoframe equalNeighbourOrigin A)
        (solderLegVector equalNeighbourN equalNeighbourCoframe equalNeighbourOrigin A)
        (equalNeighbourConnection equalNeighbourOrigin A).shift) = 0)
    (b : RoleSpace) (hb : b ≠ 0) :
    ¬ (candidateEdgeMismatch (LinearEquiv.refl ℝ RoleSpace) b (archiveRoleBasis r)
        (constantLinearReferenceCandidate a c d (LinearEquiv.refl ℝ RoleSpace)
          (archiveRoleBasis r) (archiveRoleBasis r) b) = b) := by
  intro hvis
  have hac : a + c = 1 := flat_normalization_forces_sum_coeff a c d r hflat
  have hd : d = -1 := equalNeighbour_forces_d_neg_one_coord a c d hac hgauge
  subst hd
  have hzero := forced_candidate_pureShift_mismatch_zero a c b r hac
  have : b = 0 := by
    simpa [hzero] using hvis.symm
  exact hb this

/-! ## 5. Predecessor endpoint corollaries -/

/-- Endpoint `q = L.symm v_x` has `κ = b` identically. -/
theorem predecessor_endpoint_transport_mismatch
    (L : RoleSpace ≃ₗ[ℝ] RoleSpace) (b v_x : RoleSpace) :
    candidateEdgeMismatch L b v_x (L.symm v_x) = b := by
  simp [candidateEdgeMismatch, LinearEquiv.apply_symm_apply]

/-- Endpoint `q = L.symm (v_x - b)` has `κ = 0` identically (tautological cancel). -/
theorem predecessor_endpoint_affineInverse_mismatch
    (L : RoleSpace ≃ₗ[ℝ] RoleSpace) (b v_x : RoleSpace) :
    candidateEdgeMismatch L b v_x (L.symm (v_x - b)) = 0 := by
  simp [candidateEdgeMismatch, map_sub, LinearEquiv.apply_symm_apply]

/-- Specialization `L = I`: `q = v_x` ⇒ `κ = b`. -/
theorem predecessor_endpoint_transport_mismatch_id (b v_x : RoleSpace) :
    candidateEdgeMismatch (LinearEquiv.refl ℝ RoleSpace) b v_x v_x = b :=
  predecessor_endpoint_transport_mismatch (LinearEquiv.refl ℝ RoleSpace) b v_x

/-- Specialization `L = I`: `q = v_x - b` ⇒ `κ = 0`. -/
theorem predecessor_endpoint_affineInverse_mismatch_id (b v_x : RoleSpace) :
    candidateEdgeMismatch (LinearEquiv.refl ℝ RoleSpace) b v_x (v_x - b) = 0 :=
  predecessor_endpoint_affineInverse_mismatch (LinearEquiv.refl ℝ RoleSpace) b v_x

#print axioms flat_normalization_forces_sum_coeff
#print axioms equalNeighbour_forces_d_neg_one_coord
#print axioms forced_candidate_pureShift_mismatch_zero
#print axioms constantLinearReferenceCandidate_no_go
#print axioms predecessor_endpoint_transport_mismatch
#print axioms predecessor_endpoint_affineInverse_mismatch

end

end D0.Geometry
