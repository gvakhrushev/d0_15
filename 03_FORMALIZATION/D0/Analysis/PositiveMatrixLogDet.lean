import Mathlib.Analysis.Matrix.Order
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.NoncommRing
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/-!
# Positive matrix log determinants and affine spectral pencils

The finite matrix bridge used by §5, equations (10)--(12), of the existing
same-task return-price source. Loewner monotonicity is proved by positive
factorization and determinant algebra. Affine spectral formulas retain a
strictly positive identity term and allow a singular positive semidefinite
past, including the zero matrix. No physical execution is selected.
-/

noncomputable section

namespace D0.Analysis.PositiveMatrixLogDet

open Matrix
open scoped ComplexOrder MatrixOrder BigOperators

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- The positive regularized return pencil; `S` itself need not be invertible. -/
def affinePencil (S : Matrix n n ℂ) (a q : ℝ) : Matrix n n ℂ :=
  (a : ℂ) • 1 + (q : ℂ) • S

private theorem det_unitary_conjugate (U : unitary (Matrix n n ℂ))
    (D : Matrix n n ℂ) :
    (Unitary.conjStarAlgAut ℂ _ U D).det = D.det := by
  have hU : (U : Matrix n n ℂ).det * (star (U : Matrix n n ℂ)).det = 1 := by
    rw [← Matrix.det_mul, Unitary.mul_star_self_of_mem U.property, Matrix.det_one]
  simp only [Unitary.conjStarAlgAut_apply, Matrix.det_mul]
  calc
    (U : Matrix n n ℂ).det * D.det * (star (U : Matrix n n ℂ)).det =
        D.det * ((U : Matrix n n ℂ).det * (star (U : Matrix n n ℂ)).det) := by ring
    _ = D.det := by rw [hU, mul_one]

private theorem trace_unitary_conjugate (U : unitary (Matrix n n ℂ))
    (D : Matrix n n ℂ) :
    (Unitary.conjStarAlgAut ℂ _ U D).trace = D.trace := by
  simp only [Unitary.conjStarAlgAut_apply]
  rw [Matrix.trace_mul_cycle, Unitary.coe_star_mul_self, one_mul]

/-- The original spectral basis diagonalizes every affine pencil in the same `S`. -/
theorem affinePencil_spectral (S : Matrix n n ℂ) (hS : S.IsHermitian) (a q : ℝ) :
    affinePencil S a q = Unitary.conjStarAlgAut ℂ _ hS.eigenvectorUnitary
      (Matrix.diagonal (fun i => ((a + q * hS.eigenvalues i : ℝ) : ℂ))) := by
  have hdiag : Matrix.diagonal (fun i => ((a + q * hS.eigenvalues i : ℝ) : ℂ)) =
      (a : ℂ) • (1 : Matrix n n ℂ) +
        (q : ℂ) • Matrix.diagonal (fun i => (hS.eigenvalues i : ℂ)) := by
    ext i j
    by_cases hij : i = j
    · subst j
      simp [Matrix.smul_apply]
    · simp [Matrix.smul_apply, hij]
  rw [hdiag, map_add, map_smul, map_one, map_smul]
  have hspec : S = Unitary.conjStarAlgAut ℂ _ hS.eigenvectorUnitary
      (Matrix.diagonal (fun i => (hS.eigenvalues i : ℂ))) := by
    simpa only [Function.comp_def] using hS.spectral_theorem
  rw [← hspec]
  rfl

/-- Exact determinant product, without any positivity assumption on the scalars. -/
theorem affinePencil_det (S : Matrix n n ℂ) (hS : S.IsHermitian) (a q : ℝ) :
    (affinePencil S a q).det =
      ((∏ i, (a + q * hS.eigenvalues i) : ℝ) : ℂ) := by
  rw [affinePencil_spectral S hS, det_unitary_conjugate, Matrix.det_diagonal]
  simp only [Complex.ofReal_prod]

omit [Fintype n] in
/-- A positive identity term regularizes even a singular positive past. -/
theorem affinePencil_posDef (S : Matrix n n ℂ) (hS : S.PosSemidef)
    {a q : ℝ} (ha : 0 < a) (hq : 0 ≤ q) : (affinePencil S a q).PosDef := by
  have h := (Matrix.PosDef.one.smul ha).add_posSemidef (hS.smul hq)
  simpa only [affinePencil, Complex.real_smul] using h

/-- The real log determinant is the finite sum over the spectrum of `S`. -/
theorem affinePencil_logdet (S : Matrix n n ℂ) (hS : S.PosSemidef)
    {a q : ℝ} (ha : 0 < a) (hq : 0 ≤ q) :
    Real.log ((affinePencil S a q).det.re) =
      ∑ i, Real.log (a + q * hS.isHermitian.eigenvalues i) := by
  rw [affinePencil_det S hS.isHermitian, Complex.ofReal_re]
  exact Real.log_prod fun i _ => ne_of_gt
    (add_pos_of_pos_of_nonneg ha (mul_nonneg hq (hS.eigenvalues_nonneg i)))

private theorem one_le_det_one_add (D : Matrix n n ℂ) (hD : D.PosSemidef) :
    1 ≤ (1 + D).det := by
  have hdet := affinePencil_det D hD.isHermitian 1 1
  simp only [affinePencil, Complex.ofReal_one, one_smul, one_mul] at hdet
  rw [hdet]
  have hp : (1 : ℝ) ≤ ∏ i, (1 + hD.isHermitian.eigenvalues i) := by
    exact Finset.one_le_prod fun i _ => le_add_of_nonneg_right (hD.eigenvalues_nonneg i)
  exact_mod_cast hp

/-- Determinants increase in a positive-semidefinite direction from a positive
matrix. The proof factors the base; it never assumes determinant monotonicity. -/
theorem det_mono_of_posDef {A B : Matrix n n ℂ}
    (hA : A.PosDef) (hBA : (B - A).PosSemidef) : A.det ≤ B.det := by
  obtain ⟨R, hR⟩ := CStarAlgebra.nonneg_iff_eq_star_mul_self.mp hA.posSemidef.nonneg
  have hRdet : IsUnit R.det := by
    apply isUnit_iff_ne_zero.mpr
    intro hzero
    have hAdet : A.det ≠ 0 := ne_of_gt hA.det_pos
    apply hAdet
    rw [hR, Matrix.det_mul, hzero, mul_zero]
  have hRi : R⁻¹ * R = 1 := Matrix.nonsing_inv_mul R hRdet
  let D : Matrix n n ℂ := star R⁻¹ * (B - A) * R⁻¹
  have hD : D.PosSemidef := by
    simpa only [D, Matrix.star_eq_conjTranspose] using hBA.conjTranspose_mul_mul_same R⁻¹
  have hfac : B = star R * (1 + D) * R := by
    have hstar : star R * star R⁻¹ = 1 := by
      rw [← star_mul, hRi, star_one]
    calc
      B = A + (B - A) := by noncomm_ring
      _ = star R * R + (star R * star R⁻¹) * (B - A) * (R⁻¹ * R) := by
        rw [hR, hstar, hRi, one_mul, mul_one]
      _ = star R * (1 + D) * R := by dsimp [D]; noncomm_ring
  have hdet : B.det = A.det * (1 + D).det := by
    rw [hfac, hR]
    simp only [Matrix.det_mul]
    ring
  rw [hdet]
  simpa only [mul_one] using
    mul_le_mul_of_nonneg_left (one_le_det_one_add D hD) hA.det_pos.le

/-- Real log determinants increase in the Loewner order on positive matrices. -/
theorem logdet_mono_of_posDef {A B : Matrix n n ℂ}
    (hA : A.PosDef) (hBA : (B - A).PosSemidef) :
    Real.log A.det.re ≤ Real.log B.det.re := by
  exact Real.log_le_log (Complex.pos_iff.mp hA.det_pos).1
    (Complex.le_def.mp (det_mono_of_posDef hA hBA)).1

/-- The resolvent uses the same spectral basis; positivity is only required
for the regularized pencil, not for the past to be nonsingular. -/
theorem affinePencil_inv_spectral (S : Matrix n n ℂ) (hS : S.PosSemidef)
    {a q : ℝ} (ha : 0 < a) (hq : 0 ≤ q) :
    (affinePencil S a q)⁻¹ = Unitary.conjStarAlgAut ℂ _ hS.isHermitian.eigenvectorUnitary
      (Matrix.diagonal (fun i => (((a + q * hS.isHermitian.eigenvalues i)⁻¹ : ℝ) : ℂ))) := by
  apply Matrix.inv_eq_right_inv
  rw [affinePencil_spectral S hS.isHermitian, ← map_mul, Matrix.diagonal_mul_diagonal]
  have hdiag : Matrix.diagonal (fun i =>
      ((a + q * hS.isHermitian.eigenvalues i : ℝ) : ℂ) *
      (((a + q * hS.isHermitian.eigenvalues i)⁻¹ : ℝ) : ℂ)) =
      (1 : Matrix n n ℂ) := by
    have hpos i : 0 < a + q * hS.isHermitian.eigenvalues i :=
      add_pos_of_pos_of_nonneg ha (mul_nonneg hq (hS.eigenvalues_nonneg i))
    simp only [← Complex.ofReal_mul, mul_inv_cancel₀ (ne_of_gt (hpos _)), Complex.ofReal_one,
      Matrix.diagonal_one]
  rw [hdiag, map_one]

/-- The actual weighted resolvent trace is the finite scalar spectral gain. -/
theorem affinePencil_trace_resolvent (S : Matrix n n ℂ) (hS : S.PosSemidef)
    {a q : ℝ} (ha : 0 < a) (hq : 0 ≤ q) :
    (((q : ℂ) • S * (affinePencil S a q)⁻¹).trace).re =
      ∑ i, q * hS.isHermitian.eigenvalues i / (a + q * hS.isHermitian.eigenvalues i) := by
  rw [affinePencil_inv_spectral S hS ha hq]
  have hscaled : (q : ℂ) • S =
      Unitary.conjStarAlgAut ℂ _ hS.isHermitian.eigenvectorUnitary
        ((q : ℂ) • Matrix.diagonal (fun i => (hS.isHermitian.eigenvalues i : ℂ))) := by
    rw [map_smul]
    apply congrArg (fun M : Matrix n n ℂ => (q : ℂ) • M)
    simpa only [Function.comp_def] using hS.isHermitian.spectral_theorem
  rw [hscaled, ← map_mul, ← Matrix.diagonal_smul, Matrix.diagonal_mul_diagonal,
    trace_unitary_conjugate, Matrix.trace_diagonal]
  simp only [Pi.smul_apply, smul_eq_mul, Complex.re_sum, Complex.mul_re,
    Complex.ofReal_re, Complex.ofReal_im, mul_zero, sub_zero, div_eq_mul_inv]


/-- The unscaled regularized trace coefficient, including singular `S`. -/
theorem trace_regularized_resolvent (S : Matrix n n ℂ) (hS : S.PosSemidef)
    {a : ℝ} (ha : 0 < a) :
    ((S * ((a : ℂ) • 1 + S)⁻¹).trace).re =
      ∑ i, hS.isHermitian.eigenvalues i / (a + hS.isHermitian.eigenvalues i) := by
  simpa only [affinePencil, Complex.ofReal_one, one_smul, one_mul] using
    affinePencil_trace_resolvent S hS (q := 1) ha zero_le_one

end D0.Analysis.PositiveMatrixLogDet

end
