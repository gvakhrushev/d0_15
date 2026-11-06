import D0.Probability.SubgaussianArchive

namespace D0

/-- Internally proved source facts; this excludes the external comparison hypotheses. -/
structure FiniteArchiveHSTSourceFacts (n : Nat) : Prop where
  finiteSupport : ArchiveFiniteSupport (archiveStageMeasure n)
  centered : CenteredFiniteArchiveMeasure (archiveStageMeasure n)
  covarianceSlack : ArchiveCovarianceSlack (archiveStageMeasure n)
  subgaussian : FiniteArchiveHSTSourceAdmissible n
  notHyperplaneSupported : NotHyperplaneSupported (archiveStageMeasure n)

/-- Every configured stage satisfies these internal finite-source facts. -/
theorem archive_stage_finite_hst_source_facts (n : Nat) :
    FiniteArchiveHSTSourceFacts n := by
  have hSub := finiteArchive_hst_source_admissibility n
  exact
    { finiteSupport := hSub.finiteSupport
      centered := hSub.centered
      covarianceSlack := hSub.covarianceSlack
      subgaussian := ⟨hSub⟩
      notHyperplaneSupported := hSub.notHyperplaneSupported }

end D0
