import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Fintype.Basic
import D0.Phi
import D0.Core.Delta
import D0.Spectrum.Pi0BranchDefectGeneration
import D0.Defect.Basic
import D0.Defect.ProjectiveGeneration

namespace D0

abbrev F2 := ZMod 2
abbrev Vec2F2 := F2 × F2

def ePlus : Vec2F2 := D0.Defect.ePlus
def eMinus : Vec2F2 := D0.Defect.eMinus
def eGap : Vec2F2 := D0.Defect.eGap

def NonzeroVec (v : Vec2F2) : Prop := v ≠ 0

instance decidableNonzero (v : Vec2F2) : Decidable (v ≠ 0) :=
  instDecidableNot

abbrev BranchRay := D0.Defect.BranchRay

theorem ePlus_nonzero :
  NonzeroVec ePlus := D0.Defect.ePlus_nonzero

theorem eMinus_nonzero :
  NonzeroVec eMinus := D0.Defect.eMinus_nonzero

theorem eGap_nonzero :
  NonzeroVec eGap := D0.Defect.eGap_nonzero

theorem branchRay_card :
  Fintype.card BranchRay = 3 := D0.Defect.branchRay_card

def defectAction (v : Vec2F2) : Vec2F2 :=
  D0.Defect.defectAction v

theorem defectAction_ePlus :
  defectAction ePlus = eMinus := D0.Defect.defectAction_ePlus

theorem defectAction_eMinus :
  defectAction eMinus = eGap := D0.Defect.defectAction_eMinus

theorem defectAction_eGap :
  defectAction eGap = ePlus := D0.Defect.defectAction_eGap

theorem defectAction_order_three :
  ∀ v : Vec2F2, defectAction (defectAction (defectAction v)) = v := D0.Defect.defectAction_order_three

theorem exactly_three_projective_branch_defect_generations :
  Fintype.card BranchRay = 3 := D0.Defect.branchRay_card

inductive DefectGeneration
  | plus
  | minus
  | gap
  deriving Fintype, DecidableEq

noncomputable def realLift : DefectGeneration → ℝ
  | .plus => pPlus
  | .minus => pMinus
  | .gap => branchGap

theorem defect_generation_card :
  Fintype.card DefectGeneration = 3 := by
  rfl

end D0
