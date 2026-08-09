import D0.Topology.GenericTripartiteHomology
import Mathlib.Tactic
import Mathlib.LinearAlgebra.FreeModule.Basic

/-!
# D0-GENERIC-TRIPARTITE-TOP-HOMOLOGY-RING-001

The rational rank theorem is strengthened without division.  For every
commutative coefficient ring `R`, all top cycles of the canonical
complete-tripartite clique complex are determined by their values on the
all-nonroot triangles, and the octahedral cycles give the inverse map:

```
ker ∂₂(R) ≃ₗ[R] (Fin p × Fin q × Fin r → R).
```

For `R=ℤ`, this is an explicit integral basis of `H₂` with `p*q*r` elements;
in particular the top integral homology has no torsion.  No field-rank,
Smith-normal-form, join, or homotopy-classification argument is used.
-/

namespace D0.Topology.GenericTripartiteTopHomologyRing
open scoped BigOperators
open Matrix
open D0.SelfReading.TypedIncidenceCarriers
open D0.Topology.GenericTripartiteHomology

variable (R : Type) [CommRing R]
variable {p q r : ℕ}
local notation "A" => Fin (p + 1)
local notation "B" => Fin (q + 1)
local notation "C" => Fin (r + 1)
local notation "Edge" => GenericEdge p q r
local notation "Triangle" => GenericTriangle p q r

abbrev TopCycleIndex (p q r : ℕ) := Fin p × Fin q × Fin r

def boundary2R : Matrix Edge Triangle R
  | Sum.inl (a, b), (a', b', _) =>
      if a = a' ∧ b = b' then 1 else 0
  | Sum.inr (Sum.inl (a, c)), (a', _, c') =>
      if a = a' ∧ c = c' then -1 else 0
  | Sum.inr (Sum.inr (b, c)), (_, b', c') =>
      if b = b' ∧ c = c' then 1 else 0

private lemma sum_indicator_pair_one
    {α β : Type} [Fintype α] [Fintype β]
    [DecidableEq α] [DecidableEq β]
    (f : α × β → R) (a : α) (b : β) :
    (∑ x : α, ∑ y : β,
      (if a = x ∧ b = y then (1 : R) else 0) * f (x, y)) = f (a,b) := by
  calc
    _ = ∑ x : α, if a = x then f (x,b) else 0 := by
      apply Fintype.sum_congr
      intro x
      by_cases hx : a = x
      · subst x
        simpa using Fintype.sum_ite_eq b (fun y : β => f (a,y))
      · simp [hx]
    _ = f (a,b) := by
      simpa using Fintype.sum_ite_eq a (fun x : α => f (x,b))

private lemma sum_indicator_pair_neg
    {α β : Type} [Fintype α] [Fintype β]
    [DecidableEq α] [DecidableEq β]
    (f : α × β → R) (a : α) (b : β) :
    (∑ x : α, ∑ y : β,
      (if a = x ∧ b = y then (-1 : R) else 0) * f (x, y)) = -f (a,b) := by
  calc
    _ = ∑ x : α, if a = x then -f (x,b) else 0 := by
      apply Fintype.sum_congr
      intro x
      by_cases hx : a = x
      · subst x
        simpa using Fintype.sum_ite_eq b (fun y : β => -f (a,y))
      · simp [hx]
    _ = -f (a,b) := by
      simpa using Fintype.sum_ite_eq a (fun x : α => -f (x,b))

lemma boundary2R_mulVec_ab (x : Triangle → R) (a : A) (b : B) :
    (boundary2R R (p:=p) (q:=q) (r:=r)).mulVec x (Sum.inl (a,b)) =
      ∑ c : C, x (a,b,c) := by
  simp only [Matrix.mulVec, dotProduct, boundary2R, Fintype.sum_prod_type]
  calc
    (∑ a' : A, ∑ b' : B, ∑ c : C,
      (if a = a' ∧ b = b' then (1:R) else 0) * x (a',b',c)) =
        ∑ a' : A, ∑ b' : B,
          (if a = a' ∧ b = b' then (1:R) else 0) *
            (∑ c : C, x (a',b',c)) := by
          apply Fintype.sum_congr
          intro a'
          apply Fintype.sum_congr
          intro b'
          rw [Finset.mul_sum]
    _ = ∑ c : C, x (a,b,c) := by
      exact sum_indicator_pair_one R
        (fun p : A × B => ∑ c : C, x (p.1,p.2,c)) a b

lemma boundary2R_mulVec_ac (x : Triangle → R) (a : A) (c : C) :
    (boundary2R R (p:=p) (q:=q) (r:=r)).mulVec x (Sum.inr (Sum.inl (a,c))) =
      - ∑ b : B, x (a,b,c) := by
  simp only [Matrix.mulVec, dotProduct, boundary2R, Fintype.sum_prod_type]
  calc
    (∑ a' : A, ∑ b : B, ∑ c' : C,
      (if a = a' ∧ c = c' then (-1:R) else 0) * x (a',b,c')) =
        ∑ b : B, -x (a,b,c) := by
          rw [Finset.sum_comm]
          apply Fintype.sum_congr
          intro b
          exact sum_indicator_pair_neg R
            (fun p : A × C => x (p.1,b,p.2)) a c
    _ = - ∑ b : B, x (a,b,c) := by rw [Finset.sum_neg_distrib]

lemma boundary2R_mulVec_bc (x : Triangle → R) (b : B) (c : C) :
    (boundary2R R (p:=p) (q:=q) (r:=r)).mulVec x (Sum.inr (Sum.inr (b,c))) =
      ∑ a : A, x (a,b,c) := by
  simp only [Matrix.mulVec, dotProduct, boundary2R, Fintype.sum_prod_type]
  apply Fintype.sum_congr
  intro a
  exact sum_indicator_pair_one R
    (fun p : B × C => x (a,p.1,p.2)) b c

abbrev TopKernel := LinearMap.ker (boundary2R R (p:=p) (q:=q) (r:=r)).mulVecLin

lemma kernel_sum_ab_zero (z : TopKernel R (p:=p) (q:=q) (r:=r)) (a:A) (b:B) :
    ∑ c:C, (z:Triangle→R) (a,b,c) = 0 := by
  have h := congrFun z.property (Sum.inl (a,b))
  rw [Matrix.mulVecLin_apply, boundary2R_mulVec_ab] at h
  exact h

lemma kernel_sum_ac_zero (z : TopKernel R (p:=p) (q:=q) (r:=r)) (a:A) (c:C) :
    ∑ b:B, (z:Triangle→R) (a,b,c) = 0 := by
  have h := congrFun z.property (Sum.inr (Sum.inl (a,c)))
  rw [Matrix.mulVecLin_apply, boundary2R_mulVec_ac] at h
  simpa using neg_eq_zero.mp h

lemma kernel_sum_bc_zero (z : TopKernel R (p:=p) (q:=q) (r:=r)) (b:B) (c:C) :
    ∑ a:A, (z:Triangle→R) (a,b,c) = 0 := by
  have h := congrFun z.property (Sum.inr (Sum.inr (b,c)))
  rw [Matrix.mulVecLin_apply, boundary2R_mulVec_bc] at h
  exact h


def topCoordinateAtR (i : TopCycleIndex p q r) :
    TopKernel R (p:=p) (q:=q) (r:=r) →ₗ[R] R :=
  (LinearMap.proj
      (R := R) (φ := fun _ : Triangle => R)
      (i.1.succ, i.2.1.succ, i.2.2.succ)).comp
    (LinearMap.ker
      (boundary2R R (p:=p) (q:=q) (r:=r)).mulVecLin).subtype

def topCoordinateR :
    TopKernel R (p:=p) (q:=q) (r:=r) →ₗ[R]
      (TopCycleIndex p q r → R) :=
  LinearMap.pi (fun i => topCoordinateAtR R i)

@[simp] lemma topCoordinateR_apply
    (z : TopKernel R (p:=p) (q:=q) (r:=r))
    (i : TopCycleIndex p q r) :
    topCoordinateR R z i =
      (z : Triangle → R) (i.1.succ, i.2.1.succ, i.2.2.succ) := rfl

theorem topCoordinateR_injective :
    Function.Injective (topCoordinateR R (p:=p) (q:=q) (r:=r)) := by
  rw [injective_iff_map_eq_zero]
  intro z hz
  have hnr (i : Fin p) (j : Fin q) (k : Fin r) :
      (z : Triangle → R) (i.succ,j.succ,k.succ) = 0 := by
    have h := congrFun hz (i,j,k)
    simpa using h
  have ha0 (j : Fin q) (k : Fin r) :
      (z : Triangle → R) (0,j.succ,k.succ) = 0 := by
    have h := kernel_sum_bc_zero R z j.succ k.succ
    rw [Fin.sum_univ_succ] at h
    simp only [hnr, Finset.sum_const_zero, add_zero] at h
    exact h
  have hb0 (i : Fin p) (k : Fin r) :
      (z : Triangle → R) (i.succ,0,k.succ) = 0 := by
    have h := kernel_sum_ac_zero R z i.succ k.succ
    rw [Fin.sum_univ_succ] at h
    simp only [hnr, Finset.sum_const_zero, add_zero] at h
    exact h
  have hc0 (i : Fin p) (j : Fin q) :
      (z : Triangle → R) (i.succ,j.succ,0) = 0 := by
    have h := kernel_sum_ab_zero R z i.succ j.succ
    rw [Fin.sum_univ_succ] at h
    simp only [hnr, Finset.sum_const_zero, add_zero] at h
    exact h
  have hab0 (k : Fin r) :
      (z : Triangle → R) (0,0,k.succ) = 0 := by
    have h := kernel_sum_ac_zero R z 0 k.succ
    rw [Fin.sum_univ_succ] at h
    simp only [ha0, Finset.sum_const_zero, add_zero] at h
    exact h
  have hac0 (j : Fin q) :
      (z : Triangle → R) (0,j.succ,0) = 0 := by
    have h := kernel_sum_ab_zero R z 0 j.succ
    rw [Fin.sum_univ_succ] at h
    simp only [ha0, Finset.sum_const_zero, add_zero] at h
    exact h
  have hbc0 (i : Fin p) :
      (z : Triangle → R) (i.succ,0,0) = 0 := by
    have h := kernel_sum_ac_zero R z i.succ 0
    rw [Fin.sum_univ_succ] at h
    simp only [hc0, Finset.sum_const_zero, add_zero] at h
    exact h
  have h000 : (z : Triangle → R) (0,0,0) = 0 := by
    have h := kernel_sum_ab_zero R z 0 0
    rw [Fin.sum_univ_succ] at h
    simp only [hab0, Finset.sum_const_zero, add_zero] at h
    exact h
  apply Subtype.ext
  funext t
  rcases t with ⟨a,b,c⟩
  refine Fin.cases ?_ (fun i => ?_) a
  · refine Fin.cases ?_ (fun j => ?_) b
    · refine Fin.cases ?_ (fun k => ?_) c
      · exact h000
      · exact hab0 k
    · refine Fin.cases ?_ (fun k => ?_) c
      · exact hac0 j
      · exact ha0 j k
  · refine Fin.cases ?_ (fun j => ?_) b
    · refine Fin.cases ?_ (fun k => ?_) c
      · exact hbc0 i
      · exact hb0 i k
    · refine Fin.cases ?_ (fun k => ?_) c
      · exact hc0 i j
      · exact hnr i j k


def rootDifferenceR {n : ℕ} (i : Fin n) : Fin (n + 1) → R :=
  fun x => if x = i.succ then 1 else if x = 0 then -1 else 0

@[simp] theorem rootDifferenceR_zero {n : ℕ} (i : Fin n) :
    rootDifferenceR R i (0 : Fin (n + 1)) = -1 := by
  unfold rootDifferenceR
  rw [if_neg (Fin.succ_ne_zero i).symm]
  simp

@[simp] theorem rootDifferenceR_succ {n : ℕ} (i j : Fin n) :
    rootDifferenceR R i j.succ = if j = i then 1 else 0 := by
  by_cases h : j = i
  · subst j
    simp [rootDifferenceR]
  · simp [rootDifferenceR, h, Fin.succ_inj]

theorem rootDifferenceR_sum {n : ℕ} (i : Fin n) :
    ∑ x : Fin (n + 1), rootDifferenceR R i x = 0 := by
  rw [Fin.sum_univ_succ]
  simp

def topCycleVecR (i : TopCycleIndex p q r) : Triangle → R
  | (a,b,c) =>
      rootDifferenceR R i.1 a *
        rootDifferenceR R i.2.1 b *
        rootDifferenceR R i.2.2 c

theorem boundary2R_topCycleVec_zero (i : TopCycleIndex p q r) :
    (boundary2R R (p:=p) (q:=q) (r:=r)).mulVec (topCycleVecR R i) = 0 := by
  funext e
  rcases e with ab | rest
  · rcases ab with ⟨a,b⟩
    rw [boundary2R_mulVec_ab]
    change ∑ c : C,
      (rootDifferenceR R i.1 a * rootDifferenceR R i.2.1 b) *
        rootDifferenceR R i.2.2 c = 0
    rw [← Finset.mul_sum, rootDifferenceR_sum]
    simp
  · rcases rest with ac | bc
    · rcases ac with ⟨a,c⟩
      rw [boundary2R_mulVec_ac]
      change -(∑ b : B,
        rootDifferenceR R i.1 a * rootDifferenceR R i.2.1 b *
          rootDifferenceR R i.2.2 c) = 0
      rw [show (∑ b : B,
          rootDifferenceR R i.1 a * rootDifferenceR R i.2.1 b *
            rootDifferenceR R i.2.2 c) =
          rootDifferenceR R i.1 a *
            (∑ b : B, rootDifferenceR R i.2.1 b) *
            rootDifferenceR R i.2.2 c by
        rw [Finset.mul_sum, Finset.sum_mul]]
      rw [rootDifferenceR_sum]
      simp
    · rcases bc with ⟨b,c⟩
      rw [boundary2R_mulVec_bc]
      simp only [topCycleVecR, Pi.zero_apply]
      rw [← Finset.sum_mul, ← Finset.sum_mul, rootDifferenceR_sum]
      simp

def topCycleR (i : TopCycleIndex p q r) :
    TopKernel R (p:=p) (q:=q) (r:=r) :=
  ⟨topCycleVecR R i, by
    rw [LinearMap.mem_ker, Matrix.mulVecLin_apply]
    exact boundary2R_topCycleVec_zero R i⟩

@[simp] theorem topCycleR_coe (i : TopCycleIndex p q r) :
    (topCycleR R i : Triangle → R) = topCycleVecR R i := rfl

theorem topCycleVecR_nonroot_coordinate (i j : TopCycleIndex p q r) :
    topCycleVecR R j (i.1.succ,i.2.1.succ,i.2.2.succ) =
      if i = j then 1 else 0 := by
  simp only [topCycleVecR, rootDifferenceR_succ]
  by_cases h1 : i.1 = j.1
  · by_cases h2 : i.2.1 = j.2.1
    · by_cases h3 : i.2.2 = j.2.2
      · have h : i = j := by
          rcases i with ⟨ia,ib,ic⟩
          rcases j with ⟨ja,jb,jc⟩
          simp_all
        simp [h]
      · have h : i ≠ j := by
          intro hij
          exact h3 (congrArg (fun x => x.2.2) hij)
        simp [h,h3]
    · have h : i ≠ j := by
        intro hij
        exact h2 (congrArg (fun x => x.2.1) hij)
      simp [h,h2]
  · have h : i ≠ j := by
      intro hij
      exact h1 (congrArg (fun x => x.1) hij)
    simp [h,h1]

@[simp] theorem topCoordinateAtR_topCycleR
    (i j : TopCycleIndex p q r) :
    topCoordinateAtR R i (topCycleR R j) = if i = j then 1 else 0 := by
  exact topCycleVecR_nonroot_coordinate R i j

def topSynthesisR :
    (TopCycleIndex p q r → R) →ₗ[R]
      TopKernel R (p:=p) (q:=q) (r:=r) :=
  Fintype.linearCombination R (topCycleR R)

@[simp] theorem topCoordinateR_topSynthesisR
    (g : TopCycleIndex p q r → R) :
    topCoordinateR R (topSynthesisR R g) = g := by
  funext i
  change topCoordinateAtR R i
      (∑ j, g j • topCycleR R j) = g i
  rw [map_sum]
  simp only [map_smul, topCoordinateAtR_topCycleR, smul_eq_mul]
  simp

@[simp] theorem topSynthesisR_topCoordinateR
    (z : TopKernel R (p:=p) (q:=q) (r:=r)) :
    topSynthesisR R (topCoordinateR R z) = z := by
  apply topCoordinateR_injective R
  rw [topCoordinateR_topSynthesisR]

/-- Universal top-cycle coordinates over any commutative coefficient ring. -/
def topCoordinateEquivR :
    TopKernel R (p:=p) (q:=q) (r:=r) ≃ₗ[R]
      (TopCycleIndex p q r → R) :=
  LinearEquiv.ofLinear
    (topCoordinateR R)
    (topSynthesisR R)
    (by
      apply LinearMap.ext
      intro g
      exact topCoordinateR_topSynthesisR R g)
    (by
      apply LinearMap.ext
      intro z
      exact topSynthesisR_topCoordinateR R z)

@[simp] theorem topCoordinateEquivR_apply
    (z : TopKernel R (p:=p) (q:=q) (r:=r)) :
    topCoordinateEquivR R z = topCoordinateR R z := rfl

@[simp] theorem topCoordinateEquivR_symm_apply
    (g : TopCycleIndex p q r → R) :
    (topCoordinateEquivR R).symm g = topSynthesisR R g := rfl


/-- The octahedral family is a basis over every commutative ring. -/
noncomputable def topCycleBasisR :
    Module.Basis (TopCycleIndex p q r) R
      (TopKernel R (p:=p) (q:=q) (r:=r)) :=
  Module.Basis.ofEquivFun (topCoordinateEquivR R)

@[simp] theorem topCycleBasisR_apply (i : TopCycleIndex p q r) :
    topCycleBasisR R i = topCycleR R i := by
  rw [topCycleBasisR, Module.Basis.coe_ofEquivFun]
  change (topCoordinateEquivR R).symm (Pi.single i 1) = topCycleR R i
  rw [topCoordinateEquivR_symm_apply]
  unfold topSynthesisR
  rw [Fintype.linearCombination_apply_single]
  simp

/-- Integral top homology is a free module with the explicit octahedral
basis. -/
theorem integerTopHomologyFree :
    Module.Free ℤ (TopKernel ℤ (p:=p) (q:=q) (r:=r)) :=
  Module.Free.of_basis (topCycleBasisR ℤ)

/-- Source-scene integral top homology is explicitly `Z^960`. -/
def sceneIntegerTopHomologyEquiv :
    TopKernel ℤ (p:=8) (q:=10) (r:=12) ≃ₗ[ℤ]
      (TopCycleIndex 8 10 12 → ℤ) :=
  topCoordinateEquivR ℤ

@[simp] theorem sceneIntegerTopCycleIndex_card :
    Fintype.card (TopCycleIndex 8 10 12) = 960 := by
  norm_num [TopCycleIndex]

end D0.Topology.GenericTripartiteTopHomologyRing
