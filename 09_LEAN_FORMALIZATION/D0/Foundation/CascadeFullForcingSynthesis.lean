import D0.Foundation.CascadeCarriedAssembly
import D0.Foundation.CascadeTopologicalShellAttachment
import D0.Foundation.ConcreteIndependentDetectionRepairSemantics

/-!
# Full carried forcing synthesis: the cascade is a DAG, not a false linear chain

The registered umbrella prose is written as one line. The formal work reveals a sharper structure:
the carried necessities form a **forcing DAG**.

This module adds the missing first shared-object interlock:

* the dyadic comparison repair verifies a reading but still collapses the two operation histories;
* the two-loop repair separates exactly those histories.

It then assembles every carried edge:

```
comparison ─→ one-loop memory ─→ order memory ─→ scale non-capture
                                     │
                                     └→ closed defect ─→ shell 2-cell
                                                          └→ repair quotient scene
                                                               └→ (9,11,13) by capacity
```

The branch is load-bearing. A precise countermodel proves that the linear prose edge
`non-captured scale → two-loop memory` is false: a one-register model can carry `φ` while still
collapsing the two histories. Therefore the honest full theorem is the DAG, not a forged linear
implication. This closes the carried architecture and closes the *linear route* as a no-go.
-/

namespace D0.Foundation.CascadeFullForcingSynthesis

open D0.Foundation
open D0.Foundation.CascadeTopologicalShellAttachment
open D0.Foundation.ConcreteIndependentDetectionRepairSemantics
open D0.Foundation.DiscriminationRetyping
open D0.Foundation.M1CascadeSceneNoGo
open D0.Foundation.M1RepairObservationalQuotient

/-! ## Missing first interlock: comparison repair still needs memory -/

/-- The dyadic comparison record produced from a history by direct/return agreement. -/
def dyadHistoryRecord (h : List Op) : ℤ × ℤ :=
  (runOne h 0, runOne h 0)

theorem dyad_accepts_history_record (h : List Op) :
    dyadAcceptor (dyadHistoryRecord h) := by
  rfl

/-- The dyad verifies current agreement but cannot recover which operation history produced it. -/
theorem dyad_comparison_collapses_histories :
    h₁ ≠ h₂
      ∧ dyadHistoryRecord h₁ = dyadHistoryRecord h₂
      ∧ dyadAcceptor (dyadHistoryRecord h₁)
      ∧ dyadAcceptor (dyadHistoryRecord h₂)
      ∧ runTwo h₁ (0, 0) ≠ runTwo h₂ (0, 0) := by
  refine ⟨histories_differ, ?_, dyad_accepts_history_record h₁,
    dyad_accepts_history_record h₂, two_loops_control⟩
  simp [dyadHistoryRecord, one_loop_insufficient]

/-! ## The prose linearization is false -/

/-- A model carrying both a scale ratio and a one-register memory dynamics. -/
structure ScaleMemoryModel where
  ratio : ℝ
  run : List Op → ℤ → ℤ

def ScaleAdequate (M : ScaleMemoryModel) : Prop :=
  NonCaptured M.ratio

def HistorySeparated (M : ScaleMemoryModel) : Prop :=
  ∀ k : ℤ, M.run h₁ k ≠ M.run h₂ k

/-- A non-captured scale living on the still-insufficient one-loop memory model. -/
noncomputable def phiOneLoopModel : ScaleMemoryModel where
  ratio := (1 + Real.sqrt 5) / 2
  run := runOne

theorem phiOneLoop_scale_adequate :
    ScaleAdequate phiOneLoopModel :=
  phi_non_captured

theorem phiOneLoop_history_not_separated :
    ¬ HistorySeparated phiOneLoopModel := by
  intro h
  exact h 0 (one_loop_insufficient 0)

/-- **Linear-route no-go:** scale non-capture alone does not force two-loop memory. -/
theorem scale_does_not_force_two_loop_memory :
    ¬ ∀ M : ScaleMemoryModel, ScaleAdequate M → HistorySeparated M := by
  intro h
  exact phiOneLoop_history_not_separated
    (h phiOneLoopModel phiOneLoop_scale_adequate)

/-! ## Full carried forcing DAG -/

/-- Typed bundle of every carried forcing edge, including the new topological and physical-scene
closures. -/
structure FullCarriedForcingDAG : Prop where
  comparison_to_memory :
    h₁ ≠ h₂
      ∧ dyadHistoryRecord h₁ = dyadHistoryRecord h₂
      ∧ runTwo h₁ (0, 0) ≠ runTwo h₂ (0, 0)
  memory_to_order :
    runTwo h₁ (0, 0) ≠ runTwo h₂ (0, 0)
      ∧ ¬ OrderEncoded (Multiplicative (ℤ × ℤ))
  order_to_scale :
    OrderEncoded (Equiv.Perm (Fin 3))
      ∧ (∀ r : ℝ,
          carrierRealizedRatio (Equiv.Perm (Fin 3)) r →
            ¬ NonCaptured r)
  order_to_closed_defect :
    OrderEncoded (Equiv.Perm (Fin 3))
      ∧ (∃ a b : Equiv.Perm (Fin 3), commDefect a b ≠ 1)
      ∧ ¬ (∀ g a b : Equiv.Perm (Fin 3),
          g * commDefect a b * g⁻¹ = commDefect a b)
      ∧ (∀ g x : Equiv.Perm (Fin 3),
          ConjClasses.mk (g * x * g⁻¹) = ConjClasses.mk x)
  closed_defect_to_shell :
    (∀ g : Equiv.Perm (Fin 3),
      ConjClasses.mk
          (g * commDefect defectGeneratorA defectGeneratorB * g⁻¹) =
        carriedClosedDefectCirculation.defect)
      ∧ carriedClosedDefectCirculation.cycle ≠ 0
      ∧ ¬ (∃ coeff : OpenTwoCells → ℤ,
          cellularBoundary openAttach coeff =
            carriedClosedDefectCirculation.cycle)
      ∧ (∃ coeff : ShellTwoCell → ℤ,
          cellularBoundary shellAttach coeff =
            carriedClosedDefectCirculation.cycle)
  shell_to_scene :
    Nonempty
      (FaithfulRepairSceneRepresentation
        torusShellScene RepairObservationQuotient)
      ∧ torusShellScene.zoneCount = 3
  scene_to_sizes :
    (repairClassZoneSize (repairClass discComparison),
      repairClassZoneSize (repairClass discOneLoop),
      repairClassZoneSize (repairClass discOrderMemory)) = (9, 11, 13)

/-- **All carried forcing edges are now machine-owned.** -/
theorem full_carried_forcing_dag : FullCarriedForcingDAG where
  comparison_to_memory :=
    ⟨dyad_comparison_collapses_histories.1,
      dyad_comparison_collapses_histories.2.1,
      dyad_comparison_collapses_histories.2.2.2.2⟩
  memory_to_order := chain_linked_four_five_to_five_six
  order_to_scale :=
    ⟨chain_linked_five_six_to_six_seven.1,
      chain_linked_five_six_to_six_seven.2.2.1⟩
  order_to_closed_defect := chain_linked_order_to_defect_closure
  closed_defect_to_shell :=
    ⟨topological_closure_forces_shell.1,
      topological_closure_forces_shell.2.1,
      topological_closure_forces_shell.2.2.1,
      topological_closure_forces_shell.2.2.2.1⟩
  shell_to_scene :=
    ⟨⟨torusShellSceneRepresentation⟩, torusShellScene_zoneCount⟩
  scene_to_sizes := repair_scene_sizes_selected_independently.1

/-- Capstone: the carried floors are genuine, the full forcing DAG exists, and the false linear
scale→memory route is excluded. -/
theorem cascade_full_forcing_synthesis :
    (∀ s ∈ carriedFloorsExtended,
      ¬ (s.ObligationBelow ↔ s.ObligationAbove))
      ∧ FullCarriedForcingDAG
      ∧ (¬ ∀ M : ScaleMemoryModel,
          ScaleAdequate M → HistorySeparated M) :=
  ⟨extended_floors_are_genuine,
   full_carried_forcing_dag,
   scale_does_not_force_two_loop_memory⟩

end D0.Foundation.CascadeFullForcingSynthesis
