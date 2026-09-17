import Mathlib.Data.Fintype.Card
import D0.Matter.RepresentationCarrier

namespace D0.Matter

def gaugeChargesRepWithGenerations (R : MatterRep) : RepWithGenerations R → ℚ :=
  fun g => R.gaugeCharges g.2

def replicateOverGenerationIndex {C : Type} (f : C → ℚ) : (GenerationIndex × C) → ℚ :=
  fun g => f g.2

theorem generation_index_does_not_change_gauge_charge (R : MatterRep) :
  gaugeChargesRepWithGenerations R = replicateOverGenerationIndex R.gaugeCharges := by
  rfl

theorem matter_rep_generation_multiplicity_three :
  Fintype.card GenerationIndex = 3 := by
  exact D0.Defect.branchRay_card

theorem rep_with_generations_card (R : MatterRep) :
  Fintype.card (RepWithGenerations R) = 3 * Fintype.card R.carrier := by
  have h : Fintype.card (RepWithGenerations R) = Fintype.card GenerationIndex * Fintype.card R.carrier := Fintype.card_prod _ _
  rw [h, matter_rep_generation_multiplicity_three]

end D0.Matter
