import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic

namespace D0.Cosmology

structure CoreParams where
  η : ℝ
  ρ_floor : ℝ
  L : Matrix (Fin 3) (Fin 3) ℝ
  δ₀ : ℝ

structure EmpiricalParams where
  z_pivot : ℝ
  gamma : ℝ
  A_amp : ℝ
  H0 : ℝ
  Ωm : ℝ

structure ExternalData where
  data : Fin 3 → ℝ
  covariance : Matrix (Fin 3) (Fin 3) ℝ

-- D0 core shape generator (must not depend on empirical parameters)
noncomputable def CoreShapeGenerator (cp : CoreParams) : Fin 3 → ℝ :=
  fun i => cp.η * (cp.L i i) + cp.ρ_floor + cp.δ₀

noncomputable def coreShapeEvaluated (cp : CoreParams) (ep : EmpiricalParams) : Fin 3 → ℝ :=
  CoreShapeGenerator cp

-- Empirical parameters only act as an external calibration/amplitude layer
noncomputable def RedshiftCalibration (shape : Fin 3 → ℝ) (ep : EmpiricalParams) : Fin 3 → ℝ :=
  fun i => shape i * ep.z_pivot + ep.gamma

noncomputable def AmplitudeNormalization (cal : Fin 3 → ℝ) (ep : EmpiricalParams) : Fin 3 → ℝ :=
  fun i => cal i * ep.A_amp

noncomputable def ExternalLikelihood (norm : Fin 3 → ℝ) (ed : ExternalData) : ℝ :=
  ∑ i, (norm i - ed.data i)^2

-- Guardrail 1: Core shape is strictly independent of empirical parameters
theorem core_shape_independent_of_empirical_parameters (cp : CoreParams) (ep1 ep2 : EmpiricalParams) :
    coreShapeEvaluated cp ep1 = coreShapeEvaluated cp ep2 := by
  unfold coreShapeEvaluated
  rfl

-- Guardrail 2: Any likelihood model depending on empirical parameters is not core closed
def isCoreClosed (f : CoreParams → EmpiricalParams → ExternalData → ℝ) : Prop :=
  ∃ g : CoreParams → ℝ, ∀ cp ep ed, f cp ep ed = g cp

theorem empirical_passport_not_core_closed (f : CoreParams → EmpiricalParams → ExternalData → ℝ)
    (h_depends : ∃ cp ep1 ep2 ed, f cp ep1 ed ≠ f cp ep2 ed) :
    ¬ isCoreClosed f := by
  intro h_closed
  unfold isCoreClosed at h_closed
  rcases h_closed with ⟨g, hg⟩
  rcases h_depends with ⟨cp, ep1, ep2, ed, h_neq⟩
  rw [hg cp ep1 ed, hg cp ep2 ed] at h_neq
  exact h_neq rfl

end D0.Cosmology
