import D0.Core.Phi
import Mathlib.Tactic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.Charpoly.Coeff

/-!
# D0-FIBONACCI-FUSION-RING-001 — the Fibonacci fusion rule as an integer matrix-ring identity

Sharpens D0-FIBONACCI-IF-FORCING-001's scalar dimension identity `φ² = φ + 1` to a genuine
integer-ring witness of the Fibonacci fusion rule `τ ⊗ τ = 1 ⊕ τ`: the fusion matrix
`N_τ = [[0,1],[1,1]]` over ℤ satisfies `N_τ · N_τ = N_τ + 1`, with `trace = 1`, `det = −1`, and
characteristic polynomial exactly `X² − X − 1` (the golden quadratic, whose real root is `φ`).
Reuses the pinned Mathlib `Matrix` Fin-2 / trace / det / charpoly API and `D0.Core.Phi.phi_sq`.

Honest scope: this is the RING-level fusion fact (LEM-status algebraic core). The genuine fusion
CATEGORY (object isomorphism `τ ⊗ τ ≅ 𝟙 ⊕ τ` + Ostrik uniqueness) needs a `FusionCategory` /
Grothendieck-ring structure that is ABSENT from the pin — that stays the open categorical↔toral
named gap (the Adler–Weiss owner-edge), not over-claimed here.
-/

namespace D0.Claims

open D0 Matrix Polynomial

/-- The integer Fibonacci fusion matrix `N_τ = [[0,1],[1,1]]` (the fusion rule of the τ object). -/
def fibFusionMatrix : Matrix (Fin 2) (Fin 2) ℤ := !![0, 1; 1, 1]

/-- **Ring-level Fibonacci fusion rule** `τ ⊗ τ = 1 ⊕ τ`, as `N_τ · N_τ = N_τ + 1` over ℤ. -/
theorem fibFusion_rule : fibFusionMatrix * fibFusionMatrix = fibFusionMatrix + 1 := by
  unfold fibFusionMatrix
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_succ, Matrix.add_apply]

/-- `N_τ` has trace `1`. -/
theorem fibFusion_trace : fibFusionMatrix.trace = 1 := by
  rw [fibFusionMatrix, trace_fin_two_of]; ring

/-- `N_τ` has determinant `−1`. -/
theorem fibFusion_det : fibFusionMatrix.det = -1 := by
  rw [fibFusionMatrix, det_fin_two_of]; ring

/-- The characteristic polynomial of `N_τ` is `X² − X − 1` (the golden quadratic). -/
theorem fibFusion_charpoly : fibFusionMatrix.charpoly = X ^ 2 - C 1 * X + C (-1) := by
  rw [charpoly_fin_two, fibFusion_trace, fibFusion_det]

/-- `φ` is a root of `N_τ`'s characteristic polynomial (reusing `D0.Core.Phi.phi_sq`). -/
theorem fibFusion_phi_root : phi ^ 2 - 1 * phi + (-1) = 0 := by
  have := phi_sq; linarith

end D0.Claims
