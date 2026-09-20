import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic
import D0.Topology.GenericTripartiteHomology

/-!
# D0.Geometry.SceneCochainComplex

Literal rational cochain complex for the complete-tripartite scene with
`(p,q,r) = (8,10,12)`, hence zone sizes `(9,11,13)`.

The chain maps are not dimensions declared by a carrier inventory: they are the
actual generic tripartite incidence matrices specialized at `(8,10,12)` and
transposed to cochains.  The module proves cochain nilpotency and the exact
middle-degree statement needed for `H¹ = 0` from the generic rank owners.

No physical Hamiltonian, TT dynamics, matter-gravity identification, Hodge
spatial selector, or weighted metric is introduced here.
-/

namespace D0.Geometry.SceneCochainComplex

open BigOperators Matrix
open D0.Topology.GenericTripartiteHomology

abbrev sceneP : ℕ := 8
abbrev sceneQ : ℕ := 10
abbrev sceneR : ℕ := 12

abbrev SceneVertex := GenericVertex sceneP sceneQ sceneR
abbrev SceneEdge := GenericEdge sceneP sceneQ sceneR
abbrev SceneTriangle := GenericTriangle sceneP sceneQ sceneR

abbrev SceneC0 : Type := SceneVertex → ℚ
abbrev SceneC1 : Type := SceneEdge → ℚ
abbrev SceneC2 : Type := SceneTriangle → ℚ

/-- Actual vertex-edge incidence matrix, specialized from the generic owner. -/
def sceneBoundary1 : Matrix SceneVertex SceneEdge ℚ :=
  boundary1 (p := sceneP) (q := sceneQ) (r := sceneR)

/-- Actual edge-triangle incidence matrix, specialized from the generic owner. -/
def sceneBoundary2 : Matrix SceneEdge SceneTriangle ℚ :=
  boundary2 (p := sceneP) (q := sceneQ) (r := sceneR)

/-- Literal cochain differential `d₀ = ∂₁ᵀ`. -/
def d0 (A : SceneC0) : SceneC1 :=
  sceneBoundary1.transpose.mulVec A

/-- Literal cochain differential `d₁ = ∂₂ᵀ`. -/
def d1 (B : SceneC1) : SceneC2 :=
  sceneBoundary2.transpose.mulVec B

/-- The actual specialized carrier cardinalities are derived from the generic
finite tripartite types, not imported as physical inventory constants. -/
theorem scene_carrier_cardinalities :
    Fintype.card SceneVertex = 33 ∧
    Fintype.card SceneEdge = 359 ∧
    Fintype.card SceneTriangle = 1287 := by
  simpa [sceneP, sceneQ, sceneR, vertexBoundaryRank, cycleRank] using
    (generic_face_cardinalities (p := sceneP) (q := sceneQ) (r := sceneR))

/-- The literal incidence maps satisfy `d₁ d₀ = 0`. -/
theorem scene_d1_d0_zero :
    ∀ A : SceneC0, d1 (d0 A) = 0 := by
  intro A
  funext f
  unfold d1 d0
  rw [Matrix.mulVec_mulVec]
  rw [← Matrix.transpose_mul]
  change ((sceneBoundary1 * sceneBoundary2)ᵀ *ᵥ A) f = 0
  rw [show sceneBoundary1 * sceneBoundary2 =
      boundary1 (p := sceneP) (q := sceneQ) (r := sceneR) *
        boundary2 (p := sceneP) (q := sceneQ) (r := sceneR) by rfl]
  rw [boundary_squared_zero (p := sceneP) (q := sceneQ) (r := sceneR)]
  simp

/-- The generic rank owners specialize to the literal scene ranks. -/
theorem scene_boundary_ranks :
    sceneBoundary1.rank = 32 ∧ sceneBoundary2.rank = 327 := by
  constructor
  · simpa [sceneBoundary1, sceneP, sceneQ, sceneR, vertexBoundaryRank] using
      (boundary1_rank (p := sceneP) (q := sceneQ) (r := sceneR))
  · simpa [sceneBoundary2, sceneP, sceneQ, sceneR, cycleRank] using
      (boundary2_rank (p := sceneP) (q := sceneQ) (r := sceneR))

/-- The cochain ranges have the actual ranks `32` and `327`. -/
theorem scene_cochain_range_ranks :
    Module.finrank ℚ (LinearMap.range sceneBoundary1.transpose.mulVecLin) = 32 ∧
    Module.finrank ℚ (LinearMap.range sceneBoundary2.mulVecLin) = 327 := by
  constructor
  · simpa [Matrix.rank] using congrArg id
      (show sceneBoundary1.transpose.rank = 32 by
        rw [Matrix.rank_transpose]
        exact scene_boundary_ranks.1)
  · simpa [Matrix.rank] using congrArg id
      (show sceneBoundary2.rank = 327 by
        exact scene_boundary_ranks.2)

/-- Every cochain 1-cycle is exact.  This is the literal `H¹ = 0` statement:
`range d₀ = ker d₁`, proved by nilpotency and the actual specialized ranks. -/
theorem scene_cochain_exact :
    LinearMap.range sceneBoundary1.transpose.mulVecLin =
      LinearMap.ker sceneBoundary2.transpose.mulVecLin := by
  have hle :
      LinearMap.range sceneBoundary1.transpose.mulVecLin ≤
        LinearMap.ker sceneBoundary2.transpose.mulVecLin := by
    rw [LinearMap.range_le_ker_iff]
    rw [← Matrix.mulVecLin_mul, ← Matrix.transpose_mul]
    change (sceneBoundary1 * sceneBoundary2)ᵀ.mulVecLin = 0
    rw [show sceneBoundary1 * sceneBoundary2 =
        boundary1 (p := sceneP) (q := sceneQ) (r := sceneR) *
          boundary2 (p := sceneP) (q := sceneQ) (r := sceneR) by rfl]
    rw [boundary_squared_zero (p := sceneP) (q := sceneQ) (r := sceneR)]
    exact Matrix.mulVecLin_zero
  have h0 := scene_cochain_range_ranks
  have h2t : sceneBoundary2.transpose.rank = 327 := by
    rw [Matrix.rank_transpose]
    exact scene_boundary_ranks.2
  have hker := LinearMap.finrank_range_add_finrank_ker
    sceneBoundary2.transpose.mulVecLin
  have hdom : Module.finrank ℚ (SceneEdge → ℚ) = 359 := by
    rw [Module.finrank_fintype_fun_eq_card]
    exact scene_carrier_cardinalities.2.1
  have hkerdim :
      Module.finrank ℚ (LinearMap.ker sceneBoundary2.transpose.mulVecLin) = 32 := by
    have hker' := hker
    rw [show Module.finrank ℚ
        (LinearMap.range sceneBoundary2.transpose.mulVecLin) = 327 by
          simpa [Matrix.rank] using h2t, hdom] at hker'
    omega
  exact Submodule.eq_of_le_of_finrank_le hle (by
    rw [h0.1, hkerdim])

end D0.Geometry.SceneCochainComplex
