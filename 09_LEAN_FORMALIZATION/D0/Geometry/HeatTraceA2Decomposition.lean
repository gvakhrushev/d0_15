import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic
import D0.Geometry.ConformalLaplacianTrace
import D0.Geometry.HeatTraceEHProxy

open scoped BigOperators

namespace D0.Geometry.HeatTraceA2Decomposition

open D0.Geometry

noncomputable def diagonalSquareTerm {N : Type} [Fintype N] (L : Matrix N N ℝ) (ρ : N → ℝ) : ℝ :=
  ∑ i, (L i i)^2 / (ρ i)^2

noncomputable def discreteEHActionProxy {N : Type} [Fintype N] [DecidableEq N] (L : Matrix N N ℝ) (ρ : N → ℝ) : ℝ :=
  (1 / 2 : ℝ) * ∑ i, ∑ j, if i ≠ j then (L i j)^2 / (ρ i * ρ j) else 0

theorem heat_trace_sq_exact_decomposition {N : Type} [Fintype N] [DecidableEq N] (L : Matrix N N ℝ) (ρ : N → ℝ)
    (h_pos : ∀ i, ρ i > 0) (h_symm : ∀ i j, L i j = L j i) :
    Matrix.trace ((weightedLaplacian L ρ) * (weightedLaplacian L ρ)) =
    diagonalSquareTerm L ρ + 2 * discreteEHActionProxy L ρ := by
  unfold weightedLaplacian
  unfold diagonalSquareTerm
  unfold discreteEHActionProxy
  rw [D0.Geometry.trace_square_weighted_laplacian_decomposition L ρ h_pos h_symm]
  unfold D0.Geometry.discreteEHActionProxy
  ring

theorem discrete_eh_proxy_nonnegative {N : Type} [Fintype N] [DecidableEq N] (L : Matrix N N ℝ) (ρ : N → ℝ)
    (h_pos : ∀ i, ρ i > 0) :
    discreteEHActionProxy L ρ ≥ 0 := by
  unfold discreteEHActionProxy
  have h_nonneg : D0.Geometry.discreteEHActionProxy L ρ ≥ 0 := D0.Geometry.offdiag_proxy_nonnegative L ρ h_pos
  unfold D0.Geometry.discreteEHActionProxy at h_nonneg
  linarith

theorem offdiag_double_count_guard {N : Type} [Fintype N] [DecidableEq N] (L : Matrix N N ℝ) (ρ : N → ℝ) :
    2 * discreteEHActionProxy L ρ = ∑ i, ∑ j, if i ≠ j then (L i j)^2 / (ρ i * ρ j) else 0 := by
  unfold discreteEHActionProxy
  ring

theorem double_count_factor_guard {N : Type} [Fintype N] [DecidableEq N] (L : Matrix N N ℝ) (ρ : N → ℝ) :
    2 * discreteEHActionProxy L ρ = ∑ i, ∑ j, if i ≠ j then (L i j)^2 / (ρ i * ρ j) else 0 :=
  offdiag_double_count_guard L ρ

end D0.Geometry.HeatTraceA2Decomposition
