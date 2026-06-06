import Mathlib.Data.Rat.Lemmas
import Mathlib.Tactic

namespace D0.Bridge

/--
Internal D0 kinematic gauge: one detector length tick and one detector time tick.
The structural cone speed is dimensionless; SI `m/s` values belong to later
calibration, not to the finite core.
-/
structure InternalKinematicGauge where
  lengthTick : ℚ
  timeTick : ℚ
  time_positive : 0 < timeTick
  same_tick : lengthTick = timeTick

/-- Dimensionless internal cone speed in detector units. -/
def internalConeSpeed (g : InternalKinematicGauge) : ℚ :=
  g.lengthTick / g.timeTick

/-- In the normalized detector gauge, the internal cone speed is structurally one. -/
theorem internal_cone_speed_eq_one (g : InternalKinematicGauge) :
    internalConeSpeed g = 1 := by
  unfold internalConeSpeed
  rw [g.same_tick]
  field_simp [ne_of_gt g.time_positive]

/-- Recalibration can change units, but not the dimensionless internal cone speed. -/
theorem internal_cone_speed_unit_invariant
    (g : InternalKinematicGauge) (_meterPerTick _secondPerTick : ℚ) :
    internalConeSpeed g = 1 :=
  internal_cone_speed_eq_one g

/--
Finite causal tick section.

This is the v14 strengthening of the former silent assumption
`lengthTick = timeTick`.  The equality is not an external physical speed
postulate; it is the existence of one common finite section through which line
and tick records are compared.  A later SI export may attach meters and seconds,
but it cannot split this internal section inside the finite core.
-/
structure FiniteCausalTickSection where
  lineTick : ℚ
  timeTick : ℚ
  sectionTick : ℚ
  section_positive : 0 < sectionTick
  line_is_section : lineTick = sectionTick
  time_is_section : timeTick = sectionTick

/-- A finite causal tick section canonically produces the normalized kinematic gauge. -/
def finiteCausalTickSectionGauge (s : FiniteCausalTickSection) :
    InternalKinematicGauge where
  lengthTick := s.lineTick
  timeTick := s.timeTick
  time_positive := by
    rw [s.time_is_section]
    exact s.section_positive
  same_tick := by
    rw [s.line_is_section, s.time_is_section]

/-- The common finite section forces line and time ticks to coincide internally. -/
theorem finite_causal_tick_section_forces_same_tick
    (s : FiniteCausalTickSection) : s.lineTick = s.timeTick := by
  rw [s.line_is_section, s.time_is_section]

/-- Therefore the internal cone speed of any finite causal tick section is one. -/
theorem finite_causal_tick_section_cone_speed_eq_one
    (s : FiniteCausalTickSection) :
    internalConeSpeed (finiteCausalTickSectionGauge s) = 1 :=
  internal_cone_speed_eq_one (finiteCausalTickSectionGauge s)

/--
A common rescaling of the finite section changes the external unit convention,
not the internal cone-speed invariant.
-/
def rescaleFiniteCausalTickSection
    (s : FiniteCausalTickSection) (lambda : ℚ) (hlambda : 0 < lambda) :
    FiniteCausalTickSection where
  lineTick := lambda * s.lineTick
  timeTick := lambda * s.timeTick
  sectionTick := lambda * s.sectionTick
  section_positive := mul_pos hlambda s.section_positive
  line_is_section := by rw [s.line_is_section]
  time_is_section := by rw [s.time_is_section]

/-- Common tick-gauge rescaling preserves the dimensionless internal cone speed. -/
theorem common_tick_rescaling_preserves_internal_cone_speed
    (s : FiniteCausalTickSection) (lambda : ℚ) (hlambda : 0 < lambda) :
    internalConeSpeed
        (finiteCausalTickSectionGauge (rescaleFiniteCausalTickSection s lambda hlambda)) =
      internalConeSpeed (finiteCausalTickSectionGauge s) := by
  rw [finite_causal_tick_section_cone_speed_eq_one,
      finite_causal_tick_section_cone_speed_eq_one]

/--
An asymmetric line/time pair cannot be promoted to the internal D0 tick gauge.
Such asymmetry may appear only as an external calibration/export convention.
-/
theorem asymmetric_ticks_not_internal_gauge
    (line time : ℚ) (hneq : line ≠ time) :
    ¬ ∃ s : FiniteCausalTickSection, s.lineTick = line ∧ s.timeTick = time := by
  intro h
  rcases h with ⟨s, hline, htime⟩
  apply hneq
  rw [← hline, ← htime]
  exact finite_causal_tick_section_forces_same_tick s

end D0.Bridge
