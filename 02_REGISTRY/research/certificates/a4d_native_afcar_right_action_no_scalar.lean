import Mathlib.Tactic

/-!
The linear-algebra consequence used by the AF-CAR commutant boundary:
there is no unital ring representation of the noncommutative 2-by-2 matrix
algebra in a scalar field. The concrete CAR commutant rank is checked by the
separate exact modular-minor certificate.
-/

namespace D0.Research.AFCarRightAction

abbrev M2 := Matrix (Fin 2) (Fin 2) ℂ

def e00 : M2 := !![(1 : ℂ), 0; 0, 0]
def e01 : M2 := !![(0 : ℂ), 1; 0, 0]
def e10 : M2 := !![(0 : ℂ), 0; 1, 0]
def e11 : M2 := !![(0 : ℂ), 0; 0, 1]

private theorem e00_mul_e11 : e00 * e11 = 0 := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [e00, e11, Matrix.mul_apply]

private theorem e00_add_e11 : e00 + e11 = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [e00, e11]

private theorem e00_e01_e11 : e00 * e01 * e11 = e01 := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [e00, e01, e11, Matrix.mul_apply]

private theorem e11_e10_e00 : e11 * e10 * e00 = e10 := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [e00, e10, e11, Matrix.mul_apply]

private theorem e01_mul_e10 : e01 * e10 = e00 := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [e00, e01, e10, Matrix.mul_apply]

private theorem e10_mul_e01 : e10 * e01 = e11 := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [e01, e10, e11, Matrix.mul_apply]

theorem no_unital_matrix_two_ring_hom_to_complex
    (f : M2 →+* ℂ) : False := by
  have hprod : f e00 * f e11 = 0 := by
    calc
      f e00 * f e11 = f (e00 * e11) := (map_mul f e00 e11).symm
      _ = f 0 := by rw [e00_mul_e11]
      _ = 0 := map_zero f
  have hsum : f e00 + f e11 = 1 := by
    calc
      f e00 + f e11 = f (e00 + e11) := (map_add f e00 e11).symm
      _ = f 1 := by rw [e00_add_e11]
      _ = 1 := map_one f
  have h01 : f e01 = 0 := by
    calc
      f e01 = f (e00 * e01 * e11) := by rw [e00_e01_e11]
      _ = f e00 * f e01 * f e11 := by simp [map_mul]
      _ = 0 := by
        rcases mul_eq_zero.mp hprod with h0 | h1
        · simp [h0]
        · simp [h1]
  have h10 : f e10 = 0 := by
    calc
      f e10 = f (e11 * e10 * e00) := by rw [e11_e10_e00]
      _ = f e11 * f e10 * f e00 := by simp [map_mul]
      _ = 0 := by
        rcases mul_eq_zero.mp hprod with h0 | h1
        · simp [h0]
        · simp [h1]
  have h00 : f e00 = 0 := by
    calc
      f e00 = f (e01 * e10) := by rw [e01_mul_e10]
      _ = f e01 * f e10 := map_mul f e01 e10
      _ = 0 := by rw [h01, h10]; simp
  have h11 : f e11 = 0 := by
    calc
      f e11 = f (e10 * e01) := by rw [e10_mul_e01]
      _ = f e10 * f e01 := map_mul f e10 e01
      _ = 0 := by rw [h10, h01]; simp
  rw [h00, h11] at hsum
  norm_num at hsum

end D0.Research.AFCarRightAction

#print axioms D0.Research.AFCarRightAction.no_unital_matrix_two_ring_hom_to_complex
