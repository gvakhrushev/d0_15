import D0.Analysis.MovingProjectorBookPriceDensityBridge

/-!
# Moving-cut price with varying temperature and feedback parameter

Both parameters and all matrices follow one real differentiable curve. The
extra derivatives are retained; no admission of these directions is asserted.
-/

namespace D0.Analysis.MovingProjectorBookPrice

open Filter
open scoped Topology Matrix.Norms.Frobenius
open D0.Algebra.MovingProjectorTransport

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- The partition derivative retains both changes in inverse temperature and energy. -/
theorem hasDerivAt_variable_heat_partition
    {β : ℝ → ℝ} {Δ : ℝ → Matrix ι ι ℂ} {dβ : ℝ}
    {dΔ : Matrix ι ι ℂ} {t : ℝ}
    (hβ : HasDerivAt β dβ t) (hΔ : HasDerivAt Δ dΔ t) :
    let E := NormedSpace.exp ((-β t) • Δ t)
    HasDerivAt (fun s => matrixHeatPartition (β s) (Δ s))
      (-dβ * (Matrix.trace (E * Δ t)).re -
        β t * (Matrix.trace (E * dΔ)).re) t := by
  let E := NormedSpace.exp ((-β t) • Δ t)
  have hA : HasDerivAt (fun s => (-β s) • Δ s)
      ((-dβ) • Δ t + (-β t) • dΔ) t := by
    simpa only [Pi.neg_apply, add_comm] using hβ.neg.smul hΔ
  have htrace := D0.Analysis.hasDerivAt_matrix_trace_exp hA
  have hre := Complex.reCLM.hasFDerivAt.comp_hasDerivAt t htrace
  simpa only [matrixHeatPartition, Complex.reCLM_apply, mul_add, mul_smul_comm,
    Matrix.trace_add, Matrix.trace_smul, Complex.add_re, Complex.smul_re,
    smul_eq_mul, neg_mul, sub_eq_add_neg, E] using hre

/-- The variable-β heat source, including its thermodynamic coefficient. -/
theorem hasDerivAt_variable_heat_log_partition [Nonempty ι]
    {β : ℝ → ℝ} {Δ : ℝ → Matrix ι ι ℂ} {dβ : ℝ}
    {dΔ K : Matrix ι ι ℂ} {t : ℝ}
    (hβ : HasDerivAt β dβ t) (hβne : β t ≠ 0)
    (hΔ : HasDerivAt Δ dΔ t) (hHerm : star (Δ t) = Δ t) :
    let Z := matrixHeatPartition (β t) (Δ t)
    let ρ := matrixThermalState (β t) (Δ t)
    HasDerivAt (fun s => (β s)⁻¹ * Real.log (matrixHeatPartition (β s) (Δ s)))
      (-(Matrix.trace (ρ * (dΔ - comm K (Δ t)))).re +
        (-Real.log Z / (β t)^2 - (Matrix.trace (ρ * Δ t)).re / β t) * dβ) t := by
  let E := NormedSpace.exp ((-β t) • Δ t)
  let Z := matrixHeatPartition (β t) (Δ t)
  let ρ := matrixThermalState (β t) (Δ t)
  have hZ : 0 < Z := matrix_exp_trace_re_pos ((-β t) • Δ t) (by simp [hHerm])
  have hpart := hasDerivAt_variable_heat_partition hβ hΔ
  have hlog := hpart.log (ne_of_gt hZ)
  have hinv := hβ.inv hβne
  have h := hinv.mul hlog
  have hcomm : Matrix.trace (E * (K * Δ t - Δ t * K)) = 0 :=
    matrix_exp_trace_commutator_zero (Δ t) K (β t)
  have hrel : Matrix.trace (E * (dΔ - comm K (Δ t))) = Matrix.trace (E * dΔ) := by
    change Matrix.trace (E * (dΔ - (K * Δ t - Δ t * K))) = Matrix.trace (E * dΔ)
    rw [mul_sub, Matrix.trace_sub, hcomm, sub_zero]
  have hnormΔ : (Matrix.trace (ρ * Δ t)).re = (Matrix.trace (E * Δ t)).re / Z :=
    matrixThermalState_trace_normalization (β t) (Δ t) (Δ t) hHerm
  have hnormd : (Matrix.trace (ρ * (dΔ - comm K (Δ t)))).re =
      (Matrix.trace (E * dΔ)).re / Z := by
    rw [matrixThermalState_trace_normalization (β t) (Δ t) _ hHerm, hrel]
  dsimp only
  apply h.congr_deriv
  rw [hnormΔ, hnormd]
  change (-dβ / (β t)^2) * Real.log Z + (β t)⁻¹ *
    ((-dβ * (Matrix.trace (E * Δ t)).re - β t * (Matrix.trace (E * dΔ)).re) / Z) =
    -((Matrix.trace (E * dΔ)).re / Z) +
      (-Real.log Z / (β t)^2 - ((Matrix.trace (E * Δ t)).re / Z) / β t) * dβ
  field_simp [hβne, ne_of_gt hZ]
  ring

/-- The moving-cut feedback source retains the actual `z'` direction. -/
theorem hasDerivAt_variable_feedback_logdet
    {z : ℝ → ℝ} {P U : ℝ → Matrix ι ι ℂ} {dz : ℝ}
    {dP dU : Matrix ι ι ℂ} {t : ℝ}
    (hz : HasDerivAt z dz t)
    (hP : HasDerivAt P dP t) (hU : HasDerivAt U dU t)
    (hIdem : ∀ᶠ s in 𝓝 t, P s * P s = P s)
    (hSelf : ∀ᶠ s in 𝓝 t, star (P s) = P s)
    (hSlit : (1 - (z t : ℂ) •
      (star (cut (P t) (U t)) * cut (P t) (U t))).det ∈ Complex.slitPlane) :
    let C := cut (P t) (U t)
    let F := star C * C
    let R := (1 - (z t : ℂ) • F)⁻¹
    let V := (1 - P t) * (dU - comm (generator (P t) dP) (U t)) * P t
    HasDerivAt (fun s => -Real.log ((1 - (z s : ℂ) •
      (star (cut (P s) (U s)) * cut (P s) (U s))).det.re))
      (z t * (2 * (Matrix.trace (R * star C * V)).re) +
        dz * (Matrix.trace (R * F)).re) t := by
  let C := cut (P t) (U t)
  let F := star C * C
  let dC := cutTangent (P t) dP (U t) dU
  let dF := star dC * C + star C * dC
  let R := (1 - (z t : ℂ) • F)⁻¹
  let V := (1 - P t) * (dU - comm (generator (P t) dP) (U t)) * P t
  let A : ℝ → Matrix ι ι ℂ := fun s =>
    1 - (z s : ℂ) • (star (cut (P s) (U s)) * cut (P s) (U s))
  have hF : HasDerivAt (fun s => star (cut (P s) (U s)) * cut (P s) (U s))
      dF t := (differentiable_moving_return_relative hP hU hIdem hSelf).1
  have hA : HasDerivAt A (-(z t • dF + dz • F)) t := by
    have h := HasDerivAt.const_sub 1 (hz.smul hF)
    simpa only [A, Complex.real_smul, add_comm] using h
  have hLog := D0.Analysis.hasDerivAt_matrix_clogdet A (-(z t • dF + dz • F)) t hA hSlit
  have hReal := Complex.reCLM.hasFDerivAt.comp_hasDerivAt t hLog.neg
  have hInv : IsUnit (A t).det := isUnit_iff_ne_zero.mpr (Complex.slitPlane_ne_zero hSlit)
  have hTrace : Matrix.trace (R * dF) =
      ((2 * (Matrix.trace (R * star C * V)).re : ℝ) : ℂ) := by
    exact complex_matrix_feedback_resolvent_moving_return_two_re (z t : ℂ)
      hP hU hIdem hSelf (by simp) hInv
  have hValue : (-Matrix.trace (R * (-(z t • dF + dz • F)))).re =
      z t * (2 * (Matrix.trace (R * star C * V)).re) +
        dz * (Matrix.trace (R * F)).re := by
    simp only [mul_neg, mul_add, mul_smul_comm, Matrix.trace_neg, Matrix.trace_add,
      Matrix.trace_smul, neg_neg, Complex.add_re, Complex.smul_re, smul_eq_mul]
    rw [hTrace]
    simp
  have hFun : (fun s => -(Complex.log ((A s).det)).re) =
      (fun s => -Real.log ((A s).det.re)) := by
    funext s
    have hEq := complex_matrix_feedback_det_eq_real_part (cut (P s) (U s)) (z s)
    change (A s).det = ((A s).det.re : ℂ) at hEq
    rw [hEq, Complex.log_ofReal_re]
    simp only [Complex.ofReal_re]
  have hReal' : HasDerivAt (fun s => -(Complex.log ((A s).det)).re)
      (-Matrix.trace (R * (-(z t • dF + dz • F)))).re t := by
    simpa only [Function.comp_def, Complex.reCLM_apply, Pi.neg_apply, Complex.neg_re, R, A, F, C]
      using hReal
  change HasDerivAt (fun s => -Real.log ((A s).det.re)) _ t
  rw [← hFun]
  exact hReal'.congr_deriv hValue

/-- Complete derivative of the specified scalar with both parameters varying. -/
theorem hasDerivAt_variable_moving_projector_book03_price [Nonempty ι]
    {β z : ℝ → ℝ} {P U Δ : ℝ → Matrix ι ι ℂ}
    {dβ dz : ℝ} {dP dU dΔ : Matrix ι ι ℂ} {t : ℝ}
    (hβ : HasDerivAt β dβ t) (hβne : β t ≠ 0) (hz : HasDerivAt z dz t)
    (hP : HasDerivAt P dP t) (hU : HasDerivAt U dU t)
    (hΔ : HasDerivAt Δ dΔ t) (hHerm : star (Δ t) = Δ t)
    (hIdem : ∀ᶠ s in 𝓝 t, P s * P s = P s)
    (hSelf : ∀ᶠ s in 𝓝 t, star (P s) = P s)
    (hSlit : (1 - (z t : ℂ) •
      (star (cut (P t) (U t)) * cut (P t) (U t))).det ∈ Complex.slitPlane) :
    let K := generator (P t) dP
    let C := cut (P t) (U t)
    let F := star C * C
    let R := (1 - (z t : ℂ) • F)⁻¹
    let V := (1 - P t) * (dU - comm K (U t)) * P t
    let Z := matrixHeatPartition (β t) (Δ t)
    let ρ := matrixThermalState (β t) (Δ t)
    HasDerivAt (fun s => matrixBook03Price (β s) (z s) Δ P U s)
      (-(Matrix.trace (ρ * (dΔ - comm K (Δ t)))).re +
        z t * (2 * (Matrix.trace (R * star C * V)).re) +
        (-Real.log Z / (β t)^2 - (Matrix.trace (ρ * Δ t)).re / β t) * dβ +
        dz * (Matrix.trace (R * F)).re) t := by
  have hHeat := hasDerivAt_variable_heat_log_partition (K := generator (P t) dP)
    hβ hβne hΔ hHerm
  have hFeedback := hasDerivAt_variable_feedback_logdet hz hP hU hIdem hSelf hSlit
  have h := hHeat.add hFeedback
  dsimp only at h ⊢
  convert h using 1
  abel

/-- The slit-plane premise is derived from the actual isometric cut at `t`. -/
theorem hasDerivAt_variable_moving_projector_book03_price_of_isometric_cut [Nonempty ι]
    {β z : ℝ → ℝ} {P U Δ : ℝ → Matrix ι ι ℂ}
    {dβ dz : ℝ} {dP dU dΔ : Matrix ι ι ℂ} {t : ℝ}
    (hβ : HasDerivAt β dβ t) (hβne : β t ≠ 0) (hz : HasDerivAt z dz t)
    (hz0 : 0 ≤ z t) (hz1 : z t < 1)
    (hP : HasDerivAt P dP t) (hU : HasDerivAt U dU t)
    (hΔ : HasDerivAt Δ dΔ t) (hHerm : star (Δ t) = Δ t)
    (hIdem : ∀ᶠ s in 𝓝 t, P s * P s = P s)
    (hSelf : ∀ᶠ s in 𝓝 t, star (P s) = P s)
    (hIsometry : star (U t) * U t = 1) :
    let K := generator (P t) dP
    let C := cut (P t) (U t)
    let F := star C * C
    let R := (1 - (z t : ℂ) • F)⁻¹
    let V := (1 - P t) * (dU - comm K (U t)) * P t
    let Z := matrixHeatPartition (β t) (Δ t)
    let ρ := matrixThermalState (β t) (Δ t)
    HasDerivAt (fun s => matrixBook03Price (β s) (z s) Δ P U s)
      (-(Matrix.trace (ρ * (dΔ - comm K (Δ t)))).re +
        z t * (2 * (Matrix.trace (R * star C * V)).re) +
        (-Real.log Z / (β t)^2 - (Matrix.trace (ρ * Δ t)).re / β t) * dβ +
        dz * (Matrix.trace (R * F)).re) t :=
  hasDerivAt_variable_moving_projector_book03_price hβ hβne hz hP hU hΔ hHerm hIdem hSelf
    (cut_feedback_det_mem_slitPlane (P t) (U t) (z t)
      hIdem.self_of_nhds hSelf.self_of_nhds hIsometry hz0 hz1)

/-- Both coefficients of `β'` and `z'` in the stated source are real. -/
theorem variable_parameter_trace_coefficients_real
    (β z : ℝ) (P U Δ : Matrix ι ι ℂ) (hHerm : star Δ = Δ) :
    let ρ := matrixThermalState β Δ
    let C := cut P U
    let F := star C * C
    let R := (1 - (z : ℂ) • F)⁻¹
    star (Matrix.trace (ρ * Δ)) = Matrix.trace (ρ * Δ) ∧
      star (Matrix.trace (R * F)) = Matrix.trace (R * F) := by
  let ρ := matrixThermalState β Δ
  let C := cut P U
  let F := star C * C
  let R := (1 - (z : ℂ) • F)⁻¹
  have hρ : star ρ = ρ := by
    dsimp only [ρ, matrixThermalState]
    rw [star_smul, NormedSpace.star_exp]
    simp [hHerm]
  have hF : star F = F := by simp [F, star_mul]
  have hR : star R = R :=
    complex_matrix_feedback_resolvent_selfadjoint C (z : ℂ) (by simp)
  exact ⟨matrix_trace_selfadjoint_product_real ρ Δ hρ hHerm,
    matrix_trace_selfadjoint_product_real R F hR hF⟩

end D0.Analysis.MovingProjectorBookPrice
