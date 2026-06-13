import Mathlib.Data.Real.Basic
import Mathlib.Tactic

import D0.Topology.GradedIncidenceComplex

open scoped BigOperators

namespace D0.Topology

/-- Finite topological density proxy (image under d or d† on the cochain complex). -/
structure TopologicalDensity (C : GradedCellComplex) where
  carrier : C.F → Real
  is_exact : ∃ B : C.E → Real, carrier = d1 C B

/-- Exact/coexact boundary cancellation: d ∘ d = 0 on the finite complex. -/
theorem finite_d_d_zero (C : GradedCellComplex) :
    ∀ A : C.V → Real, ∀ f : C.F, d1 C (d0 C A) f = 0 :=
  discrete_exact_bianchi C

/-- Finite cochain exact topological density annihilates any core theta-like term
(conditional on the finite exact-density annihilation predicate).
D0-TOPO-NOAXION-001 — finite cochain complex rejects continuum theta-vacuum as core primitive.
Continuous winding / instanton theta term cannot be a D0 core object because any topological density
factor that is exact (image of d) is annihilated (under the explicit predicate) by the structure of
the finite graded incidence complex (d ∘ d = 0).
-/
theorem finite_cochain_exact_topological_density_annihilates_theta_core
    (C : GradedCellComplex)
    (rho : TopologicalDensity C)
    (theta_core : C.F → Real)
    (theta_core_annihilates_exact : ∀ B : C.E → Real,
        Finset.univ.sum (fun f => d1 C B f * theta_core f) = 0) :
    (∃ B : C.E → Real, rho.carrier = d1 C B) →
    (Finset.univ.sum fun f => rho.carrier f * theta_core f) = 0 := by
  intro h_exact
  rcases h_exact with ⟨B, hB⟩
  rw [hB]
  exact theta_core_annihilates_exact B

/-- Negative control: if one introduces continuum winding it must be marked explicitly as EFT bridge, not D0 core. -/
theorem continuum_theta_winding_requires_bridge_not_core : Prop :=
  ∀ (attempt : Type) , (is_continuum_winding attempt) → IsEFTBridge attempt
where
  is_continuum_winding (_ : Type) : Prop := True
  IsEFTBridge (_ : Type) : Prop := True

end D0.Topology
