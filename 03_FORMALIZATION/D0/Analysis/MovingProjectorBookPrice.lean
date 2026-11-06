import D0.Algebra.MovingProjectorCalculus
import D0.Analysis.MatrixThermalTrace

/-!
# The complete finite Book03 source for a moving projector

This module composes the independently proved thermal and feedback
log-determinant derivatives on one differentiable finite-matrix curve. The
active projector is allowed to move; its tangent generates the common internal
transport, and the remaining source depends on the relative derivatives of
the dynamics and thermal operator. The determinant chart, Hermiticity, and
curve hypotheses are explicit. No admitted D0 field map or physical source
selection is constructed here.
-/

noncomputable section

namespace D0.Analysis.MovingProjectorBookPrice

open Filter
open scoped Topology
open D0.Algebra.MovingProjectorTransport

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- The normalized finite thermal state `exp(-β Δ) / Tr exp(-β Δ)`. -/
noncomputable def matrixThermalState (β : ℝ) (Δ : Matrix ι ι ℂ) :
    Matrix ι ι ℂ :=
  (matrixHeatPartition β Δ)⁻¹ • NormedSpace.exp ((-β) • Δ)

/-- The unchanged finite Book03 heat-plus-feedback price along three curves. -/
noncomputable def matrixBook03Price (β z : ℝ)
    (Δ P U : ℝ → Matrix ι ι ℂ) (s : ℝ) : ℝ :=
  β⁻¹ * Real.log (matrixHeatPartition β (Δ s)) -
    Real.log ((1 - (z : ℂ) •
      (star (cut (P s) (U s)) * cut (P s) (U s))).det.re)

/-- Pairing the normalized thermal state is exactly division by its partition
function; the denominator is positive on the Hermitian thermal chart. -/
theorem matrixThermalState_trace_normalization [Nonempty ι]
    (β : ℝ) (Δ Y : Matrix ι ι ℂ) (hHerm : star Δ = Δ) :
    (Matrix.trace (matrixThermalState β Δ * Y)).re =
      (Matrix.trace (NormedSpace.exp ((-β) • Δ) * Y)).re /
        matrixHeatPartition β Δ := by
  have hZ : 0 < matrixHeatPartition β Δ :=
    matrix_exp_trace_re_pos ((-β) • Δ) (by simp [hHerm])
  have hZne : matrixHeatPartition β Δ ≠ 0 := ne_of_gt hZ
  simp only [matrixThermalState, matrixHeatPartition, smul_mul_assoc,
    Matrix.trace_smul, Complex.smul_re]
  field_simp [hZne]; ring

/-- Exact first source of the original finite Book03 price when `P` moves.

For `K = [dP,P]`, the two source terms use the same curves and the same
relative derivatives. In particular the feedback source retains the motion of
the active cut through `Q (dU - [K,U]) P`. The theorem is a finite analytic
identity on the stated positive determinant chart, not a physical admission
or Einstein-source claim.
-/
theorem hasDerivAt_moving_projector_book03_price [Nonempty ι]
    (β z : ℝ) {Δ P U : ℝ → Matrix ι ι ℂ}
    {dΔ dP dU : Matrix ι ι ℂ} {t : ℝ}
    (hβ : β ≠ 0)
    (hΔ : HasDerivAt Δ dΔ t) (hHerm : star (Δ t) = Δ t)
    (hP : HasDerivAt P dP t) (hU : HasDerivAt U dU t)
    (hIdem : ∀ᶠ s in 𝓝 t, P s * P s = P s)
    (hSelfAdjoint : ∀ᶠ s in 𝓝 t, star (P s) = P s)
    (hSlit : (1 - (z : ℂ) •
      (star (cut (P t) (U t)) * cut (P t) (U t))).det ∈ Complex.slitPlane) :
    let K := generator (P t) dP
    let ρ := matrixThermalState β (Δ t)
    let C := cut (P t) (U t)
    let R := (1 - (z : ℂ) • (star C * C))⁻¹
    let V := (1 - P t) * (dU - comm K (U t)) * P t
    HasDerivAt (fun s => matrixBook03Price β z Δ P U s)
      (-(Matrix.trace (ρ * (dΔ - comm K (Δ t)))).re +
        z * (2 * (Matrix.trace (R * star C * V)).re)) t := by
  let K := generator (P t) dP
  let E := NormedSpace.exp ((-β) • Δ t)
  let Z := matrixHeatPartition β (Δ t)
  let ρ := matrixThermalState β (Δ t)
  let C := cut (P t) (U t)
  let R := (1 - (z : ℂ) • (star C * C))⁻¹
  let V := (1 - P t) * (dU - comm K (U t)) * P t
  let X := dΔ - comm K (Δ t)
  have hThermal := hasDerivAt_matrix_heat_log_partition
    (K := K) β hβ hΔ hHerm
  have hFeedback := complex_matrix_feedback_real_logdet_of_slit_hasDerivAt
    z hP hU hIdem hSelfAdjoint hSlit
  have hSum := hThermal.add hFeedback
  have hNormalize : (Matrix.trace (ρ * X)).re =
      (Matrix.trace (E * X)).re / Z := by
    dsimp [ρ, E, Z]
    exact matrixThermalState_trace_normalization β (Δ t) X hHerm
  have hDerivative :
      -(Matrix.trace (E * X)).re / Z +
          z * (2 * (Matrix.trace (R * star C * V)).re) =
        -(Matrix.trace (ρ * X)).re +
          z * (2 * (Matrix.trace (R * star C * V)).re) := by
    calc
      -(Matrix.trace (E * X)).re / Z +
          z * (2 * (Matrix.trace (R * star C * V)).re) =
        -((Matrix.trace (E * X)).re / Z) +
          z * (2 * (Matrix.trace (R * star C * V)).re) := by ring
      _ = -(Matrix.trace (ρ * X)).re +
          z * (2 * (Matrix.trace (R * star C * V)).re) := by rw [← hNormalize]
  exact hSum.congr_deriv hDerivative

end D0.Analysis.MovingProjectorBookPrice

end
