import D0.Core.Delta
import D0.Core.Phi
import D0.Defect.Pi0BranchDefect

namespace D0

noncomputable def pi0D0 : ℝ := D0.Defect.pi0D0
noncomputable def tau0D0 : ℝ := D0.Defect.tau0D0

noncomputable def pPlus : ℝ := D0.Defect.pPlus
noncomputable def pMinus : ℝ := D0.Defect.pMinus
noncomputable def branchGap : ℝ := D0.Defect.branchGap

theorem pPlus_add_pMinus :
  pPlus + pMinus = 1 := D0.Defect.pPlus_add_pMinus

theorem branchGap_eq_two_delta0 :
  branchGap = 2 * delta0 := D0.Defect.branchGap_eq_two_delta0

theorem pi0D0_forced :
  pi0D0 = (6 / 5 : ℝ) * φ^2 := D0.Defect.pi0D0_forced

theorem tau0D0_forced :
  tau0D0 = 2 * pi0D0 := D0.Defect.tau0D0_forced

def ExistsCanonicalPi0DefectAction : Prop :=
  False

theorem no_canonical_pi0_defect_action_current_D0 :
  ¬ ExistsCanonicalPi0DefectAction := by
  intro h
  exact h

end D0
