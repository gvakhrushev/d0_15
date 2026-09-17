import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic

/-! Every real orthogonal rank-one projector on a two-plane has the form
[[r,s],[s,1-r]], with r^2+s^2=r. Its reflection reverses the plane quarter-turn.
This removes frame dependence by an identity over all such projectors, not by
enumerating the three source spectral choices. It does not assert a physical
implementation of every projector. -/

namespace D0.Representation.PortFrameCovariance

abbrev M2 := Matrix (Fin 2) (Fin 2) ℝ
def J : M2 := !![0,-1;1,0]
def reflection (r s : ℝ) : M2 := !![1-2*r,-2*s;-2*s,2*r-1]

theorem reflection_anticommutes (r s : ℝ) :
    reflection r s * J = -(J * reflection r s) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [reflection, J, Matrix.mul_apply, Fin.sum_univ_two] <;> ring

theorem reflection_involution (r s : ℝ) (h : r^2+s^2=r) :
    reflection r s * reflection r s = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [reflection, Matrix.mul_apply, Fin.sum_univ_two] <;> nlinarith

theorem every_port_reverses_flow (r s : ℝ) (h : r^2+s^2=r) (a b : ℝ) :
    reflection r s * (a • (1 : M2) + b • J) * reflection r s =
      a • (1 : M2) - b • J := by
  have hs := reflection_involution r s h
  have hj := reflection_anticommutes r s
  calc
    _ = a • (reflection r s * reflection r s) +
        b • (reflection r s * J * reflection r s) := by
      simp [mul_add, add_mul, Matrix.mul_smul, Matrix.smul_mul, mul_assoc]
    _ = a • (1 : M2) + b • (-J) := by
      rw [hs, hj]
      simp [mul_assoc, hs]
    _ = _ := by simp [sub_eq_add_neg]

end D0.Representation.PortFrameCovariance
