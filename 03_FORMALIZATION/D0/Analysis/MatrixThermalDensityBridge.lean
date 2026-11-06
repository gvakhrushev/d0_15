import D0.Analysis.MatrixMovingHeatFeedback

/-!
# Fixed-Gram density normalization of the thermal source

The normalized Gibbs matrix and all traces are on the same finite complex
matrix carrier with its standard fixed Hermitian Gram. This mathematical
bridge does not select a physical realization or a field-dependent Gram.
-/

namespace D0.Algebra.MovingProjectorTransport

open Filter
open scoped Topology Matrix.Norms.Frobenius

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

omit [DecidableEq ι] in
/-- The trace of a product of two self-adjoint matrices is real. -/
theorem matrix_trace_selfadjoint_product_real
    (E V : Matrix ι ι ℂ) (hE : star E = E) (hV : star V = V) :
    star (Matrix.trace (E * V)) = Matrix.trace (E * V) := by
  calc
    star (Matrix.trace (E * V)) = Matrix.trace (star (E * V)) := by
      simpa only [Matrix.star_eq_conjTranspose] using
        (Matrix.trace_conjTranspose (E * V)).symm
    _ = Matrix.trace (V * E) := by simp only [star_mul, hE, hV]
    _ = Matrix.trace (E * V) := Matrix.trace_mul_comm V E

/-- The standard fixed-Gram Gibbs state, normalized by the actual complex trace. -/
noncomputable def matrixThermalDensity (β : ℝ) (Δ : Matrix ι ι ℂ) : Matrix ι ι ℂ :=
  let E := NormedSpace.exp ((-β) • Δ)
  (Matrix.trace E)⁻¹ • E

/-- A self-adjoint Δ and its tangent give a self-adjoint transported variation. -/
theorem matrix_relative_thermal_tangent_selfadjoint
    (Δ dΔ K : Matrix ι ι ℂ)
    (hΔ : star Δ = Δ) (hdΔ : star dΔ = dΔ) (hK : star K = -K) :
    star (dΔ - comm K Δ) = dΔ - comm K Δ := by
  simp only [comm, star_sub, star_mul, hΔ, hdΔ, hK]
  noncomm_ring

/-- The unnormalized source and partition traces are real on the same carrier. -/
theorem matrix_thermal_relative_traces_real
    (β : ℝ) (Δ dΔ K : Matrix ι ι ℂ)
    (hΔ : star Δ = Δ) (hdΔ : star dΔ = dΔ) (hK : star K = -K) :
    let E := NormedSpace.exp ((-β) • Δ)
    star (Matrix.trace E) = Matrix.trace E ∧
      star (Matrix.trace (E * (dΔ - comm K Δ))) =
        Matrix.trace (E * (dΔ - comm K Δ)) := by
  let E := NormedSpace.exp ((-β) • Δ)
  have hE : star E = E := by
    dsimp [E]
    rw [NormedSpace.star_exp]
    simp [hΔ]
  have hV := matrix_relative_thermal_tangent_selfadjoint Δ dΔ K hΔ hdΔ hK
  refine ⟨?_, matrix_trace_selfadjoint_product_real E _ hE hV⟩
  simpa only [mul_one] using
    matrix_trace_selfadjoint_product_real E (1 : Matrix ι ι ℂ) hE (star_one _)

/-- Normalization by the actual trace agrees with the ratio of the real traces. -/
theorem matrix_thermal_density_relative_trace
    (β : ℝ) (Δ dΔ K : Matrix ι ι ℂ)
    (hΔ : star Δ = Δ) (hdΔ : star dΔ = dΔ) (hK : star K = -K) :
    let E := NormedSpace.exp ((-β) • Δ)
    let V := dΔ - comm K Δ
    Matrix.trace (matrixThermalDensity β Δ * V) =
      (((Matrix.trace (E * V)).re / (Matrix.trace E).re : ℝ) : ℂ) := by
  let E := NormedSpace.exp ((-β) • Δ)
  let V := dΔ - comm K Δ
  let T : ℂ := Matrix.trace E
  let N : ℂ := Matrix.trace (E * V)
  have hreal := matrix_thermal_relative_traces_real β Δ dΔ K hΔ hdΔ hK
  have hT : ((T.re : ℝ) : ℂ) = T := Complex.conj_eq_iff_re.mp hreal.1
  have hN : ((N.re : ℝ) : ℂ) = N := Complex.conj_eq_iff_re.mp hreal.2
  change Matrix.trace (matrixThermalDensity β Δ * V) = ((N.re / T.re : ℝ) : ℂ)
  calc
    Matrix.trace (matrixThermalDensity β Δ * V) = T⁻¹ * N := by
      simp only [matrixThermalDensity, E, V, T, N, smul_mul_assoc,
        Matrix.trace_smul, smul_eq_mul]
    _ = ((T.re : ℝ) : ℂ)⁻¹ * ((N.re : ℝ) : ℂ) := by rw [hT, hN]
    _ = ((N.re / T.re : ℝ) : ℂ) := by
      push_cast
      ring

/-- The Gibbs state is genuinely trace-normalized on a nonempty carrier. -/
theorem matrix_thermal_density_trace_one [Nonempty ι]
    (β : ℝ) (Δ : Matrix ι ι ℂ) (hΔ : star Δ = Δ) :
    Matrix.trace (matrixThermalDensity β Δ) = 1 := by
  let E := NormedSpace.exp ((-β) • Δ)
  have hE : star ((-β) • Δ) = (-β) • Δ := by simp [hΔ]
  have hpos : 0 < (Matrix.trace E).re :=
    D0.Analysis.matrix_exp_trace_re_pos ((-β) • Δ) hE
  have hne : Matrix.trace E ≠ 0 := by
    intro h
    have hr := congrArg Complex.re h
    simp only [Complex.zero_re] at hr
    linarith
  change Matrix.trace ((Matrix.trace E)⁻¹ • E) = 1
  rw [Matrix.trace_smul]
  change (Matrix.trace E)⁻¹ * Matrix.trace E = 1
  exact inv_mul_cancel₀ hne

/--
The same moving-cut derivative with the literal normalized Gibbs source.
Local Hermiticity supplies the actual Hermitian tangent, and the locally
orthogonal projector supplies the anti-Hermitian canonical generator.
-/
theorem hasDerivAt_moving_heat_feedback_density [Nonempty ι]
    {P U Δ : ℝ → Matrix ι ι ℂ} {dP dU dΔ : Matrix ι ι ℂ} {t : ℝ}
    (β z : ℝ) (hβ : β ≠ 0) (hz0 : 0 ≤ z) (hz1 : z < 1)
    (hP : HasDerivAt P dP t) (hU : HasDerivAt U dU t)
    (hΔ : HasDerivAt Δ dΔ t)
    (hIdem : ∀ᶠ s in 𝓝 t, P s * P s = P s)
    (hPself : ∀ᶠ s in 𝓝 t, star (P s) = P s)
    (hIsometry : star (U t) * U t = 1)
    (hΔself : ∀ᶠ s in 𝓝 t, star (Δ s) = Δ s) :
    let K := generator (P t) dP
    let C := cut (P t) (U t)
    let R := (1 - (z : ℂ) • (star C * C))⁻¹
    let V := (1 - P t) * (dU - comm K (U t)) * P t
    let E := NormedSpace.exp ((-β) • Δ t)
    let Z := D0.Analysis.matrixHeatPartition β (Δ t)
    let ρ := matrixThermalDensity β (Δ t)
    star (Matrix.trace E) = Matrix.trace E ∧
      star (Matrix.trace (E * (dΔ - comm K (Δ t)))) =
        Matrix.trace (E * (dΔ - comm K (Δ t))) ∧
      (((-((Matrix.trace (E * (dΔ - comm K (Δ t)))).re) / Z : ℝ) : ℂ)) =
        -Matrix.trace (ρ * (dΔ - comm K (Δ t))) ∧
      Matrix.trace ρ = 1 ∧
      HasDerivAt (fun s => movingHeatFeedback β z (P s) (U s) (Δ s))
        (-(Matrix.trace (ρ * (dΔ - comm K (Δ t)))).re +
          z * (2 * (Matrix.trace (R * star C * V)).re)) t := by
  let K := generator (P t) dP
  let E := NormedSpace.exp ((-β) • Δ t)
  let ρ := matrixThermalDensity β (Δ t)
  let VΔ := dΔ - comm K (Δ t)
  have hΔpoint : star (Δ t) = Δ t := hΔself.self_of_nhds
  have hdΔ : star dΔ = dΔ := self_adjoint_tangent_of_curve hΔ hΔself
  have hK : star K = -K := generator_anti_self_adjoint_of_curve hP hPself
  have hreal := matrix_thermal_relative_traces_real β (Δ t) dΔ K hΔpoint hdΔ hK
  have hratio := matrix_thermal_density_relative_trace β (Δ t) dΔ K hΔpoint hdΔ hK
  have hratioRe : (Matrix.trace (ρ * VΔ)).re =
      (Matrix.trace (E * VΔ)).re / (Matrix.trace E).re := by
    have h := congrArg Complex.re hratio
    simpa only [Complex.ofReal_re] using h
  have hnormalized : Matrix.trace ρ = 1 :=
    matrix_thermal_density_trace_one β (Δ t) hΔpoint
  have hsource : (((-((Matrix.trace (E * VΔ)).re) /
        D0.Analysis.matrixHeatPartition β (Δ t) : ℝ) : ℂ)) =
      -Matrix.trace (ρ * VΔ) := by
    rw [hratio]
    simp [D0.Analysis.matrixHeatPartition, E, VΔ, neg_div]
  have hderiv := hasDerivAt_moving_heat_feedback β z hβ hz0 hz1 hP hU hΔ
    hIdem hPself hIsometry hΔpoint
  refine ⟨hreal.1, hreal.2, hsource, hnormalized, ?_⟩
  apply hderiv.congr_deriv
  have heq : -((Matrix.trace (E * VΔ)).re) /
      D0.Analysis.matrixHeatPartition β (Δ t) = -(Matrix.trace (ρ * VΔ)).re := by
    simpa only [D0.Analysis.matrixHeatPartition, neg_div] using
      congrArg Neg.neg hratioRe.symm
  rw [heq]

end D0.Algebra.MovingProjectorTransport
