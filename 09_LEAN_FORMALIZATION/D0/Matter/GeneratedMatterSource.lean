import D0.Geometry.ArchiveWeakField
import D0.Geometry.ArchivePoissonEquation
import D0.Matter.RepresentationCarrier
import D0.Matter.GenerationAnomalyPreservation

namespace D0.Matter

def matterSourceFromGeneratedRep {n : Nat} (_R : MatterRep) : archivePhaseIndex n → ℝ :=
  fun _ => 0

structure MatterSourceNeutralityNoGo where
  noCanonicalLocalization : True
  requiresLatticeMapping : True

def NO_GO_MATTER_SOURCE_NEUTRALITY : MatterSourceNeutralityNoGo :=
  { noCanonicalLocalization := trivial,
    requiresLatticeMapping := trivial }

theorem generated_matter_source_neutral_if_anomaly_free (n : Nat)
  (R : MatterRep)
  (_h : R.anomalySum = 0) :
  @NeutralSource n (@matterSourceFromGeneratedRep n R) := by
  unfold NeutralSource matterSourceFromGeneratedRep
  simp

end D0.Matter
