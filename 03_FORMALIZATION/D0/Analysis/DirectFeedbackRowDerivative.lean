import D0.Algebra.DirectFeedbackSource
import Mathlib.Analysis.Calculus.Deriv.Star

/-!
# The original row's feedback derivative

Scoped adapter for the direct feedback source of the existing #334 §7cx
owner at `46ebed17ddfa04faa8ab1a07a6a822b717f993ef`, source blob
`b71d07b8247ef35ef38bf8930a1c17f2ff8f5caf`. It binds a differentiable
row `a` to `A = a†a`, the actual noncommuting jet, and the matrix
log-determinant theorem. No inverse of `A` or commutation with its tangent
is used. It does not construct an admitted physical execution, full Book
price, 42-field source, gain, refinement, or physical GR.
-/

namespace D0.Analysis.DirectFeedbackRowDerivative

open Filter D0.Algebra.DirectFeedbackSource
open scoped Topology Matrix.Norms.Frobenius
noncomputable section

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def rowGram (a : Matrix ι ι ℂ) : Matrix ι ι ℂ := star a * a
def rowGramJet (a da : Matrix ι ι ℂ) : Matrix ι ι ℂ := star da * a + star a * da

theorem rowGram_hasDerivAt {a : ℝ → Matrix ι ι ℂ}
    {da : Matrix ι ι ℂ} {t : ℝ} (ha : HasDerivAt a da t) :
    HasDerivAt (fun s => rowGram (a s)) (rowGramJet (a t) da) t := by
  simpa [rowGram, rowGramJet] using ha.star.mul ha

theorem returnOperator_hasDerivAt (p : ℝ) {a : ℝ → Matrix ι ι ℂ}
    {da : Matrix ι ι ℂ} {t : ℝ} (ha : HasDerivAt a da t) :
    HasDerivAt (fun s => returnOperator p (rowGram (a s)))
      (returnJet p (rowGram (a t)) (rowGramJet (a t) da)) t := by
  have hA := rowGram_hasDerivAt ha
  have hAA := hA.mul hA
  have h := (hA.sub (hAA.const_smul ((p : ℂ) ^ 2))).const_smul (4 * (p : ℂ) ^ 2)
  simpa [returnOperator, returnJet] using h

theorem feedbackPencil_hasDerivAt (p z : ℝ) {a : ℝ → Matrix ι ι ℂ}
    {da : Matrix ι ι ℂ} {t : ℝ} (ha : HasDerivAt a da t) :
    HasDerivAt (fun s => feedbackPencil p z (rowGram (a s)))
      (-((z : ℂ) • returnJet p (rowGram (a t)) (rowGramJet (a t) da))) t := by
  have h := ((returnOperator_hasDerivAt p ha).const_smul (z : ℂ)).const_sub 1
  simpa [feedbackPencil] using h

/-- Actual first feedback source along the row, including both row jets.
The slit-plane condition is on the feedback pencil, not on `a` or `A`. -/
theorem direct_row_feedback_hasDerivAt (p z : ℝ) {a : ℝ → Matrix ι ι ℂ}
    {da : Matrix ι ι ℂ} {t : ℝ} (ha : HasDerivAt a da t)
    (hSlit : (feedbackPencil p z (rowGram (a t))).det ∈ Complex.slitPlane) :
    HasDerivAt
      (fun s => -(Complex.log ((feedbackPencil p z (rowGram (a s))).det)).re)
      (4 * z * p ^ 2 *
        (Matrix.trace ((feedbackPencil p z (rowGram (a t)))⁻¹ *
          sourceCoefficient p (rowGram (a t)) * rowGramJet (a t) da)).re) t := by
  let A := rowGram (a t)
  let H := rowGramJet (a t) da
  let D := feedbackPencil p z A
  let Fjet := returnJet p A H
  have hpencil := feedbackPencil_hasDerivAt p z ha
  have hlog := D0.Analysis.hasDerivAt_matrix_clogdet
    (fun s => feedbackPencil p z (rowGram (a s))) (-((z : ℂ) • Fjet)) t hpencil hSlit
  have hreal := Complex.reCLM.hasFDerivAt.comp_hasDerivAt t hlog.neg
  have hunit : IsUnit D.det := isUnit_iff_ne_zero.mpr (Complex.slitPlane_ne_zero hSlit)
  have htrace := trace_resolvent_returnJet_eq_sourceCoefficient p z A H hunit
  have hvalue : (-Matrix.trace (D⁻¹ * (-((z : ℂ) • Fjet)))).re =
      4 * z * p ^ 2 * (Matrix.trace (D⁻¹ * sourceCoefficient p A * H)).re := by
    simp only [mul_neg, mul_smul_comm, Matrix.trace_neg, Matrix.trace_smul,
      neg_neg, smul_eq_mul]
    rw [htrace]
    simp [← Complex.ofReal_pow, Complex.mul_re, D]
    ring
  have hreal' : HasDerivAt
      (fun s => -(Complex.log ((feedbackPencil p z (rowGram (a s))).det)).re)
      (-Matrix.trace (D⁻¹ * (-((z : ℂ) • Fjet)))).re t := by
    simpa only [Function.comp_def, Complex.reCLM_apply, Pi.neg_apply, Complex.neg_re,
      D, A, H, Fjet] using hreal
  exact hreal'.congr_deriv hvalue

/-- The original row pencil has a real determinant for real `p` and `z`. -/
theorem feedbackPencil_det_real (p z : ℝ) (a : Matrix ι ι ℂ) :
    (feedbackPencil p z (rowGram a)).det =
      (((feedbackPencil p z (rowGram a)).det.re : ℝ) : ℂ) := by
  let A := rowGram a
  have hA : A.IsHermitian := by
    simpa only [A, rowGram, Matrix.star_eq_conjTranspose] using
      Matrix.isHermitian_conjTranspose_mul_self a
  have hAA : (A * A).IsHermitian := by
    simpa only [hA.eq] using Matrix.isHermitian_conjTranspose_mul_self A
  have hp : star ((p : ℂ) ^ 2) = (p : ℂ) ^ 2 := by simp
  have h4 : star (4 * (p : ℂ) ^ 2) = 4 * (p : ℂ) ^ 2 := by simp
  have hz : star (z : ℂ) = (z : ℂ) := by simp
  have hB : (feedbackPencil p z A).IsHermitian := by
    simpa only [feedbackPencil, returnOperator] using
      Matrix.isHermitian_one.sub (((hA.sub (hAA.smul hp)).smul h4).smul hz)
  have hStar : star (feedbackPencil p z A).det = (feedbackPencil p z A).det := by
    have h := congrArg Matrix.det hB
    simpa only [Matrix.det_conjTranspose] using h
  have hIm : (feedbackPencil p z A).det.im = 0 := Complex.conj_eq_iff_im.mp (by
    simpa only [Complex.star_def] using hStar)
  change (feedbackPencil p z A).det = ((feedbackPencil p z A).det.re : ℂ)
  apply Complex.ext <;> simp [hIm]

/-- The same actual derivative for the real log of the original pencil's
determinant. The stated slit-plane chart supplies positivity at the point. -/
theorem direct_row_real_feedback_hasDerivAt (p z : ℝ) {a : ℝ → Matrix ι ι ℂ}
    {da : Matrix ι ι ℂ} {t : ℝ} (ha : HasDerivAt a da t)
    (hSlit : (feedbackPencil p z (rowGram (a t))).det ∈ Complex.slitPlane) :
    HasDerivAt
      (fun s => -Real.log ((feedbackPencil p z (rowGram (a s))).det.re))
      (4 * z * p ^ 2 *
        (Matrix.trace ((feedbackPencil p z (rowGram (a t)))⁻¹ *
          sourceCoefficient p (rowGram (a t)) * rowGramJet (a t) da)).re) t := by
  have h := direct_row_feedback_hasDerivAt p z ha hSlit
  have hFun : (fun s => -(Complex.log ((feedbackPencil p z (rowGram (a s))).det)).re) =
      (fun s => -Real.log ((feedbackPencil p z (rowGram (a s))).det.re)) := by
    funext s
    rw [feedbackPencil_det_real p z (a s), Complex.log_ofReal_re]
    simp only [Complex.ofReal_re]
  rw [hFun] at h
  exact h

section HostileControl

abbrev M2 := Matrix (Fin 2) (Fin 2) ℂ
def hostileRow : M2 := !![(0 : ℂ), 0; 0, 1 / 2]
def hostileVelocity : M2 := !![(1 : ℂ), 1; 1, 1]
def hostileCurve (s : ℝ) : M2 := hostileRow + s • hostileVelocity

theorem hostileGram : rowGram hostileRow = !![(0 : ℂ), 0; 0, 1 / 4] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [rowGram, hostileRow, Matrix.star_apply, Matrix.mul_apply, Fin.sum_univ_two]
  simp only [map_ofNat]
  norm_num

theorem hostileJet : rowGramJet hostileRow hostileVelocity =
    !![(0 : ℂ), 1 / 2; 1 / 2, 1] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [rowGramJet, hostileRow, hostileVelocity, Matrix.star_apply, Matrix.mul_apply,
      Fin.sum_univ_two]
  all_goals simp only [map_ofNat]
  all_goals norm_num

theorem hostileGram_singular : (rowGram hostileRow).det = 0 := by
  rw [hostileGram, Matrix.det_fin_two]
  norm_num

theorem hostileGram_jet_noncommuting :
    rowGram hostileRow * rowGramJet hostileRow hostileVelocity ≠
      rowGramJet hostileRow hostileVelocity * rowGram hostileRow := by
  intro h
  have he := congrArg (fun M : M2 => M 0 1) h
  rw [hostileGram, hostileJet] at he
  norm_num [Matrix.mul_apply, Fin.sum_univ_two] at he

theorem hostilePencil_resolvent :
    (feedbackPencil (1 / 2) (1 / 4) (rowGram hostileRow))⁻¹ =
      !![(1 : ℂ), 0; 0, 256 / 241] := by
  apply Matrix.inv_eq_left_inv
  rw [hostileGram]
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [feedbackPencil, returnOperator, Matrix.mul_apply,
      Fin.sum_univ_two, Matrix.one_apply]

theorem hostilePencil_slit :
    (feedbackPencil (1 / 2) (1 / 4) (rowGram hostileRow)).det ∈ Complex.slitPlane := by
  rw [hostileGram, Matrix.det_fin_two]
  norm_num [feedbackPencil, returnOperator, Matrix.mul_apply,
    Fin.sum_univ_two, Matrix.one_apply, Complex.mem_slitPlane_iff]

theorem hostileSource_value :
    (4 * (1 / 4 : ℝ) * (1 / 2 : ℝ)^2 *
      (Matrix.trace ((feedbackPencil (1 / 2) (1 / 4) (rowGram hostileRow))⁻¹ *
        sourceCoefficient (1 / 2) (rowGram hostileRow) *
          rowGramJet hostileRow hostileVelocity)).re) = 56 / 241 := by
  rw [hostilePencil_resolvent, hostileGram, hostileJet]
  norm_num [sourceCoefficient, Matrix.trace, Matrix.mul_apply, Matrix.vecMul,
    dotProduct, Fin.sum_univ_two, Matrix.one_apply]

/-- Finite rational control: the row is singular, the actual Gram jet does
not commute with the Gram, and the actual feedback derivative is nonzero. -/
theorem hostile_direct_row_feedback :
    (rowGram hostileRow).det = 0 ∧
    rowGram hostileRow * rowGramJet hostileRow hostileVelocity ≠
      rowGramJet hostileRow hostileVelocity * rowGram hostileRow ∧
    HasDerivAt
      (fun s => -Real.log ((feedbackPencil (1 / 2) (1 / 4)
        (rowGram (hostileCurve s))).det.re)) (56 / 241) 0 := by
  have ha : HasDerivAt hostileCurve hostileVelocity 0 := by
    change HasDerivAt (fun s : ℝ => hostileRow + s • hostileVelocity) hostileVelocity 0
    simpa only [one_smul] using
      ((hasDerivAt_id' (0 : ℝ)).smul_const hostileVelocity).const_add hostileRow
  have hs : (feedbackPencil (1 / 2) (1 / 4) (rowGram (hostileCurve 0))).det ∈
      Complex.slitPlane := by
    simpa [hostileCurve] using hostilePencil_slit
  have h := direct_row_real_feedback_hasDerivAt (1 / 2) (1 / 4) ha hs
  have hvalue : (4 * (1 / 4 : ℝ) * (1 / 2 : ℝ)^2 *
      (Matrix.trace ((feedbackPencil (1 / 2) (1 / 4) (rowGram (hostileCurve 0)))⁻¹ *
        sourceCoefficient (1 / 2) (rowGram (hostileCurve 0)) *
          rowGramJet (hostileCurve 0) hostileVelocity)).re) = 56 / 241 := by
    simpa [hostileCurve] using hostileSource_value
  rw [hvalue] at h
  exact ⟨hostileGram_singular, hostileGram_jet_noncommuting, h⟩

end HostileControl

end
end D0.Analysis.DirectFeedbackRowDerivative
