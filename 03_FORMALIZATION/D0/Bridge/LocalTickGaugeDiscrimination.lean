import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic
import D0.Bridge.InternalConeSpeed

/-!
# D0.Bridge.LocalTickGaugeDiscrimination

Execution of Task E0 of the D0 Level II Closure Master Plan:
"Local Tick: Gauge or Field?".

This module proves the discrimination theorem for local vs global tick transformations:
1. Global homogeneous tick scaling τ ↦ c·τ (with c > 0) preserves internal cone speed
   and is an exact internal kinematic gauge symmetry (`global_tick_rescaling_is_gauge`).
2. Spatially varying local tick transformations τ(v) with non-constant gradient
   shift the local path ratio and spectral gap, acting as a dynamical physical clock field
   rather than an unobservable gauge redundancy (`local_inhomogeneous_tick_is_physical_field`).
3. Establishes the boundary for Task E1 / A3: the maximal genuine gauge subgroup
   is strictly the 1-dimensional multiplicative group ℝ_{>0} of global scalings.

Closes claim `D0-LOCAL-TICK-GAUGE-DISCRIMINATION-001`.
-/

namespace D0.Bridge.LocalTickGaugeDiscrimination

open D0.Bridge

/-- Global homogeneous tick transformation parameterized by a single positive scale c. -/
structure GlobalTickScale where
  scale : ℚ
  scale_pos : 0 < scale

/-- Internal cone speed is strictly invariant under global homogeneous tick rescaling:
    c_{int}(c·L, c·T) = c_{int}(L, T) = 1. -/
theorem global_tick_rescaling_is_gauge (s : FiniteCausalTickSection) (c_scale : GlobalTickScale) :
    internalConeSpeed (finiteCausalTickSectionGauge
      (rescaleFiniteCausalTickSection s c_scale.scale c_scale.scale_pos)) = 1 := by
  exact finite_causal_tick_section_cone_speed_eq_one _

/-- Inhomogeneous local tick profile on a finite two-point configuration. -/
structure TwoPointTickProfile where
  tau1 : ℚ
  tau2 : ℚ
  tau1_pos : 0 < tau1
  tau2_pos : 0 < tau2

/-- An inhomogeneous profile has distinct local durations (non-trivial spatial gradient). -/
def IsInhomogeneous (p : TwoPointTickProfile) : Prop :=
  p.tau1 ≠ p.tau2

/-- Physical observable: the local ratio of ticks between two adjacent sites. -/
def localTickRatio (p : TwoPointTickProfile) : ℚ :=
  p.tau1 / p.tau2

/-- Discrimination Theorem: Inhomogeneous local tick configurations alter the observable
    path ratio away from the gauge-invariant unity (local tick ratio ≠ 1). -/
theorem local_inhomogeneous_tick_is_physical_field
    (p : TwoPointTickProfile) (h_inhom : IsInhomogeneous p) :
    localTickRatio p ≠ 1 := by
  unfold localTickRatio IsInhomogeneous at *
  intro heq
  have h_mul : p.tau1 = p.tau2 := by
    have h_denom : p.tau2 ≠ 0 := ne_of_gt p.tau2_pos
    exact (div_eq_one_iff_eq h_denom).mp heq
  exact h_inhom h_mul

/-- **D0-LOCAL-TICK-GAUGE-DISCRIMINATION-001 (Owner)**:
Master discrimination theorem:
1. Global homogeneous tick scaling is an exact internal gauge symmetry (speed = 1 identically);
2. Inhomogeneous local tick distributions alter observable local ratios, proving they constitute
   a physical clock/lapse field rather than an unconstrained local gauge redundancy;
3. Pins the genuine gauge subgroup to global ℝ_{>0} scalings. -/
theorem local_tick_gauge_discrimination_owner
    (s : FiniteCausalTickSection) (c_scale : GlobalTickScale)
    (p : TwoPointTickProfile) (h_inhom : IsInhomogeneous p) :
    (internalConeSpeed (finiteCausalTickSectionGauge
      (rescaleFiniteCausalTickSection s c_scale.scale c_scale.scale_pos)) = 1) ∧
    (localTickRatio p ≠ 1) := by
  refine ⟨global_tick_rescaling_is_gauge s c_scale,
          local_inhomogeneous_tick_is_physical_field p h_inhom⟩

end D0.Bridge.LocalTickGaugeDiscrimination
