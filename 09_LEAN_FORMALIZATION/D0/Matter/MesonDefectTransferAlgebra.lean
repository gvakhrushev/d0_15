import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic

namespace D0.Matter

/-- Common finite carrier for meson transfer algebra: edge support times generation index. -/
abbrev MesonCarrier (E Gen : Nat) : Type :=
  Prod (Fin E) (Fin Gen)

/-- Lift an edge operator to the common edge-generation carrier. -/
def liftEdge {E Gen : Nat} [DecidableEq (Fin Gen)]
    (A : Matrix (Fin E) (Fin E) Rat) :
    Matrix (MesonCarrier E Gen) (MesonCarrier E Gen) Rat :=
  fun x y => if x.2 = y.2 then A x.1 y.1 else 0

/-- Lift a generation/flavour operator to the common edge-generation carrier. -/
def liftGen {E Gen : Nat} [DecidableEq (Fin E)]
    (B : Matrix (Fin Gen) (Fin Gen) Rat) :
    Matrix (MesonCarrier E Gen) (MesonCarrier E Gen) Rat :=
  fun x y => if x.1 = y.1 then B x.2 y.2 else 0

/-- Diagonal support projector on the common meson carrier. -/
def mesonSupportProjector {E Gen : Nat} [DecidableEq (MesonCarrier E Gen)]
    (support : MesonCarrier E Gen -> Bool) :
    Matrix (MesonCarrier E Gen) (MesonCarrier E Gen) Rat :=
  fun x y => if x = y then if support x then 1 else 0 else 0

/--
Typed meson defect transfer operator.  The flavour defect is lifted with
`liftGen`; it is not added directly to edge-space operators.
-/
def mesonDefectTransferOperator {E Gen : Nat}
    [Fintype (MesonCarrier E Gen)] [DecidableEq (MesonCarrier E Gen)]
    [DecidableEq (Fin E)] [DecidableEq (Fin Gen)]
    (support : MesonCarrier E Gen -> Bool)
    (L_M R_chi R_vsp : Matrix (Fin E) (Fin E) Rat)
    (R_fl : Matrix (Fin Gen) (Fin Gen) Rat) :
    Matrix (MesonCarrier E Gen) (MesonCarrier E Gen) Rat :=
  let Pi := mesonSupportProjector support
  Pi * (liftEdge L_M + liftEdge R_chi + liftGen R_fl + liftEdge R_vsp) * Pi

/-- The bare lower-Hodge lift is blind to the internal generation index. -/
theorem lower_hodge_lift_has_internal_degeneracy
    {E Gen : Nat} [DecidableEq (Fin Gen)]
    (L_M : Matrix (Fin E) (Fin E) Rat)
    (e e' : Fin E) (g h : Fin Gen) :
    liftEdge (Gen := Gen) L_M (e, g) (e', g) =
      liftEdge (Gen := Gen) L_M (e, h) (e', h) := by
  simp [liftEdge]

/-- A matrix separates generation channels when some equal-edge diagonal entries differ. -/
def SeparatesMesonTransferChannels {E Gen : Nat}
    (M : Matrix (MesonCarrier E Gen) (MesonCarrier E Gen) Rat) : Prop :=
  exists e : Fin E, exists g h : Fin Gen, Not (M (e, g) (e, g) = M (e, h) (e, h))

/--
The bare lower-Hodge seed lifted as `L_M x I_internal` cannot by itself separate
meson transfer channels.  Chiral, flavour and vector/spin defects are required
before physical meson comparison.
-/
theorem lower_hodge_seed_not_meson_mass_operator
    {E Gen : Nat} [DecidableEq (Fin Gen)]
    (L_M : Matrix (Fin E) (Fin E) Rat) :
    Not (SeparatesMesonTransferChannels (liftEdge (Gen := Gen) L_M)) := by
  intro h
  rcases h with ⟨e, g, hgen, hneq⟩
  exact hneq (lower_hodge_lift_has_internal_degeneracy L_M e e g hgen)

/-- The flavour defect participates through the common carrier lift. -/
theorem meson_transfer_operator_uses_lifted_flavour_defect
    {E Gen : Nat}
    [Fintype (MesonCarrier E Gen)] [DecidableEq (MesonCarrier E Gen)]
    [DecidableEq (Fin E)] [DecidableEq (Fin Gen)]
    (support : MesonCarrier E Gen -> Bool)
    (L_M R_chi R_vsp : Matrix (Fin E) (Fin E) Rat)
    (R_fl : Matrix (Fin Gen) (Fin Gen) Rat) :
    mesonDefectTransferOperator support L_M R_chi R_vsp R_fl =
      (let Pi := mesonSupportProjector support
       Pi * (liftEdge L_M + liftEdge R_chi + liftGen R_fl + liftEdge R_vsp) * Pi) := by
  rfl

/-- Constructive finite algebra package for typed meson defect transfer. -/
structure MesonDefectTransferAlgebraClosure where
  carrier_dim_fixture : Nat
  lower_hodge_degeneracy :
    forall {E Gen : Nat} [DecidableEq (Fin Gen)]
      (L_M : Matrix (Fin E) (Fin E) Rat)
      (e e' : Fin E) (g h : Fin Gen),
      liftEdge (Gen := Gen) L_M (e, g) (e', g) =
        liftEdge (Gen := Gen) L_M (e, h) (e', h)
  lower_hodge_no_go :
    forall {E Gen : Nat} [DecidableEq (Fin Gen)]
      (L_M : Matrix (Fin E) (Fin E) Rat),
      Not (SeparatesMesonTransferChannels (liftEdge (Gen := Gen) L_M))
  flavour_defect_lifted :
    forall {E Gen : Nat}
      [Fintype (MesonCarrier E Gen)] [DecidableEq (MesonCarrier E Gen)]
      [DecidableEq (Fin E)] [DecidableEq (Fin Gen)]
      (support : MesonCarrier E Gen -> Bool)
      (L_M R_chi R_vsp : Matrix (Fin E) (Fin E) Rat)
      (R_fl : Matrix (Fin Gen) (Fin Gen) Rat),
      mesonDefectTransferOperator support L_M R_chi R_vsp R_fl =
        (let Pi := mesonSupportProjector support
         Pi * (liftEdge L_M + liftEdge R_chi + liftGen R_fl + liftEdge R_vsp) * Pi)

/-- Concrete owner for the meson defect-transfer algebra interface. -/
def meson_defect_transfer_algebra_closure : MesonDefectTransferAlgebraClosure where
  carrier_dim_fixture := 12
  lower_hodge_degeneracy := by
    intro E Gen hDec L_M e e' g h
    exact lower_hodge_lift_has_internal_degeneracy L_M e e' g h
  lower_hodge_no_go := by
    intro E Gen hDec L_M
    exact lower_hodge_seed_not_meson_mass_operator L_M
  flavour_defect_lifted := by
    intro E Gen hFin hDecCarrier hDecE hDecGen support L_M R_chi R_vsp R_fl
    exact meson_transfer_operator_uses_lifted_flavour_defect support L_M R_chi R_vsp R_fl

end D0.Matter
