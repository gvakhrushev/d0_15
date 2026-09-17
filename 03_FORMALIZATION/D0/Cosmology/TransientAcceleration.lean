import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic

set_option linter.unusedVariables false

namespace D0.Cosmology

def discreteAcceleration (a_prev a_curr a_next : ℝ) : ℝ :=
  a_next - 2 * a_curr + a_prev

theorem inverse_density_convex_three_point (x z la : ℝ)
    (hx : x > 0) (hz : z > 0) (hla : la > 1)
    (h_pos1 : x - z * la > 0)
    (h_pos2 : x - z > 0)
    (h_pos3 : x - z / la > 0) :
    discreteAcceleration (1 / (x - z / la)) (1 / (x - z)) (1 / (x - z * la)) > 0 := by
  have h_pos1_ne : x - z * la ≠ 0 := ne_of_gt h_pos1
  have h_pos2_ne : x - z ≠ 0 := ne_of_gt h_pos2
  have h_pos3_ne : x - z / la ≠ 0 := ne_of_gt h_pos3
  have h_la_ne : la ≠ 0 := ne_of_gt (by linarith)
  have h_la_z_pos : x * la - z > 0 := by
    have h_lam_pos : la > 0 := by linarith
    have : x * la - z = la * (x - z / la) := by
      have : z / la * la = z := div_mul_cancel₀ z h_la_ne
      calc
        x * la - z = x * la - z / la * la := by rw [this]
        _ = la * (x - z / la) := by ring
    rw [this]
    exact mul_pos h_lam_pos h_pos3
  have h_la_z_ne : x * la - z ≠ 0 := ne_of_gt h_la_z_pos
  have h_eq : discreteAcceleration (1 / (x - z / la)) (1 / (x - z)) (1 / (x - z * la)) =
      (z * (x + z) * (la - 1)^2) / (la * (x - z * la) * (x - z) * (x - z / la)) := by
    unfold discreteAcceleration
    field_simp [h_pos1_ne, h_pos2_ne, h_pos3_ne, h_la_ne, h_la_z_ne]
    ring
  rw [h_eq]
  have h_num_pos : z * (x + z) * (la - 1)^2 > 0 := by
    have hz_pos : z > 0 := hz
    have h_xz_pos : x + z > 0 := by linarith
    have h_diff_pos : (la - 1)^2 > 0 := by
      have : la - 1 > 0 := by linarith
      exact sq_pos_of_ne_zero (ne_of_gt this)
    exact mul_pos (mul_pos hz_pos h_xz_pos) h_diff_pos
  have h_den_pos : la * (x - z * la) * (x - z) * (x - z / la) > 0 := by
    have hla_pos : la > 0 := by linarith
    have h1 : la * (x - z * la) > 0 := mul_pos hla_pos h_pos1
    have h2 : la * (x - z * la) * (x - z) > 0 := mul_pos h1 h_pos2
    exact mul_pos h2 h_pos3
  exact div_pos h_num_pos h_den_pos

theorem underdense_geometric_mode_generates_positive_acceleration (c v la : ℝ)
    (hc : c > 0) (hv : v < 0) (hla : la > 1)
    (h_pos_prev : c + v / la > 0)
    (h_pos_curr : c + v > 0)
    (h_pos_next : c + v * la > 0) :
    discreteAcceleration (1 / (c + v / la)) (1 / (c + v)) (1 / (c + v * la)) > 0 := by
  let z := -v
  have hz : z > 0 := by
    dsimp [z]
    linarith
  have h_prev_eq : c + v / la = c - z / la := by
    dsimp [z]
    rw [neg_div, sub_neg_eq_add]
  have h_curr_eq : c + v = c - z := by
    dsimp [z]
    rw [sub_neg_eq_add]
  have h_next_eq : c + v * la = c - z * la := by
    dsimp [z]
    rw [neg_mul, sub_neg_eq_add]
  have h_pos1 : c - z * la > 0 := by
    rw [← h_next_eq]
    exact h_pos_next
  have h_pos2 : c - z > 0 := by
    rw [← h_curr_eq]
    exact h_pos_curr
  have h_pos3 : c - z / la > 0 := by
    rw [← h_prev_eq]
    exact h_pos_prev
  rw [h_prev_eq, h_curr_eq, h_next_eq]
  exact inverse_density_convex_three_point c z la hc hz hla h_pos1 h_pos2 h_pos3

end D0.Cosmology
