import D0.Geometry.ArchiveCARRelations
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.Ring.Parity
import Mathlib.GroupTheory.Perm.Basic
import Mathlib.Tactic

/-!
# Role permutation action on the archive Fock carrier

`ArchiveFockState` is `Role → Bool`.  A role permutation acts by transporting
occupation labels.  The plain transport preserves degree and is a group
action.  The Jordan-Wigner operators use the fixed role order
`roleOrderIndex`, with `A, B, C, D` in that sequence.  The signed transport
multiplies by the parity of occupied inversions of that same order.
`fermionSign` is `1` on the identity and satisfies the cocycle law, so the
signed transport is a group homomorphism.  Conjugation by it sends `c_r` to
`c_{σ r}`, `c_r†` to `c_{σ r}†`, and `c_s† c_r` to `c_{σ s}† c_{σ r}` for every
`Equiv.Perm Role`.  The three adjacent transpositions are the special cases
`swapAB`, `swapBC`, and `swapCD`.

Dimension `70` counts every degree-preserving endomorphism.  This file does
not prove that the CAR bilinears span that algebra.
-/

namespace D0.Geometry.RoleFockPermutation

open D0
open D0.Geometry

/-- Occupation transported along a role permutation: the label now at `r`
is the label previously at `σ⁻¹ r`. -/
def transportState (σ : Equiv.Perm Role) (s : ArchiveFockState) : ArchiveFockState :=
  fun r => s (σ.symm r)

theorem transportState_one (s : ArchiveFockState) :
    transportState 1 s = s := by
  funext r
  rfl

theorem transportState_mul (σ τ : Equiv.Perm Role) (s : ArchiveFockState) :
    transportState (σ * τ) s = transportState σ (transportState τ s) := by
  funext r
  simp [transportState, Equiv.Perm.mul_def]

theorem transportState_leftInverse (σ : Equiv.Perm Role) :
    Function.LeftInverse (transportState σ.symm) (transportState σ) := by
  intro s
  funext r
  unfold transportState
  rw [Equiv.symm_symm]
  exact congrArg s (σ.symm_apply_apply r)

theorem transportState_bijective (σ : Equiv.Perm Role) :
    Function.Bijective (transportState σ) :=
  ⟨(transportState_leftInverse σ).injective,
   (transportState_leftInverse σ.symm).surjective⟩

theorem fockDegree_transport (σ : Equiv.Perm Role) (s : ArchiveFockState) :
    fockDegree (transportState σ s) = fockDegree s := by
  unfold fockDegree transportState
  apply Finset.card_bij (fun r _ => σ.symm r)
  · intro r hr
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hr ⊢
    simpa using hr
  · intro r₁ hr₁ r₂ hr₂ h
    exact σ.symm.injective h
  · intro t ht
    refine ⟨σ t, ?_, σ.symm_apply_apply t⟩
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at ht ⊢
    simpa [Equiv.apply_symm_apply] using ht

/-- Pairs of occupied roles whose order is reversed by `σ`. -/
def occupiedInversionCount (σ : Equiv.Perm Role) (s : ArchiveFockState) : ℕ :=
  (Finset.univ.filter fun p : Role × Role =>
    s p.1 = true ∧ s p.2 = true ∧
      roleOrderIndex p.1 < roleOrderIndex p.2 ∧
      roleOrderIndex (σ p.2) < roleOrderIndex (σ p.1)).card

def fermionSign (σ : Equiv.Perm Role) (s : ArchiveFockState) : ℤ :=
  if occupiedInversionCount σ s % 2 = 0 then 1 else -1

/-- Signed permutation matrix on occupation states. -/
def signedTransport (σ : Equiv.Perm Role)
    (bra ket : ArchiveFockState) : ℤ :=
  if bra = transportState σ ket then fermionSign σ ket else 0

theorem signedTransport_one (bra ket : ArchiveFockState) :
    signedTransport 1 bra ket = fockIdentityInt bra ket := by
  classical
  unfold signedTransport fermionSign occupiedInversionCount fockIdentityInt
  by_cases h : bra = ket
  · subst h
    have hempty : (Finset.univ.filter fun p : Role × Role =>
        bra p.1 = true ∧ bra p.2 = true ∧
          roleOrderIndex p.1 < roleOrderIndex p.2 ∧
          roleOrderIndex p.2 < roleOrderIndex p.1) = ∅ := by
      apply Finset.filter_eq_empty_iff.mpr
      intro p _ hp
      exact lt_asymm hp.2.2.1 hp.2.2.2
    simp [transportState_one, hempty, Finset.card_empty]
  · simp [transportState_one, h]

def fockMatMul (M N : ArchiveFockState → ArchiveFockState → ℤ)
    (bra ket : ArchiveFockState) : ℤ :=
  ∑ mid : ArchiveFockState, M bra mid * N mid ket

/-- The three adjacent transpositions of the fixed Jordan-Wigner order. -/
def swapAB : Equiv.Perm Role := Equiv.swap A B
def swapBC : Equiv.Perm Role := Equiv.swap B C
def swapCD : Equiv.Perm Role := Equiv.swap C D

/-! ## Inversion cocycle

`fermionSign` stays the parity of `occupiedInversionCount`.  The pair factor below
is only the multiplicative form of that same parity.
-/

lemma roleOrderIndex_injective : Function.Injective roleOrderIndex := by
  intro r s hrs
  match r, s with
  | (a, b), (c, d) =>
      fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
        simp [roleOrderIndex, A, B, C, D] at hrs ⊢

lemma roleOrderIndex_lt_of_ne {p q : Role} (hpq : p ≠ q) :
    roleOrderIndex p < roleOrderIndex q ∨ roleOrderIndex q < roleOrderIndex p := by
  rcases lt_trichotomy (roleOrderIndex p) (roleOrderIndex q) with hlt | heq | hgt
  · exact Or.inl hlt
  · exact absurd (roleOrderIndex_injective heq) hpq
  · exact Or.inr hgt

lemma even_iff_mod_two_eq_zero (n : ℕ) : Even n ↔ n % 2 = 0 := by
  rw [← Nat.not_odd_iff_even, Nat.not_odd_iff]

lemma fermionSign_eq_neg_one_pow (σ : Equiv.Perm Role) (s : ArchiveFockState) :
    fermionSign σ s = (-1) ^ occupiedInversionCount σ s := by
  unfold fermionSign
  rw [neg_one_pow_eq_ite]
  by_cases h : occupiedInversionCount σ s % 2 = 0
  · have he : Even (occupiedInversionCount σ s) := (even_iff_mod_two_eq_zero _).mpr h
    simp [h, he]
  · have he : ¬ Even (occupiedInversionCount σ s) := by
      intro he
      exact h ((even_iff_mod_two_eq_zero _).mp he)
    simp [h, he]

lemma fermionSign_sq (σ : Equiv.Perm Role) (s : ArchiveFockState) :
    fermionSign σ s * fermionSign σ s = 1 := by
  unfold fermionSign
  split_ifs <;> norm_num

lemma fermionSign_one (s : ArchiveFockState) : fermionSign 1 s = 1 := by
  have h := signedTransport_one s s
  simpa [signedTransport, transportState_one, fockIdentityInt] using h

/-- Occupied pairs in the fixed Jordan-Wigner order. -/
def orderedOccupiedPairs (s : ArchiveFockState) : Finset (Role × Role) :=
  Finset.univ.filter fun p =>
    s p.1 = true ∧ s p.2 = true ∧ roleOrderIndex p.1 < roleOrderIndex p.2

/-- Sign of the ordered pair `(p, q)` after `σ`.  Equal indices do not occur for `p ≠ q`. -/
def imageOrderSign (σ : Equiv.Perm Role) (p q : Role) : ℤ :=
  if roleOrderIndex (σ q) < roleOrderIndex (σ p) then -1 else 1

/-- The rank-ordered pair.  For equal ranks this returns `(q, p)`. -/
def sortPair (p q : Role) : Role × Role :=
  if roleOrderIndex p < roleOrderIndex q then (p, q) else (q, p)

lemma occupiedInversionCount_eq (σ : Equiv.Perm Role) (s : ArchiveFockState) :
    occupiedInversionCount σ s =
      ((orderedOccupiedPairs s).filter fun p =>
        roleOrderIndex (σ p.2) < roleOrderIndex (σ p.1)).card := by
  unfold occupiedInversionCount orderedOccupiedPairs
  rw [Finset.filter_filter]
  refine congrArg Finset.card ?_
  ext p
  simp only [Finset.mem_filter, Finset.mem_univ, true_and]
  tauto

lemma prod_ite_neg_one {α : Type*} [DecidableEq α] (s : Finset α) (pred : α → Prop)
    [DecidablePred pred] :
    (∏ a ∈ s, if pred a then (-1 : ℤ) else 1) = (-1) ^ (s.filter pred).card := by
  induction s using Finset.induction with
  | empty => simp
  | @insert a s ha ih =>
      by_cases hpa : pred a
      · have hmem : a ∉ s.filter pred := by simp [ha]
        rw [Finset.prod_insert ha, if_pos hpa, Finset.filter_insert, if_pos hpa,
          Finset.card_insert_of_notMem hmem, pow_succ, ih]
        ring
      · rw [Finset.prod_insert ha, if_neg hpa, Finset.filter_insert, if_neg hpa, ih, one_mul]

lemma fermionSign_eq_prod (σ : Equiv.Perm Role) (s : ArchiveFockState) :
    fermionSign σ s =
      ∏ p ∈ orderedOccupiedPairs s, imageOrderSign σ p.1 p.2 := by
  rw [fermionSign_eq_neg_one_pow, occupiedInversionCount_eq, ← prod_ite_neg_one]
  refine Finset.prod_congr rfl fun p _ => ?_
  simp [imageOrderSign]

lemma imageOrderSign_mul (σ τ : Equiv.Perm Role) (p q : Role) :
    imageOrderSign (σ * τ) p q = imageOrderSign σ (τ p) (τ q) := by
  simp [imageOrderSign, Equiv.Perm.mul_def]

lemma imageOrderSign_anticomm (σ : Equiv.Perm Role) {p q : Role} (hpq : p ≠ q) :
    imageOrderSign σ p q = -imageOrderSign σ q p := by
  have hne : roleOrderIndex (σ p) ≠ roleOrderIndex (σ q) := by
    intro h
    exact hpq (σ.injective (roleOrderIndex_injective h))
  by_cases h1 : roleOrderIndex (σ q) < roleOrderIndex (σ p)
  · have h2 : ¬ roleOrderIndex (σ p) < roleOrderIndex (σ q) := lt_asymm h1
    simp [imageOrderSign, h1, h2]
  · have h2 : roleOrderIndex (σ p) < roleOrderIndex (σ q) :=
      (roleOrderIndex_lt_of_ne (σ.injective.ne hpq)).resolve_right h1
    simp [imageOrderSign, h1, h2]

lemma imageOrderSign_mul_sort (σ τ : Equiv.Perm Role) {p q : Role}
    (hpq : roleOrderIndex p < roleOrderIndex q) :
    imageOrderSign (σ * τ) p q =
      imageOrderSign τ p q *
        imageOrderSign σ (sortPair (τ p) (τ q)).1 (sortPair (τ p) (τ q)).2 := by
  have hpne : p ≠ q := by
    intro h
    rw [h] at hpq
    exact lt_irrefl _ hpq
  have hτ : τ p ≠ τ q := fun h => hpne (τ.injective h)
  rw [imageOrderSign_mul]
  by_cases hord : roleOrderIndex (τ p) < roleOrderIndex (τ q)
  · have hsign : imageOrderSign τ p q = 1 := by
      simp [imageOrderSign, lt_asymm hord]
    simp [sortPair, hord, hsign]
  · have hrev : roleOrderIndex (τ q) < roleOrderIndex (τ p) :=
      (roleOrderIndex_lt_of_ne hτ).resolve_left hord
    have hsign : imageOrderSign τ p q = -1 := by
      simp [imageOrderSign, hrev]
    simp [sortPair, hord, hsign, imageOrderSign_anticomm σ (Ne.symm hτ)]

lemma sortPair_ordered {p q : Role} (h : roleOrderIndex p < roleOrderIndex q) :
    sortPair p q = (p, q) := by
  simp [sortPair, h]

lemma sortPair_comm (p q : Role) : sortPair p q = sortPair q p := by
  by_cases h : roleOrderIndex p < roleOrderIndex q
  · have h' : ¬ roleOrderIndex q < roleOrderIndex p := lt_asymm h
    simp [sortPair, h, h']
  · by_cases h' : roleOrderIndex q < roleOrderIndex p
    · simp [sortPair, h, h']
    · have heq : roleOrderIndex p = roleOrderIndex q := by
        rcases lt_trichotomy (roleOrderIndex p) (roleOrderIndex q) with hlt | heq | hgt
        · exact absurd hlt h
        · exact heq
        · exact absurd hgt h'
      have hpq : p = q := roleOrderIndex_injective heq
      simp [sortPair, h, h', hpq]

lemma transport_sortPair_mem (τ : Equiv.Perm Role) (s : ArchiveFockState)
    {pq : Role × Role} (hpq : pq ∈ orderedOccupiedPairs s) :
    sortPair (τ pq.1) (τ pq.2) ∈ orderedOccupiedPairs (transportState τ s) := by
  simp only [orderedOccupiedPairs, Finset.mem_filter, Finset.mem_univ, true_and] at hpq ⊢
  obtain ⟨hp, hq, hlt⟩ := hpq
  have hne : τ pq.1 ≠ τ pq.2 := by
    intro h
    have : pq.1 ≠ pq.2 := by
      intro hrs
      rw [hrs] at hlt
      exact lt_irrefl _ hlt
    exact this (τ.injective h)
  have hocc1 : transportState τ s (τ pq.1) = true := by
    simp [transportState, hp]
  have hocc2 : transportState τ s (τ pq.2) = true := by
    simp [transportState, hq]
  rcases roleOrderIndex_lt_of_ne hne with hord | hrev
  · simpa [sortPair, hord, hocc1, hocc2] using hord
  · simpa [sortPair, show ¬ roleOrderIndex (τ pq.1) < roleOrderIndex (τ pq.2) from
      lt_asymm hrev, hocc1, hocc2] using hrev

lemma sortPair_perm (τ : Equiv.Perm Role) {p q : Role} (hne : p ≠ q) :
    sortPair (τ (sortPair p q).1) (τ (sortPair p q).2) = sortPair (τ p) (τ q) := by
  by_cases h : roleOrderIndex p < roleOrderIndex q
  · simp [sortPair_ordered h]
  · have hrev : roleOrderIndex q < roleOrderIndex p :=
      (roleOrderIndex_lt_of_ne hne).resolve_left h
    have hs : sortPair p q = (q, p) := by simp [sortPair, h]
    rw [hs]
    exact sortPair_comm (τ q) (τ p)

lemma sortPair_preimage (τ : Equiv.Perm Role) {p q : Role}
    (hpq : roleOrderIndex p < roleOrderIndex q) :
    sortPair (τ.symm (sortPair (τ p) (τ q)).1) (τ.symm (sortPair (τ p) (τ q)).2) = (p, q) := by
  have hne : τ p ≠ τ q := by
    intro h
    rw [τ.injective h] at hpq
    exact lt_irrefl _ hpq
  by_cases h : roleOrderIndex (τ p) < roleOrderIndex (τ q)
  · simp [sortPair_ordered h, sortPair_ordered hpq, Equiv.symm_apply_apply]
  · have hrev : roleOrderIndex (τ q) < roleOrderIndex (τ p) :=
      (roleOrderIndex_lt_of_ne hne).resolve_left h
    have hs : sortPair (τ p) (τ q) = (τ q, τ p) := by simp [sortPair, h]
    rw [hs]
    have hcomm : sortPair q p = sortPair p q := sortPair_comm q p
    simpa [Equiv.symm_apply_apply, sortPair_ordered hpq] using hcomm

lemma prod_imageOrderSign_transport (σ τ : Equiv.Perm Role) (s : ArchiveFockState) :
    (∏ pq ∈ orderedOccupiedPairs (transportState τ s), imageOrderSign σ pq.1 pq.2) =
      ∏ pq ∈ orderedOccupiedPairs s,
        imageOrderSign σ (sortPair (τ pq.1) (τ pq.2)).1
          (sortPair (τ pq.1) (τ pq.2)).2 := by
  classical
  symm
  refine Finset.prod_bij'
    (fun pq _ => sortPair (τ pq.1) (τ pq.2))
    (fun pq _ => sortPair (τ.symm pq.1) (τ.symm pq.2))
    (fun pq hpq => transport_sortPair_mem τ s hpq)
    ?_ ?_ ?_ (fun _ _ => rfl)
  · intro b hb
    simp only [orderedOccupiedPairs, Finset.mem_filter, Finset.mem_univ, true_and] at hb ⊢
    obtain ⟨hb1, hb2, hlt⟩ := hb
    have hp : s (τ.symm b.1) = true := by simpa [transportState] using hb1
    have hq : s (τ.symm b.2) = true := by simpa [transportState] using hb2
    have hne : τ.symm b.1 ≠ τ.symm b.2 := by
      intro h
      have : b.1 = b.2 := by simpa using congrArg τ h
      rw [this] at hlt
      exact lt_irrefl _ hlt
    by_cases hord : roleOrderIndex (τ.symm b.1) < roleOrderIndex (τ.symm b.2)
    · simp [sortPair, hord, hp, hq]
    · have hrev : roleOrderIndex (τ.symm b.2) < roleOrderIndex (τ.symm b.1) :=
        (roleOrderIndex_lt_of_ne hne).resolve_left hord
      simp [sortPair, hord, hp, hq, hrev]
  · intro pq hpq
    simp only [orderedOccupiedPairs, Finset.mem_filter, Finset.mem_univ, true_and] at hpq
    exact sortPair_preimage τ hpq.2.2
  · intro b hb
    simp only [orderedOccupiedPairs, Finset.mem_filter, Finset.mem_univ, true_and] at hb
    obtain ⟨_, _, hlt⟩ := hb
    have hne : τ.symm b.1 ≠ τ.symm b.2 := by
      intro h
      have : b.1 = b.2 := by simpa using congrArg τ h
      rw [this] at hlt
      exact lt_irrefl _ hlt
    have hsort := sortPair_perm τ hne
    have hord : sortPair b.1 b.2 = b := sortPair_ordered hlt
    calc
      sortPair (τ (sortPair (τ.symm b.1) (τ.symm b.2)).1)
          (τ (sortPair (τ.symm b.1) (τ.symm b.2)).2)
          = sortPair (τ (τ.symm b.1)) (τ (τ.symm b.2)) := hsort
      _ = sortPair b.1 b.2 := by simp [Equiv.apply_symm_apply]
      _ = b := hord

/-- Cocycle law `ε(σ τ, S) = ε(σ, τ S) ε(τ, S)`. -/
theorem fermionSign_mul (σ τ : Equiv.Perm Role) (s : ArchiveFockState) :
    fermionSign (σ * τ) s =
      fermionSign σ (transportState τ s) * fermionSign τ s := by
  rw [fermionSign_eq_prod, fermionSign_eq_prod, fermionSign_eq_prod, prod_imageOrderSign_transport]
  have hfac : ∀ pq ∈ orderedOccupiedPairs s,
      imageOrderSign (σ * τ) pq.1 pq.2 =
        imageOrderSign σ (sortPair (τ pq.1) (τ pq.2)).1 (sortPair (τ pq.1) (τ pq.2)).2 *
          imageOrderSign τ pq.1 pq.2 := by
    intro pq hpq
    have hlt : roleOrderIndex pq.1 < roleOrderIndex pq.2 := by
      simp only [orderedOccupiedPairs, Finset.mem_filter, Finset.mem_univ, true_and] at hpq
      exact hpq.2.2
    rw [imageOrderSign_mul_sort σ τ hlt, mul_comm]
  rw [Finset.prod_congr rfl hfac, Finset.prod_mul_distrib]

lemma perm_mul_symm (σ : Equiv.Perm Role) : σ * σ.symm = 1 := by
  refine Equiv.ext fun x => ?_
  simp [Equiv.Perm.mul_def]

lemma perm_symm_mul (σ : Equiv.Perm Role) : σ.symm * σ = 1 := by
  refine Equiv.ext fun x => ?_
  simp [Equiv.Perm.mul_def]

lemma fermionSign_symm_transport (σ : Equiv.Perm Role) (s : ArchiveFockState) :
    fermionSign σ.symm (transportState σ s) = fermionSign σ s := by
  have h := fermionSign_mul σ.symm σ s
  rw [perm_symm_mul, fermionSign_one] at h
  have hs := fermionSign_sq σ s
  calc
    fermionSign σ.symm (transportState σ s)
        = fermionSign σ.symm (transportState σ s) * (fermionSign σ s * fermionSign σ s) := by
          rw [hs, mul_one]
    _ = (fermionSign σ.symm (transportState σ s) * fermionSign σ s) * fermionSign σ s := by
          rw [mul_assoc]
    _ = 1 * fermionSign σ s := by rw [h]
    _ = fermionSign σ s := by rw [one_mul]

lemma neg_one_pow_eq_of_mod_eq {a b : ℕ} (h : a % 2 = b % 2) :
    (-1 : ℤ) ^ a = (-1) ^ b := by
  apply neg_one_pow_congr
  rw [even_iff_mod_two_eq_zero, even_iff_mod_two_eq_zero, h]

lemma jwSignInt_eq_neg_one_pow (s : ArchiveFockState) (r : Role) :
    jwSignInt s r = (-1) ^ precedingOccupationCount s r := by
  unfold jwSignInt
  rw [neg_one_pow_eq_ite]
  by_cases h : precedingOccupationCount s r % 2 = 0
  · have he : Even (precedingOccupationCount s r) := (even_iff_mod_two_eq_zero _).mpr h
    simp [h, he]
  · have he : ¬ Even (precedingOccupationCount s r) := by
      intro he
      exact h ((even_iff_mod_two_eq_zero _).mp he)
    simp [h, he]

lemma card_filter_eq_sum {α : Type*} [DecidableEq α] (s : Finset α) (pred : α → Prop)
    [DecidablePred pred] :
    (s.filter pred).card = ∑ a ∈ s, if pred a then (1 : ℕ) else 0 := by
  induction s using Finset.induction with
  | empty => simp
  | @insert a s ha ih =>
      by_cases hpa : pred a
      · have hmem : a ∉ s.filter pred := by simp [ha]
        rw [Finset.filter_insert, if_pos hpa, Finset.card_insert_of_notMem hmem,
          Finset.sum_insert ha, if_pos hpa, ih]
        exact Nat.add_comm _ _
      · rw [Finset.filter_insert, if_neg hpa, Finset.sum_insert ha, if_neg hpa, ih, Nat.zero_add]

/-- Roles occupied by `ket`, excluding `r`. -/
def occupiedExcept (ket : ArchiveFockState) (r : Role) : Finset Role :=
  Finset.univ.filter fun p => p ≠ r ∧ ket p = true

/-- Occupied modes whose order relative to `r` is reversed by `σ`. -/
def flipRoles (σ : Equiv.Perm Role) (ket : ArchiveFockState) (r : Role) : Finset Role :=
  Finset.univ.filter fun p =>
    p ≠ r ∧ ket p = true ∧
      decide (roleOrderIndex p < roleOrderIndex r) !=
        decide (roleOrderIndex (σ p) < roleOrderIndex (σ r))

def clearRole (ket : ArchiveFockState) (r : Role) : ArchiveFockState :=
  fun s => if s = r then false else ket s

def inversionPairs (σ : Equiv.Perm Role) (s : ArchiveFockState) : Finset (Role × Role) :=
  (orderedOccupiedPairs s).filter fun p =>
    roleOrderIndex (σ p.2) < roleOrderIndex (σ p.1)

def pairOfFlip (r p : Role) : Role × Role :=
  if roleOrderIndex p < roleOrderIndex r then (p, r) else (r, p)

def otherRole (r : Role) (p : Role × Role) : Role :=
  if p.1 = r then p.2 else p.1

lemma indicator_xor (p q : Prop) [Decidable p] [Decidable q] :
    (if decide p != decide q then (1 : ℕ) else 0) + 2 * (if p ∧ q then 1 else 0) =
      (if p then 1 else 0) + (if q then 1 else 0) := by
  cases hp : decide p <;> cases hq : decide q
  · have hnp : ¬ p := of_decide_eq_false hp
    have hnq : ¬ q := of_decide_eq_false hq
    simp [hp, hq, hnp, hnq]
  · have hnp : ¬ p := of_decide_eq_false hp
    have hq' : q := of_decide_eq_true hq
    simp [hp, hq, hnp, hq']
  · have hp' : p := of_decide_eq_true hp
    have hnq : ¬ q := of_decide_eq_false hq
    simp [hp, hq, hp', hnq]
  · have hp' : p := of_decide_eq_true hp
    have hq' : q := of_decide_eq_true hq
    simp [hp, hq, hp', hq']

lemma flipRoles_card_add (σ : Equiv.Perm Role) (ket : ArchiveFockState) (r : Role) :
    (flipRoles σ ket r).card +
        2 * ((occupiedExcept ket r).filter fun p =>
          roleOrderIndex p < roleOrderIndex r ∧
            roleOrderIndex (σ p) < roleOrderIndex (σ r)).card =
      ((occupiedExcept ket r).filter fun p => roleOrderIndex p < roleOrderIndex r).card +
        ((occupiedExcept ket r).filter fun p =>
          roleOrderIndex (σ p) < roleOrderIndex (σ r)).card := by
  have hflip : flipRoles σ ket r =
      (occupiedExcept ket r).filter fun p =>
        decide (roleOrderIndex p < roleOrderIndex r) !=
          decide (roleOrderIndex (σ p) < roleOrderIndex (σ r)) := by
    ext p
    simp only [flipRoles, occupiedExcept, Finset.mem_filter, Finset.mem_univ, true_and]
    tauto
  rw [hflip, card_filter_eq_sum, card_filter_eq_sum, card_filter_eq_sum, card_filter_eq_sum,
    Finset.mul_sum, ← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun p _ => ?_
  exact indicator_xor (roleOrderIndex p < roleOrderIndex r)
    (roleOrderIndex (σ p) < roleOrderIndex (σ r))

lemma precedingOccupationCount_except (ket : ArchiveFockState) (r : Role) :
    precedingOccupationCount ket r =
      ((occupiedExcept ket r).filter fun p => roleOrderIndex p < roleOrderIndex r).card := by
  unfold precedingOccupationCount occupiedExcept
  refine congrArg Finset.card ?_
  ext p
  simp only [Finset.mem_filter, Finset.mem_univ, true_and]
  constructor
  · intro h
    refine ⟨⟨?_, h.2⟩, h.1⟩
    intro hpr
    rw [hpr] at h
    exact lt_irrefl _ h.1
  · intro h
    exact ⟨h.2, h.1.2⟩

lemma precedingOccupationCount_transport (σ : Equiv.Perm Role) (ket : ArchiveFockState) (r : Role) :
    precedingOccupationCount (transportState σ ket) (σ r) =
      ((occupiedExcept ket r).filter fun p =>
        roleOrderIndex (σ p) < roleOrderIndex (σ r)).card := by
  unfold precedingOccupationCount
  apply Finset.card_bij (fun t _ => σ.symm t)
  · intro t ht
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, occupiedExcept, transportState] at ht ⊢
    refine ⟨⟨?_, ht.2⟩, ?_⟩
    · intro htr
      have htσ : t = σ r := by
        simpa [htr] using (σ.apply_symm_apply t).symm
      rw [htσ] at ht
      exact lt_irrefl _ ht.1
    · simpa [Equiv.apply_symm_apply] using ht.1
  · intro t₁ _ t₂ _ h
    exact σ.symm.injective h
  · intro p hp
    refine ⟨σ p, ?_, σ.symm_apply_apply p⟩
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, occupiedExcept, transportState] at hp ⊢
    exact ⟨hp.2, by simpa [Equiv.symm_apply_apply] using hp.1.2⟩

lemma neg_one_pow_flip (σ : Equiv.Perm Role) (ket : ArchiveFockState) (r : Role) :
    (-1) ^ (flipRoles σ ket r).card =
      jwSignInt ket r * jwSignInt (transportState σ ket) (σ r) := by
  rw [jwSignInt_eq_neg_one_pow, jwSignInt_eq_neg_one_pow, precedingOccupationCount_except,
    precedingOccupationCount_transport]
  have hcard := flipRoles_card_add σ ket r
  have hmod : (flipRoles σ ket r).card % 2 =
      (((occupiedExcept ket r).filter fun p => roleOrderIndex p < roleOrderIndex r).card +
        ((occupiedExcept ket r).filter fun p =>
          roleOrderIndex (σ p) < roleOrderIndex (σ r)).card) % 2 := by
    have h2 : ((flipRoles σ ket r).card + 2 *
        ((occupiedExcept ket r).filter fun p =>
          roleOrderIndex p < roleOrderIndex r ∧
            roleOrderIndex (σ p) < roleOrderIndex (σ r)).card) % 2 =
        (flipRoles σ ket r).card % 2 := by omega
    rw [← h2, hcard]
  rw [neg_one_pow_eq_of_mod_eq hmod, pow_add]

lemma clearRole_ne (ket : ArchiveFockState) {r s : Role} (hs : s ≠ r) :
    clearRole ket r s = ket s := by
  simp [clearRole, hs]

lemma ordered_clear (ket : ArchiveFockState) (r : Role) (hr : ket r = true) :
    orderedOccupiedPairs (clearRole ket r) =
      (orderedOccupiedPairs ket).filter fun p => p.1 ≠ r ∧ p.2 ≠ r := by
  ext p
  simp only [orderedOccupiedPairs, clearRole, Finset.mem_filter, Finset.mem_univ, true_and]
  constructor
  · intro h
    have h1 : p.1 ≠ r := by
      intro hr1
      simp [hr1] at h
    have h2 : p.2 ≠ r := by
      intro hr2
      simp [hr2] at h
    simp [h1, h2] at h
    exact ⟨⟨h.1, h.2.1, h.2.2⟩, h1, h2⟩
  · intro h
    rcases h with ⟨⟨h1, h2, hlt⟩, hne1, hne2⟩
    simp [hne1, hne2, h1, h2, hlt]

lemma inversion_clear_eq (σ : Equiv.Perm Role) (ket : ArchiveFockState) (r : Role)
    (hr : ket r = true) :
    inversionPairs σ (clearRole ket r) =
      (inversionPairs σ ket).filter fun p => p.1 ≠ r ∧ p.2 ≠ r := by
  unfold inversionPairs
  rw [ordered_clear ket r hr]
  ext p
  simp only [Finset.mem_filter]
  constructor
  · intro h
    exact ⟨⟨h.1.1, h.2⟩, h.1.2⟩
  · intro h
    exact ⟨⟨h.1.1, h.2⟩, h.1.2⟩

lemma inversion_card_split (σ : Equiv.Perm Role) (ket : ArchiveFockState) (r : Role)
    (hr : ket r = true) :
    (inversionPairs σ ket).card =
      (inversionPairs σ (clearRole ket r)).card +
        ((inversionPairs σ ket).filter fun p => p.1 = r ∨ p.2 = r).card := by
  have hnot :
      ((inversionPairs σ ket).filter fun p => ¬ (p.1 = r ∨ p.2 = r)) =
        ((inversionPairs σ ket).filter fun p => p.1 ≠ r ∧ p.2 ≠ r) := by
    ext p
    simp only [Finset.mem_filter, Finset.mem_univ, not_or, true_and]
  have hclear := inversion_clear_eq σ ket r hr
  have hadd := Finset.card_filter_add_card_filter_not
    (s := inversionPairs σ ket) (fun p : Role × Role => p.1 = r ∨ p.2 = r)
  rw [hnot, ← hclear] at hadd
  exact hadd.symm.trans (add_comm _ _)

lemma occupiedInversionCount_inversionPairs (σ : Equiv.Perm Role) (s : ArchiveFockState) :
    occupiedInversionCount σ s = (inversionPairs σ s).card := by
  rw [occupiedInversionCount_eq]
  rfl

lemma pairOfFlip_other_touching (σ : Equiv.Perm Role) (ket : ArchiveFockState) (r : Role)
    {p : Role × Role}
    (hp : p ∈ (inversionPairs σ ket).filter fun q => q.1 = r ∨ q.2 = r) :
    pairOfFlip r (otherRole r p) = p := by
  simp only [inversionPairs, orderedOccupiedPairs, Finset.mem_filter, Finset.mem_univ,
    true_and] at hp
  rcases hp.2 with h1 | h2
  · have hlt : roleOrderIndex r < roleOrderIndex p.2 := by simpa [h1] using hp.1.1.2.2
    have hother : otherRole r p = p.2 := by simp [otherRole, h1]
    have hpair : pairOfFlip r p.2 = (r, p.2) := by
      simp [pairOfFlip, lt_asymm hlt]
    have hpq : p = (p.1, p.2) := rfl
    rw [hother, hpair, hpq, h1]
  · have hlt : roleOrderIndex p.1 < roleOrderIndex r := by simpa [h2] using hp.1.1.2.2
    have hne : p.1 ≠ r := by
      intro h
      rw [h] at hlt
      exact lt_irrefl _ hlt
    have hother : otherRole r p = p.1 := by simp [otherRole, hne]
    have hpair : pairOfFlip r p.1 = (p.1, r) := by simp [pairOfFlip, hlt]
    rw [hother, hpair, show p = (p.1, p.2) from rfl, h2]

lemma other_mem_flip (σ : Equiv.Perm Role) (ket : ArchiveFockState) (r : Role)
    (_hr : ket r = true) {p : Role × Role}
    (hp : p ∈ (inversionPairs σ ket).filter fun q => q.1 = r ∨ q.2 = r) :
    otherRole r p ∈ flipRoles σ ket r := by
  simp only [inversionPairs, orderedOccupiedPairs, flipRoles, Finset.mem_filter, Finset.mem_univ,
    true_and] at hp ⊢
  rcases hp.2 with h1 | h2
  · have hlt : roleOrderIndex r < roleOrderIndex p.2 := by simpa [h1] using hp.1.1.2.2
    have hinv : roleOrderIndex (σ p.2) < roleOrderIndex (σ r) := by simpa [h1] using hp.1.2
    have hne : p.2 ≠ r := by
      intro h
      rw [h] at hlt
      exact lt_irrefl _ hlt
    have hocc : ket p.2 = true := by simpa [h1] using hp.1.1.2.1
    have hbefore : ¬ roleOrderIndex p.2 < roleOrderIndex r := lt_asymm hlt
    simp [otherRole, h1, hne, hocc, hbefore, hinv, decide_eq_false hbefore, decide_eq_true hinv]
  · have hlt : roleOrderIndex p.1 < roleOrderIndex r := by simpa [h2] using hp.1.1.2.2
    have hinv : roleOrderIndex (σ r) < roleOrderIndex (σ p.1) := by simpa [h2] using hp.1.2
    have hne : p.1 ≠ r := by
      intro h
      rw [h] at hlt
      exact lt_irrefl _ hlt
    have hocc : ket p.1 = true := by simpa [h2] using hp.1.1.1
    have himage : ¬ roleOrderIndex (σ p.1) < roleOrderIndex (σ r) := lt_asymm hinv
    simp [otherRole, h2, hne, hocc, hlt, himage, decide_eq_true hlt, decide_eq_false himage]

lemma touching_of_flip (σ : Equiv.Perm Role) (ket : ArchiveFockState) (r : Role)
    (hr : ket r = true) {p : Role} (hp : p ∈ flipRoles σ ket r) :
    pairOfFlip r p ∈ (inversionPairs σ ket).filter fun q => q.1 = r ∨ q.2 = r := by
  simp only [flipRoles, inversionPairs, orderedOccupiedPairs, Finset.mem_filter, Finset.mem_univ,
    true_and] at hp ⊢
  obtain ⟨hne, hocc, hxor⟩ := hp
  by_cases hbefore : roleOrderIndex p < roleOrderIndex r
  · have himage : ¬ roleOrderIndex (σ p) < roleOrderIndex (σ r) := by
      intro himage
      have : decide (roleOrderIndex p < roleOrderIndex r) =
          decide (roleOrderIndex (σ p) < roleOrderIndex (σ r)) := by
        simp [decide_eq_true hbefore, decide_eq_true himage]
      simp [this] at hxor
    have hinv : roleOrderIndex (σ r) < roleOrderIndex (σ p) :=
      (roleOrderIndex_lt_of_ne (by
        intro h
        exact hne (σ.injective h))).resolve_left himage
    simp [pairOfFlip, hbefore, hr, hocc, hinv]
  · have hrev : roleOrderIndex r < roleOrderIndex p :=
      (roleOrderIndex_lt_of_ne hne).resolve_left hbefore
    have himage : roleOrderIndex (σ p) < roleOrderIndex (σ r) := by
      by_contra himage
      have hdec : decide (roleOrderIndex p < roleOrderIndex r) =
          decide (roleOrderIndex (σ p) < roleOrderIndex (σ r)) := by
        simp [decide_eq_false hbefore, decide_eq_false himage]
      simp [hdec] at hxor
    simp [pairOfFlip, hbefore, hrev, hr, hocc, himage]

lemma other_pairOfFlip (r p : Role) (hp : p ≠ r) : otherRole r (pairOfFlip r p) = p := by
  by_cases h : roleOrderIndex p < roleOrderIndex r
  · simp [pairOfFlip, otherRole, h, hp]
  · have hne : ¬ p = r := hp
    simp [pairOfFlip, otherRole, h]

lemma touching_inversion_card (σ : Equiv.Perm Role) (ket : ArchiveFockState) (r : Role)
    (hr : ket r = true) :
    ((inversionPairs σ ket).filter fun p => p.1 = r ∨ p.2 = r).card =
      (flipRoles σ ket r).card := by
  apply Finset.card_bij (fun p _ => otherRole r p)
  · intro p hp
    exact other_mem_flip σ ket r hr hp
  · intro p hp q hq hother
    rw [← pairOfFlip_other_touching σ ket r hp, ← pairOfFlip_other_touching σ ket r hq, hother]
  · intro p hp
    have hpne : p ≠ r := by
      intro hpr
      simpa [flipRoles, Finset.mem_filter, hpr] using hp
    exact ⟨pairOfFlip r p, touching_of_flip σ ket r hr hp, other_pairOfFlip r p hpne⟩

lemma fermionSign_clear (σ : Equiv.Perm Role) (ket : ArchiveFockState) (r : Role)
    (hr : ket r = true) :
    fermionSign σ ket =
      fermionSign σ (clearRole ket r) * (-1) ^ (flipRoles σ ket r).card := by
  rw [fermionSign_eq_neg_one_pow, fermionSign_eq_neg_one_pow, occupiedInversionCount_inversionPairs,
    occupiedInversionCount_inversionPairs, inversion_card_split σ ket r hr,
    touching_inversion_card σ ket r hr, pow_add]

lemma fermionSign_clear_jw (σ : Equiv.Perm Role) (ket : ArchiveFockState) (r : Role)
    (hr : ket r = true) :
    fermionSign σ (clearRole ket r) * fermionSign σ ket * jwSignInt ket r =
      jwSignInt (transportState σ ket) (σ r) := by
  rw [fermionSign_clear σ ket r hr]
  have hsign : fermionSign σ (clearRole ket r) * fermionSign σ (clearRole ket r) = 1 :=
    fermionSign_sq σ (clearRole ket r)
  have hjw : jwSignInt ket r * jwSignInt ket r = 1 := by
    unfold jwSignInt
    split_ifs <;> norm_num
  calc
    fermionSign σ (clearRole ket r) *
        (fermionSign σ (clearRole ket r) * (-1) ^ (flipRoles σ ket r).card) * jwSignInt ket r
        = fermionSign σ (clearRole ket r) *
          (fermionSign σ (clearRole ket r) *
            (jwSignInt ket r * jwSignInt (transportState σ ket) (σ r))) * jwSignInt ket r := by
          rw [neg_one_pow_flip]
    _ = (fermionSign σ (clearRole ket r) * fermionSign σ (clearRole ket r)) *
          (jwSignInt ket r * jwSignInt ket r) *
          jwSignInt (transportState σ ket) (σ r) := by ring
    _ = jwSignInt (transportState σ ket) (σ r) := by rw [hsign, hjw]; ring

lemma transport_state_inverse_apply (σ : Equiv.Perm Role) (s : ArchiveFockState) :
    transportState σ (transportState σ.symm s) = s :=
  transportState_leftInverse σ.symm s

lemma transport_symm_apply (σ : Equiv.Perm Role) (s : ArchiveFockState) (r : Role) :
    transportState σ.symm s r = s (σ r) := by
  simp [transportState]

lemma sameOff_transport (σ : Equiv.Perm Role) (bra ket : ArchiveFockState) (r : Role) :
    ((∀ s : Role, s ≠ r → transportState σ.symm bra s = transportState σ.symm ket s) ↔
      ∀ s : Role, s ≠ σ r → bra s = ket s) := by
  constructor
  · intro h s hs
    have hpre : σ.symm s ≠ r := by
      intro hrs
      apply hs
      simpa [hrs] using (σ.apply_symm_apply s).symm
    have happ := h (σ.symm s) hpre
    simpa [transport_symm_apply, Equiv.apply_symm_apply] using happ
  · intro h s hs
    have hσ : σ s ≠ σ r := fun hsame => hs (σ.injective hsame)
    simpa [transport_symm_apply] using h (σ s) hσ

lemma annihilate_scalar (σ : Equiv.Perm Role) (r : Role) (bra ket : ArchiveFockState) :
    fermionSign σ (transportState σ.symm bra) *
        carAnnihilateInt r (transportState σ.symm bra) (transportState σ.symm ket) *
        fermionSign σ.symm ket =
      carAnnihilateInt (σ r) bra ket := by
  classical
  set bra0 := transportState σ.symm bra
  set ket0 := transportState σ.symm ket
  have hket : ket = transportState σ ket0 := by
    simpa [ket0] using (transport_state_inverse_apply σ ket).symm
  by_cases hsup : ket0 r = true ∧ bra0 r = false ∧
      ∀ s : Role, s ≠ r → bra0 s = ket0 s
  · have hbra0 : bra0 = clearRole ket0 r := by
      funext s
      by_cases hs : s = r
      · simp [clearRole, hs, hsup.2.1]
      · simp [clearRole, hs, hsup.2.2 s hs]
    have htarget : ket (σ r) = true ∧ bra (σ r) = false ∧
        ∀ s : Role, s ≠ σ r → bra s = ket s := by
      refine ⟨?_, ?_, ?_⟩
      · simpa [ket0, transport_symm_apply] using hsup.1
      · simpa [bra0, transport_symm_apply] using hsup.2.1
      · exact (sameOff_transport σ bra ket r).mp hsup.2.2
    have hsign : fermionSign σ.symm ket = fermionSign σ ket0 := by
      simpa [hket] using fermionSign_symm_transport σ ket0
    have hcar : carAnnihilateInt r bra0 ket0 = jwSignInt ket0 r := by
      unfold carAnnihilateInt
      rw [if_pos hsup]
    have hcar' : carAnnihilateInt (σ r) bra ket = jwSignInt (transportState σ ket0) (σ r) := by
      unfold carAnnihilateInt
      rw [if_pos htarget, hket]
    calc
      fermionSign σ bra0 * carAnnihilateInt r bra0 ket0 * fermionSign σ.symm ket
          = fermionSign σ (clearRole ket0 r) * jwSignInt ket0 r * fermionSign σ ket0 := by
            rw [hcar, hbra0, hsign]
      _ = fermionSign σ (clearRole ket0 r) * fermionSign σ ket0 * jwSignInt ket0 r := by ring
      _ = jwSignInt (transportState σ ket0) (σ r) := fermionSign_clear_jw σ ket0 r hsup.1
      _ = carAnnihilateInt (σ r) bra ket := hcar'.symm
  · have htarget : ¬ (ket (σ r) = true ∧ bra (σ r) = false ∧
        ∀ s : Role, s ≠ σ r → bra s = ket s) := by
      intro hbad
      apply hsup
      refine ⟨?_, ?_, ?_⟩
      · simpa [ket0, transport_symm_apply] using hbad.1
      · simpa [bra0, transport_symm_apply] using hbad.2.1
      · exact (sameOff_transport σ bra ket r).mpr hbad.2.2
    unfold carAnnihilateInt
    rw [if_neg hsup, if_neg htarget]
    ring

/-! ## Signed operator -/

lemma fockMatMul_signed_right (σ : Equiv.Perm Role)
    (M : ArchiveFockState → ArchiveFockState → ℤ) (bra ket : ArchiveFockState) :
    fockMatMul M (signedTransport σ) bra ket =
      M bra (transportState σ ket) * fermionSign σ ket := by
  classical
  unfold fockMatMul
  unfold signedTransport
  rw [Finset.sum_eq_single_of_mem (transportState σ ket) (Finset.mem_univ _)]
  · rw [if_pos rfl]
  · intro mid _ hne
    rw [if_neg hne]
    ring

lemma fockMatMul_signed_left (σ : Equiv.Perm Role)
    (M : ArchiveFockState → ArchiveFockState → ℤ) (bra ket : ArchiveFockState) :
    fockMatMul (signedTransport σ) M bra ket =
      fermionSign σ (transportState σ.symm bra) * M (transportState σ.symm bra) ket := by
  classical
  unfold fockMatMul
  unfold signedTransport
  rw [Finset.sum_eq_single_of_mem (transportState σ.symm bra) (Finset.mem_univ _)]
  · have hbra : bra = transportState σ (transportState σ.symm bra) :=
      (transport_state_inverse_apply σ bra).symm
    rw [if_pos hbra]
  · intro mid _ hne
    have hbra : bra ≠ transportState σ mid := by
      intro h
      have hmid : transportState σ.symm (transportState σ mid) = mid :=
        transportState_leftInverse σ mid
      exact hne ((congrArg (transportState σ.symm) h).trans hmid).symm
    rw [if_neg hbra]
    ring

/-- `U_σ T U_σ⁻¹`. -/
def conjTransport (σ : Equiv.Perm Role) (T : ArchiveFockState → ArchiveFockState → ℤ)
    (bra ket : ArchiveFockState) : ℤ :=
  fockMatMul (fockMatMul (signedTransport σ) T) (signedTransport σ.symm) bra ket

lemma conjTransport_apply (σ : Equiv.Perm Role) (T : ArchiveFockState → ArchiveFockState → ℤ)
    (bra ket : ArchiveFockState) :
    conjTransport σ T bra ket =
      fermionSign σ (transportState σ.symm bra) *
        T (transportState σ.symm bra) (transportState σ.symm ket) *
        fermionSign σ.symm ket := by
  rw [conjTransport, fockMatMul_signed_right, fockMatMul_signed_left]

theorem signedTransport_mul (σ τ : Equiv.Perm Role) (bra ket : ArchiveFockState) :
    fockMatMul (signedTransport σ) (signedTransport τ) bra ket =
      signedTransport (σ * τ) bra ket := by
  classical
  rw [fockMatMul_signed_right]
  unfold signedTransport
  by_cases h : bra = transportState σ (transportState τ ket)
  · have hmul : bra = transportState (σ * τ) ket := by
      rw [h, transportState_mul]
    rw [if_pos h, if_pos hmul, fermionSign_mul, mul_comm]
  · have hmul : bra ≠ transportState (σ * τ) ket := by
      rw [transportState_mul]
      exact h
    rw [if_neg h, if_neg hmul]
    ring

theorem signedTransport_inv (σ : Equiv.Perm Role) (bra ket : ArchiveFockState) :
    fockMatMul (signedTransport σ) (signedTransport σ.symm) bra ket =
      fockIdentityInt bra ket := by
  rw [signedTransport_mul, perm_mul_symm, signedTransport_one]

theorem signedTransport_inv_left (σ : Equiv.Perm Role) (bra ket : ArchiveFockState) :
    fockMatMul (signedTransport σ.symm) (signedTransport σ) bra ket =
      fockIdentityInt bra ket := by
  rw [signedTransport_mul, perm_symm_mul, signedTransport_one]

theorem fockMatMul_assoc (M N P : ArchiveFockState → ArchiveFockState → ℤ)
    (bra ket : ArchiveFockState) :
    fockMatMul (fun b k => fockMatMul M N b k) P bra ket =
      fockMatMul M (fun b k => fockMatMul N P b k) bra ket := by
  classical
  unfold fockMatMul
  simp_rw [Finset.sum_mul, Finset.mul_sum]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun _ _ => Finset.sum_congr rfl fun _ _ => ?_
  rw [mul_assoc]

theorem fockIdentityInt_mul_left (M : ArchiveFockState → ArchiveFockState → ℤ)
    (bra ket : ArchiveFockState) :
    fockMatMul fockIdentityInt M bra ket = M bra ket := by
  classical
  unfold fockMatMul
  unfold fockIdentityInt
  rw [Finset.sum_eq_single_of_mem bra (Finset.mem_univ _)]
  · rw [if_pos rfl]
    ring
  · intro mid _ hne
    rw [if_neg hne.symm]
    ring

theorem fockIdentityInt_mul_right (M : ArchiveFockState → ArchiveFockState → ℤ)
    (bra ket : ArchiveFockState) :
    fockMatMul M fockIdentityInt bra ket = M bra ket := by
  classical
  unfold fockMatMul
  unfold fockIdentityInt
  rw [Finset.sum_eq_single_of_mem ket (Finset.mem_univ _)]
  · rw [if_pos rfl]
    ring
  · intro mid _ hne
    rw [if_neg hne]
    ring

theorem conjTransport_mul (σ : Equiv.Perm Role)
    (M N : ArchiveFockState → ArchiveFockState → ℤ) (bra ket : ArchiveFockState) :
    conjTransport σ (fun b k => fockMatMul M N b k) bra ket =
      fockMatMul (fun b k => conjTransport σ M b k) (fun b k => conjTransport σ N b k) bra ket := by
  classical
  symm
  set bra0 := transportState σ.symm bra
  set ket0 := transportState σ.symm ket
  let e : ArchiveFockState ≃ ArchiveFockState :=
    { toFun := transportState σ.symm
      invFun := transportState σ
      left_inv := transport_state_inverse_apply σ
      right_inv := transportState_leftInverse σ }
  calc
    fockMatMul (fun b k => conjTransport σ M b k) (fun b k => conjTransport σ N b k) bra ket
        = ∑ mid, conjTransport σ M bra mid * conjTransport σ N mid ket := rfl
    _ = ∑ mid,
          (fermionSign σ bra0 * M bra0 (transportState σ.symm mid) * fermionSign σ.symm mid) *
            (fermionSign σ (transportState σ.symm mid) * N (transportState σ.symm mid) ket0 *
              fermionSign σ.symm ket) := by
          simp only [conjTransport_apply, bra0, ket0]
    _ = ∑ mid, fermionSign σ bra0 *
          (M bra0 (transportState σ.symm mid) * N (transportState σ.symm mid) ket0) *
          fermionSign σ.symm ket := by
          refine Finset.sum_congr rfl fun mid _ => ?_
          have htr : transportState σ (transportState σ.symm mid) = mid :=
            transport_state_inverse_apply σ mid
          have heq : fermionSign σ.symm mid =
              fermionSign σ (transportState σ.symm mid) := by
            simpa [htr] using fermionSign_symm_transport σ (transportState σ.symm mid)
          calc
            (fermionSign σ bra0 * M bra0 (transportState σ.symm mid) * fermionSign σ.symm mid) *
                (fermionSign σ (transportState σ.symm mid) *
                  N (transportState σ.symm mid) ket0 * fermionSign σ.symm ket)
                = fermionSign σ bra0 * M bra0 (transportState σ.symm mid) *
                    (fermionSign σ.symm mid * fermionSign σ (transportState σ.symm mid)) *
                    N (transportState σ.symm mid) ket0 * fermionSign σ.symm ket := by ring
            _ = fermionSign σ bra0 *
                  (M bra0 (transportState σ.symm mid) * N (transportState σ.symm mid) ket0) *
                  fermionSign σ.symm ket := by
                rw [heq, fermionSign_sq]
                ring
    _ = fermionSign σ bra0 *
          (∑ mid, M bra0 (transportState σ.symm mid) * N (transportState σ.symm mid) ket0) *
          fermionSign σ.symm ket := by
          symm
          conv_lhs =>
            arg 1
            rw [Finset.mul_sum]
          rw [Finset.sum_mul]
    _ = fermionSign σ bra0 * (∑ mid0, M bra0 mid0 * N mid0 ket0) * fermionSign σ.symm ket := by
          have hsum := e.sum_comp fun mid0 => M bra0 mid0 * N mid0 ket0
          simpa [e] using congrArg (fun z => fermionSign σ bra0 * z * fermionSign σ.symm ket) hsum
    _ = conjTransport σ (fun b k => fockMatMul M N b k) bra ket := by
          rw [conjTransport_apply, fockMatMul]

theorem conjTransport_sub (σ : Equiv.Perm Role)
    (M N : ArchiveFockState → ArchiveFockState → ℤ) (bra ket : ArchiveFockState) :
    conjTransport σ (fun b k => M b k - N b k) bra ket =
      conjTransport σ M bra ket - conjTransport σ N bra ket := by
  rw [conjTransport_apply, conjTransport_apply, conjTransport_apply]
  ring

theorem perm_conj_annihilation (σ : Equiv.Perm Role) (r : Role) (bra ket : ArchiveFockState) :
    conjTransport σ (carAnnihilateInt r) bra ket = carAnnihilateInt (σ r) bra ket := by
  rw [conjTransport_apply]
  exact annihilate_scalar σ r bra ket

theorem perm_conj_creation (σ : Equiv.Perm Role) (r : Role) (bra ket : ArchiveFockState) :
    conjTransport σ (carCreateInt r) bra ket = carCreateInt (σ r) bra ket := by
  rw [conjTransport_apply, carCreateInt]
  have hswap := perm_conj_annihilation σ r ket bra
  rw [conjTransport_apply] at hswap
  have hbra : fermionSign σ.symm bra = fermionSign σ (transportState σ.symm bra) := by
    simpa [transport_state_inverse_apply] using
      fermionSign_symm_transport σ (transportState σ.symm bra)
  have hket : fermionSign σ.symm ket = fermionSign σ (transportState σ.symm ket) := by
    simpa [transport_state_inverse_apply] using
      fermionSign_symm_transport σ (transportState σ.symm ket)
  calc
    fermionSign σ (transportState σ.symm bra) *
        carAnnihilateInt r (transportState σ.symm ket) (transportState σ.symm bra) *
        fermionSign σ.symm ket
        = fermionSign σ (transportState σ.symm ket) *
          carAnnihilateInt r (transportState σ.symm ket) (transportState σ.symm bra) *
          fermionSign σ.symm bra := by rw [hbra, hket]; ring
    _ = carAnnihilateInt (σ r) ket bra := hswap
    _ = carCreateInt (σ r) bra ket := by simp [carCreateInt]

theorem signedTransport_inv_adjacent (bra ket : ArchiveFockState) :
    fockMatMul (signedTransport swapAB) (signedTransport swapAB.symm) bra ket =
        fockIdentityInt bra ket ∧
    fockMatMul (signedTransport swapBC) (signedTransport swapBC.symm) bra ket =
        fockIdentityInt bra ket ∧
    fockMatMul (signedTransport swapCD) (signedTransport swapCD.symm) bra ket =
        fockIdentityInt bra ket := by
  exact ⟨signedTransport_inv swapAB bra ket, signedTransport_inv swapBC bra ket,
    signedTransport_inv swapCD bra ket⟩

theorem signed_annihilate_intertwining_adjacent (r : Role) (bra ket : ArchiveFockState) :
    fockMatMul (fockMatMul (signedTransport swapAB) (carAnnihilateInt r))
        (signedTransport swapAB.symm) bra ket = carAnnihilateInt (swapAB r) bra ket ∧
    fockMatMul (fockMatMul (signedTransport swapBC) (carAnnihilateInt r))
        (signedTransport swapBC.symm) bra ket = carAnnihilateInt (swapBC r) bra ket ∧
    fockMatMul (fockMatMul (signedTransport swapCD) (carAnnihilateInt r))
        (signedTransport swapCD.symm) bra ket = carAnnihilateInt (swapCD r) bra ket := by
  simpa [conjTransport] using
    ⟨perm_conj_annihilation swapAB r bra ket, perm_conj_annihilation swapBC r bra ket,
      perm_conj_annihilation swapCD r bra ket⟩

theorem signed_create_intertwining_adjacent (r : Role) (bra ket : ArchiveFockState) :
    fockMatMul (fockMatMul (signedTransport swapAB) (carCreateInt r))
        (signedTransport swapAB.symm) bra ket = carCreateInt (swapAB r) bra ket ∧
    fockMatMul (fockMatMul (signedTransport swapBC) (carCreateInt r))
        (signedTransport swapBC.symm) bra ket = carCreateInt (swapBC r) bra ket ∧
    fockMatMul (fockMatMul (signedTransport swapCD) (carCreateInt r))
        (signedTransport swapCD.symm) bra ket = carCreateInt (swapCD r) bra ket := by
  simpa [conjTransport] using
    ⟨perm_conj_creation swapAB r bra ket, perm_conj_creation swapBC r bra ket,
      perm_conj_creation swapCD r bra ket⟩

/-- Number bilinear `E_sr = c_s† c_r`. -/
def numberBilinear (s r : Role) (bra ket : ArchiveFockState) : ℤ :=
  fockMatMul (carCreateInt s) (carAnnihilateInt r) bra ket

theorem perm_conj_carBilinear (σ : Equiv.Perm Role) (s r : Role) (bra ket : ArchiveFockState) :
    conjTransport σ (numberBilinear s r) bra ket =
      numberBilinear (σ s) (σ r) bra ket := by
  unfold numberBilinear
  rw [conjTransport_mul]
  have hcreate : conjTransport σ (carCreateInt s) = carCreateInt (σ s) := by
    ext bra' ket'
    exact perm_conj_creation σ s bra' ket'
  have hann : conjTransport σ (carAnnihilateInt r) = carAnnihilateInt (σ r) := by
    ext bra' ket'
    exact perm_conj_annihilation σ r bra' ket'
  simp [hcreate, hann]

/-- Commutator of number bilinears, `[E_sr, E_tu]`. -/
def numberCommutator (s r t u : Role) (bra ket : ArchiveFockState) : ℤ :=
  fockMatMul (numberBilinear s r) (numberBilinear t u) bra ket -
    fockMatMul (numberBilinear t u) (numberBilinear s r) bra ket

theorem perm_conj_numberCommutator (σ : Equiv.Perm Role) (s r t u : Role)
    (bra ket : ArchiveFockState) :
    conjTransport σ (numberCommutator s r t u) bra ket =
      numberCommutator (σ s) (σ r) (σ t) (σ u) bra ket := by
  unfold numberCommutator
  rw [conjTransport_sub, conjTransport_mul, conjTransport_mul]
  have hsr : conjTransport σ (numberBilinear s r) = numberBilinear (σ s) (σ r) := by
    ext bra' ket'
    exact perm_conj_carBilinear σ s r bra' ket'
  have htu : conjTransport σ (numberBilinear t u) = numberBilinear (σ t) (σ u) := by
    ext bra' ket'
    exact perm_conj_carBilinear σ t u bra' ket'
  simp [hsr, htu]

theorem numberBilinear_intertwining_adjacent (s r : Role) (bra ket : ArchiveFockState) :
    fockMatMul (fockMatMul (signedTransport swapAB) (numberBilinear s r))
        (signedTransport swapAB.symm) bra ket =
          numberBilinear (swapAB s) (swapAB r) bra ket ∧
    fockMatMul (fockMatMul (signedTransport swapBC) (numberBilinear s r))
        (signedTransport swapBC.symm) bra ket =
          numberBilinear (swapBC s) (swapBC r) bra ket ∧
    fockMatMul (fockMatMul (signedTransport swapCD) (numberBilinear s r))
        (signedTransport swapCD.symm) bra ket =
          numberBilinear (swapCD s) (swapCD r) bra ket := by
  simpa [conjTransport] using
    ⟨perm_conj_carBilinear swapAB s r bra ket, perm_conj_carBilinear swapBC s r bra ket,
      perm_conj_carBilinear swapCD s r bra ket⟩

/-- A matrix preserves Fock degree when it has no matrix elements between
distinct occupation numbers. -/
def PreservesFockDegree (T : ArchiveFockState → ArchiveFockState → ℤ) : Prop :=
  ∀ bra ket, fockDegree bra ≠ fockDegree ket → T bra ket = 0

theorem numberBilinear_preserves_degree (s r : Role) (bra ket : ArchiveFockState)
    (hdeg : fockDegree bra ≠ fockDegree ket) :
    numberBilinear s r bra ket = 0 := by
  classical
  unfold numberBilinear fockMatMul
  apply Finset.sum_eq_zero
  intro mid _
  by_cases hc : carCreateInt s bra mid = 0
  · simp [hc]
  · by_cases ha : carAnnihilateInt r mid ket = 0
    · simp [ha]
    · have hcreate := carCreateInt_degree_raise s bra mid hc
      have hann := carAnnihilateInt_degree_lower r mid ket ha
      have : fockDegree bra = fockDegree ket := by omega
      exact absurd this hdeg

theorem signedTransport_preserves_degree (σ : Equiv.Perm Role) :
    PreservesFockDegree (signedTransport σ) := by
  intro bra ket hdeg
  unfold signedTransport
  by_cases h : bra = transportState σ ket
  · have hdeg' : fockDegree bra = fockDegree ket := by
      rw [h, fockDegree_transport]
    exact (hdeg hdeg').elim
  · simp [h]

theorem conjTransport_preserves_degree (σ : Equiv.Perm Role)
    (T : ArchiveFockState → ArchiveFockState → ℤ) (hT : PreservesFockDegree T) :
    PreservesFockDegree (conjTransport σ T) := by
  intro bra ket hdeg
  rw [conjTransport_apply]
  have hdeg0 : fockDegree (transportState σ.symm bra) ≠
      fockDegree (transportState σ.symm ket) := by
    simpa [fockDegree_transport] using hdeg
  rw [hT _ _ hdeg0]
  ring

end D0.Geometry.RoleFockPermutation
