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

def a4dOddCurvature (P : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    RoleSpace →ₗ[ℝ] RoleSpace :=
  (2 : ℝ)⁻¹ • (P.toLinearMap - P.symm.toLinearMap)

theorem a4dOddCurvature_conjugation
    (g P : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    a4dOddCurvature (g.symm.trans (P.trans g)) =
      g.symm.toLinearMap.comp
        ((a4dOddCurvature P).comp g.toLinearMap) := by
  ext v
  simp [a4dOddCurvature, LinearMap.sub_apply, LinearMap.comp_apply,
    LinearEquiv.trans_apply]

theorem a4dBasedOddCurvature_gauge
    (h : AffineNodeGauge N ℝ RoleSpace)
    (A : AffineCartanConnection N ℝ RoleSpace)
    (r s : Role) (x : ArchiveRolePhaseGroup N) :
    a4dOddCurvature
        (affineBasedHolonomy (affineGauge h A) r s x).lin =
      (h x).lin.symm.toLinearMap.comp
        ((a4dOddCurvature (affineBasedHolonomy A r s x).lin).comp
          (h x).lin.toLinearMap) := by
  rw [affineBasedHolonomy_gauge_lin]
  exact a4dOddCurvature_conjugation (h x).lin
    (affineBasedHolonomy A r s x).lin

theorem roleLorentzMetric_mul_transpose
    (Λ : Matrix Role Role ℝ) (hΛ : IsRoleLorentz Λ) :
    roleLorentzMetric * Λ.transpose = Λ⁻¹ * roleLorentzMetric := by
  have hu : IsUnit Λ.det := isRoleLorentz_det_isUnit Λ hΛ
  have hleft : Λ⁻¹ * Λ = (1 : Matrix Role Role ℝ) :=
    Matrix.nonsing_inv_mul Λ hu
  calc
    roleLorentzMetric * Λ.transpose =
        1 * (roleLorentzMetric * Λ.transpose) := by simp
    _ = (Λ⁻¹ * Λ) * (roleLorentzMetric * Λ.transpose) := by rw [hleft]
    _ = Λ⁻¹ * (Λ * roleLorentzMetric * Λ.transpose) := by
          simp only [Matrix.mul_assoc]
    _ = Λ⁻¹ * roleLorentzMetric := by rw [hΛ]

theorem matrixRow_mul_eq_transpose_mulVec
    (Θ Λ : Matrix Role Role ℝ) (r : Role) :
    (fun a => (Θ * Λ) r a) =
      Λ.transpose *ᵥ (fun a => Θ r a) := by
  funext a
  simp [Matrix.mul_apply, Matrix.mulVec, Matrix.transpose_apply, mul_comm]

theorem solderLegVector_fullFrame_covariant
    (e : LocalCoframeField N)
    (Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (hΛ : ∀ x, IsRoleLorentz (Λ x))
    (x : ArchiveRolePhaseGroup N) (r : Role) :
    solderLegVector N (rawFullSolderFrameAction N e Λ) x r =
      lorentzVectorEquiv (Λ x) (hΛ x) (solderLegVector N e x r) := by
  let row : RoleSpace := fun a => rawSolderMatrix N e x r a
  have hrow :
      (fun a => rawSolderMatrix N (rawFullSolderFrameAction N e Λ) x r a) =
        (Λ x).transpose *ᵥ row := by
    rw [rawFullSolderFrameAction_matrix]
    exact matrixRow_mul_eq_transpose_mulVec (rawSolderMatrix N e x) (Λ x) r
  have hmetric := roleLorentzMetric_mul_transpose (Λ x) (hΛ x)
  rw [solderLegVector, solderLegVector, hrow, lorentzVectorEquiv_apply]
  rw [← Matrix.mulVec_mulVec, hmetric, Matrix.mulVec_mulVec]

def a4dSolderBivector (N : ℕ) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) (r s : Role) :
    ⋀[ℝ]^2 RoleSpace :=
  exteriorPower.ιMulti ℝ ![solderLegVector N e x r, solderLegVector N e x s]

theorem a4dSolderBivector_fullFrame_covariant
    (e : LocalCoframeField N)
    (Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (hΛ : ∀ x, IsRoleLorentz (Λ x))
    (x : ArchiveRolePhaseGroup N) (r s : Role) :
    a4dSolderBivector N (rawFullSolderFrameAction N e Λ) x r s =
      exteriorPower.map 2 (lorentzVectorEquiv (Λ x) (hΛ x)).toLinearMap
        (a4dSolderBivector N e x r s) := by
  simp [a4dSolderBivector, exteriorPower.map_apply_ιMulti,
    solderLegVector_fullFrame_covariant e Λ hΛ x]

def a4dDegreeTwoLorentzPairing :
    LinearMap.BilinForm ℝ (⋀[ℝ]^2 RoleSpace) :=
  exteriorPairingFromBilin 2 roleLorentzMetric.toBilin'

theorem lorentzVectorEquiv_preserves_roleMetric
    (Λ : Matrix Role Role ℝ) (hΛ : IsRoleLorentz Λ) :
    (roleLorentzMetric.toBilin').comp
        (lorentzVectorEquiv Λ hΛ).toLinearMap
        (lorentzVectorEquiv Λ hΛ).toLinearMap =
      roleLorentzMetric.toBilin' := by
  have happ :
      (lorentzVectorEquiv Λ hΛ).toLinearMap = Matrix.toLin' Λ⁻¹ := by
    apply LinearMap.ext
    intro v
    simpa [Matrix.toLin'_apply] using lorentzVectorEquiv_apply Λ hΛ v
  rw [happ, Matrix.toBilin'_comp, lorentz_inv_transpose_metric Λ hΛ]

theorem a4dDegreeTwoLorentzPairing_invariant
    (Λ : Matrix Role Role ℝ) (hΛ : IsRoleLorentz Λ)
    (z w : ⋀[ℝ]^2 RoleSpace) :
    a4dDegreeTwoLorentzPairing
        (exteriorPower.map 2 (lorentzVectorEquiv Λ hΛ).toLinearMap z)
        (exteriorPower.map 2 (lorentzVectorEquiv Λ hΛ).toLinearMap w) =
      a4dDegreeTwoLorentzPairing z w := by
  change
    ((exteriorPairingFromBilin 2 roleLorentzMetric.toBilin').comp
      (exteriorPower.map 2 (lorentzVectorEquiv Λ hΛ).toLinearMap)
      (exteriorPower.map 2 (lorentzVectorEquiv Λ hΛ).toLinearMap)) z w =
      exteriorPairingFromBilin 2 roleLorentzMetric.toBilin' z w
  rw [exteriorPairingFromBilin_natural,
    lorentzVectorEquiv_preserves_roleMetric Λ hΛ]

def A4DStarLorentzCompatible
    (star : (⋀[ℝ]^2 RoleSpace) →ₗ[ℝ] (⋀[ℝ]^2 RoleSpace))
    (Λ : Matrix Role Role ℝ) (hΛ : IsRoleLorentz Λ) : Prop :=
  ∀ z,
    star (exteriorPower.map 2 (lorentzVectorEquiv Λ hΛ).toLinearMap z) =
      exteriorPower.map 2 (lorentzVectorEquiv Λ hΛ).toLinearMap (star z)

theorem a4dStarCell_invariant
    (star : (⋀[ℝ]^2 RoleSpace) →ₗ[ℝ] (⋀[ℝ]^2 RoleSpace))
    (Λ : Matrix Role Role ℝ) (hΛ : IsRoleLorentz Λ)
    (hstar : A4DStarLorentzCompatible star Λ hΛ)
    (B C : ⋀[ℝ]^2 RoleSpace) :
    a4dDegreeTwoLorentzPairing
      (exteriorPower.map 2 (lorentzVectorEquiv Λ hΛ).toLinearMap B)
      (star (exteriorPower.map 2 (lorentzVectorEquiv Λ hΛ).toLinearMap C)) =
    a4dDegreeTwoLorentzPairing B (star C) := by
  rw [hstar C]
  exact a4dDegreeTwoLorentzPairing_invariant Λ hΛ B (star C)

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
  rw [Matrix.nonsing_inv_mul rationalABBoost
    (isRoleLorentz_det_isUnit rationalABBoost rationalABBoost_lorentz)]
  simp

theorem a4dZeroSolder_constantBoost_stabilized
    (x : ArchiveRolePhaseGroup N) :
    rawSolderMatrix N
        (rawFullSolderFrameAction N (a4dZeroSolderCoframe N)
          (fun _ => rationalABBoost)) x = 0 := by
  rw [rawFullSolderFrameAction_matrix, a4dZeroSolderCoframe_matrix]
  simp

end
end D0.Geometry
