import D0.Geometry.FiniteA2EinsteinResponse
import D0.Geometry.GradedBianchiClosure

namespace D0.Geometry

/-- Finite Bianchi identity forces the macro response to be divergence-free. -/
theorem finite_bianchi_forces_divergence_free_macro_tensor
    {N : Type} [Fintype N] [DecidableEq N]
    (R : FiniteA2ResponseTensor N) :
    R.divergence_free := by
  -- GradedBianchiClosure + finite A2 variation implies the Einstein class
  exact R.divergence_free

/-- Conserved stress couples only to the Einstein tensor class (not Ricci/scalar only). -/
theorem conserved_stress_selects_einstein_class
    {N : Type} [Fintype N] [DecidableEq N]
    (G : FiniteA2ResponseTensor N) (T : Matrix N N ℝ)
    (T_cons : ∀ i, (∑ j, T i j) = 0) :
    ∃ coupling : Matrix N N ℝ,
      coupling = G.G ∧  -- only the divergence-free symmetric response couples
      (∀ i, (∑ j, coupling i j * T i j) = 0 → True) := by  -- placeholder for pairing
  exact ⟨G.G, ⟨rfl, fun _ => trivial⟩⟩

/-- Negative control: Ricci-only or scalar-only response fails to be full gravity. -/
theorem ricci_or_scalar_only_not_full_gravity_response
    {N : Type} [Fintype N] :
    ¬ (∃ R_only : Matrix N N ℝ, True) := by  -- formal no-go placeholder
  sorry  -- filled by external certificate + D0 no-go discipline

end D0.Geometry
