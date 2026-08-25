import D0.Combinatorics.Tripartite
import Mathlib.Tactic

/-!
# D0-SCENE-2OF3-INVARIANT-RECONSTRUCTION-001 — the scene is self-certifying

For an ordered positive complete-tripartite partition `(a,b,c)`, write

* `V = a+b+c` for the vertex count,
* `E = ab+ac+bc` for the edge count,
* `T = abc` for the triangle count.

The frozen scene `K(9,11,13)` has `(V,E,T) = (33,359,1287)`.  The new content
here is a **two-of-three reconstruction theorem**:

* `(V,E) = (33,359)` already forces `(a,b,c) = (9,11,13)`;
* `(V,T) = (33,1287)` already forces `(a,b,c) = (9,11,13)`;
* `(E,T) = (359,1287)` already forces `(a,b,c) = (9,11,13)`.

Thus the three raw scene counts form an internally redundant passport: any two
reconstruct the zone partition and determine the third.  This is stronger than
recomputing the three values from an already-given `(9,11,13)` partition.

The pairwise character is also minimal.  A single count is insufficient:
`(8,11,14)` has the same vertex count, `(7,10,17)` the same edge count, and
`(3,3,143)` the same triangle count.

Honest scope: this is a class-scoped reconstruction theorem for **ordered,
positive, complete tripartite** partitions.  It does not derive tripartiteness,
completeness, positivity, or the M1 admissibility of the scene; those are owned
by the carrier-forcing chain.  It adds an invariant checksum/self-reading
theorem once that class is fixed.
-/

namespace D0.Synthesis.SceneInvariantReconstruction

/-- Vertex count of a three-part partition. -/
def vertexCount (a b c : ℕ) : ℕ := a + b + c

/-- Edge count of the complete tripartite graph `K(a,b,c)`. -/
def edgeCount (a b c : ℕ) : ℕ := a * b + a * c + b * c

/-- Triangle count of the complete tripartite graph `K(a,b,c)`. -/
def triangleCount (a b c : ℕ) : ℕ := a * b * c

/-- The frozen scene has raw invariant passport `(V,E,T) = (33,359,1287)`. -/
theorem scene_passport :
    vertexCount 9 11 13 = 33 ∧
      edgeCount 9 11 13 = 359 ∧
      triangleCount 9 11 13 = 1287 := by
  exact ⟨D0.vertex_count_K_9_11_13,
    D0.edge_count_K_9_11_13,
    D0.triangle_count_K_9_11_13⟩

/-- **Owner alignment.** The local reconstruction coordinates are definitionally
the same three raw invariants owned by `D0.Combinatorics.Tripartite`; this prevents
the reverse theorem from floating on a duplicate, detached number table. -/
theorem canonical_owner_alignment :
    vertexCount 9 11 13 = D0.numVertices ∧
      edgeCount 9 11 13 = D0.numEdges ∧
      triangleCount 9 11 13 = D0.numTriangles := by
  norm_num [vertexCount, edgeCount, triangleCount,
    D0.numVertices, D0.numEdges, D0.numTriangles]

/-- **Vertices + edges reconstruct the partition.** -/
theorem reconstruct_from_vertices_edges
    (a b c : ℕ)
    (ha : 0 < a) (hab : a ≤ b) (hbc : b ≤ c)
    (hV : vertexCount a b c = 33)
    (hE : edgeCount a b c = 359) :
    (a, b, c) = (9, 11, 13) := by
  simp only [vertexCount] at hV
  simp only [edgeCount] at hE
  have ha11 : a ≤ 11 := by
    by_contra h
    have ha12 : 12 ≤ a := by omega
    have hb12 : 12 ≤ b := le_trans ha12 hab
    have hc12 : 12 ≤ c := le_trans hb12 hbc
    omega
  have hb16 : b ≤ 16 := by
    by_contra h
    have hb17 : 17 ≤ b := by omega
    have hc17 : 17 ≤ c := le_trans hb17 hbc
    omega
  interval_cases a <;> interval_cases b <;> simp_all <;> omega

/-- **Vertices + triangles reconstruct the partition.** -/
theorem reconstruct_from_vertices_triangles
    (a b c : ℕ)
    (ha : 0 < a) (hab : a ≤ b) (hbc : b ≤ c)
    (hV : vertexCount a b c = 33)
    (hT : triangleCount a b c = 1287) :
    (a, b, c) = (9, 11, 13) := by
  simp only [vertexCount] at hV
  simp only [triangleCount] at hT
  have ha11 : a ≤ 11 := by
    by_contra h
    have ha12 : 12 ≤ a := by omega
    have hb12 : 12 ≤ b := le_trans ha12 hab
    have hc12 : 12 ≤ c := le_trans hb12 hbc
    omega
  have hb16 : b ≤ 16 := by
    by_contra h
    have hb17 : 17 ≤ b := by omega
    have hc17 : 17 ≤ c := le_trans hb17 hbc
    omega
  interval_cases a <;> interval_cases b <;> simp_all <;> omega

/-- **Edges + triangles reconstruct the partition.** -/
theorem reconstruct_from_edges_triangles
    (a b c : ℕ)
    (ha : 0 < a) (hab : a ≤ b) (hbc : b ≤ c)
    (hE : edgeCount a b c = 359)
    (hT : triangleCount a b c = 1287) :
    (a, b, c) = (9, 11, 13) := by
  simp only [edgeCount] at hE
  simp only [triangleCount] at hT
  have hab_le : a * b ≤ 359 := by
    omega
  have hbc_le : b * c ≤ 359 := by
    omega
  have haa_le : a * a ≤ 359 := by
    exact le_trans (Nat.mul_le_mul_left a hab) hab_le
  have hbb_le : b * b ≤ 359 := by
    exact le_trans (Nat.mul_le_mul_left b hbc) hbc_le
  have ha18 : a ≤ 18 := by
    nlinarith
  have hb18 : b ≤ 18 := by
    nlinarith
  interval_cases a <;> interval_cases b <;> simp_all <;> omega

/-- **The rank-3 cubic coefficients are a lossless scene fingerprint.**
For a complete tripartite partition, the cubic `λ³ - E·λ - 2T` has
non-leading coefficients determined by the edge and triangle counts.  The D0
coefficients `(-359,-2574)` therefore reconstruct `(9,11,13)` without
separately supplying the vertex count. -/
theorem reconstruct_from_rank3_cubic_coefficients
    (a b c : ℕ)
    (ha : 0 < a) (hab : a ≤ b) (hbc : b ≤ c)
    (hLinear : edgeCount a b c = 359)
    (hConstant : 2 * triangleCount a b c = 2574) :
    (a, b, c) = (9, 11, 13) := by
  have hT : triangleCount a b c = 1287 := by
    omega
  exact reconstruct_from_edges_triangles a b c ha hab hbc hLinear hT

/-- One invariant alone is insufficient: the same vertex count admits a second
ordered positive partition. -/
theorem vertices_alone_not_enough :
    vertexCount 8 11 14 = 33 ∧ (8, 11, 14) ≠ (9, 11, 13) := by
  norm_num [vertexCount]

/-- One invariant alone is insufficient: the same edge count admits a second
ordered positive partition. -/
theorem edges_alone_not_enough :
    edgeCount 7 10 17 = 359 ∧ (7, 10, 17) ≠ (9, 11, 13) := by
  norm_num [edgeCount]

/-- One invariant alone is insufficient: the same triangle count admits a
second ordered positive partition. -/
theorem triangles_alone_not_enough :
    triangleCount 3 3 143 = 1287 ∧ (3, 3, 143) ≠ (9, 11, 13) := by
  norm_num [triangleCount]

/-- **Scene self-certification bundle.**  Every two-count passport reconstructs
the ordered positive partition, while each single count has a named second
object and is therefore insufficient. -/
theorem scene_two_of_three_self_certifying :
    (vertexCount 9 11 13 = D0.numVertices ∧
      edgeCount 9 11 13 = D0.numEdges ∧
      triangleCount 9 11 13 = D0.numTriangles) ∧
    (∀ a b c : ℕ,
      0 < a → a ≤ b → b ≤ c →
      vertexCount a b c = 33 → edgeCount a b c = 359 →
      (a, b, c) = (9, 11, 13)) ∧
    (∀ a b c : ℕ,
      0 < a → a ≤ b → b ≤ c →
      vertexCount a b c = 33 → triangleCount a b c = 1287 →
      (a, b, c) = (9, 11, 13)) ∧
    (∀ a b c : ℕ,
      0 < a → a ≤ b → b ≤ c →
      edgeCount a b c = 359 → triangleCount a b c = 1287 →
      (a, b, c) = (9, 11, 13)) ∧
    (∀ a b c : ℕ,
      0 < a → a ≤ b → b ≤ c →
      edgeCount a b c = 359 → 2 * triangleCount a b c = 2574 →
      (a, b, c) = (9, 11, 13)) ∧
    (vertexCount 8 11 14 = 33 ∧ (8, 11, 14) ≠ (9, 11, 13)) ∧
    (edgeCount 7 10 17 = 359 ∧ (7, 10, 17) ≠ (9, 11, 13)) ∧
    (triangleCount 3 3 143 = 1287 ∧ (3, 3, 143) ≠ (9, 11, 13)) :=
  ⟨canonical_owner_alignment,
    reconstruct_from_vertices_edges,
    reconstruct_from_vertices_triangles,
    reconstruct_from_edges_triangles,
    reconstruct_from_rank3_cubic_coefficients,
    vertices_alone_not_enough,
    edges_alone_not_enough,
    triangles_alone_not_enough⟩

end D0.Synthesis.SceneInvariantReconstruction
