import Mathlib.Tactic
import Mathlib.Data.Finset.Card

namespace D0.Physics

/-!
D0-QUASI-002 fractional window-weight owner.

The three archive/color sectors give one-sector and two-sector readout weights
`1/3` and `2/3`; the sign branch supplies the two charge signs.
-/

inductive ColorSector where
  | c0
  | c1
  | c2
deriving DecidableEq, Repr

inductive SignBranch where
  | plus
  | minus
deriving DecidableEq, Repr

def WindowWeight (S : Finset ColorSector) : Rat :=
  S.card / 3

def SignedWindowWeight (sg : SignBranch) (S : Finset ColorSector) : Rat :=
  match sg with
  | SignBranch.plus => WindowWeight S
  | SignBranch.minus => -WindowWeight S

def FractionalChargeValue (q : Rat) : Prop :=
  q = (-2) / 3 \/ q = (-1) / 3 \/ q = 1 / 3 \/ q = 2 / 3

theorem single_sector_weight_eq_one_third
    (S : Finset ColorSector) (h : S.card = 1) :
    WindowWeight S = 1 / 3 := by
  simp [WindowWeight, h]

theorem double_sector_weight_eq_two_thirds
    (S : Finset ColorSector) (h : S.card = 2) :
    WindowWeight S = 2 / 3 := by
  simp [WindowWeight, h]

theorem signed_window_charge_values
    (sg : SignBranch) (S : Finset ColorSector)
    (h : S.card = 1 \/ S.card = 2) :
    FractionalChargeValue (SignedWindowWeight sg S) := by
  rcases h with hcard | hcard <;> cases sg
  · right; right; left
    norm_num [SignedWindowWeight, single_sector_weight_eq_one_third S hcard]
  · right; left
    norm_num [SignedWindowWeight, single_sector_weight_eq_one_third S hcard]
  · right; right; right
    norm_num [SignedWindowWeight, double_sector_weight_eq_two_thirds S hcard]
  · left
    norm_num [SignedWindowWeight, double_sector_weight_eq_two_thirds S hcard]

theorem neutral_triple_window_sum_cancels :
    (1 / 3 : Rat) + 1 / 3 + 1 / 3 - 1 = 0 := by
  norm_num

theorem fractional_charge_window_weights :
    (forall S : Finset ColorSector,
      S.card = 1 -> WindowWeight S = 1 / 3) /\
    (forall S : Finset ColorSector,
      S.card = 2 -> WindowWeight S = 2 / 3) := by
  constructor
  · exact single_sector_weight_eq_one_third
  · exact double_sector_weight_eq_two_thirds

end D0.Physics
