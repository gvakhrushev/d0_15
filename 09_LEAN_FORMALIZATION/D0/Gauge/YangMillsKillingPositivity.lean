import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic

open scoped BigOperators

namespace D0.Gauge

noncomputable def discreteYangMillsAction {ι κidx g : Type}
    [Fintype ι] [Fintype κidx]
    (Killing : g → g → ℝ) (K : Matrix ι κidx g) : ℝ :=
  -∑ i : ι, ∑ j : κidx, Killing (K i j) (K i j)

theorem discreteYangMillsAction_nonnegative_of_killing_nonpos {ι κidx g : Type}
    [Fintype ι] [Fintype κidx]
    (Killing : g → g → ℝ) (K : Matrix ι κidx g)
    (hKilling : ∀ x : g, Killing x x ≤ 0) :
    discreteYangMillsAction Killing K ≥ 0 := by
  unfold discreteYangMillsAction
  have hsum : (∑ i : ι, ∑ j : κidx, Killing (K i j) (K i j)) ≤ 0 := by
    apply Finset.sum_nonpos
    intro i _
    apply Finset.sum_nonpos
    intro j _
    exact hKilling (K i j)
  linarith

end D0.Gauge
