import D0.Topology.GenericTripartiteTopHodgeSpectrum
import D0.Synthesis.SceneNormalizedQuotientDescent
import D0.Synthesis.PhasonActiveSceneConjugacy
import Mathlib.Tactic

/-!
# D0-TOP-HODGE-KIRCHHOFF-STATIONARY-BRIDGE-001

For the complete tripartite clique complex `K(a,b,c)`, with

```
a = p+1, b = q+1, c = r+1,
dₐ = b+c, dᵦ = a+c, d_c = a+b,
S = a dₐ + b dᵦ + c d_c,
```

this module connects two operators which were previously owned separately:

* the actual top Hodge Laplacian `Δ₂ = ∂₂ᵀ∂₂`, through its proved complete
  tensor eigenbasis;
* the normalized random walk on the three zone quotient, through the
  basis-free product of the two nonzero eigenvalues of `I-M`.

The common factor is

```
K = (a+b+c) dₐ^(a-1) dᵦ^(b-1) d_c^(c-1).
```

It is both the high-sector factor of the positive top-Hodge
pseudodeterminant and

```
K = pdet(I-M) * (dₐ^a dᵦ^b d_c^c) / S.
```

Classically, `K` is the spanning-tree number of `K(a,b,c)`.  This file does
not claim that interpretation as a Lean theorem: the current dependency graph
contains no Matrix-Tree theorem connecting a graph cofactor to spanning trees.
What is proved here is the operator and exact-arithmetic identity on both
sides of that missing boundary.

The scene specialization uses the already-owned descent of the literal
`33 × 33` graph and the already-owned active conjugacy with the two-mode S_DE
transfer.  The result therefore explains the value `359/160`; it does not
merely recompute it.
-/

namespace D0.Synthesis.TopHodgeKirchhoffStationaryBridge

open scoped BigOperators
open Matrix
open D0.Topology.GenericTripartiteTopHodgeSpectrum

abbrev Zone3 := Fin 3

def zoneA (p : ℕ) : ℕ := p + 1
def zoneB (q : ℕ) : ℕ := q + 1
def zoneC (r : ℕ) : ℕ := r + 1

def degreeA (q r : ℕ) : ℕ := q + r + 2
def degreeB (p r : ℕ) : ℕ := p + r + 2
def degreeC (p q : ℕ) : ℕ := p + q + 2

def totalVertices (p q r : ℕ) : ℕ := p + q + r + 3

/-- Total stationary degree mass `S = 2|E|`. -/
def stationaryMass (p q r : ℕ) : ℕ :=
  zoneA p * degreeA q r +
    zoneB q * degreeB p r +
      zoneC r * degreeC p q

theorem stationaryMass_eq_twice_edgeCount (p q r : ℕ) :
    stationaryMass p q r =
      2 * (zoneA p * zoneB q + zoneA p * zoneC r +
        zoneB q * zoneC r) := by
  simp [stationaryMass, zoneA, zoneB, zoneC, degreeA, degreeB, degreeC]
  ring

/-- Product of all literal vertex degrees. -/
def fullDegreeProduct (p q r : ℕ) : ℕ :=
  degreeA q r ^ zoneA p *
    degreeB p r ^ zoneB q *
      degreeC p q ^ zoneC r

/-- Low tensor-sector contribution to the positive top-Hodge pseudodeterminant. -/
def topHodgeLowFactor (p q r : ℕ) : ℕ :=
  zoneA p ^ (q * r) *
    zoneB q ^ (p * r) *
      zoneC r ^ (p * q)

/-- High tensor-sector contribution.  Classically this is the complete
tripartite Matrix-Tree number, but that interpretation is outside the formal
owner boundary of this module. -/
def topHodgeHighFactor (p q r : ℕ) : ℕ :=
  totalVertices p q r *
    degreeA q r ^ p *
      degreeB p r ^ q *
        degreeC p q ^ r

/-- Positive pseudodeterminant read from the proved complete eigenbasis of the
actual top-Hodge matrix.  Harmonic zero modes contribute the neutral factor
`1`. -/
def topHodgePositivePseudoDet (p q r : ℕ) : ℚ :=
  ∏ i : HodgeModeIndex p q r,
    if triangleModeEigenvalue i = 0 then 1 else triangleModeEigenvalue i

/-- The factors in `topHodgePositivePseudoDet` are the eigenvalues of a
complete basis of the actual top-Hodge matrix. -/
theorem topHodgePositivePseudoDet_basis_owner
    (p q r : ℕ) (i : HodgeModeIndex p q r) :
    (topHodgeLaplacian (p := p) (q := q) (r := r)).mulVec
        (triangleModeBasis i) =
      triangleModeEigenvalue i • triangleModeBasis i :=
  topHodge_triangleModeBasis i

theorem topHodgePositivePseudoDet_formula (p q r : ℕ) :
    topHodgePositivePseudoDet p q r =
      ((topHodgeLowFactor p q r * topHodgeHighFactor p q r : ℕ) : ℚ) := by
  have hp : (p + 1 : ℚ) ≠ 0 := by positivity
  have hq : (q + 1 : ℚ) ≠ 0 := by positivity
  have hr : (r + 1 : ℚ) ≠ 0 := by positivity
  have hpq : ((p + 1 : ℚ) + (q + 1 : ℚ)) ≠ 0 := by positivity
  have hpr : ((p + 1 : ℚ) + (r + 1 : ℚ)) ≠ 0 := by positivity
  have hqr : ((q + 1 : ℚ) + (r + 1 : ℚ)) ≠ 0 := by positivity
  have hpqr :
      ((p + 1 : ℚ) + (q + 1 : ℚ) + (r + 1 : ℚ)) ≠ 0 := by
    positivity
  simp [topHodgePositivePseudoDet, HodgeModeIndex,
    triangleModeEigenvalue, factorEigenvalue,
    Fintype.prod_prod_type, Fin.prod_univ_succ, topHodgeLowFactor,
    topHodgeHighFactor, zoneA, zoneB, zoneC, degreeA, degreeB, degreeC,
    totalVertices, hp, hq, hr, hpq, hpr, hqr, hpqr, pow_mul, mul_pow]
  ring

/-! ## Generic normalized quotient and its active characteristic coefficient -/

/-- Generic row-stochastic zone quotient of the complete tripartite graph. -/
def genericZoneTransport (p q r : ℕ) : Matrix Zone3 Zone3 ℚ :=
  !![0, (zoneB q : ℚ) / degreeA q r, (zoneC r : ℚ) / degreeA q r;
     (zoneA p : ℚ) / degreeB p r, 0, (zoneC r : ℚ) / degreeB p r;
     (zoneA p : ℚ) / degreeC p q, (zoneB q : ℚ) / degreeC p q, 0]

/-- Generic normalized quotient Laplacian `I-M`. -/
def genericNormalizedLaplacian (p q r : ℕ) : Matrix Zone3 Zone3 ℚ :=
  1 - genericZoneTransport p q r

/-- Degree-weighted stationary measure on the three quotient cells. -/
def genericStationaryWeight (p q r : ℕ) : Matrix (Fin 1) Zone3 ℚ :=
  !![(zoneA p * degreeA q r : ℕ),
     (zoneB q * degreeB p r : ℕ),
     (zoneC r * degreeC p q : ℕ)]

def genericStationaryColumn : Matrix Zone3 (Fin 1) ℚ :=
  !![1; 1; 1]

/-- The second characteristic coefficient of a `3 × 3` matrix: the sum of
its three principal `2 × 2` minors. -/
def principalMinorSum2 (L : Matrix Zone3 Zone3 ℚ) : ℚ :=
  (L 0 0 * L 1 1 - L 0 1 * L 1 0) +
    (L 0 0 * L 2 2 - L 0 2 * L 2 0) +
      (L 1 1 * L 2 2 - L 1 2 * L 2 1)

/-- Trace-only form of the second characteristic coefficient.  This is the
coordinate-free reason for using `principalMinorSum2` rather than a selected
`2 × 2` block determinant. -/
theorem principalMinorSum2_trace_formula (L : Matrix Zone3 Zone3 ℚ) :
    principalMinorSum2 L =
      (L.trace ^ 2 - (L * L).trace) / 2 := by
  simp [principalMinorSum2, Matrix.trace, Matrix.mul_apply,
    Fin.sum_univ_succ]
  ring

/-- Basis-free active pseudodeterminant coordinate of the rank-two normalized
Laplacian.  Because `I-M` has the stationary zero mode, its second
characteristic coefficient is the product of its two active eigenvalues. -/
def normalizedActivePseudoDet (p q r : ℕ) : ℚ :=
  principalMinorSum2 (genericNormalizedLaplacian p q r)

theorem genericZoneTransport_row_stochastic (p q r : ℕ) :
    ∀ i, ∑ j, genericZoneTransport p q r i j = 1 := by
  intro i
  fin_cases i <;>
    simp [genericZoneTransport, zoneA, zoneB, zoneC, degreeA, degreeB,
      degreeC, Fin.sum_univ_succ] <;>
    field_simp <;>
    ring

theorem genericStationaryWeight_stationary (p q r : ℕ) :
    genericStationaryWeight p q r * genericZoneTransport p q r =
      genericStationaryWeight p q r := by
  ext i j
  fin_cases i
  fin_cases j <;>
    simp [genericStationaryWeight, genericZoneTransport, zoneA, zoneB, zoneC,
      degreeA, degreeB, degreeC, Matrix.mul_apply, Fin.sum_univ_succ] <;>
    field_simp <;>
    ring

theorem genericStationaryWeight_total (p q r : ℕ) :
    genericStationaryWeight p q r * genericStationaryColumn =
      !![((stationaryMass p q r : ℕ) : ℚ)] := by
  ext i j
  fin_cases i
  fin_cases j
  simp [genericStationaryWeight, genericStationaryColumn, stationaryMass,
    Matrix.mul_apply, Fin.sum_univ_succ]
  ring

/-- The constant mode is the exact stationary zero mode of `I-M`. -/
theorem genericNormalizedLaplacian_mulVec_one (p q r : ℕ) :
    (genericNormalizedLaplacian p q r).mulVec (fun _ => 1) = 0 := by
  funext i
  rw [show genericNormalizedLaplacian p q r =
      1 - genericZoneTransport p q r by rfl]
  rw [Matrix.sub_mulVec, Matrix.one_mulVec]
  simp only [Pi.sub_apply, Pi.zero_apply, Matrix.mulVec,
    dotProduct, mul_one]
  rw [genericZoneTransport_row_stochastic]
  simp

theorem genericNormalizedLaplacian_det_zero (p q r : ℕ) :
    (genericNormalizedLaplacian p q r).det = 0 := by
  rw [Matrix.det_fin_three]
  simp [genericNormalizedLaplacian, genericZoneTransport, zoneA, zoneB, zoneC,
    degreeA, degreeB, degreeC]
  field_simp
  ring

/-- The active characteristic coefficient is a stationary/degree expression,
not an isolated scene number. -/
theorem normalizedActivePseudoDet_formula (p q r : ℕ) :
    normalizedActivePseudoDet p q r =
      (stationaryMass p q r : ℚ) * (totalVertices p q r : ℚ) /
        ((degreeA q r : ℚ) * (degreeB p r : ℚ) * (degreeC p q : ℚ)) := by
  simp [normalizedActivePseudoDet, principalMinorSum2,
    genericNormalizedLaplacian, genericZoneTransport,
    zoneA, zoneB, zoneC, degreeA, degreeB, degreeC, stationaryMass,
    totalVertices]
  field_simp
  ring

theorem normalizedActivePseudoDet_pos (p q r : ℕ) :
    0 < normalizedActivePseudoDet p q r := by
  rw [normalizedActivePseudoDet_formula]
  unfold stationaryMass totalVertices degreeA degreeB degreeC zoneA zoneB zoneC
  positivity

/-! ## The cross-operator bridge -/

/-- The normalized active invariant becomes exactly the high top-Hodge sector
after restoring the stationary mass and the literal degree product. -/
theorem normalizedActivePseudoDet_degree_bridge (p q r : ℕ) :
    normalizedActivePseudoDet p q r *
        (fullDegreeProduct p q r : ℚ) / (stationaryMass p q r : ℚ) =
      (topHodgeHighFactor p q r : ℚ) := by
  rw [normalizedActivePseudoDet_formula]
  simp only [fullDegreeProduct, topHodgeHighFactor, zoneA, zoneB, zoneC,
    Nat.cast_mul, Nat.cast_pow]
  have hS : (stationaryMass p q r : ℚ) ≠ 0 := by
    unfold stationaryMass degreeA degreeB degreeC zoneA zoneB zoneC
    positivity
  have hA : (degreeA q r : ℚ) ≠ 0 := by
    unfold degreeA
    positivity
  have hB : (degreeB p r : ℚ) ≠ 0 := by
    unfold degreeB
    positivity
  have hC : (degreeC p q : ℚ) ≠ 0 := by
    unfold degreeC
    positivity
  field_simp [hS, hA, hB, hC]
  simp [totalVertices, degreeA, degreeB, degreeC, pow_succ]
  ring

/-- **Generic capstone.**  The positive pseudodeterminant of the actual
top-Hodge matrix is reconstructed from its low tensor sectors and the
basis-free normalized-walk invariant together with the literal stationary
degree measure. -/
theorem topHodge_stationary_pseudodeterminant_bridge (p q r : ℕ) :
    topHodgePositivePseudoDet p q r =
      (topHodgeLowFactor p q r : ℚ) *
        normalizedActivePseudoDet p q r *
          (fullDegreeProduct p q r : ℚ) / (stationaryMass p q r : ℚ) := by
  rw [topHodgePositivePseudoDet_formula]
  push_cast
  rw [← normalizedActivePseudoDet_degree_bridge p q r]
  ring

/-! ## Literal scene and S_DE anchoring -/

theorem scene_genericZoneTransport_eq_owned :
    genericZoneTransport 8 10 12 = D0.Spectral.zoneTransport := by
  native_decide

theorem scene_genericNormalizedLaplacian_eq_owned :
    genericNormalizedLaplacian 8 10 12 =
      D0.Synthesis.PhasonActiveSceneConjugacy.normalizedSceneLaplacian := by
  native_decide

theorem scene_genericNormalizedLaplacian_eq_quotient :
    genericNormalizedLaplacian 8 10 12 =
      D0.Synthesis.SceneNormalizedQuotientDescent.quotientNormalizedLaplacian := by
  native_decide

/-- The generic operator at `(9,11,13)` is the quotient induced from the
literal `33 × 33` graph. -/
theorem scene_literal_laplacian_descends_to_generic :
    D0.Synthesis.SceneNormalizedQuotientDescent.fullNormalizedLaplacian *
        D0.Claims.Cind31 =
      D0.Claims.Cind31 * genericNormalizedLaplacian 8 10 12 := by
  calc
    _ = D0.Claims.Cind31 *
        D0.Synthesis.SceneNormalizedQuotientDescent.quotientNormalizedLaplacian :=
      D0.Synthesis.SceneNormalizedQuotientDescent.full_laplacian_indicator_intertwining
    _ = _ := by rw [scene_genericNormalizedLaplacian_eq_quotient]

theorem scene_genericStationaryWeight_eq_owned :
    genericStationaryWeight 8 10 12 =
      D0.Synthesis.SceneNormalizedQuotientDescent.stationaryWeight := by
  native_decide

theorem scene_stationaryMass :
    stationaryMass 8 10 12 = 718 := by
  norm_num [stationaryMass, zoneA, zoneB, zoneC, degreeA, degreeB, degreeC]

/-- The active characteristic coefficient of the generic normalized quotient
is exactly the determinant of the already-owned two-mode S_DE transfer. -/
theorem scene_normalizedActivePseudoDet_eq_sde_det :
    normalizedActivePseudoDet 8 10 12 =
      D0.Cosmology.phasonFlipTransferMatrix.det := by
  native_decide

/-- The equality above is operator-grounded: the actual normalized scene
Laplacian intertwines with the S_DE transfer through the owned full-rank
active embedding. -/
theorem scene_generic_normalized_sde_intertwining :
    genericNormalizedLaplacian 8 10 12 *
        D0.Synthesis.PhasonActiveSceneConjugacy.activeEmbedding =
      D0.Synthesis.PhasonActiveSceneConjugacy.activeEmbedding *
        D0.Synthesis.PhasonActiveSceneConjugacy.sdeTransfer := by
  rw [scene_genericNormalizedLaplacian_eq_owned]
  exact D0.Synthesis.PhasonActiveSceneConjugacy.normalized_scene_sde_intertwining

/-- Scene form of the bridge: the determinant of the actual active S_DE
transfer, together with the literal graph degree measure, supplies the entire
high-sector factor of the actual top-Hodge pseudodeterminant. -/
theorem scene_topHodge_sde_stationary_bridge :
    topHodgePositivePseudoDet 8 10 12 =
      (topHodgeLowFactor 8 10 12 : ℚ) *
        D0.Cosmology.phasonFlipTransferMatrix.det *
          (fullDegreeProduct 8 10 12 : ℚ) / 718 := by
  rw [topHodge_stationary_pseudodeterminant_bridge]
  rw [scene_normalizedActivePseudoDet_eq_sde_det, scene_stationaryMass]
  norm_num

/-! ## Destructive control -/

/-- Common scaling preserves the normalized active invariant but changes both
the restored high factor and the actual top-Hodge pseudodeterminant:

```
K(1,1,1): pdet_active = 9/4, high = 3;
K(2,2,2): pdet_active = 9/4, high = 384.
```

Thus the stationary mass and full degree product in the bridge are
load-bearing; the normalized operator alone cannot recover the Hodge or
Kirchhoff-scale invariant.
-/
theorem normalization_scale_destructive_control :
    normalizedActivePseudoDet 0 0 0 =
        normalizedActivePseudoDet 1 1 1 ∧
      topHodgeHighFactor 0 0 0 ≠ topHodgeHighFactor 1 1 1 ∧
      topHodgePositivePseudoDet 0 0 0 ≠
        topHodgePositivePseudoDet 1 1 1 := by
  native_decide

/-! ## Capstone -/

/-- **D0-TOP-HODGE-KIRCHHOFF-STATIONARY-BRIDGE.**  One package records the
actual eigenbasis product, generic normalized-walk restoration, literal scene
descent, and active S_DE realization. -/
theorem topHodge_kirchhoff_stationary_bridge :
    (∀ p q r,
      topHodgePositivePseudoDet p q r =
        (topHodgeLowFactor p q r : ℚ) *
          normalizedActivePseudoDet p q r *
            (fullDegreeProduct p q r : ℚ) /
              (stationaryMass p q r : ℚ)) ∧
      D0.Synthesis.SceneNormalizedQuotientDescent.fullNormalizedLaplacian *
          D0.Claims.Cind31 =
        D0.Claims.Cind31 * genericNormalizedLaplacian 8 10 12 ∧
      normalizedActivePseudoDet 8 10 12 =
        D0.Cosmology.phasonFlipTransferMatrix.det ∧
      normalizedActivePseudoDet 0 0 0 =
        normalizedActivePseudoDet 1 1 1 ∧
      topHodgeHighFactor 0 0 0 ≠ topHodgeHighFactor 1 1 1 :=
  ⟨topHodge_stationary_pseudodeterminant_bridge,
    scene_literal_laplacian_descends_to_generic,
    scene_normalizedActivePseudoDet_eq_sde_det,
    normalization_scale_destructive_control.1,
    normalization_scale_destructive_control.2.1⟩

end D0.Synthesis.TopHodgeKirchhoffStationaryBridge
