import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Tactic

/-!
# Generic finite Gram-matrix algebra

This module owns only matrix algebra: Gram symmetry, isometry invariance, the
exact quadratic expansion at an arbitrary finite frame and its useful
specializations, and the explicit half-matrix preimage of every symmetric
direction. It makes no geometric or physical selection claim.
-/

namespace D0.Algebra

open Matrix

/-- The finite Gram map defined by a fixed bilinear form `η`. -/
def finiteGram {ι : Type*} [Fintype ι]
    (η Θ : Matrix ι ι ℝ) : Matrix ι ι ℝ :=
  Θ * η * Θ.transpose

/-- A Gram matrix is symmetric when its fixed bilinear form is symmetric. -/
theorem finiteGram_symmetric {ι : Type*} [Fintype ι]
    (η Θ : Matrix ι ι ℝ) (hη_transpose : η.transpose = η) :
    (finiteGram η Θ).transpose = finiteGram η Θ := by
  simp [finiteGram, Matrix.transpose_mul, hη_transpose, Matrix.mul_assoc]

/-- Right multiplication by an isometry of `η` leaves its Gram matrix fixed. -/
theorem finiteGram_right_invariant {ι : Type*} [Fintype ι]
    (η Θ Λ : Matrix ι ι ℝ)
    (hΛ : Λ * η * Λ.transpose = η) :
    finiteGram η (Θ * Λ) = finiteGram η Θ := by
  unfold finiteGram
  rw [Matrix.transpose_mul]
  calc
    Θ * Λ * η * (Λ.transpose * Θ.transpose) =
        Θ * (Λ * η * Λ.transpose) * Θ.transpose := by
          simp only [Matrix.mul_assoc]
    _ = Θ * η * Θ.transpose := by rw [hΛ]

/-- A frame-dressed isometry transports the endpoint Gram form exactly.
Only the frame being inverted, `Θy`, must be nondegenerate. -/
theorem finiteGram_dressed_transport_compatible {ι : Type*}
    [Fintype ι] [DecidableEq ι]
    (η Θx L Θy : Matrix ι ι ℝ)
    (hL : L * η * L.transpose = η) (hΘy : IsUnit Θy.det) :
    (Θx * L * Θy⁻¹) * finiteGram η Θy *
        (Θx * L * Θy⁻¹).transpose = finiteGram η Θx := by
  have hcancelLeft : Θy⁻¹ * Θy = (1 : Matrix ι ι ℝ) :=
    Matrix.nonsing_inv_mul Θy hΘy
  have hcancelRight : Θy.transpose * (Θy⁻¹).transpose =
      (1 : Matrix ι ι ℝ) := by
    rw [← Matrix.transpose_mul]
    rw [Matrix.nonsing_inv_mul Θy hΘy]
    simp
  unfold finiteGram
  rw [Matrix.transpose_mul, Matrix.transpose_mul]
  calc
    (Θx * L * Θy⁻¹) * (Θy * η * Θy.transpose) *
        ((Θy⁻¹).transpose * (L.transpose * Θx.transpose)) =
      Θx * (L * (Θy⁻¹ * Θy) * η *
        (Θy.transpose * (Θy⁻¹).transpose) * L.transpose) * Θx.transpose := by
          noncomm_ring
    _ = Θx * (L * η * L.transpose) * Θx.transpose := by
          rw [hcancelLeft, hcancelRight]
          noncomm_ring
    _ = Θx * η * Θx.transpose := by
          exact congrArg (fun M : Matrix ι ι ℝ => Θx * M * Θx.transpose) hL

/-- Frame-dressed transport is invariant under independent endpoint frame
changes when the link transforms by the corresponding two-sided action. -/
theorem finiteMatrix_dressed_transport_frame_invariant {ι : Type*}
    [Fintype ι] [DecidableEq ι]
    (Θx L Θy Λx Λy : Matrix ι ι ℝ)
    (hΛx : IsUnit Λx.det) (hΛy : IsUnit Λy.det) :
    (Θx * Λx) * (Λx⁻¹ * L * Λy) * (Θy * Λy)⁻¹ =
      Θx * L * Θy⁻¹ := by
  have hx1 : Λx * Λx⁻¹ = (1 : Matrix ι ι ℝ) :=
    Matrix.mul_nonsing_inv Λx hΛx
  have hy1 : Λy * Λy⁻¹ = (1 : Matrix ι ι ℝ) :=
    Matrix.mul_nonsing_inv Λy hΛy
  rw [Matrix.mul_inv_rev]
  calc
    (Θx * Λx) * (Λx⁻¹ * L * Λy) * (Λy⁻¹ * Θy⁻¹) =
        Θx * (Λx * Λx⁻¹) * L * (Λy * Λy⁻¹) * Θy⁻¹ := by
          simp only [Matrix.mul_assoc]
    _ = Θx * L * Θy⁻¹ := by rw [hx1, hy1]; simp

/-- With invertible endpoint frames, equality of dressed transports is
equivalent to the corresponding two-sided change of the undressed link. -/
theorem finiteMatrix_dressed_transport_eq_iff_frame_action {ι : Type*}
    [Fintype ι] [DecidableEq ι]
    (Θx Θy Λx Λy L L' : Matrix ι ι ℝ)
    (hΘx : IsUnit Θx.det) (hΘy : IsUnit Θy.det)
    (hΛx : IsUnit Λx.det) (hΛy : IsUnit Λy.det) :
    (Θx * Λx) * L' * (Θy * Λy)⁻¹ = Θx * L * Θy⁻¹ ↔
      L' = Λx⁻¹ * L * Λy := by
  constructor
  · intro h
    have hcancel : Λx * L' * Λy⁻¹ = L := by
      have h' := congrArg (fun M : Matrix ι ι ℝ => Θx⁻¹ * M * Θy) h
      rw [Matrix.mul_inv_rev] at h'
      change Θx⁻¹ * ((Θx * Λx) * L' * (Λy⁻¹ * Θy⁻¹)) * Θy =
          Θx⁻¹ * (Θx * L * Θy⁻¹) * Θy at h'
      have hleft : Θx⁻¹ * Θx = 1 := Matrix.nonsing_inv_mul Θx hΘx
      have hright : Θy⁻¹ * Θy = 1 := Matrix.nonsing_inv_mul Θy hΘy
      calc
        Λx * L' * Λy⁻¹ = 1 * (Λx * L' * Λy⁻¹) * 1 := by simp
        _ = (Θx⁻¹ * Θx) * (Λx * L' * Λy⁻¹) * (Θy⁻¹ * Θy) := by
              rw [hleft, hright]
        _ = Θx⁻¹ * ((Θx * Λx) * L' * (Λy⁻¹ * Θy⁻¹)) * Θy := by
              noncomm_ring
        _ = Θx⁻¹ * (Θx * L * Θy⁻¹) * Θy := h'
        _ = L := by
              calc
                Θx⁻¹ * (Θx * L * Θy⁻¹) * Θy =
                    (Θx⁻¹ * Θx) * L * (Θy⁻¹ * Θy) := by noncomm_ring
                _ = L := by rw [hleft, hright]; simp
    have hleft : Λx⁻¹ * Λx = 1 := Matrix.nonsing_inv_mul Λx hΛx
    have hright : Λy⁻¹ * Λy = 1 := Matrix.nonsing_inv_mul Λy hΛy
    have h' := congrArg (fun M : Matrix ι ι ℝ => Λx⁻¹ * M * Λy) hcancel
    calc
      L' = 1 * L' * 1 := by simp
      _ = (Λx⁻¹ * Λx) * L' * (Λy⁻¹ * Λy) := by rw [hleft, hright]
      _ = Λx⁻¹ * (Λx * L' * Λy⁻¹) * Λy := by noncomm_ring
      _ = Λx⁻¹ * L * Λy := h'
  · intro hL
    rw [hL]
    exact finiteMatrix_dressed_transport_frame_invariant
      Θx L Θy Λx Λy hΛx hΛy

/-- On a nondegenerate left frame, equality of finite Gram matrices is exactly
membership in the right orbit of the isometry group of the fixed form. The
fixed form `η` itself need not be invertible; only the reference frame `Θ`
must be. -/
theorem finiteGram_right_orbit_complete {ι : Type*} [Fintype ι]
    [DecidableEq ι] (η Θ Ψ : Matrix ι ι ℝ) (hΘ : IsUnit Θ.det) :
    finiteGram η Θ = finiteGram η Ψ ↔
      ∃ Λ : Matrix ι ι ℝ, finiteGram η Λ = η ∧ Ψ = Θ * Λ := by
  constructor
  · intro hgram
    let Λ : Matrix ι ι ℝ := Θ⁻¹ * Ψ
    have hgram' : Θ * η * Θ.transpose = Ψ * η * Ψ.transpose := by
      simpa [finiteGram] using hgram
    have hright : Θ.transpose * (Θ⁻¹).transpose = 1 := by
      rw [← Matrix.transpose_mul]
      rw [Matrix.nonsing_inv_mul Θ hΘ]
      simp
    have hΛ : finiteGram η Λ = η := by
      unfold finiteGram
      dsimp [Λ]
      calc
        (Θ⁻¹ * Ψ) * η * (Θ⁻¹ * Ψ).transpose =
            Θ⁻¹ * (Ψ * η * Ψ.transpose) * (Θ⁻¹).transpose := by
              rw [Matrix.transpose_mul]
              simp only [Matrix.mul_assoc]
        _ = Θ⁻¹ * (Θ * η * Θ.transpose) * (Θ⁻¹).transpose := by
              rw [hgram']
        _ = (Θ⁻¹ * Θ) * η *
              (Θ.transpose * (Θ⁻¹).transpose) := by
              simp only [Matrix.mul_assoc]
        _ = η := by
              rw [Matrix.nonsing_inv_mul Θ hΘ, hright]
              simp
    refine ⟨Λ, hΛ, ?_⟩
    dsimp [Λ]
    calc
      Ψ = 1 * Ψ := by simp
      _ = (Θ * Θ⁻¹) * Ψ := by rw [Matrix.mul_nonsing_inv Θ hΘ]
      _ = Θ * (Θ⁻¹ * Ψ) := by rw [Matrix.mul_assoc]
  · rintro ⟨Λ, hΛ, hΨ⟩
    rw [hΨ]
    exact (finiteGram_right_invariant η Θ Λ (by
      simpa [finiteGram] using hΛ)).symm

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

/-- Exact quadratic expansion of the finite Gram map around any base frame.
The first-order source is the full two-sided variation and the quadratic
remainder is retained. -/
theorem finiteGram_add_smul_expand {ι : Type*} [Fintype ι]
    (η Θ C : Matrix ι ι ℝ) (t : ℝ) :
    finiteGram η (Θ + t • C) =
      finiteGram η Θ +
        t • (C * η * Θ.transpose + Θ * η * C.transpose) +
        t^2 • (C * η * C.transpose) := by
  unfold finiteGram
  rw [Matrix.transpose_add, Matrix.transpose_smul]
  simp [Matrix.add_mul, Matrix.mul_add, Matrix.mul_assoc, smul_add,
    smul_smul, pow_two]
  abel

/-- Exact normalized difference of the finite Gram path at any baseline.
The quadratic contribution remains as a linear-in-`t` remainder. -/
theorem finiteGram_add_smul_difference_quotient {ι : Type*} [Fintype ι]
    (η Θ C : Matrix ι ι ℝ) (t : ℝ) (ht : t ≠ 0) :
    t⁻¹ • (finiteGram η (Θ + t • C) - finiteGram η Θ) =
      (C * η * Θ.transpose + Θ * η * C.transpose) +
        t • (C * η * C.transpose) := by
  let L := C * η * Θ.transpose + Θ * η * C.transpose
  let Q := C * η * C.transpose
  rw [finiteGram_add_smul_expand]
  change t⁻¹ • (finiteGram η Θ + t • L + t^2 • Q - finiteGram η Θ) =
    L + t • Q
  have hcancel :
      finiteGram η Θ + t • L + t^2 • Q - finiteGram η Θ = t • L + t^2 • Q := by
    abel
  rw [hcancel]
  simp only [smul_add, smul_smul]
  have hlinear : t⁻¹ * t = 1 := inv_mul_cancel₀ ht
  have hquadratic : t⁻¹ * t^2 = t := by
    rw [pow_two]
    calc
      t⁻¹ * (t * t) = (t⁻¹ * t) * t := by ring
      _ = t := by rw [hlinear]; ring
  rw [hlinear, one_smul, hquadratic]

/-- The exact quadratic expansion at a symmetric involutive frame `η`. The
linear metric direction is `C + Cᵀ`; this compatibility theorem specializes
the arbitrary-frame expansion above. -/
theorem finiteGram_smul_expand {ι : Type*} [Fintype ι] [DecidableEq ι]
    (η C : Matrix ι ι ℝ) (t : ℝ)
    (hη_transpose : η.transpose = η) (hη_sq : η * η = 1) :
    finiteGram η (η + t • C) =
      η + t • (C + C.transpose) +
        t^2 • (C * η * C.transpose) := by
  simpa [finiteGram, Matrix.mul_assoc, hη_transpose, hη_sq] using
    finiteGram_add_smul_expand η η C t

/-- Exact expansion around the identity coframe. This compatibility theorem
specializes `finiteGram_add_smul_expand` and keeps the source convention
`C η + η Cᵀ`. -/
theorem finiteGram_one_smul_expand {ι : Type*} [Fintype ι] [DecidableEq ι]
    (η C : Matrix ι ι ℝ) (t : ℝ) :
    finiteGram η (1 + t • C) =
      η + t • (C * η + η * C.transpose) +
        t^2 • (C * η * C.transpose) := by
  simpa [finiteGram, Matrix.mul_assoc] using
    finiteGram_add_smul_expand η 1 C t

end D0.Algebra
