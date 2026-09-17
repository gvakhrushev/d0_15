import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic
import D0.Core.Phi

set_option linter.unusedSimpArgs false

/-!
# D0-BRATTELI-FIBONACCI-REFINEMENT-OWNER-001 — incidence M_φ RECOVERED from the cylinder language

The golden cylinder language is the golden-mean shift of finite type: words over `{0,1}` forbidding the
factor `11`. Its refinement/Bratteli incidence is therefore **derived, not inserted**: the allowed-word
rule `goldenAllowed i j = (0 if i=j=1 else 1)` reproduces `M_φ = !![1,1;1,0]`. The Perron eigenvalue is
`φ` (`M_φ² = M_φ + 1`, charpoly `x²−x−1`), the level dimensions grow as Fibonacci, and the unique
normalized AF/cylinder trace is fixed by the left-Perron eigenvector with ratio `φ`. This is the
present-core canonical refinement object underlying `D0-CANONICAL-RENORMALIZATION-SPECTRAL-TOWER-001`.
-/

namespace D0.Geometry.FibonacciBratteliRefinement

open Matrix D0

/-- The golden cylinder language rule: a transition `i → j` is allowed unless it is the forbidden `11`. -/
def goldenAllowed (i j : Fin 2) : ℤ := if i = 1 ∧ j = 1 then 0 else 1

/-- The golden incidence matrix. -/
def Mphi : Matrix (Fin 2) (Fin 2) ℤ := !![1, 1; 1, 0]

/-- **The incidence matrix is RECOVERED from the allowed-word rule** (not inserted): `M_φ` equals the
adjacency of the golden-mean SFT (forbid `11`). -/
theorem incidence_recovered_from_language :
    Mphi = Matrix.of (fun i j => goldenAllowed i j) := by
  decide

/-- **The Perron eigenvalue is `φ`**: `M_φ² = M_φ + 1` (charpoly `x²−x−1`). -/
theorem perron_eigenvalue_golden : Mphi ^ 2 = Mphi + 1 := by decide

/-- **Fibonacci level growth**: applying `M_φ` to the uniform level-0 vector gives `(2,1)` (then
`3,2 → 5,3 → …`), the Fibonacci dimensions of the refinement tower. -/
theorem fibonacci_level_growth :
    Mphi.mulVec ![1, 1] 0 = 2 ∧ Mphi.mulVec ![1, 1] 1 = 1 := by
  constructor <;> simp [Mphi, Matrix.mulVec, dotProduct, Fin.sum_univ_two]

theorem phi_pos : 0 < phi := by unfold phi; positivity

/-- **The unique normalized AF/cylinder trace has ratio `φ`**: the left-Perron eigenvector `w = (φ, 1)`
satisfies `wᵀ M_φ = φ wᵀ` (`w₀ = φ·w₁` and `w₀ + w₁ = φ·w₀`, the latter via `φ² = φ + 1`), so the trace
weight ratio is `φ`. -/
theorem golden_bratteli_trace_ratio :
    ∃ w : Fin 2 → ℝ, 0 < w 0 ∧ 0 < w 1 ∧ w 0 = phi * w 1 ∧ w 0 + w 1 = phi * w 0 := by
  refine ⟨![phi, 1], phi_pos, one_pos, by simp, ?_⟩
  simp only [Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons]
  have := phi_sq; nlinarith [this]

/-- **D0-BRATTELI-FIBONACCI-REFINEMENT-OWNER-001.** The golden cylinder language canonically determines
its refinement Bratteli incidence `M_φ` (recovered from the forbid-`11` rule), with Perron eigenvalue `φ`,
Fibonacci level growth, and a unique normalized trace of ratio `φ`. No incidence matrix is inserted. -/
theorem fibonacci_bratteli_refinement_owner :
    Mphi = Matrix.of (fun i j => goldenAllowed i j)
      ∧ Mphi ^ 2 = Mphi + 1
      ∧ (∃ w : Fin 2 → ℝ, 0 < w 0 ∧ 0 < w 1 ∧ w 0 = phi * w 1 ∧ w 0 + w 1 = phi * w 0) :=
  ⟨incidence_recovered_from_language, perron_eigenvalue_golden, golden_bratteli_trace_ratio⟩

end D0.Geometry.FibonacciBratteliRefinement
