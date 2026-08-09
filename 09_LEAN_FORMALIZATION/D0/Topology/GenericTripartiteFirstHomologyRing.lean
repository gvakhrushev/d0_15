import D0.Topology.GenericTripartiteTopHomologyRing
import Mathlib.Tactic

/-!
# D0-GENERIC-TRIPARTITE-FIRST-HOMOLOGY-RING-001

For every commutative coefficient ring `R`, this module gives a direct
filling algorithm for every 1-cycle in the canonical complete-tripartite
clique complex.  It proves

```
range ∂₂(R) = ker ∂₁(R)
```

without rank-nullity or division.  Consequently `H₁` is the zero module over
`ℤ`, every field, and every commutative ring.  The filling first cones the
`AB` component to the root of zone `C`, then fills the remaining `AC/BC`
margins on each `C`-layer using root row and root column.
-/

namespace D0.Topology.GenericTripartiteFirstHomologyRing
open scoped BigOperators
open Matrix
open D0.SelfReading.TypedIncidenceCarriers
open D0.Topology.GenericTripartiteHomology
open D0.Topology.GenericTripartiteTopHomologyRing

variable (R : Type) [CommRing R]
variable {p q r : ℕ}
local notation "A" => Fin (p + 1)
local notation "B" => Fin (q + 1)
local notation "C" => Fin (r + 1)
local notation "Vertex" => GenericVertex p q r
local notation "Edge" => GenericEdge p q r
local notation "Triangle" => GenericTriangle p q r

/-- Vertex-edge boundary over an arbitrary commutative ring. -/
def boundary1R : Matrix Vertex Edge R
  | Sum.inl a, Sum.inl (a', _) => if a = a' then -1 else 0
  | Sum.inl a, Sum.inr (Sum.inl (a', _)) => if a = a' then -1 else 0
  | Sum.inl _, Sum.inr (Sum.inr _) => 0
  | Sum.inr (Sum.inl b), Sum.inl (_, b') => if b = b' then 1 else 0
  | Sum.inr (Sum.inl _), Sum.inr (Sum.inl _) => 0
  | Sum.inr (Sum.inl b), Sum.inr (Sum.inr (b', _)) =>
      if b = b' then -1 else 0
  | Sum.inr (Sum.inr _), Sum.inl _ => 0
  | Sum.inr (Sum.inr c), Sum.inr (Sum.inl (_, c')) =>
      if c = c' then 1 else 0
  | Sum.inr (Sum.inr c), Sum.inr (Sum.inr (_, c')) =>
      if c = c' then 1 else 0

private lemma sum_indicator_fst_one
    {α β : Type} [Fintype α] [Fintype β] [DecidableEq α]
    (f : α × β → R) (a : α) :
    (∑ x : α × β,
      (if a = x.1 then (1:R) else 0) * f x) =
      ∑ b : β, f (a,b) := by
  rw [Fintype.sum_prod_type]
  calc
    _ = ∑ x : α, if a = x then ∑ y : β, f (x,y) else 0 := by
      apply Fintype.sum_congr
      intro x
      by_cases hx : a = x <;> simp [hx]
    _ = ∑ b : β, f (a,b) := by
      simpa using Fintype.sum_ite_eq a
        (fun x : α => ∑ y : β, f (x,y))

private lemma sum_indicator_fst_neg
    {α β : Type} [Fintype α] [Fintype β] [DecidableEq α]
    (f : α × β → R) (a : α) :
    (∑ x : α × β,
      (if a = x.1 then (-1:R) else 0) * f x) =
      -∑ b : β, f (a,b) := by
  calc
    _ = ∑ x : α × β,
        -((if a = x.1 then (1:R) else 0) * f x) := by
      apply Fintype.sum_congr
      intro x
      by_cases h : a = x.1 <;> simp [h]
    _ = -(∑ x : α × β,
        (if a = x.1 then (1:R) else 0) * f x) := by
      rw [Finset.sum_neg_distrib]
    _ = -∑ b : β, f (a,b) := by
      rw [sum_indicator_fst_one]

private lemma sum_indicator_snd_one
    {α β : Type} [Fintype α] [Fintype β] [DecidableEq β]
    (f : α × β → R) (b : β) :
    (∑ x : α × β,
      (if b = x.2 then (1:R) else 0) * f x) =
      ∑ a : α, f (a,b) := by
  rw [Fintype.sum_prod_type]
  apply Fintype.sum_congr
  intro a
  simpa using Fintype.sum_ite_eq b (fun y : β => f (a,y))

private lemma sum_indicator_snd_neg
    {α β : Type} [Fintype α] [Fintype β] [DecidableEq β]
    (f : α × β → R) (b : β) :
    (∑ x : α × β,
      (if b = x.2 then (-1:R) else 0) * f x) =
      -∑ a : α, f (a,b) := by
  calc
    _ = ∑ x : α × β,
        -((if b = x.2 then (1:R) else 0) * f x) := by
      apply Fintype.sum_congr
      intro x
      by_cases h : b = x.2 <;> simp [h]
    _ = -(∑ x : α × β,
        (if b = x.2 then (1:R) else 0) * f x) := by
      rw [Finset.sum_neg_distrib]
    _ = -∑ a : α, f (a,b) := by
      rw [sum_indicator_snd_one]

lemma boundary1R_mulVec_A (x : Edge → R) (a : A) :
    (boundary1R R (p:=p) (q:=q) (r:=r)).mulVec x (Sum.inl a) =
      -(∑ b:B, x (Sum.inl (a,b))) -
        ∑ c:C, x (Sum.inr (Sum.inl (a,c))) := by
  simp only [Matrix.mulVec, dotProduct, boundary1R, Fintype.sum_sum_type,
    zero_mul, Finset.sum_const_zero, add_zero]
  rw [sum_indicator_fst_neg, sum_indicator_fst_neg]
  simp [sub_eq_add_neg]

lemma boundary1R_mulVec_B (x : Edge → R) (b : B) :
    (boundary1R R (p:=p) (q:=q) (r:=r)).mulVec x (Sum.inr (Sum.inl b)) =
      (∑ a:A, x (Sum.inl (a,b))) -
        ∑ c:C, x (Sum.inr (Sum.inr (b,c))) := by
  simp only [Matrix.mulVec, dotProduct, boundary1R, Fintype.sum_sum_type,
    zero_mul, Finset.sum_const_zero, zero_add]
  rw [sum_indicator_snd_one, sum_indicator_fst_neg]
  simp [sub_eq_add_neg]

lemma boundary1R_mulVec_C (x : Edge → R) (c : C) :
    (boundary1R R (p:=p) (q:=q) (r:=r)).mulVec x (Sum.inr (Sum.inr c)) =
      (∑ a:A, x (Sum.inr (Sum.inl (a,c)))) +
        ∑ b:B, x (Sum.inr (Sum.inr (b,c))) := by
  simp only [Matrix.mulVec, dotProduct, boundary1R, Fintype.sum_sum_type,
    zero_mul, Finset.sum_const_zero, zero_add]
  rw [sum_indicator_snd_one, sum_indicator_snd_one]

abbrev OneCycle :=
  LinearMap.ker (boundary1R R (p:=p) (q:=q) (r:=r)).mulVecLin

def abPart (z : OneCycle R (p:=p) (q:=q) (r:=r)) (a:A) (b:B) : R :=
  (z:Edge→R) (Sum.inl (a,b))

def acPart (z : OneCycle R (p:=p) (q:=q) (r:=r)) (a:A) (c:C) : R :=
  (z:Edge→R) (Sum.inr (Sum.inl (a,c)))

def bcPart (z : OneCycle R (p:=p) (q:=q) (r:=r)) (b:B) (c:C) : R :=
  (z:Edge→R) (Sum.inr (Sum.inr (b,c)))

lemma oneCycle_A (z : OneCycle R (p:=p) (q:=q) (r:=r)) (a:A) :
    (∑ b:B, abPart R z a b) + ∑ c:C, acPart R z a c = 0 := by
  have h := congrFun z.property (Sum.inl a)
  rw [Matrix.mulVecLin_apply, boundary1R_mulVec_A] at h
  simp only [Pi.zero_apply] at h
  unfold abPart acPart
  linear_combination -h

lemma oneCycle_B (z : OneCycle R (p:=p) (q:=q) (r:=r)) (b:B) :
    (∑ a:A, abPart R z a b) - ∑ c:C, bcPart R z b c = 0 := by
  have h := congrFun z.property (Sum.inr (Sum.inl b))
  rw [Matrix.mulVecLin_apply, boundary1R_mulVec_B] at h
  simpa [abPart, bcPart] using h

lemma oneCycle_C (z : OneCycle R (p:=p) (q:=q) (r:=r)) (c:C) :
    (∑ a:A, acPart R z a c) + ∑ b:B, bcPart R z b c = 0 := by
  have h := congrFun z.property (Sum.inr (Sum.inr c))
  rw [Matrix.mulVecLin_apply, boundary1R_mulVec_C] at h
  simpa [acPart, bcPart] using h


def acResidual (z : OneCycle R (p:=p) (q:=q) (r:=r))
    (a:A) (c:C) : R :=
  acPart R z a c +
    if c = 0 then ∑ b:B, abPart R z a b else 0

def bcResidual (z : OneCycle R (p:=p) (q:=q) (r:=r))
    (b:B) (c:C) : R :=
  bcPart R z b c -
    if c = 0 then ∑ a:A, abPart R z a b else 0

lemma acResidual_sum_zero
    (z : OneCycle R (p:=p) (q:=q) (r:=r)) (a:A) :
    ∑ c:C, acResidual R z a c = 0 := by
  unfold acResidual
  rw [Finset.sum_add_distrib]
  have hite :
      (∑ c:C, if c = 0 then ∑ b:B, abPart R z a b else 0) =
        ∑ b:B, abPart R z a b := by
    simpa using Fintype.sum_ite_eq' (0:C)
      (fun _ : C => ∑ b:B, abPart R z a b)
  rw [hite]
  simpa [add_comm] using oneCycle_A R z a

lemma bcResidual_sum_zero
    (z : OneCycle R (p:=p) (q:=q) (r:=r)) (b:B) :
    ∑ c:C, bcResidual R z b c = 0 := by
  unfold bcResidual
  rw [Finset.sum_sub_distrib]
  have hite :
      (∑ c:C, if c = 0 then ∑ a:A, abPart R z a b else 0) =
        ∑ a:A, abPart R z a b := by
    simpa using Fintype.sum_ite_eq' (0:C)
      (fun _ : C => ∑ a:A, abPart R z a b)
  rw [hite]
  have h := oneCycle_B R z b
  linear_combination -h

lemma residual_compatibility
    (z : OneCycle R (p:=p) (q:=q) (r:=r)) (c:C) :
    -(∑ a:A, acResidual R z a c) =
      ∑ b:B, bcResidual R z b c := by
  by_cases hc : c = 0
  · subst c
    simp only [acResidual, bcResidual, if_true,
      Finset.sum_add_distrib, Finset.sum_sub_distrib]
    have hswap :
        (∑ a:A, ∑ b:B, abPart R z a b) =
          ∑ b:B, ∑ a:A, abPart R z a b := Finset.sum_comm
    have hC := oneCycle_C R z (0:C)
    rw [hswap]
    linear_combination -hC
  · simp only [acResidual, bcResidual, hc, if_false, add_zero, sub_zero]
    have hC := oneCycle_C R z c
    linear_combination -hC

/-- Fill the residual `AC/BC` margins on every `C`-layer using root row and
root column. -/
def residualFill (z : OneCycle R (p:=p) (q:=q) (r:=r)) :
    Triangle → R
  | (a,b,c) =>
      Fin.cases
        (Fin.cases
          (-acResidual R z 0 c -
            ∑ j : Fin q, bcResidual R z j.succ c)
          (fun j => bcResidual R z j.succ c)
          b)
        (fun i =>
          Fin.cases
            (-acResidual R z i.succ c)
            (fun _ => 0)
            b)
        a

lemma residualFill_row_sum
    (z : OneCycle R (p:=p) (q:=q) (r:=r)) (a:A) (c:C) :
    ∑ b:B, residualFill R z (a,b,c) = -acResidual R z a c := by
  refine Fin.cases ?_ (fun i => ?_) a
  · rw [Fin.sum_univ_succ]
    simp [residualFill]
  · rw [Fin.sum_univ_succ]
    simp [residualFill]

lemma residualFill_column_sum
    (z : OneCycle R (p:=p) (q:=q) (r:=r)) (b:B) (c:C) :
    ∑ a:A, residualFill R z (a,b,c) = bcResidual R z b c := by
  refine Fin.cases ?_ (fun j => ?_) b
  · rw [Fin.sum_univ_succ]
    simp only [residualFill, Fin.cases_zero, Fin.cases_succ]
    have h := residual_compatibility R z c
    rw [Fin.sum_univ_succ, Fin.sum_univ_succ] at h
    rw [Finset.sum_neg_distrib]
    linear_combination h
  · rw [Fin.sum_univ_succ]
    simp [residualFill]

lemma residualFill_depth_sum_zero
    (z : OneCycle R (p:=p) (q:=q) (r:=r)) (a:A) (b:B) :
    ∑ c:C, residualFill R z (a,b,c) = 0 := by
  refine Fin.cases ?_ (fun i => ?_) a
  · refine Fin.cases ?_ (fun j => ?_) b
    · simp only [residualFill, Fin.cases_zero, Fin.cases_succ]
      rw [Finset.sum_sub_distrib, Finset.sum_neg_distrib]
      rw [acResidual_sum_zero]
      simp only [neg_zero, zero_sub]
      rw [Finset.sum_comm]
      simp [bcResidual_sum_zero]
    · simp [residualFill, bcResidual_sum_zero]
  · refine Fin.cases ?_ (fun j => ?_) b
    · simp [residualFill, acResidual_sum_zero]
    · simp [residualFill]

/-- Explicit 2-chain filling of a 1-cycle. -/
def oneCycleFilling (z : OneCycle R (p:=p) (q:=q) (r:=r)) :
    Triangle → R
  | (a,b,c) =>
      (if c = 0 then abPart R z a b else 0) +
        residualFill R z (a,b,c)

lemma oneCycleFilling_ab
    (z : OneCycle R (p:=p) (q:=q) (r:=r)) (a:A) (b:B) :
    ∑ c:C, oneCycleFilling R z (a,b,c) = abPart R z a b := by
  unfold oneCycleFilling
  rw [Finset.sum_add_distrib, residualFill_depth_sum_zero]
  simp

lemma oneCycleFilling_ac
    (z : OneCycle R (p:=p) (q:=q) (r:=r)) (a:A) (c:C) :
    -(∑ b:B, oneCycleFilling R z (a,b,c)) = acPart R z a c := by
  unfold oneCycleFilling
  rw [Finset.sum_add_distrib, residualFill_row_sum]
  by_cases hc : c = 0
  · subst c
    simp only [if_true]
    unfold acResidual
    simp
  · simp only [hc, if_false, Finset.sum_const_zero, zero_add]
    unfold acResidual
    simp [hc]

lemma oneCycleFilling_bc
    (z : OneCycle R (p:=p) (q:=q) (r:=r)) (b:B) (c:C) :
    (∑ a:A, oneCycleFilling R z (a,b,c)) = bcPart R z b c := by
  unfold oneCycleFilling
  rw [Finset.sum_add_distrib, residualFill_column_sum]
  by_cases hc : c = 0
  · subst c
    simp only [if_true]
    unfold bcResidual
    simp
  · simp only [hc, if_false, Finset.sum_const_zero, zero_add]
    unfold bcResidual
    simp [hc]

/-- The explicit filling maps to the original 1-cycle. -/
theorem boundary2R_oneCycleFilling
    (z : OneCycle R (p:=p) (q:=q) (r:=r)) :
    (boundary2R R (p:=p) (q:=q) (r:=r)).mulVec
      (oneCycleFilling R z) = (z : Edge → R) := by
  funext e
  rcases e with ab | rest
  · rcases ab with ⟨a,b⟩
    rw [boundary2R_mulVec_ab]
    exact oneCycleFilling_ab R z a b
  · rcases rest with ac | bc
    · rcases ac with ⟨a,c⟩
      rw [boundary2R_mulVec_ac]
      exact oneCycleFilling_ac R z a c
    · rcases bc with ⟨b,c⟩
      rw [boundary2R_mulVec_bc]
      exact oneCycleFilling_bc R z b c


/-- The coefficient-generic oriented incidence maps form a chain complex. -/
theorem boundary1R_boundary2R_zero :
    boundary1R R (p:=p) (q:=q) (r:=r) *
      boundary2R R (p:=p) (q:=q) (r:=r) = 0 := by
  apply Matrix.mulVec_injective
  funext x
  rw [← Matrix.mulVec_mulVec]
  rw [Matrix.zero_mulVec]
  funext v
  simp only [Pi.zero_apply]
  rcases v with a | rest
  · rw [boundary1R_mulVec_A]
    simp_rw [boundary2R_mulVec_ab, boundary2R_mulVec_ac]
    rw [Finset.sum_neg_distrib]
    have hswap :
        (∑ b:B, ∑ c:C, x (a,b,c)) =
          ∑ c:C, ∑ b:B, x (a,b,c) := Finset.sum_comm
    linear_combination -hswap
  · rcases rest with b | c
    · rw [boundary1R_mulVec_B]
      simp_rw [boundary2R_mulVec_ab, boundary2R_mulVec_bc]
      have hswap :
          (∑ a:A, ∑ c:C, x (a,b,c)) =
            ∑ c:C, ∑ a:A, x (a,b,c) := Finset.sum_comm
      linear_combination hswap
    · rw [boundary1R_mulVec_C]
      simp_rw [boundary2R_mulVec_ac, boundary2R_mulVec_bc]
      rw [Finset.sum_neg_distrib]
      have hswap :
          (∑ a:A, ∑ b:B, x (a,b,c)) =
            ∑ b:B, ∑ a:A, x (a,b,c) := Finset.sum_comm
      linear_combination -hswap

/-- Every triangle boundary is a 1-cycle. -/
theorem boundary2R_range_le_boundary1R_ker :
    LinearMap.range
        (boundary2R R (p:=p) (q:=q) (r:=r)).mulVecLin ≤
      LinearMap.ker
        (boundary1R R (p:=p) (q:=q) (r:=r)).mulVecLin := by
  rw [LinearMap.range_le_ker_iff]
  rw [← Matrix.mulVecLin_mul, boundary1R_boundary2R_zero]
  exact Matrix.mulVecLin_zero

/-- Every 1-cycle is hit by the explicit filling. -/
theorem boundary1R_ker_le_boundary2R_range :
    LinearMap.ker
        (boundary1R R (p:=p) (q:=q) (r:=r)).mulVecLin ≤
      LinearMap.range
        (boundary2R R (p:=p) (q:=q) (r:=r)).mulVecLin := by
  intro z hz
  refine ⟨oneCycleFilling R ⟨z,hz⟩, ?_⟩
  exact boundary2R_oneCycleFilling R ⟨z,hz⟩

/-- **Coefficient-universal exactness in degree one.** -/
theorem boundary_exact_R :
    LinearMap.range
        (boundary2R R (p:=p) (q:=q) (r:=r)).mulVecLin =
      LinearMap.ker
        (boundary1R R (p:=p) (q:=q) (r:=r)).mulVecLin :=
  le_antisymm
    (boundary2R_range_le_boundary1R_ker R)
    (boundary1R_ker_le_boundary2R_range R)

/-- Boundaries as a submodule of 1-cycles over `R`. -/
def firstHomologyBoundariesR :
    Submodule R
      (LinearMap.ker
        (boundary1R R (p:=p) (q:=q) (r:=r)).mulVecLin) :=
  (LinearMap.range
      (boundary2R R (p:=p) (q:=q) (r:=r)).mulVecLin).comap
    (LinearMap.ker
      (boundary1R R (p:=p) (q:=q) (r:=r)).mulVecLin).subtype

theorem firstHomologyBoundariesR_top :
    firstHomologyBoundariesR R (p:=p) (q:=q) (r:=r) = ⊤ := by
  unfold firstHomologyBoundariesR
  rw [boundary_exact_R R]
  ext x
  simp

/-- First homology over any commutative coefficient ring. -/
abbrev FirstHomologyR :=
  (LinearMap.ker
      (boundary1R R (p:=p) (q:=q) (r:=r)).mulVecLin) ⧸
    firstHomologyBoundariesR R (p:=p) (q:=q) (r:=r)

/-- `H1(K(p+1,q+1,r+1);R)` is the zero module for every commutative ring. -/
theorem firstHomologyR_subsingleton :
    Subsingleton (FirstHomologyR R (p:=p) (q:=q) (r:=r)) := by
  unfold FirstHomologyR
  rw [firstHomologyBoundariesR_top]
  infer_instance

end D0.Topology.GenericTripartiteFirstHomologyRing
