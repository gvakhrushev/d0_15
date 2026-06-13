import Mathlib.Tactic
import D0.Core.Delta
import D0.Phi

namespace D0.Defect

noncomputable def pi0D0 : ℝ := (6 / 5 : ℝ) * D0.phi^2
noncomputable def tau0D0 : ℝ := 2 * pi0D0

noncomputable def pPlus : ℝ := D0.phi⁻¹
noncomputable def pMinus : ℝ := D0.phi⁻¹^2
noncomputable def branchGap : ℝ := pPlus - pMinus

theorem pPlus_add_pMinus :
  pPlus + pMinus = 1 := by
  unfold pPlus pMinus
  exact D0.p_unit_closure

theorem branchGap_eq_two_delta0 :
  branchGap = 2 * D0.delta0 := by
  unfold branchGap pPlus pMinus D0.delta0
  ring

theorem pi0D0_forced :
  pi0D0 = (6 / 5 : ℝ) * D0.phi^2 := by
  rfl

theorem tau0D0_forced :
  tau0D0 = 2 * pi0D0 := by
  rfl

end D0.Defect
