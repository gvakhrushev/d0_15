import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic

namespace D0.Dynamics

open Matrix
open scoped BigOperators

/-- Two-state carrier for the finite D0 time-transition operator. -/
abbrev TimeIx := Fin 2

/-- Integer 2 by 2 matrix carrier for the D0 time-transition operator. -/
abbrev ZMat2 := Matrix TimeIx TimeIx Int

/-- Fundamental D0 time-transition operator. -/
def T : ZMat2 := !![0, 1; 1, -1]

theorem trace_T1 : Matrix.trace T = -1 := by
  native_decide

theorem trace_T2 : Matrix.trace (T ^ 2) = 3 := by
  native_decide

theorem trace_T3 : Matrix.trace (T ^ 3) = -4 := by
  native_decide

theorem trace_T4 : Matrix.trace (T ^ 4) = 7 := by
  native_decide

theorem trace_T5 : Matrix.trace (T ^ 5) = -11 := by
  native_decide

theorem trace_T6 : Matrix.trace (T ^ 6) = 18 := by
  native_decide

theorem trace_evolution_unfolds_d0_geometry :
    Matrix.trace (T ^ 2) = 3 /\
    Matrix.trace (T ^ 3) = -4 /\
    Matrix.trace (T ^ 5) = -11 := by
  exact And.intro trace_T2 (And.intro trace_T3 trace_T5)

theorem det_T : Matrix.det T = -1 := by
  native_decide

theorem det_T_pow (n : Nat) :
    Matrix.det (T ^ n) = (-1 : Int) ^ n := by
  rw [Matrix.det_pow, det_T]

theorem neg_one_pow_square (n : Nat) :
    ((-1 : Int) ^ n) * ((-1 : Int) ^ n) = 1 := by
  induction n with
  | zero => norm_num
  | succ n ih => simp [pow_succ, ih]

/-- Determinant-square form of finite toral volume conservation. -/
theorem toral_volume_conservation_square (n : Nat) :
    Matrix.det (T ^ n) * Matrix.det (T ^ n) = 1 := by
  rw [det_T_pow]
  exact neg_one_pow_square n

/-- Unsigned Lucas numbers in integer form. -/
def lucas : Nat -> Int
  | 0 => 2
  | 1 => 1
  | n + 2 => lucas (n + 1) + lucas n

/-- Signed Lucas trace associated with the D0 time-transition operator. -/
def signedLucasTrace (n : Nat) : Int :=
  (-1 : Int) ^ n * lucas n

theorem signedLucasTrace_recurrence (n : Nat) :
    signedLucasTrace (n + 2) =
      signedLucasTrace n - signedLucasTrace (n + 1) := by
  unfold signedLucasTrace
  change
    (-1 : Int) ^ (n + 2) * (lucas (n + 1) + lucas n) =
      (-1 : Int) ^ n * lucas n -
        (-1 : Int) ^ (n + 1) * lucas (n + 1)
  have hp2 : (-1 : Int) ^ (n + 2) = (-1 : Int) ^ n := by
    calc
      (-1 : Int) ^ (n + 2) =
          (-1 : Int) ^ n * (-1 : Int) ^ 2 := by rw [pow_add]
      _ = (-1 : Int) ^ n := by norm_num
  have hp1 : (-1 : Int) ^ (n + 1) = -((-1 : Int) ^ n) := by
    rw [pow_succ]
    ring
  rw [hp2, hp1]
  ring

/-- Cayley-Hamilton relation for the finite time-transition matrix. -/
theorem T_squared_eq_identity_minus_T :
    T ^ 2 = 1 - T := by
  ext i j
  fin_cases i <;> fin_cases j <;> native_decide

theorem T_charpoly_quadratic_relation :
    T ^ 2 + T - 1 = 0 := by
  ext i j
  fin_cases i <;> fin_cases j <;> native_decide

theorem T_pow_recurrence (n : Nat) :
    T ^ (n + 2) = T ^ n - T ^ (n + 1) := by
  calc
    T ^ (n + 2) = T ^ n * T ^ 2 := by rw [pow_add]
    _ = T ^ n * (1 - T) := by rw [T_squared_eq_identity_minus_T]
    _ = T ^ n * 1 - T ^ n * T := by rw [mul_sub]
    _ = T ^ n - T ^ (n + 1) := by rw [mul_one, pow_succ]

theorem trace_recurrence (n : Nat) :
    Matrix.trace (T ^ (n + 2)) =
      Matrix.trace (T ^ n) - Matrix.trace (T ^ (n + 1)) := by
  rw [T_pow_recurrence, Matrix.trace_sub]

theorem trace_T0 :
    Matrix.trace (T ^ 0) = 2 := by
  native_decide

theorem signedLucasTrace_zero :
    signedLucasTrace 0 = 2 := by
  native_decide

theorem signedLucasTrace_one :
    signedLucasTrace 1 = -1 := by
  native_decide

theorem trace_T_pow_eq_signed_lucas (n : Nat) :
    Matrix.trace (T ^ n) = signedLucasTrace n := by
  exact
    Nat.twoStepInduction
      (by native_decide)
      (by native_decide)
      (fun n ih0 ih1 => by
        calc
          Matrix.trace (T ^ (n + 2)) =
              Matrix.trace (T ^ n) - Matrix.trace (T ^ (n + 1)) :=
            trace_recurrence n
          _ = signedLucasTrace n - signedLucasTrace (n + 1) := by
            rw [ih0, ih1]
          _ = signedLucasTrace (n + 2) := by
            rw [signedLucasTrace_recurrence n])
      n

end D0.Dynamics
