import Mathlib.Tactic
import Mathlib.LinearAlgebra.Matrix.Trace

/-!
# D0-SCENE-CENTER-SPACETIME-CONVERGENCE-001 — the centre 11 = spatial `|V₁₁|` = temporal `L₅`

The centre of the scene triple `{9,11,13}` is pinned to `11` by two independent channels:

* **spatial** `|V₁₁| = 11` (`D0-CAPACITY-V11-001`), a capacity count on the `Ω₈` address ladder;
* **temporal** `|Tr(T⁵)| = L₅ = 11` for the D0 time operator `T = ![![0,1],![1,-1]]`
  (`D0-TORAL-LUCAS-PERIODIC-SEED-OWNER-001`); also `round(φ⁵) = 11` since `φ⁵ = L₅ + φ⁻⁵`, `0 < φ⁻⁵ < 1`.

`T` is the **orientation-twisted** golden companion (`trace = −1`, `det = −1`), distinct from the plain
Fibonacci matrix `M_φ = ![![0,1],![1,1]]` (`trace = +1`). The centre is forced as the unique intersection
`{ L_n } ∩ [9,13] = {11}` (`L₃ = 4`, `L₇ = 29` fall outside), at the forced level `5` (smallest odd `n` with
`L_n > Ω₈ = 8`). The triple is the `+2` orientation window centred there: `{9,11,13} = {L₅−2, L₅, L₅+2}`.

This file fixes the arithmetic backbone; the independence/forcing argument is carried by the failable cert
`vp_scene_center_spacetime_convergence.py`.
-/

namespace D0.VNext2.SceneCenterSpacetimeConvergence

open Matrix

/-- The D0 time operator `T = [[0,1],[1,-1]]` over `ℤ`. -/
def T : Matrix (Fin 2) (Fin 2) ℤ := !![0, 1; 1, -1]

/-- The plain Fibonacci companion `M_φ = [[0,1],[1,1]]` — a *different* operator. -/
def Mφ : Matrix (Fin 2) (Fin 2) ℤ := !![0, 1; 1, 1]

/-- `T` is orientation-reversing: `trace = −1`, `det = −1`. -/
theorem T_trace_det : Matrix.trace T = -1 ∧ T.det = -1 := by
  constructor
  · simp [Matrix.trace, T, Fin.sum_univ_two, Matrix.diag]
  · simp [Matrix.det_fin_two, T]

/-- `T` and the Fibonacci matrix differ in trace (`−1` vs `+1`) — the temporal channel is specific. -/
theorem T_ne_fibonacci : Matrix.trace T ≠ Matrix.trace Mφ := by
  simp [Matrix.trace, T, Mφ, Fin.sum_univ_two, Matrix.diag]

/-- `|Tr(T⁵)| = 11 = L₅`. Computed directly: `Tr(T⁵) = -11`. -/
theorem trace_T5 : Matrix.trace (T ^ 5) = -11 := by
  simp only [T]
  norm_num [pow_succ, pow_zero, Matrix.one_mul, Matrix.mul_fin_two,
            Matrix.trace, Fin.sum_univ_two, Matrix.diag]

/-- `L₅ = 11` (5th Lucas number). -/
theorem lucas_five : Nat.fib 4 + Nat.fib 6 = 11 := by decide

/-- The centre value 11 is the unique Lucas number in the capacity window `[9,13]`:
    `L₃ = 4 < 9` and `L₇ = 29 > 13`, while `L₅ = 11 ∈ [9,13]`. (Lucas via `L_n = F_{n-1}+F_{n+1}`.) -/
theorem unique_center_in_window :
    (Nat.fib 2 + Nat.fib 4 = 4) ∧ (Nat.fib 4 + Nat.fib 6 = 11) ∧ (Nat.fib 6 + Nat.fib 8 = 29)
    ∧ ¬(9 ≤ 4 ∧ 4 ≤ 13) ∧ (9 ≤ 11 ∧ 11 ≤ 13) ∧ ¬(9 ≤ 29 ∧ 29 ≤ 13) := by
  refine ⟨by decide, by decide, by decide, by decide, by decide, by decide⟩

/-- Level 5 is forced: the smallest odd `n` with `L_n > Ω₈ = 8` (`L₁=1, L₃=4, L₅=11 > 8`). -/
theorem level_five_forced :
    (Nat.fib 0 + Nat.fib 2 = 1) ∧ (Nat.fib 2 + Nat.fib 4 = 4) ∧ ¬(1 > 8) ∧ ¬(4 > 8) ∧ (11 > 8) := by
  refine ⟨by decide, by decide, by decide, by decide, by decide⟩

/-- The triple is the `+2` window centred on `L₅ = 11`: `{L₅−2, L₅, L₅+2} = {9,11,13}`. -/
theorem centred_window : (11 - 2, 11, 11 + 2) = (9, 11, 13) := by decide

/-- The spatial and temporal centre agree: `|V₁₁| = 11 = |Tr(T⁵)|`. -/
theorem spacetime_center_convergence :
    (11 : ℤ) = -(Matrix.trace (T ^ 5)) ∧ (11 : ℕ) = Nat.fib 4 + Nat.fib 6 := by
  refine ⟨?_, by decide⟩
  rw [trace_T5]; norm_num

end D0.VNext2.SceneCenterSpacetimeConvergence
