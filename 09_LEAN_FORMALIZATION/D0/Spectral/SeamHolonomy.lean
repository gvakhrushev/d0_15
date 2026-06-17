import Mathlib.Data.Matrix.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic

/-!
# D0-Q8-SIN-CHANNEL-001 — the seam holonomy `U(θ)=cosθ·I+sinθ·G` rides the off-diagonal `sin` channel

The seam generator `G` (the Q₈ / quaternion off-diagonal block) satisfies `G² = −I`. The one-parameter
closure-holonomy `U(θ) = cos θ·I + sin θ·G` is then an orthogonal rotation whose **diagonal**
(role-preserving) entry is `cos θ` and whose **off-diagonal** (role-changing) entry is `sin θ`. So a
correction transported between distinct roles is carried by the `sin` channel, not the trace (`cos`) —
this is why the α closure-holonomy uses `sin(12/5)` (`vp_seam_holonomy_alpha.py`).

This is the genuine algebra the cert `05_CERTS/vp_q8_sin_channel.py` checks numerically — proved here,
not asserted by a definitional shell.
-/

namespace D0.Spectral

open Matrix

/-- The seam generator `G = !![0,-1; 1,0]` (the Q₈ off-diagonal block). -/
def seamG : Matrix (Fin 2) (Fin 2) ℝ := !![0, -1; 1, 0]

/-- **`G² = −I`** — the quaternion / Q₈ relation that forces the `sin`/`cos` split of `exp(θG)`. -/
theorem seamG_sq : seamG * seamG = -1 := by
  unfold seamG
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two, Matrix.neg_apply]

/-- The closure-holonomy `U(θ) = cos θ·I + sin θ·G` (`= exp(θG)` since `G² = −I`). -/
noncomputable def seamU (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  Real.cos θ • (1 : Matrix (Fin 2) (Fin 2) ℝ) + Real.sin θ • seamG

/-- **Off-diagonal (role-changing) channel = `sin θ`.** -/
theorem seamU_offdiagonal (θ : ℝ) : seamU θ 1 0 = Real.sin θ := by
  unfold seamU seamG
  simp [Matrix.add_apply, Matrix.smul_apply]

/-- **Diagonal (role-preserving) channel = `cos θ`.** -/
theorem seamU_diagonal (θ : ℝ) : seamU θ 0 0 = Real.cos θ := by
  unfold seamU seamG
  simp [Matrix.add_apply, Matrix.smul_apply]

/-- **The holonomy is a rotation:** `U(θ)ᵀ · U(θ) = I` (uses `sin²+cos²=1`). -/
theorem seamU_orthogonal (θ : ℝ) : (seamU θ)ᵀ * (seamU θ) = 1 := by
  unfold seamU seamG
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two, Matrix.transpose_apply, Matrix.one_apply,
      Matrix.add_apply, Matrix.smul_apply] <;>
    nlinarith [Real.sin_sq_add_cos_sq θ]

end D0.Spectral
