import D0.SelfReading.TypedCapacityRawScene
import D0.Synthesis.SceneInvariantReconstruction
import Mathlib.Tactic

/-!
# D0-TYPED-INCIDENCE-CARRIERS-001

This module replaces the bare scene counts `359`, `718`, and `1287` by
explicit finite types.

For any finite types `A,B,C`:

```
TripartiteEdge A B C
  = (A x B) + (A x C) + (B x C)

OrientedTripartiteEdge A B C
  = TripartiteEdge A B C x Bool

TripartiteTriangle A B C
  = A x B x C.
```

Their cardinalities are therefore the elementary symmetric functions used by
the scene cubic.  For `(A,B,C)=(V9,V11,V13)` they are exactly
`359`, `718`, and `1287`.

The module also identifies these carriers with the support of typed adjacency:

* undirected edges are ordered-zone vertex pairs;
* directed edges are adjacent ordered vertex pairs;
* triangles are increasing-zone vertex triples.

Finally, a generic reverse theorem shows that finite type cardinalities are
reconstructed as `(9,11,13)` whenever their typed edge and triangle carriers
have cardinalities `359` and `1287`.

Honest scope: `OrientedTripartiteEdge` is the finite support of directed scene
edges. It is not the same object as a gauge connection or a selected physical
edge holonomy. This module supplies carrier provenance only.
-/

namespace D0.SelfReading.TypedIncidenceCarriers

open D0.SelfReading.TypedCapacityRawScene
open D0.Synthesis.SceneInvariantReconstruction

/-- Generic undirected complete-tripartite edge carrier. -/
abbrev TripartiteEdge (A B C : Type) :=
  (A × B) ⊕ ((A × C) ⊕ (B × C))

/-- Generic directed-edge carrier: one orientation bit per undirected edge. -/
abbrev OrientedTripartiteEdge (A B C : Type) :=
  TripartiteEdge A B C × Bool

/-- Generic triangle carrier: one vertex from every zone. -/
abbrev TripartiteTriangle (A B C : Type) :=
  A × B × C

theorem tripartite_edge_cardinality
    (A B C : Type) [Fintype A] [Fintype B] [Fintype C] :
    Fintype.card (TripartiteEdge A B C) =
      Fintype.card A * Fintype.card B +
      Fintype.card A * Fintype.card C +
      Fintype.card B * Fintype.card C := by
  simp [TripartiteEdge]
  omega

theorem oriented_tripartite_edge_cardinality
    (A B C : Type) [Fintype A] [Fintype B] [Fintype C] :
    Fintype.card (OrientedTripartiteEdge A B C) =
      2 * Fintype.card (TripartiteEdge A B C) := by
  simp [OrientedTripartiteEdge]
  omega

theorem tripartite_triangle_cardinality
    (A B C : Type) [Fintype A] [Fintype B] [Fintype C] :
    Fintype.card (TripartiteTriangle A B C) =
      Fintype.card A * Fintype.card B * Fintype.card C := by
  simp [TripartiteTriangle, Nat.mul_assoc]

/-- **Generic reverse reconstruction from typed carriers.** -/
theorem reconstruct_type_cardinalities_from_incidence
    (A B C : Type) [Fintype A] [Fintype B] [Fintype C]
    (hA : 0 < Fintype.card A)
    (hAB : Fintype.card A ≤ Fintype.card B)
    (hBC : Fintype.card B ≤ Fintype.card C)
    (hE : Fintype.card (TripartiteEdge A B C) = 359)
    (hT : Fintype.card (TripartiteTriangle A B C) = 1287) :
    (Fintype.card A, Fintype.card B, Fintype.card C) = (9, 11, 13) := by
  apply reconstruct_from_edges_triangles
  · exact hA
  · exact hAB
  · exact hBC
  · rw [← hE]
    simp [edgeCount, TripartiteEdge]
    omega
  · rw [← hT]
    simp [triangleCount, TripartiteTriangle, Nat.mul_assoc]

/-! ## D0 scene instance -/

abbrev TypedEdge :=
  TripartiteEdge V9T V11T V13T

abbrev TypedDirectedEdge :=
  OrientedTripartiteEdge V9T V11T V13T

abbrev TypedTriangle :=
  TripartiteTriangle V9T V11T V13T

theorem typed_edge_cardinality : Fintype.card TypedEdge = 359 := by
  rw [tripartite_edge_cardinality]
  norm_num [D0.V9, D0.V11, D0.V13, D0.Omega8, D0.Role,
    D0.Dyad, D0.Orient, D0.Witness]

theorem typed_directed_edge_cardinality :
    Fintype.card TypedDirectedEdge = 718 := by
  rw [oriented_tripartite_edge_cardinality, typed_edge_cardinality]

theorem typed_triangle_cardinality :
    Fintype.card TypedTriangle = 1287 := by
  rw [tripartite_triangle_cardinality]
  norm_num [D0.V9, D0.V11, D0.V13, D0.Omega8, D0.Role,
    D0.Dyad, D0.Orient, D0.Witness]

theorem typed_incidence_reconstructs_zone_capacities :
    (Fintype.card V9T, Fintype.card V11T, Fintype.card V13T) =
      (9, 11, 13) := by
  change
    (Fintype.card D0.V9, Fintype.card D0.V11, Fintype.card D0.V13) =
      (9, 11, 13)
  rw [D0.card_v9, D0.card_v11, D0.card_v13]

/-- **One incidence carrier alone is insufficient.** A different typed
partition `(Fin 7, Fin 10, Fin 17)` has the same edge and directed-edge
cardinalities. -/
theorem edge_carrier_alone_not_enough :
    Fintype.card (TripartiteEdge (Fin 7) (Fin 10) (Fin 17)) = 359 ∧
      Fintype.card
        (OrientedTripartiteEdge (Fin 7) (Fin 10) (Fin 17)) = 718 ∧
      ((7, 10, 17) : ℕ × ℕ × ℕ) ≠ (9, 11, 13) := by
  native_decide

/-- A different typed partition `(Fin 1, Fin 3, Fin 429)` has the same
triangle-carrier cardinality. -/
theorem triangle_carrier_alone_not_enough :
    Fintype.card (TripartiteTriangle (Fin 1) (Fin 3) (Fin 429)) =
        1287 ∧
      ((1, 3, 429) : ℕ × ℕ × ℕ) ≠ (9, 11, 13) := by
  native_decide

/-! ## Incidence support inside the typed raw graph -/

/-- Endpoints of a canonical undirected typed edge, ordered by zone. -/
def edgeEndpoints : TypedEdge → TypedVertex × TypedVertex
  | Sum.inl (x, y) => (.zone9 x, .zone11 y)
  | Sum.inr (Sum.inl (x, z)) => (.zone9 x, .zone13 z)
  | Sum.inr (Sum.inr (y, z)) => (.zone11 y, .zone13 z)

/-- Endpoints of an oriented typed edge. `false` is canonical orientation;
`true` reverses it. -/
def directedEndpoints : TypedDirectedEdge → TypedVertex × TypedVertex
  | (e, false) => edgeEndpoints e
  | (e, true) => (edgeEndpoints e).swap

/-- Vertices of a typed triangle, ordered by zone. -/
def triangleVertices :
    TypedTriangle → TypedVertex × TypedVertex × TypedVertex
  | (x, y, z) => (.zone9 x, .zone11 y, .zone13 z)

/-- Undirected adjacency support, represented once with increasing zone tag. -/
abbrev EdgeSupport :=
  {p : TypedVertex × TypedVertex // typedZone p.1 < typedZone p.2}

/-- Directed adjacency support. -/
abbrev DirectedEdgeSupport :=
  {p : TypedVertex × TypedVertex // typedAdj p.1 p.2 = 1}

/-- Ordered triangle support. -/
abbrev TriangleSupport :=
  {p : TypedVertex × TypedVertex × TypedVertex //
    typedZone p.1 < typedZone p.2.1 ∧
    typedZone p.2.1 < typedZone p.2.2}

def edgeToSupport : TypedEdge → EdgeSupport
  | Sum.inl (x, y) =>
      ⟨(.zone9 x, .zone11 y), by simp [typedZone]⟩
  | Sum.inr (Sum.inl (x, z)) =>
      ⟨(.zone9 x, .zone13 z), by simp [typedZone]⟩
  | Sum.inr (Sum.inr (y, z)) =>
      ⟨(.zone11 y, .zone13 z), by simp [typedZone]⟩

def directedEdgeToSupport : TypedDirectedEdge → DirectedEdgeSupport
  | (Sum.inl (x, y), false) =>
      ⟨(.zone9 x, .zone11 y), by rfl⟩
  | (Sum.inl (x, y), true) =>
      ⟨(.zone11 y, .zone9 x), by rfl⟩
  | (Sum.inr (Sum.inl (x, z)), false) =>
      ⟨(.zone9 x, .zone13 z), by rfl⟩
  | (Sum.inr (Sum.inl (x, z)), true) =>
      ⟨(.zone13 z, .zone9 x), by rfl⟩
  | (Sum.inr (Sum.inr (y, z)), false) =>
      ⟨(.zone11 y, .zone13 z), by rfl⟩
  | (Sum.inr (Sum.inr (y, z)), true) =>
      ⟨(.zone13 z, .zone11 y), by rfl⟩

def triangleToSupport : TypedTriangle → TriangleSupport
  | (x, y, z) =>
      ⟨(.zone9 x, .zone11 y, .zone13 z), by simp [typedZone]⟩

theorem edgeToSupport_injective : Function.Injective edgeToSupport := by
  intro e f h
  cases e <;> cases f <;> simp [edgeToSupport] at h ⊢ <;> aesop

theorem directedEdgeToSupport_injective :
    Function.Injective directedEdgeToSupport := by
  intro e f h
  rcases e with ⟨e, o⟩
  rcases f with ⟨f, p⟩
  cases e <;> cases f <;> cases o <;> cases p <;>
    simp [directedEdgeToSupport] at h ⊢ <;> aesop

theorem triangleToSupport_injective :
    Function.Injective triangleToSupport := by
  intro e f h
  rcases e with ⟨x, y, z⟩
  rcases f with ⟨x', y', z'⟩
  simp [triangleToSupport] at h ⊢
  aesop

theorem edge_support_cardinality : Fintype.card EdgeSupport = 359 := by
  native_decide

theorem directed_edge_support_cardinality :
    Fintype.card DirectedEdgeSupport = 718 := by
  native_decide

theorem triangle_support_cardinality :
    Fintype.card TriangleSupport = 1287 := by
  native_decide

noncomputable def edgeEquivSupport : TypedEdge ≃ EdgeSupport :=
  Equiv.ofBijective edgeToSupport
    ((Fintype.bijective_iff_injective_and_card edgeToSupport).2
      ⟨edgeToSupport_injective, by native_decide⟩)

noncomputable def directedEdgeEquivSupport :
    TypedDirectedEdge ≃ DirectedEdgeSupport :=
  Equiv.ofBijective directedEdgeToSupport
    ((Fintype.bijective_iff_injective_and_card directedEdgeToSupport).2
      ⟨directedEdgeToSupport_injective, by native_decide⟩)

noncomputable def triangleEquivSupport :
    TypedTriangle ≃ TriangleSupport :=
  Equiv.ofBijective triangleToSupport
    ((Fintype.bijective_iff_injective_and_card triangleToSupport).2
      ⟨triangleToSupport_injective, by native_decide⟩)

/-- **Typed incidence carriers (bundle).** -/
theorem typed_incidence_carriers :
    Fintype.card TypedEdge = 359 ∧
    Fintype.card TypedDirectedEdge = 718 ∧
    Fintype.card TypedTriangle = 1287 ∧
    Fintype.card EdgeSupport = 359 ∧
    Fintype.card DirectedEdgeSupport = 718 ∧
    Fintype.card TriangleSupport = 1287 ∧
    (Fintype.card V9T, Fintype.card V11T, Fintype.card V13T) =
      (9, 11, 13) ∧
    Fintype.card (TripartiteEdge (Fin 7) (Fin 10) (Fin 17)) = 359 ∧
    Fintype.card (TripartiteTriangle (Fin 1) (Fin 3) (Fin 429)) =
      1287 :=
  ⟨typed_edge_cardinality,
    typed_directed_edge_cardinality,
    typed_triangle_cardinality,
    edge_support_cardinality,
    directed_edge_support_cardinality,
    triangle_support_cardinality,
    typed_incidence_reconstructs_zone_capacities,
    edge_carrier_alone_not_enough.1,
    triangle_carrier_alone_not_enough.1⟩

end D0.SelfReading.TypedIncidenceCarriers
