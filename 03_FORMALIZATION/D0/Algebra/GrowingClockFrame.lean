import D0.Algebra.IsometricClockDeterminant
import Mathlib.Data.Fin.SuccPred

/-!
# Finite clock frames and the final leakage

A finite orthogonal family of equal-rank stage embeddings and an isometric
clock which advances every non-final frame force leakage to be supported at
its final frame. No desired leakage factorization is assumed. These are
algebraic hypotheses: the concrete GROWING stage spaces, closure, field
curves and physical admission remain to be constructed separately.
-/

noncomputable section
namespace D0.Algebra.GrowingClockFrame

open scoped BigOperators Matrix
open D0.Algebra.MovingProjectorTransport

variable {κ ι : Type*} [Fintype κ] [DecidableEq κ] [Fintype ι] [DecidableEq ι]

def frameProjector {n : ℕ} (J : Fin (n+1) → Matrix κ ι ℂ) : Matrix κ κ ℂ :=
  ∑ i, J i * (J i)ᴴ

variable {n : ℕ} (J : Fin (n+1) → Matrix κ ι ℂ)

theorem frame_projector_apply (hJ : ∀ i j, (J i)ᴴ * J j = if i = j then 1 else 0)
    (j : Fin (n+1)) : frameProjector J * J j = J j := by
  classical
  calc
    frameProjector J * J j = ∑ i, J i * ((J i)ᴴ * J j) := by
      simp [frameProjector, Matrix.sum_mul, Matrix.mul_assoc]
    _ = J j := by
      rw [Finset.sum_eq_single j]
      · simp [hJ]
      · intro i hi hne
        simp [hJ, hne]
      · intro h
        exact (h (Finset.mem_univ j)).elim

theorem frame_projector_selfAdjoint : (frameProjector J)ᴴ = frameProjector J := by
  classical
  simp [frameProjector, Matrix.conjTranspose_sum, Matrix.conjTranspose_mul]

theorem frame_projector_idempotent (hJ : ∀ i j, (J i)ᴴ * J j = if i = j then 1 else 0) :
    frameProjector J * frameProjector J = frameProjector J := by
  classical
  calc
    frameProjector J * frameProjector J = ∑ i, frameProjector J * (J i * (J i)ᴴ) := by
      simp [frameProjector, Matrix.mul_sum]
    _ = ∑ i, J i * (J i)ᴴ := by
      apply Finset.sum_congr rfl
      intro i hi
      rw [← Matrix.mul_assoc, frame_projector_apply J hJ]
    _ = frameProjector J := rfl


/-- The final return seen at the initial frame. -/
def frameReturn (T : Matrix κ κ ℂ) : Matrix ι ι ℂ :=
  (J 0)ᴴ * T * J (Fin.last n)

/-- The only returned component of the final frame is the initial frame. -/
theorem final_return_projection
    (hJ : ∀ i j, (J i)ᴴ * J j = if i = j then 1 else 0)
    (T : Matrix κ κ ℂ) (hT : Tᴴ * T = 1)
    (hstep : ∀ j : Fin n, T * J j.castSucc = J j.succ) :
    frameProjector J * T * J (Fin.last n) = J 0 * frameReturn J T := by
  classical
  have hcross (j : Fin n) : (J j.succ)ᴴ * T * J (Fin.last n) = 0 := by
    calc
      (J j.succ)ᴴ * T * J (Fin.last n) =
          (J j.castSucc)ᴴ * (Tᴴ * T) * J (Fin.last n) := by
        rw [← hstep j]
        simp [Matrix.conjTranspose_mul, Matrix.mul_assoc]
      _ = 0 := by
        rw [hT, Matrix.mul_one]
        simpa [Fin.castSucc_ne_last] using hJ j.castSucc (Fin.last n)
  calc
    frameProjector J * T * J (Fin.last n) =
        ∑ i, J i * ((J i)ᴴ * T * J (Fin.last n)) := by
      simp [frameProjector, Matrix.sum_mul, Matrix.mul_assoc]
    _ = J 0 * frameReturn J T := by
      rw [Finset.sum_eq_single 0]
      · rfl
      · intro i hi hne
        obtain ⟨j, rfl⟩ := Fin.exists_succ_eq_of_ne_zero hne
        rw [hcross j, Matrix.mul_zero]
      · intro h
        exact (h (Finset.mem_univ 0)).elim

/-- Internal stage transitions never leak outside the frame projector. -/
theorem internal_frame_no_leak
    (hJ : ∀ i j, (J i)ᴴ * J j = if i = j then 1 else 0)
    (T : Matrix κ κ ℂ)
    (hstep : ∀ j : Fin n, T * J j.castSucc = J j.succ)
    (j : Fin n) : cut (frameProjector J) T * J j.castSucc = 0 := by
  have hPJ := frame_projector_apply J hJ j.castSucc
  have hPnext := frame_projector_apply J hJ j.succ
  simp only [cut, Matrix.mul_assoc, hPJ, hstep, Matrix.sub_mul,
    Matrix.one_mul, hPnext, sub_self]

/-- The entire cut is supported on the final frame; no Gram factorization is assumed. -/
theorem cut_supported_on_final
    (hJ : ∀ i j, (J i)ᴴ * J j = if i = j then 1 else 0)
    (T : Matrix κ κ ℂ)
    (hstep : ∀ j : Fin n, T * J j.castSucc = J j.succ) :
    cut (frameProjector J) T =
      (cut (frameProjector J) T * J (Fin.last n)) * (J (Fin.last n))ᴴ := by
  classical
  have hP := frame_projector_idempotent J hJ
  have hLP : cut (frameProjector J) T * frameProjector J = cut (frameProjector J) T := by
    simp only [cut, Matrix.mul_assoc, hP]
  calc
    cut (frameProjector J) T = cut (frameProjector J) T * frameProjector J := hLP.symm
    _ = ∑ i, (cut (frameProjector J) T * J i) * (J i)ᴴ := by
      simp [frameProjector, Matrix.mul_sum, Matrix.mul_assoc]
    _ = (cut (frameProjector J) T * J (Fin.last n)) * (J (Fin.last n))ᴴ := by
      rw [Finset.sum_eq_single (Fin.last n)]
      · intro i hi hne
        obtain ⟨j, rfl⟩ := Fin.eq_castSucc_of_ne_last hne
        rw [internal_frame_no_leak J hJ T hstep j, Matrix.zero_mul]
      · intro h
        exact (h (Finset.mem_univ _)).elim


/-- GROWING's final leakage factorization follows from orthogonal frames,
isometry and internal stage advances, without assuming the factorization. -/
theorem clock_cut_gram_factorization
    (hJ : ∀ i j, (J i)ᴴ * J j = if i = j then 1 else 0)
    (T : Matrix κ κ ℂ) (hT : Tᴴ * T = 1)
    (hstep : ∀ j : Fin n, T * J j.castSucc = J j.succ) :
    let P := frameProjector J
    let C := frameReturn J T
    let Jf := J (Fin.last n)
    (cut P T)ᴴ * cut P T = Jf * (1 - Cᴴ * C) * Jfᴴ := by
  let P := frameProjector J
  let Jf := J (Fin.last n)
  let C := frameReturn J T
  let L := cut P T
  let X := T * Jf
  have hP : P * P = P := frame_projector_idempotent J hJ
  have hPH : Pᴴ = P := frame_projector_selfAdjoint J
  have hPJ : P * Jf = Jf := frame_projector_apply J hJ (Fin.last n)
  have hJf : Jfᴴ * Jf = 1 := by simpa [Jf] using hJ (Fin.last n) (Fin.last n)
  have hJ0 : (J 0)ᴴ * J 0 = 1 := by simpa using hJ 0 0
  have hprojection : P * X = J 0 * C := by
    simpa [P, X, Jf, C, Matrix.mul_assoc] using final_return_projection J hJ T hT hstep
  have hX : Xᴴ * X = 1 := by
    calc
      Xᴴ * X = Jfᴴ * (Tᴴ * T) * Jf := by simp [X, Matrix.conjTranspose_mul, Matrix.mul_assoc]
      _ = 1 := by rw [hT]; simpa using hJf
  have hcomp : (1 - P)ᴴ * (1 - P) = 1 - P := by
    rw [Matrix.conjTranspose_sub, Matrix.conjTranspose_one, hPH]
    calc
      (1 - P) * (1 - P) = 1 - P - P + P * P := by noncomm_ring
      _ = 1 - P := by rw [hP]; noncomm_ring
  have hLX : L * Jf = (1 - P) * X := by
    simp [L, cut, X, Matrix.mul_assoc, hPJ]
  have hPX : Xᴴ * P * X = Cᴴ * C := by
    calc
      Xᴴ * P * X = (P * X)ᴴ * (P * X) := by
        simp only [Matrix.conjTranspose_mul, hPH, Matrix.mul_assoc]
        rw [← Matrix.mul_assoc P P X, hP]
      _ = Cᴴ * C := by
        rw [hprojection]
        simp only [Matrix.conjTranspose_mul, Matrix.mul_assoc]
        rw [← Matrix.mul_assoc ((J 0)ᴴ) (J 0) C, hJ0, Matrix.one_mul]
  have hgram : (L * Jf)ᴴ * (L * Jf) = 1 - Cᴴ * C := by
    calc
      (L * Jf)ᴴ * (L * Jf) = Xᴴ * ((1 - P)ᴴ * (1 - P)) * X := by
        rw [hLX]
        simp [Matrix.conjTranspose_mul, Matrix.mul_assoc]
      _ = Xᴴ * X - Xᴴ * P * X := by
        rw [hcomp]
        simp [Matrix.mul_sub, Matrix.sub_mul, Matrix.mul_assoc]
      _ = 1 - Cᴴ * C := by rw [hX, hPX]
  have hsupport : L = (L * Jf) * Jfᴴ := by
    simpa [L, P, Jf] using cut_supported_on_final J hJ T hstep
  calc
    Lᴴ * L = ((L * Jf) * Jfᴴ)ᴴ * ((L * Jf) * Jfᴴ) := by rw [← hsupport]
    _ = Jf * ((L * Jf)ᴴ * (L * Jf)) * Jfᴴ := by
      simp [Matrix.conjTranspose_mul, Matrix.mul_assoc]
    _ = Jf * (1 - Cᴴ * C) * Jfᴴ := by rw [hgram]

/-- The derived clock defect consumes the existing rectangular determinant theorem. -/
theorem clock_cut_determinant
    (hJ : ∀ i j, (J i)ᴴ * J j = if i = j then 1 else 0)
    (T : Matrix κ κ ℂ) (hT : Tᴴ * T = 1)
    (hstep : ∀ j : Fin n, T * J j.castSucc = J j.succ) (z : ℂ) :
    let P := frameProjector J
    let C := frameReturn J T
    (1 - z • ((cut P T)ᴴ * cut P T)).det =
      ((1 - z) • (1 : Matrix ι ι ℂ) + z • (Cᴴ * C)).det := by
  dsimp only
  rw [clock_cut_gram_factorization J hJ T hT hstep]
  apply D0.Algebra.IsometricClockDeterminant.det_clock_defect
  simpa using hJ (Fin.last n) (Fin.last n)

end D0.Algebra.GrowingClockFrame
end
