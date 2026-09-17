import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Real.Basic

open scoped BigOperators

namespace D0.Spectrum

def tensor_product_I {G N : Type} [Fintype G] [DecidableEq G] (Γ_SM : Matrix N N ℝ) : Matrix (G × N) (G × N) ℝ :=
  fun ⟨g1, n1⟩ ⟨g2, n2⟩ => (if g1 = g2 then 1 else 0) * Γ_SM n1 n2

theorem stage1_tensor_exactness {G N : Type} [Fintype G] [DecidableEq G] [Fintype N]
    (Γ_lift : Matrix (G × N) (G × N) ℝ) (Γ_SM : Matrix N N ℝ)
    (h_off : ∀ (g1 g2 : G) (n1 n2 : N), g1 ≠ g2 → Γ_lift ⟨g1, n1⟩ ⟨g2, n2⟩ = 0)
    (h_diag : ∀ (g : G) (n1 n2 : N), Γ_lift ⟨g, n1⟩ ⟨g, n2⟩ = Γ_SM n1 n2) :
    Γ_lift = tensor_product_I Γ_SM := by
  ext ⟨g1, n1⟩ ⟨g2, n2⟩
  unfold tensor_product_I
  dsimp
  split_ifs with hg
  · subst g2
    rw [one_mul]
    exact h_diag g1 n1 n2
  · rw [zero_mul]
    exact h_off g1 g2 n1 n2 hg

def cyclicShiftMatrix (n : Nat) : Matrix (Fin n) (Fin n) ℝ :=
  fun i j => if j.val = (i.val + 1) % n then 1 else 0

def kronecker_C_I {G N : Type} [Fintype G] [DecidableEq G] [DecidableEq N] (C_G : Matrix G G ℝ) : Matrix (G × N) (G × N) ℝ :=
  fun ⟨g1, n1⟩ ⟨g2, n2⟩ => C_G g1 g2 * (if n1 = n2 then 1 else 0)

def shift_g {n : Nat} [NeZero n] (g : Fin n) (k : Nat) : Fin n :=
  ⟨(g.val + k) % n, Nat.mod_lt _ (NeZero.pos n)⟩

lemma shift_g_zero {n : Nat} [NeZero n] (g : Fin n) : shift_g g 0 = g := by
  unfold shift_g
  simp only [add_zero]
  exact Fin.ext (Nat.mod_eq_of_lt g.isLt)

lemma shift_g_step {n : Nat} [NeZero n] (g : Fin n) (k : Nat) :
    shift_g g (k + 1) = shift_g (shift_g g k) 1 := by
  unfold shift_g
  ext
  dsimp
  rcases n with _|n
  · rcases g with ⟨_, isLt⟩
    contradiction
  rcases n with _|n
  · omega
  · have h1 : 1 % (n + 2) = 1 := rfl
    have h_mod := Nat.add_mod (g.val + k) 1 (n + 2)
    change (g.val + (k + 1)) % (n + 2) = ((g.val + k) % (n + 2) + 1) % (n + 2)
    have h_eq : g.val + (k + 1) = g.val + k + 1 := by omega
    rw [h_eq, h_mod, h1]

lemma flavor_blindness_step {N : Type} [Fintype N] [DecidableEq N] {n : Nat} [NeZero n]
    (Γ_lift : Matrix (Fin n × N) (Fin n × N) ℝ)
    (h_off : ∀ (g1 g2 : Fin n) (n1 n2 : N), g1 ≠ g2 → Γ_lift ⟨g1, n1⟩ ⟨g2, n2⟩ = 0)
    (h_comm : Γ_lift * (kronecker_C_I (cyclicShiftMatrix n)) = (kronecker_C_I (cyclicShiftMatrix n)) * Γ_lift)
    (g : Fin n) (n1 n2 : N) :
    Γ_lift (g, n1) (g, n2) = Γ_lift (shift_g g 1, n1) (shift_g g 1, n2) := by
  let target_g : Fin n := shift_g g 1
  have h_comm_v := congr_fun (congr_fun h_comm (g, n1)) (target_g, n2)
  rw [Matrix.mul_apply, Matrix.mul_apply] at h_comm_v
  unfold kronecker_C_I cyclicShiftMatrix at h_comm_v
  dsimp at h_comm_v
  have h_lhs_corr : (∑ x : Fin n × N, Γ_lift (g, n1) x * ((if target_g.val = (x.1.val + 1) % n then (1 : ℝ) else 0) * (if x.2 = n2 then (1 : ℝ) else 0))) = Γ_lift (g, n1) (g, n2) := by
    rw [Fintype.sum_prod_type]
    dsimp
    have h_zero : ∀ (g' : Fin n) (n' : N), g' ≠ g → Γ_lift (g, n1) (g', n') * ((if target_g.val = (g'.val + 1) % n then (1 : ℝ) else 0) * (if n' = n2 then (1 : ℝ) else 0)) = 0 := by
      intro g' n' hne
      rw [h_off g g' n1 n' hne.symm, zero_mul]
    have h_sum_g : (∑ g' : Fin n, ∑ n' : N, Γ_lift (g, n1) (g', n') * ((if target_g.val = (g'.val + 1) % n then (1 : ℝ) else 0) * (if n' = n2 then (1 : ℝ) else 0))) =
        ∑ n' : N, Γ_lift (g, n1) (g, n') * ((if target_g.val = (g.val + 1) % n then (1 : ℝ) else 0) * (if n' = n2 then (1 : ℝ) else 0)) := by
      rw [Finset.sum_eq_single g]
      · intro g' _ hne
        rw [Finset.sum_eq_zero]
        intro n' _
        exact h_zero g' n' hne
      · intro h
        exact False.elim (h (Finset.mem_univ _))
    rw [h_sum_g]
    have h_sum_n : (∑ n' : N, Γ_lift (g, n1) (g, n') * ((if target_g.val = (g.val + 1) % n then (1 : ℝ) else 0) * (if n' = n2 then (1 : ℝ) else 0))) = Γ_lift (g, n1) (g, n2) := by
      have h_cond : target_g.val = (g.val + 1) % n := rfl
      simp only [h_cond, if_true, one_mul]
      rw [Finset.sum_eq_single n2]
      · simp
      · intro n' _ hne
        rw [if_neg hne, mul_zero]
      · intro h
        exact False.elim (h (Finset.mem_univ _))
    exact h_sum_n

  have h_rhs_corr : (∑ x : Fin n × N, ((if x.1.val = (g.val + 1) % n then (1 : ℝ) else 0) * (if n1 = x.2 then (1 : ℝ) else 0)) * Γ_lift x (target_g, n2)) = Γ_lift (target_g, n1) (target_g, n2) := by
    rw [Fintype.sum_prod_type]
    dsimp
    have h_zero : ∀ (g' : Fin n) (n' : N), g' ≠ target_g → ((if g'.val = (g.val + 1) % n then (1 : ℝ) else 0) * (if n1 = n' then (1 : ℝ) else 0)) * Γ_lift (g', n') (target_g, n2) = 0 := by
      intro g' n' hne
      rw [h_off g' target_g n' n2 hne, mul_zero]
    have h_sum_g : (∑ g' : Fin n, ∑ n' : N, ((if g'.val = (g.val + 1) % n then (1 : ℝ) else 0) * (if n1 = n' then (1 : ℝ) else 0)) * Γ_lift (g', n') (target_g, n2)) =
        ∑ n' : N, ((if target_g.val = (g.val + 1) % n then (1 : ℝ) else 0) * (if n1 = n' then (1 : ℝ) else 0)) * Γ_lift (target_g, n') (target_g, n2) := by
      rw [Finset.sum_eq_single target_g]
      · intro g' _ hne
        rw [Finset.sum_eq_zero]
        intro n' _
        exact h_zero g' n' hne
      · intro h
        exact False.elim (h (Finset.mem_univ _))
    rw [h_sum_g]
    have h_sum_n : (∑ n' : N, ((if target_g.val = (g.val + 1) % n then (1 : ℝ) else 0) * (if n1 = n' then (1 : ℝ) else 0)) * Γ_lift (target_g, n') (target_g, n2)) = Γ_lift (target_g, n1) (target_g, n2) := by
      have h_cond : target_g.val = (g.val + 1) % n := rfl
      simp only [h_cond, if_true, one_mul]
      rw [Finset.sum_eq_single n1]
      · simp
      · intro n' _ hne
        rw [if_neg hne.symm, zero_mul]
      · intro h
        exact False.elim (h (Finset.mem_univ _))
    exact h_sum_n

  rw [h_lhs_corr, h_rhs_corr] at h_comm_v
  exact h_comm_v

lemma flavor_blindness_step_k {N : Type} [Fintype N] [DecidableEq N] {n : Nat} [NeZero n]
    (Γ_lift : Matrix (Fin n × N) (Fin n × N) ℝ)
    (h_off : ∀ (g1 g2 : Fin n) (n1 n2 : N), g1 ≠ g2 → Γ_lift ⟨g1, n1⟩ ⟨g2, n2⟩ = 0)
    (h_comm : Γ_lift * (kronecker_C_I (cyclicShiftMatrix n)) = (kronecker_C_I (cyclicShiftMatrix n)) * Γ_lift)
    (g : Fin n) (k : Nat) (n1 n2 : N) :
    Γ_lift (g, n1) (g, n2) = Γ_lift (shift_g g k, n1) (shift_g g k, n2) := by
  induction k with
  | zero =>
    rw [shift_g_zero]
  | succ k ih =>
    rw [ih]
    have h_step := flavor_blindness_step Γ_lift h_off h_comm (shift_g g k) n1 n2
    rw [shift_g_step]
    exact h_step

theorem stage2_flavor_blindness {N : Type} [Fintype N] [DecidableEq N] {n : Nat} [NeZero n]
    (Γ_lift : Matrix (Fin n × N) (Fin n × N) ℝ)
    (h_off : ∀ (g1 g2 : Fin n) (n1 n2 : N), g1 ≠ g2 → Γ_lift ⟨g1, n1⟩ ⟨g2, n2⟩ = 0)
    (h_comm : Γ_lift * (kronecker_C_I (cyclicShiftMatrix n)) = (kronecker_C_I (cyclicShiftMatrix n)) * Γ_lift)
    (g1 g2 : Fin n) (n1 n2 : N) :
    Γ_lift (g1, n1) (g1, n2) = Γ_lift (g2, n1) (g2, n2) := by
  have h_eq := flavor_blindness_step_k Γ_lift h_off h_comm g1 (g2.val + n - g1.val) n1 n2
  have h_val : (g1.val + (g2.val + n - g1.val)) % n = g2.val := by
    have : g1.val + (g2.val + n - g1.val) = g2.val + n := by omega
    rw [this, Nat.add_mod_right]
    exact Nat.mod_eq_of_lt g2.isLt
  have : shift_g g1 (g2.val + n - g1.val) = g2 := Fin.ext h_val
  rw [this] at h_eq
  exact h_eq

theorem stage3_tensor_exactness {N : Type} [Fintype N] [DecidableEq N] {n : Nat} [NeZero n]
    (Γ_lift : Matrix (Fin n × N) (Fin n × N) ℝ) (Γ_SM : Matrix N N ℝ)
    (h_off : ∀ (g1 g2 : Fin n) (n1 n2 : N), g1 ≠ g2 → Γ_lift ⟨g1, n1⟩ ⟨g2, n2⟩ = 0)
    (h_comm : Γ_lift * (kronecker_C_I (cyclicShiftMatrix n)) = (kronecker_C_I (cyclicShiftMatrix n)) * Γ_lift)
    (g0 : Fin n) (h_g0 : ∀ n1 n2 : N, Γ_lift (g0, n1) (g0, n2) = Γ_SM n1 n2) :
    Γ_lift = tensor_product_I Γ_SM := by
  apply stage1_tensor_exactness Γ_lift Γ_SM h_off
  intro g n1 n2
  rw [stage2_flavor_blindness Γ_lift h_off h_comm g g0 n1 n2]
  exact h_g0 n1 n2

theorem stage3_trace_relation {G N : Type} [Fintype G] [DecidableEq G] [Fintype N]
    (Γ_SM : Matrix N N ℝ) :
    Matrix.trace (tensor_product_I (G := G) Γ_SM) = Fintype.card G * Matrix.trace Γ_SM := by
  unfold Matrix.trace tensor_product_I Matrix.diag
  dsimp
  rw [Fintype.sum_prod_type]
  simp only [if_true, one_mul]
  rw [Finset.sum_const]
  simp only [Finset.card_univ, nsmul_eq_mul]

theorem stage3_trace_relation_three {G N : Type} [Fintype G] [DecidableEq G] [Fintype N]
    (Γ_SM : Matrix N N ℝ) (h_card : Fintype.card G = 3) :
    Matrix.trace (tensor_product_I (G := G) Γ_SM) = 3 * Matrix.trace Γ_SM := by
  rw [stage3_trace_relation Γ_SM, h_card]
  push_cast
  rfl

end D0.Spectrum
