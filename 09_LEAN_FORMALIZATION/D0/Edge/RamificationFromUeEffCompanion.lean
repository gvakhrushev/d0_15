import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic

/-!
# D0-EDGE-RAMIFICATION-001 — companion-cover ramification of the edge resolvent

BOOK edge layer. Python certificate: `05_CERTS/vp_ramification_edge_ueff_companion.py`.

The edge resolvent acquires ramification through two explicit cyclic companion blocks: a 4-cycle
terminal-capacity block `C4` (charpoly `x⁴ − λ`) and a 3-cycle scene-rank block `R3` (charpoly
`x³ − λ`). The companion's defining (Cayley–Hamilton) relation is `C4⁴ = λ·I`, `R3³ = λ·I`: at the
branch point `λ = 0` each cover **totally ramifies** (the block becomes nilpotent — all sheets collapse
to the single eigenvalue 0), whereas the diagonal control `diag(1,2,3,4)` has 4 distinct sheets and is
never nilpotent (no ramification).

This module machine-checks that finite arithmetic over `ℚ`: the cyclic relations, total ramification
(nilpotency) at `λ = 0`, and the unramified negative control. The physical-edge embedding (`C4 ↔ muon
terminal capacity`, `R3 ↔ tau scene-rank holonomy`, no inflation of the 359-dim edge) stays in the cert.
-/

namespace D0.Edge

open Matrix

/-- 4-cycle terminal-capacity companion block (charpoly `x⁴ − λ`). -/
def companionC4 (lam : ℚ) : Matrix (Fin 4) (Fin 4) ℚ :=
  !![0, 1, 0, 0; 0, 0, 1, 0; 0, 0, 0, 1; lam, 0, 0, 0]

/-- 3-cycle scene-rank companion block (charpoly `x³ − λ`). -/
def companionR3 (lam : ℚ) : Matrix (Fin 3) (Fin 3) ℚ :=
  !![0, 1, 0; 0, 0, 1; lam, 0, 0]

/-- Diagonal negative control with 4 distinct sheets. -/
def diagControl : Matrix (Fin 4) (Fin 4) ℚ :=
  !![1, 0, 0, 0; 0, 2, 0, 0; 0, 0, 3, 0; 0, 0, 0, 4]

/-- **4-cycle relation:** `C4⁴ = λ·I` (the companion satisfies its charpoly `x⁴ − λ`). -/
theorem companionC4_cyclic (lam : ℚ) :
    (companionC4 lam) ^ 4 = lam • (1 : Matrix (Fin 4) (Fin 4) ℚ) := by
  simp only [pow_succ, pow_zero, one_mul]
  unfold companionC4
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_four, Matrix.smul_apply]

/-- **3-cycle relation:** `R3³ = λ·I` (the companion satisfies its charpoly `x³ − λ`). -/
theorem companionR3_cyclic (lam : ℚ) :
    (companionR3 lam) ^ 3 = lam • (1 : Matrix (Fin 3) (Fin 3) ℚ) := by
  simp only [pow_succ, pow_zero, one_mul]
  unfold companionR3
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_three, Matrix.smul_apply]

/-- **Total ramification at the branch point `λ = 0`:** `C4` becomes nilpotent (`C4⁴ = 0`). -/
theorem companionC4_nilpotent_at_zero : (companionC4 0) ^ 4 = 0 := by native_decide

/-- **Total ramification at the branch point `λ = 0`:** `R3` becomes nilpotent (`R3³ = 0`). -/
theorem companionR3_nilpotent_at_zero : (companionR3 0) ^ 3 = 0 := by native_decide

/-- **Negative control (no ramification):** the diagonal block is NOT nilpotent. -/
theorem diagControl_not_nilpotent : (diagControl) ^ 4 ≠ 0 := by native_decide

/-- The 4 control sheets are distinct (`1,2,3,4` pairwise distinct). -/
theorem diagControl_distinct_sheets :
    (1 : ℚ) ≠ 2 ∧ (1 : ℚ) ≠ 3 ∧ (1 : ℚ) ≠ 4 ∧ (2 : ℚ) ≠ 3 ∧ (2 : ℚ) ≠ 4 ∧ (3 : ℚ) ≠ 4 := by
  norm_num

/-- **D0-EDGE-RAMIFICATION-001.** The companion cover: `C4⁴ = λ·I`, `R3³ = λ·I`; both totally ramify
(go nilpotent) at the branch point `λ = 0`; and the diagonal control is unramified (not nilpotent,
4 distinct sheets). -/
theorem ramification_companion_cover_cert :
    (∀ lam : ℚ, (companionC4 lam) ^ 4 = lam • (1 : Matrix (Fin 4) (Fin 4) ℚ)) ∧
    (∀ lam : ℚ, (companionR3 lam) ^ 3 = lam • (1 : Matrix (Fin 3) (Fin 3) ℚ)) ∧
    (companionC4 0) ^ 4 = 0 ∧
    (companionR3 0) ^ 3 = 0 ∧
    (diagControl) ^ 4 ≠ 0 :=
  ⟨companionC4_cyclic, companionR3_cyclic, companionC4_nilpotent_at_zero,
   companionR3_nilpotent_at_zero, diagControl_not_nilpotent⟩

end D0.Edge
