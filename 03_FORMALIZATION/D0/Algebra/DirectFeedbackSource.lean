import D0.Algebra.MovingProjectorCalculus
import D0.Analysis.MatrixDeterminantDerivative

/-!
# Direct first source of the original return feedback

This finite-dimensional layer records the source reduction for the original
return pencil `F = 4 p² A (1 - p² A)`, `A = a† a`. It differentiates the
polynomial in `A` without commuting `A` with its variation and does not invert
`A`. A positive determinant chart is retained for the logarithm. No map from an
admitted D0 history, complete Book price, or physical field variation is built
here.
-/

noncomputable section

namespace D0.Algebra.DirectFeedbackSource

open Filter

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- The return operator in the original CAR source, expressed from `A`. -/
def returnOperator (p : ℝ) (A : Matrix ι ι ℂ) : Matrix ι ι ℂ :=
  (4 * (p : ℂ) ^ 2) • (A - (p : ℂ) ^ 2 • (A * A))

/-- The polynomial coefficient multiplying the first `A`-jet. -/
def sourceCoefficient (p : ℝ) (A : Matrix ι ι ℂ) : Matrix ι ι ℂ :=
  1 - (2 * (p : ℂ) ^ 2) • A

/-- The original feedback pencil `I - z F`. -/
def feedbackPencil (p z : ℝ) (A : Matrix ι ι ℂ) : Matrix ι ι ℂ :=
  1 - (z : ℂ) • returnOperator p A

/-- The actual first derivative of the noncommutative polynomial return. -/
def returnJet (p : ℝ) (A H : Matrix ι ι ℂ) : Matrix ι ι ℂ :=
  (4 * (p : ℂ) ^ 2) •
    (H - (p : ℂ) ^ 2 • (H * A + A * H))

/-- The original feedback pencil is a polynomial in `A`, so it commutes with `A`. -/
theorem feedbackPencil_commutes_returnInput (p z : ℝ) (A : Matrix ι ι ℂ) :
    feedbackPencil p z A * A = A * feedbackPencil p z A := by
  simp [feedbackPencil, returnOperator, Matrix.sub_mul, Matrix.mul_sub]
  noncomm_ring

/-- The determinant-resolvent source reduces to the symmetric polynomial coefficient.

The only commutation used is that the resolvent is a function of the unvaried
`A`; no commutation between `A` and its variation `H` is assumed.
-/
theorem trace_resolvent_returnJet_eq_sourceCoefficient
    (p z : ℝ) (A H : Matrix ι ι ℂ)
    (hD : IsUnit (feedbackPencil p z A).det) :
    Matrix.trace ((feedbackPencil p z A)⁻¹ * returnJet p A H) =
      (4 * (p : ℂ) ^ 2) *
        Matrix.trace ((feedbackPencil p z A)⁻¹ * sourceCoefficient p A * H) := by
  let D := feedbackPencil p z A
  let R := D⁻¹
  have hDA : D * A = A * D := feedbackPencil_commutes_returnInput p z A
  have hRD : R * D = 1 := Matrix.nonsing_inv_mul D hD
  have hDR : D * R = 1 := Matrix.mul_nonsing_inv D hD
  have hRA : R * A = A * R :=
    D0.Algebra.MovingProjectorTransport.inverse_commutes_of_commutes
      D A R hDA hRD hDR
  have hTraceCycle :
      Matrix.trace (R * (H * A)) = Matrix.trace (R * A * H) := by
    calc
      Matrix.trace (R * (H * A)) = Matrix.trace (A * (R * H)) := by
        simpa [mul_assoc] using Matrix.trace_mul_cycle R H A
      _ = Matrix.trace (R * A * H) := by
        calc
          Matrix.trace (A * (R * H)) = Matrix.trace ((A * R) * H) := by
            simp only [mul_assoc]
          _ = Matrix.trace ((R * A) * H) := by rw [← hRA]
          _ = Matrix.trace (R * A * H) := by simp only [mul_assoc]
  have hCore :
      Matrix.trace (R * (H - (p : ℂ) ^ 2 • (H * A + A * H))) =
        Matrix.trace (R * sourceCoefficient p A * H) := by
    calc
      Matrix.trace (R * (H - (p : ℂ) ^ 2 • (H * A + A * H))) =
          Matrix.trace (R * H) - (p : ℂ) ^ 2 * Matrix.trace (R * (H * A)) -
            (p : ℂ) ^ 2 * Matrix.trace (R * (A * H)) := by
              simp only [mul_sub, mul_smul_comm, mul_add, Matrix.trace_sub,
                Matrix.trace_smul, Matrix.trace_add]
              ring_nf
      _ = Matrix.trace (R * H) -
            (2 * (p : ℂ) ^ 2) * Matrix.trace (R * A * H) := by
              rw [hTraceCycle]
              simp only [Matrix.mul_assoc]
              ring
      _ = Matrix.trace (R * sourceCoefficient p A * H) := by
              dsimp [sourceCoefficient]
              simp only [mul_sub, sub_mul, smul_mul_assoc,
                mul_smul_comm, Matrix.trace_sub, Matrix.trace_smul]
              simp only [smul_eq_mul, mul_one]
  change Matrix.trace (R * ((4 * (p : ℂ) ^ 2) •
      (H - (p : ℂ) ^ 2 • (H * A + A * H)))) =
    (4 * (p : ℂ) ^ 2) * Matrix.trace (R * sourceCoefficient p A * H)
  rw [mul_smul_comm, Matrix.trace_smul, hCore]
  simp only [smul_eq_mul]

end D0.Algebra.DirectFeedbackSource

end
