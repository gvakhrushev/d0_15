import D0.Analysis.MatrixThermalTrace
import D0.Algebra.MovingProjectorPositiveChart

/-!
# Fixed-Gram moving-cut heat and feedback composition

This combines the actual thermal log-partition and feedback log-determinant
on one differentiable projector, evolution and thermal-matrix curve. It is a
finite mathematical identity and does not assert physical admission, a
complete Info/work price, or a mixed second variation.
-/

namespace D0.Algebra.MovingProjectorTransport

open Filter
open scoped Topology Matrix.Norms.Frobenius

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- The original fixed-parameter heat-plus-feedback scalar on a finite carrier. -/
noncomputable def movingHeatFeedback (β z : ℝ) (P U Δ : Matrix ι ι ℂ) : ℝ :=
  β⁻¹ * Real.log (D0.Analysis.matrixHeatPartition β Δ) -
    Real.log ((1 - (z : ℂ) • (star (cut P U) * cut P U)).det.re)

/--
The two derivatives are evaluated on the same curves and canonical generator.
The projector is orthogonal locally, while the isometry and Hermiticity are
needed at the evaluation point. The carrier is finite and nonempty.
-/
theorem hasDerivAt_moving_heat_feedback [Nonempty ι]
    {P U Δ : ℝ → Matrix ι ι ℂ} {dP dU dΔ : Matrix ι ι ℂ} {t : ℝ}
    (β z : ℝ) (hβ : β ≠ 0) (hz0 : 0 ≤ z) (hz1 : z < 1)
    (hP : HasDerivAt P dP t) (hU : HasDerivAt U dU t)
    (hΔ : HasDerivAt Δ dΔ t)
    (hIdem : ∀ᶠ s in 𝓝 t, P s * P s = P s)
    (hSelfAdjoint : ∀ᶠ s in 𝓝 t, star (P s) = P s)
    (hIsometry : star (U t) * U t = 1) (hHerm : star (Δ t) = Δ t) :
    let K := generator (P t) dP
    let C := cut (P t) (U t)
    let R := (1 - (z : ℂ) • (star C * C))⁻¹
    let V := (1 - P t) * (dU - comm K (U t)) * P t
    let E := NormedSpace.exp ((-β) • Δ t)
    let Z := D0.Analysis.matrixHeatPartition β (Δ t)
    HasDerivAt (fun s => movingHeatFeedback β z (P s) (U s) (Δ s))
      (-((Matrix.trace (E * (dΔ - comm K (Δ t)))).re) / Z +
        z * (2 * (Matrix.trace (R * star C * V)).re)) t := by
  have hh := D0.Analysis.hasDerivAt_matrix_heat_log_partition
    (K := generator (P t) dP) β hβ hΔ hHerm
  have hf := complex_matrix_feedback_real_logdet_of_isometric_cut_hasDerivAt
    z hP hU hIdem hSelfAdjoint hIsometry hz0 hz1
  have h := hh.add hf
  simpa only [movingHeatFeedback, sub_eq_add_neg, comm] using h

end D0.Algebra.MovingProjectorTransport
