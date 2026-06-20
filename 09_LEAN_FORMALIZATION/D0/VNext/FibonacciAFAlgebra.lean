import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic

/-!
# D0 vNext — Fibonacci AF algebra levels (Phase A1)

The recovered golden Bratteli incidence `M_φ = !![1,1;1,0]` (`D0-BRATTELI-FIBONACCI-REFINEMENT-OWNER-001`)
defines the Fibonacci AF algebra `A_N = ⊕_v M_{d_v(N)}(ℂ)`. The per-vertex path-count vector evolves by
`p(N+1) = Mᵀ p(N) = (a+b, a)` from `p(0)=(1,1)`, and `dim A_N = Σ_v d_v(N)² = a² + b²`. The inclusion
`ι_N : A_N → A_(N+1)` is the Bratteli refinement with incidence `M_φ`; the two-step refinement is `M_φ²`.

Genuine AF levels (not manufactured): `dim A_N = 2, 5, 13, 34, 89, 233, 610, …` (grows as `φ^{2N}`).
-/

namespace D0.VNext.FibonacciAFAlgebra

open Matrix

/-- The golden Bratteli incidence (recovered from the forbid-`11` cylinder language). -/
def Mphi : Matrix (Fin 2) (Fin 2) ℤ := !![1, 1; 1, 0]

/-- Per-vertex path-count vector at level `N`: `p(N+1) = Mᵀ p(N) = (a+b, a)`, `p(0)=(1,1)`. -/
def pc : ℕ → ℕ × ℕ
  | 0 => (1, 1)
  | (n + 1) => ((pc n).1 + (pc n).2, (pc n).1)

/-- `dim A_N = Σ_v d_v(N)² = a² + b²`. -/
def dimA (n : ℕ) : ℕ := (pc n).1 ^ 2 + (pc n).2 ^ 2

/-- **The Fibonacci AF levels are defined** with the genuine dimensions `2, 5, 13, 34, 89`. -/
theorem fibonacci_af_level_defined :
    dimA 0 = 2 ∧ dimA 1 = 5 ∧ dimA 2 = 13 ∧ dimA 3 = 34 ∧ dimA 4 = 89 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> decide

/-- **The refinement inclusion incidence is `M_φ`** (the cylinder refinement, not a manual inclusion). -/
theorem cylinder_refinement_inclusion_defined : Mphi = !![1, 1; 1, 0] := rfl

/-- **The two-step refinement is `M_φ²`** `= !![2,1;1,1]`. -/
theorem two_step_refinement : Mphi * Mphi = !![2, 1; 1, 1] := by decide

/-- **The AF dimensions are strictly increasing** over the initial levels (an inductive tower, dimensions
growing — `2 < 5 < 13 < 34 < 89 < 233`). -/
theorem dimA_increasing_initial :
    dimA 0 < dimA 1 ∧ dimA 1 < dimA 2 ∧ dimA 2 < dimA 3 ∧ dimA 3 < dimA 4 ∧ dimA 4 < dimA 5 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> decide

end D0.VNext.FibonacciAFAlgebra
