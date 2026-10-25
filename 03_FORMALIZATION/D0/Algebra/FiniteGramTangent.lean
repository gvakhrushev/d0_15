import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic

/-!
# Generic finite Gram-matrix tangent algebra

This module owns only matrix algebra. It records the exact expansion of a
Gram map around a symmetric involutive frame and the explicit half-matrix
preimage of every symmetric direction. It makes no geometric or physical
selection claim.
-/

namespace D0.Algebra

open Matrix

/-- The finite Gram map defined by a fixed bilinear form `η`. -/
def finiteGram {ι : Type*} [Fintype ι]
    (η Θ : Matrix ι ι ℝ) : Matrix ι ι ℝ :=
  Θ * η * Θ.transpose

/-- Exact symmetrization witness: every symmetric matrix is `C + Cᵀ` for
`C = q/2`. -/
theorem symmetricMatrix_half {ι : Type*}
    (q : Matrix ι ι ℝ) (hq : q.transpose = q) :
    (2 : ℝ)⁻¹ • q + ((2 : ℝ)⁻¹ • q).transpose = q := by
  ext i j
  have hij := congrArg (fun M : Matrix ι ι ℝ => M i j) hq
  have hsym : q j i = q i j := by
    simpa [Matrix.transpose_apply] using hij
  simp [Matrix.add_apply, Matrix.transpose_apply, Matrix.smul_apply, hsym]
  ring

/-- The exact quadratic expansion of the finite Gram map at a symmetric
involutive frame `η`. The linear metric direction is `C + Cᵀ`; the full
quadratic remainder is retained. -/
theorem finiteGram_smul_expand {ι : Type*} [Fintype ι] [DecidableEq ι]
    (η C : Matrix ι ι ℝ) (t : ℝ)
    (hη_transpose : η.transpose = η) (hη_sq : η * η = 1) :
    finiteGram η (η + t • C) =
      η + t • (C + C.transpose) +
        t^2 • (C * η * C.transpose) := by
  unfold finiteGram
  rw [Matrix.transpose_add, Matrix.transpose_smul, hη_transpose]
  simp [Matrix.add_mul, Matrix.mul_add, Matrix.mul_assoc, hη_sq, smul_add,
    smul_smul, pow_two]
  abel

end D0.Algebra
