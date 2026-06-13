import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace D0.Cosmology

theorem positive_lower_bound_blocks_eternal_linear_underdensity (x : ℕ → ℝ) (c v la M : ℝ)
    (h_seq : ∀ k, x k = c + v * la^k)
    (h_bound : ∀ k, x k ≥ M)
    (hv : v < 0)
    (hla : la > 1) :
    False := by
  have h_lam_pos : la - 1 > 0 := by linarith
  have h_bernoulli : ∀ k : ℕ, la^k ≥ 1 + (k : ℝ) * (la - 1) := by
    intro k
    induction k with
    | zero => simp
    | succ k ih =>
      have h_lam_nonneg : la ≥ 0 := by linarith
      have h_pow_succ : la^(k + 1) = la^k * la := by ring
      rw [h_pow_succ]
      have h1 : la^k * la ≥ (1 + (k : ℝ) * (la - 1)) * la := by
        exact mul_le_mul_of_nonneg_right ih h_lam_nonneg
      have h2 : (1 + (k : ℝ) * (la - 1)) * la ≥ 1 + (k + 1 : ℝ) * (la - 1) := by
        have h_diff : (1 + (k : ℝ) * (la - 1)) * la - (1 + (k + 1 : ℝ) * (la - 1)) = (k : ℝ) * (la - 1)^2 := by
          ring
        have h_nonneg : (k : ℝ) * (la - 1)^2 ≥ 0 := by
          have hk : (k : ℝ) ≥ 0 := Nat.cast_nonneg k
          have h_sq : (la - 1)^2 ≥ 0 := sq_nonneg (la - 1)
          exact mul_nonneg hk h_sq
        linarith
      push_cast
      linarith
  let A := c + v - M
  let B := - (v * (la - 1))
  have h_B_pos : B > 0 := by
    dsimp [B]
    have : v * (la - 1) < 0 := mul_neg_of_neg_of_pos hv h_lam_pos
    linarith
  rcases exists_nat_gt (A / B) with ⟨k, hk⟩
  have h_xk := h_bound k
  rw [h_seq k] at h_xk
  have h_v_pow : v * la^k ≤ v * (1 + (k : ℝ) * (la - 1)) := by
    have h_v_neg : v ≤ 0 := le_of_lt hv
    have h_bern := h_bernoulli k
    nlinarith
  have h_xk_le : c + v * la^k ≤ c + v + (k : ℝ) * v * (la - 1) := by linarith
  have h_contra : M ≤ c + v + (k : ℝ) * v * (la - 1) := by linarith
  have h_rew : (k : ℝ) * B ≤ A := by
    dsimp [A, B]
    linarith
  have h_k_B : (k : ℝ) * B > A := by
    exact (div_lt_iff₀ h_B_pos).mp hk
  linarith

end D0.Cosmology
