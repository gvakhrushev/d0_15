import D0.Analysis.MovingProjectorBookPrice
import D0.Analysis.MatrixThermalDensityBridge
import D0.Algebra.MovingProjectorPositiveChart

/-!
# Fixed-Gram bridge for the owned Book03 price

The Book price uses a real partition scalar and the fixed-Gram density bridge
uses the complex trace. On a Hermitian thermal matrix they are the same state.
The existing Book source then applies on the isometric moving-cut chart; this
module does not duplicate its derivative proof or assert physical admission.
-/

namespace D0.Analysis.MovingProjectorBookPrice

open Filter
open scoped Topology Matrix.Norms.Frobenius
open D0.Algebra.MovingProjectorTransport

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- The two existing fixed-Gram Gibbs states coincide for Hermitian Δ. -/
theorem matrixThermalState_eq_density
    (β : ℝ) (Δ : Matrix ι ι ℂ) (hHerm : star Δ = Δ) :
    matrixThermalState β Δ = matrixThermalDensity β Δ := by
  let E : Matrix ι ι ℂ := NormedSpace.exp ((-β) • Δ)
  let T : ℂ := Matrix.trace E
  have hE : star E = E := by
    dsimp [E]
    rw [NormedSpace.star_exp]
    simp [hHerm]
  have hT : star T = T := by
    simpa only [T, mul_one] using
      matrix_trace_selfadjoint_product_real E (1 : Matrix ι ι ℂ) hE (star_one _)
  have hTreal : ((T.re : ℝ) : ℂ) = T := Complex.conj_eq_iff_re.mp hT
  change (T.re)⁻¹ • E = T⁻¹ • E
  ext i j
  simp only [Matrix.smul_apply, Complex.real_smul, smul_eq_mul, Complex.ofReal_inv]
  rw [hTreal]

/--
The existing Book03 price source on the original isometric positive chart.
No local Hermiticity of Δ is needed for this real-valued derivative.
-/
theorem hasDerivAt_moving_projector_book03_price_of_isometric_cut [Nonempty ι]
    (β z : ℝ) {Δ P U : ℝ → Matrix ι ι ℂ}
    {dΔ dP dU : Matrix ι ι ℂ} {t : ℝ}
    (hβ : β ≠ 0) (hz0 : 0 ≤ z) (hz1 : z < 1)
    (hΔ : HasDerivAt Δ dΔ t) (hHerm : star (Δ t) = Δ t)
    (hP : HasDerivAt P dP t) (hU : HasDerivAt U dU t)
    (hIdem : ∀ᶠ s in 𝓝 t, P s * P s = P s)
    (hSelfAdjoint : ∀ᶠ s in 𝓝 t, star (P s) = P s)
    (hIsometry : star (U t) * U t = 1) :
    let K := generator (P t) dP
    let ρ := matrixThermalState β (Δ t)
    let C := cut (P t) (U t)
    let R := (1 - (z : ℂ) • (star C * C))⁻¹
    let V := (1 - P t) * (dU - comm K (U t)) * P t
    HasDerivAt (fun s => matrixBook03Price β z Δ P U s)
      (-(Matrix.trace (ρ * (dΔ - comm K (Δ t)))).re +
        z * (2 * (Matrix.trace (R * star C * V)).re)) t := by
  have hSlit := cut_feedback_det_mem_slitPlane (P t) (U t) z
    hIdem.self_of_nhds hSelfAdjoint.self_of_nhds hIsometry hz0 hz1
  exact hasDerivAt_moving_projector_book03_price β z hβ hΔ hHerm
    hP hU hIdem hSelfAdjoint hSlit

/--
Under local Hermiticity, the Book state is trace-normalized and its thermal
source is literally the complex trace of the same relative variation.
-/
theorem matrix_book_thermal_source_real [Nonempty ι]
    (β : ℝ) {Δ : ℝ → Matrix ι ι ℂ} {dΔ K : Matrix ι ι ℂ} {t : ℝ}
    (hΔ : HasDerivAt Δ dΔ t)
    (hLocalHerm : ∀ᶠ s in 𝓝 t, star (Δ s) = Δ s)
    (hK : star K = -K) :
    let E := NormedSpace.exp ((-β) • Δ t)
    let X := dΔ - comm K (Δ t)
    let ρ := matrixThermalState β (Δ t)
    star (Matrix.trace E) = Matrix.trace E ∧
      star (Matrix.trace (E * X)) = Matrix.trace (E * X) ∧
      Matrix.trace ρ = 1 ∧
      (((-(Matrix.trace (E * X)).re / matrixHeatPartition β (Δ t) : ℝ) : ℂ)) =
        -Matrix.trace (ρ * X) := by
  have hHerm : star (Δ t) = Δ t := hLocalHerm.self_of_nhds
  have hdΔ : star dΔ = dΔ := self_adjoint_tangent_of_curve hΔ hLocalHerm
  have hreal := matrix_thermal_relative_traces_real β (Δ t) dΔ K hHerm hdΔ hK
  have hρ := matrixThermalState_eq_density β (Δ t) hHerm
  have hratio := matrix_thermal_density_relative_trace β (Δ t) dΔ K hHerm hdΔ hK
  refine ⟨hreal.1, hreal.2, ?_, ?_⟩
  · rw [hρ]
    exact matrix_thermal_density_trace_one β (Δ t) hHerm
  · rw [hρ, hratio]
    simp [matrixHeatPartition, neg_div]

end D0.Analysis.MovingProjectorBookPrice
