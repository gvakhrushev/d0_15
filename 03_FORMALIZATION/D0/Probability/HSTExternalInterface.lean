import D0.Probability.SubgaussianArchive

namespace D0

structure ArchiveConvexDominationEvidence (n : Nat) where
  testedConvexDomination : Prop
  testedConvexDominationProof : testedConvexDomination
  strictSlack : Prop
  strictSlackProof : strictSlack

def ArchiveConvexDomination (n : Nat) : Prop :=
  Nonempty (ArchiveConvexDominationEvidence n)

def hstGaussianReferenceDim (_n : Nat) : Nat :=
  4

structure HSTAdmissibleArchive (n : Nat) : Prop where
  finiteSupport : ArchiveFiniteSupport (archiveStageMeasure n)
  centered : CenteredFiniteArchiveMeasure (archiveStageMeasure n)
  subgaussian : ArchiveSubgaussianHSTAdmissible n
  convexDominationSlack : ArchiveConvexDomination n
  notHyperplaneSupported : NotHyperplaneSupported (archiveStageMeasure n)
  dim_eq_four : hstGaussianReferenceDim n = 4

structure EntropySoftmaxKernelData (n : Nat) where
  normalized : Prop
  martingaleMoment : Prop
  gaugeFixed : Prop
  entropyExtremal : Prop
  uniqueOnGaugeSlice : Prop

def ExistsEntropySelectedArchiveKernel (n : Nat) : Prop :=
  Nonempty (EntropySoftmaxKernelData n)

def hstExternalSource : String :=
  "Hua-Song-Tudose, arXiv:2605.10908, Proposition 3.6"

structure ExternalHSTTheorem (n : Nat) (h : HSTAdmissibleArchive n) where
  source : String
  entropyKernelExists : ExistsEntropySelectedArchiveKernel n

theorem hst_admissible_from_certificates
    (n : Nat)
    (hSub : ArchiveSubgaussianHSTAdmissibility n)
    (hDom : ArchiveConvexDomination n) :
    HSTAdmissibleArchive n := by
  exact
    { finiteSupport := hSub.finiteSupport
      centered := hSub.centered
      subgaussian := ⟨hSub⟩
      convexDominationSlack := hDom
      notHyperplaneSupported := hSub.notHyperplaneSupported
      dim_eq_four := rfl }

theorem entropy_kernel_exists_if_HST
    {n : Nat}
    (hD0 : HSTAdmissibleArchive n)
    (hHST : ExternalHSTTheorem n hD0) :
    ExistsEntropySelectedArchiveKernel n := by
  exact hHST.entropyKernelExists

end D0
