import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Data.Matrix.Mul
import Mathlib.Data.Real.Basic
import Mathlib.Logic.Equiv.Basic
import Mathlib.Tactic.Abel
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum.Basic

/-!
# Schur transfer of a finite stationary block

For a real block operator `H = [[A, B], [C, D]]` with a supplied two-sided inverse of `D`,
the reduced operator is `A - B D⁻¹ C`. Its kernel is isomorphic to `ker H` by the graph
`x ↦ (x, -D⁻¹ C x)`. An inhomogeneous right-hand side `(f, g)` reduces to
`f - B D⁻¹ g`: the auxiliary source `g` is kept.

If `A` and `D` are symmetric and `C = Bᵀ`, the same inverse gives the congruence
`H = Uᵀ diag(S, D) U` and the matching bilinear identity. A supplied `ℓ¹` bound on
`D⁻¹` bounds the reconstructed auxiliary component. The whole block `H` is not
assumed invertible.

The retained shell operator `[[H_red, T*], [T, 0]]` has lower-right block `0`.
That block is not a Schur pivot. No inverse of it is defined.

These are identities of finite real coordinate spaces under a matrix inverse
hypothesis. They do not axiomatize a Gibbs state or a log-determinant, and they
do not admit a physical or Einstein equation.
-/

namespace D0.Research.SchurStationaryTransfer

open Matrix
open scoped Matrix

variable {X Y : Type*} [Fintype X] [Fintype Y] [DecidableEq X] [DecidableEq Y]

/-- Real block operator `[[A, B], [C, D]]` on `X ⊕ Y`. -/
def blockH (A : Matrix X X ℝ) (B : Matrix X Y ℝ) (C : Matrix Y X ℝ) (D : Matrix Y Y ℝ) :
    Matrix (X ⊕ Y) (X ⊕ Y) ℝ :=
  Matrix.of <|
    Sum.elim (fun i => Sum.elim (A i) (B i)) (fun i => Sum.elim (C i) (D i))

@[simp]
lemma blockH_inl_inl (A : Matrix X X ℝ) (B : Matrix X Y ℝ) (C : Matrix Y X ℝ) (D : Matrix Y Y ℝ)
    (i j : X) : blockH A B C D (Sum.inl i) (Sum.inl j) = A i j := by
  simp [blockH]

@[simp]
lemma blockH_inl_inr (A : Matrix X X ℝ) (B : Matrix X Y ℝ) (C : Matrix Y X ℝ) (D : Matrix Y Y ℝ)
    (i : X) (j : Y) : blockH A B C D (Sum.inl i) (Sum.inr j) = B i j := by
  simp [blockH]

@[simp]
lemma blockH_inr_inl (A : Matrix X X ℝ) (B : Matrix X Y ℝ) (C : Matrix Y X ℝ) (D : Matrix Y Y ℝ)
    (i : Y) (j : X) : blockH A B C D (Sum.inr i) (Sum.inl j) = C i j := by
  simp [blockH]

@[simp]
lemma blockH_inr_inr (A : Matrix X X ℝ) (B : Matrix X Y ℝ) (C : Matrix Y X ℝ) (D : Matrix Y Y ℝ)
    (i j : Y) : blockH A B C D (Sum.inr i) (Sum.inr j) = D i j := by
  simp [blockH]

/-- Lower-right block. Used to read the shell-shell entry without inverting it. -/
def lowerRight (M : Matrix (X ⊕ Y) (X ⊕ Y) ℝ) : Matrix Y Y ℝ :=
  Matrix.of fun i j => M (Sum.inr i) (Sum.inr j)

@[simp]
lemma lowerRight_blockH (A : Matrix X X ℝ) (B : Matrix X Y ℝ) (C : Matrix Y X ℝ)
    (D : Matrix Y Y ℝ) : lowerRight (blockH A B C D) = D := by
  ext i j
  simp [lowerRight]

/-- Two-sided matrix inverse. This is a hypothesis, not a constructed Gibbs resolvent. -/
def IsTwoSidedInverse (D Dinv : Matrix Y Y ℝ) : Prop :=
  Dinv * D = 1 ∧ D * Dinv = 1

/-- Schur complement `A - B D⁻¹ C` of an invertible lower block. -/
def schurComplement (A : Matrix X X ℝ) (B : Matrix X Y ℝ) (C : Matrix Y X ℝ)
    (Dinv : Matrix Y Y ℝ) : Matrix X X ℝ :=
  A - B * Dinv * C

/-- Homogeneous auxiliary component `-D⁻¹ C x`. -/
def auxOf (Dinv : Matrix Y Y ℝ) (C : Matrix Y X ℝ) (x : X → ℝ) : Y → ℝ :=
  -(Dinv *ᵥ (C *ᵥ x))

/-- Graph of the homogeneous recovery. -/
def jointOf (Dinv : Matrix Y Y ℝ) (C : Matrix Y X ℝ) (x : X → ℝ) : (X ⊕ Y) → ℝ :=
  Sum.elim x (auxOf Dinv C x)

/-- Inhomogeneous auxiliary recovery `D⁻¹ (g - C x)`. -/
def recoveredAux (Dinv : Matrix Y Y ℝ) (C : Matrix Y X ℝ) (g : Y → ℝ) (x : X → ℝ) : Y → ℝ :=
  Dinv *ᵥ (g - C *ᵥ x)

/-- Reduced right-hand side `f - B D⁻¹ g`. The auxiliary source `g` is not dropped. -/
def reducedSource (B : Matrix X Y ℝ) (Dinv : Matrix Y Y ℝ) (f : X → ℝ) (g : Y → ℝ) : X → ℝ :=
  f - B *ᵥ (Dinv *ᵥ g)

lemma sumElim_parts (v : (X ⊕ Y) → ℝ) :
    Sum.elim (v ∘ Sum.inl) (v ∘ Sum.inr) = v := by
  ext i
  cases i <;> rfl

lemma block_mulVec (A : Matrix X X ℝ) (B : Matrix X Y ℝ) (C : Matrix Y X ℝ) (D : Matrix Y Y ℝ)
    (x : X → ℝ) (y : Y → ℝ) :
    blockH A B C D *ᵥ Sum.elim x y =
      Sum.elim (A *ᵥ x + B *ᵥ y) (C *ᵥ x + D *ᵥ y) := by
  ext i
  cases i with
  | inl i =>
    rw [Matrix.mulVec, dotProduct, Fintype.sum_sum_type]
    simp [Sum.elim_inl, Pi.add_apply, Matrix.mulVec, dotProduct]
  | inr i =>
    rw [Matrix.mulVec, dotProduct, Fintype.sum_sum_type]
    simp [Sum.elim_inr, Pi.add_apply, Matrix.mulVec, dotProduct]

lemma block_mul (A : Matrix X X ℝ) (B : Matrix X Y ℝ) (C : Matrix Y X ℝ) (D : Matrix Y Y ℝ)
    (A' : Matrix X X ℝ) (B' : Matrix X Y ℝ) (C' : Matrix Y X ℝ) (D' : Matrix Y Y ℝ) :
    blockH A B C D * blockH A' B' C' D' =
      blockH (A * A' + B * C') (A * B' + B * D') (C * A' + D * C') (C * B' + D * D') := by
  ext i j
  cases i <;> cases j
  · rw [Matrix.mul_apply, Fintype.sum_sum_type]
    simp [Matrix.add_apply, Matrix.mul_apply]
  · rw [Matrix.mul_apply, Fintype.sum_sum_type]
    simp [Matrix.add_apply, Matrix.mul_apply]
  · rw [Matrix.mul_apply, Fintype.sum_sum_type]
    simp [Matrix.add_apply, Matrix.mul_apply]
  · rw [Matrix.mul_apply, Fintype.sum_sum_type]
    simp [Matrix.add_apply, Matrix.mul_apply]

lemma block_transpose (A : Matrix X X ℝ) (B : Matrix X Y ℝ) (C : Matrix Y X ℝ)
    (D : Matrix Y Y ℝ) :
    (blockH A B C D)ᵀ = blockH Aᵀ Cᵀ Bᵀ Dᵀ := by
  ext i j
  cases i <;> cases j <;> simp [transpose_apply]

/-- A symmetric invertible block has a symmetric two-sided inverse. -/
lemma twoSidedInverse_transpose {D Dinv : Matrix Y Y ℝ}
    (hD : Dᵀ = D) (hInv : IsTwoSidedInverse D Dinv) : Dinvᵀ = Dinv := by
  have hRight : D * Dinvᵀ = 1 := by
    have hT := congrArg (·ᵀ) hInv.1
    simpa [Matrix.transpose_mul, transpose_one, hD] using hT
  calc
    Dinvᵀ = (1 : Matrix Y Y ℝ) * Dinvᵀ := by simp
    _ = (Dinv * D) * Dinvᵀ := by rw [hInv.1]
    _ = Dinv * (D * Dinvᵀ) := by rw [Matrix.mul_assoc]
    _ = Dinv * 1 := by rw [hRight]
    _ = Dinv := by simp

lemma schur_transpose {A : Matrix X X ℝ} {B : Matrix X Y ℝ} {C : Matrix Y X ℝ}
    {D Dinv : Matrix Y Y ℝ} (hA : Aᵀ = A) (hD : Dᵀ = D) (hC : C = Bᵀ)
    (hInv : IsTwoSidedInverse D Dinv) :
    (schurComplement A B C Dinv)ᵀ = schurComplement A B C Dinv := by
  have hDinv : Dinvᵀ = Dinv := twoSidedInverse_transpose hD hInv
  change (A - B * Dinv * C)ᵀ = A - B * Dinv * C
  rw [Matrix.transpose_sub, hA, hC]
  -- `(B D⁻¹ Bᵀ)ᵀ = Bᵀᵀ D⁻¹ᵀ Bᵀ = B D⁻¹ Bᵀ` once `D⁻¹` is symmetric.
  rw [Matrix.transpose_mul, Matrix.transpose_mul, Matrix.transpose_transpose, hDinv, ← Matrix.mul_assoc]

/-- LDU factorization through a proved inverse of the lower block. -/
theorem block_factorization {A : Matrix X X ℝ} {B : Matrix X Y ℝ} {C : Matrix Y X ℝ}
    {D Dinv : Matrix Y Y ℝ} (hInv : IsTwoSidedInverse D Dinv) :
    blockH A B C D =
      blockH (1 : Matrix X X ℝ) (B * Dinv) (0 : Matrix Y X ℝ) 1 *
        blockH (schurComplement A B C Dinv) (0 : Matrix X Y ℝ) (0 : Matrix Y X ℝ) D *
          blockH (1 : Matrix X X ℝ) (0 : Matrix X Y ℝ) (Dinv * C) 1 := by
  set S : Matrix X X ℝ := schurComplement A B C Dinv
  have hInner :
      blockH S (0 : Matrix X Y ℝ) (0 : Matrix Y X ℝ) D *
          blockH (1 : Matrix X X ℝ) (0 : Matrix X Y ℝ) (Dinv * C) 1 =
        blockH S (0 : Matrix X Y ℝ) (D * (Dinv * C)) D := by
    rw [block_mul]
    simp [Matrix.mul_one, Matrix.one_mul, Matrix.mul_zero, Matrix.zero_mul, add_zero, zero_add]
  have hDC : D * (Dinv * C) = C := by
    rw [← Matrix.mul_assoc, hInv.2, Matrix.one_mul]
  have hMR :
      blockH S (0 : Matrix X Y ℝ) (0 : Matrix Y X ℝ) D *
          blockH (1 : Matrix X X ℝ) (0 : Matrix X Y ℝ) (Dinv * C) 1 =
        blockH S (0 : Matrix X Y ℝ) C D := by
    rw [hInner, hDC]
  have hLeft :
      blockH (1 : Matrix X X ℝ) (B * Dinv) (0 : Matrix Y X ℝ) 1 *
          blockH S (0 : Matrix X Y ℝ) C D =
        blockH (S + (B * Dinv) * C) ((B * Dinv) * D) C D := by
    rw [block_mul]
    simp [Matrix.mul_one, Matrix.one_mul, Matrix.mul_zero, Matrix.zero_mul, add_zero, zero_add]
  have hS : S + (B * Dinv) * C = A := by
    simp [S, schurComplement, sub_add_cancel]
  have hB : (B * Dinv) * D = B := by
    rw [Matrix.mul_assoc, hInv.1, Matrix.mul_one]
  calc
    blockH A B C D =
        blockH (1 : Matrix X X ℝ) (B * Dinv) (0 : Matrix Y X ℝ) 1 *
          blockH S (0 : Matrix X Y ℝ) C D := by
      rw [hLeft, hS, hB]
    _ = blockH (1 : Matrix X X ℝ) (B * Dinv) (0 : Matrix Y X ℝ) 1 *
          (blockH S (0 : Matrix X Y ℝ) (0 : Matrix Y X ℝ) D *
            blockH (1 : Matrix X X ℝ) (0 : Matrix X Y ℝ) (Dinv * C) 1) := by
      rw [hMR]
    _ = blockH (1 : Matrix X X ℝ) (B * Dinv) (0 : Matrix Y X ℝ) 1 *
          blockH S (0 : Matrix X Y ℝ) (0 : Matrix Y X ℝ) D *
            blockH (1 : Matrix X X ℝ) (0 : Matrix X Y ℝ) (Dinv * C) 1 := by
      rw [Matrix.mul_assoc]

/-- Right factor of the symmetric congruence. -/
def symmetricFactor (B : Matrix X Y ℝ) (Dinv : Matrix Y Y ℝ) : Matrix (X ⊕ Y) (X ⊕ Y) ℝ :=
  blockH (1 : Matrix X X ℝ) (0 : Matrix X Y ℝ) (Dinv * Bᵀ) (1 : Matrix Y Y ℝ)

/-- Diagonal factor `diag(S, D)`. -/
def diagonalFactor (S : Matrix X X ℝ) (D : Matrix Y Y ℝ) : Matrix (X ⊕ Y) (X ⊕ Y) ℝ :=
  blockH S (0 : Matrix X Y ℝ) (0 : Matrix Y X ℝ) D

/-- Symmetric case: `H = Uᵀ diag(S, D) U`, and `S` stays symmetric. -/
theorem symmetric_block_congruence {A : Matrix X X ℝ} {B : Matrix X Y ℝ} {C : Matrix Y X ℝ}
    {D Dinv : Matrix Y Y ℝ} (hA : Aᵀ = A) (hD : Dᵀ = D) (hC : C = Bᵀ)
    (hInv : IsTwoSidedInverse D Dinv) :
    (schurComplement A B C Dinv)ᵀ = schurComplement A B C Dinv ∧
      blockH A B C D =
        (symmetricFactor B Dinv)ᵀ *
          diagonalFactor (schurComplement A B C Dinv) D *
            symmetricFactor B Dinv := by
  refine ⟨schur_transpose hA hD hC hInv, ?_⟩
  have hDinv : Dinvᵀ = Dinv := twoSidedInverse_transpose hD hInv
  have hBT : Bᵀ = C := hC.symm
  have hUT : (symmetricFactor B Dinv)ᵀ =
      blockH (1 : Matrix X X ℝ) (B * Dinv) (0 : Matrix Y X ℝ) 1 := by
    simp [symmetricFactor, block_transpose, transpose_one, transpose_zero, Matrix.transpose_mul,
      Matrix.transpose_transpose, hDinv]
  have hU : symmetricFactor B Dinv =
      blockH (1 : Matrix X X ℝ) (0 : Matrix X Y ℝ) (Dinv * C) 1 := by
    simp [symmetricFactor, hBT]
  rw [hUT, hU, diagonalFactor]
  exact block_factorization hInv

lemma dot_congruence {n : Type*} [Fintype n] [DecidableEq n]
    (U M : Matrix n n ℝ) (u v : n → ℝ) :
    u ⬝ᵥ (Uᵀ * M * U) *ᵥ v = (U *ᵥ u) ⬝ᵥ M *ᵥ (U *ᵥ v) := by
  have hmul : (Uᵀ * M * U) *ᵥ v = Uᵀ *ᵥ (M *ᵥ (U *ᵥ v)) := by
    calc
      (Uᵀ * M * U) *ᵥ v = (Uᵀ * (M * U)) *ᵥ v := by rw [Matrix.mul_assoc]
      _ = Uᵀ *ᵥ ((M * U) *ᵥ v) := by rw [← Matrix.mulVec_mulVec]
      _ = Uᵀ *ᵥ (M *ᵥ (U *ᵥ v)) := by rw [← Matrix.mulVec_mulVec]
  calc
    u ⬝ᵥ (Uᵀ * M * U) *ᵥ v = u ⬝ᵥ Uᵀ *ᵥ (M *ᵥ (U *ᵥ v)) := by rw [hmul]
    _ = u ᵥ* Uᵀ ⬝ᵥ (M *ᵥ (U *ᵥ v)) := by rw [Matrix.dotProduct_mulVec]
    _ = (U *ᵥ u) ⬝ᵥ M *ᵥ (U *ᵥ v) := by rw [Matrix.vecMul_transpose]

lemma factor_mulVec (C : Matrix Y X ℝ) (Dinv : Matrix Y Y ℝ) (x : X → ℝ) (y : Y → ℝ) :
    blockH (1 : Matrix X X ℝ) (0 : Matrix X Y ℝ) (Dinv * C) 1 *ᵥ Sum.elim x y =
      Sum.elim x (y + Dinv *ᵥ (C *ᵥ x)) := by
  rw [block_mulVec]
  ext i
  cases i with
  | inl i => simp [Matrix.one_mulVec, Matrix.zero_mulVec]
  | inr i => simp [Matrix.one_mulVec, Matrix.mulVec_mulVec, add_comm, Pi.add_apply]

lemma dot_block_diag (S : Matrix X X ℝ) (D : Matrix Y Y ℝ)
    (x₁ : X → ℝ) (y₁ : Y → ℝ) (x₂ : X → ℝ) (y₂ : Y → ℝ) :
    Sum.elim x₁ y₁ ⬝ᵥ diagonalFactor S D *ᵥ Sum.elim x₂ y₂ =
      x₁ ⬝ᵥ S *ᵥ x₂ + y₁ ⬝ᵥ D *ᵥ y₂ := by
  rw [diagonalFactor, block_mulVec]
  simp [sumElim_dotProduct_sumElim, Matrix.zero_mulVec, add_zero, zero_add]

/-- Bilinear form of a symmetric block splits into the Schur form plus the shifted `D` form. -/
theorem symmetric_bilinear_form {A : Matrix X X ℝ} {B : Matrix X Y ℝ} {C : Matrix Y X ℝ}
    {D Dinv : Matrix Y Y ℝ} (hA : Aᵀ = A) (hD : Dᵀ = D) (hC : C = Bᵀ)
    (hInv : IsTwoSidedInverse D Dinv) (u v : (X ⊕ Y) → ℝ) :
    u ⬝ᵥ blockH A B C D *ᵥ v =
      (u ∘ Sum.inl) ⬝ᵥ schurComplement A B C Dinv *ᵥ (v ∘ Sum.inl) +
        ((u ∘ Sum.inr) + Dinv *ᵥ (C *ᵥ (u ∘ Sum.inl))) ⬝ᵥ
          D *ᵥ ((v ∘ Sum.inr) + Dinv *ᵥ (C *ᵥ (v ∘ Sum.inl))) := by
  obtain ⟨_, hcong⟩ := symmetric_block_congruence hA hD hC hInv
  rw [hcong, dot_congruence]
  have hBT : Bᵀ = C := hC.symm
  have hU : symmetricFactor B Dinv =
      blockH (1 : Matrix X X ℝ) (0 : Matrix X Y ℝ) (Dinv * C) 1 := by
    simp [symmetricFactor, hBT]
  have hu : symmetricFactor B Dinv *ᵥ u =
      Sum.elim (u ∘ Sum.inl) ((u ∘ Sum.inr) + Dinv *ᵥ (C *ᵥ (u ∘ Sum.inl))) := by
    rw [hU, ← sumElim_parts u]
    exact factor_mulVec C Dinv (u ∘ Sum.inl) (u ∘ Sum.inr)
  have hv : symmetricFactor B Dinv *ᵥ v =
      Sum.elim (v ∘ Sum.inl) ((v ∘ Sum.inr) + Dinv *ᵥ (C *ᵥ (v ∘ Sum.inl))) := by
    rw [hU, ← sumElim_parts v]
    exact factor_mulVec C Dinv (v ∘ Sum.inl) (v ∘ Sum.inr)
  rw [hu, hv, dot_block_diag]

/-- Forward direction: a joint kernel vector has auxiliary component `-D⁻¹ C x`. -/
theorem kernel_aux_eq {A : Matrix X X ℝ} {B : Matrix X Y ℝ} {C : Matrix Y X ℝ}
    {D Dinv : Matrix Y Y ℝ} (hInv : IsTwoSidedInverse D Dinv) {x : X → ℝ} {y : Y → ℝ}
    (hv : blockH A B C D *ᵥ Sum.elim x y = 0) :
    y = auxOf Dinv C x ∧ schurComplement A B C Dinv *ᵥ x = 0 := by
  have hblock : Sum.elim (A *ᵥ x + B *ᵥ y) (C *ᵥ x + D *ᵥ y) = 0 := by
    rw [← block_mulVec]
    exact hv
  have hX : A *ᵥ x + B *ᵥ y = 0 := by
    ext i
    simpa using congr_fun hblock (Sum.inl i)
  have hY : C *ᵥ x + D *ᵥ y = 0 := by
    ext i
    simpa using congr_fun hblock (Sum.inr i)
  have hy : y = auxOf Dinv C x := by
    have hDy : D *ᵥ y = -(C *ᵥ x) := by
      rw [add_comm] at hY
      exact eq_neg_of_add_eq_zero_left hY
    have hback : y = Dinv *ᵥ (D *ᵥ y) := by
      calc
        y = (1 : Matrix Y Y ℝ) *ᵥ y := by simp
        _ = (Dinv * D) *ᵥ y := by rw [hInv.1]
        _ = Dinv *ᵥ (D *ᵥ y) := by rw [← Matrix.mulVec_mulVec]
    calc
      y = Dinv *ᵥ (D *ᵥ y) := hback
      _ = Dinv *ᵥ (-(C *ᵥ x)) := by rw [hDy]
      _ = -(Dinv *ᵥ (C *ᵥ x)) := by rw [Matrix.mulVec_neg]
      _ = auxOf Dinv C x := rfl
  refine ⟨hy, ?_⟩
  have hBy : B *ᵥ y = -((B * Dinv * C) *ᵥ x) := by
    rw [hy, auxOf, Matrix.mulVec_neg, Matrix.mulVec_mulVec, Matrix.mulVec_mulVec]
  have hS : schurComplement A B C Dinv *ᵥ x = A *ᵥ x + B *ᵥ y := by
    rw [schurComplement, Matrix.sub_mulVec, hBy, sub_eq_add_neg]
  rw [hS, hX]

/-- Converse: a reduced kernel vector lifts by `y = -D⁻¹ C x`. -/
theorem reduced_joint_kernel {A : Matrix X X ℝ} {B : Matrix X Y ℝ} {C : Matrix Y X ℝ}
    {D Dinv : Matrix Y Y ℝ} (hInv : IsTwoSidedInverse D Dinv) {x : X → ℝ}
    (hx : schurComplement A B C Dinv *ᵥ x = 0) :
    blockH A B C D *ᵥ jointOf Dinv C x = 0 := by
  rw [jointOf, block_mulVec]
  ext i
  cases i with
  | inl i =>
    have hBy : B *ᵥ auxOf Dinv C x = -((B * Dinv * C) *ᵥ x) := by
      rw [auxOf, Matrix.mulVec_neg, Matrix.mulVec_mulVec, Matrix.mulVec_mulVec]
    have hS : A *ᵥ x + B *ᵥ auxOf Dinv C x = schurComplement A B C Dinv *ᵥ x := by
      rw [hBy, schurComplement, Matrix.sub_mulVec, ← sub_eq_add_neg]
    simp [hS, hx]
  | inr i =>
    have hDy : D *ᵥ auxOf Dinv C x = -(C *ᵥ x) := by
      rw [auxOf, Matrix.mulVec_neg, Matrix.mulVec_mulVec, hInv.2, Matrix.one_mulVec]
    have hsum : C *ᵥ x + D *ᵥ auxOf Dinv C x = 0 := by
      rw [hDy, add_neg_cancel]
    simp [hsum]

theorem jointOf_add (Dinv : Matrix Y Y ℝ) (C : Matrix Y X ℝ) (x₁ x₂ : X → ℝ) :
    jointOf Dinv C (x₁ + x₂) = jointOf Dinv C x₁ + jointOf Dinv C x₂ := by
  ext i
  cases i with
  | inl _ => simp [jointOf]
  | inr _ =>
    simp [jointOf, auxOf, Matrix.mulVec_add, Pi.neg_apply, Pi.add_apply]
    abel

theorem jointOf_smul (Dinv : Matrix Y Y ℝ) (C : Matrix Y X ℝ) (r : ℝ) (x : X → ℝ) :
    jointOf Dinv C (r • x) = r • jointOf Dinv C x := by
  ext i
  cases i with
  | inl _ => simp [jointOf]
  | inr _ => simp [jointOf, auxOf, Matrix.mulVec_smul, smul_neg]

def toJointKer {A : Matrix X X ℝ} {B : Matrix X Y ℝ} {C : Matrix Y X ℝ}
    {D Dinv : Matrix Y Y ℝ} (hInv : IsTwoSidedInverse D Dinv)
    (x : {x : X → ℝ // schurComplement A B C Dinv *ᵥ x = 0}) :
    {v : (X ⊕ Y) → ℝ // blockH A B C D *ᵥ v = 0} :=
  ⟨jointOf Dinv C x.1, reduced_joint_kernel hInv x.2⟩

def ofJointKer {A : Matrix X X ℝ} {B : Matrix X Y ℝ} {C : Matrix Y X ℝ}
    {D Dinv : Matrix Y Y ℝ} (hInv : IsTwoSidedInverse D Dinv)
    (v : {v : (X ⊕ Y) → ℝ // blockH A B C D *ᵥ v = 0}) :
    {x : X → ℝ // schurComplement A B C Dinv *ᵥ x = 0} :=
  ⟨v.1 ∘ Sum.inl, by
    have hv : blockH A B C D *ᵥ Sum.elim (v.1 ∘ Sum.inl) (v.1 ∘ Sum.inr) = 0 := by
      simpa [sumElim_parts] using v.2
    exact (kernel_aux_eq hInv hv).2⟩

/-- Explicit isomorphism `ker(A - B D⁻¹ C) ≃ ker H`. -/
def schurKernelEquiv {A : Matrix X X ℝ} {B : Matrix X Y ℝ} {C : Matrix Y X ℝ}
    {D Dinv : Matrix Y Y ℝ} (hInv : IsTwoSidedInverse D Dinv) :
    {x : X → ℝ // schurComplement A B C Dinv *ᵥ x = 0} ≃
      {v : (X ⊕ Y) → ℝ // blockH A B C D *ᵥ v = 0} where
  toFun := toJointKer hInv
  invFun := ofJointKer hInv
  left_inv x := by
    apply Subtype.ext
    simp [toJointKer, ofJointKer, jointOf]
  right_inv v := by
    apply Subtype.ext
    have hv : blockH A B C D *ᵥ Sum.elim (v.1 ∘ Sum.inl) (v.1 ∘ Sum.inr) = 0 := by
      simpa [sumElim_parts] using v.2
    have hy : v.1 ∘ Sum.inr = auxOf Dinv C (v.1 ∘ Sum.inl) := (kernel_aux_eq hInv hv).1
    simp only [toJointKer, ofJointKer, jointOf]
    rw [← hy]
    exact sumElim_parts v.1

theorem schurKernelEquiv_field {A : Matrix X X ℝ} {B : Matrix X Y ℝ} {C : Matrix Y X ℝ}
    {D Dinv : Matrix Y Y ℝ} (hInv : IsTwoSidedInverse D Dinv)
    (x : {x : X → ℝ // schurComplement A B C Dinv *ᵥ x = 0}) :
    (schurKernelEquiv hInv x).1 ∘ Sum.inl = x.1 := by
  simp [schurKernelEquiv, toJointKer, jointOf]

theorem schurKernelEquiv_aux {A : Matrix X X ℝ} {B : Matrix X Y ℝ} {C : Matrix Y X ℝ}
    {D Dinv : Matrix Y Y ℝ} (hInv : IsTwoSidedInverse D Dinv)
    (x : {x : X → ℝ // schurComplement A B C Dinv *ᵥ x = 0}) :
    (schurKernelEquiv hInv x).1 ∘ Sum.inr = auxOf Dinv C x.1 := by
  simp [schurKernelEquiv, toJointKer, jointOf]

theorem schurKernelEquiv_add {A : Matrix X X ℝ} {B : Matrix X Y ℝ} {C : Matrix Y X ℝ}
    {D Dinv : Matrix Y Y ℝ} (hInv : IsTwoSidedInverse D Dinv)
    (x₁ x₂ : {x : X → ℝ // schurComplement A B C Dinv *ᵥ x = 0}) :
    (schurKernelEquiv hInv ⟨x₁.1 + x₂.1, by
        rw [Matrix.mulVec_add, x₁.2, x₂.2, add_zero]⟩).1 =
      (schurKernelEquiv hInv x₁).1 + (schurKernelEquiv hInv x₂).1 := by
  simp [schurKernelEquiv, toJointKer, jointOf_add]

theorem schurKernelEquiv_smul {A : Matrix X X ℝ} {B : Matrix X Y ℝ} {C : Matrix Y X ℝ}
    {D Dinv : Matrix Y Y ℝ} (hInv : IsTwoSidedInverse D Dinv) (r : ℝ)
    (x : {x : X → ℝ // schurComplement A B C Dinv *ᵥ x = 0}) :
    (schurKernelEquiv hInv ⟨r • x.1, by rw [Matrix.mulVec_smul, x.2, smul_zero]⟩).1 =
      r • (schurKernelEquiv hInv x).1 := by
  simp [schurKernelEquiv, toJointKer, jointOf_smul]

lemma recoveredAux_zero_source (Dinv : Matrix Y Y ℝ) (C : Matrix Y X ℝ) (x : X → ℝ) :
    recoveredAux Dinv C 0 x = auxOf Dinv C x := by
  simp [recoveredAux, auxOf, zero_sub, Matrix.mulVec_neg]

/-- Inhomogeneous transfer. `g` enters the reduced source through `-B D⁻¹ g`. -/
theorem stationary_transfer {A : Matrix X X ℝ} {B : Matrix X Y ℝ} {C : Matrix Y X ℝ}
    {D Dinv : Matrix Y Y ℝ} (hInv : IsTwoSidedInverse D Dinv)
    {x : X → ℝ} {y : Y → ℝ} {f : X → ℝ} {g : Y → ℝ}
    (hEq : blockH A B C D *ᵥ Sum.elim x y = Sum.elim f g) :
    y = recoveredAux Dinv C g x ∧
      schurComplement A B C Dinv *ᵥ x = reducedSource B Dinv f g := by
  have hblock : Sum.elim (A *ᵥ x + B *ᵥ y) (C *ᵥ x + D *ᵥ y) = Sum.elim f g := by
    rw [← block_mulVec]
    exact hEq
  have hX : A *ᵥ x + B *ᵥ y = f := by
    ext i
    simpa using congr_fun hblock (Sum.inl i)
  have hY : C *ᵥ x + D *ᵥ y = g := by
    ext i
    simpa using congr_fun hblock (Sum.inr i)
  have hDy : D *ᵥ y = g - C *ᵥ x := by
    ext i
    have hi := congr_fun hY i
    simp only [Pi.add_apply] at hi
    rw [Pi.sub_apply, ← hi, add_comm, add_sub_cancel_right]
  have hy : y = recoveredAux Dinv C g x := by
    calc
      y = (1 : Matrix Y Y ℝ) *ᵥ y := by simp
      _ = (Dinv * D) *ᵥ y := by rw [hInv.1]
      _ = Dinv *ᵥ (D *ᵥ y) := by rw [← Matrix.mulVec_mulVec]
      _ = Dinv *ᵥ (g - C *ᵥ x) := by rw [hDy]
      _ = recoveredAux Dinv C g x := rfl
  refine ⟨hy, ?_⟩
  have hBg : B *ᵥ (Dinv *ᵥ g) + schurComplement A B C Dinv *ᵥ x = A *ᵥ x + B *ᵥ y := by
    have hRec : B *ᵥ y = B *ᵥ (Dinv *ᵥ g) - (B * Dinv * C) *ᵥ x := by
      rw [hy, recoveredAux, Matrix.mulVec_sub, ← Matrix.mulVec_mulVec, ← Matrix.mulVec_mulVec,
        Matrix.mulVec_sub]
    rw [hRec, schurComplement, Matrix.sub_mulVec]
    ext i
    simp only [Pi.add_apply, Pi.sub_apply]
    abel_nf
  have hRed : schurComplement A B C Dinv *ᵥ x = f - B *ᵥ (Dinv *ᵥ g) := by
    have hEqX : A *ᵥ x + B *ᵥ y = B *ᵥ (Dinv *ᵥ g) + schurComplement A B C Dinv *ᵥ x := by
      simpa [add_comm] using hBg.symm
    have : f = B *ᵥ (Dinv *ᵥ g) + schurComplement A B C Dinv *ᵥ x := by
      rw [← hX, hEqX]
    ext i
    have hi := congr_fun this i
    simp only [Pi.add_apply] at hi
    rw [Pi.sub_apply, hi, add_comm, add_sub_cancel_right]
  simpa [reducedSource] using hRed

/-- Converse inhomogeneous transfer. -/
theorem stationary_transfer_converse {A : Matrix X X ℝ} {B : Matrix X Y ℝ} {C : Matrix Y X ℝ}
    {D Dinv : Matrix Y Y ℝ} (hInv : IsTwoSidedInverse D Dinv)
    {x : X → ℝ} {y : Y → ℝ} {f : X → ℝ} {g : Y → ℝ}
    (hx : schurComplement A B C Dinv *ᵥ x = reducedSource B Dinv f g)
    (hy : y = recoveredAux Dinv C g x) :
    blockH A B C D *ᵥ Sum.elim x y = Sum.elim f g := by
  rw [block_mulVec]
  ext i
  cases i with
  | inl i =>
    have hRec : B *ᵥ y = B *ᵥ (Dinv *ᵥ g) - (B * Dinv * C) *ᵥ x := by
      rw [hy, recoveredAux, Matrix.mulVec_sub, ← Matrix.mulVec_mulVec, ← Matrix.mulVec_mulVec,
        Matrix.mulVec_sub]
    have hS : A *ᵥ x + B *ᵥ y = f := by
      have hx' : schurComplement A B C Dinv *ᵥ x = f - B *ᵥ (Dinv *ᵥ g) := by
        simpa [reducedSource] using hx
      rw [schurComplement, Matrix.sub_mulVec] at hx'
      rw [hRec]
      ext j
      have hj := congr_fun hx' j
      simp only [Pi.sub_apply] at hj
      simp only [Pi.add_apply, Pi.sub_apply]
      have hmove :
          (A *ᵥ x) j + ((B *ᵥ (Dinv *ᵥ g)) j - ((B * Dinv * C) *ᵥ x) j) =
            ((A *ᵥ x) j - ((B * Dinv * C) *ᵥ x) j) + (B *ᵥ (Dinv *ᵥ g)) j := by
        abel
      rw [hmove, hj, sub_add_cancel]
    simp [hS]
  | inr i =>
    have hY : C *ᵥ x + D *ᵥ y = g := by
      rw [hy, recoveredAux, Matrix.mulVec_sub, Matrix.mulVec_sub, Matrix.mulVec_mulVec,
        Matrix.mulVec_mulVec, hInv.2, Matrix.one_mulVec, Matrix.one_mulVec]
      ext j
      simp only [Pi.add_apply, Pi.sub_apply]
      abel_nf
    simp [hY]

/-- A nonzero kernel vector forbids a two-sided inverse. `H` itself need not be invertible. -/
theorem not_twoSidedInverse_of_kernel {n : Type*} [Fintype n] [DecidableEq n]
    {M : Matrix n n ℝ} {v : n → ℝ} (hv : M *ᵥ v = 0) (hv0 : v ≠ 0) :
    ¬ ∃ Minv : Matrix n n ℝ, IsTwoSidedInverse M Minv := by
  rintro ⟨Minv, hM⟩
  have : v = 0 := by
    calc
      v = (1 : Matrix n n ℝ) *ᵥ v := by simp
      _ = (Minv * M) *ᵥ v := by rw [← hM.1]
      _ = Minv *ᵥ (M *ᵥ v) := by rw [← Matrix.mulVec_mulVec]
      _ = Minv *ᵥ 0 := by rw [hv]
      _ = 0 := by simp
  exact hv0 this

/-- Coordinate `ℓ¹` norm. -/
def l1 {I : Type*} [Fintype I] (v : I → ℝ) : ℝ :=
  ∑ i, |v i|

lemma l1_neg {I : Type*} [Fintype I] (v : I → ℝ) : l1 (-v) = l1 v := by
  simp [l1, Pi.neg_apply, abs_neg]

/-- Supplied operator bound. The constant is not derived from a log-det estimate. -/
def HasL1Bound {I J : Type*} [Fintype I] [Fintype J] (M : Matrix I J ℝ) (K : ℝ) : Prop :=
  ∀ x, l1 (M *ᵥ x) ≤ K * l1 x

/-- Reconstruction norm of `-D⁻¹ C x` from a supplied bound on `D⁻¹`. -/
theorem aux_reconstruction_l1 {Dinv : Matrix Y Y ℝ} {C : Matrix Y X ℝ} {K : ℝ}
    (hK : HasL1Bound Dinv K) (x : X → ℝ) :
    l1 (auxOf Dinv C x) ≤ K * l1 (C *ᵥ x) := by
  rw [auxOf, l1_neg]
  exact hK (C *ᵥ x)

theorem recovered_aux_l1 {Dinv : Matrix Y Y ℝ} {C : Matrix Y X ℝ} {K : ℝ}
    (hK : HasL1Bound Dinv K) (g : Y → ℝ) (x : X → ℝ) :
    l1 (recoveredAux Dinv C g x) ≤ K * l1 (g - C *ᵥ x) :=
  hK _

theorem kernel_aux_l1 {A : Matrix X X ℝ} {B : Matrix X Y ℝ} {C : Matrix Y X ℝ}
    {D Dinv : Matrix Y Y ℝ} (hInv : IsTwoSidedInverse D Dinv) {K : ℝ}
    (hK : HasL1Bound Dinv K) {x : X → ℝ} (hx : schurComplement A B C Dinv *ᵥ x = 0) :
    l1 ((schurKernelEquiv hInv ⟨x, hx⟩).1 ∘ Sum.inr) ≤ K * l1 (C *ᵥ x) := by
  rw [schurKernelEquiv_aux]
  exact aux_reconstruction_l1 hK x

/-- Matrix data of the extended stationary block. Invertibility of `Hy` is a hypothesis. -/
structure UnfoldingBlocks (X Y : Type*) [Fintype X] [Fintype Y] [DecidableEq X] [DecidableEq Y] where
  Lxx : Matrix X X ℝ
  Lxy : Matrix X Y ℝ
  Lyx : Matrix Y X ℝ
  Hy : Matrix Y Y ℝ
  HyInv : Matrix Y Y ℝ
  hyInv : IsTwoSidedInverse Hy HyInv

namespace UnfoldingBlocks

variable {X Y : Type*} [Fintype X] [Fintype Y] [DecidableEq X] [DecidableEq Y]

def operator (P : UnfoldingBlocks X Y) : Matrix (X ⊕ Y) (X ⊕ Y) ℝ :=
  blockH P.Lxx P.Lxy P.Lyx P.Hy

def reduced (P : UnfoldingBlocks X Y) : Matrix X X ℝ :=
  schurComplement P.Lxx P.Lxy P.Lyx P.HyInv

def kernelEquiv (P : UnfoldingBlocks X Y) :
    {x : X → ℝ // P.reduced *ᵥ x = 0} ≃ {v : (X ⊕ Y) → ℝ // P.operator *ᵥ v = 0} :=
  schurKernelEquiv P.hyInv

end UnfoldingBlocks

/-- Specialization of the transfer to the unfolding block. No log-det axiom is used. -/
theorem unfolding_reduced_equation (P : UnfoldingBlocks X Y)
    {x : X → ℝ} {y : Y → ℝ} {fx : X → ℝ} {fy : Y → ℝ}
    (hEq : P.operator *ᵥ Sum.elim x y = Sum.elim fx fy) :
    y = recoveredAux P.HyInv P.Lyx fy x ∧
      P.reduced *ᵥ x = reducedSource P.Lxy P.HyInv fx fy :=
  stationary_transfer P.hyInv hEq

theorem unfolding_reduced_equation_converse (P : UnfoldingBlocks X Y)
    {x : X → ℝ} {y : Y → ℝ} {fx : X → ℝ} {fy : Y → ℝ}
    (hx : P.reduced *ᵥ x = reducedSource P.Lxy P.HyInv fx fy)
    (hy : y = recoveredAux P.HyInv P.Lyx fy x) :
    P.operator *ᵥ Sum.elim x y = Sum.elim fx fy :=
  stationary_transfer_converse P.hyInv hx hy

/-- Retained shell saddle `[[H_red, T*], [T, 0]]`. The lower-right block is zero. -/
def shellSaddle (Hred : Matrix X X ℝ) (Tstar : Matrix X Y ℝ) (T : Matrix Y X ℝ) :
    Matrix (X ⊕ Y) (X ⊕ Y) ℝ :=
  blockH Hred Tstar T (0 : Matrix Y Y ℝ)

@[simp]
lemma lowerRight_shellSaddle (Hred : Matrix X X ℝ) (Tstar : Matrix X Y ℝ) (T : Matrix Y X ℝ) :
    lowerRight (shellSaddle Hred Tstar T) = 0 := by
  simp [shellSaddle]

lemma matrix_zero_ne_one [Nonempty Y] : (0 : Matrix Y Y ℝ) ≠ 1 := by
  intro h
  obtain ⟨j⟩ := ‹Nonempty Y›
  have hjj := congr_fun (congr_fun h j) j
  rw [Matrix.zero_apply, Matrix.one_apply_eq] at hjj
  exact zero_ne_one hjj

/-- The zero lower block admits no two-sided inverse. -/
theorem zero_block_not_twoSidedInverse [Nonempty Y] (Dinv : Matrix Y Y ℝ) :
    ¬ IsTwoSidedInverse (0 : Matrix Y Y ℝ) Dinv := by
  intro hInv
  have hZero : Dinv * (0 : Matrix Y Y ℝ) = 0 := Matrix.mul_zero Dinv
  have hOne : Dinv * (0 : Matrix Y Y ℝ) = 1 := hInv.1
  exact matrix_zero_ne_one (hZero.symm.trans hOne)

/-- A joint shell vector constrains the field row. It does not invert the zero block. -/
theorem saddle_constraint_without_inverse {Hred : Matrix X X ℝ} {Tstar : Matrix X Y ℝ}
    {T : Matrix Y X ℝ} (hAdj : Tstar = Tᵀ) {v : X → ℝ} {S : Y → ℝ}
    (h0 : shellSaddle Hred Tstar T *ᵥ Sum.elim v S = 0) :
    T *ᵥ v = 0 ∧ ∀ w : X → ℝ, T *ᵥ w = 0 → w ⬝ᵥ Hred *ᵥ v = 0 := by
  have hblock :
      Sum.elim (Hred *ᵥ v + Tstar *ᵥ S) (T *ᵥ v + (0 : Matrix Y Y ℝ) *ᵥ S) = 0 := by
    rw [← block_mulVec]
    simpa [shellSaddle] using h0
  have hField : Hred *ᵥ v + Tstar *ᵥ S = 0 := by
    ext i
    simpa using congr_fun hblock (Sum.inl i)
  have hShell : T *ᵥ v = 0 := by
    ext i
    simpa [Matrix.zero_mulVec] using congr_fun hblock (Sum.inr i)
  refine ⟨hShell, ?_⟩
  intro w hw
  have hsolve : Hred *ᵥ v = -(Tstar *ᵥ S) := eq_neg_of_add_eq_zero_left hField
  rw [hsolve, hAdj, dotProduct_neg, neg_eq_zero, Matrix.dotProduct_mulVec,
    Matrix.vecMul_transpose, hw, zero_dotProduct]

/-! ## Finite controls -/

/-- Constant one on `Fin 1`. -/
def oneVec : Fin 1 → ℝ := fun _ => 1

/-- `1 × 1` identity. -/
def eye1 : Matrix (Fin 1) (Fin 1) ℝ := 1

/-- `1 × 1` zero matrix. -/
def zero1 : Matrix (Fin 1) (Fin 1) ℝ := 0

lemma oneVec_ne_zero : oneVec ≠ 0 := by
  intro h
  have := congr_fun h 0
  simp [oneVec] at this

/-- Shell vector `(0, 1)` on `Fin 1 ⊕ Fin 1`. -/
def shellVec1 : (Fin 1 ⊕ Fin 1) → ℝ :=
  Sum.elim 0 oneVec

/-- `D = 0` is not a pivot: every candidate inverse misses a real kernel vector. -/
theorem every_candidate_inverse_misses_kernel (Dinv : Matrix (Fin 1) (Fin 1) ℝ) :
    ¬ IsTwoSidedInverse zero1 Dinv ∧
      auxOf Dinv zero1 (0 : Fin 1 → ℝ) = 0 ∧
      jointOf Dinv zero1 (0 : Fin 1 → ℝ) = 0 ∧
      blockH eye1 zero1 zero1 zero1 *ᵥ shellVec1 = 0 ∧
      shellVec1 ≠ 0 ∧
      shellVec1 ≠ jointOf Dinv zero1 (shellVec1 ∘ Sum.inl) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · simpa [zero1] using zero_block_not_twoSidedInverse (Y := Fin 1) Dinv
  · simp [auxOf, zero1, Matrix.zero_mulVec]
  · simp [jointOf, auxOf, zero1, Matrix.zero_mulVec]
  · rw [shellVec1, block_mulVec]
    simp [eye1, zero1, Matrix.zero_mulVec, Matrix.one_mulVec]
  · intro h
    have := congr_fun h (Sum.inr 0)
    simp [shellVec1, oneVec] at this
  · intro h
    have hv : shellVec1 ∘ Sum.inl = 0 := by
      ext i
      fin_cases i
      simp [shellVec1]
    rw [hv] at h
    have h0 : jointOf Dinv zero1 (0 : Fin 1 → ℝ) = 0 := by
      simp [jointOf, auxOf, zero1, Matrix.zero_mulVec]
    rw [h0] at h
    have := congr_fun h (Sum.inr 0)
    simp [shellVec1, oneVec] at this

/-- Invertible auxiliary block, singular reduced block, nonzero joint kernel. -/
theorem nonzero_reduced_kernel :
    IsTwoSidedInverse eye1 eye1 ∧
      schurComplement zero1 zero1 zero1 eye1 *ᵥ oneVec = 0 ∧
      oneVec ≠ 0 ∧
      blockH zero1 zero1 zero1 eye1 *ᵥ jointOf eye1 zero1 oneVec = 0 ∧
      ¬ ∃ Hinv : Matrix (Fin 1 ⊕ Fin 1) (Fin 1 ⊕ Fin 1) ℝ,
          IsTwoSidedInverse (blockH zero1 zero1 zero1 eye1) Hinv := by
  have hInv : IsTwoSidedInverse eye1 eye1 := by simp [IsTwoSidedInverse, eye1]
  have hS : schurComplement zero1 zero1 zero1 eye1 = 0 := by
    simp [schurComplement, zero1, eye1, Matrix.mul_zero, sub_zero]
  have hx : schurComplement zero1 zero1 zero1 eye1 *ᵥ oneVec = 0 := by simp [hS]
  have hjoint :=
    reduced_joint_kernel (A := zero1) (B := zero1) (C := zero1) (D := eye1) hInv hx
  have hvec : jointOf eye1 zero1 oneVec ≠ 0 := by
    intro h
    have := congr_fun h (Sum.inl 0)
    simp [jointOf, oneVec] at this
  refine ⟨hInv, hx, oneVec_ne_zero, hjoint, ?_⟩
  exact not_twoSidedInverse_of_kernel hjoint hvec

/-- The sign in `A - B D⁻¹ C` is sharp: the opposite sign fails the same vector. -/
theorem flipped_schur_sign_fails :
    IsTwoSidedInverse eye1 eye1 ∧
      schurComplement eye1 eye1 eye1 eye1 *ᵥ oneVec = 0 ∧
      (eye1 + eye1 * eye1 * eye1) *ᵥ oneVec ≠ 0 ∧
      blockH eye1 eye1 eye1 eye1 *ᵥ jointOf eye1 eye1 oneVec = 0 ∧
      blockH eye1 eye1 eye1 eye1 *ᵥ Sum.elim oneVec (eye1 *ᵥ (eye1 *ᵥ oneVec)) ≠ 0 := by
  have hInv : IsTwoSidedInverse eye1 eye1 := by simp [IsTwoSidedInverse, eye1]
  have hS : schurComplement eye1 eye1 eye1 eye1 = 0 := by
    ext i j
    fin_cases i
    fin_cases j
    simp [schurComplement, eye1, Matrix.mul_one, sub_self]
  have hx : schurComplement eye1 eye1 eye1 eye1 *ᵥ oneVec = 0 := by simp [hS]
  have hjoint :=
    reduced_joint_kernel (A := eye1) (B := eye1) (C := eye1) (D := eye1) hInv hx
  have hWrong : (eye1 + eye1 * eye1 * eye1) *ᵥ oneVec ≠ 0 := by
    have hMat : eye1 + eye1 * eye1 * eye1 = (1 : Matrix (Fin 1) (Fin 1) ℝ) + 1 := by
      simp [eye1, Matrix.mul_one]
    rw [hMat]
    intro h
    have := congr_fun h 0
    simp [oneVec, Matrix.add_mulVec, Matrix.one_mulVec, Pi.add_apply] at this
    norm_num at this
  have hFlipVal :
      (blockH eye1 eye1 eye1 eye1 *ᵥ Sum.elim oneVec (eye1 *ᵥ (eye1 *ᵥ oneVec))) (Sum.inl 0) = 2 := by
    rw [block_mulVec]
    simp [eye1, oneVec, Sum.elim_inl, Matrix.one_mulVec, Matrix.mulVec_mulVec, Pi.add_apply]
    norm_num
  have hFlip : blockH eye1 eye1 eye1 eye1 *ᵥ Sum.elim oneVec (eye1 *ᵥ (eye1 *ᵥ oneVec)) ≠ 0 := by
    intro h
    have := congr_fun h (Sum.inl 0)
    rw [hFlipVal] at this
    norm_num at this
  exact ⟨hInv, hx, hWrong, hjoint, hFlip⟩

/-- Dropping the auxiliary source changes the reduced right-hand side. -/
theorem direct_auxiliary_source_not_dropped :
    IsTwoSidedInverse eye1 eye1 ∧
      oneVec = recoveredAux eye1 zero1 oneVec (0 : Fin 1 → ℝ) ∧
      schurComplement zero1 eye1 zero1 eye1 *ᵥ (0 : Fin 1 → ℝ) =
        reducedSource eye1 eye1 oneVec oneVec ∧
      blockH zero1 eye1 zero1 eye1 *ᵥ Sum.elim (0 : Fin 1 → ℝ) oneVec =
        Sum.elim oneVec oneVec ∧
      reducedSource eye1 eye1 oneVec oneVec ≠ oneVec ∧
      schurComplement zero1 eye1 zero1 eye1 *ᵥ (0 : Fin 1 → ℝ) ≠ oneVec := by
  have hInv : IsTwoSidedInverse eye1 eye1 := by simp [IsTwoSidedInverse, eye1]
  have hy : oneVec = recoveredAux eye1 zero1 oneVec (0 : Fin 1 → ℝ) := by
    ext i
    fin_cases i
    simp [recoveredAux, eye1, zero1, oneVec, Matrix.one_mulVec, sub_zero]
  have hS : schurComplement zero1 eye1 zero1 eye1 = 0 := by
    simp [schurComplement, zero1, eye1, Matrix.mul_zero, sub_zero]
  have hRed : reducedSource eye1 eye1 oneVec oneVec = 0 := by
    ext i
    fin_cases i
    simp [reducedSource, eye1, oneVec, Matrix.one_mulVec, Pi.sub_apply]
  have hx : schurComplement zero1 eye1 zero1 eye1 *ᵥ (0 : Fin 1 → ℝ) =
      reducedSource eye1 eye1 oneVec oneVec := by
    simp [hS, hRed]
  have hEq :=
    stationary_transfer_converse (A := zero1) (B := eye1) (C := zero1) (D := eye1) hInv hx hy
  have hNe : reducedSource eye1 eye1 oneVec oneVec ≠ oneVec := by
    intro h
    have := congr_fun h 0
    simp [hRed, oneVec] at this
  refine ⟨hInv, hy, hx, hEq, hNe, ?_⟩
  rw [hx]
  exact hNe

/-- Nonzero shell direction of `[[1, 0], [0, 0]]`. The zero block is not eliminated. -/
theorem retained_shell_not_eliminated (Dinv : Matrix (Fin 1) (Fin 1) ℝ) :
    lowerRight (shellSaddle eye1 zero1 zero1) = 0 ∧
      ¬ IsTwoSidedInverse (lowerRight (shellSaddle eye1 zero1 zero1)) Dinv ∧
      shellSaddle eye1 zero1 zero1 *ᵥ shellVec1 = 0 ∧
      shellVec1 ∘ Sum.inr ≠ 0 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · simp [eye1, zero1]
  · simpa [eye1, zero1] using zero_block_not_twoSidedInverse (Y := Fin 1) Dinv
  · rw [shellSaddle, shellVec1, block_mulVec]
    simp [eye1, zero1, Matrix.zero_mulVec, Matrix.one_mulVec]
  · intro h
    have := congr_fun h 0
    simp [shellVec1, oneVec] at this

/-- `ker H_red` is not the saddle kernel, and the zero block still has no inverse. -/
theorem hred_kernel_is_not_saddle_kernel (Dinv : Matrix (Fin 1) (Fin 1) ℝ) :
    lowerRight (shellSaddle zero1 eye1 eye1) = 0 ∧
      ¬ IsTwoSidedInverse (lowerRight (shellSaddle zero1 eye1 eye1)) Dinv ∧
      zero1 *ᵥ oneVec = 0 ∧
      shellSaddle zero1 eye1 eye1 *ᵥ Sum.elim oneVec (0 : Fin 1 → ℝ) ≠ 0 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · simp [zero1, eye1]
  · simpa [zero1, eye1] using zero_block_not_twoSidedInverse (Y := Fin 1) Dinv
  · simp [zero1]
  · rw [shellSaddle, block_mulVec]
    intro h
    have := congr_fun h (Sum.inr 0)
    simp [zero1, eye1, oneVec, Matrix.one_mulVec, Matrix.zero_mulVec] at this

#check schurKernelEquiv
#check kernel_aux_eq
#check reduced_joint_kernel
#check stationary_transfer
#check stationary_transfer_converse
#check block_factorization
#check symmetric_block_congruence
#check symmetric_bilinear_form
#check aux_reconstruction_l1
#check unfolding_reduced_equation
#check every_candidate_inverse_misses_kernel
#check nonzero_reduced_kernel
#check flipped_schur_sign_fails
#check retained_shell_not_eliminated
#check hred_kernel_is_not_saddle_kernel
#check saddle_constraint_without_inverse

#print axioms schurKernelEquiv
#print axioms kernel_aux_eq
#print axioms reduced_joint_kernel
#print axioms stationary_transfer
#print axioms stationary_transfer_converse
#print axioms block_factorization
#print axioms symmetric_block_congruence
#print axioms symmetric_bilinear_form
#print axioms aux_reconstruction_l1
#print axioms unfolding_reduced_equation
#print axioms every_candidate_inverse_misses_kernel
#print axioms nonzero_reduced_kernel
#print axioms flipped_schur_sign_fails
#print axioms direct_auxiliary_source_not_dropped
#print axioms retained_shell_not_eliminated
#print axioms hred_kernel_is_not_saddle_kernel
#print axioms saddle_constraint_without_inverse

end D0.Research.SchurStationaryTransfer
