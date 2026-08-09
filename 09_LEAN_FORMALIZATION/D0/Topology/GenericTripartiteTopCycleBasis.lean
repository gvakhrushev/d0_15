import D0.Topology.GenericTripartiteHomology
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.Tactic

/-!
# D0-GENERIC-TRIPARTITE-TOP-CYCLE-BASIS-001

The generic rank theorem gives `β₂=p*q*r`.  This module identifies those
classes explicitly.  After choosing vertex `0` in each canonical zone, every
triple `(i,j,k) : Fin p × Fin q × Fin r` defines the tensor

```
(e_(i+1)-e_0) ⊗ (e_(j+1)-e_0) ⊗ (e_(k+1)-e_0).
```

As a 2-chain it is supported on eight triangles with coefficients `±1`: the
octahedral 2-sphere on the two selected vertices in each zone.  These cycles
form a basis of `ker ∂₂`, and every top cycle is reconstructed from its values
on the all-nonroot triangles.
-/

namespace D0.Topology.GenericTripartiteTopCycleBasis

open scoped BigOperators
open Matrix
open D0.SelfReading.TypedIncidenceCarriers
open D0.Topology.GenericTripartiteHomology

variable {p q r : ℕ}

local notation "A" => Fin (p + 1)
local notation "B" => Fin (q + 1)
local notation "C" => Fin (r + 1)
local notation "Triangle" => GenericTriangle p q r

/-- One basis index for every nonroot vertex in each zone. -/
abbrev TopCycleIndex (p q r : ℕ) := Fin p × Fin q × Fin r

/-- The reduced coordinate vector `e_(i+1)-e_0`. -/
def rootDifference {n : ℕ} (i : Fin n) : Fin (n + 1) → ℚ :=
  fun x => if x = i.succ then 1 else if x = 0 then -1 else 0

@[simp] theorem rootDifference_zero {n : ℕ} (i : Fin n) :
    rootDifference i (0 : Fin (n + 1)) = -1 := by
  unfold rootDifference
  rw [if_neg (Fin.succ_ne_zero i).symm]
  simp

@[simp] theorem rootDifference_succ {n : ℕ} (i j : Fin n) :
    rootDifference i j.succ = if j = i then 1 else 0 := by
  by_cases h : j = i
  · subst j
    simp [rootDifference]
  · simp [rootDifference, h, Fin.succ_inj]

theorem rootDifference_sum {n : ℕ} (i : Fin n) :
    ∑ x : Fin (n + 1), rootDifference i x = 0 := by
  rw [Fin.sum_univ_succ]
  simp

/-- The octahedral 2-chain indexed by one nonroot vertex in every zone. -/
def topCycleVec (i : TopCycleIndex p q r) : Triangle → ℚ
  | (a, b, c) =>
      rootDifference i.1 a *
        rootDifference i.2.1 b *
        rootDifference i.2.2 c

private theorem sum_indicator_ab
    {α β γ : Type} [Fintype α] [Fintype β] [Fintype γ]
    [DecidableEq α] [DecidableEq β]
    (u : α → ℚ) (v : β → ℚ) (w : γ → ℚ)
    (a : α) (b : β) (s : ℚ) :
    (∑ x : α, ∑ y : β, ∑ z : γ,
      (if a = x ∧ b = y then s else 0) * (u x * v y * w z)) =
      s * u a * v b * (∑ z : γ, w z) := by
  calc
    _ = ∑ x : α, ∑ y : β,
        if a = x ∧ b = y then
          ∑ z : γ, s * (u x * v y * w z)
        else 0 := by
      apply Fintype.sum_congr
      intro x
      apply Fintype.sum_congr
      intro y
      by_cases h : a = x ∧ b = y <;> simp [h]
    _ = ∑ x : α,
        if a = x then
          ∑ z : γ, s * (u x * v b * w z)
        else 0 := by
      apply Fintype.sum_congr
      intro x
      by_cases hx : a = x
      · subst x
        simpa using Fintype.sum_ite_eq b
          (fun y : β => ∑ z : γ, s * (u a * v y * w z))
      · simp [hx]
    _ = ∑ z : γ, s * (u a * v b * w z) := by
      simpa using Fintype.sum_ite_eq a
        (fun x : α => ∑ z : γ, s * (u x * v b * w z))
    _ = s * u a * v b * (∑ z : γ, w z) := by
      rw [Finset.mul_sum]
      apply Fintype.sum_congr
      intro z
      ring

private theorem sum_indicator_ac
    {α β γ : Type} [Fintype α] [Fintype β] [Fintype γ]
    [DecidableEq α] [DecidableEq γ]
    (u : α → ℚ) (v : β → ℚ) (w : γ → ℚ)
    (a : α) (c : γ) (s : ℚ) :
    (∑ x : α, ∑ y : β, ∑ z : γ,
      (if a = x ∧ c = z then s else 0) * (u x * v y * w z)) =
      s * u a * w c * (∑ y : β, v y) := by
  calc
    _ = ∑ x : α, ∑ y : β,
        if a = x then
          ∑ z : γ,
            (if c = z then s else 0) * (u x * v y * w z)
        else 0 := by
      apply Fintype.sum_congr
      intro x
      apply Fintype.sum_congr
      intro y
      by_cases hx : a = x
      · subst x
        simp
      · simp [hx]
    _ = ∑ x : α, ∑ y : β,
        if a = x then s * (u x * v y * w c) else 0 := by
      apply Fintype.sum_congr
      intro x
      apply Fintype.sum_congr
      intro y
      by_cases hx : a = x
      · simp only [hx, if_true]
        simpa using Fintype.sum_ite_eq c
          (fun z : γ => s * (u x * v y * w z))
      · simp [hx]
    _ = ∑ y : β, s * (u a * v y * w c) := by
      rw [Finset.sum_comm]
      apply Fintype.sum_congr
      intro y
      simpa using Fintype.sum_ite_eq a
        (fun x : α => s * (u x * v y * w c))
    _ = s * u a * w c * (∑ y : β, v y) := by
      rw [Finset.mul_sum]
      apply Fintype.sum_congr
      intro y
      ring

private theorem sum_indicator_bc
    {α β γ : Type} [Fintype α] [Fintype β] [Fintype γ]
    [DecidableEq β] [DecidableEq γ]
    (u : α → ℚ) (v : β → ℚ) (w : γ → ℚ)
    (b : β) (c : γ) (s : ℚ) :
    (∑ x : α, ∑ y : β, ∑ z : γ,
      (if b = y ∧ c = z then s else 0) * (u x * v y * w z)) =
      s * v b * w c * (∑ x : α, u x) := by
  calc
    _ = ∑ x : α, s * (u x * v b * w c) := by
      apply Fintype.sum_congr
      intro x
      calc
        (∑ y : β, ∑ z : γ,
          (if b = y ∧ c = z then s else 0) * (u x * v y * w z)) =
            ∑ y : β,
              if b = y then s * (u x * v y * w c) else 0 := by
              apply Fintype.sum_congr
              intro y
              by_cases hy : b = y
              · subst y
                simpa using Fintype.sum_ite_eq c
                  (fun z : γ => s * (u x * v b * w z))
              · simp [hy]
        _ = s * (u x * v b * w c) := by
          simpa using Fintype.sum_ite_eq b
            (fun y : β => s * (u x * v y * w c))
    _ = s * v b * w c * (∑ x : α, u x) := by
      rw [Finset.mul_sum]
      apply Fintype.sum_congr
      intro x
      ring

/-- Every octahedral chain has zero edge boundary. -/
theorem boundary_topCycleVec_zero (i : TopCycleIndex p q r) :
    (boundary2 (p := p) (q := q) (r := r)).mulVec
      (topCycleVec i) = 0 := by
  funext e
  rcases e with ab | rest
  · rcases ab with ⟨a, b⟩
    simp only [Matrix.mulVec, dotProduct, boundary2, topCycleVec,
      Fintype.sum_prod_type]
    rw [sum_indicator_ab, rootDifference_sum]
    simp
  · rcases rest with ac | bc
    · rcases ac with ⟨a, c⟩
      simp only [Matrix.mulVec, dotProduct, boundary2, topCycleVec,
        Fintype.sum_prod_type]
      rw [sum_indicator_ac, rootDifference_sum]
      simp
    · rcases bc with ⟨b, c⟩
      simp only [Matrix.mulVec, dotProduct, boundary2, topCycleVec,
        Fintype.sum_prod_type]
      rw [sum_indicator_bc, rootDifference_sum]
      simp

/-- The octahedral chain bundled as an actual element of `ker ∂₂`. -/
noncomputable def topCycle (i : TopCycleIndex p q r) :
    LinearMap.ker
      (boundary2 (p := p) (q := q) (r := r)).mulVecLin :=
  ⟨topCycleVec i, by
    rw [LinearMap.mem_ker, Matrix.mulVecLin_apply]
    exact boundary_topCycleVec_zero i⟩

@[simp] theorem topCycle_coe (i : TopCycleIndex p q r) :
    (topCycle i : Triangle → ℚ) = topCycleVec i := rfl

/-- On all-nonroot triangles the coordinate matrix is the identity. -/
theorem topCycle_nonroot_coordinate (i j : TopCycleIndex p q r) :
    topCycleVec j (i.1.succ, i.2.1.succ, i.2.2.succ) =
      if i = j then 1 else 0 := by
  simp only [topCycleVec, rootDifference_succ]
  by_cases h1 : i.1 = j.1
  · by_cases h2 : i.2.1 = j.2.1
    · by_cases h3 : i.2.2 = j.2.2
      · have h : i = j := by
          rcases i with ⟨ia, ib, ic⟩
          rcases j with ⟨ja, jb, jc⟩
          simp_all
        simp [h]
      · have h : i ≠ j := by
          intro hij
          exact h3 (congrArg (fun x => x.2.2) hij)
        simp [h, h3]
    · have h : i ≠ j := by
        intro hij
        exact h2 (congrArg (fun x => x.2.1) hij)
      simp [h, h2]
  · have h : i ≠ j := by
      intro hij
      exact h1 (congrArg (fun x => x.1) hij)
    simp [h, h1]

/-- Read a top cycle on one all-nonroot triangle. -/
def topCycleCoordinate (i : TopCycleIndex p q r) :
    LinearMap.ker
        (boundary2 (p := p) (q := q) (r := r)).mulVecLin →ₗ[ℚ] ℚ :=
  (LinearMap.proj
      (R := ℚ) (φ := fun _ : Triangle => ℚ)
      (i.1.succ, i.2.1.succ, i.2.2.succ)).comp
    (LinearMap.ker
      (boundary2 (p := p) (q := q) (r := r)).mulVecLin).subtype

@[simp] theorem topCycleCoordinate_apply
    (i : TopCycleIndex p q r)
    (z : LinearMap.ker
      (boundary2 (p := p) (q := q) (r := r)).mulVecLin) :
    topCycleCoordinate i z =
      (z : Triangle → ℚ)
        (i.1.succ, i.2.1.succ, i.2.2.succ) := rfl

/-- The explicit octahedral cycles are linearly independent. -/
theorem topCycle_linearIndependent :
    LinearIndependent ℚ
      (topCycle (p := p) (q := q) (r := r)) := by
  rw [Fintype.linearIndependent_iff]
  intro g h i
  have hcoord := congrArg (topCycleCoordinate i) h
  simp only [map_sum, map_smul, map_zero, topCycleCoordinate_apply,
    topCycle_coe, smul_eq_mul] at hcoord
  rw [show (∑ j, g j * topCycleVec j
      (i.1.succ, i.2.1.succ, i.2.2.succ)) = g i by
    simp_rw [topCycle_nonroot_coordinate i]
    simp] at hcoord
  exact hcoord

private theorem topCycleIndex_card :
    Fintype.card (TopCycleIndex p q r) = p * q * r := by
  simp [TopCycleIndex, Nat.mul_assoc]

/-- **Explicit canonical basis of rational top homology.** -/
noncomputable def topCycleBasis :
    Module.Basis (TopCycleIndex p q r) ℚ
      (LinearMap.ker
        (boundary2 (p := p) (q := q) (r := r)).mulVecLin) :=
  basisOfLinearIndependentOfCardEqFinrank'
    (topCycle (p := p) (q := q) (r := r))
    (topCycle_linearIndependent (p := p) (q := q) (r := r))
    (by
      rw [topCycleIndex_card]
      exact
        (boundary2_kernel_finrank
          (p := p) (q := q) (r := r)).symm)

@[simp] theorem topCycleBasis_apply (i : TopCycleIndex p q r) :
    topCycleBasis i = topCycle i := by
  simp [topCycleBasis]

/-- Basis coefficients are the all-nonroot triangle values. -/
theorem topCycle_repr_eq_coordinate
    (z : LinearMap.ker
      (boundary2 (p := p) (q := q) (r := r)).mulVecLin)
    (i : TopCycleIndex p q r) :
    (topCycleBasis (p := p) (q := q) (r := r)).repr z i =
      topCycleCoordinate i z := by
  have h := congrArg (topCycleCoordinate i)
    ((topCycleBasis (p := p) (q := q) (r := r)).sum_repr z)
  simp only [map_sum, map_smul, topCycleBasis_apply,
    topCycleCoordinate_apply, topCycle_coe, smul_eq_mul] at h
  rw [show (∑ j,
      (topCycleBasis (p := p) (q := q) (r := r)).repr z j *
        topCycleVec j (i.1.succ, i.2.1.succ, i.2.2.succ)) =
      (topCycleBasis (p := p) (q := q) (r := r)).repr z i by
    simp_rw [topCycle_nonroot_coordinate i]
    simp] at h
  exact h

/-- Every top cycle is reconstructed from its nonroot triangle coordinates. -/
theorem topCycle_reconstruction
    (z : LinearMap.ker
      (boundary2 (p := p) (q := q) (r := r)).mulVecLin) :
    ∑ i : TopCycleIndex p q r,
      topCycleCoordinate i z • topCycle i = z := by
  calc
    _ = ∑ i : TopCycleIndex p q r,
        (topCycleBasis (p := p) (q := q) (r := r)).repr z i •
          topCycleBasis i := by
      apply Fintype.sum_congr
      intro i
      rw [topCycleBasis_apply, topCycle_repr_eq_coordinate]
    _ = z :=
      (topCycleBasis (p := p) (q := q) (r := r)).sum_repr z

/-- Explicit equivalence `H₂ ≃ ℚ^(Fin p × Fin q × Fin r)`. -/
noncomputable def topCycleCoordinateEquiv :
    LinearMap.ker
        (boundary2 (p := p) (q := q) (r := r)).mulVecLin ≃ₗ[ℚ]
      (TopCycleIndex p q r → ℚ) :=
  (topCycleBasis (p := p) (q := q) (r := r)).equivFun

@[simp] theorem topCycleCoordinateEquiv_apply
    (z : LinearMap.ker
      (boundary2 (p := p) (q := q) (r := r)).mulVecLin)
    (i : TopCycleIndex p q r) :
    topCycleCoordinateEquiv z i = topCycleCoordinate i z := by
  rw [topCycleCoordinateEquiv, Module.Basis.equivFun_apply,
    topCycle_repr_eq_coordinate]

end D0.Topology.GenericTripartiteTopCycleBasis
