import D0.Synthesis.SceneInvariantReconstruction
import D0.Topology.GenericTripartiteFiniteTypeTransport
import D0.Topology.GenericTripartiteHomology
import D0.Topology.TypedSceneEulerReading
import Mathlib.Tactic

/-!
# D0-CARRIER-TOPOLOGICAL-SCENE-PASSPORT-001

The incidence passport reconstructs `K(9,11,13)` from edge and triangle
carriers.  This module proves a genuinely different **mixed
carrier-topological** reverse route:

```
total vertex carrier + clique Euler characteristic
  -> ordered zone cardinalities (9,11,13).
```

For positive zone sizes the elementary identity

```
χ(K(a,b,c)) = 1 + (a-1)(b-1)(c-1)
```

is proved directly from the clique-complex f-vector.  Hence either

```
V = 33, χ = 961
```

or

```
V = 33, (a-1)(b-1)(c-1) = 960
```

uniquely reconstructs the ordered positive partition `(9,11,13)`.

The controls are load-bearing:

* `χ=961` or reduced product `960` alone is insufficient:
  `(9,9,16)` has both values but total vertex count `34`;
* positivity is required for the natural-subtraction product formula:
  the zero-zone example `(0,2,2)` breaks it.

Honest scope: `(V,χ)` is not a purely homotopy-topological passport because
`V` is a carrier cardinality and is not invariant under subdivision.  It is a
carrier-topological passport: one carrier coordinate plus one topological
coordinate.  The reduced-product route is its positive arithmetic
factorization.  The generic rational homology theorem now makes `(V,β₂)`
unconditional for canonical zones `Fin (p+1)`, `Fin (q+1)`, `Fin (r+1)`;
the finite-type transport theorem explicitly conjugates arbitrary natural
typed boundary complexes along `Fintype.equivFin`, so `(V,β₂)` is also
unconditional for arbitrary nonempty finite zones.
-/

namespace D0.Synthesis.CarrierTopologicalScenePassport

open D0.Synthesis.SceneInvariantReconstruction
open D0.SelfReading.TypedCapacityRawScene
open D0.SelfReading.TypedIncidenceCarriers
open D0.Topology.GenericTripartiteFiniteTypeTransport
open D0.Topology.GenericTripartiteHomology
open D0.Topology.TypedSceneEulerReading

/-- Reduced product of three positive zone cardinalities. -/
def reducedZoneProduct (a b c : ℕ) : ℕ :=
  (a - 1) * (b - 1) * (c - 1)

/-- Euler characteristic of the complete-tripartite clique complex, read from
its `0/1/2`-face counts. -/
def cliqueEuler (a b c : ℕ) : ℤ :=
  (vertexCount a b c : ℤ) -
    (edgeCount a b c : ℤ) +
    (triangleCount a b c : ℤ)

/-- Positive complete-tripartite Euler characteristic is one plus the reduced
zone product. -/
theorem clique_euler_eq_one_add_reduced_product
    (a b c : ℕ) (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :
    cliqueEuler a b c = 1 + reducedZoneProduct a b c := by
  have haeq : a = (a - 1) + 1 := by omega
  have hbeq : b = (b - 1) + 1 := by omega
  have hceq : c = (c - 1) + 1 := by omega
  rw [haeq, hbeq, hceq]
  simp [cliqueEuler, vertexCount, edgeCount, triangleCount,
    reducedZoneProduct]
  ring

/-- The source scene has topological coordinates `(V,χ,reduced)=(33,961,960)`. -/
theorem scene_topological_coordinates :
    vertexCount 9 11 13 = 33 ∧
      cliqueEuler 9 11 13 = 961 ∧
      reducedZoneProduct 9 11 13 = 960 := by
  norm_num [vertexCount, edgeCount, triangleCount, cliqueEuler,
    reducedZoneProduct]

/-- **Vertex count + reduced topological product reconstruct the scene.** -/
theorem reconstruct_from_vertices_reduced_product
    (a b c : ℕ)
    (ha : 0 < a) (hab : a ≤ b) (hbc : b ≤ c)
    (hV : vertexCount a b c = 33)
    (hB : reducedZoneProduct a b c = 960) :
    (a, b, c) = (9, 11, 13) := by
  simp only [vertexCount] at hV
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
  interval_cases a <;> interval_cases b <;>
    simp_all [reducedZoneProduct] <;> omega

/-- Abstract `β₂` form of the reverse theorem when a caller supplies its
identification with the reduced product.  The canonical `Fin` complex below
discharges this identification internally. -/
theorem reconstruct_from_vertices_beta2_if_join_formula
    (a b c beta2 : ℕ)
    (ha : 0 < a) (hab : a ≤ b) (hbc : b ≤ c)
    (hV : vertexCount a b c = 33)
    (hJoin : beta2 = reducedZoneProduct a b c)
    (hBeta2 : beta2 = 960) :
    (a, b, c) = (9, 11, 13) := by
  apply reconstruct_from_vertices_reduced_product a b c ha hab hbc hV
  omega

/-! ## Unconditional canonical rational-homology passport -/

/-- Actual rational top Betti number of the canonical complete-tripartite
complex with zone sizes `(p+1,q+1,r+1)`. -/
noncomputable def canonicalTopBetti (p q r : ℕ) : ℕ :=
  Module.finrank ℚ
    (LinearMap.ker
      (boundary2 (p := p) (q := q) (r := r)).mulVecLin)

/-- The generic chain-level theorem computes the canonical top Betti number. -/
theorem canonical_top_betti_formula (p q r : ℕ) :
    canonicalTopBetti p q r = p * q * r := by
  exact boundary2_kernel_finrank (p := p) (q := q) (r := r)

/-- **Unconditional `(V,β₂)` reverse passport for canonical finite zones.**
No join-homology formula is supplied as a hypothesis: `β₂` is the finrank of
the actual kernel of the proved generic boundary map. -/
theorem reconstruct_canonical_fin_from_vertex_beta2
    (p q r : ℕ)
    (hpq : p ≤ q) (hqr : q ≤ r)
    (hV : Fintype.card (GenericVertex p q r) = 33)
    (hBeta2 : canonicalTopBetti p q r = 960) :
    (Fintype.card (Fin (p + 1)),
      Fintype.card (Fin (q + 1)),
      Fintype.card (Fin (r + 1))) = (9, 11, 13) := by
  have hProduct : p * q * r = 960 := by
    rw [← canonical_top_betti_formula p q r]
    exact hBeta2
  have hReconstruct :=
    reconstruct_from_vertices_reduced_product
      (p + 1) (q + 1) (r + 1)
      (by omega) (by omega) (by omega)
      (by
        simpa [GenericVertex, vertexCount, add_assoc] using hV)
      (by
        simpa [reducedZoneProduct] using hProduct)
  simpa using hReconstruct

/-- The source scene supplies the canonical passport coordinates directly from
the generic chain complex. -/
theorem scene_canonical_vertex_beta2_coordinates :
    Fintype.card (GenericVertex 8 10 12) = 33 ∧
      canonicalTopBetti 8 10 12 = 960 := by
  constructor
  · norm_num [GenericVertex]
  · exact scene_top_homology_finrank

/-- **Vertex count + Euler characteristic reconstruct the scene.** -/
theorem reconstruct_from_vertices_euler
    (a b c : ℕ)
    (ha : 0 < a) (hab : a ≤ b) (hbc : b ≤ c)
    (hV : vertexCount a b c = 33)
    (hChi : cliqueEuler a b c = 961) :
    (a, b, c) = (9, 11, 13) := by
  have hbpos : 0 < b := lt_of_lt_of_le ha hab
  have hcpos : 0 < c := lt_of_lt_of_le hbpos hbc
  have hIdentity :=
    clique_euler_eq_one_add_reduced_product a b c ha hbpos hcpos
  rw [hChi] at hIdentity
  have hB : reducedZoneProduct a b c = 960 := by omega
  exact reconstruct_from_vertices_reduced_product
    a b c ha hab hbc hV hB

/-! ## Typed finite-carrier lift -/

/-- Generic three-zone vertex carrier with the same nesting convention as the
canonical boundary complex. -/
abbrev TripartiteVertex (A B C : Type) :=
  A ⊕ (B ⊕ C)

/-- Euler characteristic read directly from arbitrary finite typed carriers. -/
def typeCliqueEuler (A B C : Type)
    [Fintype A] [Fintype B] [Fintype C] : ℤ :=
  (Fintype.card (TripartiteVertex A B C) : ℤ) -
    (Fintype.card (TripartiteEdge A B C) : ℤ) +
    (Fintype.card (TripartiteTriangle A B C) : ℤ)

/-- Reduced product read directly from arbitrary finite typed carriers. -/
def typeReducedZoneProduct (A B C : Type)
    [Fintype A] [Fintype B] [Fintype C] : ℕ :=
  reducedZoneProduct
    (Fintype.card A) (Fintype.card B) (Fintype.card C)

theorem type_vertex_cardinality
    (A B C : Type) [Fintype A] [Fintype B] [Fintype C] :
    Fintype.card (TripartiteVertex A B C) =
      Fintype.card A + Fintype.card B + Fintype.card C := by
  simp [TripartiteVertex]
  omega

theorem type_clique_euler_formula
    (A B C : Type) [Fintype A] [Fintype B] [Fintype C] :
    typeCliqueEuler A B C =
      cliqueEuler
        (Fintype.card A) (Fintype.card B) (Fintype.card C) := by
  simp [typeCliqueEuler, cliqueEuler, vertexCount, edgeCount,
    triangleCount, TripartiteVertex]
  ring

/-- Generic finite-type Euler/product identity under nonemptiness. -/
theorem type_clique_euler_eq_one_add_reduced_product
    (A B C : Type) [Fintype A] [Fintype B] [Fintype C]
    (hA : 0 < Fintype.card A)
    (hB : 0 < Fintype.card B)
    (hC : 0 < Fintype.card C) :
    typeCliqueEuler A B C = 1 + typeReducedZoneProduct A B C := by
  rw [type_clique_euler_formula]
  exact clique_euler_eq_one_add_reduced_product
    (Fintype.card A) (Fintype.card B) (Fintype.card C) hA hB hC

/-- Universal finite-type reconstruction from total vertex cardinality and
clique Euler characteristic. -/
theorem reconstruct_type_cardinalities_from_vertex_euler
    (A B C : Type) [Fintype A] [Fintype B] [Fintype C]
    (hA : 0 < Fintype.card A)
    (hAB : Fintype.card A ≤ Fintype.card B)
    (hBC : Fintype.card B ≤ Fintype.card C)
    (hV : Fintype.card (TripartiteVertex A B C) = 33)
    (hChi : typeCliqueEuler A B C = 961) :
    (Fintype.card A, Fintype.card B, Fintype.card C) =
      (9, 11, 13) := by
  apply reconstruct_from_vertices_euler
  · exact hA
  · exact hAB
  · exact hBC
  · simpa only [vertexCount, type_vertex_cardinality, add_assoc] using hV
  · simpa [type_clique_euler_formula] using hChi

/-- Universal finite-type reconstruction from total vertex cardinality and
reduced topological product. -/
theorem reconstruct_type_cardinalities_from_vertex_reduced_product
    (A B C : Type) [Fintype A] [Fintype B] [Fintype C]
    (hA : 0 < Fintype.card A)
    (hAB : Fintype.card A ≤ Fintype.card B)
    (hBC : Fintype.card B ≤ Fintype.card C)
    (hV : Fintype.card (TripartiteVertex A B C) = 33)
    (hB : typeReducedZoneProduct A B C = 960) :
    (Fintype.card A, Fintype.card B, Fintype.card C) =
      (9, 11, 13) := by
  apply reconstruct_from_vertices_reduced_product
  · exact hA
  · exact hAB
  · exact hBC
  · simpa only [vertexCount, type_vertex_cardinality, add_assoc] using hV
  · exact hB

/-- Conditional finite-type `β₂` passport.  The caller must explicitly supply
the generic homology identification `β₂ = reducedZoneProduct`. -/
theorem reconstruct_type_cardinalities_from_vertex_beta2_if_join_formula
    (A B C : Type) [Fintype A] [Fintype B] [Fintype C]
    (beta2 : ℕ)
    (hA : 0 < Fintype.card A)
    (hAB : Fintype.card A ≤ Fintype.card B)
    (hBC : Fintype.card B ≤ Fintype.card C)
    (hV : Fintype.card (TripartiteVertex A B C) = 33)
    (hJoin : beta2 = typeReducedZoneProduct A B C)
    (hBeta2 : beta2 = 960) :
    (Fintype.card A, Fintype.card B, Fintype.card C) =
      (9, 11, 13) := by
  apply reconstruct_type_cardinalities_from_vertex_reduced_product
    A B C hA hAB hBC hV
  omega

/-- **Unconditional finite-type `(V,β₂)` passport.**  Here `β₂` is the
rational kernel dimension of the natural typed triangle boundary; its reduced
product formula is supplied by the proved finite-carrier conjugation theorem,
not by a caller hypothesis. -/
theorem reconstruct_type_cardinalities_from_vertex_beta2
    (A B C : Type) [Fintype A] [Fintype B] [Fintype C]
    [DecidableEq A] [DecidableEq B] [DecidableEq C]
    (hA : 0 < Fintype.card A)
    (hAB : Fintype.card A ≤ Fintype.card B)
    (hBC : Fintype.card B ≤ Fintype.card C)
    (hV : Fintype.card (TripartiteVertex A B C) = 33)
    (hBeta2 : finiteTypeTopBetti (A:=A) (B:=B) (C:=C) = 960) :
    (Fintype.card A, Fintype.card B, Fintype.card C) =
      (9, 11, 13) := by
  have hBpos : 0 < Fintype.card B := lt_of_lt_of_le hA hAB
  have hCpos : 0 < Fintype.card C := lt_of_lt_of_le hBpos hBC
  apply reconstruct_type_cardinalities_from_vertex_reduced_product
    A B C hA hAB hBC hV
  rw [finiteTypeTopBetti_formula hA hBpos hCpos] at hBeta2
  simpa [typeReducedZoneProduct, reducedZoneProduct] using hBeta2

/-- The owned source carriers satisfy the unconditional `(V,β₂)` coordinates
of the transported natural boundary complex. -/
theorem typed_source_vertex_beta2_coordinates :
    Fintype.card (TripartiteVertex V9T V11T V13T) = 33 ∧
      finiteTypeTopBetti (A:=V9T) (B:=V11T) (C:=V13T) = 960 := by
  constructor
  · simpa [TripartiteVertex] using typed_cardinality
  · rw [finiteTypeTopBetti_formula]
    · norm_num [D0.V9, D0.V11, D0.V13, D0.Omega8, D0.Role,
        D0.Dyad, D0.Orient, D0.Witness]
    · rw [D0.card_v9]
      norm_num
    · rw [D0.card_v11]
      norm_num
    · rw [D0.card_v13]
      norm_num

/-- Universal finite-type `(V,β₂)` reconstruction into the owned source
capacity carriers. -/
theorem typed_carrier_beta2_passport_universal :
    ∀ (A B C : Type) [Fintype A] [Fintype B] [Fintype C]
      [DecidableEq A] [DecidableEq B] [DecidableEq C],
      0 < Fintype.card A →
      Fintype.card A ≤ Fintype.card B →
      Fintype.card B ≤ Fintype.card C →
      Fintype.card (TripartiteVertex A B C) =
        Fintype.card TypedVertex →
      finiteTypeTopBetti (A:=A) (B:=B) (C:=C) = 960 →
      (Fintype.card A, Fintype.card B, Fintype.card C) =
        (Fintype.card V9T, Fintype.card V11T, Fintype.card V13T) := by
  intro A B C _ _ _ _ _ _ hA hAB hBC hV hBeta2
  rw [typed_cardinality] at hV
  calc
    (Fintype.card A, Fintype.card B, Fintype.card C) =
        (9, 11, 13) :=
      reconstruct_type_cardinalities_from_vertex_beta2
        A B C hA hAB hBC hV hBeta2
    _ =
        (Fintype.card V9T,
          Fintype.card V11T,
          Fintype.card V13T) := by
      symm
      exact typed_incidence_reconstructs_zone_capacities

/-- The carrier-topological passport returns the same owned source
capacities. -/
theorem typed_carrier_topological_passport_universal :
    ∀ (A B C : Type) [Fintype A] [Fintype B] [Fintype C],
      0 < Fintype.card A →
      Fintype.card A ≤ Fintype.card B →
      Fintype.card B ≤ Fintype.card C →
      Fintype.card (TripartiteVertex A B C) =
        Fintype.card TypedVertex →
      typeCliqueEuler A B C = typedEulerCharacteristic →
      (Fintype.card A, Fintype.card B, Fintype.card C) =
        (Fintype.card V9T, Fintype.card V11T, Fintype.card V13T) := by
  intro A B C _ _ _ hA hAB hBC hV hChi
  rw [typed_cardinality] at hV
  rw [typed_euler_characteristic] at hChi
  calc
    (Fintype.card A, Fintype.card B, Fintype.card C) =
        (9, 11, 13) :=
      reconstruct_type_cardinalities_from_vertex_euler
        A B C hA hAB hBC hV hChi
    _ =
        (Fintype.card V9T,
          Fintype.card V11T,
          Fintype.card V13T) := by
      symm
      exact typed_incidence_reconstructs_zone_capacities

/-! ## Destructive controls -/

/-- Euler characteristic or reduced product alone does not reconstruct the
scene: `(9,9,16)` has the same values `961/960` but total cardinality `34`. -/
theorem euler_alone_not_enough :
    cliqueEuler 9 9 16 = 961 ∧
      reducedZoneProduct 9 9 16 = 960 ∧
      (9, 9, 16) ≠ (9, 11, 13) := by
  norm_num [cliqueEuler, vertexCount, edgeCount, triangleCount,
    reducedZoneProduct]

/-- The total vertex coordinate is also individually insufficient. -/
theorem vertex_coordinate_alone_not_enough :
    vertexCount 8 11 14 = 33 ∧
      (8, 11, 14) ≠ (9, 11, 13) :=
  vertices_alone_not_enough

/-- Ordering is canonical gauge fixing: a nontrivial permutation preserves the
passport values but is not the chosen ordered representative. -/
theorem ordering_is_load_bearing :
    vertexCount 11 9 13 = 33 ∧
      cliqueEuler 11 9 13 = 961 ∧
      (11, 9, 13) ≠ (9, 11, 13) := by
  norm_num [cliqueEuler, vertexCount, edgeCount, triangleCount]

/-- Positivity is load-bearing because natural subtraction truncates at zero. -/
theorem positivity_is_load_bearing :
    cliqueEuler 0 2 2 ≠ 1 + reducedZoneProduct 0 2 2 := by
  norm_num [cliqueEuler, vertexCount, edgeCount, triangleCount,
    reducedZoneProduct]

/-- **Carrier-topological scene passport bundle.** -/
theorem carrier_topological_scene_passport :
    cliqueEuler 9 11 13 = 961 ∧
    reducedZoneProduct 9 11 13 = 960 ∧
    (∀ a b c : ℕ,
      0 < a → a ≤ b → b ≤ c →
      vertexCount a b c = 33 → cliqueEuler a b c = 961 →
      (a, b, c) = (9, 11, 13)) ∧
    (∀ a b c : ℕ,
      0 < a → a ≤ b → b ≤ c →
      vertexCount a b c = 33 → reducedZoneProduct a b c = 960 →
      (a, b, c) = (9, 11, 13)) ∧
    (cliqueEuler 9 9 16 = 961 ∧
      reducedZoneProduct 9 9 16 = 960 ∧
      (9, 9, 16) ≠ (9, 11, 13)) ∧
    (vertexCount 8 11 14 = 33 ∧
      (8, 11, 14) ≠ (9, 11, 13)) ∧
    (vertexCount 11 9 13 = 33 ∧
      cliqueEuler 11 9 13 = 961 ∧
      (11, 9, 13) ≠ (9, 11, 13)) ∧
    cliqueEuler 0 2 2 ≠ 1 + reducedZoneProduct 0 2 2 :=
  ⟨scene_topological_coordinates.2.1,
    scene_topological_coordinates.2.2,
    reconstruct_from_vertices_euler,
    reconstruct_from_vertices_reduced_product,
    euler_alone_not_enough,
    vertex_coordinate_alone_not_enough,
    ordering_is_load_bearing,
    positivity_is_load_bearing⟩

end D0.Synthesis.CarrierTopologicalScenePassport
