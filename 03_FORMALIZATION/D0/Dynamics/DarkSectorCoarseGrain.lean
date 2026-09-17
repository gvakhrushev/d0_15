import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic

namespace D0.Dynamics

open scoped BigOperators

/-- Discrete archive branch orientation sign. -/
def darkSign (n : Nat) : Int :=
  (-1 : Int) ^ n

theorem dark_sign_even (n : Nat) :
    darkSign (2 * n) = 1 := by
  simp [darkSign, pow_mul]

theorem dark_sign_odd (n : Nat) :
    darkSign (2 * n + 1) = -1 := by
  unfold darkSign
  rw [pow_succ]
  have h_even : (-1 : Int) ^ (2 * n) = 1 := by
    exact dark_sign_even n
  rw [h_even]
  norm_num

/-- Even archive windows cancel the alternating branch sign exactly. -/
def alternatingWindowSum : Nat -> Int
  | 0 => 0
  | n + 1 => Finset.sum (Finset.range (2 * (n + 1)))
      (fun k => (-1 : Int) ^ k)

theorem alternating_even_window_sum_zero (N : Nat) :
    Finset.sum (Finset.range (2 * N)) (fun k => (-1 : Int) ^ k) = 0 := by
  induction N with
  | zero => simp
  | succ N ih =>
      rw [show 2 * (N + 1) = 2 * N + 2 by omega]
      rw [Finset.sum_range_succ, Finset.sum_range_succ]
      rw [ih]
      have h_even : (-1 : Int) ^ (2 * N) = 1 := by
        exact dark_sign_even N
      have h_odd : (-1 : Int) ^ (2 * N + 1) = -1 := by
        exact dark_sign_odd N
      rw [h_odd, h_even]
      norm_num

/-- Book-facing record for an even-window coarse-grained archive readout. -/
structure CoarseGrainedDarkReadout where
  window : Nat
  even_window : exists N, window = 2 * N
  response : Int

theorem dark_sector_even_window_readout_zero (N : Nat) :
    Finset.sum (Finset.range (2 * N)) (fun k => darkSign k) = 0 := by
  exact alternating_even_window_sum_zero N

end D0.Dynamics
