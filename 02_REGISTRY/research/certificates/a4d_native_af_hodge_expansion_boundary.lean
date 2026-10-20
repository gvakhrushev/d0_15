import D0.Geometry.ArchiveHodgeCARDiracSquare
import D0.Geometry.ArchivePhaseEdgeMetricScale

namespace D0.Research.NativeAFHodgeExpansionBoundary

open D0.Geometry
open D0.Geometry.ArchivePhaseEdgeMetricScale

/-- The actual forward/backward Hodge difference coefficient is the inverse
square of the owned phase edge length, for every archive size. -/
theorem actual_hodge_scale_matches_phase_metric (N : ℕ) :
    forwardDifferenceScale N ^ 2 * phaseEdgeMetricLength N ^ 2 = 1 := by
  rw [← metric_scale_eq_inverse_square_edge_length]
  rfl

/-- The Dirac square uses the very same scaled differences on every cochain
component; no second coefficient is introduced at the heat readout. -/
theorem actual_hodge_square_is_owned_scaled_laplacian
    (N : ℕ) (ψ : ArchiveCochain N) :
    hodgeCarDirac N (hodgeCarDirac N ψ) = cochainDifferenceLaplacian N ψ := by
  exact hodgeCarDirac_sq N ψ

end D0.Research.NativeAFHodgeExpansionBoundary

#print D0.Research.NativeAFHodgeExpansionBoundary.actual_hodge_scale_matches_phase_metric
#print axioms D0.Research.NativeAFHodgeExpansionBoundary.actual_hodge_scale_matches_phase_metric
#print D0.Research.NativeAFHodgeExpansionBoundary.actual_hodge_square_is_owned_scaled_laplacian
#print axioms D0.Research.NativeAFHodgeExpansionBoundary.actual_hodge_square_is_owned_scaled_laplacian
