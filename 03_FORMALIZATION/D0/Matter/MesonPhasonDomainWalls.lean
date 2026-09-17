import D0.Matter.PhasonStrainGenerations
import D0.Matter.MesonDefectTransferOrigin

namespace D0.Matter

/-!
QUASI-007: meson phason domain-wall carrier.

The wall carrier is finite and oriented: a wall is a transition between two
different phason modes.  This module only supplies the carrier/origin layer and
reuses the existing meson defect-transfer operator on `Edge x Generation`.
-/

/-- Six oriented phason domain walls between the three phason modes. -/
inductive MesonPhasonDomainWall where
  | w01 | w02 | w10 | w12 | w20 | w21
  deriving DecidableEq, Repr, Fintype

/-- Source phason slot of an oriented wall. -/
def MesonPhasonDomainWall.sourceIx : MesonPhasonDomainWall -> Fin 3
  | .w01 => 0
  | .w02 => 0
  | .w10 => 1
  | .w12 => 1
  | .w20 => 2
  | .w21 => 2

/-- Target phason slot of an oriented wall. -/
def MesonPhasonDomainWall.targetIx : MesonPhasonDomainWall -> Fin 3
  | .w01 => 1
  | .w02 => 2
  | .w10 => 0
  | .w12 => 2
  | .w20 => 0
  | .w21 => 1

/-- Every listed meson phason wall has a nonzero boundary. -/
theorem meson_phason_domain_wall_boundary_nonzero
    (w : MesonPhasonDomainWall) :
    w.sourceIx ≠ w.targetIx := by
  cases w <;> decide

/-- The oriented domain-wall carrier has `3*2=6` walls. -/
theorem meson_phason_domain_wall_card_eq_six :
    Fintype.card MesonPhasonDomainWall = 6 := by
  native_decide

/-- Meson wall carrier includes generation readout. -/
abbrev MesonDomainWallCarrier : Type :=
  Prod MesonPhasonDomainWall GenerationPhasonMode

/-- The meson domain-wall carrier has dimension `6*3=18`. -/
theorem meson_domain_wall_generation_carrier_card_eq_eighteen :
    Fintype.card MesonDomainWallCarrier = 18 := by
  native_decide

/--
Domain-wall meson transfer still enters through the existing lifted flavour
defect operator on the common meson carrier.
-/
theorem meson_domain_wall_transfer_uses_lifted_defect
    {E Gen : Nat}
    [Fintype (MesonCarrier E Gen)] [DecidableEq (MesonCarrier E Gen)]
    [DecidableEq (Fin E)] [DecidableEq (Fin Gen)]
    (support : MesonCarrier E Gen -> Bool)
    (L_M R_chi R_vsp : Matrix (Fin E) (Fin E) Rat)
    (R_fl : Matrix (Fin Gen) (Fin Gen) Rat) :
    MesonPositiveDefectTransferAdmissible support L_M R_chi R_vsp R_fl := by
  exact meson_positive_defect_transfer_admissible support L_M R_chi R_vsp R_fl

/-- Closure package for the finite meson phason domain-wall origin. -/
structure MesonPhasonDomainWallClosure where
  wall_count : Fintype.card MesonPhasonDomainWall = 6
  wall_boundary_nonzero :
    forall w : MesonPhasonDomainWall, w.sourceIx ≠ w.targetIx
  wall_generation_carrier : Fintype.card MesonDomainWallCarrier = 18
  meson_transfer_origin : MesonDefectTransferOriginClosure

/-- Concrete finite domain-wall closure. -/
def mesonPhasonDomainWallClosure :
    MesonPhasonDomainWallClosure where
  wall_count := meson_phason_domain_wall_card_eq_six
  wall_boundary_nonzero := meson_phason_domain_wall_boundary_nonzero
  wall_generation_carrier := meson_domain_wall_generation_carrier_card_eq_eighteen
  meson_transfer_origin := meson_defect_transfer_origin_closure

/-- Machine-checkable QUASI-007 domain-wall closure theorem. -/
theorem meson_phason_domain_wall_closure :
    Fintype.card MesonPhasonDomainWall = 6 /\
      (forall w : MesonPhasonDomainWall, w.sourceIx ≠ w.targetIx) /\
      Fintype.card MesonDomainWallCarrier = 18 /\
      MesonDefectTransferOriginClosure := by
  exact
    ⟨mesonPhasonDomainWallClosure.wall_count,
      mesonPhasonDomainWallClosure.wall_boundary_nonzero,
      mesonPhasonDomainWallClosure.wall_generation_carrier,
      mesonPhasonDomainWallClosure.meson_transfer_origin⟩


end D0.Matter
