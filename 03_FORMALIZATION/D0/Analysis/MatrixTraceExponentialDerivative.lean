import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Comp
import Mathlib.Analysis.Calculus.SmoothSeries
import Mathlib.Analysis.Normed.Algebra.MatrixExponential
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.Analysis.Normed.Operator.Basic
import Mathlib.Tactic

/-! Finite-matrix trace calculus for noncommuting variations. -/

namespace D0.Analysis

open scoped Matrix.Norms.Frobenius BigOperators

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- The cyclic trace collapses all noncommuting insertions in a power. -/
theorem matrix_trace_power_insertions
    (A H : Matrix ι ι ℂ) (n : ℕ) :
    Matrix.trace (∑ i ∈ Finset.range n, A ^ (n.pred - i) * H * A ^ i) =
      (n : ℂ) * Matrix.trace (A ^ (n - 1) * H) := by
  rw [Matrix.trace_sum]
  have hterm : ∀ i ∈ Finset.range n,
      Matrix.trace (A ^ (n.pred - i) * H * A ^ i) =
        Matrix.trace (A ^ (n - 1) * H) := by
    intro i hi
    have hi' : i ≤ n.pred := by
      simp only [Finset.mem_range] at hi
      simp only [Nat.pred_eq_sub_one]
      omega
    have hidx : i + (n.pred - i) = n - 1 := by
      simp only [Nat.pred_eq_sub_one] at *
      omega
    rw [Matrix.trace_mul_cycle, ← pow_add, hidx]
  rw [Finset.sum_congr rfl hterm]
  simp

/-- Derivative of every trace power for an arbitrary differentiable curve. -/
theorem hasDerivAt_matrix_trace_pow
    {A : ℝ → Matrix ι ι ℂ} {H : Matrix ι ι ℂ} {t : ℝ}
    (hA : HasDerivAt A H t) (n : ℕ) :
    HasDerivAt (fun s => Matrix.trace (A s ^ n))
      ((n : ℂ) * Matrix.trace (A t ^ (n - 1) * H)) t := by
  let tr : Matrix ι ι ℂ →L[ℝ] ℂ :=
    (Matrix.traceLinearMap ι ℝ ℂ).toContinuousLinearMap
  have h := tr.hasFDerivAt.comp_hasDerivAt t (hA.fun_pow' n)
  change HasDerivAt (fun s => Matrix.trace (A s ^ n))
    (Matrix.trace (∑ i ∈ Finset.range n, A t ^ (n.pred - i) * H * A t ^ i)) t at h
  rw [matrix_trace_power_insertions] at h
  exact h

/-- A finite exponential polynomial already has the full noncommuting derivative. -/
theorem hasDerivAt_matrix_trace_exp_partial
    {A : ℝ → Matrix ι ι ℂ} {H : Matrix ι ι ℂ} {t : ℝ}
    (hA : HasDerivAt A H t) (N : ℕ) :
    HasDerivAt
      (fun s => ∑ n ∈ Finset.range N,
        ((n.factorial : ℝ)⁻¹) • Matrix.trace (A s ^ n))
      (∑ n ∈ Finset.range N, ((n.factorial : ℝ)⁻¹) •
        ((n : ℂ) * Matrix.trace (A t ^ (n - 1) * H))) t := by
  apply HasDerivAt.fun_sum
  intro n _
  exact (hasDerivAt_matrix_trace_pow hA n).const_smul ((n.factorial : ℝ)⁻¹)

private theorem factorial_derivative_cancel (k : ℕ) (w : ℂ) :
    (((k + 1).factorial : ℝ)⁻¹) • (((k + 1 : ℕ) : ℂ) * w) =
      ((k.factorial : ℝ)⁻¹) • w := by
  simp only [Complex.real_smul, Nat.factorial_succ, Nat.cast_mul,
    Complex.ofReal_inv, Complex.ofReal_mul, Complex.ofReal_natCast]
  have hk : (k.factorial : ℂ) ≠ 0 := by exact_mod_cast Nat.factorial_ne_zero k
  have hs : ((k + 1 : ℕ) : ℂ) ≠ 0 := by exact_mod_cast Nat.succ_ne_zero k
  field_simp

/-- After cancellation of the factorial the n+1-st term has this derivative. -/
theorem hasDerivAt_matrix_trace_exp_succ_term
    {A : ℝ → Matrix ι ι ℂ} {H : Matrix ι ι ℂ} {t : ℝ}
    (hA : HasDerivAt A H t) (k : ℕ) :
    HasDerivAt
      (fun s => (((k + 1).factorial : ℝ)⁻¹) • Matrix.trace (A s ^ (k + 1)))
      (((k.factorial : ℝ)⁻¹) • Matrix.trace (A t ^ k * H)) t := by
  have h := (hasDerivAt_matrix_trace_pow hA (k + 1)).const_smul
    (((k + 1).factorial : ℝ)⁻¹)
  simpa only [Nat.add_sub_cancel, factorial_derivative_cancel] using h

/-- A uniform bound that remains valid for the non-unit-normalized Frobenius norm. -/
private theorem matrix_norm_pow_bound (X : Matrix ι ι ℂ) (B : ℝ)
    (hB : 0 ≤ B) (hX : ‖X‖ ≤ B) (k : ℕ) :
    ‖X ^ k‖ ≤ max 1 ‖(1 : Matrix ι ι ℂ)‖ * B ^ k := by
  cases k with
  | zero => simp
  | succ k =>
    calc
      ‖X ^ (k + 1)‖ ≤ ‖X‖ ^ (k + 1) := norm_pow_le' X (by omega)
      _ ≤ B ^ (k + 1) := pow_le_pow_left₀ (norm_nonneg X) hX _
      _ ≤ max 1 ‖(1 : Matrix ι ι ℂ)‖ * B ^ (k + 1) := by
        have hm := le_max_left 1 ‖(1 : Matrix ι ι ℂ)‖
        have hp := pow_nonneg hB (k + 1)
        nlinarith

private theorem matrix_trace_power_bound (X H : Matrix ι ι ℂ) (B C : ℝ)
    (hB : 0 ≤ B) (hX : ‖X‖ ≤ B) (hC : 0 ≤ C)
    (htrace : ∀ Y : Matrix ι ι ℂ, ‖Matrix.trace Y‖ ≤ C * ‖Y‖) (k : ℕ) :
    ‖Matrix.trace (X ^ k * H)‖ ≤
      C * (max 1 ‖(1 : Matrix ι ι ℂ)‖ * B ^ k * ‖H‖) := by
  calc
    ‖Matrix.trace (X ^ k * H)‖ ≤ C * ‖X ^ k * H‖ := htrace _
    _ ≤ C * (‖X ^ k‖ * ‖H‖) := by gcongr; exact norm_mul_le _ _
    _ ≤ C * (max 1 ‖(1 : Matrix ι ι ℂ)‖ * B ^ k * ‖H‖) := by
      gcongr
      exact matrix_norm_pow_bound X B hB hX k

private theorem matrix_trace_bound :
    ∃ C : ℝ, 0 < C ∧ ∀ Y : Matrix ι ι ℂ, ‖Matrix.trace Y‖ ≤ C * ‖Y‖ := by
  let tr : Matrix ι ι ℂ →L[ℝ] ℂ :=
    (Matrix.traceLinearMap ι ℝ ℂ).toContinuousLinearMap
  obtain ⟨C, hC, h⟩ := tr.bound
  exact ⟨C, hC, h⟩

/-- The trace may be interchanged with the absolutely convergent matrix exponential series. -/
theorem matrix_trace_exp_eq_tsum (A : Matrix ι ι ℂ) :
    Matrix.trace (NormedSpace.exp A) =
      ∑' n : ℕ, ((n.factorial : ℝ)⁻¹) • Matrix.trace (A ^ n) := by
  let tr : Matrix ι ι ℂ →L[ℝ] ℂ :=
    (Matrix.traceLinearMap ι ℝ ℂ).toContinuousLinearMap
  have hs := (NormedSpace.expSeries_summable' (𝕂 := ℝ) A).hasSum
  have hm := (hs.map tr tr.continuous).tsum_eq
  rw [NormedSpace.exp_eq_tsum ℝ]
  simpa only [Function.comp_def, map_smul, tr, Matrix.traceLinearMap_apply] using hm.symm

private theorem matrix_trace_exp_series_summable (A : Matrix ι ι ℂ) :
    Summable (fun n : ℕ => ((n.factorial : ℝ)⁻¹) • Matrix.trace (A ^ n)) := by
  let tr : Matrix ι ι ℂ →L[ℝ] ℂ :=
    (Matrix.traceLinearMap ι ℝ ℂ).toContinuousLinearMap
  have hs := (NormedSpace.expSeries_summable' (𝕂 := ℝ) A).hasSum
  have hm := (hs.map tr tr.continuous).summable
  simpa only [Function.comp_def, map_smul, tr, Matrix.traceLinearMap_apply] using hm

private theorem matrix_trace_exp_mul_eq_tsum (A H : Matrix ι ι ℂ) :
    Matrix.trace (NormedSpace.exp A * H) =
      ∑' n : ℕ, ((n.factorial : ℝ)⁻¹) • Matrix.trace (A ^ n * H) := by
  let tr : Matrix ι ι ℂ →L[ℝ] ℂ :=
    (Matrix.traceLinearMap ι ℝ ℂ).toContinuousLinearMap
  have hs := (NormedSpace.expSeries_summable' (𝕂 := ℝ) A).hasSum
  have hm := ((hs.mul_right H).map tr tr.continuous).tsum_eq
  rw [NormedSpace.exp_eq_tsum ℝ]
  simpa only [Function.comp_def, smul_mul_assoc, map_smul, tr,
    Matrix.traceLinearMap_apply] using hm.symm

private theorem shifted_exp_bound_summable (K B : ℝ) :
    Summable (fun n : ℕ => if n = 0 then 0 else
      K * (((n - 1).factorial : ℝ)⁻¹) * B ^ (n - 1)) := by
  apply (summable_nat_add_iff 1).mp
  have hs := (NormedSpace.expSeries_summable' (𝕂 := ℝ) B).mul_left K
  simpa [Nat.add_sub_cancel, smul_eq_mul, mul_assoc] using hs

private theorem affine_norm_bound (A H : Matrix ι ι ℂ) (s : ℝ)
    (hs : |s| ≤ 1) : ‖A + s • H‖ ≤ ‖A‖ + ‖H‖ + 1 := by
  calc
    ‖A + s • H‖ ≤ ‖A‖ + ‖s • H‖ := norm_add_le _ _
    _ = ‖A‖ + |s| * ‖H‖ := by simp [norm_smul, Real.norm_eq_abs]
    _ ≤ ‖A‖ + ‖H‖ + 1 := by nlinarith [norm_nonneg H, abs_nonneg s]

/-- Trace of the exponential along any affine direction, without commutativity. -/
theorem hasDerivAt_matrix_trace_exp_affine (A H : Matrix ι ι ℂ) :
    HasDerivAt (fun s : ℝ => Matrix.trace (NormedSpace.exp (A + s • H)))
      (Matrix.trace (NormedSpace.exp A * H)) 0 := by
  obtain ⟨C, hC, htrace⟩ := matrix_trace_bound (ι := ι)
  let B : ℝ := ‖A‖ + ‖H‖ + 1
  let D : ℝ := max 1 ‖(1 : Matrix ι ι ℂ)‖
  let K : ℝ := C * D * ‖H‖
  let g : ℕ → ℝ → ℂ := fun n s =>
    ((n.factorial : ℝ)⁻¹) • Matrix.trace ((A + s • H) ^ n)
  let g' : ℕ → ℝ → ℂ := fun n s => match n with
    | 0 => 0
    | k + 1 => ((k.factorial : ℝ)⁻¹) • Matrix.trace ((A + s • H) ^ k * H)
  let u : ℕ → ℝ := fun n => if n = 0 then 0 else
    K * (((n - 1).factorial : ℝ)⁻¹) * B ^ (n - 1)
  have hB : 0 ≤ B := by dsimp [B]; positivity
  have hK : 0 ≤ K := by dsimp [K, D]; positivity
  have hu : Summable u := shifted_exp_bound_summable K B
  have hcurve (s : ℝ) : HasDerivAt (fun r : ℝ => A + r • H) H s := by
    simpa only [one_smul] using ((hasDerivAt_id s).smul_const H).const_add A
  have hg : ∀ n s, s ∈ Set.Ioo (-1 : ℝ) 1 → HasDerivAt (g n) (g' n s) s := by
    intro n s _
    cases n with
    | zero =>
      simpa [g, g'] using
        (hasDerivAt_const s (Matrix.trace (1 : Matrix ι ι ℂ)))
    | succ k =>
      simpa [g, g'] using hasDerivAt_matrix_trace_exp_succ_term (hcurve s) k
  have hbound : ∀ n s, s ∈ Set.Ioo (-1 : ℝ) 1 → ‖g' n s‖ ≤ u n := by
    intro n s hs
    cases n with
    | zero => simp [g', u]
    | succ k =>
      have hs' : |s| ≤ 1 := abs_le.mpr ⟨le_of_lt hs.1, le_of_lt hs.2⟩
      have hx : ‖A + s • H‖ ≤ B := affine_norm_bound A H s hs'
      have hp := matrix_trace_power_bound (A + s • H) H B C hB hx hC.le htrace k
      have hf : 0 ≤ ((k.factorial : ℝ)⁻¹) := inv_nonneg.mpr (Nat.cast_nonneg _)
      calc
        ‖g' (k + 1) s‖ = ((k.factorial : ℝ)⁻¹) *
            ‖Matrix.trace ((A + s • H) ^ k * H)‖ := by
          simp [g']
        _ ≤ ((k.factorial : ℝ)⁻¹) * (C * (D * B ^ k * ‖H‖)) :=
          mul_le_mul_of_nonneg_left hp hf
        _ = u (k + 1) := by simp [u, K, D]; ring
  have hg0 : Summable (fun n => g n 0) := by
    simpa [g] using matrix_trace_exp_series_summable A
  have hzero : (0 : ℝ) ∈ Set.Ioo (-1 : ℝ) 1 := by norm_num
  have hmain := hasDerivAt_tsum_of_isPreconnected hu isOpen_Ioo isPreconnected_Ioo
    hg hbound hzero hg0 hzero
  have hsumd : Summable (fun n => g' n 0) :=
    Summable.of_norm_bounded hu (fun n => hbound n 0 hzero)
  have hderiv : (∑' n, g' n 0) = Matrix.trace (NormedSpace.exp A * H) := by
    rw [hsumd.tsum_eq_zero_add]
    simpa [g'] using (matrix_trace_exp_mul_eq_tsum A H).symm
  have hfun : (fun s => ∑' n, g n s) =
      (fun s => Matrix.trace (NormedSpace.exp (A + s • H))) := by
    funext s
    exact (matrix_trace_exp_eq_tsum (A + s • H)).symm
  rw [hfun, hderiv] at hmain
  exact hmain

/-- Trace of the exponential for an arbitrary differentiable finite-matrix curve. -/
theorem hasDerivAt_matrix_trace_exp
    {A : ℝ → Matrix ι ι ℂ} {H : Matrix ι ι ℂ} {t : ℝ}
    (hA : HasDerivAt A H t) :
    HasDerivAt (fun s => Matrix.trace (NormedSpace.exp (A s)))
      (Matrix.trace (NormedSpace.exp (A t) * H)) t := by
  let tr : Matrix ι ι ℂ →L[ℝ] ℂ :=
    (Matrix.traceLinearMap ι ℝ ℂ).toContinuousLinearMap
  let F : Matrix ι ι ℂ → ℂ := fun X => tr (NormedSpace.exp X)
  have hexp : DifferentiableAt ℝ (NormedSpace.exp : Matrix ι ι ℂ → Matrix ι ι ℂ) (A t) :=
    (NormedSpace.exp_analytic (𝕂 := ℝ) (A t)).differentiableAt
  have hF : DifferentiableAt ℝ F (A t) := tr.differentiableAt.comp (A t) hexp
  have hline : HasDerivAt (fun s : ℝ => A t + s • H) H 0 := by
    simpa only [one_smul] using ((hasDerivAt_id (0 : ℝ)).smul_const H).const_add (A t)
  have hFat : HasFDerivAt F (fderiv ℝ F (A t)) (A t + (0 : ℝ) • H) := by
    simpa only [zero_smul, add_zero] using hF.hasFDerivAt
  have hcomp := hFat.comp_hasDerivAt 0 hline
  have hderiv : (fderiv ℝ F (A t)) H = Matrix.trace (NormedSpace.exp (A t) * H) := by
    exact hcomp.unique (hasDerivAt_matrix_trace_exp_affine (A t) H)
  have h := hF.hasFDerivAt.comp_hasDerivAt t hA
  exact h.congr_deriv hderiv

end D0.Analysis
