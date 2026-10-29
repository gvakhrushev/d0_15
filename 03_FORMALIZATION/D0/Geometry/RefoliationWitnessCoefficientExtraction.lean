import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic

/-!
# Exact coefficient extraction from the refoliation witnesses

This module formalizes only the algebraic consequence of the three exact
constant-coefficient witness equations displayed in §4 of the pinned
refoliation proof from PR #334 (`c4a92cb0f2326bf7ae2a8127c49f5b65ea71ce5a`,
`PROOF_RU.md`, blob `03ad9147c46411099667658871f847e9f3bee883`).

The witness equations are inputs here. This module does not derive the
continuum Poisson bracket, the strong hypersurface-deformation algebra, its
canonical variables, or any D0 physical admission. It proves that if those
three exact evaluations hold with a common nonzero witness integral, then the
constant coefficients are forced as stated in the source.
-/

namespace D0.Geometry.RefoliationWitnessCoefficientExtraction

/-- The three source-displayed witness evaluations force the coefficients
`a*b = 1`, `lambda = 1/2`, and `C*D = 1` in the constant-coefficient family.

`gravityWitness` is the trace-free momentum witness with geometric value
`-2 * scale`; `traceWitness` is the independent trace witness whose required
geometric value is zero; `matterWitness` is the entrywise two-scalar witness.
All three are exact equalities, not numerical controls. -/
theorem refoliation_witness_equations_force_coefficients
    (scale a b lambda : ℝ) (C D : Matrix (Fin 2) (Fin 2) ℝ)
    (hscale : scale ≠ 0)
    (gravityWitness : a * b * (-2 * scale) = -2 * scale)
    (traceWitness : 2 * a * b * (1 - 2 * lambda) * scale = 0)
    (matterWitness : ∀ i j : Fin 2,
      scale * (C * D) i j = scale * (if i = j then (1 : ℝ) else 0)) :
    a * b = 1 ∧ lambda = (1 : ℝ) / 2 ∧ C * D = 1 := by
  have hgravityScale : (-2 : ℝ) * scale ≠ 0 :=
    mul_ne_zero (by norm_num) hscale
  have hab : a * b = 1 := by
    apply mul_right_cancel₀ hgravityScale
    simpa using gravityWitness
  have habCoeff : 2 * a * b = 2 := by
    calc
      2 * a * b = 2 * (a * b) := by ring
      _ = 2 := by rw [hab]; ring
  have htrace : 2 * (1 - 2 * lambda) * scale = 0 := by
    have h := traceWitness
    rw [habCoeff] at h
    exact h
  have htwoScale : (2 : ℝ) * scale ≠ 0 :=
    mul_ne_zero (by norm_num) hscale
  have htraceFactor : (1 - 2 * lambda) * (2 * scale) = 0 := by
    calc
      (1 - 2 * lambda) * (2 * scale) = 2 * (1 - 2 * lambda) * scale := by ring
      _ = 0 := htrace
  have hlambda : lambda = (1 : ℝ) / 2 := by
    rcases mul_eq_zero.mp htraceFactor with hzero | hzero
    · nlinarith
    · exact (htwoScale hzero).elim
  have hentry : ∀ i j : Fin 2, (C * D) i j = if i = j then (1 : ℝ) else 0 := by
    intro i j
    exact mul_left_cancel₀ hscale (matterWitness i j)
  have hCD : C * D = 1 := by
    ext i j
    simpa using hentry i j
  exact ⟨hab, hlambda, hCD⟩

end D0.Geometry.RefoliationWitnessCoefficientExtraction
