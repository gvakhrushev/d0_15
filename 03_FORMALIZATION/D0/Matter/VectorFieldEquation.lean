import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic.Linarith
import D0.Algebra.GaugeActionSignBridge

namespace D0.Matter

def isSkew {n : Type} (M : Matrix n n ℝ) : Prop :=
  M.transpose = -M

lemma skew_orthogonal_to_all_skew_is_zero {n : Type} [Fintype n] [DecidableEq n]
    (M : Matrix n n ℝ) (hM_skew : isSkew M)
    (h_orth : ∀ dA : Matrix n n ℝ, isSkew dA → Matrix.trace (dA.transpose * M) = 0) :
    M = 0 := by
  have h_orth_M := h_orth M hM_skew
  unfold isSkew at hM_skew
  have h_trans : M.transpose = -M := hM_skew
  rw [h_trans, Matrix.neg_mul, Matrix.trace_neg, neg_eq_zero] at h_orth_M
  exact (D0.Algebra.skew_square_trace_eq_zero_iff M h_trans).mp h_orth_M

theorem skew_stationarity_implies_vector_equation {n : Type} [Fintype n] [DecidableEq n]
    (L_vec : Matrix n n ℝ → Matrix n n ℝ)
    (A J : Matrix n n ℝ)
    (hA : isSkew A)
    (hJ : isSkew J)
    (hL : ∀ X, isSkew X → isSkew (L_vec X))
    (h_stat : ∀ dA, isSkew dA → Matrix.trace (dA.transpose * (L_vec A - J)) = 0) :
    L_vec A - J = 0 := by
  have h_res_skew : isSkew (L_vec A - J) := by
    unfold isSkew
    rw [Matrix.transpose_sub]
    have h1 := hL A hA
    unfold isSkew at h1 hJ
    rw [h1, hJ]
    rw [sub_neg_eq_add, add_comm, neg_sub]
    rfl
  exact skew_orthogonal_to_all_skew_is_zero (L_vec A - J) h_res_skew h_stat

theorem skew_stationarity_implies_vector_equation_eq {n : Type} [Fintype n] [DecidableEq n]
    (L_vec : Matrix n n ℝ → Matrix n n ℝ)
    (A J : Matrix n n ℝ)
    (hA : isSkew A)
    (hJ : isSkew J)
    (hL : ∀ X, isSkew X → isSkew (L_vec X))
    (h_stat : ∀ dA, isSkew dA → Matrix.trace (dA.transpose * (L_vec A - J)) = 0) :
    L_vec A = J := by
  have h_res := skew_stationarity_implies_vector_equation L_vec A J hA hJ hL h_stat
  exact sub_eq_zero.mp h_res

end D0.Matter
