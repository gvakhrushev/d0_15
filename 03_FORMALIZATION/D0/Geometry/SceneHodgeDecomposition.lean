import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic
import D0.Geometry.SceneCochainComplex

/-!
# D0.Geometry.SceneHodgeDecomposition

Literal Euclidean cochain/Hodge identities for the scene `(p,q,r)=(8,10,12)`.
The incidence maps and exactness are the actual specialized generic
tripartite maps. No carrier-inventory constant is used as a proof of rank or
homology. Weighted metrics, spatial selectors, physical interpretations, TT
dynamics, and gravity couplings remain outside this worker.
-/

namespace D0.Geometry.SceneHodgeDecomposition

open BigOperators Matrix
open D0.Geometry.SceneCochainComplex
open D0.Topology.GenericTripartiteHomology

abbrev SceneC0 := D0.Geometry.SceneCochainComplex.SceneC0
abbrev SceneC1 := D0.Geometry.SceneCochainComplex.SceneC1
abbrev SceneC2 := D0.Geometry.SceneCochainComplex.SceneC2

def inner0 (u v : SceneC0) : ℚ := ∑ i, u i * v i
def inner1 (u v : SceneC1) : ℚ := ∑ i, u i * v i
def inner2 (u v : SceneC2) : ℚ := ∑ i, u i * v i

def delta0 (B : SceneC1) : SceneC0 := sceneBoundary1.mulVec B
def delta1 (F : SceneC2) : SceneC1 := sceneBoundary2.mulVec F

/-- `d₀ᵀ` is the Euclidean adjoint of `d₀`. -/
theorem adjoint_identity_01 (A : SceneC0) (B : SceneC1) :
    inner1 (d0 A) B = inner0 A (delta0 B) := by
  unfold inner1 inner0 d0 delta0
  have h_swap :
      (∑ e : SceneEdge, (∑ v : SceneVertex,
        sceneBoundary1.transpose e v * A v) * B e) =
        ∑ v : SceneVertex, A v * (∑ e : SceneEdge,
          sceneBoundary1 v e * B e) := by
    simp_rw [Finset.sum_mul]
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro v _
    calc
      (∑ e : SceneEdge, sceneBoundary1.transpose e v * A v * B e) =
          A v * (∑ e : SceneEdge, sceneBoundary1.transpose e v * B e) := by
            calc
              _ = ∑ e : SceneEdge, A v *
                  (sceneBoundary1.transpose e v * B e) := by
                    apply Finset.sum_congr rfl
                    intro e _
                    ring
              _ = _ := by rw [Finset.mul_sum]
      _ = A v * (∑ e : SceneEdge, sceneBoundary1 v e * B e) := by
            apply congrArg (fun z => A v * z)
            apply Finset.sum_congr rfl
            intro e _
            rfl
  exact h_swap

/-- `d₁ᵀ` is the Euclidean adjoint of `d₁`. -/
theorem adjoint_identity_12 (B : SceneC1) (F : SceneC2) :
    inner2 (d1 B) F = inner1 B (delta1 F) := by
  unfold inner2 inner1 d1 delta1
  have h_swap :
      (∑ f : SceneTriangle, (∑ e : SceneEdge,
        sceneBoundary2.transpose f e * B e) * F f) =
        ∑ e : SceneEdge, B e * (∑ f : SceneTriangle,
          sceneBoundary2 e f * F f) := by
    simp_rw [Finset.sum_mul]
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro e _
    calc
      (∑ f : SceneTriangle, sceneBoundary2.transpose f e * B e * F f) =
          B e * (∑ f : SceneTriangle, sceneBoundary2.transpose f e * F f) := by
            calc
              _ = ∑ f : SceneTriangle, B e *
                  (sceneBoundary2.transpose f e * F f) := by
                    apply Finset.sum_congr rfl
                    intro f _
                    ring
              _ = _ := by rw [Finset.mul_sum]
      _ = B e * (∑ f : SceneTriangle, sceneBoundary2 e f * F f) := by
            apply congrArg (fun z => B e * z)
            apply Finset.sum_congr rfl
            intro f _
            rfl
  exact h_swap

/-- Dual nilpotency `δ₀δ₁=0`, from the actual specialized incidence identity. -/
theorem codifferential_nilpotency (F : SceneC2) : delta0 (delta1 F) = 0 := by
  unfold delta0 delta1
  funext v
  change ∑ e : SceneEdge, sceneBoundary1 v e *
      (∑ f : SceneTriangle, sceneBoundary2 e f * F f) = 0
  simp_rw [Finset.mul_sum]
  rw [Finset.sum_comm]
  have hsum :
      (∑ y : SceneTriangle, ∑ x : SceneEdge,
        sceneBoundary1 v x * (sceneBoundary2 x y * F y)) =
        ∑ y : SceneTriangle,
          (∑ x : SceneEdge, sceneBoundary1 v x * sceneBoundary2 x y) * F y := by
    apply Finset.sum_congr rfl
    intro y _
    calc
      _ = ∑ x : SceneEdge, (sceneBoundary1 v x * sceneBoundary2 x y) * F y := by
        apply Finset.sum_congr rfl
        intro x _
        ring
      _ = _ := by rw [Finset.sum_mul]
  rw [hsum]
  apply Finset.sum_eq_zero
  intro f _
  have hzero :
      (∑ e : SceneEdge, sceneBoundary1 v e * sceneBoundary2 e f) = 0 := by
    have h := congrFun (congrFun
      (boundary_squared_zero (p := sceneP) (q := sceneQ) (r := sceneR)) v) f
    exact h
  rw [hzero, zero_mul]

/-- Exact and co-exact literal edge cochains are orthogonal. -/
theorem exact_coexact_orthogonal (A : SceneC0) (F : SceneC2) :
    inner1 (d0 A) (delta1 F) = 0 := by
  rw [adjoint_identity_01]
  have hzero := codifferential_nilpotency F
  unfold inner0 delta0 at *
  rw [hzero]
  simp

/-- Literal exactness of the middle cochain complex. -/
theorem scene_exactness :
    LinearMap.range sceneBoundary1.transpose.mulVecLin =
      LinearMap.ker sceneBoundary2.transpose.mulVecLin :=
  scene_cochain_exact

/-- Literal first homology vanishes, using the generic tripartite owner at the
required specialization. -/
theorem scene_first_homology_zero :
    Module.finrank ℚ
      (FirstHomology (p := sceneP) (q := sceneQ) (r := sceneR)) = 0 := by
  simpa [sceneP, sceneQ, sceneR] using
    (first_homology_finrank (p := sceneP) (q := sceneQ) (r := sceneR))

/-- Master owner for the literal scene cochain/Hodge identities: Euclidean
adjointness, exact/co-exact orthogonality, middle cochain exactness, and
vanishing first homology. -/
theorem scene_hodge_identities_owner :
    (∀ A : SceneC0, ∀ B : SceneC1, inner1 (d0 A) B = inner0 A (delta0 B)) ∧
    (∀ B : SceneC1, ∀ F : SceneC2, inner2 (d1 B) F = inner1 B (delta1 F)) ∧
    (∀ A : SceneC0, ∀ F : SceneC2, inner1 (d0 A) (delta1 F) = 0) ∧
    (LinearMap.range sceneBoundary1.transpose.mulVecLin =
      LinearMap.ker sceneBoundary2.transpose.mulVecLin) ∧
    (Module.finrank ℚ
      (FirstHomology (p := sceneP) (q := sceneQ) (r := sceneR)) = 0) := by
  exact ⟨fun A B => adjoint_identity_01 A B,
    fun B F => adjoint_identity_12 B F,
    fun A F => exact_coexact_orthogonal A F,
    scene_exactness,
    scene_first_homology_zero⟩

end D0.Geometry.SceneHodgeDecomposition
