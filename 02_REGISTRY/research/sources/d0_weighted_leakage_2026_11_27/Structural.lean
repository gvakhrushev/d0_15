import Mathlib.Tactic
import D0.Geometry.ArchiveRolePhaseProductCarrier
import D0.Geometry.ArchiveCARRelations

/-!
This file gives an exact weighted-exterior obstruction on two declared scopes:
(1) a formula and a local varying-neighbour criterion for two commuting shifts;
(2) a full four-role CAR operator on the actual archive carrier at depth 0.
It does not prove a no-go at arbitrary depth or that Hodge weighting is the
only alternative.  See `RESULT_STRUCTURAL_RU.md` for the precise boundary.
-/

namespace WeightedLeakageGeneral

variable {X : Type}

def diff (shift : X → X) (f : X → ℚ) (x : X) : ℚ := f (shift x) - f x

def weightedSquare (sx sy : X → X) (s f : X → ℚ) (x : X) : ℚ :=
  s x * (diff sx (fun y => s y * diff sy f y) x -
         diff sy (fun y => s y * diff sx f y) x)

theorem weighted_square_formula (sx sy : X → X) (s f : X → ℚ)
    (x : X) (hcomm : sy (sx x) = sx (sy x)) :
    weightedSquare sx sy s f x =
      s x * ((s (sx x) - s (sy x)) * f (sx (sy x)) +
             (s (sy x) - s x) * f (sy x) +
             (s x - s (sx x)) * f (sx x)) := by
  simp only [weightedSquare, diff, hcomm]
  ring

def delta [DecidableEq X] (p x : X) : ℚ := if x = p then 1 else 0

theorem weighted_square_probe [DecidableEq X] (sx sy : X → X) (s : X → ℚ) (x : X)
    (hcomm : sy (sx x) = sx (sy x))
    (hdiagonal : sx (sy x) ≠ sx x) (hdirections : sy x ≠ sx x) :
    weightedSquare sx sy s (delta (sx x)) x = s x * (s x - s (sx x)) := by
  rw [weighted_square_formula sx sy s _ x hcomm]
  simp [delta, hdiagonal, hdirections]

theorem weighted_square_ne_zero_of_varying_neighbor [DecidableEq X]
    (sx sy : X → X) (s : X → ℚ) (x : X)
    (hcomm : sy (sx x) = sx (sy x))
    (hdiagonal : sx (sy x) ≠ sx x) (hdirections : sy x ≠ sx x)
    (hnonzero : s x ≠ 0) (hvar : s x ≠ s (sx x)) :
    weightedSquare sx sy s (delta (sx x)) x ≠ 0 := by
  rw [weighted_square_probe sx sy s x hcomm hdiagonal hdirections]
  exact mul_ne_zero hnonzero (sub_ne_zero.mpr hvar)

end WeightedLeakageGeneral

namespace TypedArchiveLeakage

open D0
open D0.Geometry
open D0.Geometry.ArchiveRolePhaseProductCarrier
open WeightedLeakageGeneral

abbrev Site := ArchiveRolePhasePoint 0

def flip (a : Fin 2) : Fin 2 := if a = 0 then 1 else 0

def shiftA (x : Site) (r : Role) : Fin 2 := if r = A then flip (x r) else x r
def shiftB (x : Site) (r : Role) : Fin 2 := if r = B then flip (x r) else x r
def origin : Site := fun _ => (0 : Fin 2)

def sqrtWeight (x : Site) : ℚ := if x A = (0 : Fin 2) then 1 else 2

theorem sqrtWeight_positive (x : Site) : 0 < sqrtWeight x := by
  unfold sqrtWeight
  split_ifs <;> norm_num

theorem shifts_commute (x : Site) : shiftB (shiftA x) = shiftA (shiftB x) := by
  funext r
  by_cases ha : r = A
  · subst r
    simp [shiftA, shiftB, A, B]
  · by_cases hb : r = B
    · subst r
      simp [shiftA, shiftB, A, B]
    · simp [shiftA, shiftB, ha, hb]

theorem diagonal_ne : shiftA (shiftB origin) ≠ shiftA origin := by
  intro h
  have hb := congrFun h B
  norm_num [shiftA, shiftB, origin, flip, A, B] at hb

theorem directions_ne : shiftB origin ≠ shiftA origin := by
  intro h
  have hb := congrFun h B
  norm_num [shiftA, shiftB, origin, flip, A, B] at hb

theorem weighted_carrier_component :
    weightedSquare shiftA shiftB sqrtWeight (delta (shiftA origin)) origin = -1 := by
  rw [weighted_square_probe shiftA shiftB sqrtWeight origin
    (shifts_commute origin) diagonal_ne directions_ne]
  have hw0 : sqrtWeight origin = 1 := by decide
  have hw1 : sqrtWeight (shiftA origin) = 2 := by decide
  rw [hw0, hw1]
  norm_num

def vacuum : ArchiveFockState := fun _ => false
def abOccupied : ArchiveFockState := fun r => r = A || r = B

theorem two_creation_modes :
    (∑ f : ArchiveFockState, carCreateInt A abOccupied f * carCreateInt B f vacuum) = 1 := by
  decide

set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def shiftRole (r : Role) (x : Site) (t : Role) : Fin 2 :=
  if t = r then flip (x t) else x t

def sqrtWeightInt (x : Site) : ℤ := if x A = (0 : Fin 2) then 1 else 2

def carFieldProbe (x : Site) (f : ArchiveFockState) : ℤ :=
  if x = shiftA origin ∧ f = vacuum then 1 else 0

/-- The left-weighted four-role exterior difference with the existing CAR matrices. -/
def weightedExterior (field : Site → ArchiveFockState → ℤ)
    (x : Site) (bra : ArchiveFockState) : ℤ :=
  sqrtWeightInt x * ∑ r : Role, ∑ ket : ArchiveFockState,
    (field (shiftRole r x) ket - field x ket) * carCreateInt r bra ket

theorem actual_four_role_car_square :
    weightedExterior (weightedExterior carFieldProbe) origin abOccupied = -1 := by
  decide

theorem fock_degree_vacuum_and_pair :
    fockDegree vacuum = 0 ∧ fockDegree abOccupied = 2 := by
  decide

theorem weight_values :
    sqrtWeightInt origin = 1 ∧ sqrtWeightInt (shiftA origin) = 2 := by
  decide

def unweightedExterior (field : Site → ArchiveFockState → ℤ)
    (x : Site) (bra : ArchiveFockState) : ℤ :=
  ∑ r : Role, ∑ ket : ArchiveFockState,
    (field (shiftRole r x) ket - field x ket) * carCreateInt r bra ket

theorem unweighted_four_role_car_control :
    unweightedExterior (unweightedExterior carFieldProbe) origin abOccupied = 0 := by
  decide

def weightInt (x : Site) : ℤ := sqrtWeightInt x ^ 2

theorem sqrtWeightInt_positive (x : Site) : 0 < sqrtWeightInt x := by
  unfold sqrtWeightInt
  split_ifs <;> norm_num

theorem sqrt_weight_correct (x : Site) :
    Real.sqrt (weightInt x : ℝ) = (sqrtWeightInt x : ℝ) := by
  unfold weightInt sqrtWeightInt
  split_ifs <;> norm_num

end TypedArchiveLeakage

#print axioms WeightedLeakageGeneral.weighted_square_ne_zero_of_varying_neighbor
#print axioms TypedArchiveLeakage.actual_four_role_car_square
#print axioms TypedArchiveLeakage.unweighted_four_role_car_control
