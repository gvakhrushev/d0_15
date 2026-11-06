import Mathlib.Data.Real.Basic
import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import D0.Geometry.ArchiveCubicalCochainCarrier

namespace D0.Geometry

open D0

/-!
# D0.Geometry.ArchiveMetricMeasureHodgeLift

Owner: `D0-ARCHIVE-METRIC-MEASURE-HODGE-LIFT-001`.

Candidate metric-measure Hodge-weight family on cell degree `k`:
`W_k = mu^(1-k) * prod_c`. Its exponent is defined for each natural-number
degree. The compiled owner below checks the degree-0 and degree-1 endpoint
identities and the finite carrier cardinalities. The formula's uniqueness,
positivity conditions, and its claimed reduction from the frozen tensor
refinement weights are not derived in this file.
-/

/-- Power exponent of scalar density μ in the Hodge weight of degree k: 1 - k. -/
def muExponent (k : ℕ) : ℤ := 1 - (k : ℤ)

theorem mu_exponent_0 : muExponent 0 = 1 := rfl
theorem mu_exponent_1 : muExponent 1 = 0 := rfl
theorem mu_exponent_4 : muExponent 4 = -3 := rfl

/-- Candidate grade-k Hodge weight for real arguments mu and prod_c. This definition imposes no positivity condition. -/
noncomputable def hodgeMetricMeasureWeight (k : ℕ) (mu : ℝ) (prod_c : ℝ) : ℝ :=
  (mu ^ (muExponent k)) * prod_c

theorem hodge_weight_0_eq_mu (mu : ℝ) :
    hodgeMetricMeasureWeight 0 mu 1 = mu := by
  unfold hodgeMetricMeasureWeight muExponent
  simp [zpow_one]

theorem hodge_weight_1_eq_conductance (mu c_r : ℝ) :
    hodgeMetricMeasureWeight 1 mu c_r = c_r := by
  unfold hodgeMetricMeasureWeight muExponent
  simp

/-- Current compiled owner result: the degree-0 and degree-1 endpoint
identities hold for real inputs, and the two finite carrier cardinalities are
16 and 4. This result does not establish a unique metric across all grades
or a reduction from frozen refinement weights. -/
theorem archive_metric_measure_hodge_lift_owner (mu c_r : ℝ) :
    (hodgeMetricMeasureWeight 0 mu 1 = mu) ∧
    (hodgeMetricMeasureWeight 1 mu c_r = c_r) ∧
    (Fintype.card CubicalCellType = 16) ∧
    (Fintype.card Role = 4) :=
  ⟨hodge_weight_0_eq_mu mu, hodge_weight_1_eq_conductance mu c_r, card_archive_fock_state, card_role⟩

end D0.Geometry
