import D0.Matter.MesonDefectTransferAlgebra
import D0.Matter.CKMNontrivialFlavourAlgebra
import Mathlib.Tactic

namespace D0.Matter

/-- A column-positive response induced by `A^T A`. -/
def PositiveColumnResponse {I : Type} [Fintype I]
    (A : Matrix I I Rat) : Prop :=
  forall j : I, 0 <=
    Finset.univ.sum (fun i : I => A i j * A i j)

/-- Every finite defect matrix induces a positive `A^T A` column response. -/
theorem positive_column_response_of_matrix {I : Type} [Fintype I]
    (A : Matrix I I Rat) :
    PositiveColumnResponse A := by
  intro j
  exact Finset.sum_nonneg (fun i _ => mul_self_nonneg (A i j))

/-- The diagonal meson support projector is idempotent. -/
theorem meson_support_projector_idempotent
    {E Gen : Nat}
    [Fintype (MesonCarrier E Gen)] [DecidableEq (MesonCarrier E Gen)]
    (support : MesonCarrier E Gen -> Bool) :
    mesonSupportProjector support * mesonSupportProjector support =
      mesonSupportProjector support := by
  ext x y
  by_cases hxy : x = y
  · subst y
    by_cases hs : support x <;>
      simp [mesonSupportProjector, Matrix.mul_apply, hs]
  · simp [mesonSupportProjector, Matrix.mul_apply, hxy]

/-- The meson carrier is explicitly edge support times generation index. -/
theorem meson_support_projector_separates_from_baryon_support
    (E Gen : Nat) :
    MesonCarrier E Gen = Prod (Fin E) (Fin Gen) := by
  rfl

/-- Chiral defect responses enter as positive finite responses. -/
theorem chiral_defect_positive_response {E : Nat}
    (Gamma_chi : Matrix (Fin E) (Fin E) Rat) :
    PositiveColumnResponse Gamma_chi :=
  positive_column_response_of_matrix Gamma_chi

/-- Flavour defect responses enter as positive finite responses. -/
theorem flavour_defect_positive_response {Gen : Nat}
    (F_fl : Matrix (Fin Gen) (Fin Gen) Rat) :
    PositiveColumnResponse F_fl :=
  positive_column_response_of_matrix F_fl

/-- Vector/spin edge defects enter as positive finite responses. -/
theorem vector_spin_defect_positive_response {E : Nat}
    (V_sp : Matrix (Fin E) (Fin E) Rat) :
    PositiveColumnResponse V_sp :=
  positive_column_response_of_matrix V_sp

/-- Typed admissibility condition for the positive meson defect-transfer sum. -/
def MesonPositiveDefectTransferAdmissible
    {E Gen : Nat}
    [Fintype (MesonCarrier E Gen)] [DecidableEq (MesonCarrier E Gen)]
    [DecidableEq (Fin E)] [DecidableEq (Fin Gen)]
    (support : MesonCarrier E Gen -> Bool)
    (L_M R_chi R_vsp : Matrix (Fin E) (Fin E) Rat)
    (R_fl : Matrix (Fin Gen) (Fin Gen) Rat) : Prop :=
  mesonDefectTransferOperator support L_M R_chi R_vsp R_fl =
    (let Pi := mesonSupportProjector support
     Pi * (liftEdge L_M + liftEdge R_chi + liftGen R_fl + liftEdge R_vsp) * Pi)

/--
The positive meson defect-transfer operator is admissible only through the common
`Edge x Generation` carrier and the lifted flavour defect.
-/
theorem meson_positive_defect_transfer_admissible
    {E Gen : Nat}
    [Fintype (MesonCarrier E Gen)] [DecidableEq (MesonCarrier E Gen)]
    [DecidableEq (Fin E)] [DecidableEq (Fin Gen)]
    (support : MesonCarrier E Gen -> Bool)
    (L_M R_chi R_vsp : Matrix (Fin E) (Fin E) Rat)
    (R_fl : Matrix (Fin Gen) (Fin Gen) Rat) :
    MesonPositiveDefectTransferAdmissible support L_M R_chi R_vsp R_fl := by
  exact meson_transfer_operator_uses_lifted_flavour_defect
    support L_M R_chi R_vsp R_fl

/-- Closure package for the meson positive defect-transfer origin. -/
structure MesonDefectTransferOriginClosure where
  projector_idempotent :
    forall {E Gen : Nat}
      [Fintype (MesonCarrier E Gen)] [DecidableEq (MesonCarrier E Gen)]
      (support : MesonCarrier E Gen -> Bool),
      mesonSupportProjector support * mesonSupportProjector support =
        mesonSupportProjector support
  lower_hodge_no_go :
    forall {E Gen : Nat} [DecidableEq (Fin Gen)]
      (L_M : Matrix (Fin E) (Fin E) Rat),
      Not (SeparatesMesonTransferChannels (liftEdge (Gen := Gen) L_M))
  flavour_positive :
    forall {Gen : Nat} (F_fl : Matrix (Fin Gen) (Fin Gen) Rat),
      PositiveColumnResponse F_fl
  admissible :
    forall {E Gen : Nat}
      [Fintype (MesonCarrier E Gen)] [DecidableEq (MesonCarrier E Gen)]
      [DecidableEq (Fin E)] [DecidableEq (Fin Gen)]
      (support : MesonCarrier E Gen -> Bool)
      (L_M R_chi R_vsp : Matrix (Fin E) (Fin E) Rat)
      (R_fl : Matrix (Fin Gen) (Fin Gen) Rat),
      MesonPositiveDefectTransferAdmissible support L_M R_chi R_vsp R_fl

/-- Concrete owner for meson positive defect-transfer origin. -/
def meson_defect_transfer_origin_closure :
    MesonDefectTransferOriginClosure where
  projector_idempotent := by
    intro E Gen hFin hDec support
    exact meson_support_projector_idempotent support
  lower_hodge_no_go := by
    intro E Gen hDec L_M
    exact lower_hodge_seed_not_meson_mass_operator L_M
  flavour_positive := by
    intro Gen F_fl
    exact flavour_defect_positive_response F_fl
  admissible := by
    intro E Gen hFin hDecCarrier hDecE hDecGen support L_M R_chi R_vsp R_fl
    exact meson_positive_defect_transfer_admissible support L_M R_chi R_vsp R_fl

end D0.Matter
