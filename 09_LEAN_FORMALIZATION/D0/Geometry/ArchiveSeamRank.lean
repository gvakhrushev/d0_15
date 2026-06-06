import D0.Geometry.ArchiveSeamCurvature

namespace D0

def SeamCommutatorRankTwoObligation (n : Nat) : Prop :=
  ∃ _basisWitness : Matrix (Fin 2) (archivePhaseIndex n) ℝ,
    ArchiveSeamSupport n

structure SeamRankCertificate (n : Nat) where
  rankTwoChecked : SeamCommutatorRankTwoObligation n
  certificateName : String

end D0
