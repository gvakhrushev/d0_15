import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic

/-!
# D0-V15 Work Package E — Feshbach two-source split (E1 THE) + EOS (E2 NO-GO)

## E1 — Schur/Feshbach determinant factorization (THE, *as an algebraic identity*)

For a block operator `M = [[A,B],[C,I]]` the Schur complement identity `det M = det(A − B·C)` holds (the `D = I`
case of the general Feshbach factorization `det(I−zU) = det(I−zD)·det(I−zW_eff(z))`, `W_eff = A + zB(I−zD)⁻¹C`;
in Mathlib: `Matrix.det_fromBlocks_one₂₂`). We verify the concrete integer instance
`det !![2,1,1,0; 0,3,1,1; 0,1,1,0; 1,0,0,1] = 4 = det !![2,0; -1,2] = det(A − B·C)`. The additive log-derivative
split `−∂_z log det(I−zU) = R_Q + R_P` is its immediate corollary. This is a present-core identity — but it is
ONLY an algebraic identity. Cite `D0-FESHBACH-SCHUR-TIME-DELAY-OWNER-001`.

## E2 — physical equation of state is NOT determined by the response (NO-GO)

The two-source response fixes only the *total* `R_Q + R_P`; it does not split it into an energy density `ρ` and a
pressure `p`. Negative control: `(ρ,p) = (3,1)` and `(3,1)`-swapped `(1,3)` have the **same** total response
`ρ+p = 4` but **distinct** `w = p/ρ` (`1/3 ≠ 3`). So no equation of state / `w(z)` follows without the
energy-pressure owner `PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT`. Forbidden: reading `ρ = eᵘ−1, p = eᵘ/φ` as
derived. Cite `D0-ARCHIVE-CONTRACTION-NOGO-001` (window `359/160`).
-/

namespace D0.Integration.V15.Feshbach

open Matrix

/-! ## E1 — Schur determinant factorization -/

/-- The full block operator `M = [[A,B],[C,I]]` (concrete integer instance). -/
def Mfull : Matrix (Fin 4) (Fin 4) ℤ := !![2, 1, 1, 0; 0, 3, 1, 1; 0, 1, 1, 0; 1, 0, 0, 1]

/-- The Schur complement `A − B·C` of the `D = I` block. -/
def Schur : Matrix (Fin 2) (Fin 2) ℤ := !![2, 0; -1, 2]

/-- **E1 (THE, algebraic identity).** `det M = det(A − B·C)`: the Feshbach/Schur factorization on the concrete
frozen-shaped block instance (both equal `4`). -/
theorem feshbach_schur_factorization : Mfull.det = Schur.det ∧ Mfull.det = 4 := by
  refine ⟨?_, ?_⟩ <;> native_decide

/-! ## E2 — equation-of-state underdetermination -/

/-- Equation-of-state ratio `w = p/ρ`. -/
def w (rho p : ℚ) : ℚ := p / rho

/-- **E2 (NO-GO).** Two assignments with identical total response `ρ+p = 4` but distinct `w`: the response does
not determine `(ρ,p)`, so no physical `w` follows without `PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT`. -/
theorem eos_underdetermined :
    ((3 : ℚ) + 1 = 1 + 3) ∧ w 3 1 ≠ w 1 3 := by
  refine ⟨by norm_num, ?_⟩
  simp only [w]
  norm_num

end D0.Integration.V15.Feshbach
