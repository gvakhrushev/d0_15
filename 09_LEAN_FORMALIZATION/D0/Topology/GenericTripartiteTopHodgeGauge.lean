import D0.Topology.GenericTripartiteTopHodgeGreen
import Mathlib.Tactic

/-!
# D0-GENERIC-TRIPARTITE-TOP-HODGE-GAUGE-001

For every rational 1-cycle `z`, the complete Hodge spectral calculus selects
the canonical filling

```
u = G ∂₂ᵀ z,
```

where `G` is the upper-Hodge Green operator.  This filling satisfies

```
∂₂ u = z,
P_harm u = 0,
```

and is the unique filling with vanishing harmonic projection.

Scope: this is a finite rational Hodge gauge.  It is not a physical gauge
field, propagator prescription, or arbitrary-ring construction.
-/

namespace D0.Topology.GenericTripartiteTopHodgeGauge
open Matrix
open D0.Topology.GenericTripartiteHomology
open D0.Topology.GenericTripartiteTopHomologyRing
open D0.Topology.GenericTripartiteFirstHomologyRing
open D0.Topology.GenericTripartiteTopHodgeSpectrum
open D0.Topology.GenericTripartiteTopHodgeGreen

variable {p q r : ℕ}
local notation "Edge" => GenericEdge p q r
local notation "Triangle" => GenericTriangle p q r

/-- Transpose boundary from edge chains to triangle chains. -/
def boundary2Transpose : (Edge → ℚ) →ₗ[ℚ] (Triangle → ℚ) :=
  (boundary2R ℚ (p:=p) (q:=q) (r:=r)).transpose.mulVecLin

/-- Canonical Hodge-gauge filling of a 1-cycle. -/
noncomputable def hodgeGaugeFilling :
    OneCycle ℚ (p:=p) (q:=q) (r:=r) →ₗ[ℚ] (Triangle → ℚ) :=
  (topHodgeGreen (p:=p) (q:=q) (r:=r)).comp
    ((boundary2Transpose (p:=p) (q:=q) (r:=r)).comp
      (LinearMap.ker
        (boundary1R ℚ (p:=p) (q:=q) (r:=r)).mulVecLin).subtype)

/-- The harmonic projector lands in `ker d2`. -/
theorem boundary2_harmonicProjector_zero (x : Triangle → ℚ) :
    (boundary2R ℚ (p:=p) (q:=q) (r:=r)).mulVec
      (topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r) x) = 0 := by
  have hDelta := congrArg
    (fun f => f x)
    (topHodge_comp_harmonicProjector (p:=p) (q:=q) (r:=r))
  simp only [LinearMap.comp_apply, LinearMap.zero_apply] at hDelta
  have hmem :
      topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r) x ∈
        LinearMap.ker
          (topHodgeLaplacian (p:=p) (q:=q) (r:=r)).mulVecLin := by
    rw [LinearMap.mem_ker]
    exact hDelta
  rw [topHodge_kernel_eq_topKernel] at hmem
  rw [LinearMap.mem_ker, Matrix.mulVecLin_apply] at hmem
  exact hmem

private lemma transpose_boundary_of_filling
    (z : OneCycle ℚ (p:=p) (q:=q) (r:=r)) :
    (boundary2Transpose (p:=p) (q:=q) (r:=r)) z =
      topHodgeEnd (p:=p) (q:=q) (r:=r)
        (oneCycleFilling ℚ z) := by
  unfold boundary2Transpose topHodgeEnd topHodgeLaplacian
  change
    (boundary2R ℚ (p:=p) (q:=q) (r:=r)).transpose.mulVec z =
      ((boundary2R ℚ (p:=p) (q:=q) (r:=r)).transpose *
        boundary2R ℚ (p:=p) (q:=q) (r:=r)).mulVec
          (oneCycleFilling ℚ z)
  rw [← Matrix.mulVec_mulVec]
  rw [boundary2R_oneCycleFilling]

/-- The Hodge-gauge filling solves `d2 u = z`. -/
theorem boundary2_hodgeGaugeFilling
    (z : OneCycle ℚ (p:=p) (q:=q) (r:=r)) :
    (boundary2R ℚ (p:=p) (q:=q) (r:=r)).mulVec
      (hodgeGaugeFilling (p:=p) (q:=q) (r:=r) z) = z := by
  unfold hodgeGaugeFilling
  simp only [LinearMap.comp_apply]
  have hTranspose :=
    transpose_boundary_of_filling (p:=p) (q:=q) (r:=r) z
  change
    (boundary2R ℚ (p:=p) (q:=q) (r:=r)).mulVec
      (topHodgeGreen
        ((boundary2Transpose (p:=p) (q:=q) (r:=r))
          ((LinearMap.ker
            (boundary1R ℚ (p:=p) (q:=q) (r:=r)).mulVecLin).subtype z))) =
        (z : Edge → ℚ)
  change
    (boundary2Transpose (p:=p) (q:=q) (r:=r))
        ((LinearMap.ker
          (boundary1R ℚ (p:=p) (q:=q) (r:=r)).mulVecLin).subtype z) =
      topHodgeEnd (p:=p) (q:=q) (r:=r)
        (oneCycleFilling ℚ z) at hTranspose
  rw [hTranspose]
  have hGreen := congrArg
    (fun f => f (oneCycleFilling ℚ z))
    (green_comp_topHodge (p:=p) (q:=q) (r:=r))
  simp only [LinearMap.comp_apply, LinearMap.sub_apply, LinearMap.id_apply] at hGreen
  rw [hGreen, Matrix.mulVec_sub, boundary2R_oneCycleFilling,
    boundary2_harmonicProjector_zero, sub_zero]

/-- The canonical filling is orthogonal to the harmonic tensor sectors. -/
theorem hodgeGaugeFilling_gauge
    (z : OneCycle ℚ (p:=p) (q:=q) (r:=r)) :
    topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r)
      (hodgeGaugeFilling (p:=p) (q:=q) (r:=r) z) = 0 := by
  unfold hodgeGaugeFilling
  simp only [LinearMap.comp_apply]
  have h := congrArg
    (fun f => f ((boundary2Transpose (p:=p) (q:=q) (r:=r)) z))
    (harmonicProjector_comp_green (p:=p) (q:=q) (r:=r))
  simpa [LinearMap.comp_apply] using h

/-- Uniqueness of the filling in Hodge gauge. -/
theorem hodgeGaugeFilling_unique
    (z : OneCycle ℚ (p:=p) (q:=q) (r:=r))
    (x : Triangle → ℚ)
    (hFill :
      (boundary2R ℚ (p:=p) (q:=q) (r:=r)).mulVec x = z)
    (hGauge :
      topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r) x = 0) :
    x = hodgeGaugeFilling (p:=p) (q:=q) (r:=r) z := by
  let u := hodgeGaugeFilling (p:=p) (q:=q) (r:=r) z
  have hDiffBoundary :
      (boundary2R ℚ (p:=p) (q:=q) (r:=r)).mulVec (x-u) = 0 := by
    rw [Matrix.mulVec_sub, hFill, boundary2_hodgeGaugeFilling, sub_self]
  have hDiffHodge :
      topHodgeEnd (p:=p) (q:=q) (r:=r) (x-u) = 0 := by
    unfold topHodgeEnd topHodgeLaplacian
    change
      ((boundary2R ℚ (p:=p) (q:=q) (r:=r)).transpose *
        boundary2R ℚ (p:=p) (q:=q) (r:=r)).mulVec (x-u) = 0
    rw [← Matrix.mulVec_mulVec, hDiffBoundary, Matrix.mulVec_zero]
  have hDiffGauge :
      topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r) (x-u) = 0 := by
    rw [map_sub, hGauge, hodgeGaugeFilling_gauge, sub_self]
  have hGreen := congrArg
    (fun f => f (x-u))
    (green_comp_topHodge (p:=p) (q:=q) (r:=r))
  simp only [LinearMap.comp_apply, LinearMap.sub_apply, LinearMap.id_apply] at hGreen
  rw [hDiffHodge, map_zero, hDiffGauge, sub_zero] at hGreen
  have hxu : x-u = 0 := hGreen.symm
  exact sub_eq_zero.mp hxu

/-- Canonical filling passport. -/
structure HodgeGaugeFillingPassport (p q r : ℕ) where
  fills : ∀ z : OneCycle ℚ (p:=p) (q:=q) (r:=r),
    (boundary2R ℚ (p:=p) (q:=q) (r:=r)).mulVec
      (hodgeGaugeFilling (p:=p) (q:=q) (r:=r) z) = z
  gauge : ∀ z : OneCycle ℚ (p:=p) (q:=q) (r:=r),
    topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r)
      (hodgeGaugeFilling (p:=p) (q:=q) (r:=r) z) = 0
  unique : ∀ z : OneCycle ℚ (p:=p) (q:=q) (r:=r),
    ∀ x : GenericTriangle p q r → ℚ,
      (boundary2R ℚ (p:=p) (q:=q) (r:=r)).mulVec x = z →
      topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r) x = 0 →
      x = hodgeGaugeFilling (p:=p) (q:=q) (r:=r) z

noncomputable def hodgeGaugeFillingPassport :
    HodgeGaugeFillingPassport p q r where
  fills := boundary2_hodgeGaugeFilling
  gauge := hodgeGaugeFilling_gauge
  unique := hodgeGaugeFilling_unique

end D0.Topology.GenericTripartiteTopHodgeGauge
