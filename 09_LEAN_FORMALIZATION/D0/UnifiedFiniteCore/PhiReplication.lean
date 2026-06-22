import Mathlib.NumberTheory.Real.GoldenRatio
import Mathlib.Data.Nat.Fib.Basic
import Mathlib.Tactic

/-!
# D0-v15 Unified spine §11 — Fibonacci / Pisot replication of the coupled determinant

Replicating the coupled edge unitary `U_E` with Fibonacci multiplicities `F_n` gives the action
`A_n = F_n · A_1` with `A_1 = −log det(I − zU_E)`. Two exact facts hold:

* **Fibonacci recurrence** `A_{n+1} = A_n + A_{n-1}` (from `Nat.fib_add_two`).
* **Pisot correction** `A_{n+1} − φ·A_n = ψⁿ · A_1` with `|ψ| = φ⁻¹ < 1` (Binet's formula), so the
  golden-scaled increment decays geometrically with alternating sign — a genuine Pisot tail.

(The determinant `det(I − zU_E)` whose log is `A_1` is verified exactly in
`05_CERTS/verify_unified_feedback.py`; here we prove the replication algebra over `ℝ`.)
-/

namespace D0.UnifiedFiniteCore.PhiReplication

open Real
open scoped goldenRatio

/-- The replicated action `A_n = F_n · A₁`. -/
noncomputable def A (A1 : ℝ) (n : ℕ) : ℝ := (Nat.fib n : ℝ) * A1

/-- **Fibonacci recurrence** of the replicated action: `A_{n+2} = A_{n+1} + A_n`. -/
theorem replication_recurrence (A1 : ℝ) (n : ℕ) :
    A A1 (n + 2) = A A1 (n + 1) + A A1 n := by
  unfold A
  rw [Nat.fib_add_two]
  push_cast
  ring

/-- **Pisot correction identity** (Binet): `F_{n+1} − φ·F_n = ψⁿ`. -/
theorem fib_pisot (n : ℕ) : (Nat.fib (n + 1) : ℝ) - φ * (Nat.fib n : ℝ) = ψ ^ n := by
  rw [coe_fib_eq (n + 1), coe_fib_eq n, pow_succ, pow_succ]
  have h5 : Real.sqrt 5 ≠ 0 := by positivity
  have hd : φ - ψ = Real.sqrt 5 := goldenRatio_sub_goldenConj
  field_simp
  linear_combination (ψ ^ n) * hd

/-- **Pisot correction of the action**: `A_{n+1} − φ·A_n = ψⁿ · A₁`. -/
theorem action_pisot (A1 : ℝ) (n : ℕ) :
    A A1 (n + 1) - φ * A A1 n = ψ ^ n * A1 := by
  unfold A
  linear_combination A1 * fib_pisot n

/-- **Pisot decay**: `|ψ| < 1` (the golden conjugate), so the correction is a decaying tail. -/
theorem pisot_decay : |ψ| < 1 := by
  rw [abs_lt]
  exact ⟨neg_one_lt_goldenConj, by linarith [goldenConj_neg]⟩

/-- **D0-v15 §11.** Fibonacci replication recurrence + golden Pisot correction with `|ψ| < 1`. -/
theorem phi_replication (A1 : ℝ) (n : ℕ) :
    A A1 (n + 2) = A A1 (n + 1) + A A1 n ∧
    A A1 (n + 1) - φ * A A1 n = ψ ^ n * A1 ∧
    |ψ| < 1 :=
  ⟨replication_recurrence A1 n, action_pisot A1 n, pisot_decay⟩

end D0.UnifiedFiniteCore.PhiReplication
