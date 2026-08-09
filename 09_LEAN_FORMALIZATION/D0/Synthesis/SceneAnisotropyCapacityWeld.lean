import D0.Core.DyadABCD
import D0.Phase
import D0.Synthesis.SceneInvariantReconstruction
import D0.VNext2.Rank3CubicSymmetricFunctions
import D0.VNext2.Rank3MetricSignature
import Mathlib.Tactic

/-!
# D0-SCENE-ANISOTROPY-CAPACITY-WELD-001

The address ladder is the centered triple `(9,11,13) = (11-2,11,11+2)`.
This module proves that its departure from the equal-zone control `(11,11,11)`
is not an unrelated set of integers:

* the half-spread is `2 = |Dyad|`;
* the total squared zone deviation is `8 = |Omega8|`;
* the missing edge count relative to `K(11,11,11)` is `4 = |ABCD|`;
* the missing triangle count is `44 = qT = |ABCD| * |V11|`, the first
  forced terminal return window;
* the same spread parameter is the factor that makes the rank-3 cubic
  discriminant nonzero, while spread `0` gives the equal-zone isotropic control.

The load-bearing content is the generic polynomial identity for a centered
triple `(m-d,m,m+d)`, proved before the D0 cardinalities are substituted:

```
sum squared deviations = 2 d^2
equal-zone edges - actual edges = d^2
equal-zone triangles - actual triangles = m d^2
```

At `d = |Dyad|`, the first two quantities become the signed role carrier
`Omega8 = Role x Orient` and the unsigned role carrier `ABCD = Dyad x Dyad`.
At `m = |V11|`, the third becomes the terminal window `qT`.

Honest scope: this is an exact combinatorial/capacity weld. It does not claim
that `4`, `8`, or `44` are new physical observables, does not derive the
complete-tripartite carrier again, and does not promote the finite carrier
anisotropy to an observed spacetime anisotropy.
-/

namespace D0.Synthesis.SceneAnisotropyCapacityWeld

/-- Edge count of the complete tripartite centered triple `(m-d,m,m+d)`. -/
def centeredEdges (m d : ℤ) : ℤ :=
  (m - d) * m + (m - d) * (m + d) + m * (m + d)

/-- Triangle count of the complete tripartite centered triple `(m-d,m,m+d)`. -/
def centeredTriangles (m d : ℤ) : ℤ :=
  (m - d) * m * (m + d)

/-- Sum of squared deviations from the center `m`. -/
def squaredAnisotropy (m d : ℤ) : ℤ :=
  ((m - d) - m) ^ 2 + (m - m) ^ 2 + ((m + d) - m) ^ 2

/-- Discriminant of the depressed rank-3 cubic
`lambda^3 - E lambda - 2T` attached to the centered triple. -/
def centeredCubicDiscriminant (m d : ℤ) : ℤ :=
  4 * (centeredEdges m d) ^ 3 - 108 * (centeredTriangles m d) ^ 2

/-- **Generic defect identities.** These are polynomial identities, not
scene-number checks. -/
theorem centered_defect_identities (m d : ℤ) :
    squaredAnisotropy m d = 2 * d ^ 2 ∧
      3 * m ^ 2 - centeredEdges m d = d ^ 2 ∧
      m ^ 3 - centeredTriangles m d = m * d ^ 2 := by
  unfold squaredAnisotropy centeredEdges centeredTriangles
  constructor
  · ring
  constructor <;> ring

/-- **Defect hierarchy.** The signed/oriented second moment is twice the
edge defect, and the triangle defect is the center times the edge defect.
This is the generic algebra behind `ABCD -> Omega8` and `ABCD*V11 -> qT`. -/
theorem centered_defect_hierarchy (m d : ℤ) :
    squaredAnisotropy m d =
        2 * (3 * m ^ 2 - centeredEdges m d) ∧
      m ^ 3 - centeredTriangles m d =
        m * (3 * m ^ 2 - centeredEdges m d) := by
  unfold squaredAnisotropy centeredEdges centeredTriangles
  constructor <;> ring

/-- The same spread `d` factors the cubic discriminant. In particular `d=0`
is the equal-zone isotropic control with zero discriminant. -/
theorem centered_discriminant_factorization (m d : ℤ) :
    centeredCubicDiscriminant m d =
      4 * d ^ 2 * (27 * m ^ 4 - 18 * d ^ 2 * m ^ 2 - d ^ 4) := by
  unfold centeredCubicDiscriminant centeredEdges centeredTriangles
  ring

/-- The capacity chain itself supplies the center and half-spread:
`|V11|=11`, `|Dyad|=2`, hence `(11-2,11,11+2)=(9,11,13)`. -/
theorem scene_ladder_is_capacity_centered :
    (((Fintype.card D0.V11 : ℤ) - (Fintype.card D0.Dyad : ℤ)),
      (Fintype.card D0.V11 : ℤ),
      ((Fintype.card D0.V11 : ℤ) + (Fintype.card D0.Dyad : ℤ))) =
        ((9 : ℤ), 11, 13) := by
  norm_num [D0.V11, D0.V9, D0.Omega8, D0.Role, D0.Dyad,
    D0.Orient, D0.Witness]

/-- **Capacity interpretation of the three defects.**

* squared anisotropy `8` is the oriented role carrier `Omega8`;
* the edge deficit `4` is the unsigned role carrier `ABCD`;
* the triangle deficit `44` is the first forced terminal window `qT`;
* `qT = |ABCD| * |V11|`.
-/
theorem scene_defects_are_capacity :
    squaredAnisotropy 11 2 = (Fintype.card D0.Omega8 : ℤ) ∧
      3 * (11 : ℤ) ^ 2 - centeredEdges 11 2 =
        (Fintype.card D0.Role : ℤ) ∧
      (11 : ℤ) ^ 3 - centeredTriangles 11 2 = (D0.qT : ℤ) ∧
      D0.qT = Fintype.card D0.Role * Fintype.card D0.V11 := by
  norm_num [squaredAnisotropy, centeredEdges, centeredTriangles,
    D0.qT, D0.Role, D0.Dyad, D0.Omega8, D0.Orient,
    D0.V11, D0.V9, D0.Witness]

/-- The generic defect hierarchy becomes the typed capacity hierarchy:
`Omega8 = 2*ABCD` and `qT = V11*ABCD`. -/
theorem scene_capacity_hierarchy :
    squaredAnisotropy 11 2 =
        2 * (3 * (11 : ℤ) ^ 2 - centeredEdges 11 2) ∧
      (Fintype.card D0.Omega8 : ℤ) =
        2 * (Fintype.card D0.Role : ℤ) ∧
      (11 : ℤ) ^ 3 - centeredTriangles 11 2 =
        11 * (3 * (11 : ℤ) ^ 2 - centeredEdges 11 2) ∧
      (D0.qT : ℤ) =
        (Fintype.card D0.V11 : ℤ) * (Fintype.card D0.Role : ℤ) := by
  norm_num [squaredAnisotropy, centeredEdges, centeredTriangles,
    D0.qT, D0.Role, D0.Dyad, D0.Omega8, D0.Orient,
    D0.V11, D0.V9, D0.Witness]

/-- **Reverse capacity reconstruction.** The two capacity faces

* edge defect `= |ABCD| = 4`,
* triangle defect `= qT = 44`,

uniquely recover the nonnegative centered spread `d=2` and center `m=11`,
hence the scene `(9,11,13)`. This is a structural alternative to reconstructing
the scene from `(V,E,T)`. -/
theorem capacity_defects_reconstruct_scene
    (m d : ℤ) (hd : 0 ≤ d)
    (hEdge :
      3 * m ^ 2 - centeredEdges m d = (Fintype.card D0.Role : ℤ))
    (hTriangle :
      m ^ 3 - centeredTriangles m d = (D0.qT : ℤ)) :
    (m - d, m, m + d) = ((9 : ℤ), 11, 13) := by
  have hDef := centered_defect_identities m d
  have hdSq : d ^ 2 = 4 := by
    rw [hDef.2.1] at hEdge
    norm_num [D0.Role, D0.Dyad] at hEdge
    exact hEdge
  have hmdSq : m * d ^ 2 = 44 := by
    rw [hDef.2.2] at hTriangle
    norm_num [D0.qT] at hTriangle
    exact hTriangle
  have hd2 : d = 2 := by
    nlinarith [sq_nonneg (d - 2), sq_nonneg (d + 2)]
  have hm11 : m = 11 := by
    rw [hd2] at hmdSq
    omega
  rw [hd2, hm11]
  norm_num

/-- Each capacity face alone is insufficient: edge defect `4` allows a
different center, while triangle defect `44` allows a different spread. -/
theorem single_capacity_face_not_enough :
    (3 * (10 : ℤ) ^ 2 - centeredEdges 10 2 =
      (Fintype.card D0.Role : ℤ) ∧
      ((10 - 2, 10, 10 + 2) : ℤ × ℤ × ℤ) ≠ ((9 : ℤ), 11, 13)) ∧
    ((44 : ℤ) ^ 3 - centeredTriangles 44 1 = (D0.qT : ℤ) ∧
      ((44 - 1, 44, 44 + 1) : ℤ × ℤ × ℤ) ≠ ((9 : ℤ), 11, 13)) := by
  norm_num [centeredEdges, centeredTriangles, D0.qT, D0.Role, D0.Dyad]

/-- **Dual reconstruction consistency.** The downstream cubic passport
`(E,T)=(359,1287)` and the upstream capacity-defect passport
`(ABCD,qT)=(4,44)` independently reconstruct the same canonical scene.
This is the commutative consistency square between the first and second
full-book synthesis passes. -/
theorem dual_scene_reconstruction :
    (∀ a b c : ℕ,
      0 < a → a ≤ b → b ≤ c →
      D0.Synthesis.SceneInvariantReconstruction.edgeCount a b c = 359 →
      D0.Synthesis.SceneInvariantReconstruction.triangleCount a b c = 1287 →
      (a, b, c) = (9, 11, 13)) ∧
    (∀ m d : ℤ,
      0 ≤ d →
      3 * m ^ 2 - centeredEdges m d = (Fintype.card D0.Role : ℤ) →
      m ^ 3 - centeredTriangles m d = (D0.qT : ℤ) →
      (m - d, m, m + d) = ((9 : ℤ), 11, 13)) :=
  ⟨D0.Synthesis.SceneInvariantReconstruction.reconstruct_from_edges_triangles,
    capacity_defects_reconstruct_scene⟩

/-- The scene instance reproduces the owned cubic discriminant, while the
equal-zone control has discriminant zero. -/
theorem scene_discriminant_weld :
    centeredCubicDiscriminant 11 2 = 6185264 ∧
      (0 : ℤ) < centeredCubicDiscriminant 11 2 ∧
      centeredCubicDiscriminant 11 0 = 0 := by
  have hScene :=
    D0.VNext2.Rank3CubicSymmetricFunctions.discriminant_positive
  have hEqual :=
    D0.VNext2.Rank3MetricSignature.equal_zone_discriminant_zero (11 : ℤ)
  constructor
  · calc
      centeredCubicDiscriminant 11 2 =
          (-4) * (-359 : ℤ) ^ 3 - 27 * (-2574 : ℤ) ^ 2 := by
            norm_num [centeredCubicDiscriminant, centeredEdges, centeredTriangles]
      _ = 6185264 := hScene.1
  constructor
  · norm_num [centeredCubicDiscriminant, centeredEdges, centeredTriangles]
  · calc
      centeredCubicDiscriminant 11 0 =
          (-4) * (-3 * (11 : ℤ) ^ 2) ^ 3 -
            27 * (-2 * (11 : ℤ) ^ 3) ^ 2 := by
              norm_num [centeredCubicDiscriminant, centeredEdges, centeredTriangles]
      _ = 0 := hEqual

/-- Negative controls: spread `1` and spread `3` do not realize the role
capacities, and changing the center to `10` breaks the terminal-window weld. -/
theorem capacity_weld_negative_controls :
    squaredAnisotropy 11 1 ≠ (Fintype.card D0.Omega8 : ℤ) ∧
      3 * (11 : ℤ) ^ 2 - centeredEdges 11 3 ≠
        (Fintype.card D0.Role : ℤ) ∧
      (10 : ℤ) ^ 3 - centeredTriangles 10 2 ≠ (D0.qT : ℤ) := by
  norm_num [squaredAnisotropy, centeredEdges, centeredTriangles,
    D0.qT, D0.Role, D0.Dyad, D0.Omega8, D0.Orient,
    D0.V11, D0.V9, D0.Witness]

/-- **Scene anisotropy-capacity weld (bundle).** -/
theorem scene_anisotropy_capacity_weld :
    (∀ m d : ℤ,
      squaredAnisotropy m d = 2 * d ^ 2 ∧
        3 * m ^ 2 - centeredEdges m d = d ^ 2 ∧
        m ^ 3 - centeredTriangles m d = m * d ^ 2) ∧
    squaredAnisotropy 11 2 = (Fintype.card D0.Omega8 : ℤ) ∧
    3 * (11 : ℤ) ^ 2 - centeredEdges 11 2 =
      (Fintype.card D0.Role : ℤ) ∧
    (11 : ℤ) ^ 3 - centeredTriangles 11 2 = (D0.qT : ℤ) ∧
    (∀ m d : ℤ, 0 ≤ d →
      3 * m ^ 2 - centeredEdges m d = (Fintype.card D0.Role : ℤ) →
      m ^ 3 - centeredTriangles m d = (D0.qT : ℤ) →
      (m - d, m, m + d) = ((9 : ℤ), 11, 13)) ∧
    (∀ a b c : ℕ,
      0 < a → a ≤ b → b ≤ c →
      D0.Synthesis.SceneInvariantReconstruction.edgeCount a b c = 359 →
      D0.Synthesis.SceneInvariantReconstruction.triangleCount a b c = 1287 →
      (a, b, c) = (9, 11, 13)) ∧
    centeredCubicDiscriminant 11 2 = 6185264 ∧
    centeredCubicDiscriminant 11 0 = 0 :=
  by
    refine ⟨centered_defect_identities, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
    · norm_num [squaredAnisotropy, D0.Omega8, D0.Role, D0.Dyad, D0.Orient]
    · norm_num [centeredEdges, D0.Role, D0.Dyad]
    · norm_num [centeredTriangles, D0.qT, D0.Role, D0.Dyad,
        D0.V11, D0.V9, D0.Omega8, D0.Orient, D0.Witness]
    · exact capacity_defects_reconstruct_scene
    · exact
        D0.Synthesis.SceneInvariantReconstruction.reconstruct_from_edges_triangles
    · exact scene_discriminant_weld.1
    · exact scene_discriminant_weld.2.2

end D0.Synthesis.SceneAnisotropyCapacityWeld
