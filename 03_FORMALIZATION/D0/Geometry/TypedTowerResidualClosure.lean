import D0.Geometry.TypedRoleOppositeCut
import Mathlib.Tactic

/-!
# Typed tower probe closure

Three intrinsic probes sit on the typed tower:

* balanced functions on `Omega8`, extended by zero on the witness of `V9`;
* balanced functions on `Dyad`, extended by zero on the `V9` summand of `V11`;
* balanced functions on `Role`, extended by zero on the `V9` summand of `V13`.

Their opposite-cut residuals carry coefficients `143`, `117`, and `99`.
The three residuals vanish simultaneously if and only if the three block
weights are equal.  That locus is algebraic.  It is not a theorem of M1, and
it is not a selection by physical dynamics.

`BalancedOmega8` is a typed scene sector of dimension 7.  It is not Fock
space and not a generation space.
-/

namespace D0.Geometry.TypedTowerResidualClosure

open D0.Geometry.OppositeCutPairing
open D0.Geometry.TypedSceneOppositeCut
open D0.Geometry.TypedRoleOppositeCut

abbrev BalancedDyad := BalancedOn Dyad

theorem balancedDyad_finrank : Module.finrank ℚ BalancedDyad = 1 := by
  simpa [card_dyad] using balancedOn_finrank (ι := Dyad) (0 : Dyad)

def extendDyadToV11 : (Dyad → ℚ) →ₗ[ℚ] (V11 → ℚ) :=
  extendInrLin (α := V9) (β := Dyad)

theorem extendDyad_balanced (f : BalancedDyad) :
    ∑ v : V11, extendDyadToV11 f.1 v = 0 := by
  have h := sum_extendInr (α := V9) (β := Dyad) f.1
  simpa [extendDyadToV11, coordinateSum] using h.trans f.2

def typedDyadOppositeCut : BalancedDyad →ₗ[ℚ] TypedEdgeCochain :=
  (oppositeCutBetaLin (α := V9) (γ := V13)).comp
    (extendDyadToV11.comp BalancedDyad.subtype)

theorem typedDyadOppositeCut_apply (f : BalancedDyad) :
    typedDyadOppositeCut f = oppositeCutBeta (α := V9) (γ := V13) (extendDyadToV11 f.1) :=
  rfl

def typedDyadResidual (wAB wAC wBC : ℚ) : BalancedDyad →ₗ[ℚ] TypedVertexCochain :=
  (typedWeightedIncidence wAB wAC wBC).comp typedDyadOppositeCut

theorem typed_dyad_cut_factorization (wAB wAC wBC : ℚ) (f : BalancedDyad) :
    unsignedIncidence (blockScale wAB wAC wBC (typedDyadOppositeCut f)) =
      (117 * (wAB - wBC)) • liftBeta (α := V9) (γ := V13) (extendDyadToV11 f.1) := by
  rw [typedDyadOppositeCut_apply]
  have h :=
    unsignedIncidence_block_oppositeCutBeta (α := V9) (β := V11) (γ := V13)
      wAB wAC wBC (extendDyadToV11 f.1) (extendDyad_balanced f)
  rw [typed_scene_coeff_117] at h
  exact h

theorem typedDyadResidual_apply (wAB wAC wBC : ℚ) (f : BalancedDyad) :
    typedDyadResidual wAB wAC wBC f =
      (117 * (wAB - wBC)) • liftBeta (α := V9) (γ := V13) (extendDyadToV11 f.1) :=
  typed_dyad_cut_factorization wAB wAC wBC f

theorem typed_dyad_residual_v9Summand_zero
    (wAB wAC wBC : ℚ) (f : BalancedDyad) (v : V9) :
    typedDyadResidual wAB wAC wBC f (Sum.inr (Sum.inl (Sum.inl v))) = 0 := by
  rw [typedDyadResidual_apply]
  simp [liftBeta, extendDyadToV11, extendInrLin, smul_eq_mul]

theorem typed_dyad_residual_dyadSummand
    (wAB wAC wBC : ℚ) (f : BalancedDyad) (d : Dyad) :
    typedDyadResidual wAB wAC wBC f (Sum.inr (Sum.inl (Sum.inr d))) =
      117 * (wAB - wBC) * f.1 d := by
  rw [typedDyadResidual_apply]
  simp [liftBeta, extendDyadToV11, extendInrLin, smul_eq_mul]

def dyadProbe : BalancedDyad :=
  ⟨fun d => if d = 0 then -1 else 1, by
    simp [coordinateSum, Dyad, Fin.sum_univ_two]⟩

theorem dyadProbe_at_one : dyadProbe.1 (1 : Dyad) = 1 := by
  simp [dyadProbe]

theorem coeff117_ne_zero : (117 : ℚ) ≠ 0 := by norm_num

theorem typed_dyad_cut_zero_of_weights_eq (wAC w : ℚ) (f : BalancedDyad) :
    typedDyadResidual w wAC w f = 0 := by
  rw [typedDyadResidual_apply, sub_self, mul_zero, zero_smul]

theorem typed_dyad_residual_eq_zero_iff (wAB wAC wBC : ℚ) :
    typedDyadResidual wAB wAC wBC = 0 ↔ wAB = wBC := by
  constructor
  · intro h
    have hzero : typedDyadResidual wAB wAC wBC dyadProbe = 0 := by
      rw [h, LinearMap.zero_apply]
    have hval := congrFun hzero (Sum.inr (Sum.inl (Sum.inr (1 : Dyad))))
    rw [typed_dyad_residual_dyadSummand, dyadProbe_at_one, Pi.zero_apply] at hval
    have hmul : 117 * (wAB - wBC) = 0 := by nlinarith
    exact sub_eq_zero.mp ((mul_eq_zero.mp hmul).resolve_left coeff117_ne_zero)
  · rintro rfl
    apply LinearMap.ext
    intro f
    exact typed_dyad_cut_zero_of_weights_eq wAC wAB f

theorem typed_dyad_cut_injective_of_weight_ne
    (wAB wAC wBC : ℚ) (hne : wAB ≠ wBC) :
    Function.Injective (typedDyadResidual wAB wAC wBC) := by
  intro f g hfg
  have hf : typedDyadResidual wAB wAC wBC (f - g) = 0 := by
    rw [map_sub, hfg, sub_self]
  rw [typedDyadResidual_apply] at hf
  have hc : (117 : ℚ) * (wAB - wBC) ≠ 0 :=
    mul_ne_zero coeff117_ne_zero (sub_ne_zero.mpr hne)
  have hlift : liftBeta (α := V9) (γ := V13) (extendDyadToV11 (f - g).1) = 0 :=
    (smul_eq_zero.mp hf).resolve_left hc
  have hf0 : (f - g).1 = 0 := by
    funext d
    have hv := congrFun hlift (Sum.inr (Sum.inl (Sum.inr d)))
    have hv0 : liftBeta (α := V9) (γ := V13) (extendDyadToV11 (f - g).1)
        (Sum.inr (Sum.inl (Sum.inr d))) = 0 := by
      simpa using hv
    simpa [liftBeta, extendDyadToV11, extendInrLin] using hv0
  exact sub_eq_zero.mp (Subtype.ext hf0)

theorem typed_dyad_cut_rank_one (wAB wAC wBC : ℚ) (hne : wAB ≠ wBC) :
    Module.finrank ℚ (LinearMap.range (typedDyadResidual wAB wAC wBC)) = 1 := by
  rw [LinearMap.finrank_range_of_inj (typed_dyad_cut_injective_of_weight_ne wAB wAC wBC hne),
    balancedDyad_finrank]

/-! ## Omega8 summand of V9 -/

abbrev BalancedOmega8 := BalancedOn Omega8

theorem balancedOmega8_finrank : Module.finrank ℚ BalancedOmega8 = 7 := by
  have hcard : Fintype.card Omega8 = 8 := card_omega8
  simpa [hcard] using
    balancedOn_finrank (ι := Omega8) (((0, 0), false) : Omega8)

def extendOmega8ToV9 : (Omega8 → ℚ) →ₗ[ℚ] (V9 → ℚ) :=
  extendInlLin (α := Omega8) (β := Witness)

theorem extendOmega8_balanced (f : BalancedOmega8) :
    ∑ v : V9, extendOmega8ToV9 f.1 v = 0 := by
  have h := sum_extendInl (α := Omega8) (β := Witness) f.1
  simpa [extendOmega8ToV9, coordinateSum] using h.trans f.2

def typedOmega8OppositeCut : BalancedOmega8 →ₗ[ℚ] TypedEdgeCochain :=
  (oppositeCutAlphaLin (β := V11) (γ := V13)).comp
    (extendOmega8ToV9.comp BalancedOmega8.subtype)

theorem typedOmega8OppositeCut_apply (f : BalancedOmega8) :
    typedOmega8OppositeCut f =
      oppositeCutAlpha (β := V11) (γ := V13) (extendOmega8ToV9 f.1) :=
  rfl

def typedOmega8Residual (wAB wAC wBC : ℚ) :
    BalancedOmega8 →ₗ[ℚ] TypedVertexCochain :=
  (typedWeightedIncidence wAB wAC wBC).comp typedOmega8OppositeCut

theorem typed_omega8_cut_factorization (wAB wAC wBC : ℚ) (f : BalancedOmega8) :
    unsignedIncidence (blockScale wAB wAC wBC (typedOmega8OppositeCut f)) =
      (143 * (wAB - wAC)) • liftAlpha (β := V11) (γ := V13) (extendOmega8ToV9 f.1) := by
  rw [typedOmega8OppositeCut_apply]
  have h :=
    unsignedIncidence_block_oppositeCutAlpha (α := V9) (β := V11) (γ := V13)
      wAB wAC wBC (extendOmega8ToV9 f.1) (extendOmega8_balanced f)
  rw [typed_scene_coeff_143] at h
  exact h

theorem typedOmega8Residual_apply (wAB wAC wBC : ℚ) (f : BalancedOmega8) :
    typedOmega8Residual wAB wAC wBC f =
      (143 * (wAB - wAC)) • liftAlpha (β := V11) (γ := V13) (extendOmega8ToV9 f.1) :=
  typed_omega8_cut_factorization wAB wAC wBC f

theorem typed_omega8_residual_witness_zero
    (wAB wAC wBC : ℚ) (f : BalancedOmega8) (w : Witness) :
    typedOmega8Residual wAB wAC wBC f (Sum.inl (Sum.inr w)) = 0 := by
  rw [typedOmega8Residual_apply]
  simp [liftAlpha, extendOmega8ToV9, extendInlLin, smul_eq_mul]

theorem typed_omega8_residual_omegaSummand
    (wAB wAC wBC : ℚ) (f : BalancedOmega8) (x : Omega8) :
    typedOmega8Residual wAB wAC wBC f (Sum.inl (Sum.inl x)) =
      143 * (wAB - wAC) * f.1 x := by
  rw [typedOmega8Residual_apply]
  simp [liftAlpha, extendOmega8ToV9, extendInlLin, smul_eq_mul]

def omegaProbePoint : Omega8 := ((0, 0), false)
def omegaProbeOther : Omega8 := ((0, 0), true)

def omegaProbe : BalancedOmega8 :=
  ⟨fun x => if x = omegaProbePoint then 1 else if x = omegaProbeOther then -1 else 0, by
    simp [coordinateSum, omegaProbePoint, omegaProbeOther, Omega8, Role, Dyad, Orient,
      Fintype.sum_prod_type, Fin.sum_univ_two]⟩

theorem omegaProbe_at_point : omegaProbe.1 omegaProbePoint = 1 := by
  simp [omegaProbe, omegaProbePoint, omegaProbeOther]

theorem coeff143_ne_zero : (143 : ℚ) ≠ 0 := by norm_num

theorem typed_omega8_cut_zero_of_weights_eq (wBC w : ℚ) (f : BalancedOmega8) :
    typedOmega8Residual w w wBC f = 0 := by
  rw [typedOmega8Residual_apply, sub_self, mul_zero, zero_smul]

theorem typed_omega8_residual_eq_zero_iff (wAB wAC wBC : ℚ) :
    typedOmega8Residual wAB wAC wBC = 0 ↔ wAB = wAC := by
  constructor
  · intro h
    have hzero : typedOmega8Residual wAB wAC wBC omegaProbe = 0 := by
      rw [h, LinearMap.zero_apply]
    have hval := congrFun hzero (Sum.inl (Sum.inl omegaProbePoint))
    rw [typed_omega8_residual_omegaSummand, omegaProbe_at_point, Pi.zero_apply] at hval
    have hmul : 143 * (wAB - wAC) = 0 := by nlinarith
    exact sub_eq_zero.mp ((mul_eq_zero.mp hmul).resolve_left coeff143_ne_zero)
  · rintro rfl
    apply LinearMap.ext
    intro f
    exact typed_omega8_cut_zero_of_weights_eq wBC wAB f

theorem typed_omega8_cut_injective_of_weight_ne
    (wAB wAC wBC : ℚ) (hne : wAB ≠ wAC) :
    Function.Injective (typedOmega8Residual wAB wAC wBC) := by
  intro f g hfg
  have hf : typedOmega8Residual wAB wAC wBC (f - g) = 0 := by
    rw [map_sub, hfg, sub_self]
  rw [typedOmega8Residual_apply] at hf
  have hc : (143 : ℚ) * (wAB - wAC) ≠ 0 :=
    mul_ne_zero coeff143_ne_zero (sub_ne_zero.mpr hne)
  have hlift : liftAlpha (β := V11) (γ := V13) (extendOmega8ToV9 (f - g).1) = 0 :=
    (smul_eq_zero.mp hf).resolve_left hc
  have hf0 : (f - g).1 = 0 := by
    funext x
    have hv := congrFun hlift (Sum.inl (Sum.inl x))
    have hv0 : liftAlpha (β := V11) (γ := V13) (extendOmega8ToV9 (f - g).1)
        (Sum.inl (Sum.inl x)) = 0 := by
      simpa using hv
    simpa [liftAlpha, extendOmega8ToV9, extendInlLin] using hv0
  exact sub_eq_zero.mp (Subtype.ext hf0)

theorem typed_omega8_cut_rank_seven (wAB wAC wBC : ℚ) (hne : wAB ≠ wAC) :
    Module.finrank ℚ (LinearMap.range (typedOmega8Residual wAB wAC wBC)) = 7 := by
  rw [LinearMap.finrank_range_of_inj (typed_omega8_cut_injective_of_weight_ne wAB wAC wBC hne),
    balancedOmega8_finrank]

/-! ## Simultaneous vanishing -/

theorem typed_tower_uniform_kills_probes (w : ℚ) :
    typedOmega8Residual w w w = 0 ∧
      typedDyadResidual w w w = 0 ∧
      typedRoleResidual w w w = 0 := by
  refine ⟨?_, ?_, ?_⟩
  · apply LinearMap.ext; intro f; exact typed_omega8_cut_zero_of_weights_eq w w f
  · apply LinearMap.ext; intro f; exact typed_dyad_cut_zero_of_weights_eq w w f
  · apply LinearMap.ext; intro f; exact typed_role_cut_zero_of_weights_eq w w f

/-- Vanishing of the three typed probe residuals is exactly uniformity of the
three block weights.  This is an algebraic locus, not an M1 theorem. -/
theorem typed_tower_probe_residual_zero_iff_uniform_weights (wAB wAC wBC : ℚ) :
    (typedOmega8Residual wAB wAC wBC = 0 ∧
        typedDyadResidual wAB wAC wBC = 0 ∧
        typedRoleResidual wAB wAC wBC = 0) ↔
      (wAB = wAC ∧ wAB = wBC ∧ wAC = wBC) := by
  constructor
  · intro ⟨hΩ, hD, hR⟩
    have hAC := (typed_omega8_residual_eq_zero_iff wAB wAC wBC).mp hΩ
    have hBC := (typed_dyad_residual_eq_zero_iff wAB wAC wBC).mp hD
    have hRole := (typed_role_residual_eq_zero_iff wAB wAC wBC).mp hR
    exact ⟨hAC, hBC, hRole⟩
  · intro ⟨hAC, hBC, hRole⟩
    have hAB : wAB = wAC := hAC
    refine ⟨?_, ?_, ?_⟩
    · rw [hAB]; apply LinearMap.ext; intro f; exact typed_omega8_cut_zero_of_weights_eq wBC wAC f
    · rw [← hBC]; apply LinearMap.ext; intro f; exact typed_dyad_cut_zero_of_weights_eq wAC wAB f
    · rw [hRole]; apply LinearMap.ext; intro f; exact typed_role_cut_zero_of_weights_eq wAB wBC f

/-- The Role sector alone does not force the three weights to agree. -/
theorem role_sector_alone_does_not_force_uniform_weights :
    typedRoleResidual 1 0 0 = 0 ∧ ¬ ((1 : ℚ) = 0 ∧ (1 : ℚ) = 0 ∧ (0 : ℚ) = 0) := by
  refine ⟨?_, ?_⟩
  · apply LinearMap.ext
    intro f
    exact typed_role_cut_zero_of_weights_eq 1 0 f
  · intro h
    exact one_ne_zero h.1

end D0.Geometry.TypedTowerResidualClosure
