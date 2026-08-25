import D0.Synthesis.EquivariantSeamNoGo
import Mathlib.Tactic

/-!
# Equivariant carrier selection for the hypercharge row: three classes audited, two closed

The corpus owns the one-generation hypercharge row via the anomaly route
(`D0-SM-HYPERCHARGE-ROW-OWNER-001`: "SM is the nondegenerate t=-3a branch at a=1/6 →
(1/6,-2/3,1/3,-1/2,1)") — **five distinct rationals**. The map that would read this row off the
scene (`D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001`, PROOF-TARGET) has EXACT-MISSING: "a divergence-free
EdgeCurrent on K(9,11,13) whose zone-normalized U(1) holonomy trace YIELDS the hypercharge row".

This module proves the **counting-level carrier selection** behind that shape:

* `vertex_carrier_nogo` — an `Aut`-equivariant vertex function is zone-constant
  (`equivariant_zone_constant`), so its image has at most **3** values: it cannot contain the
  5-value row. *No equivariant vertex hypercharge exists.*
* `unoriented_edge_carrier_nogo` — an `Aut`-equivariant **symmetric** edge weight factors through
  unordered cross-zone pair classes: again at most **3** values on edges: same kill.
* `oriented_edge_image_card_le_six` — an `Aut`-equivariant **directed** edge function factors
  through ordered cross-zone pairs: at most **6** values, and the row's 5 values fit — the
  directed carrier **passes** the gate.

**Audited class scoping (post-skeptic 2026-08-02).** The selection is among the THREE audited
carrier classes {vertex, symmetric edge, directed edge}: the first two are theorem-closed, the
third passes. Counting alone does NOT make the directed current unique among all equivariant
carriers — e.g. ordered cross-zone triangles (6 orderings of the zones, image ≤ 6) and directed
2-paths (12 classes) also pass the same gate and are not audited here. What distinguishes the
directed edge current is that it is the PROOF-TARGET's own named EXACT-MISSING object (row
`D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001`), and the no-gos close the two coarser carriers below it.
Equivariance is the same class as `EquivariantSeamNoGo` (same-zone transpositions generate
`Aut = S₉×S₁₁×S₁₃`); orientation *between* zones is `Aut`-stable, which is why directed
currents escape.

**Ownership (cite, not re-mint).** The ≤ 6 bound is the operator-level face of the owned
"6 cross-part" `Aut` pair-orbit count (`D0-RAW-SCENE-GRAPH-001`: "3 diag + 3 same-part +
6 cross-part"); the vertex leg is the function-level corollary of the owned zone-indicator
minimality (`D0-P-INVARIANT-MINIMAL-001` / F7: the only `Aut`-invariant covectors are the three
zone indicators). This module contributes the carrier no-gos as composed statements, not the
counts.

**Two row conventions.** The 5-field anomaly row `(1/6, −2/3, 1/3, −1/2, 1)`
(`D0-SM-HYPERCHARGE-ROW-OWNER-001`) has 5 distinct values: gate passes with slack. The 6-field
left-Weyl convention adds `ν_R = 0` (`RoleHyperchargeReadout.Yrow`, row `D0-…-GRAPH-FLOW` batch):
6 distinct values (`hypercharge_row_six`) — the gate SATURATES, so under that reading a directed
equivariant carrier must be *injective* on the six ordered zone classes. Both readings recorded;
neither is chosen here.

**Scope honesty.** Counting-level only: this does not construct the current and does not claim
attainment. Candidate consumers (forward-looking, none cite this yet): rows 351/412, the
representation no-gos (479/487) — same externality pattern as the Dixmier necessity.
-/

namespace D0.Synthesis.EquivariantHyperchargeCarrier

open D0.Synthesis.EquivariantSeamNoGo
open D0.Spectral.DarkArchiveStructure

/-- Equivariance for vertex functions: invariance under every same-zone transposition. -/
def EquivariantVec (v : Fin 33 → ℚ) : Prop :=
  ∀ a b : Fin 33, zone a = zone b → ∀ u, v (Equiv.swap a b u) = v u

/-- An equivariant vertex function is constant on zones — delegation to the owned
`swap_fixed_zoneConstant` (`EquivariantSeamNoGo`), whose `hfix` hypothesis IS `EquivariantVec`. -/
theorem equivariant_zone_constant (v : Fin 33 → ℚ) (hv : EquivariantVec v) :
    ∀ u w : Fin 33, zone u = zone w → v u = v w :=
  fun u w huw => swap_fixed_zoneConstant v hv u w huw

/-- Zone labels of the three representatives. -/
theorem zone_reps :
    zone (0 : Fin 33) = 0 ∧ zone (9 : Fin 33) = 1 ∧ zone (20 : Fin 33) = 2 := by
  decide

/-- The image of an equivariant vertex function lies in the three representative values. -/
theorem vec_image_subset (v : Fin 33 → ℚ) (hv : EquivariantVec v) :
    Finset.univ.image v ⊆ ({v 0, v 9, v 20} : Finset ℚ) := by
  intro y hy
  obtain ⟨u, _, rfl⟩ := Finset.mem_image.mp hy
  have h3 : ∀ z : Fin 3, z = 0 ∨ z = 1 ∨ z = 2 := by decide
  have hz := equivariant_zone_constant v hv
  simp only [Finset.mem_insert, Finset.mem_singleton]
  rcases h3 (zone u) with h | h | h
  · exact Or.inl (hz u 0 (h.trans zone_reps.1.symm))
  · exact Or.inr (Or.inl (hz u 9 (h.trans zone_reps.2.1.symm)))
  · exact Or.inr (Or.inr (hz u 20 (h.trans zone_reps.2.2.symm)))

/-- An equivariant (matrix) edge function is constant on ordered cross-zone pair classes. -/
theorem equivariant_cross_constant (F : Fin 33 → Fin 33 → ℚ) (hF : Equivariant F) :
    ∀ i j i' j' : Fin 33, zone i = zone i' → zone j = zone j' → zone i ≠ zone j →
      F i j = F i' j' := by
  intro i j i' j' hii hjj hne
  have hji : j ≠ i := fun h => hne (congrArg zone h.symm)
  have hji' : j ≠ i' := fun h => hne (hii.trans (congrArg zone h).symm)
  have hi'j : i' ≠ j := fun h => hne (hii.trans (congrArg zone h))
  have hi'j' : i' ≠ j' := fun h => hne (hii.trans ((congrArg zone h).trans hjj.symm))
  have step1 : F i' j = F i j := by
    have h := hF i i' hii i j
    rw [Equiv.swap_apply_left, Equiv.swap_apply_of_ne_of_ne hji hji'] at h
    exact h
  have step2 : F i' j' = F i' j := by
    have h := hF j j' hjj i' j
    rw [Equiv.swap_apply_left, Equiv.swap_apply_of_ne_of_ne hi'j hi'j'] at h
    exact h
  rw [step2, step1]

/-- The cross-zone (edge) index set. -/
def crossPairs : Finset (Fin 33 × Fin 33) :=
  Finset.univ.filter (fun p => zone p.1 ≠ zone p.2)

/-- The image of an equivariant directed edge function over edges lies in six class values. -/
theorem oriented_image_subset (F : Fin 33 → Fin 33 → ℚ) (hF : Equivariant F) :
    crossPairs.image (fun p => F p.1 p.2)
      ⊆ ({F 0 9, F 0 20, F 9 0, F 9 20, F 20 0, F 20 9} : Finset ℚ) := by
  intro y hy
  obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp hy
  have hne : zone p.1 ≠ zone p.2 := (Finset.mem_filter.mp hp).2
  have h3 : ∀ z : Fin 3, z = 0 ∨ z = 1 ∨ z = 2 := by decide
  have hcc := equivariant_cross_constant F hF
  simp only [Finset.mem_insert, Finset.mem_singleton]
  rcases h3 (zone p.1) with h1 | h1 | h1 <;> rcases h3 (zone p.2) with h2 | h2 | h2
  · exact absurd (h1.trans h2.symm) hne
  · exact Or.inl (hcc p.1 p.2 0 9 (h1.trans zone_reps.1.symm) (h2.trans zone_reps.2.1.symm) hne)
  · exact Or.inr (Or.inl (hcc p.1 p.2 0 20 (h1.trans zone_reps.1.symm)
      (h2.trans zone_reps.2.2.symm) hne))
  · exact Or.inr (Or.inr (Or.inl (hcc p.1 p.2 9 0 (h1.trans zone_reps.2.1.symm)
      (h2.trans zone_reps.1.symm) hne)))
  · exact absurd (h1.trans h2.symm) hne
  · exact Or.inr (Or.inr (Or.inr (Or.inl (hcc p.1 p.2 9 20 (h1.trans zone_reps.2.1.symm)
      (h2.trans zone_reps.2.2.symm) hne))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl (hcc p.1 p.2 20 0
      (h1.trans zone_reps.2.2.symm) (h2.trans zone_reps.1.symm) hne)))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (hcc p.1 p.2 20 9
      (h1.trans zone_reps.2.2.symm) (h2.trans zone_reps.2.1.symm) hne)))))
  · exact absurd (h1.trans h2.symm) hne

/-- **The directed-carrier bound**: at most six values — the counting gate that the 5-value row
passes (`5 ≤ 6`). -/
theorem oriented_edge_image_card_le_six (F : Fin 33 → Fin 33 → ℚ) (hF : Equivariant F) :
    (crossPairs.image (fun p => F p.1 p.2)).card ≤ 6 := by
  refine le_trans (Finset.card_le_card (oriented_image_subset F hF)) ?_
  have c1 : ({F 20 9} : Finset ℚ).card = 1 := Finset.card_singleton _
  have c2 := Finset.card_insert_le (F 20 0) ({F 20 9} : Finset ℚ)
  have c3 := Finset.card_insert_le (F 9 20) ({F 20 0, F 20 9} : Finset ℚ)
  have c4 := Finset.card_insert_le (F 9 0) ({F 9 20, F 20 0, F 20 9} : Finset ℚ)
  have c5 := Finset.card_insert_le (F 0 20) ({F 9 0, F 9 20, F 20 0, F 20 9} : Finset ℚ)
  have c6 := Finset.card_insert_le (F 0 9)
    ({F 0 20, F 9 0, F 9 20, F 20 0, F 20 9} : Finset ℚ)
  omega

/-- A symmetric equivariant edge weight collapses to three values. -/
theorem symmetric_image_subset (F : Fin 33 → Fin 33 → ℚ) (hF : Equivariant F)
    (hsym : ∀ i j, F i j = F j i) :
    crossPairs.image (fun p => F p.1 p.2) ⊆ ({F 0 9, F 0 20, F 9 20} : Finset ℚ) := by
  intro y hy
  have h6 := oriented_image_subset F hF hy
  simp only [Finset.mem_insert, Finset.mem_singleton] at h6 ⊢
  rcases h6 with h | h | h | h | h | h
  · exact Or.inl h
  · exact Or.inr (Or.inl h)
  · exact Or.inl (h.trans (hsym 9 0))
  · exact Or.inr (Or.inr h)
  · exact Or.inr (Or.inl (h.trans (hsym 20 0)))
  · exact Or.inr (Or.inr (h.trans (hsym 20 9)))

/-- The 6-field (left-Weyl, with `ν_R = 0`) row has six distinct values: under that convention
the directed-carrier gate saturates. -/
theorem hypercharge_row_six :
    ({1/6, -2/3, 1/3, -1/2, 1, 0} : Finset ℚ).card = 6 := by
  have m0 : (1/6 : ℚ) ∉ ({-2/3, 1/3, -1/2, 1, 0} : Finset ℚ) := by
    simp only [Finset.mem_insert, Finset.mem_singleton]; norm_num
  have m1 : (-2/3 : ℚ) ∉ ({1/3, -1/2, 1, 0} : Finset ℚ) := by
    simp only [Finset.mem_insert, Finset.mem_singleton]; norm_num
  have m2 : (1/3 : ℚ) ∉ ({-1/2, 1, 0} : Finset ℚ) := by
    simp only [Finset.mem_insert, Finset.mem_singleton]; norm_num
  have m3 : (-1/2 : ℚ) ∉ ({1, 0} : Finset ℚ) := by
    simp only [Finset.mem_insert, Finset.mem_singleton]; norm_num
  have m4 : (1 : ℚ) ∉ ({0} : Finset ℚ) := by
    simp only [Finset.mem_singleton]; norm_num
  rw [Finset.card_insert_of_notMem m0, Finset.card_insert_of_notMem m1,
      Finset.card_insert_of_notMem m2, Finset.card_insert_of_notMem m3,
      Finset.card_insert_of_notMem m4, Finset.card_singleton]

/-- The owned hypercharge row has five distinct values. -/
theorem hypercharge_row_five :
    ({1/6, -2/3, 1/3, -1/2, 1} : Finset ℚ).card = 5 := by
  have m1 : (1/6 : ℚ) ∉ ({-2/3, 1/3, -1/2, 1} : Finset ℚ) := by
    simp only [Finset.mem_insert, Finset.mem_singleton]; norm_num
  have m2 : (-2/3 : ℚ) ∉ ({1/3, -1/2, 1} : Finset ℚ) := by
    simp only [Finset.mem_insert, Finset.mem_singleton]; norm_num
  have m3 : (1/3 : ℚ) ∉ ({-1/2, 1} : Finset ℚ) := by
    simp only [Finset.mem_insert, Finset.mem_singleton]; norm_num
  have m4 : (-1/2 : ℚ) ∉ ({1} : Finset ℚ) := by
    simp only [Finset.mem_singleton]; norm_num
  rw [Finset.card_insert_of_notMem m1, Finset.card_insert_of_notMem m2,
      Finset.card_insert_of_notMem m3, Finset.card_insert_of_notMem m4,
      Finset.card_singleton]

/-- **No-go: no equivariant vertex hypercharge.** The 5-value row cannot land in a ≤3-value
image. -/
theorem vertex_carrier_nogo (v : Fin 33 → ℚ) (hv : EquivariantVec v) :
    ¬ (({1/6, -2/3, 1/3, -1/2, 1} : Finset ℚ) ⊆ Finset.univ.image v) := by
  intro hsub
  have h5 := hypercharge_row_five
  have hrow := Finset.card_le_card hsub
  have himg := Finset.card_le_card (vec_image_subset v hv)
  have c1 : ({v 20} : Finset ℚ).card = 1 := Finset.card_singleton _
  have c2 := Finset.card_insert_le (v 9) ({v 20} : Finset ℚ)
  have c3 := Finset.card_insert_le (v 0) ({v 9, v 20} : Finset ℚ)
  omega

/-- **No-go: no equivariant symmetric edge hypercharge.** Undirected weights also cap at 3. -/
theorem unoriented_edge_carrier_nogo (F : Fin 33 → Fin 33 → ℚ) (hF : Equivariant F)
    (hsym : ∀ i j, F i j = F j i) :
    ¬ (({1/6, -2/3, 1/3, -1/2, 1} : Finset ℚ) ⊆ crossPairs.image (fun p => F p.1 p.2)) := by
  intro hsub
  have h5 := hypercharge_row_five
  have hrow := Finset.card_le_card hsub
  have himg := Finset.card_le_card (symmetric_image_subset F hF hsym)
  have c1 : ({F 9 20} : Finset ℚ).card = 1 := Finset.card_singleton _
  have c2 := Finset.card_insert_le (F 0 20) ({F 9 20} : Finset ℚ)
  have c3 := Finset.card_insert_le (F 0 9) ({F 0 20, F 9 20} : Finset ℚ)
  omega

/-- **Assembled carrier selection over the audited classes**: vertices and undirected edges are
closed; the directed edge carrier — the PROOF-TARGET's own EXACT-MISSING object — passes: the
row's own card (5, by `hypercharge_row_five`) is within the directed bound 6. -/
theorem carrier_selection :
    (∀ v, EquivariantVec v →
      ¬ (({1/6, -2/3, 1/3, -1/2, 1} : Finset ℚ) ⊆ Finset.univ.image v)) ∧
    (∀ F, Equivariant F → (∀ i j, F i j = F j i) →
      ¬ (({1/6, -2/3, 1/3, -1/2, 1} : Finset ℚ) ⊆ crossPairs.image (fun p => F p.1 p.2))) ∧
    (∀ F, Equivariant F → (crossPairs.image (fun p => F p.1 p.2)).card ≤ 6) ∧
    (({1/6, -2/3, 1/3, -1/2, 1} : Finset ℚ).card ≤ 6) :=
  ⟨vertex_carrier_nogo, unoriented_edge_carrier_nogo,
   oriented_edge_image_card_le_six, by rw [hypercharge_row_five]; omega⟩

end D0.Synthesis.EquivariantHyperchargeCarrier
