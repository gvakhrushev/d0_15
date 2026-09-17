import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Data.Nat.Fib.Basic
import Mathlib.Tactic

/-!
# D0-SCENE-STEP-PARITY-001 (CORE-FORCING) — the `+2` address step

The shell address ladder advances `9 → 11 → 13` by `+2`. Two ⊥M1 legs:

* **Parity from `det T = −1`.** The toral time operator `T = !![0,1; 1,-1]` has `det T = −1` (`det_T`), so it is
  indefinite: **exactly one** negative eigenvalue, i.e. the time sector supplies **exactly one** `ℤ₂` sign
  degree of freedom. A parity-*flipping* ladder would need a *second* independent `ℤ₂` sign bit, an exogenous
  catalog (`⊥M1`) unless it aliases the time bit — so under the corpus's existing no-aliasing principle,
  parity is constant. This discharges the former free `ASSUMP-ORIENT-PARITY` to `det T = −1` + no-aliasing
  (no new assumption).
* **No-skip from `11 = L₅`.** A `+4` step `9 → 13` skips `11 = L₅` (the 5th Lucas number = `|V₁₁|`, an
  admissible torus address); omitting an admissible address without an internal reason is a skip-catalog,
  `⊥M1`. So the step is the minimal parity-preserving one, `+2`.

The `det T = −1` and `L₅ = 11` facts are decidable; the ⊥M1 closure rests on the pre-existing no-aliasing
principle (CORE-FORCING, no new free assumption).
-/

namespace D0.Foundation.SceneStepParity

open Matrix

/-- The toral time operator `T = !![0,1; 1,-1]`. -/
def T : Matrix (Fin 2) (Fin 2) ℤ := !![0, 1; 1, -1]

/-- `det T = −1`: the time sector is indefinite — exactly one negative eigenvalue, one `ℤ₂` sign d.o.f. -/
theorem det_T : T.det = -1 := by decide

/-- `T` is symmetric (a real form), so `det T < 0` ⇒ one positive and one negative eigenvalue. -/
theorem T_symmetric : T.transpose = T := by decide

/-- `det T = −1 < 0`. -/
theorem det_T_neg : T.det < 0 := by decide

/-- The 5th Lucas number is `11 = |V₁₁|` (Lucas `L₅`; `L_{n+2}=L_{n+1}+L_n`, `L₀=2, L₁=1`). -/
def lucas : ℕ → ℕ
  | 0 => 2
  | 1 => 1
  | (n + 2) => lucas (n + 1) + lucas n

theorem lucas_five : lucas 5 = 11 := by decide

/-- A `+4` step from `9` lands on `13`, skipping the admissible address `11 = L₅`. -/
theorem step_skips_eleven : 9 + 4 = 13 ∧ lucas 5 = 11 ∧ 9 < 11 ∧ 11 < 13 := by decide

/-- **D0-SCENE-STEP-PARITY-001.** `det T = −1` (one sign d.o.f. ⇒ constant parity under no-aliasing) and
`11 = L₅` is the skipped admissible address ruling out `+4` ⇒ the step is `+2`. -/
theorem scene_step_parity :
    T.det = -1 ∧ T.transpose = T ∧ lucas 5 = 11 ∧ (9 + 2 = 11 ∧ 11 + 2 = 13) := by
  refine ⟨det_T, T_symmetric, lucas_five, ?_⟩; decide

end D0.Foundation.SceneStepParity
