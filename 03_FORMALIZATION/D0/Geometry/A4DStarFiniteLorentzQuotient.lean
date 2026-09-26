import Mathlib.Tactic
import Mathlib.LinearAlgebra.ExteriorPower.Basic
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
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
  rawSolderMatrix N e x * roleLorentzMetric * (rawSolderMatrix N e x).transpose

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
