import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic

/-!
# D0-v15 Unified spine §3 — marked `Q₈` terminal Fourier decomposition

The terminal subsystem `Ω₈ ≅ Q₈` (the quaternion group on `V₉ = {ω₀} ⊔ Ω₈`) has group algebra
`ℂ[Q₈] ≅ ℂ⁴ ⊕ M₂(ℂ)`. The three physically-used Fourier projectors, built from the left regular
representation (`E₀ = ⅛Σ_q L_q`, `E₄ = ½(I−L_{−1})`, `E₃ = ½(I+L_{−1})−E₀`), are exact rational `8×8`
matrices. They are orthogonal idempotents summing to `I` with **ranks `(1,4,3)`** (= trace of each
idempotent). This is the branch-order signature `(1,4,3)` of the chain, derived from `Q₈` alone.

Fixed correspondence (consumed downstream): `Q₉↔E₀` (rank 1, unramified), `Q₁₁↔E₄` (rank 4, order-4
sector), `Q₁₃↔E₃` (rank 3, order-3 sector). All entries are computed from the `Q₈` multiplication table.
-/

namespace D0.UnifiedFiniteCore.Q8Terminal

open Matrix

/-- `E₀ = ⅛ Σ_{q∈Q₈} L_q` — the trivial-rep projector (rank 1). -/
def E0 : Matrix (Fin 8) (Fin 8) ℚ :=
  !![1/8,1/8,1/8,1/8,1/8,1/8,1/8,1/8;
     1/8,1/8,1/8,1/8,1/8,1/8,1/8,1/8;
     1/8,1/8,1/8,1/8,1/8,1/8,1/8,1/8;
     1/8,1/8,1/8,1/8,1/8,1/8,1/8,1/8;
     1/8,1/8,1/8,1/8,1/8,1/8,1/8,1/8;
     1/8,1/8,1/8,1/8,1/8,1/8,1/8,1/8;
     1/8,1/8,1/8,1/8,1/8,1/8,1/8,1/8;
     1/8,1/8,1/8,1/8,1/8,1/8,1/8,1/8]

/-- `E₄ = ½(I − L_{−1})` — the order-4 (`M₂`) sector projector (rank 4). -/
def E4 : Matrix (Fin 8) (Fin 8) ℚ :=
  !![1/2,0,0,0,-1/2,0,0,0;
     0,1/2,0,0,0,-1/2,0,0;
     0,0,1/2,0,0,0,-1/2,0;
     0,0,0,1/2,0,0,0,-1/2;
     -1/2,0,0,0,1/2,0,0,0;
     0,-1/2,0,0,0,1/2,0,0;
     0,0,-1/2,0,0,0,1/2,0;
     0,0,0,-1/2,0,0,0,1/2]

/-- `E₃ = ½(I + L_{−1}) − E₀` — the order-3 (three sign-reps) sector projector (rank 3). -/
def E3 : Matrix (Fin 8) (Fin 8) ℚ :=
  !![3/8,-1/8,-1/8,-1/8,3/8,-1/8,-1/8,-1/8;
     -1/8,3/8,-1/8,-1/8,-1/8,3/8,-1/8,-1/8;
     -1/8,-1/8,3/8,-1/8,-1/8,-1/8,3/8,-1/8;
     -1/8,-1/8,-1/8,3/8,-1/8,-1/8,-1/8,3/8;
     3/8,-1/8,-1/8,-1/8,3/8,-1/8,-1/8,-1/8;
     -1/8,3/8,-1/8,-1/8,-1/8,3/8,-1/8,-1/8;
     -1/8,-1/8,3/8,-1/8,-1/8,-1/8,3/8,-1/8;
     -1/8,-1/8,-1/8,3/8,-1/8,-1/8,-1/8,3/8]

theorem E0_idem : E0 * E0 = E0 := by native_decide
theorem E4_idem : E4 * E4 = E4 := by native_decide
theorem E3_idem : E3 * E3 = E3 := by native_decide

/-- Complete: `E₀ + E₄ + E₃ = I`. -/
theorem fourier_complete : E0 + E4 + E3 = (1 : Matrix (Fin 8) (Fin 8) ℚ) := by native_decide

theorem E0_E4_orth : E0 * E4 = 0 := by native_decide
theorem E0_E3_orth : E0 * E3 = 0 := by native_decide
theorem E4_E3_orth : E4 * E3 = 0 := by native_decide

/-- Branch-order signature: ranks `(E₀,E₄,E₃) = (1,4,3)` via trace of each idempotent. -/
theorem branch_orders : E0.trace = 1 ∧ E4.trace = 4 ∧ E3.trace = 3 := by
  refine ⟨?_,?_,?_⟩ <;> native_decide

/-- **D0-v15 §3.** The `Q₈` Fourier system: three orthogonal idempotents summing to `I`, with the
branch-order signature `(1,4,3)` = `(dim E₀, dim E₄, dim E₃)`. -/
theorem q8_terminal_fourier :
    E0 * E0 = E0 ∧ E4 * E4 = E4 ∧ E3 * E3 = E3 ∧
    E0 + E4 + E3 = (1 : Matrix (Fin 8) (Fin 8) ℚ) ∧
    E0 * E4 = 0 ∧ E0 * E3 = 0 ∧ E4 * E3 = 0 ∧
    E0.trace = 1 ∧ E4.trace = 4 ∧ E3.trace = 3 :=
  ⟨E0_idem, E4_idem, E3_idem, fourier_complete, E0_E4_orth, E0_E3_orth, E4_E3_orth,
    branch_orders.1, branch_orders.2.1, branch_orders.2.2⟩

end D0.UnifiedFiniteCore.Q8Terminal
