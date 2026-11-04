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

end D0.Algebra.GrowingClockFrame
end
