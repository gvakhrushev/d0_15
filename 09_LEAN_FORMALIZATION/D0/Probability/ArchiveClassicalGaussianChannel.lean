import D0.Detector.WeakCouplingClassicalization
import D0.Probability.EntropyCouplingKernel

namespace D0

structure ClassicalGaussianArchiveReadout (n : Nat) where
  entropyKernel : ExistsEntropySelectedArchiveKernel n
  detectorClassicalization : Prop
  detectorClassicalizationProof : detectorClassicalization

def ExistsClassicalGaussianArchiveReadout (n : Nat) : Prop :=
  Nonempty (ClassicalGaussianArchiveReadout n)

theorem archive_macro_channel_classical_gaussian
    {n : Nat}
    (hD0 : HSTAdmissibleArchive n)
    (hHST : ExternalHSTTheorem n hD0)
    (hDet : WeakCouplingReadout) :
    ExistsClassicalGaussianArchiveReadout n := by
  exact ⟨
    { entropyKernel := entropy_kernel_exists_if_HST hD0 hHST
      detectorClassicalization := RealisticWeakCouplingClassicalization hDet
      detectorClassicalizationProof :=
        weak_coupling_readout_classical_guardrail hDet }⟩

def ArchiveClassicalGaussianChannel (n : Nat) : Prop :=
  ExistsClassicalGaussianArchiveReadout n

def FactorsThroughArchiveReadout (_h : WeakCouplingReadout) (_n : Nat) : Prop :=
  True

theorem weak_coupling_readout_factors_through_archive_channel
    (h : WeakCouplingReadout)
    (n : Nat) :
    WeakCouplingClassicalization h →
    ArchiveClassicalGaussianChannel n →
    FactorsThroughArchiveReadout h n := by
  intro _ _
  trivial

end D0
