import D0.Bridge.InternalConeSpeed
import D0.Algebra.LorentzNoGo

namespace D0.Bridge

/--
Finite Lorentz/tick-gauge closure.

The finite core closes two independent facts before any smooth Lorentz bridge is
exported: one causal tick section fixes the dimensionless cone speed, and the
terminal role signature is `(1,3)`.  Smooth boosts, SI meters/seconds and
laboratory clocks are bridge exports after this finite closure.
-/
structure FiniteLorentzTickGaugeClosure where
  tickSection : FiniteCausalTickSection
  signature_closed : D0.roleSignature = (1, 3) := D0.roleSignature_eq_1_3

/-- The finite tick section closes the internal cone speed before SI export. -/
theorem finite_lorentz_tick_gauge_cone_speed_closed
    (C : FiniteLorentzTickGaugeClosure) :
    internalConeSpeed (finiteCausalTickSectionGauge C.tickSection) = 1 :=
  finite_causal_tick_section_cone_speed_eq_one C.tickSection

/-- The same closure fixes the Lorentz-facing terminal signature `(1,3)`. -/
theorem finite_lorentz_tick_gauge_signature_closed
    (_C : FiniteLorentzTickGaugeClosure) :
    D0.roleSignature = (1, 3) :=
  D0.roleSignature_eq_1_3

/-- Euclidean `(4,0)` cannot be obtained by a tick-gauge export of the D0 core. -/
theorem finite_lorentz_tick_gauge_no_euclidean_export
    (_C : FiniteLorentzTickGaugeClosure) :
    D0.roleSignature ≠ (4, 0) :=
  D0.no_euclidean_SO4

/-- Split `(2,2)` cannot be obtained by a tick-gauge export of the D0 core. -/
theorem finite_lorentz_tick_gauge_no_split_export
    (_C : FiniteLorentzTickGaugeClosure) :
    D0.roleSignature ≠ (2, 2) :=
  D0.no_split_SO22

/--
Common rescaling of line/tick units cannot change either the internal speed or
the Lorentz-facing role signature.
-/
theorem finite_lorentz_tick_rescaling_preserves_closure
    (C : FiniteLorentzTickGaugeClosure) (lambda : ℚ) (hlambda : 0 < lambda) :
    internalConeSpeed
        (finiteCausalTickSectionGauge
          (rescaleFiniteCausalTickSection C.tickSection lambda hlambda)) = 1 ∧
      D0.roleSignature = (1, 3) := by
  exact ⟨finite_causal_tick_section_cone_speed_eq_one _, D0.roleSignature_eq_1_3⟩

end D0.Bridge
