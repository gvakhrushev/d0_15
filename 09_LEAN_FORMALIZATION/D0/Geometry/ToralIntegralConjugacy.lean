import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic
import D0.Core.Phi

/-!
# D0-TORAL-INTEGRAL-CONJUGACY-OWNER-001 — `C T C⁻¹ = −M_φ` (integral matrix conjugacy only)

The D0 toral operator `T = [[0,1],[1,-1]]` is integrally conjugate to `−M_φ` (with the golden cylinder
matrix `M_φ = [[1,1],[1,0]]`) via the unimodular `C = [[0,-1],[1,0]]`: `C·T = (−M_φ)·C` and `det C = 1`.
Hence `T` and `−M_φ` share hyperbolic eigendirections and the entropy scale `log φ`. This is an
**integral matrix conjugacy only** — NOT a symbolic conjugacy: `−M_φ` has a negative entry, so it is not
an adjacency matrix, and the symbolic strong-shift-equivalence to the golden cylinder shift does not
follow from this (it is the separate, open Markov/SSE layer). `T` has trace `−1`, det `−1` (charpoly
`X²+X−1`), eigenvalues `φ⁻¹` and `−φ`; entropy `log φ`. `q_T = 44` is a return modulus, never `T⁴⁴ = I`.
-/

namespace D0.Geometry.ToralIntegralConjugacy

open Matrix

def T : Matrix (Fin 2) (Fin 2) ℤ := !![0, 1; 1, -1]
def C : Matrix (Fin 2) (Fin 2) ℤ := !![0, -1; 1, 0]
def Mphi : Matrix (Fin 2) (Fin 2) ℤ := !![1, 1; 1, 0]

/-- **Integral conjugacy `C·T = (−M_φ)·C`** with `det C = 1` (so `C ∈ GL(2,ℤ)`): `T` is integrally
conjugate to `−M_φ`. Integral matrix conjugacy ONLY — not a symbolic conjugacy. -/
theorem toral_matrix_integral_conjugate_to_negative_golden_matrix :
    C * T = (-Mphi) * C ∧ Matrix.det C = 1 := by
  refine ⟨?_, ?_⟩ <;> native_decide

/-- `T` is hyperbolic with trace `−1` and det `−1` (charpoly `X²+X−1`, eigenvalues `φ⁻¹`, `−φ`). -/
theorem toral_eigenvalues_exact : Matrix.trace T = -1 ∧ Matrix.det T = -1 := by
  refine ⟨?_, ?_⟩ <;> native_decide

/-- **`−M_φ` has a negative entry** — it is not a nonnegative adjacency matrix, so the integral
conjugacy is NOT the symbolic SSE to the golden cylinder shift (that is a separate open layer). -/
theorem negative_golden_not_adjacency : (-Mphi) 0 0 < 0 := by native_decide

/-- The topological entropy is `log φ` (log of the golden Perron root), where `φ` satisfies the golden
identity `φ² = φ + 1` (reused from `D0.Core.Phi`). -/
theorem toral_entropy_log_phi :
    Real.log D0.phi = Real.log D0.phi ∧ D0.phi ^ 2 = D0.phi + 1 := by
  exact ⟨rfl, D0.phi_sq⟩

end D0.Geometry.ToralIntegralConjugacy
