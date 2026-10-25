import Mathlib.Tactic
import Mathlib.LinearAlgebra.ExteriorPower.Basic
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import D0.Algebra.FiniteGramTangent
import D0.Geometry.A4DRawSolderFrameAction
import D0.Geometry.ArchiveAffineExteriorLink
import D0.Geometry.A4DObserverPositiveExterior

/-!
# Finite nonlinear local-Lorentz quotient layer

This module formalizes the finite site-dependent Lorentz layer selected by the
merged nonlinear quotient research. Affine translations do not occur here.
-/

namespace D0.Geometry

open D0
open scoped BigOperators

noncomputable section

variable {N : ℕ}

abbrev A4DLinearLinkField (N : ℕ) :=
  ArchiveRolePhaseGroup N → Role → Matrix Role Role ℝ

def a4dFiniteLorentzLinkAction (N : ℕ) (L : A4DLinearLinkField N)
    (Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ) :
    A4DLinearLinkField N :=
  fun x r =>
    (Λ x)⁻¹ * L x r * Λ (roleTranslatePlus N r x)

@[simp] theorem a4dFiniteLorentzLinkAction_apply
    (L : A4DLinearLinkField N)
    (Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (x : ArchiveRolePhaseGroup N) (r : Role) :
    a4dFiniteLorentzLinkAction N L Λ x r =
      (Λ x)⁻¹ * L x r * Λ (roleTranslatePlus N r x) := rfl

theorem affineGauge_lin_is_sitewise_lorentz_conjugation
    (h : AffineNodeGauge N ℝ RoleSpace)
    (A : AffineCartanConnection N ℝ RoleSpace)
    (x : ArchiveRolePhaseGroup N) (r : Role) :
    (affineGauge h A x r).lin =
      ((h (roleTranslatePlus N r x)).lin.symm).trans
        ((A x r).lin.trans (h x).lin) :=
  affineGauge_lin h A x r

/-!
The curvature/bivector covariance layer is intentionally not promoted here.
The first worker draft exposed an orientation mismatch in the attempted
odd-curvature conjugation lemma and an incomplete exterior-power proof.
This module therefore closes only the already stable quotient-coordinate and
stabilizer core; the omitted covariance layer requires a separate strengthening
task rather than a `sorry`.
-/

def a4dSiteGram (N : ℕ) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) : Matrix Role Role ℝ :=
  D0.Algebra.finiteGram roleLorentzMetric (rawSolderMatrix N e x)

/-- At a nondegenerate solder frame, equality of the site Gram matrices is
equivalent to one right action by the full Lorentz isometry group.  The
statement uses `IsRoleLorentz` as defined in the finite carrier, so it does
not silently restrict the discrete orientation components to `SO⁺(1,3)`. -/
theorem a4dRightLorentz_gram_complete
    (Θ Ψ : Matrix Role Role ℝ) (hΘ : IsUnit Θ.det) :
    D0.Algebra.finiteGram roleLorentzMetric Θ =
        D0.Algebra.finiteGram roleLorentzMetric Ψ ↔
      ∃ Λ : Matrix Role Role ℝ,
        IsRoleLorentz Λ ∧ Ψ = Θ * Λ := by
  constructor
  · intro hgram
    rcases
      (D0.Algebra.finiteGram_right_orbit_complete roleLorentzMetric Θ Ψ hΘ).mp
        hgram with
      ⟨Λ, hΛ, hΨ⟩
    exact ⟨Λ, by simpa [D0.Algebra.finiteGram, IsRoleLorentz] using hΛ, hΨ⟩
  · rintro ⟨Λ, hΛ, hΨ⟩
    apply
      (D0.Algebra.finiteGram_right_orbit_complete roleLorentzMetric Θ Ψ hΘ).mpr
    refine ⟨Λ, ?_, hΨ⟩
    simpa [D0.Algebra.finiteGram, IsRoleLorentz] using hΛ

/-- The determinant-one subgroup of the finite Lorentz isometries. This
records spatial orientation; it does not impose a time-orientation component. -/
def IsProperRoleLorentz (Λ : Matrix Role Role ℝ) : Prop :=
  IsRoleLorentz Λ ∧ Matrix.det Λ = 1

/-- Two nondegenerate solder frames lie in the same determinant-orientation
component exactly when the product of their determinants is positive. -/
def a4dSameFrameOrientation (Θ Ψ : Matrix Role Role ℝ) : Prop :=
  0 < Θ.det * Ψ.det

/-- A Lorentz frame witness between equally oriented invertible solder frames
has determinant one, so it belongs to the proper determinant component. -/
theorem a4dRightLorentz_sameOrientation_isProper
    (Θ Ψ Λ : Matrix Role Role ℝ)
    (hΘ : IsUnit Θ.det) (hΛ : IsRoleLorentz Λ)
    (hΨ : Ψ = Θ * Λ)
    (hOrientation : a4dSameFrameOrientation Θ Ψ) :
    IsProperRoleLorentz Λ := by
  have hdetEq : Ψ.det = Θ.det * Λ.det := by
    rw [hΨ, Matrix.det_mul]
  have hΘne : Θ.det ≠ 0 := (isUnit_iff_ne_zero).mp hΘ
  have hΘsq : 0 < Θ.det ^ 2 := sq_pos_of_ne_zero hΘne
  have hOrientation' : 0 < Θ.det * Ψ.det := by
    change 0 < Θ.det * Ψ.det at hOrientation
    exact hOrientation
  have hdetProduct : 0 < Θ.det ^ 2 * Λ.det := by
    calc
      0 < Θ.det * Ψ.det := hOrientation'
      _ = Θ.det ^ 2 * Λ.det := by rw [hdetEq]; ring
  have hdetPos : 0 < Λ.det :=
    (mul_pos_iff_of_pos_left hΘsq).mp hdetProduct
  have hdetSq : Λ.det ^ 2 = 1 := by
    simpa only [pow_two] using isRoleLorentz_det_sq Λ hΛ
  have hfactor : (Λ.det - 1) * (Λ.det + 1) = 0 := by
    nlinarith [hdetSq]
  rcases mul_eq_zero.mp hfactor with hOne | hMinus
  · exact ⟨hΛ, by linarith⟩
  · have hdetEqMinus : Λ.det = -1 := by linarith
    rw [hdetEqMinus] at hdetPos
    exact False.elim (by linarith)

/-- Adding the relative orientation tag refines the full `O(1,3)` Gram
classification to its determinant-one subgroup. -/
theorem a4dRightProperLorentz_gram_complete
    (Θ Ψ : Matrix Role Role ℝ) (hΘ : IsUnit Θ.det) :
    (D0.Algebra.finiteGram roleLorentzMetric Θ =
        D0.Algebra.finiteGram roleLorentzMetric Ψ ∧
      a4dSameFrameOrientation Θ Ψ) ↔
      ∃ Λ : Matrix Role Role ℝ,
        IsProperRoleLorentz Λ ∧ Ψ = Θ * Λ := by
  constructor
  · rintro ⟨hgram, hOrientation⟩
    rcases (a4dRightLorentz_gram_complete Θ Ψ hΘ).mp hgram with
      ⟨Λ, hΛ, hΨ⟩
    exact ⟨Λ, a4dRightLorentz_sameOrientation_isProper
      Θ Ψ Λ hΘ hΛ hΨ hOrientation, hΨ⟩
  · rintro ⟨Λ, ⟨hΛ, hdetΛ⟩, hΨ⟩
    constructor
    · exact (a4dRightLorentz_gram_complete Θ Ψ hΘ).mpr
        ⟨Λ, hΛ, hΨ⟩
    · change 0 < Θ.det * Ψ.det
      have hdetΨ : Ψ.det = Θ.det := by
        rw [hΨ, Matrix.det_mul, hdetΛ]
        ring
      rw [hdetΨ]
      simpa only [pow_two] using
        sq_pos_of_ne_zero ((isUnit_iff_ne_zero).mp hΘ)

theorem a4dSiteGram_fullFrame_invariant
    (e : LocalCoframeField N)
    (Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (hΛ : ∀ x, IsRoleLorentz (Λ x))
    (x : ArchiveRolePhaseGroup N) :
    a4dSiteGram N (rawFullSolderFrameAction N e Λ) x =
      a4dSiteGram N e x := by
  rw [a4dSiteGram, a4dSiteGram, rawFullSolderFrameAction_matrix]
  exact rawSolderGram_frame_invariant (rawSolderMatrix N e x) (Λ x) (hΛ x)

def a4dDressedLink (Θx L Θy : Matrix Role Role ℝ) :
    Matrix Role Role ℝ :=
  Θx * L * Θy⁻¹

/-- A Lorentz link makes the solder-dressed transport an exact isometry
between the endpoint Gram forms. Only the target solder frame must be
invertible, since it is the frame inverted in `a4dDressedLink`. -/
theorem a4dDressedLink_metric_compatible
    (Θx L Θy : Matrix Role Role ℝ)
    (hL : IsRoleLorentz L) (hΘy : IsUnit Θy.det) :
    a4dDressedLink Θx L Θy *
        (Θy * roleLorentzMetric * Θy.transpose) *
        (a4dDressedLink Θx L Θy).transpose =
      Θx * roleLorentzMetric * Θx.transpose := by
  have hcancelLeft : Θy⁻¹ * Θy = (1 : Matrix Role Role ℝ) :=
    Matrix.nonsing_inv_mul Θy hΘy
  have hcancelRight : Θy.transpose * (Θy⁻¹).transpose =
      (1 : Matrix Role Role ℝ) := by
    rw [← Matrix.transpose_mul]
    rw [Matrix.nonsing_inv_mul Θy hΘy]
    simp
  unfold a4dDressedLink
  rw [Matrix.transpose_mul, Matrix.transpose_mul]
  calc
    (Θx * L * Θy⁻¹) * (Θy * roleLorentzMetric * Θy.transpose) *
        ((Θy⁻¹).transpose * (L.transpose * Θx.transpose)) =
      Θx * (L * (Θy⁻¹ * Θy) * roleLorentzMetric *
        (Θy.transpose * (Θy⁻¹).transpose) * L.transpose) * Θx.transpose := by
          noncomm_ring
    _ = Θx * (L * roleLorentzMetric * L.transpose) * Θx.transpose := by
          rw [hcancelLeft, hcancelRight]
          noncomm_ring
    _ = Θx * roleLorentzMetric * Θx.transpose := by
          exact congrArg (fun M : Matrix Role Role ℝ => Θx * M * Θx.transpose) hL

def a4dDressedLinkField (N : ℕ) (e : LocalCoframeField N)
    (L : A4DLinearLinkField N) (x : ArchiveRolePhaseGroup N) (r : Role) :
    Matrix Role Role ℝ :=
  a4dDressedLink (rawSolderMatrix N e x) (L x r)
    (rawSolderMatrix N e (roleTranslatePlus N r x))

/-- The exact finite endpoint metric-compatibility equation for a Lorentz
link. The sole nondegeneracy premise is at the transported-to site. -/
theorem a4dDressedLinkField_metric_compatible
    (e : LocalCoframeField N) (L : A4DLinearLinkField N)
    (hL : ∀ x r, IsRoleLorentz (L x r))
    (x : ArchiveRolePhaseGroup N) (r : Role)
    (hnd : IsUnit
      (rawSolderMatrix N e (roleTranslatePlus N r x)).det) :
    a4dDressedLinkField N e L x r *
        a4dSiteGram N e (roleTranslatePlus N r x) *
        (a4dDressedLinkField N e L x r).transpose =
      a4dSiteGram N e x := by
  simpa [a4dDressedLinkField, a4dSiteGram, D0.Algebra.finiteGram] using
    a4dDressedLink_metric_compatible
      (rawSolderMatrix N e x) (L x r)
      (rawSolderMatrix N e (roleTranslatePlus N r x)) (hL x r) hnd

theorem a4dDressedLink_frame_invariant
    (Θx L Θy Λx Λy : Matrix Role Role ℝ)
    (hΛx : IsRoleLorentz Λx) (hΛy : IsRoleLorentz Λy)
    (_hΘy : IsUnit Θy.det) :
    a4dDressedLink (Θx * Λx) (Λx⁻¹ * L * Λy) (Θy * Λy) =
      a4dDressedLink Θx L Θy := by
  have hx1 : Λx * Λx⁻¹ = (1 : Matrix Role Role ℝ) :=
    Matrix.mul_nonsing_inv Λx (isRoleLorentz_det_isUnit Λx hΛx)
  have hy1 : Λy * Λy⁻¹ = (1 : Matrix Role Role ℝ) :=
    Matrix.mul_nonsing_inv Λy (isRoleLorentz_det_isUnit Λy hΛy)
  unfold a4dDressedLink
  rw [Matrix.mul_inv_rev]
  calc
    (Θx * Λx) * (Λx⁻¹ * L * Λy) * (Λy⁻¹ * Θy⁻¹) =
        Θx * (Λx * Λx⁻¹) * L * (Λy * Λy⁻¹) * Θy⁻¹ := by
          simp only [Matrix.mul_assoc]
    _ = Θx * L * Θy⁻¹ := by rw [hx1, hy1]; simp

/-- With invertible solder frames at both endpoints, equality of dressed links
forces exactly the sitewise Lorentz transport of the undressed link. -/
theorem a4dDressedLink_eq_iff_rightAction
    (Θx Θy Λx Λy L L' : Matrix Role Role ℝ)
    (hΘx : IsUnit Θx.det) (hΘy : IsUnit Θy.det)
    (hΛx : IsRoleLorentz Λx) (hΛy : IsRoleLorentz Λy) :
    a4dDressedLink (Θx * Λx) L' (Θy * Λy) =
        a4dDressedLink Θx L Θy ↔
      L' = Λx⁻¹ * L * Λy := by
  constructor
  · intro h
    have hcancel : Λx * L' * Λy⁻¹ = L := by
      have h' := congrArg (fun M : Matrix Role Role ℝ => Θx⁻¹ * M * Θy) h
      rw [a4dDressedLink, a4dDressedLink, Matrix.mul_inv_rev] at h'
      change Θx⁻¹ * ((Θx * Λx) * L' * (Λy⁻¹ * Θy⁻¹)) * Θy =
          Θx⁻¹ * (Θx * L * Θy⁻¹) * Θy at h'
      have hleft : Θx⁻¹ * Θx = 1 := Matrix.nonsing_inv_mul Θx hΘx
      have hright : Θy⁻¹ * Θy = 1 := Matrix.nonsing_inv_mul Θy hΘy
      calc
        Λx * L' * Λy⁻¹ = 1 * (Λx * L' * Λy⁻¹) * 1 := by simp
        _ = (Θx⁻¹ * Θx) * (Λx * L' * Λy⁻¹) * (Θy⁻¹ * Θy) := by
              rw [hleft, hright]
        _ = Θx⁻¹ * ((Θx * Λx) * L' * (Λy⁻¹ * Θy⁻¹)) * Θy := by
              noncomm_ring
        _ = Θx⁻¹ * (Θx * L * Θy⁻¹) * Θy := h'
        _ = L := by
              calc
                Θx⁻¹ * (Θx * L * Θy⁻¹) * Θy =
                    (Θx⁻¹ * Θx) * L * (Θy⁻¹ * Θy) := by noncomm_ring
                _ = L := by rw [hleft, hright]; simp
    have hΛxUnit : IsUnit Λx.det := isRoleLorentz_det_isUnit Λx hΛx
    have hΛyUnit : IsUnit Λy.det := isRoleLorentz_det_isUnit Λy hΛy
    have hleft : Λx⁻¹ * Λx = 1 := Matrix.nonsing_inv_mul Λx hΛxUnit
    have hright : Λy⁻¹ * Λy = 1 := Matrix.nonsing_inv_mul Λy hΛyUnit
    have h' := congrArg (fun M : Matrix Role Role ℝ => Λx⁻¹ * M * Λy) hcancel
    calc
      L' = 1 * L' * 1 := by simp
      _ = (Λx⁻¹ * Λx) * L' * (Λy⁻¹ * Λy) := by rw [hleft, hright]
      _ = Λx⁻¹ * (Λx * L' * Λy⁻¹) * Λy := by noncomm_ring
      _ = Λx⁻¹ * L * Λy := h'
  · intro hL
    rw [hL]
    exact a4dDressedLink_frame_invariant Θx L Θy Λx Λy hΛx hΛy hΘy

/-- On the all-site nondegenerate sector, equality of every site Gram and
every solder-dressed link is equivalent to one site-dependent Lorentz frame
relating the complete coframe and link fields. This is the full `IsRoleLorentz`
orbit statement; fixed `SO⁺(1,3)` components require their discrete labels. -/
theorem a4d_complete_orbit_coordinates
    (e e' : LocalCoframeField N) (L L' : A4DLinearLinkField N)
    (hnd : ∀ x, IsUnit (rawSolderMatrix N e x).det) :
    ((∀ x, a4dSiteGram N e' x = a4dSiteGram N e x) ∧
      (∀ x r, a4dDressedLinkField N e' L' x r =
        a4dDressedLinkField N e L x r)) ↔
    ∃ Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ,
      (∀ x, IsRoleLorentz (Λ x)) ∧
      e' = rawFullSolderFrameAction N e Λ ∧
      L' = a4dFiniteLorentzLinkAction N L Λ := by
  constructor
  · rintro ⟨hgram, hlink⟩
    let Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ := fun x =>
      Classical.choose
        ((a4dRightLorentz_gram_complete (rawSolderMatrix N e x)
          (rawSolderMatrix N e' x) (hnd x)).mp (hgram x).symm)
    have hsite (x : ArchiveRolePhaseGroup N) :
        IsRoleLorentz (Λ x) ∧
          rawSolderMatrix N e' x = rawSolderMatrix N e x * Λ x := by
      dsimp [Λ]
      exact Classical.choose_spec
        ((a4dRightLorentz_gram_complete (rawSolderMatrix N e x)
          (rawSolderMatrix N e' x) (hnd x)).mp (hgram x).symm)
    have hcoframe : e' = rawFullSolderFrameAction N e Λ := by
      funext x r a
      have hmat : rawSolderMatrix N e' x =
          rawSolderMatrix N (rawFullSolderFrameAction N e Λ) x := by
        rw [rawFullSolderFrameAction_matrix]
        exact (hsite x).2
      have hentry := congrArg (fun M : Matrix Role Role ℝ => M r a) hmat
      simp only [rawSolderMatrix, rawFullSolderFrameAction] at hentry ⊢
      linarith
    have hlink' : ∀ x r, L' x r =
        (Λ x)⁻¹ * L x r * Λ (roleTranslatePlus N r x) := by
      intro x r
      let y := roleTranslatePlus N r x
      have hcoord :
          a4dDressedLink (rawSolderMatrix N e x * Λ x) (L' x r)
              (rawSolderMatrix N e y * Λ y) =
            a4dDressedLink (rawSolderMatrix N e x) (L x r)
              (rawSolderMatrix N e y) := by
        simpa [a4dDressedLinkField, y, (hsite x).2, (hsite y).2] using
          hlink x r
      exact (a4dDressedLink_eq_iff_rightAction
        (rawSolderMatrix N e x) (rawSolderMatrix N e y) (Λ x) (Λ y)
        (L x r) (L' x r) (hnd x) (hnd y) (hsite x).1 (hsite y).1).mp hcoord
    refine ⟨Λ, (fun x => (hsite x).1), hcoframe, ?_⟩
    funext x
    funext r
    simpa [a4dFiniteLorentzLinkAction] using hlink' x r
  · rintro ⟨Λ, hΛ, rfl, rfl⟩
    constructor
    · intro x
      exact a4dSiteGram_fullFrame_invariant e Λ hΛ x
    · intro x r
      let y := roleTranslatePlus N r x
      change a4dDressedLink
          (rawSolderMatrix N (rawFullSolderFrameAction N e Λ) x)
          (a4dFiniteLorentzLinkAction N L Λ x r)
          (rawSolderMatrix N (rawFullSolderFrameAction N e Λ) y) =
        a4dDressedLink (rawSolderMatrix N e x) (L x r)
          (rawSolderMatrix N e y)
      rw [rawFullSolderFrameAction_matrix, rawFullSolderFrameAction_matrix]
      simpa [a4dFiniteLorentzLinkAction] using
        (a4dDressedLink_frame_invariant
          (rawSolderMatrix N e x) (L x r) (rawSolderMatrix N e y)
          (Λ x) (Λ y) (hΛ x) (hΛ y) (hnd y))

/-- On the all-site nondegenerate sector, equality of every site Gram,
every dressed link, and the relative determinant-orientation tags is
equivalent to one site-dependent determinant-one Lorentz frame relating the
complete coframe and link fields. This selects the proper determinant
component but leaves time orientation unrestricted. -/
theorem a4d_complete_proper_orbit_coordinates
    (e e' : LocalCoframeField N) (L L' : A4DLinearLinkField N)
    (hnd : ∀ x, IsUnit (rawSolderMatrix N e x).det) :
    ((∀ x, a4dSiteGram N e' x = a4dSiteGram N e x) ∧
      (∀ x r, a4dDressedLinkField N e' L' x r =
        a4dDressedLinkField N e L x r) ∧
      (∀ x, a4dSameFrameOrientation (rawSolderMatrix N e x)
        (rawSolderMatrix N e' x))) ↔
    ∃ Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ,
      (∀ x, IsProperRoleLorentz (Λ x)) ∧
      e' = rawFullSolderFrameAction N e Λ ∧
      L' = a4dFiniteLorentzLinkAction N L Λ := by
  constructor
  · rintro ⟨hgram, hlink, hOrientation⟩
    rcases (a4d_complete_orbit_coordinates e e' L L' hnd).mp
        ⟨hgram, hlink⟩ with ⟨Λ, hLorentz, hcoframe, hlinks⟩
    have hproper (x : ArchiveRolePhaseGroup N) :
        IsProperRoleLorentz (Λ x) := by
      have hframe : rawSolderMatrix N e' x =
          rawSolderMatrix N e x * Λ x := by
        rw [hcoframe, rawFullSolderFrameAction_matrix]
      exact a4dRightLorentz_sameOrientation_isProper
        (rawSolderMatrix N e x) (rawSolderMatrix N e' x) (Λ x)
        (hnd x) (hLorentz x) hframe (hOrientation x)
    exact ⟨Λ, hproper, hcoframe, hlinks⟩
  · rintro ⟨Λ, hproper, rfl, rfl⟩
    have hcoordinates :=
      (a4d_complete_orbit_coordinates e
        (rawFullSolderFrameAction N e Λ) L
        (a4dFiniteLorentzLinkAction N L Λ) hnd).mpr
        ⟨Λ, (fun x => (hproper x).1), rfl, rfl⟩
    refine ⟨hcoordinates.1, hcoordinates.2, ?_⟩
    intro x
    have hdet :
        (rawSolderMatrix N (rawFullSolderFrameAction N e Λ) x).det =
          (rawSolderMatrix N e x).det := by
      rw [rawFullSolderFrameAction_matrix, Matrix.det_mul, (hproper x).2]
      simp
    change 0 < (rawSolderMatrix N e x).det *
      (rawSolderMatrix N (rawFullSolderFrameAction N e Λ) x).det
    rw [hdet]
    simpa only [pow_two] using
      sq_pos_of_ne_zero ((isUnit_iff_ne_zero).mp (hnd x))

theorem invertibleSolder_trivial_right_stabilizer
    (Θ Λ : Matrix Role Role ℝ) (hΘ : IsUnit Θ.det)
    (hfix : Θ * Λ = Θ) :
    Λ = 1 := by
  calc
    Λ = 1 * Λ := by simp
    _ = (Θ⁻¹ * Θ) * Λ := by rw [Matrix.nonsing_inv_mul Θ hΘ]
    _ = Θ⁻¹ * (Θ * Λ) := by simp only [Matrix.mul_assoc]
    _ = Θ⁻¹ * Θ := by rw [hfix]
    _ = 1 := Matrix.nonsing_inv_mul Θ hΘ

def a4dZeroSolderCoframe (N : ℕ) : LocalCoframeField N :=
  fun _ r a => -roleLorentzMetric r a

@[simp] theorem a4dZeroSolderCoframe_matrix
    (x : ArchiveRolePhaseGroup N) :
    rawSolderMatrix N (a4dZeroSolderCoframe N) x = 0 := by
  ext r a
  simp [rawSolderMatrix, a4dZeroSolderCoframe]

theorem rationalABBoost_ne_one :
    rationalABBoost ≠ (1 : Matrix Role Role ℝ) := by
  intro h
  have hab := congrArg (fun M : Matrix Role Role ℝ => M A B) h
  norm_num [rationalABBoost, Matrix.one_apply, A, B] at hab

theorem degenerateZeroSolder_flatLink_nontrivial_stabilizer :
    IsRoleLorentz rationalABBoost ∧
      rationalABBoost ≠ (1 : Matrix Role Role ℝ) ∧
      (0 : Matrix Role Role ℝ) * rationalABBoost = 0 ∧
      rationalABBoost⁻¹ * (1 : Matrix Role Role ℝ) * rationalABBoost = 1 := by
  refine ⟨rationalABBoost_lorentz, rationalABBoost_ne_one, by simp, ?_⟩
  -- Normalize the intermediate identity factor before applying the inverse lemma.
  simpa using Matrix.nonsing_inv_mul rationalABBoost
    (isRoleLorentz_det_isUnit rationalABBoost rationalABBoost_lorentz)

theorem a4dZeroSolder_constantBoost_stabilized
    (x : ArchiveRolePhaseGroup N) :
    rawSolderMatrix N
        (rawFullSolderFrameAction N (a4dZeroSolderCoframe N)
          (fun _ => rationalABBoost)) x = 0 := by
  rw [rawFullSolderFrameAction_matrix, a4dZeroSolderCoframe_matrix]
  simp

end
end D0.Geometry
