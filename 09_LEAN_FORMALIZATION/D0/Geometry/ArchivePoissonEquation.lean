import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Data.Real.Basic
import D0.Geometry.ArchiveCanonicalLaplacian
import D0.Geometry.ArchiveWeakField
import D0.Geometry.ArchiveWeightedGraph
import D0.Geometry.ArchiveBianchiIdentity

open scoped BigOperators

namespace D0

theorem poisson_requires_neutral_source {n : Nat}
  (φ : ArchivePotential n) (ρ : archivePhaseIndex n → ℝ)
  (h : ArchivePoissonEquation φ ρ) :
  NeutralSource ρ := by
  unfold NeutralSource
  rw [← h]
  unfold Matrix.mulVec dotProduct
  rw [Finset.sum_comm]
  have h_eq : ∀ y : archivePhaseIndex n, (∑ i : archivePhaseIndex n, archiveCanonicalLaplacian n i y * φ y) = φ y * ∑ i : archivePhaseIndex n, archiveCanonicalLaplacian n i y := by
    intro y
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i _
    ring
  simp_rw [h_eq]
  have h_sym : ∀ y : archivePhaseIndex n, (∑ i : archivePhaseIndex n, archiveCanonicalLaplacian n i y) = 0 := by
    intro y
    have h_row := archiveCanonicalLaplacian_row_sum_zero n y
    have h_swap : (∑ i : archivePhaseIndex n, archiveCanonicalLaplacian n i y) = ∑ i : archivePhaseIndex n, archiveCanonicalLaplacian n y i := by
      apply Finset.sum_congr rfl
      intro i _
      exact archiveCanonicalLaplacian_symmetric n i y
    rw [h_swap, h_row]
  simp_rw [h_sym, mul_zero, Finset.sum_const_zero]

lemma ψ_eq_of_adjacent {n : Nat} (ψ : archivePhaseIndex n → ℝ)
  (hL : Matrix.mulVec (archiveCanonicalLaplacian n) ψ = 0)
  (i j : archivePhaseIndex n) (hadj : archiveAdjacent n i j) :
  ψ i = ψ j := by
  have h_qf : matrixQuadraticForm (archiveCanonicalLaplacian n) ψ = 0 := by
    unfold matrixQuadraticForm
    have h_zero : ∀ i : archivePhaseIndex n, (∑ j : archivePhaseIndex n, ψ i * archiveCanonicalLaplacian n i j * ψ j) = 0 := by
      intro i
      have hL0 : (Matrix.mulVec (archiveCanonicalLaplacian n) ψ) i = 0 := by
        rw [hL]
        rfl
      unfold Matrix.mulVec dotProduct at hL0
      calc
        (∑ j : archivePhaseIndex n, ψ i * archiveCanonicalLaplacian n i j * ψ j) =
          ψ i * ∑ j : archivePhaseIndex n, archiveCanonicalLaplacian n i j * ψ j := by
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro j _
          ring
        _ = ψ i * 0 := by rw [hL0]
        _ = 0 := by ring
    simp_rw [h_zero, Finset.sum_const_zero]
  rw [matrixQuadraticForm_eq_dirichlet] at h_qf
  have h_dir : archiveDirichletEnergy n ψ = 0 := by
    linarith
  unfold archiveDirichletEnergy at h_dir
  have h_term_nonneg : ∀ i j : archivePhaseIndex n, 0 ≤ if archiveAdjacent n i j then (ψ i - ψ j)^2 else 0 := by
    intro i j
    split_ifs
    · positivity
    · linarith
  have h_sum_j_nonneg : ∀ i : archivePhaseIndex n, 0 ≤ ∑ j : archivePhaseIndex n, if archiveAdjacent n i j then (ψ i - ψ j)^2 else 0 := by
    intro i
    apply Finset.sum_nonneg
    intro j _
    exact h_term_nonneg i j
  have h_inner_zero : ∀ i : archivePhaseIndex n, (∑ j : archivePhaseIndex n, if archiveAdjacent n i j then (ψ i - ψ j)^2 else 0) = 0 := by
    intro i
    exact (Finset.sum_eq_zero_iff_of_nonneg (fun i _ => h_sum_j_nonneg i)).mp h_dir i (Finset.mem_univ i)
  have h_term_zero : (if archiveAdjacent n i j then (ψ i - ψ j)^2 else 0) = 0 := by
    exact (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => h_term_nonneg i j)).mp (h_inner_zero i) j (Finset.mem_univ j)
  rw [if_pos hadj] at h_term_zero
  have h_diff_zero : ψ i - ψ j = 0 := sq_eq_zero_iff.mp h_term_zero
  linarith

lemma adjacent_step {n : Nat} (k : Nat) (h1 : k + 1 < archiveFibers n) :
  archiveAdjacent n ⟨k + 1, h1⟩ ⟨k, by omega⟩ := by
  unfold archiveAdjacent cyclicDistance archiveFibers
  have ht1 : (k + 1 + (n + 2) - k) % (n + 2) = 1 := by
    have : k + 1 + (n + 2) - k = 1 + (n + 2) := by omega
    rw [this, Nat.add_mod_right]
    exact Nat.mod_eq_of_lt (by omega)
  have ht2 : (k + (n + 2) - (k + 1)) % (n + 2) = n + 1 := by
    have : k + (n + 2) - (k + 1) = n + 1 := by omega
    rw [this]
    exact Nat.mod_eq_of_lt (by omega)
  rw [ht1, ht2]
  rw [min_eq_left]
  omega

lemma ψ_constant_helper {n : Nat} (ψ : archivePhaseIndex n → ℝ)
  (h : ∀ i j, archiveAdjacent n i j → ψ i = ψ j) (k : Nat) (hk : k < archiveFibers n) :
  ψ ⟨k, hk⟩ = ψ ⟨0, by unfold archiveFibers; omega⟩ := by
  induction k with
  | zero => rfl
  | succ k ih =>
    have hk_lt : k < archiveFibers n := by omega
    have h_adj := adjacent_step k hk
    have heq := h ⟨k + 1, hk⟩ ⟨k, hk_lt⟩ h_adj
    rw [heq, ih hk_lt]

theorem poisson_solution_unique_mod_constant {n : Nat}
  (ρ : archivePhaseIndex n → ℝ) (_hρ : NeutralSource ρ)
  (φ₁ φ₂ : ArchivePotential n)
  (h1 : ArchivePoissonEquation φ₁ ρ)
  (h2 : ArchivePoissonEquation φ₂ ρ) :
  ∃ c : ℝ, φ₁ - φ₂ = constantPotential c := by
  let ψ := φ₁ - φ₂
  have hL : Matrix.mulVec (archiveCanonicalLaplacian n) ψ = 0 := by
    funext i
    dsimp [Matrix.mulVec, dotProduct, ψ]
    change (∑ j : archivePhaseIndex n, archiveCanonicalLaplacian n i j * (φ₁ j - φ₂ j)) = 0
    have h_split : (∑ j : archivePhaseIndex n, archiveCanonicalLaplacian n i j * (φ₁ j - φ₂ j)) =
        (∑ j, archiveCanonicalLaplacian n i j * φ₁ j) - (∑ j, archiveCanonicalLaplacian n i j * φ₂ j) := by
      simp_rw [mul_sub, Finset.sum_sub_distrib]
    rw [h_split]
    have h1_val : (∑ j : archivePhaseIndex n, archiveCanonicalLaplacian n i j * φ₁ j) = ρ i := by
      have := congr_fun h1 i
      unfold Matrix.mulVec dotProduct at this
      exact this
    have h2_val : (∑ j : archivePhaseIndex n, archiveCanonicalLaplacian n i j * φ₂ j) = ρ i := by
      have := congr_fun h2 i
      unfold Matrix.mulVec dotProduct at this
      exact this
    rw [h1_val, h2_val, sub_self]
  have h_adj : ∀ i j, archiveAdjacent n i j → ψ i = ψ j := by
    intro i j hadj
    exact ψ_eq_of_adjacent ψ hL i j hadj
  have h_const : ∀ i : archivePhaseIndex n, ψ i = ψ ⟨0, by unfold archiveFibers; omega⟩ := by
    intro i
    have := ψ_constant_helper ψ h_adj i.val i.isLt
    have h_eq_i : i = ⟨i.val, i.isLt⟩ := by simp
    rw [h_eq_i]
    exact this
  use ψ ⟨0, by unfold archiveFibers; omega⟩
  funext i
  change φ₁ i - φ₂ i = ψ ⟨0, by unfold archiveFibers; omega⟩
  rw [← h_const i]
  rfl

end D0
