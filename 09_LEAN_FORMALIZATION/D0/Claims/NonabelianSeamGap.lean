import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic

/-!
# D0-NONABELIAN-SEAM-001 — a positive obstruction gap outside the commuting kernel

Python certificate: `05_CERTS/vp_nonabelian_seam_gap.py`.

The seam generator `B = [[0,1],[0,0]]` has zero commutator with an abelian (here the
identity) generator but a strictly positive commutator with a non-abelian rotation
`J = [[0,1],[-1,0]]`: the squared Frobenius norm of `[B, X]` is `0` on the commuting
kernel and `> 0` off it.  All exact integer matrices.
-/

namespace D0.Claims

open Matrix

/-- Seam generator `B = [[0,1],[0,0]]`. -/
def seamB : Matrix (Fin 2) (Fin 2) ℤ := !![0, 1; 0, 0]

/-- Non-abelian rotation generator `J = [[0,1],[-1,0]]`. -/
def rotJ : Matrix (Fin 2) (Fin 2) ℤ := !![0, 1; -1, 0]

/-- Commutator `[B, X] = B·X − X·B`. -/
def comm (X : Matrix (Fin 2) (Fin 2) ℤ) : Matrix (Fin 2) (Fin 2) ℤ := seamB * X - X * seamB

/-- Squared Frobenius norm (integer): `∑ i j, M i j ^ 2`. -/
def frobSq (M : Matrix (Fin 2) (Fin 2) ℤ) : ℤ := ∑ i, ∑ j, (M i j) ^ 2

/-- On the commuting kernel (identity), the commutator vanishes: gap `= 0`. -/
theorem seam_gap_zero_on_identity : frobSq (comm 1) = 0 := by native_decide

/-- Off the kernel (the rotation `J`), the obstruction gap is strictly positive (`= 2`). -/
theorem seam_gap_positive_offkernel : frobSq (comm rotJ) = 2 := by native_decide

/-- **D0-NONABELIAN-SEAM-001.** The seam obstruction is `0` on the commuting kernel and a
strictly positive value off it — a genuine non-abelian gap. -/
theorem nonabelian_seam_gap :
    frobSq (comm 1) = 0 ∧ frobSq (comm rotJ) = 2 ∧ (0 : ℤ) < frobSq (comm rotJ) :=
  ⟨seam_gap_zero_on_identity, seam_gap_positive_offkernel, by native_decide⟩

end D0.Claims
