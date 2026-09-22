import Mathlib.LinearAlgebra.Matrix.BilinearForm
import D0.Bridge.T4LocalRoleFrame

namespace D0.Bridge

open D0
open D0.Geometry
open Manifold
open scoped ContDiff Manifold

noncomputable section

def roleBilin (T : SymRoleTensor) : LinearMap.BilinForm ℝ RoleVec :=
  Matrix.toBilin' T.toMatrix

theorem roleBilin_apply (T : SymRoleTensor) (u v : RoleVec) :
    roleBilin T u v = ∑ a, ∑ b, u a * T.toMatrix a b * v b := by
  exact Matrix.toBilin'_apply T.toMatrix u v

theorem roleBilin_symmetric (T : SymRoleTensor) (u v : RoleVec) :
    roleBilin T u v = roleBilin T v u := by
  classical
  rw [roleBilin_apply, roleBilin_apply]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr rfl
  intro b hb
  rw [T.symmetric]
  ring

def reconstructResponseFromFrame {x : T4} (frame : RoleVec ≃L[ℝ] T4Tangent x)
    (T : SymRoleTensor) : SymCov2At x where
  toBilin := (roleBilin T).comp frame.symm.toLinearMap frame.symm.toLinearMap
  symmetric := by
    intro v w
    rw [LinearMap.BilinForm.comp_apply, LinearMap.BilinForm.comp_apply]
    exact roleBilin_symmetric T (frame.symm v) (frame.symm w)

def reconstructResponse (F : T4LocalRoleFrame x) (T : SymRoleTensor) : SymCov2At x :=
  reconstructResponseFromFrame (centerFrame F) T

theorem reconstructResponse_apply {x : T4} (F : T4LocalRoleFrame x)
    (T : SymRoleTensor) (v w : T4Tangent x) :
    (reconstructResponse F T).toBilin v w =
      roleBilin T ((centerFrame F).symm v) ((centerFrame F).symm w) := by
  rfl

theorem reconstructResponse_literal_sum {x : T4} (F : T4LocalRoleFrame x)
    (T : SymRoleTensor) (v w : T4Tangent x) :
    (reconstructResponse F T).toBilin v w =
      ∑ a, ∑ b, T.toMatrix a b * ((centerFrame F).symm v) a *
        ((centerFrame F).symm w) b := by
  rw [reconstructResponse_apply, roleBilin_apply]
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr rfl
  intro b hb
  ring

abbrev RadiusTwoStencil := RadiusTwoOffset → SymRoleTensor

def sampleMetric (N : ℕ) (F : T4LocalRoleFrame x) (g : SmoothLorentzMetric)
    (hF : StencilAdmissible N F) : RadiusTwoStencil :=
  fun z =>
    { toMatrix := fun a b =>
          metricBilin g (F.chart (stencilModelPoint N F z))
          (stencilFrame N F z (hF z) (Pi.single a 1))
          (stencilFrame N F z (hF z) (Pi.single b 1))
      symmetric := by
        intro a b
        exact metricBilin_symmetric g _ _ _ }

theorem sampleMetric_entry (N : ℕ) (F : T4LocalRoleFrame x)
    (g : SmoothLorentzMetric) (hF : StencilAdmissible N F)
    (z : RadiusTwoOffset) (a b : Role) :
    (sampleMetric N F g hF z).toMatrix a b =
      metricBilin g (F.chart (stencilModelPoint N F z))
        (stencilFrame N F z (hF z) (Pi.single a 1))
        (stencilFrame N F z (hF z) (Pi.single b 1)) := by
  rfl

def pullbackSymCov2 {x : T4} (φ : PartialDiffeomorph T4I T4I T4 T4 ω)
    (hx : x ∈ φ.source) (A : SymCov2At (φ x)) : SymCov2At x := by
  let dφ := IsLocalDiffeomorphAt.mfderivToContinuousLinearEquiv
    (PartialDiffeomorph.isLocalDiffeomorphAt T4I T4I ω φ hx) (by norm_num)
  exact
    { toBilin := A.toBilin.comp dφ.toLinearMap dφ.toLinearMap
      symmetric := by
        intro v w
        rw [LinearMap.BilinForm.comp_apply, LinearMap.BilinForm.comp_apply]
        exact A.symmetric _ _ }

theorem pullbackSymCov2_apply {x : T4} (φ : PartialDiffeomorph T4I T4I T4 T4 ω)
    (hx : x ∈ φ.source) (A : SymCov2At (φ x)) (v w : T4Tangent x) :
    (pullbackSymCov2 φ hx A).toBilin v w =
      A.toBilin
        (IsLocalDiffeomorphAt.mfderivToContinuousLinearEquiv
          (PartialDiffeomorph.isLocalDiffeomorphAt T4I T4I ω φ hx) (by norm_num) v)
        (IsLocalDiffeomorphAt.mfderivToContinuousLinearEquiv
          (PartialDiffeomorph.isLocalDiffeomorphAt T4I T4I ω φ hx) (by norm_num) w) := by
  rfl

def pulledCenterFrame {x : T4} (φ : PartialDiffeomorph T4I T4I T4 T4 ω)
    (hx : x ∈ φ.source) (frame : RoleVec ≃L[ℝ] T4Tangent (φ x)) :
    RoleVec ≃L[ℝ] T4Tangent x :=
  let dφ := IsLocalDiffeomorphAt.mfderivToContinuousLinearEquiv
    (PartialDiffeomorph.isLocalDiffeomorphAt T4I T4I ω φ hx) (by norm_num)
  frame.trans dφ.symm

theorem centerFrame_pullback {x : T4} (φ : PartialDiffeomorph T4I T4I T4 T4 ω)
    (hx : x ∈ φ.source) (frame : RoleVec ≃L[ℝ] T4Tangent (φ x)) :
    (pulledCenterFrame φ hx frame).symm =
      (IsLocalDiffeomorphAt.mfderivToContinuousLinearEquiv
        (PartialDiffeomorph.isLocalDiffeomorphAt T4I T4I ω φ hx) (by norm_num)).trans
        frame.symm := by
  rfl

theorem reconstructResponse_pullback {x : T4}
    (φ : PartialDiffeomorph T4I T4I T4 T4 ω) (hx : x ∈ φ.source)
    (frame : RoleVec ≃L[ℝ] T4Tangent (φ x)) (T : SymRoleTensor) :
    pullbackSymCov2 φ hx (reconstructResponseFromFrame frame T) =
      reconstructResponseFromFrame (pulledCenterFrame φ hx frame) T := by
  apply SymCov2At.ext
  ext v w
  simp [pullbackSymCov2, reconstructResponseFromFrame, pulledCenterFrame,
    LinearMap.BilinForm.comp_apply]

end
end D0.Bridge
