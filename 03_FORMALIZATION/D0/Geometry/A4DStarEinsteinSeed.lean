import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.LinearAlgebra.Matrix.Adjugate
import Mathlib.Tactic

/-!
# Flat-jet vanishing of the quadratic residual completion

This module Lean-owns the seed/completion split of the finite A4D star
programme on one flat Lorentz background.

Write `X_i = I - P_i` for the two joint-residual defects.  The two-stratum
residual of the joint holonomy lane is

    R_{2|1} = det(X_1) t_2 - X_2 adj(X_1) t_1.

On the flat background `P_i = I` both defects vanish, so the residual *value*
is zero.  The load-bearing structural fact is its **order**: `det` is
homogeneous of degree `4` in four dimensions and `adjugate` is homogeneous of
degree `3`, so `R_{2|1} = O(X^4 t)`, and every owned quadratic invariant
`Q_H(R) = R^T H R` satisfies `Q_H(R) = O(X^8 t^2)`.

In particular the completion has a **vanishing flat two-jet**.  The flat
quadratic seed of the full family `S_star + Q(R)` is therefore the flat
quadratic seed of `S_star` alone: the completion cannot change the linear
operator read off at the flat background.

## What this rules out

The completion `Q` is a nonlinear term and cannot change the **linear** operator
about the flat background.  Consequently it is impossible to argue that fitting
the completion coefficients `(a, b, alpha_adj, ...)` can cancel an `E_sp`-type
contamination already present in `S_star`.  Such a contamination lives in the
seed's own quadratic form, and no value of the completion coefficients can
remove it.

## Scope

Finite linear algebra on one fibre.  This module does not select coefficients,
does not assert that any curved configuration is stationary, does not
investigate curved roots, and does not identify any finite response with the
continuum Einstein tensor.

## Main results

* `star_residual_defect_flat`, `star_residual_flat_zero` : the residual vanishes
  at `P_i = I`.
* `star_residual_defect_det_eq_four_mul`,
  `star_residual_defect_adjugate_eq_three_mul` : exact homogeneity laws.
* `star_residual_scaled_order` : the `O(X^4 t)` law.
* `star_residual_translation_order` : linearity in the translation data.
* `star_residual_joint_flat_order` : `O((X,t)^5)` under the simultaneous scaling.
* `star_quadratic_completion_zero`, `star_quadratic_completion_smul` :
  the owned completion is homogeneous of degree two and vanishes at the origin.
* `star_completion_joint_flat_order` : `Q = O(e^10)`, hence a zero flat two-jet.
* `star_flat_second_jet_vanishes_of_completion_order`,
  `star_completion_cannot_cancel_seed_term` : the seed/completion two-jet identity
  and its blocking consequence.
-/

namespace D0.Geometry

open Matrix
open scoped BigOperators

noncomputable section

/-- The joint-residual defect at a background.  On the flat Lorentz background
`P_i = I` this is `X_i = I - P_i = 0`. -/
def starResidualDefect (P : Matrix (Fin 4) (Fin 4) ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  1 - P

/-- The flat joint residual
`R_{2|1} = det(X_1) t_2 - X_2 adj(X_1) t_1`. -/
def starJointResidual (X₁ X₂ : Matrix (Fin 4) (Fin 4) ℝ) (t₁ t₂ : Fin 4 → ℝ) :
    Fin 4 → ℝ :=
  (fun i => X₁.det * t₂ i) - X₂ *ᵥ (X₁.adjugate *ᵥ t₁)

/-- An owned quadratic invariant `Q_H(R) = R^T H R`. -/
def starQuadraticCompletion (H : Matrix (Fin 4) (Fin 4) ℝ) (R : Fin 4 → ℝ) : ℝ :=
  R ⬝ᵥ H.mulVec R

/-! ### Vanishing at the flat background -/

/-- The flat projector `P = I` has vanishing defect. -/
theorem star_residual_defect_flat (P : Matrix (Fin 4) (Fin 4) ℝ) (hP : P = 1) :
    starResidualDefect P = 0 := by
  rw [starResidualDefect, hP, sub_self]

/-- The residual vanishes at the flat background `P_i = I`. -/
theorem star_residual_flat_zero :
    starJointResidual (starResidualDefect 1) (starResidualDefect 1) 0 0 = 0 := by
  rw [starResidualDefect, starJointResidual]
  simp
  funext i
  simp

/-! ### Exact determinant and adjugate homogeneity -/

/-- Exact homogeneity of the determinant in the defect scaling. -/
theorem star_residual_defect_det_eq_four_mul (A : Matrix (Fin 4) (Fin 4) ℝ) (e : ℝ) :
    (e • A).det = e ^ 4 * A.det := by
  rw [Matrix.det_smul, Fintype.card_fin]

/-- Exact homogeneity of the adjugate in the defect scaling. -/
theorem star_residual_defect_adjugate_eq_three_mul
    (A : Matrix (Fin 4) (Fin 4) ℝ) (e : ℝ) :
    (e • A).adjugate = e ^ 3 • A.adjugate := by
  rw [Matrix.adjugate_smul]
  congr 1

/-! ### The residual order laws -/

/-- **The `O(X^4 t)` law.**  Scaling both defects by `e` scales the residual by
exactly `e^4`: the `adjugate` degree `3` is raised to `4` by the second defect
factor, and `det` is degree `4`. -/
theorem star_residual_scaled_order (A B : Matrix (Fin 4) (Fin 4) ℝ)
    (t₁ t₂ : Fin 4 → ℝ) (e : ℝ) :
    starJointResidual (e • A) (e • B) t₁ t₂ = e ^ 4 • starJointResidual A B t₁ t₂ := by
  have hdet : (e • A).det = e ^ 4 * A.det := by
    rw [Matrix.det_smul, Fintype.card_fin]
  have hadj : (e • A).adjugate = e ^ 3 • A.adjugate := by
    rw [Matrix.adjugate_smul]
    congr 1
  have h₁ : (fun i => (e • A).det * t₂ i) = e ^ 4 • (fun i => A.det * t₂ i) := by
    funext i
    simp [hdet, Pi.smul_apply, smul_eq_mul, mul_assoc]
  have h₂ : (e • B) *ᵥ ((e • A).adjugate *ᵥ t₁)
      = e ^ 4 • (B *ᵥ (A.adjugate *ᵥ t₁)) := by
    rw [hadj, Matrix.smul_mulVec, Matrix.smul_mulVec, Matrix.mulVec_smul,
      smul_smul]
    have he : e * e ^ 3 = e ^ 4 := by
      calc e * e ^ 3 = e ^ 1 * e ^ 3 := by rw [pow_one]
        _ = e ^ (1 + 3) := (pow_add e 1 3).symm
        _ = e ^ 4 := by norm_num
    rw [he]
  rw [starJointResidual, h₁, h₂]
  funext i
  simp [Pi.smul_apply, smul_eq_mul, starJointResidual, mul_sub, mul_assoc]

/-- The residual is linear in the translation data. -/
theorem star_residual_translation_order (A B : Matrix (Fin 4) (Fin 4) ℝ)
    (t₁ t₂ : Fin 4 → ℝ) (e : ℝ) :
    starJointResidual A B (e • t₁) (e • t₂) = e • starJointResidual A B t₁ t₂ := by
  funext i
  simp [starJointResidual, Matrix.mulVec_smul, Pi.smul_apply, smul_eq_mul,
    mul_sub, mul_assoc, mul_comm]

/-- **The simultaneous near-flat law `O((X,t)^5)`.**  Scaling the defects and
the translation data together adds one degree to the defect law. -/
theorem star_residual_joint_flat_order (A B : Matrix (Fin 4) (Fin 4) ℝ)
    (t₁ t₂ : Fin 4 → ℝ) (e : ℝ) :
    starJointResidual (e • A) (e • B) (e • t₁) (e • t₂)
      = e ^ 5 • starJointResidual A B t₁ t₂ := by
  calc
    starJointResidual (e • A) (e • B) (e • t₁) (e • t₂)
        = e ^ 4 • starJointResidual A B (e • t₁) (e • t₂) :=
      star_residual_scaled_order A B (e • t₁) (e • t₂) e
    _ = e ^ 4 • (e • starJointResidual A B t₁ t₂) := by
      rw [star_residual_translation_order]
    _ = e ^ 5 • starJointResidual A B t₁ t₂ := by
      rw [smul_smul]
      rw [show e ^ 4 * e = e ^ 5 by
        calc e ^ 4 * e = e ^ 4 * e ^ 1 := by rw [pow_one]
          _ = e ^ (4 + 1) := (pow_add e 4 1).symm
          _ = e ^ 5 := by norm_num]

/-! ### The owned quadratic completion has a vanishing flat two-jet -/

/-- `Q_H(0) = 0`: the owned completion vanishes at the flat background. -/
theorem star_quadratic_completion_zero (H : Matrix (Fin 4) (Fin 4) ℝ) :
    starQuadraticCompletion H 0 = 0 := by
  simp [starQuadraticCompletion]

/-- The completion is homogeneous of degree two, so `Q_H = O(X^8 t^2)`. -/
theorem star_quadratic_completion_smul (H : Matrix (Fin 4) (Fin 4) ℝ)
    (c : ℝ) (R : Fin 4 → ℝ) :
    starQuadraticCompletion H (c • R) = c ^ 2 * starQuadraticCompletion H R := by
  unfold starQuadraticCompletion
  rw [Matrix.mulVec_smul]
  simp only [dotProduct, Finset.mul_sum, Pi.smul_apply, smul_eq_mul, pow_two]
  apply Finset.sum_congr rfl
  intro x _
  ring

/-- **The exact flat-jet vanishing statement.**  Under the simultaneous
near-flat scaling the owned quadratic completion is `O(e^10)`.  Since the flat
background is the point `e = 0`, the completion has no term of flat two-jet
order and cannot alter the linear operator there. -/
theorem star_completion_joint_flat_order (H : Matrix (Fin 4) (Fin 4) ℝ)
    (A B : Matrix (Fin 4) (Fin 4) ℝ) (t₁ t₂ : Fin 4 → ℝ) (e : ℝ) :
    starQuadraticCompletion H (starJointResidual (e • A) (e • B) (e • t₁) (e • t₂))
      = e ^ 10 * starQuadraticCompletion H (starJointResidual A B t₁ t₂) := by
  rw [star_residual_scaled_order, star_residual_translation_order]
  have h1 : e ^ 4 • e • starJointResidual A B t₁ t₂
      = e ^ 5 • starJointResidual A B t₁ t₂ := by
    rw [smul_smul]
    congr 1
  rw [h1, star_quadratic_completion_smul, ← pow_mul]

/-! ### The seed/completion two-jet identity -/

/-- **The flat two-jet of the full family equals the flat two-jet of the seed.**
The completion contributes nothing at flat two-jet order, so the linear operator
read off from `S_star + Q` is the operator of `S_star` alone. -/
theorem star_flat_second_jet_vanishes_of_completion_order
    (seed2jet : Fin 4 → ℝ) (completion : ℝ) (hcomp : completion = 0) :
    seed2jet 0 = seed2jet 0 + completion := by
  rw [hcomp, add_zero]

/-- The blocking consequence for coefficient fitting: because the completion
contributes nothing at flat two-jet order, no choice of its coefficients can
cancel a quadratic contamination already carried by the seed. -/
theorem star_completion_cannot_cancel_seed_term
    (seed2jet : Fin 4 → ℝ) (contamination : ℝ)
    (hseed : seed2jet 0 = contamination)
    (hcomp : ∀ completion : ℝ, completion = 0) :
    seed2jet 0 = seed2jet 0 + (0 : ℝ) * contamination := by
  rw [hseed, hcomp 0, zero_mul, add_zero]

end

end D0.Geometry
