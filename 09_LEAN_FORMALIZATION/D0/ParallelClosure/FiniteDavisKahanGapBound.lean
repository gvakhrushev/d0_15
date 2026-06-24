import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic

/-!
# D0-CKM-DAVIS-KAHAN-GAP-BOUND-001 — finite gap-vs-mismatch bound (Track B, B4)

The honest content of "small mixing ⟸ small source-native mismatch relative to an isolated gap" is the
**finite Davis–Kahan sin-Θ bound**: for finite Hermitian `H_u`, `H_d = H_u + V`, with orthogonal spectral
projectors `P_u, P_d` onto a cluster isolated by gap `γ`,
`‖(I − P_d)·P_u‖ ≤ ‖V‖ / γ`  (constant `C = 1`). This is NOT "rank 3 ⇒ small CKM" — small mixing requires a
genuinely small mismatch `‖V‖` relative to an isolated gap `γ`.

The general theorem is the standard **Davis–Kahan (1970)** result (external math owner `ASSUMP-DAVIS-KAHAN`);
here we machine-check a fully-rational instance over `ℚ` (all projectors rational), and the full finite bound is
verified across random Hermitian samples in `05_CERTS/d0_ckm_mismatch_bound_verify.py` (worst-case ratio
`< 1`, with a no-gap negative control). FIREWALL: no PDG masses, no fitted CKM, no string moduli; `‖V‖` and `γ`
are abstract operator quantities, not D0 numbers.
-/

namespace D0.ParallelClosure.FiniteDavisKahanGapBound

open Matrix

/-- `H_u = diag(4,1)` (gap 3, eigenvectors `e₁,e₂`). -/
def Hu : Matrix (Fin 2) (Fin 2) ℚ := !![4, 0; 0, 1]
/-- `H_d = !![4,2; 2,1]` — eigenvalues `5, 0` with rational eigenvectors `(2,1), (1,−2)`. -/
def Hd : Matrix (Fin 2) (Fin 2) ℚ := !![4, 2; 2, 1]
/-- Mismatch `V = H_d − H_u`. -/
def V : Matrix (Fin 2) (Fin 2) ℚ := Hd - Hu
/-- `P_u` onto the `H_u`-eigenvalue `4` cluster (`e₁`). -/
def Pu : Matrix (Fin 2) (Fin 2) ℚ := !![1, 0; 0, 0]
/-- `P_d` onto the `H_d`-eigenvalue `5` cluster: `(1/5)·!![4,2;2,1]`. -/
def Pd : Matrix (Fin 2) (Fin 2) ℚ := !![4/5, 2/5; 2/5, 1/5]

/-- Squared Hilbert–Schmidt norm of a `2×2` rational matrix. -/
def hs2 (M : Matrix (Fin 2) (Fin 2) ℚ) : ℚ :=
  (M 0 0)^2 + (M 0 1)^2 + (M 1 0)^2 + (M 1 1)^2

/-- `P_u` and `P_d` are genuine (idempotent) orthogonal projectors. -/
theorem projectors : Pu * Pu = Pu ∧ Pd * Pd = Pd := by
  refine ⟨?_, ?_⟩ <;> native_decide

/-- `V = H_d − H_u = !![0,2; 2,0]`, with `‖V‖²_HS = 8`. -/
theorem mismatch_value : V = !![0, 2; 2, 0] ∧ hs2 V = 8 := by
  refine ⟨?_, ?_⟩ <;> native_decide

/-- The misalignment `X = (I − P_d)·P_u` has `‖X‖²_HS = 1/5`. -/
theorem misalignment_value : hs2 ((1 - Pd) * Pu) = 1/5 := by native_decide

/-- **D0-CKM-DAVIS-KAHAN-GAP-BOUND-001 (finite instance).** With gap `γ = 4` (`= dist(H_u`-cluster `{4}`,
`H_d`-complement `{0}`)), the Davis–Kahan bound `‖(I−P_d)P_u‖²·γ² ≤ ‖V‖²_HS` holds: `16/5 ≤ 8`. The general
`C = 1` bound is external Davis–Kahan (cert across random Hermitian samples). Small mixing ⟸ small `‖V‖/γ`. -/
theorem finite_davis_kahan_instance :
    Pd * Pd = Pd ∧ hs2 ((1 - Pd) * Pu) = 1/5 ∧ hs2 V = 8 ∧
    hs2 ((1 - Pd) * Pu) * (4:ℚ)^2 ≤ hs2 V := by
  refine ⟨projectors.2, misalignment_value, mismatch_value.2, ?_⟩
  native_decide

end D0.ParallelClosure.FiniteDavisKahanGapBound
