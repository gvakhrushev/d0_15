import Mathlib.Tactic

namespace D0.Physics

/-!
D0-QUASI-002 phason-flip inertia owner.

The finite inertia proxy is the rewrite count forced by a phason membership
change under accelerated defect transport.
-/

structure MovingDefect where
  flipTick : Option Nat

def PhasonFlipCount (p : MovingDefect) (n : Nat) : Nat :=
  match p.flipTick with
  | none => 0
  | some k => if k < n then 1 else 0

def InertialCost (p : MovingDefect) (n : Nat) : Nat :=
  PhasonFlipCount p n

def NonzeroAcceleration (p : MovingDefect) : Prop :=
  p.flipTick.isSome

theorem acceleration_requires_nonzero_flip_count
    (p : MovingDefect) (hacc : NonzeroAcceleration p) :
    exists n : Nat, 0 < PhasonFlipCount p n := by
  cases h : p.flipTick with
  | none =>
      unfold NonzeroAcceleration at hacc
      simp [h] at hacc
  | some k =>
      use k + 1
      unfold PhasonFlipCount
      simp [h]

theorem inertial_cost_lower_bound
    (p : MovingDefect) (hacc : NonzeroAcceleration p) :
    exists n : Nat, 0 < InertialCost p n := by
  rcases acceleration_requires_nonzero_flip_count p hacc with ⟨n, hn⟩
  exact ⟨n, hn⟩

theorem phason_flip_drag_positive_cost
    (p : MovingDefect) (hacc : NonzeroAcceleration p) :
    exists n : Nat, 0 < InertialCost p n := by
  exact inertial_cost_lower_bound p hacc

end D0.Physics
