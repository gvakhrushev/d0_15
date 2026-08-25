import D0.Topology.GenericTripartiteFirstHomologyRing
import Mathlib.LinearAlgebra.Isomorphisms
import Mathlib.Tactic

/-!
# D0-GENERIC-TRIPARTITE-ZERO-HOMOLOGY-RING-001

For every commutative coefficient ring `R`, the image of the graph boundary
is exactly the augmentation-zero submodule.  An explicit spanning-tree
filling proves

```
range ∂₁(R) = ker augmentation,
H₀(K(p+1,q+1,r+1);R) ≃ R.
```

No rank or field argument is used.
-/

namespace D0.Topology.GenericTripartiteZeroHomologyRing
open scoped BigOperators
open Matrix
open D0.SelfReading.TypedIncidenceCarriers
open D0.Topology.GenericTripartiteHomology
open D0.Topology.GenericTripartiteTopHomologyRing
open D0.Topology.GenericTripartiteFirstHomologyRing

variable (R : Type) [CommRing R]
variable {p q r : ℕ}
local notation "A" => Fin (p + 1)
local notation "B" => Fin (q + 1)
local notation "C" => Fin (r + 1)
local notation "Vertex" => GenericVertex p q r
local notation "Edge" => GenericEdge p q r

/-- Sum of all vertex coefficients. -/
def augmentationR : (Vertex → R) →ₗ[R] R :=
  Fintype.linearCombination R (fun _ : Vertex => (1:R))

lemma augmentationR_apply (x : Vertex → R) :
    augmentationR R x =
      (∑ a:A, x (Sum.inl a)) +
        (∑ b:B, x (Sum.inr (Sum.inl b))) +
        ∑ c:C, x (Sum.inr (Sum.inr c)) := by
  simp [augmentationR, Fintype.linearCombination_apply,
    Fintype.sum_sum_type]
  abel

lemma augmentationR_surjective :
    Function.Surjective (augmentationR R (p:=p) (q:=q) (r:=r)) := by
  intro value
  refine ⟨Pi.single (Sum.inl (0:A)) value, ?_⟩
  rw [augmentationR_apply]
  simp [Pi.single_apply]

lemma augmentationR_boundary1R_zero (x : Edge → R) :
    augmentationR R
      ((boundary1R R (p:=p) (q:=q) (r:=r)).mulVec x) = 0 := by
  rw [augmentationR_apply]
  simp_rw [boundary1R_mulVec_A, boundary1R_mulVec_B,
    boundary1R_mulVec_C]
  have hab :
      (∑ a:A, ∑ b:B, x (Sum.inl (a,b))) =
        ∑ b:B, ∑ a:A, x (Sum.inl (a,b)) := Finset.sum_comm
  have hac :
      (∑ a:A, ∑ c:C, x (Sum.inr (Sum.inl (a,c)))) =
        ∑ c:C, ∑ a:A, x (Sum.inr (Sum.inl (a,c))) := Finset.sum_comm
  have hbc :
      (∑ b:B, ∑ c:C, x (Sum.inr (Sum.inr (b,c)))) =
        ∑ c:C, ∑ b:B, x (Sum.inr (Sum.inr (b,c))) := Finset.sum_comm
  simp only [Finset.sum_sub_distrib, Finset.sum_add_distrib,
    Finset.sum_neg_distrib]
  linear_combination -hab - hac - hbc

/-- Explicit spanning-tree edge chain for a zero-chain. -/
def zeroChainFilling (y : Vertex → R) : Edge → R
  | Sum.inl (a,b) =>
      Fin.cases
        (Fin.cases
          (y (Sum.inr (Sum.inl (0:B))) +
            ∑ i : Fin p, y (Sum.inl i.succ))
          (fun j => y (Sum.inr (Sum.inl j.succ)))
          b)
        (fun i => Fin.cases (-y (Sum.inl i.succ)) (fun _ => 0) b)
        a
  | Sum.inr (Sum.inl (a,c)) =>
      Fin.cases (y (Sum.inr (Sum.inr c))) (fun _ => 0) a
  | Sum.inr (Sum.inr _) => 0

lemma boundary1R_zeroChainFilling
    (y : Vertex → R)
    (hy : augmentationR R (p:=p) (q:=q) (r:=r) y = 0) :
    (boundary1R R (p:=p) (q:=q) (r:=r)).mulVec
      (zeroChainFilling R y) = y := by
  funext v
  rcases v with a | rest
  · refine Fin.cases ?_ (fun i => ?_) a
    · rw [boundary1R_mulVec_A, Fin.sum_univ_succ]
      simp only [zeroChainFilling, Fin.cases_zero, Fin.cases_succ,
        Finset.sum_const_zero, add_zero]
      rw [augmentationR_apply] at hy
      rw [Fin.sum_univ_succ, Fin.sum_univ_succ] at hy
      linear_combination -hy
    · rw [boundary1R_mulVec_A, Fin.sum_univ_succ]
      simp [zeroChainFilling]
  · rcases rest with b | c
    · refine Fin.cases ?_ (fun j => ?_) b
      · rw [boundary1R_mulVec_B, Fin.sum_univ_succ]
        simp [zeroChainFilling]
      · rw [boundary1R_mulVec_B, Fin.sum_univ_succ]
        simp [zeroChainFilling]
    · rw [boundary1R_mulVec_C, Fin.sum_univ_succ]
      simp [zeroChainFilling]

/-- The graph boundary image is exactly the augmentation-zero submodule. -/
theorem boundary1R_range_eq_augmentationR_ker :
    LinearMap.range
        (boundary1R R (p:=p) (q:=q) (r:=r)).mulVecLin =
      LinearMap.ker (augmentationR R (p:=p) (q:=q) (r:=r)) := by
  apply le_antisymm
  · intro y hy
    rcases hy with ⟨x,rfl⟩
    rw [LinearMap.mem_ker, Matrix.mulVecLin_apply]
    exact augmentationR_boundary1R_zero R x
  · intro y hy
    rw [LinearMap.mem_ker] at hy
    refine ⟨zeroChainFilling R y, ?_⟩
    exact boundary1R_zeroChainFilling R y hy

/-- Degree-zero homology over `R`. -/
abbrev ZeroHomologyR :=
  (Vertex → R) ⧸
    LinearMap.range
      (boundary1R R (p:=p) (q:=q) (r:=r)).mulVecLin

/-- **Connectedness over every commutative coefficient ring:** `H0 ≃ R`. -/
noncomputable def zeroHomologyEquivR :
    ZeroHomologyR R (p:=p) (q:=q) (r:=r) ≃ₗ[R] R :=
  (Submodule.quotEquivOfEq
      (LinearMap.range
        (boundary1R R (p:=p) (q:=q) (r:=r)).mulVecLin)
      (LinearMap.ker (augmentationR R (p:=p) (q:=q) (r:=r)))
      (boundary1R_range_eq_augmentationR_ker R)).trans
    ((augmentationR R (p:=p) (q:=q) (r:=r)).quotKerEquivOfSurjective
      (augmentationR_surjective R))

end D0.Topology.GenericTripartiteZeroHomologyRing
