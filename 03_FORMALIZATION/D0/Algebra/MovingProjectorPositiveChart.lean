import D0.Algebra.MovingProjectorCalculus
import Mathlib.Analysis.Matrix.PosDef

/-!
# Positive feedback chart for an orthogonal moving cut

For the finite fixed-Gram carrier in the moving-cut source, an orthogonal
projector and an isometric evolution make the feedback determinant strictly
positive whenever `0 ≤ z < 1`. This supplies the analytic chart of the
existing same-curve feedback derivative. It does not select an admitted
physical variation, a thermal source, or a complete price.
-/

namespace D0.Algebra.MovingProjectorTransport

open Filter
open scoped Topology ComplexOrder Matrix.Norms.Frobenius

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- The complement of the cut return is a sum of two actual Gram matrices. -/
theorem cut_return_complement_eq_gram_sum
    (P U : Matrix ι ι ℂ)
    (hP : P * P = P) (hSelfAdjoint : star P = P)
    (hU : star U * U = 1) :
    1 - star (cut P U) * cut P U =
      star (1 - P) * (1 - P) + star (P * U * P) * (P * U * P) := by
  let Q : Matrix ι ι ℂ := 1 - P
  let X : Matrix ι ι ℂ := P * U * P
  let C : Matrix ι ι ℂ := cut P U
  have hQ : star Q * Q = Q := by
    dsimp [Q]
    simp only [star_sub, star_one, hSelfAdjoint]
    calc
      (1 - P) * (1 - P) = 1 - P - P + P * P := by noncomm_ring
      _ = 1 - P := by rw [hP]; noncomm_ring
  have hQsq : Q * Q = Q := by
    simpa only [Q, star_sub, star_one, hSelfAdjoint] using hQ
  have hC : star C * C = P * star U * Q * U * P := by
    dsimp [C, cut]
    simp only [star_mul, star_sub, star_one, hSelfAdjoint]
    calc
      P * (star U * (1 - P)) * ((1 - P) * U * P) =
          P * star U * ((1 - P) * (1 - P)) * U * P := by noncomm_ring
      _ = P * star U * (1 - P) * U * P := by
        change P * star U * (Q * Q) * U * P = P * star U * Q * U * P
        rw [hQsq]
  have hX : star X * X = P * star U * P * U * P := by
    dsimp [X]
    simp only [star_mul, hSelfAdjoint]
    calc
      P * (star U * P) * (P * U * P) = P * star U * (P * P) * U * P := by
        noncomm_ring
      _ = P * star U * P * U * P := by rw [hP]
  have hsum : star C * C + star X * X = P := by
    rw [hC, hX]
    calc
      P * star U * Q * U * P + P * star U * P * U * P =
          P * star U * (Q + P) * U * P := by noncomm_ring
      _ = P * (star U * U) * P := by simp [Q, mul_assoc]
      _ = P := by rw [hU]; simpa using hP
  have hrem : P - star C * C = star X * X := by
    rw [← hsum]
    abel
  change 1 - star C * C = star Q * Q + star X * X
  rw [hQ, ← hrem]
  dsimp [Q]
  abel

/-- An orthogonal cut of an isometry has a strictly positive feedback matrix. -/
theorem cut_feedback_posDef
    (P U : Matrix ι ι ℂ) (z : ℝ)
    (hP : P * P = P) (hSelfAdjoint : star P = P)
    (hU : star U * U = 1) (hz0 : 0 ≤ z) (hz1 : z < 1) :
    (1 - (z : ℂ) • (star (cut P U) * cut P U)).PosDef := by
  let Q : Matrix ι ι ℂ := 1 - P
  let X : Matrix ι ι ℂ := P * U * P
  let F : Matrix ι ι ℂ := star (cut P U) * cut P U
  have hgap : 1 - F = star Q * Q + star X * X :=
    cut_return_complement_eq_gram_sum P U hP hSelfAdjoint hU
  have hgram : (star Q * Q + star X * X).PosSemidef := by
    have hQ : (star Q * Q).PosSemidef := by
      simpa only [Matrix.star_eq_conjTranspose] using
        Matrix.posSemidef_conjTranspose_mul_self Q
    have hX : (star X * X).PosSemidef := by
      simpa only [Matrix.star_eq_conjTranspose] using
        Matrix.posSemidef_conjTranspose_mul_self X
    exact hQ.add hX
  have hstrict : ((1 - z) • (1 : Matrix ι ι ℂ)).PosDef :=
    Matrix.PosDef.one.smul (sub_pos.mpr hz1)
  have hweighted : (z • (star Q * Q + star X * X)).PosSemidef :=
    hgram.smul hz0
  have hdecomp :
      1 - (z : ℂ) • F = (1 - z) • (1 : Matrix ι ι ℂ) +
        z • (star Q * Q + star X * X) := by
    rw [← hgap]
    ext i j
    simp only [Matrix.sub_apply, Matrix.add_apply, Matrix.smul_apply,
      sub_smul, one_smul, smul_sub, Complex.real_smul, smul_eq_mul]
    abel
  rw [hdecomp]
  exact hstrict.add_posSemidef hweighted

/-- The actual feedback determinant lies on the positive real slit-plane chart. -/
theorem cut_feedback_det_mem_slitPlane
    (P U : Matrix ι ι ℂ) (z : ℝ)
    (hP : P * P = P) (hSelfAdjoint : star P = P)
    (hU : star U * U = 1) (hz0 : 0 ≤ z) (hz1 : z < 1) :
    (1 - (z : ℂ) • (star (cut P U) * cut P U)).det ∈ Complex.slitPlane := by
  have hdet := (cut_feedback_posDef P U z hP hSelfAdjoint hU hz0 hz1).det_pos
  exact Complex.mem_slitPlane_iff.mpr (Or.inl (Complex.pos_iff.mp hdet).1)

/--
The existing same-curve feedback derivative follows directly from the original
projector and unitary-carrier assumptions, without assuming the log chart.
-/
theorem complex_matrix_feedback_real_logdet_of_isometric_cut_hasDerivAt
    {P U : ℝ → Matrix ι ι ℂ} {dP dU : Matrix ι ι ℂ} {t : ℝ} (z : ℝ)
    (hP : HasDerivAt P dP t) (hU : HasDerivAt U dU t)
    (hIdem : ∀ᶠ s in 𝓝 t, P s * P s = P s)
    (hSelfAdjoint : ∀ᶠ s in 𝓝 t, star (P s) = P s)
    (hIsometry : star (U t) * U t = 1) (hz0 : 0 ≤ z) (hz1 : z < 1) :
    let C := cut (P t) (U t)
    let R := (1 - (z : ℂ) • (star C * C))⁻¹
    let V := (1 - P t) * (dU - comm (generator (P t) dP) (U t)) * P t
    HasDerivAt
      (fun s => -Real.log ((1 - (z : ℂ) •
        (star (cut (P s) (U s)) * cut (P s) (U s))).det.re))
      (z * (2 * (Matrix.trace (R * star C * V)).re)) t := by
  apply complex_matrix_feedback_real_logdet_of_slit_hasDerivAt z hP hU hIdem hSelfAdjoint
  exact cut_feedback_det_mem_slitPlane (P t) (U t) z hIdem.self_of_nhds
    hSelfAdjoint.self_of_nhds hIsometry hz0 hz1

end D0.Algebra.MovingProjectorTransport
