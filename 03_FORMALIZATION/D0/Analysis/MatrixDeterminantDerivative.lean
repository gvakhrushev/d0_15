import Mathlib.Analysis.Calculus.FDeriv.Analytic
import Mathlib.Analysis.Calculus.Deriv.Comp
import Mathlib.Analysis.SpecialFunctions.Complex.LogDeriv
import Mathlib.Analysis.Matrix.Normed
import Mathlib.LinearAlgebra.Complex.FiniteDimensional
import Mathlib.LinearAlgebra.Matrix.Adjugate
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Topology.Instances.Matrix
import Mathlib.Topology.Algebra.Module.FiniteDimension
import Mathlib.Tactic

/-!
# The derivative of a finite complex matrix determinant

The determinant is treated as a continuous multilinear function of its rows.
The resulting derivative is first stated without invertibility as a sum of
row replacements. A separate algebraic calculation identifies that sum with
Jacobi's inverse-trace expression at an invertible matrix. The results concern
arbitrary real-parameter curves of finite complex matrices; they do not select
a physical field, action, or admitted variation.
-/

namespace D0.Analysis

noncomputable section

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- The ordinary determinant is continuous and multilinear in its rows. -/
def determinantRows : ContinuousMultilinearMap ℂ (fun _ : ι => ι → ℂ) ℂ where
  toMultilinearMap :=
    (Matrix.detRowAlternating : (ι → ℂ) [⋀^ι]→ₗ[ℂ] ℂ).toMultilinearMap
  cont := by
    change Continuous (fun M : Matrix ι ι ℂ => M.det)
    exact continuous_id.matrix_det

/-- The same determinant on Euclidean rows, regarded as real multilinear. -/
def euclideanDeterminantRows :
    ContinuousMultilinearMap ℝ (fun _ : ι => EuclideanSpace ℂ ι) ℂ :=
  (determinantRows.compContinuousLinearMap
    (fun _ => (EuclideanSpace.equiv ι ℂ).toContinuousLinearMap)).restrictScalars ℝ

@[simp] theorem euclideanDeterminantRows_apply (v : ι → EuclideanSpace ℂ ι) :
    euclideanDeterminantRows v = Matrix.det (fun i j => v i j) := by
  rfl

open scoped Matrix.Norms.Frobenius

/-- The continuous map that reads a Frobenius matrix as its Euclidean rows. -/
def matrixEuclideanRows : Matrix ι ι ℂ →L[ℝ] (ι → EuclideanSpace ℂ ι) :=
  ContinuousLinearMap.pi fun i =>
    ((EuclideanSpace.equiv ι ℂ).symm.toContinuousLinearMap.restrictScalars ℝ).comp
      (LinearMap.toContinuousLinearMap
        (LinearMap.proj i : Matrix ι ι ℂ →ₗ[ℝ] (ι → ℂ)))

omit [DecidableEq ι] in
@[simp] theorem matrixEuclideanRows_apply (A : Matrix ι ι ℂ) (i : ι) :
    matrixEuclideanRows A i = WithLp.toLp 2 (A i) := by
  rfl

@[simp] theorem euclideanDeterminantRows_matrixEuclideanRows (A : Matrix ι ι ℂ) :
    euclideanDeterminantRows (matrixEuclideanRows A) = A.det := by
  rfl

/--
The exact derivative of determinant along any differentiable complex-matrix
curve, before any invertibility assumption. The matrix uses the Frobenius norm.
-/
theorem hasDerivAt_matrix_det_rowUpdate
    (A : ℝ → Matrix ι ι ℂ) (H : Matrix ι ι ℂ) (t : ℝ)
    (hA : HasDerivAt A H t) :
    HasDerivAt (fun s => (A s).det)
      (∑ i : ι, ((A t).updateRow i (H i)).det) t := by
  have hRows : HasDerivAt (fun s => matrixEuclideanRows (A s))
      (matrixEuclideanRows H) t := by
    simpa only [Function.comp_def] using
      matrixEuclideanRows.hasFDerivAt.comp_hasDerivAt t hA
  have hDet :=
    (euclideanDeterminantRows.hasFDerivAt (matrixEuclideanRows (A t)))
      |>.comp_hasDerivAt t hRows
  have hFormula :
      euclideanDeterminantRows.linearDeriv (matrixEuclideanRows (A t))
          (matrixEuclideanRows H) =
        ∑ i : ι, ((A t).updateRow i (H i)).det := by
    rw [ContinuousMultilinearMap.linearDeriv_apply]
    apply Finset.sum_congr rfl
    intro i hi
    rw [euclideanDeterminantRows_apply]
    congr 1
    ext j k
    by_cases h : j = i
    · subst j
      simp [Matrix.updateRow]
    · simp [Matrix.updateRow, h]
  simpa only [Function.comp_def, euclideanDeterminantRows_matrixEuclideanRows,
    hFormula] using hDet

/--
For an invertible matrix, the row-replacement sum is the determinant times
the trace of the inverse applied to the variation.
-/
theorem matrix_det_rowUpdate_sum_eq_det_mul_trace
    (A H : Matrix ι ι ℂ) (hdet : IsUnit A.det) :
    (∑ i : ι, (A.updateRow i (H i)).det) =
      A.det * (A⁻¹ * H).trace := by
  let B : Matrix ι ι ℂ := H * A⁻¹
  have hBA : B * A = H := by
    dsimp [B]
    rw [Matrix.mul_assoc, Matrix.nonsing_inv_mul A hdet, Matrix.mul_one]
  have hRow : ∀ i : ι, H i = ∑ k : ι, B i k • A k := by
    intro i
    funext j
    have h := congrArg (fun X : Matrix ι ι ℂ => X i j) hBA
    simpa only [Matrix.mul_apply, Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
      using h.symm
  calc
    (∑ i : ι, (A.updateRow i (H i)).det) =
        ∑ i : ι, B i i * A.det := by
      apply Finset.sum_congr rfl
      intro i hi
      rw [hRow i]
      simpa only [smul_eq_mul] using
        Matrix.det_updateRow_sum A i (fun k => B i k)
    _ = A.det * (A⁻¹ * H).trace := by
      rw [Matrix.trace_mul_comm A⁻¹ H]
      change (∑ i : ι, B i i * A.det) = A.det * B.trace
      simp only [Matrix.trace, Matrix.diag_apply, ← Finset.sum_mul]
      ring

/-- Jacobi's derivative formula along a real-parameter complex-matrix curve. -/
theorem hasDerivAt_matrix_det_jacobi
    (A : ℝ → Matrix ι ι ℂ) (H : Matrix ι ι ℂ) (t : ℝ)
    (hA : HasDerivAt A H t) (hdet : IsUnit (A t).det) :
    HasDerivAt (fun s => (A s).det)
      ((A t).det * ((A t)⁻¹ * H).trace) t :=
  (hasDerivAt_matrix_det_rowUpdate A H t hA).congr_deriv
    (matrix_det_rowUpdate_sum_eq_det_mul_trace (A t) H hdet)

/--
The principal complex log-determinant derivative on the slit plane. The
slit-plane hypothesis supplies the nonzero determinant needed by Jacobi's
formula and the branch condition for `Complex.log`.
-/
theorem hasDerivAt_matrix_clogdet
    (A : ℝ → Matrix ι ι ℂ) (H : Matrix ι ι ℂ) (t : ℝ)
    (hA : HasDerivAt A H t) (hSlit : (A t).det ∈ Complex.slitPlane) :
    HasDerivAt (fun s => Complex.log ((A s).det))
      (((A t)⁻¹ * H).trace) t := by
  have hne : (A t).det ≠ 0 := Complex.slitPlane_ne_zero hSlit
  have hUnit : IsUnit (A t).det := isUnit_iff_ne_zero.mpr hne
  have hLog := (hasDerivAt_matrix_det_jacobi A H t hA hUnit).clog_real hSlit
  have hquot : ((A t).det * ((A t)⁻¹ * H).trace) / (A t).det =
      ((A t)⁻¹ * H).trace := by
    field_simp [hne]
  simpa only [hquot] using hLog

end

end D0.Analysis
