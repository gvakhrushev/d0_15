import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.BigOperators.Fin
import D0.Geometry.ArchivePhaseDistance
import D0.Geometry.ArchiveWeightedGraph
import D0.Geometry.ArchiveCanonicalDirichlet

open scoped BigOperators

namespace D0

local notation:70 A " *ᵥ " B => Matrix.mulVec A B

def MatrixSymmetric {N : Type} (L : Matrix N N ℝ) : Prop :=
  ∀ i j, L i j = L j i

def archiveDegree (n : Nat) (i : archivePhaseIndex n) : ℝ :=
  ∑ j : archivePhaseIndex n, if archiveAdjacent n i j then (1 : ℝ) else 0

def archiveCanonicalLaplacian (n : Nat) : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ :=
  fun i j => if i = j then archiveDegree n i else if archiveAdjacent n i j then -1 else 0

def matrixQuadraticForm {N : Type} [Fintype N] (L : Matrix N N ℝ) (f : N → ℝ) : ℝ :=
  ∑ i : N, ∑ j : N, f i * L i j * f j

theorem archiveCanonicalLaplacian_symmetric (n : Nat) :
  MatrixSymmetric (archiveCanonicalLaplacian n) := by
  intro a b
  unfold archiveCanonicalLaplacian
  by_cases h : a = b
  · subst b
    simp
  · simp [h, Ne.symm h]
    by_cases ha : archiveAdjacent n a b
    · have hb := archiveAdjacent_symmetric n ha
      simp [ha, hb]
    · have hb : ¬ archiveAdjacent n b a := fun hc => ha (archiveAdjacent_symmetric n hc)
      simp [ha, hb]

theorem archiveCanonicalLaplacian_constant_zero (n : Nat) (c : ℝ) :
  (archiveCanonicalLaplacian n *ᵥ (fun _ => c)) = 0 := by
  funext i
  unfold archiveCanonicalLaplacian Matrix.mulVec dotProduct
  dsimp
  rw [← Finset.sum_mul]
  have hsum : ∑ j : archivePhaseIndex n, (if i = j then archiveDegree n i else if archiveAdjacent n i j then -1 else 0) = 0 := by
    have h_split := Finset.sum_erase_add Finset.univ (fun j => if i = j then archiveDegree n i else if archiveAdjacent n i j then -1 else 0) (Finset.mem_univ i)
    rw [← h_split]
    have h_erase_sum : ∑ j ∈ Finset.univ.erase i, (if i = j then archiveDegree n i else if archiveAdjacent n i j then -1 else 0) =
      ∑ j ∈ Finset.univ.erase i, (if archiveAdjacent n i j then -1 else 0) := by
      apply Finset.sum_congr rfl
      intro j hj
      have h_ne : i ≠ j := (Finset.ne_of_mem_erase hj).symm
      rw [if_neg h_ne]
    rw [h_erase_sum]
    simp only [if_true, eq_self_iff_true]
    unfold archiveDegree
    have h_erase : ∑ j : archivePhaseIndex n, (if archiveAdjacent n i j then (1:ℝ) else 0) =
      ∑ j ∈ Finset.univ.erase i, (if archiveAdjacent n i j then (1:ℝ) else 0) := by
      have h_split2 := Finset.sum_erase_add Finset.univ (fun j => if archiveAdjacent n i j then (1:ℝ) else 0) (Finset.mem_univ i)
      rw [← h_split2]
      have h_ii : ¬ archiveAdjacent n i i := archiveAdjacent_irreflexive n i
      simp only [h_ii, if_false, add_zero]
    rw [h_erase]
    rw [← Finset.sum_add_distrib]
    have h_zero : ∀ j ∈ Finset.univ.erase i,
      (if archiveAdjacent n i j then (-1:ℝ) else 0) + (if archiveAdjacent n i j then (1:ℝ) else 0) = 0 := by
      intro j _
      split_ifs <;> linarith
    apply Finset.sum_eq_zero
    exact h_zero
  rw [hsum, zero_mul]

theorem archiveDirichletEnergy_nonnegative (n : Nat) (f : archivePhaseIndex n → ℝ) :
  0 ≤ archiveDirichletEnergy n f := by
  unfold archiveDirichletEnergy
  apply Finset.sum_nonneg
  intro i _
  apply Finset.sum_nonneg
  intro j _
  split_ifs
  · positivity
  · linarith

theorem matrixQuadraticForm_eq_dirichlet (n : Nat) (f : archivePhaseIndex n → ℝ) :
  matrixQuadraticForm (archiveCanonicalLaplacian n) f = (1/2 : ℝ) * archiveDirichletEnergy n f := by
  unfold matrixQuadraticForm archiveCanonicalLaplacian archiveDirichletEnergy
  have sum_f_i_sq : ∑ i : archivePhaseIndex n, ∑ j : archivePhaseIndex n, (if archiveAdjacent n i j then (f i)^2 else 0) =
    ∑ i : archivePhaseIndex n, (f i)^2 * archiveDegree n i := by
    apply Finset.sum_congr rfl
    intro i _
    unfold archiveDegree
    have h_term : ∀ j, (if archiveAdjacent n i j then (f i)^2 else 0) = (f i)^2 * (if archiveAdjacent n i j then 1 else 0) := by
      intro j
      split_ifs <;> ring
    simp_rw [h_term]
    rw [← Finset.mul_sum]
  have sum_f_j_sq : ∑ i : archivePhaseIndex n, ∑ j : archivePhaseIndex n, (if archiveAdjacent n i j then (f j)^2 else 0) =
    ∑ i : archivePhaseIndex n, (f i)^2 * archiveDegree n i := by
    rw [Finset.sum_comm]
    have h_fact : ∀ j : archivePhaseIndex n, (∑ i : archivePhaseIndex n, if archiveAdjacent n i j then (f j)^2 else 0) =
      (f j)^2 * archiveDegree n j := by
      intro j
      unfold archiveDegree
      have h_symm : ∀ i, archiveAdjacent n j i ↔ archiveAdjacent n i j := by
        intro i
        constructor <;> exact fun h => archiveAdjacent_symmetric n h
      have h_term : ∀ i, (if archiveAdjacent n i j then (f j)^2 else 0) = (f j)^2 * (if archiveAdjacent n j i then 1 else 0) := by
        intro i
        by_cases h : archiveAdjacent n i j
        · have hj := archiveAdjacent_symmetric n h
          simp [h, hj]
        · have hj : ¬ archiveAdjacent n j i := fun hc => h (archiveAdjacent_symmetric n hc)
          simp [h, hj]
      simp_rw [h_term]
      rw [← Finset.mul_sum]
    simp_rw [h_fact]
  have h_L_term : ∀ i j, f i * (if i = j then archiveDegree n i else if archiveAdjacent n i j then -1 else 0) * f j =
    if i = j then (f i)^2 * archiveDegree n i else if archiveAdjacent n i j then -(f i * f j) else 0 := by
    intro i j
    split_ifs with h1 h2
    · subst h1; ring
    · ring
    · ring
  simp_rw [h_L_term]
  have h_sum_split : ∀ i, (∑ j, (if i = j then (f i)^2 * archiveDegree n i else if archiveAdjacent n i j then -(f i * f j) else 0)) =
    (f i)^2 * archiveDegree n i - (∑ j, if archiveAdjacent n i j then f i * f j else 0) := by
    intro i
    have h_split := Finset.sum_erase_add Finset.univ (fun j => if i = j then (f i)^2 * archiveDegree n i else if archiveAdjacent n i j then -(f i * f j) else 0) (Finset.mem_univ i)
    rw [← h_split]
    have h_erase_sum : ∑ j ∈ Finset.univ.erase i, (if i = j then (f i)^2 * archiveDegree n i else if archiveAdjacent n i j then -(f i * f j) else 0) =
      ∑ j ∈ Finset.univ.erase i, (if archiveAdjacent n i j then -(f i * f j) else 0) := by
      apply Finset.sum_congr rfl
      intro j hj
      have h_ne : i ≠ j := (Finset.ne_of_mem_erase hj).symm
      rw [if_neg h_ne]
    rw [h_erase_sum]
    simp only [if_true, eq_self_iff_true]
    have h_erase2 : (∑ j, if archiveAdjacent n i j then f i * f j else 0) =
      ∑ j ∈ Finset.univ.erase i, if archiveAdjacent n i j then f i * f j else 0 := by
      have h_split2 := Finset.sum_erase_add Finset.univ (fun j => if archiveAdjacent n i j then f i * f j else 0) (Finset.mem_univ i)
      rw [← h_split2]
      have h_ii : ¬ archiveAdjacent n i i := archiveAdjacent_irreflexive n i
      simp only [h_ii, if_false, add_zero]
    rw [h_erase2]
    have h_neg : (∑ j ∈ Finset.univ.erase i, if archiveAdjacent n i j then -(f i * f j) else 0) =
      - ∑ j ∈ Finset.univ.erase i, if archiveAdjacent n i j then f i * f j else 0 := by
      rw [← Finset.sum_neg_distrib]
      apply Finset.sum_congr rfl
      intro j _
      split_ifs <;> simp
    rw [h_neg]
    ring
  simp_rw [h_sum_split]
  rw [Finset.sum_sub_distrib]
  have h_term_split : ∀ i j, (if archiveAdjacent n i j then (f i - f j)^2 else 0) =
    (if archiveAdjacent n i j then (f i)^2 else 0) - 2 * (if archiveAdjacent n i j then f i * f j else 0) + (if archiveAdjacent n i j then (f j)^2 else 0) := by
    intro i j
    split_ifs <;> ring
  simp_rw [h_term_split]
  simp_rw [Finset.sum_add_distrib, Finset.sum_sub_distrib]
  rw [sum_f_i_sq, sum_f_j_sq]
  simp_rw [← Finset.mul_sum]
  ring

theorem archiveCanonicalLaplacian_nonnegative (n : Nat) (f : archivePhaseIndex n → ℝ) :
  0 ≤ matrixQuadraticForm (archiveCanonicalLaplacian n) f := by
  rw [matrixQuadraticForm_eq_dirichlet]
  have hD := archiveDirichletEnergy_nonnegative n f
  nlinarith

end D0
