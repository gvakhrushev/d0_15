import D0.Topology.GenericTripartiteTopHodgeSpectrum
import D0.Synthesis.CarrierTopologicalScenePassport
import Mathlib.Tactic

/-!
# D0-TOP-HODGE-SPECTRAL-SCENE-RECONSTRUCTION-001

For the canonical complete-tripartite clique complex with zone sizes

```
a = p + 1,  b = q + 1,  c = r + 1,
```

the already-proved complete eigenbasis of the actual upper Hodge Laplacian
`Δ₂ = ∂₂ᵀ∂₂` supplies three intrinsic spectral coordinates:

* `D = dim C₂ = abc`;
* `H = dim ker Δ₂ = (a-1)(b-1)(c-1)`;
* `M₂ = Σ λᵢ² = D(a+b+c+6)`.

Consequently these data recover the elementary symmetric invariants

```
T = D,
V = M₂ / D - 6,
E = T + V - 1 - H.
```

Thus the top-Hodge spectrum recovers the unordered tripartite partition through
the root multiset of `X³ - V X² + E X - T`.  The scene instance is

```
(D,H,M₂) = (1287,960,50193)
```

and reconstructs the unordered zone multiset `{9,11,13}` without an ordering
hypothesis or externally supplied search bounds.

The control pair `K(2,6,6)` / `K(3,3,8)` has the same `D=72` and the same
second moment `M₂=1440`, but harmonic multiplicities `25` and `28`.
Accordingly the harmonic coordinate is genuinely load-bearing.

Formal scope: the generic Lean theorem reconstructs the three elementary
symmetric invariants `V,E,T`; the unordered root-multiset conclusion is
packaged here for the scene values.  A separate generic polynomial-roots
injectivity theorem is not claimed by this module.
-/

namespace D0.Synthesis.TopHodgeSpectralSceneReconstruction

open scoped BigOperators
open D0.SelfReading.TypedIncidenceCarriers
open D0.Synthesis.SceneInvariantReconstruction
open D0.Topology.GenericTripartiteHomology
open D0.Topology.GenericTripartiteTopHodgeSpectrum
open D0.Synthesis.CarrierTopologicalScenePassport

/-- Dimension of the actual top-chain carrier on which `topHodgeLaplacian`
acts. -/
def topHodgeTriangleDimension (p q r : ℕ) : ℕ :=
  Fintype.card (HodgeModeIndex p q r)

/-- Harmonic multiplicity defined as the finrank of the actual Hodge kernel,
not as a declared sector count. -/
noncomputable def topHodgeHarmonicMultiplicity (p q r : ℕ) : ℕ :=
  Module.finrank ℚ
    (LinearMap.ker
      (topHodgeLaplacian (p := p) (q := q) (r := r)).mulVecLin)

/-- Second spectral moment of the actual complete eigenbasis. -/
def topHodgeSecondMoment (p q r : ℕ) : ℚ :=
  ∑ i : HodgeModeIndex p q r,
    triangleModeEigenvalue i ^ 2

/-- The mode family used in `topHodgeSecondMoment` is the already-proved
complete eigenbasis of the actual Hodge matrix. -/
theorem topHodgeSecondMoment_basis_owner
    (p q r : ℕ) (i : HodgeModeIndex p q r) :
    (topHodgeLaplacian (p := p) (q := q) (r := r)).mulVec
        (triangleModeBasis i) =
      triangleModeEigenvalue i • triangleModeBasis i :=
  topHodge_triangleModeBasis i

theorem topHodgeTriangleDimension_formula (p q r : ℕ) :
    topHodgeTriangleDimension p q r =
      (p + 1) * (q + 1) * (r + 1) := by
  simp [topHodgeTriangleDimension, HodgeModeIndex, GenericTriangle,
    TripartiteTriangle]
  ring

/-- The harmonic multiplicity is actual top homology: first identify the
Hodge kernel with `ker ∂₂`, then use the proved generic finrank theorem. -/
theorem topHodgeHarmonicMultiplicity_formula (p q r : ℕ) :
    topHodgeHarmonicMultiplicity p q r = p * q * r := by
  unfold topHodgeHarmonicMultiplicity
  rw [topHodge_kernel_eq_topKernel]
  exact boundary2_kernel_finrank

/-- Exact generic second spectral moment of the complete top-Hodge
eigenbasis.  The first moment is always `3D`; this is the first moment that
contains the vertex count. -/
theorem topHodgeSecondMoment_formula (p q r : ℕ) :
    topHodgeSecondMoment p q r =
      (((p + 1) * (q + 1) * (r + 1) : ℕ) : ℚ) *
        (((p + 1) + (q + 1) + (r + 1) + 6 : ℕ) : ℚ) := by
  simp [topHodgeSecondMoment, HodgeModeIndex, GenericTriangle,
    TripartiteTriangle, triangleModeEigenvalue, factorEigenvalue,
    Fintype.sum_prod_type, Fin.sum_univ_succ]
  ring

/-- The top-chain dimension is exactly the triangle count `T`. -/
theorem triangleCount_from_topHodgeDimension (p q r : ℕ) :
    triangleCount (p + 1) (q + 1) (r + 1) =
      topHodgeTriangleDimension p q r := by
  rw [topHodgeTriangleDimension_formula]
  rfl

/-- The second moment recovers the vertex count after division by the
nonzero top-chain dimension. -/
theorem vertexCount_from_topHodgeSecondMoment (p q r : ℕ) :
    (vertexCount (p + 1) (q + 1) (r + 1) : ℚ) =
      topHodgeSecondMoment p q r /
        topHodgeTriangleDimension p q r - 6 := by
  rw [topHodgeSecondMoment_formula, topHodgeTriangleDimension_formula]
  simp only [vertexCount]
  push_cast
  have hne :
      (((p + 1) * (q + 1) * (r + 1) : ℕ) : ℚ) ≠ 0 := by
    positivity
  field_simp
  ring

/-- The harmonic multiplicity is the Euler defect
`H = T - E + V - 1`; hence `D,H,M₂` recover the edge count `E`. -/
theorem edgeCount_from_topHodgeData (p q r : ℕ) :
    (edgeCount (p + 1) (q + 1) (r + 1) : ℤ) =
      (topHodgeTriangleDimension p q r : ℤ) +
        (vertexCount (p + 1) (q + 1) (r + 1) : ℤ) - 1 -
          (topHodgeHarmonicMultiplicity p q r : ℤ) := by
  rw [topHodgeTriangleDimension_formula,
    topHodgeHarmonicMultiplicity_formula]
  simp only [edgeCount, vertexCount]
  push_cast
  ring

/-- Generic moment-to-elementary-symmetric reconstruction bundle. -/
theorem topHodge_spectral_data_recovers_VET (p q r : ℕ) :
    triangleCount (p + 1) (q + 1) (r + 1) =
        topHodgeTriangleDimension p q r ∧
      (vertexCount (p + 1) (q + 1) (r + 1) : ℚ) =
        topHodgeSecondMoment p q r /
          topHodgeTriangleDimension p q r - 6 ∧
      (edgeCount (p + 1) (q + 1) (r + 1) : ℤ) =
        (topHodgeTriangleDimension p q r : ℤ) +
          (vertexCount (p + 1) (q + 1) (r + 1) : ℤ) - 1 -
            (topHodgeHarmonicMultiplicity p q r : ℤ) :=
  ⟨triangleCount_from_topHodgeDimension p q r,
    vertexCount_from_topHodgeSecondMoment p q r,
    edgeCount_from_topHodgeData p q r⟩

/-- Arithmetic classification behind the unordered scene theorem: the only
labelled reduced triples are the six permutations of `(8,10,12)`.  Numeric
upper bounds are not hypotheses; ordering is used only internally to invoke
the already-proved ordered representative theorem. -/
theorem reduced_scene_six_permutations
    (p q r : ℕ)
    (hV : vertexCount (p + 1) (q + 1) (r + 1) = 33)
    (hB : p * q * r = 960) :
    (p = 8 ∧ q = 10 ∧ r = 12) ∨
    (p = 8 ∧ q = 12 ∧ r = 10) ∨
    (p = 10 ∧ q = 8 ∧ r = 12) ∨
    (p = 10 ∧ q = 12 ∧ r = 8) ∨
    (p = 12 ∧ q = 8 ∧ r = 10) ∨
    (p = 12 ∧ q = 10 ∧ r = 8) := by
  have ordered
      (x y z : ℕ)
      (hxy : x ≤ y) (hyz : y ≤ z)
      (hVxyz : vertexCount (x + 1) (y + 1) (z + 1) = 33)
      (hBxyz : x * y * z = 960) :
      (x + 1, y + 1, z + 1) = (9, 11, 13) := by
    apply reconstruct_from_vertices_reduced_product
    · omega
    · omega
    · omega
    · exact hVxyz
    · simpa [reducedZoneProduct] using hBxyz
  rcases le_total p q with hpq | hqp
  · rcases le_total q r with hqr | hrq
    · have h := ordered p q r hpq hqr hV hB
      simp only [Prod.mk.injEq] at h
      omega
    · rcases le_total p r with hpr | hrp
      · have h := ordered p r q hpr hrq
          (by
            simpa [vertexCount, add_comm, add_left_comm, add_assoc] using hV)
          (by
            simpa [mul_comm, mul_left_comm, mul_assoc] using hB)
        simp only [Prod.mk.injEq] at h
        omega
      · have h := ordered r p q hrp hpq
          (by
            simpa [vertexCount, add_comm, add_left_comm, add_assoc] using hV)
          (by
            simpa [mul_comm, mul_left_comm, mul_assoc] using hB)
        simp only [Prod.mk.injEq] at h
        omega
  · rcases le_total p r with hpr | hrp
    · have h := ordered q p r hqp hpr
        (by
          simpa [vertexCount, add_comm, add_left_comm, add_assoc] using hV)
        (by
          simpa [mul_comm, mul_left_comm, mul_assoc] using hB)
      simp only [Prod.mk.injEq] at h
      omega
    · rcases le_total q r with hqr | hrq
      · have h := ordered q r p hqr hrp
          (by
            simpa [vertexCount, add_comm, add_left_comm, add_assoc] using hV)
          (by
            simpa [mul_comm, mul_left_comm, mul_assoc] using hB)
        simp only [Prod.mk.injEq] at h
        omega
      · have h := ordered r q p hrq hqp
          (by
            simpa [vertexCount, add_comm, add_left_comm, add_assoc] using hV)
          (by
            simpa [mul_comm, mul_left_comm, mul_assoc] using hB)
        simp only [Prod.mk.injEq] at h
        omega

/-- Unordered arithmetic scene reconstruction. -/
theorem reduced_scene_unordered
    (p q r : ℕ)
    (hV : vertexCount (p + 1) (q + 1) (r + 1) = 33)
    (hB : p * q * r = 960) :
    ({p + 1, q + 1, r + 1} : Multiset ℕ) =
      ({9, 11, 13} : Multiset ℕ) := by
  rcases reduced_scene_six_permutations p q r hV hB with
    h | h | h | h | h | h
  all_goals
    rcases h with ⟨rfl, rfl, rfl⟩
    decide

/-- Exact source-scene spectral coordinates. -/
theorem scene_topHodge_spectral_coordinates :
    topHodgeTriangleDimension 8 10 12 = 1287 ∧
      topHodgeHarmonicMultiplicity 8 10 12 = 960 ∧
      topHodgeSecondMoment 8 10 12 = 50193 := by
  rw [topHodgeTriangleDimension_formula,
    topHodgeHarmonicMultiplicity_formula,
    topHodgeSecondMoment_formula]
  norm_num

/-- **Scene capstone.** Any canonical complete-tripartite top-Hodge operator
with the scene's top-chain dimension, actual harmonic multiplicity and second
spectral moment has the unordered zone multiset `{9,11,13}`.  There is no
ordering assumption and no externally supplied search bound. -/
theorem reconstruct_scene_unordered_from_topHodge_spectral_data
    (p q r : ℕ)
    (hD : topHodgeTriangleDimension p q r = 1287)
    (hH : topHodgeHarmonicMultiplicity p q r = 960)
    (hM2 : topHodgeSecondMoment p q r = 50193) :
    ({p + 1, q + 1, r + 1} : Multiset ℕ) =
      ({9, 11, 13} : Multiset ℕ) := by
  have hT : (p + 1) * (q + 1) * (r + 1) = 1287 := by
    rw [topHodgeTriangleDimension_formula] at hD
    exact hD
  have hB : p * q * r = 960 := by
    rw [topHodgeHarmonicMultiplicity_formula] at hH
    exact hH
  have hMoment := topHodgeSecondMoment_formula p q r
  rw [hM2, hT] at hMoment
  have hVQ :
      (p : ℚ) + 1 + ((q : ℚ) + 1) + ((r : ℚ) + 1) = 33 := by
    norm_num at hMoment
    nlinarith
  have hV : vertexCount (p + 1) (q + 1) (r + 1) = 33 := by
    simp only [vertexCount]
    exact_mod_cast hVQ
  exact reduced_scene_unordered p q r hV hB

/-- Load-bearing control: equal top-chain dimension and equal second moment do
not determine the partition without the actual harmonic multiplicity. -/
theorem harmonic_multiplicity_is_load_bearing :
    topHodgeTriangleDimension 1 5 5 = 72 ∧
      topHodgeTriangleDimension 2 2 7 = 72 ∧
      topHodgeSecondMoment 1 5 5 = 1440 ∧
      topHodgeSecondMoment 2 2 7 = 1440 ∧
      topHodgeHarmonicMultiplicity 1 5 5 = 25 ∧
      topHodgeHarmonicMultiplicity 2 2 7 = 28 ∧
      ({2, 6, 6} : Multiset ℕ) ≠
        ({3, 3, 8} : Multiset ℕ) := by
  rw [topHodgeTriangleDimension_formula,
    topHodgeTriangleDimension_formula,
    topHodgeSecondMoment_formula,
    topHodgeSecondMoment_formula,
    topHodgeHarmonicMultiplicity_formula,
    topHodgeHarmonicMultiplicity_formula]
  norm_num
  decide

end D0.Synthesis.TopHodgeSpectralSceneReconstruction
