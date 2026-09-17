import Mathlib.Tactic

namespace D0.Physics

/-!
D0-QUASI-002 acceptance-window owner.

A centered finite archive window keeps inversion symmetry.  A nonzero archive
offset gives a concrete left/right asymmetric readout witness.
-/

structure AcceptanceWindow where
  center : Rat
  radius : Rat
  radius_nonnegative : 0 <= radius

def AcceptanceWindow.contains (W : AcceptanceWindow) (x : Rat) : Prop :=
  W.center - W.radius <= x /\ x <= W.center + W.radius

def Centered (W : AcceptanceWindow) : Prop :=
  W.center = 0

def InversionSymmetric (W : AcceptanceWindow) : Prop :=
  forall x : Rat, W.contains x <-> W.contains (-x)

def ChiralReadout (W : AcceptanceWindow) : Prop :=
  exists x : Rat, W.contains x /\ Not (W.contains (-x))

theorem centered_window_has_parity
    (W : AcceptanceWindow) (hcenter : Centered W) :
    InversionSymmetric W := by
  intro x
  unfold AcceptanceWindow.contains Centered at *
  constructor
  · intro hx
    constructor <;> linarith
  · intro hx
    constructor <;> linarith

theorem offset_window_breaks_parity_witness
    (W : AcceptanceWindow) (hoffset : W.center ≠ 0) :
    ChiralReadout W := by
  unfold ChiralReadout
  by_cases hpos : 0 < W.center
  · use W.center + W.radius
    constructor
    · unfold AcceptanceWindow.contains
      constructor <;> linarith [W.radius_nonnegative]
    · intro hneg
      have hlow : W.center - W.radius <= -(W.center + W.radius) := hneg.1
      linarith
  · have hle : W.center <= 0 := le_of_not_gt hpos
    have hnegc : W.center < 0 := lt_of_le_of_ne hle hoffset
    use W.center - W.radius
    constructor
    · unfold AcceptanceWindow.contains
      constructor <;> linarith [W.radius_nonnegative]
    · intro hneg
      have hhigh : -(W.center - W.radius) <= W.center + W.radius := hneg.2
      linarith

def unitOffsetWindow : AcceptanceWindow where
  center := 1
  radius := 0
  radius_nonnegative := by norm_num

theorem window_offset_forces_chiral_readout :
    ChiralReadout unitOffsetWindow := by
  exact offset_window_breaks_parity_witness unitOffsetWindow (by
    intro h
    norm_num [unitOffsetWindow] at h)

end D0.Physics
