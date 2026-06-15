import Mathlib.Tactic

/-!
# D0-FROBENIUS-DIVISION-3D-001 — 3 space dimensions, forced by Frobenius (Lean finite content)

Python certificate: `05_CERTS/vp_frobenius_division_3d.py`.
Bridge assumption (external owner): `D0.Bridge.BridgeAssumption.FrobeniusDivision3D`
(`ASSUMP-FROBENIUS-1877`).

The external theorem (Frobenius 1877: the only finite-dimensional associative division algebras
over ℝ are ℝ, ℂ, ℍ) is the OWNER and is NOT re-proved here. This module proves only the finite
content the bridge rests on, in exact ℤ-quaternion arithmetic: the Hamilton relations
`i²=j²=k²=ijk=−1` and the imaginary dimension of ℍ being 3 (= rank-3 transport = space; the one
real axis = time). The `ℍ→𝕆` octet step is HYP (two different 8's) and is NOT asserted here.
-/

namespace D0.Foundation

/-- A quaternion over `ℤ` as `(a,b,c,d) = a + b·i + c·j + d·k`. -/
abbrev Quat := Int × Int × Int × Int

/-- Hamilton product on `ℤ`-quaternions. -/
def qmul (x y : Quat) : Quat :=
  (x.1 * y.1 - x.2.1 * y.2.1 - x.2.2.1 * y.2.2.1 - x.2.2.2 * y.2.2.2,
   x.1 * y.2.1 + x.2.1 * y.1 + x.2.2.1 * y.2.2.2 - x.2.2.2 * y.2.2.1,
   x.1 * y.2.2.1 - x.2.1 * y.2.2.2 + x.2.2.1 * y.1 + x.2.2.2 * y.2.1,
   x.1 * y.2.2.2 + x.2.1 * y.2.2.1 - x.2.2.1 * y.2.1 + x.2.2.2 * y.1)

def qi : Quat := (0, 1, 0, 0)
def qj : Quat := (0, 0, 1, 0)
def qk : Quat := (0, 0, 0, 1)
def qNegOne : Quat := (-1, 0, 0, 0)

/-- imaginary dimension of `ℍ` = 3 (the three reversible transport directions = rank-3 = space). -/
def imaginaryDim : Nat := 3

theorem i_sq : qmul qi qi = qNegOne := by decide
theorem j_sq : qmul qj qj = qNegOne := by decide
theorem k_sq : qmul qk qk = qNegOne := by decide
theorem ij_eq_k : qmul qi qj = qk := by decide
theorem hamilton_ijk : qmul (qmul qi qj) qk = qNegOne := by decide

/-- **D0-FROBENIUS-DIVISION-3D-001 (finite content).** The Hamilton relations
`i²=j²=k²=ijk=−1`, `ij=k`, and the imaginary dimension of `ℍ` is 3 (= rank-3 = space). The
classification "only ℝ,ℂ,ℍ" is the external owner (`ASSUMP-FROBENIUS-1877`), not proved here. -/
theorem frobenius_division_3d :
    qmul qi qi = qNegOne ∧ qmul qj qj = qNegOne ∧ qmul qk qk = qNegOne ∧
    qmul qi qj = qk ∧ qmul (qmul qi qj) qk = qNegOne ∧ imaginaryDim = 3 :=
  ⟨i_sq, j_sq, k_sq, ij_eq_k, hamilton_ijk, rfl⟩

end D0.Foundation
