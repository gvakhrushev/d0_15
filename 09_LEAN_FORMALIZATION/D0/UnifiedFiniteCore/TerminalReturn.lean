import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic

/-!
# D0-v15 Unified spine §5/§6 — bare terminal return sectors `C₄`, `C₃`

At trivial holonomy `λ = 1` the order-4 (`μ`) and order-3 (`τ`) terminal return operators are the cyclic
permutations `U_μ` (4-cycle on `c₁,c_i,c_{−1},c_{−i}`) and `U_τ` (3-cycle on `r_B,r_C,r_D`). Their finite
orders `U_μ⁴ = I`, `U_τ³ = I` give the bare characteristic factors `det(I−zU_μ)=1−z⁴`, `det(I−zU_τ)=1−z³`
(the polynomial/holonomy `λ` forms are verified exactly in `05_CERTS/verify_unified_backbone.py`).
-/

namespace D0.UnifiedFiniteCore.TerminalReturn

open Matrix

/-- Order-4 return `U_μ` (cyclic 4-permutation at `λ = 1`). -/
def Umu : Matrix (Fin 4) (Fin 4) ℤ := !![0,0,0,1; 1,0,0,0; 0,1,0,0; 0,0,1,0]

/-- Order-3 return `U_τ` (cyclic 3-permutation at `λ = 1`). -/
def Utau : Matrix (Fin 3) (Fin 3) ℤ := !![0,0,1; 1,0,0; 0,1,0]

/-- `U_μ⁴ = I`: the order-4 sector. -/
theorem Umu_order4 : Umu ^ 4 = 1 := by native_decide
/-- `U_τ³ = I`: the order-3 sector. -/
theorem Utau_order3 : Utau ^ 3 = 1 := by native_decide

/-- Neither return is the identity (the sectors genuinely rotate). -/
theorem returns_nontrivial : Umu ≠ 1 ∧ Utau ≠ 1 := by
  refine ⟨?_, ?_⟩ <;> native_decide

/-- Minimal orders: `U_μ²  ≠ I` and `U_τ` not `I` confirm the orders are exactly 4 and 3. -/
theorem Umu_order_exact : Umu ^ 2 ≠ 1 := by native_decide

/-- **D0-v15 §5/§6.** The terminal return sectors have exact orders 4 and 3 (branch orders matching the
`Q₈` Fourier ranks `(·,4,3)`). -/
theorem terminal_return :
    Umu ^ 4 = 1 ∧ Utau ^ 3 = 1 ∧ Umu ^ 2 ≠ 1 ∧ Umu ≠ 1 ∧ Utau ≠ 1 :=
  ⟨Umu_order4, Utau_order3, Umu_order_exact, returns_nontrivial.1, returns_nontrivial.2⟩

end D0.UnifiedFiniteCore.TerminalReturn
