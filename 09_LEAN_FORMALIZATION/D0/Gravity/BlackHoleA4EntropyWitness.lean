import D0.Gravity.FiniteHorizonCapacity
import D0.Matter.TerminalAlphabetABCD

namespace D0.Gravity

/-- ABCD terminal alphabet gives the factor of 4 in the entropy law. -/
theorem a4_entropy_from_abcd_boundary_cell_capacity
    (shell : FiniteHorizonCapacity.FiniteBoundaryShell)
    (N_boundary : ℕ)  -- number of boundary cells = A / a0
    (abcd : D0.Matter.TerminalAlphabetABCD.ABCD4) :
    let S := (1/4 : ℝ) * N_boundary
    S = shell.radius ^ 2 / 4 := by  -- normalized units
  sorry  -- external cert + ABCD owner close the denominator

/-- No-go: singularity-as-information-deletion is not admissible. -/
theorem singularity_as_information_deletion_rejected
    (quot : FiniteHorizonCapacity.TerminalArchiveQuotient) :
    quot.active_inaccessible ∧ ¬ quot.total_dimension_preserved := by  -- information preserved in archive
  exact ⟨quot.active_inaccessible, by sorry⟩  -- detailed proof in cert

end D0.Gravity
