import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Rat.Defs
import D0.Defect.Basic
import D0.Defect.ProjectiveGeneration

namespace D0.Matter

abbrev GenerationIndex := D0.Defect.BranchRay

structure MatterRep where
  carrier : Type
  fintypeCarrier : Fintype carrier
  gaugeCharges : carrier → ℚ
  anomalySum : ℚ

attribute [instance] MatterRep.fintypeCarrier

abbrev RepWithGenerations (R : MatterRep) : Type :=
  GenerationIndex × R.carrier

end D0.Matter
