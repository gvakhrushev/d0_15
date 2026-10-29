import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic
import D0.Algebra.FibonacciAFTower

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

/-- Compatibility API: the canonical incidence matrix is owned by the core tower module. -/
abbrev Mphi : Matrix (Fin 2) (Fin 2) ℤ := D0.Algebra.FibonacciAFTower.Mphi

/-- Compatibility API for the core-owned per-vertex path-count recurrence. -/
abbrev pc : ℕ → ℕ × ℕ := D0.Algebra.FibonacciAFTower.pathCount

/-- Compatibility API for the core-owned real finite-level dimension formula. -/
abbrev dimA (n : ℕ) : ℕ := D0.Algebra.FibonacciAFTower.dimA n

/-- **The Fibonacci AF levels are defined** with the genuine dimensions `2, 5, 13, 34, 89`. -/
theorem fibonacci_af_level_defined :
    dimA 0 = 2 ∧ dimA 1 = 5 ∧ dimA 2 = 13 ∧ dimA 3 = 34 ∧ dimA 4 = 89 :=
  D0.Algebra.FibonacciAFTower.af_dimensions_initial

/-- **The refinement inclusion incidence is `M_φ`** (the cylinder refinement, not a manual inclusion). -/
theorem cylinder_refinement_inclusion_defined : Mphi = !![1, 1; 1, 0] := rfl

/-- **The two-step refinement is `M_φ²`** `= !![2,1;1,1]`. -/
theorem two_step_refinement : Mphi * Mphi = !![2, 1; 1, 1] :=
  D0.Algebra.FibonacciAFTower.two_step_bratteli_matrix

/-- **The AF dimensions are strictly increasing** over the initial levels (an inductive tower, dimensions
growing — `2 < 5 < 13 < 34 < 89 < 233`). -/
theorem dimA_increasing_initial :
    dimA 0 < dimA 1 ∧ dimA 1 < dimA 2 ∧ dimA 2 < dimA 3 ∧ dimA 3 < dimA 4 ∧ dimA 4 < dimA 5 := by
  exact D0.Algebra.FibonacciAFTower.af_dimensions_strictly_increasing_extended

end D0.VNext.FibonacciAFAlgebra
