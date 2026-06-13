import D0.Geometry.TorusCore13GeometryOrigin
import Mathlib.Tactic

namespace D0.Matter

/-- The finite D0 generation carrier. -/
abbrev GenCarrier : Type := Fin 3

/-- Terminal generation ordinal readout. -/
def generationOrdinalSelector : GenCarrier -> GenCarrier -> Int :=
  fun i j => if i = j then Int.ofNat i.val else 0

/-- Archive nearest-neighbour incidence on the ordered generation chain 0-1-2. -/
def generationAdjacencySelector : GenCarrier -> GenCarrier -> Int :=
  fun i j =>
    if (i.val + 1 = j.val) \/ (j.val + 1 = i.val) then 1 else 0

/-- Down-sector selector: terminal ordinal plus archive adjacency defect. -/
def generationDownSelector : GenCarrier -> GenCarrier -> Int :=
  fun i j => generationOrdinalSelector i j + generationAdjacencySelector i j

/-- Multiplication of generation selectors over the finite `Fin 3` carrier. -/
def matMul3 (A B : GenCarrier -> GenCarrier -> Int) :
    GenCarrier -> GenCarrier -> Int :=
  fun i k => Finset.univ.sum (fun j : GenCarrier => A i j * B j k)

/-- Commutator of two finite generation selectors. -/
def commutator3 (A B : GenCarrier -> GenCarrier -> Int) :
    GenCarrier -> GenCarrier -> Int :=
  fun i j => matMul3 A B i j - matMul3 B A i j

/-- The generation ordinal and adjacency selectors do not commute. -/
theorem generation_ordinal_adjacency_noncommute :
    commutator3 generationOrdinalSelector generationAdjacencySelector
      (0 : GenCarrier) (1 : GenCarrier) = -1 := by
  native_decide

/-- Therefore the up/down generation selectors are intrinsically noncommuting. -/
theorem generation_up_down_selectors_noncommute :
    commutator3 generationOrdinalSelector generationDownSelector
      (0 : GenCarrier) (1 : GenCarrier) = -1 := by
  native_decide

/-- Selector-level noncommutation on the finite generation carrier. -/
def SelectorsDoNotCommute
    (A B : GenCarrier -> GenCarrier -> Int) : Prop :=
  exists i j, commutator3 A B i j != 0

/-- The concrete D0 generation selectors have a nonzero commutator. -/
theorem generation_selectors_do_not_commute :
    SelectorsDoNotCommute generationOrdinalSelector generationDownSelector := by
  refine ⟨(0 : GenCarrier), (1 : GenCarrier), ?_⟩
  rw [generation_up_down_selectors_noncommute]
  norm_num

/-- Noncommuting generation selectors sourced by torus shell geometry. -/
def HasNonCommutingGenerationSelectors
    (A B : D0.Geometry.ShellMat) : Prop :=
  exists i j, D0.Geometry.commutator3 A B i j ≠ 0

/--
The D0 memory-torus shell geometry supplies the active noncommuting generation
selector source: radial hopping does not commute with phase/radius drift.
-/
theorem torus_geometry_forces_generation_selector_noncommute
    (T : D0.Geometry.TorusParameter) :
    HasNonCommutingGenerationSelectors
      D0.Geometry.radialAdjacency
      (D0.Geometry.phaseDrift T) := by
  refine ⟨(0 : D0.Geometry.Shell3), (1 : D0.Geometry.Shell3), ?_⟩
  exact D0.Geometry.radial_hopping_phase_drift_noncommute T

/-- Non-vacuous closure witness for the finite D0 generation selector origin. -/
structure GenerationSelectorOriginClosure where
  witness_row : GenCarrier
  witness_col : GenCarrier
  ordinal_adjacency_entry :
    commutator3 generationOrdinalSelector generationAdjacencySelector
      witness_row witness_col = -1
  up_down_entry :
    commutator3 generationOrdinalSelector generationDownSelector
      witness_row witness_col = -1
  selectors_noncommute :
    SelectorsDoNotCommute generationOrdinalSelector generationDownSelector
  torus_selector_source :
    forall T : D0.Geometry.TorusParameter,
      HasNonCommutingGenerationSelectors
        D0.Geometry.radialAdjacency
        (D0.Geometry.phaseDrift T)

/-- Concrete D0 generation selector origin closure. -/
def generationSelectorOriginClosure : GenerationSelectorOriginClosure where
  witness_row := 0
  witness_col := 1
  ordinal_adjacency_entry := generation_ordinal_adjacency_noncommute
  up_down_entry := generation_up_down_selectors_noncommute
  selectors_noncommute := generation_selectors_do_not_commute
  torus_selector_source := torus_geometry_forces_generation_selector_noncommute

end D0.Matter
