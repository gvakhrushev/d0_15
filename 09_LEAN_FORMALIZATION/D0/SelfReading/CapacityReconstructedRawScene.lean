import D0.SelfReading.RawSceneGraph
import D0.Synthesis.SceneAnisotropyCapacityWeld
import Mathlib.Tactic

/-!
# D0-CAPACITY-RECONSTRUCTED-RAW-SCENE-001

`D0.SelfReading.RawSceneGraph` correctly derives degrees, edge capacity,
`trace(A^2)`, and the pair-orbit commutant from a raw graph.  Its entry object,
however, still writes the partition thresholds `9` and `20` directly into
`lab : Fin 33 -> Fin 3`.

This module closes that provenance seam. The upstream finite capacities give

```
center = |V11| = 11
spread = |Dyad| = 2
(center-spread, center, center+spread) = (9,11,13)
```

and the anisotropy-capacity theorem proves that the pair
`(|ABCD|,qT)=(4,44)` uniquely reconstructs that center/spread. From these
capacities we build the cuts `9` and `9+11=20`, recover exactly the existing
raw part-label function and adjacency, and therefore inherit every existing raw
self-reading invariant without a second stipulated partition table.

Honest scope: the theorem composes already-owned capacity/cardinality and raw
graph owners. It does not derive the orbital complete-tripartite class anew,
does not create a new graph, and does not promote finite graph anisotropy to an
observed spacetime anisotropy.
-/

namespace D0.SelfReading.CapacityReconstructedRawScene

open D0.SelfReading.RawSceneGraph
open D0.Synthesis.SceneAnisotropyCapacityWeld

/-- Center of the three-zone ladder, derived from the `V11` capacity. -/
def capacityCenter : ℤ := Fintype.card (D0.V11 : Type)

/-- Half-spread of the three-zone ladder, derived from the dyad. -/
def capacitySpread : ℤ := Fintype.card (D0.Dyad : Type)

/-- Natural-number zone sizes used as cuts on `Fin 33`. -/
def innerSize : ℕ :=
  Fintype.card (D0.V11 : Type) - Fintype.card (D0.Dyad : Type)
def middleSize : ℕ := Fintype.card (D0.V11 : Type)
def outerSize : ℕ :=
  Fintype.card (D0.V11 : Type) + Fintype.card (D0.Dyad : Type)

/-- First and second cumulative cuts of the capacity-derived partition. -/
def firstCut : ℕ := innerSize
def secondCut : ℕ := innerSize + middleSize

/-- Part label built only from capacity-derived cuts. -/
def capacityLab (i : Fin 33) : Fin 3 :=
  if i.val < firstCut then 0 else if i.val < secondCut then 1 else 2

/-- Complete-tripartite adjacency built from the capacity label. -/
def capacityAdj (i j : Fin 33) : ℕ :=
  if capacityLab i = capacityLab j then 0 else 1

/-- Degree in the capacity-reconstructed graph. -/
def capacityDegree (i : Fin 33) : ℕ := ∑ j : Fin 33, capacityAdj i j

/-- Pair-orbit class in the capacity-reconstructed graph. -/
def capacityPairClass (p : Fin 33 × Fin 33) : Fin 3 × Fin 3 × Bool :=
  (capacityLab p.1, capacityLab p.2, decide (p.1 = p.2))

/-- Pair-orbit commutant dimension in the capacity-reconstructed graph. -/
def capacityCommutantDim : ℕ := (Finset.univ.image capacityPairClass).card

/-- **The capacity-defect pair reconstructs the centered zone sizes.** The
imported reverse theorem is load-bearing: `ABCD=4` fixes `d^2`, while `qT=44`
then fixes the center. -/
theorem capacity_pair_recovers_sizes :
    (capacityCenter - capacitySpread, capacityCenter,
      capacityCenter + capacitySpread) = ((9 : ℤ), 11, 13) := by
  apply capacity_defects_reconstruct_scene
  · norm_num [capacitySpread, D0.Dyad]
  · norm_num [capacityCenter, capacitySpread, centeredEdges,
      D0.Role, D0.Dyad, D0.V11, D0.V9, D0.Omega8,
      D0.Orient, D0.Witness]
  · norm_num [capacityCenter, capacitySpread, centeredTriangles,
      D0.qT, D0.Role, D0.Dyad, D0.V11, D0.V9, D0.Omega8,
      D0.Orient, D0.Witness]

/-- The natural capacity sizes and cumulative cuts are exactly
`(9,11,13; 9,20)`. -/
theorem capacity_sizes_and_cuts :
    (innerSize, middleSize, outerSize, firstCut, secondCut) =
      (9, 11, 13, 9, 20) := by
  norm_num [innerSize, middleSize, outerSize, firstCut, secondCut,
    D0.Dyad, D0.V11, D0.V9, D0.Omega8, D0.Role,
    D0.Orient, D0.Witness]

/-- **The capacity label is exactly the canonical raw-scene label.** -/
theorem capacityLab_eq_raw : capacityLab = lab := by
  native_decide

/-- **The capacity adjacency is exactly the canonical raw-scene adjacency.** -/
theorem capacityAdj_eq_raw : capacityAdj = Aadj := by
  native_decide

/-- Degrees are inherited from the canonical raw graph, rather than recomputed
from a detached numeric fixture. -/
theorem capacityDegree_eq_raw : capacityDegree = degree := by
  native_decide

/-- Pair classes and their commutant count are inherited from the same raw
graph. -/
theorem capacityPairClass_eq_raw : capacityPairClass = pairClass := by
  native_decide

theorem capacityCommutantDim_eq_raw : capacityCommutantDim = commutantDim := by
  native_decide

/-- Raw degree profile inherited through the capacity reconstruction. -/
theorem capacity_degree_profile :
    (∀ i : Fin 33, i.val < 9 → capacityDegree i = 24) ∧
      (∀ i : Fin 33, 9 ≤ i.val → i.val < 20 → capacityDegree i = 22) ∧
      (∀ i : Fin 33, 20 ≤ i.val → capacityDegree i = 20) := by
  rw [capacityDegree_eq_raw]
  exact ⟨degree_part0, degree_part1, degree_part2⟩

/-- The existing raw self-reading outputs now descend from capacity-derived
cuts and adjacency. -/
theorem capacity_raw_scene_invariants :
    (∑ i : Fin 33, capacityDegree i) = 718 ∧
      (∑ i : Fin 33, ∑ k : Fin 33, capacityAdj i k * capacityAdj k i) = 718 ∧
      capacityCommutantDim = 12 := by
  rw [capacityDegree_eq_raw, capacityAdj_eq_raw, capacityCommutantDim_eq_raw]
  exact ⟨two_edges, trace_A_sq, commutant_dim_raw⟩

/-- **Capacity-reconstructed raw self-reading graph (bundle).** -/
theorem capacity_reconstructed_raw_scene :
    (capacityCenter - capacitySpread, capacityCenter,
      capacityCenter + capacitySpread) = ((9 : ℤ), 11, 13) ∧
    capacityLab = lab ∧
    capacityAdj = Aadj ∧
    (∑ i : Fin 33, capacityDegree i) = 718 ∧
    (∑ i : Fin 33, ∑ k : Fin 33, capacityAdj i k * capacityAdj k i) = 718 ∧
    capacityCommutantDim = 12 :=
  ⟨capacity_pair_recovers_sizes, capacityLab_eq_raw, capacityAdj_eq_raw,
    capacity_raw_scene_invariants.1,
    capacity_raw_scene_invariants.2.1,
    capacity_raw_scene_invariants.2.2⟩

end D0.SelfReading.CapacityReconstructedRawScene
