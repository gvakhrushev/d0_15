import Mathlib.Analysis.InnerProductSpace.Positive
import Mathlib.Analysis.Matrix.Order

/-!
# Gram matrices and actual Hilbert-space norm comparisons

An explicit orthonormal basis transfers a pointwise squared-norm comparison
to positive-semidefinite order of the corresponding Gram matrices. The maps
may be singular. The norm is the given Hilbert norm, not an entrywise norm.
-/

noncomputable section

namespace D0.Analysis

open scoped ComplexOrder

variable {V W : Type*} [NormedAddCommGroup V] [InnerProductSpace ℂ V]
  [FiniteDimensional ℂ V] [NormedAddCommGroup W] [InnerProductSpace ℂ W]
  [FiniteDimensional ℂ W]
  {n : Type*} [Fintype n] [DecidableEq n]

/-- The Gram operator in a supplied orthonormal basis of its input space. -/
def gramMatrix (K : V →ₗ[ℂ] W) (b : OrthonormalBasis n ℂ V) : Matrix n n ℂ :=
  (K.adjoint ∘ₗ K).toMatrix b.toBasis b.toBasis

theorem gramMatrix_posSemidef (K : V →ₗ[ℂ] W) (b : OrthonormalBasis n ℂ V) :
    (gramMatrix K b).PosSemidef := by
  exact (LinearMap.posSemidef_toMatrix_iff b).mpr
    (LinearMap.isPositive_adjoint_comp_self K)

/-- This is exactly the usual matrix `K†K`, with both coordinate maps explicit. -/
theorem gramMatrix_eq_conjTranspose_mul
    {m : Type*} [Fintype m] [DecidableEq m]
    (K : V →ₗ[ℂ] W) (b : OrthonormalBasis n ℂ V) (c : OrthonormalBasis m ℂ W) :
    gramMatrix K b =
      (K.toMatrix b.toBasis c.toBasis).conjTranspose * K.toMatrix b.toBasis c.toBasis := by
  rw [gramMatrix, LinearMap.toMatrix_comp _ c.toBasis,
    LinearMap.toMatrix_adjoint]

/-- A comparison on every vector is transferred to the entire Gram operator. -/
theorem gramMatrix_smul_sub_smul_posSemidef
    (K L : V →ₗ[ℂ] W) (b : OrthonormalBasis n ℂ V) (r s : ℝ)
    (h : ∀ x, r * ‖K x‖ ^ 2 ≤ s * ‖L x‖ ^ 2) :
    ((s : ℂ) • gramMatrix L b - (r : ℂ) • gramMatrix K b).PosSemidef := by
  have hpos : ((s : ℂ) • (L.adjoint ∘ₗ L) -
      (r : ℂ) • (K.adjoint ∘ₗ K)).IsPositive := by
    refine ⟨((LinearMap.isPositive_adjoint_comp_self L).isSymmetric.smul (by simp)).sub
      ((LinearMap.isPositive_adjoint_comp_self K).isSymmetric.smul (by simp)), ?_⟩
    intro x
    have hquad (F : V →ₗ[ℂ] W) (u : ℝ) :
        (inner ℂ ((u : ℂ) • F.adjoint (F x)) x).re = u * ‖F x‖ ^ 2 := by
      rw [inner_smul_left, LinearMap.adjoint_inner_left]
      have hu : starRingEnd ℂ (u : ℂ) = (u : ℂ) := by simp
      rw [hu, Complex.mul_re]
      simp only [Complex.ofReal_re, Complex.ofReal_im, zero_mul, sub_zero]
      congr 1
      exact (norm_sq_eq_re_inner (𝕜 := ℂ) (F x)).symm
    change 0 ≤ (inner ℂ
      ((s : ℂ) • L.adjoint (L x) - (r : ℂ) • K.adjoint (K x)) x).re
    rw [inner_sub_left, Complex.sub_re, hquad, hquad]
    exact sub_nonneg.mpr (h x)
  simpa only [gramMatrix, map_sub, map_smul] using
    (LinearMap.posSemidef_toMatrix_iff b).mpr hpos

theorem gramMatrix_sub_smul_posSemidef
    (K L : V →ₗ[ℂ] W) (b : OrthonormalBasis n ℂ V) (r : ℝ)
    (h : ∀ x, r * ‖K x‖ ^ 2 ≤ ‖L x‖ ^ 2) :
    (gramMatrix L b - (r : ℂ) • gramMatrix K b).PosSemidef := by
  simpa using gramMatrix_smul_sub_smul_posSemidef K L b r 1 (by simpa using h)

theorem gramMatrix_smul_sub_posSemidef
    (K L : V →ₗ[ℂ] W) (b : OrthonormalBasis n ℂ V) (r : ℝ)
    (h : ∀ x, ‖L x‖ ^ 2 ≤ r * ‖K x‖ ^ 2) :
    ((r : ℂ) • gramMatrix K b - gramMatrix L b).PosSemidef := by
  simpa using gramMatrix_smul_sub_smul_posSemidef L K b 1 r (by simpa using h)

end D0.Analysis

end
