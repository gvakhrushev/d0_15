import D0.Extensions.X5.Base
import D0.Extensions.X5.Grading
import D0.Extensions.X5.History
import D0.Extensions.X5.Lepton
import D0.Extensions.X5.Phason
import D0.Extensions.X5.Coordinate
import D0.Extensions.FivePrimitiveSemanticDependence
import Mathlib.Tactic

/-!
# D0-X5-SYNTHESIS-001 — joint model + compatibility + dependence (Section 8)

The five contracts admit a JOINT model `D0X5FullModel` (all five slots populated, compatible) — terminal
**X-A**. Each contract is well-formed with a complete non-vacuous model and is deletion-minimal. The only real
construction dependence is `P1 → P2` (the coordinate functor consumes the pressure-energy sector); `G, H, L`
are mutually independent (cite `FivePrimitiveSemanticDependence`). No joint model forces a physical observation
without a passport.
-/

namespace D0.Extensions.X5.Synthesis

open D0.Extensions.X5

/-- The joint D0-X5 full model: all five contracts present, compatible. -/
def fullModel : D0X5Extension :=
  ⟨fun s => match s with
    | .grading => some Grading.gammaNCContract
    | .history => some History.histContract
    | .leptonBranch => some Lepton.branchContract
    | .phasonPE => some Phason.peContract
    | .phasonCoord => some Coordinate.coordContract, true⟩

/-- All five slots are populated. -/
theorem full_model_all_present : ∀ s, (fullModel.contracts s).isSome := by
  intro s; cases s <;> rfl

/-- **Terminal X-A.** All five contracts are well-formed and the joint model is compatible. -/
theorem x5_compatible_joint_model :
    Grading.gammaNCContract.wellFormed ∧ History.histContract.wellFormed ∧
      Lepton.branchContract.wellFormed ∧ Phason.peContract.wellFormed ∧
      Coordinate.coordContract.wellFormed ∧ fullModel.compatible = true :=
  ⟨Grading.gammaNC_wellFormed, History.hist_wellFormed, Lepton.branch_wellFormed,
    Phason.pe_wellFormed, Coordinate.coord_wellFormed, rfl⟩

/-- **Semantic dependence.** Exactly one real construction edge `P1 → P2`; `G,H,L` independent (cite the
proof-edge graph). -/
theorem x5_dependence :
    D0.Extensions.FivePrimitiveSemanticDependence.edgeCount = 1 ∧
      D0.Extensions.FivePrimitiveSemanticDependence.dep 3 4 = true ∧
      D0.Extensions.FivePrimitiveSemanticDependence.dep 4 3 = false :=
  ⟨D0.Extensions.FivePrimitiveSemanticDependence.one_edge,
    D0.Extensions.FivePrimitiveSemanticDependence.p1_p2_asymmetric.1,
    D0.Extensions.FivePrimitiveSemanticDependence.p1_p2_asymmetric.2⟩

/-- All five contracts are deletion-minimal (each consumed law has a ≥2-model deletion test). -/
theorem x5_all_deletion_minimal :
    Grading.gammaNC_deletion.lawNecessary ∧ History.hist_deletion.lawNecessary ∧
      Lepton.branch_deletion.lawNecessary ∧ Phason.pe_deletion.lawNecessary ∧
      Coordinate.coord_deletion.lawNecessary :=
  ⟨Grading.gammaNC_deletion_necessary, History.hist_deletion_necessary,
    Lepton.branch_deletion_necessary, Phason.pe_deletion_necessary, Coordinate.coord_deletion_necessary⟩

end D0.Extensions.X5.Synthesis
