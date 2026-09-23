import D0.Geometry.TypedSceneOppositeCut
import Mathlib.Tactic

/-!
# Role-supported opposite cut

`RoleCut` is the generic `γ`-cut of a function supported on the Role summand
of typed `V13`.  Its weighted incidence coefficient is the typed product
`|V9| |V11| = 99`.  The output vertex residual is zero on the `V9` summand of
zone 13 and equals `99 (wAC - wBC) f(r)` on the Role summand.

When `wAC ≠ wBC` this residual is injective on the 3-dimensional balanced
Role space, so the rank is 3.  When the two incident weights agree, the
residual vanishes.  One Role sector does not constrain `wAB`.
-/

namespace D0.Geometry.TypedRoleOppositeCut

open D0.Geometry.OppositeCutPairing
open D0.Geometry.TypedSceneOppositeCut

abbrev TypedEdgeCochain := TypedSceneEdge → ℚ

abbrev TypedVertexCochain := TypedSceneVertex → ℚ

def typedRoleOppositeCut : BalancedRole →ₗ[ℚ] TypedEdgeCochain :=
  (oppositeCutGammaLin (α := V9) (β := V11) (γ := V13)).comp
    (extendRoleToV13.comp BalancedRole.subtype)

theorem typedRoleOppositeCut_apply (f : BalancedRole) :
    typedRoleOppositeCut f = oppositeCutGamma (α := V9) (β := V11) (extendRoleToV13 f.1) :=
  rfl

def typedWeightedIncidence (wAB wAC wBC : ℚ) :
    TypedEdgeCochain →ₗ[ℚ] TypedVertexCochain :=
  (unsignedIncidenceLin (α := V9) (β := V11) (γ := V13)).comp (blockScaleLin wAB wAC wBC)

def typedRoleResidual (wAB wAC wBC : ℚ) : BalancedRole →ₗ[ℚ] TypedVertexCochain :=
  (typedWeightedIncidence wAB wAC wBC).comp typedRoleOppositeCut

theorem typed_role_cut_factorization (wAB wAC wBC : ℚ) (f : BalancedRole) :
    unsignedIncidence (blockScale wAB wAC wBC (typedRoleOppositeCut f)) =
      (99 * (wAC - wBC)) • liftGamma (α := V9) (β := V11) (extendRoleToV13 f.1) := by
  rw [typedRoleOppositeCut_apply]
  have h :=
    unsignedIncidence_block_oppositeCutGamma (α := V9) (β := V11) (γ := V13)
      wAB wAC wBC (extendRoleToV13 f.1) (extendRole_balanced f)
  rw [typed_scene_coeff_99] at h
  exact h

theorem typedRoleResidual_apply (wAB wAC wBC : ℚ) (f : BalancedRole) :
    typedRoleResidual wAB wAC wBC f =
      (99 * (wAC - wBC)) • liftGamma (α := V9) (β := V11) (extendRoleToV13 f.1) :=
  typed_role_cut_factorization wAB wAC wBC f

/-- The Role residual vanishes on the `V9` summand of zone 13. -/
theorem typed_role_residual_v9Summand_zero
    (wAB wAC wBC : ℚ) (f : BalancedRole) (v : V9) :
    typedRoleResidual wAB wAC wBC f (Sum.inr (Sum.inr (Sum.inl v))) = 0 := by
  rw [typedRoleResidual_apply]
  simp [liftGamma, extendRoleToV13, extendInrLin, smul_eq_mul]

/-- On the Role summand the residual is the scalar `99 (wAC - wBC)` times `f`. -/
theorem typed_role_residual_roleSummand
    (wAB wAC wBC : ℚ) (f : BalancedRole) (r : Role) :
    typedRoleResidual wAB wAC wBC f (Sum.inr (Sum.inr (Sum.inr r))) =
      99 * (wAC - wBC) * f.1 r := by
  rw [typedRoleResidual_apply]
  simp [liftGamma, extendRoleToV13, extendInrLin, smul_eq_mul]

theorem typed_role_cut_zero_of_weights_eq (wAB w : ℚ) (f : BalancedRole) :
    typedRoleResidual wAB w w f = 0 := by
  rw [typedRoleResidual_apply, sub_self, mul_zero, zero_smul]

/-- A balanced probe with value `1` at `B` and `-1` at `A`. -/
def roleProbeBA : BalancedRole :=
  ⟨fun r => if r = B then 1 else if r = A then -1 else 0, by
    simp [coordinateSum, A, B, Role, Dyad, Fintype.sum_prod_type, Fin.sum_univ_two]⟩

theorem roleProbeBA_at_B : roleProbeBA.1 B = 1 := by
  simp [roleProbeBA, A, B]

theorem coeff99_ne_zero : (99 : ℚ) ≠ 0 := by norm_num

theorem typed_role_residual_eq_zero_iff (wAB wAC wBC : ℚ) :
    typedRoleResidual wAB wAC wBC = 0 ↔ wAC = wBC := by
  constructor
  · intro h
    have hzero : typedRoleResidual wAB wAC wBC roleProbeBA = 0 := by
      rw [h, LinearMap.zero_apply]
    have hval := congrFun hzero (Sum.inr (Sum.inr (Sum.inr B)))
    rw [typed_role_residual_roleSummand, roleProbeBA_at_B, Pi.zero_apply] at hval
    have hmul : 99 * (wAC - wBC) = 0 := by nlinarith
    exact sub_eq_zero.mp ((mul_eq_zero.mp hmul).resolve_left coeff99_ne_zero)
  · rintro rfl
    apply LinearMap.ext
    intro f
    exact typed_role_cut_zero_of_weights_eq wAB wAC f

theorem liftGamma_role_injective :
    Function.Injective (liftGamma (α := V9) (β := V11) (γ := V13)) := by
  intro f g h
  funext c
  have hc := congrFun h (Sum.inr (Sum.inr c))
  simpa [liftGamma] using hc

theorem typed_role_cut_injective_of_weight_ne
    (wAB wAC wBC : ℚ) (hne : wAC ≠ wBC) :
    Function.Injective (typedRoleResidual wAB wAC wBC) := by
  intro f g hfg
  have hf : typedRoleResidual wAB wAC wBC (f - g) = 0 := by
    rw [map_sub, hfg, sub_self]
  rw [typedRoleResidual_apply] at hf
  have hc : (99 : ℚ) * (wAC - wBC) ≠ 0 :=
    mul_ne_zero coeff99_ne_zero (sub_ne_zero.mpr hne)
  have hlift : liftGamma (α := V9) (β := V11) (extendRoleToV13 (f - g).1) = 0 :=
    (smul_eq_zero.mp hf).resolve_left hc
  have hf0 : (f - g).1 = 0 := by
    apply extendRoleToV13_injective
    apply liftGamma_role_injective
    rw [hlift]
    ext v
    rcases v with a | b | c
    · simp [liftGamma]
    · simp [liftGamma]
    · rcases c with v9 | r <;> simp [liftGamma, extendRoleToV13, extendInrLin]
  exact sub_eq_zero.mp (Subtype.ext hf0)

theorem typed_role_cut_rank_three (wAB wAC wBC : ℚ) (hne : wAC ≠ wBC) :
    Module.finrank ℚ (LinearMap.range (typedRoleResidual wAB wAC wBC)) = 3 := by
  rw [LinearMap.finrank_range_of_inj (typed_role_cut_injective_of_weight_ne wAB wAC wBC hne),
    balancedRole_finrank]

/-- The Role coefficient follows the typed zone sizes.  The control scene
`K(3,3,8)` has gamma coefficient `9`, not `99`. -/
theorem typed_role_coefficient_changes_with_zone_size :
    (Fintype.card V9 : ℚ) * Fintype.card V11 = 99 ∧
      (Fintype.card (Fin 3) : ℚ) * Fintype.card (Fin 3) = 9 ∧
      ((99 : ℚ) ≠ 9) := by
  refine ⟨typed_scene_coeff_99, ?_, by norm_num⟩
  simp [Fintype.card_fin]
  norm_num

end D0.Geometry.TypedRoleOppositeCut
