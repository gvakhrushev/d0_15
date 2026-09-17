import D0.Phi

namespace D0

def D0ResponseRoot (x : Real) : Prop :=
  0 < x ∧ x + x^2 = 1

theorem unique_D0_response_root :
    ∃! x : Real, D0ResponseRoot x := by
  refine ⟨p, ⟨p_positive, p_unit_closure⟩, ?_⟩
  intro y hy
  exact p_unique_positive y hy.1 hy.2

noncomputable def D0PhaseGenerator : Real := p^2

theorem D0PhaseGenerator_eq_phi_inv_sq :
    D0PhaseGenerator = phi^(-2 : Int) := by
  simp [D0PhaseGenerator, p]
  rfl

theorem D0_response_forces_phase_generator
    (x : Real) (hx : D0ResponseRoot x) :
    x^2 = D0PhaseGenerator := by
  have hxeq : x = p := p_unique_positive x hx.1 hx.2
  rw [hxeq]
  rfl

end D0
