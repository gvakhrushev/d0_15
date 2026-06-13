import D0.Probability.HSTExternalInterface

namespace D0

structure StrictSlackEvidence (n : Nat) where
  domination : ArchiveConvexDomination n
  slackWitness : Prop
  slackProof : slackWitness

def StrictSlack (n : Nat) : Prop :=
  Nonempty (StrictSlackEvidence n)

structure GaugeFixedEvidence (n : Nat) where
  uGauge : Prop
  uGaugeProof : uGauge
  vGauge : Prop
  vGaugeProof : vGauge

def GaugeFixed (n : Nat) : Prop :=
  Nonempty (GaugeFixedEvidence n)

structure UniqueEntropyForgettingKernel (n : Nat) : Prop where
  domination : ArchiveConvexDomination n
  slack : StrictSlack n
  gauge : GaugeFixed n
  entropyKernel : ExistsEntropySelectedArchiveKernel n

theorem archive_entropy_kernel_exists_if_HST
    {n : Nat}
    (hD0 : HSTAdmissibleArchive n)
    (hHST : ExternalHSTTheorem n hD0) :
    ExistsEntropySelectedArchiveKernel n := by
  exact entropy_kernel_exists_if_HST hD0 hHST

theorem archive_forgetting_channel_unique
    {n : Nat}
    (hDom : ArchiveConvexDomination n)
    (hSlack : StrictSlack n)
    (hGauge : GaugeFixed n)
    (hEntropy : ExistsEntropySelectedArchiveKernel n) :
    UniqueEntropyForgettingKernel n := by
  exact
    { domination := hDom
      slack := hSlack
      gauge := hGauge
      entropyKernel := hEntropy }

end D0
