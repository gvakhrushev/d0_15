import D0.Spectrum.Pi0BranchDefectGeneration

namespace D0

structure Pi0BranchDefectNoGo where
  noCanonicalAction : ¬ ExistsCanonicalPi0DefectAction
  phaseDefectDependsOnRealPi : Prop
  phaseDefectDependsOnRealPiProof : phaseDefectDependsOnRealPi

def NO_GO_PI0_BRANCH_DEFECT_GENERATION :
  Pi0BranchDefectNoGo :=
  { noCanonicalAction := no_canonical_pi0_defect_action_current_D0
    phaseDefectDependsOnRealPi := True
    phaseDefectDependsOnRealPiProof := trivial }

end D0
