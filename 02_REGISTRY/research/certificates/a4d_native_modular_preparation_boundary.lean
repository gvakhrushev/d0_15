import D0.Bridge.TomitaTakesakiBridge
import D0.Dynamics.ToralAutomorphism
import D0.Representation.GoldenCoherentMemory
import Mathlib.Analysis.Normed.Module.Basic
import Mathlib.Tactic

/-! A bounded linear representation of the literal hyperbolic two-coordinate
step cannot be a real modular automorphism step. The finite density/Gibbs
reconstruction in the accompanying proof is analytic, not proved by this file. -/
namespace D0.Research.ModularPreparationBoundary
noncomputable section

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

theorem isometric_eigenvector_zero (U : E →ₗ[ℝ] E)
    (hU : ∀ x, ‖U x‖ = ‖x‖) (v : E) (r : ℝ)
    (hr : |r| ≠ 1) (hv : U v = r • v) : v = 0 := by
  have hn : |r| * ‖v‖ = ‖v‖ := by
    simpa [hv, norm_smul, Real.norm_eq_abs] using hU v
  have hz : (|r| - 1) * ‖v‖ = 0 := by nlinarith [hn]
  apply norm_eq_zero.mp
  exact (mul_eq_zero.mp hz).resolve_left (sub_ne_zero.mpr hr)

/-- These are precisely the two column equations for T=[[0,1],[1,-1]].
No faithful representation, finite or infinite dimensional, satisfies them
under a norm-isometric linear evolution. Nonlinear torus coordinates and
unbounded observables are outside this statement. -/
theorem golden_columns_zero (U : E →ₗ[ℝ] E)
    (hU : ∀ x, ‖U x‖ = ‖x‖) (a b : E)
    (ha : U a = b) (hb : U b = a - b)
    (p : ℝ) (hp : p + p^2 = 1) (hp0 : 0 < p) (hp1 : p < 1) :
    a = 0 ∧ b = 0 := by
  have hpp : 1 - p = p * p := by nlinarith [hp]
  have hqq : 2 + p = (1+p) * (1+p) := by nlinarith [hp]
  have hc : U (a + p • b) = p • (a + p • b) := by
    rw [map_add, map_smul, ha, hb]
    calc
      b + p • (a - b) = p • a + (1-p) • b := by module
      _ = p • (a + p • b) := by rw [hpp]; module
  have he : U (a - (1+p) • b) = (-(1+p)) • (a - (1+p) • b) := by
    rw [map_sub, map_smul, ha, hb]
    calc
      b - (1+p) • (a-b) = (-(1+p)) • a + (2+p) • b := by module
      _ = (-(1+p)) • (a - (1+p) • b) := by rw [hqq]; module
  have hc0 : a + p • b = 0 :=
    isometric_eigenvector_zero U hU _ p
      (by rw [abs_of_pos hp0]; exact ne_of_lt hp1) hc
  have he0 : a - (1+p) • b = 0 :=
    isometric_eigenvector_zero U hU _ (-(1+p))
      (by rw [abs_neg, abs_of_pos (by linarith : 0 < 1+p)]; linarith) he
  have hs : (1 + 2*p) • b = 0 := by
    calc
      (1 + 2*p) • b = (a + p • b) - (a - (1+p) • b) := by module
      _ = 0 := by rw [hc0, he0]; simp
  have hb0 : b = 0 :=
    (smul_eq_zero.mp hs).resolve_left (by linarith : (1+2*p : ℝ) ≠ 0)
  exact ⟨by simpa [hb0] using hc0, hb0⟩

open Matrix
open D0.Representation.GoldenCoherentMemory

/-- Literal prepared output from the existing full retained recording gate. -/
theorem blank_zero_output (a p : ℝ) :
    (fullStep a p).mulVec ![1,0,0,0] = ![a,0,0,p] := by
  simpa using blank_record_evolution a p 1 0

/-- A legitimate input of the declared unit-sphere interface gives a pure
retained marginal. Thus faithfulness is not a theorem for every input. -/
theorem separating_input_output (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) :
    a^2 + (-p)^2 = 1 ∧
    (fullStep a p).mulVec ![a,0,-p,0] = ![1,0,0,0] := by
  constructor
  · nlinarith [ha, hp]
  · rw [blank_record_evolution]
    ext i
    fin_cases i <;> simp <;> nlinarith [ha, hp]

end
end D0.Research.ModularPreparationBoundary

#check D0.Research.ModularPreparationBoundary.isometric_eigenvector_zero
#check D0.Research.ModularPreparationBoundary.golden_columns_zero
#check D0.Research.ModularPreparationBoundary.blank_zero_output
#check D0.Research.ModularPreparationBoundary.separating_input_output
#print D0.Bridge.BridgeAssumption.TomitaModularFlow
#check D0.Bridge.tomita_modular_flow_conditional
#print D0.Dynamics.T
#check D0.Representation.GoldenCoherentMemory.blank_record_evolution
#print axioms D0.Research.ModularPreparationBoundary.isometric_eigenvector_zero
#print axioms D0.Research.ModularPreparationBoundary.golden_columns_zero
#print axioms D0.Research.ModularPreparationBoundary.blank_zero_output
#print axioms D0.Research.ModularPreparationBoundary.separating_input_output
#print axioms D0.Bridge.tomita_modular_flow_conditional
#print axioms D0.Representation.GoldenCoherentMemory.blank_record_evolution
