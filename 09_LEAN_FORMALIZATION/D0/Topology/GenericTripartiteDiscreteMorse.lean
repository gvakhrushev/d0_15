import D0.Topology.GenericTripartiteAbstractComplex
import D0.Topology.GenericTripartiteTopHomologyRing
import Mathlib.Logic.Relation
import Mathlib.Tactic

/-!
# D0-GENERIC-TRIPARTITE-DISCRETE-MORSE-001

A canonical root-lexicographic discrete Morse matching is constructed on the
actual face carrier of `K(p+1,q+1,r+1)`.  It adds the first available root
vertex in zone order and proves:

* every matched pair is a genuine codimension-one inclusion of faces;
* the upper/lower pairing maps are inverse on matched faces;
* the only critical cells are the root vertex and the all-nonroot triangles;
* those critical 2-cells are indexed by the same
  `Fin p × Fin q × Fin r` type as the octahedral top-homology basis;
* every Forman `V`-path strictly decreases an explicit finite rank, so the
  matching is acyclic.

For the source scene this gives exactly one critical 0-cell, no critical
1-cells, and `960` critical 2-cells.  A standard discrete Morse realization
theorem would therefore yield a wedge of `960` two-spheres.  That final
realization theorem is not presently available in Mathlib and is deliberately
not asserted here.
-/

namespace D0.Topology.GenericTripartiteDiscreteMorse
open D0.Topology.GenericTripartiteHomology
open D0.Topology.GenericTripartiteTopHomologyRing

variable {p q r : ℕ}

open D0.Topology.GenericTripartiteAbstractComplex

namespace Face

/-- Distinguished critical root vertex in the first zone. -/
def root : Face p q r := .vertex (Sum.inl 0)

/-- Face dimension. -/
def dimension : Face p q r → ℕ
  | .vertex _ => 0
  | .edge _ => 1
  | .triangle _ => 2

/-- Codimension-one face relation. -/
def CodimOne : Face p q r → Face p q r → Prop
  | .vertex (Sum.inl a), .edge (Sum.inl (a',_)) => a = a'
  | .vertex (Sum.inl a), .edge (Sum.inr (Sum.inl (a',_))) => a = a'
  | .vertex (Sum.inl _), .edge (Sum.inr (Sum.inr _)) => False
  | .vertex (Sum.inr (Sum.inl b)), .edge (Sum.inl (_,b')) => b = b'
  | .vertex (Sum.inr (Sum.inl _)), .edge (Sum.inr (Sum.inl _)) => False
  | .vertex (Sum.inr (Sum.inl b)), .edge (Sum.inr (Sum.inr (b',_))) => b = b'
  | .vertex (Sum.inr (Sum.inr _)), .edge (Sum.inl _) => False
  | .vertex (Sum.inr (Sum.inr c)), .edge (Sum.inr (Sum.inl (_,c'))) => c = c'
  | .vertex (Sum.inr (Sum.inr c)), .edge (Sum.inr (Sum.inr (_,c'))) => c = c'
  | .edge (Sum.inl (a,b)), .triangle (a',b',_) => a = a' ∧ b = b'
  | .edge (Sum.inr (Sum.inl (a,c))), .triangle (a',_,c') => a = a' ∧ c = c'
  | .edge (Sum.inr (Sum.inr (b,c))), .triangle (_,b',c') => b = b' ∧ c = c'
  | _, _ => False

/-- Root-lexicographic matching: first add `A₀`, then `B₀`, then `C₀`. -/
def pairUpper : Face p q r → Option (Face p q r)
  | .vertex (Sum.inl a) =>
      if a = 0 then none else some (.edge (Sum.inl (a,0)))
  | .vertex (Sum.inr (Sum.inl b)) =>
      some (.edge (Sum.inl (0,b)))
  | .vertex (Sum.inr (Sum.inr c)) =>
      some (.edge (Sum.inr (Sum.inl (0,c))))
  | .edge (Sum.inl (a,b)) =>
      if a = 0 ∨ b = 0 then none else some (.triangle (a,b,0))
  | .edge (Sum.inr (Sum.inl (a,c))) =>
      if a = 0 then none else some (.triangle (a,0,c))
  | .edge (Sum.inr (Sum.inr (b,c))) =>
      some (.triangle (0,b,c))
  | .triangle _ => none

/-- Inverse matching on upper faces. -/
def pairLower : Face p q r → Option (Face p q r)
  | .vertex _ => none
  | .edge (Sum.inl (a,b)) =>
      if a = 0 then some (.vertex (Sum.inr (Sum.inl b)))
      else if b = 0 then some (.vertex (Sum.inl a)) else none
  | .edge (Sum.inr (Sum.inl (a,c))) =>
      if a = 0 then some (.vertex (Sum.inr (Sum.inr c))) else none
  | .edge (Sum.inr (Sum.inr _)) => none
  | .triangle (a,b,c) =>
      if a = 0 then some (.edge (Sum.inr (Sum.inr (b,c))))
      else if b = 0 then some (.edge (Sum.inr (Sum.inl (a,c))))
      else if c = 0 then some (.edge (Sum.inl (a,b))) else none

lemma pairUpper_codimOne {lower upper : Face p q r}
    (h : pairUpper lower = some upper) : CodimOne lower upper := by
  rcases lower with v | e | t
  · rcases v with a | bc
    · simp only [pairUpper] at h
      split at h
      · contradiction
      · have hu : .edge (Sum.inl (a,0)) = upper := by simpa using h
        subst upper
        simp [CodimOne]
    · rcases bc with b | c
      · have hu : .edge (Sum.inl (0,b)) = upper := by simpa [pairUpper] using h
        subst upper
        simp [CodimOne]
      · have hu : .edge (Sum.inr (Sum.inl (0,c))) = upper := by simpa [pairUpper] using h
        subst upper
        simp [CodimOne]
  · rcases e with ab | rest
    · rcases ab with ⟨a,b⟩
      simp only [pairUpper] at h
      split at h
      · contradiction
      · have hu : .triangle (a,b,0) = upper := by simpa using h
        subst upper
        simp [CodimOne]
    · rcases rest with ac | bc
      · rcases ac with ⟨a,c⟩
        simp only [pairUpper] at h
        split at h
        · contradiction
        · have hu : .triangle (a,0,c) = upper := by simpa using h
          subst upper
          simp [CodimOne]
      · rcases bc with ⟨b,c⟩
        have hu : .triangle (0,b,c) = upper := by simpa [pairUpper] using h
        subst upper
        simp [CodimOne]
  · simp [pairUpper] at h

/-- Every matched pair is an actual codimension-one inclusion in the Mathlib
abstract simplicial complex. -/
lemma pairUpper_actual_codimOne {lower upper : Face p q r}
    (h : pairUpper lower = some upper) :
    D0.Topology.GenericTripartiteAbstractComplex.Face.vertices lower ⊆
        D0.Topology.GenericTripartiteAbstractComplex.Face.vertices upper ∧
      (D0.Topology.GenericTripartiteAbstractComplex.Face.vertices upper).card =
        (D0.Topology.GenericTripartiteAbstractComplex.Face.vertices lower).card + 1 := by
  rcases lower with v | e | t
  · rcases v with a | bc
    · simp only [pairUpper] at h
      split at h
      · contradiction
      · have hu : .edge (Sum.inl (a,0)) = upper := by simpa using h
        subst upper
        simp [D0.Topology.GenericTripartiteAbstractComplex.Face.vertices,
          D0.Topology.GenericTripartiteAbstractComplex.Face.toCoordinates,
          D0.Topology.GenericTripartiteAbstractComplex.FaceCoordinates.vertices]
    · rcases bc with b | c
      · have hu : .edge (Sum.inl (0,b)) = upper := by simpa [pairUpper] using h
        subst upper
        simp [D0.Topology.GenericTripartiteAbstractComplex.Face.vertices,
          D0.Topology.GenericTripartiteAbstractComplex.Face.toCoordinates,
          D0.Topology.GenericTripartiteAbstractComplex.FaceCoordinates.vertices]
      · have hu : .edge (Sum.inr (Sum.inl (0,c))) = upper := by simpa [pairUpper] using h
        subst upper
        simp [D0.Topology.GenericTripartiteAbstractComplex.Face.vertices,
          D0.Topology.GenericTripartiteAbstractComplex.Face.toCoordinates,
          D0.Topology.GenericTripartiteAbstractComplex.FaceCoordinates.vertices]
  · rcases e with ab | rest
    · rcases ab with ⟨a,b⟩
      simp only [pairUpper] at h
      split at h
      · contradiction
      · have hu : .triangle (a,b,0) = upper := by simpa using h
        subst upper
        simp [D0.Topology.GenericTripartiteAbstractComplex.Face.vertices,
          D0.Topology.GenericTripartiteAbstractComplex.Face.toCoordinates,
          D0.Topology.GenericTripartiteAbstractComplex.FaceCoordinates.vertices]
    · rcases rest with ac | bc
      · rcases ac with ⟨a,c⟩
        simp only [pairUpper] at h
        split at h
        · contradiction
        · have hu : .triangle (a,0,c) = upper := by simpa using h
          subst upper
          simp [D0.Topology.GenericTripartiteAbstractComplex.Face.vertices,
            D0.Topology.GenericTripartiteAbstractComplex.Face.toCoordinates,
            D0.Topology.GenericTripartiteAbstractComplex.FaceCoordinates.vertices]
      · rcases bc with ⟨b,c⟩
        have hu : .triangle (0,b,c) = upper := by simpa [pairUpper] using h
        subst upper
        simp [D0.Topology.GenericTripartiteAbstractComplex.Face.vertices,
          D0.Topology.GenericTripartiteAbstractComplex.Face.toCoordinates,
          D0.Topology.GenericTripartiteAbstractComplex.FaceCoordinates.vertices]
  · simp [pairUpper] at h

lemma pairUpper_pairLower {lower upper : Face p q r}
    (h : pairUpper lower = some upper) : pairLower upper = some lower := by
  rcases lower with v | e | t
  · rcases v with a | bc
    · simp only [pairUpper] at h
      split at h
      · contradiction
      · have hu : .edge (Sum.inl (a,0)) = upper := by simpa using h
        subst upper
        simp [pairLower, *]
    · rcases bc with b | c
      · have hu : .edge (Sum.inl (0,b)) = upper := by simpa [pairUpper] using h
        subst upper
        simp [pairLower]
      · have hu : .edge (Sum.inr (Sum.inl (0,c))) = upper := by simpa [pairUpper] using h
        subst upper
        simp [pairLower]
  · rcases e with ab | rest
    · rcases ab with ⟨a,b⟩
      simp only [pairUpper] at h
      split at h
      · contradiction
      · have hu : .triangle (a,b,0) = upper := by simpa using h
        subst upper
        have ha : a ≠ 0 := by aesop
        have hb : b ≠ 0 := by aesop
        simp [pairLower, ha, hb]
    · rcases rest with ac | bc
      · rcases ac with ⟨a,c⟩
        simp only [pairUpper] at h
        split at h
        · contradiction
        · have hu : .triangle (a,0,c) = upper := by simpa using h
          subst upper
          simp [pairLower, *]
      · rcases bc with ⟨b,c⟩
        have hu : .triangle (0,b,c) = upper := by simpa [pairUpper] using h
        subst upper
        simp [pairLower]
  · simp [pairUpper] at h


lemma pairLower_pairUpper {upper lower : Face p q r}
    (h : pairLower upper = some lower) : pairUpper lower = some upper := by
  rcases upper with v | e | t
  · simp [pairLower] at h
  · rcases e with ab | rest
    · rcases ab with ⟨a,b⟩
      simp only [pairLower] at h
      split at h
      · have hl : .vertex (Sum.inr (Sum.inl b)) = lower := by simpa using h
        subst lower
        simp [pairUpper, *]
      · split at h
        · have hl : .vertex (Sum.inl a) = lower := by simpa using h
          subst lower
          simp [pairUpper, *]
        · contradiction
    · rcases rest with ac | bc
      · rcases ac with ⟨a,c⟩
        simp only [pairLower] at h
        split at h
        · have hl : .vertex (Sum.inr (Sum.inr c)) = lower := by simpa using h
          subst lower
          simp [pairUpper, *]
        · contradiction
      · simp [pairLower] at h
  · rcases t with ⟨a,b,c⟩
    simp only [pairLower] at h
    split at h
    · have hl : .edge (Sum.inr (Sum.inr (b,c))) = lower := by simpa using h
      subst lower
      simp [pairUpper, *]
    · split at h
      · have hl : .edge (Sum.inr (Sum.inl (a,c))) = lower := by simpa using h
        subst lower
        simp [pairUpper, *]
      · split at h
        · have hl : .edge (Sum.inl (a,b)) = lower := by simpa using h
          subst lower
          simp [pairUpper, *]
        · contradiction

/-- No face is simultaneously the lower and upper member of a matched pair. -/
lemma pair_roles_disjoint (f : Face p q r) :
    ¬ ((pairUpper f).isSome ∧ (pairLower f).isSome) := by
  rcases f with v | e | t
  · simp [pairLower]
  · rcases e with ab | rest
    · rcases ab with ⟨a,b⟩
      by_cases ha : a = 0
      · simp [pairUpper, pairLower, ha]
      · by_cases hb : b = 0
        · simp [pairUpper, pairLower, ha, hb]
        · simp [pairUpper, pairLower, ha, hb]
    · rcases rest with ac | bc
      · rcases ac with ⟨a,c⟩
        by_cases ha : a = 0 <;> simp [pairUpper, pairLower, ha]
      · simp [pairUpper, pairLower]
  · simp [pairUpper]

/-- Phase of a lower matched face: `0=A₀`, `1=B₀`, `2=C₀`. -/
def matchingPhase : Face p q r → Option (Fin 3)
  | .vertex (Sum.inl a) => if a = 0 then none else some 0
  | .vertex (Sum.inr (Sum.inl _)) => some 1
  | .vertex (Sum.inr (Sum.inr _)) => some 2
  | .edge (Sum.inl (a,b)) => if a = 0 ∨ b = 0 then none else some 2
  | .edge (Sum.inr (Sum.inl (a,_))) => if a = 0 then none else some 1
  | .edge (Sum.inr (Sum.inr _)) => some 0
  | .triangle _ => none

lemma pairUpper_isSome_iff_phase_isSome (f : Face p q r) :
    (pairUpper f).isSome ↔ (matchingPhase f).isSome := by
  rcases f with v | e | t
  · rcases v with a | bc
    · simp [pairUpper, matchingPhase]
    · rcases bc with b | c <;> simp [pairUpper, matchingPhase]
  · rcases e with ab | rest
    · rcases ab with ⟨a,b⟩
      simp [pairUpper, matchingPhase]
    · rcases rest with ac | bc
      · rcases ac with ⟨a,c⟩
        simp [pairUpper, matchingPhase]
      · simp [pairUpper, matchingPhase]
  · simp [pairUpper, matchingPhase]

end Face
end D0.Topology.GenericTripartiteDiscreteMorse

namespace D0.Topology.GenericTripartiteDiscreteMorse
open D0.Topology.GenericTripartiteAbstractComplex
open D0.Topology.GenericTripartiteHomology
open D0.Topology.GenericTripartiteTopHomologyRing

variable {p q r : ℕ}

namespace Face

/-- Unmatched faces of the canonical Morse matching. -/
def IsCritical (f : Face p q r) : Prop :=
  pairUpper f = none ∧ pairLower f = none

/-- Every face is either critical, a lower matched face, or an upper matched
face. Together with `pair_roles_disjoint`, this is the matching partition. -/
lemma critical_or_matched (f : Face p q r) :
    IsCritical f ∨ (pairUpper f).isSome ∨ (pairLower f).isSome := by
  cases hu : pairUpper f with
  | none =>
      cases hl : pairLower f with
      | none => exact Or.inl ⟨hu,hl⟩
      | some lower => exact Or.inr (Or.inr (by simp))
  | some upper => exact Or.inr (Or.inl (by simp))

lemma root_isCritical : IsCritical (root (p:=p) (q:=q) (r:=r)) := by
  simp [IsCritical, root, pairUpper, pairLower]

lemma triangle_isCritical_iff
    (a : Fin (p+1)) (b : Fin (q+1)) (c : Fin (r+1)) :
    IsCritical (.triangle (a,b,c) : Face p q r) ↔
      a ≠ 0 ∧ b ≠ 0 ∧ c ≠ 0 := by
  simp only [IsCritical, pairUpper, true_and]
  by_cases ha : a = 0
  · simp [pairLower, ha]
  · by_cases hb : b = 0
    · simp [pairLower, ha, hb]
    · by_cases hc : c = 0 <;> simp [pairLower, ha, hb, hc]

lemma vertex_isCritical_iff (v : GenericVertex p q r) :
    IsCritical (.vertex v : Face p q r) ↔
      v = Sum.inl 0 := by
  rcases v with a | bc
  · simp [IsCritical, pairUpper, pairLower]
  · rcases bc with b | c <;> simp [IsCritical, pairUpper, pairLower]

lemma edge_not_isCritical (e : GenericEdge p q r) :
    ¬ IsCritical (.edge e : Face p q r) := by
  rcases e with ab | rest
  · rcases ab with ⟨a,b⟩
    simp only [IsCritical, pairUpper, pairLower]
    by_cases ha : a = 0
    · simp [ha]
    · by_cases hb : b = 0
      · simp [ha, hb]
      · simp [ha, hb]
  · rcases rest with ac | bc
    · rcases ac with ⟨a,c⟩
      simp only [IsCritical, pairUpper, pairLower]
      by_cases ha : a = 0 <;> simp [ha]
    · rcases bc with ⟨b,c⟩
      simp [IsCritical, pairUpper, pairLower]

/-- Critical 2-faces are exactly the all-nonroot triangles. -/
def criticalTriangle (i : TopCycleIndex p q r) : Face p q r :=
  .triangle (i.1.succ, i.2.1.succ, i.2.2.succ)

lemma criticalTriangle_isCritical (i : TopCycleIndex p q r) :
    IsCritical (criticalTriangle i) := by
  change IsCritical
    (.triangle (i.1.succ, i.2.1.succ, i.2.2.succ) : Face p q r)
  rw [triangle_isCritical_iff]
  exact ⟨Fin.succ_ne_zero _, Fin.succ_ne_zero _, Fin.succ_ne_zero _⟩

lemma criticalTriangle_injective : Function.Injective
    (criticalTriangle : TopCycleIndex p q r → Face p q r) := by
  intro i i' h
  have ht :
      (i.1.succ, i.2.1.succ, i.2.2.succ) =
        (i'.1.succ, i'.2.1.succ, i'.2.2.succ) := by
    simpa only [criticalTriangle, Face.triangle.injEq] using h
  have ha : i.1.succ = i'.1.succ := congrArg Prod.fst ht
  have hb : i.2.1.succ = i'.2.1.succ :=
    congrArg (fun x => x.2.1) ht
  have hc : i.2.2.succ = i'.2.2.succ :=
    congrArg (fun x => x.2.2) ht
  exact Prod.ext (Fin.succ_inj.mp ha)
    (Prod.ext (Fin.succ_inj.mp hb) (Fin.succ_inj.mp hc))

lemma isCritical_iff (f : Face p q r) :
    IsCritical f ↔
      f = root ∨ ∃ i : TopCycleIndex p q r, f = criticalTriangle i := by
  rcases f with v | e | t
  · rw [vertex_isCritical_iff]
    constructor
    · intro h
      left
      simpa [root] using congrArg Face.vertex h
    · rintro (h | ⟨i,h⟩)
      · simpa [root] using congrArg (fun x => match x with | Face.vertex v => v | _ => Sum.inl 0) h
      · cases h
  · constructor
    · intro h
      exact (edge_not_isCritical e h).elim
    · rintro (h | ⟨i,h⟩) <;> cases h
  · rcases t with ⟨a,b,c⟩
    rw [triangle_isCritical_iff]
    constructor
    · rintro ⟨ha,hb,hc⟩
      obtain ⟨i,rfl⟩ := Fin.eq_succ_of_ne_zero ha
      obtain ⟨j,rfl⟩ := Fin.eq_succ_of_ne_zero hb
      obtain ⟨k,rfl⟩ := Fin.eq_succ_of_ne_zero hc
      exact Or.inr ⟨(i,j,k), rfl⟩
    · rintro (h | ⟨⟨i,j,k⟩,h⟩)
      · cases h
      · cases h
        exact ⟨Fin.succ_ne_zero _, Fin.succ_ne_zero _, Fin.succ_ne_zero _⟩


/-- Canonical enumeration of all critical faces: the root vertex plus one
critical 2-face for each top-cycle index. -/
def criticalFaceMap : Unit ⊕ TopCycleIndex p q r →
    {f : Face p q r // IsCritical f}
  | Sum.inl _ => ⟨root, root_isCritical⟩
  | Sum.inr i => ⟨criticalTriangle i, criticalTriangle_isCritical i⟩

lemma criticalFaceMap_injective : Function.Injective
    (criticalFaceMap : Unit ⊕ TopCycleIndex p q r →
      {f : Face p q r // IsCritical f}) := by
  intro x y h
  rcases x with u | i <;> rcases y with v | j
  · cases u; cases v; rfl
  · have hval := congrArg Subtype.val h
    simp [criticalFaceMap, root, criticalTriangle] at hval
  · have hval := congrArg Subtype.val h
    simp [criticalFaceMap, root, criticalTriangle] at hval
  · congr
    exact criticalTriangle_injective (congrArg Subtype.val h)

lemma criticalFaceMap_surjective : Function.Surjective
    (criticalFaceMap : Unit ⊕ TopCycleIndex p q r →
      {f : Face p q r // IsCritical f}) := by
  rintro ⟨f,hf⟩
  rcases (isCritical_iff f).mp hf with hroot | ⟨i,hi⟩
  · subst f
    exact ⟨Sum.inl (), rfl⟩
  · subst f
    exact ⟨Sum.inr i, rfl⟩

noncomputable def criticalFaceEquiv :
    {f : Face p q r // IsCritical f} ≃
      Unit ⊕ TopCycleIndex p q r :=
  (Equiv.ofBijective criticalFaceMap
    ⟨criticalFaceMap_injective, criticalFaceMap_surjective⟩).symm

noncomputable instance criticalFaceFintype :
    Fintype {f : Face p q r // IsCritical f} :=
  Fintype.ofFinite _

/-- Critical faces in dimension two. -/
abbrev CriticalTwoFace (p q r : ℕ) :=
  {f : Face p q r // IsCritical f ∧ dimension f = 2}

/-- Canonical enumeration of the critical 2-faces. -/
def criticalTwoFaceMap :
    TopCycleIndex p q r → CriticalTwoFace p q r :=
  fun i => ⟨criticalTriangle i, criticalTriangle_isCritical i, rfl⟩

lemma criticalTwoFaceMap_bijective : Function.Bijective
    (criticalTwoFaceMap :
      TopCycleIndex p q r → CriticalTwoFace p q r) := by
  constructor
  · intro i j h
    exact criticalTriangle_injective (congrArg Subtype.val h)
  · rintro ⟨f,hf,hdim⟩
    rcases (isCritical_iff f).mp hf with hroot | ⟨i,hi⟩
    · subst f
      simp [dimension, root] at hdim
    · subst f
      exact ⟨i, rfl⟩

noncomputable def criticalTwoFaceEquiv :
    CriticalTwoFace p q r ≃ TopCycleIndex p q r :=
  (Equiv.ofBijective criticalTwoFaceMap
    criticalTwoFaceMap_bijective).symm

noncomputable instance criticalTwoFaceFintype :
    Fintype (CriticalTwoFace p q r) :=
  Fintype.ofFinite _

/-- Exact critical-cell count of the canonical matching. -/
theorem criticalFace_card :
    Fintype.card {f : Face p q r // IsCritical f} = 1 + p*q*r := by
  rw [Fintype.card_congr (criticalFaceEquiv (p:=p) (q:=q) (r:=r))]
  simp [TopCycleIndex, Nat.mul_assoc]

/-- Exact count of critical 2-cells. -/
theorem criticalTwoFace_card :
    Fintype.card (CriticalTwoFace p q r) = p*q*r := by
  rw [Fintype.card_congr
    (criticalTwoFaceEquiv (p:=p) (q:=q) (r:=r))]
  simp [TopCycleIndex, Nat.mul_assoc]

/-- The discrete-Morse critical 2-cell count equals the already-proved
rational top-homology rank. -/
theorem criticalTwoFace_card_eq_top_homology_finrank :
    Fintype.card (CriticalTwoFace p q r) =
      Module.finrank ℚ
        (LinearMap.ker
          (boundary2 (p:=p) (q:=q) (r:=r)).mulVecLin) := by
  rw [criticalTwoFace_card, boundary2_kernel_finrank]

/-- Scene specialization: one critical vertex and `960` critical 2-faces. -/
theorem scene_criticalFace_card :
    Fintype.card {f : Face 8 10 12 // IsCritical f} = 961 := by
  simpa using criticalFace_card (p:=8) (q:=10) (r:=12)

/-- Scene specialization of the critical 2-cell count. -/
theorem scene_criticalTwoFace_card :
    Fintype.card (CriticalTwoFace 8 10 12) = 960 := by
  simpa using criticalTwoFace_card (p:=8) (q:=10) (r:=12)

/-- The critical 2-faces use exactly the same `960`-element index as the
explicit octahedral top-homology basis. -/
theorem scene_criticalTriangle_index_card :
    Fintype.card (TopCycleIndex 8 10 12) = 960 := by
  native_decide

end Face
end D0.Topology.GenericTripartiteDiscreteMorse

namespace D0.Topology.GenericTripartiteDiscreteMorse
open D0.Topology.GenericTripartiteAbstractComplex
open D0.Topology.GenericTripartiteHomology
open D0.Topology.GenericTripartiteTopHomologyRing

variable {p q r : ℕ}

namespace Face

/-- A Forman `V`-path step: follow a matched lower face to its upper face,
then move to a different codimension-one face which is itself matched upward. -/
def GradientStep (lower next : Face p q r) : Prop :=
  ∃ upper,
    pairUpper lower = some upper ∧
    CodimOne next upper ∧
    next ≠ lower ∧
    (pairUpper next).isSome

/-- Strict descent rank for the canonical matching.  It is dimension-local:
`A* > B*` on matched vertices and `AB* > AC* > BC*` on matched edges. -/
def gradientRank : Face p q r → ℕ
  | .vertex (Sum.inl a) => if a = 0 then 0 else 1
  | .vertex (Sum.inr _) => 0
  | .edge (Sum.inl (a,b)) => if a = 0 ∨ b = 0 then 0 else 2
  | .edge (Sum.inr (Sum.inl (a,_))) => if a = 0 then 0 else 1
  | .edge (Sum.inr (Sum.inr _)) => 0
  | .triangle _ => 0

lemma gradientStep_rank_lt {lower next : Face p q r}
    (h : GradientStep lower next) :
    gradientRank next < gradientRank lower := by
  rcases h with ⟨upper, hup, hface, hne, hnext⟩
  rcases lower with v | e | t
  · rcases v with a | bc
    · simp only [pairUpper] at hup
      split at hup
      · contradiction
      · have hu : .edge (Sum.inl (a,0)) = upper := by simpa using hup
        subst upper
        rcases next with v' | e' | t'
        · rcases v' with a' | bc'
          · simp [CodimOne] at hface
            subst a'
            exact (hne rfl).elim
          · rcases bc' with b' | c'
            · simp [CodimOne] at hface
              subst b'
              have ha : a ≠ 0 := by aesop
              simp [gradientRank, ha]
            · simp [CodimOne] at hface
        · simp [CodimOne] at hface
        · simp [CodimOne] at hface
    · rcases bc with b | c
      · have hu : .edge (Sum.inl (0,b)) = upper := by simpa [pairUpper] using hup
        subst upper
        rcases next with v' | e' | t'
        · rcases v' with a' | bc'
          · simp [CodimOne] at hface
            subst a'
            simp [pairUpper] at hnext
          · rcases bc' with b' | c'
            · simp [CodimOne] at hface
              subst b'
              exact (hne rfl).elim
            · simp [CodimOne] at hface
        · simp [CodimOne] at hface
        · simp [CodimOne] at hface
      · have hu : .edge (Sum.inr (Sum.inl (0,c))) = upper := by simpa [pairUpper] using hup
        subst upper
        rcases next with v' | e' | t'
        · rcases v' with a' | bc'
          · simp [CodimOne] at hface
            subst a'
            simp [pairUpper] at hnext
          · rcases bc' with b' | c'
            · simp [CodimOne] at hface
            · simp [CodimOne] at hface
              subst c'
              exact (hne rfl).elim
        · simp [CodimOne] at hface
        · simp [CodimOne] at hface
  · rcases e with ab | rest
    · rcases ab with ⟨a,b⟩
      simp only [pairUpper] at hup
      split at hup
      · contradiction
      · have hu : .triangle (a,b,0) = upper := by simpa using hup
        subst upper
        rcases next with v' | e' | t'
        · simp [CodimOne] at hface
        · rcases e' with ab' | rest'
          · rcases ab' with ⟨a',b'⟩
            simp [CodimOne] at hface
            rcases hface with ⟨rfl,rfl⟩
            exact (hne rfl).elim
          · rcases rest' with ac' | bc'
            · rcases ac' with ⟨a',c'⟩
              simp [CodimOne] at hface
              rcases hface with ⟨rfl,rfl⟩
              have ha : a' ≠ 0 := by aesop
              have hb : b ≠ 0 := by aesop
              simp [gradientRank, ha, hb]
            · rcases bc' with ⟨b',c'⟩
              simp [CodimOne] at hface
              rcases hface with ⟨rfl,rfl⟩
              have ha : a ≠ 0 := by aesop
              have hb : b' ≠ 0 := by aesop
              simp [gradientRank, ha, hb]
        · simp [CodimOne] at hface
    · rcases rest with ac | bc
      · rcases ac with ⟨a,c⟩
        simp only [pairUpper] at hup
        split at hup
        · contradiction
        · have hu : .triangle (a,0,c) = upper := by simpa using hup
          subst upper
          rcases next with v' | e' | t'
          · simp [CodimOne] at hface
          · rcases e' with ab' | rest'
            · rcases ab' with ⟨a',b'⟩
              simp [CodimOne] at hface
              rcases hface with ⟨rfl,rfl⟩
              simp [pairUpper] at hnext
            · rcases rest' with ac' | bc'
              · rcases ac' with ⟨a',c'⟩
                simp [CodimOne] at hface
                rcases hface with ⟨rfl,rfl⟩
                exact (hne rfl).elim
              · rcases bc' with ⟨b',c'⟩
                simp [CodimOne] at hface
                rcases hface with ⟨rfl,rfl⟩
                have ha : a ≠ 0 := by aesop
                simp [gradientRank, ha]
          · simp [CodimOne] at hface
      · rcases bc with ⟨b,c⟩
        have hu : .triangle (0,b,c) = upper := by simpa [pairUpper] using hup
        subst upper
        rcases next with v' | e' | t'
        · simp [CodimOne] at hface
        · rcases e' with ab' | rest'
          · rcases ab' with ⟨a',b'⟩
            simp [CodimOne] at hface
            rcases hface with ⟨rfl,rfl⟩
            simp [pairUpper] at hnext
          · rcases rest' with ac' | bc'
            · rcases ac' with ⟨a',c'⟩
              simp [CodimOne] at hface
              rcases hface with ⟨rfl,rfl⟩
              simp [pairUpper] at hnext
            · rcases bc' with ⟨b',c'⟩
              simp [CodimOne] at hface
              rcases hface with ⟨rfl,rfl⟩
              exact (hne rfl).elim
        · simp [CodimOne] at hface
  · simp [pairUpper] at hup

lemma gradientPath_rank_lt {lower next : Face p q r}
    (h : Relation.TransGen GradientStep lower next) :
    gradientRank next < gradientRank lower := by
  induction h with
  | single h => exact gradientStep_rank_lt h
  | tail _ hstep ih => exact lt_trans (gradientStep_rank_lt hstep) ih

/-- The root-lexicographic matching is acyclic: no nonempty closed `V`-path exists. -/
theorem gradient_acyclic (f : Face p q r) :
    ¬ Relation.TransGen GradientStep f f := by
  intro h
  exact (lt_irrefl _ (gradientPath_rank_lt h))

end Face
end D0.Topology.GenericTripartiteDiscreteMorse
