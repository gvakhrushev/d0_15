import D0.Topology.GenericTripartiteSimplicialMorse
import Mathlib.AlgebraicTopology.SimplicialSet.AnodyneExtensions.Basic
import Mathlib.Tactic

/-!
# D0-GENERIC-TRIPARTITE-DEGENERATE-PAIRING-001

This module proves the first genuine spatial-collapse statement available for
the canonical tripartite simplicial set.

When `p*q*r = 0`, there are no critical two-simplices.  The root is then the
only critical simplex, and all other nondegenerate simplices are partitioned
by the transported Morse matching into lower and upper pairs.  We package this
partition as a Mathlib `SSet.Subcomplex.Pairing` relative to the root
subcomplex, prove that it is proper and regular, and conclude that the root
inclusion is both strong anodyne and anodyne.

Thus the zero-top-cell boundary has a formal simplicial collapse certificate,
not merely a chain contraction.  The current Mathlib tree does not yet provide
the final bridge saying that geometric realization sends this anodyne
inclusion to a topological `HomotopyEquiv`; that stronger topological claim is
deliberately not asserted here.
-/

namespace D0.Topology.GenericTripartiteDegeneratePairing

open D0.Topology.GenericTripartiteSimplicialMorse
open D0.Topology.GenericTripartiteSimplicialSet
open D0.Topology.GenericTripartiteAbstractComplex
open D0.Topology.GenericTripartiteDiscreteMorse

variable {p q r : ℕ}

abbrev RootComplement (p q r : ℕ) :=
  (rootSubcomplex (p:=p) (q:=q) (r:=r)).N

private def IsLower (x : RootComplement p q r) : Prop :=
  (pairUpper x.toN).isSome

private def IsUpper (x : RootComplement p q r) : Prop :=
  (pairLower x.toN).isSome

private lemma pairUpper_get_eq_some {x : NondegenerateFace p q r}
    (hx : (pairUpper x).isSome) :
    pairUpper x = some ((pairUpper x).get hx) := by
  exact (Option.some_get hx).symm

private lemma pairLower_get_eq_some {x : NondegenerateFace p q r}
    (hx : (pairLower x).isSome) :
    pairLower x = some ((pairLower x).get hx) := by
  exact (Option.some_get hx).symm

private lemma matched_notMem_root_of_zero
    (hzero : p = 0 ∨ q = 0 ∨ r = 0)
    (x : NondegenerateFace p q r)
    (hx : (pairUpper x).isSome ∨ (pairLower x).isSome) :
    x.simplex ∉ (rootSubcomplex (p:=p) (q:=q) (r:=r)).obj _ := by
  intro hmem
  have hcrit : IsCritical x :=
    (rootSubcomplex_exactly_critical_of_zero hzero x).1 hmem
  rcases hx with hupper | hlower
  · rw [hcrit.1] at hupper
    simp at hupper
  · rw [hcrit.2] at hlower
    simp at hlower

noncomputable def upperOfLower
    (hzero : p = 0 ∨ q = 0 ∨ r = 0)
    (x : {x : RootComplement p q r // IsLower x}) :
    {x : RootComplement p q r // IsUpper x} := by
  let upper := (pairUpper x.1.toN).get x.2
  have hpair : pairUpper x.1.toN = some upper :=
    pairUpper_get_eq_some x.2
  have hinv : pairLower upper = some x.1.toN :=
    pairUpper_pairLower hpair
  let upper' : RootComplement p q r :=
    SSet.Subcomplex.N.mk' upper
      (matched_notMem_root_of_zero hzero upper
        (Or.inr (by rw [hinv]; simp)))
  exact ⟨upper', by
    change (pairLower upper).isSome
    rw [hinv]
    simp⟩

noncomputable def lowerOfUpper
    (hzero : p = 0 ∨ q = 0 ∨ r = 0)
    (x : {x : RootComplement p q r // IsUpper x}) :
    {x : RootComplement p q r // IsLower x} := by
  let lower := (pairLower x.1.toN).get x.2
  have hpair : pairLower x.1.toN = some lower :=
    pairLower_get_eq_some x.2
  have hinv : pairUpper lower = some x.1.toN :=
    pairLower_pairUpper hpair
  let lower' : RootComplement p q r :=
    SSet.Subcomplex.N.mk' lower
      (matched_notMem_root_of_zero hzero lower
        (Or.inl (by rw [hinv]; simp)))
  exact ⟨lower', by
    change (pairUpper lower).isSome
    rw [hinv]
    simp⟩

lemma lowerOfUpper_upperOfLower
    (hzero : p = 0 ∨ q = 0 ∨ r = 0)
    (x : {x : RootComplement p q r // IsLower x}) :
    lowerOfUpper hzero (upperOfLower hzero x) = x := by
  apply Subtype.ext
  apply (SSet.Subcomplex.N.ext_iff _ _).2
  change (pairLower ((pairUpper x.1.toN).get x.2)).get _ =
    x.1.toN
  have hpair : pairUpper x.1.toN =
      some ((pairUpper x.1.toN).get x.2) :=
    pairUpper_get_eq_some x.2
  have hinv := pairUpper_pairLower hpair
  obtain ⟨_, hget⟩ := Option.eq_some_iff_get_eq.mp hinv
  simpa using hget

lemma upperOfLower_lowerOfUpper
    (hzero : p = 0 ∨ q = 0 ∨ r = 0)
    (x : {x : RootComplement p q r // IsUpper x}) :
    upperOfLower hzero (lowerOfUpper hzero x) = x := by
  apply Subtype.ext
  apply (SSet.Subcomplex.N.ext_iff _ _).2
  change (pairUpper ((pairLower x.1.toN).get x.2)).get _ =
    x.1.toN
  have hpair : pairLower x.1.toN =
      some ((pairLower x.1.toN).get x.2) :=
    pairLower_get_eq_some x.2
  have hinv := pairLower_pairUpper hpair
  obtain ⟨_, hget⟩ := Option.eq_some_iff_get_eq.mp hinv
  simpa using hget

noncomputable def matchedEquiv
    (hzero : p = 0 ∨ q = 0 ∨ r = 0) :
    {x : RootComplement p q r // IsLower x} ≃
      {x : RootComplement p q r // IsUpper x} where
  toFun := upperOfLower hzero
  invFun := lowerOfUpper hzero
  left_inv := lowerOfUpper_upperOfLower hzero
  right_inv := upperOfLower_lowerOfUpper hzero

/-- Pair all nonroot nondegenerate simplices by the transported Morse
matching. -/
noncomputable def pairing
    (hzero : p = 0 ∨ q = 0 ∨ r = 0) :
    (rootSubcomplex (p:=p) (q:=q) (r:=r)).Pairing where
  I := {x | IsUpper x}
  II := {x | IsLower x}
  inter := by
    ext x
    simp only [Set.mem_inter_iff, Set.mem_setOf_eq,
      Set.mem_empty_iff_false, iff_false]
    exact pair_roles_disjoint x.toN ∘ And.symm
  union := by
    ext x
    simp only [Set.mem_union, Set.mem_setOf_eq,
      Set.mem_univ, iff_true]
    have hpartition := critical_or_matched x.toN
    rcases hpartition with hcrit | hlower | hupper
    · have hmem :=
        (rootSubcomplex_exactly_critical_of_zero hzero x.toN).2 hcrit
      exact (x.notMem hmem).elim
    · exact Or.inr hlower
    · exact Or.inl hupper
  p := matchedEquiv hzero

@[simp] lemma pairing_p_apply
    (hzero : p = 0 ∨ q = 0 ∨ r = 0)
    (x : {x : RootComplement p q r // IsLower x}) :
    (pairing hzero).p x = upperOfLower hzero x := rfl

instance pairing_isProper
    (hzero : p = 0 ∨ q = 0 ∨ r = 0) :
    (pairing hzero).IsProper where
  isUniquelyCodimOneFace := by
    rintro ⟨x, hx⟩
    have hpair : pairUpper x.toN =
        some ((pairUpper x.toN).get hx) :=
      pairUpper_get_eq_some hx
    have hproper := pairUpper_isUniquelyCodimOneFace hpair
    simpa [pairing, matchedEquiv, upperOfLower] using hproper

/-- The inherited gradient rank is a weak rank function for the root
pairing. -/
noncomputable def pairingWeakRank
    (hzero : p = 0 ∨ q = 0 ∨ r = 0) :
    (pairing hzero).WeakRankFunction ℕ where
  rank x := gradientRank x.1.toN
  lt {x y} hxy hdim := by
    have hxLower : IsLower x.1 := by
      have hx := x.2
      change IsLower x.1 at hx
      exact hx
    have hyLower : IsLower y.1 := by
      have hy := y.2
      change IsLower y.1 at hy
      exact hy
    have hyPair : pairUpper y.1.toN =
        some (((pairing hzero).p y).1.toN) := by
      rw [pairing_p_apply]
      exact pairUpper_get_eq_some hyLower
    have hdimUpper : ((pairing hzero).p y).1.toN.dim =
        x.1.toN.dim + 1 := by
      calc
        ((pairing hzero).p y).1.toN.dim =
            y.1.toN.dim + 1 := pairUpper_dimension hyPair
        _ = x.1.toN.dim + 1 := by rw [hdim]
    have hxCodim : Face.CodimOne
        (nondegenerateFaceEquiv x.1.toN)
        (nondegenerateFaceEquiv ((pairing hzero).p y).1.toN) :=
      codimOne_of_le_of_dimension hxy.2.le hdimUpper
    have hyTypedPair : Face.pairUpper
        (nondegenerateFaceEquiv y.1.toN) =
        some (nondegenerateFaceEquiv ((pairing hzero).p y).1.toN) :=
      (pairUpper_eq_some_iff).1 hyPair
    have hxyTypedNe : nondegenerateFaceEquiv x.1.toN ≠
        nondegenerateFaceEquiv y.1.toN := by
      intro heq
      apply hxy.1
      apply Subtype.ext
      apply (SSet.Subcomplex.N.ext_iff _ _).2
      exact (nondegenerateFaceEquiv
        (p:=p) (q:=q) (r:=r)).injective heq
    have hstep : Face.GradientStep
        (nondegenerateFaceEquiv y.1.toN)
        (nondegenerateFaceEquiv x.1.toN) :=
      ⟨nondegenerateFaceEquiv ((pairing hzero).p y).1.toN,
        hyTypedPair, hxCodim, hxyTypedNe,
        (pairUpper_isSome_iff x.1.toN).1 hxLower⟩
    exact Face.gradientStep_rank_lt hstep

instance pairing_isRegular
    (hzero : p = 0 ∨ q = 0 ∨ r = 0) :
    (pairing hzero).IsRegular :=
  (pairingWeakRank hzero).isRegular

/-- In the zero-top-cell cases, the root inclusion is strong anodyne. -/
theorem root_inclusion_strongAnodyne
    (hzero : p = 0 ∨ q = 0 ∨ r = 0) :
    SSet.strongAnodyneExtensions
      (rootSubcomplex (p:=p) (q:=q) (r:=r)).ι :=
  (pairing hzero).strongAnodyneExtensions

/-- In the zero-top-cell cases, the root inclusion is an anodyne
extension. -/
theorem root_inclusion_anodyne
    (hzero : p = 0 ∨ q = 0 ∨ r = 0) :
    SSet.anodyneExtensions
      (rootSubcomplex (p:=p) (q:=q) (r:=r)).ι :=
  (pairing hzero).anodyneExtensions

/-- Numeric form of the strong-anodyne boundary. -/
theorem root_inclusion_strongAnodyne_of_topCount_zero
    (hzero : p * q * r = 0) :
    SSet.strongAnodyneExtensions
      (rootSubcomplex (p:=p) (q:=q) (r:=r)).ι := by
  rw [Nat.mul_eq_zero] at hzero
  rcases hzero with hpq | hr
  · rw [Nat.mul_eq_zero] at hpq
    rcases hpq with hp | hq
    · exact root_inclusion_strongAnodyne (Or.inl hp)
    · exact root_inclusion_strongAnodyne (Or.inr (Or.inl hq))
  · exact root_inclusion_strongAnodyne (Or.inr (Or.inr hr))

/-- Numeric form of the anodyne boundary. -/
theorem root_inclusion_anodyne_of_topCount_zero
    (hzero : p * q * r = 0) :
    SSet.anodyneExtensions
      (rootSubcomplex (p:=p) (q:=q) (r:=r)).ι := by
  rw [Nat.mul_eq_zero] at hzero
  rcases hzero with hpq | hr
  · rw [Nat.mul_eq_zero] at hpq
    rcases hpq with hp | hq
    · exact root_inclusion_anodyne (Or.inl hp)
    · exact root_inclusion_anodyne (Or.inr (Or.inl hq))
  · exact root_inclusion_anodyne (Or.inr (Or.inr hr))

end D0.Topology.GenericTripartiteDegeneratePairing
