import D0.Topology.GenericTripartiteDegeneratePairing
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic

/-!
# D0-GENERIC-TRIPARTITE-PAIRING-BOUNDARY-001

This module proves the converse to the degenerate-pairing construction.

The nondegenerate simplices outside the root subcomplex are finite and have
alternating Euler sum exactly `p*q*r`.  For any **proper** pairing of that
complement, every type-II simplex is paired with a unique codimension-one
type-I simplex, so the two signs cancel pairwise.  Therefore any proper
pairing forces `p*q*r = 0`.

Together with `GenericTripartiteDegeneratePairing`, this gives the exact
boundary

```
there exists a proper pairing outside the root
  ↔ there exists a regular pairing outside the root
  ↔ the root inclusion is strong anodyne
  ↔ p*q*r = 0.
```

This is a theorem about simplicial pairings and strong-anodyne extensions.  It
does not use, and does not assert, the still-missing bridge from anodyne
extensions through geometric realization to topological homotopy
equivalences.
-/

namespace D0.Topology.GenericTripartitePairingBoundary

open scoped BigOperators
open D0.Topology.GenericTripartiteSimplicialMorse
open D0.Topology.GenericTripartiteSimplicialSet
open D0.Topology.GenericTripartiteAbstractComplex
open D0.Topology.GenericTripartiteDiscreteMorse
open D0.Topology.GenericTripartiteHomology
open D0.Topology.GenericTripartiteDegeneratePairing

variable {p q r : ℕ}

private def sign (n : ℕ) : ℤ := (-1 : ℤ) ^ n

lemma sign_succ (n : ℕ) : sign (n + 1) = -sign n := by
  simp [sign, pow_succ]

/-- Nondegenerate simplices outside the root are exactly typed faces other
than the root face. -/
noncomputable def rootComplementFaceEquiv :
    RootComplement p q r ≃ {f : Face p q r // f ≠ Face.root} where
  toFun x := ⟨nondegenerateFaceEquiv x.toN, by
    intro h
    have hx : x.toN = rootSimplex := by
      apply (nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r)).injective
      calc
        nondegenerateFaceEquiv x.toN = Face.root := h
        _ = nondegenerateFaceEquiv rootSimplex :=
          nondegenerateFaceEquiv_rootSimplex.symm
    exact x.notMem ((mem_rootSubcomplex_iff x.toN).2 hx)⟩
  invFun f := SSet.Subcomplex.N.mk'
    (faceNondegenerateEquiv f.1)
    (by
      intro hmem
      have heq := (mem_rootSubcomplex_iff
        (faceNondegenerateEquiv f.1)).1 hmem
      apply f.2
      calc
        f.1 = nondegenerateFaceEquiv (faceNondegenerateEquiv f.1) :=
          ((nondegenerateFaceEquiv
            (p:=p) (q:=q) (r:=r)).apply_symm_apply f.1).symm
        _ = nondegenerateFaceEquiv rootSimplex := congrArg _ heq
        _ = Face.root := nondegenerateFaceEquiv_rootSimplex)
  left_inv x := by
    apply (SSet.Subcomplex.N.ext_iff _ _).2
    apply (nondegenerateFaceEquiv (p:=p) (q:=q) (r:=r)).injective
    exact (nondegenerateFaceEquiv
      (p:=p) (q:=q) (r:=r)).apply_symm_apply _
  right_inv f := by
    apply Subtype.ext
    exact (nondegenerateFaceEquiv
      (p:=p) (q:=q) (r:=r)).apply_symm_apply _

noncomputable instance rootComplementFintype :
    Fintype (RootComplement p q r) :=
  Fintype.ofEquiv {f : Face p q r // f ≠ Face.root}
    (rootComplementFaceEquiv (p:=p) (q:=q) (r:=r)).symm

@[simp] lemma rootComplementFaceEquiv_dimension
    (x : RootComplement p q r) :
    Face.dimension (rootComplementFaceEquiv x).1 = x.toN.dim :=
  nondegenerateFaceEquiv_dimension x.toN

/-- The two parts of any pairing exhaust the root complement. -/
noncomputable def pairingPartitionEquiv
    (P : (rootSubcomplex (p:=p) (q:=q) (r:=r)).Pairing) :
    P.II ⊕ P.I ≃ RootComplement p q r := by
  classical
  refine
    { toFun := fun x => match x with
        | Sum.inl x => x.1
        | Sum.inr x => x.1
      invFun := fun x => if h : x ∈ P.II then Sum.inl ⟨x,h⟩ else
        Sum.inr ⟨x, ?_⟩
      left_inv := ?_
      right_inv := ?_ }
  · have hu : x ∈ P.I ∪ P.II := by rw [P.union]; trivial
    rcases hu with hI | hII
    · exact hI
    · exact (h hII).elim
  · rintro (x | x)
    · simp [x.2]
    · have hxII : x.1 ∉ P.II := by
        intro hxII
        have : x.1 ∈ P.I ∩ P.II := ⟨x.2, hxII⟩
        simpa [P.inter] using this
      simp [hxII]
  · intro x
    by_cases h : x ∈ P.II <;> simp [h]

/-- Alternating sum over all typed faces is the Euler characteristic. -/
lemma face_euler_sum :
    (∑ f : Face p q r, sign (Face.dimension f)) =
      eulerCharacteristic (p:=p) (q:=q) (r:=r) := by
  let e := faceEquivSum (p:=p) (q:=q) (r:=r)
  calc
    (∑ f : Face p q r, sign (Face.dimension f)) =
        ∑ x : GenericVertex p q r ⊕
          (GenericEdge p q r ⊕ GenericTriangle p q r),
          sign (Face.dimension (e.symm x)) := by
      apply Fintype.sum_equiv e
      intro f
      simp
    _ = (Fintype.card (GenericVertex p q r) : ℤ)
        - Fintype.card (GenericEdge p q r)
        + Fintype.card (GenericTriangle p q r) := by
      rw [Fintype.sum_sum_type, Fintype.sum_sum_type]
      simp [e, faceEquivSum, Face.dimension, sign]
      ring
    _ = eulerCharacteristic (p:=p) (q:=q) (r:=r) := rfl

/-- Removing the root from the face carrier leaves alternating sum `p*q*r`. -/
lemma rootComplement_euler_sum :
    (∑ x : RootComplement p q r, sign x.toN.dim) =
      (p * q * r : ℤ) := by
  classical
  let eRoot := Equiv.sumCompl (fun f : Face p q r => f = Face.root)
  have hsplit :
      (∑ f : Face p q r, sign (Face.dimension f)) =
        (∑ f : {f : Face p q r // f = Face.root},
          sign (Face.dimension f.1)) +
        (∑ f : {f : Face p q r // ¬ f = Face.root},
          sign (Face.dimension f.1)) := by
    calc
      _ = ∑ z : {f : Face p q r // f = Face.root} ⊕
          {f : Face p q r // ¬ f = Face.root},
          sign (Face.dimension (eRoot z)) :=
        (eRoot.sum_comp (fun f => sign (Face.dimension f))).symm
      _ = _ := by rw [Fintype.sum_sum_type]; rfl
  have hroot :
      (∑ f : {f : Face p q r // f = Face.root},
        sign (Face.dimension f.1)) = 1 := by
    let rootFace : {f : Face p q r // f = Face.root} :=
      ⟨Face.root, rfl⟩
    letI : Unique {f : Face p q r // f = Face.root} :=
      { default := rootFace
        uniq := fun f => Subtype.ext f.2 }
    simp [sign, Face.root, Face.dimension]
  have hnot :
      (∑ f : {f : Face p q r // ¬ f = Face.root},
        sign (Face.dimension f.1)) = (p * q * r : ℤ) := by
    rw [face_euler_sum, euler_characteristic_formula, hroot] at hsplit
    omega
  calc
    _ = ∑ f : {f : Face p q r // f ≠ Face.root},
        sign (Face.dimension f.1) := by
      apply Fintype.sum_equiv
        (rootComplementFaceEquiv (p:=p) (q:=q) (r:=r))
      intro x
      rw [rootComplementFaceEquiv_dimension]
    _ = _ := hnot

/-- Every proper pair contributes opposite Euler signs, hence any proper
pairing of the root complement has zero alternating sum. -/
lemma properPairing_euler_zero
    (P : (rootSubcomplex (p:=p) (q:=q) (r:=r)).Pairing)
    [P.IsProper] :
    (∑ x : RootComplement p q r, sign x.toN.dim) = 0 := by
  classical
  calc
    _ = ∑ z : P.II ⊕ P.I,
        sign (pairingPartitionEquiv P z).toN.dim := by
      symm
      exact (pairingPartitionEquiv P).sum_comp
        (fun x => sign x.toN.dim)
    _ = (∑ x : P.II, sign x.1.toN.dim) +
        ∑ y : P.I, sign y.1.toN.dim := by
      rw [Fintype.sum_sum_type]
      rfl
    _ = (∑ x : P.II, sign x.1.toN.dim) +
        ∑ x : P.II, sign (P.p x).1.toN.dim := by
      congr 1
      exact (P.p.sum_comp (fun y : P.I => sign y.1.toN.dim)).symm
    _ = ∑ x : P.II,
        (sign x.1.toN.dim + sign (P.p x).1.toN.dim) := by
      rw [Finset.sum_add_distrib]
    _ = 0 := by
      apply Fintype.sum_eq_zero
      intro x
      rw [P.dim_p, sign_succ]
      simp

/-- Any proper pairing outside the root forces the top critical count to
vanish. -/
theorem properPairing_forces_topCount_zero
    (P : (rootSubcomplex (p:=p) (q:=q) (r:=r)).Pairing)
    [P.IsProper] : p * q * r = 0 := by
  have hzero := properPairing_euler_zero P
  have hvalue := rootComplement_euler_sum (p:=p) (q:=q) (r:=r)
  have hz : (p * q * r : ℤ) = 0 := hvalue.symm.trans hzero
  exact_mod_cast hz

/-- Exact boundary for proper pairings outside the root. -/
theorem exists_proper_pairing_iff_topCount_zero :
    (∃ P : (rootSubcomplex (p:=p) (q:=q) (r:=r)).Pairing,
      P.IsProper) ↔ p * q * r = 0 := by
  constructor
  · rintro ⟨P, hP⟩
    letI : P.IsProper := hP
    exact properPairing_forces_topCount_zero P
  · intro hzero
    rw [Nat.mul_eq_zero] at hzero
    rcases hzero with hpq | hr
    · rw [Nat.mul_eq_zero] at hpq
      rcases hpq with hp | hq
      · let P := pairing (p:=p) (q:=q) (r:=r) (Or.inl hp)
        exact ⟨P, inferInstance⟩
      · let P := pairing (p:=p) (q:=q) (r:=r) (Or.inr (Or.inl hq))
        exact ⟨P, inferInstance⟩
    · let P := pairing (p:=p) (q:=q) (r:=r) (Or.inr (Or.inr hr))
      exact ⟨P, inferInstance⟩

/-- Exact boundary for regular pairings outside the root. -/
theorem exists_regular_pairing_iff_topCount_zero :
    (∃ P : (rootSubcomplex (p:=p) (q:=q) (r:=r)).Pairing,
      P.IsRegular) ↔ p * q * r = 0 := by
  constructor
  · rintro ⟨P, hP⟩
    letI : P.IsRegular := hP
    exact properPairing_forces_topCount_zero P
  · intro hzero
    rw [Nat.mul_eq_zero] at hzero
    rcases hzero with hpq | hr
    · rw [Nat.mul_eq_zero] at hpq
      rcases hpq with hp | hq
      · let P := pairing (p:=p) (q:=q) (r:=r) (Or.inl hp)
        exact ⟨P, inferInstance⟩
      · let P := pairing (p:=p) (q:=q) (r:=r) (Or.inr (Or.inl hq))
        exact ⟨P, inferInstance⟩
    · let P := pairing (p:=p) (q:=q) (r:=r) (Or.inr (Or.inr hr))
      exact ⟨P, inferInstance⟩

/-- Exact strong-anodyne boundary for the root inclusion. -/
theorem root_inclusion_strongAnodyne_iff_topCount_zero :
    SSet.strongAnodyneExtensions
      (rootSubcomplex (p:=p) (q:=q) (r:=r)).ι ↔
      p * q * r = 0 := by
  rw [SSet.strongAnodyneExtensions_ι_iff,
      exists_regular_pairing_iff_topCount_zero]

end D0.Topology.GenericTripartitePairingBoundary
