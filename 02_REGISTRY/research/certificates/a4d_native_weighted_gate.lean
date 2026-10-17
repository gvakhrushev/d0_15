import D0.Geometry.HeatTraceA2Decomposition
import D0.Gravity.A2CompensatorNoether

/-! Research capsule. Literal inverse-volume coordinates and full edge gates.
No physical metric identification, native lift variation, or Einstein equation
is assumed to be owned by these algebraic facts.
-/

open scoped BigOperators

namespace D0.Research.NativeWeightedGate

noncomputable section

theorem proxy_inverse_volume {N : Type} [Fintype N] [DecidableEq N]
    (L : Matrix N N ℝ) (ρ : N → ℝ) :
    D0.Geometry.discreteEHActionProxy L ρ =
      ∑ i, ∑ j, if i ≠ j then (L i j)^2 * (1 / ρ i) * (1 / ρ j) else 0 := by
  unfold D0.Geometry.discreteEHActionProxy
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  split_ifs
  · simp [div_eq_mul_inv, mul_inv_rev, mul_comm, mul_left_comm, mul_assoc]
  · rfl

theorem archive_volume_inverse_coordinate {N : Type} [Fintype N]
    (ρ : N → ℝ) :
    D0.Cosmology.archiveVolume ρ = (∑ i, 1 / ρ i) / Fintype.card N := rfl

theorem proxy_affine_volume_profile {N : Type} [Fintype N] [DecidableEq N]
    (L : Matrix N N ℝ) (ρ u v : N → ℝ) (s : ℝ)
    (hμ : ∀ i, 1 / ρ i = u i + s * v i) :
    D0.Geometry.discreteEHActionProxy L ρ =
      (∑ i, ∑ j, if i ≠ j then (L i j)^2 * u i * u j else 0) +
      s * (∑ i, ∑ j, if i ≠ j then
        (L i j)^2 * (u i * v j + v i * u j) else 0) +
      s^2 * (∑ i, ∑ j, if i ≠ j then (L i j)^2 * v i * v j else 0) := by
  rw [proxy_inverse_volume]
  simp_rw [hμ]
  simp only [Finset.mul_sum, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  split_ifs <;> ring

open D0.Gravity.A2CompensatorNoether

theorem full_edge_gate_iff_residual_zero {V E : Type*}
    [Fintype V] [Fintype E] [DecidableEq V] [DecidableEq E]
    (B : Matrix V E ℚ) (W : E → ℚ) (h : E → ℚ) (eta : V → ℚ)
    (hW : ∀ e, 0 < W e) :
    (∀ e, edgeResponse B W h eta e = 0) ↔
      (∀ e, compensatorResidual B h eta e = 0) := by
  constructor
  · intro hgate e
    have he := hgate e
    change 4 * W e * compensatorResidual B h eta e = 0 at he
    exact (mul_eq_zero.mp he).resolve_left (ne_of_gt (mul_pos (by norm_num) (hW e)))
  · intro hr e
    simp [edgeResponse, hr e]

theorem full_edge_gate_action_zero {V E : Type*}
    [Fintype V] [Fintype E] [DecidableEq V] [DecidableEq E]
    (B : Matrix V E ℚ) (W : E → ℚ) (h : E → ℚ) (eta : V → ℚ)
    (hW : ∀ e, 0 < W e) (hgate : ∀ e, edgeResponse B W h eta e = 0) :
    extendedAction B W h eta = 0 := by
  have hr := (full_edge_gate_iff_residual_zero B W h eta hW).mp hgate
  simp [extendedAction, hr]

theorem full_edge_gate_diagonal_zero {V E : Type*}
    [Fintype V] [Fintype E] [DecidableEq V] [DecidableEq E]
    (B : Matrix V E ℚ) (W : E → ℚ) (h : E → ℚ) (eta : V → ℚ)
    (hW : ∀ e, 0 < W e) (hgate : ∀ e, edgeResponse B W h eta e = 0)
    (v : V) : diagonalResponse B W h eta v = 0 := by
  have hr := (full_edge_gate_iff_residual_zero B W h eta hW).mp hgate
  simp [diagonalResponse, BPlus, Matrix.mulVec, dotProduct,
    weightedEdge_apply, hr]

theorem residual_zero_weight_variation {V E : Type*}
    [Fintype V] [Fintype E] [DecidableEq V] [DecidableEq E]
    (B : Matrix V E ℚ) (W dW : E → ℚ) (h : E → ℚ) (eta : V → ℚ)
    (hr : ∀ e, compensatorResidual B h eta e = 0) :
    extendedAction B (W + dW) h eta - extendedAction B W h eta = 0 := by
  simp [extendedAction, hr]

#print axioms proxy_inverse_volume
#print axioms archive_volume_inverse_coordinate
#print axioms proxy_affine_volume_profile
#print axioms full_edge_gate_iff_residual_zero
#print axioms full_edge_gate_action_zero
#print axioms full_edge_gate_diagonal_zero
#print axioms residual_zero_weight_variation

end
end D0.Research.NativeWeightedGate
