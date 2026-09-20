import D0.Geometry.SceneCochainComplex
import D0.Topology.GenericTripartiteFirstHomologyRing
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Tactic

/-!
# C1 — typed common carrier for the literal `K(9,11,13)` scene

This file keeps the unsigned A1 endpoint-sum operator and the signed
transitive incidence/current-divergence operator on the same literal edge
carrier.  The local symmetry is the product of independent within-zone
permutations.  Its edge action is pullback along the induced permutation of
`SceneEdge`; no second edge carrier is introduced.

The semantic firewall is intentional: `BPlus` is the unsigned A1
Weyl/Ward endpoint-sum operator, while `BMinus` is the signed current
 divergence.  This file does not import any TT wave/dynamics module.
-/

namespace D0.Geometry.SignlessSignedCommonCarrier

open BigOperators Matrix
open D0.Geometry.SceneCochainComplex

abbrev V9T := Fin 9
abbrev V11T := Fin 11
abbrev V13T := Fin 13

/-- Independent within-zone relabellings; zones are not mixed. -/
abbrev LocalRelabelling :=
  Equiv.Perm V9T × Equiv.Perm V11T × Equiv.Perm V13T

/-- The induced relabelling of the literal edge carrier. -/
def edgeRelabel (h : LocalRelabelling) : SceneEdge → SceneEdge
  | Sum.inl (x, y) => Sum.inl (h.1 x, h.2.1 y)
  | Sum.inr (Sum.inl (x, z)) => Sum.inr (Sum.inl (h.1 x, h.2.2 z))
  | Sum.inr (Sum.inr (y, z)) => Sum.inr (Sum.inr (h.2.1 y, h.2.2 z))

/-- Inverse of a product relabelling, componentwise. -/
def localRelabellingInv (h : LocalRelabelling) : LocalRelabelling :=
  (h.1.symm, (h.2.1.symm, h.2.2.symm))

/-- Pullback action on `SceneC1 = SceneEdge → ℚ`, written componentwise. -/
def sceneAction (h : LocalRelabelling) (X : SceneC1) : SceneC1 :=
  fun e => X (edgeRelabel (localRelabellingInv h) e)

/-- Pullback action on vertex fields. -/
def vertexAction (h : LocalRelabelling) (A : SceneC0) : SceneC0
  | Sum.inl x => A (Sum.inl (h.1.symm x))
  | Sum.inr (Sum.inl y) => A (Sum.inr (Sum.inl (h.2.1.symm y)))
  | Sum.inr (Sum.inr z) => A (Sum.inr (Sum.inr (h.2.2.symm z)))

/-- Literal unsigned A1 Weyl/Ward endpoint-sum operator. -/
def BPlus (X : SceneC1) : SceneC0 := fun v =>
  match v with
  | Sum.inl x =>
      (∑ y : V11T, X (Sum.inl (x, y))) +
        ∑ z : V13T, X (Sum.inr (Sum.inl (x, z)))
  | Sum.inr (Sum.inl y) =>
      (∑ x : V9T, X (Sum.inl (x, y))) +
        ∑ z : V13T, X (Sum.inr (Sum.inr (y, z)))
  | Sum.inr (Sum.inr z) =>
      (∑ x : V9T, X (Sum.inr (Sum.inl (x, z)))) +
        ∑ y : V11T, X (Sum.inr (Sum.inr (y, z)))

/-- Literal signed incidence/current divergence for `9 → 11 → 13`. -/
def BMinus (X : SceneC1) : SceneC0 := fun v =>
  match v with
  | Sum.inl x =>
      -(∑ y : V11T, X (Sum.inl (x, y))) -
        ∑ z : V13T, X (Sum.inr (Sum.inl (x, z)))
  | Sum.inr (Sum.inl y) =>
      (∑ x : V9T, X (Sum.inl (x, y))) -
        ∑ z : V13T, X (Sum.inr (Sum.inr (y, z)))
  | Sum.inr (Sum.inr z) =>
      (∑ x : V9T, X (Sum.inr (Sum.inl (x, z)))) +
        ∑ y : V11T, X (Sum.inr (Sum.inr (y, z)))

/-- Matrix form of the unsigned A1 endpoint-sum operator. -/
def BPlusMatrix : Matrix SceneVertex SceneEdge ℚ
  | Sum.inl x, Sum.inl (x', _) => if x = x' then 1 else 0
  | Sum.inl x, Sum.inr (Sum.inl (x', _)) => if x = x' then 1 else 0
  | Sum.inl _, Sum.inr (Sum.inr _) => 0
  | Sum.inr (Sum.inl y), Sum.inl (_, y') => if y = y' then 1 else 0
  | Sum.inr (Sum.inl y), Sum.inr (Sum.inl _) => 0
  | Sum.inr (Sum.inl y), Sum.inr (Sum.inr (y', _)) => if y = y' then 1 else 0
  | Sum.inr (Sum.inr _), Sum.inl _ => 0
  | Sum.inr (Sum.inr z), Sum.inr (Sum.inl (_, z')) => if z = z' then 1 else 0
  | Sum.inr (Sum.inr z), Sum.inr (Sum.inr (_, z')) => if z = z' then 1 else 0

def BPlusLin : SceneC1 →ₗ[ℚ] SceneC0 := BPlusMatrix.mulVecLin

theorem BPlus_transpose_injective :
    Function.Injective BPlusMatrix.transpose.mulVecLin := by
  rw [injective_iff_map_eq_zero]
  intro xi hxi
  funext v
  rcases v with x | yz
  · have h1 := congrFun hxi (Sum.inl (x, (0 : V11T)))
    have h2 := congrFun hxi (Sum.inr (Sum.inl (x, (0 : V13T))))
    have h3 := congrFun hxi (Sum.inr (Sum.inr ((0 : V11T), (0 : V13T))))
    dsimp [Matrix.mulVecLin_apply, Matrix.mulVec, dotProduct, transpose_apply, BPlusMatrix] at h1 h2 h3
    simp only [Fintype.sum_sum_type, Finset.sum_const_zero, add_zero, zero_add, mul_ite, mul_one, mul_zero, zero_mul] at h1 h2 h3
    simp only [Fintype.sum_prod_type, Fintype.sum_ite_eq] at h1 h2 h3
    linarith
  · rcases yz with y | z
    · have h1 := congrFun hxi (Sum.inl ((0 : V9T), y))
      have h2 := congrFun hxi (Sum.inr (Sum.inr (y, (0 : V13T))))
      have h3 := congrFun hxi (Sum.inr (Sum.inl ((0 : V9T), (0 : V13T))))
      dsimp [Matrix.mulVecLin_apply, Matrix.mulVec, dotProduct, transpose_apply, BPlusMatrix] at h1 h2 h3
      simp only [Fintype.sum_sum_type, Finset.sum_const_zero, add_zero, zero_add, mul_ite, mul_one, mul_zero, zero_mul] at h1 h2 h3
      simp only [Fintype.sum_prod_type, Fintype.sum_ite_eq] at h1 h2 h3
      linarith
    · have h1 := congrFun hxi (Sum.inr (Sum.inl ((0 : V9T), z)))
      have h2 := congrFun hxi (Sum.inr (Sum.inr ((0 : V11T), z)))
      have h3 := congrFun hxi (Sum.inl ((0 : V9T), (0 : V11T)))
      dsimp [Matrix.mulVecLin_apply, Matrix.mulVec, dotProduct, transpose_apply, BPlusMatrix] at h1 h2 h3
      simp only [Fintype.sum_sum_type, Finset.sum_const_zero, add_zero, zero_add, mul_ite, mul_one, mul_zero, zero_mul] at h1 h2 h3
      simp only [Fintype.sum_prod_type, Fintype.sum_ite_eq] at h1 h2 h3
      linarith

/-- The signless map has full row rank `33`. -/
theorem BPlus_rank : Matrix.rank BPlusMatrix = 33 := by
  rw [Matrix.rank_transpose, Matrix.rank]
  rw [LinearMap.range_eq_top.mpr BPlus_transpose_injective]
  rw [Module.finrank_fintype_fun_eq_card]
  simp [GenericVertex]

/-- The actual unsigned linear owner has kernel dimension `326`. -/
theorem BPlus_kernel_finrank :
    Module.finrank ℚ (LinearMap.ker BPlusLin) = 326 := by
  have h := LinearMap.finrank_range_add_finrank_ker BPlusLin
  have hdom : Module.finrank ℚ SceneC1 = 359 := by
    rw [Module.finrank_fintype_fun_eq_card]
    exact scene_carrier_cardinalities.2.1
  have hrange : Module.finrank ℚ (LinearMap.range BPlusLin) = 33 := by
    simpa [BPlusLin, Matrix.rank] using BPlus_rank
  rw [hrange, hdom] at h
  omega

/-- The explicit C1 carrier map. -/
def U (X : SceneC1) : SceneC1 := fun e =>
  match e with
  | Sum.inl _ => X e
  | Sum.inr (Sum.inl _) => X e
  | Sum.inr (Sum.inr (y, _)) =>
      X e - (2 / 13 : ℚ) *
        ((∑ z' : V13T, X (Sum.inr (Sum.inr (y, z')))) -
          (1 / 11 : ℚ) *
            ∑ y' : V11T, ∑ z' : V13T,
              X (Sum.inr (Sum.inr (y', z'))))

/-- `U` is a linear operator on `SceneC1`. -/
def ULin : SceneC1 →ₗ[ℚ] SceneC1 where
  toFun := U
  map_add' X Y := by funext e; rcases e with ⟨x, y⟩ | ⟨x, z⟩ | ⟨y, z⟩ <;> (dsimp [U]; simp; ring)
  map_smul' r X := by funext e; rcases e with ⟨x, y⟩ | ⟨x, z⟩ | ⟨y, z⟩ <;> (dsimp [U]; simp; ring)

theorem U_involutive (X : SceneC1) : U (U X) = X := by
  funext e
  rcases e with ⟨x, y⟩ | ⟨x, z⟩ | ⟨y, z⟩
  · rfl
  · rfl
  · simp only [U]
    let Ry (f : SceneC1) (y' : V11T) := ∑ z' : V13T, f (Sum.inr (Sum.inr (y', z')))
    let T (f : SceneC1) := ∑ y' : V11T, Ry f y'
    have hRy : ∀ y', Ry (U X) y' = Ry X y' - (2 / 13) * (13 * Ry X y' - (13 / 11) * T X) := by
      intro y'
      simp only [Ry, U]
      rw [Finset.sum_sub_distrib, Finset.sum_const]
      simp only [Finset.card_fin, nsmul_eq_mul]
      ring
    have hRy_simp : ∀ y', Ry (U X) y' = -Ry X y' + (2 / 11) * T X := by
      intro y'
      rw [hRy y']
      ring
    have hT : T (U X) = -T X + (2 / 11) * (11 * T X) := by
      simp only [T, hRy_simp]
      rw [Finset.sum_add_distrib, Finset.sum_const, Finset.sum_neg_distrib]
      simp only [Finset.card_fin, nsmul_eq_mul]
      ring
    have hT_simp : T (U X) = T X := by rw [hT]; ring
    simp only [hRy_simp, hT_simp]
    ring

/-- Standard inner product on `SceneC1`. -/
def inner (X Y : SceneC1) : ℚ := ∑ e, X e * Y e

/-- `U` is an isometry with respect to the standard inner product. -/
theorem U_isometry (X Y : SceneC1) : inner (U X) (U Y) = inner X Y := by
  simp only [inner, U, Fintype.sum_sum_type]
  congr 1; congr 1
  let Sz (f : SceneC1) (y : V11T) := ∑ z : V13T, f (Sum.inr (Sum.inr (y, z)))
  let Tz (f : SceneC1) := ∑ y : V11T, Sz f y
  have h_block : ∑ y : V11T, ∑ z : V13T,
      (X (Sum.inr (Sum.inr (y, z))) - (2 / 13) * (Sz X y - (1 / 11) * Tz X)) *
      (Y (Sum.inr (Sum.inr (y, z))) - (2 / 13) * (Sz Y y - (1 / 11) * Tz Y)) =
      ∑ y : V11T, ∑ z : V13T, X (Sum.inr (Sum.inr (y, z))) * Y (Sum.inr (Sum.inr (y, z))) := by
    simp only [sub_mul, mul_sub]
    rw [Finset.sum_sub_distrib, Finset.sum_sub_distrib, Finset.sum_add_distrib]
    simp only [Finset.sum_mul, Finset.mul_sum]
    simp only [Finset.sum_const, Finset.card_fin, nsmul_eq_mul]
    simp only [Sz, Tz]
    field_simp
    ring
  exact h_block

/-- The block-constant signed cycle mode. -/
def omega : SceneC1 := fun e =>
  match e with
  | Sum.inl _ => 13
  | Sum.inr (Sum.inl _) => -11
  | Sum.inr (Sum.inr _) => 9

theorem omega_norm : ∑ e : SceneEdge, (omega e) ^ 2 = 42471 := by native_decide

theorem omega_BMinus_zero : BMinus omega = 0 := by
  funext v; rcases v with x | yz <;> (simp [BMinus, omega, Finset.sum_const]; ring)

/-- Orthogonality to the block-constant mode. -/
def omega_perp (X : SceneC1) : Prop := inner X omega = 0

theorem T_of_omega_perp_ker_BMinus {X : SceneC1} (hB : BMinus X = 0) (hO : omega_perp X) :
    ∑ y : V11T, ∑ z : V13T, X (Sum.inr (Sum.inr (y, z))) = 0 := by
  let Sx := ∑ x : V9T, ∑ y : V11T, X (Sum.inl (x, y))
  let Sy := ∑ x : V9T, ∑ z : V13T, X (Sum.inr (Sum.inl (x, z)))
  let Sz := ∑ y : V11T, ∑ z : V13T, X (Sum.inr (Sum.inr (y, z)))
  have h1 : Sx + Sy = 0 := by
    have h : ∑ x, BMinus X (Sum.inl x) = 0 := by simp [hB]
    simp [BMinus, Finset.sum_add_distrib, Finset.sum_neg_distrib] at h
    exact neg_eq_zero.mp h
  have h2 : Sx - Sz = 0 := by
    have h : ∑ y, BMinus X (Sum.inr (Sum.inl y)) = 0 := by simp [hB]
    simp [BMinus, Finset.sum_add_distrib, Finset.sum_sub_distrib] at h
    exact h
  have h3 : 13 * Sx - 11 * Sy + 9 * Sz = 0 := by
    simp [omega_perp, omega, inner, Fintype.sum_sum_type, Finset.sum_mul, mul_comm] at hO
    exact hO
  linarith

theorem U_maps_ker_BMinus_to_ker_BPlus {X : SceneC1} (hB : BMinus X = 0) (hO : omega_perp X) :
    BPlus (U X) = 0 := by
  have hT := T_of_omega_perp_ker_BMinus hB hO
  funext v
  rcases v with x | yz
  · simp [BPlus, U, hB, Sum.inl]
    have h := congrFun hB (Sum.inl x)
    simp [BMinus] at h; exact neg_eq_zero.mp h
  · rcases yz with y | z
    · simp [BPlus, U, hB, hT]
      have h := congrFun hB (Sum.inr (Sum.inl y))
      simp [BMinus] at h
      let Ry := ∑ z' : V13T, X (Sum.inr (Sum.inr (y, z')))
      have hsum : ∑ z : V13T, (X (Sum.inr (Sum.inr (y, z))) - (2 / 13) * Ry) = -Ry := by
        rw [Finset.sum_sub_distrib, Finset.sum_const]; simp [Ry]; ring
      rw [hsum]; exact h
    · simp [BPlus, U, hB]; have h := congrFun hB (Sum.inr (Sum.inr z)); simp [BMinus] at h; exact h

theorem U_maps_ker_BPlus_to_ker_BMinus {X : SceneC1} (hB : BPlus X = 0) :
    BMinus (U X) = 0 ∧ omega_perp (U X) := by
  have hSx : (∑ x, ∑ y, X (Sum.inl (x, y))) = 0 := by
    have h : ∑ x, BPlus X (Sum.inl x) = 0 := by simp [hB]
    simp [BPlus, Finset.sum_add_distrib] at h
    let Sx := ∑ x, ∑ y, X (Sum.inl (x, y))
    let Sy := ∑ x, ∑ z, X (Sum.inr (Sum.inl (x, z)))
    have h1 : Sx + Sy = 0 := h
    have h2 : Sx + (∑ y, ∑ z, X (Sum.inr (Sum.inr (y, z)))) = 0 := by
      have hh : ∑ y, BPlus X (Sum.inr (Sum.inl y)) = 0 := by simp [hB]
      simp [BPlus, Finset.sum_add_distrib] at hh; exact hh
    have h3 : Sy + (∑ y, ∑ z, X (Sum.inr (Sum.inr (y, z)))) = 0 := by
      have hh : ∑ z, BPlus X (Sum.inr (Sum.inr z)) = 0 := by simp [hB]
      simp [BPlus, Finset.sum_add_distrib] at hh; exact hh
    linarith
  have hSy : (∑ x, ∑ z, X (Sum.inr (Sum.inl (x, z)))) = 0 := by
    have h : ∑ x, BPlus X (Sum.inl x) = 0 := by simp [hB]
    simp [BPlus, Finset.sum_add_distrib] at h; linarith
  have hSz : (∑ y, ∑ z, X (Sum.inr (Sum.inr (y, z)))) = 0 := by
    have h : ∑ y, BPlus X (Sum.inr (Sum.inl y)) = 0 := by simp [hB]
    simp [BPlus, Finset.sum_add_distrib] at h; linarith
  have hT : (∑ y', ∑ z', X (Sum.inr (Sum.inr (y', z')))) = 0 := hSz
  constructor
  · funext v
    rcases v with x | yz
    · simp [BMinus, U, hB, Sum.inl]
      have h := congrFun hB (Sum.inl x); simp [BPlus] at h; exact neg_eq_zero.mpr h
    · rcases yz with y | z
      · simp [BMinus, U, hB, hT]
        have h := congrFun hB (Sum.inr (Sum.inl y)); simp [BPlus] at h
        let Ry := ∑ z' : V13T, X (Sum.inr (Sum.inr (y, z')))
        have hsum : ∑ z : V13T, (X (Sum.inr (Sum.inr (y, z))) - (2 / 13) * Ry) = -Ry := by
          rw [Finset.sum_sub_distrib, Finset.sum_const]; simp [Ry]; ring
        rw [hsum]; linarith
      · simp [BMinus, U, hB]; have h := congrFun hB (Sum.inr (Sum.inr z)); simp [BPlus] at h; exact h
  · simp [omega_perp, omega, inner, Fintype.sum_sum_type, Finset.sum_mul, mul_comm]
    have hUz : ∑ y, ∑ z, (U X (Sum.inr (Sum.inr (y, z)))) = 0 := by
      simp [U, hT]; exact hSz
    simp [U] at hUz; linarith

/-- The kernel mapping isomorphism theorem. -/
theorem ker_BPlus_iso_ker_BMinus_perp :
    LinearMap.ker BPlusLin ≃ₗ[ℚ] {Y : SceneC1 // BMinus Y = 0 ∧ omega_perp Y} where
  toFun X := ⟨U X, (U_maps_ker_BPlus_to_ker_BMinus (LinearMap.mem_ker.mp X.2)).1,
                  (U_maps_ker_BPlus_to_ker_BMinus (LinearMap.mem_ker.mp X.2)).2⟩
  map_add' X Y := by ext; simp [ULin]; exact ULin.map_add X Y
  map_smul' r X := by ext; simp [ULin]; exact ULin.map_smul r X
  invFun Y := ⟨U Y.1, by
    have h := U_maps_ker_BMinus_to_ker_BPlus Y.2.1 Y.2.2
    exact LinearMap.mem_ker.mpr h⟩
  left_inv X := by ext; exact U_involutive X
  right_inv Y := by ext; exact U_involutive Y

/-- Projection onto the matter-gravity sector. -/
def Pmg (Y : SceneC1) : SceneC1 := Y - ((inner Y omega) / 42471) • omega

theorem Pmg_omega_perp (Y : SceneC1) : omega_perp (Pmg Y) := by
  unfold omega_perp; simp only [Pmg, Pi.sub_apply, Pi.smul_apply, inner, smul_eq_mul]
  simp only [Finset.sum_sub_distrib, Finset.sum_mul]
  rw [show ∑ e, (inner Y omega / 42471 * omega e) * omega e =
    (inner Y omega / 42471) * ∑ e, omega e * omega e by
      simp only [mul_assoc]; rw [Finset.mul_sum]; congr]
  rw [omega_norm]; simp only [inner]; field_simp; ring

theorem ker_BMinus_decomposition (Y : SceneC1) (hY : BMinus Y = 0) :
    Y = Pmg Y + ((inner Y omega) / 42471) • omega ∧
    BMinus (Pmg Y) = 0 ∧ omega_perp (Pmg Y) := by
  constructor
  · simp [Pmg]
  · constructor
    · simp [Pmg, hY, omega_BMinus_zero]
    · exact Pmg_omega_perp Y

theorem Pmg_omega : Pmg omega = 0 := by unfold Pmg; simp [inner, omega_norm]

theorem Pmg_eq_self_of_omega_perp {Y : SceneC1} (h : omega_perp Y) : Pmg Y = Y := by
  unfold Pmg; simp [inner]; have h' : inner Y omega = 0 := h; rw [h']; simp

theorem Pmg_idempotent (Y : SceneC1) : Pmg (Pmg Y) = Pmg Y :=
  Pmg_eq_self_of_omega_perp (Pmg_omega_perp Y)

/-- Sum functional on the zone-11 coefficient space. -/
def rowCoeffSum : (V11T → ℚ) →ₗ[ℚ] ℚ where
  toFun a := ∑ y, a y
  map_add' a b := Finset.sum_add_distrib
  map_smul' r a := by simp [Finset.mul_sum]

/-- The centered coefficient subspace. -/
def CenteredRowCoeff : Submodule ℚ (V11T → ℚ) := LinearMap.ker rowCoeffSum

theorem CenteredRowCoeff_finrank : Module.finrank ℚ CenteredRowCoeff = 10 := by
  have h_range : LinearMap.range rowCoeffSum = ⊤ := by
    rw [LinearMap.range_eq_top]; intro r; use fun _ => r / 11
    dsimp [rowCoeffSum]; rw [Finset.sum_const, Finset.card_fin]; simp [nsmul_eq_mul]
  have h := LinearMap.finrank_range_add_finrank_ker rowCoeffSum
  rw [h_range, finrank_top, Module.finrank_self] at h
  have h_dom : Module.finrank ℚ (V11T → ℚ) = 11 := by rw [Module.finrank_fintype_fun_eq_card]; simp
  rw [h_dom] at h; omega

/-- Embedding of centered coefficients into the edge space. -/
def rowCorrectionEmbed : CenteredRowCoeff →ₗ[ℚ] SceneC1 where
  toFun a e := match e with
    | Sum.inl _ => 0
    | Sum.inr (Sum.inl _) => 0
    | Sum.inr (Sum.inr (y, _)) => a.1 y
  map_add' a b := by funext e; rcases e with ⟨x, y⟩ | ⟨x, z⟩ | ⟨y, z⟩ <;> (dsimp; simp; try rfl)
  map_smul' r a := by funext e; rcases e with ⟨x, y⟩ | ⟨x, z⟩ | ⟨y, z⟩ <;> (dsimp; simp; try rfl)

theorem rowCorrectionEmbed_injective : Function.Injective rowCorrectionEmbed := by
  rw [← LinearMap.ker_eq_bot, LinearMap.ker_eq_bot']; intro a ha; ext y
  have h := congrFun ha (Sum.inr (Sum.inr (y, 0))); simpa using h

/-- The rank-10 space of centered row corrections on (11,13). -/
def RowCorrectionSpace : Submodule ℚ SceneC1 := LinearMap.range rowCorrectionEmbed

theorem RowCorrectionSpace_finrank : Module.finrank ℚ RowCorrectionSpace = 10 := by
  rw [RowCorrectionSpace, LinearMap.finrank_range_of_inj rowCorrectionEmbed_injective]
  exact CenteredRowCoeff_finrank

theorem U_minus_I_in_RowCorrectionSpace (X : SceneC1) : U X - X ∈ RowCorrectionSpace := by
  let a : V11T → ℚ := fun y => -(2 / 13) * (
    (∑ z', X (Sum.inr (Sum.inr (y, z')))) -
    (1 / 11) * ∑ y', ∑ z', X (Sum.inr (Sum.inr (y', z')))
  )
  have ha : a ∈ CenteredRowCoeff := by
    rw [CenteredRowCoeff, LinearMap.mem_ker]; dsimp [rowCoeffSum, a]
    simp only [Finset.sum_neg_distrib, Finset.mul_sum, Finset.sum_sub_distrib]
    simp only [Finset.sum_const, Finset.card_fin, nsmul_eq_mul]; field_simp; ring
  use ⟨a, ha⟩; funext e; rcases e with ⟨x, y⟩ | ⟨x, z⟩ | ⟨y, z⟩
  · simp [U]; rfl
  · simp [U]; rfl
  · simp [U, rowCorrectionEmbed, a]; ring

end D0.Geometry.SignlessSignedCommonCarrier

open D0.Geometry.SignlessSignedCommonCarrier
#print axioms BMinus_eq_sceneBoundary1_mulVec
#print axioms BMinus_kernel_finrank
#print axioms BPlus_rank
#print axioms BPlus_kernel_finrank
#print axioms U_involutive
#print axioms U_isometry
#print axioms ker_BPlus_iso_ker_BMinus_perp
#print axioms ker_BMinus_decomposition
#print axioms CenteredRowCoeff_finrank
#print axioms RowCorrectionSpace_finrank
#print axioms Pmg_idempotent
#print axioms D0.Topology.GenericTripartiteHomology.boundary1_rank
#print axioms D0.Topology.GenericTripartiteHomology.boundary2_rank
