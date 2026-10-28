import D0.Algebra.MovingProjectorTransport
import D0.Analysis.MatrixDeterminantDerivative
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Star
import Mathlib.Analysis.Matrix.Normed
import Mathlib.LinearAlgebra.Matrix.Hermitian
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Trace

/-!
# Differentiable moving projectors and their cut

This module connects the owned algebraic moving-cut transport to actual
real-parameter differentiable curves. A locally idempotent curve supplies its
own tangent equation, and the derivative of the cut is obtained by the product
rule. The complex-matrix adapter uses the Frobenius norm and the same concrete
curves and derivatives throughout. The feedback log-determinant derivative
is proved only on its stated invertible, positive-determinant chart. The module
does not construct an admitted physical variation or the thermal and full-price
source.
-/

namespace D0.Algebra.MovingProjectorTransport

open Filter
open scoped Topology

section ReturnAlgebra

variable {A : Type*} [Ring A] [StarRing A]

/-- The cut return is the original projector-compressed return. -/
theorem cut_return_eq_projector_compression (P U : A)
    (hP : P * P = P) (hSelfAdjoint : star P = P) :
    star (cut P U) * cut P U = P * star U * (1 - P) * U * P := by
  have hQ : (1 - P) * (1 - P) = 1 - P := by
    calc
      (1 - P) * (1 - P) = 1 - P - P + P * P := by noncomm_ring
      _ = 1 - P := by rw [hP]; noncomm_ring
  calc
    star (cut P U) * cut P U =
        P * star U * ((1 - P) * (1 - P)) * U * P := by
          simp only [cut, star_mul, star_sub, star_one, hSelfAdjoint]
          noncomm_ring
    _ = P * star U * (1 - P) * U * P := by rw [hQ]

/--
For an anti-self-adjoint transport generator, the derivative of `C* C` minus
its common transport depends only on the relative derivative of `C`.
-/
theorem return_tangent_relative (C dC K : A) (hK : star K = -K) :
    (star dC * C + star C * dC) - comm K (star C * C) =
      star (dC - comm K C) * C + star C * (dC - comm K C) := by
  simp only [comm, star_sub, star_mul, hK]
  noncomm_ring

end ReturnAlgebra

section InverseAlgebra

variable {A : Type*} [Ring A]

/-- An inverse commutes with every element commuting with its original. -/
theorem inverse_commutes_of_commutes (B X S : A)
    (hBX : B * X = X * B) (hSB : S * B = 1) (hBS : B * S = 1) :
    S * X = X * S := by
  calc
    S * X = (S * X) * (B * S) := by rw [hBS, mul_one]
    _ = S * (X * B) * S := by simp only [mul_assoc]
    _ = S * (B * X) * S := by rw [hBX]
    _ = X * S := by simp only [← mul_assoc, hSB, one_mul]

end InverseAlgebra

section MatrixTrace

variable {ι 𝕜 : Type*} [Fintype ι] [DecidableEq ι] [CommRing 𝕜]

/-- A trace weight commuting with `F` annihilates a commutator of `F`. -/
theorem matrix_trace_mul_commutator_zero
    (R K F : Matrix ι ι 𝕜) (hRF : R * F = F * R) :
    Matrix.trace (R * comm K F) = 0 := by
  simp only [comm, mul_sub, Matrix.trace_sub, ← mul_assoc]
  rw [Matrix.trace_mul_cycle R K F, ← hRF, sub_self]

end MatrixTrace

section NormedAlgebra

variable {A : Type*} [NormedRing A] [NormedAlgebra ℝ A]

/-- Differentiating a locally idempotent curve gives its tangent equation. -/
theorem tangent_of_differentiable_projector
    {P : ℝ → A} {dP : A} {t : ℝ}
    (hP : HasDerivAt P dP t)
    (hIdem : ∀ᶠ s in 𝓝 t, P s * P s = P s) :
    P t * dP + dP * P t = dP := by
  have hSquare : HasDerivAt (fun s => P s * P s)
      (dP * P t + P t * dP) t := hP.mul hP
  have hSame : HasDerivAt (fun s => P s * P s) dP t :=
    hP.congr_of_eventuallyEq hIdem
  simpa [add_comm] using hSquare.unique hSame

/-- The literal moving cut has the derivative displayed by the product rule. -/
theorem hasDerivAt_moving_cut
    {P U : ℝ → A} {dP dU : A} {t : ℝ}
    (hP : HasDerivAt P dP t) (hU : HasDerivAt U dU t) :
    HasDerivAt (fun s => cut (P s) (U s))
      (cutTangent (P t) dP (U t) dU) t := by
  have hQ : HasDerivAt (fun s => 1 - P s) (-dP) t := by
    exact HasDerivAt.const_sub (1 : A) hP
  have hCut := (hQ.mul hU).mul hP
  simpa only [cut, cutTangent, add_mul] using hCut

/--
The same curve derivatives satisfy the exact relative-cut identity. Local
idempotence supplies both the pointwise projector and its tangent equation;
neither is an independent premise of the conclusion.
-/
theorem differentiable_moving_cut_relative
    {P U : ℝ → A} {dP dU : A} {t : ℝ}
    (hP : HasDerivAt P dP t) (hU : HasDerivAt U dU t)
    (hIdem : ∀ᶠ s in 𝓝 t, P s * P s = P s) :
    HasDerivAt (fun s => cut (P s) (U s))
        (cutTangent (P t) dP (U t) dU) t ∧
      comm (generator (P t) dP) (P t) = dP ∧
      cutTangent (P t) dP (U t) dU -
          comm (generator (P t) dP) (cut (P t) (U t)) =
        (1 - P t) * (dU - comm (generator (P t) dP) (U t)) * P t := by
  have hPoint : P t * P t = P t := hIdem.self_of_nhds
  have hTangent := tangent_of_differentiable_projector hP hIdem
  exact ⟨hasDerivAt_moving_cut hP hU,
    generator_transports (P t) dP hPoint hTangent,
    cut_relative (P t) dP (U t) dU hPoint hTangent⟩

section Star

variable [StarRing A] [StarModule ℝ A] [ContinuousStar A]

/-- The derivative of a locally self-adjoint real curve is self-adjoint. -/
theorem self_adjoint_tangent_of_curve
    {P : ℝ → A} {dP : A} {t : ℝ}
    (hP : HasDerivAt P dP t)
    (hSelfAdjoint : ∀ᶠ s in 𝓝 t, star (P s) = P s) :
    star dP = dP := by
  have hSame : HasDerivAt (fun s => star (P s)) dP t :=
    hP.congr_of_eventuallyEq hSelfAdjoint
  exact hP.star.unique hSame

/-- The canonical transport generator of such a curve is anti-self-adjoint. -/
theorem generator_anti_self_adjoint_of_curve
    {P : ℝ → A} {dP : A} {t : ℝ}
    (hP : HasDerivAt P dP t)
    (hSelfAdjoint : ∀ᶠ s in 𝓝 t, star (P s) = P s) :
    star (generator (P t) dP) = -generator (P t) dP :=
  generator_star_eq_neg (P t) dP hSelfAdjoint.self_of_nhds
    (self_adjoint_tangent_of_curve hP hSelfAdjoint)

/--
The original return `C* C` has its actual product-rule derivative, and its
relative derivative is built from the same moving-cut curve and generator.
-/
theorem differentiable_moving_return_relative
    {P U : ℝ → A} {dP dU : A} {t : ℝ}
    (hP : HasDerivAt P dP t) (hU : HasDerivAt U dU t)
    (hIdem : ∀ᶠ s in 𝓝 t, P s * P s = P s)
    (hSelfAdjoint : ∀ᶠ s in 𝓝 t, star (P s) = P s) :
    HasDerivAt (fun s => star (cut (P s) (U s)) * cut (P s) (U s))
        (star (cutTangent (P t) dP (U t) dU) * cut (P t) (U t) +
          star (cut (P t) (U t)) * cutTangent (P t) dP (U t) dU) t ∧
      (star (cutTangent (P t) dP (U t) dU) * cut (P t) (U t) +
          star (cut (P t) (U t)) * cutTangent (P t) dP (U t) dU) -
        comm (generator (P t) dP) (star (cut (P t) (U t)) * cut (P t) (U t)) =
      star ((1 - P t) * (dU - comm (generator (P t) dP) (U t)) * P t) *
          cut (P t) (U t) +
        star (cut (P t) (U t)) *
          ((1 - P t) * (dU - comm (generator (P t) dP) (U t)) * P t) := by
  have hCut := hasDerivAt_moving_cut hP hU
  refine ⟨hCut.star.mul hCut, ?_⟩
  have hRelative := (differentiable_moving_cut_relative hP hU hIdem).2.2
  rw [← hRelative]
  exact return_tangent_relative (cut (P t) (U t))
    (cutTangent (P t) dP (U t) dU) (generator (P t) dP)
    (generator_anti_self_adjoint_of_curve hP hSelfAdjoint)

end Star
end NormedAlgebra

section ComplexMatrix

open scoped Matrix.Norms.Frobenius

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- The actual nonsingular `1-zF` resolvent commutes with `F`. -/
theorem complex_matrix_resolvent_commutes
    (F : Matrix ι ι ℂ) (z : ℂ) (hInv : IsUnit (1 - z • F).det) :
    (1 - z • F)⁻¹ * F = F * (1 - z • F)⁻¹ := by
  let B : Matrix ι ι ℂ := 1 - z • F
  have hBF : B * F = F * B := by
    dsimp [B]
    simp only [sub_mul, mul_sub, one_mul, mul_one, smul_mul_assoc, mul_smul_comm]
  have hInvB : IsUnit B.det := hInv
  exact inverse_commutes_of_commutes B F B⁻¹ hBF
    (Matrix.nonsing_inv_mul B hInvB) (Matrix.mul_nonsing_inv B hInvB)

/-- For a self-adjoint scalar, the `1-z C* C` resolvent is self-adjoint. -/
theorem complex_matrix_feedback_resolvent_selfadjoint
    (C : Matrix ι ι ℂ) (z : ℂ) (hz : star z = z) :
    star ((1 - z • (star C * C))⁻¹) = (1 - z • (star C * C))⁻¹ := by
  have hF : (star C * C).IsHermitian := by
    simpa only [Matrix.star_eq_conjTranspose] using
      Matrix.isHermitian_conjTranspose_mul_self C
  have hB : (1 - z • (star C * C)).IsHermitian :=
    Matrix.isHermitian_one.sub (hF.smul hz)
  simpa only [Matrix.IsHermitian, Matrix.star_eq_conjTranspose] using hB.inv

/-- For real `z`, the determinant of the feedback matrix is real. -/
theorem complex_matrix_feedback_det_eq_real_part
    (C : Matrix ι ι ℂ) (z : ℝ) :
    (1 - (z : ℂ) • (star C * C)).det =
      (((1 - (z : ℂ) • (star C * C)).det.re : ℝ) : ℂ) := by
  let B : Matrix ι ι ℂ := 1 - (z : ℂ) • (star C * C)
  have hF : (star C * C).IsHermitian := by
    simpa only [Matrix.star_eq_conjTranspose] using
      Matrix.isHermitian_conjTranspose_mul_self C
  have hB : B.IsHermitian := Matrix.isHermitian_one.sub
    (hF.smul (by
      change star (z : ℂ) = (z : ℂ)
      simp only [Complex.star_def, Complex.conj_ofReal]))
  have hStar : star B.det = B.det := by
    have h := congrArg Matrix.det hB
    simpa only [Matrix.det_conjTranspose] using h
  have hIm : B.det.im = 0 := Complex.conj_eq_iff_im.mp (by
    simpa only [Complex.star_def] using hStar)
  change B.det = (B.det.re : ℂ)
  apply Complex.ext <;> simp [hIm]

/-- A self-adjoint trace weight pairs the two return variations as conjugates. -/
theorem complex_matrix_return_trace_eq_two_re
    (R C V : Matrix ι ι ℂ) (hR : star R = R) :
    Matrix.trace (R * (star V * C + star C * V)) =
      ((2 * (Matrix.trace (R * star C * V)).re : ℝ) : ℂ) := by
  have hConj : star (Matrix.trace (R * star C * V)) =
      Matrix.trace (R * star V * C) := by
    calc
      star (Matrix.trace (R * star C * V)) =
          Matrix.trace (star (R * star C * V)) := by
            simpa only [Matrix.star_eq_conjTranspose] using
              (Matrix.trace_conjTranspose (R * star C * V)).symm
      _ = Matrix.trace (star V * C * R) := by simp only [star_mul, star_star, hR, mul_assoc]
      _ = Matrix.trace (R * star V * C) := Matrix.trace_mul_cycle (star V) C R
  calc
    Matrix.trace (R * (star V * C + star C * V)) =
        Matrix.trace (R * star V * C) + Matrix.trace (R * star C * V) := by
          simp only [mul_add, Matrix.trace_add, mul_assoc]
    _ = star (Matrix.trace (R * star C * V)) + Matrix.trace (R * star C * V) := by
          rw [hConj]
    _ = ((2 * (Matrix.trace (R * star C * V)).re : ℝ) : ℂ) := by
          simpa only [Complex.star_def, add_comm] using
            Complex.add_conj (Matrix.trace (R * star C * V))

/--
Finite complex-matrix realization of the same derivative and transport,
including the anti-self-adjoint generator of a locally Hermitian curve.
The hypotheses describe the actual curves; no unitary or admission claim is
inferred from them.
-/
theorem complex_matrix_differentiable_moving_cut_relative
    {P U : ℝ → Matrix ι ι ℂ} {dP dU : Matrix ι ι ℂ} {t : ℝ}
    (hP : HasDerivAt P dP t) (hU : HasDerivAt U dU t)
    (hIdem : ∀ᶠ s in 𝓝 t, P s * P s = P s)
    (hSelfAdjoint : ∀ᶠ s in 𝓝 t, star (P s) = P s) :
    HasDerivAt (fun s => cut (P s) (U s))
        (cutTangent (P t) dP (U t) dU) t ∧
      comm (generator (P t) dP) (P t) = dP ∧
      cutTangent (P t) dP (U t) dU -
          comm (generator (P t) dP) (cut (P t) (U t)) =
        (1 - P t) * (dU - comm (generator (P t) dP) (U t)) * P t ∧
      star (generator (P t) dP) = -generator (P t) dP := by
  have hRelative := differentiable_moving_cut_relative hP hU hIdem
  exact ⟨hRelative.1, hRelative.2.1, hRelative.2.2,
    generator_anti_self_adjoint_of_curve hP hSelfAdjoint⟩

/--
On the actual complex-matrix curve, a weight commuting with the return
eliminates its common-transport commutator from the weighted first variation.
-/
theorem complex_matrix_moving_return_trace_relative
    {P U : ℝ → Matrix ι ι ℂ} {dP dU R : Matrix ι ι ℂ} {t : ℝ}
    (hP : HasDerivAt P dP t) (hU : HasDerivAt U dU t)
    (hIdem : ∀ᶠ s in 𝓝 t, P s * P s = P s)
    (hSelfAdjoint : ∀ᶠ s in 𝓝 t, star (P s) = P s)
    (hRF : R * (star (cut (P t) (U t)) * cut (P t) (U t)) =
      (star (cut (P t) (U t)) * cut (P t) (U t)) * R) :
    Matrix.trace (R *
        (star (cutTangent (P t) dP (U t) dU) * cut (P t) (U t) +
          star (cut (P t) (U t)) * cutTangent (P t) dP (U t) dU)) =
      Matrix.trace (R *
        (star ((1 - P t) * (dU - comm (generator (P t) dP) (U t)) * P t) *
            cut (P t) (U t) +
          star (cut (P t) (U t)) *
            ((1 - P t) * (dU - comm (generator (P t) dP) (U t)) * P t))) := by
  have hCancel := matrix_trace_mul_commutator_zero R (generator (P t) dP)
    (star (cut (P t) (U t)) * cut (P t) (U t)) hRF
  have hRelative := (differentiable_moving_return_relative hP hU hIdem hSelfAdjoint).2
  have hTrace := congrArg (fun X : Matrix ι ι ℂ => Matrix.trace (R * X)) hRelative
  simpa only [mul_sub, Matrix.trace_sub, hCancel, sub_zero] using hTrace

/-- The same curve's weighted return variation has the source's `2 Re` form. -/
theorem complex_matrix_moving_return_trace_two_re
    {P U : ℝ → Matrix ι ι ℂ} {dP dU R : Matrix ι ι ℂ} {t : ℝ}
    (hP : HasDerivAt P dP t) (hU : HasDerivAt U dU t)
    (hIdem : ∀ᶠ s in 𝓝 t, P s * P s = P s)
    (hSelfAdjoint : ∀ᶠ s in 𝓝 t, star (P s) = P s)
    (hRF : R * (star (cut (P t) (U t)) * cut (P t) (U t)) =
      (star (cut (P t) (U t)) * cut (P t) (U t)) * R)
    (hR : star R = R) :
    Matrix.trace (R *
        (star (cutTangent (P t) dP (U t) dU) * cut (P t) (U t) +
          star (cut (P t) (U t)) * cutTangent (P t) dP (U t) dU)) =
      ((2 * (Matrix.trace (R * star (cut (P t) (U t)) *
        ((1 - P t) * (dU - comm (generator (P t) dP) (U t)) * P t))).re : ℝ) : ℂ) := by
  calc
    _ = Matrix.trace (R *
        (star ((1 - P t) * (dU - comm (generator (P t) dP) (U t)) * P t) *
            cut (P t) (U t) +
          star (cut (P t) (U t)) *
            ((1 - P t) * (dU - comm (generator (P t) dP) (U t)) * P t))) :=
      complex_matrix_moving_return_trace_relative hP hU hIdem hSelfAdjoint hRF
    _ = _ := complex_matrix_return_trace_eq_two_re R (cut (P t) (U t))
      ((1 - P t) * (dU - comm (generator (P t) dP) (U t)) * P t) hR

/--
The actual invertible feedback resolvent yields the moving-cut `2 Re` trace
identity. This is the algebraic trace step; no log-determinant derivative is
assumed or asserted.
-/
theorem complex_matrix_feedback_resolvent_moving_return_two_re
    {P U : ℝ → Matrix ι ι ℂ} {dP dU : Matrix ι ι ℂ} {t : ℝ} (z : ℂ)
    (hP : HasDerivAt P dP t) (hU : HasDerivAt U dU t)
    (hIdem : ∀ᶠ s in 𝓝 t, P s * P s = P s)
    (hSelfAdjoint : ∀ᶠ s in 𝓝 t, star (P s) = P s)
    (hz : star z = z)
    (hInv : IsUnit (1 - z • (star (cut (P t) (U t)) * cut (P t) (U t))).det) :
    let C := cut (P t) (U t)
    let R := (1 - z • (star C * C))⁻¹
    Matrix.trace (R *
        (star (cutTangent (P t) dP (U t) dU) * C +
          star C * cutTangent (P t) dP (U t) dU)) =
      ((2 * (Matrix.trace (R * star C *
        ((1 - P t) * (dU - comm (generator (P t) dP) (U t)) * P t))).re : ℝ) : ℂ) := by
  dsimp only
  apply complex_matrix_moving_return_trace_two_re hP hU hIdem hSelfAdjoint
  · exact complex_matrix_resolvent_commutes _ z hInv
  · exact complex_matrix_feedback_resolvent_selfadjoint _ z hz

/--
The principal complex feedback log-determinant has the original moving-cut
first derivative on its actual differentiable curve. The slit-plane premise
provides both invertibility and the branch condition. It is not an admission
or a proof of the thermal contribution.
-/
theorem complex_matrix_feedback_logdet_hasDerivAt
    {P U : ℝ → Matrix ι ι ℂ} {dP dU : Matrix ι ι ℂ} {t : ℝ} (z : ℂ)
    (hP : HasDerivAt P dP t) (hU : HasDerivAt U dU t)
    (hIdem : ∀ᶠ s in 𝓝 t, P s * P s = P s)
    (hSelfAdjoint : ∀ᶠ s in 𝓝 t, star (P s) = P s)
    (hz : star z = z)
    (hSlit : (1 - z • (star (cut (P t) (U t)) * cut (P t) (U t))).det ∈
      Complex.slitPlane) :
    let C := cut (P t) (U t)
    let R := (1 - z • (star C * C))⁻¹
    let V := (1 - P t) * (dU - comm (generator (P t) dP) (U t)) * P t
    HasDerivAt
      (fun s => -Complex.log
        ((1 - z • (star (cut (P s) (U s)) * cut (P s) (U s))).det))
      (z * ((2 * (Matrix.trace (R * star C * V)).re : ℝ) : ℂ)) t := by
  let C := cut (P t) (U t)
  let dC := cutTangent (P t) dP (U t) dU
  let dF := star dC * C + star C * dC
  let V := (1 - P t) * (dU - comm (generator (P t) dP) (U t)) * P t
  let A : ℝ → Matrix ι ι ℂ := fun s =>
    1 - z • (star (cut (P s) (U s)) * cut (P s) (U s))
  have hF : HasDerivAt (fun s => star (cut (P s) (U s)) * cut (P s) (U s))
      dF t := by
    exact (differentiable_moving_return_relative hP hU hIdem hSelfAdjoint).1
  have hZF := HasDerivAt.const_smul z hF
  have hA : HasDerivAt A (-(z • dF)) t := HasDerivAt.const_sub 1 hZF
  have hLog := D0.Analysis.hasDerivAt_matrix_clogdet A (-(z • dF)) t hA hSlit
  have hInv : IsUnit (A t).det := isUnit_iff_ne_zero.mpr (Complex.slitPlane_ne_zero hSlit)
  have hTrace : Matrix.trace ((A t)⁻¹ * dF) =
      ((2 * (Matrix.trace ((A t)⁻¹ * star C * V)).re : ℝ) : ℂ) := by
    exact complex_matrix_feedback_resolvent_moving_return_two_re z
      hP hU hIdem hSelfAdjoint hz hInv
  have hDerivative : -Matrix.trace ((A t)⁻¹ * (-(z • dF))) =
      z * ((2 * (Matrix.trace ((A t)⁻¹ * star C * V)).re : ℝ) : ℂ) := by
    simp only [mul_neg, mul_smul_comm, Matrix.trace_neg, Matrix.trace_smul,
      neg_neg, smul_eq_mul]
    rw [hTrace]
  change HasDerivAt (fun s => -Complex.log ((A s).det))
    (z * ((2 * (Matrix.trace ((A t)⁻¹ * star C * V)).re : ℝ) : ℂ)) t
  exact (HasDerivAt.neg hLog).congr_deriv hDerivative

/--
For real `z`, the same result differentiates the real log absolute
determinant; on a positive-determinant chart this is the original real
feedback term.
-/
theorem complex_matrix_feedback_real_logabsdet_hasDerivAt
    {P U : ℝ → Matrix ι ι ℂ} {dP dU : Matrix ι ι ℂ} {t : ℝ} (z : ℝ)
    (hP : HasDerivAt P dP t) (hU : HasDerivAt U dU t)
    (hIdem : ∀ᶠ s in 𝓝 t, P s * P s = P s)
    (hSelfAdjoint : ∀ᶠ s in 𝓝 t, star (P s) = P s)
    (hSlit : (1 - (z : ℂ) •
      (star (cut (P t) (U t)) * cut (P t) (U t))).det ∈ Complex.slitPlane) :
    let C := cut (P t) (U t)
    let R := (1 - (z : ℂ) • (star C * C))⁻¹
    let V := (1 - P t) * (dU - comm (generator (P t) dP) (U t)) * P t
    HasDerivAt
      (fun s => -Real.log ‖(1 - (z : ℂ) •
        (star (cut (P s) (U s)) * cut (P s) (U s))).det‖)
      (z * (2 * (Matrix.trace (R * star C * V)).re)) t := by
  have hComplex := complex_matrix_feedback_logdet_hasDerivAt (z : ℂ)
    hP hU hIdem hSelfAdjoint (by simp) hSlit
  have hReal := Complex.reCLM.hasFDerivAt.comp_hasDerivAt t hComplex
  simpa only [Function.comp_def, Complex.reCLM_apply, Complex.neg_re, Complex.log_re,
    ← Complex.ofReal_mul, Complex.ofReal_re] using hReal

/--
On a locally positive real-determinant chart, the real Book03 feedback term
itself has the moving-cut derivative. Positivity is a chart hypothesis here;
it is not inferred from a named physical execution.
-/
theorem complex_matrix_feedback_real_logdet_hasDerivAt
    {P U : ℝ → Matrix ι ι ℂ} {dP dU : Matrix ι ι ℂ} {t : ℝ} (z : ℝ)
    (hP : HasDerivAt P dP t) (hU : HasDerivAt U dU t)
    (hIdem : ∀ᶠ s in 𝓝 t, P s * P s = P s)
    (hSelfAdjoint : ∀ᶠ s in 𝓝 t, star (P s) = P s)
    (hPositive : ∀ᶠ s in 𝓝 t, ∃ q : ℝ, 0 < q ∧
      (1 - (z : ℂ) • (star (cut (P s) (U s)) * cut (P s) (U s))).det = (q : ℂ)) :
    let C := cut (P t) (U t)
    let R := (1 - (z : ℂ) • (star C * C))⁻¹
    let V := (1 - P t) * (dU - comm (generator (P t) dP) (U t)) * P t
    HasDerivAt
      (fun s => -Real.log ((1 - (z : ℂ) •
        (star (cut (P s) (U s)) * cut (P s) (U s))).det.re))
      (z * (2 * (Matrix.trace (R * star C * V)).re)) t := by
  have hSlit : (1 - (z : ℂ) •
      (star (cut (P t) (U t)) * cut (P t) (U t))).det ∈ Complex.slitPlane := by
    rcases hPositive.self_of_nhds with ⟨q, hq, hqeq⟩
    rw [hqeq]
    exact Complex.ofReal_mem_slitPlane.mpr hq
  have hReal := complex_matrix_feedback_real_logabsdet_hasDerivAt z
    hP hU hIdem hSelfAdjoint hSlit
  have hFunctions :
      (fun s => -Real.log ((1 - (z : ℂ) •
        (star (cut (P s) (U s)) * cut (P s) (U s))).det.re)) =ᶠ[𝓝 t]
      (fun s => -Real.log ‖(1 - (z : ℂ) •
        (star (cut (P s) (U s)) * cut (P s) (U s))).det‖) := by
    filter_upwards [hPositive] with s hs
    rcases hs with ⟨q, hq, hqeq⟩
    rw [hqeq]
    simp [Real.norm_eq_abs, abs_of_pos hq]
  exact hReal.congr_of_eventuallyEq hFunctions

/--
For a differentiable curve and real `z`, a slit-plane determinant at one
point is positive and remains so locally: the feedback matrix is Hermitian
and its determinant is continuous.
-/
theorem complex_matrix_feedback_positive_near
    {P U : ℝ → Matrix ι ι ℂ} {dP dU : Matrix ι ι ℂ} {t : ℝ} (z : ℝ)
    (hP : HasDerivAt P dP t) (hU : HasDerivAt U dU t)
    (hSlit : (1 - (z : ℂ) •
      (star (cut (P t) (U t)) * cut (P t) (U t))).det ∈ Complex.slitPlane) :
    ∀ᶠ s in 𝓝 t, ∃ q : ℝ, 0 < q ∧
      (1 - (z : ℂ) • (star (cut (P s) (U s)) * cut (P s) (U s))).det = (q : ℂ) := by
  let A : ℝ → Matrix ι ι ℂ := fun s =>
    1 - (z : ℂ) • (star (cut (P s) (U s)) * cut (P s) (U s))
  let dC := cutTangent (P t) dP (U t) dU
  let C := cut (P t) (U t)
  let dF := star dC * C + star C * dC
  have hCut := hasDerivAt_moving_cut hP hU
  have hF : HasDerivAt (fun s => star (cut (P s) (U s)) * cut (P s) (U s))
      dF t := hCut.star.mul hCut
  have hA : HasDerivAt A (-((z : ℂ) • dF)) t :=
    HasDerivAt.const_sub 1 (HasDerivAt.const_smul (z : ℂ) hF)
  have hDet := D0.Analysis.hasDerivAt_matrix_det_rowUpdate A (-((z : ℂ) • dF)) t hA
  have hCont : ContinuousAt (fun s => (A s).det.re) t :=
    Complex.continuous_re.continuousAt.comp hDet.continuousAt
  have hRealAt : (A t).det = ((A t).det.re : ℂ) :=
    complex_matrix_feedback_det_eq_real_part (cut (P t) (U t)) z
  have hAtPositive : 0 < (A t).det.re := by
    change (A t).det ∈ Complex.slitPlane at hSlit
    rw [hRealAt, Complex.ofReal_mem_slitPlane] at hSlit
    exact hSlit
  have hEventually : ∀ᶠ s in 𝓝 t, 0 < (A s).det.re :=
    hCont.eventually (Ioi_mem_nhds hAtPositive)
  filter_upwards [hEventually] with s hs
  refine ⟨(A s).det.re, hs, ?_⟩
  exact complex_matrix_feedback_det_eq_real_part (cut (P s) (U s)) z

/-- The positive-chart premise follows from a slit-plane point on the same curve. -/
theorem complex_matrix_feedback_real_logdet_of_slit_hasDerivAt
    {P U : ℝ → Matrix ι ι ℂ} {dP dU : Matrix ι ι ℂ} {t : ℝ} (z : ℝ)
    (hP : HasDerivAt P dP t) (hU : HasDerivAt U dU t)
    (hIdem : ∀ᶠ s in 𝓝 t, P s * P s = P s)
    (hSelfAdjoint : ∀ᶠ s in 𝓝 t, star (P s) = P s)
    (hSlit : (1 - (z : ℂ) •
      (star (cut (P t) (U t)) * cut (P t) (U t))).det ∈ Complex.slitPlane) :
    let C := cut (P t) (U t)
    let R := (1 - (z : ℂ) • (star C * C))⁻¹
    let V := (1 - P t) * (dU - comm (generator (P t) dP) (U t)) * P t
    HasDerivAt
      (fun s => -Real.log ((1 - (z : ℂ) •
        (star (cut (P s) (U s)) * cut (P s) (U s))).det.re))
      (z * (2 * (Matrix.trace (R * star C * V)).re)) t :=
  complex_matrix_feedback_real_logdet_hasDerivAt z hP hU hIdem hSelfAdjoint
    (complex_matrix_feedback_positive_near z hP hU hSlit)

end ComplexMatrix

section ConcreteMovingCut

open scoped Matrix.Norms.Frobenius
noncomputable section

/-- A concrete complex two-dimensional projector curve and fixed unitary. -/
def exampleProjectorBase : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, 0]
def exampleProjectorVelocity : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 1, 0]
def exampleProjectorOther : Matrix (Fin 2) (Fin 2) ℂ := !![0, 0; 0, 1]
def exampleReflection : Matrix (Fin 2) (Fin 2) ℂ := !![3 / 5, 4 / 5; 4 / 5, -(3 / 5)]
def exampleCutAtZero : Matrix (Fin 2) (Fin 2) ℂ := !![0, 0; 4 / 5, 0]
def exampleCutVelocity : Matrix (Fin 2) (Fin 2) ℂ := !![-(4 / 5), 0; -(6 / 5), 4 / 5]
def exampleReturnVelocity : Matrix (Fin 2) (Fin 2) ℂ :=
  !![-(48 / 25), 16 / 25; 16 / 25, 0]
def exampleResolvent : Matrix (Fin 2) (Fin 2) ℂ := !![25 / 17, 0; 0, 1]

def exampleProjector (t : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  ((1 + t ^ 2)⁻¹ : ℝ) •
    (exampleProjectorBase + t • exampleProjectorVelocity + t ^ 2 • exampleProjectorOther)

/-- The displayed curve consists of orthogonal projectors at every real time. -/
theorem exampleProjector_idempotent (t : ℝ) :
    exampleProjector t * exampleProjector t = exampleProjector t := by
  have hn : (1 + t ^ 2 : ℝ) ≠ 0 := by positivity
  have hnC : (1 + (t : ℂ) ^ 2) ≠ 0 := by exact_mod_cast hn
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [exampleProjector, exampleProjectorBase, exampleProjectorVelocity,
      exampleProjectorOther, Matrix.mul_apply, Fin.sum_univ_two, Complex.real_smul,
      Complex.ofReal_inv, Complex.ofReal_add, Complex.ofReal_pow] <;>
    field_simp [hnC]

theorem exampleProjector_selfadjoint (t : ℝ) :
    star (exampleProjector t) = exampleProjector t := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [exampleProjector, exampleProjectorBase, exampleProjectorVelocity,
      exampleProjectorOther, Matrix.star_apply, Complex.real_smul]

theorem exampleProjector_trace (t : ℝ) : Matrix.trace (exampleProjector t) = 1 := by
  have hn : (1 + t ^ 2 : ℝ) ≠ 0 := by positivity
  have hnC : (1 + (t : ℂ) ^ 2) ≠ 0 := by exact_mod_cast hn
  simp [Matrix.trace, Fin.sum_univ_two, exampleProjector, exampleProjectorBase,
    exampleProjectorVelocity, exampleProjectorOther, Complex.real_smul,
    Complex.ofReal_inv, Complex.ofReal_add, Complex.ofReal_pow]
  field_simp [hnC]

/-- The entire curve has the same rank-one active space dimension. -/
theorem exampleProjector_rank_one (t : ℝ) : (exampleProjector t).rank = 1 := by
  let A := exampleProjector t
  have he : IsIdempotentElem A.toLin' := by
    change A.toLin' * A.toLin' = A.toLin'
    rw [Module.End.mul_eq_comp, ← Matrix.toLin'_mul, exampleProjector_idempotent t]
  have hp : LinearMap.IsProj (LinearMap.range A.toLin') A.toLin' :=
    (LinearMap.isProj_range_iff_isIdempotentElem _).2 he
  have htrace := hp.trace
  rw [Matrix.trace_toLin'_eq] at htrace
  have hrank : Module.finrank ℂ (LinearMap.range A.toLin') = A.rank := by
    rw [Matrix.toLin'_apply']
    rfl
  rw [hrank] at htrace
  have htr : A.trace = 1 := exampleProjector_trace t
  rw [htr] at htrace
  exact_mod_cast htrace.symm

/-- Its genuine derivative at zero is the nonzero off-diagonal matrix. -/
theorem exampleProjector_hasDerivAt :
    HasDerivAt exampleProjector exampleProjectorVelocity 0 := by
  have hid : HasDerivAt (fun t : ℝ => t) 1 0 := hasDerivAt_id' 0
  have hsq : HasDerivAt (fun t : ℝ => t ^ 2) 0 0 := by
    simpa using hid.pow 2
  have hden : HasDerivAt (fun t : ℝ => 1 + t ^ 2) 0 0 := by
    exact (hasDerivAt_const_add_iff (1 : ℝ)).2 hsq
  have hinv : HasDerivAt (fun t : ℝ => (1 + t ^ 2)⁻¹) 0 0 := by
    have h := hden.inv (by norm_num)
    simpa using h
  have hnum : HasDerivAt
      (fun t : ℝ => exampleProjectorBase + t • exampleProjectorVelocity +
        t ^ 2 • exampleProjectorOther) exampleProjectorVelocity 0 := by
    have ha := hasDerivAt_const (0 : ℝ) exampleProjectorBase
    have hb := hid.smul_const exampleProjectorVelocity
    have hc := hsq.smul_const exampleProjectorOther
    simpa using (ha.add hb).add hc
  have h := hinv.smul hnum
  simpa [exampleProjector] using h

theorem exampleReflection_unitary :
    star exampleReflection * exampleReflection = 1 ∧
      exampleReflection * star exampleReflection = 1 := by
  constructor <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    norm_num [exampleReflection, Matrix.star_apply, Matrix.mul_apply,
      Fin.sum_univ_two, Matrix.one_apply] <;> simp only [map_ofNat] <;> norm_num

theorem example_cut_tangent :
    cutTangent (exampleProjector 0) exampleProjectorVelocity exampleReflection 0 =
      exampleCutVelocity := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [cutTangent, exampleProjector, exampleProjectorBase,
      exampleProjectorVelocity, exampleProjectorOther, exampleReflection,
      exampleCutVelocity, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_apply]

theorem example_cut_at_zero :
    cut (exampleProjector 0) exampleReflection = exampleCutAtZero := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [cut, exampleProjector, exampleProjectorBase, exampleProjectorVelocity,
      exampleProjectorOther, exampleReflection, exampleCutAtZero, Matrix.mul_apply,
      Fin.sum_univ_two, Matrix.one_apply]

theorem example_return_tangent :
    star exampleCutVelocity * exampleCutAtZero + star exampleCutAtZero * exampleCutVelocity =
      exampleReturnVelocity := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [exampleCutVelocity, exampleCutAtZero, exampleReturnVelocity,
      Matrix.star_apply, Matrix.mul_apply, Fin.sum_univ_two] <;>
    simp only [map_ofNat] <;> norm_num

theorem example_feedback_resolvent :
    (1 - (1 / 2 : ℂ) • (star exampleCutAtZero * exampleCutAtZero))⁻¹ =
      exampleResolvent := by
  apply Matrix.inv_eq_left_inv
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [exampleCutAtZero, exampleResolvent, Matrix.star_apply, Matrix.mul_apply,
      Fin.sum_univ_two, Matrix.one_apply]
  simp only [map_ofNat]
  norm_num

theorem example_weighted_return_trace :
    Matrix.trace (exampleResolvent * exampleReturnVelocity) = -(48 / 17 : ℂ) := by
  norm_num [Matrix.trace, exampleResolvent, exampleReturnVelocity, Matrix.mul_apply,
    Fin.sum_univ_two]

theorem example_feedback_det_at_zero :
    (1 - (1 / 2 : ℂ) • (star exampleCutAtZero * exampleCutAtZero)).det = (17 / 25 : ℂ) := by
  rw [Matrix.det_fin_two]
  norm_num [exampleCutAtZero, Matrix.star_apply, Matrix.mul_apply,
    Fin.sum_univ_two, Matrix.one_apply]
  simp only [map_ofNat]
  norm_num

theorem example_feedback_det_slit :
    (1 - (1 / 2 : ℂ) • (star exampleCutAtZero * exampleCutAtZero)).det ∈ Complex.slitPlane := by
  rw [example_feedback_det_at_zero]
  norm_num [Complex.mem_slitPlane_iff]

theorem example_cut_velocity_ne_zero : exampleCutVelocity ≠ 0 := by
  intro h
  have hEntry := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℂ => M 1 0) h
  norm_num [exampleCutVelocity] at hEntry

theorem example_return_velocity_ne_zero : exampleReturnVelocity ≠ 0 := by
  intro h
  have hEntry := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℂ => M 0 0) h
  norm_num [exampleReturnVelocity] at hEntry

/--
This actual projector curve and fixed unitary consume the generic moving-cut
theorem. Their cut has the displayed nonzero derivative even though `U` is
constant. No claim about the derivative of the physical price follows here.
-/
theorem example_moving_cut_has_nonzero_derivative :
    HasDerivAt (fun t => cut (exampleProjector t) exampleReflection)
        exampleCutVelocity 0 ∧ exampleCutVelocity ≠ 0 := by
  have hIdem : ∀ᶠ t in 𝓝 (0 : ℝ),
      exampleProjector t * exampleProjector t = exampleProjector t :=
    Filter.Eventually.of_forall exampleProjector_idempotent
  have hU : HasDerivAt (fun _ : ℝ => exampleReflection) 0 0 :=
    hasDerivAt_const 0 exampleReflection
  have hCut := (differentiable_moving_cut_relative exampleProjector_hasDerivAt hU hIdem).1
  exact ⟨by simpa only [example_cut_tangent] using hCut, example_cut_velocity_ne_zero⟩

/-- The same actual curve has a nonzero derivative of the return `C* C`. -/
theorem example_moving_return_has_nonzero_derivative :
    HasDerivAt (fun t => star (cut (exampleProjector t) exampleReflection) *
        cut (exampleProjector t) exampleReflection) exampleReturnVelocity 0 ∧
      exampleReturnVelocity ≠ 0 := by
  have hIdem : ∀ᶠ t in 𝓝 (0 : ℝ),
      exampleProjector t * exampleProjector t = exampleProjector t :=
    Filter.Eventually.of_forall exampleProjector_idempotent
  have hSelf : ∀ᶠ t in 𝓝 (0 : ℝ), star (exampleProjector t) = exampleProjector t :=
    Filter.Eventually.of_forall exampleProjector_selfadjoint
  have hU : HasDerivAt (fun _ : ℝ => exampleReflection) 0 0 :=
    hasDerivAt_const 0 exampleReflection
  have hReturn :=
    (differentiable_moving_return_relative exampleProjector_hasDerivAt hU hIdem hSelf).1
  exact ⟨by simpa only [example_cut_tangent, example_cut_at_zero, example_return_tangent]
    using hReturn, example_return_velocity_ne_zero⟩

/-- The same curve yields the exact feedback derivative at `z = 1/2`. -/
theorem example_feedback_logdet_hasDerivAt :
    HasDerivAt
      (fun t => -Real.log ((1 - (1 / 2 : ℂ) •
        (star (cut (exampleProjector t) exampleReflection) *
          cut (exampleProjector t) exampleReflection)).det.re))
      (-(24 / 17 : ℝ)) 0 := by
  have hIdem : ∀ᶠ t in 𝓝 (0 : ℝ),
      exampleProjector t * exampleProjector t = exampleProjector t :=
    Filter.Eventually.of_forall exampleProjector_idempotent
  have hSelf : ∀ᶠ t in 𝓝 (0 : ℝ), star (exampleProjector t) = exampleProjector t :=
    Filter.Eventually.of_forall exampleProjector_selfadjoint
  have hU : HasDerivAt (fun _ : ℝ => exampleReflection) 0 0 :=
    hasDerivAt_const 0 exampleReflection
  have hSlit : (1 - ((1 / 2 : ℝ) : ℂ) •
      (star (cut (exampleProjector 0) exampleReflection) *
        cut (exampleProjector 0) exampleReflection)).det ∈ Complex.slitPlane := by
    simpa only [example_cut_at_zero, Complex.ofReal_div, Complex.ofReal_one,
      Complex.ofReal_ofNat] using example_feedback_det_slit
  have h := complex_matrix_feedback_real_logdet_of_slit_hasDerivAt (1 / 2 : ℝ)
    exampleProjector_hasDerivAt hU hIdem hSelf hSlit
  have hv : (1 / 2 : ℝ) * (2 * (Matrix.trace
      ((1 - ((1 / 2 : ℝ) : ℂ) • (star (cut (exampleProjector 0) exampleReflection) *
          cut (exampleProjector 0) exampleReflection))⁻¹ *
        star (cut (exampleProjector 0) exampleReflection) *
        ((1 - exampleProjector 0) *
          (0 - comm (generator (exampleProjector 0) exampleProjectorVelocity)
            exampleReflection) * exampleProjector 0))).re) = -(24 / 17 : ℝ) := by
    rw [example_cut_at_zero]
    norm_num only [Complex.ofReal_div, Complex.ofReal_one, Complex.ofReal_ofNat]
    rw [example_feedback_resolvent]
    norm_num [exampleProjector,
      exampleProjectorBase, exampleProjectorVelocity, exampleProjectorOther,
      exampleReflection, exampleCutAtZero, exampleResolvent, comm, generator,
      Matrix.trace, Matrix.star_apply, Matrix.mul_apply, Matrix.vecMul, dotProduct,
      Fin.sum_univ_two,
      Matrix.one_apply]
    simp only [map_ofNat]
    norm_num
  dsimp only at h
  rw [hv] at h
  simpa only [Complex.ofReal_div, Complex.ofReal_one, Complex.ofReal_ofNat] using h

end
end ConcreteMovingCut

end D0.Algebra.MovingProjectorTransport
