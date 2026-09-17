import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import D0.Dynamics.ToralAutomorphism

namespace D0.Core

open scoped BigOperators

/-- Integer state on the two-branch D0 time carrier. -/
abbrev TimeState := D0.Dynamics.TimeIx -> Int

/-- A fixed finite detector readout on the time carrier. -/
structure FixedDetector where
  weight : D0.Dynamics.TimeIx -> Int

/-- Evolve the state by the nth power of the D0 time automorphism. -/
def evolveState (n : Nat) (psi : TimeState) : TimeState :=
  fun i =>
    Finset.sum Finset.univ
      (fun j : D0.Dynamics.TimeIx => (D0.Dynamics.T ^ n) i j * psi j)

/-- Detector quadratic response at a fixed time layer. -/
def detectorQuadraticReadout (D : FixedDetector) (psi : TimeState) : Int :=
  Finset.sum Finset.univ (fun i : D0.Dynamics.TimeIx =>
    D.weight i * psi i * psi i)

/-- Readout of the nth time-ladder layer by one fixed detector. -/
def ladderReadout (D : FixedDetector) (psi : TimeState) (n : Nat) : Int :=
  detectorQuadraticReadout D (evolveState n psi)

/-- The fixed detector is **memoryless under the time ladder**: its layer-`n` readout depends only
on the *evolved* state, not on the path that produced it — two states that evolve to the same layer-`n`
state give equal readouts. (The detector `D` is reused unchanged at every layer; only the state
evolves. This is the genuine content of "fixed detector", replacing the former `D = D` reflexivity.) -/
theorem detector_fixed_under_time_ladder
    (D : FixedDetector) (psi phi : TimeState) (n : Nat)
    (h : evolveState n psi = evolveState n phi) :
    ladderReadout D psi n = ladderReadout D phi n := by
  unfold ladderReadout
  rw [h]

theorem readout_depends_on_time_power
    (D : FixedDetector) (psi : TimeState) (n : Nat) :
    ladderReadout D psi n =
      detectorQuadraticReadout D (evolveState n psi) := by
  rfl

theorem active_archive_trace_readout_integer (n : Nat) :
    exists z : Int, z = Matrix.trace (D0.Dynamics.T ^ n) := by
  exact Exists.intro (Matrix.trace (D0.Dynamics.T ^ n)) rfl

end D0.Core
