import D0.SelfReading.TypedIncidenceCarriers
import D0.Matter.HyperchargeFlowLattice
import D0.Topology.TripartiteComplex
import D0.Topology.TypedTripartiteBoundaryRank
import Mathlib.Tactic

/-!
# D0-TYPED-SCENE-EULER-READING-001

This module adds the honest topological reading of the typed scene carriers.
It derives the clique-complex Euler characteristic directly from the explicit
typed vertex, edge, and triangle types:

```
χ = |TypedVertex| - |TypedEdge| + |TypedTriangle| = 961.
```

The same typed carriers also align with the already-owned graph cycle-rank
number `327`.  This gives the arithmetic complement

```
|TypedTriangle| - 327 = 960
```

and the Euler decomposition

```
χ = 1 - 0 + 960.
```

Euler arithmetic alone does not prove a Betti vector.  The load-bearing
homological step is supplied by `TypedTripartiteBoundaryRank`: explicit
oriented boundary matrices have ranks `rank ∂₁=32`, `rank ∂₂=327`.  This module
transports those matrices from canonical `Fin 9/11/13` representatives to the
owned typed capacity carriers `V9/V11/V13`, then proves the unconditional
Betti vector `(1,0,960)`.
-/

namespace D0.Topology.TypedSceneEulerReading

open D0.SelfReading.TypedCapacityRawScene
open D0.SelfReading.TypedIncidenceCarriers
open D0.Topology.TypedTripartiteBoundaryRank

/-! ## Transport of the canonical boundary matrices to owned capacity types -/

/-- Zone-preserving equivalence from the owned typed vertex carrier to the
canonical `Fin 9 ⊕ Fin 11 ⊕ Fin 13` chain carrier. -/
noncomputable def typedVertexEquivCanonical :
    TypedVertex ≃ Vertex where
  toFun
    | .zone9 x => Sum.inl (enum9 x)
    | .zone11 y => Sum.inr (Sum.inl (enum11 y))
    | .zone13 z => Sum.inr (Sum.inr (enum13 z))
  invFun
    | Sum.inl a => .zone9 (enum9.symm a)
    | Sum.inr (Sum.inl b) => .zone11 (enum11.symm b)
    | Sum.inr (Sum.inr c) => .zone13 (enum13.symm c)
  left_inv x := by cases x <;> simp
  right_inv x := by
    rcases x with x | x <;> rcases x with x | x <;> simp

/-- The owned typed edge carrier is equivalent to the canonical edge carrier. -/
noncomputable def typedEdgeEquivCanonical : TypedEdge ≃ Edge :=
  Equiv.sumCongr
    (Equiv.prodCongr enum9 enum11)
    (Equiv.sumCongr
      (Equiv.prodCongr enum9 enum13)
      (Equiv.prodCongr enum11 enum13))

/-- The owned typed triangle carrier is equivalent to the canonical triangle
carrier. -/
noncomputable def typedTriangleEquivCanonical :
    TypedTriangle ≃ Triangle :=
  Equiv.prodCongr enum9 (Equiv.prodCongr enum11 enum13)

/-- Typed `∂₁`, transported to `TypedVertex` and `TypedEdge`. -/
noncomputable def typedBoundary1 : Matrix TypedVertex TypedEdge ℚ :=
  Matrix.reindex
    typedVertexEquivCanonical.symm
    typedEdgeEquivCanonical.symm
    boundary1

/-- Typed `∂₂`, transported to `TypedEdge` and `TypedTriangle`. -/
noncomputable def typedBoundary2 : Matrix TypedEdge TypedTriangle ℚ :=
  Matrix.reindex
    typedEdgeEquivCanonical.symm
    typedTriangleEquivCanonical.symm
    boundary2

/-- Boundary nilpotency survives the type transport. -/
theorem typed_boundary_squared_zero :
    typedBoundary1 * typedBoundary2 = 0 := by
  unfold typedBoundary1 typedBoundary2
  change
    Matrix.reindexLinearEquiv ℚ ℚ
        typedVertexEquivCanonical.symm
        typedEdgeEquivCanonical.symm boundary1 *
      Matrix.reindexLinearEquiv ℚ ℚ
        typedEdgeEquivCanonical.symm
        typedTriangleEquivCanonical.symm boundary2 = 0
  rw [Matrix.reindexLinearEquiv_mul ℚ ℚ
    typedVertexEquivCanonical.symm
    typedEdgeEquivCanonical.symm
    typedTriangleEquivCanonical.symm boundary1 boundary2]
  rw [boundary_squared_zero]
  rfl

/-- Typed vertex-edge boundary rank. -/
theorem typed_boundary1_rank : typedBoundary1.rank = 32 := by
  unfold typedBoundary1
  rw [Matrix.rank_reindex]
  exact boundary1_rank

/-- Typed triangle-edge boundary rank. -/
theorem typed_boundary2_rank : typedBoundary2.rank = 327 := by
  unfold typedBoundary2
  rw [Matrix.rank_reindex]
  exact boundary2_rank

/-- The typed triangle boundaries exhaust the typed graph cycle space.  This is
the theorem-grade content behind `β₁=0`, not an Euler-characteristic inference. -/
theorem typed_boundary_exact :
    LinearMap.range typedBoundary2.mulVecLin =
      LinearMap.ker typedBoundary1.mulVecLin := by
  have hle :
      LinearMap.range typedBoundary2.mulVecLin ≤
        LinearMap.ker typedBoundary1.mulVecLin := by
    rw [LinearMap.range_le_ker_iff]
    rw [← Matrix.mulVecLin_mul, typed_boundary_squared_zero]
    exact Matrix.mulVecLin_zero
  have hrange2 :
      Module.finrank ℚ
        (LinearMap.range typedBoundary2.mulVecLin) = 327 := by
    simpa [Matrix.rank] using typed_boundary2_rank
  have hrange1 :
      Module.finrank ℚ
        (LinearMap.range typedBoundary1.mulVecLin) = 32 := by
    simpa [Matrix.rank] using typed_boundary1_rank
  have hrankNullity :=
    LinearMap.finrank_range_add_finrank_ker typedBoundary1.mulVecLin
  have hdomain :
      Module.finrank ℚ (TypedEdge → ℚ) = 359 := by
    rw [Module.finrank_fintype_fun_eq_card, typed_edge_cardinality]
  have hker1 :
      Module.finrank ℚ
        (LinearMap.ker typedBoundary1.mulVecLin) = 327 := by
    omega
  exact Submodule.eq_of_le_of_finrank_le hle (by omega)

/-- The top-cycle space has dimension `960`, so the top Betti number is an
actual kernel dimension. -/
theorem typed_boundary2_kernel_finrank :
    Module.finrank ℚ
      (LinearMap.ker typedBoundary2.mulVecLin) = 960 := by
  have hrange2 :
      Module.finrank ℚ
        (LinearMap.range typedBoundary2.mulVecLin) = 327 := by
    simpa [Matrix.rank] using typed_boundary2_rank
  have hrankNullity :=
    LinearMap.finrank_range_add_finrank_ker typedBoundary2.mulVecLin
  have hdomain :
      Module.finrank ℚ (TypedTriangle → ℚ) = 1287 := by
    rw [Module.finrank_fintype_fun_eq_card, typed_triangle_cardinality]
  omega

/-- The degree-zero quotient has dimension one. -/
theorem typed_boundary1_cokernel_finrank :
    Module.finrank ℚ
      ((TypedVertex → ℚ) ⧸ LinearMap.range typedBoundary1.mulVecLin) =
        1 := by
  have hrange1 :
      Module.finrank ℚ
        (LinearMap.range typedBoundary1.mulVecLin) = 32 := by
    simpa [Matrix.rank] using typed_boundary1_rank
  have hquot :=
    Submodule.finrank_quotient_add_finrank
      (LinearMap.range typedBoundary1.mulVecLin)
  have hdomain :
      Module.finrank ℚ (TypedVertex → ℚ) = 33 := by
    rw [Module.finrank_fintype_fun_eq_card, typed_cardinality]
  omega

/-- Boundaries viewed as a subspace of 1-cycles. -/
noncomputable def typedFirstHomologyBoundaries :
    Submodule ℚ (LinearMap.ker typedBoundary1.mulVecLin) :=
  (LinearMap.range typedBoundary2.mulVecLin).comap
    (LinearMap.ker typedBoundary1.mulVecLin).subtype

/-- Exactness makes every typed 1-cycle a boundary. -/
theorem typed_first_homology_boundaries_top :
    typedFirstHomologyBoundaries = ⊤ := by
  unfold typedFirstHomologyBoundaries
  rw [typed_boundary_exact]
  ext x
  simp

/-- Actual degree-one homology space. -/
noncomputable abbrev TypedFirstHomology :=
  (LinearMap.ker typedBoundary1.mulVecLin) ⧸
    typedFirstHomologyBoundaries

/-- The typed clique complex has no rational first homology. -/
theorem typed_first_homology_finrank :
    Module.finrank ℚ TypedFirstHomology = 0 := by
  unfold TypedFirstHomology
  rw [typed_first_homology_boundaries_top]
  have hquot :=
    Submodule.finrank_quotient_add_finrank
      (⊤ : Submodule ℚ
        (LinearMap.ker typedBoundary1.mulVecLin))
  have htop :
      Module.finrank ℚ
        (↥(⊤ : Submodule ℚ
          (LinearMap.ker typedBoundary1.mulVecLin))) =
        Module.finrank ℚ
          (LinearMap.ker typedBoundary1.mulVecLin) := by
    simp
  omega

/-- The actual rational homology ranks, using cokernel/quotient/kernel rather
than only the arithmetic rank-deficiency formulas. -/
theorem typed_homology_rank_vector :
    (Module.finrank ℚ
        ((TypedVertex → ℚ) ⧸
          LinearMap.range typedBoundary1.mulVecLin),
      Module.finrank ℚ TypedFirstHomology,
      Module.finrank ℚ
        (LinearMap.ker typedBoundary2.mulVecLin)) =
      (1, 0, 960) := by
  rw [typed_boundary1_cokernel_finrank,
    typed_first_homology_finrank,
    typed_boundary2_kernel_finrank]

/-- Euler characteristic generated by the three explicit typed face carriers. -/
def typedEulerCharacteristic : ℤ :=
  (Fintype.card TypedVertex : ℤ) -
    (Fintype.card TypedEdge : ℤ) +
    (Fintype.card TypedTriangle : ℤ)

/-- The typed clique-complex face carriers generate `χ = 961`. -/
theorem typed_euler_characteristic :
    typedEulerCharacteristic = 961 := by
  unfold typedEulerCharacteristic
  rw [typed_cardinality, typed_edge_cardinality,
    typed_triangle_cardinality]
  norm_num

/-- The graph first-cycle-space dimension read from the typed vertex and edge
carriers.  This is an arithmetic carrier readout; its graph-theoretic ownership
is aligned below with `D0-HYPERCHARGE-FLOW-LATTICE-001`. -/
def typedGraphCycleRank : ℕ :=
  Fintype.card TypedEdge - Fintype.card TypedVertex + 1

theorem typed_graph_cycle_rank :
    typedGraphCycleRank = 327 := by
  unfold typedGraphCycleRank
  rw [typed_edge_cardinality, typed_cardinality]

/-- Owner alignment: the typed-carrier cycle-rank readout equals the canonical
incidence-lattice owner, not a detached duplicate number. -/
theorem typed_graph_cycle_rank_aligns_owner :
    typedGraphCycleRank =
      D0.Matter.HyperchargeFlowLattice.cycleDim := by
  rw [typed_graph_cycle_rank,
    D0.Matter.HyperchargeFlowLattice.cycleDim_eq]

/-- Zeroth Betti number from the typed `∂₁` rank. -/
noncomputable def typedBeta0 : ℕ :=
  Fintype.card TypedVertex - typedBoundary1.rank

/-- First Betti number from the typed chain ranks. -/
noncomputable def typedBeta1 : ℕ :=
  Fintype.card TypedEdge - typedBoundary1.rank - typedBoundary2.rank

/-- Second Betti number from typed `∂₂` rank-nullity. -/
noncomputable def typedBeta2 : ℕ :=
  Fintype.card TypedTriangle - typedBoundary2.rank

theorem typed_beta0 : typedBeta0 = 1 := by
  unfold typedBeta0
  rw [typed_cardinality, typed_boundary1_rank]

theorem typed_beta1 : typedBeta1 = 0 := by
  unfold typedBeta1
  rw [typed_edge_cardinality, typed_boundary1_rank,
    typed_boundary2_rank]

theorem typed_beta2 : typedBeta2 = 960 := by
  unfold typedBeta2
  rw [typed_triangle_cardinality, typed_boundary2_rank]

/-- The typed clique-complex Betti vector. -/
theorem typed_betti_vector :
    (typedBeta0, typedBeta1, typedBeta2) = (1, 0, 960) := by
  rw [typed_beta0, typed_beta1, typed_beta2]

/-- Equivalent product reading of the same candidate, derived from the three
typed capacity cardinalities rather than inserted as `960`. -/
def typedReducedZoneProduct : ℕ :=
  (Fintype.card V9T - 1) *
    (Fintype.card V11T - 1) *
    (Fintype.card V13T - 1)

theorem typed_reduced_zone_product :
    typedReducedZoneProduct = 960 := by
  unfold typedReducedZoneProduct
  norm_num [D0.V9, D0.V11, D0.V13]

theorem top_candidate_equals_reduced_zone_product :
    typedBeta2 = typedReducedZoneProduct := by
  rw [typed_beta2, typed_reduced_zone_product]

/-- Euler-Poincaré for the typed finite clique complex. -/
theorem typed_euler_poincare :
    typedEulerCharacteristic =
      (typedBeta0 : ℤ) - typedBeta1 + typedBeta2 := by
  rw [typed_euler_characteristic, typed_beta0, typed_beta1, typed_beta2]
  norm_num

/-- The clique-complex dimension guardrail is inherited from the canonical
tripartite owner: four vertices cannot occupy four distinct parts, so there are
no 3-simplices in the three-part scene. -/
theorem typed_scene_has_no_three_simplices (a b c d : D0.Part) :
    ¬ D0.FourCliqueParts a b c d :=
  D0.no_three_simplices_K_9_11_13 a b c d

/-- Negative control: face counts and Euler arithmetic alone do not select the
Betti vector.  `(0,0,961)` has the same alternating sum as `(1,0,960)` but is a
different vector. -/
theorem euler_characteristic_alone_not_enough :
    ((0 : ℤ) - 0 + 961 = typedEulerCharacteristic) ∧
      ((0, 0, 961) : ℕ × ℕ × ℕ) ≠ (1, 0, 960) := by
  rw [typed_euler_characteristic]
  decide

/-- **Typed Euler reading bundle.** -/
theorem typed_scene_euler_reading :
    typedEulerCharacteristic = 961 ∧
    typedBoundary1 * typedBoundary2 = 0 ∧
    typedBoundary1.rank = 32 ∧
    typedBoundary2.rank = 327 ∧
    LinearMap.range typedBoundary2.mulVecLin =
      LinearMap.ker typedBoundary1.mulVecLin ∧
    Module.finrank ℚ
      (LinearMap.ker typedBoundary2.mulVecLin) = 960 ∧
    Module.finrank ℚ
      ((TypedVertex → ℚ) ⧸ LinearMap.range typedBoundary1.mulVecLin) =
        1 ∧
    (Module.finrank ℚ
        ((TypedVertex → ℚ) ⧸
          LinearMap.range typedBoundary1.mulVecLin),
      Module.finrank ℚ TypedFirstHomology,
      Module.finrank ℚ
        (LinearMap.ker typedBoundary2.mulVecLin)) =
      (1, 0, 960) ∧
    typedGraphCycleRank =
      D0.Matter.HyperchargeFlowLattice.cycleDim ∧
    (typedBeta0, typedBeta1, typedBeta2) = (1, 0, 960) ∧
    typedBeta2 = typedReducedZoneProduct ∧
    typedEulerCharacteristic =
      (typedBeta0 : ℤ) - typedBeta1 + typedBeta2 ∧
    ((0 : ℤ) - 0 + 961 = typedEulerCharacteristic) ∧
    ((0, 0, 961) : ℕ × ℕ × ℕ) ≠ (1, 0, 960) :=
  ⟨typed_euler_characteristic,
    typed_boundary_squared_zero,
    typed_boundary1_rank,
    typed_boundary2_rank,
    typed_boundary_exact,
    typed_boundary2_kernel_finrank,
    typed_boundary1_cokernel_finrank,
    typed_homology_rank_vector,
    typed_graph_cycle_rank_aligns_owner,
    typed_betti_vector,
    top_candidate_equals_reduced_zone_product,
    typed_euler_poincare,
    euler_characteristic_alone_not_enough.1,
    euler_characteristic_alone_not_enough.2⟩

end D0.Topology.TypedSceneEulerReading
