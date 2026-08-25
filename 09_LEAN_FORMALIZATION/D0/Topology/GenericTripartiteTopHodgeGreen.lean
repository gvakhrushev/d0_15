import D0.Topology.GenericTripartiteTopHodgeSpectrum
import Mathlib.Tactic

/-!
# D0-GENERIC-TRIPARTITE-TOP-HODGE-GREEN-001

Using the complete rational eigenbasis of the upper Hodge Laplacian, this
module constructs its canonical spectral pseudoinverse:

* positive sectors of eigenvalue `λ` are multiplied by `λ⁻¹`;
* the harmonic sector is annihilated.

If `G` is this Green operator and `P_harm` the spectral harmonic projector,

```
Δ₂ G = G Δ₂ = I - P_harm,
P_harm² = P_harm,
G P_harm = 0.
```

Scope: this is a finite rational chain-level Green operator.  It is not a
physical propagator, and its construction is not asserted over arbitrary
coefficient rings.
-/

namespace D0.Topology.GenericTripartiteTopHodgeGreen
open Matrix
open D0.Topology.GenericTripartiteHomology
open D0.Topology.GenericTripartiteTopHodgeSpectrum

variable {p q r : ℕ}

local notation "Triangle" => GenericTriangle p q r
local notation "Mode" => HodgeModeIndex p q r

/-- Spectral inverse weight: invert positive sectors, kill the harmonic sector. -/
def greenWeight (i : Mode) : ℚ :=
  if triangleModeEigenvalue i = 0 then 0 else (triangleModeEigenvalue i)⁻¹

/-- Spectral characteristic function of the harmonic sector. -/
def harmonicWeight (i : Mode) : ℚ :=
  if triangleModeEigenvalue i = 0 then 1 else 0

/-- Upper Hodge Laplacian as a linear endomorphism. -/
def topHodgeEnd : Module.End ℚ (Triangle → ℚ) :=
  (topHodgeLaplacian (p:=p) (q:=q) (r:=r)).mulVecLin

/-- Moore-Penrose/Green spectral inverse of the upper Hodge Laplacian. -/
noncomputable def topHodgeGreen : Module.End ℚ (Triangle → ℚ) :=
  (triangleModeBasis (p:=p) (q:=q) (r:=r)).constr ℚ
    (fun i => greenWeight i • triangleModeBasis i)

/-- Spectral projector onto the harmonic tensor sectors. -/
noncomputable def topHodgeHarmonicProjector : Module.End ℚ (Triangle → ℚ) :=
  (triangleModeBasis (p:=p) (q:=q) (r:=r)).constr ℚ
    (fun i => harmonicWeight i • triangleModeBasis i)

@[simp] theorem topHodgeGreen_basis (i : Mode) :
    topHodgeGreen (p:=p) (q:=q) (r:=r)
        (triangleModeBasis i) =
      greenWeight i • triangleModeBasis i := by
  exact Module.Basis.constr_basis
    (triangleModeBasis (p:=p) (q:=q) (r:=r)) ℚ _ i

@[simp] theorem topHodgeHarmonicProjector_basis (i : Mode) :
    topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r)
        (triangleModeBasis i) =
      harmonicWeight i • triangleModeBasis i := by
  exact Module.Basis.constr_basis
    (triangleModeBasis (p:=p) (q:=q) (r:=r)) ℚ _ i

@[simp] theorem topHodgeEnd_basis (i : Mode) :
    topHodgeEnd (p:=p) (q:=q) (r:=r) (triangleModeBasis i) =
      triangleModeEigenvalue i • triangleModeBasis i := by
  exact topHodge_triangleModeBasis i

private lemma eigenvalue_mul_greenWeight (i : Mode) :
    triangleModeEigenvalue i * greenWeight i = 1 - harmonicWeight i := by
  unfold greenWeight harmonicWeight
  by_cases h : triangleModeEigenvalue i = 0
  · simp [h]
  · simp [h]

private lemma greenWeight_mul_eigenvalue (i : Mode) :
    greenWeight i * triangleModeEigenvalue i = 1 - harmonicWeight i := by
  rw [mul_comm]
  exact eigenvalue_mul_greenWeight i

/-- `Delta G = I - P_harm`. -/
theorem topHodge_comp_green :
    (topHodgeEnd (p:=p) (q:=q) (r:=r)).comp
        (topHodgeGreen (p:=p) (q:=q) (r:=r)) =
      LinearMap.id -
        topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r) := by
  apply (triangleModeBasis (p:=p) (q:=q) (r:=r)).ext
  intro i
  simp only [LinearMap.comp_apply, topHodgeGreen_basis, map_smul,
    topHodgeEnd_basis, smul_smul, LinearMap.sub_apply, LinearMap.id_apply,
    topHodgeHarmonicProjector_basis]
  rw [greenWeight_mul_eigenvalue]
  rw [sub_smul]
  simp

/-- `G Delta = I - P_harm`. -/
theorem green_comp_topHodge :
    (topHodgeGreen (p:=p) (q:=q) (r:=r)).comp
        (topHodgeEnd (p:=p) (q:=q) (r:=r)) =
      LinearMap.id -
        topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r) := by
  apply (triangleModeBasis (p:=p) (q:=q) (r:=r)).ext
  intro i
  simp only [LinearMap.comp_apply, topHodgeEnd_basis, map_smul,
    topHodgeGreen_basis, smul_smul, LinearMap.sub_apply, LinearMap.id_apply,
    topHodgeHarmonicProjector_basis]
  rw [eigenvalue_mul_greenWeight]
  rw [sub_smul]
  simp

/-- The harmonic projector is idempotent. -/
theorem harmonicProjector_idempotent :
    (topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r)).comp
        (topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r)) =
      topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r) := by
  apply (triangleModeBasis (p:=p) (q:=q) (r:=r)).ext
  intro i
  simp only [LinearMap.comp_apply, topHodgeHarmonicProjector_basis,
    map_smul, smul_smul]
  unfold harmonicWeight
  by_cases h : triangleModeEigenvalue i = 0 <;> simp [h]

/-- The Green operator kills harmonic modes. -/
theorem green_comp_harmonicProjector :
    (topHodgeGreen (p:=p) (q:=q) (r:=r)).comp
        (topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r)) = 0 := by
  apply (triangleModeBasis (p:=p) (q:=q) (r:=r)).ext
  intro i
  simp only [LinearMap.comp_apply, topHodgeHarmonicProjector_basis,
    map_smul, topHodgeGreen_basis, smul_smul, LinearMap.zero_apply]
  unfold greenWeight harmonicWeight
  by_cases h : triangleModeEigenvalue i = 0 <;> simp [h]

/-- The harmonic projector also kills the image of Green. -/
theorem harmonicProjector_comp_green :
    (topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r)).comp
        (topHodgeGreen (p:=p) (q:=q) (r:=r)) = 0 := by
  apply (triangleModeBasis (p:=p) (q:=q) (r:=r)).ext
  intro i
  simp only [LinearMap.comp_apply, topHodgeGreen_basis, map_smul,
    topHodgeHarmonicProjector_basis, smul_smul, LinearMap.zero_apply]
  unfold greenWeight harmonicWeight
  by_cases h : triangleModeEigenvalue i = 0 <;> simp [h]

/-- The Hodge operator kills its harmonic projector. -/
theorem topHodge_comp_harmonicProjector :
    (topHodgeEnd (p:=p) (q:=q) (r:=r)).comp
        (topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r)) = 0 := by
  apply (triangleModeBasis (p:=p) (q:=q) (r:=r)).ext
  intro i
  simp only [LinearMap.comp_apply, topHodgeHarmonicProjector_basis,
    map_smul, topHodgeEnd_basis, smul_smul, LinearMap.zero_apply]
  unfold harmonicWeight
  by_cases h : triangleModeEigenvalue i = 0 <;> simp [h]

/-- Green acts on each nonharmonic sector by reciprocal eigenvalue. -/
theorem topHodgeGreen_nonzero_basis (i : Mode)
    (h : triangleModeEigenvalue i ≠ 0) :
    topHodgeGreen (p:=p) (q:=q) (r:=r)
        (triangleModeBasis i) =
      (triangleModeEigenvalue i)⁻¹ • triangleModeBasis i := by
  rw [topHodgeGreen_basis]
  simp [greenWeight, h]

/-- Green vanishes on every harmonic tensor mode. -/
theorem topHodgeGreen_zero_basis (i : Mode)
    (h : triangleModeEigenvalue i = 0) :
    topHodgeGreen (p:=p) (q:=q) (r:=r)
        (triangleModeBasis i) = 0 := by
  rw [topHodgeGreen_basis]
  simp [greenWeight, h]

/-- Source-scene Green eigenvalues with multiplicity. -/
def sceneTopHodgeGreenSpectrum : List (ℚ × ℕ) :=
  [(0,960), (1/9,120), (1/11,96), (1/13,80),
   (1/20,12), (1/22,10), (1/24,8), (1/33,1)]

/-- Exact trace of the finite source-scene Green operator. -/
theorem scene_top_hodge_green_trace :
    (sceneTopHodgeGreenSpectrum.map
      (fun x => x.1 * (x.2 : ℚ))).sum = 63562 / 2145 := by
  norm_num [sceneTopHodgeGreenSpectrum]

/-- Green's largest eigenvalue is the reciprocal spectral gap `1/9`. -/
theorem scene_top_hodge_green_positive_bound :
    ∀ x ∈ sceneTopHodgeGreenSpectrum,
      x.1 ≠ 0 → 0 < x.1 ∧ x.1 ≤ (1/9 : ℚ) := by
  native_decide

/-- Pseudoinverse passport. -/
structure TopHodgeGreenPassport (p q r : ℕ) where
  leftInverseOffHarmonic :
    (topHodgeEnd (p:=p) (q:=q) (r:=r)).comp
        (topHodgeGreen (p:=p) (q:=q) (r:=r)) =
      LinearMap.id -
        topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r)
  rightInverseOffHarmonic :
    (topHodgeGreen (p:=p) (q:=q) (r:=r)).comp
        (topHodgeEnd (p:=p) (q:=q) (r:=r)) =
      LinearMap.id -
        topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r)
  projectorIdempotent :
    (topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r)).comp
        (topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r)) =
      topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r)
  greenKillsHarmonic :
    (topHodgeGreen (p:=p) (q:=q) (r:=r)).comp
        (topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r)) = 0
  harmonicKillsGreen :
    (topHodgeHarmonicProjector (p:=p) (q:=q) (r:=r)).comp
        (topHodgeGreen (p:=p) (q:=q) (r:=r)) = 0

noncomputable def topHodgeGreenPassport :
    TopHodgeGreenPassport p q r where
  leftInverseOffHarmonic := topHodge_comp_green
  rightInverseOffHarmonic := green_comp_topHodge
  projectorIdempotent := harmonicProjector_idempotent
  greenKillsHarmonic := green_comp_harmonicProjector
  harmonicKillsGreen := harmonicProjector_comp_green

end D0.Topology.GenericTripartiteTopHodgeGreen
