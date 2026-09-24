import Mathlib.Algebra.Ring.Hom.Defs
import Mathlib.Algebra.Ring.Prod
import Mathlib.Data.Complex.Basic
import Mathlib.Data.Matrix.Basis
import Mathlib.Data.Matrix.Basic
import D0.Algebra.FibonacciAFTower
import D0.Geometry.ArchiveRefinementTower
import D0.Geometry.ArchiveRolePhaseProductCarrier

/-!
# AF stage → commutative Role-algebra boundary

Matrix blocks of size `m ≥ 2` admit no unital ring homomorphism into a nontrivial
commutative unital ring. Connecting to the Fibonacci AF stage shape:

* `k = 0`: two scalar blocks; characters exist;
* `k = 1`: `M₂ ⊕ ℂ`; the scalar summand still supplies a character;
* `k ≥ 2`: both path-count blocks have size ≥ 2, so no unital map into `C(B_n)`.

Normalized traces are not used as algebra homomorphisms.
Reverse maps `C(B_n) → A_k` are not excluded.
-/

namespace D0.Geometry

open D0
open Matrix
open D0.Algebra.FibonacciAFTower
open D0.Geometry.ArchiveRolePhaseProductCarrier

/-- Finite-stage AF algebra alias: two matrix blocks of sizes given by `pathCount k`. -/
abbrev AFStageAlgebra (k : ℕ) : Type :=
  Matrix (Fin (pathCount k).1) (Fin (pathCount k).1) ℂ ×
    Matrix (Fin (pathCount k).2) (Fin (pathCount k).2) ℂ

/-- Pointwise function algebra on the Role-phase carrier (commutative model of `C(B_n)`). -/
abbrev RolePhaseFunctionAlgebra (n : ℕ) : Type :=
  ArchiveRolePhasePoint n → ℂ

/-- Algebraic matrix-unit theorem: no unital ring hom from `M_ι(R)` into a nontrivial
commutative unital ring when `|ι| ≥ 2`. -/
theorem no_unital_ringHom_matrix_to_comm
    {ι R D : Type*} [Fintype ι] [DecidableEq ι] [Ring R]
    [CommRing D] [Nontrivial D] (hm : 2 ≤ Fintype.card ι)
    (f : Matrix ι ι R →+* D) : False := by
  obtain ⟨i, j, hij⟩ : ∃ i j : ι, i ≠ j := by
    have : Nontrivial ι :=
      Fintype.one_lt_card_iff_nontrivial.mp (lt_of_lt_of_le (by decide : (1 : ℕ) < 2) hm)
    exact exists_pair_ne ι
  let e11 : Matrix ι ι R := single i i 1
  let e22 : Matrix ι ι R := single j j 1
  let e12 : Matrix ι ι R := single i j 1
  let e21 : Matrix ι ι R := single j i 1
  have h11 : e12 * e21 = e11 := by simp [e11, e12, e21, single_mul_single_same]
  have h22 : e21 * e12 = e22 := by simp [e22, e12, e21, single_mul_single_same]
  have hprod : e11 * e22 = 0 := by
    simpa [e11, e22] using (single_mul_single_of_ne (c := (1 : R)) i i j hij (1 : R))
  have himg : f e11 = f e22 := by
    calc
      f e11 = f (e12 * e21) := by rw [h11]
      _ = f e12 * f e21 := map_mul f _ _
      _ = f e21 * f e12 := mul_comm _ _
      _ = f (e21 * e12) := (map_mul f _ _).symm
      _ = f e22 := by rw [h22]
  have hsq : f e11 * f e11 = 0 := by
    calc
      f e11 * f e11 = f e11 * f e22 := by rw [himg]
      _ = f (e11 * e22) := (map_mul f _ _).symm
      _ = f 0 := by rw [hprod]
      _ = 0 := map_zero f
  have hone : (1 : Matrix ι ι R) = ∑ k : ι, single k k (1 : R) :=
    (sum_single_one (α := R) (m := ι)).symm
  have hsum : (1 : D) = ∑ k : ι, f (single k k (1 : R)) := by
    rw [← map_sum f, ← hone, map_one]
  have hdiag : ∀ k : ι, f (single k k (1 : R)) = f e11 := by
    intro k
    by_cases hk : k = i
    · simp [hk, e11]
    · let ek1 : Matrix ι ι R := single k i 1
      let e1k : Matrix ι ι R := single i k 1
      have hk1 : e1k * ek1 = e11 := by simp [e11, ek1, e1k, single_mul_single_same]
      have hkk : ek1 * e1k = single k k 1 := by simp [ek1, e1k, single_mul_single_same]
      calc
        f (single k k 1) = f (ek1 * e1k) := by rw [hkk]
        _ = f ek1 * f e1k := map_mul f _ _
        _ = f e1k * f ek1 := mul_comm _ _
        _ = f (e1k * ek1) := (map_mul f _ _).symm
        _ = f e11 := by rw [hk1]
  have h1eq : (1 : D) = Fintype.card ι • f e11 := by
    rw [hsum]; simp_rw [hdiag]; simp [Finset.sum_const]
  have hzero : f e11 = 0 := by
    have hmul : f e11 * (Fintype.card ι • f e11) =
        Fintype.card ι • (f e11 * f e11) := by
      simp only [nsmul_eq_mul]
      ring
    calc
      f e11 = f e11 * (1 : D) := (mul_one _).symm
      _ = f e11 * (Fintype.card ι • f e11) := by rw [h1eq]
      _ = Fintype.card ι • (f e11 * f e11) := hmul
      _ = Fintype.card ι • (0 : D) := by rw [hsq]
      _ = 0 := nsmul_zero _
  have : (1 : D) = 0 := by rw [h1eq, hzero, nsmul_zero]
  exact one_ne_zero this

theorem no_unital_ringHom_matrixComplex_to_comm
    {m : ℕ} {D : Type*} [CommRing D] [Nontrivial D]
    (hm : 2 ≤ m) (f : Matrix (Fin m) (Fin m) ℂ →+* D) : False := by
  have : 2 ≤ Fintype.card (Fin m) := by simpa using hm
  exact no_unital_ringHom_matrix_to_comm (R := ℂ) this f

theorem pathCount_zero : pathCount 0 = (1, 1) := rfl
theorem pathCount_one : pathCount 1 = (2, 1) := rfl

theorem pathCount_block_ge_two_of_two_le (k : ℕ) (hk : 2 ≤ k) :
    2 ≤ (pathCount k).1 ∧ 2 ≤ (pathCount k).2 := by
  induction k, hk using Nat.le_induction with
  | base => decide
  | succ k hk ih =>
      rcases ih with ⟨ha, hb⟩
      refine ⟨?_, ha⟩
      have : 2 ≤ (pathCount k).1 + (pathCount k).2 :=
        le_trans ha (Nat.le_add_right _ _)
      simpa [pathCount] using this

theorem pathCount_fst_ge_two_of_one_le (k : ℕ) (hk : 1 ≤ k) :
    2 ≤ (pathCount k).1 := by
  match k, hk with
  | 0, h => cases h
  | n + 1, _ =>
    induction n with
    | zero => decide
    | succ n ih =>
        have : 2 ≤ (pathCount (n + 1)).1 := ih (Nat.le_add_left _ _)
        have : 2 ≤ (pathCount (n + 1)).1 + (pathCount (n + 1)).2 :=
          le_trans this (Nat.le_add_right _ _)
        simpa [pathCount] using this

/-- Entry extraction for `1×1` complex matrices. -/
def matrixFinOneEntry : Matrix (Fin 1) (Fin 1) ℂ →+* ℂ where
  toFun M := M 0 0
  map_one' := by simp
  map_mul' A B := by
    simp [mul_apply, Finset.univ_unique, Fin.default_eq_zero]
  map_zero' := rfl
  map_add' _ _ := rfl

/-- Constant embedding `ℂ → (X → ℂ)`. -/
def constRingHom (X : Type*) : ℂ →+* (X → ℂ) where
  toFun c := fun _ => c
  map_one' := rfl
  map_mul' _ _ := rfl
  map_zero' := rfl
  map_add' _ _ := rfl

/-- `k = 0`: character via the first scalar block. -/
def afStage0Character (n : ℕ) : AFStageAlgebra 0 →+* RolePhaseFunctionAlgebra n :=
  (constRingHom (ArchiveRolePhasePoint n)).comp
    (matrixFinOneEntry.comp (RingHom.fst _ _))

theorem af_stage_zero_character_exists (n : ℕ) :
    Nonempty (AFStageAlgebra 0 →+* RolePhaseFunctionAlgebra n) :=
  ⟨afStage0Character n⟩

/-- `k = 1`: character via the scalar (`1×1`) summand. -/
def afStage1ScalarCharacter (n : ℕ) : AFStageAlgebra 1 →+* RolePhaseFunctionAlgebra n :=
  (constRingHom (ArchiveRolePhasePoint n)).comp
    (matrixFinOneEntry.comp (RingHom.snd _ _))

theorem af_stage_one_scalar_character_exists (n : ℕ) :
    Nonempty (AFStageAlgebra 1 →+* RolePhaseFunctionAlgebra n) :=
  ⟨afStage1ScalarCharacter n⟩

/-- Evaluation character on `C(B_n)`. -/
def evalAt {n : ℕ} (x : ArchiveRolePhasePoint n) :
    RolePhaseFunctionAlgebra n →+* ℂ where
  toFun f := f x
  map_one' := rfl
  map_mul' _ _ := rfl
  map_zero' := rfl
  map_add' _ _ := rfl

private theorem complex_idempotent_eq_zero_or_one {p : ℂ} (hp : p * p = p) :
    p = 0 ∨ p = 1 := by
  have : p * (p - 1) = 0 := by
    calc
      p * (p - 1) = p * p - p := by ring
      _ = p - p := by rw [hp]
      _ = 0 := sub_self _
  exact (mul_eq_zero.mp this).elim Or.inl fun h => Or.inr (sub_eq_zero.mp h)

/-- Unital character of the first AF block when the complementary idempotent is 1. -/
def firstBlockCharacter {k : ℕ} (χ : AFStageAlgebra k →+* ℂ)
    (hp1 : χ (1, 0) = 1) :
    Matrix (Fin (pathCount k).1) (Fin (pathCount k).1) ℂ →+* ℂ where
  toFun M := χ (M, 0)
  map_one' := hp1
  map_mul' A B := by
    calc
      χ (A * B, 0) = χ ((A, 0) * (B, 0)) := by simp [Prod.mk_mul_mk]
      _ = χ (A, 0) * χ (B, 0) := map_mul χ _ _
  map_zero' := map_zero χ
  map_add' A B := by
    calc
      χ (A + B, 0) = χ ((A, 0) + (B, 0)) := by simp [Prod.mk_add_mk]
      _ = χ (A, 0) + χ (B, 0) := map_add χ _ _

/-- Unital character of the second AF block when its unit maps to 1. -/
def secondBlockCharacter {k : ℕ} (χ : AFStageAlgebra k →+* ℂ)
    (hq1 : χ (0, 1) = 1) :
    Matrix (Fin (pathCount k).2) (Fin (pathCount k).2) ℂ →+* ℂ where
  toFun M := χ (0, M)
  map_one' := hq1
  map_mul' A B := by
    calc
      χ (0, A * B) = χ ((0, A) * (0, B)) := by simp [Prod.mk_mul_mk]
      _ = χ (0, A) * χ (0, B) := map_mul χ _ _
  map_zero' := map_zero χ
  map_add' A B := by
    calc
      χ (0, A + B) = χ ((0, A) + (0, B)) := by simp [Prod.mk_add_mk]
      _ = χ (0, A) + χ (0, B) := map_add χ _ _

/-- For `k ≥ 2`, no unital map `A_k → C(B_n)`. -/
theorem no_unital_afStage_to_rolePhaseFunction_of_two_le (k n : ℕ) (hk : 2 ≤ k)
    (F : AFStageAlgebra k →+* RolePhaseFunctionAlgebra n) : False := by
  obtain ⟨ha, hb⟩ := pathCount_block_ge_two_of_two_le k hk
  obtain ⟨x⟩ := (inferInstance : Nonempty (ArchiveRolePhasePoint n))
  let χ : AFStageAlgebra k →+* ℂ := (evalAt x).comp F
  let p : ℂ := χ (1, 0)
  let q : ℂ := χ (0, 1)
  have hpq : p + q = 1 := by
    have hsum : (1, 0) + (0, 1) = (1 : AFStageAlgebra k) := by
      simp [Prod.mk_add_mk]
    calc
      p + q = χ (1, 0) + χ (0, 1) := rfl
      _ = χ ((1, 0) + (0, 1)) := (map_add χ _ _).symm
      _ = χ 1 := by rw [hsum]
      _ = 1 := map_one χ
  have hp2 : p * p = p := by
    have hmul : (1, 0) * (1, 0) = ((1, 0) : AFStageAlgebra k) := by
      simp [Prod.mk_mul_mk]
    calc
      p * p = χ (1, 0) * χ (1, 0) := rfl
      _ = χ ((1, 0) * (1, 0)) := (map_mul χ _ _).symm
      _ = χ (1, 0) := by rw [hmul]
  have hidem := complex_idempotent_eq_zero_or_one hp2
  cases hidem with
  | inl hp0 =>
      have hq1 : q = 1 := by simpa [hp0] using hpq
      exact no_unital_ringHom_matrixComplex_to_comm hb (secondBlockCharacter χ hq1)
  | inr hp1 =>
      exact no_unital_ringHom_matrixComplex_to_comm ha (firstBlockCharacter χ hp1)

/-- Weaker optional fact: `k ≥ 1` ⇒ no injective unital map into a commutative target,
because the first block is already noncommutative. -/
theorem no_injective_unital_afStage_to_comm_of_one_le
    {k : ℕ} {D : Type*} [CommRing D] [Nontrivial D]
    (hk : 1 ≤ k) (f : AFStageAlgebra k →+* D) (hinj : Function.Injective f) : False := by
  have hpc := pathCount_fst_ge_two_of_one_le k hk
  -- pick 0 and 1 in Fin m
  have hm0 : (0 : ℕ) < (pathCount k).1 := lt_of_lt_of_le (by decide : 0 < 2) hpc
  have hm1 : (1 : ℕ) < (pathCount k).1 := lt_of_lt_of_le (by decide : 1 < 2) hpc
  let i0 : Fin (pathCount k).1 := ⟨0, hm0⟩
  let i1 : Fin (pathCount k).1 := ⟨1, hm1⟩
  let e12 := single i0 i1 (1 : ℂ)
  let e21 := single i1 i0 (1 : ℂ)
  have hne : e12 * e21 ≠ e21 * e12 := by
    intro h
    have h' : single i0 i0 (1 : ℂ) = single i1 i1 (1 : ℂ) := by
      simpa [e12, e21, single_mul_single_same] using h
    have h01 : (single i0 i0 (1 : ℂ)) i0 i0 = (single i1 i1 (1 : ℂ)) i0 i0 :=
      congrFun (congrFun h' i0) i0
    have hl : (single i0 i0 (1 : ℂ)) i0 i0 = 1 := by simp [single]
    have hr : (single i1 i1 (1 : ℂ)) i0 i0 = 0 := by
      simp [single]
      intro h
      exact (by decide : (1 : ℕ) ≠ 0) (by simpa [i0, i1] using congrArg Fin.val h.symm)
    have : (1 : ℂ) = 0 := by
      calc
        (1 : ℂ) = (single i0 i0 (1 : ℂ)) i0 i0 := hl.symm
        _ = (single i1 i1 (1 : ℂ)) i0 i0 := h01
        _ = 0 := hr
    exact one_ne_zero this
  have heq : f (e12 * e21, 0) = f (e21 * e12, 0) := by
    have hc : f (e12, 0) * f (e21, 0) = f (e21, 0) * f (e12, 0) := mul_comm _ _
    calc
      f (e12 * e21, 0) = f ((e12, 0) * (e21, 0)) := by simp
      _ = f (e12, 0) * f (e21, 0) := map_mul _ _ _
      _ = f (e21, 0) * f (e12, 0) := hc
      _ = f ((e21, 0) * (e12, 0)) := (map_mul _ _ _).symm
      _ = f (e21 * e12, 0) := by simp
  have hprod : (e12 * e21, (0 : Matrix (Fin (pathCount k).2) (Fin (pathCount k).2) ℂ)) =
      (e21 * e12, 0) := hinj heq
  exact hne (congrArg Prod.fst hprod)

/-- Safe reverse-direction note placeholder (existence is noncanonical; not constructed). -/
theorem reverse_direction_not_excluded : True := trivial

end D0.Geometry
