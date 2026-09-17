import D0.Core.FiniteTypes
import D0.SelfReading.RawSceneGraph
import D0.Synthesis.SceneAnisotropyCapacityWeld
import Mathlib.Tactic

/-!
# D0-TYPED-CAPACITY-RAW-SCENE-001

The canonical raw self-reading owner is represented on `Fin 33`.  This module
constructs the same graph first on the typed capacity carrier

```
V9 ⊔ V11 ⊔ V13
```

with one constructor for each already-owned finite type.  The zone label is
therefore the constructor tag, not an integer threshold.  From that typed
object we derive:

* carrier cardinality `33`;
* degree profile `24^9, 22^11, 20^13`;
* `2|E| = 718`;
* `trace(A^2) = 718`;
* pair-orbit commutant dimension `12`.

An explicit block-preserving equivalence transports the typed carrier to
`Fin 33` and proves that its labels and adjacency agree with
`D0.SelfReading.RawSceneGraph`.

Honest scope: the internal `Fin 9/11/13` enumerations used to exhibit the
representation equivalence are arbitrary within each zone.  No theorem depends
on those within-zone names; only the constructor tags and cardinalities are
physical data.  Completeness/tripartiteness remains owned by `CarrierForcing`.
-/

namespace D0.SelfReading.TypedCapacityRawScene

open D0.SelfReading.RawSceneGraph
open D0.Synthesis.SceneAnisotropyCapacityWeld

abbrev V9T : Type := D0.V9
abbrev V11T : Type := D0.V11
abbrev V13T : Type := D0.V13

/-- Typed carrier: the zone is part of the type constructor. -/
inductive TypedVertex where
  | zone9 : V9T → TypedVertex
  | zone11 : V11T → TypedVertex
  | zone13 : V13T → TypedVertex
  deriving DecidableEq, Fintype

/-- Zone label read directly from the constructor, with no numeric cuts. -/
def typedZone : TypedVertex → Fin 3
  | .zone9 _ => 0
  | .zone11 _ => 1
  | .zone13 _ => 2

/-- Complete-tripartite adjacency on the typed carrier. -/
def typedAdj (i j : TypedVertex) : ℕ :=
  if typedZone i = typedZone j then 0 else 1

/-- Degree in the typed raw graph. -/
def typedDegree (i : TypedVertex) : ℕ :=
  ∑ j : TypedVertex, typedAdj i j

/-- Pair-orbit class in the typed graph. -/
def typedPairClass (p : TypedVertex × TypedVertex) :
    Fin 3 × Fin 3 × Bool :=
  (typedZone p.1, typedZone p.2, decide (p.1 = p.2))

/-- Pair-orbit commutant dimension in the typed graph. -/
def typedCommutantDim : ℕ :=
  (Finset.univ.image typedPairClass).card

/-- The typed carrier has the owned total capacity `9+11+13=33`. -/
theorem typed_cardinality : Fintype.card TypedVertex = 33 := by
  decide

/-- Typed degree profile, derived directly from constructor-tag adjacency. -/
theorem typed_degree_profile :
    (∀ x : V9T, typedDegree (.zone9 x) = 24) ∧
      (∀ x : V11T, typedDegree (.zone11 x) = 22) ∧
      (∀ x : V13T, typedDegree (.zone13 x) = 20) := by
  native_decide

/-- Raw edge capacity on the typed carrier. -/
theorem typed_two_edges : (∑ i : TypedVertex, typedDegree i) = 718 := by
  native_decide

/-- Raw adjacency-square trace on the typed carrier. -/
theorem typed_trace_A_sq :
    (∑ i : TypedVertex, ∑ k : TypedVertex,
      typedAdj i k * typedAdj k i) = 718 := by
  native_decide

/-- Raw pair-orbit commutant dimension on the typed carrier. -/
theorem typed_commutant_dim : typedCommutantDim = 12 := by
  native_decide

/-- The upstream capacity-defect passport reconstructs the same three
constructor cardinalities. -/
theorem capacity_pair_recovers_typed_sizes :
    ((Fintype.card V11T : ℤ) - (Fintype.card D0.Dyad : ℤ),
      (Fintype.card V11T : ℤ),
      (Fintype.card V11T : ℤ) + (Fintype.card D0.Dyad : ℤ)) =
        ((Fintype.card V9T : ℤ),
          (Fintype.card V11T : ℤ),
          (Fintype.card V13T : ℤ)) := by
  have h := capacity_defects_reconstruct_scene
    (Fintype.card V11T : ℤ) (Fintype.card D0.Dyad : ℤ)
    (by norm_num [D0.Dyad])
    (by
      norm_num [centeredEdges, D0.Role, D0.Dyad,
        D0.V11, D0.V9, D0.Omega8, D0.Orient, D0.Witness])
    (by
      norm_num [centeredTriangles, D0.qT, D0.Role, D0.Dyad,
        D0.V11, D0.V9, D0.Omega8, D0.Orient, D0.Witness])
  norm_num [D0.V9, D0.V11, D0.V13, D0.Dyad,
    D0.Omega8, D0.Role, D0.Orient, D0.Witness] at h ⊢

/-! ## Representation equivalence with the canonical `Fin 33` owner -/

noncomputable def enum9 : V9T ≃ Fin 9 :=
  Fintype.equivFinOfCardEq D0.card_v9

noncomputable def enum11 : V11T ≃ Fin 11 :=
  Fintype.equivFinOfCardEq D0.card_v11

noncomputable def enum13 : V13T ≃ Fin 13 :=
  Fintype.equivFinOfCardEq D0.card_v13

/-- Block-preserving representation map into `Fin 33`.  Within-zone
enumerations are arbitrary equivalences; offsets are forced by block
cardinalities. -/
noncomputable def typedToRaw : TypedVertex → Fin 33
  | .zone9 x =>
      ⟨(enum9 x).val, by have := (enum9 x).isLt; omega⟩
  | .zone11 x =>
      ⟨Fintype.card V9T + (enum11 x).val, by
        have h9 : Fintype.card V9T = 9 := D0.card_v9
        have h11 := (enum11 x).isLt
        omega⟩
  | .zone13 x =>
      ⟨Fintype.card V9T + Fintype.card V11T + (enum13 x).val, by
        have h9 : Fintype.card V9T = 9 := D0.card_v9
        have h11 : Fintype.card V11T = 11 := D0.card_v11
        have h13 := (enum13 x).isLt
        omega⟩

@[simp] theorem typedToRaw_zone9_val (x : V9T) :
    (typedToRaw (.zone9 x)).val = (enum9 x).val := rfl

@[simp] theorem typedToRaw_zone11_val (x : V11T) :
    (typedToRaw (.zone11 x)).val =
      Fintype.card V9T + (enum11 x).val := rfl

@[simp] theorem typedToRaw_zone13_val (x : V13T) :
    (typedToRaw (.zone13 x)).val =
      Fintype.card V9T + Fintype.card V11T + (enum13 x).val := rfl

theorem typedToRaw_injective : Function.Injective typedToRaw := by
  intro x y h
  cases x with
  | zone9 x =>
      cases y with
      | zone9 y =>
          congr 1
          apply enum9.injective
          apply Fin.ext
          have hv := congrArg Fin.val h
          simpa [typedToRaw] using hv
      | zone11 y =>
          have hv := congrArg Fin.val h
          have hx := (enum9 x).isLt
          simp [typedToRaw] at hv
          omega
      | zone13 y =>
          have hv := congrArg Fin.val h
          have hx := (enum9 x).isLt
          simp [typedToRaw] at hv
          omega
  | zone11 x =>
      cases y with
      | zone9 y =>
          have hv := congrArg Fin.val h
          have hy := (enum9 y).isLt
          simp [typedToRaw] at hv
          omega
      | zone11 y =>
          congr 1
          apply enum11.injective
          apply Fin.ext
          have hv := congrArg Fin.val h
          simpa [typedToRaw] using hv
      | zone13 y =>
          have hv := congrArg Fin.val h
          have hx := (enum11 x).isLt
          simp [typedToRaw] at hv
          omega
  | zone13 x =>
      cases y with
      | zone9 y =>
          have hv := congrArg Fin.val h
          have hy := (enum9 y).isLt
          simp [typedToRaw] at hv
          omega
      | zone11 y =>
          have hv := congrArg Fin.val h
          have hy := (enum11 y).isLt
          simp [typedToRaw] at hv
          omega
      | zone13 y =>
          congr 1
          apply enum13.injective
          apply Fin.ext
          have hv := congrArg Fin.val h
          simpa [typedToRaw] using hv

theorem typedToRaw_surjective : Function.Surjective typedToRaw := by
  intro i
  by_cases h9 : i.val < 9
  · let j : Fin 9 := ⟨i.val, h9⟩
    refine ⟨.zone9 (enum9.symm j), ?_⟩
    apply Fin.ext
    simp [typedToRaw, j]
  · by_cases h20 : i.val < 20
    · let j : Fin 11 := ⟨i.val - 9, by omega⟩
      refine ⟨.zone11 (enum11.symm j), ?_⟩
      apply Fin.ext
      simp [typedToRaw, j]
      omega
    · let j : Fin 13 := ⟨i.val - 20, by omega⟩
      refine ⟨.zone13 (enum13.symm j), ?_⟩
      apply Fin.ext
      simp [typedToRaw, j]
      omega

/-- Explicit equivalence from the typed capacity carrier to the canonical
`Fin 33` representation. -/
noncomputable def typedEquivRaw : TypedVertex ≃ Fin 33 :=
  Equiv.ofBijective typedToRaw
    ⟨typedToRaw_injective, typedToRaw_surjective⟩

/-- The representation equivalence preserves zone labels. -/
theorem lab_typedEquivRaw (x : TypedVertex) :
    lab (typedEquivRaw x) = typedZone x := by
  cases x with
  | zone9 x =>
      unfold typedEquivRaw
      unfold lab typedZone
      have hx := (enum9 x).isLt
      simp [Equiv.ofBijective, typedToRaw, hx]
  | zone11 x =>
      unfold typedEquivRaw
      unfold lab typedZone
      have hx := (enum11 x).isLt
      simp [Equiv.ofBijective, typedToRaw]
      omega
  | zone13 x =>
      unfold typedEquivRaw
      unfold lab typedZone
      have hx := (enum13 x).isLt
      simp [Equiv.ofBijective, typedToRaw]
      omega

/-- The representation equivalence preserves adjacency entrywise. -/
theorem adjacency_typedEquivRaw (i j : TypedVertex) :
    Aadj (typedEquivRaw i) (typedEquivRaw j) = typedAdj i j := by
  unfold Aadj typedAdj
  rw [lab_typedEquivRaw i, lab_typedEquivRaw j]

/-- **Universal within-zone gauge invariance.** Any equivalence preserving the
constructor tag preserves typed adjacency. This is stronger than checking one
chosen local enumeration. -/
theorem adjacency_invariant_under_zone_preserving_equiv
    (σ : TypedVertex ≃ TypedVertex)
    (hσ : ∀ x, typedZone (σ x) = typedZone x) :
    ∀ i j, typedAdj (σ i) (σ j) = typedAdj i j := by
  intro i j
  unfold typedAdj
  rw [hσ i, hσ j]

/-- Concrete corollary: arbitrary independent permutations inside the three
typed zones preserve the graph. -/
theorem adjacency_invariant_under_local_permutations
    (σ9 : V9T ≃ V9T) (σ11 : V11T ≃ V11T) (σ13 : V13T ≃ V13T) :
    ∀ i j,
      typedAdj
        (match i with
          | .zone9 x => .zone9 (σ9 x)
          | .zone11 x => .zone11 (σ11 x)
          | .zone13 x => .zone13 (σ13 x))
        (match j with
          | .zone9 x => .zone9 (σ9 x)
          | .zone11 x => .zone11 (σ11 x)
          | .zone13 x => .zone13 (σ13 x)) =
      typedAdj i j := by
  intro i j
  cases i <;> cases j <;> rfl

/-- **Typed raw scene (bundle).** -/
theorem typed_capacity_raw_scene :
    Fintype.card TypedVertex = 33 ∧
    (∀ x : V9T, typedDegree (.zone9 x) = 24) ∧
    (∀ x : V11T, typedDegree (.zone11 x) = 22) ∧
    (∀ x : V13T, typedDegree (.zone13 x) = 20) ∧
    (∑ i : TypedVertex, typedDegree i) = 718 ∧
    (∑ i : TypedVertex, ∑ k : TypedVertex,
      typedAdj i k * typedAdj k i) = 718 ∧
    typedCommutantDim = 12 ∧
    (∀ x : TypedVertex, lab (typedEquivRaw x) = typedZone x) ∧
    (∀ i j : TypedVertex,
      Aadj (typedEquivRaw i) (typedEquivRaw j) = typedAdj i j) ∧
    (∀ (σ : TypedVertex ≃ TypedVertex),
      (∀ x, typedZone (σ x) = typedZone x) →
      ∀ i j, typedAdj (σ i) (σ j) = typedAdj i j) :=
  ⟨typed_cardinality,
    typed_degree_profile.1,
    typed_degree_profile.2.1,
    typed_degree_profile.2.2,
    typed_two_edges,
    typed_trace_A_sq,
    typed_commutant_dim,
    lab_typedEquivRaw,
    adjacency_typedEquivRaw,
    adjacency_invariant_under_zone_preserving_equiv⟩

end D0.SelfReading.TypedCapacityRawScene
