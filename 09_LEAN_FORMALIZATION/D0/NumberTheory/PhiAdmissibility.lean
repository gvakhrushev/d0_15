import D0.NumberTheory.PhiContinuedFraction

namespace D0

theorem D0_admissible_rotation_unique :
    ∃! theta : Real, ∃ x : Real, D0ResponseRoot x ∧ theta = x^2 := by
  refine ⟨D0PhaseGenerator, ?_, ?_⟩
  · exact ⟨p, ⟨p_positive, p_unit_closure⟩, rfl⟩
  · intro theta htheta
    rcases htheta with ⟨x, hx, rfl⟩
    exact D0_response_forces_phase_generator x hx

end D0

