import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Real.Basic
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Tactic
import D0.Geometry.SceneSourceStratification

/-!
# D0.Geometry.SignlessSignedCommonCarrier

This module owns the literal finite C1 carrier for the scene `K(9,11,13)`.
`BPlus` is the unsigned endpoint-sum/Weyl-Ward operator.  `BMinus` is the
signed current-divergence operator, and its equality with the accepted scene
incidence owner is proved explicitly.  The carrier map below is a Euclidean
isometry between the unsigned kernel and the signed kernel with the accepted
`omega_scene` line removed.

No TT, graviton, continuum Einstein, quadratic matter source, or selector
theorem is claimed here.
-/

namespace D0.Geometry.SignlessSignedCommonCarrier

open BigOperators Matrix
open D0.Geometry.SceneCochainComplex
open D0.Geometry.SceneHodgeDecomposition
open D0.Geometry.SceneSourceStratification

abbrev V9 := Fin 9
abbrev V11 := Fin 11
abbrev V13 := Fin 13
abbrev EdgeCochain := SceneCochainComplex.SceneC1
abbrev VertexCochain := SceneCochainComplex.SceneC0

private theorem sum_indicator_fst_one {α β : Type} [Fintype α] [Fintype β]
    [DecidableEq α] (f : α × β → ℚ) (a : α) :
    (∑ x : α × β, (if a = x.1 then (1 : ℚ) else 0) * f x) =
      ∑ b : β, f (a, b) := by
  rw [Fintype.sum_prod_type]
  calc
    (∑ x : α, ∑ y : β, (if a = x then (1 : ℚ) else 0) * f (x, y)) =
        ∑ x : α, if a = x then ∑ y : β, f (x, y) else 0 := by
      apply Fintype.sum_congr
      intro x
      by_cases h : a = x <;> simp [h]
    _ = ∑ b : β, f (a, b) := by
      simpa using Fintype.sum_ite_eq a (fun x : α => ∑ y : β, f (x, y))

private theorem sum_indicator_fst_neg {α β : Type} [Fintype α] [Fintype β]
    [DecidableEq α] (f : α × β → ℚ) (a : α) :
    (∑ x : α × β, (if a = x.1 then (-1 : ℚ) else 0) * f x) =
      -(∑ b : β, f (a, b)) := by
  rw [Fintype.sum_prod_type]
  calc
    (∑ x : α, ∑ y : β, (if a = x then (-1 : ℚ) else 0) * f (x, y)) =
        ∑ x : α, if a = x then -(∑ y : β, f (x, y)) else 0 := by
      apply Fintype.sum_congr
      intro x
      by_cases h : a = x <;> simp [h]
    _ = -(∑ b : β, f (a, b)) := by
      simpa using Fintype.sum_ite_eq a
        (fun x : α => -(∑ y : β, f (x, y)))

private theorem sum_indicator_snd_one {α β : Type} [Fintype α] [Fintype β]
    [DecidableEq β] (f : α × β → ℚ) (b : β) :
    (∑ x : α × β, (if b = x.2 then (1 : ℚ) else 0) * f x) =
      ∑ a : α, f (a, b) := by
  rw [Fintype.sum_prod_type]
  apply Fintype.sum_congr
  intro a
  simpa using Fintype.sum_ite_eq b (fun y : β => f (a, y))

private theorem sum_indicator_snd_neg {α β : Type} [Fintype α] [Fintype β]
    [DecidableEq β] (f : α × β → ℚ) (b : β) :
    (∑ x : α × β, (if b = x.2 then (-1 : ℚ) else 0) * f x) =
      -(∑ a : α, f (a, b)) := by
  calc
    (∑ x : α × β, (if b = x.2 then (-1 : ℚ) else 0) * f x) =
        -(∑ x : α × β, (if b = x.2 then (1 : ℚ) else 0) * f x) := by
      rw [← Finset.sum_neg_distrib]
      apply Finset.sum_congr rfl
      intro x hx
      by_cases h : b = x.2 <;> simp [h]
    _ = -(∑ a : α, f (a, b)) := by rw [sum_indicator_snd_one]

private theorem sum_ite_reversed {α : Type} [Fintype α] [DecidableEq α]
    (f : α → ℚ) (a : α) :
    (∑ x : α, if x = a then f x else 0) = f a := by
  simpa [eq_comm] using Fintype.sum_ite_eq a f

/-- The unsigned endpoint-sum/Weyl-Ward operator. -/
def BPlus (X : EdgeCochain) : VertexCochain := fun v =>
  match v with
  | Sum.inl x =>
      (∑ y : V11, X (Sum.inl (x, y))) +
        ∑ z : V13, X (Sum.inr (Sum.inl (x, z)))
  | Sum.inr (Sum.inl y) =>
      (∑ x : V9, X (Sum.inl (x, y))) +
        ∑ z : V13, X (Sum.inr (Sum.inr (y, z)))
  | Sum.inr (Sum.inr z) =>
      (∑ x : V9, X (Sum.inr (Sum.inl (x, z)))) +
        ∑ y : V11, X (Sum.inr (Sum.inr (y, z)))

/-- Matrix-backed unsigned operator on the literal edge carrier. -/
def BPlusMatrix : Matrix SceneVertex SceneEdge ℚ
  | Sum.inl x, Sum.inl (x', _) => if x = x' then 1 else 0
  | Sum.inl x, Sum.inr (Sum.inl (x', _)) => if x = x' then 1 else 0
  | Sum.inl _, Sum.inr (Sum.inr _) => 0
  | Sum.inr (Sum.inl y), Sum.inl (_, y') => if y = y' then 1 else 0
  | Sum.inr (Sum.inl _), Sum.inr (Sum.inl _) => 0
  | Sum.inr (Sum.inl y), Sum.inr (Sum.inr (y', _)) => if y = y' then 1 else 0
  | Sum.inr (Sum.inr _), Sum.inl _ => 0
  | Sum.inr (Sum.inr z), Sum.inr (Sum.inl (_, z')) => if z = z' then 1 else 0
  | Sum.inr (Sum.inr z), Sum.inr (Sum.inr (_, z')) => if z = z' then 1 else 0

def BPlusLin : EdgeCochain →ₗ[ℚ] VertexCochain := BPlusMatrix.mulVecLin

theorem BPlusMatrix_mulVec_eq (X : EdgeCochain) :
    BPlusMatrix.mulVec X = BPlus X := by
  funext v
  rcases v with x | yz
  · simp only [BPlus, Matrix.mulVec, dotProduct, BPlusMatrix,
      Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
      add_zero, zero_add]
    rw [sum_indicator_fst_one, sum_indicator_fst_one]
  · rcases yz with y | z
    · simp only [BPlus, Matrix.mulVec, dotProduct, BPlusMatrix,
        Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
        add_zero, zero_add]
      rw [sum_indicator_snd_one, sum_indicator_fst_one]
    · simp only [BPlus, Matrix.mulVec, dotProduct, BPlusMatrix,
        Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
        add_zero, zero_add]
      rw [sum_indicator_snd_one, sum_indicator_snd_one]

theorem BPlusLin_apply (X : EdgeCochain) : BPlusLin X = BPlus X := by
  change BPlusMatrix.mulVec X = BPlus X
  exact BPlusMatrix_mulVec_eq X

/-- The signed current divergence, initially written independently of the
matrix owner so its literal sign convention is visible. -/
def BMinus (X : EdgeCochain) : VertexCochain := fun v =>
  match v with
  | Sum.inl x =>
      -(∑ y : V11, X (Sum.inl (x, y))) -
        ∑ z : V13, X (Sum.inr (Sum.inl (x, z)))
  | Sum.inr (Sum.inl y) =>
      (∑ x : V9, X (Sum.inl (x, y))) -
        ∑ z : V13, X (Sum.inr (Sum.inr (y, z)))
  | Sum.inr (Sum.inr z) =>
      (∑ x : V9, X (Sum.inr (Sum.inl (x, z)))) +
        ∑ y : V11, X (Sum.inr (Sum.inr (y, z)))

theorem BMinus_eq_sceneBoundary1_mulVec (X : EdgeCochain) :
    BMinus X = sceneBoundary1.mulVec X := by
  funext v
  rcases v with x | yz
  · simp only [BMinus, Matrix.mulVec, dotProduct, sceneBoundary1,
      D0.Topology.GenericTripartiteHomology.boundary1,
      Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
      add_zero, zero_add]
    rw [sum_indicator_fst_neg, sum_indicator_fst_neg]
    ring
  · rcases yz with y | z
    · simp only [BMinus, Matrix.mulVec, dotProduct, sceneBoundary1,
        D0.Topology.GenericTripartiteHomology.boundary1,
        Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
        add_zero, zero_add]
      rw [sum_indicator_snd_one, sum_indicator_fst_neg]
      ring
    · simp only [BMinus, Matrix.mulVec, dotProduct, sceneBoundary1,
        D0.Topology.GenericTripartiteHomology.boundary1,
        Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
        add_zero, zero_add]
      rw [sum_indicator_snd_one, sum_indicator_snd_one]

/-- The signed linear owner is the accepted scene incidence map. -/
def BMinusLin : EdgeCochain →ₗ[ℚ] VertexCochain := sceneBoundary1.mulVecLin

theorem BMinusLin_apply (X : EdgeCochain) : BMinusLin X = BMinus X := by
  rw [BMinus_eq_sceneBoundary1_mulVec]
  rfl

theorem BPlus_transpose_injective :
    Function.Injective BPlusMatrix.transpose.mulVecLin := by
  rw [injective_iff_map_eq_zero]
  intro hxi hzero
  funext v
  rcases v with x | yz
  · have hab := congrFun hzero (Sum.inl (x, (0 : V11)))
    have hac := congrFun hzero (Sum.inr (Sum.inl (x, (0 : V13))))
    have hbc := congrFun hzero
      (Sum.inr (Sum.inr ((0 : V11), (0 : V13))))
    rw [Matrix.mulVecLin_apply] at hab hac hbc
    simp only [Matrix.mulVec, dotProduct, transpose_apply, BPlusMatrix,
      Fintype.sum_sum_type, ite_mul, mul_ite, mul_one, mul_zero, zero_mul,
      Finset.sum_const_zero, eq_comm, Fintype.sum_ite_eq, sum_ite_reversed,
      Pi.zero_apply,
      add_zero, zero_add] at hab hac hbc
    norm_num at hab hac hbc
    change hxi (Sum.inl x) = 0
    linarith
  · rcases yz with y | z
    · have hab := congrFun hzero (Sum.inl ((0 : V9), y))
      have hbc := congrFun hzero
        (Sum.inr (Sum.inr (y, (0 : V13))))
      have hac := congrFun hzero
        (Sum.inr (Sum.inl ((0 : V9), (0 : V13))))
      rw [Matrix.mulVecLin_apply] at hab hbc hac
      simp only [Matrix.mulVec, dotProduct, transpose_apply, BPlusMatrix,
        Fintype.sum_sum_type, ite_mul, mul_ite, mul_one, mul_zero, zero_mul,
        Finset.sum_const_zero, eq_comm, Fintype.sum_ite_eq, sum_ite_reversed,
        Pi.zero_apply,
        add_zero, zero_add] at hab hbc hac
      norm_num at hab hbc hac
      change hxi (Sum.inr (Sum.inl y)) = 0
      linarith
    · have hac := congrFun hzero
        (Sum.inr (Sum.inl ((0 : V9), z)))
      have hbc := congrFun hzero
        (Sum.inr (Sum.inr ((0 : V11), z)))
      have hab := congrFun hzero
        (Sum.inl ((0 : V9), (0 : V11)))
      rw [Matrix.mulVecLin_apply] at hac hbc hab
      simp only [Matrix.mulVec, dotProduct, transpose_apply, BPlusMatrix,
        Fintype.sum_sum_type, ite_mul, mul_ite, mul_one, mul_zero, zero_mul,
        Finset.sum_const_zero, eq_comm, Fintype.sum_ite_eq, sum_ite_reversed,
        Pi.zero_apply,
        add_zero, zero_add] at hac hbc hab
      norm_num at hac hbc hab
      change hxi (Sum.inr (Sum.inr z)) = 0
      linarith

theorem BPlus_rank : Matrix.rank BPlusMatrix = 33 := by
  have hker : LinearMap.ker BPlusMatrix.transpose.mulVecLin = ⊥ :=
    LinearMap.ker_eq_bot.mpr BPlus_transpose_injective
  have h := LinearMap.finrank_range_add_finrank_ker
    BPlusMatrix.transpose.mulVecLin
  have hdom : Module.finrank ℚ VertexCochain = 33 := by
    rw [Module.finrank_fintype_fun_eq_card]
    exact scene_carrier_cardinalities.1
  have hrange : Module.finrank ℚ
      (LinearMap.range BPlusMatrix.transpose.mulVecLin) = 33 := by
    rw [hker] at h
    simpa [hdom] using h
  have htranspose : Matrix.rank BPlusMatrix.transpose = 33 := by
    simpa [Matrix.rank] using hrange
  rw [Matrix.rank_transpose] at htranspose
  exact htranspose

theorem BPlus_kernel_finrank :
    Module.finrank ℚ (LinearMap.ker BPlusLin) = 326 := by
  have h := LinearMap.finrank_range_add_finrank_ker BPlusLin
  have hdom : Module.finrank ℚ EdgeCochain = 359 := by
    rw [Module.finrank_fintype_fun_eq_card]
    exact scene_carrier_cardinalities.2.1
  have hrange : Module.finrank ℚ (LinearMap.range BPlusLin) = 33 := by
    simpa [BPlusLin, Matrix.rank] using BPlus_rank
  rw [hrange, hdom] at h
  omega

theorem BMinus_kernel_finrank :
    Module.finrank ℚ (LinearMap.ker BMinusLin) = 327 := by
  have h := LinearMap.finrank_range_add_finrank_ker BMinusLin
  have hdom : Module.finrank ℚ EdgeCochain = 359 := by
    rw [Module.finrank_fintype_fun_eq_card]
    exact scene_carrier_cardinalities.2.1
  have hrange : Module.finrank ℚ (LinearMap.range BMinusLin) = 32 := by
    simpa [BMinusLin, Matrix.rank] using scene_boundary_ranks.1
  rw [hrange, hdom] at h
  omega

/-- The explicit common-carrier map.  It is the identity on `(9,11)` and
`(9,13)`.  On `(11,13)` it subtracts the centered row correction
`(2/13) C₁₁ X 1 1ᵀ`. -/
def U (X : EdgeCochain) : EdgeCochain := fun e =>
  match e with
  | Sum.inl _ => X e
  | Sum.inr (Sum.inl _) => X e
  | Sum.inr (Sum.inr (y, _)) =>
      X e - (2 / 13 : ℚ) *
        ((∑ z' : V13, X (Sum.inr (Sum.inr (y, z')))) -
          (1 / 11 : ℚ) * ∑ y' : V11, ∑ z' : V13,
            X (Sum.inr (Sum.inr (y', z'))))

/-- `U` is linear over the common rational edge carrier. -/
def ULin : EdgeCochain →ₗ[ℚ] EdgeCochain where
  toFun := U
  map_add' X Y := by
    funext e
    rcases e with e | e | ⟨y, z⟩
    · rfl
    · rfl
    · simp only [U, Pi.add_apply, Finset.sum_add_distrib]
      ring
  map_smul' r X := by
    funext e
    rcases e with e | e | ⟨y, z⟩
    · rfl
    · rfl
    · simp only [U, Pi.smul_apply, smul_eq_mul, RingHom.id_apply]
      simp_rw [← Finset.mul_sum]
      ring

/-- The common-carrier map is an involution. -/
theorem U_involutive (X : EdgeCochain) : U (U X) = X := by
  funext e
  rcases e with e | e | ⟨y, z⟩
  · rfl
  · rfl
  ·
    let Ry (f : EdgeCochain) (y' : V11) :=
      ∑ z' : V13, f (Sum.inr (Sum.inr (y', z')))
    let T (f : EdgeCochain) := ∑ y' : V11, Ry f y'
    have hRy : ∀ y', Ry (U X) y' = Ry X y' - (2 / 13) *
        (13 * Ry X y' - (13 / 11) * T X) := by
      intro y'
      simp only [Ry, U, Finset.sum_sub_distrib, Finset.sum_const]
      simp only [Finset.card_fin, nsmul_eq_mul]
      ring
    have hRy_simp : ∀ y', Ry (U X) y' = -Ry X y' + (2 / 11) * T X := by
      intro y'
      rw [hRy y']
      ring
    have hT : T (U X) = -T X + (2 / 11) * (11 * T X) := by
      simp only [T, hRy_simp, Finset.sum_add_distrib, Finset.sum_const,
        Finset.sum_neg_distrib, Finset.card_fin, nsmul_eq_mul]
      ring
    have hT_simp : T (U X) = T X := by
      rw [hT]
      ring
    rw [show U (U X) (Sum.inr (Sum.inr (y, z))) =
        U X (Sum.inr (Sum.inr (y, z))) - (2 / 13 : ℚ) *
          ((∑ z' : V13, U X (Sum.inr (Sum.inr (y, z')))) -
            (1 / 11 : ℚ) * ∑ y' : V11, ∑ z' : V13,
              U X (Sum.inr (Sum.inr (y', z')))) by rfl,
      show U X (Sum.inr (Sum.inr (y, z))) =
        X (Sum.inr (Sum.inr (y, z))) - (2 / 13 : ℚ) *
          ((∑ z' : V13, X (Sum.inr (Sum.inr (y, z')))) -
            (1 / 11 : ℚ) * ∑ y' : V11, ∑ z' : V13,
              X (Sum.inr (Sum.inr (y', z')))) by rfl,
      show (∑ z' : V13, U X (Sum.inr (Sum.inr (y, z')))) = Ry (U X) y by rfl,
      show (∑ y' : V11, ∑ z' : V13,
          U X (Sum.inr (Sum.inr (y', z')))) = T (U X) by rfl,
      show (∑ z' : V13, X (Sum.inr (Sum.inr (y, z')))) = Ry X y by rfl,
      show (∑ y' : V11, ∑ z' : V13,
          X (Sum.inr (Sum.inr (y', z')))) = T X by rfl,
      hRy_simp y, hT_simp]
    ring

theorem ULin_involutive : ULin.comp ULin = LinearMap.id := by
  apply LinearMap.ext
  intro X
  exact U_involutive X

/-- The accepted block-constant signed cycle mode is reused verbatim. -/
theorem omega_scene_norm :
    inner1 omega_scene omega_scene = 42471 := by
  native_decide

theorem BMinus_omega_scene_zero : BMinus omega_scene = 0 := by
  rw [BMinus_eq_sceneBoundary1_mulVec]
  exact sceneBoundary1_mulVec_omega_scene

/-- Orthogonality to the accepted block-constant source mode. -/
def omegaPerp (X : EdgeCochain) : Prop :=
  inner1 X omega_scene = 0

private theorem T_of_omega_perp_ker_BMinus {X : EdgeCochain}
    (hB : BMinus X = 0) (hO : omegaPerp X) :
    ∑ y : V11, ∑ z : V13,
      X (Sum.inr (Sum.inr (y, z))) = 0 := by
  let Sx := ∑ x : V9, ∑ y : V11, X (Sum.inl (x, y))
  let Sy := ∑ x : V9, ∑ z : V13, X (Sum.inr (Sum.inl (x, z)))
  let Sz := ∑ y : V11, ∑ z : V13,
    X (Sum.inr (Sum.inr (y, z)))
  have h1 : Sx + Sy = 0 := by
    have h : ∑ x, BMinus X (Sum.inl x) = 0 := by
      simp [hB]
    simp [BMinus, Finset.sum_add_distrib, Finset.sum_neg_distrib] at h
    dsimp [Sx, Sy] at h ⊢
    linarith
  have h2 : Sx - Sz = 0 := by
    have h : ∑ y, BMinus X (Sum.inr (Sum.inl y)) = 0 := by
      simp [hB]
    simp [BMinus, Finset.sum_add_distrib, Finset.sum_sub_distrib] at h
    dsimp [Sx, Sz] at ⊢
    rw [Finset.sum_comm] at h
    exact h
  have h3 : 13 * Sx - 11 * Sy + 9 * Sz = 0 := by
    simp only [omegaPerp, inner1, omega_scene, Fintype.sum_sum_type,
      Fintype.sum_prod_type] at hO
    simp_rw [← Finset.sum_mul] at hO
    ring_nf at hO ⊢
    exact hO
  have hSy : Sy = -Sx := by linarith
  have hSz : Sz = Sx := by linarith
  linarith

private theorem U_col_sum (X : EdgeCochain) (z : V13) :
    (∑ y : V11, U X (Sum.inr (Sum.inr (y, z)))) =
      ∑ y : V11, X (Sum.inr (Sum.inr (y, z))) := by
  simp [U, Finset.sum_sub_distrib]
  simp_rw [mul_sub]
  rw [Finset.sum_sub_distrib]
  rw [show (∑ x : V11, (2 / 13 : ℚ) *
      ∑ z' : V13, X (Sum.inr (Sum.inr (x, z')))) =
      (2 / 13 : ℚ) * ∑ x : V11, ∑ z' : V13,
        X (Sum.inr (Sum.inr (x, z'))) by
    rw [Finset.mul_sum]]
  rw [show (∑ x : V11, (2 / 13 : ℚ) *
      (11⁻¹ * ∑ y' : V11, ∑ z' : V13,
        X (Sum.inr (Sum.inr (y', z'))))) =
      (2 / 13 : ℚ) * ∑ x : V11,
        (11⁻¹ * ∑ y' : V11, ∑ z' : V13,
          X (Sum.inr (Sum.inr (y', z')))) by
    simp only [Finset.mul_sum]]
  simp [Finset.sum_const, Finset.card_fin, nsmul_eq_mul]

/-- `U` sends the signed kernel, after removing the accepted source mode,
to the unsigned kernel. -/
theorem U_maps_ker_BMinus_to_ker_BPlus {X : EdgeCochain}
    (hB : BMinus X = 0) (hO : omegaPerp X) :
    BPlus (U X) = 0 := by
  have hT : (∑ y' : V11, ∑ z' : V13,
      X (Sum.inr (Sum.inr (y', z')))) = 0 :=
    T_of_omega_perp_ker_BMinus hB hO
  have hrow : ∀ y, (∑ z, U X (Sum.inr (Sum.inr (y, z)))) =
      -(∑ z, X (Sum.inr (Sum.inr (y, z)))) := by
    intro y
    simp [U, hT]
    ring
  have hglobal : (∑ y, ∑ z,
      U X (Sum.inr (Sum.inr (y, z)))) = 0 := by
    simp [U, hT]
    simp_rw [← Finset.mul_sum]
    linarith [hT]
  funext v
  rcases v with x | yz
  · change (∑ y, U X (Sum.inl (x, y))) +
      ∑ z, U X (Sum.inr (Sum.inl (x, z))) = 0
    have h := congrFun hB (Sum.inl x)
    simp [BMinus] at h
    have h' : (∑ y, X (Sum.inl (x, y))) +
        ∑ z, X (Sum.inr (Sum.inl (x, z))) = 0 := by
      linarith
    simpa [U] using h'
  · rcases yz with y | z
    · change (∑ x, U X (Sum.inl (x, y))) +
        ∑ z, U X (Sum.inr (Sum.inr (y, z))) = 0
      rw [hrow y]
      simpa [BMinus, U, sub_eq_add_neg] using
        congrFun hB (Sum.inr (Sum.inl y))
    · change (∑ x, U X (Sum.inr (Sum.inl (x, z)))) +
        ∑ y, U X (Sum.inr (Sum.inr (y, z))) = 0
      rw [U_col_sum]
      simp only [U]
      have h : BMinus X (Sum.inr (Sum.inr z)) = 0 :=
        congrFun hB (Sum.inr (Sum.inr z))
      simp [BMinus] at h
      linarith [h, hT]

/-- `U` sends the unsigned kernel to the signed kernel and makes its image
orthogonal to the accepted source mode. -/
theorem U_maps_ker_BPlus_to_ker_BMinus {X : EdgeCochain}
    (hB : BPlus X = 0) :
    BMinus (U X) = 0 ∧ omegaPerp (U X) := by
  have hSx : (∑ x, ∑ y, X (Sum.inl (x, y))) = 0 := by
    have h : ∑ x, BPlus X (Sum.inl x) = 0 := by simp [hB]
    simp [BPlus, Finset.sum_add_distrib] at h
    have h1 : (∑ x, ∑ y, X (Sum.inl (x, y))) +
        (∑ x, ∑ z, X (Sum.inr (Sum.inl (x, z)))) = 0 := by
      exact h
    have h2 : (∑ x, ∑ y, X (Sum.inl (x, y))) +
        (∑ y, ∑ z, X (Sum.inr (Sum.inr (y, z)))) = 0 := by
      have hh : ∑ y, BPlus X (Sum.inr (Sum.inl y)) = 0 := by simp [hB]
      simp [BPlus, Finset.sum_add_distrib] at hh
      rw [Finset.sum_comm] at hh
      exact hh
    have h3 : (∑ x, ∑ z, X (Sum.inr (Sum.inl (x, z)))) +
        (∑ y, ∑ z, X (Sum.inr (Sum.inr (y, z)))) = 0 := by
      have hh : ∑ z, BPlus X (Sum.inr (Sum.inr z)) = 0 := by simp [hB]
      simp [BPlus, Finset.sum_add_distrib] at hh
      have hswap : (∑ z : V13, ∑ x : V9,
          X (Sum.inr (Sum.inl (x, z)))) = ∑ x : V9, ∑ z : V13,
          X (Sum.inr (Sum.inl (x, z))) := by
        rw [Finset.sum_comm]
      have hswapBC : (∑ z : V13, ∑ y : V11,
          X (Sum.inr (Sum.inr (y, z)))) = ∑ y : V11, ∑ z : V13,
          X (Sum.inr (Sum.inr (y, z))) := by
        rw [Finset.sum_comm]
      rw [hswap, hswapBC] at hh
      exact hh
    linarith
  have hSy : (∑ x, ∑ z,
      X (Sum.inr (Sum.inl (x, z)))) = 0 := by
    have h : ∑ x, BPlus X (Sum.inl x) = 0 := by simp [hB]
    simp [BPlus, Finset.sum_add_distrib] at h
    linarith
  have hSz : (∑ y, ∑ z,
      X (Sum.inr (Sum.inr (y, z)))) = 0 := by
    have h : ∑ y, BPlus X (Sum.inr (Sum.inl y)) = 0 := by simp [hB]
    simp [BPlus, Finset.sum_add_distrib] at h
    have hswap : (∑ y : V11, ∑ x : V9,
        X (Sum.inl (x, y))) = ∑ x : V9, ∑ y : V11,
        X (Sum.inl (x, y)) := by
      rw [Finset.sum_comm]
    rw [hswap] at h
    have hh : (∑ x, ∑ y, X (Sum.inl (x, y))) +
        (∑ y, ∑ z, X (Sum.inr (Sum.inr (y, z)))) = 0 := by
      exact h
    linarith [hSx, hh]
  have hT : (∑ y', ∑ z',
      X (Sum.inr (Sum.inr (y', z')))) = 0 := hSz
  have hrow : ∀ y, (∑ z, U X (Sum.inr (Sum.inr (y, z)))) =
      -(∑ z, X (Sum.inr (Sum.inr (y, z)))) := by
    intro y
    simp [U, hT]
    ring
  have hglobal : (∑ y, ∑ z,
      U X (Sum.inr (Sum.inr (y, z)))) = 0 := by
    simp [U, hT]
    simp_rw [← Finset.mul_sum]
    linarith [hT]
  constructor
  · funext v
    rcases v with x | yz
    · change -(∑ y, U X (Sum.inl (x, y))) -
        ∑ z, U X (Sum.inr (Sum.inl (x, z))) = 0
      have h := congrFun hB (Sum.inl x)
      simp [BPlus] at h
      have h' : -(∑ y, X (Sum.inl (x, y))) -
          ∑ z, X (Sum.inr (Sum.inl (x, z))) = 0 := by
        linarith
      simpa [U] using h'
    · rcases yz with y | z
      · change (∑ x, U X (Sum.inl (x, y))) -
          ∑ z, U X (Sum.inr (Sum.inr (y, z))) = 0
        rw [hrow y]
        simpa [BPlus, U, sub_eq_add_neg] using
          congrFun hB (Sum.inr (Sum.inl y))
      · change (∑ x, U X (Sum.inr (Sum.inl (x, z)))) +
          ∑ y, U X (Sum.inr (Sum.inr (y, z))) = 0
        rw [U_col_sum]
        simp only [U]
        have h : BPlus X (Sum.inr (Sum.inr z)) = 0 :=
          congrFun hB (Sum.inr (Sum.inr z))
        simp [BPlus] at h
        linarith [h, hT]
  · change inner1 (U X) omega_scene = 0
    have hUSx : (∑ x, ∑ y, U X (Sum.inl (x, y))) = 0 := by
      simpa [U] using hSx
    have hUSy : (∑ x, ∑ z,
        U X (Sum.inr (Sum.inl (x, z)))) = 0 := by
      simpa [U] using hSy
    simp [inner1, omega_scene, Fintype.sum_sum_type,
      Fintype.sum_prod_type, Finset.sum_mul, mul_comm]
    simp_rw [← Finset.mul_sum]
    rw [hUSx, hUSy, hglobal]
    ring

/-- `U` preserves the standard rational inner product on the literal carrier. -/
theorem U_isometry (X Y : EdgeCochain) :
    inner1 (U X) (U Y) = inner1 X Y := by
  let A : V11 → V13 → ℚ := fun y z =>
    X (Sum.inr (Sum.inr (y, z)))
  let B : V11 → V13 → ℚ := fun y z =>
    Y (Sum.inr (Sum.inr (y, z)))
  let sx : V11 → ℚ := fun y => ∑ z, A y z
  let sy : V11 → ℚ := fun y => ∑ z, B y z
  let tx : ℚ := ∑ y, sx y
  let ty : ℚ := ∑ y, sy y
  let cx : V11 → ℚ := fun y => sx y - (1 / 11 : ℚ) * tx
  let cy : V11 → ℚ := fun y => sy y - (1 / 11 : ℚ) * ty
  have hsx : (∑ y, sx y) = tx := rfl
  have hsy : (∑ y, sy y) = ty := rfl
  have hBC :
      (∑ y : V11, ∑ z : V13,
        (A y z - (2 / 13 : ℚ) * cx y) *
          (B y z - (2 / 13 : ℚ) * cy y)) =
        (∑ y : V11, ∑ z : V13, A y z * B y z) := by
    have hscaleL (a : ℚ) (f : V11 → V13 → ℚ) :
        (∑ y, ∑ z, a * f y z) = a * ∑ y, ∑ z, f y z := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro y hy
      rw [Finset.mul_sum]
    have hscaleR (a : ℚ) (f : V11 → V13 → ℚ) :
        (∑ y, ∑ z, f y z * a) = a * ∑ y, ∑ z, f y z := by
      simpa [mul_comm] using hscaleL a f
    have hconstL (a : ℚ) (f : V11 → ℚ) :
        (∑ y, a * f y) = a * ∑ y, f y := by
      rw [Finset.mul_sum]
    have hconstR (a : ℚ) (f : V11 → ℚ) :
        (∑ y, f y * a) = a * ∑ y, f y := by
      simpa [mul_comm] using hconstL a f
    have hrowX :
        (∑ y, ∑ z, cx y * B y z) = ∑ y, cx y * sy y := by
      apply Finset.sum_congr rfl
      intro y hy
      simp only [sy]
      rw [Finset.mul_sum]
    have hrowY :
        (∑ y, ∑ z, A y z * cy y) = ∑ y, cy y * sx y := by
      apply Finset.sum_congr rfl
      intro y hy
      simp only [sx]
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro z hz
      ring
    have hcc :
        (∑ y : V11, ∑ z : V13, cx y * cy y) =
          13 * ∑ y : V11, cx y * cy y := by
      calc
        (∑ y : V11, ∑ z : V13, cx y * cy y) =
            ∑ y : V11, (13 : ℚ) * (cx y * cy y) := by
          apply Finset.sum_congr rfl
          intro y
          simp [Finset.sum_const, Finset.card_fin, nsmul_eq_mul]
        _ = 13 * ∑ y, cx y * cy y := by rw [Finset.mul_sum]
    have hcx : (∑ y, cx y) = 0 := by
      simp only [cx, Finset.sum_sub_distrib]
      rw [hsx]
      simp [Finset.sum_const, Finset.card_fin, nsmul_eq_mul]
    have hcy : (∑ y, cy y) = 0 := by
      simp only [cy, Finset.sum_sub_distrib]
      rw [hsy]
      simp [Finset.sum_const, Finset.card_fin, nsmul_eq_mul]
    have hcenter :
        (∑ y, cx y * sy y) = ∑ y, cy y * sx y := by
      simp only [cx, cy, sub_mul, Finset.sum_sub_distrib]
      have htx : (∑ y, (1 / 11 : ℚ) * tx * sy y) =
          (1 / 11 : ℚ) * tx * ty := by
        exact hconstL ((1 / 11 : ℚ) * tx) sy |>.trans
          (congrArg (fun q => (1 / 11 : ℚ) * tx * q) hsy)
      have hty : (∑ y, (1 / 11 : ℚ) * ty * sx y) =
          (1 / 11 : ℚ) * ty * tx := by
        exact hconstL ((1 / 11 : ℚ) * ty) sx |>.trans
          (congrArg (fun q => (1 / 11 : ℚ) * ty * q) hsx)
      have hsym : (∑ y, sx y * sy y) = ∑ y, sy y * sx y := by
        apply Finset.sum_congr rfl
        intro y hy
        ring
      rw [htx, hty]
      rw [hsym]
      rw [show (1 / 11 : ℚ) * tx * ty =
          (1 / 11 : ℚ) * ty * tx by ring]
    have hQ :
        (∑ y, cx y * sy y) = ∑ y, cx y * cy y := by
      simp only [cy, mul_sub, Finset.sum_sub_distrib]
      have hconst :
          (∑ y, cx y * ((1 / 11 : ℚ) * ty)) =
            (1 / 11 : ℚ) * ty * ∑ y, cx y := by
        exact hconstR ((1 / 11 : ℚ) * ty) cx
      rw [hconst, hcx]
      ring
    calc
      _ = (∑ y, ∑ z, A y z * B y z) -
          (∑ y, ∑ z, ((2 / 13 : ℚ) * cx y) * B y z) -
          (∑ y, ∑ z, A y z * ((2 / 13 : ℚ) * cy y)) +
          ∑ y, ∑ z, ((2 / 13 : ℚ) * cx y) *
            ((2 / 13 : ℚ) * cy y) := by
        simp only [sub_mul, mul_sub, Finset.sum_sub_distrib]
        ring
      _ = (∑ y, ∑ z, A y z * B y z) -
          (2 / 13 : ℚ) * (∑ y, ∑ z, cx y * B y z) -
          (2 / 13 : ℚ) * (∑ y, ∑ z, A y z * cy y) +
          (2 / 13 : ℚ) ^ 2 * (∑ y, ∑ z, cx y * cy y) := by
        have hscale1 :
            (∑ y, ∑ z, ((2 / 13 : ℚ) * cx y) * B y z) =
              (2 / 13 : ℚ) * (∑ y, ∑ z, cx y * B y z) := by
          calc
            _ = ∑ y, ∑ z, (2 / 13 : ℚ) * (cx y * B y z) := by
              apply Finset.sum_congr rfl
              intro y hy
              apply Finset.sum_congr rfl
              intro z hz
              ring
            _ = _ := hscaleL (2 / 13 : ℚ)
              (fun y z => cx y * B y z)
        have hscale2 :
            (∑ y, ∑ z, A y z * ((2 / 13 : ℚ) * cy y)) =
              (2 / 13 : ℚ) * (∑ y, ∑ z, A y z * cy y) := by
          calc
            _ = ∑ y, ∑ z, (2 / 13 : ℚ) * (A y z * cy y) := by
              apply Finset.sum_congr rfl
              intro y hy
              apply Finset.sum_congr rfl
              intro z hz
              ring
            _ = _ := hscaleL (2 / 13 : ℚ)
              (fun y z => A y z * cy y)
        have hscale3 :
            (∑ y : V11, ∑ z : V13, ((2 / 13 : ℚ) * cx y) *
              ((2 / 13 : ℚ) * cy y)) =
              (2 / 13 : ℚ) ^ 2 *
                (∑ y : V11, ∑ z : V13, cx y * cy y) := by
          calc
            _ = ∑ y, ∑ z, (2 / 13 : ℚ) ^ 2 * (cx y * cy y) := by
              apply Finset.sum_congr rfl
              intro y hy
              apply Finset.sum_congr rfl
              intro z hz
              ring
            _ = _ := hscaleL ((2 / 13 : ℚ) ^ 2)
              (fun y z => cx y * cy y)
        linear_combination -hscale1 - hscale2 + hscale3
      _ = ∑ y, ∑ z, A y z * B y z := by
        rw [hrowX, hrowY, hcc, ← hcenter, hQ]
        ring
    
  simp only [inner1, U, Fintype.sum_sum_type]
  congr 1
  congr 1
  simp only [Fintype.sum_prod_type, Prod.fst]
  simpa [A, B, sx, sy, tx, ty, cx, cy] using hBC

/-- The signed kernel sector orthogonal to the accepted source line. -/
def omegaFunctional : EdgeCochain →ₗ[ℚ] ℚ where
  toFun X := inner1 X omega_scene
  map_add' X Y := by
    simp only [inner1, Pi.add_apply, add_mul, Fintype.sum_sum_type,
      Fintype.sum_prod_type, Finset.sum_add_distrib]
  map_smul' r X := by
    simp only [inner1, Pi.smul_apply, smul_eq_mul, mul_assoc,
      Fintype.sum_sum_type, Fintype.sum_prod_type, RingHom.id_apply]
    simp_rw [← Finset.mul_sum]
    ring

def OmegaPerp : Submodule ℚ EdgeCochain :=
  LinearMap.ker omegaFunctional

def SignedOmegaPerp : Submodule ℚ EdgeCochain :=
  LinearMap.ker BMinusLin ⊓ OmegaPerp

/-- The actual linear equivalence between the two typed kernel sectors. -/
def ker_BPlus_iso_ker_BMinus_perp :
    LinearMap.ker BPlusLin ≃ₗ[ℚ] SignedOmegaPerp where
  toFun X := by
    have hB := LinearMap.mem_ker.mp X.2
    rw [BPlusLin_apply] at hB
    have h := U_maps_ker_BPlus_to_ker_BMinus hB
    refine ⟨U X, ?_⟩
    constructor
    · apply LinearMap.mem_ker.mpr
      rw [BMinusLin_apply]
      exact h.1
    · exact LinearMap.mem_ker.mpr h.2
  map_add' X Y := by
    apply Subtype.ext
    change U ((X : EdgeCochain) + Y) = U X + U Y
    exact ULin.map_add X Y
  map_smul' r X := by
    apply Subtype.ext
    change U (r • (X : EdgeCochain)) = r • U X
    exact ULin.map_smul r X
  invFun Y := by
    have hB := LinearMap.mem_ker.mp Y.2.1
    rw [BMinusLin_apply] at hB
    have hO : omegaPerp Y.1 := LinearMap.mem_ker.mp Y.2.2
    refine ⟨U Y.1, ?_⟩
    apply LinearMap.mem_ker.mpr
    rw [BPlusLin_apply]
    exact U_maps_ker_BMinus_to_ker_BPlus hB hO
  left_inv X := by
    apply Subtype.ext
    exact U_involutive X
  right_inv Y := by
    apply Subtype.ext
    exact U_involutive Y.1

/-- Orthogonal projection onto the signed kernel sector without `omega_scene`. -/
def Pmg (Y : EdgeCochain) : EdgeCochain :=
  Y - ((inner1 Y omega_scene) / 42471) • omega_scene

theorem Pmg_omega_perp (Y : EdgeCochain) : omegaPerp (Pmg Y) := by
  change (∑ e, (Y e - (inner1 Y omega_scene / 42471) * omega_scene e) *
      omega_scene e) = 0
  simp_rw [sub_mul]
  rw [Finset.sum_sub_distrib]
  change inner1 Y omega_scene -
      ∑ e, (inner1 Y omega_scene / 42471 * omega_scene e) *
        omega_scene e = 0
  rw [show ∑ e, (inner1 Y omega_scene / 42471 * omega_scene e) *
      omega_scene e =
    (inner1 Y omega_scene / 42471) * ∑ e, omega_scene e * omega_scene e by
      simp only [mul_assoc]
      rw [Finset.mul_sum]]
  have h_norm : (∑ e, omega_scene e * omega_scene e) = 42471 := by
    simpa [inner1] using omega_scene_norm
  rw [h_norm]
  ring

theorem Pmg_eq_self_of_omega_perp {Y : EdgeCochain}
    (h : omegaPerp Y) : Pmg Y = Y := by
  unfold Pmg
  have h' : inner1 Y omega_scene = 0 := h
  rw [h']
  simp

theorem Pmg_idempotent (Y : EdgeCochain) : Pmg (Pmg Y) = Pmg Y :=
  Pmg_eq_self_of_omega_perp (Pmg_omega_perp Y)

theorem Pmg_omega : Pmg omega_scene = 0 := by
  unfold Pmg
  change omega_scene - (inner1 omega_scene omega_scene / 42471) • omega_scene = 0
  rw [omega_scene_norm]
  norm_num

theorem signed_kernel_decomposition (Y : EdgeCochain)
    (hY : Y ∈ LinearMap.ker BMinusLin) :
    Y = Pmg Y + ((inner1 Y omega_scene) / 42471) • omega_scene ∧
      Pmg Y ∈ SignedOmegaPerp := by
  have hB : BMinusLin Y = 0 := LinearMap.mem_ker.mp hY
  have hOmega : BMinusLin omega_scene = 0 := by
    rw [BMinusLin_apply]
    exact BMinus_omega_scene_zero
  have hPmg : BMinusLin (Pmg Y) = 0 := by
    change BMinusLin
      (Y - ((inner1 Y omega_scene) / 42471) • omega_scene) = 0
    rw [map_sub, map_smul, hB, hOmega]
    simp
  constructor
  · simp [Pmg]
  · exact ⟨LinearMap.mem_ker.mpr hPmg, Pmg_omega_perp Y⟩

/-- Sum functional on the eleven-zone row-coefficient space. -/
def rowCoeffSum : (V11 → ℚ) →ₗ[ℚ] ℚ where
  toFun a := ∑ y, a y
  map_add' a b := Finset.sum_add_distrib
  map_smul' r a := by
    simp [Finset.mul_sum]

/-- Centered coefficients on the eleven-zone: the row coefficients sum to zero. -/
def CenteredRowCoeff : Submodule ℚ (V11 → ℚ) :=
  LinearMap.ker rowCoeffSum

theorem CenteredRowCoeff_finrank :
    Module.finrank ℚ CenteredRowCoeff = 10 := by
  change Module.finrank ℚ (LinearMap.ker rowCoeffSum) = 10
  have h_range : LinearMap.range rowCoeffSum = ⊤ := by
    rw [LinearMap.range_eq_top]
    intro r
    use fun _ => r / 11
    dsimp [rowCoeffSum]
    rw [Finset.sum_const, Finset.card_fin]
    simp [nsmul_eq_mul]
    ring
  have h_range_finrank :
      Module.finrank ℚ (LinearMap.range rowCoeffSum) = 1 := by
    rw [h_range, finrank_top]
    simp
  have h := LinearMap.finrank_range_add_finrank_ker rowCoeffSum
  have h_dom : Module.finrank ℚ (V11 → ℚ) = 11 := by
    rw [Module.finrank_fintype_fun_eq_card]
    simp
  rw [h_range_finrank, h_dom] at h
  omega

/-- Embed centered eleven-zone row coefficients into the literal edge carrier. -/
def rowCorrectionEmbed : CenteredRowCoeff →ₗ[ℚ] EdgeCochain where
  toFun a e :=
    match e with
    | Sum.inl _ => 0
    | Sum.inr (Sum.inl _) => 0
    | Sum.inr (Sum.inr (y, _)) => a.1 y
  map_add' a b := by
    funext e
    rcases e with e | e
    · simp
    · rcases e with e | ⟨y, z⟩
      · simp
      · simp
  map_smul' r a := by
    funext e
    rcases e with e | e
    · simp
    · rcases e with e | ⟨y, z⟩
      · simp
      · simp

theorem rowCorrectionEmbed_injective :
    Function.Injective rowCorrectionEmbed := by
  rw [← LinearMap.ker_eq_bot, LinearMap.ker_eq_bot']
  intro a ha
  ext y
  have h := congrFun ha (Sum.inr (Sum.inr (y, (0 : V13))))
  simpa [rowCorrectionEmbed] using h

/-- The actual ten-dimensional correction space used by `U - I`. -/
def RowCorrectionSpace : Submodule ℚ EdgeCochain :=
  LinearMap.range rowCorrectionEmbed

theorem RowCorrectionSpace_finrank :
    Module.finrank ℚ RowCorrectionSpace = 10 := by
  rw [RowCorrectionSpace,
    LinearMap.finrank_range_of_inj rowCorrectionEmbed_injective]
  exact CenteredRowCoeff_finrank

theorem U_minus_I_in_RowCorrectionSpace (X : EdgeCochain) :
    U X - X ∈ RowCorrectionSpace := by
  let a : V11 → ℚ := fun y =>
    -(2 / 13 : ℚ) *
      ((∑ z' : V13, X (Sum.inr (Sum.inr (y, z'))) -
        (1 / 11 : ℚ) *
          ∑ y' : V11, ∑ z' : V13,
            X (Sum.inr (Sum.inr (y', z')))))
  have ha : a ∈ CenteredRowCoeff := by
    rw [CenteredRowCoeff, LinearMap.mem_ker]
    dsimp [rowCoeffSum, a]
    simp_rw [mul_sub]
    rw [Finset.sum_sub_distrib]
    rw [← Finset.mul_sum]
    rw [Finset.sum_const, Finset.card_fin]
    simp [nsmul_eq_mul]
    ring
  refine ⟨⟨a, ha⟩, ?_⟩
  funext e
  rcases e with e | e
  · simp [rowCorrectionEmbed, U, Pi.sub_apply, a]
  · rcases e with e | ⟨y, z⟩
    · simp [rowCorrectionEmbed, U, Pi.sub_apply, a]
    · simp [rowCorrectionEmbed, U, Pi.sub_apply, a]

end D0.Geometry.SignlessSignedCommonCarrier
