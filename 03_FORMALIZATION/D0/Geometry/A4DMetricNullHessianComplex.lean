import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.FiniteDimensional.Basic
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Tactic

/-!
# D0.Geometry.A4DMetricNullHessianComplex

Exact finite polarized metric-response complex from merged #270/#292.

The 24x10 symbol is entered from the independently certified linear
coefficient matrices C_r. The nonzero-character rank proof uses the eleven
explicit projective 9x9 minor certificates and four Bézout unit-ideal
identities; no generic-rank shortcut is used.
-/

namespace D0.Geometry.A4DMetricNullHessianComplex

open BigOperators Matrix

noncomputable section


@[simp] private def cCoeff_row_0 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 7, 1 => (1 : ℚ) / 2
  | 9, 1 => (1 : ℚ) / 2
  | 5, 2 => (-1 : ℚ) / 2
  | 6, 3 => (-1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_1 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 5, 1 => (-1 : ℚ) / 2
  | 4, 2 => (1 : ℚ) / 2
  | 9, 2 => (1 : ℚ) / 2
  | 8, 3 => (-1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_2 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 6, 1 => (-1 : ℚ) / 2
  | 8, 2 => (-1 : ℚ) / 2
  | 4, 3 => (1 : ℚ) / 2
  | 7, 3 => (1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_3 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 2, 1 => (-1 : ℚ) / 2
  | 1, 2 => (1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_4 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 3, 1 => (-1 : ℚ) / 2
  | 1, 3 => (1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_5 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 3, 2 => (-1 : ℚ) / 2
  | 2, 3 => (1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_6 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 7, 0 => (-1 : ℚ) / 2
  | 9, 0 => (-1 : ℚ) / 2
  | 2, 2 => (1 : ℚ) / 2
  | 3, 3 => (1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_7 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 5, 0 => (1 : ℚ) / 2
  | 1, 2 => (-1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_8 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 6, 0 => (1 : ℚ) / 2
  | 1, 3 => (-1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_9 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 2, 0 => (1 : ℚ) / 2
  | 0, 2 => (-1 : ℚ) / 2
  | 9, 2 => (1 : ℚ) / 2
  | 8, 3 => (-1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_10 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 3, 0 => (1 : ℚ) / 2
  | 8, 2 => (-1 : ℚ) / 2
  | 0, 3 => (-1 : ℚ) / 2
  | 7, 3 => (1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_11 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 6, 2 => (1 : ℚ) / 2
  | 5, 3 => (-1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_12 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 5, 0 => (1 : ℚ) / 2
  | 2, 1 => (-1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_13 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 4, 0 => (-1 : ℚ) / 2
  | 9, 0 => (-1 : ℚ) / 2
  | 1, 1 => (1 : ℚ) / 2
  | 3, 3 => (1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_14 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 8, 0 => (1 : ℚ) / 2
  | 2, 3 => (-1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_15 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 1, 0 => (-1 : ℚ) / 2
  | 0, 1 => (1 : ℚ) / 2
  | 9, 1 => (-1 : ℚ) / 2
  | 6, 3 => (1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_16 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 8, 1 => (1 : ℚ) / 2
  | 5, 3 => (-1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_17 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 3, 0 => (1 : ℚ) / 2
  | 6, 1 => (-1 : ℚ) / 2
  | 0, 3 => (-1 : ℚ) / 2
  | 4, 3 => (1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_18 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 6, 0 => (1 : ℚ) / 2
  | 3, 1 => (-1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_19 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 8, 0 => (1 : ℚ) / 2
  | 3, 2 => (-1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_20 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 4, 0 => (-1 : ℚ) / 2
  | 7, 0 => (-1 : ℚ) / 2
  | 1, 1 => (1 : ℚ) / 2
  | 2, 2 => (1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_21 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 8, 1 => (1 : ℚ) / 2
  | 6, 2 => (-1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_22 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 1, 0 => (-1 : ℚ) / 2
  | 0, 1 => (1 : ℚ) / 2
  | 7, 1 => (-1 : ℚ) / 2
  | 5, 2 => (1 : ℚ) / 2
  | _, _ => 0

@[simp] private def cCoeff_row_23 (j : Fin 10) (r : Fin 4) : ℚ :=
  match j.val, r.val with
  | 2, 0 => (-1 : ℚ) / 2
  | 5, 1 => (1 : ℚ) / 2
  | 0, 2 => (1 : ℚ) / 2
  | 4, 2 => (-1 : ℚ) / 2
  | _, _ => 0

def cCoeff (i : Fin 24) (j : Fin 10) (r : Fin 4) : ℚ :=
  match i.val with
  | 0 => cCoeff_row_0 j r
  | 1 => cCoeff_row_1 j r
  | 2 => cCoeff_row_2 j r
  | 3 => cCoeff_row_3 j r
  | 4 => cCoeff_row_4 j r
  | 5 => cCoeff_row_5 j r
  | 6 => cCoeff_row_6 j r
  | 7 => cCoeff_row_7 j r
  | 8 => cCoeff_row_8 j r
  | 9 => cCoeff_row_9 j r
  | 10 => cCoeff_row_10 j r
  | 11 => cCoeff_row_11 j r
  | 12 => cCoeff_row_12 j r
  | 13 => cCoeff_row_13 j r
  | 14 => cCoeff_row_14 j r
  | 15 => cCoeff_row_15 j r
  | 16 => cCoeff_row_16 j r
  | 17 => cCoeff_row_17 j r
  | 18 => cCoeff_row_18 j r
  | 19 => cCoeff_row_19 j r
  | 20 => cCoeff_row_20 j r
  | 21 => cCoeff_row_21 j r
  | 22 => cCoeff_row_22 j r
  | 23 => cCoeff_row_23 j r
  | _ => 0

def cMatrixFromCoeff (d : Fin 4 → ℂ) : Matrix (Fin 24) (Fin 10) ℂ := fun i j =>
  ∑ r : Fin 4, (cCoeff i j r : ℂ) * d r


/-- Direct literal view of the same #292 coefficient table, used to keep
large exact certificates computationally small. The bridge theorem below
proves it entrywise equal to `cMatrix`. -/
@[simp] private def cMatrix_row_0 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 5 => ((-1 / 2 : ℚ) : ℂ) * d 2
  | 6 => ((-1 / 2 : ℚ) : ℂ) * d 3
  | 7 => ((1 / 2 : ℚ) : ℂ) * d 1
  | 9 => ((1 / 2 : ℚ) : ℂ) * d 1
  | _ => 0

@[simp] private def cMatrix_row_1 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 4 => ((1 / 2 : ℚ) : ℂ) * d 2
  | 5 => ((-1 / 2 : ℚ) : ℂ) * d 1
  | 8 => ((-1 / 2 : ℚ) : ℂ) * d 3
  | 9 => ((1 / 2 : ℚ) : ℂ) * d 2
  | _ => 0

@[simp] private def cMatrix_row_2 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 4 => ((1 / 2 : ℚ) : ℂ) * d 3
  | 6 => ((-1 / 2 : ℚ) : ℂ) * d 1
  | 7 => ((1 / 2 : ℚ) : ℂ) * d 3
  | 8 => ((-1 / 2 : ℚ) : ℂ) * d 2
  | _ => 0

@[simp] private def cMatrix_row_3 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 1 => ((1 / 2 : ℚ) : ℂ) * d 2
  | 2 => ((-1 / 2 : ℚ) : ℂ) * d 1
  | _ => 0

@[simp] private def cMatrix_row_4 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 1 => ((1 / 2 : ℚ) : ℂ) * d 3
  | 3 => ((-1 / 2 : ℚ) : ℂ) * d 1
  | _ => 0

@[simp] private def cMatrix_row_5 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 2 => ((1 / 2 : ℚ) : ℂ) * d 3
  | 3 => ((-1 / 2 : ℚ) : ℂ) * d 2
  | _ => 0

@[simp] private def cMatrix_row_6 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 2 => ((1 / 2 : ℚ) : ℂ) * d 2
  | 3 => ((1 / 2 : ℚ) : ℂ) * d 3
  | 7 => ((-1 / 2 : ℚ) : ℂ) * d 0
  | 9 => ((-1 / 2 : ℚ) : ℂ) * d 0
  | _ => 0

@[simp] private def cMatrix_row_7 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 1 => ((-1 / 2 : ℚ) : ℂ) * d 2
  | 5 => ((1 / 2 : ℚ) : ℂ) * d 0
  | _ => 0

@[simp] private def cMatrix_row_8 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 1 => ((-1 / 2 : ℚ) : ℂ) * d 3
  | 6 => ((1 / 2 : ℚ) : ℂ) * d 0
  | _ => 0

@[simp] private def cMatrix_row_9 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 0 => ((-1 / 2 : ℚ) : ℂ) * d 2
  | 2 => ((1 / 2 : ℚ) : ℂ) * d 0
  | 8 => ((-1 / 2 : ℚ) : ℂ) * d 3
  | 9 => ((1 / 2 : ℚ) : ℂ) * d 2
  | _ => 0

@[simp] private def cMatrix_row_10 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 0 => ((-1 / 2 : ℚ) : ℂ) * d 3
  | 3 => ((1 / 2 : ℚ) : ℂ) * d 0
  | 7 => ((1 / 2 : ℚ) : ℂ) * d 3
  | 8 => ((-1 / 2 : ℚ) : ℂ) * d 2
  | _ => 0

@[simp] private def cMatrix_row_11 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 5 => ((-1 / 2 : ℚ) : ℂ) * d 3
  | 6 => ((1 / 2 : ℚ) : ℂ) * d 2
  | _ => 0

@[simp] private def cMatrix_row_12 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 2 => ((-1 / 2 : ℚ) : ℂ) * d 1
  | 5 => ((1 / 2 : ℚ) : ℂ) * d 0
  | _ => 0

@[simp] private def cMatrix_row_13 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 1 => ((1 / 2 : ℚ) : ℂ) * d 1
  | 3 => ((1 / 2 : ℚ) : ℂ) * d 3
  | 4 => ((-1 / 2 : ℚ) : ℂ) * d 0
  | 9 => ((-1 / 2 : ℚ) : ℂ) * d 0
  | _ => 0

@[simp] private def cMatrix_row_14 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 2 => ((-1 / 2 : ℚ) : ℂ) * d 3
  | 8 => ((1 / 2 : ℚ) : ℂ) * d 0
  | _ => 0

@[simp] private def cMatrix_row_15 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 0 => ((1 / 2 : ℚ) : ℂ) * d 1
  | 1 => ((-1 / 2 : ℚ) : ℂ) * d 0
  | 6 => ((1 / 2 : ℚ) : ℂ) * d 3
  | 9 => ((-1 / 2 : ℚ) : ℂ) * d 1
  | _ => 0

@[simp] private def cMatrix_row_16 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 5 => ((-1 / 2 : ℚ) : ℂ) * d 3
  | 8 => ((1 / 2 : ℚ) : ℂ) * d 1
  | _ => 0

@[simp] private def cMatrix_row_17 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 0 => ((-1 / 2 : ℚ) : ℂ) * d 3
  | 3 => ((1 / 2 : ℚ) : ℂ) * d 0
  | 4 => ((1 / 2 : ℚ) : ℂ) * d 3
  | 6 => ((-1 / 2 : ℚ) : ℂ) * d 1
  | _ => 0

@[simp] private def cMatrix_row_18 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 3 => ((-1 / 2 : ℚ) : ℂ) * d 1
  | 6 => ((1 / 2 : ℚ) : ℂ) * d 0
  | _ => 0

@[simp] private def cMatrix_row_19 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 3 => ((-1 / 2 : ℚ) : ℂ) * d 2
  | 8 => ((1 / 2 : ℚ) : ℂ) * d 0
  | _ => 0

@[simp] private def cMatrix_row_20 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 1 => ((1 / 2 : ℚ) : ℂ) * d 1
  | 2 => ((1 / 2 : ℚ) : ℂ) * d 2
  | 4 => ((-1 / 2 : ℚ) : ℂ) * d 0
  | 7 => ((-1 / 2 : ℚ) : ℂ) * d 0
  | _ => 0

@[simp] private def cMatrix_row_21 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 6 => ((-1 / 2 : ℚ) : ℂ) * d 2
  | 8 => ((1 / 2 : ℚ) : ℂ) * d 1
  | _ => 0

@[simp] private def cMatrix_row_22 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 0 => ((1 / 2 : ℚ) : ℂ) * d 1
  | 1 => ((-1 / 2 : ℚ) : ℂ) * d 0
  | 5 => ((1 / 2 : ℚ) : ℂ) * d 2
  | 7 => ((-1 / 2 : ℚ) : ℂ) * d 1
  | _ => 0

@[simp] private def cMatrix_row_23 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 0 => ((1 / 2 : ℚ) : ℂ) * d 2
  | 2 => ((-1 / 2 : ℚ) : ℂ) * d 0
  | 4 => ((-1 / 2 : ℚ) : ℂ) * d 2
  | 5 => ((1 / 2 : ℚ) : ℂ) * d 1
  | _ => 0

def cMatrix (d : Fin 4 → ℂ) : Matrix (Fin 24) (Fin 10) ℂ := fun i j =>
  match i.val with
  | 0 => cMatrix_row_0 d j
  | 1 => cMatrix_row_1 d j
  | 2 => cMatrix_row_2 d j
  | 3 => cMatrix_row_3 d j
  | 4 => cMatrix_row_4 d j
  | 5 => cMatrix_row_5 d j
  | 6 => cMatrix_row_6 d j
  | 7 => cMatrix_row_7 d j
  | 8 => cMatrix_row_8 d j
  | 9 => cMatrix_row_9 d j
  | 10 => cMatrix_row_10 d j
  | 11 => cMatrix_row_11 d j
  | 12 => cMatrix_row_12 d j
  | 13 => cMatrix_row_13 d j
  | 14 => cMatrix_row_14 d j
  | 15 => cMatrix_row_15 d j
  | 16 => cMatrix_row_16 d j
  | 17 => cMatrix_row_17 d j
  | 18 => cMatrix_row_18 d j
  | 19 => cMatrix_row_19 d j
  | 20 => cMatrix_row_20 d j
  | 21 => cMatrix_row_21 d j
  | 22 => cMatrix_row_22 d j
  | 23 => cMatrix_row_23 d j
  | _ => 0


private theorem cMatrix_eq_cMatrixFromCoeff_row_0
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (0 : Fin 24) j = cMatrixFromCoeff d (0 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_1
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (1 : Fin 24) j = cMatrixFromCoeff d (1 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_2
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (2 : Fin 24) j = cMatrixFromCoeff d (2 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_3
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (3 : Fin 24) j = cMatrixFromCoeff d (3 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_4
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (4 : Fin 24) j = cMatrixFromCoeff d (4 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_5
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (5 : Fin 24) j = cMatrixFromCoeff d (5 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_6
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (6 : Fin 24) j = cMatrixFromCoeff d (6 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_7
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (7 : Fin 24) j = cMatrixFromCoeff d (7 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_8
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (8 : Fin 24) j = cMatrixFromCoeff d (8 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_9
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (9 : Fin 24) j = cMatrixFromCoeff d (9 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_10
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (10 : Fin 24) j = cMatrixFromCoeff d (10 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_11
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (11 : Fin 24) j = cMatrixFromCoeff d (11 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_12
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (12 : Fin 24) j = cMatrixFromCoeff d (12 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_13
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (13 : Fin 24) j = cMatrixFromCoeff d (13 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_14
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (14 : Fin 24) j = cMatrixFromCoeff d (14 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_15
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (15 : Fin 24) j = cMatrixFromCoeff d (15 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_16
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (16 : Fin 24) j = cMatrixFromCoeff d (16 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_17
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (17 : Fin 24) j = cMatrixFromCoeff d (17 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_18
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (18 : Fin 24) j = cMatrixFromCoeff d (18 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_19
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (19 : Fin 24) j = cMatrixFromCoeff d (19 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_20
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (20 : Fin 24) j = cMatrixFromCoeff d (20 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_21
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (21 : Fin 24) j = cMatrixFromCoeff d (21 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_22
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (22 : Fin 24) j = cMatrixFromCoeff d (22 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

private theorem cMatrix_eq_cMatrixFromCoeff_row_23
    (d : Fin 4 → ℂ) (j : Fin 10) :
    cMatrix d (23 : Fin 24) j = cMatrixFromCoeff d (23 : Fin 24) j := by
  fin_cases j <;>
    simp [cMatrix, cMatrixFromCoeff, cCoeff, Fin.sum_univ_succ]

theorem cMatrix_eq_cMatrixFromCoeff (d : Fin 4 → ℂ) :
    cMatrix d = cMatrixFromCoeff d := by
  ext i j
  fin_cases i
  · exact cMatrix_eq_cMatrixFromCoeff_row_0 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_1 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_2 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_3 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_4 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_5 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_6 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_7 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_8 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_9 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_10 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_11 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_12 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_13 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_14 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_15 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_16 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_17 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_18 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_19 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_20 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_21 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_22 d j
  · exact cMatrix_eq_cMatrixFromCoeff_row_23 d j

def q0 (d : Fin 4 → ℂ) (j : Fin 10) : ℂ :=
  match j.val with
  | 0 => d 0 * d 0
  | 1 => d 0 * d 1
  | 2 => d 0 * d 2
  | 3 => d 0 * d 3
  | 4 => d 1 * d 1
  | 5 => d 1 * d 2
  | 6 => d 1 * d 3
  | 7 => d 2 * d 2
  | 8 => d 2 * d 3
  | 9 => d 3 * d 3
  | _ => 0


private theorem cMatrix_q0_zero_row_0 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (0 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_1 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (1 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_2 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (2 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_3 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (3 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_4 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (4 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_5 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (5 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_6 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (6 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_7 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (7 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_8 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (8 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_9 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (9 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_10 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (10 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_11 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (11 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_12 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (12 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_13 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (13 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_14 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (14 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_15 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (15 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_16 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (16 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_17 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (17 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_18 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (18 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_19 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (19 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_20 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (20 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_21 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (21 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_22 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (22 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

private theorem cMatrix_q0_zero_row_23 (d : Fin 4 → ℂ) :
    ((cMatrix d).mulVec (q0 d)) (23 : Fin 24) = 0 := by
  simp [cMatrix, q0, Matrix.mulVec, dotProduct,
    Fin.sum_univ_succ] <;> ring

theorem cMatrix_q0_zero (d : Fin 4 → ℂ) :
    (cMatrix d).mulVec (q0 d) = 0 := by
  funext i
  fin_cases i
  · exact cMatrix_q0_zero_row_0 d
  · exact cMatrix_q0_zero_row_1 d
  · exact cMatrix_q0_zero_row_2 d
  · exact cMatrix_q0_zero_row_3 d
  · exact cMatrix_q0_zero_row_4 d
  · exact cMatrix_q0_zero_row_5 d
  · exact cMatrix_q0_zero_row_6 d
  · exact cMatrix_q0_zero_row_7 d
  · exact cMatrix_q0_zero_row_8 d
  · exact cMatrix_q0_zero_row_9 d
  · exact cMatrix_q0_zero_row_10 d
  · exact cMatrix_q0_zero_row_11 d
  · exact cMatrix_q0_zero_row_12 d
  · exact cMatrix_q0_zero_row_13 d
  · exact cMatrix_q0_zero_row_14 d
  · exact cMatrix_q0_zero_row_15 d
  · exact cMatrix_q0_zero_row_16 d
  · exact cMatrix_q0_zero_row_17 d
  · exact cMatrix_q0_zero_row_18 d
  · exact cMatrix_q0_zero_row_19 d
  · exact cMatrix_q0_zero_row_20 d
  · exact cMatrix_q0_zero_row_21 d
  · exact cMatrix_q0_zero_row_22 d
  · exact cMatrix_q0_zero_row_23 d

theorem cMatrix_zero : cMatrix (0 : Fin 4 → ℂ) = 0 := by
  ext i j
  simp [cMatrix]

theorem q0_zero : q0 (0 : Fin 4 → ℂ) = 0 := by
  funext j
  fin_cases j <;> simp [q0]

theorem q0_ne_zero {d : Fin 4 → ℂ} (hd : d ≠ 0) : q0 d ≠ 0 := by
  intro hq
  apply hd
  funext r
  fin_cases r
  · have h := congrFun hq (0 : Fin 10)
    simp [q0] at h
    exact h
  · have h := congrFun hq (4 : Fin 10)
    simp [q0] at h
    exact h
  · have h := congrFun hq (7 : Fin 10)
    simp [q0] at h
    exact h
  · have h := congrFun hq (9 : Fin 10)
    simp [q0] at h
    exact h

def rows_0_0 (i : Fin 9) : Fin 24 :=
  match i.val with
  | 0 => 6
  | 1 => 7
  | 2 => 8
  | 3 => 9
  | 4 => 10
  | 5 => 13
  | 6 => 14
  | 7 => 15
  | 8 => 20
  | _ => 0

def cols_0_0 (i : Fin 9) : Fin 10 :=
  match i.val with
  | 0 => 1
  | 1 => 2
  | 2 => 3
  | 3 => 4
  | 4 => 5
  | 5 => 6
  | 6 => 7
  | 7 => 8
  | 8 => 9
  | _ => 0

def minor_0_0 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  (cMatrix d).submatrix rows_0_0 cols_0_0
def detPoly_0_0 (d : Fin 4 → ℂ) : ℂ := (-d 0^5*(d 0 - d 3)^2*(d 0 + d 3)^2/256 : ℂ)
private def adj_0_0_row_0 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0^3*d1*(d0 - d3)^2*(d0 + d3)^2/256 : ℂ)
  | 2 => (-d0^5*d3*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 4 => (d0^4*d1*d3*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 5 => (-d0^3*d1*(d0 - d3)*(d0 + d3)*(d0^2 + d3^2)/256 : ℂ)
  | 6 => (d0^3*d1*d2*d3*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 7 => (d0^6*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 8 => (d0^3*d1*(d0 - d3)*(d0 + d3)*(d0^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_0_0_row_1 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0^3*d2*(d0 - d3)^2*(d0 + d3)^2/256 : ℂ)
  | 3 => (-d0^6*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 4 => (d0^4*d2*d3*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 5 => (-d0^3*d2*(d0 - d3)*(d0 + d3)*(d0^2 + d3^2)/256 : ℂ)
  | 6 => (-d0^3*d3*(d0 - d2)*(d0 + d2)*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 8 => (d0^3*d2*(d0 - d3)*(d0 + d3)*(d0^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_0_0_row_2 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0^3*d3*(d0 - d3)^2*(d0 + d3)^2/256 : ℂ)
  | 4 => (-d0^4*(d0 - d3)^2*(d0 + d3)^2/128 : ℂ)
  | 5 => (d0^3*d3*(d0 - d3)^2*(d0 + d3)^2/256 : ℂ)
  | 6 => (-d0^3*d2*(d0 - d3)^2*(d0 + d3)^2/128 : ℂ)
  | 8 => (-d0^3*d3*(d0 - d3)^2*(d0 + d3)^2/256 : ℂ)
  | _ => 0

private def adj_0_0_row_3 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0^2*(d0 - d3)^2*(d0 + d3)^2*(d0^2 + d1^2)/256 : ℂ)
  | 2 => (-d0^4*d1*d3*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 4 => (d0^3*d1^2*d3*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 5 => (d0^2*(d0 - d3)*(d0 + d3)*(d0^4 - d0^2*d1^2 - d0^2*d3^2 - d1^2*d3^2)/256 : ℂ)
  | 6 => (d0^2*d1^2*d2*d3*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 7 => (d0^5*d1*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 8 => (d0^2*(d0 - d3)*(d0 + d3)*(d0^4 + d0^2*d1^2 - d0^2*d3^2 + d1^2*d3^2)/256 : ℂ)
  | _ => 0

private def adj_0_0_row_4 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0^2*d1*d2*(d0 - d3)^2*(d0 + d3)^2/256 : ℂ)
  | 1 => (-d0^4*(d0 - d3)^2*(d0 + d3)^2/128 : ℂ)
  | 2 => (-d0^4*d2*d3*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 4 => (d0^3*d1*d2*d3*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 5 => (-d0^2*d1*d2*(d0 - d3)*(d0 + d3)*(d0^2 + d3^2)/256 : ℂ)
  | 6 => (d0^2*d1*d2^2*d3*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 7 => (d0^5*d2*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 8 => (d0^2*d1*d2*(d0 - d3)*(d0 + d3)*(d0^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_0_0_row_5 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0^2*d1*d3*(d0 - d3)^2*(d0 + d3)^2/256 : ℂ)
  | 2 => (-d0^6*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 4 => (d0^3*d1*d3^2*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 5 => (-d0^2*d1*d3*(d0 - d3)*(d0 + d3)*(d0^2 + d3^2)/256 : ℂ)
  | 6 => (d0^2*d1*d2*d3^2*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 7 => (d0^5*d3*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 8 => (d0^2*d1*d3*(d0 - d3)*(d0 + d3)*(d0^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_0_0_row_6 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d0^2*(d0 - d2)*(d0 + d2)*(d0 - d3)^2*(d0 + d3)^2/256 : ℂ)
  | 3 => (-d0^5*d2*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 4 => (d0^3*d2^2*d3*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 5 => (-d0^2*(d0 - d3)*(d0 + d3)*(d0^4 + d0^2*d2^2 - d0^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 6 => (-d0^2*d2*d3*(d0 - d2)*(d0 + d2)*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 8 => (d0^2*(d0 - d3)*(d0 + d3)*(d0^4 + d0^2*d2^2 - d0^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | _ => 0

private def adj_0_0_row_7 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0^2*d2*d3*(d0 - d3)^2*(d0 + d3)^2/256 : ℂ)
  | 3 => (-d0^5*d3*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 4 => (d0^3*d2*d3^2*(d0 - d3)*(d0 + d3)/128 : ℂ)
  | 5 => (-d0^2*d2*d3*(d0 - d3)*(d0 + d3)*(d0^2 + d3^2)/256 : ℂ)
  | 6 => (-d0^2*(d0 - d3)*(d0 + d3)*(d0^2 - d2*d3)*(d0^2 + d2*d3)/128 : ℂ)
  | 8 => (d0^2*d2*d3*(d0 - d3)*(d0 + d3)*(d0^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_0_0_row_8 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d0^2*(d0 - d3)^3*(d0 + d3)^3/256 : ℂ)
  | 4 => (-d0^3*d3*(d0 - d3)^2*(d0 + d3)^2/128 : ℂ)
  | 5 => (d0^2*(d0 - d3)^2*(d0 + d3)^2*(d0^2 + d3^2)/256 : ℂ)
  | 6 => (-d0^2*d2*d3*(d0 - d3)^2*(d0 + d3)^2/128 : ℂ)
  | 8 => (-d0^2*(d0 - d3)^2*(d0 + d3)^2*(d0^2 + d3^2)/256 : ℂ)
  | _ => 0

def adj_0_0 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  let d0 := d 0
  let d1 := d 1
  let d2 := d 2
  let d3 := d 3
  fun i j =>
    match i.val with
    | 0 => adj_0_0_row_0 d0 d1 d2 d3 j
    | 1 => adj_0_0_row_1 d0 d1 d2 d3 j
    | 2 => adj_0_0_row_2 d0 d1 d2 d3 j
    | 3 => adj_0_0_row_3 d0 d1 d2 d3 j
    | 4 => adj_0_0_row_4 d0 d1 d2 d3 j
    | 5 => adj_0_0_row_5 d0 d1 d2 d3 j
    | 6 => adj_0_0_row_6 d0 d1 d2 d3 j
    | 7 => adj_0_0_row_7 d0 d1 d2 d3 j
    | 8 => adj_0_0_row_8 d0 d1 d2 d3 j
    | _ => 0
def rows_0_1 (i : Fin 9) : Fin 24 :=
  match i.val with
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 4
  | 4 => 5
  | 5 => 6
  | 6 => 7
  | 7 => 10
  | 8 => 13
  | _ => 0

def cols_0_1 (i : Fin 9) : Fin 10 :=
  match i.val with
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 4
  | 5 => 5
  | 6 => 6
  | 7 => 7
  | 8 => 8
  | _ => 0

def minor_0_1 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  (cMatrix d).submatrix rows_0_1 cols_0_1
def detPoly_0_1 (d : Fin 4 → ℂ) : ℂ := (d 0^2*d 3^7/256 : ℂ)
private def adj_0_1_row_0 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0^2*d1*d3^3*(d0^2 + d3^2)/256 : ℂ)
  | 1 => (-d0^2*d2*d3^3*(d0 - d3)*(d0 + d3)/256 : ℂ)
  | 2 => (d0^2*d3^4*(d0^2 + d3^2)/256 : ℂ)
  | 3 => (-d0*d1*d3^2*(d0^2 + d3^2)*(d2^2 + d3^2)/256 : ℂ)
  | 4 => (d0*d2*d3^2*(d0^2*d1^2 - d0^2*d3^2 + d1^2*d3^2 + d3^4)/256 : ℂ)
  | 5 => (-d0*d3^3*(d0^2*d1^2 - d0^2*d3^2 + d1^2*d3^2 + d3^4)/256 : ℂ)
  | 6 => (-d0^3*d1*d2*d3^3/128 : ℂ)
  | 7 => (-d0^2*d3^6/128 : ℂ)
  | 8 => (-d0*d3^3*(d0^2*d2^2 - d0^2*d3^2 - d2^2*d3^2 - d3^4)/256 : ℂ)
  | _ => 0

private def adj_0_1_row_1 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0^3*d1^2*d3^3/256 : ℂ)
  | 1 => (-d0^3*d1*d2*d3^3/256 : ℂ)
  | 2 => (d0^3*d1*d3^4/256 : ℂ)
  | 3 => (-d0^2*d3^2*(d1^2*d2^2 + d1^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 4 => (d0^2*d1*d2*d3^2*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 5 => (-d0^2*d1*d3^3*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 6 => (-d0^2*d1^2*d2*d3^3/128 : ℂ)
  | 8 => (-d0^2*d1*d3^3*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | _ => 0

private def adj_0_1_row_2 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0^3*d1*d2*d3^3/256 : ℂ)
  | 1 => (-d0^3*d2^2*d3^3/256 : ℂ)
  | 2 => (d0^3*d2*d3^4/256 : ℂ)
  | 3 => (-d0^2*d1*d2*d3^2*(d2^2 + d3^2)/256 : ℂ)
  | 4 => (d0^2*d3^2*(d1^2*d2^2 - d2^2*d3^2 + 2*d3^4)/256 : ℂ)
  | 5 => (-d0^2*d2*d3^3*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 6 => (-d0^2*d1*d2^2*d3^3/128 : ℂ)
  | 8 => (-d0^2*d2*d3^3*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | _ => 0

private def adj_0_1_row_3 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0^3*d1*d3^4/256 : ℂ)
  | 1 => (-d0^3*d2*d3^4/256 : ℂ)
  | 2 => (d0^3*d3^5/256 : ℂ)
  | 3 => (-d0^2*d1*d3^3*(d2^2 + d3^2)/256 : ℂ)
  | 4 => (d0^2*d2*d3^3*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 5 => (-d0^2*d3^4*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 6 => (-d0^2*d1*d2*d3^4/128 : ℂ)
  | 8 => (-d0^2*d3^4*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | _ => 0

private def adj_0_1_row_4 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0^2*d1*d3^3*(d1^2 + d3^2)/256 : ℂ)
  | 1 => (-d0^2*d2*d3^3*(d1^2 + d3^2)/256 : ℂ)
  | 2 => (d0^2*d3^4*(d1^2 + d3^2)/256 : ℂ)
  | 3 => (-d0*d1*d3^2*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 4 => (d0*d2*d3^2*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 5 => (-d0*d3^3*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 6 => (-d0*d1*d2*d3^3*(d1^2 + d3^2)/128 : ℂ)
  | 8 => (-d0*d3^3*(d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2 + d3^4)/256 : ℂ)
  | _ => 0

private def adj_0_1_row_5 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0^2*d1^2*d2*d3^3/256 : ℂ)
  | 1 => (-d0^2*d1*d2^2*d3^3/256 : ℂ)
  | 2 => (d0^2*d1*d2*d3^4/256 : ℂ)
  | 3 => (-d0*d2*d3^2*(d1^2*d2^2 + d1^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 4 => (d0*d1*d2^2*d3^2*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 5 => (-d0*d1*d2*d3^3*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 6 => (-d0*d3^3*(d1*d2 - d3^2)*(d1*d2 + d3^2)/128 : ℂ)
  | 8 => (-d0*d1*d2*d3^3*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | _ => 0

private def adj_0_1_row_6 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0^2*d3^4*(d1^2 + 2*d3^2)/256 : ℂ)
  | 1 => (-d0^2*d1*d2*d3^4/256 : ℂ)
  | 2 => (d0^2*d1*d3^5/256 : ℂ)
  | 3 => (-d0*d3^3*(d1^2*d2^2 + d1^2*d3^2 + 2*d2^2*d3^2)/256 : ℂ)
  | 4 => (d0*d1*d2*d3^3*(d1^2 + d3^2)/256 : ℂ)
  | 5 => (-d0*d1*d3^4*(d1^2 + d3^2)/256 : ℂ)
  | 6 => (-d0*d2*d3^4*(d1^2 + d3^2)/128 : ℂ)
  | 8 => (-d0*d1*d3^4*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | _ => 0

private def adj_0_1_row_7 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0^2*d1*d3^3*(d2^2 + d3^2)/256 : ℂ)
  | 1 => (-d0^2*d2*d3^3*(d2^2 + d3^2)/256 : ℂ)
  | 2 => (d0^2*d3^4*(d2^2 + d3^2)/256 : ℂ)
  | 3 => (-d0*d1*d3^2*(d2^2 + d3^2)^2/256 : ℂ)
  | 4 => (d0*d2*d3^2*(d1^2*d2^2 + d1^2*d3^2 - d2^2*d3^2 + d3^4)/256 : ℂ)
  | 5 => (-d0*d3^3*(d1^2*d2^2 + d1^2*d3^2 - d2^2*d3^2 + d3^4)/256 : ℂ)
  | 6 => (-d0*d1*d2*d3^3*(d2^2 + d3^2)/128 : ℂ)
  | 8 => (-d0*d3^3*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_0_1_row_8 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0^2*d1*d2*d3^4/256 : ℂ)
  | 1 => (-d0^2*d3^4*(d2^2 + 2*d3^2)/256 : ℂ)
  | 2 => (d0^2*d2*d3^5/256 : ℂ)
  | 3 => (-d0*d1*d2*d3^3*(d2^2 + d3^2)/256 : ℂ)
  | 4 => (d0*d2^2*d3^3*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 5 => (-d0*d2*d3^4*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 6 => (-d0*d1*d3^4*(d2^2 + d3^2)/128 : ℂ)
  | 8 => (-d0*d2*d3^4*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

def adj_0_1 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  let d0 := d 0
  let d1 := d 1
  let d2 := d 2
  let d3 := d 3
  fun i j =>
    match i.val with
    | 0 => adj_0_1_row_0 d0 d1 d2 d3 j
    | 1 => adj_0_1_row_1 d0 d1 d2 d3 j
    | 2 => adj_0_1_row_2 d0 d1 d2 d3 j
    | 3 => adj_0_1_row_3 d0 d1 d2 d3 j
    | 4 => adj_0_1_row_4 d0 d1 d2 d3 j
    | 5 => adj_0_1_row_5 d0 d1 d2 d3 j
    | 6 => adj_0_1_row_6 d0 d1 d2 d3 j
    | 7 => adj_0_1_row_7 d0 d1 d2 d3 j
    | 8 => adj_0_1_row_8 d0 d1 d2 d3 j
    | _ => 0
def rows_1_0 (i : Fin 9) : Fin 24 :=
  match i.val with
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 4
  | 5 => 13
  | 6 => 15
  | 7 => 16
  | 8 => 22
  | _ => 0

def cols_1_0 (i : Fin 9) : Fin 10 :=
  match i.val with
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 5
  | 5 => 6
  | 6 => 7
  | 7 => 8
  | 8 => 9
  | _ => 0

def minor_1_0 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  (cMatrix d).submatrix rows_1_0 cols_1_0
def detPoly_1_0 (d : Fin 4 → ℂ) : ℂ := (-d 1^5*(d 1^2 + d 3^2)^2/256 : ℂ)
private def adj_1_0_row_0 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d1^2*(d0^2 + d1^2)*(d1^2 + d3^2)^2/256 : ℂ)
  | 2 => (d0^2*d1^3*d3*(d1^2 + d3^2)/128 : ℂ)
  | 4 => (-d0*d1^4*d3*(d1^2 + d3^2)/128 : ℂ)
  | 5 => (-d0*d1^5*(d1^2 + d3^2)/128 : ℂ)
  | 6 => (d1^2*(d1^2 + d3^2)*(d0^2*d1^2 - d0^2*d3^2 - d1^4 - d1^2*d3^2)/256 : ℂ)
  | 7 => (d0^2*d1^2*d2*d3*(d1^2 + d3^2)/128 : ℂ)
  | 8 => (-d1^2*(d1^2 + d3^2)*(d0^2*d1^2 - d0^2*d3^2 + d1^4 + d1^2*d3^2)/256 : ℂ)
  | _ => 0

private def adj_1_0_row_1 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0*d1^3*(d1^2 + d3^2)^2/256 : ℂ)
  | 2 => (d0*d1^4*d3*(d1^2 + d3^2)/128 : ℂ)
  | 4 => (-d1^5*d3*(d1^2 + d3^2)/128 : ℂ)
  | 5 => (-d1^6*(d1^2 + d3^2)/128 : ℂ)
  | 6 => (d0*d1^3*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 7 => (d0*d1^3*d2*d3*(d1^2 + d3^2)/128 : ℂ)
  | 8 => (-d0*d1^3*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_1_0_row_2 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0*d1^2*d2*(d1^2 + d3^2)^2/256 : ℂ)
  | 2 => (d0*d1^3*d2*d3*(d1^2 + d3^2)/128 : ℂ)
  | 3 => (d1^4*(d1^2 + d3^2)^2/128 : ℂ)
  | 4 => (-d1^4*d2*d3*(d1^2 + d3^2)/128 : ℂ)
  | 5 => (-d1^5*d2*(d1^2 + d3^2)/128 : ℂ)
  | 6 => (d0*d1^2*d2*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 7 => (d0*d1^2*d2^2*d3*(d1^2 + d3^2)/128 : ℂ)
  | 8 => (-d0*d1^2*d2*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_1_0_row_3 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0*d1^2*d3*(d1^2 + d3^2)^2/256 : ℂ)
  | 2 => (d0*d1^3*d3^2*(d1^2 + d3^2)/128 : ℂ)
  | 4 => (d1^6*(d1^2 + d3^2)/128 : ℂ)
  | 5 => (-d1^5*d3*(d1^2 + d3^2)/128 : ℂ)
  | 6 => (d0*d1^2*d3*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 7 => (d0*d1^2*d2*d3^2*(d1^2 + d3^2)/128 : ℂ)
  | 8 => (-d0*d1^2*d3*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_1_0_row_4 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d1^3*d2*(d1^2 + d3^2)^2/256 : ℂ)
  | 1 => (d1^6*(d1^2 + d3^2)/128 : ℂ)
  | 2 => (d1^4*d2*d3*(d1^2 + d3^2)/128 : ℂ)
  | 6 => (d1^3*d2*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 7 => (d1^3*d3*(d1^2 + d2^2)*(d1^2 + d3^2)/128 : ℂ)
  | 8 => (-d1^3*d2*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_1_0_row_5 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d1^3*d3*(d1^2 + d3^2)^2/256 : ℂ)
  | 2 => (d1^4*(d1^2 + d3^2)^2/128 : ℂ)
  | 6 => (-d1^3*d3*(d1^2 + d3^2)^2/256 : ℂ)
  | 7 => (d1^3*d2*(d1^2 + d3^2)^2/128 : ℂ)
  | 8 => (d1^3*d3*(d1^2 + d3^2)^2/256 : ℂ)
  | _ => 0

private def adj_1_0_row_6 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d1^2*(d1^2 + d2^2)*(d1^2 + d3^2)^2/256 : ℂ)
  | 1 => (d1^5*d2*(d1^2 + d3^2)/128 : ℂ)
  | 2 => (d1^3*d2^2*d3*(d1^2 + d3^2)/128 : ℂ)
  | 6 => (-d1^2*(d1^2 + d3^2)*(d1^4 - d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 7 => (d1^2*d2*d3*(d1^2 + d2^2)*(d1^2 + d3^2)/128 : ℂ)
  | 8 => (d1^2*(d1^2 + d3^2)*(d1^4 - d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | _ => 0

private def adj_1_0_row_7 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d1^2*d2*d3*(d1^2 + d3^2)^2/256 : ℂ)
  | 1 => (d1^5*d3*(d1^2 + d3^2)/128 : ℂ)
  | 2 => (d1^3*d2*d3^2*(d1^2 + d3^2)/128 : ℂ)
  | 6 => (d1^2*d2*d3*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 7 => (-d1^2*(d1^2 + d3^2)*(d1^2 - d2*d3)*(d1^2 + d2*d3)/128 : ℂ)
  | 8 => (-d1^2*d2*d3*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_1_0_row_8 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d1^2*(d1^2 + d3^2)^3/256 : ℂ)
  | 2 => (d1^3*d3*(d1^2 + d3^2)^2/128 : ℂ)
  | 6 => (d1^2*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)^2/256 : ℂ)
  | 7 => (d1^2*d2*d3*(d1^2 + d3^2)^2/128 : ℂ)
  | 8 => (-d1^2*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)^2/256 : ℂ)
  | _ => 0

def adj_1_0 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  let d0 := d 0
  let d1 := d 1
  let d2 := d 2
  let d3 := d 3
  fun i j =>
    match i.val with
    | 0 => adj_1_0_row_0 d0 d1 d2 d3 j
    | 1 => adj_1_0_row_1 d0 d1 d2 d3 j
    | 2 => adj_1_0_row_2 d0 d1 d2 d3 j
    | 3 => adj_1_0_row_3 d0 d1 d2 d3 j
    | 4 => adj_1_0_row_4 d0 d1 d2 d3 j
    | 5 => adj_1_0_row_5 d0 d1 d2 d3 j
    | 6 => adj_1_0_row_6 d0 d1 d2 d3 j
    | 7 => adj_1_0_row_7 d0 d1 d2 d3 j
    | 8 => adj_1_0_row_8 d0 d1 d2 d3 j
    | _ => 0
def rows_1_1 (i : Fin 9) : Fin 24 :=
  match i.val with
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 4
  | 5 => 6
  | 6 => 9
  | 7 => 10
  | 8 => 15
  | _ => 0

def cols_1_1 (i : Fin 9) : Fin 10 :=
  match i.val with
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 4
  | 5 => 5
  | 6 => 6
  | 7 => 7
  | 8 => 8
  | _ => 0

def minor_1_1 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  (cMatrix d).submatrix rows_1_1 cols_1_1
def detPoly_1_1 (d : Fin 4 → ℂ) : ℂ := (d 1^3*d 3^4*(d 2^2 + d 3^2)/256 : ℂ)
private def adj_1_1_row_0 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d1^2*d3^2*(d0^2*d2^2 - d0^2*d3^2 - d2^2*d3^2 - d3^4)/256 : ℂ)
  | 1 => (d1*d2*d3^2*(d0^2*d2^2 - d0^2*d3^2 - d2^2*d3^2 - d3^4)/256 : ℂ)
  | 2 => (-d1*d2^2*d3*(d0^2*d2^2 - d0^2*d3^2 - d2^2*d3^2 - d3^4)/256 : ℂ)
  | 3 => (-d0*d2*(d0^2*d1^2*d2^2 + d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 - d0^2*d3^4 - d1^2*d2^2*d3^2 - 3*d1^2*d3^4 - d2^2*d3^4 - d3^6)/256 : ℂ)
  | 4 => (d0*d3*(d0^2*d1^2*d2^2 + d0^2*d1^2*d3^2 + d0^2*d2^4 - d0^2*d2^2*d3^2 - d1^2*d2^2*d3^2 + d1^2*d3^4 - d2^4*d3^2 - d2^2*d3^4)/256 : ℂ)
  | 5 => (d0*d1^3*d3^4/128 : ℂ)
  | 6 => (-d1*d2*(d0^2*d1^2*d2^2 + d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 - d0^2*d3^4 - d1^2*d2^2*d3^2 - d1^2*d3^4 - d2^2*d3^4 - d3^6)/256 : ℂ)
  | 7 => (d1*d3*(d0^2*d1^2*d2^2 + d0^2*d1^2*d3^2 + d0^2*d2^4 - d0^2*d2^2*d3^2 - d1^2*d2^2*d3^2 - d1^2*d3^4 - d2^4*d3^2 - d2^2*d3^4)/256 : ℂ)
  | 8 => (-d1^2*(d2^2 + d3^2)*(d0^2*d2^2 - d0^2*d3^2 - d2^2*d3^2 - d3^4)/256 : ℂ)
  | _ => 0

private def adj_1_1_row_1 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0*d1^3*d3^2*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | 1 => (d0*d1^2*d2*d3^2*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | 2 => (-d0*d1^2*d2^2*d3*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | 3 => (-d1*d2*(d0^2*d1^2*d2^2 + d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 - d0^2*d3^4 - 2*d1^2*d3^4)/256 : ℂ)
  | 4 => (d1*d3*(d0^2*d1^2*d2^2 + d0^2*d1^2*d3^2 + d0^2*d2^4 - d0^2*d2^2*d3^2 + 2*d1^2*d3^4)/256 : ℂ)
  | 5 => (d1^4*d3^4/128 : ℂ)
  | 6 => (-d0*d1^2*d2*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 7 => (d0*d1^2*d3*(d1^2*d2^2 + d1^2*d3^2 + d2^4 - d2^2*d3^2)/256 : ℂ)
  | 8 => (-d0*d1^3*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_1_1_row_2 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0*d1^2*d2*d3^2*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | 1 => (d0*d1*d2^2*d3^2*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | 2 => (-d0*d1*d2^3*d3*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | 3 => (-(d0^2*d1^2*d2^4 + d0^2*d1^2*d2^2*d3^2 + d0^2*d2^4*d3^2 - d0^2*d2^2*d3^4 + 2*d1^2*d3^6)/256 : ℂ)
  | 4 => (d2*d3*(d0^2*d1^2*d2^2 + d0^2*d1^2*d3^2 + d0^2*d2^4 - d0^2*d2^2*d3^2 + 2*d1^2*d3^4)/256 : ℂ)
  | 5 => (d1^3*d2*d3^4/128 : ℂ)
  | 6 => (-d0*d1*d2^2*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 7 => (d0*d1*d2*d3*(d1^2*d2^2 + d1^2*d3^2 + d2^4 - d2^2*d3^2)/256 : ℂ)
  | 8 => (-d0*d1^2*d2*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_1_1_row_3 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d0*d1^2*d3^3*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | 1 => (d0*d1*d2*d3^3*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | 2 => (-d0*d1*d2^2*d3^2*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | 3 => (-d2*d3*(d0^2*d1^2*d2^2 + d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 - d0^2*d3^4 - 2*d1^2*d3^4)/256 : ℂ)
  | 4 => (d3^2*(d0^2*d1^2*d2^2 + d0^2*d1^2*d3^2 + d0^2*d2^4 - d0^2*d2^2*d3^2 - 2*d1^2*d2^2*d3^2)/256 : ℂ)
  | 5 => (d1^3*d3^5/128 : ℂ)
  | 6 => (-d0*d1*d2*d3*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 7 => (d0*d1*d3^2*(d1^2*d2^2 + d1^2*d3^2 + d2^4 - d2^2*d3^2)/256 : ℂ)
  | 8 => (-d0*d1^2*d3*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_1_1_row_4 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d1^2*d3^2*(d1^2 + d3^2)*(d2^2 + d3^2)/256 : ℂ)
  | 1 => (d1*d2*d3^2*(d1^2 + d3^2)*(d2^2 + d3^2)/256 : ℂ)
  | 2 => (-d1*d3*(d2^2 + d3^2)*(d1^2*d2^2 - 2*d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 3 => (-d0*d2*(d1^2 + d3^2)^2*(d2^2 + d3^2)/256 : ℂ)
  | 4 => (d0*d3*(d2^2 + d3^2)*(d1^4 + d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 6 => (-d1*d2*(d1^2 + d3^2)^2*(d2^2 + d3^2)/256 : ℂ)
  | 7 => (d1*d3*(d2^2 + d3^2)*(d1^4 + d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 8 => (-d1^2*(d2^2 + d3^2)*(d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2 + d3^4)/256 : ℂ)
  | _ => 0

private def adj_1_1_row_5 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d1^3*d2*d3^2*(d2^2 + d3^2)/256 : ℂ)
  | 1 => (d1^2*d3^2*(d2^2 - 2*d3^2)*(d2^2 + d3^2)/256 : ℂ)
  | 2 => (-d1^2*d2*d3*(d2^2 - 2*d3^2)*(d2^2 + d3^2)/256 : ℂ)
  | 3 => (-d0*d1*(d2^2 + d3^2)*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 4 => (d0*d1*d2*d3*(d2^2 + d3^2)*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 6 => (-d1^2*(d2^2 + d3^2)*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 7 => (d1^2*d2*d3*(d2^2 + d3^2)*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 8 => (-d1^3*d2*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_1_1_row_6 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d1^3*d3^3*(d2^2 + d3^2)/256 : ℂ)
  | 1 => (d1^2*d2*d3^3*(d2^2 + d3^2)/256 : ℂ)
  | 2 => (-d1^2*d2^2*d3^2*(d2^2 + d3^2)/256 : ℂ)
  | 3 => (-d0*d1*d2*d3*(d1^2 + d3^2)*(d2^2 + d3^2)/256 : ℂ)
  | 4 => (d0*d1*d3^2*(d1^2 + d2^2)*(d2^2 + d3^2)/256 : ℂ)
  | 6 => (-d1^2*d2*d3*(d1^2 + d3^2)*(d2^2 + d3^2)/256 : ℂ)
  | 7 => (d1^2*d3^2*(d1^2 + d2^2)*(d2^2 + d3^2)/256 : ℂ)
  | 8 => (-d1^3*d3*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_1_1_row_7 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d1^2*d3^2*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | 1 => (d1*d2*d3^2*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | 2 => (-d1*d2^2*d3*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | 3 => (-d0*d2*(d2^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 4 => (d0*d3*(d2^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 + d2^4 - d2^2*d3^2)/256 : ℂ)
  | 6 => (-d1*d2*(d2^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 7 => (d1*d3*(d2^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 + d2^4 - d2^2*d3^2)/256 : ℂ)
  | 8 => (-d1^2*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)^2/256 : ℂ)
  | _ => 0

private def adj_1_1_row_8 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d1^2*d2*d3^3*(d2^2 + d3^2)/256 : ℂ)
  | 1 => (d1*d2^2*d3^3*(d2^2 + d3^2)/256 : ℂ)
  | 2 => (-d1*d2^3*d3^2*(d2^2 + d3^2)/256 : ℂ)
  | 3 => (-d0*d3*(d2^2 + d3^2)*(d1^2*d2^2 + 2*d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 4 => (d0*d2*d3^2*(d1^2 + d2^2)*(d2^2 + d3^2)/256 : ℂ)
  | 6 => (-d1*d3*(d2^2 + d3^2)*(d1^2*d2^2 + 2*d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 7 => (d1*d2*d3^2*(d1^2 + d2^2)*(d2^2 + d3^2)/256 : ℂ)
  | 8 => (-d1^2*d2*d3*(d2^2 + d3^2)^2/256 : ℂ)
  | _ => 0

def adj_1_1 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  let d0 := d 0
  let d1 := d 1
  let d2 := d 2
  let d3 := d 3
  fun i j =>
    match i.val with
    | 0 => adj_1_1_row_0 d0 d1 d2 d3 j
    | 1 => adj_1_1_row_1 d0 d1 d2 d3 j
    | 2 => adj_1_1_row_2 d0 d1 d2 d3 j
    | 3 => adj_1_1_row_3 d0 d1 d2 d3 j
    | 4 => adj_1_1_row_4 d0 d1 d2 d3 j
    | 5 => adj_1_1_row_5 d0 d1 d2 d3 j
    | 6 => adj_1_1_row_6 d0 d1 d2 d3 j
    | 7 => adj_1_1_row_7 d0 d1 d2 d3 j
    | 8 => adj_1_1_row_8 d0 d1 d2 d3 j
    | _ => 0
def rows_1_2 (i : Fin 9) : Fin 24 :=
  match i.val with
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 4
  | 5 => 7
  | 6 => 9
  | 7 => 10
  | 8 => 15
  | _ => 0

def cols_1_2 (i : Fin 9) : Fin 10 :=
  match i.val with
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 4
  | 5 => 5
  | 6 => 6
  | 7 => 7
  | 8 => 8
  | _ => 0

def minor_1_2 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  (cMatrix d).submatrix rows_1_2 cols_1_2
def detPoly_1_2 (d : Fin 4 → ℂ) : ℂ := (-d 1^4*d 2*d 3^4/256 : ℂ)
private def adj_1_2_row_0 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1^3*d2*d3^2*(d0 - d3)*(d0 + d3)/256 : ℂ)
  | 1 => (-d1^2*d3^2*(d0^2*d2^2 - 2*d0^2*d3^2 - d2^2*d3^2)/256 : ℂ)
  | 2 => (d1^2*d2*d3*(d0^2*d2^2 - 2*d0^2*d3^2 - d2^2*d3^2)/256 : ℂ)
  | 3 => (d0*d1*(d0^2*d1^2*d2^2 + d0^2*d2^2*d3^2 - 2*d0^2*d3^4 - d1^2*d2^2*d3^2 - d2^2*d3^4)/256 : ℂ)
  | 4 => (-d0*d1*d2*d3*(d0^2*d1^2 + d0^2*d2^2 - 2*d0^2*d3^2 - d1^2*d3^2 - d2^2*d3^2)/256 : ℂ)
  | 5 => (d0*d1^3*d3^4/128 : ℂ)
  | 6 => (d1^2*(d0^2*d1^2*d2^2 + d0^2*d2^2*d3^2 - 2*d0^2*d3^4 - d1^2*d2^2*d3^2 - d2^2*d3^4)/256 : ℂ)
  | 7 => (-d1^2*d2*d3*(d0^2*d1^2 + d0^2*d2^2 - 2*d0^2*d3^2 - d1^2*d3^2 - d2^2*d3^2)/256 : ℂ)
  | 8 => (d1^3*d2*(d0^2*d2^2 - d0^2*d3^2 - d2^2*d3^2 - d3^4)/256 : ℂ)
  | _ => 0

private def adj_1_2_row_1 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d0*d1^4*d2*d3^2/256 : ℂ)
  | 1 => (-d0*d1^3*d3^2*(d2^2 - 2*d3^2)/256 : ℂ)
  | 2 => (d0*d1^3*d2*d3*(d2^2 - 2*d3^2)/256 : ℂ)
  | 3 => (d0^2*d1^2*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 4 => (-d0^2*d1^2*d2*d3*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 5 => (d1^4*d3^4/128 : ℂ)
  | 6 => (d0*d1^3*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 7 => (-d0*d1^3*d2*d3*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 8 => (d0*d1^4*d2*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | _ => 0

private def adj_1_2_row_2 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d0*d1^3*d2^2*d3^2/256 : ℂ)
  | 1 => (-d0*d1^2*d2*d3^2*(d2^2 - 2*d3^2)/256 : ℂ)
  | 2 => (d0*d1^2*d2^2*d3*(d2^2 - 2*d3^2)/256 : ℂ)
  | 3 => (d1*d2*(d0^2*d1^2*d2^2 + d0^2*d2^2*d3^2 - 2*d0^2*d3^4 + 2*d1^2*d3^4)/256 : ℂ)
  | 4 => (-d0^2*d1*d2^2*d3*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 5 => (d1^3*d2*d3^4/128 : ℂ)
  | 6 => (d0*d1^2*d2*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 7 => (-d0*d1^2*d2^2*d3*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 8 => (d0*d1^3*d2^2*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | _ => 0

private def adj_1_2_row_3 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d0*d1^3*d2*d3^3/256 : ℂ)
  | 1 => (-d0*d1^2*d3^3*(d2^2 - 2*d3^2)/256 : ℂ)
  | 2 => (d0*d1^2*d2*d3^2*(d2^2 - 2*d3^2)/256 : ℂ)
  | 3 => (d0^2*d1*d3*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 4 => (-d1*d2*d3^2*(d0^2*d1^2 + d0^2*d2^2 - 2*d0^2*d3^2 - 2*d1^2*d3^2)/256 : ℂ)
  | 5 => (d1^3*d3^5/128 : ℂ)
  | 6 => (d0*d1^2*d3*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 7 => (-d0*d1^2*d2*d3^2*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 8 => (d0*d1^3*d2*d3*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | _ => 0

private def adj_1_2_row_4 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1^3*d2*d3^2*(d1^2 + d3^2)/256 : ℂ)
  | 1 => (-d1^2*d2^2*d3^2*(d1^2 + d3^2)/256 : ℂ)
  | 2 => (d1^2*d2*d3*(d1^2*d2^2 - 2*d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 3 => (d0*d1*d2^2*(d1^2 + d3^2)^2/256 : ℂ)
  | 4 => (-d0*d1*d2*d3*(d1^4 + d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 6 => (d1^2*d2^2*(d1^2 + d3^2)^2/256 : ℂ)
  | 7 => (-d1^2*d2*d3*(d1^4 + d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 8 => (d1^3*d2*(d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2 + d3^4)/256 : ℂ)
  | _ => 0

private def adj_1_2_row_5 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1^4*d2^2*d3^2/256 : ℂ)
  | 1 => (-d1^3*d2*d3^2*(d2^2 - 2*d3^2)/256 : ℂ)
  | 2 => (d1^3*d2^2*d3*(d2^2 - 2*d3^2)/256 : ℂ)
  | 3 => (d0*d1^2*d2*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 4 => (-d0*d1^2*d2^2*d3*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 6 => (d1^3*d2*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 7 => (-d1^3*d2^2*d3*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 8 => (d1^4*d2^2*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | _ => 0

private def adj_1_2_row_6 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1^4*d2*d3^3/256 : ℂ)
  | 1 => (-d1^3*d2^2*d3^3/256 : ℂ)
  | 2 => (d1^3*d2^3*d3^2/256 : ℂ)
  | 3 => (d0*d1^2*d2^2*d3*(d1^2 + d3^2)/256 : ℂ)
  | 4 => (-d0*d1^2*d2*d3^2*(d1^2 + d2^2)/256 : ℂ)
  | 6 => (d1^3*d2^2*d3*(d1^2 + d3^2)/256 : ℂ)
  | 7 => (-d1^3*d2*d3^2*(d1^2 + d2^2)/256 : ℂ)
  | 8 => (d1^4*d2*d3*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | _ => 0

private def adj_1_2_row_7 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1^3*d2*d3^2*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | 1 => (-d1^2*d2^2*d3^2*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | 2 => (d1^2*d2^3*d3*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | 3 => (d0*d1*d2^2*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 4 => (-d0*d1*d2*d3*(d1^2*d2^2 + d1^2*d3^2 + d2^4 - d2^2*d3^2)/256 : ℂ)
  | 6 => (d1^2*d2^2*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 7 => (-d1^2*d2*d3*(d1^2*d2^2 + d1^2*d3^2 + d2^4 - d2^2*d3^2)/256 : ℂ)
  | 8 => (d1^3*d2*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_1_2_row_8 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1^3*d2^2*d3^3/256 : ℂ)
  | 1 => (-d1^2*d2^3*d3^3/256 : ℂ)
  | 2 => (d1^2*d2^4*d3^2/256 : ℂ)
  | 3 => (d0*d1*d2*d3*(d1^2*d2^2 + 2*d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 4 => (-d0*d1*d2^2*d3^2*(d1^2 + d2^2)/256 : ℂ)
  | 6 => (d1^2*d2*d3*(d1^2*d2^2 + 2*d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 7 => (-d1^2*d2^2*d3^2*(d1^2 + d2^2)/256 : ℂ)
  | 8 => (d1^3*d2^2*d3*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

def adj_1_2 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  let d0 := d 0
  let d1 := d 1
  let d2 := d 2
  let d3 := d 3
  fun i j =>
    match i.val with
    | 0 => adj_1_2_row_0 d0 d1 d2 d3 j
    | 1 => adj_1_2_row_1 d0 d1 d2 d3 j
    | 2 => adj_1_2_row_2 d0 d1 d2 d3 j
    | 3 => adj_1_2_row_3 d0 d1 d2 d3 j
    | 4 => adj_1_2_row_4 d0 d1 d2 d3 j
    | 5 => adj_1_2_row_5 d0 d1 d2 d3 j
    | 6 => adj_1_2_row_6 d0 d1 d2 d3 j
    | 7 => adj_1_2_row_7 d0 d1 d2 d3 j
    | 8 => adj_1_2_row_8 d0 d1 d2 d3 j
    | _ => 0
def rows_2_0 (i : Fin 9) : Fin 24 :=
  match i.val with
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 5
  | 5 => 6
  | 6 => 9
  | 7 => 11
  | 8 => 23
  | _ => 0

def cols_2_0 (i : Fin 9) : Fin 10 :=
  match i.val with
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 4
  | 5 => 5
  | 6 => 6
  | 7 => 8
  | 8 => 9
  | _ => 0

def minor_2_0 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  (cMatrix d).submatrix rows_2_0 cols_2_0
def detPoly_2_0 (d : Fin 4 → ℂ) : ℂ := (d 2^5*(d 2^2 + d 3^2)^2/256 : ℂ)
private def adj_2_0_row_0 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 1 => (d2^2*(d0^2 + d2^2)*(d2^2 + d3^2)^2/256 : ℂ)
  | 2 => (-d0^2*d2^3*d3*(d2^2 + d3^2)/128 : ℂ)
  | 4 => (d0*d2^4*d3*(d2^2 + d3^2)/128 : ℂ)
  | 5 => (d0*d2^5*(d2^2 + d3^2)/128 : ℂ)
  | 6 => (d2^2*(d2^2 + d3^2)*(d0^2*d2^2 - d0^2*d3^2 - d2^4 - d2^2*d3^2)/256 : ℂ)
  | 7 => (-d0^2*d1*d2^2*d3*(d2^2 + d3^2)/128 : ℂ)
  | 8 => (d2^2*(d2^2 + d3^2)*(d0^2*d2^2 - d0^2*d3^2 + d2^4 + d2^2*d3^2)/256 : ℂ)
  | _ => 0

private def adj_2_0_row_1 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 1 => (d0*d1*d2^2*(d2^2 + d3^2)^2/256 : ℂ)
  | 2 => (-d0*d1*d2^3*d3*(d2^2 + d3^2)/128 : ℂ)
  | 3 => (d2^4*(d2^2 + d3^2)^2/128 : ℂ)
  | 4 => (d1*d2^4*d3*(d2^2 + d3^2)/128 : ℂ)
  | 5 => (d1*d2^5*(d2^2 + d3^2)/128 : ℂ)
  | 6 => (d0*d1*d2^2*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | 7 => (-d0*d1^2*d2^2*d3*(d2^2 + d3^2)/128 : ℂ)
  | 8 => (d0*d1*d2^2*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_2_0_row_2 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 1 => (d0*d2^3*(d2^2 + d3^2)^2/256 : ℂ)
  | 2 => (-d0*d2^4*d3*(d2^2 + d3^2)/128 : ℂ)
  | 4 => (d2^5*d3*(d2^2 + d3^2)/128 : ℂ)
  | 5 => (d2^6*(d2^2 + d3^2)/128 : ℂ)
  | 6 => (d0*d2^3*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | 7 => (-d0*d1*d2^3*d3*(d2^2 + d3^2)/128 : ℂ)
  | 8 => (d0*d2^3*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_2_0_row_3 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 1 => (d0*d2^2*d3*(d2^2 + d3^2)^2/256 : ℂ)
  | 2 => (-d0*d2^3*d3^2*(d2^2 + d3^2)/128 : ℂ)
  | 4 => (-d2^6*(d2^2 + d3^2)/128 : ℂ)
  | 5 => (d2^5*d3*(d2^2 + d3^2)/128 : ℂ)
  | 6 => (d0*d2^2*d3*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | 7 => (-d0*d1*d2^2*d3^2*(d2^2 + d3^2)/128 : ℂ)
  | 8 => (d0*d2^2*d3*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_2_0_row_4 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d1*d2^5*(d2^2 + d3^2)/128 : ℂ)
  | 1 => (d2^2*(d1^2 + d2^2)*(d2^2 + d3^2)^2/256 : ℂ)
  | 2 => (-d1^2*d2^3*d3*(d2^2 + d3^2)/128 : ℂ)
  | 6 => (d2^2*(d2^2 + d3^2)*(d1^2*d2^2 - d1^2*d3^2 - d2^4 - d2^2*d3^2)/256 : ℂ)
  | 7 => (-d1*d2^2*d3*(d1^2 + d2^2)*(d2^2 + d3^2)/128 : ℂ)
  | 8 => (d2^2*(d2^2 + d3^2)*(d1^2*d2^2 - d1^2*d3^2 - d2^4 - d2^2*d3^2)/256 : ℂ)
  | _ => 0

private def adj_2_0_row_5 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d2^6*(d2^2 + d3^2)/128 : ℂ)
  | 1 => (d1*d2^3*(d2^2 + d3^2)^2/256 : ℂ)
  | 2 => (-d1*d2^4*d3*(d2^2 + d3^2)/128 : ℂ)
  | 6 => (d1*d2^3*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | 7 => (-d2^3*d3*(d1^2 + d2^2)*(d2^2 + d3^2)/128 : ℂ)
  | 8 => (d1*d2^3*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_2_0_row_6 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (-d2^5*d3*(d2^2 + d3^2)/128 : ℂ)
  | 1 => (d1*d2^2*d3*(d2^2 + d3^2)^2/256 : ℂ)
  | 2 => (-d1*d2^3*d3^2*(d2^2 + d3^2)/128 : ℂ)
  | 6 => (d1*d2^2*d3*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | 7 => (-d2^2*(d2^2 + d3^2)*(d1*d3 - d2^2)*(d1*d3 + d2^2)/128 : ℂ)
  | 8 => (d1*d2^2*d3*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_2_0_row_7 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 1 => (d2^3*d3*(d2^2 + d3^2)^2/256 : ℂ)
  | 2 => (-d2^4*(d2^2 + d3^2)^2/128 : ℂ)
  | 6 => (-d2^3*d3*(d2^2 + d3^2)^2/256 : ℂ)
  | 7 => (-d1*d2^3*(d2^2 + d3^2)^2/128 : ℂ)
  | 8 => (-d2^3*d3*(d2^2 + d3^2)^2/256 : ℂ)
  | _ => 0

private def adj_2_0_row_8 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 1 => (d2^2*(d2^2 + d3^2)^3/256 : ℂ)
  | 2 => (-d2^3*d3*(d2^2 + d3^2)^2/128 : ℂ)
  | 6 => (d2^2*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)^2/256 : ℂ)
  | 7 => (-d1*d2^2*d3*(d2^2 + d3^2)^2/128 : ℂ)
  | 8 => (d2^2*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)^2/256 : ℂ)
  | _ => 0

def adj_2_0 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  let d0 := d 0
  let d1 := d 1
  let d2 := d 2
  let d3 := d 3
  fun i j =>
    match i.val with
    | 0 => adj_2_0_row_0 d0 d1 d2 d3 j
    | 1 => adj_2_0_row_1 d0 d1 d2 d3 j
    | 2 => adj_2_0_row_2 d0 d1 d2 d3 j
    | 3 => adj_2_0_row_3 d0 d1 d2 d3 j
    | 4 => adj_2_0_row_4 d0 d1 d2 d3 j
    | 5 => adj_2_0_row_5 d0 d1 d2 d3 j
    | 6 => adj_2_0_row_6 d0 d1 d2 d3 j
    | 7 => adj_2_0_row_7 d0 d1 d2 d3 j
    | 8 => adj_2_0_row_8 d0 d1 d2 d3 j
    | _ => 0
def rows_2_1 (i : Fin 9) : Fin 24 :=
  match i.val with
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 4
  | 5 => 7
  | 6 => 9
  | 7 => 10
  | 8 => 15
  | _ => 0

def cols_2_1 (i : Fin 9) : Fin 10 :=
  match i.val with
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 4
  | 5 => 5
  | 6 => 6
  | 7 => 7
  | 8 => 8
  | _ => 0

def minor_2_1 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  (cMatrix d).submatrix rows_2_1 cols_2_1
def detPoly_2_1 (d : Fin 4 → ℂ) : ℂ := (-d 1^4*d 2*d 3^4/256 : ℂ)
private def adj_2_1_row_0 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1^3*d2*d3^2*(d0 - d3)*(d0 + d3)/256 : ℂ)
  | 1 => (-d1^2*d3^2*(d0^2*d2^2 - 2*d0^2*d3^2 - d2^2*d3^2)/256 : ℂ)
  | 2 => (d1^2*d2*d3*(d0^2*d2^2 - 2*d0^2*d3^2 - d2^2*d3^2)/256 : ℂ)
  | 3 => (d0*d1*(d0^2*d1^2*d2^2 + d0^2*d2^2*d3^2 - 2*d0^2*d3^4 - d1^2*d2^2*d3^2 - d2^2*d3^4)/256 : ℂ)
  | 4 => (-d0*d1*d2*d3*(d0^2*d1^2 + d0^2*d2^2 - 2*d0^2*d3^2 - d1^2*d3^2 - d2^2*d3^2)/256 : ℂ)
  | 5 => (d0*d1^3*d3^4/128 : ℂ)
  | 6 => (d1^2*(d0^2*d1^2*d2^2 + d0^2*d2^2*d3^2 - 2*d0^2*d3^4 - d1^2*d2^2*d3^2 - d2^2*d3^4)/256 : ℂ)
  | 7 => (-d1^2*d2*d3*(d0^2*d1^2 + d0^2*d2^2 - 2*d0^2*d3^2 - d1^2*d3^2 - d2^2*d3^2)/256 : ℂ)
  | 8 => (d1^3*d2*(d0^2*d2^2 - d0^2*d3^2 - d2^2*d3^2 - d3^4)/256 : ℂ)
  | _ => 0

private def adj_2_1_row_1 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d0*d1^4*d2*d3^2/256 : ℂ)
  | 1 => (-d0*d1^3*d3^2*(d2^2 - 2*d3^2)/256 : ℂ)
  | 2 => (d0*d1^3*d2*d3*(d2^2 - 2*d3^2)/256 : ℂ)
  | 3 => (d0^2*d1^2*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 4 => (-d0^2*d1^2*d2*d3*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 5 => (d1^4*d3^4/128 : ℂ)
  | 6 => (d0*d1^3*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 7 => (-d0*d1^3*d2*d3*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 8 => (d0*d1^4*d2*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | _ => 0

private def adj_2_1_row_2 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d0*d1^3*d2^2*d3^2/256 : ℂ)
  | 1 => (-d0*d1^2*d2*d3^2*(d2^2 - 2*d3^2)/256 : ℂ)
  | 2 => (d0*d1^2*d2^2*d3*(d2^2 - 2*d3^2)/256 : ℂ)
  | 3 => (d1*d2*(d0^2*d1^2*d2^2 + d0^2*d2^2*d3^2 - 2*d0^2*d3^4 + 2*d1^2*d3^4)/256 : ℂ)
  | 4 => (-d0^2*d1*d2^2*d3*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 5 => (d1^3*d2*d3^4/128 : ℂ)
  | 6 => (d0*d1^2*d2*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 7 => (-d0*d1^2*d2^2*d3*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 8 => (d0*d1^3*d2^2*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | _ => 0

private def adj_2_1_row_3 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d0*d1^3*d2*d3^3/256 : ℂ)
  | 1 => (-d0*d1^2*d3^3*(d2^2 - 2*d3^2)/256 : ℂ)
  | 2 => (d0*d1^2*d2*d3^2*(d2^2 - 2*d3^2)/256 : ℂ)
  | 3 => (d0^2*d1*d3*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 4 => (-d1*d2*d3^2*(d0^2*d1^2 + d0^2*d2^2 - 2*d0^2*d3^2 - 2*d1^2*d3^2)/256 : ℂ)
  | 5 => (d1^3*d3^5/128 : ℂ)
  | 6 => (d0*d1^2*d3*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 7 => (-d0*d1^2*d2*d3^2*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 8 => (d0*d1^3*d2*d3*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | _ => 0

private def adj_2_1_row_4 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1^3*d2*d3^2*(d1^2 + d3^2)/256 : ℂ)
  | 1 => (-d1^2*d2^2*d3^2*(d1^2 + d3^2)/256 : ℂ)
  | 2 => (d1^2*d2*d3*(d1^2*d2^2 - 2*d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 3 => (d0*d1*d2^2*(d1^2 + d3^2)^2/256 : ℂ)
  | 4 => (-d0*d1*d2*d3*(d1^4 + d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 6 => (d1^2*d2^2*(d1^2 + d3^2)^2/256 : ℂ)
  | 7 => (-d1^2*d2*d3*(d1^4 + d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 8 => (d1^3*d2*(d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2 + d3^4)/256 : ℂ)
  | _ => 0

private def adj_2_1_row_5 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1^4*d2^2*d3^2/256 : ℂ)
  | 1 => (-d1^3*d2*d3^2*(d2^2 - 2*d3^2)/256 : ℂ)
  | 2 => (d1^3*d2^2*d3*(d2^2 - 2*d3^2)/256 : ℂ)
  | 3 => (d0*d1^2*d2*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 4 => (-d0*d1^2*d2^2*d3*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 6 => (d1^3*d2*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 7 => (-d1^3*d2^2*d3*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 8 => (d1^4*d2^2*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | _ => 0

private def adj_2_1_row_6 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1^4*d2*d3^3/256 : ℂ)
  | 1 => (-d1^3*d2^2*d3^3/256 : ℂ)
  | 2 => (d1^3*d2^3*d3^2/256 : ℂ)
  | 3 => (d0*d1^2*d2^2*d3*(d1^2 + d3^2)/256 : ℂ)
  | 4 => (-d0*d1^2*d2*d3^2*(d1^2 + d2^2)/256 : ℂ)
  | 6 => (d1^3*d2^2*d3*(d1^2 + d3^2)/256 : ℂ)
  | 7 => (-d1^3*d2*d3^2*(d1^2 + d2^2)/256 : ℂ)
  | 8 => (d1^4*d2*d3*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | _ => 0

private def adj_2_1_row_7 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1^3*d2*d3^2*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | 1 => (-d1^2*d2^2*d3^2*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | 2 => (d1^2*d2^3*d3*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | 3 => (d0*d1*d2^2*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 4 => (-d0*d1*d2*d3*(d1^2*d2^2 + d1^2*d3^2 + d2^4 - d2^2*d3^2)/256 : ℂ)
  | 6 => (d1^2*d2^2*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 7 => (-d1^2*d2*d3*(d1^2*d2^2 + d1^2*d3^2 + d2^4 - d2^2*d3^2)/256 : ℂ)
  | 8 => (d1^3*d2*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_2_1_row_8 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1^3*d2^2*d3^3/256 : ℂ)
  | 1 => (-d1^2*d2^3*d3^3/256 : ℂ)
  | 2 => (d1^2*d2^4*d3^2/256 : ℂ)
  | 3 => (d0*d1*d2*d3*(d1^2*d2^2 + 2*d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 4 => (-d0*d1*d2^2*d3^2*(d1^2 + d2^2)/256 : ℂ)
  | 6 => (d1^2*d2*d3*(d1^2*d2^2 + 2*d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 7 => (-d1^2*d2^2*d3^2*(d1^2 + d2^2)/256 : ℂ)
  | 8 => (d1^3*d2^2*d3*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

def adj_2_1 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  let d0 := d 0
  let d1 := d 1
  let d2 := d 2
  let d3 := d 3
  fun i j =>
    match i.val with
    | 0 => adj_2_1_row_0 d0 d1 d2 d3 j
    | 1 => adj_2_1_row_1 d0 d1 d2 d3 j
    | 2 => adj_2_1_row_2 d0 d1 d2 d3 j
    | 3 => adj_2_1_row_3 d0 d1 d2 d3 j
    | 4 => adj_2_1_row_4 d0 d1 d2 d3 j
    | 5 => adj_2_1_row_5 d0 d1 d2 d3 j
    | 6 => adj_2_1_row_6 d0 d1 d2 d3 j
    | 7 => adj_2_1_row_7 d0 d1 d2 d3 j
    | 8 => adj_2_1_row_8 d0 d1 d2 d3 j
    | _ => 0
def rows_2_2 (i : Fin 9) : Fin 24 :=
  match i.val with
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 5
  | 5 => 9
  | 6 => 13
  | 7 => 15
  | 8 => 17
  | _ => 0

def cols_2_2 (i : Fin 9) : Fin 10 :=
  match i.val with
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 4
  | 5 => 5
  | 6 => 6
  | 7 => 7
  | 8 => 8
  | _ => 0

def minor_2_2 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  (cMatrix d).submatrix rows_2_2 cols_2_2
def detPoly_2_2 (d : Fin 4 → ℂ) : ℂ := (d 2^3*d 3^4*(d 1^2 + d 3^2)/256 : ℂ)
private def adj_2_2_row_0 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1*d2*d3^2*(d0^2*d1^2 - d0^2*d3^2 - d1^2*d3^2 - d3^4)/256 : ℂ)
  | 1 => (-d2^2*d3^2*(d0^2*d1^2 - d0^2*d3^2 - d1^2*d3^2 - d3^4)/256 : ℂ)
  | 2 => (-d1^2*d2*d3*(d0^2*d1^2 - d0^2*d3^2 - d1^2*d3^2 - d3^4)/256 : ℂ)
  | 3 => (d0*d1*(d0^2*d1^2*d2^2 + d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 - d0^2*d3^4 - d1^2*d2^2*d3^2 - d1^2*d3^4 - 3*d2^2*d3^4 - d3^6)/256 : ℂ)
  | 4 => (d0*d3*(d0^2*d1^4 + d0^2*d1^2*d2^2 - d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 - d1^4*d3^2 - d1^2*d2^2*d3^2 - d1^2*d3^4 + d2^2*d3^4)/256 : ℂ)
  | 5 => (d2^2*(d1^2 + d3^2)*(d0^2*d1^2 - d0^2*d3^2 - d1^2*d3^2 - d3^4)/256 : ℂ)
  | 6 => (d0*d2^3*d3^4/128 : ℂ)
  | 7 => (d1*d2*(d0^2*d1^2*d2^2 + d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 - d0^2*d3^4 - d1^2*d2^2*d3^2 - d1^2*d3^4 - d2^2*d3^4 - d3^6)/256 : ℂ)
  | 8 => (d2*d3*(d0^2*d1^4 + d0^2*d1^2*d2^2 - d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 - d1^4*d3^2 - d1^2*d2^2*d3^2 - d1^2*d3^4 - d2^2*d3^4)/256 : ℂ)
  | _ => 0

private def adj_2_2_row_1 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d0*d1^2*d2*d3^2*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 1 => (-d0*d1*d2^2*d3^2*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 2 => (-d0*d1^3*d2*d3*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 3 => ((d0^2*d1^4*d2^2 + d0^2*d1^4*d3^2 + d0^2*d1^2*d2^2*d3^2 - d0^2*d1^2*d3^4 + 2*d2^2*d3^6)/256 : ℂ)
  | 4 => (d1*d3*(d0^2*d1^4 + d0^2*d1^2*d2^2 - d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 + 2*d2^2*d3^4)/256 : ℂ)
  | 5 => (d0*d1*d2^2*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 6 => (d1*d2^3*d3^4/128 : ℂ)
  | 7 => (d0*d1^2*d2*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 8 => (d0*d1*d2*d3*(d1^4 + d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | _ => 0

private def adj_2_2_row_2 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d0*d1*d2^2*d3^2*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 1 => (-d0*d2^3*d3^2*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 2 => (-d0*d1^2*d2^2*d3*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 3 => (d1*d2*(d0^2*d1^2*d2^2 + d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 - d0^2*d3^4 - 2*d2^2*d3^4)/256 : ℂ)
  | 4 => (d2*d3*(d0^2*d1^4 + d0^2*d1^2*d2^2 - d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 + 2*d2^2*d3^4)/256 : ℂ)
  | 5 => (d0*d2^3*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 6 => (d2^4*d3^4/128 : ℂ)
  | 7 => (d0*d1*d2^2*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 8 => (d0*d2^2*d3*(d1^4 + d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | _ => 0

private def adj_2_2_row_3 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d0*d1*d2*d3^3*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 1 => (-d0*d2^2*d3^3*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 2 => (-d0*d1^2*d2*d3^2*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 3 => (d1*d3*(d0^2*d1^2*d2^2 + d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 - d0^2*d3^4 - 2*d2^2*d3^4)/256 : ℂ)
  | 4 => (d3^2*(d0^2*d1^4 + d0^2*d1^2*d2^2 - d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 - 2*d1^2*d2^2*d3^2)/256 : ℂ)
  | 5 => (d0*d2^2*d3*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 6 => (d2^3*d3^5/128 : ℂ)
  | 7 => (d0*d1*d2*d3*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 8 => (d0*d2*d3^2*(d1^4 + d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | _ => 0

private def adj_2_2_row_4 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1*d2*d3^2*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 1 => (-d2^2*d3^2*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 2 => (-d1^2*d2*d3*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 3 => (d0*d1*(d1^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 4 => (d0*d3*(d1^2 + d3^2)*(d1^4 + d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 5 => (d2^2*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)^2/256 : ℂ)
  | 7 => (d1*d2*(d1^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 8 => (d2*d3*(d1^2 + d3^2)*(d1^4 + d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | _ => 0

private def adj_2_2_row_5 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d2^2*d3^2*(d1^2 - 2*d3^2)*(d1^2 + d3^2)/256 : ℂ)
  | 1 => (-d1*d2^3*d3^2*(d1^2 + d3^2)/256 : ℂ)
  | 2 => (-d1*d2^2*d3*(d1^2 - 2*d3^2)*(d1^2 + d3^2)/256 : ℂ)
  | 3 => (d0*d2*(d1^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 4 => (d0*d1*d2*d3*(d1^2 + d3^2)*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 5 => (d1*d2^3*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 7 => (d2^2*(d1^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 8 => (d1*d2^2*d3*(d1^2 + d3^2)*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | _ => 0

private def adj_2_2_row_6 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1^2*d2*d3^3*(d1^2 + d3^2)/256 : ℂ)
  | 1 => (-d1*d2^2*d3^3*(d1^2 + d3^2)/256 : ℂ)
  | 2 => (-d1^3*d2*d3^2*(d1^2 + d3^2)/256 : ℂ)
  | 3 => (d0*d3*(d1^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 + 2*d2^2*d3^2)/256 : ℂ)
  | 4 => (d0*d1*d3^2*(d1^2 + d2^2)*(d1^2 + d3^2)/256 : ℂ)
  | 5 => (d1*d2^2*d3*(d1^2 + d3^2)^2/256 : ℂ)
  | 7 => (d2*d3*(d1^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 + 2*d2^2*d3^2)/256 : ℂ)
  | 8 => (d1*d2*d3^2*(d1^2 + d2^2)*(d1^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_2_2_row_7 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1*d2*d3^2*(d1^2 + d3^2)*(d2^2 + d3^2)/256 : ℂ)
  | 1 => (-d2^2*d3^2*(d1^2 + d3^2)*(d2^2 + d3^2)/256 : ℂ)
  | 2 => (-d2*d3*(d1^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 - 2*d2^2*d3^2)/256 : ℂ)
  | 3 => (d0*d1*(d1^2 + d3^2)*(d2^2 + d3^2)^2/256 : ℂ)
  | 4 => (d0*d3*(d1^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 + d2^4 - d2^2*d3^2)/256 : ℂ)
  | 5 => (d2^2*(d1^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 - d2^2*d3^2 + d3^4)/256 : ℂ)
  | 7 => (d1*d2*(d1^2 + d3^2)*(d2^2 + d3^2)^2/256 : ℂ)
  | 8 => (d2*d3*(d1^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 + d2^4 - d2^2*d3^2)/256 : ℂ)
  | _ => 0

private def adj_2_2_row_8 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1*d2^2*d3^3*(d1^2 + d3^2)/256 : ℂ)
  | 1 => (-d2^3*d3^3*(d1^2 + d3^2)/256 : ℂ)
  | 2 => (-d1^2*d2^2*d3^2*(d1^2 + d3^2)/256 : ℂ)
  | 3 => (d0*d1*d2*d3*(d1^2 + d3^2)*(d2^2 + d3^2)/256 : ℂ)
  | 4 => (d0*d2*d3^2*(d1^2 + d2^2)*(d1^2 + d3^2)/256 : ℂ)
  | 5 => (d2^3*d3*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 7 => (d1*d2^2*d3*(d1^2 + d3^2)*(d2^2 + d3^2)/256 : ℂ)
  | 8 => (d2^2*d3^2*(d1^2 + d2^2)*(d1^2 + d3^2)/256 : ℂ)
  | _ => 0

def adj_2_2 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  let d0 := d 0
  let d1 := d 1
  let d2 := d 2
  let d3 := d 3
  fun i j =>
    match i.val with
    | 0 => adj_2_2_row_0 d0 d1 d2 d3 j
    | 1 => adj_2_2_row_1 d0 d1 d2 d3 j
    | 2 => adj_2_2_row_2 d0 d1 d2 d3 j
    | 3 => adj_2_2_row_3 d0 d1 d2 d3 j
    | 4 => adj_2_2_row_4 d0 d1 d2 d3 j
    | 5 => adj_2_2_row_5 d0 d1 d2 d3 j
    | 6 => adj_2_2_row_6 d0 d1 d2 d3 j
    | 7 => adj_2_2_row_7 d0 d1 d2 d3 j
    | 8 => adj_2_2_row_8 d0 d1 d2 d3 j
    | _ => 0
def rows_3_0 (i : Fin 9) : Fin 24 :=
  match i.val with
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 4
  | 4 => 5
  | 5 => 6
  | 6 => 10
  | 7 => 11
  | 8 => 17
  | _ => 0

def cols_3_0 (i : Fin 9) : Fin 10 :=
  match i.val with
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 4
  | 5 => 5
  | 6 => 6
  | 7 => 7
  | 8 => 8
  | _ => 0

def minor_3_0 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  (cMatrix d).submatrix rows_3_0 cols_3_0
def detPoly_3_0 (d : Fin 4 → ℂ) : ℂ := (-d 3^5*(d 2^2 + d 3^2)^2/256 : ℂ)
private def adj_3_0_row_0 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 1 => (d0^2*d2*d3^3*(d2^2 + d3^2)/128 : ℂ)
  | 2 => (-d3^2*(d0^2 + d3^2)*(d2^2 + d3^2)^2/256 : ℂ)
  | 4 => (d0*d2*d3^4*(d2^2 + d3^2)/128 : ℂ)
  | 5 => (-d0*d3^5*(d2^2 + d3^2)/128 : ℂ)
  | 6 => (d3^2*(d2^2 + d3^2)*(d0^2*d2^2 - d0^2*d3^2 + d2^2*d3^2 + d3^4)/256 : ℂ)
  | 7 => (-d0^2*d1*d2*d3^2*(d2^2 + d3^2)/128 : ℂ)
  | 8 => (-d3^2*(d2^2 + d3^2)*(d0^2*d2^2 - d0^2*d3^2 - d2^2*d3^2 - d3^4)/256 : ℂ)
  | _ => 0

private def adj_3_0_row_1 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 1 => (d0*d1*d2*d3^3*(d2^2 + d3^2)/128 : ℂ)
  | 2 => (-d0*d1*d3^2*(d2^2 + d3^2)^2/256 : ℂ)
  | 3 => (-d3^4*(d2^2 + d3^2)^2/128 : ℂ)
  | 4 => (d1*d2*d3^4*(d2^2 + d3^2)/128 : ℂ)
  | 5 => (-d1*d3^5*(d2^2 + d3^2)/128 : ℂ)
  | 6 => (d0*d1*d3^2*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | 7 => (-d0*d1^2*d2*d3^2*(d2^2 + d3^2)/128 : ℂ)
  | 8 => (-d0*d1*d3^2*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_3_0_row_2 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 1 => (d0*d2^2*d3^3*(d2^2 + d3^2)/128 : ℂ)
  | 2 => (-d0*d2*d3^2*(d2^2 + d3^2)^2/256 : ℂ)
  | 4 => (-d3^6*(d2^2 + d3^2)/128 : ℂ)
  | 5 => (-d2*d3^5*(d2^2 + d3^2)/128 : ℂ)
  | 6 => (d0*d2*d3^2*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | 7 => (-d0*d1*d2^2*d3^2*(d2^2 + d3^2)/128 : ℂ)
  | 8 => (-d0*d2*d3^2*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_3_0_row_3 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 1 => (d0*d2*d3^4*(d2^2 + d3^2)/128 : ℂ)
  | 2 => (-d0*d3^3*(d2^2 + d3^2)^2/256 : ℂ)
  | 4 => (d2*d3^5*(d2^2 + d3^2)/128 : ℂ)
  | 5 => (-d3^6*(d2^2 + d3^2)/128 : ℂ)
  | 6 => (d0*d3^3*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | 7 => (-d0*d1*d2*d3^3*(d2^2 + d3^2)/128 : ℂ)
  | 8 => (-d0*d3^3*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_3_0_row_4 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1*d3^5*(d2^2 + d3^2)/128 : ℂ)
  | 1 => (d1^2*d2*d3^3*(d2^2 + d3^2)/128 : ℂ)
  | 2 => (-d3^2*(d1^2 + d3^2)*(d2^2 + d3^2)^2/256 : ℂ)
  | 6 => (d3^2*(d2^2 + d3^2)*(d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2 + d3^4)/256 : ℂ)
  | 7 => (-d1*d2*d3^2*(d1^2 + d3^2)*(d2^2 + d3^2)/128 : ℂ)
  | 8 => (-d3^2*(d2^2 + d3^2)*(d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2 + d3^4)/256 : ℂ)
  | _ => 0

private def adj_3_0_row_5 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d2*d3^5*(d2^2 + d3^2)/128 : ℂ)
  | 1 => (d1*d2^2*d3^3*(d2^2 + d3^2)/128 : ℂ)
  | 2 => (-d1*d2*d3^2*(d2^2 + d3^2)^2/256 : ℂ)
  | 6 => (d1*d2*d3^2*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | 7 => (-d3^2*(d2^2 + d3^2)*(d1*d2 - d3^2)*(d1*d2 + d3^2)/128 : ℂ)
  | 8 => (-d1*d2*d3^2*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_3_0_row_6 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d3^6*(d2^2 + d3^2)/128 : ℂ)
  | 1 => (d1*d2*d3^4*(d2^2 + d3^2)/128 : ℂ)
  | 2 => (-d1*d3^3*(d2^2 + d3^2)^2/256 : ℂ)
  | 6 => (d1*d3^3*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | 7 => (-d2*d3^3*(d1^2 + d3^2)*(d2^2 + d3^2)/128 : ℂ)
  | 8 => (-d1*d3^3*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_3_0_row_7 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 1 => (d2*d3^3*(d2^2 + d3^2)^2/128 : ℂ)
  | 2 => (-d3^2*(d2^2 + d3^2)^3/256 : ℂ)
  | 6 => (d3^2*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)^2/256 : ℂ)
  | 7 => (-d1*d2*d3^2*(d2^2 + d3^2)^2/128 : ℂ)
  | 8 => (-d3^2*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)^2/256 : ℂ)
  | _ => 0

private def adj_3_0_row_8 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 1 => (d3^4*(d2^2 + d3^2)^2/128 : ℂ)
  | 2 => (-d2*d3^3*(d2^2 + d3^2)^2/256 : ℂ)
  | 6 => (d2*d3^3*(d2^2 + d3^2)^2/256 : ℂ)
  | 7 => (-d1*d3^3*(d2^2 + d3^2)^2/128 : ℂ)
  | 8 => (-d2*d3^3*(d2^2 + d3^2)^2/256 : ℂ)
  | _ => 0

def adj_3_0 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  let d0 := d 0
  let d1 := d 1
  let d2 := d 2
  let d3 := d 3
  fun i j =>
    match i.val with
    | 0 => adj_3_0_row_0 d0 d1 d2 d3 j
    | 1 => adj_3_0_row_1 d0 d1 d2 d3 j
    | 2 => adj_3_0_row_2 d0 d1 d2 d3 j
    | 3 => adj_3_0_row_3 d0 d1 d2 d3 j
    | 4 => adj_3_0_row_4 d0 d1 d2 d3 j
    | 5 => adj_3_0_row_5 d0 d1 d2 d3 j
    | 6 => adj_3_0_row_6 d0 d1 d2 d3 j
    | 7 => adj_3_0_row_7 d0 d1 d2 d3 j
    | 8 => adj_3_0_row_8 d0 d1 d2 d3 j
    | _ => 0
def rows_3_1 (i : Fin 9) : Fin 24 :=
  match i.val with
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 4
  | 5 => 7
  | 6 => 9
  | 7 => 10
  | 8 => 15
  | _ => 0

def cols_3_1 (i : Fin 9) : Fin 10 :=
  match i.val with
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 4
  | 5 => 5
  | 6 => 6
  | 7 => 7
  | 8 => 8
  | _ => 0

def minor_3_1 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  (cMatrix d).submatrix rows_3_1 cols_3_1
def detPoly_3_1 (d : Fin 4 → ℂ) : ℂ := (-d 1^4*d 2*d 3^4/256 : ℂ)
private def adj_3_1_row_0 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1^3*d2*d3^2*(d0 - d3)*(d0 + d3)/256 : ℂ)
  | 1 => (-d1^2*d3^2*(d0^2*d2^2 - 2*d0^2*d3^2 - d2^2*d3^2)/256 : ℂ)
  | 2 => (d1^2*d2*d3*(d0^2*d2^2 - 2*d0^2*d3^2 - d2^2*d3^2)/256 : ℂ)
  | 3 => (d0*d1*(d0^2*d1^2*d2^2 + d0^2*d2^2*d3^2 - 2*d0^2*d3^4 - d1^2*d2^2*d3^2 - d2^2*d3^4)/256 : ℂ)
  | 4 => (-d0*d1*d2*d3*(d0^2*d1^2 + d0^2*d2^2 - 2*d0^2*d3^2 - d1^2*d3^2 - d2^2*d3^2)/256 : ℂ)
  | 5 => (d0*d1^3*d3^4/128 : ℂ)
  | 6 => (d1^2*(d0^2*d1^2*d2^2 + d0^2*d2^2*d3^2 - 2*d0^2*d3^4 - d1^2*d2^2*d3^2 - d2^2*d3^4)/256 : ℂ)
  | 7 => (-d1^2*d2*d3*(d0^2*d1^2 + d0^2*d2^2 - 2*d0^2*d3^2 - d1^2*d3^2 - d2^2*d3^2)/256 : ℂ)
  | 8 => (d1^3*d2*(d0^2*d2^2 - d0^2*d3^2 - d2^2*d3^2 - d3^4)/256 : ℂ)
  | _ => 0

private def adj_3_1_row_1 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d0*d1^4*d2*d3^2/256 : ℂ)
  | 1 => (-d0*d1^3*d3^2*(d2^2 - 2*d3^2)/256 : ℂ)
  | 2 => (d0*d1^3*d2*d3*(d2^2 - 2*d3^2)/256 : ℂ)
  | 3 => (d0^2*d1^2*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 4 => (-d0^2*d1^2*d2*d3*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 5 => (d1^4*d3^4/128 : ℂ)
  | 6 => (d0*d1^3*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 7 => (-d0*d1^3*d2*d3*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 8 => (d0*d1^4*d2*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | _ => 0

private def adj_3_1_row_2 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d0*d1^3*d2^2*d3^2/256 : ℂ)
  | 1 => (-d0*d1^2*d2*d3^2*(d2^2 - 2*d3^2)/256 : ℂ)
  | 2 => (d0*d1^2*d2^2*d3*(d2^2 - 2*d3^2)/256 : ℂ)
  | 3 => (d1*d2*(d0^2*d1^2*d2^2 + d0^2*d2^2*d3^2 - 2*d0^2*d3^4 + 2*d1^2*d3^4)/256 : ℂ)
  | 4 => (-d0^2*d1*d2^2*d3*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 5 => (d1^3*d2*d3^4/128 : ℂ)
  | 6 => (d0*d1^2*d2*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 7 => (-d0*d1^2*d2^2*d3*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 8 => (d0*d1^3*d2^2*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | _ => 0

private def adj_3_1_row_3 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d0*d1^3*d2*d3^3/256 : ℂ)
  | 1 => (-d0*d1^2*d3^3*(d2^2 - 2*d3^2)/256 : ℂ)
  | 2 => (d0*d1^2*d2*d3^2*(d2^2 - 2*d3^2)/256 : ℂ)
  | 3 => (d0^2*d1*d3*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 4 => (-d1*d2*d3^2*(d0^2*d1^2 + d0^2*d2^2 - 2*d0^2*d3^2 - 2*d1^2*d3^2)/256 : ℂ)
  | 5 => (d1^3*d3^5/128 : ℂ)
  | 6 => (d0*d1^2*d3*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 7 => (-d0*d1^2*d2*d3^2*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 8 => (d0*d1^3*d2*d3*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | _ => 0

private def adj_3_1_row_4 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1^3*d2*d3^2*(d1^2 + d3^2)/256 : ℂ)
  | 1 => (-d1^2*d2^2*d3^2*(d1^2 + d3^2)/256 : ℂ)
  | 2 => (d1^2*d2*d3*(d1^2*d2^2 - 2*d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 3 => (d0*d1*d2^2*(d1^2 + d3^2)^2/256 : ℂ)
  | 4 => (-d0*d1*d2*d3*(d1^4 + d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 6 => (d1^2*d2^2*(d1^2 + d3^2)^2/256 : ℂ)
  | 7 => (-d1^2*d2*d3*(d1^4 + d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 8 => (d1^3*d2*(d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2 + d3^4)/256 : ℂ)
  | _ => 0

private def adj_3_1_row_5 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1^4*d2^2*d3^2/256 : ℂ)
  | 1 => (-d1^3*d2*d3^2*(d2^2 - 2*d3^2)/256 : ℂ)
  | 2 => (d1^3*d2^2*d3*(d2^2 - 2*d3^2)/256 : ℂ)
  | 3 => (d0*d1^2*d2*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 4 => (-d0*d1^2*d2^2*d3*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 6 => (d1^3*d2*(d1^2*d2^2 + d2^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 7 => (-d1^3*d2^2*d3*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 8 => (d1^4*d2^2*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | _ => 0

private def adj_3_1_row_6 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1^4*d2*d3^3/256 : ℂ)
  | 1 => (-d1^3*d2^2*d3^3/256 : ℂ)
  | 2 => (d1^3*d2^3*d3^2/256 : ℂ)
  | 3 => (d0*d1^2*d2^2*d3*(d1^2 + d3^2)/256 : ℂ)
  | 4 => (-d0*d1^2*d2*d3^2*(d1^2 + d2^2)/256 : ℂ)
  | 6 => (d1^3*d2^2*d3*(d1^2 + d3^2)/256 : ℂ)
  | 7 => (-d1^3*d2*d3^2*(d1^2 + d2^2)/256 : ℂ)
  | 8 => (d1^4*d2*d3*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | _ => 0

private def adj_3_1_row_7 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1^3*d2*d3^2*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | 1 => (-d1^2*d2^2*d3^2*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | 2 => (d1^2*d2^3*d3*(d2 - d3)*(d2 + d3)/256 : ℂ)
  | 3 => (d0*d1*d2^2*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 4 => (-d0*d1*d2*d3*(d1^2*d2^2 + d1^2*d3^2 + d2^4 - d2^2*d3^2)/256 : ℂ)
  | 6 => (d1^2*d2^2*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 7 => (-d1^2*d2*d3*(d1^2*d2^2 + d1^2*d3^2 + d2^4 - d2^2*d3^2)/256 : ℂ)
  | 8 => (d1^3*d2*(d2 - d3)*(d2 + d3)*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_3_1_row_8 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1^3*d2^2*d3^3/256 : ℂ)
  | 1 => (-d1^2*d2^3*d3^3/256 : ℂ)
  | 2 => (d1^2*d2^4*d3^2/256 : ℂ)
  | 3 => (d0*d1*d2*d3*(d1^2*d2^2 + 2*d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 4 => (-d0*d1*d2^2*d3^2*(d1^2 + d2^2)/256 : ℂ)
  | 6 => (d1^2*d2*d3*(d1^2*d2^2 + 2*d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 7 => (-d1^2*d2^2*d3^2*(d1^2 + d2^2)/256 : ℂ)
  | 8 => (d1^3*d2^2*d3*(d2^2 + d3^2)/256 : ℂ)
  | _ => 0

def adj_3_1 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  let d0 := d 0
  let d1 := d 1
  let d2 := d 2
  let d3 := d 3
  fun i j =>
    match i.val with
    | 0 => adj_3_1_row_0 d0 d1 d2 d3 j
    | 1 => adj_3_1_row_1 d0 d1 d2 d3 j
    | 2 => adj_3_1_row_2 d0 d1 d2 d3 j
    | 3 => adj_3_1_row_3 d0 d1 d2 d3 j
    | 4 => adj_3_1_row_4 d0 d1 d2 d3 j
    | 5 => adj_3_1_row_5 d0 d1 d2 d3 j
    | 6 => adj_3_1_row_6 d0 d1 d2 d3 j
    | 7 => adj_3_1_row_7 d0 d1 d2 d3 j
    | 8 => adj_3_1_row_8 d0 d1 d2 d3 j
    | _ => 0
def rows_3_2 (i : Fin 9) : Fin 24 :=
  match i.val with
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 5
  | 5 => 9
  | 6 => 13
  | 7 => 15
  | 8 => 17
  | _ => 0

def cols_3_2 (i : Fin 9) : Fin 10 :=
  match i.val with
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 3
  | 4 => 4
  | 5 => 5
  | 6 => 6
  | 7 => 7
  | 8 => 8
  | _ => 0

def minor_3_2 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  (cMatrix d).submatrix rows_3_2 cols_3_2
def detPoly_3_2 (d : Fin 4 → ℂ) : ℂ := (d 2^3*d 3^4*(d 1^2 + d 3^2)/256 : ℂ)
private def adj_3_2_row_0 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1*d2*d3^2*(d0^2*d1^2 - d0^2*d3^2 - d1^2*d3^2 - d3^4)/256 : ℂ)
  | 1 => (-d2^2*d3^2*(d0^2*d1^2 - d0^2*d3^2 - d1^2*d3^2 - d3^4)/256 : ℂ)
  | 2 => (-d1^2*d2*d3*(d0^2*d1^2 - d0^2*d3^2 - d1^2*d3^2 - d3^4)/256 : ℂ)
  | 3 => (d0*d1*(d0^2*d1^2*d2^2 + d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 - d0^2*d3^4 - d1^2*d2^2*d3^2 - d1^2*d3^4 - 3*d2^2*d3^4 - d3^6)/256 : ℂ)
  | 4 => (d0*d3*(d0^2*d1^4 + d0^2*d1^2*d2^2 - d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 - d1^4*d3^2 - d1^2*d2^2*d3^2 - d1^2*d3^4 + d2^2*d3^4)/256 : ℂ)
  | 5 => (d2^2*(d1^2 + d3^2)*(d0^2*d1^2 - d0^2*d3^2 - d1^2*d3^2 - d3^4)/256 : ℂ)
  | 6 => (d0*d2^3*d3^4/128 : ℂ)
  | 7 => (d1*d2*(d0^2*d1^2*d2^2 + d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 - d0^2*d3^4 - d1^2*d2^2*d3^2 - d1^2*d3^4 - d2^2*d3^4 - d3^6)/256 : ℂ)
  | 8 => (d2*d3*(d0^2*d1^4 + d0^2*d1^2*d2^2 - d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 - d1^4*d3^2 - d1^2*d2^2*d3^2 - d1^2*d3^4 - d2^2*d3^4)/256 : ℂ)
  | _ => 0

private def adj_3_2_row_1 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d0*d1^2*d2*d3^2*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 1 => (-d0*d1*d2^2*d3^2*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 2 => (-d0*d1^3*d2*d3*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 3 => ((d0^2*d1^4*d2^2 + d0^2*d1^4*d3^2 + d0^2*d1^2*d2^2*d3^2 - d0^2*d1^2*d3^4 + 2*d2^2*d3^6)/256 : ℂ)
  | 4 => (d1*d3*(d0^2*d1^4 + d0^2*d1^2*d2^2 - d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 + 2*d2^2*d3^4)/256 : ℂ)
  | 5 => (d0*d1*d2^2*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 6 => (d1*d2^3*d3^4/128 : ℂ)
  | 7 => (d0*d1^2*d2*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 8 => (d0*d1*d2*d3*(d1^4 + d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | _ => 0

private def adj_3_2_row_2 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d0*d1*d2^2*d3^2*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 1 => (-d0*d2^3*d3^2*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 2 => (-d0*d1^2*d2^2*d3*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 3 => (d1*d2*(d0^2*d1^2*d2^2 + d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 - d0^2*d3^4 - 2*d2^2*d3^4)/256 : ℂ)
  | 4 => (d2*d3*(d0^2*d1^4 + d0^2*d1^2*d2^2 - d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 + 2*d2^2*d3^4)/256 : ℂ)
  | 5 => (d0*d2^3*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 6 => (d2^4*d3^4/128 : ℂ)
  | 7 => (d0*d1*d2^2*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 8 => (d0*d2^2*d3*(d1^4 + d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | _ => 0

private def adj_3_2_row_3 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d0*d1*d2*d3^3*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 1 => (-d0*d2^2*d3^3*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 2 => (-d0*d1^2*d2*d3^2*(d1 - d3)*(d1 + d3)/256 : ℂ)
  | 3 => (d1*d3*(d0^2*d1^2*d2^2 + d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 - d0^2*d3^4 - 2*d2^2*d3^4)/256 : ℂ)
  | 4 => (d3^2*(d0^2*d1^4 + d0^2*d1^2*d2^2 - d0^2*d1^2*d3^2 + d0^2*d2^2*d3^2 - 2*d1^2*d2^2*d3^2)/256 : ℂ)
  | 5 => (d0*d2^2*d3*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 6 => (d2^3*d3^5/128 : ℂ)
  | 7 => (d0*d1*d2*d3*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 8 => (d0*d2*d3^2*(d1^4 + d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | _ => 0

private def adj_3_2_row_4 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1*d2*d3^2*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 1 => (-d2^2*d3^2*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 2 => (-d1^2*d2*d3*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 3 => (d0*d1*(d1^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 4 => (d0*d3*(d1^2 + d3^2)*(d1^4 + d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | 5 => (d2^2*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)^2/256 : ℂ)
  | 7 => (d1*d2*(d1^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 + d2^2*d3^2 - d3^4)/256 : ℂ)
  | 8 => (d2*d3*(d1^2 + d3^2)*(d1^4 + d1^2*d2^2 - d1^2*d3^2 + d2^2*d3^2)/256 : ℂ)
  | _ => 0

private def adj_3_2_row_5 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d2^2*d3^2*(d1^2 - 2*d3^2)*(d1^2 + d3^2)/256 : ℂ)
  | 1 => (-d1*d2^3*d3^2*(d1^2 + d3^2)/256 : ℂ)
  | 2 => (-d1*d2^2*d3*(d1^2 - 2*d3^2)*(d1^2 + d3^2)/256 : ℂ)
  | 3 => (d0*d2*(d1^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 4 => (d0*d1*d2*d3*(d1^2 + d3^2)*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | 5 => (d1*d2^3*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 7 => (d2^2*(d1^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 - 2*d3^4)/256 : ℂ)
  | 8 => (d1*d2^2*d3*(d1^2 + d3^2)*(d1^2 + d2^2 - 2*d3^2)/256 : ℂ)
  | _ => 0

private def adj_3_2_row_6 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1^2*d2*d3^3*(d1^2 + d3^2)/256 : ℂ)
  | 1 => (-d1*d2^2*d3^3*(d1^2 + d3^2)/256 : ℂ)
  | 2 => (-d1^3*d2*d3^2*(d1^2 + d3^2)/256 : ℂ)
  | 3 => (d0*d3*(d1^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 + 2*d2^2*d3^2)/256 : ℂ)
  | 4 => (d0*d1*d3^2*(d1^2 + d2^2)*(d1^2 + d3^2)/256 : ℂ)
  | 5 => (d1*d2^2*d3*(d1^2 + d3^2)^2/256 : ℂ)
  | 7 => (d2*d3*(d1^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 + 2*d2^2*d3^2)/256 : ℂ)
  | 8 => (d1*d2*d3^2*(d1^2 + d2^2)*(d1^2 + d3^2)/256 : ℂ)
  | _ => 0

private def adj_3_2_row_7 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1*d2*d3^2*(d1^2 + d3^2)*(d2^2 + d3^2)/256 : ℂ)
  | 1 => (-d2^2*d3^2*(d1^2 + d3^2)*(d2^2 + d3^2)/256 : ℂ)
  | 2 => (-d2*d3*(d1^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 - 2*d2^2*d3^2)/256 : ℂ)
  | 3 => (d0*d1*(d1^2 + d3^2)*(d2^2 + d3^2)^2/256 : ℂ)
  | 4 => (d0*d3*(d1^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 + d2^4 - d2^2*d3^2)/256 : ℂ)
  | 5 => (d2^2*(d1^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 - d2^2*d3^2 + d3^4)/256 : ℂ)
  | 7 => (d1*d2*(d1^2 + d3^2)*(d2^2 + d3^2)^2/256 : ℂ)
  | 8 => (d2*d3*(d1^2 + d3^2)*(d1^2*d2^2 + d1^2*d3^2 + d2^4 - d2^2*d3^2)/256 : ℂ)
  | _ => 0

private def adj_3_2_row_8 (d0 d1 d2 d3 : ℂ) (j : Fin 9) : ℂ :=
  match j.val with
  | 0 => (d1*d2^2*d3^3*(d1^2 + d3^2)/256 : ℂ)
  | 1 => (-d2^3*d3^3*(d1^2 + d3^2)/256 : ℂ)
  | 2 => (-d1^2*d2^2*d3^2*(d1^2 + d3^2)/256 : ℂ)
  | 3 => (d0*d1*d2*d3*(d1^2 + d3^2)*(d2^2 + d3^2)/256 : ℂ)
  | 4 => (d0*d2*d3^2*(d1^2 + d2^2)*(d1^2 + d3^2)/256 : ℂ)
  | 5 => (d2^3*d3*(d1 - d3)*(d1 + d3)*(d1^2 + d3^2)/256 : ℂ)
  | 7 => (d1*d2^2*d3*(d1^2 + d3^2)*(d2^2 + d3^2)/256 : ℂ)
  | 8 => (d2^2*d3^2*(d1^2 + d2^2)*(d1^2 + d3^2)/256 : ℂ)
  | _ => 0

def adj_3_2 (d : Fin 4 → ℂ) : Matrix (Fin 9) (Fin 9) ℂ :=
  let d0 := d 0
  let d1 := d 1
  let d2 := d 2
  let d3 := d 3
  fun i j =>
    match i.val with
    | 0 => adj_3_2_row_0 d0 d1 d2 d3 j
    | 1 => adj_3_2_row_1 d0 d1 d2 d3 j
    | 2 => adj_3_2_row_2 d0 d1 d2 d3 j
    | 3 => adj_3_2_row_3 d0 d1 d2 d3 j
    | 4 => adj_3_2_row_4 d0 d1 d2 d3 j
    | 5 => adj_3_2_row_5 d0 d1 d2 d3 j
    | 6 => adj_3_2_row_6 d0 d1 d2 d3 j
    | 7 => adj_3_2_row_7 d0 d1 d2 d3 j
    | 8 => adj_3_2_row_8 d0 d1 d2 d3 j
    | _ => 0
private theorem minor_0_0_eq_lit (d : Fin 4 → ℂ) :
    minor_0_0 d = (cMatrix d).submatrix rows_0_0 cols_0_0 := by
  rfl

private theorem minor_0_0_scaled_inverse_row_0 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_0_0 d * adj_0_0 d) (0 : Fin 9) j =
      (detPoly_0_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (0 : Fin 9) j := by
  rw [minor_0_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_0_0, cols_0_0, adj_0_0,
      adj_0_0_row_0, adj_0_0_row_1, adj_0_0_row_2, adj_0_0_row_3, adj_0_0_row_4, adj_0_0_row_5, adj_0_0_row_6, adj_0_0_row_7, adj_0_0_row_8, detPoly_0_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_0_0_scaled_inverse_row_1 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_0_0 d * adj_0_0 d) (1 : Fin 9) j =
      (detPoly_0_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (1 : Fin 9) j := by
  rw [minor_0_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_0_0, cols_0_0, adj_0_0,
      adj_0_0_row_0, adj_0_0_row_1, adj_0_0_row_2, adj_0_0_row_3, adj_0_0_row_4, adj_0_0_row_5, adj_0_0_row_6, adj_0_0_row_7, adj_0_0_row_8, detPoly_0_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_0_0_scaled_inverse_row_2 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_0_0 d * adj_0_0 d) (2 : Fin 9) j =
      (detPoly_0_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (2 : Fin 9) j := by
  rw [minor_0_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_0_0, cols_0_0, adj_0_0,
      adj_0_0_row_0, adj_0_0_row_1, adj_0_0_row_2, adj_0_0_row_3, adj_0_0_row_4, adj_0_0_row_5, adj_0_0_row_6, adj_0_0_row_7, adj_0_0_row_8, detPoly_0_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_0_0_scaled_inverse_row_3 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_0_0 d * adj_0_0 d) (3 : Fin 9) j =
      (detPoly_0_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (3 : Fin 9) j := by
  rw [minor_0_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_0_0, cols_0_0, adj_0_0,
      adj_0_0_row_0, adj_0_0_row_1, adj_0_0_row_2, adj_0_0_row_3, adj_0_0_row_4, adj_0_0_row_5, adj_0_0_row_6, adj_0_0_row_7, adj_0_0_row_8, detPoly_0_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_0_0_scaled_inverse_row_4 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_0_0 d * adj_0_0 d) (4 : Fin 9) j =
      (detPoly_0_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (4 : Fin 9) j := by
  rw [minor_0_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_0_0, cols_0_0, adj_0_0,
      adj_0_0_row_0, adj_0_0_row_1, adj_0_0_row_2, adj_0_0_row_3, adj_0_0_row_4, adj_0_0_row_5, adj_0_0_row_6, adj_0_0_row_7, adj_0_0_row_8, detPoly_0_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_0_0_scaled_inverse_row_5 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_0_0 d * adj_0_0 d) (5 : Fin 9) j =
      (detPoly_0_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (5 : Fin 9) j := by
  rw [minor_0_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_0_0, cols_0_0, adj_0_0,
      adj_0_0_row_0, adj_0_0_row_1, adj_0_0_row_2, adj_0_0_row_3, adj_0_0_row_4, adj_0_0_row_5, adj_0_0_row_6, adj_0_0_row_7, adj_0_0_row_8, detPoly_0_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_0_0_scaled_inverse_row_6 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_0_0 d * adj_0_0 d) (6 : Fin 9) j =
      (detPoly_0_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (6 : Fin 9) j := by
  rw [minor_0_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_0_0, cols_0_0, adj_0_0,
      adj_0_0_row_0, adj_0_0_row_1, adj_0_0_row_2, adj_0_0_row_3, adj_0_0_row_4, adj_0_0_row_5, adj_0_0_row_6, adj_0_0_row_7, adj_0_0_row_8, detPoly_0_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_0_0_scaled_inverse_row_7 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_0_0 d * adj_0_0 d) (7 : Fin 9) j =
      (detPoly_0_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (7 : Fin 9) j := by
  rw [minor_0_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_0_0, cols_0_0, adj_0_0,
      adj_0_0_row_0, adj_0_0_row_1, adj_0_0_row_2, adj_0_0_row_3, adj_0_0_row_4, adj_0_0_row_5, adj_0_0_row_6, adj_0_0_row_7, adj_0_0_row_8, detPoly_0_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_0_0_scaled_inverse_row_8 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_0_0 d * adj_0_0 d) (8 : Fin 9) j =
      (detPoly_0_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (8 : Fin 9) j := by
  rw [minor_0_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_0_0, cols_0_0, adj_0_0,
      adj_0_0_row_0, adj_0_0_row_1, adj_0_0_row_2, adj_0_0_row_3, adj_0_0_row_4, adj_0_0_row_5, adj_0_0_row_6, adj_0_0_row_7, adj_0_0_row_8, detPoly_0_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

theorem minor_0_0_scaled_inverse (d : Fin 4 → ℂ) :
    minor_0_0 d * adj_0_0 d =
      detPoly_0_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ) := by
  ext i j
  fin_cases i
  · exact minor_0_0_scaled_inverse_row_0 d j
  · exact minor_0_0_scaled_inverse_row_1 d j
  · exact minor_0_0_scaled_inverse_row_2 d j
  · exact minor_0_0_scaled_inverse_row_3 d j
  · exact minor_0_0_scaled_inverse_row_4 d j
  · exact minor_0_0_scaled_inverse_row_5 d j
  · exact minor_0_0_scaled_inverse_row_6 d j
  · exact minor_0_0_scaled_inverse_row_7 d j
  · exact minor_0_0_scaled_inverse_row_8 d j

private theorem minor_0_1_eq_lit (d : Fin 4 → ℂ) :
    minor_0_1 d = (cMatrix d).submatrix rows_0_1 cols_0_1 := by
  rfl

private theorem minor_0_1_scaled_inverse_row_0 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_0_1 d * adj_0_1 d) (0 : Fin 9) j =
      (detPoly_0_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (0 : Fin 9) j := by
  rw [minor_0_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_0_1, cols_0_1, adj_0_1,
      adj_0_1_row_0, adj_0_1_row_1, adj_0_1_row_2, adj_0_1_row_3, adj_0_1_row_4, adj_0_1_row_5, adj_0_1_row_6, adj_0_1_row_7, adj_0_1_row_8, detPoly_0_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_0_1_scaled_inverse_row_1 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_0_1 d * adj_0_1 d) (1 : Fin 9) j =
      (detPoly_0_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (1 : Fin 9) j := by
  rw [minor_0_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_0_1, cols_0_1, adj_0_1,
      adj_0_1_row_0, adj_0_1_row_1, adj_0_1_row_2, adj_0_1_row_3, adj_0_1_row_4, adj_0_1_row_5, adj_0_1_row_6, adj_0_1_row_7, adj_0_1_row_8, detPoly_0_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_0_1_scaled_inverse_row_2 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_0_1 d * adj_0_1 d) (2 : Fin 9) j =
      (detPoly_0_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (2 : Fin 9) j := by
  rw [minor_0_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_0_1, cols_0_1, adj_0_1,
      adj_0_1_row_0, adj_0_1_row_1, adj_0_1_row_2, adj_0_1_row_3, adj_0_1_row_4, adj_0_1_row_5, adj_0_1_row_6, adj_0_1_row_7, adj_0_1_row_8, detPoly_0_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_0_1_scaled_inverse_row_3 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_0_1 d * adj_0_1 d) (3 : Fin 9) j =
      (detPoly_0_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (3 : Fin 9) j := by
  rw [minor_0_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_0_1, cols_0_1, adj_0_1,
      adj_0_1_row_0, adj_0_1_row_1, adj_0_1_row_2, adj_0_1_row_3, adj_0_1_row_4, adj_0_1_row_5, adj_0_1_row_6, adj_0_1_row_7, adj_0_1_row_8, detPoly_0_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_0_1_scaled_inverse_row_4 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_0_1 d * adj_0_1 d) (4 : Fin 9) j =
      (detPoly_0_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (4 : Fin 9) j := by
  rw [minor_0_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_0_1, cols_0_1, adj_0_1,
      adj_0_1_row_0, adj_0_1_row_1, adj_0_1_row_2, adj_0_1_row_3, adj_0_1_row_4, adj_0_1_row_5, adj_0_1_row_6, adj_0_1_row_7, adj_0_1_row_8, detPoly_0_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_0_1_scaled_inverse_row_5 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_0_1 d * adj_0_1 d) (5 : Fin 9) j =
      (detPoly_0_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (5 : Fin 9) j := by
  rw [minor_0_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_0_1, cols_0_1, adj_0_1,
      adj_0_1_row_0, adj_0_1_row_1, adj_0_1_row_2, adj_0_1_row_3, adj_0_1_row_4, adj_0_1_row_5, adj_0_1_row_6, adj_0_1_row_7, adj_0_1_row_8, detPoly_0_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_0_1_scaled_inverse_row_6 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_0_1 d * adj_0_1 d) (6 : Fin 9) j =
      (detPoly_0_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (6 : Fin 9) j := by
  rw [minor_0_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_0_1, cols_0_1, adj_0_1,
      adj_0_1_row_0, adj_0_1_row_1, adj_0_1_row_2, adj_0_1_row_3, adj_0_1_row_4, adj_0_1_row_5, adj_0_1_row_6, adj_0_1_row_7, adj_0_1_row_8, detPoly_0_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_0_1_scaled_inverse_row_7 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_0_1 d * adj_0_1 d) (7 : Fin 9) j =
      (detPoly_0_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (7 : Fin 9) j := by
  rw [minor_0_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_0_1, cols_0_1, adj_0_1,
      adj_0_1_row_0, adj_0_1_row_1, adj_0_1_row_2, adj_0_1_row_3, adj_0_1_row_4, adj_0_1_row_5, adj_0_1_row_6, adj_0_1_row_7, adj_0_1_row_8, detPoly_0_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_0_1_scaled_inverse_row_8 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_0_1 d * adj_0_1 d) (8 : Fin 9) j =
      (detPoly_0_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (8 : Fin 9) j := by
  rw [minor_0_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_0_1, cols_0_1, adj_0_1,
      adj_0_1_row_0, adj_0_1_row_1, adj_0_1_row_2, adj_0_1_row_3, adj_0_1_row_4, adj_0_1_row_5, adj_0_1_row_6, adj_0_1_row_7, adj_0_1_row_8, detPoly_0_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

theorem minor_0_1_scaled_inverse (d : Fin 4 → ℂ) :
    minor_0_1 d * adj_0_1 d =
      detPoly_0_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ) := by
  ext i j
  fin_cases i
  · exact minor_0_1_scaled_inverse_row_0 d j
  · exact minor_0_1_scaled_inverse_row_1 d j
  · exact minor_0_1_scaled_inverse_row_2 d j
  · exact minor_0_1_scaled_inverse_row_3 d j
  · exact minor_0_1_scaled_inverse_row_4 d j
  · exact minor_0_1_scaled_inverse_row_5 d j
  · exact minor_0_1_scaled_inverse_row_6 d j
  · exact minor_0_1_scaled_inverse_row_7 d j
  · exact minor_0_1_scaled_inverse_row_8 d j

private theorem minor_1_0_eq_lit (d : Fin 4 → ℂ) :
    minor_1_0 d = (cMatrix d).submatrix rows_1_0 cols_1_0 := by
  rfl

private theorem minor_1_0_scaled_inverse_row_0 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_0 d * adj_1_0 d) (0 : Fin 9) j =
      (detPoly_1_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (0 : Fin 9) j := by
  rw [minor_1_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_0, cols_1_0, adj_1_0,
      adj_1_0_row_0, adj_1_0_row_1, adj_1_0_row_2, adj_1_0_row_3, adj_1_0_row_4, adj_1_0_row_5, adj_1_0_row_6, adj_1_0_row_7, adj_1_0_row_8, detPoly_1_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_0_scaled_inverse_row_1 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_0 d * adj_1_0 d) (1 : Fin 9) j =
      (detPoly_1_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (1 : Fin 9) j := by
  rw [minor_1_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_0, cols_1_0, adj_1_0,
      adj_1_0_row_0, adj_1_0_row_1, adj_1_0_row_2, adj_1_0_row_3, adj_1_0_row_4, adj_1_0_row_5, adj_1_0_row_6, adj_1_0_row_7, adj_1_0_row_8, detPoly_1_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_0_scaled_inverse_row_2 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_0 d * adj_1_0 d) (2 : Fin 9) j =
      (detPoly_1_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (2 : Fin 9) j := by
  rw [minor_1_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_0, cols_1_0, adj_1_0,
      adj_1_0_row_0, adj_1_0_row_1, adj_1_0_row_2, adj_1_0_row_3, adj_1_0_row_4, adj_1_0_row_5, adj_1_0_row_6, adj_1_0_row_7, adj_1_0_row_8, detPoly_1_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_0_scaled_inverse_row_3 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_0 d * adj_1_0 d) (3 : Fin 9) j =
      (detPoly_1_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (3 : Fin 9) j := by
  rw [minor_1_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_0, cols_1_0, adj_1_0,
      adj_1_0_row_0, adj_1_0_row_1, adj_1_0_row_2, adj_1_0_row_3, adj_1_0_row_4, adj_1_0_row_5, adj_1_0_row_6, adj_1_0_row_7, adj_1_0_row_8, detPoly_1_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_0_scaled_inverse_row_4 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_0 d * adj_1_0 d) (4 : Fin 9) j =
      (detPoly_1_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (4 : Fin 9) j := by
  rw [minor_1_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_0, cols_1_0, adj_1_0,
      adj_1_0_row_0, adj_1_0_row_1, adj_1_0_row_2, adj_1_0_row_3, adj_1_0_row_4, adj_1_0_row_5, adj_1_0_row_6, adj_1_0_row_7, adj_1_0_row_8, detPoly_1_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_0_scaled_inverse_row_5 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_0 d * adj_1_0 d) (5 : Fin 9) j =
      (detPoly_1_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (5 : Fin 9) j := by
  rw [minor_1_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_0, cols_1_0, adj_1_0,
      adj_1_0_row_0, adj_1_0_row_1, adj_1_0_row_2, adj_1_0_row_3, adj_1_0_row_4, adj_1_0_row_5, adj_1_0_row_6, adj_1_0_row_7, adj_1_0_row_8, detPoly_1_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_0_scaled_inverse_row_6 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_0 d * adj_1_0 d) (6 : Fin 9) j =
      (detPoly_1_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (6 : Fin 9) j := by
  rw [minor_1_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_0, cols_1_0, adj_1_0,
      adj_1_0_row_0, adj_1_0_row_1, adj_1_0_row_2, adj_1_0_row_3, adj_1_0_row_4, adj_1_0_row_5, adj_1_0_row_6, adj_1_0_row_7, adj_1_0_row_8, detPoly_1_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_0_scaled_inverse_row_7 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_0 d * adj_1_0 d) (7 : Fin 9) j =
      (detPoly_1_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (7 : Fin 9) j := by
  rw [minor_1_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_0, cols_1_0, adj_1_0,
      adj_1_0_row_0, adj_1_0_row_1, adj_1_0_row_2, adj_1_0_row_3, adj_1_0_row_4, adj_1_0_row_5, adj_1_0_row_6, adj_1_0_row_7, adj_1_0_row_8, detPoly_1_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_0_scaled_inverse_row_8 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_0 d * adj_1_0 d) (8 : Fin 9) j =
      (detPoly_1_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (8 : Fin 9) j := by
  rw [minor_1_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_0, cols_1_0, adj_1_0,
      adj_1_0_row_0, adj_1_0_row_1, adj_1_0_row_2, adj_1_0_row_3, adj_1_0_row_4, adj_1_0_row_5, adj_1_0_row_6, adj_1_0_row_7, adj_1_0_row_8, detPoly_1_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

theorem minor_1_0_scaled_inverse (d : Fin 4 → ℂ) :
    minor_1_0 d * adj_1_0 d =
      detPoly_1_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ) := by
  ext i j
  fin_cases i
  · exact minor_1_0_scaled_inverse_row_0 d j
  · exact minor_1_0_scaled_inverse_row_1 d j
  · exact minor_1_0_scaled_inverse_row_2 d j
  · exact minor_1_0_scaled_inverse_row_3 d j
  · exact minor_1_0_scaled_inverse_row_4 d j
  · exact minor_1_0_scaled_inverse_row_5 d j
  · exact minor_1_0_scaled_inverse_row_6 d j
  · exact minor_1_0_scaled_inverse_row_7 d j
  · exact minor_1_0_scaled_inverse_row_8 d j

private theorem minor_1_1_eq_lit (d : Fin 4 → ℂ) :
    minor_1_1 d = (cMatrix d).submatrix rows_1_1 cols_1_1 := by
  rfl

private theorem minor_1_1_scaled_inverse_row_0 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_1 d * adj_1_1 d) (0 : Fin 9) j =
      (detPoly_1_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (0 : Fin 9) j := by
  rw [minor_1_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_1, cols_1_1, adj_1_1,
      adj_1_1_row_0, adj_1_1_row_1, adj_1_1_row_2, adj_1_1_row_3, adj_1_1_row_4, adj_1_1_row_5, adj_1_1_row_6, adj_1_1_row_7, adj_1_1_row_8, detPoly_1_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_1_scaled_inverse_row_1 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_1 d * adj_1_1 d) (1 : Fin 9) j =
      (detPoly_1_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (1 : Fin 9) j := by
  rw [minor_1_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_1, cols_1_1, adj_1_1,
      adj_1_1_row_0, adj_1_1_row_1, adj_1_1_row_2, adj_1_1_row_3, adj_1_1_row_4, adj_1_1_row_5, adj_1_1_row_6, adj_1_1_row_7, adj_1_1_row_8, detPoly_1_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_1_scaled_inverse_row_2 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_1 d * adj_1_1 d) (2 : Fin 9) j =
      (detPoly_1_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (2 : Fin 9) j := by
  rw [minor_1_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_1, cols_1_1, adj_1_1,
      adj_1_1_row_0, adj_1_1_row_1, adj_1_1_row_2, adj_1_1_row_3, adj_1_1_row_4, adj_1_1_row_5, adj_1_1_row_6, adj_1_1_row_7, adj_1_1_row_8, detPoly_1_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_1_scaled_inverse_row_3 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_1 d * adj_1_1 d) (3 : Fin 9) j =
      (detPoly_1_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (3 : Fin 9) j := by
  rw [minor_1_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_1, cols_1_1, adj_1_1,
      adj_1_1_row_0, adj_1_1_row_1, adj_1_1_row_2, adj_1_1_row_3, adj_1_1_row_4, adj_1_1_row_5, adj_1_1_row_6, adj_1_1_row_7, adj_1_1_row_8, detPoly_1_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_1_scaled_inverse_row_4 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_1 d * adj_1_1 d) (4 : Fin 9) j =
      (detPoly_1_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (4 : Fin 9) j := by
  rw [minor_1_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_1, cols_1_1, adj_1_1,
      adj_1_1_row_0, adj_1_1_row_1, adj_1_1_row_2, adj_1_1_row_3, adj_1_1_row_4, adj_1_1_row_5, adj_1_1_row_6, adj_1_1_row_7, adj_1_1_row_8, detPoly_1_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_1_scaled_inverse_row_5 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_1 d * adj_1_1 d) (5 : Fin 9) j =
      (detPoly_1_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (5 : Fin 9) j := by
  rw [minor_1_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_1, cols_1_1, adj_1_1,
      adj_1_1_row_0, adj_1_1_row_1, adj_1_1_row_2, adj_1_1_row_3, adj_1_1_row_4, adj_1_1_row_5, adj_1_1_row_6, adj_1_1_row_7, adj_1_1_row_8, detPoly_1_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_1_scaled_inverse_row_6 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_1 d * adj_1_1 d) (6 : Fin 9) j =
      (detPoly_1_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (6 : Fin 9) j := by
  rw [minor_1_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_1, cols_1_1, adj_1_1,
      adj_1_1_row_0, adj_1_1_row_1, adj_1_1_row_2, adj_1_1_row_3, adj_1_1_row_4, adj_1_1_row_5, adj_1_1_row_6, adj_1_1_row_7, adj_1_1_row_8, detPoly_1_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_1_scaled_inverse_row_7 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_1 d * adj_1_1 d) (7 : Fin 9) j =
      (detPoly_1_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (7 : Fin 9) j := by
  rw [minor_1_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_1, cols_1_1, adj_1_1,
      adj_1_1_row_0, adj_1_1_row_1, adj_1_1_row_2, adj_1_1_row_3, adj_1_1_row_4, adj_1_1_row_5, adj_1_1_row_6, adj_1_1_row_7, adj_1_1_row_8, detPoly_1_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_1_scaled_inverse_row_8 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_1 d * adj_1_1 d) (8 : Fin 9) j =
      (detPoly_1_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (8 : Fin 9) j := by
  rw [minor_1_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_1, cols_1_1, adj_1_1,
      adj_1_1_row_0, adj_1_1_row_1, adj_1_1_row_2, adj_1_1_row_3, adj_1_1_row_4, adj_1_1_row_5, adj_1_1_row_6, adj_1_1_row_7, adj_1_1_row_8, detPoly_1_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

theorem minor_1_1_scaled_inverse (d : Fin 4 → ℂ) :
    minor_1_1 d * adj_1_1 d =
      detPoly_1_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ) := by
  ext i j
  fin_cases i
  · exact minor_1_1_scaled_inverse_row_0 d j
  · exact minor_1_1_scaled_inverse_row_1 d j
  · exact minor_1_1_scaled_inverse_row_2 d j
  · exact minor_1_1_scaled_inverse_row_3 d j
  · exact minor_1_1_scaled_inverse_row_4 d j
  · exact minor_1_1_scaled_inverse_row_5 d j
  · exact minor_1_1_scaled_inverse_row_6 d j
  · exact minor_1_1_scaled_inverse_row_7 d j
  · exact minor_1_1_scaled_inverse_row_8 d j

private theorem minor_1_2_eq_lit (d : Fin 4 → ℂ) :
    minor_1_2 d = (cMatrix d).submatrix rows_1_2 cols_1_2 := by
  rfl

private theorem minor_1_2_scaled_inverse_row_0 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_2 d * adj_1_2 d) (0 : Fin 9) j =
      (detPoly_1_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (0 : Fin 9) j := by
  rw [minor_1_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_2, cols_1_2, adj_1_2,
      adj_1_2_row_0, adj_1_2_row_1, adj_1_2_row_2, adj_1_2_row_3, adj_1_2_row_4, adj_1_2_row_5, adj_1_2_row_6, adj_1_2_row_7, adj_1_2_row_8, detPoly_1_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_2_scaled_inverse_row_1 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_2 d * adj_1_2 d) (1 : Fin 9) j =
      (detPoly_1_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (1 : Fin 9) j := by
  rw [minor_1_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_2, cols_1_2, adj_1_2,
      adj_1_2_row_0, adj_1_2_row_1, adj_1_2_row_2, adj_1_2_row_3, adj_1_2_row_4, adj_1_2_row_5, adj_1_2_row_6, adj_1_2_row_7, adj_1_2_row_8, detPoly_1_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_2_scaled_inverse_row_2 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_2 d * adj_1_2 d) (2 : Fin 9) j =
      (detPoly_1_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (2 : Fin 9) j := by
  rw [minor_1_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_2, cols_1_2, adj_1_2,
      adj_1_2_row_0, adj_1_2_row_1, adj_1_2_row_2, adj_1_2_row_3, adj_1_2_row_4, adj_1_2_row_5, adj_1_2_row_6, adj_1_2_row_7, adj_1_2_row_8, detPoly_1_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_2_scaled_inverse_row_3 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_2 d * adj_1_2 d) (3 : Fin 9) j =
      (detPoly_1_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (3 : Fin 9) j := by
  rw [minor_1_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_2, cols_1_2, adj_1_2,
      adj_1_2_row_0, adj_1_2_row_1, adj_1_2_row_2, adj_1_2_row_3, adj_1_2_row_4, adj_1_2_row_5, adj_1_2_row_6, adj_1_2_row_7, adj_1_2_row_8, detPoly_1_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_2_scaled_inverse_row_4 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_2 d * adj_1_2 d) (4 : Fin 9) j =
      (detPoly_1_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (4 : Fin 9) j := by
  rw [minor_1_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_2, cols_1_2, adj_1_2,
      adj_1_2_row_0, adj_1_2_row_1, adj_1_2_row_2, adj_1_2_row_3, adj_1_2_row_4, adj_1_2_row_5, adj_1_2_row_6, adj_1_2_row_7, adj_1_2_row_8, detPoly_1_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_2_scaled_inverse_row_5 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_2 d * adj_1_2 d) (5 : Fin 9) j =
      (detPoly_1_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (5 : Fin 9) j := by
  rw [minor_1_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_2, cols_1_2, adj_1_2,
      adj_1_2_row_0, adj_1_2_row_1, adj_1_2_row_2, adj_1_2_row_3, adj_1_2_row_4, adj_1_2_row_5, adj_1_2_row_6, adj_1_2_row_7, adj_1_2_row_8, detPoly_1_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_2_scaled_inverse_row_6 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_2 d * adj_1_2 d) (6 : Fin 9) j =
      (detPoly_1_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (6 : Fin 9) j := by
  rw [minor_1_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_2, cols_1_2, adj_1_2,
      adj_1_2_row_0, adj_1_2_row_1, adj_1_2_row_2, adj_1_2_row_3, adj_1_2_row_4, adj_1_2_row_5, adj_1_2_row_6, adj_1_2_row_7, adj_1_2_row_8, detPoly_1_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_2_scaled_inverse_row_7 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_2 d * adj_1_2 d) (7 : Fin 9) j =
      (detPoly_1_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (7 : Fin 9) j := by
  rw [minor_1_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_2, cols_1_2, adj_1_2,
      adj_1_2_row_0, adj_1_2_row_1, adj_1_2_row_2, adj_1_2_row_3, adj_1_2_row_4, adj_1_2_row_5, adj_1_2_row_6, adj_1_2_row_7, adj_1_2_row_8, detPoly_1_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_1_2_scaled_inverse_row_8 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_1_2 d * adj_1_2 d) (8 : Fin 9) j =
      (detPoly_1_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (8 : Fin 9) j := by
  rw [minor_1_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_1_2, cols_1_2, adj_1_2,
      adj_1_2_row_0, adj_1_2_row_1, adj_1_2_row_2, adj_1_2_row_3, adj_1_2_row_4, adj_1_2_row_5, adj_1_2_row_6, adj_1_2_row_7, adj_1_2_row_8, detPoly_1_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

theorem minor_1_2_scaled_inverse (d : Fin 4 → ℂ) :
    minor_1_2 d * adj_1_2 d =
      detPoly_1_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ) := by
  ext i j
  fin_cases i
  · exact minor_1_2_scaled_inverse_row_0 d j
  · exact minor_1_2_scaled_inverse_row_1 d j
  · exact minor_1_2_scaled_inverse_row_2 d j
  · exact minor_1_2_scaled_inverse_row_3 d j
  · exact minor_1_2_scaled_inverse_row_4 d j
  · exact minor_1_2_scaled_inverse_row_5 d j
  · exact minor_1_2_scaled_inverse_row_6 d j
  · exact minor_1_2_scaled_inverse_row_7 d j
  · exact minor_1_2_scaled_inverse_row_8 d j

private theorem minor_2_0_eq_lit (d : Fin 4 → ℂ) :
    minor_2_0 d = (cMatrix d).submatrix rows_2_0 cols_2_0 := by
  rfl

private theorem minor_2_0_scaled_inverse_row_0 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_0 d * adj_2_0 d) (0 : Fin 9) j =
      (detPoly_2_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (0 : Fin 9) j := by
  rw [minor_2_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_0, cols_2_0, adj_2_0,
      adj_2_0_row_0, adj_2_0_row_1, adj_2_0_row_2, adj_2_0_row_3, adj_2_0_row_4, adj_2_0_row_5, adj_2_0_row_6, adj_2_0_row_7, adj_2_0_row_8, detPoly_2_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_0_scaled_inverse_row_1 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_0 d * adj_2_0 d) (1 : Fin 9) j =
      (detPoly_2_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (1 : Fin 9) j := by
  rw [minor_2_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_0, cols_2_0, adj_2_0,
      adj_2_0_row_0, adj_2_0_row_1, adj_2_0_row_2, adj_2_0_row_3, adj_2_0_row_4, adj_2_0_row_5, adj_2_0_row_6, adj_2_0_row_7, adj_2_0_row_8, detPoly_2_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_0_scaled_inverse_row_2 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_0 d * adj_2_0 d) (2 : Fin 9) j =
      (detPoly_2_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (2 : Fin 9) j := by
  rw [minor_2_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_0, cols_2_0, adj_2_0,
      adj_2_0_row_0, adj_2_0_row_1, adj_2_0_row_2, adj_2_0_row_3, adj_2_0_row_4, adj_2_0_row_5, adj_2_0_row_6, adj_2_0_row_7, adj_2_0_row_8, detPoly_2_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_0_scaled_inverse_row_3 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_0 d * adj_2_0 d) (3 : Fin 9) j =
      (detPoly_2_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (3 : Fin 9) j := by
  rw [minor_2_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_0, cols_2_0, adj_2_0,
      adj_2_0_row_0, adj_2_0_row_1, adj_2_0_row_2, adj_2_0_row_3, adj_2_0_row_4, adj_2_0_row_5, adj_2_0_row_6, adj_2_0_row_7, adj_2_0_row_8, detPoly_2_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_0_scaled_inverse_row_4 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_0 d * adj_2_0 d) (4 : Fin 9) j =
      (detPoly_2_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (4 : Fin 9) j := by
  rw [minor_2_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_0, cols_2_0, adj_2_0,
      adj_2_0_row_0, adj_2_0_row_1, adj_2_0_row_2, adj_2_0_row_3, adj_2_0_row_4, adj_2_0_row_5, adj_2_0_row_6, adj_2_0_row_7, adj_2_0_row_8, detPoly_2_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_0_scaled_inverse_row_5 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_0 d * adj_2_0 d) (5 : Fin 9) j =
      (detPoly_2_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (5 : Fin 9) j := by
  rw [minor_2_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_0, cols_2_0, adj_2_0,
      adj_2_0_row_0, adj_2_0_row_1, adj_2_0_row_2, adj_2_0_row_3, adj_2_0_row_4, adj_2_0_row_5, adj_2_0_row_6, adj_2_0_row_7, adj_2_0_row_8, detPoly_2_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_0_scaled_inverse_row_6 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_0 d * adj_2_0 d) (6 : Fin 9) j =
      (detPoly_2_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (6 : Fin 9) j := by
  rw [minor_2_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_0, cols_2_0, adj_2_0,
      adj_2_0_row_0, adj_2_0_row_1, adj_2_0_row_2, adj_2_0_row_3, adj_2_0_row_4, adj_2_0_row_5, adj_2_0_row_6, adj_2_0_row_7, adj_2_0_row_8, detPoly_2_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_0_scaled_inverse_row_7 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_0 d * adj_2_0 d) (7 : Fin 9) j =
      (detPoly_2_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (7 : Fin 9) j := by
  rw [minor_2_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_0, cols_2_0, adj_2_0,
      adj_2_0_row_0, adj_2_0_row_1, adj_2_0_row_2, adj_2_0_row_3, adj_2_0_row_4, adj_2_0_row_5, adj_2_0_row_6, adj_2_0_row_7, adj_2_0_row_8, detPoly_2_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_0_scaled_inverse_row_8 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_0 d * adj_2_0 d) (8 : Fin 9) j =
      (detPoly_2_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (8 : Fin 9) j := by
  rw [minor_2_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_0, cols_2_0, adj_2_0,
      adj_2_0_row_0, adj_2_0_row_1, adj_2_0_row_2, adj_2_0_row_3, adj_2_0_row_4, adj_2_0_row_5, adj_2_0_row_6, adj_2_0_row_7, adj_2_0_row_8, detPoly_2_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

theorem minor_2_0_scaled_inverse (d : Fin 4 → ℂ) :
    minor_2_0 d * adj_2_0 d =
      detPoly_2_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ) := by
  ext i j
  fin_cases i
  · exact minor_2_0_scaled_inverse_row_0 d j
  · exact minor_2_0_scaled_inverse_row_1 d j
  · exact minor_2_0_scaled_inverse_row_2 d j
  · exact minor_2_0_scaled_inverse_row_3 d j
  · exact minor_2_0_scaled_inverse_row_4 d j
  · exact minor_2_0_scaled_inverse_row_5 d j
  · exact minor_2_0_scaled_inverse_row_6 d j
  · exact minor_2_0_scaled_inverse_row_7 d j
  · exact minor_2_0_scaled_inverse_row_8 d j

private theorem minor_2_1_eq_lit (d : Fin 4 → ℂ) :
    minor_2_1 d = (cMatrix d).submatrix rows_2_1 cols_2_1 := by
  rfl

private theorem minor_2_1_scaled_inverse_row_0 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_1 d * adj_2_1 d) (0 : Fin 9) j =
      (detPoly_2_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (0 : Fin 9) j := by
  rw [minor_2_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_1, cols_2_1, adj_2_1,
      adj_2_1_row_0, adj_2_1_row_1, adj_2_1_row_2, adj_2_1_row_3, adj_2_1_row_4, adj_2_1_row_5, adj_2_1_row_6, adj_2_1_row_7, adj_2_1_row_8, detPoly_2_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_1_scaled_inverse_row_1 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_1 d * adj_2_1 d) (1 : Fin 9) j =
      (detPoly_2_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (1 : Fin 9) j := by
  rw [minor_2_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_1, cols_2_1, adj_2_1,
      adj_2_1_row_0, adj_2_1_row_1, adj_2_1_row_2, adj_2_1_row_3, adj_2_1_row_4, adj_2_1_row_5, adj_2_1_row_6, adj_2_1_row_7, adj_2_1_row_8, detPoly_2_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_1_scaled_inverse_row_2 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_1 d * adj_2_1 d) (2 : Fin 9) j =
      (detPoly_2_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (2 : Fin 9) j := by
  rw [minor_2_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_1, cols_2_1, adj_2_1,
      adj_2_1_row_0, adj_2_1_row_1, adj_2_1_row_2, adj_2_1_row_3, adj_2_1_row_4, adj_2_1_row_5, adj_2_1_row_6, adj_2_1_row_7, adj_2_1_row_8, detPoly_2_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_1_scaled_inverse_row_3 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_1 d * adj_2_1 d) (3 : Fin 9) j =
      (detPoly_2_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (3 : Fin 9) j := by
  rw [minor_2_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_1, cols_2_1, adj_2_1,
      adj_2_1_row_0, adj_2_1_row_1, adj_2_1_row_2, adj_2_1_row_3, adj_2_1_row_4, adj_2_1_row_5, adj_2_1_row_6, adj_2_1_row_7, adj_2_1_row_8, detPoly_2_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_1_scaled_inverse_row_4 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_1 d * adj_2_1 d) (4 : Fin 9) j =
      (detPoly_2_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (4 : Fin 9) j := by
  rw [minor_2_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_1, cols_2_1, adj_2_1,
      adj_2_1_row_0, adj_2_1_row_1, adj_2_1_row_2, adj_2_1_row_3, adj_2_1_row_4, adj_2_1_row_5, adj_2_1_row_6, adj_2_1_row_7, adj_2_1_row_8, detPoly_2_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_1_scaled_inverse_row_5 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_1 d * adj_2_1 d) (5 : Fin 9) j =
      (detPoly_2_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (5 : Fin 9) j := by
  rw [minor_2_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_1, cols_2_1, adj_2_1,
      adj_2_1_row_0, adj_2_1_row_1, adj_2_1_row_2, adj_2_1_row_3, adj_2_1_row_4, adj_2_1_row_5, adj_2_1_row_6, adj_2_1_row_7, adj_2_1_row_8, detPoly_2_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_1_scaled_inverse_row_6 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_1 d * adj_2_1 d) (6 : Fin 9) j =
      (detPoly_2_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (6 : Fin 9) j := by
  rw [minor_2_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_1, cols_2_1, adj_2_1,
      adj_2_1_row_0, adj_2_1_row_1, adj_2_1_row_2, adj_2_1_row_3, adj_2_1_row_4, adj_2_1_row_5, adj_2_1_row_6, adj_2_1_row_7, adj_2_1_row_8, detPoly_2_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_1_scaled_inverse_row_7 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_1 d * adj_2_1 d) (7 : Fin 9) j =
      (detPoly_2_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (7 : Fin 9) j := by
  rw [minor_2_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_1, cols_2_1, adj_2_1,
      adj_2_1_row_0, adj_2_1_row_1, adj_2_1_row_2, adj_2_1_row_3, adj_2_1_row_4, adj_2_1_row_5, adj_2_1_row_6, adj_2_1_row_7, adj_2_1_row_8, detPoly_2_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_1_scaled_inverse_row_8 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_1 d * adj_2_1 d) (8 : Fin 9) j =
      (detPoly_2_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (8 : Fin 9) j := by
  rw [minor_2_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_1, cols_2_1, adj_2_1,
      adj_2_1_row_0, adj_2_1_row_1, adj_2_1_row_2, adj_2_1_row_3, adj_2_1_row_4, adj_2_1_row_5, adj_2_1_row_6, adj_2_1_row_7, adj_2_1_row_8, detPoly_2_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

theorem minor_2_1_scaled_inverse (d : Fin 4 → ℂ) :
    minor_2_1 d * adj_2_1 d =
      detPoly_2_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ) := by
  ext i j
  fin_cases i
  · exact minor_2_1_scaled_inverse_row_0 d j
  · exact minor_2_1_scaled_inverse_row_1 d j
  · exact minor_2_1_scaled_inverse_row_2 d j
  · exact minor_2_1_scaled_inverse_row_3 d j
  · exact minor_2_1_scaled_inverse_row_4 d j
  · exact minor_2_1_scaled_inverse_row_5 d j
  · exact minor_2_1_scaled_inverse_row_6 d j
  · exact minor_2_1_scaled_inverse_row_7 d j
  · exact minor_2_1_scaled_inverse_row_8 d j

private theorem minor_2_2_eq_lit (d : Fin 4 → ℂ) :
    minor_2_2 d = (cMatrix d).submatrix rows_2_2 cols_2_2 := by
  rfl

private theorem minor_2_2_scaled_inverse_row_0 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_2 d * adj_2_2 d) (0 : Fin 9) j =
      (detPoly_2_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (0 : Fin 9) j := by
  rw [minor_2_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_2, cols_2_2, adj_2_2,
      adj_2_2_row_0, adj_2_2_row_1, adj_2_2_row_2, adj_2_2_row_3, adj_2_2_row_4, adj_2_2_row_5, adj_2_2_row_6, adj_2_2_row_7, adj_2_2_row_8, detPoly_2_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_2_scaled_inverse_row_1 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_2 d * adj_2_2 d) (1 : Fin 9) j =
      (detPoly_2_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (1 : Fin 9) j := by
  rw [minor_2_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_2, cols_2_2, adj_2_2,
      adj_2_2_row_0, adj_2_2_row_1, adj_2_2_row_2, adj_2_2_row_3, adj_2_2_row_4, adj_2_2_row_5, adj_2_2_row_6, adj_2_2_row_7, adj_2_2_row_8, detPoly_2_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_2_scaled_inverse_row_2 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_2 d * adj_2_2 d) (2 : Fin 9) j =
      (detPoly_2_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (2 : Fin 9) j := by
  rw [minor_2_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_2, cols_2_2, adj_2_2,
      adj_2_2_row_0, adj_2_2_row_1, adj_2_2_row_2, adj_2_2_row_3, adj_2_2_row_4, adj_2_2_row_5, adj_2_2_row_6, adj_2_2_row_7, adj_2_2_row_8, detPoly_2_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_2_scaled_inverse_row_3 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_2 d * adj_2_2 d) (3 : Fin 9) j =
      (detPoly_2_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (3 : Fin 9) j := by
  rw [minor_2_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_2, cols_2_2, adj_2_2,
      adj_2_2_row_0, adj_2_2_row_1, adj_2_2_row_2, adj_2_2_row_3, adj_2_2_row_4, adj_2_2_row_5, adj_2_2_row_6, adj_2_2_row_7, adj_2_2_row_8, detPoly_2_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_2_scaled_inverse_row_4 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_2 d * adj_2_2 d) (4 : Fin 9) j =
      (detPoly_2_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (4 : Fin 9) j := by
  rw [minor_2_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_2, cols_2_2, adj_2_2,
      adj_2_2_row_0, adj_2_2_row_1, adj_2_2_row_2, adj_2_2_row_3, adj_2_2_row_4, adj_2_2_row_5, adj_2_2_row_6, adj_2_2_row_7, adj_2_2_row_8, detPoly_2_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_2_scaled_inverse_row_5 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_2 d * adj_2_2 d) (5 : Fin 9) j =
      (detPoly_2_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (5 : Fin 9) j := by
  rw [minor_2_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_2, cols_2_2, adj_2_2,
      adj_2_2_row_0, adj_2_2_row_1, adj_2_2_row_2, adj_2_2_row_3, adj_2_2_row_4, adj_2_2_row_5, adj_2_2_row_6, adj_2_2_row_7, adj_2_2_row_8, detPoly_2_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_2_scaled_inverse_row_6 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_2 d * adj_2_2 d) (6 : Fin 9) j =
      (detPoly_2_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (6 : Fin 9) j := by
  rw [minor_2_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_2, cols_2_2, adj_2_2,
      adj_2_2_row_0, adj_2_2_row_1, adj_2_2_row_2, adj_2_2_row_3, adj_2_2_row_4, adj_2_2_row_5, adj_2_2_row_6, adj_2_2_row_7, adj_2_2_row_8, detPoly_2_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_2_scaled_inverse_row_7 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_2 d * adj_2_2 d) (7 : Fin 9) j =
      (detPoly_2_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (7 : Fin 9) j := by
  rw [minor_2_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_2, cols_2_2, adj_2_2,
      adj_2_2_row_0, adj_2_2_row_1, adj_2_2_row_2, adj_2_2_row_3, adj_2_2_row_4, adj_2_2_row_5, adj_2_2_row_6, adj_2_2_row_7, adj_2_2_row_8, detPoly_2_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_2_2_scaled_inverse_row_8 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_2_2 d * adj_2_2 d) (8 : Fin 9) j =
      (detPoly_2_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (8 : Fin 9) j := by
  rw [minor_2_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_2_2, cols_2_2, adj_2_2,
      adj_2_2_row_0, adj_2_2_row_1, adj_2_2_row_2, adj_2_2_row_3, adj_2_2_row_4, adj_2_2_row_5, adj_2_2_row_6, adj_2_2_row_7, adj_2_2_row_8, detPoly_2_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

theorem minor_2_2_scaled_inverse (d : Fin 4 → ℂ) :
    minor_2_2 d * adj_2_2 d =
      detPoly_2_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ) := by
  ext i j
  fin_cases i
  · exact minor_2_2_scaled_inverse_row_0 d j
  · exact minor_2_2_scaled_inverse_row_1 d j
  · exact minor_2_2_scaled_inverse_row_2 d j
  · exact minor_2_2_scaled_inverse_row_3 d j
  · exact minor_2_2_scaled_inverse_row_4 d j
  · exact minor_2_2_scaled_inverse_row_5 d j
  · exact minor_2_2_scaled_inverse_row_6 d j
  · exact minor_2_2_scaled_inverse_row_7 d j
  · exact minor_2_2_scaled_inverse_row_8 d j

private theorem minor_3_0_eq_lit (d : Fin 4 → ℂ) :
    minor_3_0 d = (cMatrix d).submatrix rows_3_0 cols_3_0 := by
  rfl

private theorem minor_3_0_scaled_inverse_row_0 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_0 d * adj_3_0 d) (0 : Fin 9) j =
      (detPoly_3_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (0 : Fin 9) j := by
  rw [minor_3_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_0, cols_3_0, adj_3_0,
      adj_3_0_row_0, adj_3_0_row_1, adj_3_0_row_2, adj_3_0_row_3, adj_3_0_row_4, adj_3_0_row_5, adj_3_0_row_6, adj_3_0_row_7, adj_3_0_row_8, detPoly_3_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_0_scaled_inverse_row_1 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_0 d * adj_3_0 d) (1 : Fin 9) j =
      (detPoly_3_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (1 : Fin 9) j := by
  rw [minor_3_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_0, cols_3_0, adj_3_0,
      adj_3_0_row_0, adj_3_0_row_1, adj_3_0_row_2, adj_3_0_row_3, adj_3_0_row_4, adj_3_0_row_5, adj_3_0_row_6, adj_3_0_row_7, adj_3_0_row_8, detPoly_3_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_0_scaled_inverse_row_2 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_0 d * adj_3_0 d) (2 : Fin 9) j =
      (detPoly_3_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (2 : Fin 9) j := by
  rw [minor_3_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_0, cols_3_0, adj_3_0,
      adj_3_0_row_0, adj_3_0_row_1, adj_3_0_row_2, adj_3_0_row_3, adj_3_0_row_4, adj_3_0_row_5, adj_3_0_row_6, adj_3_0_row_7, adj_3_0_row_8, detPoly_3_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_0_scaled_inverse_row_3 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_0 d * adj_3_0 d) (3 : Fin 9) j =
      (detPoly_3_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (3 : Fin 9) j := by
  rw [minor_3_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_0, cols_3_0, adj_3_0,
      adj_3_0_row_0, adj_3_0_row_1, adj_3_0_row_2, adj_3_0_row_3, adj_3_0_row_4, adj_3_0_row_5, adj_3_0_row_6, adj_3_0_row_7, adj_3_0_row_8, detPoly_3_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_0_scaled_inverse_row_4 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_0 d * adj_3_0 d) (4 : Fin 9) j =
      (detPoly_3_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (4 : Fin 9) j := by
  rw [minor_3_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_0, cols_3_0, adj_3_0,
      adj_3_0_row_0, adj_3_0_row_1, adj_3_0_row_2, adj_3_0_row_3, adj_3_0_row_4, adj_3_0_row_5, adj_3_0_row_6, adj_3_0_row_7, adj_3_0_row_8, detPoly_3_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_0_scaled_inverse_row_5 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_0 d * adj_3_0 d) (5 : Fin 9) j =
      (detPoly_3_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (5 : Fin 9) j := by
  rw [minor_3_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_0, cols_3_0, adj_3_0,
      adj_3_0_row_0, adj_3_0_row_1, adj_3_0_row_2, adj_3_0_row_3, adj_3_0_row_4, adj_3_0_row_5, adj_3_0_row_6, adj_3_0_row_7, adj_3_0_row_8, detPoly_3_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_0_scaled_inverse_row_6 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_0 d * adj_3_0 d) (6 : Fin 9) j =
      (detPoly_3_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (6 : Fin 9) j := by
  rw [minor_3_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_0, cols_3_0, adj_3_0,
      adj_3_0_row_0, adj_3_0_row_1, adj_3_0_row_2, adj_3_0_row_3, adj_3_0_row_4, adj_3_0_row_5, adj_3_0_row_6, adj_3_0_row_7, adj_3_0_row_8, detPoly_3_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_0_scaled_inverse_row_7 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_0 d * adj_3_0 d) (7 : Fin 9) j =
      (detPoly_3_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (7 : Fin 9) j := by
  rw [minor_3_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_0, cols_3_0, adj_3_0,
      adj_3_0_row_0, adj_3_0_row_1, adj_3_0_row_2, adj_3_0_row_3, adj_3_0_row_4, adj_3_0_row_5, adj_3_0_row_6, adj_3_0_row_7, adj_3_0_row_8, detPoly_3_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_0_scaled_inverse_row_8 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_0 d * adj_3_0 d) (8 : Fin 9) j =
      (detPoly_3_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (8 : Fin 9) j := by
  rw [minor_3_0_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_0, cols_3_0, adj_3_0,
      adj_3_0_row_0, adj_3_0_row_1, adj_3_0_row_2, adj_3_0_row_3, adj_3_0_row_4, adj_3_0_row_5, adj_3_0_row_6, adj_3_0_row_7, adj_3_0_row_8, detPoly_3_0, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

theorem minor_3_0_scaled_inverse (d : Fin 4 → ℂ) :
    minor_3_0 d * adj_3_0 d =
      detPoly_3_0 d • (1 : Matrix (Fin 9) (Fin 9) ℂ) := by
  ext i j
  fin_cases i
  · exact minor_3_0_scaled_inverse_row_0 d j
  · exact minor_3_0_scaled_inverse_row_1 d j
  · exact minor_3_0_scaled_inverse_row_2 d j
  · exact minor_3_0_scaled_inverse_row_3 d j
  · exact minor_3_0_scaled_inverse_row_4 d j
  · exact minor_3_0_scaled_inverse_row_5 d j
  · exact minor_3_0_scaled_inverse_row_6 d j
  · exact minor_3_0_scaled_inverse_row_7 d j
  · exact minor_3_0_scaled_inverse_row_8 d j

private theorem minor_3_1_eq_lit (d : Fin 4 → ℂ) :
    minor_3_1 d = (cMatrix d).submatrix rows_3_1 cols_3_1 := by
  rfl

private theorem minor_3_1_scaled_inverse_row_0 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_1 d * adj_3_1 d) (0 : Fin 9) j =
      (detPoly_3_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (0 : Fin 9) j := by
  rw [minor_3_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_1, cols_3_1, adj_3_1,
      adj_3_1_row_0, adj_3_1_row_1, adj_3_1_row_2, adj_3_1_row_3, adj_3_1_row_4, adj_3_1_row_5, adj_3_1_row_6, adj_3_1_row_7, adj_3_1_row_8, detPoly_3_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_1_scaled_inverse_row_1 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_1 d * adj_3_1 d) (1 : Fin 9) j =
      (detPoly_3_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (1 : Fin 9) j := by
  rw [minor_3_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_1, cols_3_1, adj_3_1,
      adj_3_1_row_0, adj_3_1_row_1, adj_3_1_row_2, adj_3_1_row_3, adj_3_1_row_4, adj_3_1_row_5, adj_3_1_row_6, adj_3_1_row_7, adj_3_1_row_8, detPoly_3_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_1_scaled_inverse_row_2 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_1 d * adj_3_1 d) (2 : Fin 9) j =
      (detPoly_3_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (2 : Fin 9) j := by
  rw [minor_3_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_1, cols_3_1, adj_3_1,
      adj_3_1_row_0, adj_3_1_row_1, adj_3_1_row_2, adj_3_1_row_3, adj_3_1_row_4, adj_3_1_row_5, adj_3_1_row_6, adj_3_1_row_7, adj_3_1_row_8, detPoly_3_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_1_scaled_inverse_row_3 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_1 d * adj_3_1 d) (3 : Fin 9) j =
      (detPoly_3_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (3 : Fin 9) j := by
  rw [minor_3_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_1, cols_3_1, adj_3_1,
      adj_3_1_row_0, adj_3_1_row_1, adj_3_1_row_2, adj_3_1_row_3, adj_3_1_row_4, adj_3_1_row_5, adj_3_1_row_6, adj_3_1_row_7, adj_3_1_row_8, detPoly_3_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_1_scaled_inverse_row_4 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_1 d * adj_3_1 d) (4 : Fin 9) j =
      (detPoly_3_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (4 : Fin 9) j := by
  rw [minor_3_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_1, cols_3_1, adj_3_1,
      adj_3_1_row_0, adj_3_1_row_1, adj_3_1_row_2, adj_3_1_row_3, adj_3_1_row_4, adj_3_1_row_5, adj_3_1_row_6, adj_3_1_row_7, adj_3_1_row_8, detPoly_3_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_1_scaled_inverse_row_5 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_1 d * adj_3_1 d) (5 : Fin 9) j =
      (detPoly_3_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (5 : Fin 9) j := by
  rw [minor_3_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_1, cols_3_1, adj_3_1,
      adj_3_1_row_0, adj_3_1_row_1, adj_3_1_row_2, adj_3_1_row_3, adj_3_1_row_4, adj_3_1_row_5, adj_3_1_row_6, adj_3_1_row_7, adj_3_1_row_8, detPoly_3_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_1_scaled_inverse_row_6 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_1 d * adj_3_1 d) (6 : Fin 9) j =
      (detPoly_3_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (6 : Fin 9) j := by
  rw [minor_3_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_1, cols_3_1, adj_3_1,
      adj_3_1_row_0, adj_3_1_row_1, adj_3_1_row_2, adj_3_1_row_3, adj_3_1_row_4, adj_3_1_row_5, adj_3_1_row_6, adj_3_1_row_7, adj_3_1_row_8, detPoly_3_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_1_scaled_inverse_row_7 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_1 d * adj_3_1 d) (7 : Fin 9) j =
      (detPoly_3_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (7 : Fin 9) j := by
  rw [minor_3_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_1, cols_3_1, adj_3_1,
      adj_3_1_row_0, adj_3_1_row_1, adj_3_1_row_2, adj_3_1_row_3, adj_3_1_row_4, adj_3_1_row_5, adj_3_1_row_6, adj_3_1_row_7, adj_3_1_row_8, detPoly_3_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_1_scaled_inverse_row_8 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_1 d * adj_3_1 d) (8 : Fin 9) j =
      (detPoly_3_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (8 : Fin 9) j := by
  rw [minor_3_1_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_1, cols_3_1, adj_3_1,
      adj_3_1_row_0, adj_3_1_row_1, adj_3_1_row_2, adj_3_1_row_3, adj_3_1_row_4, adj_3_1_row_5, adj_3_1_row_6, adj_3_1_row_7, adj_3_1_row_8, detPoly_3_1, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

theorem minor_3_1_scaled_inverse (d : Fin 4 → ℂ) :
    minor_3_1 d * adj_3_1 d =
      detPoly_3_1 d • (1 : Matrix (Fin 9) (Fin 9) ℂ) := by
  ext i j
  fin_cases i
  · exact minor_3_1_scaled_inverse_row_0 d j
  · exact minor_3_1_scaled_inverse_row_1 d j
  · exact minor_3_1_scaled_inverse_row_2 d j
  · exact minor_3_1_scaled_inverse_row_3 d j
  · exact minor_3_1_scaled_inverse_row_4 d j
  · exact minor_3_1_scaled_inverse_row_5 d j
  · exact minor_3_1_scaled_inverse_row_6 d j
  · exact minor_3_1_scaled_inverse_row_7 d j
  · exact minor_3_1_scaled_inverse_row_8 d j

private theorem minor_3_2_eq_lit (d : Fin 4 → ℂ) :
    minor_3_2 d = (cMatrix d).submatrix rows_3_2 cols_3_2 := by
  rfl

private theorem minor_3_2_scaled_inverse_row_0 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_2 d * adj_3_2 d) (0 : Fin 9) j =
      (detPoly_3_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (0 : Fin 9) j := by
  rw [minor_3_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_2, cols_3_2, adj_3_2,
      adj_3_2_row_0, adj_3_2_row_1, adj_3_2_row_2, adj_3_2_row_3, adj_3_2_row_4, adj_3_2_row_5, adj_3_2_row_6, adj_3_2_row_7, adj_3_2_row_8, detPoly_3_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_2_scaled_inverse_row_1 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_2 d * adj_3_2 d) (1 : Fin 9) j =
      (detPoly_3_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (1 : Fin 9) j := by
  rw [minor_3_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_2, cols_3_2, adj_3_2,
      adj_3_2_row_0, adj_3_2_row_1, adj_3_2_row_2, adj_3_2_row_3, adj_3_2_row_4, adj_3_2_row_5, adj_3_2_row_6, adj_3_2_row_7, adj_3_2_row_8, detPoly_3_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_2_scaled_inverse_row_2 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_2 d * adj_3_2 d) (2 : Fin 9) j =
      (detPoly_3_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (2 : Fin 9) j := by
  rw [minor_3_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_2, cols_3_2, adj_3_2,
      adj_3_2_row_0, adj_3_2_row_1, adj_3_2_row_2, adj_3_2_row_3, adj_3_2_row_4, adj_3_2_row_5, adj_3_2_row_6, adj_3_2_row_7, adj_3_2_row_8, detPoly_3_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_2_scaled_inverse_row_3 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_2 d * adj_3_2 d) (3 : Fin 9) j =
      (detPoly_3_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (3 : Fin 9) j := by
  rw [minor_3_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_2, cols_3_2, adj_3_2,
      adj_3_2_row_0, adj_3_2_row_1, adj_3_2_row_2, adj_3_2_row_3, adj_3_2_row_4, adj_3_2_row_5, adj_3_2_row_6, adj_3_2_row_7, adj_3_2_row_8, detPoly_3_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_2_scaled_inverse_row_4 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_2 d * adj_3_2 d) (4 : Fin 9) j =
      (detPoly_3_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (4 : Fin 9) j := by
  rw [minor_3_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_2, cols_3_2, adj_3_2,
      adj_3_2_row_0, adj_3_2_row_1, adj_3_2_row_2, adj_3_2_row_3, adj_3_2_row_4, adj_3_2_row_5, adj_3_2_row_6, adj_3_2_row_7, adj_3_2_row_8, detPoly_3_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_2_scaled_inverse_row_5 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_2 d * adj_3_2 d) (5 : Fin 9) j =
      (detPoly_3_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (5 : Fin 9) j := by
  rw [minor_3_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_2, cols_3_2, adj_3_2,
      adj_3_2_row_0, adj_3_2_row_1, adj_3_2_row_2, adj_3_2_row_3, adj_3_2_row_4, adj_3_2_row_5, adj_3_2_row_6, adj_3_2_row_7, adj_3_2_row_8, detPoly_3_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_2_scaled_inverse_row_6 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_2 d * adj_3_2 d) (6 : Fin 9) j =
      (detPoly_3_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (6 : Fin 9) j := by
  rw [minor_3_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_2, cols_3_2, adj_3_2,
      adj_3_2_row_0, adj_3_2_row_1, adj_3_2_row_2, adj_3_2_row_3, adj_3_2_row_4, adj_3_2_row_5, adj_3_2_row_6, adj_3_2_row_7, adj_3_2_row_8, detPoly_3_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_2_scaled_inverse_row_7 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_2 d * adj_3_2 d) (7 : Fin 9) j =
      (detPoly_3_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (7 : Fin 9) j := by
  rw [minor_3_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_2, cols_3_2, adj_3_2,
      adj_3_2_row_0, adj_3_2_row_1, adj_3_2_row_2, adj_3_2_row_3, adj_3_2_row_4, adj_3_2_row_5, adj_3_2_row_6, adj_3_2_row_7, adj_3_2_row_8, detPoly_3_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

private theorem minor_3_2_scaled_inverse_row_8 (d : Fin 4 → ℂ) (j : Fin 9) :
    (minor_3_2 d * adj_3_2 d) (8 : Fin 9) j =
      (detPoly_3_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ)) (8 : Fin 9) j := by
  rw [minor_3_2_eq_lit]
  fin_cases j <;>
    simp [cMatrix, rows_3_2, cols_3_2, adj_3_2,
      adj_3_2_row_0, adj_3_2_row_1, adj_3_2_row_2, adj_3_2_row_3, adj_3_2_row_4, adj_3_2_row_5, adj_3_2_row_6, adj_3_2_row_7, adj_3_2_row_8, detPoly_3_2, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

theorem minor_3_2_scaled_inverse (d : Fin 4 → ℂ) :
    minor_3_2 d * adj_3_2 d =
      detPoly_3_2 d • (1 : Matrix (Fin 9) (Fin 9) ℂ) := by
  ext i j
  fin_cases i
  · exact minor_3_2_scaled_inverse_row_0 d j
  · exact minor_3_2_scaled_inverse_row_1 d j
  · exact minor_3_2_scaled_inverse_row_2 d j
  · exact minor_3_2_scaled_inverse_row_3 d j
  · exact minor_3_2_scaled_inverse_row_4 d j
  · exact minor_3_2_scaled_inverse_row_5 d j
  · exact minor_3_2_scaled_inverse_row_6 d j
  · exact minor_3_2_scaled_inverse_row_7 d j
  · exact minor_3_2_scaled_inverse_row_8 d j

/-! Normalized chart minor polynomials and their explicit unit-ideal witnesses. -/

def f00 (x : ℂ) : ℂ := -((x - 1)^2 * (x + 1)^2) / 256
def f01 (x : ℂ) : ℂ := x^7 / 256
theorem chart0_bezout (x : ℂ) :
    (256 * (-4*x^6 - 3*x^4 - 2*x^2 - 1)) * f00 x +
    (256 * (-x * (4*x^2 - 5))) * f01 x = 1 := by
  simp [f00, f01]
  ring

def f10 (z : ℂ) : ℂ := -((z^2 + 1)^2) / 256
def f11 (y z : ℂ) : ℂ := z^4 * (y^2 + z^2) / 256
def f12 (y z : ℂ) : ℂ := -y * z^4 / 256
theorem chart1_bezout (y z : ℂ) :
    let s := -3*z^4 + 2*z^2 - 1
    let t := -3*z^2 - 4
    (256*s) * f10 z + (256*t) * f11 y z + (256*t*y) * f12 y z = 1 := by
  dsimp [f10, f11, f12]
  ring

def f20 (z : ℂ) : ℂ := (z^2 + 1)^2 / 256
def f21 (y z : ℂ) : ℂ := -y^4 * z^4 / 256
def f22 (y z : ℂ) : ℂ := z^4 * (y^2 + z^2) / 256
theorem chart2_bezout (y z : ℂ) :
    let s := -4*z^6 + 3*z^4 - 2*z^2 + 1
    let t := 4*z^2 + 5
    (256*s) * f20 z - (256*t) * f21 y z +
      (256*t*(z^2-y^2)) * f22 y z = 1 := by
  dsimp [f20, f21, f22]
  ring

def f30 (x : ℂ) : ℂ := -((x^2 + 1)^2) / 256
def f31 (y x : ℂ) : ℂ := -y^4 * x / 256
def f32 (y x : ℂ) : ℂ := x^3 * (y^2 + 1) / 256
theorem chart3_bezout (y x : ℂ) :
    let s := 2*x^2 - 1
    let t := x*(2*x^2 + 3)
    (256*s) * f30 x - (256*t*x^2) * f31 y x -
      (256*t*(y^2-1)) * f32 y x = 1 := by
  dsimp [f30, f31, f32]
  ring


/-! ## Capstone: exact nonzero-character rank and null line -/

private theorem rank_ge_nine_of_certificate
    (d : Fin 4 → ℂ)
    (rows : Fin 9 → Fin 24) (cols : Fin 9 → Fin 10)
    (adj : Matrix (Fin 9) (Fin 9) ℂ) (c : ℂ)
    (hcert :
      (cMatrix d).submatrix rows cols * adj =
        c • (1 : Matrix (Fin 9) (Fin 9) ℂ))
    (hc : c ≠ 0) :
    9 ≤ (cMatrix d).rank := by
  have hscaled :
      (c • (1 : Matrix (Fin 9) (Fin 9) ℂ)).rank = 9 := by
    have hunit : IsUnit (c • (1 : Matrix (Fin 9) (Fin 9) ℂ)) := by
      rw [Matrix.isUnit_iff_isUnit_det]
      simp [Matrix.det_smul, hc]
    simpa using Matrix.rank_of_isUnit
      (c • (1 : Matrix (Fin 9) (Fin 9) ℂ)) hunit
  calc
    9 = (c • (1 : Matrix (Fin 9) (Fin 9) ℂ)).rank := hscaled.symm
    _ = ((cMatrix d).submatrix rows cols * adj).rank :=
      congrArg Matrix.rank hcert.symm
    _ ≤ ((cMatrix d).submatrix rows cols).rank :=
      Matrix.rank_mul_le_left _ _
    _ ≤ (cMatrix d).rank :=
      Matrix.rank_submatrix_le _ _ _

theorem cMatrix_rank_ge_nine {d : Fin 4 → ℂ} (hd : d ≠ 0) :
    9 ≤ (cMatrix d).rank := by
  have hcoord :
      d 0 ≠ 0 ∨ d 1 ≠ 0 ∨ d 2 ≠ 0 ∨ d 3 ≠ 0 := by
    by_contra h
    push_neg at h
    apply hd
    funext i
    fin_cases i <;> simp_all
  rcases hcoord with h0 | h1 | h2 | h3
  · by_cases h3' : d 3 = 0
    · exact rank_ge_nine_of_certificate d rows_0_0 cols_0_0
        (adj_0_0 d) (detPoly_0_0 d)
        (by simpa [minor_0_0] using minor_0_0_scaled_inverse d)
        (by simp [detPoly_0_0, h0, h3'])
    · exact rank_ge_nine_of_certificate d rows_0_1 cols_0_1
        (adj_0_1 d) (detPoly_0_1 d)
        (by simpa [minor_0_1] using minor_0_1_scaled_inverse d)
        (by simp [detPoly_0_1, h0, h3'])
  · by_cases h3' : d 3 = 0
    · exact rank_ge_nine_of_certificate d rows_1_0 cols_1_0
        (adj_1_0 d) (detPoly_1_0 d)
        (by simpa [minor_1_0] using minor_1_0_scaled_inverse d)
        (by simp [detPoly_1_0, h1, h3'])
    · by_cases h2' : d 2 = 0
      · exact rank_ge_nine_of_certificate d rows_1_1 cols_1_1
          (adj_1_1 d) (detPoly_1_1 d)
          (by simpa [minor_1_1] using minor_1_1_scaled_inverse d)
          (by simp [detPoly_1_1, h1, h2', h3'])
      · exact rank_ge_nine_of_certificate d rows_1_2 cols_1_2
          (adj_1_2 d) (detPoly_1_2 d)
          (by simpa [minor_1_2] using minor_1_2_scaled_inverse d)
          (by simp [detPoly_1_2, h1, h2', h3'])
  · by_cases h3' : d 3 = 0
    · exact rank_ge_nine_of_certificate d rows_2_0 cols_2_0
        (adj_2_0 d) (detPoly_2_0 d)
        (by simpa [minor_2_0] using minor_2_0_scaled_inverse d)
        (by simp [detPoly_2_0, h2, h3'])
    · by_cases h1' : d 1 = 0
      · exact rank_ge_nine_of_certificate d rows_2_2 cols_2_2
          (adj_2_2 d) (detPoly_2_2 d)
          (by simpa [minor_2_2] using minor_2_2_scaled_inverse d)
          (by simp [detPoly_2_2, h1', h2, h3'])
      · exact rank_ge_nine_of_certificate d rows_2_1 cols_2_1
          (adj_2_1 d) (detPoly_2_1 d)
          (by simpa [minor_2_1] using minor_2_1_scaled_inverse d)
          (by simp [detPoly_2_1, h1', h2, h3'])
  · by_cases h2' : d 2 = 0
    · exact rank_ge_nine_of_certificate d rows_3_0 cols_3_0
        (adj_3_0 d) (detPoly_3_0 d)
        (by simpa [minor_3_0] using minor_3_0_scaled_inverse d)
        (by simp [detPoly_3_0, h2', h3])
    · by_cases h1' : d 1 = 0
      · exact rank_ge_nine_of_certificate d rows_3_2 cols_3_2
          (adj_3_2 d) (detPoly_3_2 d)
          (by simpa [minor_3_2] using minor_3_2_scaled_inverse d)
          (by simp [detPoly_3_2, h1', h2', h3])
      · exact rank_ge_nine_of_certificate d rows_3_1 cols_3_1
          (adj_3_1 d) (detPoly_3_1 d)
          (by simpa [minor_3_1] using minor_3_1_scaled_inverse d)
          (by simp [detPoly_3_1, h1', h2', h3])

theorem cMatrix_rank_le_nine {d : Fin 4 → ℂ} (hd : d ≠ 0) :
    (cMatrix d).rank ≤ 9 := by
  let L := (cMatrix d).mulVecLin
  have hqker : q0 d ∈ LinearMap.ker L := by
    simp only [LinearMap.mem_ker, L, Matrix.mulVecLin_apply]
    exact cMatrix_q0_zero d
  have hspan_le : ℂ ∙ q0 d ≤ LinearMap.ker L :=
    (Submodule.span_singleton_le_iff_mem _ _).mpr hqker
  have hone : 1 ≤ Module.finrank ℂ (LinearMap.ker L) := by
    have hspanrank : Module.finrank ℂ (ℂ ∙ q0 d) = 1 :=
      finrank_span_singleton (K := ℂ) (q0_ne_zero hd)
    rw [← hspanrank]
    exact Submodule.finrank_mono hspan_le
  have hrn :
      (cMatrix d).rank + Module.finrank ℂ (LinearMap.ker L) = 10 := by
    simpa [L, Matrix.rank] using L.finrank_range_add_finrank_ker
  omega

theorem cMatrix_rank_eq_nine {d : Fin 4 → ℂ} (hd : d ≠ 0) :
    (cMatrix d).rank = 9 :=
  le_antisymm (cMatrix_rank_le_nine hd) (cMatrix_rank_ge_nine hd)

theorem cMatrix_ker_finrank_eq_one {d : Fin 4 → ℂ} (hd : d ≠ 0) :
    Module.finrank ℂ (LinearMap.ker (cMatrix d).mulVecLin) = 1 := by
  have hrn :
      (cMatrix d).rank +
          Module.finrank ℂ (LinearMap.ker (cMatrix d).mulVecLin) = 10 := by
    simpa [Matrix.rank] using
      (cMatrix d).mulVecLin.finrank_range_add_finrank_ker
  rw [cMatrix_rank_eq_nine hd] at hrn
  omega

theorem cMatrix_ker_eq_span_q0 {d : Fin 4 → ℂ} (hd : d ≠ 0) :
    LinearMap.ker (cMatrix d).mulVecLin = ℂ ∙ q0 d := by
  have hqker :
      q0 d ∈ LinearMap.ker (cMatrix d).mulVecLin := by
    simp only [LinearMap.mem_ker, Matrix.mulVecLin_apply]
    exact cMatrix_q0_zero d
  have hspan_le :
      ℂ ∙ q0 d ≤ LinearMap.ker (cMatrix d).mulVecLin :=
    (Submodule.span_singleton_le_iff_mem _ _).mpr hqker
  have hfin :
      Module.finrank ℂ (ℂ ∙ q0 d) =
        Module.finrank ℂ (LinearMap.ker (cMatrix d).mulVecLin) := by
    rw [finrank_span_singleton (q0_ne_zero hd),
      cMatrix_ker_finrank_eq_one hd]
  exact (Submodule.eq_of_le_of_finrank_eq hspan_le hfin).symm


/-! The origin is a special fiber: both adjacent differentials vanish there. -/

theorem q0_zero_smul (φ : ℂ) :
    φ • q0 (0 : Fin 4 → ℂ) = 0 := by
  rw [q0_zero]
  simp

theorem cMatrix_zero_ker_eq_top :
    LinearMap.ker (cMatrix (0 : Fin 4 → ℂ)).mulVecLin = ⊤ := by
  rw [cMatrix_zero]
  simp

theorem cMatrix_zero_ker_finrank_eq_ten :
    Module.finrank ℂ
      (LinearMap.ker (cMatrix (0 : Fin 4 → ℂ)).mulVecLin) = 10 := by
  rw [cMatrix_zero_ker_eq_top]
  simp


/- Post-merge full-closure validation trigger; theorem content unchanged. -/

end

end D0.Geometry.A4DMetricNullHessianComplex
