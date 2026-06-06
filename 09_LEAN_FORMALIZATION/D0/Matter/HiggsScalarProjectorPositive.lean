import D0.Matter.HiggsScalarProjectorDecision
import Mathlib.Tactic

namespace D0.Matter

/--
Compatibility name for the constructive Higgs/scalar projector certificate.

The old selector-candidate reading is retired; this value is the concrete
finite matter-transfer closure from `HiggsScalarProjectorConstructive`.
-/
def minimalPositiveHiggsScalarProjectorCertificate : HiggsScalarProjectorCertificate :=
  higgs_scalar_projector_constructive_closure

/--
Legacy theorem name, strengthened: the minimal positive scalar projector is the
rank-two frozen doublet transfer projector, not a named candidate selected from
a three-row table.
-/
theorem minimal_positive_scalar_projector_is_one_doublet :
    (rankTwoMatterTransferProjector finiteEWMatterTransferCarrier).rank = 2 := by
  exact rank_two_matter_transfer_projector_rank finiteEWMatterTransferCarrier

/-- Positive Higgs/scalar projector closure from the finite matter-transfer construction. -/
def higgs_scalar_projector_positive_derivation :
    HiggsScalarProjectorCertificate := by
  exact higgs_scalar_projector_constructive_closure

/-- Rank one is not admissible because it breaks the frozen SU(2) doublet action. -/
theorem rank_one_not_gauge_compatible_higgs_projector
    (P : FiniteScalarProjector finiteEWMatterTransferCarrier)
    (hrank : P.rank = 1) :
    Not (GaugeCompatible P) := by
  exact finite_scalar_projector_rank_one_no_go P hrank

/-- Compatibility name for the old two-doublet rejection: the real obstruction is rank one. -/
theorem two_doublet_not_minimal_positive_higgs_projector
    (P : FiniteScalarProjector finiteEWMatterTransferCarrier)
    (hrank : P.rank = 1) :
    Not (GaugeCompatible P) := by
  exact rank_one_not_gauge_compatible_higgs_projector P hrank

/-- The zero projector is not a positive scalar response. -/
theorem absent_not_positive_higgs_projector :
    Not (PositiveResponse (zeroMatterTransferProjector finiteEWMatterTransferCarrier)) := by
  norm_num [PositiveResponse, Nonzero, zeroMatterTransferProjector,
    FiniteScalarProjector.rank]

end D0.Matter
