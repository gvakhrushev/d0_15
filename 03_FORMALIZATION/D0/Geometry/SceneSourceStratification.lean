import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic
import D0.Geometry.SceneHodgeDecomposition

/-!
# D0.Geometry.SceneSourceStratification

The literal source stratification of the scene edge cochains.  The
blockwise-zero-marginal sector is defined directly on the three typed edge
blocks; it is a signed kernel and is orthogonal to every signed vertex source.
The final identity records the literal uniform triangle source with the
unnormalized block vector `(13, -11, 9)`.

This module does not identify the tensor sector with TT, a graviton, or any
physical radiation carrier.
-/

namespace D0.Geometry.SceneSourceStratification

open BigOperators Matrix
open D0.Geometry.SceneCochainComplex
open D0.Topology.GenericTripartiteHomology

abbrev SceneA := Fin 9
abbrev SceneB := Fin 11
abbrev SceneC := Fin 13
abbrev EdgeCochain := D0.Geometry.SceneCochainComplex.SceneC1
abbrev Triangle := D0.Geometry.SceneCochainComplex.SceneTriangle

private lemma sum_indicator_one
    {α : Type} [Fintype α] [DecidableEq α]
    (f : α → ℚ) (a : α) :
    (∑ x : α, (if a = x then (1 : ℚ) else 0) * f x) = f a := by
  simp_rw [ite_mul, one_mul, zero_mul]
  exact Fintype.sum_ite_eq a f

private lemma sum_indicator_neg_one
    {α : Type} [Fintype α] [DecidableEq α]
    (f : α → ℚ) (a : α) :
    (∑ x : α, (if a = x then (-1 : ℚ) else 0) * f x) = -f a := by
  simp_rw [ite_mul, neg_one_mul, zero_mul]
  rw [Fintype.sum_ite_eq]

def sceneABRowMarginal (z : EdgeCochain) (a : SceneA) : ℚ :=
  ∑ b : SceneB, z (Sum.inl (a, b))

def sceneABColumnMarginal (z : EdgeCochain) (b : SceneB) : ℚ :=
  ∑ a : SceneA, z (Sum.inl (a, b))

def sceneACRowMarginal (z : EdgeCochain) (a : SceneA) : ℚ :=
  ∑ c : SceneC, z (Sum.inr (Sum.inl (a, c)))

def sceneACColumnMarginal (z : EdgeCochain) (c : SceneC) : ℚ :=
  ∑ a : SceneA, z (Sum.inr (Sum.inl (a, c)))

def sceneBCRowMarginal (z : EdgeCochain) (b : SceneB) : ℚ :=
  ∑ c : SceneC, z (Sum.inr (Sum.inr (b, c)))

def sceneBCColumnMarginal (z : EdgeCochain) (c : SceneC) : ℚ :=
  ∑ b : SceneB, z (Sum.inr (Sum.inr (b, c)))

/-- The literal edge sector with zero row and column marginals in every edge
block `(9,11)`, `(9,13)`, and `(11,13)`. -/
def SceneTensorBlock : Submodule ℚ EdgeCochain where
  carrier := {z |
    (∀ a, sceneABRowMarginal z a = 0) ∧
    (∀ b, sceneABColumnMarginal z b = 0) ∧
    (∀ a, sceneACRowMarginal z a = 0) ∧
    (∀ c, sceneACColumnMarginal z c = 0) ∧
    (∀ b, sceneBCRowMarginal z b = 0) ∧
    (∀ c, sceneBCColumnMarginal z c = 0)}
  zero_mem' := by
    simp [sceneABRowMarginal, sceneABColumnMarginal,
      sceneACRowMarginal, sceneACColumnMarginal,
      sceneBCRowMarginal, sceneBCColumnMarginal]
  add_mem' := by
    intro x y hx hy
    rcases hx with ⟨hxABr, hxABc, hxACr, hxACc, hxBCr, hxBCc⟩
    rcases hy with ⟨hyABr, hyABc, hyACr, hyACc, hyBCr, hyBCc⟩
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;> intro i
    · change sceneABRowMarginal (x + y) i = 0
      simpa [sceneABRowMarginal, Pi.add_apply, Finset.sum_add_distrib]
        using congrArg₂ (· + ·) (hxABr i) (hyABr i)
    · change sceneABColumnMarginal (x + y) i = 0
      simpa [sceneABColumnMarginal, Pi.add_apply, Finset.sum_add_distrib]
        using congrArg₂ (· + ·) (hxABc i) (hyABc i)
    · change sceneACRowMarginal (x + y) i = 0
      simpa [sceneACRowMarginal, Pi.add_apply, Finset.sum_add_distrib]
        using congrArg₂ (· + ·) (hxACr i) (hyACr i)
    · change sceneACColumnMarginal (x + y) i = 0
      simpa [sceneACColumnMarginal, Pi.add_apply, Finset.sum_add_distrib]
        using congrArg₂ (· + ·) (hxACc i) (hyACc i)
    · change sceneBCRowMarginal (x + y) i = 0
      simpa [sceneBCRowMarginal, Pi.add_apply, Finset.sum_add_distrib]
        using congrArg₂ (· + ·) (hxBCr i) (hyBCr i)
    · change sceneBCColumnMarginal (x + y) i = 0
      simpa [sceneBCColumnMarginal, Pi.add_apply, Finset.sum_add_distrib]
        using congrArg₂ (· + ·) (hxBCc i) (hyBCc i)
  smul_mem' := by
    intro r z hz
    rcases hz with ⟨hzABr, hzABc, hzACr, hzACc, hzBCr, hzBCc⟩
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;> intro i
    · change sceneABRowMarginal (r • z) i = 0
      simp only [sceneABRowMarginal, Pi.smul_apply]
      rw [← Finset.smul_sum]
      have h := hzABr i
      change (∑ b : SceneB, z (Sum.inl (i, b))) = 0 at h
      rw [h, smul_zero]
    · change sceneABColumnMarginal (r • z) i = 0
      simp only [sceneABColumnMarginal, Pi.smul_apply]
      rw [← Finset.smul_sum]
      have h := hzABc i
      change (∑ a : SceneA, z (Sum.inl (a, i))) = 0 at h
      rw [h, smul_zero]
    · change sceneACRowMarginal (r • z) i = 0
      simp only [sceneACRowMarginal, Pi.smul_apply]
      rw [← Finset.smul_sum]
      have h := hzACr i
      change (∑ c : SceneC, z (Sum.inr (Sum.inl (i, c)))) = 0 at h
      rw [h, smul_zero]
    · change sceneACColumnMarginal (r • z) i = 0
      simp only [sceneACColumnMarginal, Pi.smul_apply]
      rw [← Finset.smul_sum]
      have h := hzACc i
      change (∑ a : SceneA, z (Sum.inr (Sum.inl (a, i)))) = 0 at h
      rw [h, smul_zero]
    · change sceneBCRowMarginal (r • z) i = 0
      simp only [sceneBCRowMarginal, Pi.smul_apply]
      rw [← Finset.smul_sum]
      have h := hzBCr i
      change (∑ c : SceneC, z (Sum.inr (Sum.inr (i, c)))) = 0 at h
      rw [h, smul_zero]
    · change sceneBCColumnMarginal (r • z) i = 0
      simp only [sceneBCColumnMarginal, Pi.smul_apply]
      rw [← Finset.smul_sum]
      have h := hzBCc i
      change (∑ b : SceneB, z (Sum.inr (Sum.inr (b, i)))) = 0 at h
      rw [h, smul_zero]

/-- Public form of the blockwise marginal equations defining the sector. -/
theorem mem_SceneTensorBlock_iff (z : EdgeCochain) :
    z ∈ SceneTensorBlock ↔
      (∀ a, sceneABRowMarginal z a = 0) ∧
      (∀ b, sceneABColumnMarginal z b = 0) ∧
      (∀ a, sceneACRowMarginal z a = 0) ∧
      (∀ c, sceneACColumnMarginal z c = 0) ∧
      (∀ b, sceneBCRowMarginal z b = 0) ∧
      (∀ c, sceneBCColumnMarginal z c = 0) := Iff.rfl

/-- The blockwise-zero-marginal sector is signed-divergence-free. -/
private lemma signed_boundary_at_A (z : EdgeCochain) (a : SceneA) :
    sceneBoundary1.mulVec z (Sum.inl a) =
      -sceneABRowMarginal z a - sceneACRowMarginal z a := by
  simp only [Matrix.mulVec, dotProduct, sceneBoundary1, boundary1,
    Fintype.sum_sum_type, Fintype.sum_prod_type, zero_mul,
    Finset.sum_const_zero, add_zero, zero_add]
  have hAB :
      (∑ a' : SceneA, ∑ b : SceneB,
        (if a = a' then (-1 : ℚ) else 0) * z (Sum.inl (a', b))) =
        -∑ b : SceneB, z (Sum.inl (a, b)) := by
    calc
      _ = ∑ a' : SceneA, (if a = a' then (-1 : ℚ) else 0) *
          (∑ b : SceneB, z (Sum.inl (a', b))) := by
        apply Finset.sum_congr rfl
        intro a' _
        rw [← Finset.mul_sum]
      _ = -∑ b : SceneB, z (Sum.inl (a, b)) := by
        rw [sum_indicator_neg_one]
  have hAC :
      (∑ a' : SceneA, ∑ c : SceneC,
        (if a = a' then (-1 : ℚ) else 0) *
          z (Sum.inr (Sum.inl (a', c)))) =
        -∑ c : SceneC, z (Sum.inr (Sum.inl (a, c))) := by
    calc
      _ = ∑ a' : SceneA, (if a = a' then (-1 : ℚ) else 0) *
          (∑ c : SceneC, z (Sum.inr (Sum.inl (a', c)))) := by
        apply Finset.sum_congr rfl
        intro a' _
        rw [← Finset.mul_sum]
      _ = -∑ c : SceneC, z (Sum.inr (Sum.inl (a, c))) := by
        rw [sum_indicator_neg_one]
  rw [hAB, hAC]
  simp [sceneABRowMarginal, sceneACRowMarginal]
  ring

private lemma signed_boundary_at_B (z : EdgeCochain) (b : SceneB) :
    sceneBoundary1.mulVec z (Sum.inr (Sum.inl b)) =
      sceneABColumnMarginal z b - sceneBCRowMarginal z b := by
  simp only [Matrix.mulVec, dotProduct, sceneBoundary1, boundary1,
    Fintype.sum_sum_type, Fintype.sum_prod_type, zero_mul,
    Finset.sum_const_zero, add_zero, zero_add]
  have hAB :
      (∑ a : SceneA, ∑ b' : SceneB,
        (if b = b' then (1 : ℚ) else 0) * z (Sum.inl (a, b'))) =
        ∑ a : SceneA, z (Sum.inl (a, b)) := by
    apply Finset.sum_congr rfl
    intro a _
    exact sum_indicator_one (fun b' : SceneB => z (Sum.inl (a, b'))) b
  have hBC :
      (∑ b' : SceneB, ∑ c : SceneC,
        (if b = b' then (-1 : ℚ) else 0) *
          z (Sum.inr (Sum.inr (b', c)))) =
        -∑ c : SceneC, z (Sum.inr (Sum.inr (b, c))) := by
    calc
      _ = ∑ b' : SceneB, (if b = b' then (-1 : ℚ) else 0) *
          (∑ c : SceneC, z (Sum.inr (Sum.inr (b', c)))) := by
        apply Finset.sum_congr rfl
        intro b' _
        rw [← Finset.mul_sum]
      _ = -∑ c : SceneC, z (Sum.inr (Sum.inr (b, c))) := by
        rw [sum_indicator_neg_one]
  rw [hAB, hBC]
  simp [sceneABColumnMarginal, sceneBCRowMarginal]
  ring

private lemma signed_boundary_at_C (z : EdgeCochain) (c : SceneC) :
    sceneBoundary1.mulVec z (Sum.inr (Sum.inr c)) =
      sceneACColumnMarginal z c + sceneBCColumnMarginal z c := by
  simp only [Matrix.mulVec, dotProduct, sceneBoundary1, boundary1,
    Fintype.sum_sum_type, Fintype.sum_prod_type, zero_mul,
    Finset.sum_const_zero, add_zero, zero_add]
  have hAC :
      (∑ a : SceneA, ∑ c' : SceneC,
        (if c = c' then (1 : ℚ) else 0) *
          z (Sum.inr (Sum.inl (a, c')))) =
        ∑ a : SceneA, z (Sum.inr (Sum.inl (a, c))) := by
    apply Finset.sum_congr rfl
    intro a _
    exact sum_indicator_one
      (fun c' : SceneC => z (Sum.inr (Sum.inl (a, c')))) c
  have hBC :
      (∑ b : SceneB, ∑ c' : SceneC,
        (if c = c' then (1 : ℚ) else 0) *
          z (Sum.inr (Sum.inr (b, c')))) =
        ∑ b : SceneB, z (Sum.inr (Sum.inr (b, c))) := by
    apply Finset.sum_congr rfl
    intro b _
    exact sum_indicator_one
      (fun c' : SceneC => z (Sum.inr (Sum.inr (b, c')))) c
  rw [hAC, hBC]
  simp [sceneACColumnMarginal, sceneBCColumnMarginal]

theorem sceneTensorBlock_le_signed_kernel :
    SceneTensorBlock ≤ LinearMap.ker sceneBoundary1.mulVecLin := by
  intro z hz
  change sceneBoundary1.mulVec z = 0
  funext v
  cases v with
  | inl a =>
      rw [signed_boundary_at_A, hz.1 a, hz.2.2.1 a]
      simp
  | inr bc =>
      cases bc with
      | inl b =>
          rw [signed_boundary_at_B, hz.2.1 b, hz.2.2.2.2.1 b]
          simp
      | inr c =>
          rw [signed_boundary_at_C, hz.2.2.2.1 c, hz.2.2.2.2.2 c]
          simp

/-- The signed vertex source has no component in the blockwise tensor sector. -/
theorem vertex_source_orthogonal_to_tensorBlock
    (f : SceneCochainComplex.SceneC0) (z : SceneTensorBlock) :
    SceneHodgeDecomposition.inner1 (sceneBoundary1.transpose.mulVec f)
      (z : EdgeCochain) = 0 := by
  change SceneHodgeDecomposition.inner1
    (SceneCochainComplex.d0 f) (z : EdgeCochain) = 0
  rw [SceneHodgeDecomposition.adjoint_identity_01]
  rw [show SceneHodgeDecomposition.delta0 (z : EdgeCochain) = 0 from
    congrArg (fun x => x) (sceneTensorBlock_le_signed_kernel z.property)]
  simp [SceneHodgeDecomposition.inner0]

/-- The literal block-constant triangle-source pattern `(13,-11,9)`. -/
def omega_scene : EdgeCochain
  | Sum.inl _ => 13
  | Sum.inr (Sum.inl _) => -11
  | Sum.inr (Sum.inr _) => 9

/-- The signed boundary annihilates the uniform triangle-source pattern. -/
theorem sceneBoundary1_mulVec_omega_scene :
    sceneBoundary1.mulVec omega_scene = 0 := by
  native_decide

/-- The uniform triangle cochain produces `omega_scene` with no extra factor. -/
theorem sceneBoundary2_mulVec_one :
    sceneBoundary2.mulVec (fun _ : Triangle => (1 : ℚ)) = omega_scene := by
  native_decide

end D0.Geometry.SceneSourceStratification
