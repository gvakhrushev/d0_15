import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.BigOperators.Fin
import D0.Matter.ArchivePartialTrace
import D0.Geometry.ArchiveBianchiIdentity

open scoped BigOperators

namespace D0.Cosmology

theorem canonical_archive_density_is_uniform {V : Type} [Fintype V] [DecidableEq V] {n : ℕ} [NeZero n]
    (Γ_tot : Matrix (V × ZMod n) (V × ZMod n) ℝ)
    (h_comm : Γ_tot * (D0.Matter.kronecker_I_C (D0.Geometry.archiveShiftMatrix n)) = (D0.Matter.kronecker_I_C (D0.Geometry.archiveShiftMatrix n)) * Γ_tot) :
    ∃ c : ℝ, ∀ i : ZMod n, (D0.Matter.partialTraceV Γ_tot) i i = c := by
  exact D0.Matter.density_uniform_from_commute Γ_tot h_comm

theorem exact_generation_lift_trace {G : Type} [Fintype G] [DecidableEq G] {n : Nat}
    (Γ_SM : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ)
    (Γ_lift : Matrix (G × archivePhaseIndex n) (G × archivePhaseIndex n) ℝ)
    (h_lift : Γ_lift = D0.Spectrum.tensor_product_I Γ_SM)
    (h_zero : Matrix.trace Γ_SM = 0) :
    NeutralSource (D0.Matter.localTraceDensity (D0.Matter.partialTraceV Γ_lift)) := by
  exact D0.Matter.generation_trace_neutrality_connection Γ_SM Γ_lift h_lift h_zero

theorem canonical_seam_source_properties (n : Nat) (i : archivePhaseIndex (n+1)) :
    ∑ j : archivePhaseIndex n, seamCommutator n i j = 0 := by
  exact seamCommutator_row_sum_zero n i

end D0.Cosmology
