import Mathlib.Geometry.Manifold.LocalDiffeomorph
import D0.Bridge.T4TypedGeometry
import D0.Geometry.ArchiveRolePhaseGroup

namespace D0.Bridge

open D0
open D0.Geometry
open Manifold
open scoped ContDiff Manifold

noncomputable section

/-- The four role coordinates in the order `A, B, C, D`. -/
def roleFin : Role ≃ Fin 4 where
  toFun r :=
    if r = A then 0 else if r = B then 1 else if r = C then 2 else 3
  invFun i :=
    if i = 0 then A else if i = 1 then B else if i = 2 then C else D
  left_inv := by
    intro r
    rcases r with ⟨r₁, r₂⟩
    fin_cases r₁ <;> fin_cases r₂ <;> simp [A, B, C, D]
  right_inv := by
    intro i
    fin_cases i <;> rfl

abbrev RoleVec := Role → ℝ

/-- Re-index a role vector by the explicit `A,B,C,D` correspondence. -/
def roleVecToFin : RoleVec ≃L[ℝ] (Fin 4 → ℝ) :=
  (ContinuousLinearEquiv.piCongrLeft ℝ (fun _ : Role => ℝ) roleFin.symm).symm

/-- The canonical continuous-linear identification of four Euclidean coordinates with `T4E`. -/
def finFourToT4E : EuclideanSpace ℝ (Fin 4) ≃L[ℝ] T4E :=
  (EuclideanSpace.finAddEquivProd (𝕜 := ℝ) (n := 2) (m := 2)).trans
    (ContinuousLinearEquiv.prodCongr
      (EuclideanSpace.finAddEquivProd (𝕜 := ℝ) (n := 1) (m := 1))
      (EuclideanSpace.finAddEquivProd (𝕜 := ℝ) (n := 1) (m := 1)))

def roleVecToModel : RoleVec ≃L[ℝ] T4E :=
  (roleVecToFin.trans (EuclideanSpace.equiv (Fin 4) ℝ).symm).trans finFourToT4E

/-- An actual local model chart together with its center and role-labelled model frame. -/
structure T4LocalRoleFrame (x : T4) where
  chart : PartialDiffeomorph T4I T4I T4E T4 ω
  center : T4E
  center_mem : center ∈ chart.source
  chart_center : chart center = x
  roleToModel : RoleVec ≃L[ℝ] T4E

def canonicalRoleFrame (x : T4) (chart : PartialDiffeomorph T4I T4I T4E T4 ω)
    (center : T4E) (center_mem : center ∈ chart.source) (chart_center : chart center = x) :
    T4LocalRoleFrame x :=
  { chart := chart
    center := center
    center_mem := center_mem
    chart_center := chart_center
    roleToModel := roleVecToModel }

def localFrameAt (F : T4LocalRoleFrame x) (z : T4E) (hz : z ∈ F.chart.source) :
    RoleVec ≃L[ℝ] T4Tangent (F.chart z) :=
  F.roleToModel.trans
    (IsLocalDiffeomorphAt.mfderivToContinuousLinearEquiv
      (PartialDiffeomorph.isLocalDiffeomorphAt T4I T4I ω F.chart hz) (by norm_num))

def centerFrame (F : T4LocalRoleFrame x) : RoleVec ≃L[ℝ] T4Tangent x :=
  F.chart_center ▸ localFrameAt F F.center F.center_mem

abbrev RadiusTwoOffset := Role → Fin 5

def radiusTwoOffsetValue (k : Fin 5) : ℤ := (k : ℤ) - 2

def mesh (N : ℕ) : ℝ := 1 / ((N + 2 : ℕ) : ℝ)

theorem mesh_eq (N : ℕ) : mesh N = 1 / ((N + 2 : ℕ) : ℝ) := rfl

/-- Radius-two offsets are embedded in the archive phase group by their five-site index. -/
def radiusTwoPhase (N : ℕ) (z : RadiusTwoOffset) : ArchiveRolePhaseGroup N :=
  fun r => (radiusTwoOffsetValue (z r) : ZMod (archiveFibers N))

theorem radiusTwoPhase_injective (N : ℕ) (hN : 3 ≤ N) :
    Function.Injective (radiusTwoPhase N) := by
  intro z w h
  funext r
  have hr : (z r : ℕ) < archiveFibers N := by
    dsimp [archiveFibers]
    omega
  have hs : (w r : ℕ) < archiveFibers N := by
    dsimp [archiveFibers]
    omega
  have hcast : ((z r : ℕ) : ZMod (archiveFibers N)) =
      ((w r : ℕ) : ZMod (archiveFibers N)) := by
    apply sub_right_injective (b := (2 : ZMod (archiveFibers N)))
    simpa [radiusTwoPhase, radiusTwoOffsetValue] using congrFun h r
  have hv := congrArg ZMod.val hcast
  apply Fin.ext
  simpa [radiusTwoPhase, ZMod.val_natCast_of_lt hr, ZMod.val_natCast_of_lt hs] using hv

def stencilModelPoint (N : ℕ) (F : T4LocalRoleFrame x) (z : RadiusTwoOffset) : T4E :=
  F.center + F.roleToModel (fun r => mesh N * (radiusTwoOffsetValue (z r) : ℝ))

def StencilAdmissible (N : ℕ) (F : T4LocalRoleFrame x) : Prop :=
  ∀ z : RadiusTwoOffset, stencilModelPoint N F z ∈ F.chart.source

def stencilFrame (N : ℕ) (F : T4LocalRoleFrame x) (z : RadiusTwoOffset)
    (hz : stencilModelPoint N F z ∈ F.chart.source) :
    RoleVec ≃L[ℝ] T4Tangent (F.chart (stencilModelPoint N F z)) :=
  localFrameAt F (stencilModelPoint N F z) hz

end
end D0.Bridge
