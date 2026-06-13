import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.Ring
import D0.Matter.GenerationMultiplicity

open scoped BigOperators

namespace D0.Matter

noncomputable def anomalySumGen (R : MatterRep) (f : ℚ → ℚ) : ℚ :=
  ∑ x : R.carrier, f (R.gaugeCharges x)

noncomputable def anomalySumRepWithGenerations (R : MatterRep) (f : ℚ → ℚ) : ℚ :=
  ∑ x : RepWithGenerations R, f (gaugeChargesRepWithGenerations R x)

theorem anomaly_sum_triples (R : MatterRep) (f : ℚ → ℚ) :
  anomalySumRepWithGenerations R f = 3 * anomalySumGen R f := by
  unfold anomalySumRepWithGenerations anomalySumGen gaugeChargesRepWithGenerations RepWithGenerations
  -- Goal: ∑ x : GenerationIndex × R.carrier, f (R.gaugeCharges x.2) = 3 * ∑ x : R.carrier, f (R.gaugeCharges x)
  -- Step 1: expand product sum via Finset.univ_product_univ + Finset.sum_product
  rw [← Finset.univ_product_univ, Finset.sum_product]
  dsimp only
  -- Step 3: outer sum of a constant = card • constant
  rw [Finset.sum_const, Finset.card_univ, matter_rep_generation_multiplicity_three,
      nsmul_eq_mul]
  -- Step 4: ↑(3 : ℕ) * S = (3 : ℚ) * S
  norm_cast

theorem anomaly_zero_preserved (R : MatterRep) (f : ℚ → ℚ)
  (h : anomalySumGen R f = 0) :
  anomalySumRepWithGenerations R f = 0 := by
  rw [anomaly_sum_triples, h, mul_zero]

end D0.Matter
