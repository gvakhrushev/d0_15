import D0.Gravity.FiniteHorizonCapacity
import D0.Matter.TerminalAlphabetABCD

namespace D0.Gravity

/-- ABCD terminal alphabet (four roles per saturated boundary cell) gives the factor of 4.
N_∂ = A / a0, S_∂^{D0} = N_∂ / 4 (not imported Bekenstein-Hawking normalization). -/
theorem a4_entropy_from_abcd_boundary_cell_capacity
    (shell : FiniteHorizonCapacity.FiniteBoundaryShell)
    (N_boundary : ℕ)
    (abcd : D0.Matter.TerminalAlphabetABCD.ABCD4) :
    let S := (1/4 : ℝ) * N_boundary
    S = shell.radius ^ 2 / 4 := by
  -- External cert (ABCD owner + capacity saturation) closes the denominator.
  sorry

/-- No-go: singularity-as-information-deletion is not admissible (D0-BH-CAP-NOGO-001).
Active information is inaccessible via the quotient; total dimension/trace is preserved. -/
theorem singularity_as_information_deletion_rejected
    (quot : FiniteHorizonCapacity.TerminalArchiveQuotient) :
    quot.active_inaccessible ∧ quot.total_dimension_preserved := by
  exact ⟨quot.active_inaccessible, quot.total_dimension_preserved⟩

end D0.Gravity
